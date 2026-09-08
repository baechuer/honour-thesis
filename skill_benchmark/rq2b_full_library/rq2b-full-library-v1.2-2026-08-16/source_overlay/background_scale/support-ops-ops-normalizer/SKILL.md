---
name: support-ops-ops-normalizer
description: Normalizes support process operations material into a consistent naming, schema, format, or taxonomy.
---

# Support Ops Ops Normalizer

## Use when

- The user wants consistency and canonicalization for support macro, escalation rule, queue report, knowledge base article.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: support macro, escalation rule, queue report, knowledge base article.

## Dependencies and resources

- support policy
- queue data
- macro library
- escalation owner
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
