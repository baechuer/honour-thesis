---
name: sentence-transformer-finetuner
description: "Plans sentence-transformer fine-tuning for retrieval or similarity with training pairs, losses, evaluation splits, and embedding checks."
---

# Sentence Transformer Finetuner

Improves an embedding model for a specific retrieval task.

## Use when

- The user has positive/negative pairs, triplets, or retrieval labels.
- The output should be a fine-tuning/evaluation plan for embeddings.

## Not for

- Selecting an off-the-shelf local LLM.
- Building a Gradio interface.
- Inspecting only dataset columns.

## Preconditions

- Training examples or labels are available.
- The target metric is retrieval or semantic similarity.

## Workflow

1. Identify labels and retrieval objective.
2. Choose base model, loss, negatives, and split strategy.
3. Define evaluation metrics.
4. Return training config and risks.

## Writing rules

- Do not promise improved retrieval without eval design.
- Keep leakage and hard negatives explicit.

## Default shape

- Training data
- Model/loss
- Evaluation
- Risks
