# RQ2B V7 Phase-5 two-machine handoff freeze

This directory is a dispatch artifact, not an experiment, result, acceptable-set
decision, or reconciliation output. It is frozen from the V7 unified manifest
and the official execution-state reconciliation.

## Scope

- 147 `FINALISED` groups are locked and deliberately absent.
- `RQ2B-P4-V7-U0077` is a traceable reissue: its existing return remains in
  the canonical return directory and must be revalidated rather than replaced.
- The remaining 1,078 `UNSTARTED` groups are newly issued.
- Pending `batch_id`s are ordered by `SHA-256(batch_id)`; ranks 1--540 are
  `machine_a`, ranks 541--1,079 are `machine_b`.
- A group is indivisible: one prompt, six sealed main candidates, and two
  sealed tail candidates. The reviewer-facing packet intentionally hides
  main/tail role, target identity, labels, ranks, paths, provenance and all
  outcomes.

### State-snapshot freshness gate

This handoff is intentionally bound to the named V14 execution-state snapshot,
not to a count inferred from files in a reviewer directory. Before anyone
begins dispatch, rerun the execution-state reconciler. If its replay differs
from the V14 snapshot, stop and create a new state-pinned handoff rather than
reviewing any group whose current state may have changed.

## Two-computer procedure

1. Both computers clone the same frozen commit containing this directory.
2. Machine A reads only `machine_a_manifest.jsonl`; machine B reads only
   `machine_b_manifest.jsonl`. Do not redistribute a group between machines.
3. For every assigned group, create two **independent, target-blind** returns:
   one for reviewer role `A` and one for reviewer role `B`. Machine ownership
   is workload partitioning; it is not a substitute for the two reviewers.
4. Keep reviewer A and B work sealed from each other until submission. Each
   reviewer reads only the assigned role-hidden packet and the frozen V7 return
   schema in `reviewer_return_schema.json`.
5. Write returns on separate branches and directories:
   - `codex/rq2b-v7-review-machine-a`
   - `codex/rq2b-v7-review-machine-b`
   Canonical integration locations remain
   `.../review/RQ2B-NC-phase4-v7-strict-unified-independent-returns-2026-09-05/reviewer_A/`
   and `reviewer_B/`; never overwrite an existing return. For U0077, first
   validate the preserved A return under the V7 contract, then issue only the
   missing or invalid role as a separate traceable reissue.
6. Before merge, rerun this handoff verifier plus the frozen V7 return
   validator/reconciliation contract. Merge is blocked unless coverage,
   machine disjointness, packet hashes, schema, and two-return coverage all
   pass.

## Files

- `phase5_v7_pending_assignment_v1.jsonl`: administrative provenance and
  assignment ledger; it is not reviewer input.
- `machine_a_manifest.jsonl`, `machine_b_manifest.jsonl`: role-hidden,
  complete eight-candidate packets owned by exactly one machine.
- `integrity_report.json` / `.md`: frozen inputs, counts, and replay checks.

Do not inspect V7 allocation, token joins, targets, historical gold, peer
returns, reconciliation material, retrieval/reranking/provider outputs, or
metrics while reviewing.
