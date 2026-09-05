---
name: psc-related-work-synthesizer
description: "Research-reading workflow involving papers, sources, claims, methods, evidence, comparison, synthesis, and thesis writing. Synthesize multiple papers into related-work themes, contrasts, unresolved gaps, and positioning for a thesis argument."
category: public-style-controlled
tags:
  - public-style
  - controlled-confusability
  - psc-research-reading
metadata:
  source_style: public_style_controlled
  cluster_id: psc_research_reading
---

# Related Work Synthesizer

## About

Synthesize multiple papers into related-work themes, contrasts, unresolved gaps, and positioning for a thesis argument. This guide is written for a public-skill style library where the same artifact can be handled by several neighbouring workflows. Research reading tasks where summary, method extraction, citation grounding, and synthesis share academic language.

The important distinction is not just the file type or tool name. Route here when the user is asking for related-work synthesis and the request depends on two or more sources, and need for thematic comparison and gap framing. If the task shifts toward a different final artifact, keep the domain context but choose the neighbouring skill instead.

## Use it for

Use when there are multiple sources and the output should connect them into a research narrative. In practice the request may mention only part of the context, so check for the combination of source material, requested judgement, and the kind of handoff the user expects.

| Useful clue | Why it matters |
|---|---|
| Two or more sources | Related-work synthesis |
| Need for thematic comparison and gap framing | Theme comparison |

When the request is underspecified, ask for the smallest missing item. For example, if the user gives the artifact but not the acceptance criterion, state what you will assume before doing irreversible work.

## Process

A normal run is usually:

1. Group approaches by theme.
2. Compare assumptions and evidence.
3. Identify tensions and gaps.
4. Write positioning notes.

Do not treat the list above as a rigid template. Public skills often arrive with partial notes, linked files, or copied examples. Preserve the user's ordering when it matters, but keep the final answer focused on the decision the skill is responsible for.

```yaml
handoff:
  needs: ["Two or more sources", "Need for thematic comparison and gap framing"]
  returns: ["Related-work synthesis", "Theme comparison"]
  tools: ["Multiple source notes"]
  uncertainty: keep page, file, row, log, or source anchors when available
```

## Expected artifacts

The handoff is usually a compact artifact rather than a long essay. Include related-work synthesis, theme comparison, and gap statement when those pieces are supported by the source material. If a requested field cannot be found, mark it as missing instead of inventing it.

Typical return blocks:

- Related-work synthesis
- Theme comparison
- Gap statement

## Do not use for

Not for single-paper method extraction or claim-level citation checking. Nearby skills in this cluster include `psc-paper-method-mapper`, `psc-citation-claim-support-auditor`, `psc-source-field-table-extractor`. They may share nouns with this skill, so route by the requested artifact and the work sequence, not by the domain word alone.

A common routing mistake is to select by a shared noun in the prompt and miss the user's requested output. Prefer the skill whose procedure would actually produce the requested handoff.

## Runtime assumptions

This workflow can be carried out with multiple source notes. Equivalent tools are fine, but they must preserve the same inspection or verification standard. Keep anchors such as filenames, pages, rows, source snippets, log lines, screenshots, or model/dataset identifiers when they are available.

Useful source clues, in rough order: Two or more sources. Need for thematic comparison and gap framing.

## Examples

- Use these three papers to write related-work notes that compare approaches, show where they agree or diverge, and identify the gap my thesis targets.
- Synthesize multiple sources into a related-work argument with themes, contrasts, unresolved limitations, and thesis positioning.

Less ideal but still valid request: "Can you look at this and tell me what should happen next?" In that case, first decide whether the user wants related-work synthesis or a neighbouring artifact, then ask one clarifying question if needed.

## Acceptance

- The response clearly produces related-work synthesis.
- The answer explains uncertainty instead of silently guessing.
- The chosen process matches the user's artifact and requested outcome.
- Secondary outputs are included only when they support the requested result.

Before finishing, compare the answer against the nearby-skill boundary above. If the output would be more naturally produced by another skill, say so and switch rather than stretching this workflow.
