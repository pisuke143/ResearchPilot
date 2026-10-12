# ResearchPilot — Data Flow and Result Format

## 1. Purpose

This document defines how information should move through the target system and
how the relationship between a document, chunk, search result, and citation is preserved.

## 2. Ingestion flow

```text
PDF file
  |
  v
Validate file
  |
  v
Extract text page by page
  |
  v
Create page-aware chunks
  |
  v
Assign document and chunk identifiers
  |
  v
Generate embeddings
  |
  v
Build vector index
  |
  v
Save metadata and index when persistence is implemented
```

Each stage should fail clearly. A failed stage must not leave a misleading
record that the document is ready for searching.

## 3. Query flow

```text
Question
  |
  v
Validate query
  |
  v
Keyword and/or semantic retrieval
  |
  v
Combine and rank candidate passages
  |
  v
Select evidence
  |
  v
Check evidence sufficiency
  |
  v
Generate answer when enabled
  |
  v
Validate citations
  |
  v
Format answer and sources
```

## 4. Proposed document record

```python
{
    "document_id": "doc-001",
    "filename": "example-paper.pdf",
    "content_hash": "optional-content-hash",
    "page_count": 12,
    "status": "ready"
}
```

This is an illustrative target schema.

## 5. Proposed chunk record

```python
{
    "chunk_id": "doc-001-chunk-0001",
    "document_id": "doc-001",
    "page_number": 1,
    "chunk_index": 0,
    "text": "The extracted passage goes here."
}
```

If a chunk spans multiple pages, the data model should represent a page range
or explicit source segments rather than assigning a misleading single page.

## 6. Search scores

Different retrieval strategies may produce scores with different meanings.

- Keyword score: may count matching query terms.
- Semantic score: may measure embedding similarity.
- Reranking score: may be produced by a separate ranking model.

Do not compare these scores as if they were automatically on the same scale.
If hybrid retrieval is introduced, document how scores are normalized or how
candidate rankings are combined.

## 7. Citation model

A citation should identify at least:
- Source document
- Page number or page range
- Evidence chunk or source segment

A user-facing citation might display a filename and page number. The internal
identifier should remain available so that the reference can be validated.

Citation formatting must not manufacture page numbers or source documents.

## 8. Insufficient evidence

The system should distinguish among:
- No results returned
- Results returned but not sufficiently relevant
- Relevant evidence found, but it does not answer the full question
- Model or retrieval service failure

These conditions should not all be treated as the same error.

## 9. Index consistency

The vector index and its metadata must share:
- The same document/chunk set
- The same ordering
- Compatible embedding dimensions
- Compatible model and preprocessing configuration

When any relevant property changes, the system must rebuild or reject the stale index.

## 10. Data lifecycle

The planned system should define:
- Ingestion
- Updating a document
- Re-indexing after model or chunking changes
- Deleting a document
- Recovering a missing index
- Clearing optional session history
- Backing up and restoring persistent metadata

## 11. Validation cases

Test at least:
- A normal text-based PDF
- A PDF with empty pages
- A scanned PDF
- A malformed PDF
- A document with repeated text
- A query with no relevant evidence
- A query with evidence on multiple pages
- A missing or stale index
- A citation pointing to an unknown chunk

<!-- PERSISTENCE-STATUS-START -->
## Implemented persistence step

The initial persistence module stores two files:

- `index.faiss`: the FAISS vector index.
- `chunks.json`: the matching chunk records.

The two files must describe the same ordered collection. Loading rejects a
vector/chunk count mismatch.

This initial format does not yet include a manifest containing the embedding
model, dimension, preprocessing configuration, or schema version. Those checks
must be designed before indexes are reused across model or configuration changes.
<!-- PERSISTENCE-STATUS-END -->
