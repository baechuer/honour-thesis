---
name: prometheus-alert-rule-writer
description: "Writes Prometheus alert rules from SLOs, metric names, thresholds, windows, labels, and severity policies."
---

# Prometheus Alert Rule Writer

Produces alerting rules rather than dashboards or incident summaries.

## Use when

- The user has SLOs or metric thresholds.
- They need alert expressions, labels, and routing severity.

## Not for

- Building Grafana dashboards.
- Diagnosing traces.
- Writing an incident narrative.

## Preconditions

- Metric names and SLO thresholds are known.
- Alert windows and severity rules are available or can be proposed.

## Workflow

1. Map SLO to metric expression.
2. Choose burn-rate/window strategy.
3. Write alert rule and labels.
4. Add verification query.

## Writing rules

- Do not invent metric names without marking assumptions.
- Avoid noisy alerts without window logic.

## Default shape

- Alert rule
- Labels/severity
- Verification
- Noise risk
