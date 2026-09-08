---
name: iot-ops-normalizer
description: Normalizes IoT operations material into a consistent naming, schema, format, or taxonomy.
---

# Iot Ops Normalizer

## Use when

- The user wants consistency and canonicalization for device telemetry, firmware note, sensor log, provisioning record.

## Input and preconditions

- There is a target schema, naming convention, taxonomy, or example format.
- Relevant material: device telemetry, firmware note, sensor log, provisioning record.

## Dependencies and resources

- device registry
- telemetry data
- firmware version
- network context
- task-specific constraints

## Procedure

1. Identify the target naming, schema, format, or taxonomy.
2. Map source values to canonical values and retain unmapped exceptions.
3. Check the transformed artifact for consistency.
4. Return the normalised artifact and mapping notes.

## Output

Normalized artifact with mapping from original values to canonical values.
