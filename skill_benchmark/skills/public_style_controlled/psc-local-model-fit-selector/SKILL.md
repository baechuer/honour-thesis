---
name: psc-local-model-fit-selector
description: "Hugging Face machine-learning workflow involving datasets, models, embedding training, demos, Spaces, deployment, and evaluation. Choose local model candidates by task, memory, quantization, runtime, latency, and installation constraints."
category: public-style-controlled
tags:
  - public-style
  - controlled-confusability
  - psc-huggingface-workflow
metadata:
  source_style: public_style_controlled
  cluster_id: psc_huggingface_workflow
---

# Local Model Fit Selector

## How this works

Choose local model candidates by task, memory, quantization, runtime, latency, and installation constraints. This guide is written for a public-skill style library where the same artifact can be handled by several neighbouring workflows. Hugging Face tasks where dataset inspection, local model selection, training, and deployment share vocabulary.

The important distinction is not just the file type or tool name. Route here when the user is asking for model shortlist and the request depends on task type, and memory/runtime budget. If the task shifts toward a different final artifact, keep the domain context but choose the neighbouring skill instead.

## Typical triggers

Use when hardware limits are central to model choice. In practice the request may mention only part of the context, so check for the combination of source material, requested judgement, and the kind of handoff the user expects.

| Useful clue | Why it matters |
|---|---|
| Task type | Model shortlist |
| Memory/runtime budget | Quantization choice |
| Quality and latency tradeoff | Hardware fit reasoning |

When the request is underspecified, ask for the smallest missing item. For example, if the user gives the artifact but not the acceptance criterion, state what you will assume before doing irreversible work.

## Steps

A normal run is usually:

1. Translate task needs into model family constraints.
2. Compare model sizes and quantization options.
3. Recommend candidates with fallback checks.

Do not treat the list above as a rigid template. Public skills often arrive with partial notes, linked files, or copied examples. Preserve the user's ordering when it matters, but keep the final answer focused on the decision the skill is responsible for.

```yaml
handoff:
  needs: ["Task type", "Memory/runtime budget"]
  returns: ["Model shortlist", "Quantization choice"]
  tools: ["Local runtime such as GGUF, llama.cpp, transformers, or MLX"]
  uncertainty: keep page, file, row, log, or source anchors when available
```

## What to return

The handoff is usually a compact artifact rather than a long essay. Include model shortlist, quantization choice, hardware fit reasoning, and setup checks when those pieces are supported by the source material. If a requested field cannot be found, mark it as missing instead of inventing it.

Typical return blocks:

- Model shortlist
- Quantization choice
- Hardware fit reasoning
- Setup checks

## Neighbouring skills

Not for dataset schema inspection, fine-tuning plans, or hosted demo deployment. Nearby skills in this cluster include `psc-hf-dataset-card-inspector`, `psc-sentence-embedding-trainer`, `psc-hf-space-deployment-preparer`. They may share nouns with this skill, so route by the requested artifact and the work sequence, not by the domain word alone.

A common routing mistake is to select by a shared noun in the prompt and miss the user's requested output. Prefer the skill whose procedure would actually produce the requested handoff.

## Operational notes

This workflow can be carried out with local runtime such as gguf, llama.cpp, transformers, or mlx. Equivalent tools are fine, but they must preserve the same inspection or verification standard. Keep anchors such as filenames, pages, rows, source snippets, log lines, screenshots, or model/dataset identifiers when they are available.

Useful source clues, in rough order: Task type. Memory/runtime budget. Quality and latency tradeoff.

## Requests

- I need a support-ticket classifier that can run locally on an 8 GB laptop. Shortlist realistic model sizes, quantization choices, and latency tradeoffs.
- Choose Hugging Face or GGUF local model candidates for an 8 GB Mac. I need memory-fit and quantization reasoning, not a dataset card audit.

Less ideal but still valid request: "Can you look at this and tell me what should happen next?" In that case, first decide whether the user wants model shortlist or a neighbouring artifact, then ask one clarifying question if needed.

## Review notes

- The response clearly produces model shortlist.
- The answer explains uncertainty instead of silently guessing.
- The chosen process matches the user's artifact and requested outcome.
- Secondary outputs are included only when they support the requested result.

Before finishing, compare the answer against the nearby-skill boundary above. If the output would be more naturally produced by another skill, say so and switch rather than stretching this workflow.
