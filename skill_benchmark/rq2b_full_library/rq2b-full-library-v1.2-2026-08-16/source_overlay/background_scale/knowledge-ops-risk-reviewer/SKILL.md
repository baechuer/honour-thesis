---
name: knowledge-ops-risk-reviewer
description: Reviews knowledge management operations material for operational, compliance, security, quality, or delivery risk.
---

# Knowledge Ops Risk Reviewer

## Use when

- The user wants risk findings from notes, wiki pages, knowledge base articles, taxonomy rather than extraction or formatting.

## Input and preconditions

- The task includes enough context to identify impact, likelihood, and mitigation.
- Relevant material: notes, wiki pages, knowledge base articles, taxonomy.

## Dependencies and resources

- note corpus
- taxonomy
- source links
- owner context
- task-specific constraints

## Procedure

1. Identify concrete risks in the supplied material.
2. Estimate impact and likelihood using the available evidence.
3. Connect each material risk to a mitigation or an owner question.
4. Return a prioritised risk register.

## Output

Risk register with severity, evidence, mitigation, and owner questions.
