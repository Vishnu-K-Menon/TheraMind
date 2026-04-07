# Concerns

## Technical Debt

### 1. Single-File Architecture
- `app.py` (132 lines) contains all application logic: model loading, RAG retrieval, prompt engineering, chat handling, and SOAP generation
- No separation of concerns — prompt templates, inference logic, and UI handlers are interleaved
- As the app grows, this will become difficult to maintain

### 2. No Error Handling
- No try/except blocks anywhere in `app.py`
- Model inference failures will crash the Chainlit server
- ChromaDB connection failures are unhandled
- No graceful degradation if HuggingFace Hub is unreachable during model download

### 3. Hardcoded RAG Corpus
- Only 3 clinical guidelines in `build_db.py` (migraine, back pain, fever)
- No mechanism to add guidelines without modifying source code
- No admin interface for knowledge base management

### 4. No Session Persistence
- Conversation history exists only in `cl.user_session` (in-memory)
- All history is lost on server restart or page refresh
- No database backing for audit trails or clinical record-keeping

## Security Concerns

### 1. HuggingFace Token Exposure
- `upload_weights.py` is gitignored, but the token was initially committed in conversation context
- No environment variable pattern for secrets management
- No `.env` file support implemented

### 2. No Authentication
- Chainlit server runs open on `localhost:8000`
- No user authentication or access control
- Anyone on the network could access the medical AI if exposed

### 3. Prompt Injection Risk
- System prompt is injected via f-string with user-controlled content (`retrieved_context`)
- No sanitization of user input before passing to the model
- Adversarial users could attempt to override system instructions

## Performance Concerns

### 1. VRAM Constraints
- RTX 3060 Laptop (6GB VRAM) is at capacity with 4-bit quantized 3B model
- No headroom for larger models or batch processing
- `max_new_tokens=512` limits response length

### 2. Synchronous Inference
- Model inference blocks the Chainlit event loop
- Long generation times (~30-60s) make the UI feel unresponsive
- No streaming token output (response appears all at once)

### 3. Cold Start
- Model loading takes 3-5 seconds on startup (downloading from HuggingFace on first run)
- ChromaDB initialization adds additional startup time

## Fragile Areas

### 1. Chainlit API Stability
- Already encountered multiple breaking changes between Gradio 6.0 and Chainlit v2.0
- `cl.Action` API changed (`value` → `payload`)
- `Message.update()` API changed (no kwargs)
- Future Chainlit updates may break existing code

### 2. SOAP Note Quality
- SOAP generation uses a separate, simpler system prompt without the full guardrails
- No structured output validation (SOAP format not enforced)
- Quality depends entirely on DPO alignment holding

### 3. RAG Relevance
- ChromaDB returns `n_results=1` — only the single closest match
- No relevance threshold — always returns something even if no guideline matches
- Could lead to false context injection for completely unrelated symptoms
