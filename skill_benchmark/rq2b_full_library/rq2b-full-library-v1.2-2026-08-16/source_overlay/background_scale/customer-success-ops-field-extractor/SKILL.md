---
name: customer-success-ops-field-extractor
description: Extracts structured fields from customer success operations material while preserving source location, uncertainty, and required normalization.
---

# Customer Success Ops Field Extractor

## Use when

- The user wants structured fields from account health note, renewal plan, usage report, success plan rather than a narrative summary.

## Input and preconditions

- The source includes identifiable fields or evidence spans that can be mapped into a table.
- Relevant material: account health note, renewal plan, usage report, success plan.

## Dependencies and resources

- account profile
- usage data
- renewal date
- success criteria
- task-specific constraints

## Procedure

1. Locate the requested fields and their supporting evidence in the source material.
2. Capture values with their source locations and identify ambiguous values.
3. Normalise values only against the stated target schema.
4. Return the structured table with evidence and uncertainty notes.

## Output

Structured field table with source evidence, confidence, and normalization notes.
