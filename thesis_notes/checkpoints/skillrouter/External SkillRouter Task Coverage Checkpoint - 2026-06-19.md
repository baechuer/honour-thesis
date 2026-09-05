# External SkillRouter Task Coverage Checkpoint - 2026-06-19

Purpose: verify whether the external I3 extraction slices currently overlap the scored SkillRouter-Eval-Core tasks.

## Source Files

- Skill artifacts: `skill_benchmark/external/skillrouter_eval_core/derived/representations/all_I2.jsonl`
- Scored tasks: `skill_benchmark/external/skillrouter_eval_core/derived/tasks_scored.jsonl`
- Relevance labels: `skill_benchmark/external/skillrouter_eval_core/raw/relevance.json`
- I3M completed slice: rows `0-2999`
- I3C completed slice: rows `3000-5999`

## Coverage Result

| Item | Value |
|---|---:|
| Scored tasks | 75 |
| Unique core gold skill ids | 186 |
| Missing gold ids from `all_I2.jsonl` | 0 |
| Minimum gold row index | 27018 |
| Maximum gold row index | 27213 |
| Gold skills in I3M rows `0-2999` | 0 |
| Gold skills in I3C rows `3000-5999` | 0 |
| Gold skills in current extracted rows `0-5999` | 0 |

## Interpretation

The completed I3M/I3C extraction slices are useful extraction-quality pilots, but they are not yet evaluable external retrieval conditions for SkillRouter-Eval-Core. A retrieval run over only those slices would test the wrong candidate universe and would contain none of the scored gold skills.

## Required Next Step

Before external I3M/I3C retrieval claims:

1. Define the external candidate universe:
   - full Easy/Hard tier; or
   - a fixed task-relevant candidate pool generated independently of I3M/I3C.
2. Parse that candidate universe into I3M and/or I3C.
3. Run SkillRouter metrics using the same universe for each information layer:
   - Hit@1;
   - MRR@10;
   - Recall@k;
   - FullCoverage@k;
   - nDCG@10.

Do not compare partial-slice I3M/I3C results against full-library I1/I2/I3H results.
