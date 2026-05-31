import pdfplumber
import PyPDF2
from langchain_core.documents import Document


def extract_documents(pdf_file):
    documents = []
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text and text.strip():
                    documents.append(Document(
                        page_content=text.strip(),
                        metadata={
                            "page": i + 1,
                            "total_pages": len(pdf.pages),
                            "source": getattr(pdf_file, "name", "uploaded_pdf"),
                        }
                    ))
    except Exception as e:
        print(f"pdfplumber failed: {e}, trying PyPDF2...")
        pdf_file.seek(0)
        reader = PyPDF2.PdfReader(pdf_file)
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text and text.strip():
                documents.append(Document(
                    page_content=text.strip(),
                    metadata={
                        "page": i + 1,
                        "total_pages": len(reader.pages),
                        "source": getattr(pdf_file, "name", "uploaded_pdf"),
                    }
                ))
    return documents


def get_full_text(documents):
    return "\n\n".join([doc.page_content for doc in documents])