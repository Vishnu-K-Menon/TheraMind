"""
TheraMind - FastAPI Backend Server
Dual-Mode Clinical AI Assistant with RAG-augmented inference.
Uses HuggingFace Transformers + PEFT for Llama 3.2 inference.
"""

import torch
import chromadb
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel


# ──────────────────────────────────────────────────────────────
# 1. Initialize FastAPI App
# ──────────────────────────────────────────────────────────────

app = FastAPI(
    title="TheraMind API",
    description="Dual-Mode Clinical AI Assistant with RAG-augmented inference",
    version="1.0.0",
)

# Mount static directory to serve custom UI
app.mount("/static", StaticFiles(directory="static"), name="static")


# ──────────────────────────────────────────────────────────────
# 2. Load Model & Database at Startup
# ──────────────────────────────────────────────────────────────

BASE_MODEL_NAME = "meta-llama/Llama-3.2-3B-Instruct"
ADAPTER_NAME = "VKM47/TheraMind-DPO-Adapters"

print("Loading DPO-Aligned Model with PEFT adapters...")

# Configure 4-bit quantization
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_NAME)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Load base model with quantization
base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL_NAME,
    quantization_config=bnb_config,
    device_map="auto",
    torch_dtype=torch.float16,
)

# Load fine-tuned PEFT adapters on top of the base model
model = PeftModel.from_pretrained(base_model, ADAPTER_NAME)
model.eval()

print("Model loaded successfully.")

# Load ChromaDB vector database for RAG
print("Loading Vector Database...")
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(name="clinical_guidelines")
print("Vector database loaded successfully.")


# ──────────────────────────────────────────────────────────────
# 3. Pydantic Request/Response Models
# ──────────────────────────────────────────────────────────────

class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[ChatMessage] = []


class SOAPRequest(BaseModel):
    history: list[ChatMessage] = []


class ChatResponse(BaseModel):
    response: str


class SOAPResponse(BaseModel):
    soap_note: str


# ──────────────────────────────────────────────────────────────
# 4. Inference Helper
# ──────────────────────────────────────────────────────────────

def generate_response(messages: list[dict], max_new_tokens: int = 512, temperature: float = 0.3) -> str:
    """Run inference through the PEFT-adapted Llama model."""
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer([text], return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            use_cache=True,
            temperature=temperature,
            do_sample=temperature > 0,
        )

    response = tokenizer.batch_decode(
        outputs[:, inputs["input_ids"].shape[1]:],
        skip_special_tokens=True,
    )[0]

    return response.strip()


# ──────────────────────────────────────────────────────────────
# 5. System Prompts
# ──────────────────────────────────────────────────────────────

PATIENT_SYSTEM_PROMPT_TEMPLATE = """You are an empathetic, professional AI medical assistant. You will chat with the patient to understand their symptoms. 

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

SOAP_SYSTEM_PROMPT_TEMPLATE = """You are a professional medical scribe. Output a highly structured SOAP note based ONLY on the conversation history. 

---
MEDICAL TEXTBOOK REFERENCE:
{retrieved_context}
---"""


# ──────────────────────────────────────────────────────────────
# 6. Routes - HTML Pages
# ──────────────────────────────────────────────────────────────

@app.get("/")
async def serve_index():
    """Serve the Patient Mode UI."""
    return FileResponse("static/index.html")


@app.get("/doctor-mode")
async def serve_doctor():
    """Serve the Doctor Mode UI."""
    return FileResponse("static/doctor.html")


# ──────────────────────────────────────────────────────────────
# 7. Routes - API Endpoints
# ──────────────────────────────────────────────────────────────

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Patient Mode chat endpoint.
    Accepts a message and conversation history, performs RAG lookup,
    and returns the AI assistant's response.
    """
    user_query = request.message

    # Convert history to dict format for the model
    history_dicts = [{"role": msg.role, "content": msg.content} for msg in request.history]

    # RAG: Retrieve relevant clinical guidelines
    results = collection.query(query_texts=[user_query], n_results=1)

    retrieved_context = ""
    if results["documents"] and results["documents"][0]:
        retrieved_context = results["documents"][0][0]

    # Build the message list with system prompt
    system_prompt = PATIENT_SYSTEM_PROMPT_TEMPLATE.format(retrieved_context=retrieved_context)
    messages = [{"role": "system", "content": system_prompt}] + history_dicts

    # Generate response
    response = generate_response(messages, max_new_tokens=512, temperature=0.3)

    return ChatResponse(response=response)


@app.post("/generate_soap", response_model=SOAPResponse)
async def generate_soap(request: SOAPRequest):
    """
    Doctor Mode SOAP note generation endpoint.
    Accepts conversation history, performs RAG lookup,
    and returns a structured SOAP note.
    """
    # Convert history to dict format
    history_dicts = [{"role": msg.role, "content": msg.content} for msg in request.history]

    if not history_dicts:
        return SOAPResponse(soap_note="⚠️ No patient conversation history available to summarize yet.")

    # RAG: Retrieve relevant clinical guidelines using full patient conversation
    full_conversation = " ".join([m["content"] for m in history_dicts if m["role"] == "user"])
    results = collection.query(query_texts=[full_conversation], n_results=1)

    retrieved_context = ""
    if results["documents"] and results["documents"][0]:
        retrieved_context = results["documents"][0][0]

    # Build the message list with SOAP system prompt
    system_prompt = SOAP_SYSTEM_PROMPT_TEMPLATE.format(retrieved_context=retrieved_context)
    messages = [{"role": "system", "content": system_prompt}] + history_dicts
    messages.append({"role": "user", "content": "Generate clinical documentation."})

    # Generate SOAP note with lower temperature for precision
    response = generate_response(messages, max_new_tokens=512, temperature=0.1)

    return SOAPResponse(soap_note=response)


# ──────────────────────────────────────────────────────────────
# 8. Development Server Entry Point
# ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fastapi_app:app", host="0.0.0.0", port=8000, reload=False)