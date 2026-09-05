# Test Case Expansion Toward 400 - 2026-06-16

Purpose: expand the benchmark toward roughly 400 prompts while preserving the existing validation rubric: integrity, procedural distinctness, prompt-specific alignment, semantic confusability, leakage, and scale pressure.

## Expansion Added

| Stratum | Before | Added | Current |
|---|---:|---:|---:|
| Controlled prompts | 201 | 44 | 245 |
| Public-gold prompts | 120 | 24 | 144 |
| Low-information stress prompts | 12 | 0 | 12 |
| Total broad prompt pool | 333 | 68 | 401 |

New files:

- `skill_benchmark/prompts/benchmark_expansion_clear_confusability.json`: 20 clear controlled cases.
- `skill_benchmark/prompts/public_like_extra_confusability.json`: 24 public-like controlled cases.
- `skill_benchmark/prompts_public_gold/public_gold_expansion_confusability.json`: 24 public-gold cases using imported public skills as targets.

## Current Library And Scale

| Item | Count / estimate |
|---|---:|
| Total skills | 2433 |
| Generated background-scale skills | 1800 |
| Public imported background skills | 460 |
| Public-style controlled skills | 32 |
| Empty descriptions | 0 |
| Median `SKILL.md` size | 1986 chars |
| R1 flat metadata | ~332,992 tokens |
| R2 structured procedural cards | ~2,257,002 tokens |
| R3 dependency/resource-aware cards | ~2,854,228 tokens |

Interpretation: the library is now above the user's approximate 200k-token context budget even for full flat metadata exposure, so dynamic candidate subsetting is no longer just a hypothetical scaling concern.

## Rubric Rerun Results

| Gate | Controlled result | Public-gold result |
|---|---|---|
| Step 1 integrity | PASS: 245 prompts, 0 missing refs | PASS: 144 prompts, 0 missing refs |
| Step 2 procedural distinctness | PASS: 245/245 prompts; 830/830 pairs | PASS: 144/144 prompts; 575/575 pairs |
| Step 2 prompt-specific alignment | 238/245 prompts; strict top-1 236/245; acceptable top-1 241/245 | 131/144 prompts; strict top-1 118/144; acceptable top-1 138/144 |
| Step 3 semantic confusability | PASS: 243/245 prompts (99.2%) | PASS: 144/144 prompts (100.0%) |
| Step 4 leakage | PASS: 0 critical, 0 high | PASS: 0 critical, 0 high |

Notes:

- The two high-risk leakage cases introduced during drafting were rewritten before this snapshot.
- The one weak public-gold distinctness pair was repaired by replacing a thin Trello distractor with a procedurally richer n8n workflow distractor.
- Step 3 is not expected to be 100%; it verifies that most prompts have plausible semantic neighbours, while some high-specificity tasks remain intentionally clearer.

## Background / Non-Core Pressure

| Check | Result | Interpretation |
|---|---:|---|
| Controlled semantic non-core top-1 | 56/245 | Background/public skills sometimes win under flat semantic cards, so scale distractors are active. |
| Controlled best non-core beats gold | 88/245 | There is meaningful scale pressure for candidate subsetting. |
| Controlled procedural non-core above gold | 14/245 prompts | Structured procedural comparison removes most background false positives, but residuals still need manual adjudication if used in final claims. |

Caveat: the public-gold non-core metric is not a headline quality metric because public-gold targets themselves are imported public/background skills.

## Local Selector Sanity Check

Controlled 245-prompt full-library local results:

| Method | Top-1 | Top-5 | MRR | Visible tokens approx | Non-main top-1 |
|---|---:|---:|---:|---:|---:|
| `m1_bm25_flat` | 55.9% | 87.4% | 0.693 | 125,184 | 10.6% |
| `m1_tfidf_flat` | 53.9% | 85.3% | 0.677 | 125,184 | 16.3% |
| `m3_tfidf_schema` | 64.5% | 93.1% | 0.772 | 1,061,244 | 9.4% |
| `m6_bm25_schema_rerank` | 60.8% | 90.2% | 0.743 | 132,805 | 3.7% |
| `m6_tfidf_schema_rerank` | 63.3% | 88.6% | 0.749 | 132,805 | 6.1% |

Public-gold 144-prompt full-library local results:

| Method | Strict top-1 | Accept top-1 | Strict top-5 | Accept top-5 | MRR |
|---|---:|---:|---:|---:|---:|
| `m1_bm25_flat` | 55.6% | 65.3% | 81.9% | 86.8% | 0.673 |
| `m1_tfidf_flat` | 56.9% | 64.6% | 86.8% | 91.0% | 0.697 |
| `m3_tfidf_schema` | 48.6% | 55.6% | 81.2% | 87.5% | 0.629 |
| `m6_bm25_schema_rerank` | 43.1% | 57.6% | 80.6% | 86.1% | 0.585 |
| `m6_tfidf_schema_rerank` | 45.8% | 55.6% | 84.7% | 89.6% | 0.612 |


Interpretation:

- The controlled expansion did not make the benchmark trivial: full-library local top-1 remains roughly 54-65% for flat/schema lexical methods.
- The public-gold stratum remains harder and messier: local strict top-1 is roughly 43-57%, and acceptable scoring is necessary because public skills often overlap or wrap similar workflows.
- The new clear-controlled expansion is intentionally explicit, but selector results show it still creates pressure under scale because many public-style and background near-neighbours exist.

## Remaining Risks

- Gold-label stability still needs manual adjudication for strongest-method failures and residual non-core winners.
- Public-gold cases are valuable external-validity pressure, but they should be reported separately from controlled causal-field claims.
- Local lexical schema reranking is still a diagnostic baseline, not the final structure-aware method.
- Provider/SkillRouter runs have not been rerun on the expanded 245 controlled / 144 public-gold prompt sets.

## Semantic repair follow-up

A same-day Step 3 repair improved controlled semantic confusability from 221/245 to 243/245 and public-gold semantic confusability from 137/144 to 144/144, while preserving Step 2 prompt-specific alignment and leakage results. See `thesis_notes/checkpoints/benchmark_validation/Semantic Confusability Repair - 2026-06-16.md`.
