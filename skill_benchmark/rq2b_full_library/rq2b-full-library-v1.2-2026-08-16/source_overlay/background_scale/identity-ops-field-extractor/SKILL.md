---
name: identity-ops-field-extractor
description: Extracts structured fields from identity and access operations material while preserving source location, uncertainty, and required normalization.
---

# Identity Ops Field Extractor

## Use when

- The user wants structured fields from access request, role matrix, audit log, permission review rather than a narrative summary.

## Input and preconditions

- The source includes identifiable fields or evidence spans that can be mapped into a table.
- Relevant material: access request, role matrix, audit log, permission review.

## Dependencies and resources

- identity provider
- role matrix
- access logs
- approval policy
- task-specific constraints

## Procedure

1. Locate the requested fields and their supporting evidence in the source material.
2. Capture values with their source locations and identify ambiguous values.
3. Normalise values only against the stated target schema.
4. Return the structured table with evidence and uncertainty notes.

## Output

Structured field table with source evidence, confidence, and normalization notes.
