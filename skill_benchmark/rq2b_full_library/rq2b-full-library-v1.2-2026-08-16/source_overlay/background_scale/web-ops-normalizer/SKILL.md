---
name: web-ops-normalizer
description: Normalizes web automation and QA material into a consistent naming, schema, format, or taxonomy.
---

# Web Ops Normalizer

## Use when

- The user wants consistency and canonicalization for web page, browser state, test flow, screenshot evidence.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: web page, browser state, test flow, screenshot evidence.

## Dependencies and resources

- web target
- browser runtime
- test data
- screenshot evidence
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
