---
name: robotics-ops-failure-diagnoser
description: Diagnoses why a robotics operations workflow, artifact, or previous answer failed to meet expectations.
---

# Robotics Ops Failure Diagnoser

## Use when

- The user wants failure analysis for robotics operations rather than a fresh artifact.

## Input and preconditions

- There is a failed output, error report, mismatch, or user complaint to analyze.
- Relevant material: robot log, mission plan, sensor trace, calibration note.

## Dependencies and resources

- robot platform
- sensor data
- mission objective
- calibration file
- task-specific constraints

## Procedure

1. Collect the failed output, expected outcome, and available evidence.
2. Classify the observed mismatch and trace plausible contributing causes.
3. Separate established causes from hypotheses needing verification.
4. Return corrective actions with evidence links.

## Output

Failure classification, evidence, root-cause hypothesis, and corrective action.
