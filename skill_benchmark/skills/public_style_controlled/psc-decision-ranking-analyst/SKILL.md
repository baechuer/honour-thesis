---
name: psc-decision-ranking-analyst
description: "Spreadsheet analysis workflow involving CSV data, metrics, data quality, anomalies, decision ranking, reporting, and business interpretation. Rank options for action using criteria, tradeoffs, evidence, constraints, and recommendation confidence."
metadata:
  source_style: public_style_controlled
  cluster_id: psc_data_analysis_intent
---

# Decision Ranking Analyst

This is a public-style controlled skill used for retrieval evaluation. It is written as a practical capability note rather than a neat benchmark schema.

Cluster intent: Same spreadsheet or dataset, different analytical intent: trust audit, anomaly watchlist, decision ranking, or executive narrative.

## When to use

Use when the dataset represents alternatives and the output should choose or rank options.

## Requirements

- Candidate options
- Decision criteria
- Constraints and tradeoffs

## Instructions

- Define criteria.
- Score and compare options.
- Explain tradeoffs and uncertainty.
- Recommend first action.

## Deliverables

- Ranked options
- Criteria
- Recommendation
- Tradeoffs

## When not to use

Not for general data quality checks or anomaly detection unless those affect the decision.

## External dependencies to preserve

- Option table or decision matrix

## Example use

A good request names the artifact or situation, gives enough operational context to choose this capability, and asks for the deliverable above.
