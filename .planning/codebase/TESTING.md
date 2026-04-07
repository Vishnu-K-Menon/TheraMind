# Testing

## Current State: No Automated Tests

There are no unit tests, integration tests, or test framework configured in this project.

## Evaluation Approach
Testing is performed through:

### 1. Manual Red-Teaming
- Direct interaction with the Chainlit UI
- Adversarial prompts to test safety guardrails (e.g., infant dosage attacks)
- Out-of-domain queries to verify fallback behavior
- Demographic mismatch scenarios

### 2. Baseline Metrics (Notebook-Based)
- **Phase 1:** ROUGE score evaluation in `Llama_3_Baseline_Evaluation.ipynb`
- **Phase 3:** DPO preference pair validation in `Version_3_DPO_Alignment_4090 (1).ipynb`
- Evaluation data in `data/v1_llama_baseline.csv`

### 3. Demo Automation
- `demo_typer.py` — PyAutoGUI script for recording demo videos
- Types predefined medical scenarios into the Chainlit UI

## CI/CD
- No CI/CD pipeline configured
- No GitHub Actions or pre-commit hooks
- Manual `git push` workflow

## Recommended Test Areas (Future)
- RAG retrieval accuracy (does ChromaDB return correct guideline for symptoms?)
- System prompt compliance (does AI follow guardrail instructions?)
- Demographic mismatch detection
- SOAP note structure validation
- Regression tests for known hallucination patterns from DPO training data
