---
name: security-ops-risk-reviewer
description: Reviews application security operations material for operational, compliance, security, quality, or delivery risk.
---

# Security Ops Risk Reviewer

## Use when

- The user wants risk findings from repository files, threat notes, scan findings, architecture description rather than extraction or formatting.

## Input and preconditions

- The task includes enough context to identify impact, likelihood, and mitigation.
- Relevant material: repository files, threat notes, scan findings, architecture description.

## Dependencies and resources

- codebase
- architecture context
- security findings
- asset list
- task-specific constraints

## Procedure

1. Identify concrete risks in the supplied material.
2. Estimate impact and likelihood using the available evidence.
3. Connect each material risk to a mitigation or an owner question.
4. Return a prioritised risk register.

## Output

Risk register with severity, evidence, mitigation, and owner questions.
