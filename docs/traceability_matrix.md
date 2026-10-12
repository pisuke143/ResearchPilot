# ResearchPilot — Requirements Traceability Matrix

## Purpose

This matrix connects SRS requirements to implementation modules and tests.
It should be updated as the project evolves.

The file names below are suggested mappings. Verify actual implementation and
test coverage before marking a requirement complete.

| Requirement | Planned implementation area | Test evidence | Initial status |
|---|---|---|---|
| FR-001 PDF input | `pdf_processing.py`, document manager | PDF input tests | Existing foundation; verify |
| FR-002 Input validation | ingestion layer | Invalid path and malformed PDF tests | Verify |
| FR-003 Text extraction | `pdf_processing.py` | Extraction tests | Existing foundation; verify |
| FR-004 Provenance | processing pipeline | Page metadata tests | Existing foundation; verify |
| FR-006 Chunking | `text_processing.py` | Chunk boundary tests | Existing foundation; verify |
| FR-010 Keyword search | `retrieval.py` | Keyword retrieval tests | Existing foundation; verify |
| FR-011 Semantic search | `semantic_search.py` | Semantic search tests | Existing foundation; verify |
| FR-013 Ranked results | retrieval engine | Ranking tests | Existing foundation; verify |
| FR-014 Source metadata | search modules | Source mapping tests | Verify |
| FR-016 Hybrid retrieval | retrieval engine | Comparative retrieval tests | Planned |
| FR-017 Retrieval evaluation | evaluation tooling | Evaluation report | Planned |
| FR-020 Persistent metadata | storage layer | Save/reload tests | Planned |
| FR-021 Persistent index | vector store and storage | Index reload tests | Planned |
| FR-025 Grounded answers | answer generation | Evidence support tests | Planned |
| FR-026 Citations | answer and citation layers | Citation correctness tests | Planned |
| FR-027 Citation validation | citation validator | Invalid citation tests | Planned |
| FR-028 Insufficient evidence | retrieval and answer layers | No-evidence tests | Planned |
| FR-031 Document UI | UI layer | UI workflow tests | Planned |
| FR-032 Question input | UI/controller | Query submission tests | Planned |
| FR-033 Results display | UI layer | Result rendering tests | Planned |
| FR-038 Logging | logging configuration | Redaction and error logging tests | Planned |
| FR-039 Setup instructions | README and setup guide | Clean-environment walkthrough | Planned |
| FR-040 Automated tests | `tests/` | Test-run report | Existing foundation; verify |

## Status definitions

- **Planned:** not implemented.
- **In progress:** implementation exists but is incomplete.
- **Implemented:** code exists and has been inspected.
- **Verified:** implementation and relevant tests demonstrate the requirement.
- **Blocked:** work cannot proceed because a dependency or decision is unresolved.

A module existing does not automatically mean every related requirement is verified.

## Update procedure

When a requirement changes:
1. Update `SRS.md`.
2. Update this matrix.
3. Identify the affected implementation and tests.
4. Run the relevant tests.
5. Update the status only when evidence supports it.
