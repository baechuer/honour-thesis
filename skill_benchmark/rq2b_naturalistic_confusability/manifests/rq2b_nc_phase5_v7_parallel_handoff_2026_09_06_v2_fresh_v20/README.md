# RQ2B V7 Phase-5 current two-machine handoff

This is an append-only dispatch package for the historical **V7 unified
dispatch package**. It is not the newer 528-group package, and it neither
creates results nor reads adequacy outcomes, target joins, retrieval,
reranking, provider outputs, or metrics.

## Frozen scope and current state

- V7 has `1226` prompt groups.
- This package is bound to `skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_phase5_execution_state_reconciliation_2026_09_06_v20_v7_dispatch_freshness_replay/execution_state_reconciliation.json`.
- `160` `FINALISED` groups are locked and omitted.
- `1` `STARTED_INCOMPLETE`
  group is retained as a traceable reissue: preserve its existing return(s),
  validate them, and issue only a missing or invalid reviewer role.
- `1065` `UNSTARTED` groups are issued.
- The `1066` pending groups are SHA-256 ordered by
  `batch_id`; Machine A owns ranks 1--533 and Machine B owns
  the remainder (533).

A group is indivisible: one prompt, six sealed main candidates, and two sealed
tail candidates. Reviewer-facing packets deliberately hide main/tail role,
target identity, labels, ranks, paths, provenance, peer returns, and outcomes.

## Deferred successor boundary

The newer 528-group current package is deferred. Do not mix its packets,
candidate tokens, returns, labels, outcomes, or reconciliation artifacts with
this V7 audit. This audit's completed groups count only toward V7 execution
completion; they do not establish whole-library closure, strict-gold closure,
retrieval performance, or coverage of deferred additions.

## Two-computer launch

Both machines first clone the same commit containing this directory, then use
their own review branch.

Machine A:

```bash
git switch -c codex/rq2b-v7-review-machine-a
python3 skill_benchmark/scripts/materialize_rq2b_nc_phase5_v7_parallel_handoff_2026_09_06_v2.py verify --state-file skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_phase5_execution_state_reconciliation_2026_09_06_v20_v7_dispatch_freshness_replay/execution_state_reconciliation.json --output-dir skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_phase5_v7_parallel_handoff_2026_09_06_v2_fresh_v20
# Review only: skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_phase5_v7_parallel_handoff_2026_09_06_v2_fresh_v20/machine_a_manifest.jsonl
```

Machine B:

```bash
git switch -c codex/rq2b-v7-review-machine-b
python3 skill_benchmark/scripts/materialize_rq2b_nc_phase5_v7_parallel_handoff_2026_09_06_v2.py verify --state-file skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_phase5_execution_state_reconciliation_2026_09_06_v20_v7_dispatch_freshness_replay/execution_state_reconciliation.json --output-dir skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_phase5_v7_parallel_handoff_2026_09_06_v2_fresh_v20
# Review only: skill_benchmark/rq2b_naturalistic_confusability/manifests/rq2b_nc_phase5_v7_parallel_handoff_2026_09_06_v2_fresh_v20/machine_b_manifest.jsonl
```

For each owned group, create two separate **target-blind** reviewer returns,
one for role A and one for role B. Machine ownership is workload partitioning,
not a substitute for independent A/B review. Keep A and B sealed from one
another. Send disagreements only to the sealed coordinator. Never overwrite an
existing canonical return; write traceable reissues as new files/records under
the V7 return contract.

Before every commit, rerun this verifier, the frozen V7 return validator for
each changed reviewer file, and a fresh execution-state reconciliation. Merge
is blocked unless packet/input hashes, schema, target blindness, complete A/B
coverage, machine disjointness, and pending-scope coverage pass.

## Files

- `current_phase5_pending_assignment_v1.jsonl`: administrative assignment
  ledger; it is not reviewer input.
- `machine_a_manifest.jsonl`, `machine_b_manifest.jsonl`: complete,
  role-hidden packets owned by exactly one machine.
- `reviewer_return_schema.json`: frozen V7 independent-return schema.
- `integrity_report.json` / `.md`: hash-bound state, counts, and checks.
- `V7_SCOPE_AMENDMENT.md`: the operative-scope and deferred-successor boundary.
