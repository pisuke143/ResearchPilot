"""Utilities for extracting text from PDF documents."""

from pathlib import Path
import pymupdf


def extract_text_from_pdf(pdf_path: str) -> list[dict]:
    """Extract text from a PDF, keeping each page's number."""
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    pages = []

    with pymupdf.open(pdf_path) as document:
        for page_number, page in enumerate(document, start=1):
            pages.append({
                "page_number": page_number,
                "text": page.get_text(),
            })

    return pages
