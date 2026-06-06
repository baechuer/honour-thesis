---
name: grafana-dashboard-builder
description: "Builds Grafana dashboard structure with panels, variables, queries, thresholds, and operator-facing layout."
---

# Grafana Dashboard Builder

Creates observability dashboards for scanning service health.

## Use when

- The user wants a dashboard or panel layout.
- Queries, variables, thresholds, and visual grouping matter.

## Not for

- Writing alert rules only.
- Diagnosing one trace.
- Writing post-incident narrative.

## Preconditions

- Metrics and dashboard audience are known.
- Panel grouping or service scope is specified.

## Workflow

1. Identify dashboard purpose and variables.
2. Design panels and queries.
3. Set thresholds and legends.
4. Return dashboard plan or JSON outline.

## Writing rules

- Do not overload dashboards with every metric.
- Prioritize operator scanability.

## Default shape

- Dashboard sections
- Panels/queries
- Thresholds
- Notes
