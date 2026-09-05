# External SkillRouter I3C V2 Full-All Extraction Launch - 2026-06-19

## Purpose

The external validation direction has been expanded from the task-relevant top-20 candidate pool to full SkillRouter-Eval-Core I3C V2 extraction.

The goal is to parse every SkillRouter skill in `all_I2.jsonl` into the thesis I3C seven-field representation so later experiments can evaluate I3C under full-library or full-tier conditions, not only fixed-candidate top-20 reranking.

## Source

- Full source: `skill_benchmark/external/skillrouter_eval_core/derived/representations/all_I2.jsonl`
- Source rows: `79141`
- This corresponds to the full hard-tier SkillRouter universe, which contains all Easy skills plus Hard-only distractors.

## Seeded Rows

- Seed source: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_top20_pool/I3C_V2_top20_pool_cleaned.jsonl`
- Seeded rows: `3284`
- Reason for seeding: the cleaned top-20 pool already passed I3C V2 QA with `0` parse failures and `25544/25544` exact evidence matches.
- Older DeepSeek `I3M` and older V1-style I3C slices are not seeded into this full V2 representation because they use different extraction protocols.

## Remaining Work

- Remaining rows to extract: `75857`
- Chunk size: `100`
- Missing chunk count: `759`
- Preparation script: `skill_benchmark/scripts/prepare_skillrouter_i3c_full_extraction.py`
- Working directory: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_full_all`
- Manifest: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_full_all/manifest.json`
- Seed cache: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_full_all/cached/I3C_V2_full_all_seed_top20_cleaned.jsonl`

## Extraction Rules

- Prompt/schema: `skill_benchmark/extraction_prompts/I3C_SUBAGENT_EXTRACTION_V2.md`
- Fields:
  - `use_conditions`
  - `input_preconditions`
  - `output_artifacts`
  - `workflow_steps`
  - `constraints_boundaries`
  - `dependencies_resources`
  - `success_criteria`
- Worker chunk size: `100` skills per subagent unless the final chunk is smaller.
- No external APIs.
- No online search.
- Use only the source artifact text.
- Each worker must validate JSON parsing, row count, identity alignment, and exact evidence substrings before completion.

## Completion Criteria

This step counts as complete only when:

- Seeded rows plus extracted missing rows cover all `79141` SkillRouter skills.
- Every output chunk has the expected row count.
- Merged full I3C V2 has `0` missing skill ids and `0` duplicate skill ids.
- Parse-failed rows are counted and repaired or explicitly documented.
- Selector-visible evidence strings are validated against source artifacts.
- Heading-only evidence is cleaned or documented.
- The final canonical full-all I3C file and quality report are written and referenced in the methodology tracker.

## Current Status

- Manifest prepared.
- Seed cache prepared.
- Missing chunks prepared.
- First extraction wave is being launched after this checkpoint.
