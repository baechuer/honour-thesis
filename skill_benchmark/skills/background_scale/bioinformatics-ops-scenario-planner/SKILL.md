---
name: bioinformatics-ops-scenario-planner
description: Plans alternative scenarios for bioinformatics operations decisions under changing assumptions, constraints, or risks.
---

# Bioinformatics Ops Scenario Planner

Background scale skill used to create realistic retrieval pressure in the benchmark.

## Dependency Profile

bioinformatics operations procedure over sequence file, variant table, pipeline log, sample metadata; requires preserving the procedure-specific input state and output artifact.

## External Dependencies To Preserve

- sequence data
- sample metadata
- pipeline config
- reference genome
- task-specific constraints

## Resource And Structure Signals

- sequence
- variants
- samples
- pipeline
- genome
- scenario planner

## Use when

- The user wants scenario planning for bioinformatics operations rather than a single recommendation.
- Key assumptions, decision options, or uncertainty drivers are available.
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

Scenario table with assumptions, expected outcomes, risks, and decision triggers.

## Writing rules

- Keep the result focused on this skill's procedural role.
- Do not silently switch to a more specific benchmark core skill.
- Preserve important caveats and source limits.
