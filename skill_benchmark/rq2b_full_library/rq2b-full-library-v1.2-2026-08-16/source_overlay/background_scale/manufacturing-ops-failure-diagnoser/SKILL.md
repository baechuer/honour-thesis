---
name: manufacturing-ops-failure-diagnoser
description: Diagnoses why a manufacturing operations workflow, artifact, or previous answer failed to meet expectations.
---

# Manufacturing Ops Failure Diagnoser

## Use when

- The user wants failure analysis for manufacturing operations rather than a fresh artifact.

## Input and preconditions

- There is a failed output, error report, mismatch, or user complaint to analyze.
- Relevant material: work order, defect log, production schedule, quality report.

## Dependencies and resources

- work order
- production line
- quality criteria
- operator notes
- task-specific constraints

## Procedure

1. Collect the failed output, expected outcome, and available evidence.
2. Classify the observed mismatch and trace plausible contributing causes.
3. Separate established causes from hypotheses needing verification.
4. Return corrective actions with evidence links.

## Output

Failure classification, evidence, root-cause hypothesis, and corrective action.
