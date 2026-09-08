---
name: ml-ops-risk-reviewer
description: Reviews machine learning operations material for operational, compliance, security, quality, or delivery risk.
---

# Ml Ops Risk Reviewer

## Use when

- The user wants risk findings from model card, training log, evaluation table, dataset note rather than extraction or formatting.

## Input and preconditions

- The task includes enough context to identify impact, likelihood, and mitigation.
- Relevant material: model card, training log, evaluation table, dataset note.

## Dependencies and resources

- model artifact
- dataset split
- training config
- evaluation metric
- task-specific constraints

## Procedure

1. Identify concrete risks in the supplied material.
2. Estimate impact and likelihood using the available evidence.
3. Connect each material risk to a mitigation or an owner question.
4. Return a prioritised risk register.

## Output

Risk register with severity, evidence, mitigation, and owner questions.
