---
name: incident-ops-risk-reviewer
description: Reviews incident and reliability operations material for operational, compliance, security, quality, or delivery risk.
---

# Incident Ops Risk Reviewer

## Use when

- The user wants risk findings from incident timeline, logs, alerts, postmortem notes rather than extraction or formatting.

## Input and preconditions

- The task includes enough context to identify impact, likelihood, and mitigation.
- Relevant material: incident timeline, logs, alerts, postmortem notes.

## Dependencies and resources

- timeline
- service logs
- alert history
- owner map
- task-specific constraints

## Procedure

1. Identify concrete risks in the supplied material.
2. Estimate impact and likelihood using the available evidence.
3. Connect each material risk to a mitigation or an owner question.
4. Return a prioritised risk register.

## Output

Risk register with severity, evidence, mitigation, and owner questions.
