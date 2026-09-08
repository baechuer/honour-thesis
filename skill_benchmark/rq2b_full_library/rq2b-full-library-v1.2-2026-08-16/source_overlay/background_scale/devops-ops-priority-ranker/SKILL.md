---
name: devops-ops-priority-ranker
description: Ranks DevOps pipeline operations items by urgency, impact, effort, dependency, evidence strength, or stakeholder importance.
---

# Devops Ops Priority Ranker

## Use when

- The user wants prioritization among candidate DevOps pipeline operations items rather than a summary.

## Input and preconditions

- Items and ranking criteria are explicit or inferable from the task context.
- Relevant material: pipeline log, build script, deploy config, release checklist.

## Dependencies and resources

- CI logs
- build config
- environment variables
- release target
- task-specific constraints

## Procedure

1. List the candidate items and the applicable ranking criteria.
2. Assess each item against urgency, impact, effort, dependency, and available evidence.
3. Make sensitivity to uncertain criteria explicit.
4. Return the ranked list with rationale.

## Output

Ranked list with scoring criteria, rationale, and sensitivity notes.
