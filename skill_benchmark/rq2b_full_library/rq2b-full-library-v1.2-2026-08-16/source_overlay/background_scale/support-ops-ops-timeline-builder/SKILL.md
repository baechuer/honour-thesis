---
name: support-ops-ops-timeline-builder
description: Builds a timeline for support process operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Support Ops Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from support macro, escalation rule, queue report, knowledge base article.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: support macro, escalation rule, queue report, knowledge base article.

## Dependencies and resources

- support policy
- queue data
- macro library
- escalation owner
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
