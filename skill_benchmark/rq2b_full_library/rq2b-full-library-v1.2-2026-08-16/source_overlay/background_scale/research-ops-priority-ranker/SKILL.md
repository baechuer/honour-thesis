---
name: research-ops-priority-ranker
description: Ranks research and source review items by urgency, impact, effort, dependency, evidence strength, or stakeholder importance.
---

# Research Ops Priority Ranker

## Use when

- The user wants prioritization among candidate research and source review items rather than a summary.

## Input and preconditions

- Items and ranking criteria are explicit or inferable from the task context.
- Relevant material: papers, reports, source notes, citation metadata.

## Dependencies and resources

- source text
- citation metadata
- method section
- evidence snippets
- task-specific constraints

## Procedure

1. List the candidate items and the applicable ranking criteria.
2. Assess each item against urgency, impact, effort, dependency, and available evidence.
3. Make sensitivity to uncertain criteria explicit.
4. Return the ranked list with rationale.

## Output

Ranked list with scoring criteria, rationale, and sensitivity notes.
