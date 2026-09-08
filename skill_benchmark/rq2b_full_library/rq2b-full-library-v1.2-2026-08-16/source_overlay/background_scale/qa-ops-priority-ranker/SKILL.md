---
name: qa-ops-priority-ranker
description: Ranks quality assurance operations items by urgency, impact, effort, dependency, evidence strength, or stakeholder importance.
---

# Qa Ops Priority Ranker

## Use when

- The user wants prioritization among candidate quality assurance operations items rather than a summary.

## Input and preconditions

- Items and ranking criteria are explicit or inferable from the task context.
- Relevant material: test plan, defect report, acceptance criteria, release evidence.

## Dependencies and resources

- test plan
- defect log
- acceptance criteria
- release scope
- task-specific constraints

## Procedure

1. List the candidate items and the applicable ranking criteria.
2. Assess each item against urgency, impact, effort, dependency, and available evidence.
3. Make sensitivity to uncertain criteria explicit.
4. Return the ranked list with rationale.

## Output

Ranked list with scoring criteria, rationale, and sensitivity notes.
