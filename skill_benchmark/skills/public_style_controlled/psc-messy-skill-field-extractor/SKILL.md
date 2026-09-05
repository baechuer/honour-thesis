---
name: psc-messy-skill-field-extractor
description: "Skill-library workflow involving skill artifacts, routing, fields, atomization, benchmark results, candidates, and evaluation. Extract triggers, inputs, outputs, workflow, dependencies, resources, examples, and boundaries from messy public-style skill files."
category: public-style-controlled
tags:
  - public-style
  - controlled-confusability
  - psc-skill-representation
metadata:
  source_style: public_style_controlled
  cluster_id: psc_skill_representation
---

# Messy Skill Field Extractor

## Overview

Extract triggers, inputs, outputs, workflow, dependencies, resources, examples, and boundaries from messy public-style skill files. This guide is written for a public-skill style library where the same artifact can be handled by several neighbouring workflows. Skill-library maintenance where field extraction, atomization, routing policy, and result adjudication are easily conflated.

The important distinction is not just the file type or tool name. Route here when the user is asking for field audit and the request depends on one or more skill files, and field taxonomy. If the task shifts toward a different final artifact, keep the domain context but choose the neighbouring skill instead.

## When to use this skill

Use when the source is an existing skill artifact and the output is a field audit. In practice the request may mention only part of the context, so check for the combination of source material, requested judgement, and the kind of handoff the user expects.

| Useful clue | Why it matters |
|---|---|
| One or more skill files | Field audit |
| Field taxonomy | Evidence spans |
| Need for evidence spans | Explicit/implicit/missing labels |

When the request is underspecified, ask for the smallest missing item. For example, if the user gives the artifact but not the acceptance criterion, state what you will assume before doing irreversible work.

## Quick start

A normal run is usually:

1. Read the raw skill body.
2. Extract explicit and implicit fields.
3. Quote evidence and mark missing fields.
4. Separate artifact fields from inferred selector fields.

Do not treat the list above as a rigid template. Public skills often arrive with partial notes, linked files, or copied examples. Preserve the user's ordering when it matters, but keep the final answer focused on the decision the skill is responsible for.

```yaml
handoff:
  needs: ["One or more skill files", "Field taxonomy"]
  returns: ["Field audit", "Evidence spans"]
  tools: ["Raw skill artifacts"]
  uncertainty: keep page, file, row, log, or source anchors when available
```

## Output format

The handoff is usually a compact artifact rather than a long essay. Include field audit, evidence spans, and explicit/implicit/missing labels when those pieces are supported by the source material. If a requested field cannot be found, mark it as missing instead of inventing it.

Typical return blocks:

- Field audit
- Evidence spans
- Explicit/implicit/missing labels

## When not to use this skill

Not for authoring a new skill, installing a package, or evaluating retrieval results. Nearby skills in this cluster include `psc-public-skill-atomizer`, `psc-skill-routing-budget-planner`, `psc-retrieval-result-adjudicator`. They may share nouns with this skill, so route by the requested artifact and the work sequence, not by the domain word alone.

A common routing mistake is to select by a shared noun in the prompt and miss the user's requested output. Prefer the skill whose procedure would actually produce the requested handoff.

## References

This workflow can be carried out with raw skill artifacts. Equivalent tools are fine, but they must preserve the same inspection or verification standard. Keep anchors such as filenames, pages, rows, source snippets, log lines, screenshots, or model/dataset identifiers when they are available.

Useful source clues, in rough order: One or more skill files. Field taxonomy. Need for evidence spans.

## Examples

- Review this rough capability note and produce a selector-facing inventory: when it should trigger, required inputs, expected artifact, steps, tools, examples, and gaps.
- Perform a field-taxonomy audit of an existing skill artifact with evidence spans. Do not write or install a new skill.

Less ideal but still valid request: "Can you look at this and tell me what should happen next?" In that case, first decide whether the user wants field audit or a neighbouring artifact, then ask one clarifying question if needed.

## Best Practices

- The response clearly produces field audit.
- The answer explains uncertainty instead of silently guessing.
- The chosen process matches the user's artifact and requested outcome.
- Secondary outputs are included only when they support the requested result.

Before finishing, compare the answer against the nearby-skill boundary above. If the output would be more naturally produced by another skill, say so and switch rather than stretching this workflow.
