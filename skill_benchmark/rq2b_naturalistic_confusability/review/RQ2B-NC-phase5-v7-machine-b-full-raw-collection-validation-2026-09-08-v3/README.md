# V7 Machine B full raw-collection validation

Replay with:

```sh
python3 skill_benchmark/scripts/verify_rq2b_nc_phase5_v7_machine_b_raw_collection.py
```

The verifier writes a new report only when all 533 Machine-B groups have two frozen-validator-passing raw returns except the retained, previously documented `RQ2B-P4-V7-U0527` A/B source-anchor failures. This is not a reconciliation or an acceptable-set result.
