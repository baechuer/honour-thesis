---
name: mobile-ops-normalizer
description: Normalizes mobile application operations material into a consistent naming, schema, format, or taxonomy.
---

# Mobile Ops Normalizer

## Use when

- The user wants consistency and canonicalization for app crash log, release note, store review, mobile test report.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: app crash log, release note, store review, mobile test report.

## Dependencies and resources

- mobile app build
- device context
- crash log
- release channel
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
