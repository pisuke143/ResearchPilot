# ResearchPilot — Architecture Decision Log

## Purpose

Record decisions that affect requirements, architecture, implementation, or release.
An entry should explain the context and trade-offs, not only the selected option.

## Decision status

- Proposed: under consideration
- Accepted: selected for implementation
- Rejected: considered and not selected
- Superseded: replaced by a later decision

## ADR-001 — Python as the implementation language

**Status:** Accepted as the current project baseline

**Context:** Existing modules are written in Python.

**Decision:** Continue the current implementation in Python unless a future
requirement provides a compelling reason to change.

**Consequences:** Reuse the existing ecosystem and keep Python compatibility documented.

## ADR-002 — Sentence Transformers for semantic embeddings

**Status:** Existing implementation choice; future review permitted

**Context:** The current code uses `sentence-transformers/all-MiniLM-L6-v2`.

**Decision:** Retain this as the current baseline until retrieval evaluation justifies a change.

**Consequences:** Model version and embedding settings must be recorded for reproducible
evaluation and index compatibility.

## ADR-003 — FAISS for vector search

**Status:** Existing implementation choice; persistence strategy not yet finalized

**Context:** The current vector-store module uses FAISS.

**Decision:** Use FAISS as the existing baseline for vector similarity search.

**Consequences:** Index vector ordering must match the associated chunk metadata.
Persistence and recovery behavior require explicit design and tests.

## ADR-004 — Local-first initial development

**Status:** Proposed

**Context:** The current development environment is local and the application handles research documents.

**Decision:** Prefer local document processing unless a requirement justifies an external service.

**Consequences:** Model resource use, storage, and installation need documentation.
Any external API integration requires a privacy review.

## ADR-005 — Page-level provenance

**Status:** Required by the project scope

**Context:** Users must be able to verify retrieved passages in their papers.

**Decision:** Preserve document and page metadata throughout ingestion, retrieval,
and answer generation.

**Consequences:** Provenance loss or incorrect citation mapping is a release-blocking defect.

## ADR-006 — Evaluate retrieval before tuning

**Status:** Proposed development rule

**Context:** A search result can look plausible without answering the question.

**Decision:** Establish a fixed evaluation dataset and baseline before making major ranking changes.

**Consequences:** Retrieval improvements must be supported by measured results.

## Future decision template

### ADR-NNN — Decision title

**Status:** Proposed / Accepted / Rejected / Superseded

**Context:** What problem needs a decision?

**Options:** What alternatives were considered?

**Decision:** What was selected and why?

**Consequences:** What trade-offs, implementation work, and risks follow?

**Date:** YYYY-MM-DD
