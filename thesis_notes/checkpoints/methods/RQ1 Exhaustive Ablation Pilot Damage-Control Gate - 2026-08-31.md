# RQ1 Exhaustive Ablation Pilot Damage-Control Gate

Date: 2026-08-31

Status: `TARGET CLEARANCE COMPLETE / CONTROL GATE BLOCKED / NO SCORING`

## Target Clearance

- Single-field units: 14/14 `CLEAR`
- Candidate masks: 49/49 `CLEAR`
- Clearance rounds: four in round one, six in round two, four in round three
- Final ledger: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/pilot_clearance/final/FINAL_CLEARANCE_LEDGER.json`

## Damage-Control Materialisation

- Deterministic seeds: 1103, 2207, 3301
- Candidate-control documents: 147
- Target carrier lines altered: zero
- Units with at least two mechanically valid controls for every candidate: 6/14

| Unit | Field | Mechanical status |
|---|---|---|
| EXA-P001 | use condition | fail |
| EXA-P002 | input/precondition | eligible |
| EXA-P003 | output/artifact | fail |
| EXA-P004 | workflow/procedure | fail |
| EXA-P005 | success/verification | fail |
| EXA-P006 | boundary/not-for | fail |
| EXA-P007 | dependency/resource | eligible |
| EXA-P008 | use condition | eligible |
| EXA-P009 | input/precondition | eligible |
| EXA-P010 | output/artifact | fail |
| EXA-P011 | workflow/procedure | fail |
| EXA-P012 | success/verification | eligible |
| EXA-P013 | boundary/not-for | eligible |
| EXA-P014 | dependency/resource | fail |

## Blocking Finding

At least one pilot composition is eligible for five field families. Neither
output/artifact nor workflow/procedure has an eligible pilot composition. Their
target spans occupy too much of at least one candidate document to permit a
same-volume non-target deletion within the frozen tolerance. This is not a
selector result and does not show that either field lacks routing value.

The next action requires a protocol decision: select replacement pilot
compositions for output/workflow, or redesign the matched-damage control and
record a prospective amendment. Do not relax the tolerance or score unmatched
conditions retrospectively.
