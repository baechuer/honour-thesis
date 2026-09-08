---
name: property-ops-normalizer
description: Normalizes property management operations material into a consistent naming, schema, format, or taxonomy.
---

# Property Ops Normalizer

## Use when

- The user wants consistency and canonicalization for lease, maintenance ticket, inspection report, tenant message.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: lease, maintenance ticket, inspection report, tenant message.

## Dependencies and resources

- property record
- lease terms
- maintenance history
- tenant context
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
