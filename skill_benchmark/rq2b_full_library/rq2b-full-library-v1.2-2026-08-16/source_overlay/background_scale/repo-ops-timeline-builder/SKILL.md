---
name: repo-ops-timeline-builder
description: Builds a timeline for repository and engineering workflow events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Repo Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from pull request, diff, CI logs, issue description.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: pull request, diff, CI logs, issue description.

## Dependencies and resources

- repository diff
- test output
- issue context
- review policy
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
