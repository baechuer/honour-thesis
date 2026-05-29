# Public Skill Model Verification Checkpoint - 200 Skills

Date: 2026-05-29

Purpose: record the full Step 6 model-assisted semantic verification run over the imported public-skill corpus.

## Run

The model audit rows were already generated in:

- `skill_benchmark/outputs/public_skill_field_model_audit.jsonl`

Local comparison command rerun:

```bash
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

- Heuristic rows: 200
- Model-audited rows: 200
- Compared skills: 200

## Agreement Summary

| Field | Agreement | Both Present | Both Missing | Heuristic Only | Model Only | Read |
|---|---:|---:|---:|---:|---:|---|
| `routing_trigger` | 68.0% | 136 | 0 | 64 | 0 | high heuristic overcount or model strictness |
| `input_precondition` | 83.0% | 153 | 13 | 22 | 12 | good agreement |
| `output_artifact` | 85.5% | 168 | 3 | 14 | 15 | good agreement |
| `workflow_procedure` | 85.5% | 168 | 3 | 13 | 16 | good agreement |
| `constraints_boundaries` | 81.0% | 116 | 46 | 27 | 11 | good but needs disagreement review |
| `dependencies_tools` | 92.0% | 177 | 7 | 3 | 13 | strongest agreement |
| `resources_references` | 74.5% | 131 | 18 | 42 | 9 | likely heuristic overcount |
| `examples_tests` | 91.5% | 173 | 10 | 14 | 3 | strong agreement |
| `safety_side_effects` | 72.0% | 24 | 120 | 29 | 27 | weak/contested field |
| `portability_environment` | 87.5% | 157 | 18 | 14 | 11 | strong agreement |
| `hierarchy_links` | 88.5% | 86 | 91 | 7 | 16 | strong agreement |

Disagreement total:

- Total field disagreements: 382
- `heuristic_only`: 249
- `model_only`: 133

Most disagreement-prone fields:

1. `routing_trigger`: 64 disagreements
2. `safety_side_effects`: 56 disagreements
3. `resources_references`: 51 disagreements
4. `constraints_boundaries`: 38 disagreements
5. `input_precondition`: 34 disagreements

## Interpretation

The full 200-skill checkpoint strengthens the thesis claim that public skills contain many procedural signals, especially:

- dependencies/tools
- examples/tests
- hierarchy links
- portability/environment
- workflow/procedure
- output artifacts
- input/preconditions

It also sharpens the caveat:

- `routing_trigger` is too easy for the heuristic because every public skill has a frontmatter description, but DeepSeek often refuses to treat broad descriptive metadata as an actual routing condition.
- `resources_references` is likely overcounted by the heuristic when it sees inline templates, related metadata, or generic resource language without concrete files/URLs.
- `safety_side_effects` remains the least stable field: many public skills lack explicit safety, privacy, permission, mutation, or side-effect guidance.

## Methodological Meaning

This is useful for the thesis because it separates field types:

- `observed`: dependencies/tools, workflow/procedure, output artifacts, examples/tests, portability/environment
- `extractable`: input/preconditions, hierarchy links, constraints/boundaries, resources/references
- `proposed or weakly observed`: safety/side effects
- `needs definition refinement`: routing trigger, because broad descriptions should not automatically count as a high-quality routing condition

## Evidence-Span Caveat

The agreement report still shows some model-present labels where exact evidence matching fails. This probably happens because the model shortens, normalizes, or paraphrases quoted text.

Therefore:

- Do not treat the model audit as ground-truth annotation.
- Use the model audit to identify disagreement cases.
- Manually review a targeted sample before reporting final field prevalence.
- If scaling model-assisted verification further, tighten the prompt or post-processing around exact evidence spans.

## Recommended Next Step

Do not rerun the 200-skill model checkpoint unless the schema or prompt changes.

Next work should be:

1. Use `thesis_notes/Public Skill Disagreement Adjudication - Step 6.md` to tighten field definitions.
2. Convert the final field taxonomy into observed / extractable / proposed categories.
3. Use the completed Step 7 field-ablation results to decide which fields belong in the final thesis representation.
