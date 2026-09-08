---
name: support-ops-failure-diagnoser
description: Diagnoses why a customer support operations workflow, artifact, or previous answer failed to meet expectations.
---

# Support Ops Failure Diagnoser

## Use when

- The user wants failure analysis for customer support operations rather than a fresh artifact.

## Input and preconditions

- There is a failed output, error report, mismatch, or user complaint to analyze.
- Relevant material: support tickets, chat transcripts, issue labels, customer history.

## Dependencies and resources

- ticket queue
- customer context
- product area
- severity policy
- task-specific constraints

## Procedure

1. Collect the failed output, expected outcome, and available evidence.
2. Classify the observed mismatch and trace plausible contributing causes.
3. Separate established causes from hypotheses needing verification.
4. Return corrective actions with evidence links.

## Output

Failure classification, evidence, root-cause hypothesis, and corrective action.
