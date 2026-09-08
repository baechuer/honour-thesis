---
name: dataset-ops-risk-reviewer
description: Reviews dataset and analytics preparation material for operational, compliance, security, quality, or delivery risk.
---

# Dataset Ops Risk Reviewer

## Use when

- The user wants risk findings from CSV files, data dictionary, metric definitions, quality notes rather than extraction or formatting.

## Input and preconditions

- The task includes enough context to identify impact, likelihood, and mitigation.
- Relevant material: CSV files, data dictionary, metric definitions, quality notes.

## Dependencies and resources

- dataset file
- schema
- metric definitions
- sampling notes
- task-specific constraints

## Procedure

1. Identify concrete risks in the supplied material.
2. Estimate impact and likelihood using the available evidence.
3. Connect each material risk to a mitigation or an owner question.
4. Return a prioritised risk register.

## Output

Risk register with severity, evidence, mitigation, and owner questions.
