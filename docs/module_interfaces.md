# ResearchPilot — Module Interfaces and Responsibilities

## 1. Purpose

This document defines current module responsibilities and proposed future
interfaces. Proposed interfaces are design targets, not claims about existing code.

## 2. Current modules

### `pdf_processing.py`

Responsibility:
- Open PDFs and extract page text.

Expected conceptual output:
- A collection of page records with text and page numbers.

Checks:
- Missing and unreadable files
- Empty pages and empty documents
- Correct page-number conventions

### `text_processing.py`

Responsibility:
- Split text into manageable chunks.

Expected conceptual input:
- Extracted text and chunking settings.

Expected conceptual output:
- Ordered chunks that do not lose their source association.

Checks:
- Empty input
- Very short text
- Long words and whitespace
- Chunk-size boundaries
- Page association

### `pipeline.py`

Responsibility:
- Coordinate extraction and chunking.

Expected output:
- Chunks linked to the page or pages they came from.

### `retrieval.py`

Responsibility:
- Keyword-based search.

Current conceptual score:
- Count of distinct query words that also occur in a chunk.

Limitations:
- Exact token overlap does not understand synonyms or word meaning.
- Score magnitude is not directly comparable to semantic similarity scores.

### `semantic_search.py`

Responsibility:
- Load and reuse the embedding model.
- Encode query and chunk text.
- Rank chunks by semantic similarity.

Important concerns:
- Cache invalidation
- Empty inputs
- Model load failures
- Embedding/chunk ordering
- Similarity-score interpretation

### `vector_store.py`

Responsibility:
- Build a FAISS index from chunk embeddings.
- Search the index and map returned positions to source chunks.

Important invariant:
- The index vector at position N must correspond to the chunk at position N.

### `paper_search.py`

Responsibility:
- Coordinate PDF processing, index construction, and vector search.

Current design limitation:
- It rebuilds the vector index for each call; index persistence and reuse are future improvements.

## 3. Proposed future modules

These names are suggestions and may be adjusted after inspecting the full codebase.

### `config.py`

Responsibility:
- Centralize model names, chunk settings, storage paths, and supported configuration.
- Validate configuration at startup.

### `document_manager.py`

Proposed functions:
- `ingest_document(path, settings)`: validate, process, and register a document.
- `remove_document(document_id)`: remove document records and associated index data safely.
- `list_documents()`: return document metadata.

### `storage.py`

Proposed functions:
- `save_document(document_record)`
- `save_chunks(document_id, chunks)`
- `load_document(document_id)`
- `load_chunks(document_id)`
- `delete_document(document_id)`

Exact signatures depend on the selected storage technology.

### `retrieval_engine.py`

Proposed functions:
- `search_library(query, filters, top_k)`
- `combine_candidates(keyword_results, semantic_results)`
- `rank_candidates(candidates, settings)`

Responsibilities:
- Coordinate retrieval strategies.
- Apply documented ranking and filtering.
- Preserve source metadata.

### `answer_generation.py`

Proposed function:
- `generate_answer(query, evidence, settings)`

Responsibilities:
- Assemble evidence context.
- Call the selected model or service.
- Return a structured answer candidate.
- Handle model errors and insufficient evidence.

### `citation_validation.py`

Proposed functions:
- `validate_citations(answer, evidence)`
- `format_citation(source_record)`

Responsibilities:
- Ensure citations map to valid source records.
- Prevent unknown document or page references from being presented as verified.

### `application_controller.py`

Responsibilities:
- Coordinate UI requests and services.
- Validate request parameters.
- Convert domain results and failures into predictable responses.

### `evaluation.py`

Responsibilities:
- Run fixed evaluation datasets.
- Calculate retrieval metrics.
- Record configuration and results.
- Compare experiments.

### `logging_config.py`

Responsibilities:
- Configure structured logging.
- Redact sensitive values.
- Avoid routine full-document logging.

## 4. Common data contracts

### Chunk record

```python
{
    "chunk_id": "stable-chunk-id",
    "document_id": "stable-document-id",
    "page_number": 1,
    "chunk_index": 0,
    "text": "Passage extracted from a paper."
}
```

The identifiers are proposed fields; the current implementation may use a smaller structure.

### Search result

```python
{
    "document_id": "stable-document-id",
    "chunk_id": "stable-chunk-id",
    "page_number": 1,
    "text": "Retrieved passage.",
    "score": 0.82,
    "retrieval_method": "semantic"
}
```

The score is illustrative, not a quality guarantee.

### Answer response

```python
{
    "answer_text": "Answer supported by retrieved evidence.",
    "citations": [
        {
            "document_id": "stable-document-id",
            "page_number": 1,
            "chunk_id": "stable-chunk-id"
        }
    ],
    "insufficient_evidence": False,
    "warnings": []
}
```

## 5. Interface rules

1. Preserve document identity and page metadata.
2. Validate public function arguments.
3. Define empty-input behavior.
4. Use explicit exceptions for invalid operations.
5. Avoid mixing UI concerns into core retrieval code.
6. Never silently pair an index with a different chunk ordering.
7. Keep return structures documented and tested.
8. Update this document whenever a public interface changes.

## 6. Interface validation checklist

For every public function, document:
- Purpose
- Input types
- Required and optional parameters
- Return structure
- Possible exceptions
- Empty-input behavior
- Side effects
- Unit tests
