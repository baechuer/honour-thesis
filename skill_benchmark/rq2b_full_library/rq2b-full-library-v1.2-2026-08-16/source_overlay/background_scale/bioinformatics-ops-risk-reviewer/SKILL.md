---
name: bioinformatics-ops-risk-reviewer
description: Reviews bioinformatics operations material for operational, compliance, security, quality, or delivery risk.
---

# Bioinformatics Ops Risk Reviewer

## Use when

- The user wants risk findings from sequence file, variant table, pipeline log, sample metadata rather than extraction or formatting.

## Input and preconditions

- The task includes enough context to identify impact, likelihood, and mitigation.
- Relevant material: sequence file, variant table, pipeline log, sample metadata.

## Dependencies and resources

- sequence data
- sample metadata
- pipeline config
- reference genome
- task-specific constraints

## Procedure

1. Identify concrete risks in the supplied material.
2. Estimate impact and likelihood using the available evidence.
3. Connect each material risk to a mitigation or an owner question.
4. Return a prioritised risk register.

## Output

Risk register with severity, evidence, mitigation, and owner questions.
