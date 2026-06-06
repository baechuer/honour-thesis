---
name: psc-anomaly-watchlist-builder
description: "Spreadsheet analysis workflow involving CSV data, metrics, data quality, anomalies, decision ranking, reporting, and business interpretation. Find unusual spikes, drops, outliers, concentration, and abrupt changes in tabular metrics for follow-up investigation."
metadata:
  source_style: public_style_controlled
  cluster_id: psc_data_analysis_intent
---

# Anomaly Watchlist Builder

This is a public-style controlled skill used for retrieval evaluation. It is written as a practical capability note rather than a neat benchmark schema.

Cluster intent: Same spreadsheet or dataset, different analytical intent: trust audit, anomaly watchlist, decision ranking, or executive narrative.

## When to use

Use when the task is to identify what looks unusual rather than explain the final cause.

## Requirements

- Time series or metric table
- Baseline or comparison window
- Need for follow-up prioritization

## Instructions

- Compare current values to baseline.
- Flag spikes, dips, outliers, and concentration.
- Rank anomalies by severity and confidence.

## Deliverables

- Anomaly watchlist
- Evidence metric/window
- Priority
- Next check

## When not to use

Not for data trust auditing, forecasting, or final executive narrative.

## External dependencies to preserve

- Tabular metrics

## Example use

A good request names the artifact or situation, gives enough operational context to choose this capability, and asks for the deliverable above.
