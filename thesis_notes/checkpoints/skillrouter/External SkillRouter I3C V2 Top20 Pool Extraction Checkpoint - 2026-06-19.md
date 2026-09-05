# External SkillRouter I3C V2 Top-20 Pool Extraction Checkpoint - 2026-06-19

## Purpose

Parse the SkillRouter-Eval-Core task-relevant top-20 candidate pool into the frozen seven-field I3C representation so the external benchmark can test I1/I2/I3C information-layer ablations under a fixed selector-visible candidate universe.

This is an extraction checkpoint, not a retrieval-result checkpoint.

## Source Pool

- Source pool: `skill_benchmark/external/skillrouter_eval_core/derived/representations/skillrouter_task_relevant_pool_top20_I2.jsonl`
- Pool construction: union of top-20 candidates from existing SkillRouter-Eval-Core full-library lexical rankings plus all scored-task gold skills.
- Source rows: `3284`
- Scope: task-relevant fixed-candidate pool for the 75 scored SkillRouter-Eval-Core tasks.
- This does not replace full-library first-stage retrieval.

## Extraction Method

- Extraction condition: `I3C`
- Prompt/schema: `skill_benchmark/extraction_prompts/I3C_SUBAGENT_EXTRACTION_V2.md`
- Schema version in rows: `I3C_SUBAGENT_EXTRACTION_V2`
- Fields extracted:
  - `use_conditions`
  - `input_preconditions`
  - `output_artifacts`
  - `workflow_steps`
  - `constraints_boundaries`
  - `dependencies_resources`
  - `success_criteria`
- Worker setup: 33 Codex subagent chunks, mostly 100 skills per worker, final chunk 84 skills.
- External APIs: none.
- Online search: none.
- All subagents were closed after completion.

## Raw Merge

- Raw merged output: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_top20_pool/I3C_V2_top20_pool_merged.jsonl`
- Raw summary: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_top20_pool/I3C_V2_top20_pool_summary.json`
- Rows: `3284`
- Source chunk files: `33`
- Parse-failed rows: `0`
- Missing skill ids: `0`
- Duplicate skill ids: `0`
- Order matches source pool: yes.

Raw merge field counts:

| Field | Row Coverage | Item Count |
|---|---:|---:|
| `use_conditions` | 3250 | 4655 |
| `input_preconditions` | 1378 | 2440 |
| `output_artifacts` | 1914 | 3341 |
| `workflow_steps` | 1967 | 5632 |
| `constraints_boundaries` | 1508 | 2818 |
| `dependencies_resources` | 1918 | 4028 |
| `success_criteria` | 1521 | 2657 |

## Cleaned Canonical Output

The raw merge contained 27 heading-only evidence items, such as `Use this skill when:` or `## Workflow`. These were exact source substrings, but not selector-useful evidence. They were removed into a cleaned canonical file while preserving the raw merge for audit.

- Cleaned output for retrieval experiments: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_top20_pool/I3C_V2_top20_pool_cleaned.jsonl`
- Clean summary: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_top20_pool/I3C_V2_top20_pool_clean_summary.json`
- Clean quality check: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_top20_pool/I3C_V2_top20_pool_cleaned_quality_check.json`

Cleaned validation:

- Rows: `3284`
- Parse-failed rows: `0`
- Missing skill ids: `0`
- Duplicate skill ids: `0`
- Order matches source pool: yes.
- Evidence items: `25544`
- Exact evidence matches: `25544/25544`
- Evidence mismatches: `0`
- Heading-only evidence after cleaning: `0`
- Empty fields without `absent_fields`: `0`
- Nonempty fields marked absent: `0`
- Rows with zero selector-visible fields: `7`

Cleaned field counts:

| Field | Row Coverage | Item Count |
|---|---:|---:|
| `use_conditions` | 3241 | 4642 |
| `input_preconditions` | 1378 | 2440 |
| `output_artifacts` | 1914 | 3341 |
| `workflow_steps` | 1962 | 5618 |
| `constraints_boundaries` | 1508 | 2818 |
| `dependencies_resources` | 1918 | 4028 |
| `success_criteria` | 1521 | 2657 |

## Interpretation

This pass supports using `I3C_V2_top20_pool_cleaned.jsonl` as the structured-field representation for the next SkillRouter-Eval-Core external-validation experiment.

It does not yet show whether I3C improves retrieval. The next step is to run the SkillRouter-Eval-Core evaluation over the fixed top-20 candidate pool and report Hit@1, MRR@10, Recall@k, FullCoverage@k, nDCG@10, and representation/token cost for I1, I2, and I3C.

## Caveats

- The pool is task-relevant and fixed-candidate. It is suitable for reranking/information-layer ablation, not for claiming full-library retrieval performance.
- Sparse public skills remain sparse in I3C by design. Missing or weak fields are recorded in `absent_fields`, `field_warnings`, and `qa_warnings` rather than made selector-visible.
- Seven rows have no selector-visible fields after conservative extraction. They should be retained as realistic sparse-artifact cases unless they cause evaluator failures.
