# core/parser.py

import io
from pypdf import PdfReader
from docx import Document

SUPPORTED_EXTENSIONS = {".txt", ".pdf", ".docx", ".doc"}

def extract_text(content: bytes, filename: str) -> str:
    """
    Extract plain text from an uploaded file based on its extension.

    Supported formats:
        .txt   → decoded as UTF-8
        .pdf   → extracted page by page using pypdf
        .docx  → extracted paragraph by paragraph using python-docx
        .doc   → not natively supported (legacy format), raises error

    Args:
        content:  Raw file bytes
        filename: Original filename (used to detect format)

    Returns:
        Extracted plain text string
    """
    name = filename.lower()

    if name.endswith(".txt"):
        return _extract_txt(content)

    elif name.endswith(".pdf"):
        return _extract_pdf(content)

    elif name.endswith(".docx"):
        return _extract_docx(content)

    elif name.endswith(".doc"):
        raise ValueError(
            "Legacy .doc format is not supported. "
            "Please convert to .docx (Save As → .docx in Word) and re-upload."
        )

    else:
        ext = filename.rsplit(".", 1)[-1] if "." in filename else "unknown"
        raise ValueError(f"Unsupported file type: .{ext}. Allowed: .txt, .pdf, .docx")


def _extract_txt(content: bytes) -> str:
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError:
        # Fallback to latin-1 which never fails
        return content.decode("latin-1")


def _extract_pdf(content: bytes) -> str:
    reader = PdfReader(io.BytesIO(content))
    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text and text.strip():
            pages.append(text.strip())
    if not pages:
        raise ValueError("PDF appears to be empty or contains only scanned images (no extractable text).")
    return "\n\n".join(pages)


def _extract_docx(content: bytes) -> str:
    doc = Document(io.BytesIO(content))
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    if not paragraphs:
        raise ValueError("Word document appears to be empty.")
    return "\n\n".join(paragraphs)
