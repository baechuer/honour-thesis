---
name: risk-ops-timeline-builder
description: Builds a timeline for risk management operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Risk Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from risk register, control report, incident note, mitigation plan.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: risk register, control report, incident note, mitigation plan.

## Dependencies and resources

- risk taxonomy
- control evidence
- owner map
- impact scale
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
