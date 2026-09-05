---
name: psc-source-field-table-extractor
description: "Research-reading workflow involving papers, sources, claims, methods, evidence, comparison, synthesis, and thesis writing. Extract specific fields from sources into a structured table for later comparison or coding."
category: public-style-controlled
tags:
  - public-style
  - controlled-confusability
  - psc-research-reading
metadata:
  source_style: public_style_controlled
  cluster_id: psc_research_reading
---

# Source Field Table Extractor

## Purpose

Extract specific fields from sources into a structured table for later comparison or coding. This guide is written for a public-skill style library where the same artifact can be handled by several neighbouring workflows. Research reading tasks where summary, method extraction, citation grounding, and synthesis share academic language.

The important distinction is not just the file type or tool name. Route here when the user is asking for field-value table and the request depends on source text, and field list or extraction schema. If the task shifts toward a different final artifact, keep the domain context but choose the neighbouring skill instead.

## Common requests

Use when the user wants reusable fields, not prose summary. In practice the request may mention only part of the context, so check for the combination of source material, requested judgement, and the kind of handoff the user expects.

| Useful clue | Why it matters |
|---|---|
| Source text | Field-value table |
| Field list or extraction schema | Evidence snippets |
| Need for structured output | Missing-field notes |

When the request is underspecified, ask for the smallest missing item. For example, if the user gives the artifact but not the acceptance criterion, state what you will assume before doing irreversible work.

## Instructions

A normal run is usually:

1. Identify requested fields.
2. Extract values with evidence snippets.
3. Mark missing or ambiguous fields.
4. Return a table.

Do not treat the list above as a rigid template. Public skills often arrive with partial notes, linked files, or copied examples. Preserve the user's ordering when it matters, but keep the final answer focused on the decision the skill is responsible for.

```yaml
handoff:
  needs: ["Source text", "Field list or extraction schema"]
  returns: ["Field-value table", "Evidence snippets"]
  tools: ["Source text and field schema"]
  uncertainty: keep page, file, row, log, or source anchors when available
```

## Response shape

The handoff is usually a compact artifact rather than a long essay. Include field-value table, evidence snippets, and missing-field notes when those pieces are supported by the source material. If a requested field cannot be found, mark it as missing instead of inventing it.

Typical return blocks:

- Field-value table
- Evidence snippets
- Missing-field notes

## Common mistakes

Not for broad synthesis, citation support, or method-only reading unless those are requested fields. Nearby skills in this cluster include `psc-paper-method-mapper`, `psc-citation-claim-support-auditor`, `psc-related-work-synthesizer`. They may share nouns with this skill, so route by the requested artifact and the work sequence, not by the domain word alone.

A common routing mistake is to select by a shared noun in the prompt and miss the user's requested output. Prefer the skill whose procedure would actually produce the requested handoff.

## Environment notes

This workflow can be carried out with source text and field schema. Equivalent tools are fine, but they must preserve the same inspection or verification standard. Keep anchors such as filenames, pages, rows, source snippets, log lines, screenshots, or model/dataset identifiers when they are available.

Useful source clues, in rough order: Source text. Field list or extraction schema. Need for structured output.

## Example prompts

- Extract each paper's dataset, task, model, baseline, metric, result, and limitation into a comparison table with source evidence.
- Turn the source into a structured field table. I need field values and evidence snippets, not a narrative summary or related-work synthesis.

Less ideal but still valid request: "Can you look at this and tell me what should happen next?" In that case, first decide whether the user wants field-value table or a neighbouring artifact, then ask one clarifying question if needed.

## Validation

- The response clearly produces field-value table.
- The answer explains uncertainty instead of silently guessing.
- The chosen process matches the user's artifact and requested outcome.
- Secondary outputs are included only when they support the requested result.

Before finishing, compare the answer against the nearby-skill boundary above. If the output would be more naturally produced by another skill, say so and switch rather than stretching this workflow.
