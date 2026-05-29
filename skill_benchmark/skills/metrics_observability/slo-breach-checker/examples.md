# SLO Breach Checker Examples

## Example 1

User ask:

`Check whether this service looks like it is breaching its SLO.`

Example output:

- SLO status: At risk, but not enough evidence here to call a confirmed breach.
- Supporting evidence: Error rate is elevated and burn rate appears above normal for the current window.
- Risk level: Medium to high if the condition persists.
- What to verify next: Confirm the exact SLO target and whether the current window is representative enough to judge error-budget consumption.

## Example 2

User ask:

`Is this still inside the reliability target or not?`

Example output:

- SLO status: Likely breached in the current window.
- Supporting evidence: Availability is below the stated target and the failure rate remains elevated throughout the chart.
- Risk level: High.
- What to verify next: Check whether the issue is localized to one dependency or endpoint and whether mitigation has already reduced the burn rate.
