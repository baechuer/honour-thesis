---
name: energy-ops-field-extractor
description: Extracts structured fields from energy operations material while preserving source location, uncertainty, and required normalization.
---

# Energy Ops Field Extractor

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
- field extractor

## Use when

- The user wants structured fields from usage report, meter reading, sustainability plan, tariff note rather than a narrative summary.
- The source includes identifiable fields or evidence spans that can be mapped into a table.
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

Structured field table with source evidence, confidence, and normalization notes.

## Writing rules

- Keep the result focused on this skill's procedural role.
- Do not silently switch to a more specific benchmark core skill.
- Preserve important caveats and source limits.
