# 🧠 TheraMind: Dual-Mode Clinical Agent

TheraMind is an advanced, medically-aligned conversational AI agent designed to assist with clinical queries. It utilizes a robust **Retrieval-Augmented Generation (RAG)** pipeline combined with **Direct Preference Optimization (DPO)** to ensure responses are accurate, agentic, and clinically safe.

The frontend is built with **Chainlit**, providing a seamless, real-time chat interface, while the backend dynamically pulls fine-tuned adapter weights directly from the Hugging Face Hub.

## ✨ Core Features: The Dual-Mode Architecture

This model was explicitly fine-tuned using Multi-Task chaining to handle two distinct clinical workflows within a single continuous context window:

1. **Patient Intake Mode:** The agent acts as an empathetic, professional medical assistant. It engages in natural, back-and-forth dialogue to gather symptoms, ask clarifying questions, and build a comprehensive understanding of the patient's condition. 
2. **Clinical Scribe Mode (Doctor Mode):** Triggered by the specific command *"Generate clinical documentation"*, the model instantly switches personas. It stops conversing and synthesizes the entire preceding chat history into a highly structured, professional **SOAP note** (Subjective, Objective, Assessment, Plan).

## 🏗️ System Architecture & Evolution

This project was developed in three major iterative phases, following the industry-standard alignment pipeline:

* **Phase 1: Baseline Evaluation (Zero-Shot & One-Shot Prompting)**
  * Established baseline ROUGE metrics using the base Llama 3.2 (3B) model with 4-bit quantization. Evaluated output accuracy using zero-shot and one-shot prompt engineering against the `omi-health/medical-dialogue-to-soap-summary` dataset.
* **Phase 2: Supervised Fine-Tuning (SFT) for Agentic Multi-Tasking**
  * Applied Supervised Fine-Tuning (SFT) using Unsloth and PEFT QLoRA adapters. Mapped dialogues into a turn-by-turn chat template to teach the model to act as an active chatbot and instantly generate structured SOAP notes upon a specific user trigger.
  * *Weights hosted on Hugging Face: `VKM47/TheraMind-Agentic-V2`*
* **Phase 3: Direct Preference Optimization (DPO)**
  * Extracted baseline hallucinations from Phase 1 to create a targeted preference dataset of 49 chosen vs. rejected pairs. Applied DPO via Unsloth's patched `DPOTrainer` to align the SFT model, significantly reducing medical hallucinations and enforcing strict clinical guardrails.
  * *Weights hosted on Hugging Face: `VKM47/TheraMind-DPO-Adapters`*

## ⚙️ Core Technologies
* **LLM Framework:** Unsloth (for highly optimized, memory-efficient fine-tuning)
* **Base Model:** Llama-3.2-3B-Instruct
* **Vector Database:** ChromaDB (for local RAG implementation)
* **Frontend UI:** Chainlit
* **Model Registry:** Hugging Face Hub

## 📂 Repository Structure

```text
TheraMind/
├── data/                    # Raw medical datasets and evaluation CSVs
├── notebooks/               # Jupyter notebooks for baseline testing, SFT, and DPO fine-tuning
├── .chainlit/               # Chainlit UI configuration
├── app.py                   # Main application entry point and inference logic
├── build_db.py              # Script to instantiate and populate the Chroma vector database
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
Initialize the RAG pipeline by building the local ChromaDB instances from the provided data.

```Bash
python build_db.py
```
5. Launch the Application
Run the Chainlit server. The application will automatically pull the necessary DPO adapter weights from Hugging Face during the initial load.

```Bash
chainlit run app.py -w
```

***

