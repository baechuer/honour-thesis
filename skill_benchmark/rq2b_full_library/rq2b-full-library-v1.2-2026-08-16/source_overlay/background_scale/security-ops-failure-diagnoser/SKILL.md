---
name: security-ops-failure-diagnoser
description: Diagnoses why a application security operations workflow, artifact, or previous answer failed to meet expectations.
---

# Security Ops Failure Diagnoser

## Use when

- The user wants failure analysis for application security operations rather than a fresh artifact.

## Input and preconditions

- There is a failed output, error report, mismatch, or user complaint to analyze.
- Relevant material: repository files, threat notes, scan findings, architecture description.

## Dependencies and resources

- codebase
- architecture context
- security findings
- asset list
- task-specific constraints

## Procedure

1. Collect the failed output, expected outcome, and available evidence.
2. Classify the observed mismatch and trace plausible contributing causes.
3. Separate established causes from hypotheses needing verification.
4. Return corrective actions with evidence links.

## Output

Failure classification, evidence, root-cause hypothesis, and corrective action.
