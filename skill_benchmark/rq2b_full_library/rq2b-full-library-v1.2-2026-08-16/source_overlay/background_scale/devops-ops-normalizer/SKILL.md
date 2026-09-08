---
name: devops-ops-normalizer
description: Normalizes DevOps pipeline operations material into a consistent naming, schema, format, or taxonomy.
---

# Devops Ops Normalizer

## Use when

- The user wants consistency and canonicalization for pipeline log, build script, deploy config, release checklist.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: pipeline log, build script, deploy config, release checklist.

## Dependencies and resources

- CI logs
- build config
- environment variables
- release target
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
