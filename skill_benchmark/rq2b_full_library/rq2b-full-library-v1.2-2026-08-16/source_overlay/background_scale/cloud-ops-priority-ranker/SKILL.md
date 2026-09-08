---
name: cloud-ops-priority-ranker
description: Ranks cloud infrastructure operations items by urgency, impact, effort, dependency, evidence strength, or stakeholder importance.
---

# Cloud Ops Priority Ranker

## Use when

- The user wants prioritization among candidate cloud infrastructure operations items rather than a summary.

## Input and preconditions

- Items and ranking criteria are explicit or inferable from the task context.
- Relevant material: cloud config, resource inventory, deployment note, cost report.

## Dependencies and resources

- cloud account
- resource inventory
- deployment config
- cost data
- task-specific constraints

## Procedure

1. List the candidate items and the applicable ranking criteria.
2. Assess each item against urgency, impact, effort, dependency, and available evidence.
3. Make sensitivity to uncertain criteria explicit.
4. Return the ranked list with rationale.

## Output

Ranked list with scoring criteria, rationale, and sensitivity notes.
