---
name: marketing-ops-timeline-builder
description: Builds a timeline for marketing campaign operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Marketing Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from campaign brief, ad copy, audience segment, performance report.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: campaign brief, ad copy, audience segment, performance report.

## Dependencies and resources

- campaign goal
- audience data
- creative assets
- performance metrics
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
