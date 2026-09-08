---
name: recruiting-ops-normalizer
description: Normalizes recruiting pipeline operations material into a consistent naming, schema, format, or taxonomy.
---

# Recruiting Ops Normalizer

## Use when

- The user wants consistency and canonicalization for resume, interview notes, job criteria, candidate comparison table.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: resume, interview notes, job criteria, candidate comparison table.

## Dependencies and resources

- resume file
- job criteria
- interview notes
- candidate stage
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
