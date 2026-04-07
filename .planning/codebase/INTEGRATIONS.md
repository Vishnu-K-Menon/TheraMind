# External Integrations

## HuggingFace Hub
- **Purpose:** Model weight hosting & dynamic download
- **Repositories:**
  - `VKM47/TheraMind-DPO-Adapters` — Production DPO-aligned LoRA adapters (Phase 3)
  - `VKM47/TheraMind-Agentic-V2` — SFT adapters (Phase 2)
- **Usage in `app.py`:** Model loaded at startup via `FastLanguageModel.from_pretrained(model_name="VKM47/TheraMind-DPO-Adapters")`
- **Upload script:** `upload_weights.py` (gitignored for security — contains HF token placeholder)
- **Auth:** HuggingFace write token required for uploads only; reads are public

## ChromaDB (Local Vector Store)
- **Purpose:** RAG pipeline — stores clinical guideline embeddings for retrieval
- **Type:** `PersistentClient` at `./chroma_db/`
- **Collection:** `clinical_guidelines` (3 documents)
- **Documents indexed:**
  1. `doc_1` — Primary Migraine Management (source: `Neurology_Guidelines_2026`)
  2. `doc_2` — Acute Non-Specific Low Back Pain (source: `Ortho_Guidelines_2026`)
  3. `doc_3` — Acute Fever Management in Adults (source: `Internal_Med_Guidelines_2026`)
- **Query:** Single-result nearest-neighbor (`n_results=1`) per user message
- **Builder script:** `build_db.py` — uses `upsert()` for idempotent population

## Chainlit Server
- **Purpose:** Async WebSocket-based chat UI server
- **URL:** `http://localhost:8000`
- **Session management:** `cl.user_session` stores per-user conversation `history` list
- **Action buttons:** `cl.Action` with `payload` dict (Chainlit v2.0+ API)

## No External APIs
- No third-party REST APIs, webhooks, or external databases
- All inference runs locally on GPU
- All embeddings computed locally via ChromaDB's default embedding function
