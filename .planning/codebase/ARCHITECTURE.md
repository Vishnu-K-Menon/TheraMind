# Architecture

## Pattern: Monolithic RAG + LLM Chat Application

Single-file async application (`app.py`) combining:
1. **Model loading** — Runs once at module import time
2. **Vector DB connection** — Persistent ChromaDB client
3. **Chainlit event handlers** — Async decorators for UI interactions

## Data Flow

```
User Input
    │
    ▼
@cl.on_message ─── history.append(user_query)
    │
    ▼
ChromaDB.query(user_query, n_results=1) ── retrieves closest clinical guideline
    │
    ▼
Build dynamic_system_prompt with:
  - Goldilocks RAG injection (MEDICAL TEXTBOOK REFERENCE)
  - Patient intake guardrails (7 instructions)
  - Retrieved context inserted as reference
    │
    ▼
tokenizer.apply_chat_template([system + history])
    │
    ▼
model.generate(temp=0.3 for chat, temp=0.1 for SOAP)
    │
    ▼
Response → history.append(assistant) → cl.Message.update()
    │
    ▼
cl.Action button attached ("generate_soap")
```

## Dual-Mode Architecture

### Patient Mode (`@cl.on_message`)
- Triggered by every user message
- RAG retrieval based on single user query
- Temperature: 0.3 (natural conversational flow)
- Attaches "Generate SOAP Note" action button to each response

### Doctor Mode (`@cl.action_callback("generate_soap")`)
- Triggered by clicking the action button
- RAG retrieval based on entire conversation history (all user messages concatenated)
- Temperature: 0.1 (strict medical formatting)
- Uses a separate `soap_prompt` system message (medical scribe persona)
- Removes button after click via `await action.remove()`

## System Prompt Engineering (Goldilocks Prompt)

The system prompt implements a multi-branch safety logic:

| Branch | Condition | Behavior |
|--------|-----------|----------|
| Guardrail 1 | No prior patient knowledge | Never assume demographics |
| Guardrail 2 | Generic greeting ("hi") | Respond with greeting only |
| Guardrail 3 | Virtual chatbot limitation | Never pretend physical exam |
| Branch 4 | Symptoms match guideline | Strict guideline adherence |
| Branch 5 | Red flag symptoms detected | Immediate emergency referral |
| Branch 6 | Demographic mismatch | Refuse dosages, state AI limitation |
| Branch 7 | Symptoms don't match | Ignore excerpt, safe conservative advice |

## Entry Points
- **`chainlit run app.py`** — Production entry point (Chainlit CLI)
- **`python build_db.py`** — One-time vector DB population
- **`python upload_weights.py`** — One-time weight upload to HuggingFace
- **`python demo_typer.py`** — Demo automation utility

## Model Training Pipeline (Notebooks)
1. `Llama_3_Baseline_Evaluation.ipynb` — Phase 1: Zero/one-shot baseline ROUGE metrics
2. `Version_2_using 4090.ipynb` — Phase 2: SFT with QLoRA on cloud RTX 4090
3. `Version_3_DPO_Alignment_4090 (1).ipynb` — Phase 3: DPO alignment on cloud RTX 4090
