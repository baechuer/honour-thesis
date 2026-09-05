---
name: psc-citation-claim-support-auditor
description: "Research-reading workflow involving papers, sources, claims, methods, evidence, comparison, synthesis, and thesis writing. Check whether a draft claim is supported by a source and record quoted/paraphrased evidence, caveats, and citation risk."
category: public-style-controlled
tags:
  - public-style
  - controlled-confusability
  - psc-research-reading
metadata:
  source_style: public_style_controlled
  cluster_id: psc_research_reading
---

# Citation Claim Support Auditor

## Guide

Check whether a draft claim is supported by a source and record quoted/paraphrased evidence, caveats, and citation risk. This guide is written for a public-skill style library where the same artifact can be handled by several neighbouring workflows. Research reading tasks where summary, method extraction, citation grounding, and synthesis share academic language.

The important distinction is not just the file type or tool name. Route here when the user is asking for support verdict and the request depends on draft claim, and source text. If the task shifts toward a different final artifact, keep the domain context but choose the neighbouring skill instead.

## Routing notes

Use when the user has a claim and needs to know whether the source supports it. In practice the request may mention only part of the context, so check for the combination of source material, requested judgement, and the kind of handoff the user expects.

| Useful clue | Why it matters |
|---|---|
| Draft claim | Support verdict |
| Source text | Evidence |
| Need for support/caveat judgment | Caveat |

When the request is underspecified, ask for the smallest missing item. For example, if the user gives the artifact but not the acceptance criterion, state what you will assume before doing irreversible work.

## Workflow

A normal run is usually:

1. Locate source evidence.
2. Judge support strength.
3. Identify overclaiming or missing caveats.
4. Return safe wording.

Do not treat the list above as a rigid template. Public skills often arrive with partial notes, linked files, or copied examples. Preserve the user's ordering when it matters, but keep the final answer focused on the decision the skill is responsible for.

```yaml
handoff:
  needs: ["Draft claim", "Source text"]
  returns: ["Support verdict", "Evidence"]
  tools: ["Source text and draft claim"]
  uncertainty: keep page, file, row, log, or source anchors when available
```

## Deliverables

The handoff is usually a compact artifact rather than a long essay. Include support verdict, evidence, caveat, and safer wording when those pieces are supported by the source material. If a requested field cannot be found, mark it as missing instead of inventing it.

Typical return blocks:

- Support verdict
- Evidence
- Caveat
- Safer wording

## Anti-patterns

Not for summarizing the whole paper or extracting all methods. Nearby skills in this cluster include `psc-paper-method-mapper`, `psc-related-work-synthesizer`, `psc-source-field-table-extractor`. They may share nouns with this skill, so route by the requested artifact and the work sequence, not by the domain word alone.

A common routing mistake is to select by a shared noun in the prompt and miss the user's requested output. Prefer the skill whose procedure would actually produce the requested handoff.

## Dependencies

This workflow can be carried out with source text and draft claim. Equivalent tools are fine, but they must preserve the same inspection or verification standard. Keep anchors such as filenames, pages, rows, source snippets, log lines, screenshots, or model/dataset identifiers when they are available.

Useful source clues, in rough order: Draft claim. Source text. Need for support/caveat judgment.

## Usage examples

- Check whether this source really supports my sentence about skill libraries improving agent reliability, and suggest safer wording if it overclaims.
- Perform a citation-grounding audit for one draft claim: support strength, exact evidence, caveats, and revised claim wording.

Less ideal but still valid request: "Can you look at this and tell me what should happen next?" In that case, first decide whether the user wants support verdict or a neighbouring artifact, then ask one clarifying question if needed.

## Quality bar

- The response clearly produces support verdict.
- The answer explains uncertainty instead of silently guessing.
- The chosen process matches the user's artifact and requested outcome.
- Secondary outputs are included only when they support the requested result.

Before finishing, compare the answer against the nearby-skill boundary above. If the output would be more naturally produced by another skill, say so and switch rather than stretching this workflow.
