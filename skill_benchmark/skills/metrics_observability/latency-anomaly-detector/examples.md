# Latency Anomaly Detector Examples

## Example 1

User ask:

`Does this latency graph look abnormal?`

Example output:

- Observed anomaly: Yes, there is a sustained tail-latency regression rather than a brief spike.
- Evidence: p95 and p99 rise sharply for more than 20 minutes while median latency moves only slightly.
- Scope or affected segment: The issue appears concentrated in slower requests rather than the full request population.
- Operational concern: This pattern often points to queueing, retries, or a degraded dependency.
- Confidence or uncertainty: Moderate confidence because the baseline before the shift is visible, but endpoint-level detail is missing.

## Example 2

User ask:

`Tell me if anything weird is happening with latency here.`

Example output:

- Observed anomaly: There is a short-lived spike, but not yet a sustained regression.
- Evidence: Latency jumps briefly and then returns close to baseline within the same window.
- Scope or affected segment: The spike affects both average and tail latency, suggesting a broader transient disturbance.
- Operational concern: Worth watching, but this does not yet look like a persistent degradation.
- Confidence or uncertainty: Medium confidence because the recovery is visible in the chart.
