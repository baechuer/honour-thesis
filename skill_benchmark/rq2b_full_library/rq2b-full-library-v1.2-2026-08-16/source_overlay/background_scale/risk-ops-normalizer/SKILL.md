---
name: risk-ops-normalizer
description: Normalizes risk management operations material into a consistent naming, schema, format, or taxonomy.
---

# Risk Ops Normalizer

## Use when

- The user wants consistency and canonicalization for risk register, control report, incident note, mitigation plan.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: risk register, control report, incident note, mitigation plan.

## Dependencies and resources

- risk taxonomy
- control evidence
- owner map
- impact scale
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
