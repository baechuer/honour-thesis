# Capacity Risk Forecaster Examples

## Example 1

User ask:

`Do these metrics suggest we are heading toward capacity trouble?`

Example output:

- Capacity risk level: Medium and rising.
- Leading signals: CPU, concurrency, and queue depth are climbing together while throughput has flattened.
- Likely bottleneck or constraint: The service may be saturating a worker pool or downstream dependency rather than scaling linearly with demand.
- What to watch next: Check whether queue depth continues to grow and whether latency begins rising alongside utilization.

## Example 2

User ask:

`How worried should I be about headroom here?`

Example output:

- Capacity risk level: High in the near term.
- Leading signals: Memory is close to its usual ceiling and tail latency is already drifting upward under steady traffic.
- Likely bottleneck or constraint: The system appears close to a saturation threshold where small traffic increases could trigger broader degradation.
- What to watch next: Confirm whether autoscaling, worker counts, or dependency limits are preventing additional headroom.
