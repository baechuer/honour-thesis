---
name: geospatial-ops-normalizer
description: Normalizes geospatial analysis operations material into a consistent naming, schema, format, or taxonomy.
---

# Geospatial Ops Normalizer

## Use when

- The user wants consistency and canonicalization for map layer, coordinate table, spatial query, GIS project note.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: map layer, coordinate table, spatial query, GIS project note.

## Dependencies and resources

- spatial data
- coordinate reference system
- map layers
- analysis boundary
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
