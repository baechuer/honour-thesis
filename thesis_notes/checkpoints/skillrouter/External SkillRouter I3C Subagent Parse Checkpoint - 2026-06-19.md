# External SkillRouter I3C Subagent Parse Checkpoint - 2026-06-19

Purpose: create an auxiliary no-provider-API `I3C` extraction track for SkillRouter-Eval-Core skills, using Codex subagents rather than DeepSeek/Qwen API calls.

Status: completed for rows `3000-5999` of `skill_benchmark/external/skillrouter_eval_core/derived/representations/all_I2.jsonl`.

## Framing

This is **not** a replacement for `I3M`.

- `I3M`: model-parsed I3 using the recorded DeepSeek extraction protocol and provider API.
- `I3C`: Codex/subagent-parsed I3, produced without external provider API calls.

Use `I3C` as a candidate practical extraction route after QA gates. It is useful for checking whether a cheaper human-like parsing process can recover selection fields, but it introduces a different extractor and should not be mixed into the main result table without being clearly labeled.

## Work Completed

Created 30 input chunks of 100 skills each:

- Input range: `3000-5999`
- Input directory: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_subagent_chunks/inputs/`
- Output directory: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_subagent_chunks/outputs/`
- Manifest: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_subagent_chunks/manifest.json`

Subagent execution:

- Requested concurrency: 30 agents.
- Actual app concurrency cap: 6 active agents.
- Execution strategy: rolling queue until all 30 chunks completed.
- Model override: `gpt-5.4-mini`
- Reasoning effort: low
- External API use: disallowed in worker prompts.
- Each worker owned exactly one input JSONL and one output/report pair.

## Canonical Output

Merged and normalized output:

- `skill_benchmark/external/skillrouter_eval_core/derived/representations/I3C_codex_subagent_rows_03000_05999.jsonl`
- `skill_benchmark/external/skillrouter_eval_core/derived/representations/I3C_codex_subagent_rows_03000_05999.summary.json`

Normalizer script:

- `skill_benchmark/scripts/merge_i3c_subagent_chunks.py`

The normalizer was needed because 5 of the 30 worker outputs placed the seven I3 fields at the top level instead of under `fields`, and the final chunk omitted identity metadata. The normalizer now overlays worker output onto the original input rows by order, preserving skill ids while canonicalizing the output shape.

## Validation Summary

Overall status: **PASS WITH CAVEATS** for extraction feasibility; **not yet approved** as unchecked headline extraction ground truth.

Canonical merged file:

| Metric | Value |
|---|---:|
| Source chunk files | 30 |
| Rows | 3000 |
| Parse-failed rows | 0 |
| Missing skill ids after merge repair | 0 |
| Schema-shape errors after normalization | 0 |
| Non-object field items after normalization | 0 |
| Items missing evidence after normalization | 0 |
| Extracted evidence items | 46129 |
| Exact evidence matches | 45507 |
| Missing exact evidence strings | 620 |
| Missing exact evidence rate | 1.34% |
| Absent-field metadata after normalizer update | recorded |
| QA warning counts in old V1 chunks | 0 |

Field coverage in canonical merged file:

| Field | Rows with non-empty field | Extracted item count |
|---|---:|---:|
| `use_conditions` | 1780 | 4011 |
| `input_preconditions` | 977 | 3019 |
| `output_artifacts` | 1112 | 4500 |
| `workflow_steps` | 1565 | 14447 |
| `constraints_boundaries` | 1054 | 3762 |
| `dependencies_resources` | 1755 | 13344 |
| `success_criteria` | 878 | 3046 |

## Caveats

- Worker extraction is useful but heterogeneous: each subagent followed the same schema prompt, but the actual extraction style may vary.
- Some workers emitted simpler top-level field arrays; this was normalized after the fact.
- Some normalized string items use the extracted text as both `text` and `evidence`; these should be treated as lower-confidence than strict `I3M` evidence spans.
- Manual sample inspection found generally usable fields but occasional broad/background extraction. Therefore, `I3C` can be a practical main extraction candidate only after passing evidence and manual QA gates, and after re-extracting the local controlled benchmark with the same prompt/normalizer.
- Specific manual caveats observed: generic trigger phrases such as "Use this skill when:", checklist fragments appearing under constraints/boundaries, and broad shared-resource skills producing weak dependencies/resources. These are repairable with a stricter worker prompt or a post-parse generic-fragment filter.
- Corrective prompt: `skill_benchmark/extraction_prompts/I3C_SUBAGENT_EXTRACTION_V2.md`. Future I3C runs should use this prompt so subagents check selector-usefulness, skip low-value fragments, and record sparse/generic/missing-field cases in `absent_fields`, `field_warnings`, and `qa_warnings`.
- Normalizer update: `skill_benchmark/scripts/merge_i3c_subagent_chunks.py` now preserves `absent_fields`, `field_warnings`, and `qa_warnings`. The existing V1 chunks do not contain QA warnings, so warning counts remain empty until V2 extraction is run.
- The current rows `3000-5999` are not enough for SkillRouter retrieval evaluation because the 75 scored tasks use 186 unique gold skills at rows `27018-27213`.

## Next Step

If used experimentally, compare `I3C` separately against:

- `I1`: flat metadata
- `I2`: full skill artifact
- `I3H`: heuristic structured extraction
- `I3M`: DeepSeek model-parsed extraction

Do not combine `I3C` and `I3M` rows into one representation layer.
