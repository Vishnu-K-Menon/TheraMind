# Directory Structure

```text
d:\git\MedAlign-V.1/
├── .chainlit/              # Chainlit UI config (gitignored)
├── .files/                 # Chainlit file uploads
├── .git/                   # Git repository
├── .gitignore              # Excludes venv, weights, chroma_db, secrets
├── .planning/              # GSD workflow planning documents
│   └── codebase/           # This codebase map
├── .venv/                  # Python virtual environment (gitignored)
├── __pycache__/            # Python bytecode cache (gitignored)
│
├── app.py                  # ★ Main application — Chainlit server + RAG + inference
├── build_db.py             # ChromaDB population script (3 clinical guidelines)
├── chainlit.md             # Chainlit welcome screen content
├── demo_typer.py           # PyAutoGUI demo typing automation
├── upload_weights.py       # HuggingFace weight upload (gitignored)
├── README.md               # Project documentation
├── requirements.txt        # pip dependencies (12KB, comprehensive)
│
├── chroma_db/              # ChromaDB persistent storage (gitignored, built locally)
├── unsloth_compiled_cache/ # Unsloth kernel cache (gitignored)
│
├── data/
│   ├── v1_llama_baseline.csv           # Phase 1 baseline evaluation results
│   └── v3_dpo_preference_data.json     # Phase 3 DPO training pairs (chosen/rejected)
│
└── notebook/
    ├── Llama_3_Baseline_Evaluation.ipynb      # Phase 1: baseline ROUGE metrics
    ├── Version_2_using 4090.ipynb             # Phase 2: SFT on cloud 4090
    ├── Version_3_DPO_Alignment_4090 (1).ipynb # Phase 3: DPO alignment
    ├── v2_agentic_adapters/                   # SFT LoRA weights (gitignored)
    ├── v3_dpo_aligned_adapters/               # DPO LoRA weights (gitignored)
    └── unsloth_compiled_cache/                # Notebook kernel cache (gitignored)
```

## Key Locations
| What | Where |
|------|-------|
| Application entry | `app.py` |
| RAG database builder | `build_db.py` |
| Training notebooks | `notebook/*.ipynb` |
| Training data | `data/` |
| Model weights (local) | `notebook/v3_dpo_aligned_adapters/` |
| Vector store (local) | `chroma_db/` |
| Dependencies | `requirements.txt` |

## Naming Conventions
- **Files:** `snake_case.py` for scripts, descriptive names for notebooks
- **Directories:** lowercase, underscore-separated
- **Git branch:** `main`
- **Remote:** `origin` → `https://github.com/Vishnu-K-Menon/TheraMind.git`
