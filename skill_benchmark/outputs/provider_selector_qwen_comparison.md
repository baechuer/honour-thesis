# Qwen Provider Selector Comparison

This report compares Qwen `text-embedding-v4` embedding retrieval (M7) against Qwen `text-embedding-v4` plus `qwen3-rerank` over top-20 candidates (M8) on the 1006-skill benchmark.

## Summary

| Representation | Method | Top-1 | Accept Top-1 | Top-5 | Accept Top-5 | MRR | Non-Core Top-1 | API Calls | Approx API Tokens |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| R1 flat card | Embedding only | 35.8% | 35.8% | 56.7% | 59.7% | 0.449 | 43.3% | 0 | 0 |
| R1 flat card | Embedding + rerank | 64.2% | 67.2% | 67.2% | 70.2% | 0.649 | 31.3% | 168 | 194602 |
| Full SKILL.md | Embedding only | 46.3% | 47.8% | 71.6% | 74.6% | 0.574 | 29.8% | 0 | 0 |
| Full SKILL.md | Embedding + rerank | 61.2% | 65.7% | 65.7% | 70.2% | 0.644 | 37.3% | 223 | 1211230 |
| R2 structured card | Embedding only | 47.8% | 47.8% | 65.7% | 67.2% | 0.563 | 31.3% | 0 | 0 |
| R2 structured card | Embedding + rerank | 65.7% | 67.2% | 71.6% | 73.1% | 0.688 | 26.9% | 168 | 821405 |

## Reranker Effect

| Representation | Gold in Embedding Top-20 | Rerank Rescues | Rerank Hurts | Rerank Net Top-1 Change |
|---|---:|---:|---:|---:|
| R1 flat card | 45/67 (67.2%) | 21 | 2 | +19 |
| Full SKILL.md | 51/67 (76.1%) | 16 | 6 | +10 |
| R2 structured card | 50/67 (74.6%) | 15 | 3 | +12 |

## Interpretation

- Qwen embedding-only is not a solved baseline on this benchmark. It struggles especially with generated near-domain background skills.
- Qwen reranking improves top-1 for every representation, but it can only recover skills that enter the first-stage top-20 candidate set.
- The best Qwen condition is currently R2 structured cards plus reranking, at 65.7% strict top-1 and 71.6% top-5.
- The best local method remains M6 MiniLM full-skill retrieval plus deterministic schema reranking, at 80.6% strict top-1 in the previous offline selector report.
- This strengthens the thesis framing: representation and procedural information remain important even when using a stronger provider embedding/reranking stack.

