---
name: psc-local-model-fit-selector
description: "Hugging Face machine-learning workflow involving datasets, models, embedding training, demos, Spaces, deployment, and evaluation. Choose local model candidates by task, memory, quantization, runtime, latency, and installation constraints."
metadata:
  source_style: public_style_controlled
  cluster_id: psc_huggingface_workflow
---

# Local Model Fit Selector

This is a public-style controlled skill used for retrieval evaluation. It is written as a practical capability note rather than a neat benchmark schema.

Cluster intent: Hugging Face tasks where dataset inspection, local model selection, training, and deployment share vocabulary.

## When to use

Use when hardware limits are central to model choice.

## Requirements

- Task type
- Memory/runtime budget
- Quality and latency tradeoff

## Instructions

- Translate task needs into model family constraints.
- Compare model sizes and quantization options.
- Recommend candidates with fallback checks.

## Deliverables

- Model shortlist
- Quantization choice
- Hardware fit reasoning
- Setup checks

## When not to use

Not for dataset schema inspection, fine-tuning plans, or hosted demo deployment.

## External dependencies to preserve

- Local runtime such as GGUF, llama.cpp, transformers, or MLX

## Example use

A good request names the artifact or situation, gives enough operational context to choose this capability, and asks for the deliverable above.
