---
name: search-ops-priority-ranker
description: Ranks search and retrieval operations items by urgency, impact, effort, dependency, evidence strength, or stakeholder importance.
---

# Search Ops Priority Ranker

## Use when

- The user wants prioritization among candidate search and retrieval operations items rather than a summary.

## Input and preconditions

- Items and ranking criteria are explicit or inferable from the task context.
- Relevant material: search query log, retrieval results, index schema, relevance judgment.

## Dependencies and resources

- query logs
- index schema
- relevance labels
- retrieval config
- task-specific constraints

## Procedure

1. List the candidate items and the applicable ranking criteria.
2. Assess each item against urgency, impact, effort, dependency, and available evidence.
3. Make sensitivity to uncertain criteria explicit.
4. Return the ranked list with rationale.

## Output

Ranked list with scoring criteria, rationale, and sensitivity notes.
