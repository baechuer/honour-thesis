---
name: hf-dataset-viewer-inspector
description: "Inspects Hugging Face dataset metadata, splits, subsets, row examples, and schema risks."
---

# Hf Dataset Viewer Inspector

Uses dataset viewer information to understand a dataset before modelling.

## Use when

- The user provides a dataset id or dataset task.
- They need splits, columns, examples, or schema constraints.

## Not for

- Choosing a local model for hardware.
- Training sentence transformers.
- Building a Gradio demo.

## Preconditions

- A dataset id, dataset card, or expected dataset schema exists.
- The goal is dataset inspection rather than model deployment.

## Workflow

1. Fetch or inspect dataset metadata.
2. Check subsets, splits, columns, and row examples.
3. Identify licensing or schema caveats.
4. Return a dataset readiness summary.

## Writing rules

- Do not recommend models before checking dataset shape.
- Separate metadata facts from assumptions.

## Default shape

- Dataset overview
- Splits/subsets
- Columns/examples
- Risks
