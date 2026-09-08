---
name: robotics-ops-field-extractor
description: Extracts structured fields from robotics operations material while preserving source location, uncertainty, and required normalization.
---

# Robotics Ops Field Extractor

## Use when

- The user wants structured fields from robot log, mission plan, sensor trace, calibration note rather than a narrative summary.

## Input and preconditions

- The source includes identifiable fields or evidence spans that can be mapped into a table.
- Relevant material: robot log, mission plan, sensor trace, calibration note.

## Dependencies and resources

- robot platform
- sensor data
- mission objective
- calibration file
- task-specific constraints

## Procedure

1. Locate the requested fields and their supporting evidence in the source material.
2. Capture values with their source locations and identify ambiguous values.
3. Normalise values only against the stated target schema.
4. Return the structured table with evidence and uncertainty notes.

## Output

Structured field table with source evidence, confidence, and normalization notes.
