# Technology Stack

## Languages & Runtime
- **Python 3.13** — Primary language for all application and training code
- **Platform:** Windows 11, NVIDIA GeForce RTX 3060 Laptop GPU (6GB VRAM)
- **CUDA:** 12.4 with Torch 2.6.0+cu124

## Core Frameworks
| Framework | Version | Purpose |
|-----------|---------|---------|
| Unsloth | 2026.3.4 | 4-bit quantized LLM inference & fine-tuning (QLoRA/DPO) |
| Chainlit | 2.10.0 | ChatGPT-style async web UI framework |
| ChromaDB | latest | Local persistent vector database for RAG |
| Transformers | 5.2.0 | HuggingFace model loading & tokenization |
| PyTorch | 2.6.0+cu124 | Deep learning runtime |
| PEFT | latest | Parameter-Efficient Fine-Tuning (LoRA adapters) |
| BitsAndBytes | latest | 4-bit quantization backend |

## Base Model
- **Llama-3.2-3B-Instruct** via `unsloth/llama-3.2-3b-instruct-unsloth-bnb-4bit`
- DPO-aligned LoRA adapters loaded from HuggingFace: `VKM47/TheraMind-DPO-Adapters`
- SFT adapters available at: `VKM47/TheraMind-Agentic-V2`

## Key Dependencies (from `requirements.txt`)
- `chainlit` — Web UI server
- `chromadb` — Vector store for RAG
- `sentence-transformers` — Embedding model for ChromaDB
- `unsloth` — Optimized LLM inference
- `trl` — DPO/RLHF training
- `peft`, `accelerate`, `bitsandbytes` — Quantized fine-tuning stack
- `pyautogui` — Demo automation utility
- `huggingface_hub` — Model weight upload/download

## Configuration
- No `.env` file used (secrets handled via gitignored `upload_weights.py`)
- ChromaDB persisted to `./chroma_db/` (gitignored, built locally via `build_db.py`)
- Model weights downloaded dynamically at runtime from HuggingFace Hub
- Chainlit config in `.chainlit/` directory (gitignored)

## Development Environment
- Virtual environment: `.venv/` (gitignored)
- Activation: `d:\git\MedAlign-V.1\.venv\Scripts\Activate.ps1`
- Run app: `chainlit run app.py`
- Build vector DB: `python build_db.py`
