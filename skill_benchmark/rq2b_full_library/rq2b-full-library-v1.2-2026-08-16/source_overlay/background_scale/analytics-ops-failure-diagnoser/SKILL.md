---
name: analytics-ops-failure-diagnoser
description: Diagnoses why a analytics and experimentation operations workflow, artifact, or previous answer failed to meet expectations.
---

# Analytics Ops Failure Diagnoser

## Use when

- The user wants failure analysis for analytics and experimentation operations rather than a fresh artifact.

## Input and preconditions

- There is a failed output, error report, mismatch, or user complaint to analyze.
- Relevant material: experiment result, metric table, cohort data, analytics request.

## Dependencies and resources

- metric definitions
- experiment design
- cohort data
- analysis window
- task-specific constraints

## Procedure

1. Collect the failed output, expected outcome, and available evidence.
2. Classify the observed mismatch and trace plausible contributing causes.
3. Separate established causes from hypotheses needing verification.
4. Return corrective actions with evidence links.

## Output

Failure classification, evidence, root-cause hypothesis, and corrective action.
