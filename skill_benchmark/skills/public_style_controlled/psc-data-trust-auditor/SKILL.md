---
name: psc-data-trust-auditor
description: "Spreadsheet analysis workflow involving CSV data, metrics, data quality, anomalies, decision ranking, reporting, and business interpretation. Audit whether tabular data is trustworthy by checking missing values, duplicates, invalid ranges, schema drift, and calculation assumptions."
metadata:
  source_style: public_style_controlled
  cluster_id: psc_data_analysis_intent
---

# Data Trust Auditor

This is a public-style controlled skill used for retrieval evaluation. It is written as a practical capability note rather than a neat benchmark schema.

Cluster intent: Same spreadsheet or dataset, different analytical intent: trust audit, anomaly watchlist, decision ranking, or executive narrative.

## When to use

Use before acting on a dataset when the user asks whether the numbers can be trusted.

## Requirements

- Spreadsheet/CSV
- Expected fields or assumptions
- Need for quality checks

## Instructions

- Check missingness, duplicates, invalid values, and schema drift.
- Flag formula or aggregation assumptions.
- Return trust verdict and fixes.

## Deliverables

- Data-quality findings
- Affected fields
- Severity
- Fix/check

## When not to use

Not for ranking options, executive storytelling, or root-cause explanation unless trust is established.

## External dependencies to preserve

- CSV/spreadsheet parser

## Example use

A good request names the artifact or situation, gives enough operational context to choose this capability, and asks for the deliverable above.
