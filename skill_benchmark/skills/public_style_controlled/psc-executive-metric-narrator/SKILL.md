---
name: psc-executive-metric-narrator
description: "Spreadsheet analysis workflow involving CSV data, metrics, data quality, anomalies, decision ranking, reporting, and business interpretation. Turn tabular metrics into an upward-facing executive brief with headline, key takeaways, risks, and recommended next steps."
metadata:
  source_style: public_style_controlled
  cluster_id: psc_data_analysis_intent
---

# Executive Metric Narrator

This is a public-style controlled skill used for retrieval evaluation. It is written as a practical capability note rather than a neat benchmark schema.

Cluster intent: Same spreadsheet or dataset, different analytical intent: trust audit, anomaly watchlist, decision ranking, or executive narrative.

## When to use

Use when the audience is leadership and the requested output is communication, not exploration.

## Requirements

- Metric table
- Business audience
- Need for concise takeaway narrative

## Instructions

- Identify headline and key movements.
- Translate metrics into business implications.
- List risks and recommended next steps.

## Deliverables

- Executive headline
- Key takeaways
- Risks
- Recommended actions

## When not to use

Not for deep anomaly scanning, data-quality auditing, or option ranking unless requested.

## External dependencies to preserve

- Metric summary or spreadsheet

## Example use

A good request names the artifact or situation, gives enough operational context to choose this capability, and asks for the deliverable above.
