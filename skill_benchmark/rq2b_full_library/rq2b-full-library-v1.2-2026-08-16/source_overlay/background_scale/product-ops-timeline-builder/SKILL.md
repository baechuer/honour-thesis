---
name: product-ops-timeline-builder
description: Builds a timeline for product management operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Product Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from feature brief, roadmap item, user feedback, acceptance criteria.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: feature brief, roadmap item, user feedback, acceptance criteria.

## Dependencies and resources

- feature brief
- user feedback
- roadmap context
- acceptance criteria
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
