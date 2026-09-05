---
name: psc-executive-metric-narrator
description: "Spreadsheet analysis workflow involving CSV data, metrics, data quality, anomalies, decision ranking, reporting, and business interpretation. Turn tabular metrics into an upward-facing executive brief with headline, key takeaways, risks, and recommended next steps."
category: public-style-controlled
tags:
  - public-style
  - controlled-confusability
  - psc-data-analysis-intent
metadata:
  source_style: public_style_controlled
  cluster_id: psc_data_analysis_intent
---

# Executive Metric Narrator

## How this works

Turn tabular metrics into an upward-facing executive brief with headline, key takeaways, risks, and recommended next steps. This guide is written for a public-skill style library where the same artifact can be handled by several neighbouring workflows. Same spreadsheet or dataset, different analytical intent: trust audit, anomaly watchlist, decision ranking, or executive narrative.

The important distinction is not just the file type or tool name. Route here when the user is asking for executive headline and the request depends on metric table, and business audience. If the task shifts toward a different final artifact, keep the domain context but choose the neighbouring skill instead.

## Typical triggers

Use when the audience is leadership and the requested output is communication, not exploration. In practice the request may mention only part of the context, so check for the combination of source material, requested judgement, and the kind of handoff the user expects.

| Useful clue | Why it matters |
|---|---|
| Metric table | Executive headline |
| Business audience | Key takeaways |
| Need for concise takeaway narrative | Risks |

When the request is underspecified, ask for the smallest missing item. For example, if the user gives the artifact but not the acceptance criterion, state what you will assume before doing irreversible work.

## Steps

A normal run is usually:

1. Identify headline and key movements.
2. Translate metrics into business implications.
3. List risks and recommended next steps.

Do not treat the list above as a rigid template. Public skills often arrive with partial notes, linked files, or copied examples. Preserve the user's ordering when it matters, but keep the final answer focused on the decision the skill is responsible for.

```yaml
handoff:
  needs: ["Metric table", "Business audience"]
  returns: ["Executive headline", "Key takeaways"]
  tools: ["Metric summary or spreadsheet"]
  uncertainty: keep page, file, row, log, or source anchors when available
```

## What to return

The handoff is usually a compact artifact rather than a long essay. Include executive headline, key takeaways, risks, and recommended actions when those pieces are supported by the source material. If a requested field cannot be found, mark it as missing instead of inventing it.

Typical return blocks:

- Executive headline
- Key takeaways
- Risks
- Recommended actions

## Neighbouring skills

Not for deep anomaly scanning, data-quality auditing, or option ranking unless requested. Nearby skills in this cluster include `psc-data-trust-auditor`, `psc-anomaly-watchlist-builder`, `psc-decision-ranking-analyst`. They may share nouns with this skill, so route by the requested artifact and the work sequence, not by the domain word alone.

A common routing mistake is to select by a shared noun in the prompt and miss the user's requested output. Prefer the skill whose procedure would actually produce the requested handoff.

## Operational notes

This workflow can be carried out with metric summary or spreadsheet. Equivalent tools are fine, but they must preserve the same inspection or verification standard. Keep anchors such as filenames, pages, rows, source snippets, log lines, screenshots, or model/dataset identifiers when they are available.

Useful source clues, in rough order: Metric table. Business audience. Need for concise takeaway narrative.

## Requests

- Turn the weekly performance table into a leadership-ready brief: headline, key movements, risks, and two recommended next steps.
- Write an executive metric narrative from the spreadsheet. I need business takeaways and actions, not data validation or anomaly hunting.

Less ideal but still valid request: "Can you look at this and tell me what should happen next?" In that case, first decide whether the user wants executive headline or a neighbouring artifact, then ask one clarifying question if needed.

## Review notes

- The response clearly produces executive headline.
- The answer explains uncertainty instead of silently guessing.
- The chosen process matches the user's artifact and requested outcome.
- Secondary outputs are included only when they support the requested result.

Before finishing, compare the answer against the nearby-skill boundary above. If the output would be more naturally produced by another skill, say so and switch rather than stretching this workflow.
