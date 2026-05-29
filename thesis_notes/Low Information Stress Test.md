# Low-Information Prompt Stress Test

Date: 2026-05-26

This stress test adds 12 deliberately less-informative prompts. The prompts still have defensible gold labels, but they avoid spelling out every procedural field. They are separate from the main 67-prompt benchmark.

## Why This Exists

The main benchmark checks whether methods can distinguish semantically similar skills when the request contains enough procedural evidence. This stress set checks a different question: what happens when the user request is vague or only partially specifies the intended procedure?

This is an anti-cheating check for the schema reranker. If schema reranking only works when the prompt explicitly names outputs, workflows, and constraints, performance should drop here.

## Results

| Method | Top-1 | Accept Top-1 | Top-5 | Accept Top-5 | MRR | Non-Core Top-1 |
|---|---:|---:|---:|---:|---:|---:|
| M1 BM25 flat | 8.3% | 8.3% | 25.0% | 33.3% | 0.160 | 33.3% |
| M1 TF-IDF flat | 0.0% | 0.0% | 33.3% | 33.3% | 0.111 | 66.7% |
| M2a MiniLM description | 25.0% | 33.3% | 50.0% | 66.7% | 0.375 | 33.3% |
| M2b MiniLM full skill | 41.7% | 50.0% | 66.7% | 75.0% | 0.527 | 41.7% |
| M3 TF-IDF schema | 16.7% | 25.0% | 41.7% | 41.7% | 0.289 | 33.3% |
| M6 BM25 -> schema rerank | 8.3% | 8.3% | 41.7% | 41.7% | 0.215 | 16.7% |
| M6 TF-IDF -> schema rerank | 8.3% | 8.3% | 33.3% | 33.3% | 0.163 | 41.7% |
| M6 MiniLM full -> schema rerank | 33.3% | 33.3% | 66.7% | 66.7% | 0.470 | 25.0% |
| Qwen full + qwen3-rerank, top-20 | 33.3% | 41.7% | 50.0% | 58.3% | 0.408 | 66.7% |
| Qwen full + local schema rerank, top-100 | 25.0% | 25.0% | 66.7% | 66.7% | 0.421 | 33.3% |

## Interpretation

- Performance drops sharply compared with the main benchmark, including for schema reranking.
- This means the schema reranker is not magically inferring hidden intent. It depends on procedural evidence present in the user request.
- Full-skill embedding methods are more robust than flat lexical methods on vague prompts, but they still struggle.
- Qwen full + local schema top-100 reaches only 25.0% strict top-1 but 66.7% top-5, suggesting the correct skill is often in the broader candidate set but difficult to rank first without clearer intent.
- Qwen generic reranking has high non-core top-1 on this set, selecting background skills for 66.7% of prompts.

## What This Means For The Thesis

This stress test should be reported as a limitation and robustness check, not as the main benchmark. It shows that structure-aware retrieval works best when the request contains enough procedural evidence to match against structured fields. For underspecified requests, a realistic agent may need a query-understanding or clarification step before retrieval.

Possible next method family:

```text
raw user request -> requirement extraction / clarification -> structured query -> retrieval/reranking
```

This would test whether an agent or model can infer missing fields before schema matching, instead of expecting the deterministic reranker to infer them.
