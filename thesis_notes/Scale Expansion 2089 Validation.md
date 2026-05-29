# Scale Expansion 2089 Validation

Date: 2026-05-28

This note records the current scale-expansion pass for the skill retrieval benchmark.

## What Changed

- Expanded generated background skills from 920 to 1800.
- Expanded public imported background skills from 15 to 200.
- Added 18 controlled-core v2 skills and prompts:
  - `office_artifact_workflows`: 6 skills.
  - `deployment_browser_qa`: 6 skills.
  - `api_backend_design`: 6 skills.
- Total benchmark size is now 2089 skills and 85 evaluated prompts.

## Current Composition

| Layer | Count | Role |
|---|---:|---|
| Controlled/evaluated core | 85 | Gold-label retrieval evaluation. |
| Generated background scale | 1800 | Large-library pressure and near-domain distractors. |
| Public imported background | 200 | Real-world skill noise, dependencies, resources, and uneven formatting. |
| Support email skills | 4 | Legacy support/background family. |

Public import status: 200/200 original public `SKILL.md` files downloaded successfully.

## Rubric Results

| Step | Status | Result |
|---|---|---|
| 1. Integrity | PASS | 85 prompts and 2089 skills resolve; no duplicates or missing references. |
| 2. Procedural distinctness | PASS | 85/85 prompts pass; 251/251 gold/alternative pairs differ on at least two primary axes. |
| 2. Prompt alignment | PASS | 85/85 pass after prompt refinements and negation-aware alignment scoring. |
| 3. Semantic confusability | PASS | 75/85 prompts pass using local MiniLM embeddings. |
| 4. Prompt leakage | PASS | 0 critical leaks and 0 high-risk leaks. |
| 5. Scale regime | PASS | Full condition now has 2089 skills. |
| 6. Selector pressure | PASS | Full-library top-1 ranges from 49.4% to 82.3%, so the benchmark is not too easy. |

## Local Selector Results

| Method | Core top-1 | Full top-1 | Full top-5 | Full non-core top-1 |
|---|---:|---:|---:|---:|
| M1 BM25 flat | 76.5% | 70.6% | 87.1% | 14.1% |
| M1 TF-IDF flat | 75.3% | 58.8% | 80.0% | 28.2% |
| M2a MiniLM description | 67.1% | 49.4% | 77.6% | 31.8% |
| M2b MiniLM full skill | 71.8% | 64.7% | 83.5% | 15.3% |
| M3 TF-IDF schema | 84.7% | 78.8% | 94.1% | 7.1% |
| M6 BM25 -> schema rerank | 80.0% | 78.8% | 91.8% | 4.7% |
| M6 TF-IDF -> schema rerank | 84.7% | 75.3% | 88.2% | 11.8% |
| M6 MiniLM full -> schema rerank | 90.6% | 82.3% | 89.4% | 5.9% |

Interpretation: the expanded library creates real scale pressure. Description-only dense retrieval degrades the most, while structured/schema-aware methods degrade less and produce fewer non-core top-1 false positives.

## Non-Core Competition

Embedding semantic competition:

- A non-core skill is top-1 for 24/85 prompts.
- The best non-core skill beats gold for 33/85 prompts.

Embedding-backed procedural competition:

- 16/85 prompts have at least one non-core skill above gold.
- Highest-risk families: `skill_lifecycle`, `documents_files`, `deployment_browser_qa`, and `api_backend_design`.

Interpretation: this is useful pressure, but it also means the expanded benchmark now needs manual adjudication of non-core winners before final thesis claims. Some non-core winners are probably just plausible distractors; others may be acceptable alternatives or signs that an old prompt should be refined.

## Context Scale

Approximate selector-visible token budgets from the local evaluator:

| Representation | Approx selector-visible tokens |
|---|---:|
| R1 flat metadata | 105,272 |
| Full `SKILL.md` documents | 1,065,572 |
| M3 schema cards | 590,432 |
| M6 flat shortlist + schema rerank | 111,268 |

Interpretation: 2089 skills creates a stronger scalability argument. Compact metadata may still be possible for some large-context models, but full skill artifacts and rich structured cards are far beyond a practical single-context strategy.

## Immediate Next Actions

1. Update the human adjudication note for the current 33 semantic non-core-over-gold cases and 16 procedural non-core-over-gold cases.
2. Decide whether the remaining Step 3 weak prompts should be kept as high-precision cases or revised into stronger semantic-confusion cases.
3. Rerun Qwen provider methods on the 2089-skill condition only after the non-core adjudication is stable.
4. Keep 1006-skill results as v1 historical comparison; use 2089 as the active scale condition.
