---
name: sre-ops-risk-reviewer
description: Reviews site reliability engineering operations material for operational, compliance, security, quality, or delivery risk.
---

# Sre Ops Risk Reviewer

## Use when

- The user wants risk findings from SLO report, runbook, alert history, reliability review rather than extraction or formatting.

## Input and preconditions

- The task includes enough context to identify impact, likelihood, and mitigation.
- Relevant material: SLO report, runbook, alert history, reliability review.

## Dependencies and resources

- service map
- SLO definitions
- alert data
- runbook
- task-specific constraints

## Procedure

1. Identify concrete risks in the supplied material.
2. Estimate impact and likelihood using the available evidence.
3. Connect each material risk to a mitigation or an owner question.
4. Return a prioritised risk register.

## Output

Risk register with severity, evidence, mitigation, and owner questions.
