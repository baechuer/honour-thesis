---
name: energy-ops-normalizer
description: Normalizes energy operations material into a consistent naming, schema, format, or taxonomy.
---

# Energy Ops Normalizer

Background scale skill used to create realistic retrieval pressure in the benchmark.

## Dependency Profile

energy operations procedure over usage report, meter reading, sustainability plan, tariff note; requires preserving the procedure-specific input state and output artifact.

## External Dependencies To Preserve

- meter data
- tariff schedule
- facility profile
- sustainability target
- task-specific constraints

## Resource And Structure Signals

- energy
- meter
- tariff
- usage
- sustainability
- normalizer

## Use when

- The user wants consistency and canonicalization for usage report, meter reading, sustainability plan, tariff note.
- There is a target schema, naming convention, taxonomy, or example format.
- The task needs this specific procedure rather than a neighboring confusable skill.
- The output should match the expected artifact below.

## Not for

- Replacing a gold-label core benchmark skill when that core skill is procedurally more specific.
- Broad internal routing across unrelated domains.
- Acting on missing context without asking for or identifying the needed input.

## Workflow

1. Identify the user's intended input and desired artifact.
2. Confirm this skill's procedure is the best fit rather than a neighboring skill.
3. Extract the relevant constraints, evidence, or requirements.
4. Produce the expected output in a compact and reusable form.
5. State uncertainty or required follow-up when the input is incomplete.

## Expected output

Normalized artifact with mapping from original values to canonical values.

## Writing rules

- Keep the result focused on this skill's procedural role.
- Do not silently switch to a more specific benchmark core skill.
- Preserve important caveats and source limits.
