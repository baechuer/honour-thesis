---
name: skill-benchmark-evaluator
description: "Evaluates skill retrieval benchmarks using gold labels, acceptable alternatives, top-k metrics, MRR, false positives, and failure modes."
---

# Skill Benchmark Evaluator

Assesses benchmark results rather than authoring or installing skills.

## Use when

- The user has retrieval outputs or benchmark prompts.
- The output should be metrics and failure analysis.

## Not for

- Creating a skill file.
- Installing public skills.
- Flattening hierarchy.

## Preconditions

- Prompt/gold labels and retrieval rankings are available.
- Metrics and acceptable-alternative policy are known.

## Workflow

1. Load rankings and gold labels.
2. Compute top-k, MRR, and false positives.
3. Inspect failure modes.
4. Return evaluation summary.

## Writing rules

- Do not tune benchmark after seeing results without logging it.
- Separate strict and acceptable accuracy.

## Default shape

- Metrics
- Failure modes
- Risk/caveats
- Next validation
