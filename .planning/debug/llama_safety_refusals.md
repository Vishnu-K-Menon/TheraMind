# GSD Debug: Llama 3.2 System Prompt Refusals

## Objective
Investigate issue: Llama 3.2 is returning default base-model safety refusals for medical queries instead of using the TheraMind persona.

## Symptoms
**expected:** Model follows the TheraMind persona and strictly outputs medical advice guided by RAG.
**actual:** Model ignores the system prompt and falls back to default Meta Llama 3 warnings/refusals.
**reproduction:** Running the fastapi_app.py with PEFT adapters, generating responses via the `/chat` endpoint.

## Root Cause
When `tokenizer.apply_chat_template` is used with `tokenize=False`, the method outputs a raw string prefixed with the `<|begin_of_text|>` token (Llama 3's BOS token). However, the manual call to `tokenizer([text], return_tensors="pt")` subsequently applied the tokenizer's default `add_special_tokens=True` behavior, which injected a *second* `<|begin_of_text|>` token into the `input_ids`. Llama 3 explicitly breaks instruction-following when its token format is malformed or duplicated, reverting its behavior to the base model's domain. Additionally, generation stopped randomly as `eos_token_id` and the `<|eot_id|>` boundaries were not explicitly provided to the generate method.

## Resolution
1. Added `add_special_tokens=False` to the manual string tokenization so only the template's special headers are preserved.
2. Sourced `terminators` (both regular EOS and `<|eot_id|>`) from the tokenizer and supplied it directly to `model.generate`.
3. Added `pad_token_id` to avoid warning traces in FastAPI's console.
4. Input prompt array parsing is kept intact with `inputs["input_ids"].shape[1]` correctly stripping the entire input.

## DEBUG COMPLETE
