---
name: qa-ops-normalizer
description: Normalizes quality assurance operations material into a consistent naming, schema, format, or taxonomy.
---

# Qa Ops Normalizer

## Use when

- The user wants consistency and canonicalization for test plan, defect report, acceptance criteria, release evidence.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: test plan, defect report, acceptance criteria, release evidence.

## Dependencies and resources

- test plan
- defect log
- acceptance criteria
- release scope
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
