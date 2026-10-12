"""Utilities for extracting text from PDF documents."""

from pathlib import Path
import pymupdf


def extract_text_from_pdf(pdf_path: str) -> list[dict]:
    """Extract text from a PDF, keeping each page's number."""
    pdf_path = Path(pdf_path)
    # check if the PDF file exists at that location before trying to open it
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    # empty list of pages
    pages = []
    # using pymupdf to open the PDF and extract text from each page
    with pymupdf.open(pdf_path) as document:
        # iterate through each page in the PDF, starting with page number 1
        for page_number, page in enumerate(document, start=1):
            # extract the text from the page and append it to the list of pages
            pages.append({
                "page_number": page_number,
                "text": page.get_text(),
            })

    return pages
