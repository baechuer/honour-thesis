---
name: repo-ops-normalizer
description: Normalizes repository and engineering workflow material into a consistent naming, schema, format, or taxonomy.
---

# Repo Ops Normalizer

## Use when

- The user wants consistency and canonicalization for pull request, diff, CI logs, issue description.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: pull request, diff, CI logs, issue description.

## Dependencies and resources

- repository diff
- test output
- issue context
- review policy
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
