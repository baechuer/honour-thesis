---
name: support-ops-normalizer
description: Normalizes customer support operations material into a consistent naming, schema, format, or taxonomy.
---

# Support Ops Normalizer

## Use when

- The user wants consistency and canonicalization for support tickets, chat transcripts, issue labels, customer history.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: support tickets, chat transcripts, issue labels, customer history.

## Dependencies and resources

- ticket queue
- customer context
- product area
- severity policy
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
