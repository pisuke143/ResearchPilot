# ResearchPilot — Software Architecture Document

## 1. Purpose

This document describes the architecture planned for the complete ResearchPilot
application and distinguishes it from the current implementation.

The design should evolve through small, testable changes rather than a large rewrite.

## 2. Architecture principles

1. Separate responsibilities.
2. Preserve document and page provenance through every processing stage.
3. Treat retrieved text as evidence, not automatic proof of a claim.
4. Keep retrieval and answer generation independently testable.
5. Store vectors and their corresponding metadata consistently.
6. Keep configuration outside core business logic where practical.
7. Make failures observable and recoverable.
8. Avoid adding a component until a requirement justifies it.

## 3. Current implementation versus target

### Existing foundation (verify against the current code)

- `pdf_processing.py`: PDF text extraction.
- `text_processing.py`: text chunking.
- `pipeline.py`: extraction and chunking orchestration.
- `retrieval.py`: keyword-based retrieval.
- `semantic_search.py`: Sentence Transformers embeddings and semantic search.
- `vector_store.py`: FAISS index construction and search.
- `paper_search.py`: end-to-end PDF search orchestration.
- `tests/`: existing tests that must be rerun before relying on them.

### Target components not yet assumed to exist

- Document/library manager.
- Persistent metadata and index storage.
- Hybrid retrieval and reranking.
- Answer generation and citation validation.
- Application controller/API.
- User interface.
- Session and conversation management.
- Centralized configuration, logging, evaluation, and deployment support.

## 4. Target logical architecture

```text
                         USER
                          |
                          v
                +-------------------+
                | User Interface    |
                | Upload / Search   |
                | Answers / Sources |
                +---------+---------+
                          |
                          v
                +-------------------+
                | Application       |
                | Controller        |
                +---------+---------+
                          |
              +-----------+-----------+
              |                       |
              v                       v
     +----------------+      +----------------+
     | Document       |      | Query and       |
     | Ingestion      |      | Session Logic   |
     +--------+-------+      +--------+-------+
              |                       |
              v                       v
     +----------------+      +----------------+
     | Extraction and |      | Retrieval      |
     | Chunking       |      | Orchestrator   |
     +--------+-------+      +--------+-------+
              |                       |
              v              +--------+--------+
     +----------------+       |                 |
     | Embedding and  |       v                 v
     | Index Builder  |  +---------+     +-------------+
     +--------+-------+  | Keyword |     | Vector      |
              |          | Search  |     | Search      |
              |          +----+----+     +------+------+
              |               |                 |
              |               +--------+--------+
              |                        |
              v                        v
     +----------------+       +----------------+
     | Persistent     |       | Ranking and    |
     | Library Store  |<----->| Evidence Select|
     +----------------+       +--------+-------+
                                       |
                                       v
                              +------------------+
                              | Answer Generator |
                              +--------+---------+
                                       |
                                       v
                              +------------------+
                              | Citation Checker |
                              +--------+---------+
                                       |
                                       v
                              +------------------+
                              | Response Formatter|
                              +--------+---------+
                                       |
                                       v
                                     USER
```

Logging, configuration, validation, and evaluation support the relevant layers.

## 5. Component responsibilities

### 5.1 User interface

Accept document selection and questions. Display progress, search results,
answers, citations, and error messages. It should not implement embedding
calculation or ranking algorithms itself.

### 5.2 Application controller

Coordinate user requests and call domain services. Validate request parameters,
manage application-level errors, and return a consistent response structure.

### 5.3 Ingestion

Validate files, extract page text, chunk content, assign stable document and chunk
identifiers, and retain metadata needed to locate original evidence.

### 5.4 Embedding and index builder

Generate embeddings for chunks and build the selected vector index. Save or
register the index only alongside metadata that matches its vector ordering.

### 5.5 Retrieval orchestrator

Coordinate keyword and vector search, combine candidates when hybrid retrieval
is enabled, rank results, apply result limits, and return source-linked passages.

### 5.6 Answer generator

Use selected passages to produce an answer. The generator must not be treated as
a source of truth independent of the retrieved evidence.

### 5.7 Citation checker

Validate that cited document and page references correspond to known retrieved
records. Invalid citations must not be presented as verified citations.

### 5.8 Persistent library store

Store document metadata, chunks, index metadata, and any approved session history.
The concrete database and index persistence format remain design decisions.

### 5.9 Evaluation and observability

Record operational timings and errors. Run repeatable retrieval and answer-quality
experiments. Avoid storing full private document text in routine logs.

## 6. Target request flow

1. The user selects one or more papers.
2. The ingestion service validates each paper.
3. Text is extracted page by page.
4. Text is split into chunks with source metadata.
5. Embeddings are generated and indexed.
6. Document and index metadata are persisted when storage is implemented.
7. A user submits a question.
8. The retrieval orchestrator searches the available library.
9. Candidate passages are ranked and selected.
10. The system determines whether enough evidence is available.
11. If answer generation is enabled and evidence is sufficient, a grounded answer is generated.
12. Citations are checked against the retrieved source records.
13. The final response is formatted and shown to the user.

## 7. Proposed data model

### Document

- `document_id`: stable internal identifier
- `filename`: display filename
- `content_hash`: optional content fingerprint
- `page_count`: number of pages, if available
- `status`: processing status
- `created_at`: ingestion time, if recorded
- `metadata`: supported optional document metadata

### Chunk

- `chunk_id`: stable identifier
- `document_id`: parent document
- `page_number` or page range
- `text`: extracted passage
- `chunk_index`: order within the document
- `embedding_reference`: optional storage reference

### Search result

- `document_id`
- `chunk_id`
- `text`
- `page_number` or page range
- `score`
- `retrieval_method`, where useful

### Answer

- `answer_text`
- `citations`
- `evidence_chunk_ids`
- `insufficient_evidence` or equivalent status
- `warnings`, if applicable

These are proposed logical models. They do not assert that every field exists in
the current code.

## 8. Error handling

The system should distinguish among:

- Invalid input path
- Unsupported or malformed PDF
- Empty extracted text
- Model load failure
- Embedding failure
- Index creation or load failure
- Retrieval failure
- Answer generation failure
- Citation validation failure
- Storage failure
- User cancellation

Errors should preserve enough context to diagnose the failure without exposing
private document contents unnecessarily.

## 9. Scalability and performance

The initial system may use local processing and an in-memory index while the
document collection is small. Persistent indexes and more advanced retrieval
should be introduced only when their requirements and tests are defined.

Potential optimizations include model reuse, embedding caching, batched ingestion,
index reuse, and limiting the amount of context sent to a generator.

## 10. Architectural decisions still open

- UI framework and application delivery method
- Local model versus remote answer-generation API
- Persistent database and vector-index format
- Index versioning and rebuild policy
- OCR support
- Hybrid retrieval and reranking method
- Session history and deletion behavior
- Supported operating systems and packaging format

<!-- PERSISTENCE-STATUS-START -->
## Persistence implementation update

The project now has a separate persistence module for writing and reading FAISS
indexes and JSON chunk metadata.

The current implementation is a first step, not a complete document library.
It does not yet provide document registration, index versioning, automatic
index reuse, multi-document management, or integration with the main search flow.

Before relying on saved indexes, test round-trip loading, damaged metadata,
interrupted writes, and index compatibility.
<!-- PERSISTENCE-STATUS-END -->
