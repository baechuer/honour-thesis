# Provider Step 6 Results - 2089 Scale

Date: 2026-05-28

This note records the Qwen provider runs that were rerun on the active 2089-skill benchmark.

## Scope

These runs update Step 6 for one representative provider setup:

- Embedding provider: Qwen / DashScope.
- Embedding model: `text-embedding-v4`.
- Embedding representation: full `SKILL.md`.
- Scale: `current_full`, 2089 skills.

This does not rerun every historical provider variant. It is enough to compare:

- modern provider embedding-only retrieval
- modern provider embedding plus generic neural reranking
- modern provider embedding plus local procedural schema reranking

## Results

| Method | Candidate Budget | Top-1 | Accept Top-1 | Top-5 | Accept Top-5 | MRR | Non-Core Top-1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Qwen full-skill embedding only | none | 50.6% | 51.8% | 69.4% | 71.8% | 0.591 | 30.6% |
| Qwen full-skill + Qwen rerank | 20 | 63.5% | 68.2% | 69.4% | 72.9% | 0.668 | 32.9% |
| Qwen full-skill + local schema rerank | 50 | 80.0% | 81.2% | 84.7% | 85.9% | 0.822 | 12.9% |
| Qwen full-skill + local schema rerank | 100 | 84.7% | 84.7% | 89.4% | 89.4% | 0.872 | 9.4% |

## Interpretation

Qwen full-skill embeddings are useful for broad candidate generation, but embedding-only retrieval is not enough on the 2089-skill library.

Qwen's generic reranker improves top-1 over embedding-only, but it does not solve the benchmark and it increases non-core top-1 slightly. This suggests that a general relevance reranker can still prefer semantically plausible background skills when procedural boundaries matter.

The strongest provider-backed result is Qwen full-skill embedding plus local schema reranking over the top-100 candidate pool. This supports the thesis framing:

> strong semantic retrieval is useful for candidate subsetting, but final skill selection benefits from explicit procedural fields.

## Cost And Cache Notes

The first 2089-scale smoke test populated much of the Qwen embedding cache. Later runs reused cached embeddings.

For the full Qwen rerank run:

- Embedding API calls made: 26.
- Embedding cache hits: 2148.
- Approx uncached embedding input tokens: 1594.
- Rerank API calls made: 71.
- Rerank cache hits: 14.
- Approx uncached rerank input tokens: 790,763.

The local-schema rerank runs made no rerank API calls.

## Reports

- `skill_benchmark/outputs/provider_selector_qwen_2089_full_embedding.md`
- `skill_benchmark/outputs/provider_selector_qwen_2089_full_rerank.md`
- `skill_benchmark/outputs/provider_selector_qwen_2089_full_local_schema_top50.md`
- `skill_benchmark/outputs/provider_selector_qwen_2089_full_local_schema_top100.md`
- Smoke test: `skill_benchmark/outputs/provider_selector_qwen_2089_full_rerank_smoke.md`

## Caveat

Only the full-skill representation was rerun for Qwen at 2089 scale. Historical Qwen results for R1 and R2 remain 1006-scale unless rerun later.

This is acceptable for the current thesis direction because full-skill embedding plus procedural reranking is the most relevant provider-backed architecture for testing whether explicit procedural information improves final selection.

