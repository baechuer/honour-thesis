---
name: dashboard-ops-normalizer
description: Normalizes dashboard and metric reporting material into a consistent naming, schema, format, or taxonomy.
---

# Dashboard Ops Normalizer

## Use when

- The user wants consistency and canonicalization for dashboard screenshots, metric tables, alert notes, KPI definitions.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: dashboard screenshots, metric tables, alert notes, KPI definitions.

## Dependencies and resources

- dashboard export
- metric glossary
- time window
- owner notes
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
