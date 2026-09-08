---
name: support-ops-field-extractor
description: Extracts structured fields from customer support operations material while preserving source location, uncertainty, and required normalization.
---

# Support Ops Field Extractor

## Use when

- The user wants structured fields from support tickets, chat transcripts, issue labels, customer history rather than a narrative summary.

## Input and preconditions

- The source includes identifiable fields or evidence spans that can be mapped into a table.
- Relevant material: support tickets, chat transcripts, issue labels, customer history.

## Dependencies and resources

- ticket queue
- customer context
- product area
- severity policy
- task-specific constraints

## Procedure

1. Locate the requested fields and their supporting evidence in the source material.
2. Capture values with their source locations and identify ambiguous values.
3. Normalise values only against the stated target schema.
4. Return the structured table with evidence and uncertainty notes.

## Output

Structured field table with source evidence, confidence, and normalization notes.
