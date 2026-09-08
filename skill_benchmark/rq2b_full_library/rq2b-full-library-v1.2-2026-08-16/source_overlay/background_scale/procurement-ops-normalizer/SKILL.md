---
name: procurement-ops-normalizer
description: Normalizes procurement operations material into a consistent naming, schema, format, or taxonomy.
---

# Procurement Ops Normalizer

## Use when

- The user wants consistency and canonicalization for purchase request, vendor quote, RFP response, approval note.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: purchase request, vendor quote, RFP response, approval note.

## Dependencies and resources

- purchase request
- vendor quote
- budget code
- approval policy
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
