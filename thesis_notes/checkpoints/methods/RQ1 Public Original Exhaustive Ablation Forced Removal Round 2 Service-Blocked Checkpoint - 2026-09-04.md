# RQ1 Public-Original Exhaustive Ablation: Forced-Removal Round 2 Service-Blocked Checkpoint

Date: 2026-09-04

## Scope

This is a progress and service-state checkpoint, not an experimental result or
scoring approval. Round 2 starts from the immutable Round-1 masks and deletes
every exact residual span cited in the canonical Round-1 ledger. A damaged or
non-executable edited skill is allowed here because the intervention tests
routing information rather than executability.

## Verified Round-2 Clearance So Far

The parent validator and canonical ledger now cover `OR82-001` through
`OR82-070` inclusively:

| Measure | Count |
|---|---:|
| Canonical field units | 490 / 574 |
| Canonical compositions | 70 / 82 |
| Reviewed candidate cards | 1,589 / 1,855 |
| `CLEAR` candidate decisions | 1,229 |
| `RESIDUAL` candidate decisions | 358 |
| `UNCERTAIN` candidate decisions | 2 |
| Units with every candidate `CLEAR` | 312 |

Every canonical JSON submission parsed, had exact candidate identity coverage,
used the prescribed `status` and `residual_spans` schema, and passed exact
quote-to-current-card validation. The SOP was amended before continued review
to make the JSON field names and evidence rules explicit.

One completed batch, `OR82-068` through `OR82-070`, initially used a truncated
composition id in its `unit_id` field. Its original blind reviewer corrected
only that mechanical identity field; it did not change statuses, evidence,
rationales, candidate labels, or target fields. The parent validator then
passed all 21 corrected records before canonical ingestion.

## Unreviewed Scope and Blocker

The remaining 84 field units / 266 candidate cards are exactly
`OR82-071` through `OR82-082`. They have no clearance disposition by
inference and are not part of any future score denominator.

Fresh-reviewer startup became unavailable on 2026-09-04. Multiple independent
agent-launch attempts, including a no-history launch, failed before packet
access with the same platform error: `404 Not Found` from the Codex responses
backend. Failed agents were closed; they read no packet and wrote no output.
The main thread must not substitute for the fresh blind reviewer because it
knows prior Round-1/Round-2 state.

## Interpretation Boundary

These counts establish only partial fresh clearance. They do not authorise
BM25, Qwen, external APIs, hosted work, selector metrics, or thesis/PDF result
writing. `RESIDUAL` and `UNCERTAIN` records remain evidence for a future
Round-3 deletion design; they are not discarded.

## Resume Order

1. Confirm fresh-reviewer service is available with one unassigned missing
   composition.
2. Complete anonymous clearance for `OR82-071` through `OR82-082`, validating
   and canonicalising every unit before closing its reviewer.
3. Only after 574/574 coverage, create the Round-3 deletion plan from every
   canonical Round-2 residual span and perform another fresh clearance.

Authoritative SOP:
`skill_benchmark/rq1_public_original_exhaustive_ablation_v1/FORCED_REMOVAL_ROUND2_SOP.md`.
