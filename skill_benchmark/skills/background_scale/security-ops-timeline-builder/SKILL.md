---
name: security-ops-timeline-builder
description: Builds a timeline for application security operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Security Ops Timeline Builder

Background scale skill used to create realistic retrieval pressure in the benchmark.

## Dependency Profile

application security operations procedure over repository files, threat notes, scan findings, architecture description; requires preserving the procedure-specific input state and output artifact.

## External Dependencies To Preserve

- codebase
- architecture context
- security findings
- asset list
- task-specific constraints

## Resource And Structure Signals

- threats
- vulnerabilities
- controls
- assets
- trust boundaries
- timeline builder

## Use when

- The user wants sequence reconstruction or schedule structure from repository files, threat notes, scan findings, architecture description.
- The source contains dates, order cues, event descriptions, or dependency markers.
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

Timeline with dates, event descriptions, dependencies, and unresolved gaps.

## Writing rules

- Keep the result focused on this skill's procedural role.
- Do not silently switch to a more specific benchmark core skill.
- Preserve important caveats and source limits.
