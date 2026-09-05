# Public Skill Gold Validation Checkpoint - 2026-05-30

This checkpoint records Step 6b: using externally authored public skills as candidate gold-label retrieval targets.

Last refreshed: 2026-06-01.

## What Changed

- Added a public-gold prompt generator: `skill_benchmark/scripts/generate_public_gold_validation.py`.
- Added a separate prompt stratum: `skill_benchmark/prompts_public_gold/public_gold_validation_confusability.json`.
- Added a separate acceptable-alternative file: `skill_benchmark/annotations/public_gold_acceptable_alternatives.json`.
- Added a draft review packet: `skill_benchmark/outputs/public_gold_validation_draft.md`.
- Updated `skill_benchmark/scripts/export_skill_representations.py` so public imported skills can use the downloaded original `source/SKILL.original.md` body for procedural field extraction when available.

The public-gold prompts are intentionally kept outside `skill_benchmark/prompts/` for now. They should not change the main controlled benchmark until manual adjudication is complete.

## Public-Gold Subset

- Draft prompts: 32.
- Gold labels: imported public skills only.
- Coverage: documents/PDF, browser QA, web quality, debugging, GitHub/CI, deployment, MCP/API, Hugging Face, data workflows, contracts/email, slides, Figma, skill lifecycle, and security.
- Each prompt includes source family, field axes, rationale, and optional acceptable alternatives.

## Validation Results

| Gate | Result | Pass Read |
|---|---:|---|
| Step 1 integrity | PASS, 32/32 references resolve | Pass |
| Step 2 procedural distinctness | 32/32 prompts; 114/128 gold/alternative pairs have 2+ primary axes | Pass |
| Step 2 prompt-specific alignment | 32/32 prompts; gold top-1 among listed candidates for 31/32 | Pass |
| Step 3 semantic confusability | 31/32 prompts | Pass |
| Step 4 prompt leakage | 0 critical, 0 high-risk | Pass |

This meets the Step 6b construction thresholds for an initial public-gold subset.

## Public-Gold Local Selector Results

Current run: `skill_benchmark/outputs/public_gold_offline_selector_evaluation.md`.

| Method | Top-1 | Accept Top-1 | Top-5 | Accept Top-5 | MRR |
|---|---:|---:|---:|---:|---:|
| M1 BM25 flat | 62.5% | 65.6% | 87.5% | 90.6% | 0.715 |
| M1 TF-IDF flat | 59.4% | 65.6% | 87.5% | 87.5% | 0.701 |
| M2a MiniLM description | 65.6% | 68.8% | 87.5% | 87.5% | 0.738 |
| M2b MiniLM full skill | 31.2% | 34.4% | 71.9% | 75.0% | 0.483 |
| M3 TF-IDF schema | 50.0% | 50.0% | 71.9% | 78.1% | 0.607 |
| M6 BM25 -> schema rerank | 46.9% | 53.1% | 87.5% | 90.6% | 0.631 |
| M6 TF-IDF -> schema rerank | 40.6% | 46.9% | 84.4% | 87.5% | 0.591 |
| M6 MiniLM full -> schema rerank | 34.4% | 40.6% | 75.0% | 81.2% | 0.521 |

Important interpretation:

- The public-gold subset behaves differently from the controlled-authored benchmark.
- Flat metadata and description retrieval are currently stronger than the naive extracted-schema methods on this public-only stratum.
- This does not refute the representation thesis. It suggests the public extraction layer is noisier than the clean controlled schema, and needs failure analysis before final claims.
- BM25 is retained here as a lexical control baseline only. It should not be treated as the final retrieval architecture; when it performs strongly, it diagnoses surface-keyword strength or leakage-like lexical cues in the public-gold stratum.
- The `non_main_top1` metric is not meaningful for this stratum because the public gold skills are themselves non-main/background skills.

## Public-Gold Qwen Provider Results

These runs use Qwen `text-embedding-v4` and, where noted, Qwen `qwen3-rerank` or the local schema reranker.

| Method | Top-1 | Accept Top-1 | Top-5 | Accept Top-5 | MRR |
|---|---:|---:|---:|---:|---:|
| Qwen R1 flat-card embedding | 59.4% | 65.6% | 87.5% | 90.6% | 0.716 |
| Qwen R2 structured-card embedding | 59.4% | 62.5% | 87.5% | 87.5% | 0.732 |
| Qwen full-skill embedding | 28.1% | 34.4% | 65.6% | 68.8% | 0.469 |
| Qwen R1 + local schema rerank top-100 | 40.6% | 46.9% | 90.6% | 93.8% | 0.616 |
| Qwen R2 + local schema rerank top-100 | 46.9% | 50.0% | 90.6% | 93.8% | 0.653 |
| Qwen full-skill + local schema rerank top-100 | 25.0% | 31.2% | 78.1% | 81.2% | 0.482 |
| Qwen full-skill + Qwen rerank top-20 | 68.8% | 71.9% | 84.4% | 84.4% | 0.763 |

Provider interpretation:

- The generic Qwen reranker is currently strongest on public-gold top-1, which suggests neural reranking helps when public skill artifacts are broad or inconsistently structured.
- Qwen full-skill embedding alone performs poorly on this stratum, likely because long public artifacts and wrappers add noise.
- Local schema reranking improves top-5 recall for R1/R2 but lowers top-1, reinforcing that the extraction/normalization layer needs public-skill failure analysis before final claims.

## Current Caveats

- Manual gold-label adjudication has not yet been done. These are candidate public-gold prompts, not final thesis gold labels.
- Some public skills are broad, duplicated across sources, or overlap strongly with controlled skills. Acceptable alternatives are recorded for known near-equivalents, but this needs a second pass.
- The representation exporter now extracts from public original skill bodies, but the extraction is still heuristic. Some public sections may add too much noise, especially when full public skills contain long examples or broad reference material.
- Provider-backed Qwen results have not yet been run on this public-gold stratum.

## Recommended Next Step

Run a failure-mode review over the public-gold selector results:

1. Inspect strict top-1 failures for M1 BM25 flat, M2a MiniLM description, and M6 BM25 schema rerank.
2. Label each failure as acceptable alternative, public skill too broad, controlled skill genuinely better, first-stage lexical collision, extraction noise, or schema-rerank overweighting.
3. Remove or revise public-gold cases where the public gold label is not manually defensible.
4. Only after that, decide whether to move the public-gold file into the main benchmark or keep it as a separate external-validity stratum.
