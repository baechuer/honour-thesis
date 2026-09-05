# I3M Local Full-Library Parse Checkpoint - 2026-06-18

## Status

Local full-library model-parsed I3M extraction is complete for `benchmark-v0.4-2026-06-16`.

This run creates a model-parsed structured information layer for all local benchmark skills. It does not replace frozen-v0.4 I3H retrieval results unless a later retrieval experiment explicitly uses the new `I3M_model_parsed` artifact.

## Method Condition

- Script: `skill_benchmark/scripts/model_parse_i3m_skills.py`
- Schema version: `I3_MODEL_EXTRACTION_V1`
- Active prompt: compact strict I3M prompt in the script, using the seven approved I3 fields only.
- Primary provider/model: `deepseek` / `deepseek-v4-flash`
- Fallback model: `deepseek-chat`
- Temperature: `0`
- JSON mode: enabled through `response_format = {"type": "json_object"}`
- Input cap: `max_chars = 22000`
- Truncated rows: `0`
- Resume behavior: append JSONL rows and skip completed `family/skill` keys.

Final full-run command:

```bash
python3 skill_benchmark/scripts/model_parse_i3m_skills.py \
  --mode full \
  --concurrency 30 \
  --timeout 45 \
  --max-retries 0 \
  --fallback-model deepseek-chat \
  --max-chars 22000
```

## Output Artifacts

- Full model-parse QA rows: `skill_benchmark/outputs/i3m/local_i3m_full_model_parse.jsonl`
- Selector-facing representation: `skill_benchmark/representations/I3M_model_parsed.jsonl`
- Full parse report: `skill_benchmark/outputs/i3m/local_i3m_full_model_parse_report.md`
- Full parse summary: `skill_benchmark/outputs/i3m/local_i3m_full_model_parse_report.summary.json`
- Pilot report used as gate: `skill_benchmark/outputs/i3m/local_i3m_pilot_flash_primary_chat_fallback_report.md`

## Pilot Gate

The accepted local pilot condition used `deepseek-v4-flash` primary, `deepseek-chat` fallback, and repaired evidence validation.

- Rows: `60`
- Valid rows: `57` (`95.0%`)
- Parse-failed rows: `0`
- Fallback rows: `2`
- Extracted items: `1063`
- Evidence exact match rate: `99.3%`
- Evidence case-insensitive / whitespace-insensitive match rate: `99.6%`

Manual inspection found the residual invalid rows were near-quote/evidence issues rather than systematic field hallucination. The pilot was accepted with caveats and used to start the full local run.

## Full Local Result

- Rows: `2433`
- Valid rows: `2333` (`95.9%`)
- Rows with validation issues: `100`
- Parse-failed rows: `0`
- Fallback-model rows: `1398`
- Extracted items: `54,989`
- Evidence exact match rate: `98.7%`
- Evidence case-insensitive / whitespace-insensitive match rate: `99.7%`

Field coverage:

| I3M field | Skills with field | Extracted items |
|---|---:|---:|
| `use_conditions` | 2433 | 9198 |
| `input_preconditions` | 2425 | 10141 |
| `output_artifacts` | 2080 | 2499 |
| `workflow_steps` | 2007 | 9830 |
| `constraints_boundaries` | 2433 | 12844 |
| `dependencies_resources` | 2060 | 9455 |
| `success_criteria` | 604 | 1022 |

Group coverage:

| Group | Skills |
|---|---:|
| `background_scale` | 1800 |
| `controlled_core` | 127 |
| `other_local` | 4 |
| `public_imported_background` | 460 |
| `public_style_or_implicit_controlled` | 42 |

## Interpretation

The local full-library I3M extraction is usable as a new information-layer artifact. It shows that the proposed I3 information categories are recoverable at scale from the local library, including generated background skills and imported public skills.

The high fallback count means `deepseek-v4-flash` was not sufficiently reliable alone for strict JSON extraction. The fallback design should be reported as part of the extraction method, not hidden. This is an important operational caveat for model-parsed information layers.

The 100 issue rows mean I3M is not perfectly clean. Retrieval runs using I3M should either include validation issue indicators in method notes, compare I3M against I3H as an extraction-quality ablation, or repair the small invalid subset before final headline results.

## Next Steps

1. Run coverage/length comparison: I3H/R2 versus I3M.
2. Run retrieval/reranking on I3M under at least one fixed method family.
3. Compare I1, I3H, I3M, and I2 to separate information usefulness from extraction quality.
4. Inspect top recurring evidence-issue patterns before final thesis claims.
5. Keep SkillRouter-Eval-Core I3M as a separate future external-validation step.
