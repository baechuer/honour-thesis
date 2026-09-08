---
name: social-ops-field-extractor
description: Extracts structured fields from social media operations material while preserving source location, uncertainty, and required normalization.
---

# Social Ops Field Extractor

## Use when

- The user wants structured fields from post draft, publishing calendar, engagement report, campaign note rather than a narrative summary.

## Input and preconditions

- The source includes identifiable fields or evidence spans that can be mapped into a table.
- Relevant material: post draft, publishing calendar, engagement report, campaign note.

## Dependencies and resources

- platform rules
- posting schedule
- brand guidelines
- engagement data
- task-specific constraints

## Procedure

1. Locate the requested fields and their supporting evidence in the source material.
2. Capture values with their source locations and identify ambiguous values.
3. Normalise values only against the stated target schema.
4. Return the structured table with evidence and uncertainty notes.

## Output

Structured field table with source evidence, confidence, and normalization notes.
