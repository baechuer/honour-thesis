---
name: psc-sentence-embedding-trainer
description: "Hugging Face machine-learning workflow involving datasets, models, embedding training, demos, Spaces, deployment, and evaluation. Plan sentence embedding fine-tuning with positive pairs, hard negatives, loss choice, splits, and retrieval metrics."
metadata:
  source_style: public_style_controlled
  cluster_id: psc_huggingface_workflow
---

# Sentence Embedding Trainer

This is a public-style controlled skill used for retrieval evaluation. It is written as a practical capability note rather than a neat benchmark schema.

Cluster intent: Hugging Face tasks where dataset inspection, local model selection, training, and deployment share vocabulary.

## When to use

Use when the user has labelled query-document or skill-query pairs and wants a better embedding model.

## Requirements

- Training pairs or triplets
- Retrieval objective
- Evaluation labels or split

## Instructions

- Define positives, negatives, and leakage controls.
- Choose a base model and contrastive/ranking loss.
- Specify top-k and MRR evaluation.

## Deliverables

- Training plan
- Loss and data format
- Evaluation setup
- Risk notes

## When not to use

Not for choosing an off-the-shelf local LLM or building a demo UI.

## External dependencies to preserve

- sentence-transformers or equivalent embedding training stack

## Example use

A good request names the artifact or situation, gives enough operational context to choose this capability, and asks for the deliverable above.
