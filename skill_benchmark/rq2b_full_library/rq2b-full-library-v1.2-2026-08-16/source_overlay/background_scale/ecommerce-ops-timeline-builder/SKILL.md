---
name: ecommerce-ops-timeline-builder
description: Builds a timeline for ecommerce operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Ecommerce Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from order export, product listing, refund note, marketplace report.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: order export, product listing, refund note, marketplace report.

## Dependencies and resources

- order data
- product catalog
- marketplace rules
- customer message
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
