---
name: supply-chain-ops-priority-ranker
description: Ranks supply chain operations items by urgency, impact, effort, dependency, evidence strength, or stakeholder importance.
---

# Supply Chain Ops Priority Ranker

## Use when

- The user wants prioritization among candidate supply chain operations items rather than a summary.

## Input and preconditions

- Items and ranking criteria are explicit or inferable from the task context.
- Relevant material: supplier update, demand forecast, inventory plan, risk note.

## Dependencies and resources

- supplier list
- forecast data
- inventory position
- risk register
- task-specific constraints

## Procedure

1. List the candidate items and the applicable ranking criteria.
2. Assess each item against urgency, impact, effort, dependency, and available evidence.
3. Make sensitivity to uncertain criteria explicit.
4. Return the ranked list with rationale.

## Output

Ranked list with scoring criteria, rationale, and sensitivity notes.
