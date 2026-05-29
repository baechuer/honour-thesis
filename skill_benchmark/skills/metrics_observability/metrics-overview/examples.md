# Metrics Overview Examples

## Example 1

User ask:

`Give me a quick read on this service dashboard.`

Example output:

- Overall state: The service looks degraded but not fully unstable.
- Notable signals: Request volume is steady, p95 latency is rising, and error rate is elevated but not catastrophic.
- Main concern or watch area: Tail latency is worsening faster than the average, suggesting a localized bottleneck or overloaded dependency.
- Immediate priority or open question: Check whether the latency increase is isolated to one endpoint, shard, or downstream dependency.

## Example 2

User ask:

`Summarise what matters from these metrics.`

Example output:

- Overall state: Most indicators are stable, but capacity pressure is building.
- Notable signals: CPU and queue depth are climbing together while throughput stays flat.
- Main concern or watch area: The system may be approaching a saturation point even though user-facing errors remain low.
- Immediate priority or open question: Confirm whether this load pattern is normal for the time window or whether headroom is shrinking unusually fast.
