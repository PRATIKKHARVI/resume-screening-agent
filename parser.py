# parser.py
import io
from typing import Tuple
import pdfplumber
from docx import Document

def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
    return "\n".join(text)

def extract_text_from_docx(file_bytes: bytes) -> str:
    from io import BytesIO
    doc = Document(BytesIO(file_bytes))
    paragraphs = [p.text for p in doc.paragraphs if p.text]
    return "\n".join(paragraphs)

def parse_uploaded_file(uploaded) -> Tuple[str, str]:
    """
    uploaded: Streamlit uploaded file object (has .name and .getvalue())
    returns (filename, extracted_text)
    """
    name = uploaded.name
    data = uploaded.getvalue()
    lower = name.lower()
    if lower.endswith(".pdf"):
        return name, extract_text_from_pdf(data)
    if lower.endswith(".docx"):
        return name, extract_text_from_docx(data)
    if lower.endswith(".txt"):
        return name, data.decode("utf-8", errors="ignore")
    # fallback to text decode
    try:
        return name, data.decode("utf-8", errors="ignore")
    except Exception:
        return name, ""
