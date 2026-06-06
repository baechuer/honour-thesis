---
name: psc-hf-dataset-card-inspector
description: "Hugging Face machine-learning workflow involving datasets, models, embedding training, demos, Spaces, deployment, and evaluation. Inspect Hugging Face dataset cards, subsets, splits, columns, labels, examples, licensing, and schema caveats."
metadata:
  source_style: public_style_controlled
  cluster_id: psc_huggingface_workflow
---

# Hf Dataset Card Inspector

This is a public-style controlled skill used for retrieval evaluation. It is written as a practical capability note rather than a neat benchmark schema.

Cluster intent: Hugging Face tasks where dataset inspection, local model selection, training, and deployment share vocabulary.

## When to use

Use before modelling when the user needs to understand data shape and suitability.

## Requirements

- Dataset id/card or dataset description
- Need for splits, columns, row examples, or labels

## Instructions

- Inspect dataset metadata.
- Check subsets/splits/features.
- List examples and caveats.
- Identify readiness risks.

## Deliverables

- Dataset readiness summary
- Schema and split table
- Risks

## When not to use

Not for local model selection, fine-tuning, Gradio UI, or Spaces deployment.

## External dependencies to preserve

- Hugging Face Dataset Viewer or dataset card

## Example use

A good request names the artifact or situation, gives enough operational context to choose this capability, and asks for the deliverable above.
