---
name: crm-ops-timeline-builder
description: Builds a timeline for CRM and sales operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Crm Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from CRM records, account notes, opportunity fields, email history.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: CRM records, account notes, opportunity fields, email history.

## Dependencies and resources

- CRM export
- account stage
- contact fields
- activity history
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
