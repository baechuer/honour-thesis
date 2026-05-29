# Metrics Root Cause Diagnoser Examples

## Example 1

User ask:

`What looks like the likely cause of this regression?`

Example output:

- Main symptom: Tail latency and error rate rose together while traffic stayed roughly flat.
- Likely cause or causes: A degraded downstream dependency or exhausted worker pool is the leading explanation.
- Supporting signals: Queue depth and timeout-related errors increased at the same time as p99 latency.
- Contradicting or missing signals: CPU is not saturated, so a pure compute bottleneck looks less likely.
- Next checks: Verify dependency latency, timeout distribution, and whether one endpoint or shard is overrepresented.

## Example 2

User ask:

`Give me a root-cause style read of these metrics.`

Example output:

- Main symptom: Throughput flattened while utilization and queueing rose sharply.
- Likely cause or causes: The service appears constrained by saturation rather than low demand.
- Supporting signals: Requests in flight increased, queue depth rose, and tail latency worsened without a traffic surge.
- Contradicting or missing signals: Without dependency metrics, it is unclear whether the bottleneck is internal or downstream.
- Next checks: Compare worker saturation, autoscaling behavior, and downstream response times.
