---
name: knowledge-ops-normalizer
description: Normalizes knowledge management operations material into a consistent naming, schema, format, or taxonomy.
---

# Knowledge Ops Normalizer

## Use when

- The user wants consistency and canonicalization for notes, wiki pages, knowledge base articles, taxonomy.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: notes, wiki pages, knowledge base articles, taxonomy.

## Dependencies and resources

- note corpus
- taxonomy
- source links
- owner context
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
