---
name: psc-hf-space-deployment-preparer
description: "Hugging Face machine-learning workflow involving datasets, models, embedding training, demos, Spaces, deployment, and evaluation. Prepare Hugging Face Space deployment with app files, requirements, hardware tier, queue behavior, secrets, and verification."
metadata:
  source_style: public_style_controlled
  cluster_id: psc_huggingface_workflow
---

# Hf Space Deployment Preparer

This is a public-style controlled skill used for retrieval evaluation. It is written as a practical capability note rather than a neat benchmark schema.

Cluster intent: Hugging Face tasks where dataset inspection, local model selection, training, and deployment share vocabulary.

## When to use

Use when a demo or model app needs to be published on Spaces.

## Requirements

- App or demo code
- Space hardware/runtime choice
- Dependencies and secrets

## Instructions

- Check app entrypoint and requirements.
- Select CPU/GPU/ZeroGPU assumptions.
- Plan secrets, queues, and sleep behavior.
- Verify public launch.

## Deliverables

- Space file checklist
- Runtime constraints
- Deployment verification

## When not to use

Not for model training, dataset inspection, or local-only model selection.

## External dependencies to preserve

- Hugging Face Spaces
- Gradio or Streamlit when relevant

## Example use

A good request names the artifact or situation, gives enough operational context to choose this capability, and asks for the deliverable above.
