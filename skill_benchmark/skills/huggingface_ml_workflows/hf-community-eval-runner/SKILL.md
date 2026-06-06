---
name: hf-community-eval-runner
description: "Runs or plans Hugging Face model evaluations using benchmark tasks, metrics, hardware assumptions, and reproducible result reporting."
---

# Hf Community Eval Runner

Evaluates model quality instead of building a demo or selecting local hardware.

## Use when

- The user wants to compare models with a benchmark or eval suite.
- Metrics, reproducibility, and result artifacts matter.

## Not for

- Inspecting dataset rows.
- Deploying to ZeroGPU.
- Building a UI demo.

## Preconditions

- Candidate models and evaluation task are known.
- Metrics and dataset split are specified or can be chosen.

## Workflow

1. Identify models, tasks, metrics, and hardware.
2. Prepare evaluation commands or scripts.
3. Run or describe reproducible evaluation.
4. Report scores and caveats.

## Writing rules

- Do not infer model quality from popularity alone.
- Keep benchmark limitations explicit.

## Default shape

- Models
- Eval setup
- Metrics/results
- Caveats
