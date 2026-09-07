# RQ2b-NC V7 mechanical integration intake

This is a frozen pointer-and-hash intake package for the two supplied machine commits. It is not a merged raw-return tree and does not alter canonical raw returns. The intake ledger selects at most one validator-passing active return per lane; all reissues are selected by source path and SHA.

## Exact replay

```sh
python3 skill_benchmark/scripts/integrate_rq2b_nc_phase5_v7_mechanical_intake.py \
  --source-machine-a 71fb10eb297f4a9c5ae8d8bb4bec8dc8b955a0d8 \
  --source-machine-b ab7ea5a5a72d22c2e06fcdbcad2d2a0d70b0cbee \
  --validator-render-cache /private/tmp/rq2b-v7-mechanical-replay-cache \
  --materialise-validator-render-cache \
  --output /private/tmp/rq2b-v7-mechanical-integration-replay
```

The command materialises source-visible but target-blind validator renders only in `/private/tmp`; they are replay cache, not intake evidence, and must not be committed. It must run in a clone containing both source commits and the frozen V7 protocol.

## Stop boundary

Do not execute either routing queue until the gate docket has explicit approval. In particular, `READY_FOR_RECONCILIATION` is not `FINALISED`. This package contains no target identity, gold label, retrieval outcome, acceptable set, or library update.
