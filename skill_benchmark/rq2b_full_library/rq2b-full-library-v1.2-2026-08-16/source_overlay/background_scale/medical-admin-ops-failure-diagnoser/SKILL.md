---
name: medical-admin-ops-failure-diagnoser
description: Diagnoses why a medical administration operations workflow, artifact, or previous answer failed to meet expectations.
---

# Medical Admin Ops Failure Diagnoser

## Use when

- The user wants failure analysis for medical administration operations rather than a fresh artifact.

## Input and preconditions

- There is a failed output, error report, mismatch, or user complaint to analyze.
- Relevant material: appointment note, referral text, intake form, clinic instruction.

## Dependencies and resources

- patient-provided note
- appointment details
- clinic policy
- form fields
- task-specific constraints

## Procedure

1. Collect the failed output, expected outcome, and available evidence.
2. Classify the observed mismatch and trace plausible contributing causes.
3. Separate established causes from hypotheses needing verification.
4. Return corrective actions with evidence links.

## Output

Failure classification, evidence, root-cause hypothesis, and corrective action.
