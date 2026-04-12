---
quick_id: 260412-qnw
description: "Backend Refactor - Convert to FastAPI and Replace Unsloth with PEFT"
mode: quick-full
must_haves:
  truths:
    - "FastAPI instance initialized as `app = FastAPI()`"
    - "Static directory mounted via `app.mount('/static', StaticFiles(directory='static'), name='static')`"
    - "The word 'unsloth' does NOT appear anywhere in the generated code"
    - "No chainlit imports or references exist in the generated code"
    - "Standard HuggingFace `transformers` (`AutoModelForCausalLM`, `AutoTokenizer`, `BitsAndBytesConfig`) used for model loading"
    - "`peft` library (`PeftModel`) used to load fine-tuned adapters"
    - "Base model is `meta-llama/Llama-3.2-3B-Instruct` with 4-bit quantization and `device_map='auto'`"
    - "Adapters loaded from `VKM47/TheraMind-DPO-Adapters`"
    - "POST /chat endpoint returns JSON `{response: string}`"
    - "POST /generate_soap endpoint returns JSON `{soap_note: string}`"
    - "GET / returns static/index.html"
    - "GET /doctor-mode returns static/doctor.html"
    - "ChromaDB RAG logic preserved"
  artifacts:
    - "fastapi_app.py"
  key_links:
    - "static/index.html - Patient Mode frontend (expects `{response: ...}`)"
    - "static/doctor.html - Doctor Mode frontend (expects `{soap_note: ...}` or `{response: ...}`)"
---

# Quick Plan: Backend Refactor - Convert to FastAPI and Replace Unsloth with PEFT

## Task 1: Rewrite fastapi_app.py as production FastAPI server

**files:** `fastapi_app.py`
**action:**
1. Rewrite the entire `fastapi_app.py` to replace Chainlit + Unsloth with FastAPI + HuggingFace transformers + PEFT
2. Structure:
   a. **Imports:** FastAPI, Pydantic, transformers (AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig), peft (PeftModel), torch, chromadb, StaticFiles, FileResponse
   b. **FastAPI init:** `app = FastAPI(title="TheraMind API")`
   c. **Static mount:** `app.mount("/static", StaticFiles(directory="static"), name="static")`
   d. **Model loading:** 
      - BitsAndBytesConfig with `load_in_4bit=True`, `bnb_4bit_compute_dtype=torch.float16`
      - AutoTokenizer from `meta-llama/Llama-3.2-3B-Instruct`
      - AutoModelForCausalLM from `meta-llama/Llama-3.2-3B-Instruct` with quantization config + `device_map="auto"`
      - PeftModel.from_pretrained wrapping the base model with `VKM47/TheraMind-DPO-Adapters`
   e. **ChromaDB:** Same PersistentClient + collection as before
   f. **Pydantic models:** `ChatRequest(message: str, history: list)`, `SOAPRequest(history: list)`
   g. **GET /:** Return `FileResponse("static/index.html")`
   h. **GET /doctor-mode:** Return `FileResponse("static/doctor.html")`
   i. **POST /chat:** Accept ChatRequest, perform RAG lookup, build system prompt, generate response, return `{"response": "..."}`
   j. **POST /generate_soap:** Accept SOAPRequest, perform RAG lookup, build SOAP prompt, generate response, return `{"soap_note": "..."}`
3. Preserve the exact system prompt text and SOAP prompt text from the original code
4. Ensure ZERO references to `unsloth` or `chainlit` anywhere

**verify:**
- `app = FastAPI()` exists
- `app.mount("/static"` exists  
- `from transformers import` present
- `from peft import PeftModel` present
- No `unsloth` or `chainlit` strings anywhere
- `/chat` returns `{"response": ...}`
- `/generate_soap` returns `{"soap_note": ...}`

**done:** fastapi_app.py is a complete FastAPI server with PEFT model loading
