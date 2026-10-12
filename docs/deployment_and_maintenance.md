# ResearchPilot — Deployment and Maintenance Plan

## 1. Initial deployment assumption

The initial target is a local application running in a Python environment.
The exact UI framework and packaging method remain undecided.

Do not describe the application as production-ready until deployment and acceptance
tests have actually been completed.

## 2. Environment requirements

Record and verify:
- Supported Python version
- Operating system
- Dependency versions
- Embedding model identifier
- Model download requirements
- Storage directories
- Available memory and disk requirements
- Any answer-generation API or local model requirements

## 3. Configuration

The completed application should document:
- Model configuration
- Chunk size and overlap, if supported
- Retrieval result count
- Storage paths
- Index version
- Logging level
- External service configuration, if any

Avoid embedding machine-specific paths in application logic.

## 4. Installation and startup

The release instructions should cover:
1. Obtaining the project source.
2. Creating the virtual environment.
3. Installing documented dependencies.
4. Downloading required models where applicable.
5. Creating required data directories.
6. Running automated tests.
7. Starting the application.
8. Adding a sample paper and testing a query.

## 5. Persistent data

Document where these items are stored:
- Original or referenced PDFs
- Extracted text and chunks
- Document metadata
- Vector indexes
- Optional session history
- Logs

Define which data can be regenerated and which data needs backup.

## 6. Version compatibility

Saved indexes may depend on:
- Embedding model
- Embedding dimension
- Text preprocessing
- Chunking settings
- Index implementation
- Metadata schema

Store enough metadata to detect incompatible saved indexes. Rebuild rather than
silently loading an incompatible index.

## 7. Backup and recovery

Before release, define:
- What is backed up
- Backup location
- Restore procedure
- Index rebuild procedure
- Behavior after interrupted writes
- Document deletion procedure

Test recovery rather than assuming it works.

## 8. Monitoring and diagnostics

The application should expose useful information about:
- Ingestion failures
- Model loading failures
- Index creation and loading
- Retrieval latency
- Answer-generation failures
- Citation validation failures

Routine logs should not contain complete private documents.

## 9. Updates

For each update:
1. Review dependency and model changes.
2. Run automated tests.
3. Re-run relevant evaluation experiments.
4. Check saved-index compatibility.
5. Document changes and known limitations.
6. Provide recovery instructions for incompatible data.

## 10. Release checklist

- [ ] Installation instructions verified on a clean environment.
- [ ] Automated tests pass.
- [ ] Required models and dependencies are documented.
- [ ] Core workflows tested end to end.
- [ ] Citation behavior validated, if answer generation is included.
- [ ] Storage and recovery behavior tested, if persistence is included.
- [ ] Security and privacy review completed.
- [ ] Known limitations documented.
- [ ] Demonstration workflow prepared.
