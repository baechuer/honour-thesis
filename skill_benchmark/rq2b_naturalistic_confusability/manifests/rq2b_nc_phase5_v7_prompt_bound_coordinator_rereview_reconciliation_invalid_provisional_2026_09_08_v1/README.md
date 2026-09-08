# RQ2b-NC target-blind prompt-bound reconciliation

Reproduce with:

```sh
python3 skill_benchmark/scripts/verify_rq2b_nc_phase5_v7_prompt_bound_coordinator_rereview.py
python3 skill_benchmark/scripts/reconcile_rq2b_nc_phase5_v7_prompt_bound_coordinator_rereview.py
```

The reconciliation refuses to run unless all 2,291 prompt-bound returns validate. It then combines only exact A/B agreements and valid prompt-bound coordinator decisions using opaque packet IDs. It does not open a target join or derive acceptable-set/library outcomes.
