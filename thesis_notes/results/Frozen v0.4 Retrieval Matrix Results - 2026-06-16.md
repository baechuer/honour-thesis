# Frozen v0.4 Retrieval Matrix Results - 2026-06-16

Source benchmark version: `benchmark-v0.4-2026-06-16`.

Full result report:

- `skill_benchmark/outputs/frozen_v0_4_retrieval_matrix_summary.md`
- `skill_benchmark/outputs/frozen_v0_4_retrieval_matrix_summary.json`

## What Was Rerun

- Controlled stratum: 245 prompts against the full 2433-skill library.
- Public-gold stratum: 144 prompts against the full 2433-skill library, with strict-gold and gold-or-acceptable scoring.
- Local offline methods: BM25, TF-IDF, MiniLM, schema retrieval, and schema rerank variants.
- Qwen methods: R1/R2/full embedding-only, Qwen rerank top-20, and local-schema top-20 over the same representations.
- M6-v1 field-aware prototype: Qwen full-skill first stage with top-20 and top-100 candidate budgets.
- Field ablations: controlled and public-gold diagnostic runs.

## Main Findings

Controlled prompts support the representation-layer claim. With the same Qwen first-stage retriever and the same Qwen reranker, R2 structured representation improves top-1 over R1 flat representation: 58.0% versus 51.4%. Full skill text is only slightly higher at 58.8%, while exposing much more selector-visible text.

Public-gold behaves differently. Qwen embedding-only performs best on R2 at 63.2% strict top-1, but Qwen rerank top-20 is highest on R1 at 74.3% strict top-1. This suggests public skills often encode strong provider/task cues in names and short descriptions, while structured fields improve recall and ranking depth.

Full skill text is not automatically the best representation. On public-gold, full-skill Qwen embedding drops to 36.1% strict top-1 and full-skill Qwen rerank reaches 65.3%, below R1/R2 reranked cards.

The current local schema and M6-v1 field-aware rerankers are diagnostic rather than final robust methods. They help controlled cases and show that candidate recall is high, but they are brittle on public-gold because lexical field matching does not yet handle messy public skill prose well.

## Remaining Work

- Rerun SkillRouter across R1/R2/full under frozen v0.4.
- Add paired statistical tests and confidence intervals for the key comparisons.
- Analyze public-gold R1/R2 disagreements to separate valid provider cues from title/provider bias.
- Implement M6-v2 semantic field matching or LLM-assisted field matching.
- Decide whether M4 tree and M5 graph methods add enough thesis value to implement before writing final results.
