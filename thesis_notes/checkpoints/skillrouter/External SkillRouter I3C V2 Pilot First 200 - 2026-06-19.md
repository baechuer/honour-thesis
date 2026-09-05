# External SkillRouter I3C V2 Pilot First 200 - 2026-06-19

Purpose: verify whether `I3C_SUBAGENT_EXTRACTION_V2` improves ChatGPT/Codex-subagent extraction quality before scaling to the SkillRouter-Eval-Core task-relevant pools.

## Setup

- Source pool: `skill_benchmark/external/skillrouter_eval_core/derived/representations/skillrouter_task_relevant_pool_top20_I2.jsonl`
- Pilot rows: first `200`
- Chunking: `2` subagents, `100` skills per subagent
- Prompt: `skill_benchmark/extraction_prompts/I3C_SUBAGENT_EXTRACTION_V2.md`
- Input folder: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_pilot_first200/inputs/`
- Output folder: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_pilot_first200/outputs/`
- Merged output: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_pilot_first200/I3C_V2_pilot_first200_merged.jsonl`
- Summary: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_pilot_first200/I3C_V2_pilot_first200_summary.json`

Both subagents were closed after output collection.

## Merge / Schema Results

| Metric | Value |
|---|---:|
| Rows requested | 200 |
| Rows merged | 200 |
| Parse-failed rows | 0 |
| Missing skill ids | 0 |
| Extraction schema versions | `I3C_SUBAGENT_EXTRACTION_V2`: 200 |
| Extracted evidence items | 1184 |
| Exact evidence matches | 1184 |
| Missing evidence items | 0 |
| Missing evidence rate | 0.0% |

## Field Coverage

| Field | Rows with field | Extracted items | Absent count |
|---|---:|---:|---:|
| `use_conditions` | 199 | 200 | 1 |
| `input_preconditions` | 91 | 108 | 109 |
| `output_artifacts` | 140 | 157 | 60 |
| `workflow_steps` | 153 | 252 | 47 |
| `constraints_boundaries` | 98 | 119 | 102 |
| `dependencies_resources` | 134 | 220 | 66 |
| `success_criteria` | 100 | 128 | 100 |

## QA Warning Counts

| Warning code | Count |
|---|---:|
| `broad_skill` | 21 |
| `field_absent` | 30 |
| `generic_fragment_skipped` | 6 |
| `limited_selector_content` | 9 |
| `sparse_artifact` | 16 |

## Manual Quality Notes

V2 substantially improves the previous I3C failure mode:

- generic trigger headings such as `Use this skill when:` were not extracted as standalone field evidence;
- sparse and broad skills now receive QA warnings rather than forced field content;
- exact evidence grounding is currently perfect on the 200-row pilot;
- manual samples show more concise, selector-useful fields than V1.

Residual caveat:

- A pattern scan still flags checklist markers, `Output:` labels, and `return` strings in some evidence spans.
- Most inspected cases are legitimate evidence, such as acceptance checklist items, output headings, or code return examples that define artifacts/constraints.
- This is not currently a blocker, but future large runs should keep the suspect-fragment scan as a QA companion.

## Decision

Status: **PASS WITH MINOR QA CAVEATS**.

Recommendation:

1. Scale I3C V2 to the task-relevant top-20 SkillRouter pool first (`3284` skills), not the full 79k library.
2. Keep `100` skills per subagent as requested.
3. Merge and validate after each batch:
   - row count equals requested rows;
   - 0 parse failures;
   - 0 missing skill ids;
   - evidence exact-match at least 95%;
   - warning counts present and interpretable;
   - suspect-fragment scan does not show generic headings being extracted as selector-visible fields.
4. Only after top-20 pool validation should we decide whether to parse the top-50 pool (`7113` skills) or a full Easy/Hard tier.
