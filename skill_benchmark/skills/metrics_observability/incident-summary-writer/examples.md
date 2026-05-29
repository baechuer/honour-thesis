# Incident Summary Writer Examples

## Example 1

User ask:

`Write a short incident summary from these notes and metrics.`

Example output:

- Incident overview: The service experienced a period of degraded performance driven by rising tail latency and elevated error rate.
- Customer or system impact: A subset of requests timed out and users saw slower responses during the incident window.
- Key timeline points: Latency began rising first, queue depth increased shortly afterward, and mitigation reduced the error rate within the hour.
- Current status: The system is recovering, but tail latency remains above baseline.
- Next actions or open issues: Confirm the underlying bottleneck and decide whether further capacity or dependency mitigation is needed.

## Example 2

User ask:

`Turn this into something I can send as an incident update.`

Example output:

- Incident overview: We observed a reliability degradation affecting multi-step request handling.
- Customer or system impact: Error rate increased and long-running requests were the most affected.
- Key timeline points: The issue emerged under steady traffic, peaked as queueing worsened, and partially improved after mitigation.
- Current status: Core service availability has improved, but investigation is ongoing.
- Next actions or open issues: Validate the root cause, confirm scope, and monitor for recurrence.
