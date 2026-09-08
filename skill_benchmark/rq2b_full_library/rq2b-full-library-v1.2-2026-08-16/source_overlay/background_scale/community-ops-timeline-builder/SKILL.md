---
name: community-ops-timeline-builder
description: Builds a timeline for community management operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Community Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from forum post, moderation queue, announcement draft, user feedback thread.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: forum post, moderation queue, announcement draft, user feedback thread.

## Dependencies and resources

- community guidelines
- thread context
- user history
- announcement goal
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
