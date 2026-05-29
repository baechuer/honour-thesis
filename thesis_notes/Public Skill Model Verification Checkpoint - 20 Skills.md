# Public Skill Model Verification Checkpoint - 20 Skills

Date: 2026-05-29

Purpose: record the first Step 6 model-assisted semantic verification run so it does not need to be rerun unless the schema, prompt, model, or field definitions change.

## Run

Command:

```bash
python3 skill_benchmark/scripts/model_verify_public_skill_fields.py --limit 20
python3 skill_benchmark/scripts/compare_public_skill_field_audits.py
```

Provider/model:

- Provider: DeepSeek API
- Base URL: `https://api.deepseek.com`
- Model: `deepseek-v4-flash`

Outputs:

- `skill_benchmark/outputs/public_skill_field_model_audit.jsonl`
- `skill_benchmark/outputs/public_skill_field_agreement_report.json`
- `skill_benchmark/outputs/public_skill_field_agreement_report.md`

Run result:

- Selected skills: 20
- New model-audited skills: 20
- API calls: 20
- Cached rows: 20

## Agreement Summary

| Field | Agreement | Both Present | Both Missing | Heuristic Only | Model Only |
|---|---:|---:|---:|---:|---:|
| `routing_trigger` | 95.0% | 19 | 0 | 1 | 0 |
| `input_precondition` | 80.0% | 15 | 1 | 1 | 3 |
| `output_artifact` | 75.0% | 15 | 0 | 0 | 5 |
| `workflow_procedure` | 85.0% | 16 | 1 | 2 | 1 |
| `constraints_boundaries` | 75.0% | 11 | 4 | 2 | 3 |
| `dependencies_tools` | 75.0% | 12 | 3 | 1 | 4 |
| `resources_references` | 85.0% | 15 | 2 | 1 | 2 |
| `examples_tests` | 90.0% | 15 | 3 | 2 | 0 |
| `safety_side_effects` | 85.0% | 7 | 10 | 2 | 1 |
| `portability_environment` | 75.0% | 12 | 3 | 3 | 2 |
| `hierarchy_links` | 90.0% | 12 | 6 | 0 | 2 |

## Interpretation

The 20-skill checkpoint supports using model-assisted extraction as a useful semantic verifier:

- high agreement for routing trigger, examples/tests, hierarchy links, safety/side effects, resources/references, and workflow/procedure
- moderate disagreement for output artifact, constraints/boundaries, dependencies/tools, and portability/environment
- model-only cases often reveal semantic evidence missed by keyword rules
- heuristic-only cases often reveal keyword overcounts or broad metadata overcounts

This aligns with the subagent pilot: public skills often contain procedural signals, but those signals are inconsistently normalized.

## Important Caveat

The evidence-span check exposed a model-output problem: some model-present labels did not pass exact substring matching against the skill text. This likely means the model sometimes paraphrased or shortened a quote rather than copying it exactly.

Therefore:

- Treat the model pass as a semantic verifier, not ground truth.
- Prioritize disagreement cases for manual review.
- Before scaling to all 200 skills, consider tightening the model prompt or post-processing to require exact copied spans more aggressively.
- Do not report model agreement as validated annotation without manual calibration.

## Next Step

Review the disagreement cases in:

- `skill_benchmark/outputs/public_skill_field_agreement_report.md`

Then decide whether to:

1. tighten the model prompt and rerun this same 20-skill checkpoint, or
2. accept this as a semantic-verification sample and manually review disagreement cases before scaling.
