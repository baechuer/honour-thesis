---
name: docs-ops-timeline-builder
description: Builds a timeline for document operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Docs Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from PDF, DOCX, Markdown file, policy draft, extracted text.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: PDF, DOCX, Markdown file, policy draft, extracted text.

## Dependencies and resources

- document file
- layout evidence
- source text
- format target
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
