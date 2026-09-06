# Machine A Reviewer-B binding gate — V7

The V7 frozen validator rejected two newly collected Reviewer-B returns with the identical error: `V7 return identity or cryptographic binding drift`. The affected groups are `RQ2B-P4-V7-U0979` and `RQ2B-P4-V7-U1078`.

For both returns, the reviewer identifier and batch identifier matched, while the blind-packet identifier, packet-input hash, instruction hash, and output hash did not. Their Reviewer-A returns separately pass the frozen target-blind validator. The two invalid Reviewer-B payloads are preserved under `reviewer_B/superseded_invalid/` with immutable hashes and traceable-reissue records; they are not reconciliation evidence.

This is a frozen-method gate, not a judgement disagreement. No coordinator or finalisation was run for either group, no finalised group was changed, and no new Machine-A group may be dispatched until a frozen-SOP disposition decides whether and how a traceable Reviewer-B reissue can occur.

The authoritative counts remain those in `execution_state_reconciliation.json`: 447 `FINALISED`, 2 `STARTED_INCOMPLETE`, and 777 `UNSTARTED`.
