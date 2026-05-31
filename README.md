# 📄 GenAI Document Intelligence Assistant

A RAG (Retrieval-Augmented Generation) powered document analysis system that processes financial and healthcare PDFs to answer questions, extract KPIs, and generate executive summaries.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red)
![LangChain](https://img.shields.io/badge/LangChain-0.1.16-green)
![Groq](https://img.shields.io/badge/Groq-LLaMA3-orange)
![FAISS](https://img.shields.io/badge/FAISS-Vector_DB-purple)

---

## 🎯 Project Overview

This project builds an end-to-end GenAI pipeline that:
- Accepts financial (JPMorgan, BofA) and healthcare (CMS, CDC) PDF documents
- Chunks and embeds document text into a FAISS vector store
- Uses RAG to answer natural language questions with page citations
- Auto-extracts KPIs using regex + LLM
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
| ⚡ Fast Responses | Powered by Groq API — answers in seconds |
| 🆓 Free to Use | No OpenAI costs — uses Groq free tier |

---

## 🏗️ Architecture
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
RAG Pipeline (LangChain + Groq LLaMA3)
↓
┌─────────────────────────────────┐
│  Q&A  │  KPI Extraction  │ Summary │
└─────────────────────────────────┘
```
---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| **Frontend** | Streamlit |
| **LLM** | Groq API (LLaMA3-8b) |
| **Embeddings** | HuggingFace all-MiniLM-L6-v2 |
| **Vector DB** | FAISS |
| **RAG Framework** | LangChain |
| **PDF Parsing** | pdfplumber + PyPDF2 |
| **KPI Extraction** | Regex + Groq LLM |
| **Language** | Python 3.10 |

---

## 📁 Project Structure
```
genai-document-assistant/
│
├── app.py                    # Main Streamlit UI
├── requirements.txt          # Python dependencies
├── .env                      # API keys (not uploaded)
├── README.md
│
└── utils/
├── init.py
├── pdf_processor.py      # PDF text extraction
├── vector_store.py       # FAISS vector store builder
├── rag_chain.py          # RAG chain with Groq
└── kpi_extractor.py      # KPI extraction logic
```
---

## 🚀 How to Run

### Prerequisites
- Python 3.10+
- Groq API key (free at https://console.groq.com)

### Step 1 — Clone the repository
```bash
git clone https://github.com/YourUsername/genai-document-assistant.git
cd genai-document-assistant
```

### Step 2 — Create conda environment
```bash
conda create -n genai-doc-env python=3.10
conda activate genai-doc-env
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Add API key
Create a `.env` file in the root folder:
'''
GROQ_API_KEY=your_groq_api_key_here
'''
### Step 5 — Run the app
```bash
streamlit run app.py
```

### Step 6 — Open in browser
'''
http://localhost:8501
''''
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
| Revenue | $158,104M |
| Net Income | $49,552M |
| Total Assets | $3,875,393M |

### Q&A with Citation
Q: What is the net income?
A: The net income for the year ended December 31, 2023
is $49,552 million (Page 1)
Source: Page 1 — Financial Highlights 2023
---

## 🔧 RAG Pipeline Details

1. **PDF Parsing** — pdfplumber extracts text page by page with metadata
2. **Chunking** — 800 char chunks with 150 char overlap
3. **Embeddings** — HuggingFace MiniLM creates semantic vectors
4. **FAISS Index** — stores vectors for similarity search
5. **Retrieval** — top 3 relevant chunks retrieved per query
6. **Generation** — Groq LLaMA3 generates answer from context
7. **Citation** — page numbers returned with every answer

---

## 🆓 Why Groq?

- ✅ Free API tier available
- ✅ Runs LLaMA3 model
- ✅ 10x faster than local Ollama
- ✅ No GPU required
- ✅ No credit card needed

---

## 👩‍💻 Author

**Navya Yalavarthi**
- GitHub: [@navyayalavarthi](https://github.com/navyayalavarthi)
- LinkedIn: [linkedin.com/in/navyayalavarthi](https://linkedin.com/in/navyayalavarthi)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
  
