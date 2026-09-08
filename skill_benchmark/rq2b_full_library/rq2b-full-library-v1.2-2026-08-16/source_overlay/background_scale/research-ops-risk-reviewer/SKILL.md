---
name: research-ops-risk-reviewer
description: Reviews research and source review material for operational, compliance, security, quality, or delivery risk.
---

# Research Ops Risk Reviewer

## Use when

- The user wants risk findings from papers, reports, source notes, citation metadata rather than extraction or formatting.

## Input and preconditions

- The task includes enough context to identify impact, likelihood, and mitigation.
- Relevant material: papers, reports, source notes, citation metadata.

## Dependencies and resources

- source text
- citation metadata
- method section
- evidence snippets
- task-specific constraints

## Procedure

1. Identify concrete risks in the supplied material.
2. Estimate impact and likelihood using the available evidence.
3. Connect each material risk to a mitigation or an owner question.
4. Return a prioritised risk register.

## Output

Risk register with severity, evidence, mitigation, and owner questions.
