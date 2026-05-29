# Qwen + Local Schema Reranker Ablation

Date: 2026-05-26

This experiment combines Qwen `text-embedding-v4` as the first-stage retriever with our deterministic structure-aware schema reranker.

Purpose:

- isolate Qwen embedding quality from Qwen reranking quality;
- test whether the procedural schema reranker still helps when the candidate pool comes from a stronger provider embedding model;
- test candidate-budget sensitivity for top-20, top-50, and top-100 shortlists.

## Architecture

| Variant | First Stage | Candidate Budget | Reranker | Reranking Evidence |
|---|---|---:|---|---|
| Qwen + Qwen rerank | Qwen embedding | 20 | `qwen3-rerank` | candidate text only |
| Qwen + local schema rerank | Qwen embedding | 20/50/100 | deterministic schema rerank | R2/R3 fields: description, use_when, output, preconditions, workflow, dependencies, resources, not_for penalty |

The library, prompts, and gold labels are unchanged.

## Results

| Method | First-Stage Representation | Candidate Budget | Top-1 | Top-5 | MRR | Non-Core Top-1 |
|---|---|---:|---:|---:|---:|---:|
| Qwen R1 + local schema | R1 flat card | 20 | 58.2% | 67.2% | 0.622 | 25.4% |
| Qwen full + local schema | Full `SKILL.md` | 20 | 68.7% | 74.6% | 0.715 | 22.4% |
| Qwen full + local schema | Full `SKILL.md` | 50 | 80.6% | 88.1% | 0.834 | 11.9% |
| Qwen full + local schema | Full `SKILL.md` | 100 | 85.1% | 91.0% | 0.878 | 9.0% |
| Qwen R2 + local schema | R2 structured card | 20 | 64.2% | 73.1% | 0.687 | 22.4% |
| Qwen R2 + local schema | R2 structured card | 50 | 70.2% | 79.1% | 0.746 | 14.9% |
| Qwen R2 + local schema | R2 structured card | 100 | 79.1% | 89.5% | 0.838 | 10.4% |

For comparison:

| Method | Top-1 | Top-5 | MRR | Non-Core Top-1 |
|---|---:|---:|---:|---:|
| Best previous local M6: MiniLM full -> schema rerank, top-20 | 80.6% | 91.0% | 0.856 | 7.5% |
| Best Qwen generic rerank: R2 + `qwen3-rerank`, top-20 | 65.7% | 71.6% | 0.688 | 26.9% |
| Best new hybrid: Qwen full -> local schema rerank, top-100 | 85.1% | 91.0% | 0.878 | 9.0% |

## Interpretation

This is the cleanest evidence so far for the thesis.

The weakness was not simply Qwen embedding quality. Qwen embeddings can provide a useful candidate pool, but the correct skill often needs a larger shortlist than top-20. Once the shortlist is expanded to top-50 or top-100, the structure-aware schema reranker can select the procedurally correct skill more reliably.

The result supports this claim:

> Strong semantic retrieval and structure-aware procedural reranking are complementary. The best current architecture uses Qwen embeddings for broad candidate generation and explicit procedural fields for final selection.

This changes the earlier interpretation. It is not accurate to say "local beats Qwen" in general. The better result is:

> Qwen's generic reranker underperforms our task-specific schema reranker, but Qwen embeddings combined with schema reranking become the strongest current method.

## Next Checks

- Inspect the remaining failures of Qwen full + local schema top-100.
- Measure latency and candidate-budget cost for top-20, top-50, and top-100.
- Decide whether top-100 is acceptable as an offline retriever/reranker budget before passing only a small final candidate set to the main agent.
- Consider testing SkillRouter only if it gives a meaningful comparison beyond this hybrid result.
