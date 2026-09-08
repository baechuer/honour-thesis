---
name: partnerships-ops-field-extractor
description: Extracts structured fields from partnership operations material while preserving source location, uncertainty, and required normalization.
---

# Partnerships Ops Field Extractor

## Use when

- The user wants structured fields from partner proposal, MOU draft, co-marketing plan, partner report rather than a narrative summary.

## Input and preconditions

- The source includes identifiable fields or evidence spans that can be mapped into a table.
- Relevant material: partner proposal, MOU draft, co-marketing plan, partner report.

## Dependencies and resources

- partner profile
- proposal terms
- shared goals
- approval process
- task-specific constraints

## Procedure

1. Locate the requested fields and their supporting evidence in the source material.
2. Capture values with their source locations and identify ambiguous values.
3. Normalise values only against the stated target schema.
4. Return the structured table with evidence and uncertainty notes.

## Output

Structured field table with source evidence, confidence, and normalization notes.
