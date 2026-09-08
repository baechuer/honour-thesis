---
name: vendor-ops-timeline-builder
description: Builds a timeline for vendor and procurement review events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Vendor Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from vendor proposal, security questionnaire, pricing sheet, contract summary.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: vendor proposal, security questionnaire, pricing sheet, contract summary.

## Dependencies and resources

- vendor profile
- pricing document
- security answers
- procurement criteria
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
