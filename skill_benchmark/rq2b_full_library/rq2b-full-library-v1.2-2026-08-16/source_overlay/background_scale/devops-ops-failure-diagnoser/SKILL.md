---
name: devops-ops-failure-diagnoser
description: Diagnoses why a DevOps pipeline operations workflow, artifact, or previous answer failed to meet expectations.
---

# Devops Ops Failure Diagnoser

## Use when

- The user wants failure analysis for DevOps pipeline operations rather than a fresh artifact.

## Input and preconditions

- There is a failed output, error report, mismatch, or user complaint to analyze.
- Relevant material: pipeline log, build script, deploy config, release checklist.

## Dependencies and resources

- CI logs
- build config
- environment variables
- release target
- task-specific constraints

## Procedure

1. Collect the failed output, expected outcome, and available evidence.
2. Classify the observed mismatch and trace plausible contributing causes.
3. Separate established causes from hypotheses needing verification.
4. Return corrective actions with evidence links.

## Output

Failure classification, evidence, root-cause hypothesis, and corrective action.
