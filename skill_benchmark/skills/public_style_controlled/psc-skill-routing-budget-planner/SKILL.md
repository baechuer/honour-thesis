---
name: psc-skill-routing-budget-planner
description: "Skill-library workflow involving skill artifacts, routing, fields, atomization, benchmark results, candidates, and evaluation. Design candidate-generation, representation, reranking, budget, fallback, and clarification policy for large skill libraries."
category: public-style-controlled
tags:
  - public-style
  - controlled-confusability
  - psc-skill-representation
metadata:
  source_style: public_style_controlled
  cluster_id: psc_skill_representation
---

# Skill Routing Budget Planner

## Guide

Design candidate-generation, representation, reranking, budget, fallback, and clarification policy for large skill libraries. This guide is written for a public-skill style library where the same artifact can be handled by several neighbouring workflows. Skill-library maintenance where field extraction, atomization, routing policy, and result adjudication are easily conflated.

The important distinction is not just the file type or tool name. Route here when the user is asking for routing stages and the request depends on skill library scale, and candidate budget. If the task shifts toward a different final artifact, keep the domain context but choose the neighbouring skill instead.

## Routing notes

Use when the requested artifact is a selector or routing policy. In practice the request may mention only part of the context, so check for the combination of source material, requested judgement, and the kind of handoff the user expects.

| Useful clue | Why it matters |
|---|---|
| Skill library scale | Routing stages |
| Candidate budget | Budgets |
| Representation/retrieval choices | Representation fields |

When the request is underspecified, ask for the smallest missing item. For example, if the user gives the artifact but not the acceptance criterion, state what you will assume before doing irreversible work.

## Workflow

A normal run is usually:

1. Define first-stage retrieval.
2. Choose representation fields.
3. Set reranking and fallback policy.
4. Specify metrics and cost controls.

Do not treat the list above as a rigid template. Public skills often arrive with partial notes, linked files, or copied examples. Preserve the user's ordering when it matters, but keep the final answer focused on the decision the skill is responsible for.

```yaml
handoff:
  needs: ["Skill library scale", "Candidate budget"]
  returns: ["Routing stages", "Budgets"]
  tools: ["Skill library inventory or scale assumptions"]
  uncertainty: keep page, file, row, log, or source anchors when available
```

## Deliverables

The handoff is usually a compact artifact rather than a long essay. Include routing stages, budgets, representation fields, and fallback/metrics when those pieces are supported by the source material. If a requested field cannot be found, mark it as missing instead of inventing it.

Typical return blocks:

- Routing stages
- Budgets
- Representation fields
- Fallback/metrics

## Anti-patterns

Not for auditing one skill's fields or splitting a hierarchical skill. Nearby skills in this cluster include `psc-messy-skill-field-extractor`, `psc-public-skill-atomizer`, `psc-retrieval-result-adjudicator`. They may share nouns with this skill, so route by the requested artifact and the work sequence, not by the domain word alone.

A common routing mistake is to select by a shared noun in the prompt and miss the user's requested output. Prefer the skill whose procedure would actually produce the requested handoff.

## Dependencies

This workflow can be carried out with skill library inventory or scale assumptions. Equivalent tools are fine, but they must preserve the same inspection or verification standard. Keep anchors such as filenames, pages, rows, source snippets, log lines, screenshots, or model/dataset identifiers when they are available.

Useful source clues, in rough order: Skill library scale. Candidate budget. Representation/retrieval choices.

## Usage examples

- Design a routing policy for a 2000-skill library: candidate generation, representation fields, reranking, fallback, and cost controls.
- Specify a candidate-subsetting architecture for skill retrieval with top-k budgets, field-aware reranking, fallback, and evaluation metrics.

Less ideal but still valid request: "Can you look at this and tell me what should happen next?" In that case, first decide whether the user wants routing stages or a neighbouring artifact, then ask one clarifying question if needed.

## Quality bar

- The response clearly produces routing stages.
- The answer explains uncertainty instead of silently guessing.
- The chosen process matches the user's artifact and requested outcome.
- Secondary outputs are included only when they support the requested result.

Before finishing, compare the answer against the nearby-skill boundary above. If the output would be more naturally produced by another skill, say so and switch rather than stretching this workflow.
