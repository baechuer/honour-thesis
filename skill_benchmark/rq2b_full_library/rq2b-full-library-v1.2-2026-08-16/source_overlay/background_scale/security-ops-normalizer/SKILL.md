---
name: security-ops-normalizer
description: Normalizes application security operations material into a consistent naming, schema, format, or taxonomy.
---

# Security Ops Normalizer

## Use when

- The user wants consistency and canonicalization for repository files, threat notes, scan findings, architecture description.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: repository files, threat notes, scan findings, architecture description.

## Dependencies and resources

- codebase
- architecture context
- security findings
- asset list
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
