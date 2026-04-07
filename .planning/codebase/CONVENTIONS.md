# Code Conventions

## Python Style
- **No linter/formatter enforced** — No `pyproject.toml`, `setup.cfg`, or tool configs
- Mostly PEP 8 compliant, though not strictly enforced
- 4-space indentation throughout
- f-strings used consistently for string interpolation
- Triple-quoted f-strings for multi-line prompts

## Function Patterns

### Chainlit Async Decorators
All UI-facing functions are async and decorated with Chainlit lifecycle hooks:
```python
@cl.on_chat_start      # Session initialization
@cl.on_message          # User message handler
@cl.action_callback     # Button click handler
```

### Message Update Pattern (Chainlit v2.0+)
Due to Chainlit v2.0 breaking changes, content updates follow:
```python
msg = cl.Message(content="")
await msg.send()
# ... generate response ...
msg.content = response
await msg.update()  # No kwargs allowed
```

### Action Button Pattern (Chainlit v2.0+)
```python
cl.Action(name="...", payload={"key": "value"}, description="...")
# NOT: cl.Action(name="...", value="...") — deprecated
```

## System Prompt Engineering
- Prompts are embedded as f-string literals inside handler functions
- RAG context injected via `{retrieved_context}` interpolation
- Instructions are numbered and categorized (GUARDRAILS vs CLINICAL INSTRUCTIONS)
- Two separate prompt templates: patient chat vs SOAP scribe

## Error Handling
- Minimal — no try/except blocks in the application
- Empty history check in SOAP callback (`if not history: return`)
- ChromaDB results validated with `if results['documents'] and results['documents'][0]`

## State Management
- `cl.user_session.set("history", [])` — per-session conversation memory
- History is a list of `{"role": "...", "content": "..."}` dicts
- No database persistence — sessions are ephemeral

## Import Style
- Standard library first, then third-party
- No relative imports (single-file application)

## Comments
- Section headers use `# --- N. Section Name ---` format
- Inline comments explain non-obvious decisions
- No docstrings on functions
