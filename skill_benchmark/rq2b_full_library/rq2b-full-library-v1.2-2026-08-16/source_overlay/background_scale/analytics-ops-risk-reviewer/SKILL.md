---
name: analytics-ops-risk-reviewer
description: Reviews analytics and experimentation operations material for operational, compliance, security, quality, or delivery risk.
---

# Analytics Ops Risk Reviewer

## Use when

- The user wants risk findings from experiment result, metric table, cohort data, analytics request rather than extraction or formatting.

## Input and preconditions

- The task includes enough context to identify impact, likelihood, and mitigation.
- Relevant material: experiment result, metric table, cohort data, analytics request.

## Dependencies and resources

- metric definitions
- experiment design
- cohort data
- analysis window
- task-specific constraints

## Procedure

1. Identify concrete risks in the supplied material.
2. Estimate impact and likelihood using the available evidence.
3. Connect each material risk to a mitigation or an owner question.
4. Return a prioritised risk register.

## Output

Risk register with severity, evidence, mitigation, and owner questions.
