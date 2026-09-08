---
name: support-ops-risk-reviewer
description: Reviews customer support operations material for operational, compliance, security, quality, or delivery risk.
---

# Support Ops Risk Reviewer

## Use when

- The user wants risk findings from support tickets, chat transcripts, issue labels, customer history rather than extraction or formatting.

## Input and preconditions

- The task includes enough context to identify impact, likelihood, and mitigation.
- Relevant material: support tickets, chat transcripts, issue labels, customer history.

## Dependencies and resources

- ticket queue
- customer context
- product area
- severity policy
- task-specific constraints

## Procedure

1. Identify concrete risks in the supplied material.
2. Estimate impact and likelihood using the available evidence.
3. Connect each material risk to a mitigation or an owner question.
4. Return a prioritised risk register.

## Output

Risk register with severity, evidence, mitigation, and owner questions.
