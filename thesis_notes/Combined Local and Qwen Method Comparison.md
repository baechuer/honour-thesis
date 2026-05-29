# Combined Local and Qwen Method Comparison

Date: 2026-05-26

All results below use the same 1006-skill benchmark, the same 67 prompts, and the same gold labels. They are comparable as method-family results, but they are not a pure model leaderboard because the methods expose different representations and use different reranking logic.

## Full-Library Results

| Method | Representation / Evidence | Reranker | Top-1 | Top-5 | MRR | Non-Core Top-1 |
|---|---|---|---:|---:|---:|---:|
| M1 BM25 flat | R1 flat metadata | none | 64.2% | 86.6% | 0.733 | 16.4% |
| M1 TF-IDF flat | R1 flat metadata | none | 58.2% | 85.1% | 0.697 | 16.4% |
| M2a MiniLM description | R1 description embedding | none | 47.8% | 74.6% | 0.603 | 25.4% |
| M2b MiniLM full skill | Full `SKILL.md` embedding | none | 61.2% | 82.1% | 0.717 | 9.0% |
| M3 TF-IDF schema | R2 structured procedural text | none | 71.6% | 95.5% | 0.807 | 9.0% |
| M6 BM25 -> schema rerank | BM25 shortlist + R2/R3 schema fields | deterministic schema rerank | 71.6% | 92.5% | 0.815 | 7.5% |
| M6 TF-IDF -> schema rerank | TF-IDF shortlist + R2/R3 schema fields | deterministic schema rerank | 70.2% | 85.1% | 0.778 | 10.4% |
| M6 MiniLM full -> schema rerank | Full-skill MiniLM shortlist + R2/R3 schema fields | deterministic schema rerank | 80.6% | 91.0% | 0.856 | 7.5% |
| Qwen R1 embedding | R1 flat card | none | 35.8% | 56.7% | 0.449 | 43.3% |
| Qwen R1 embedding -> rerank | R1 flat card | `qwen3-rerank` | 64.2% | 67.2% | 0.649 | 31.3% |
| Qwen full embedding | Full `SKILL.md` | none | 46.3% | 71.6% | 0.574 | 29.8% |
| Qwen full embedding -> rerank | Full `SKILL.md` | `qwen3-rerank` | 61.2% | 65.7% | 0.644 | 37.3% |
| Qwen R2 embedding | R2 structured card | none | 47.8% | 65.7% | 0.563 | 31.3% |
| Qwen R2 embedding -> rerank | R2 structured card | `qwen3-rerank` | 65.7% | 71.6% | 0.688 | 26.9% |
| Qwen full embedding -> schema rerank | Full `SKILL.md` shortlist + R2/R3 schema fields | deterministic schema rerank, top-20 | 68.7% | 74.6% | 0.715 | 22.4% |
| Qwen full embedding -> schema rerank | Full `SKILL.md` shortlist + R2/R3 schema fields | deterministic schema rerank, top-50 | 80.6% | 88.1% | 0.834 | 11.9% |
| Qwen full embedding -> schema rerank | Full `SKILL.md` shortlist + R2/R3 schema fields | deterministic schema rerank, top-100 | 85.1% | 91.0% | 0.878 | 9.0% |
| Qwen R2 embedding -> schema rerank | R2 structured shortlist + R2/R3 schema fields | deterministic schema rerank, top-100 | 79.1% | 89.5% | 0.838 | 10.4% |

## Candidate Recall

The reranker can only choose the gold skill if the first-stage retriever placed the gold skill inside the top-20 candidate pool.

| Method | Gold In Stored Top-20 | Top-1 Gold |
|---|---:|---:|
| M2b MiniLM full skill | 61/67 | 41/67 |
| M3 TF-IDF schema | 64/67 | 48/67 |
| M6 MiniLM full -> schema rerank | 61/67 | 54/67 |
| Qwen R1 embedding -> rerank | 45/67 | 43/67 |
| Qwen full embedding -> rerank | 51/67 | 41/67 |
| Qwen R2 embedding -> rerank | 50/67 | 44/67 |

## Are These Comparing The Same Thing?

Yes, in the sense that they are evaluated on the same benchmark:

- same 1006-skill library
- same prompts
- same gold labels
- same top-1, top-5, MRR, and non-core false-positive metrics

No, in the sense that they are not identical architectures:

- M6 uses a local first-stage selector and a hand-engineered schema reranker.
- Qwen uses a provider embedding model and a generic neural reranker.
- M6 reranking explicitly scores procedural fields such as `use_when`, outputs, preconditions, workflow, dependencies, resources, and `not_for`.
- Qwen reranking reads the candidate text and returns a relevance score, but it is not explicitly told or engineered to weight each procedural field the way M6 does.

So the correct interpretation is not “MiniLM is better than Qwen.” The correct interpretation is:

> A structure-aware reranking method using explicit procedural fields beats a generic neural embedding/reranking stack on this benchmark. The strongest current architecture combines Qwen embeddings for broad first-stage retrieval with our local procedural schema reranker.

## Why Can Local M6 Beat Qwen?

1. M6 is not just a weaker local model. It is a structure-aware retrieval method.
2. The benchmark is designed around procedural distinctions, so explicit procedural fields are highly informative.
3. Qwen embedding often misses the gold skill in the first-stage top-20. For R2, gold appears in top-20 for 50/67 prompts, which caps reranker success.
4. Qwen reranking improves over Qwen embedding-only, but it cannot recover candidates that were not retrieved.
5. The generic reranker is attracted to plausible background skills, especially generated domain-operation distractors.
6. M6 uses a mild `not_for` penalty and weighted schema fields, which directly targets the benchmark failure mode.

## What Changed Across Experiments?

Representation changed:

- R1 flat card: compressed metadata.
- Full `SKILL.md`: full skill artifact.
- R2 structured card: procedural fields.
- R3 fields are used by local M6 schema scoring.

Retriever changed:

- BM25 / TF-IDF lexical retrieval.
- MiniLM local embedding retrieval.
- Qwen provider embedding retrieval.

Reranker changed:

- No reranker.
- Local deterministic schema reranker.
- Qwen `qwen3-rerank` neural reranker.

The library, prompts, and gold labels did not change.

## Thesis Interpretation

This result is useful because it supports the central thesis question:

> What information must a skill representation preserve to support reliable candidate subsetting under semantic confusion and scale?

The current evidence suggests:

- generic semantic embeddings are not sufficient;
- reranking helps, but first-stage candidate recall matters;
- procedural fields are valuable;
- structure-aware scoring can outperform a generic neural reranker when the task depends on procedural suitability rather than topical similarity.

## Updated Strongest Result

The strongest method so far is:

- first stage: Qwen `text-embedding-v4` over full `SKILL.md`;
- candidate budget: top-100;
- reranker: local deterministic schema reranker over R2/R3 procedural fields;
- result: 85.1% top-1, 91.0% top-5, MRR 0.878.

This means Qwen embeddings are useful, but Qwen's generic reranker is not the best final selector for this benchmark. The procedural schema reranker is better aligned with the task.

## Next Analysis Needed

- Inspect Qwen full + local schema top-100 failures.
- Compare top-20, top-50, and top-100 latency/cost.
- Decide whether top-100 is an acceptable candidate-subsetting budget.
- Only after that decide whether SkillRouter is necessary.
