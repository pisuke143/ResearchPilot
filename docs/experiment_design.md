# ResearchPilot — Retrieval and Answer Evaluation Plan

## 1. Purpose

This document defines experiments to measure whether ResearchPilot retrieves
useful evidence and, when answer generation is implemented, whether its answers
are supported by that evidence.

## 2. Research questions

1. How well does keyword retrieval find relevant passages?
2. How well does semantic retrieval find relevant passages?
3. Does combining retrieval methods improve ranking?
4. Which query types cause failures?
5. How often are generated claims supported by retrieved passages?
6. How often do citations identify the correct source?
7. What are ingestion and query latency under a defined workload?

## 3. Dataset

Build a small, manually reviewed evaluation set before tuning the retrieval system.

Each query record should include:
- Query identifier
- Question
- Corpus/document identifiers
- Relevant chunk identifiers or source page ranges
- Relevance labels
- Query category
- Reviewer notes

Include:
- Exact-term queries
- Paraphrased queries
- Acronyms and technical terminology
- Questions requiring specific numerical details
- Questions whose evidence spans more than one passage
- Questions with no answer in the corpus

Avoid tuning on the test set and then reporting the same results as independent evaluation.

## 4. Baselines

Measure separately:
- Keyword retrieval
- Semantic retrieval
- Hybrid retrieval, once implemented
- Reranking, if implemented

Keep the corpus, queries, chunking, and evaluation rules fixed when comparing
methods. Record any configuration changes.

## 5. Retrieval metrics

### Precision@k

The proportion of the top k retrieved passages judged relevant.

### Recall@k

The proportion of all known relevant passages that appear in the top k results.

### Mean Reciprocal Rank (MRR)

Measures how highly the first relevant passage is ranked across queries.

### nDCG@k

Measures ranking quality when relevance has multiple grades.

Choose metrics that match the available relevance labels. Do not report metrics
whose inputs have not been collected.

## 6. Answer evaluation

When answer generation is implemented, evaluate:
- Relevance to the question
- Support from the provided evidence
- Citation correctness
- Coverage of the question
- Unsupported-claim frequency
- Appropriate refusal or uncertainty when evidence is insufficient

Use human review for a sample of answers. Automated scores alone do not prove
factual correctness.

## 7. Performance evaluation

Record:
- Number of documents and pages
- Total extracted characters or chunks
- Embedding model and version
- Ingestion duration
- Index construction duration
- Query latency
- Memory use where measurable
- Hardware and software environment

Repeat runs when variability is significant. Distinguish cold-start time from
steady-state query time.

## 8. Experiment procedure

1. Freeze a version of the evaluation dataset.
2. Record the code revision and configuration.
3. Run the baseline.
4. Save predictions and scores.
5. Calculate metrics.
6. Inspect failed queries.
7. Make one targeted change.
8. Rerun the same evaluation.
9. Compare results and regressions.
10. Record the decision.

## 9. Reporting template

For each experiment, record:

- Experiment ID
- Date
- Hypothesis
- Code revision
- Dataset version
- Configuration
- Baseline method
- Changed method
- Metrics
- Representative successes
- Representative failures
- Limitations
- Decision: keep, revise, or reject

## 10. Acceptance thresholds

Set numeric thresholds only after establishing a baseline and understanding the
project's intended use. The final report must show measured results and must
not claim that a model is reliable merely because it returns a result.
