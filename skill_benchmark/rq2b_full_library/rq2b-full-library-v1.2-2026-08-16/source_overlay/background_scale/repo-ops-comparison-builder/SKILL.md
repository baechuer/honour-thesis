---
name: repo-ops-comparison-builder
description: Compares multiple repository and engineering workflow items by criteria, differences, conflicts, tradeoffs, and decision relevance.
---

# Repo Ops Comparison Builder

## Use when

- The user wants comparison across two or more repository and engineering workflow sources or options.

## Input and preconditions

- At least two comparable items and evaluation criteria are available.
- Relevant material: pull request, diff, CI logs, issue description.

## Dependencies and resources

- repository diff
- test output
- issue context
- review policy
- task-specific constraints

## Procedure

1. Identify the items and criteria that make the comparison meaningful.
2. Extract comparable evidence for each criterion.
3. Surface material differences, trade-offs, and missing evidence.
4. Return the comparison table with bounded recommendation notes.

## Output

Comparison table with criteria, differences, tradeoffs, and recommendation caveats.
