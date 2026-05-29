---
name: medical-admin-ops-normalizer
description: Normalizes medical administration operations material into a consistent naming, schema, format, or taxonomy.
---

# Medical Admin Ops Normalizer

Background scale skill used to create realistic retrieval pressure in the benchmark.

## Dependency Profile

medical administration operations procedure over appointment note, referral text, intake form, clinic instruction; requires preserving the procedure-specific input state and output artifact.

## External Dependencies To Preserve

- patient-provided note
- appointment details
- clinic policy
- form fields
- task-specific constraints

## Resource And Structure Signals

- appointments
- referrals
- intake
- forms
- follow-up
- normalizer

## Use when

- The user wants consistency and canonicalization for appointment note, referral text, intake form, clinic instruction.
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
