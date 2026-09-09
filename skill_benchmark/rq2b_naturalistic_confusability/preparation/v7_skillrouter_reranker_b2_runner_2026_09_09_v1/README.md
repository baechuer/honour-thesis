# V7 SkillRouter reranker B2 runner v1

Status: `IMPLEMENTED_ZERO_INFERENCE_AWAITING_PHASE8_B1_PAYLOAD_AND_ROOT_RELEASE`.

The runner implements the SkillRouter B2 branch for 15 materialised
conditions: B01-GS through B12-GS plus C1-S, C3-S and C4-S, each covering all
1,077 frozen queries. C2-S is the exact B05-GS alias and is deliberately not
materialised. This implementation task did not load a model, make a forward
pass, access a network, or read labels, acceptable sets, metrics or retrieval
results.

## Closed intake and execution gates

Execution has exactly one scientific-data intake: a later
`rq2b-v7-skillrouter-reranker-b2-phase8-payload-v1` payload named and
hash-bound by a one-use
`rq2b-v7-skillrouter-reranker-b2-root-release-v1` record. The payload must
bind:

- the frozen label-free query runtime, source manifest, core conditions and
  fixed-candidate bridge manifest;
- the authoritative Phase-7 v2 I1/I2 artifacts and final Phase-8 V4.1
  I3C-fielded/I3-flat artifacts;
- one or more immutable B1 output artifacts containing the complete 12 x
  1,077 Top-100 rows; and
- a persisted PASS receipt from the official label-free output validator for
  those 12 B1 cells.

Final I3 paths and hashes are intentionally absent from the runner. They must
arrive in the later payload with
`extraction_protocol=I3C_SUBAGENT_EXTRACTION_V4_1`, `phase8_final=true`, a
PASS Phase-8 receipt, and exact artifact SHA-256 values. The runner will not
guess or substitute them. The root release binds that payload SHA, the Phase-8
receipt SHA and B1 validation-receipt SHA before local model imports occur.

## Scientific method contract

- model `pipizhao/SkillRouter-Reranker-0.6B`, revision
  `78986e1142d12857cfd85b8005e62902cd42d858`, with every local snapshot file
  checked against the runtime-preflight SHA-256 manifest;
- released system/instruction/query/document/assistant prompt contract with
  score `final_token_yes_logit - final_token_no_logit`;
- 2,048-token pair contract, 16-token safety reserve, complete lossless
  query-specific document windows, 128-token source overlap, and maximum
  window score per candidate;
- exact model-input-token-length buckets, no padding, MPS bfloat16 default
  SDPA, batch size at most 16, local-files-only loading, no silent device or
  dtype fallback and no automatic retries;
- exact scores retained, descending score order, and ascending
  `source_sha256` deterministic tie-break;
- each official `rq2b-v7-b2-runner-output-v1` row is an exact permutation of
  the already persisted B1 Top-20 and binds both the B1 Top-20 SHA and the
  representation-specific candidate-view SHAs.

The CPU float32 sensitivity branch is planned but not executed by the primary
run. Its deterministic hook selects eight pairs per representation under the
sealed namespace and writes a pending plan/receipt for a later, separately
authorised CPU eager comparison.

## Failure, cache and cost evidence

Each model forward has started/completed receipts. Scores use immutable cache
entries bound to the exact model, prompt, runtime, window and token-ID hashes.
The completed package includes B2 rows, an exact-tie ledger, cache inventory,
CPU sensitivity plan/pending receipt, and cost ledger. Cost fields distinguish
logical candidate pairs/windows, unique pairs, cache hits, new tokens,
forward batches, model-load/forward/aggregation/wall time, retries, failures,
network/provider calls and monetary cost. A failure keeps the unique attempt
directory and any staging/cache state, writes `run_failed.json`, performs no
retry, and never publishes a completed output directory.

## Zero-inference checks

From the clean repository root:

```sh
.venv-rq2b-v7/bin/python -B skill_benchmark/scripts/run_rq2b_v7_skillrouter_reranker_b2.py --self-test
.venv-rq2b-v7/bin/python -B skill_benchmark/scripts/test_rq2b_v7_skillrouter_reranker_b2.py
PYTHONPYCACHEPREFIX=/private/tmp/rq2b-skillrouter-b2-pycache .venv-rq2b-v7/bin/python -B -m py_compile skill_benchmark/scripts/run_rq2b_v7_skillrouter_reranker_b2.py skill_benchmark/scripts/test_rq2b_v7_skillrouter_reranker_b2.py
git diff --check
```

Only after the final Phase-8 payload, complete persisted B1 outputs, official
B1 validation receipt, pinned local model snapshot and one-use root release
exist is execution syntactically available:

```sh
.venv-rq2b-v7/bin/python -B skill_benchmark/scripts/run_rq2b_v7_skillrouter_reranker_b2.py \
  --execute --authorisation path/to/one_use_root_release.json
```

Do not run that command during implementation. After a future scientific run,
the emitted B2 gzip should be validated together with the exact persisted B1
artifacts by `validate_rq2b_v7_runner_outputs.py --allow-incomplete`. The
official validator's complete 30-condition mode applies only after the other
15 B2 reranker conditions are joined.
