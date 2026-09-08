---
name: email-ops-normalizer
description: Normalizes email and messaging operations material into a consistent naming, schema, format, or taxonomy.
---

# Email Ops Normalizer

## Use when

- The user wants consistency and canonicalization for draft email, message thread, recipient context, tone constraints.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: draft email, message thread, recipient context, tone constraints.

## Dependencies and resources

- message thread
- recipient relationship
- tone target
- requested action
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
