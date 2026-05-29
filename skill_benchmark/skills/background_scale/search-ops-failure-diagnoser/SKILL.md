---
name: search-ops-failure-diagnoser
description: Diagnoses why a search and retrieval operations workflow, artifact, or previous answer failed to meet expectations.
---

# Search Ops Failure Diagnoser

Background scale skill used to create realistic retrieval pressure in the benchmark.

## Dependency Profile

search and retrieval operations procedure over search query log, retrieval results, index schema, relevance judgment; requires preserving the procedure-specific input state and output artifact.

## External Dependencies To Preserve

- query logs
- index schema
- relevance labels
- retrieval config
- task-specific constraints

## Resource And Structure Signals

- queries
- ranking
- index
- relevance
- recall
- failure diagnoser

## Use when

- The user wants failure analysis for search and retrieval operations rather than a fresh artifact.
- There is a failed output, error report, mismatch, or user complaint to analyze.
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

Failure classification, evidence, root-cause hypothesis, and corrective action.

## Writing rules

- Keep the result focused on this skill's procedural role.
- Do not silently switch to a more specific benchmark core skill.
- Preserve important caveats and source limits.
