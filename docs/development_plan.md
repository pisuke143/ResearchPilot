# ResearchPilot — End-to-End Development Plan

## 1. Purpose

This roadmap describes the intended project from requirements through release.
A phase is complete only when its deliverables and exit criteria are satisfied.

## 2. Working method

- Work on one small, understandable change at a time.
- Inspect the current implementation before changing it.
- Establish a test baseline before significant refactoring.
- Run relevant tests after each change.
- Keep documentation synchronized with code.
- Do not begin dependent work while essential earlier decisions remain unresolved.

## 3. Phases

### Phase 1 — Requirements and scope

Tasks:
- Review `SRS.md`.
- Confirm user workflows and release scope.
- Decide which features are required for the first usable release.
- Define measurable acceptance criteria.
- Record unresolved decisions.

Deliverables:
- Reviewed SRS
- Initial acceptance criteria
- Prioritized requirements

Exit criteria:
- Each required feature has an identifier and a way to test it.

### Phase 2 — Architecture and design

Tasks:
- Review the target architecture.
- Define module boundaries and data structures.
- Specify module interfaces.
- Choose UI, storage, and answer-generation approaches when needed.
- Record decisions and trade-offs.

Deliverables:
- Architecture document
- Interface document
- Decision log

Exit criteria:
- The implementation sequence and dependencies are clear.

### Phase 3 — Audit the existing code

Tasks:
- Inspect every current Python module.
- Understand current function inputs and outputs.
- Run the existing test suite.
- Record failures and dependency versions.
- Verify page metadata and score behavior.
- Identify duplicate or overlapping search paths.

Deliverables:
- Current-state code inventory
- Test baseline
- List of known defects and limitations

Exit criteria:
- Existing behavior is understood and reproducible.

### Phase 4 — Stabilize document processing

Tasks:
- Test PDF validation and extraction.
- Test empty, malformed, and scanned documents.
- Verify page numbering.
- Test chunk boundaries and configurable chunk sizes.
- Decide whether overlap and OCR are necessary.

Deliverables:
- Reliable ingestion and chunking
- Tests for edge cases

Exit criteria:
- Processed chunks preserve source provenance.

### Phase 5 — Evaluate and improve retrieval

Tasks:
- Build a representative query-and-evidence dataset.
- Establish a baseline for keyword and semantic search.
- Measure ranking quality.
- Inspect incorrect and irrelevant results.
- Consider hybrid retrieval, score normalization, filters, and reranking.
- Keep only changes that show measured benefits.

Deliverables:
- Evaluation dataset
- Baseline report
- Improved retrieval implementation, if justified

Exit criteria:
- Retrieval quality is measured and limitations are documented.

### Phase 6 — Persistent document library

Tasks:
- Select a metadata storage approach.
- Define stable document and chunk identifiers.
- Save document metadata and processed chunks.
- Persist and reload vector indexes.
- Version indexes and embedding-model settings.
- Test deletion, rebuilding, and corrupted storage recovery.

Deliverables:
- Persistent library
- Index lifecycle handling
- Persistence tests

Exit criteria:
- Restarting the application does not silently lose the saved library.

### Phase 7 — Evidence-grounded answer generation

Tasks:
- Select the answer-generation model or service.
- Define prompt and context assembly.
- Generate answers only from selected evidence.
- Define behavior when evidence is insufficient.
- Validate citations against retrieved chunks.
- Evaluate hallucination and citation errors.

Deliverables:
- Answer-generation service
- Citation validation
- Grounded-answer evaluation

Exit criteria:
- Answers are traceable and insufficient evidence is handled explicitly.

### Phase 8 — Complete research workflow

Tasks:
- Add multi-paper search if in scope.
- Add follow-up questions if in scope.
- Define session context boundaries.
- Implement document selection and result inspection workflows.
- Test end-to-end interactions.

Deliverables:
- Complete application workflow
- Integration tests

Exit criteria:
- A user can complete the intended research task from input to evidence review.

### Phase 9 — User interface

Tasks:
- Select the UI framework.
- Build document selection and status views.
- Add question input and result display.
- Display answers, citations, source pages, and errors.
- Add loading and empty states.
- Test usability with representative tasks.

Deliverables:
- Working UI
- UI usage instructions

Exit criteria:
- Core workflows work without manually calling Python functions.

### Phase 10 — Quality, security, and performance

Tasks:
- Run unit, integration, and end-to-end tests.
- Test malicious and malformed inputs.
- Review privacy and logging behavior.
- Measure ingestion and query latency.
- Test storage recovery and model failures.
- Fix release-blocking defects.

Deliverables:
- Test report
- Risk review
- Performance baseline
- Known-issues list

Exit criteria:
- Release acceptance criteria are met or exceptions are explicitly approved.

### Phase 11 — Packaging and release

Tasks:
- Document installation and startup.
- Define supported environment and dependency versions.
- Provide configuration examples.
- Create a demonstration dataset that can legally be distributed.
- Prepare screenshots or a live demonstration as appropriate.
- Document limitations and troubleshooting.

Deliverables:
- Release candidate
- Final README and setup guide
- Demonstration plan
- Release notes

Exit criteria:
- Another person can follow the instructions and reproduce the core workflow.

## 4. Priority levels

- **P0 — Essential:** required for a safe, working end-to-end release.
- **P1 — Important:** strongly desired for usability or quality.
- **P2 — Optional:** enhancement that can follow after the first release.

Initial suggested priorities:
- P0: reliable ingestion, page-aware retrieval, tests, usable interface, honest errors.
- P0: source-grounded citations if answer generation is included in the release promise.
- P1: persistent library and hybrid retrieval, subject to agreed scope.
- P1: multi-paper search and follow-up questions.
- P2: OCR, advanced reranking, collaboration, cloud deployment.

These priorities must be confirmed against the final project goals.

## 5. Milestone tracking

For each milestone, record:
- Status: Not started / In progress / Blocked / Complete
- Requirements covered
- Files changed
- Tests run
- Test outcome
- Remaining risks
- Evidence of completion

Do not mark a milestone complete based only on code being written.

## 6. Immediate next steps

1. Review the SRS.
2. Review architecture and interfaces.
3. Run the existing test suite.
4. Record the current baseline.
5. Select the first uncompleted phase.
6. Make one small change and verify it.

<!-- PERSISTENCE-STATUS-START -->
## Persistence milestone update

The first persistence module has been added, and automated tests have been
prepared for its basic behavior.

Remaining work before persistence can be considered integrated:

1. Run the new persistence tests.
2. Correct any failures.
3. Add index/model metadata and compatibility checks.
4. Review recovery behavior if one saved file is missing or corrupted.
5. Integrate persistence into the search workflow.
6. Test that a saved index can be reused without rebuilding embeddings.
7. Run the full regression suite.

Do not mark the persistence milestone complete until the integrated workflow
and its tests pass.
<!-- PERSISTENCE-STATUS-END -->
