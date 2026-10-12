# ResearchPilot — Software Testing Plan

## 1. Purpose

This plan defines how ResearchPilot will be tested throughout development and
before release.

## 2. Test levels

### Unit testing

Test individual functions in isolation.

Examples:
- PDF validation
- Chunk boundary behavior
- Empty-query handling
- Keyword tokenization
- Result sorting
- Citation validation

### Integration testing

Test components working together.

Examples:
- PDF extraction followed by chunking
- Chunking followed by embedding and index creation
- Index search mapped back to the correct chunks
- Retrieval evidence passed to answer generation
- Persistent index loaded with its metadata

### End-to-end testing

Test the full intended user workflow.

Example:
1. Add a paper.
2. Ask a question.
3. Retrieve relevant evidence.
4. Generate an answer when enabled.
5. Inspect citations.

### Acceptance testing

Verify the SRS acceptance criteria using realistic user tasks.

## 3. Test categories

### Input and error handling

- Missing file
- Invalid path
- Unsupported file type
- Malformed PDF
- Empty PDF
- Blank query
- Invalid `top_k`
- Model loading failure
- Index loading failure
- Storage failure

### Data correctness

- Correct page numbering
- Correct document association
- Stable chunk ordering
- No index/chunk mismatch
- Correct score association
- Valid citation references

### Retrieval quality

- Relevant passage ranked highly
- Irrelevant passage ranked lower
- Exact terminology queries
- Paraphrased queries
- Queries containing acronyms
- Queries involving negation or numerical details
- Queries with evidence spread across pages
- Queries with no answer in the corpus

### Answer quality

- Answer supported by cited evidence
- Citation points to the correct page
- No invented citation
- Partial evidence acknowledged
- Insufficient evidence acknowledged
- Conflicting passages handled transparently

### Persistence

- Save and reload
- Restart application
- Rebuild missing index
- Reject incompatible index metadata
- Delete document and associated data
- Recover from interrupted writes where supported

### Security and privacy

- Unexpected file inputs
- Path handling
- Prompt-injection text inside documents
- Sensitive text in logs
- External API data handling, if applicable

## 4. Test fixtures

Maintain small, stable fixtures that can be redistributed legally.

For each fixture, record:
- Purpose
- Expected extraction behavior
- Expected page metadata
- Known relevant passages
- Expected failure or success
- License or permission status

Avoid relying on a single paper as the only evaluation source.

## 5. Automation

Use the existing test framework where practical. The project currently includes
`unittest`-style tests; inspect the actual files before assuming all tests follow
one convention.

Run tests from the project root with the virtual environment activated:

```powershell
python -m unittest discover -s tests -v
```

Record the date, environment, command, and result when establishing a baseline.

## 6. Test result reporting

For each run, record:
- Test name
- Expected result
- Actual result
- Pass/fail
- Relevant error output
- Environment and dependency versions

## 7. Release gate

Do not release while critical tests fail, source metadata is incorrect, or
citations are presented as verified without validation.

Any known limitation accepted for release must be documented.
