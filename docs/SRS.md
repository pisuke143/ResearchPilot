# ResearchPilot — Software Requirements Specification

**Document status:** Initial baseline; requirements require review and validation.
**Version:** 1.0
**Project:** ResearchPilot

## 1. Introduction

### 1.1 Purpose

This document specifies the intended requirements for ResearchPilot, an
AI-powered research-paper assistant. It establishes the system scope,
functional behavior, quality expectations, constraints, and acceptance criteria.

It is the reference point for architecture, implementation, testing, and release.

### 1.2 Product vision

A user should be able to provide academic papers, ask a research question,
find relevant passages, inspect their sources, and receive an answer supported
by identifiable evidence in those papers.

The system must distinguish between what the documents support and what
cannot be established from the available evidence.

### 1.3 Intended audience

- Project developer
- Software reviewers and evaluators
- Testers
- Future contributors
- End users of the completed application

### 1.4 Terminology

- **PDF ingestion:** opening a PDF and preparing its content for use.
- **Chunk:** a manageable passage of extracted document text.
- **Embedding:** a numeric representation of text used for semantic comparison.
- **Vector index:** a structure that helps search numeric embeddings.
- **Retrieval:** selecting passages relevant to a query.
- **RAG:** retrieval-augmented generation; generating an answer using retrieved evidence.
- **Citation:** a reference connecting a claim or passage to its source document and page.
- **Persistence:** saving information so it remains available after a restart.
- **Acceptance criterion:** a condition that must be met for a requirement to count as complete.

## 2. Scope

### 2.1 In scope

The intended system includes:

1. PDF document ingestion and validation.
2. Text extraction and page-aware chunking.
3. Document and chunk metadata.
4. Keyword-based search.
5. Semantic search using embeddings.
6. Vector indexing and similarity search.
7. Retrieval evaluation and ranking improvements.
8. Persistent storage for supported document and index data.
9. Evidence-grounded answer generation.
10. Page-level source citations and evidence inspection.
11. Multi-paper search, subject to the final storage design.
12. Follow-up questions and research sessions, if included in the approved release scope.
13. A user interface for uploading documents, asking questions, and viewing results.
14. Error handling, logging, configuration, and testing.
15. Setup, deployment, and maintenance documentation.

### 2.2 Out of scope unless explicitly approved

- Training a foundation language model from scratch.
- Guaranteeing that every answer is correct.
- Automatically accessing paywalled papers or bypassing access controls.
- Performing a complete systematic literature review without human oversight.
- Replacing expert interpretation or peer review.
- Supporting every file format from the first release.
- Multi-user cloud hosting, accounts, and enterprise permissions unless selected later.
- OCR for scanned PDFs until the OCR requirement and implementation are approved.

### 2.3 Product boundaries

ResearchPilot processes documents provided through its supported input workflow.
The answer generator, if enabled, must use retrieved evidence as its grounding
source. External web research is not assumed to be part of the initial product.

## 3. Stakeholders and user classes

### 3.1 Researcher or student

Needs to upload papers, ask questions, locate relevant passages, and verify
the original source before relying on a response.

### 3.2 Developer

Needs maintainable modules, documented interfaces, reproducible setup,
automated tests, and understandable errors.

### 3.3 Evaluator or reviewer

Needs clear requirements, evidence that tests were performed, and measured
results rather than unsupported quality claims.

## 4. Assumptions and constraints

### 4.1 Assumptions

- Users provide PDFs they are permitted to use.
- Many PDFs contain extractable text, but some may be scanned or malformed.
- Model downloads may require an internet connection during setup.
- Local hardware and available memory may limit model and document size.
- Research questions may be ambiguous or impossible to answer from the supplied papers.

### 4.2 Constraints

- The existing project is written in Python.
- Development currently uses Windows, VS Code, PowerShell, and a Python virtual environment.
- Existing dependencies include PyMuPDF, Sentence Transformers, PyTorch, NumPy, FAISS, and unittest.
- Dependency versions must be verified from the actual environment before a reproducible release is defined.
- A local-first deployment is the initial planning assumption, subject to confirmation.
- The system must preserve the connection between every retrieved chunk and its source.

## 5. Functional requirements

Requirement identifiers must remain stable so that implementation and tests can
refer to them.

### 5.1 Document ingestion

**FR-001 — Accept PDF input:** The system shall accept a PDF through its supported input workflow.

**FR-002 — Validate input:** The system shall detect missing paths, unsupported files,
unreadable PDFs, and other ingestion errors and report a useful message.

**FR-003 — Extract text:** The system shall extract available text from each supported PDF.

**FR-004 — Preserve provenance:** Extracted content shall retain the document identity
and source page number.

**FR-005 — Handle empty extraction:** The system shall report when a PDF produces no
usable text instead of pretending that processing succeeded.

**FR-006 — Chunk text:** The system shall divide extracted text into manageable passages
using a configurable chunking policy.

**FR-007 — Preserve chunk metadata:** Each chunk shall be associated with its source
document and page or page range.

**FR-008 — Avoid duplicate ingestion:** The planned document manager should detect
re-ingestion of the same document where a stable identifier or content hash is available.

**FR-009 — Report processing status:** The completed application should expose useful
success, failure, and processing-status information.

### 5.2 Search and retrieval

**FR-010 — Keyword retrieval:** The system shall support lexical matching of query words
against indexed passages.

**FR-011 — Semantic retrieval:** The system shall support semantic retrieval using text
embeddings.

**FR-012 — Configurable result count:** The search workflow shall allow a valid requested
result count and reject invalid values.

**FR-013 — Ranked results:** The system shall return passages ordered according to the
selected retrieval or ranking strategy.

**FR-014 — Source metadata:** Each search result shall preserve its source document,
page information, text, and retrieval score where applicable.

**FR-015 — Empty query handling:** An empty or whitespace-only query shall not trigger
unnecessary expensive processing.

**FR-016 — Hybrid retrieval:** The planned retrieval engine should combine lexical and
semantic evidence when evaluation demonstrates that the combined approach is useful.

**FR-017 — Ranking evaluation:** Retrieval changes shall be evaluated against a
documented test set before being accepted.

**FR-018 — No-evidence handling:** The system shall be able to report that no sufficiently
relevant evidence was found, based on a documented policy.

**FR-019 — Multi-paper retrieval:** The target application should support retrieval across
multiple ingested papers if this remains in the approved release scope.

### 5.3 Storage and document management

**FR-020 — Persistent metadata:** The completed application shall save document metadata
and the information needed to identify source passages.

**FR-021 — Index persistence:** The completed application should save and reload vector
indexes and their associated chunk metadata.

**FR-022 — Index consistency:** An index shall only be used with the exact ordered
metadata collection that corresponds to its vectors.

**FR-023 — Document removal:** If document management is included in the release,
removing a document shall also handle its associated chunks and index entries safely.

**FR-024 — Recovery:** A missing, incompatible, or corrupted saved index shall be detected
and handled through a documented recovery or rebuild procedure.

### 5.4 Answer generation and citations

**FR-025 — Evidence-grounded answers:** The planned answer generator shall use retrieved
passages as its evidence source.

**FR-026 — Traceable citations:** Generated answers shall provide citations that map to
source documents and page numbers.

**FR-027 — Citation validation:** The system shall verify that every emitted citation
refers to an actual retrieved source record.

**FR-028 — Insufficient evidence:** When the available evidence does not support an answer,
the system shall communicate the limitation instead of inventing support.

**FR-029 — Claim verification:** The system should make it possible to inspect the evidence
supporting a response and identify unsupported claims during evaluation.

**FR-030 — Separate evidence from inference:** The answer format should distinguish
directly supported information from uncertainty or interpretation where necessary.

### 5.5 User interaction

**FR-031 — Document selection:** The target UI shall let users select or upload supported papers.

**FR-032 — Question input:** The target UI shall provide a way to submit a research question.

**FR-033 — Results display:** The target UI shall display ranked passages and their sources.

**FR-034 — Citation inspection:** Users should be able to inspect the cited passage and its
source page or document metadata.

**FR-035 — Follow-up questions:** If included in the approved scope, users shall be able to
ask a follow-up question with clearly defined session context.

**FR-036 — Clear feedback:** The UI shall display understandable loading, empty-result,
and error states.

### 5.6 Operations and configuration

**FR-037 — Configuration:** Model selection, chunking parameters, retrieval settings, and
storage paths should be configurable without unnecessary code changes.

**FR-038 — Logging:** The application shall record useful operational events and errors
without routinely logging full private document contents.

**FR-039 — Reproducible setup:** The project shall document environment setup,
dependency installation, and test execution.

**FR-040 — Automated tests:** The project shall provide automated tests for critical
processing, retrieval, persistence, citation, and error-handling behavior.

## 6. Non-functional requirements

**NFR-001 — Correctness:** Processing and retrieval must preserve source associations.
Tests must detect incorrect page references and index-to-chunk mismatches.

**NFR-002 — Reliability:** Invalid inputs and recoverable failures must produce controlled
errors rather than unexplained crashes.

**NFR-003 — Performance:** The project shall measure ingestion and query latency on a
documented test corpus. Numerical performance targets will be set after a baseline is measured.

**NFR-004 — Retrieval quality:** Search quality shall be measured using labelled queries
and appropriate ranking metrics.

**NFR-005 — Answer quality:** Generated answers shall be evaluated for evidence support,
citation correctness, relevance, and appropriate abstention.

**NFR-006 — Maintainability:** Extraction, chunking, indexing, retrieval, generation,
storage, and presentation shall have separate responsibilities.

**NFR-007 — Testability:** Core processing and ranking logic should be testable without
requiring a full UI session.

**NFR-008 — Portability:** Setup and dependency assumptions shall be documented.
Additional operating systems are not guaranteed until tested.

**NFR-009 — Security:** The application shall validate inputs and treat document contents
as untrusted data.

**NFR-010 — Privacy:** Local documents should remain local under the local-first design.
Any future external model or API integration must document what data leaves the machine.

**NFR-011 — Usability:** Errors and unsupported operations should be described in language
that a non-expert user can understand.

**NFR-012 — Reproducibility:** Evaluation results shall record relevant configuration,
model identifiers, corpus details, and test-set versions.

## 7. Main use cases

### UC-01: Ingest a research paper

1. The user selects a PDF.
2. The system validates and opens it.
3. The system extracts page text.
4. The system splits text into chunks and attaches metadata.
5. The system reports success or a meaningful failure.
6. When persistence is implemented, the system saves the document records.

**Success condition:** Usable chunks retain their source document and page information.

### UC-02: Search a paper

1. The user submits a question.
2. The system validates the query.
3. The retrieval engine searches the available chunks.
4. Results are ranked and limited to the requested count.
5. The system displays passages, scores where useful, and source references.

**Success condition:** Results can be traced back to their source passages.

### UC-03: Ask a question and receive an evidence-based answer

1. The user submits a question.
2. The system retrieves relevant passages.
3. The system evaluates whether sufficient evidence is available.
4. The answer generator produces a response from the evidence.
5. Citations are attached and validated.
6. The response is displayed with source inspection options.

**Success condition:** Citations are valid, and unsupported questions are handled honestly.

### UC-04: Restart and reuse an existing library

1. The user starts the application.
2. The system loads saved document metadata and indexes.
3. The system checks compatibility and consistency.
4. The user searches previously ingested papers.

**Success condition:** Saved content can be reused without silently mismatching vectors and chunks.

### UC-05: Handle a processing failure

1. The user provides an invalid or unreadable file.
2. The system detects the failure.
3. The system reports what failed and, where possible, how to recover.
4. No misleading successful document record is created.

## 8. Acceptance criteria

The project is not complete merely because the program starts.

The final release should demonstrate that:

- Supported PDFs can be ingested and source page information is preserved.
- Invalid and empty inputs are handled correctly.
- Keyword and semantic retrieval execute successfully.
- Search results map to the correct source chunks.
- Retrieval quality is evaluated on a documented test set.
- Persistent data can be reloaded and checked for consistency.
- Generated answers, if enabled, have valid source citations.
- Insufficient evidence is handled appropriately.
- The intended UI workflow works from document selection through result inspection.
- Critical automated tests pass in the documented environment.
- Setup, usage, limitations, and known issues are documented.
- Performance and quality results are reported honestly.

Specific numeric thresholds will be agreed upon after baseline evaluation.

## 9. Risks and open questions

- How should scanned PDFs be handled: unsupported, OCR-enabled, or deferred?
- Which language model will generate answers, and will it run locally or through an API?
- Which persistent storage approach best fits the project scale?
- Which UI framework will be selected?
- Should the first release support multiple papers and sessions?
- What corpus and relevance labels will be used for retrieval evaluation?
- What latency and retrieval-quality targets are achievable on the development hardware?
- What document deletion and data-retention behavior is required?

These decisions must be recorded rather than silently assumed.

## 10. Requirement change management

When requirements change:

1. Update this document.
2. Record the reason in `decision_log.md`.
3. Review affected architecture and interfaces.
4. Update the traceability matrix.
5. Add or update tests.
6. Verify the implementation before marking the requirement complete.
