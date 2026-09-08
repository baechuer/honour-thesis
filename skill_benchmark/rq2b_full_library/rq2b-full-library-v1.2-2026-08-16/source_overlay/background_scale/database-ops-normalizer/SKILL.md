---
name: database-ops-normalizer
description: Normalizes database operations material into a consistent naming, schema, format, or taxonomy.
---

# Database Ops Normalizer

## Use when

- The user wants consistency and canonicalization for schema, migration file, query plan, data quality note.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: schema, migration file, query plan, data quality note.

## Dependencies and resources

- database schema
- migration file
- query plan
- data sample
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
