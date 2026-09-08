---
name: localization-ops-field-extractor
description: Extracts structured fields from localization and translation operations material while preserving source location, uncertainty, and required normalization.
---

# Localization Ops Field Extractor

## Use when

- The user wants structured fields from source copy, translation memory, locale guide, glossary rather than a narrative summary.

## Input and preconditions

- The source includes identifiable fields or evidence spans that can be mapped into a table.
- Relevant material: source copy, translation memory, locale guide, glossary.

## Dependencies and resources

- source text
- target locale
- glossary
- style guide
- task-specific constraints

## Procedure

1. Locate the requested fields and their supporting evidence in the source material.
2. Capture values with their source locations and identify ambiguous values.
3. Normalise values only against the stated target schema.
4. Return the structured table with evidence and uncertainty notes.

## Output

Structured field table with source evidence, confidence, and normalization notes.
