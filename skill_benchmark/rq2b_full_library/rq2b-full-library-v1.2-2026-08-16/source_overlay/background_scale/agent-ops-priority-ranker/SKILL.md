---
name: agent-ops-priority-ranker
description: Ranks agent and skill operations items by urgency, impact, effort, dependency, evidence strength, or stakeholder importance.
---

# Agent Ops Priority Ranker

## Use when

- The user wants prioritization among candidate agent and skill operations items rather than a summary.

## Input and preconditions

- Items and ranking criteria are explicit or inferable from the task context.
- Relevant material: agent traces, tool specs, skill cards, evaluation notes.

## Dependencies and resources

- agent trace
- skill library
- tool definitions
- evaluation criteria
- task-specific constraints

## Procedure

1. List the candidate items and the applicable ranking criteria.
2. Assess each item against urgency, impact, effort, dependency, and available evidence.
3. Make sensitivity to uncertain criteria explicit.
4. Return the ranked list with rationale.

## Output

Ranked list with scoring criteria, rationale, and sensitivity notes.
