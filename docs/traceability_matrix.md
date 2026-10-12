# ResearchPilot — Requirements Traceability Matrix

## Status definitions

- **Existing — verification pending:** A related module exists, but the requirement has not yet been verified completely.
- **Planned:** The feature is intended for a future development phase.
- **Verified:** Tests and implementation evidence demonstrate the requirement is satisfied.
- **Blocked:** Work cannot proceed until a dependency or decision is resolved.

## Current implementation baseline

The project contains these modules:

- `pdf_processing.py`
- `text_processing.py`
- `pipeline.py`
- `retrieval.py`
- `semantic_search.py`
- `vector_store.py`
- `paper_search.py`

The latest observed test run passed 21 tests. This is a baseline observation,
not proof that every requirement below is satisfied.

## Requirements matrix

| ID | Requirement | Related module or component | Status |
|---|---|---|---|
| FR-001 | Accept PDF input | `pdf_processing.py` | Existing — verification pending |
| FR-002 | Validate input files | Ingestion | Existing — verification pending |
| FR-003 | Extract PDF text | `pdf_processing.py` | Existing — verification pending |
| FR-004 | Preserve source page information | `pipeline.py` | Existing — verification pending |
| FR-006 | Split text into chunks | `text_processing.py` | Existing — verification pending |
| FR-010 | Keyword retrieval | `retrieval.py` | Existing — verification pending |
| FR-011 | Semantic retrieval | `semantic_search.py` | Existing — verification pending |
| FR-012 | Validate result count | Search modules | Existing — verification pending |
| FR-013 | Rank search results | Retrieval modules | Existing — verification pending |
| FR-014 | Preserve source metadata in results | Search modules | Existing — verification pending |
| FR-016 | Combine keyword and semantic retrieval | Future retrieval engine | Planned |
| FR-017 | Measure retrieval quality | Evaluation tooling | Planned |
| FR-018 | Handle insufficient search evidence | Retrieval workflow | Planned |
| FR-019 | Search across multiple papers | Document library | Planned |
| FR-020 | Persist document metadata | Storage layer | Planned |
| FR-021 | Save and reload vector indexes | Vector storage | Planned |
| FR-022 | Keep index and chunk ordering consistent | Vector storage | Existing design concern; verify |
| FR-025 | Generate evidence-grounded answers | Answer generation | Planned |
| FR-026 | Attach page-level citations | Answer and citation components | Planned |
| FR-027 | Validate citations | Citation validator | Planned |
| FR-028 | Handle questions without sufficient evidence | Answer generation | Planned |
| FR-031 | Provide document selection UI | User interface | Planned |
| FR-032 | Accept questions through the UI | User interface | Planned |
| FR-033 | Display ranked passages | User interface | Planned |
| FR-034 | Let users inspect source citations | User interface | Planned |
| FR-035 | Support follow-up questions | Session management | Planned |
| FR-037 | Centralize application configuration | Configuration module | Planned |
| FR-038 | Provide useful operational logging | Logging module | Planned |
| FR-039 | Document reproducible setup | README and setup guide | Documentation created; verify instructions |
| FR-040 | Automate critical tests | `tests/` | Existing tests; broader coverage pending |

## Next actions

1. Inspect the implementation audit.
2. Verify current function behavior against the requirements.
3. Run tests for the affected modules.
4. Change a requirement's status only when evidence supports it.
5. Implement future requirements in dependency order.

<!-- PERSISTENCE-STATUS-START -->
## Persistence implementation tracking

| Requirement | Implementation | Evidence needed | Status |
|---|---|---|---|
| FR-020 Persistent document metadata | `persistence.py` currently saves chunk metadata | Save/load tests and schema review | In progress |
| FR-021 Save and reload vector index | `persistence.py` | Round-trip test and integration test | In progress |
| FR-022 Index/chunk consistency | `persistence.py` | Mismatch and compatibility tests | Partial; count check implemented |
| FR-024 Recover from missing or incompatible index | Future storage/recovery logic | Recovery tests | Planned |

The existence of a persistence module does not mean the full persistent library
requirement is satisfied.
<!-- PERSISTENCE-STATUS-END -->
