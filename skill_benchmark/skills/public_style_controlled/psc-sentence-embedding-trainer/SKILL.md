---
name: psc-sentence-embedding-trainer
description: "Hugging Face machine-learning workflow involving datasets, models, embedding training, demos, Spaces, deployment, and evaluation. Plan sentence embedding fine-tuning with positive pairs, hard negatives, loss choice, splits, and retrieval metrics."
category: public-style-controlled
tags:
  - public-style
  - controlled-confusability
  - psc-huggingface-workflow
metadata:
  source_style: public_style_controlled
  cluster_id: psc_huggingface_workflow
---

# Sentence Embedding Trainer

## How this works

Plan sentence embedding fine-tuning with positive pairs, hard negatives, loss choice, splits, and retrieval metrics. This guide is written for a public-skill style library where the same artifact can be handled by several neighbouring workflows. Hugging Face tasks where dataset inspection, local model selection, training, and deployment share vocabulary.

The important distinction is not just the file type or tool name. Route here when the user is asking for training plan and the request depends on training pairs or triplets, and retrieval objective. If the task shifts toward a different final artifact, keep the domain context but choose the neighbouring skill instead.

## Typical triggers

Use when the user has labelled query-document or skill-query pairs and wants a better embedding model. In practice the request may mention only part of the context, so check for the combination of source material, requested judgement, and the kind of handoff the user expects.

| Useful clue | Why it matters |
|---|---|
| Training pairs or triplets | Training plan |
| Retrieval objective | Loss and data format |
| Evaluation labels or split | Evaluation setup |

When the request is underspecified, ask for the smallest missing item. For example, if the user gives the artifact but not the acceptance criterion, state what you will assume before doing irreversible work.

## Steps

A normal run is usually:

1. Define positives, negatives, and leakage controls.
2. Choose a base model and contrastive/ranking loss.
3. Specify top-k and MRR evaluation.

Do not treat the list above as a rigid template. Public skills often arrive with partial notes, linked files, or copied examples. Preserve the user's ordering when it matters, but keep the final answer focused on the decision the skill is responsible for.

```yaml
handoff:
  needs: ["Training pairs or triplets", "Retrieval objective"]
  returns: ["Training plan", "Loss and data format"]
  tools: ["sentence-transformers or equivalent embedding training stack"]
  uncertainty: keep page, file, row, log, or source anchors when available
```

## What to return

The handoff is usually a compact artifact rather than a long essay. Include training plan, loss and data format, evaluation setup, and risk notes when those pieces are supported by the source material. If a requested field cannot be found, mark it as missing instead of inventing it.

Typical return blocks:

- Training plan
- Loss and data format
- Evaluation setup
- Risk notes

## Neighbouring skills

Not for choosing an off-the-shelf local LLM or building a demo UI. Nearby skills in this cluster include `psc-hf-dataset-card-inspector`, `psc-local-model-fit-selector`, `psc-hf-space-deployment-preparer`. They may share nouns with this skill, so route by the requested artifact and the work sequence, not by the domain word alone.

A common routing mistake is to select by a shared noun in the prompt and miss the user's requested output. Prefer the skill whose procedure would actually produce the requested handoff.

## Operational notes

This workflow can be carried out with sentence-transformers or equivalent embedding training stack. Equivalent tools are fine, but they must preserve the same inspection or verification standard. Keep anchors such as filenames, pages, rows, source snippets, log lines, screenshots, or model/dataset identifiers when they are available.

Useful source clues, in rough order: Training pairs or triplets. Retrieval objective. Evaluation labels or split.

## Requests

- We have labelled skill queries, gold skills, and hard negatives. Design the embedding fine-tuning setup and retrieval evaluation for a skill router.
- Plan a SentenceTransformer fine-tuning run with positives, hard negatives, loss function, splits, top-k recall, and MRR. Do not choose a local chatbot model.

Less ideal but still valid request: "Can you look at this and tell me what should happen next?" In that case, first decide whether the user wants training plan or a neighbouring artifact, then ask one clarifying question if needed.

## Review notes

- The response clearly produces training plan.
- The answer explains uncertainty instead of silently guessing.
- The chosen process matches the user's artifact and requested outcome.
- Secondary outputs are included only when they support the requested result.

Before finishing, compare the answer against the nearby-skill boundary above. If the output would be more naturally produced by another skill, say so and switch rather than stretching this workflow.
