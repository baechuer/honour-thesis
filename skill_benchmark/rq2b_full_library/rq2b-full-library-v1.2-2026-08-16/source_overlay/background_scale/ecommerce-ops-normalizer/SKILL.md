---
name: ecommerce-ops-normalizer
description: Normalizes ecommerce operations material into a consistent naming, schema, format, or taxonomy.
---

# Ecommerce Ops Normalizer

## Use when

- The user wants consistency and canonicalization for order export, product listing, refund note, marketplace report.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: order export, product listing, refund note, marketplace report.

## Dependencies and resources

- order data
- product catalog
- marketplace rules
- customer message
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
