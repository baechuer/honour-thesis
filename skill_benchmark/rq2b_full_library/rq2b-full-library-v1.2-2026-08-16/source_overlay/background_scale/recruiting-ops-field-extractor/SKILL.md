---
name: recruiting-ops-field-extractor
description: Extracts structured fields from recruiting pipeline operations material while preserving source location, uncertainty, and required normalization.
---

# Recruiting Ops Field Extractor

## Use when

- The user wants structured fields from resume, interview notes, job criteria, candidate comparison table rather than a narrative summary.

## Input and preconditions

- The source includes identifiable fields or evidence spans that can be mapped into a table.
- Relevant material: resume, interview notes, job criteria, candidate comparison table.

## Dependencies and resources

- resume file
- job criteria
- interview notes
- candidate stage
- task-specific constraints

## Procedure

1. Locate the requested fields and their supporting evidence in the source material.
2. Capture values with their source locations and identify ambiguous values.
3. Normalise values only against the stated target schema.
4. Return the structured table with evidence and uncertainty notes.

## Output

Structured field table with source evidence, confidence, and normalization notes.
