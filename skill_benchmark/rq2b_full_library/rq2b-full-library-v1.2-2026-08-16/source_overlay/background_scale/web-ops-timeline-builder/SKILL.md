---
name: web-ops-timeline-builder
description: Builds a timeline for web automation and QA events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Web Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from web page, browser state, test flow, screenshot evidence.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: web page, browser state, test flow, screenshot evidence.

## Dependencies and resources

- web target
- browser runtime
- test data
- screenshot evidence
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
