---
name: engineering-design-ops-field-extractor
description: Extracts structured fields from engineering design operations material while preserving source location, uncertainty, and required normalization.
---

# Engineering Design Ops Field Extractor

## Use when

- The user wants structured fields from design specification, calculation note, review comment, requirement list rather than a narrative summary.

## Input and preconditions

- The source includes identifiable fields or evidence spans that can be mapped into a table.
- Relevant material: design specification, calculation note, review comment, requirement list.

## Dependencies and resources

- specification
- requirement set
- calculation record
- review standard
- task-specific constraints

## Procedure

1. Locate the requested fields and their supporting evidence in the source material.
2. Capture values with their source locations and identify ambiguous values.
3. Normalise values only against the stated target schema.
4. Return the structured table with evidence and uncertainty notes.

## Output

Structured field table with source evidence, confidence, and normalization notes.
