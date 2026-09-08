---
name: search-ops-timeline-builder
description: Builds a timeline for search and retrieval operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Search Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from search query log, retrieval results, index schema, relevance judgment.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: search query log, retrieval results, index schema, relevance judgment.

## Dependencies and resources

- query logs
- index schema
- relevance labels
- retrieval config
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
