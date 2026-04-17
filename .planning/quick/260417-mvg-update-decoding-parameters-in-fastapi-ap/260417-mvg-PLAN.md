---
quick_id: 260417-mvg
description: Update decoding parameters in fastapi_app.py for clinical safety
mode: quick-full
date: 2026-04-17
must_haves:
  truths:
    - generate_response function signature includes top_p and top_k parameters with correct defaults
    - model.generate() call contains top_p=top_p and top_k=top_k arguments
    - do_sample is set to True (hardcoded, not conditional)
    - temperature default is 0.15, top_p default is 0.90, top_k default is 40, max_new_tokens default is 512
    - No other parts of fastapi_app.py are modified
  artifacts:
    - fastapi_app.py (modified)
  key_links:
    - fastapi_app.py#L104 (generate_response function signature)
    - fastapi_app.py#L114-L123 (model.generate block)
---

# Quick Task 260417-mvg: Update Decoding Parameters in fastapi_app.py for Clinical Safety

## Goal

Update the `generate_response` inference helper function in `fastapi_app.py` to use stricter nucleus sampling (top_p/top_k) and always-on sampling mode (`do_sample=True`). This reduces RAG context bleed and hallucinations for clinical safety.

## Tasks

### Task 1: Update generate_response function signature and model.generate() call

**Files:**
- `fastapi_app.py`

**Action:**
Modify ONLY the `generate_response` function (lines 104–130). Two changes required:

1. **Function signature** (line 104) — replace current signature with:
   ```python
   def generate_response(messages: list[dict], max_new_tokens: int = 512, temperature: float = 0.15, top_p: float = 0.90, top_k: int = 40) -> str:
   ```

2. **model.generate() call** (lines 115–123) — add `top_p` and `top_k` arguments and change `do_sample`:
   ```python
   outputs = model.generate(
       **inputs,
       max_new_tokens=max_new_tokens,
       use_cache=True,
       temperature=temperature,
       top_p=top_p,
       top_k=top_k,
       do_sample=True,
       eos_token_id=terminators,
       pad_token_id=tokenizer.eos_token_id,
   )
   ```

**Verify:**
- `grep "def generate_response" fastapi_app.py` contains `top_p: float = 0.90, top_k: int = 40`
- `grep "top_p=" fastapi_app.py` shows `top_p=top_p,` inside model.generate()
- `grep "top_k=" fastapi_app.py` shows `top_k=top_k,` inside model.generate()
- `grep "do_sample=" fastapi_app.py` shows `do_sample=True,` (not conditional)

**Done:** Function signature and model.generate() block updated with nucleus sampling params
