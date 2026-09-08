---
name: search-ops-normalizer
description: Normalizes search and retrieval operations material into a consistent naming, schema, format, or taxonomy.
---

# Search Ops Normalizer

## Use when

- The user wants consistency and canonicalization for search query log, retrieval results, index schema, relevance judgment.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: search query log, retrieval results, index schema, relevance judgment.

## Dependencies and resources

- query logs
- index schema
- relevance labels
- retrieval config
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
