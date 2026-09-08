---
name: legal-discovery-ops-failure-diagnoser
description: Diagnoses why a legal discovery operations workflow, artifact, or previous answer failed to meet expectations.
---

# Legal Discovery Ops Failure Diagnoser

## Use when

- The user wants failure analysis for legal discovery operations rather than a fresh artifact.

## Input and preconditions

- There is a failed output, error report, mismatch, or user complaint to analyze.
- Relevant material: document production, privilege log, deposition note, evidence request.

## Dependencies and resources

- case context
- document set
- privilege criteria
- request scope
- task-specific constraints

## Procedure

1. Collect the failed output, expected outcome, and available evidence.
2. Classify the observed mismatch and trace plausible contributing causes.
3. Separate established causes from hypotheses needing verification.
4. Return corrective actions with evidence links.

## Output

Failure classification, evidence, root-cause hypothesis, and corrective action.
