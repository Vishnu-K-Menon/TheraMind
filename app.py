import chainlit as cl
from unsloth import FastLanguageModel
import torch
import chromadb

# --- 1. Load Model & Database ---
print("Loading DPO-Aligned Model...")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="VKM47/TheraMind-DPO-Adapters",
    max_seq_length=4096,
    dtype=None,
    load_in_4bit=True,
)
FastLanguageModel.for_inference(model)

print("Loading Vector Database...")
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(name="clinical_guidelines")


# --- 2. Initialize Chat Session ---
@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("history", [])
    
    welcome_msg = """
# 🏥 TheraMind
### *Dual-Mode Clinical AI Assistant*
***
Welcome to the patient portal. I am designed to evaluate your case using strict, retrieval-augmented clinical guidelines.

**How to use this agent:**
* **Patient Portal:** Describe your symptoms in the chat below, and I will conduct a triage interview.
* **Doctor Mode:** You will see a **'Generate SOAP note'** button attached to my responses. Click it at any time to instantly synthesize our active conversation into formal medical documentation.

> ⚠️ *Disclaimer: This is an AI. I am not a licensed healthcare provider. Do not use this for actual medical emergencies.*
"""
    
    await cl.Message(content=welcome_msg).send()


# --- 3. Main Chat Loop (Patient Mode) ---
@cl.on_message
async def on_message(message: cl.Message):
    msg = cl.Message(content="")
    await msg.send()
    
    history = cl.user_session.get("history")
    user_query = message.content
    history.append({"role": "user", "content": user_query})
    
    results = collection.query(query_texts=[user_query], n_results=1)
    
    retrieved_context = ""
    if results['documents'] and results['documents'][0]:
        retrieved_context = results['documents'][0][0]
        
    dynamic_system_prompt = f"""You are an empathetic, professional AI medical assistant. You will chat with the patient to understand their symptoms. 

---
MEDICAL TEXTBOOK REFERENCE (THIS IS NOT THE PATIENT'S MEDICAL HISTORY):
{retrieved_context}
---

CRITICAL PATIENT INTAKE GUARDRAILS:
1. You have absolutely no prior knowledge of the patient. Do NOT assume, invent, or guess their age, gender, or medical history based on the textbook reference.
2. If the user only provides a generic greeting (e.g., "hi", "hello"), you must respond ONLY with a polite greeting and ask how you can help them today. Do NOT mention any symptoms or reference the medical text yet.
3. YOU ARE A VIRTUAL CHATBOT. You CANNOT perform physical examinations, touch the patient, check vital signs, or run lab tests. NEVER pretend to physically examine the patient. If you need physical data (like a temperature), you must ask the patient if they have taken it themselves.

CLINICAL RAG & SAFETY INSTRUCTIONS:
4. EVALUATE CONTEXT: First, evaluate if the textbook excerpt matches the patient's current symptoms and demographic (e.g., age).
5. IF IT MATCHES: Adhere strictly to the guidelines. If the patient describes "red flag" symptoms mentioned in the text, follow the emergency/referral instructions immediately.
6. IF DEMOGRAPHIC MISMATCH (e.g., the guideline is for adults but the patient is a baby): YOU MUST REFUSE TO GIVE DOSAGES OR TREATMENTS. State clearly that you are an AI and cannot safely advise on this demographic.
7. IF SYMPTOMS DO NOT MATCH THE EXCERPT: Ignore the excerpt. You may rely on your general medical training to assist the patient safely. Provide a brief, natural disclaimer that you are an AI, and then give safe, conservative advice. If symptoms are life-threatening (like a heart attack), advise immediate emergency care without explicitly diagnosing them."""
    messages = [{"role": "system", "content": dynamic_system_prompt}] + history
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer([text], return_tensors="pt").to("cuda")
    
    outputs = model.generate(**inputs, max_new_tokens=512, use_cache=True, temperature=0.3)
    response = tokenizer.batch_decode(outputs[:, inputs["input_ids"].shape[1]:], skip_special_tokens=True)[0]
    
    history.append({"role": "assistant", "content": response})
    cl.user_session.set("history", history)
    
    # Attach the button to the bottom of the AI's response!
    msg.content = response
    msg.actions = [
        cl.Action(name="generate_soap", payload={"action": "generate"}, description="Click to generate SOAP note")
    ]
    await msg.update()


# --- 4. Doctor Mode (Action Callback) ---
@cl.action_callback("generate_soap")
async def on_action(action: cl.Action):
    # Instantly remove the clicked button so it doesn't clutter the chat
    await action.remove()
    
    history = cl.user_session.get("history")
    
    if not history:
        await cl.Message(content="⚠️ No patient conversation history available to summarize yet.").send()
        return
        
    msg = cl.Message(content="*Synthesizing clinical documentation...*")
    await msg.send()
    
    full_conversation = " ".join([m["content"] for m in history if m["role"] == "user"])
    results = collection.query(query_texts=[full_conversation], n_results=1)
    
    retrieved_context = ""
    if results['documents'] and results['documents'][0]:
        retrieved_context = results['documents'][0][0]
        
    soap_prompt = f"""You are a professional medical scribe. Output a highly structured SOAP note based ONLY on the conversation history. 

---
MEDICAL TEXTBOOK REFERENCE:
{retrieved_context}
---"""

    messages = [{"role": "system", "content": soap_prompt}] + history
    messages.append({"role": "user", "content": "Generate clinical documentation."})
    
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer([text], return_tensors="pt").to("cuda")
    
    outputs = model.generate(**inputs, max_new_tokens=512, use_cache=True, temperature=0.1)
    response = tokenizer.batch_decode(outputs[:, inputs["input_ids"].shape[1]:], skip_special_tokens=True)[0]
    
    msg.content = f"### 🩺 Official SOAP Note\n\n{response}"
    await msg.update()