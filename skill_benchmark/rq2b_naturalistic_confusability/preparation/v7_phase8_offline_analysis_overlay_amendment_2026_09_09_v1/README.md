# RQ2b-NC V7 Phase-8 offline-analysis overlay amendment v1

Status: `PRE_OUTCOME_PROSPECTIVE_ANALYSIS_AMENDMENT_PASS`.

This package fixes the Phase-8 quality-closure overlays before any selector
outcome is scored. It amends the offline scoring interpretation only. It does
not alter the frozen 1,077 prompts, 3,798 sources, label rows, D_q review rows,
retrieval inputs, conditions, or outputs.

Three hash-bound overlays are active:

- 25 source-equivalence edges are closed transitively. If a frozen acceptable
  member belongs to an equivalence component, every member of that component
  receives acceptable credit in the offline scorer. Any newly acceptable
  member is removed from effective D_q and from the effective unjudged set.
  The frozen label ledger remains unchanged.
- 41 byte-frozen avoidable-identity-cue prompts are marked
  `identity_cue_sensitivity`. They are excluded from primary inference and
  reported separately.
- Three prompt-dependency edges are replayed. Their three endpoints already
  share frozen dependency group `D-E49C16FF6B945B5F`; the scorer fails closed
  if an edge crosses dependency components.

The observed pre-outcome cue distribution matters. All 41 cue prompts are in
the parent-delta lane; none is in `B_NC_FULL_UNION`. Therefore P1-P5 preserve
the approved 714-prompt NC primary estimand (with an explicit cue exclusion
that is currently a no-op). The 1,036-prompt all-library no-cue population is
added as descriptive/sensitivity output, not substituted for the NC primary
estimand. The 322 no-cue parent-delta prompts remain a separate diagnostic,
and the 41 cue parent prompts are a sensitivity-only scope.

The source-equivalence overlay expands eight prompts. Four formerly singleton
effective labels become acceptable sets, yielding 877 effective `STRICT` and
200 effective `ACCEPTABLE_SET` prompts. These are scoring-time identities only;
the frozen source library and label rows are not rewritten.

Exact verification:

```sh
python3 -B skill_benchmark/scripts/test_rq2b_v7_offline_analysis_contract.py
PYTHONPATH=skill_benchmark/scripts python3 -B -c 'from analyse_rq2b_v7_offline_outputs import OfflineAuthority; OfflineAuthority.load(); print("PASS")'
git diff --check
```

No result was read, generated, or used to choose this amendment.
