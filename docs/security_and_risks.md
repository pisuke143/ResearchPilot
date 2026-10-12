# ResearchPilot — Security, Privacy, and Risk Management

## 1. Security objectives

- Protect user documents and metadata.
- Handle untrusted PDF content safely.
- Prevent unsupported content from being treated as verified evidence.
- Avoid leaking private content through logs or external services.
- Make failures visible and recoverable.

## 2. Untrusted documents

PDF files may be malformed, unusually large, or contain misleading instructions.
The system should:
- Validate file type and readability.
- Handle extraction errors safely.
- Apply reasonable configurable limits to file size and processing workload.
- Treat extracted text as data, not as trusted system instructions.
- Avoid executing content extracted from a paper.

## 3. Prompt injection

A paper may contain text that attempts to instruct the AI system to ignore its
rules or reveal information.

The answer-generation design should:
- Treat retrieved passages as untrusted evidence.
- Separate system instructions from document content.
- Tell the generator not to follow instructions embedded in source documents.
- Limit tools and external actions available to the generator.
- Test malicious or misleading passages.
- Validate citations independently of the generator's claims.

These measures reduce risk but do not guarantee complete protection.

## 4. Privacy

Under the initial local-first assumption:
- Keep papers and indexes on the local machine.
- Do not transmit document contents externally unless the user-facing design explicitly requires it.
- If an external model API is selected, document what text, metadata, and query data are sent.
- Avoid putting full paper text or API credentials in logs.
- Document how stored data can be deleted.

## 5. Secrets and dependencies

- Never commit API keys or passwords.
- Use environment variables or an appropriate local secrets mechanism.
- Keep dependencies documented.
- Review security-relevant dependency updates.
- Do not disable security checks just to make tests pass.

## 6. Operational risks

### Incorrect citations

Impact: Users may trust a claim that is not supported by the cited source.

Mitigation: Validate citations against retrieved evidence and test page mapping.

### Poor retrieval

Impact: Relevant evidence may be missed.

Mitigation: Maintain an evaluation set and measure ranking quality.

### Hallucinated answers

Impact: The answer may include unsupported details.

Mitigation: Ground answers in evidence, check citations, and handle insufficient evidence.

### Stale index

Impact: Results may point to the wrong chunk or outdated content.

Mitigation: Track index metadata and rebuild when compatibility checks fail.

### Large or malformed documents

Impact: Excessive resource use or processing failure.

Mitigation: Validate inputs, set reasonable limits, and report errors.

### Model unavailable

Impact: Ingestion or search may fail.

Mitigation: Report the failure clearly and define which operations can still work.

### Data loss

Impact: Documents or indexes may need to be processed again.

Mitigation: Define backup, rebuild, and recovery procedures for persistent storage.

## 7. Risk review

Review risks at each major milestone. For every significant risk, record:
- Likelihood
- Impact
- Mitigation
- Owner
- Status
- Residual risk

## 8. Incident handling

For a serious defect:
1. Reproduce the issue safely.
2. Identify affected requirements and data.
3. Prevent further damage where possible.
4. Correct the defect.
5. Add a regression test.
6. Update documentation and known issues.
