---
name: psc-paper-method-mapper
description: "Research-reading workflow involving papers, sources, claims, methods, evidence, comparison, synthesis, and thesis writing. Extract a paper's method design, data, baselines, experimental setup, assumptions, and evaluation limitations."
category: public-style-controlled
tags:
  - public-style
  - controlled-confusability
  - psc-research-reading
metadata:
  source_style: public_style_controlled
  cluster_id: psc_research_reading
---

# Paper Method Mapper

## Capability

Extract a paper's method design, data, baselines, experimental setup, assumptions, and evaluation limitations. This guide is written for a public-skill style library where the same artifact can be handled by several neighbouring workflows. Research reading tasks where summary, method extraction, citation grounding, and synthesis share academic language.

The important distinction is not just the file type or tool name. Route here when the user is asking for method map and the request depends on paper or method excerpt, and need for experiment/setup detail. If the task shifts toward a different final artifact, keep the domain context but choose the neighbouring skill instead.

## Good fit

Use when the user cares about how a paper was carried out rather than only its conclusion. In practice the request may mention only part of the context, so check for the combination of source material, requested judgement, and the kind of handoff the user expects.

| Useful clue | Why it matters |
|---|---|
| Paper or method excerpt | Method map |
| Need for experiment/setup detail | Evaluation setup |

When the request is underspecified, ask for the smallest missing item. For example, if the user gives the artifact but not the acceptance criterion, state what you will assume before doing irreversible work.

## Playbook

A normal run is usually:

1. Identify method components, data, baselines, metrics, and assumptions.
2. Separate reported results from evaluation design.
3. List limitations.

Do not treat the list above as a rigid template. Public skills often arrive with partial notes, linked files, or copied examples. Preserve the user's ordering when it matters, but keep the final answer focused on the decision the skill is responsible for.

```yaml
handoff:
  needs: ["Paper or method excerpt", "Need for experiment/setup detail"]
  returns: ["Method map", "Evaluation setup"]
  tools: ["Paper text"]
  uncertainty: keep page, file, row, log, or source anchors when available
```

## Handoff

The handoff is usually a compact artifact rather than a long essay. Include method map, evaluation setup, assumptions, and limitations when those pieces are supported by the source material. If a requested field cannot be found, mark it as missing instead of inventing it.

Typical return blocks:

- Method map
- Evaluation setup
- Assumptions
- Limitations

## Boundaries

Not a general summary, citation support audit, or multi-paper synthesis. Nearby skills in this cluster include `psc-citation-claim-support-auditor`, `psc-related-work-synthesizer`, `psc-source-field-table-extractor`. They may share nouns with this skill, so route by the requested artifact and the work sequence, not by the domain word alone.

A common routing mistake is to select by a shared noun in the prompt and miss the user's requested output. Prefer the skill whose procedure would actually produce the requested handoff.

## Tools and files

This workflow can be carried out with paper text. Equivalent tools are fine, but they must preserve the same inspection or verification standard. Keep anchors such as filenames, pages, rows, source snippets, log lines, screenshots, or model/dataset identifiers when they are available.

Useful source clues, in rough order: Paper or method excerpt. Need for experiment/setup detail.

## Samples

- For this paper, map how the study was carried out: data, method components, baselines, metrics, assumptions, and evaluation limits.
- Extract method and evaluation details from the paper. I need setup, baselines, metrics, assumptions, and limitations, not a broad summary.

Less ideal but still valid request: "Can you look at this and tell me what should happen next?" In that case, first decide whether the user wants method map or a neighbouring artifact, then ask one clarifying question if needed.

## Checks

- The response clearly produces method map.
- The answer explains uncertainty instead of silently guessing.
- The chosen process matches the user's artifact and requested outcome.
- Secondary outputs are included only when they support the requested result.

Before finishing, compare the answer against the nearby-skill boundary above. If the output would be more naturally produced by another skill, say so and switch rather than stretching this workflow.
