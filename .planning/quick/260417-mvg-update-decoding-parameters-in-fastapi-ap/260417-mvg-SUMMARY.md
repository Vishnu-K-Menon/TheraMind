# Quick Task 260417-mvg: Summary

**Task:** Update decoding parameters in fastapi_app.py for clinical safety  
**Date:** 2026-04-17  
**Commit:** 29c0fe3

## Changes Made

### `fastapi_app.py` — `generate_response` function

**Signature (line 104):**
- Added `top_p: float = 0.90` parameter
- Added `top_k: int = 40` parameter  
- Changed `temperature` default from `0.3` → `0.15`

**`model.generate()` block (lines 119-122):**
- Added `top_p=top_p,`
- Added `top_k=top_k,`
- Changed `do_sample=temperature > 0` → `do_sample=True` (hardcoded, unconditional)

## Rationale

- **Nucleus sampling (top_p=0.90):** Restricts token selection to the top 90% cumulative probability mass, cutting off low-probability tail tokens that cause hallucinations.
- **Top-k filtering (top_k=40):** Caps candidate tokens at 40 per step, preventing the model from wandering into incoherent continuations from RAG context bleed.
- **do_sample=True (hardcoded):** Removes the conditional `temperature > 0` guard. At low temperatures nucleus sampling is still preferable to pure greedy decoding for clinical text fidelity.
- **temperature=0.15 default:** More conservative than 0.3 — reduces creativity at the cost of higher determinism, appropriate for clinical documentation.

No other parts of `fastapi_app.py` were modified.
