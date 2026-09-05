---
name: psc-retrieval-result-adjudicator
description: "Skill-library workflow involving skill artifacts, routing, fields, atomization, benchmark results, candidates, and evaluation. Adjudicate skill retrieval results with strict gold labels, acceptable alternatives, failure categories, top-k, MRR, and non-core false positives."
category: public-style-controlled
tags:
  - public-style
  - controlled-confusability
  - psc-skill-representation
metadata:
  source_style: public_style_controlled
  cluster_id: psc_skill_representation
---

# Retrieval Result Adjudicator

## How this works

Adjudicate skill retrieval results with strict gold labels, acceptable alternatives, failure categories, top-k, MRR, and non-core false positives. This guide is written for a public-skill style library where the same artifact can be handled by several neighbouring workflows. Skill-library maintenance where field extraction, atomization, routing policy, and result adjudication are easily conflated.

The important distinction is not just the file type or tool name. Route here when the user is asking for metrics and the request depends on prompt/gold set, and ranked retrieval output. If the task shifts toward a different final artifact, keep the domain context but choose the neighbouring skill instead.

## Typical triggers

Use after retrieval has already produced rankings and the task is evaluation. In practice the request may mention only part of the context, so check for the combination of source material, requested judgement, and the kind of handoff the user expects.

| Useful clue | Why it matters |
|---|---|
| Prompt/gold set | Metrics |
| Ranked retrieval output | Failure categories |
| Acceptable alternative policy | Adjudication notes |

When the request is underspecified, ask for the smallest missing item. For example, if the user gives the artifact but not the acceptance criterion, state what you will assume before doing irreversible work.

## Steps

A normal run is usually:

1. Score strict and acceptable labels separately.
2. Compute top-k and MRR.
3. Classify failures by candidate miss, reranker ordering, ambiguity, or better-than-gold.

Do not treat the list above as a rigid template. Public skills often arrive with partial notes, linked files, or copied examples. Preserve the user's ordering when it matters, but keep the final answer focused on the decision the skill is responsible for.

```yaml
handoff:
  needs: ["Prompt/gold set", "Ranked retrieval output"]
  returns: ["Metrics", "Failure categories"]
  tools: ["Retrieval result JSON", "Gold labels"]
  uncertainty: keep page, file, row, log, or source anchors when available
```

## What to return

The handoff is usually a compact artifact rather than a long essay. Include metrics, failure categories, adjudication notes, and revision queue when those pieces are supported by the source material. If a requested field cannot be found, mark it as missing instead of inventing it.

Typical return blocks:

- Metrics
- Failure categories
- Adjudication notes
- Revision queue

## Neighbouring skills

Not for designing a router policy from scratch or extracting fields from raw skills. Nearby skills in this cluster include `psc-messy-skill-field-extractor`, `psc-public-skill-atomizer`, `psc-skill-routing-budget-planner`. They may share nouns with this skill, so route by the requested artifact and the work sequence, not by the domain word alone.

A common routing mistake is to select by a shared noun in the prompt and miss the user's requested output. Prefer the skill whose procedure would actually produce the requested handoff.

## Operational notes

This workflow can be carried out with retrieval result json, and gold labels. Equivalent tools are fine, but they must preserve the same inspection or verification standard. Keep anchors such as filenames, pages, rows, source snippets, log lines, screenshots, or model/dataset identifiers when they are available.

Useful source clues, in rough order: Prompt/gold set. Ranked retrieval output. Acceptable alternative policy.

## Requests

- Evaluate these skill retrieval rankings with strict gold labels, acceptable alternatives, top-1, top-5, MRR, and failure categories.
- Adjudicate retrieval results: separate strict and acceptable scoring, identify candidate misses versus reranker losses, and flag better-than-gold cases.

Less ideal but still valid request: "Can you look at this and tell me what should happen next?" In that case, first decide whether the user wants metrics or a neighbouring artifact, then ask one clarifying question if needed.

## Review notes

- The response clearly produces metrics.
- The answer explains uncertainty instead of silently guessing.
- The chosen process matches the user's artifact and requested outcome.
- Secondary outputs are included only when they support the requested result.

Before finishing, compare the answer against the nearby-skill boundary above. If the output would be more naturally produced by another skill, say so and switch rather than stretching this workflow.
