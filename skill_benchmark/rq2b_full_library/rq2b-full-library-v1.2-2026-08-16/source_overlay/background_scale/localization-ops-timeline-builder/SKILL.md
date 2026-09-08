---
name: localization-ops-timeline-builder
description: Builds a timeline for localization and translation operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Localization Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from source copy, translation memory, locale guide, glossary.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: source copy, translation memory, locale guide, glossary.

## Dependencies and resources

- source text
- target locale
- glossary
- style guide
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
