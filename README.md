# 📄 GenAI Document Intelligence Assistant

A RAG (Retrieval-Augmented Generation) powered document analysis system that processes financial and healthcare PDFs to answer questions, extract KPIs, and generate executive summaries.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red)
![LangChain](https://img.shields.io/badge/LangChain-0.1.16-green)
![Ollama](https://img.shields.io/badge/Ollama-TinyLlama-orange)
![FAISS](https://img.shields.io/badge/FAISS-Vector_DB-purple)

---

## 🎯 Project Overview

This project builds an end-to-end GenAI pipeline that:
- Accepts financial (JPMorgan, BofA) and healthcare (CMS, CDC) PDF documents
- Chunks and embeds document text into a FAISS vector store
- Uses RAG to answer natural language questions with page citations
- Auto-extracts KPIs using regex + Ollama LLM
- Generates 3-paragraph executive summaries

---

## ✨ Features

| Feature | Description |
|---|---|
| 📤 PDF Upload | Upload any financial or healthcare PDF |
| 💬 Q&A with Citations | Ask questions, get answers with page numbers |
| 📊 KPI Extraction | Auto-extract revenue, net income, EPS, assets |
| 📝 Summary Generation | Generate executive summaries instantly |
| 🏥 Healthcare Support | Works with CMS/CDC clinical documents |
| 💰 Financial Support | Works with annual reports and 10-K filings |
| 🦙 Local LLM | Powered by Ollama TinyLlama — runs on your machine |
| 🆓 Free to Use | No API costs — fully local and free |

---

## 🏗️ RAG Architecture
```
PDF Upload
↓
Text Extraction (pdfplumber + PyPDF2)
↓
Text Chunking (RecursiveCharacterTextSplitter)
↓
Embeddings (HuggingFace all-MiniLM-L6-v2)
↓
Vector Store (FAISS)
↓
RAG Pipeline (LangChain + Ollama TinyLlama)
↓
┌──────────────────────────────────┐
│  Q&A  │  KPI Extraction  │ Summary │
└──────────────────────────────────┘
```
---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| **Frontend** | Streamlit |
| **LLM** | Ollama (TinyLlama) — runs locally |
| **Embeddings** | HuggingFace all-MiniLM-L6-v2 — free, local |
| **Vector DB** | FAISS |
| **RAG Framework** | LangChain |
| **PDF Parsing** | pdfplumber + PyPDF2 |
| **KPI Extraction** | Regex + Ollama LLM |
| **Language** | Python 3.10 |

---

## 📁 Project Structure
```
genai-document-assistant/
│
├── app.py
├── requirements.txt
├── README.md
│
└── utils/
├── init.py
├── pdf_processor.py
├── vector_store.py
├── rag_chain.py
└── kpi_extractor.py
```
---

## 🚀 How to Run

### Prerequisites
- Python 3.10+
- Ollama installed — free at https://ollama.com
- No API keys needed

### Step 1 — Clone the repository
```bash
git clone https://github.com/naviy408-commits/genai-document-assistant.git
cd genai-document-assistant
```

### Step 2 — Install Ollama and pull model
```bash
ollama pull tinyllama
```

### Step 3 — Start Ollama server
```bash
ollama serve
```
Keep this terminal open.

### Step 4 — Create conda environment
```bash
conda create -n genai-doc-env python=3.10
conda activate genai-doc-env
```

### Step 5 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 6 — Run the app
```bash
streamlit run app.py
```

### Step 7 — Open in browser
http://localhost:8501
---

## 📊 Supported Documents

### Financial Documents
- JPMorgan Chase Annual Reports
- Bank of America Annual Reports
- Any 10-K / 10-Q SEC filings
- Financial highlights summaries

### Healthcare Documents
- CMS Hospital Quality Reports
- CDC Health Statistics Reports
- Clinical guidelines
- Patient outcome reports

---

## 💡 How to Use

1. **Select document type** — Financial or Healthcare
2. **Upload PDF** — drag and drop or browse
3. **Click Process PDFs** — builds vector index
4. **Ask Questions** — type or click suggested questions
5. **Extract KPIs** — auto-pulls key metrics
6. **Generate Summary** — creates executive summary

---

## 📸 Sample Questions

### Financial Documents
What was the total revenue in 2023?
What is the net income?
What are the main business risks?
What is the earnings per share (EPS)?
Summarize the financial highlights.
### Healthcare Documents
What are the readmission rates?
What quality metrics are reported?
What are the key clinical guidelines?
Summarize the patient outcomes.
---

## 📈 Sample Output

### KPIs Extracted
| KPI | Value |
|---|---|
| Revenue | 158,104 |
| Net Income | 49,552 |
| Total Assets | 3,875,393 |

### Q&A with Citation
Q: What is the net income?
A: The net income for the year ended December 31, 2023
is $49,552 million (Page 1)
Source: Page 1 — Financial Highlights 2023
---

## 🔧 How RAG Works

1. **PDF Parsing** — pdfplumber extracts text page by page
2. **Chunking** — 800 char chunks with 150 char overlap
3. **Embeddings** — HuggingFace MiniLM creates semantic vectors
4. **FAISS Index** — stores vectors for similarity search
5. **Retrieval** — top 3 relevant chunks per query
6. **Generation** — Ollama TinyLlama generates answer from context
7. **Citation** — page numbers returned with every answer

---

## 📦 Requirements
streamlit==1.32.0
langchain==0.1.16
langchain-community==0.0.34
langchain-core==0.1.46
langchain-text-splitters==0.0.1
faiss-cpu==1.8.0
pdfplumber==0.11.0
PyPDF2==3.0.1
sentence-transformers==2.7.0
ollama==0.1.9
tiktoken==0.7.0
pandas==2.2.2
plotly==5.21.0
python-dotenv==1.0.1
torch==2.2.2
---

## 🆓 Why Ollama + TinyLlama?

- ✅ Completely free — no API costs
- ✅ Runs 100% locally on your machine
- ✅ No internet required after setup
- ✅ No API key needed
- ✅ Private — your documents never leave your computer

---

## 👩‍💻 Author

**Navya Yalavarthi**
- GitHub: [@naviy408-commits](https://github.com/naviy408-commits)
- LinkedIn: [linkedin.com/in/navyayalavarthi](https://linkedin.com/in/navyayalavarthi)

---

## 📄 License

This project is open source and available under the MIT License.
