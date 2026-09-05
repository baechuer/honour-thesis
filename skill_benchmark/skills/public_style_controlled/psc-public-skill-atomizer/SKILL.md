---
name: psc-public-skill-atomizer
description: "Skill-library workflow involving skill artifacts, routing, fields, atomization, benchmark results, candidates, and evaluation. Split broad or hierarchical public skills into atomic skill candidates while preserving shared resources and routing boundaries."
category: public-style-controlled
tags:
  - public-style
  - controlled-confusability
  - psc-skill-representation
metadata:
  source_style: public_style_controlled
  cluster_id: psc_skill_representation
---

# Public Skill Atomizer

## How this works

Split broad or hierarchical public skills into atomic skill candidates while preserving shared resources and routing boundaries. This guide is written for a public-skill style library where the same artifact can be handled by several neighbouring workflows. Skill-library maintenance where field extraction, atomization, routing policy, and result adjudication are easily conflated.

The important distinction is not just the file type or tool name. Route here when the user is asking for atomic skill list and the request depends on broad skill artifact, and subworkflow boundaries. If the task shifts toward a different final artifact, keep the domain context but choose the neighbouring skill instead.

## Typical triggers

Use when one public skill contains multiple internal workflows or domain branches. In practice the request may mention only part of the context, so check for the combination of source material, requested judgement, and the kind of handoff the user expects.

| Useful clue | Why it matters |
|---|---|
| Broad skill artifact | Atomic skill list |
| Subworkflow boundaries | Shared resources |
| Shared resources or links | Parent/child mapping |

When the request is underspecified, ask for the smallest missing item. For example, if the user gives the artifact but not the acceptance criterion, state what you will assume before doing irreversible work.

## Steps

A normal run is usually:

1. Identify internal branches.
2. Create atomic child-skill candidates.
3. Preserve shared resources and parent links.
4. State routing boundaries.

Do not treat the list above as a rigid template. Public skills often arrive with partial notes, linked files, or copied examples. Preserve the user's ordering when it matters, but keep the final answer focused on the decision the skill is responsible for.

```yaml
handoff:
  needs: ["Broad skill artifact", "Subworkflow boundaries"]
  returns: ["Atomic skill list", "Shared resources"]
  tools: ["Broad skill file and linked resources"]
  uncertainty: keep page, file, row, log, or source anchors when available
```

## What to return

The handoff is usually a compact artifact rather than a long essay. Include atomic skill list, shared resources, parent/child mapping, and boundary notes when those pieces are supported by the source material. If a requested field cannot be found, mark it as missing instead of inventing it.

Typical return blocks:

- Atomic skill list
- Shared resources
- Parent/child mapping
- Boundary notes

## Neighbouring skills

Not for simple field extraction or retrieval-result scoring. Nearby skills in this cluster include `psc-messy-skill-field-extractor`, `psc-skill-routing-budget-planner`, `psc-retrieval-result-adjudicator`. They may share nouns with this skill, so route by the requested artifact and the work sequence, not by the domain word alone.

A common routing mistake is to select by a shared noun in the prompt and miss the user's requested output. Prefer the skill whose procedure would actually produce the requested handoff.

## Operational notes

This workflow can be carried out with broad skill file and linked resources. Equivalent tools are fine, but they must preserve the same inspection or verification standard. Keep anchors such as filenames, pages, rows, source snippets, log lines, screenshots, or model/dataset identifiers when they are available.

Useful source clues, in rough order: Broad skill artifact. Subworkflow boundaries. Shared resources or links.

## Requests

- This public skill has separate finance, document, and research branches inside one file. Split it into atomic skill candidates and keep shared resources linked.
- Atomize a broad hierarchical skill into standalone child skills with preserved resource references and routing boundaries.

Less ideal but still valid request: "Can you look at this and tell me what should happen next?" In that case, first decide whether the user wants atomic skill list or a neighbouring artifact, then ask one clarifying question if needed.

## Review notes

- The response clearly produces atomic skill list.
- The answer explains uncertainty instead of silently guessing.
- The chosen process matches the user's artifact and requested outcome.
- Secondary outputs are included only when they support the requested result.

Before finishing, compare the answer against the nearby-skill boundary above. If the output would be more naturally produced by another skill, say so and switch rather than stretching this workflow.
