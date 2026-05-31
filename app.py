import streamlit as st
import pandas as pd
import time

from utils.pdf_processor import extract_documents, get_full_text
from utils.vector_store import build_vector_store
from utils.rag_chain import build_rag_chain, ask_question
from utils.kpi_extractor import (
    extract_financial_kpis,
    extract_healthcare_kpis,
    generate_summary,
)

st.set_page_config(
    page_title="GenAI Financial Report Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #fffbf0; }
    .main-title { font-size: 2.8rem; font-weight: 800; color: #1a1a1a; }
    .subtitle { color: #555; font-size: 1rem; margin-bottom: 2rem; }
    .section-card {
        background: #f9f9f9;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #eee;
        height: 100%;
    }
    .section-title { font-size: 1.2rem; font-weight: 700; margin-bottom: 0.8rem; }
    .source-box {
        background: #f0f9ff;
        border-left: 3px solid #0ea5e9;
        border-radius: 4px;
        padding: 0.7rem 1rem;
        margin: 0.4rem 0;
        font-size: 0.85rem;
    }
    .answer-box {
        background: #f0fdf4;
        border-left: 3px solid #22c55e;
        border-radius: 4px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
    }
    .kpi-card {
        background: #fff;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.4rem 0;
        text-align: center;
    }
    .kpi-label { font-size: 0.75rem; color: #6b7280; text-transform: uppercase; }
    .kpi-value { font-size: 1.5rem; font-weight: 700; color: #111827; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ────────────────────────────
for key, val in {
    "vector_store": None,
    "rag_chain": None,
    "full_text": "",
    "doc_type": "financial",
    "qa_history": [],
    "kpis": None,
    "summary": None,
    "doc_name": "",
    "processed": False,
    "pending_q": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── SIDEBAR ──────────────────────────────────
with st.sidebar:
    st.markdown("### 📁 Upload Documents")
    st.markdown("")
    doc_type = st.selectbox("Document Type", ["financial", "healthcare"])
    st.session_state.doc_type = doc_type
    st.markdown("**Upload PDF Files**")
    uploaded_file = st.file_uploader(
        "", type=["pdf"], label_visibility="collapsed"
    )
    st.markdown("")

    if uploaded_file:
        if st.button("🚀 Process PDFs", use_container_width=True, type="primary"):
            st.session_state.processed = False
            st.session_state.qa_history = []
            st.session_state.kpis = None
            st.session_state.summary = None
            st.session_state.pending_q = ""

            with st.spinner("Processing PDFs..."):
                st.write(f"Processing: {uploaded_file.name}")
                documents = extract_documents(uploaded_file)
                st.session_state.full_text = get_full_text(documents)
                st.session_state.doc_name = uploaded_file.name

            if not documents:
                st.error("Could not extract text from PDF.")
            else:
                with st.spinner(f"Building index ({len(documents)} pages)..."):
                    vs = build_vector_store(documents)
                    st.session_state.vector_store = vs
                with st.spinner("Loading AI model..."):
                    chain = build_rag_chain(vs)
                    st.session_state.rag_chain = chain
                    st.session_state.processed = True
                st.success(f"✅ Done! {len(documents)} pages indexed.")

    st.markdown("---")
    st.markdown("⚡ LLM: Groq (llama3)")
    st.markdown("🔢 Embeddings: MiniLM-L6-v2")
    st.markdown("📦 Vector DB: FAISS")
    st.caption("Free · Fast · No local GPU needed")

# ── MAIN HEADER ──────────────────────────────
col_icon, col_title = st.columns([0.08, 0.92])
with col_icon:
    st.markdown("# 📊")
with col_title:
    st.markdown(
        '<div class="main-title">GenAI Financial Report Assistant</div>',
        unsafe_allow_html=True,
    )

st.markdown(
    '<div class="subtitle">Upload Annual Reports — Ask Questions — Powered by RAG</div>',
    unsafe_allow_html=True,
)
st.markdown("---")

# ── LANDING PAGE ─────────────────────────────
if not st.session_state.processed:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">📊 Financial Analysis</div>
            <p style="color:#888;font-size:0.85rem">Upload annual reports and ask:</p>
            <ul style="color:#555;font-size:0.9rem">
                <li>What was the total revenue?</li>
                <li>What are the key risks?</li>
                <li>What is the EPS?</li>
                <li>Summarize financial highlights</li>
                <li>What was net income growth?</li>
            </ul>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">🏥 Healthcare Analysis</div>
            <p style="color:#888;font-size:0.85rem">Upload healthcare reports and ask:</p>
            <ul style="color:#555;font-size:0.9rem">
                <li>What are readmission rates?</li>
                <li>What are quality metrics?</li>
                <li>Summarize patient outcomes</li>
                <li>Extract clinical KPIs</li>
                <li>What are policy changes?</li>
            </ul>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">⚙️ How RAG Works</div>
            <p style="color:#888;font-size:0.85rem">Simple 5 steps:</p>
            <ol style="color:#555;font-size:0.9rem">
                <li>Upload PDF in sidebar</li>
                <li>Click Process PDFs</li>
                <li>Ask any question</li>
                <li>Get answer + citation</li>
                <li>Extract KPIs + Summary</li>
            </ol>
        </div>""", unsafe_allow_html=True)
    st.markdown("")
    st.info("👆 Upload a PDF document in the sidebar to get started!")
    st.stop()

# ── TABS ─────────────────────────────────────
st.markdown(f"### 📄 `{st.session_state.doc_name}` — Ready!")
tab_qa, tab_kpi, tab_summary = st.tabs([
    "💬 Ask Questions",
    "📊 KPI Extraction",
    "📝 Summary",
])

# ── TAB 1: Q&A ───────────────────────────────
with tab_qa:
    suggestions = (
        [
            "What was the total revenue?",
            "What is the net income?",
            "What are the main business risks?",
            "What is the earnings per share (EPS)?",
        ]
        if st.session_state.doc_type == "financial"
        else [
            "What is the readmission rate?",
            "What are key clinical guidelines?",
            "What quality metrics are reported?",
            "What recommendations are made?",
        ]
    )

    st.markdown("**Try a suggested question:**")
    cols = st.columns(4)
    for i, sug in enumerate(suggestions):
        if cols[i].button(sug, key=f"sug_{i}", use_container_width=True):
            st.session_state.pending_q = sug
            st.rerun()

    st.markdown("")

    typed_question = st.text_input(
        "Ask a question about the document:",
        placeholder="e.g. What was the total revenue in 2023?",
        key="question_input",
    )

    if st.session_state.pending_q and not typed_question:
        st.info(f"📌 Selected: **{st.session_state.pending_q}**")

    if st.button("🔍 Get Answer", type="primary"):
        final_question = (
            typed_question.strip()
            if typed_question.strip()
            else st.session_state.pending_q.strip()
        )

        if not final_question:
            st.warning("⚠️ Please type a question or click a suggested question!")
        else:
            st.session_state.pending_q = ""
            with st.spinner("🔍 Searching document and generating answer..."):
                start = time.time()
                try:
                    result = ask_question(
                        st.session_state.rag_chain, final_question
                    )
                    elapsed = round(time.time() - start, 1)
                    st.session_state.qa_history.insert(0, {
                        "question": final_question,
                        "answer": result["answer"],
                        "sources": result["sources"],
                        "time": elapsed,
                    })
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

    st.markdown("")

    if st.session_state.qa_history:
        for qa in st.session_state.qa_history:
            st.markdown(f"**Q: {qa['question']}**")
            st.markdown(
                f'<div class="answer-box">{qa["answer"]}</div>',
                unsafe_allow_html=True,
            )
            with st.expander(
                f"📚 View Sources ({len(qa['sources'])} pages) · ⏱️ {qa['time']}s"
            ):
                for src in qa["sources"]:
                    st.markdown(
                        f'<div class="source-box">'
                        f'<strong>📄 Page {src["page"]}</strong>'
                        f'<br>{src["content"]}</div>',
                        unsafe_allow_html=True,
                    )
            st.markdown("---")
    else:
        st.info("💡 Ask a question above to get started!")

# ── TAB 2: KPI ───────────────────────────────
with tab_kpi:
    st.markdown(f"### Extract KPIs from `{st.session_state.doc_name}`")

    if st.button("🔍 Extract KPIs", type="primary"):
        with st.spinner("Extracting KPIs..."):
            if st.session_state.doc_type == "financial":
                st.session_state.kpis = extract_financial_kpis(
                    st.session_state.full_text
                )
            else:
                st.session_state.kpis = extract_healthcare_kpis(
                    st.session_state.full_text
                )

    if st.session_state.kpis:
        kpis = st.session_state.kpis
        found = {
            k: v for k, v in kpis.items()
            if v and str(v).lower() not in ("none", "null", "")
        }
        st.markdown(
            f"**✅ {len(found)} KPIs found · "
            f"❌ {len(kpis) - len(found)} not in document**"
        )
        if found:
            cols = st.columns(3)
            for i, (key, val) in enumerate(found.items()):
                cols[i % 3].markdown(
                    f'<div class="kpi-card">'
                    f'<div class="kpi-label">{key}</div>'
                    f'<div class="kpi-value">{val}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
        st.markdown("")
        df = pd.DataFrame([
            {
                "KPI": k,
                "Value": v if v else "Not found",
                "Status": "✅" if v else "❌",
            }
            for k, v in kpis.items()
        ])
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Click **Extract KPIs** to automatically pull key metrics.")

# ── TAB 3: SUMMARY ───────────────────────────
with tab_summary:
    st.markdown(f"### Executive Summary of `{st.session_state.doc_name}`")

    if st.button("📝 Generate Summary", type="primary"):
        with st.spinner("Generating summary..."):
            try:
                st.session_state.summary = generate_summary(
                    st.session_state.full_text
                )
            except Exception as e:
                st.error(f"Error: {str(e)}")

    if st.session_state.summary:
        st.markdown(st.session_state.summary)
        st.markdown("")
        st.download_button(
            "⬇️ Download Summary",
            data=st.session_state.summary,
            file_name=f"summary_{st.session_state.doc_name}.txt",
            mime="text/plain",
        )
    else:
        st.info("Click **Generate Summary** to create an executive summary.")