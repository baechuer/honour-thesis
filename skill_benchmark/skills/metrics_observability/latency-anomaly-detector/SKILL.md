---
name: latency-anomaly-detector
description: Identifies unusual latency behavior from metrics, charts, or service observations, including spikes, shifts, and tail regressions.
---

# Latency Anomaly Detector

Identifies unusual latency behavior from metrics or dashboard evidence.

## Use when

- The user wants to know whether latency behavior looks abnormal.
- The input includes p50, p95, p99, duration charts, endpoint latency, or similar performance indicators.
- The output should focus on anomaly shape, scope, and operational significance rather than causal driver attribution.

## Not for

- Providing only a broad service-health overview.
- Explaining definitive root cause.
- Comparing competing cause hypotheses or selecting the most plausible degradation driver.
- Checking formal SLO compliance.
- Writing incident communication.

## Preconditions

- The user provides service metrics, dashboard values, incident notes, or operational observations.
- The user indicates whether they need current-state summary, anomaly detection, SLO judgment, forecast, root cause, or incident communication.

## Workflow

1. Identify which latency signals are available and what time window they cover.
2. Compare the observed behavior to the implied baseline in the snapshot.
3. Distinguish brief spikes, sustained shifts, and tail-only regressions.
4. Note where the anomaly appears to be concentrated if the input supports that.
5. Return a compact anomaly-focused assessment.

## Writing rules

- Focus on whether the behavior looks unusual, not just whether latency is high.
- Make the anomaly shape explicit when possible.
- Distinguish broad latency movement from tail-only movement.
- Preserve uncertainty when the baseline is weak or missing.
- Return only the anomaly assessment unless the user asks for more.

## Output pattern

Use this shape unless the user asks for something else:

- Observed anomaly
- Evidence
- Scope or affected segment
- Operational concern
- Confidence or uncertainty

For worked examples, see `examples.md`.
