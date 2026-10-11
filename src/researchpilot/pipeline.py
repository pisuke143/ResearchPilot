"""Combine PDF extraction and text chunking."""

from researchpilot.pdf_processing import extract_text_from_pdf
from researchpilot.text_processing import split_into_chunks


def process_pdf(pdf_path: str, chunk_size: int = 500) -> list[dict]:
    """Extract a PDF's text and split it into page-linked chunks."""
    pages = extract_text_from_pdf(pdf_path)
    all_chunks = []

    for page in pages:
        chunks = split_into_chunks(page["text"], chunk_size)

        for chunk in chunks:
            all_chunks.append({
                "page_number": page["page_number"],
                "text": chunk,
            })

    return all_chunks
