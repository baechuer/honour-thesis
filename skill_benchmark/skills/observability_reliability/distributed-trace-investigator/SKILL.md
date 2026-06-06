---
name: distributed-trace-investigator
description: "Investigates distributed traces to locate latency, retries, failing spans, dependency calls, and propagation gaps."
---

# Distributed Trace Investigator

Uses trace spans to explain a request path problem.

## Use when

- The user provides trace spans or tracing output.
- The task is to locate latency or failure across services.

## Not for

- Building dashboards.
- Writing alerts.
- Reviewing resilience code without trace evidence.

## Preconditions

- Trace spans or service timing data are available.
- The target request or symptom is known.

## Workflow

1. Read trace hierarchy and critical path.
2. Identify slow or failing spans.
3. Connect spans to dependencies.
4. Return diagnosis and missing instrumentation.

## Writing rules

- Do not infer causality from one span without caveat.
- Keep timing evidence visible.

## Default shape

- Trace path
- Bottleneck/failure
- Evidence
- Next check
