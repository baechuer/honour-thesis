---
name: psc-hf-dataset-card-inspector
description: "Hugging Face machine-learning workflow involving datasets, models, embedding training, demos, Spaces, deployment, and evaluation. Inspect Hugging Face dataset cards, subsets, splits, columns, labels, examples, licensing, and schema caveats."
category: public-style-controlled
tags:
  - public-style
  - controlled-confusability
  - psc-huggingface-workflow
metadata:
  source_style: public_style_controlled
  cluster_id: psc_huggingface_workflow
---

# Hf Dataset Card Inspector

## Capability

Inspect Hugging Face dataset cards, subsets, splits, columns, labels, examples, licensing, and schema caveats. This guide is written for a public-skill style library where the same artifact can be handled by several neighbouring workflows. Hugging Face tasks where dataset inspection, local model selection, training, and deployment share vocabulary.

The important distinction is not just the file type or tool name. Route here when the user is asking for dataset readiness summary and the request depends on dataset id/card or dataset description, and need for splits, columns, row examples, or labels. If the task shifts toward a different final artifact, keep the domain context but choose the neighbouring skill instead.

## Good fit

Use before modelling when the user needs to understand data shape and suitability. In practice the request may mention only part of the context, so check for the combination of source material, requested judgement, and the kind of handoff the user expects.

| Useful clue | Why it matters |
|---|---|
| Dataset id/card or dataset description | Dataset readiness summary |
| Need for splits, columns, row examples, or labels | Schema and split table |

When the request is underspecified, ask for the smallest missing item. For example, if the user gives the artifact but not the acceptance criterion, state what you will assume before doing irreversible work.

## Playbook

A normal run is usually:

1. Inspect dataset metadata.
2. Check subsets/splits/features.
3. List examples and caveats.
4. Identify readiness risks.

Do not treat the list above as a rigid template. Public skills often arrive with partial notes, linked files, or copied examples. Preserve the user's ordering when it matters, but keep the final answer focused on the decision the skill is responsible for.

```yaml
handoff:
  needs: ["Dataset id/card or dataset description", "Need for splits, columns, row examples, or labels"]
  returns: ["Dataset readiness summary", "Schema and split table"]
  tools: ["Hugging Face Dataset Viewer or dataset card"]
  uncertainty: keep page, file, row, log, or source anchors when available
```

## Handoff

The handoff is usually a compact artifact rather than a long essay. Include dataset readiness summary, schema and split table, and risks when those pieces are supported by the source material. If a requested field cannot be found, mark it as missing instead of inventing it.

Typical return blocks:

- Dataset readiness summary
- Schema and split table
- Risks

## Boundaries

Not for local model selection, fine-tuning, Gradio UI, or Spaces deployment. Nearby skills in this cluster include `psc-local-model-fit-selector`, `psc-sentence-embedding-trainer`, `psc-hf-space-deployment-preparer`. They may share nouns with this skill, so route by the requested artifact and the work sequence, not by the domain word alone.

A common routing mistake is to select by a shared noun in the prompt and miss the user's requested output. Prefer the skill whose procedure would actually produce the requested handoff.

## Tools and files

This workflow can be carried out with hugging face dataset viewer or dataset card. Equivalent tools are fine, but they must preserve the same inspection or verification standard. Keep anchors such as filenames, pages, rows, source snippets, log lines, screenshots, or model/dataset identifiers when they are available.

Useful source clues, in rough order: Dataset id/card or dataset description. Need for splits, columns, row examples, or labels.

## Samples

- Use Hugging Face dataset information to inspect the ticket dataset's splits, columns, labels, row examples, and licensing caveats before we model it.
- Before training anything, audit the dataset card: subsets, train/validation/test split, feature schema, example rows, labels, and data caveats.

Less ideal but still valid request: "Can you look at this and tell me what should happen next?" In that case, first decide whether the user wants dataset readiness summary or a neighbouring artifact, then ask one clarifying question if needed.

## Checks

- The response clearly produces dataset readiness summary.
- The answer explains uncertainty instead of silently guessing.
- The chosen process matches the user's artifact and requested outcome.
- Secondary outputs are included only when they support the requested result.

Before finishing, compare the answer against the nearby-skill boundary above. If the output would be more naturally produced by another skill, say so and switch rather than stretching this workflow.
