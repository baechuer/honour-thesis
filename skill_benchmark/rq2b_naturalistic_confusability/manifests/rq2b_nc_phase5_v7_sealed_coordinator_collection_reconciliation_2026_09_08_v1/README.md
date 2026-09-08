# V7 sealed coordinator collection reconciliation

Reproduce with:

```sh
python3 skill_benchmark/scripts/verify_rq2b_nc_phase5_v7_sealed_coordinator_returns.py
python3 skill_benchmark/scripts/reconcile_rq2b_nc_phase5_v7_sealed_coordinator_collection.py
```

The second command refuses to overwrite this frozen package. It validates every return first, then writes only opaque collection states. It does not perform a target join, finalise a group, create acceptable sets, or update the library.
