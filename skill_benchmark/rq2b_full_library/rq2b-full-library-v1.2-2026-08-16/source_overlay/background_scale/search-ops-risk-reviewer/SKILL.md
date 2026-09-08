---
name: search-ops-risk-reviewer
description: Reviews search and retrieval operations material for operational, compliance, security, quality, or delivery risk.
---

# Search Ops Risk Reviewer

## Use when

- The user wants risk findings from search query log, retrieval results, index schema, relevance judgment rather than extraction or formatting.

## Input and preconditions

- The task includes enough context to identify impact, likelihood, and mitigation.
- Relevant material: search query log, retrieval results, index schema, relevance judgment.

## Dependencies and resources

- query logs
- index schema
- relevance labels
- retrieval config
- task-specific constraints

## Procedure

1. Identify concrete risks in the supplied material.
2. Estimate impact and likelihood using the available evidence.
3. Connect each material risk to a mitigation or an owner question.
4. Return a prioritised risk register.

## Output

Risk register with severity, evidence, mitigation, and owner questions.
