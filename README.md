# HIND ISRAE BAHAOUI - RAG Chatbot

*A localized Retrieval-Augmented Generation (RAG) chatbot powered by Ollama’s Mistral model, LangChain, FAISS, and Streamlit.*

---

## Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [One-Time Data Indexing](#one-time-data-indexing)
5. [Launching the Chatbot](#launching-the-chatbot)
6. [Customization](#customization)
7. [Project Structure](#project-structure)
8. [Data Workflow & RAG Principle](#data-workflow--rag-principle)

---

## Features

* **Retrieval-Driven Answers**: Efficiently search semantically embedded PDF content using FAISS.
* **High-Quality Generation**: Produce fluent, context-aware responses with Ollama’s Mistral LLM.
* **Configurable Sampling**: Tweak `temperature`, `top_k`, and `top_p` live via the Streamlit sidebar.
* **Dark-Themed UI**: Modern, sleek chat interface built with custom CSS.
* **One-Time Indexing**: Offline ingestion (`ingest.py`) generates `faiss_index.pkl`—no runtime overhead.
* **Privacy & Locality**: Entirely local execution; no data leaves your machine or external APIs.

---

## Prerequisites

* **Python 3.8+** installed.
* **Ollama CLI** with the Mistral model:

  ```bash
  ollama pull mistral
  ```
* **Git** (optional) for version control.
* **Operating System**: Windows, macOS, or Linux.
* **RAM**: ≥ 8 GB recommended for large documents.

### CPU-Only Justification

This project is designed for CPU-only environments to maximize accessibility:

* **No GPU required**: Embedding (Sentence-Transformers) and inference (Ollama/Mistral) run on CPU.
* **Ease of setup**: Simplifies installation for users without specialized hardware.
* **Portability**: Works on standard laptops or cloud VMs without GPU.
* **Reproducibility**: CPU pipelines reduce variability across environments.

Modern multi-core CPUs can comfortably handle moderate document sizes and interactive query loads.

---

## Installation

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/rag-chatbot.git
cd rag-chatbot

# 2. Create & activate a virtual environment
python -m venv .venv
# Windows (PowerShell)
. .venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

## One-Time Data Indexing

1. **Add PDFs**: Place your `.pdf` files into `data/pdfs/` (create if missing).
2. **Run ingestion**:

   ```bash
   python ingest.py
   ```

   * **Process**:

     * `PDFPlumberLoader` extracts text.
     * `SemanticChunker` splits into semantic chunks.
     * `HuggingFaceEmbeddings` embeds each chunk.
     * FAISS builds and saves `faiss_index.pkl`.
3. **Confirm**: Look for `Indexed X chunks to 'faiss_index.pkl'` in console.

Re-run only when document corpus changes.

---

## Launching the Chatbot

```bash
streamlit run app.py
```

* Open [http://localhost:8501](http://localhost:8501) in your browser.
* Enter your question and see grounded answers derived from your PDFs.

---

## Customization

* **Sampling Settings**: Adjust in the sidebar for creative vs. deterministic responses.
* **UI Styling**: Tweak colors in the `<style>` block of `app.py`.
* **Document Types**: Extend `ingest.py` to support CSV, DOCX, etc., via additional loaders.

---

## Project Structure

```bash
rag_app/
├── data/
│   ├── pdfs/            # Your PDF documents
│   └── faiss_index.pkl  # FAISS index (post-ingestion)
├── ingest.py            # Offline ingestion & indexing script
├── rag_chain.py         # RetrievalQA chain (FAISS + Ollama)
├── app.py               # Dark-themed Streamlit chat UI
├── requirements.txt     # Pinned Python dependencies
└── README.md            # This documentation
```

---

## Data Workflow & RAG Principle

```mermaid
flowchart LR
  subgraph Ingestion [One-Time Ingestion]
    A[PDFs in data/pdfs/] --> B[ingest.py]
    B --> C[FAISS Index<br/>(faiss_index.pkl)]
  end

  subgraph Query [Runtime Query]
    D[User Question] --> E[rag_chain.py]
    C --> E
    E --> F[Ollama Mistral LLM]
    F --> G[Streamlit UI: Answer]
  end
```

**RAG Steps**:

1. **Retrieve**: FAISS returns top-K similar chunks.
2. **Augment**: Combine chunks into context prompt.
3. **Generate**: Mistral LLM produces a grounded answer.

---
