---
name: psc-anomaly-watchlist-builder
description: "Spreadsheet analysis workflow involving CSV data, metrics, data quality, anomalies, decision ranking, reporting, and business interpretation. Find unusual spikes, drops, outliers, concentration, and abrupt changes in tabular metrics for follow-up investigation."
category: public-style-controlled
tags:
  - public-style
  - controlled-confusability
  - psc-data-analysis-intent
metadata:
  source_style: public_style_controlled
  cluster_id: psc_data_analysis_intent
---

# Anomaly Watchlist Builder

## Guide

Find unusual spikes, drops, outliers, concentration, and abrupt changes in tabular metrics for follow-up investigation. This guide is written for a public-skill style library where the same artifact can be handled by several neighbouring workflows. Same spreadsheet or dataset, different analytical intent: trust audit, anomaly watchlist, decision ranking, or executive narrative.

The important distinction is not just the file type or tool name. Route here when the user is asking for anomaly watchlist and the request depends on time series or metric table, and baseline or comparison window. If the task shifts toward a different final artifact, keep the domain context but choose the neighbouring skill instead.

## Routing notes

Use when the task is to identify what looks unusual rather than explain the final cause. In practice the request may mention only part of the context, so check for the combination of source material, requested judgement, and the kind of handoff the user expects.

| Useful clue | Why it matters |
|---|---|
| Time series or metric table | Anomaly watchlist |
| Baseline or comparison window | Evidence metric/window |
| Need for follow-up prioritization | Priority |

When the request is underspecified, ask for the smallest missing item. For example, if the user gives the artifact but not the acceptance criterion, state what you will assume before doing irreversible work.

## Workflow

A normal run is usually:

1. Compare current values to baseline.
2. Flag spikes, dips, outliers, and concentration.
3. Rank anomalies by severity and confidence.

Do not treat the list above as a rigid template. Public skills often arrive with partial notes, linked files, or copied examples. Preserve the user's ordering when it matters, but keep the final answer focused on the decision the skill is responsible for.

```yaml
handoff:
  needs: ["Time series or metric table", "Baseline or comparison window"]
  returns: ["Anomaly watchlist", "Evidence metric/window"]
  tools: ["Tabular metrics"]
  uncertainty: keep page, file, row, log, or source anchors when available
```

## Deliverables

The handoff is usually a compact artifact rather than a long essay. Include anomaly watchlist, evidence metric/window, priority, and next check when those pieces are supported by the source material. If a requested field cannot be found, mark it as missing instead of inventing it.

Typical return blocks:

- Anomaly watchlist
- Evidence metric/window
- Priority
- Next check

## Anti-patterns

Not for data trust auditing, forecasting, or final executive narrative. Nearby skills in this cluster include `psc-data-trust-auditor`, `psc-decision-ranking-analyst`, `psc-executive-metric-narrator`. They may share nouns with this skill, so route by the requested artifact and the work sequence, not by the domain word alone.

A common routing mistake is to select by a shared noun in the prompt and miss the user's requested output. Prefer the skill whose procedure would actually produce the requested handoff.

## Dependencies

This workflow can be carried out with tabular metrics. Equivalent tools are fine, but they must preserve the same inspection or verification standard. Keep anchors such as filenames, pages, rows, source snippets, log lines, screenshots, or model/dataset identifiers when they are available.

Useful source clues, in rough order: Time series or metric table. Baseline or comparison window. Need for follow-up prioritization.

## Usage examples

- Scan the weekly channel metrics for unusual spikes, drops, outliers, or concentrated deviations that deserve follow-up.
- Build an anomaly watchlist from the CSV with evidence windows and priorities. Do not turn it into a broad reporting brief.

Less ideal but still valid request: "Can you look at this and tell me what should happen next?" In that case, first decide whether the user wants anomaly watchlist or a neighbouring artifact, then ask one clarifying question if needed.

## Quality bar

- The response clearly produces anomaly watchlist.
- The answer explains uncertainty instead of silently guessing.
- The chosen process matches the user's artifact and requested outcome.
- Secondary outputs are included only when they support the requested result.

Before finishing, compare the answer against the nearby-skill boundary above. If the output would be more naturally produced by another skill, say so and switch rather than stretching this workflow.
