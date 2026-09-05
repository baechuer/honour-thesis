# Public Skill Model Verification Checkpoint - 460 Skills

Date: 2026-05-29

Purpose: strengthen Step 6 by checking whether the proposed representation-field taxonomy is visible in public `SKILL.md` artifacts, rather than only in the controlled/generated benchmark skills.

## Run

- Heuristic audit input: `skill_benchmark/outputs/public_skill_field_audit.jsonl`
- Model audit output: `skill_benchmark/outputs/public_skill_field_model_audit.jsonl`
- Agreement report: `skill_benchmark/outputs/public_skill_field_agreement_report.md`
- Disagreement review packet: `skill_benchmark/outputs/public_skill_field_disagreement_review_packet.md`
- Public skills compared: 460/460
- Provider: DeepSeek-compatible chat verifier, with strict JSON/evidence schema

The verifier was resumed from the earlier 200-skill checkpoint and completed the full 460-skill imported public set. The script is now resumable and supports bounded concurrency.

## Model-Assisted Field Prevalence

| Field | Model Present | Read |
|---|---:|---|
| `routing_trigger` | 394/460, 85.7% | observed, but broad descriptions are sometimes not true triggers |
| `input_precondition` | 314/460, 68.3% | often extractable rather than cleanly labelled |
| `output_artifact` | 369/460, 80.2% | observed/extractable |
| `workflow_procedure` | 416/460, 90.4% | strongly observed |
| `constraints_boundaries` | 346/460, 75.2% | observed, but definition-sensitive |
| `dependencies_tools` | 412/460, 89.6% | strongly observed |
| `resources_references` | 355/460, 77.2% | observed/extractable |
| `examples_tests` | 403/460, 87.6% | strongly observed |
| `safety_side_effects` | 137/460, 29.8% | weakly observed/proposed |
| `portability_environment` | 341/460, 74.1% | observed/extractable |
| `hierarchy_links` | 238/460, 51.7% | partially observed |

## Agreement With Heuristic Audit

Highest agreement:

- `examples_tests`: 91.1%
- `dependencies_tools`: 85.9%
- `routing_trigger`: 85.7%
- `workflow_procedure`: 83.9%
- `constraints_boundaries`: 81.5%

Lowest agreement:

- `safety_side_effects`: 66.7%
- `hierarchy_links`: 69.8%
- `input_precondition`: 70.2%
- `output_artifact`: 75.4%

Interpretation: the core procedural fields are grounded in public skills, but the boundary fields need careful definitions. Hierarchy is often missed by keyword heuristics because it appears as related-skill prose or route-outs. Safety/side-effect evidence is sparse and definition-sensitive.

## Thesis Interpretation

This checkpoint supports the current thesis framing:

> Public skills often contain procedural signals, but those signals are unevenly expressed. A scalable representation layer should extract and normalize retrieval-critical fields rather than assuming authors provide clean schemas.

The result does not mean every public skill already has ideal structured metadata. It means that fields such as workflow, dependencies, outputs, examples, resources, and routing intent are common enough to be realistic representation targets.

## Caveats

- Model extraction is not a gold-standard human annotation.
- Some model evidence was difficult to verify exactly because public skills contain long code/YAML blocks and the verifier sometimes returned long quotes.
- The disagreement packet still needs manual review before final prevalence numbers are used as strong thesis evidence.
- `safety_side_effects` should be framed as a proposed reliability/quality field, not a mature public-skill convention.
- `constraints_boundaries` should be split conceptually between procedural constraints, scope boundaries, and negative routing conditions.

## Next Use

Use this checkpoint to freeze the field taxonomy before final Step 7/Step 9 claims. Do not keep expanding public skills unless the taxonomy changes materially.
