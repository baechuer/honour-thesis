---
name: geospatial-ops-quality-auditor
description: Audits geospatial analysis operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Geospatial Ops Quality Auditor

## Use when

- The user wants quality assurance over map layer, coordinate table, spatial query, GIS project note before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: map layer, coordinate table, spatial query, GIS project note.

## Dependencies and resources

- spatial data
- coordinate reference system
- map layers
- analysis boundary
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
