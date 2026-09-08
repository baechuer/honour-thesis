---
name: compliance-ops-normalizer
description: Normalizes compliance operations material into a consistent naming, schema, format, or taxonomy.
---

# Compliance Ops Normalizer

## Use when

- The user wants consistency and canonicalization for control checklist, audit finding, policy exception, evidence packet.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: control checklist, audit finding, policy exception, evidence packet.

## Dependencies and resources

- control framework
- evidence files
- audit scope
- owner map
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
