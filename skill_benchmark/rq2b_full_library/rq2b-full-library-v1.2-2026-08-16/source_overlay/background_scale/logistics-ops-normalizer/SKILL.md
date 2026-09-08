---
name: logistics-ops-normalizer
description: Normalizes logistics and shipment operations material into a consistent naming, schema, format, or taxonomy.
---

# Logistics Ops Normalizer

## Use when

- The user wants consistency and canonicalization for shipment manifest, tracking update, carrier note, customs form.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: shipment manifest, tracking update, carrier note, customs form.

## Dependencies and resources

- shipment manifest
- carrier data
- delivery window
- customs details
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
