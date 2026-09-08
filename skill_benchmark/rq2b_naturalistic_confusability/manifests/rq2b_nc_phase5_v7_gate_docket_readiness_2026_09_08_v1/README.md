# V7 gate-docket readiness

Reproduce with:

```sh
python3 skill_benchmark/scripts/materialise_rq2b_nc_phase5_v7_gate_docket_readiness.py
```

The script refuses to overwrite a frozen package and verifies the source docket, U0323 method-gate note, and U0527 reissue validation states. It contains no target identity, gold, retrieval outcome, acceptable-set, library outcome, or K change.
