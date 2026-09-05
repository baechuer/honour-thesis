---
name: psc-hf-space-deployment-preparer
description: "Hugging Face machine-learning workflow involving datasets, models, embedding training, demos, Spaces, deployment, and evaluation. Prepare Hugging Face Space deployment with app files, requirements, hardware tier, queue behavior, secrets, and verification."
category: public-style-controlled
tags:
  - public-style
  - controlled-confusability
  - psc-huggingface-workflow
metadata:
  source_style: public_style_controlled
  cluster_id: psc_huggingface_workflow
---

# Hf Space Deployment Preparer

## How this works

Prepare Hugging Face Space deployment with app files, requirements, hardware tier, queue behavior, secrets, and verification. This guide is written for a public-skill style library where the same artifact can be handled by several neighbouring workflows. Hugging Face tasks where dataset inspection, local model selection, training, and deployment share vocabulary.

The important distinction is not just the file type or tool name. Route here when the user is asking for space file checklist and the request depends on app or demo code, and space hardware/runtime choice. If the task shifts toward a different final artifact, keep the domain context but choose the neighbouring skill instead.

## Typical triggers

Use when a demo or model app needs to be published on Spaces. In practice the request may mention only part of the context, so check for the combination of source material, requested judgement, and the kind of handoff the user expects.

| Useful clue | Why it matters |
|---|---|
| App or demo code | Space file checklist |
| Space hardware/runtime choice | Runtime constraints |
| Dependencies and secrets | Deployment verification |

When the request is underspecified, ask for the smallest missing item. For example, if the user gives the artifact but not the acceptance criterion, state what you will assume before doing irreversible work.

## Steps

A normal run is usually:

1. Check app entrypoint and requirements.
2. Select CPU/GPU/ZeroGPU assumptions.
3. Plan secrets, queues, and sleep behavior.
4. Verify public launch.

Do not treat the list above as a rigid template. Public skills often arrive with partial notes, linked files, or copied examples. Preserve the user's ordering when it matters, but keep the final answer focused on the decision the skill is responsible for.

```yaml
handoff:
  needs: ["App or demo code", "Space hardware/runtime choice"]
  returns: ["Space file checklist", "Runtime constraints"]
  tools: ["Hugging Face Spaces", "Gradio or Streamlit when relevant"]
  uncertainty: keep page, file, row, log, or source anchors when available
```

## What to return

The handoff is usually a compact artifact rather than a long essay. Include space file checklist, runtime constraints, and deployment verification when those pieces are supported by the source material. If a requested field cannot be found, mark it as missing instead of inventing it.

Typical return blocks:

- Space file checklist
- Runtime constraints
- Deployment verification

## Neighbouring skills

Not for model training, dataset inspection, or local-only model selection. Nearby skills in this cluster include `psc-hf-dataset-card-inspector`, `psc-local-model-fit-selector`, `psc-sentence-embedding-trainer`. They may share nouns with this skill, so route by the requested artifact and the work sequence, not by the domain word alone.

A common routing mistake is to select by a shared noun in the prompt and miss the user's requested output. Prefer the skill whose procedure would actually produce the requested handoff.

## Operational notes

This workflow can be carried out with hugging face spaces, and gradio or streamlit when relevant. Equivalent tools are fine, but they must preserve the same inspection or verification standard. Keep anchors such as filenames, pages, rows, source snippets, log lines, screenshots, or model/dataset identifiers when they are available.

Useful source clues, in rough order: App or demo code. Space hardware/runtime choice. Dependencies and secrets.

## Requests

- Prepare the classifier demo for Hugging Face Spaces with requirements, app entrypoint, secrets, hardware tier, queue behavior, and verification after launch.
- Package this model demo for a hosted Space-style deployment. Focus on runtime files, dependency pins, GPU/queue assumptions, and launch checks rather than training.

Less ideal but still valid request: "Can you look at this and tell me what should happen next?" In that case, first decide whether the user wants space file checklist or a neighbouring artifact, then ask one clarifying question if needed.

## Review notes

- The response clearly produces space file checklist.
- The answer explains uncertainty instead of silently guessing.
- The chosen process matches the user's artifact and requested outcome.
- Secondary outputs are included only when they support the requested result.

Before finishing, compare the answer against the nearby-skill boundary above. If the output would be more naturally produced by another skill, say so and switch rather than stretching this workflow.
