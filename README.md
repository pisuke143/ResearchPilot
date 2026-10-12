# ResearchPilot

ResearchPilot is an AI-powered research-paper assistant intended to help users
search academic papers, retrieve relevant evidence, and obtain answers grounded
in the contents of their documents.

## Project status

This project is being developed in stages. Existing Python modules provide the
starting point; the complete application described in the documentation is the
target system, not a claim that all features already exist.

## Planned capabilities

- PDF ingestion and document validation
- Text extraction and page-aware chunking
- Keyword and semantic retrieval
- Hybrid retrieval and result ranking
- Persistent document metadata and vector indexes
- Evidence-grounded answer generation
- Page-level citations and source inspection
- Search across multiple papers
- Follow-up questions and research sessions
- A user interface
- Testing, evaluation, logging, and error handling
- Setup instructions and reproducible deployment

## Documentation

- `docs/SRS.md` — Software Requirements Specification
- `docs/architecture.md` — current and target architecture
- `docs/development_plan.md` — end-to-end development roadmap
- `docs/module_interfaces.md` — module responsibilities and interfaces
- `docs/data_flow_and_result_format.md` — data structures and processing flow
- `docs/testing_plan.md` — software testing strategy
- `docs/experiment_design.md` — retrieval and answer-quality experiments
- `docs/security_and_risks.md` — security, privacy, and risk management
- `docs/deployment_and_maintenance.md` — packaging and maintenance
- `docs/setup_guide.md` — development environment setup
- `docs/decision_log.md` — architectural decisions
- `docs/traceability_matrix.md` — requirements-to-test mapping

## Development principles

1. Understand existing code before changing it.
2. Build incrementally and test each change.
3. Preserve document and page provenance.
4. Separate document processing, retrieval, answer generation, and UI code.
5. Distinguish implemented features from planned features.
6. Evaluate retrieval and answer quality instead of assuming AI output is correct.
7. Keep sensitive documents private and avoid logging their full contents.
8. Update documentation whenever a significant decision changes.

## Immediate priority

Complete the requirements and architecture, inspect and test the existing
implementation, and then follow the development roadmap in order.

<!-- PERSISTENCE-STATUS-START -->
## Persistence implementation status

- `src/researchpilot/persistence.py` provides functions to save and load a FAISS index and its corresponding chunk metadata.
- `tests/test_persistence.py` tests round-trip behavior, missing files, and index/chunk count consistency.
- Persistence is not yet integrated into `paper_search.py`.
- The saved index and metadata must always remain consistent.
<!-- PERSISTENCE-STATUS-END -->
