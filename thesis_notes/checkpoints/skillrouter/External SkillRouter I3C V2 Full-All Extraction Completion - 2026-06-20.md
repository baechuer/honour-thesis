# External SkillRouter I3C V2 Full-All Extraction Completion - 2026-06-20

## Purpose

Complete the full SkillRouter-Eval-Core I3C V2 extraction over the Hard-tier `all_I2.jsonl` skill universe so external validation can evaluate I3C as a full-library/full-tier information layer, not only as a fixed top-20 candidate-pool reranking representation.

This is an extraction and QA checkpoint, not a retrieval-result checkpoint.

## Source

- Source file: `skill_benchmark/external/skillrouter_eval_core/derived/representations/all_I2.jsonl`
- Source rows: `79141`
- Seed cache: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_full_all/cached/I3C_V2_full_all_seed_top20_cleaned.jsonl`
- Missing-chunk manifest: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_full_all/manifest.json`
- Prompt/schema: `skill_benchmark/extraction_prompts/I3C_SUBAGENT_EXTRACTION_V2.md`

## Extraction Method

- Extraction condition: `I3C V2`
- External APIs: none.
- Online search: none.
- Seed rows: `3284` cleaned rows from the top-20 task-relevant I3C V2 pool.
- Newly extracted rows: `75857`.
- Missing chunks: `759` total; chunks `0-757` have `100` rows each and final chunk `758` has `57` rows.
- Worker rule: one JSON object per input row, preserving `skill_id` and `source_row_index`, with exact evidence substring validation before completion.
- All final workers were closed after parent validation.

## Outputs

- Raw merged audit output: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_full_all/I3C_V2_full_all_merged.jsonl`
- Raw summary: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_full_all/I3C_V2_full_all_summary.json`
- Raw quality check: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_full_all/I3C_V2_full_all_quality_check.json`
- Cleaned canonical output: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_full_all/I3C_V2_full_all_cleaned.jsonl`
- Clean summary: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_full_all/I3C_V2_full_all_clean_summary.json`
- Clean quality check: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_full_all/I3C_V2_full_all_cleaned_quality_check.json`

## Raw Merge QA

- Rows: `79141`
- Source order matches `all_I2.jsonl`: yes.
- Parse-failed rows: `0`
- Missing skill ids: `0`
- Extra skill ids: `0`
- Duplicate skill ids: `0`
- Evidence items: `499274`
- Exact evidence matches: `499274/499274`
- Evidence mismatches: `0`
- Generic heading-only evidence items: `438`
- Empty fields without `absent_fields`: `0`
- Nonempty fields marked absent: `0`
- Rows with zero selector-visible fields: `873`

## Cleaned Canonical QA

The raw merge contained `438` generic heading-only evidence items such as `Use this skill when:`, `Workflow`, `## Workflow`, `Overview`, and `## Example`. These were exact source substrings but weak selector evidence, so they were removed from selector-visible fields while preserving the raw merge for audit.

- Rows: `79141`
- Source order matches `all_I2.jsonl`: yes.
- Parse-failed rows: `0`
- Missing skill ids: `0`
- Extra skill ids: `0`
- Duplicate skill ids: `0`
- Evidence items: `498836`
- Exact evidence matches: `498836/498836`
- Evidence mismatches: `0`
- Heading-only evidence after cleaning: `0`
- Empty fields without `absent_fields`: `0`
- Nonempty fields marked absent: `0`
- Rows with zero selector-visible fields: `875`

Cleaned field counts:

| Field | Row Coverage | Item Count |
|---|---:|---:|
| `use_conditions` | 75928 | 109095 |
| `input_preconditions` | 21688 | 40982 |
| `output_artifacts` | 28755 | 51042 |
| `workflow_steps` | 32795 | 98531 |
| `constraints_boundaries` | 23617 | 48441 |
| `dependencies_resources` | 43056 | 105217 |
| `success_criteria` | 22052 | 45529 |

Heading-only removals by field:

| Field | Removed Items |
|---|---:|
| `use_conditions` | 193 |
| `input_preconditions` | 1 |
| `output_artifacts` | 9 |
| `workflow_steps` | 224 |
| `constraints_boundaries` | 0 |
| `dependencies_resources` | 11 |
| `success_criteria` | 0 |

## Interpretation

This pass completes the extraction prerequisite for full-library/full-tier SkillRouter-Eval-Core I3C experiments. The cleaned full-all artifact can be used for future external I1/I2/I3C information-layer ablations and full-tier reranking/retrieval tests.

It does not by itself establish retrieval performance. Any result table using this artifact should still report the scored task set, tier, candidate universe, retriever, reranker, candidate budget, scoring rule, and whether the run is fixed-candidate or full-library.

## Caveats

- Sparse public skills remain sparse by design. The `875` zero-selector rows are retained with absence/QA metadata rather than overfilled.
- The cleaned file removes generic heading-only evidence from selector-visible fields, but the raw merged file remains available for audit.
- The full artifact is large and should be treated as an external validation representation, separate from the local frozen-v0.4 2433-skill benchmark artifacts.
