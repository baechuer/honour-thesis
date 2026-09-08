---
name: medical-admin-ops-comparison-builder
description: Compares multiple medical administration operations items by criteria, differences, conflicts, tradeoffs, and decision relevance.
---

# Medical Admin Ops Comparison Builder

## Use when

- The user wants comparison across two or more medical administration operations sources or options.

## Input and preconditions

- At least two comparable items and evaluation criteria are available.
- Relevant material: appointment note, referral text, intake form, clinic instruction.

## Dependencies and resources

- patient-provided note
- appointment details
- clinic policy
- form fields
- task-specific constraints

## Procedure

1. Identify the items and criteria that make the comparison meaningful.
2. Extract comparable evidence for each criterion.
3. Surface material differences, trade-offs, and missing evidence.
4. Return the comparison table with bounded recommendation notes.

## Output

Comparison table with criteria, differences, tradeoffs, and recommendation caveats.
