🧠 **TheraMind**: Dual-Mode Clinical Agent
TheraMind is an advanced, medically-aligned conversational AI agent designed to safely assist with clinical intake queries. It utilizes a robust Retrieval-Augmented Generation (RAG) pipeline combined with Direct Preference Optimization (DPO) to ensure responses are accurate, agentic, and clinically safe.

Moving beyond simple API wrapping, TheraMind is a full-stack, containerized deployment featuring a custom FastAPI backend, mathematical decoding guardrails, and a sleek, dual-persona web interface.

🌐 ***Try the Live Web App on Hugging Face Spaces!***: https://vkm47-theramind-ai.hf.space  (Note: The free-tier GPU sleeps after 15 minutes of inactivity; please allow ~60 seconds for the model to wake up and load into VRAM on the first request.)

✨ ***Core Features***: The Dual-Mode Architecture
This model was explicitly fine-tuned using Multi-Task chaining to handle two distinct clinical workflows within a single continuous context window, accessible via a custom-built UI:

Patient Intake Mode: The agent acts as an empathetic, professional medical assistant. It engages in natural, back-and-forth dialogue to gather symptoms, ask clarifying questions, and build a comprehensive understanding of the patient's condition.

Doctor SOAP Dashboard: With a single click, the interface transitions to a provider-facing view. The model instantly switches personas, stopping the conversation to synthesize the entire preceding chat history into a highly structured, professional SOAP note (Subjective, Objective, Assessment, Plan).

🛡️ ***Clinical Guardrails & "Zero-Knowledge" RAG***
To combat "Context Bleed" (a common flaw in smaller LLMs where they hallucinate textbook RAG data as patient history), TheraMind employs a strict safety hierarchy:

The Decoding Triad: Inference is mathematically constrained using aggressive nucleus sampling (top_p=0.95, top_k=50, temp=0.25) to prevent hallucinated medications and dosage recommendations.

Zero-Knowledge Start: The system prompt forces a positive constraint, explicitly telling the model that every new patient is a blank slate, neutralizing demographic and historical hallucinations.

Critical Emergency Overrides: The model actively scans for life-threatening symptoms (e.g., "crushing chest pain"). If detected, it breaks its intake loop, explicitly names the suspected emergency, and advises the user to call 911 immediately.

🏗️ ***System Architecture & Evolution***
This project was developed in major iterative phases, following the industry-standard alignment pipeline:

Phase 1: Baseline Evaluation (Zero-Shot & One-Shot Prompting)

Established baseline ROUGE metrics using the base Llama 3.2 (3B) model with 4-bit quantization. Evaluated output accuracy using zero-shot and one-shot prompt engineering against the omi-health/medical-dialogue-to-soap-summary dataset.

Phase 2: Supervised Fine-Tuning (SFT) for Agentic Multi-Tasking

Applied Supervised Fine-Tuning (SFT) using Unsloth and PEFT QLoRA adapters. Mapped dialogues into a turn-by-turn chat template to teach the model to act as an active chatbot and instantly generate structured SOAP notes.

Weights hosted on Hugging Face: VKM47/TheraMind-Agentic-V2

Phase 3: Direct Preference Optimization (DPO)

Extracted baseline hallucinations from Phase 1 to create a targeted preference dataset of chosen vs. rejected pairs. Applied DPO via Unsloth's patched DPOTrainer to align the SFT model, significantly reducing medical hallucinations and enforcing strict clinical guardrails.

Weights hosted on Hugging Face: VKM47/TheraMind-DPO-Adapters

Phase 4: Full-Stack Containerization & Deployment

Migrated from a local Chainlit prototype to a production-ready FastAPI backend serving custom static HTML/JS frontend assets.

Containerized the environment using Docker, embedding the ChromaDB vector store directly into the image for seamless cloud deployment.

⚙️ ***Core Technologies***
LLM Framework: Unsloth (for highly optimized, memory-efficient fine-tuning) & Hugging Face Transformers

Base Model: Llama-3.2-3B-Instruct

Vector Database: ChromaDB (for local RAG implementation)

Backend API: FastAPI & Uvicorn

Frontend UI: Custom HTML, CSS, JavaScript (Vanilla)

Deployment: Docker & Hugging Face Spaces

## 📂 Repository Structure

```text
TheraMind/
├── .planning/               # GSD workflow planning documents
├── chroma_db/               # ChromaDB persistent storage (gitignored, built locally)
├── data/                    # Raw medical datasets and evaluation CSVs
├── notebooks/               # Jupyter notebooks for baseline testing, SFT, and DPO fine-tuning
├── static/                  # Custom frontend web assets (HTML, JS, CSS, Images)
├── fastapi_app.py           # Main backend application entry point and inference logic
├── build_db.py              # Script to instantiate and populate the Chroma vector database
├── demo_typer.py            # PyAutoGUI script for recording demo videos
├── Dockerfile               # Containerization blueprint for cloud deployment
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```
Note: Model .safetensors weights and local .venv environments are strictly .gitignored to maintain a lightweight codebase. Weights are downloaded dynamically at runtime.

🚀 Quick Start Guide
Follow these steps to run TheraMind locally on your machine.

1. **Clone the Repository**
```Bash
git clone [https://github.com/Vishnu-K-Menon/TheraMind.git](https://github.com/Vishnu-K-Menon/TheraMind.git)
cd TheraMind
```
2. Set Up the Virtual Environment
It is highly recommended to use an isolated Python environment.

```Bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```
3. Install Dependencies
```Bash
pip install -r requirements.txt
```

5. Build the Vector Database
Initialize the RAG pipeline by building the local ChromaDB instances from the provided clinical guidelines.

```Bash
python build_db.py
```
5. Launch the Application
Run the FastAPI server. The application will automatically pull the necessary DPO adapter weights from Hugging Face during the initial load (this will take a few moments on the first run).

```Bash
python fastapi_app.py
```
Once you see Application startup complete in your terminal, open your web browser and navigate to http://localhost:8000 to interact with the dual-mode UI!
***

