---
name: k8s-ops-normalizer
description: Normalizes Kubernetes platform operations material into a consistent naming, schema, format, or taxonomy.
---

# K8s Ops Normalizer

## Use when

- The user wants consistency and canonicalization for manifest, pod log, deployment event, cluster configuration.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: manifest, pod log, deployment event, cluster configuration.

## Dependencies and resources

- cluster context
- manifest
- pod logs
- namespace
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
