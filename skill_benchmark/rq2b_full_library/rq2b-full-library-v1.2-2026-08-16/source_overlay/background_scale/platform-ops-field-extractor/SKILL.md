---
name: platform-ops-field-extractor
description: Extracts structured fields from platform engineering operations material while preserving source location, uncertainty, and required normalization.
---

# Platform Ops Field Extractor

## Use when

- The user wants structured fields from developer platform request, service catalog, template repo, platform metric rather than a narrative summary.

## Input and preconditions

- The source includes identifiable fields or evidence spans that can be mapped into a table.
- Relevant material: developer platform request, service catalog, template repo, platform metric.

## Dependencies and resources

- platform service
- template repository
- developer workflow
- service owner
- task-specific constraints

## Procedure

1. Locate the requested fields and their supporting evidence in the source material.
2. Capture values with their source locations and identify ambiguous values.
3. Normalise values only against the stated target schema.
4. Return the structured table with evidence and uncertainty notes.

## Output

Structured field table with source evidence, confidence, and normalization notes.
