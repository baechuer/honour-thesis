---
name: psc-data-trust-auditor
description: "Spreadsheet analysis workflow involving CSV data, metrics, data quality, anomalies, decision ranking, reporting, and business interpretation. Audit whether tabular data is trustworthy by checking missing values, duplicates, invalid ranges, schema drift, and calculation assumptions."
category: public-style-controlled
tags:
  - public-style
  - controlled-confusability
  - psc-data-analysis-intent
metadata:
  source_style: public_style_controlled
  cluster_id: psc_data_analysis_intent
---

# Data Trust Auditor

## Purpose

Audit whether tabular data is trustworthy by checking missing values, duplicates, invalid ranges, schema drift, and calculation assumptions. This guide is written for a public-skill style library where the same artifact can be handled by several neighbouring workflows. Same spreadsheet or dataset, different analytical intent: trust audit, anomaly watchlist, decision ranking, or executive narrative.

The important distinction is not just the file type or tool name. Route here when the user is asking for data-quality findings and the request depends on spreadsheet/csv, and expected fields or assumptions. If the task shifts toward a different final artifact, keep the domain context but choose the neighbouring skill instead.

## Common requests

Use before acting on a dataset when the user asks whether the numbers can be trusted. In practice the request may mention only part of the context, so check for the combination of source material, requested judgement, and the kind of handoff the user expects.

| Useful clue | Why it matters |
|---|---|
| Spreadsheet/CSV | Data-quality findings |
| Expected fields or assumptions | Affected fields |
| Need for quality checks | Severity |

When the request is underspecified, ask for the smallest missing item. For example, if the user gives the artifact but not the acceptance criterion, state what you will assume before doing irreversible work.

## Instructions

A normal run is usually:

1. Check missingness, duplicates, invalid values, and schema drift.
2. Flag formula or aggregation assumptions.
3. Return trust verdict and fixes.

Do not treat the list above as a rigid template. Public skills often arrive with partial notes, linked files, or copied examples. Preserve the user's ordering when it matters, but keep the final answer focused on the decision the skill is responsible for.

```yaml
handoff:
  needs: ["Spreadsheet/CSV", "Expected fields or assumptions"]
  returns: ["Data-quality findings", "Affected fields"]
  tools: ["CSV/spreadsheet parser"]
  uncertainty: keep page, file, row, log, or source anchors when available
```

## Response shape

The handoff is usually a compact artifact rather than a long essay. Include data-quality findings, affected fields, severity, and fix/check when those pieces are supported by the source material. If a requested field cannot be found, mark it as missing instead of inventing it.

Typical return blocks:

- Data-quality findings
- Affected fields
- Severity
- Fix/check

## Common mistakes

Not for ranking options, executive storytelling, or root-cause explanation unless trust is established. Nearby skills in this cluster include `psc-anomaly-watchlist-builder`, `psc-decision-ranking-analyst`, `psc-executive-metric-narrator`. They may share nouns with this skill, so route by the requested artifact and the work sequence, not by the domain word alone.

A common routing mistake is to select by a shared noun in the prompt and miss the user's requested output. Prefer the skill whose procedure would actually produce the requested handoff.

## Environment notes

This workflow can be carried out with csv/spreadsheet parser. Equivalent tools are fine, but they must preserve the same inspection or verification standard. Keep anchors such as filenames, pages, rows, source snippets, log lines, screenshots, or model/dataset identifiers when they are available.

Useful source clues, in rough order: Spreadsheet/CSV. Expected fields or assumptions. Need for quality checks.

## Example prompts

- Before we make a decision from this weekly channel CSV, check whether the data is trustworthy: missing values, duplicate rows, invalid ranges, and schema issues.
- Audit the spreadsheet's data quality and assumptions. I need trustworthiness checks, not a ranking recommendation or executive summary.

Less ideal but still valid request: "Can you look at this and tell me what should happen next?" In that case, first decide whether the user wants data-quality findings or a neighbouring artifact, then ask one clarifying question if needed.

## Validation

- The response clearly produces data-quality findings.
- The answer explains uncertainty instead of silently guessing.
- The chosen process matches the user's artifact and requested outcome.
- Secondary outputs are included only when they support the requested result.

Before finishing, compare the answer against the nearby-skill boundary above. If the output would be more naturally produced by another skill, say so and switch rather than stretching this workflow.
