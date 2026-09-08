---
name: mobile-ops-timeline-builder
description: Builds a timeline for mobile application operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Mobile Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from app crash log, release note, store review, mobile test report.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: app crash log, release note, store review, mobile test report.

## Dependencies and resources

- mobile app build
- device context
- crash log
- release channel
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
