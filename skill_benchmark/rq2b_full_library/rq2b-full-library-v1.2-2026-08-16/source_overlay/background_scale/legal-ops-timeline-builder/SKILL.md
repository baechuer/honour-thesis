---
name: legal-ops-timeline-builder
description: Builds a timeline for legal and policy operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Legal Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from policy text, legal memo, contract clause, compliance question.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: policy text, legal memo, contract clause, compliance question.

## Dependencies and resources

- legal text
- jurisdiction note
- policy version
- review purpose
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
