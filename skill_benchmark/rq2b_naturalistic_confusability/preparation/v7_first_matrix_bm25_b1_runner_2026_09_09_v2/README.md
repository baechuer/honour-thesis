# V7 first-matrix BM25 B1 runner v2

Status: `IMPLEMENTED_NO_EXECUTION_AWAITING_FINAL_PHASE8_PAYLOAD_AND_ONE_USE_ROOT_RELEASE`.

`run_rq2b_v7_first_matrix_bm25_b1_v2.py` replaces the legacy BM25 entrypoint
for Phase 8. The legacy runner remains unmodified and is not eligible for the
final execution root because it binds superseded representations and lacks a
one-use release boundary. This V2 runner has no default scientific payload or
output path and refuses to overwrite output or attempt directories.

## Intake boundary

The runner executes only after a separate record with schema
`rq2b-v7-bm25-b1-root-release-v2` uses state
`EXPLICITLY_AUTHORISED_FOR_ONE_PHASE8_ROOT_RELEASED_EXECUTION`, is unused and
one-use, and binds an exact payload SHA, Phase-8 readiness receipt SHA, unique
run/attempt/release IDs, cache destinations and resource ceilings. A pending
template cannot pass this gate.

The payload schema `rq2b-v7-bm25-b1-phase8-payload-v2` must bind the frozen
label-free query runtime, source and core-condition manifests, the official
output validator, the runner itself, and all four representations. I1/I2 are
fixed to the authoritative `rq2b_v7_phase7_i1_i2_2026_09_09_v2` files. Final
V4.1 I3C-fielded and I3-flat paths/hashes are deliberately absent from source
code and must arrive through the later explicit Phase-8 payload with
`phase8_final=true`. The runner has no label, acceptable-set, target, result or
offline-analysis intake.

## Method and outputs

For B01, B04, B07 and B10, the runner tokenises queries and representation text
with lowercase `[a-z0-9]+`, builds one global BM25 index per representation,
uses `k1=1.5`, `b=0.75`, multiplicative query term frequency and the sealed IDF
formula, and emits Top-100 rows compatible with
`rq2b-v7-b1-runner-output-v1`. Ranking is descending score with ascending
`source_sha256` as the deterministic exact-tie key. The ordered Top-20 is
hash-bound for later B2 consumption. BM25 rows record zero provider calls,
tokens, model forwards, retries, timeouts and failures; only measured query
wall time is nonzero.

Execution first writes a unique attempt receipt, then stages output and
atomically renames it to the unused destination. A failure keeps its attempt
record and never produces a completed output package. There is no provider,
model-loading or network code and no automatic retry path.

## No-inference checks

From the clean repository root:

```sh
python3 -B skill_benchmark/scripts/run_rq2b_v7_first_matrix_bm25_b1_v2.py --self-test
python3 -B skill_benchmark/scripts/test_rq2b_v7_first_matrix_bm25_b1_v2.py
PYTHONPYCACHEPREFIX=/private/tmp/rq2b-bm25-b1-v2-pycache python3 -B -m py_compile \
  skill_benchmark/scripts/run_rq2b_v7_first_matrix_bm25_b1_v2.py \
  skill_benchmark/scripts/test_rq2b_v7_first_matrix_bm25_b1_v2.py
git diff --check
```

The scientific execution form is intentionally documented without a concrete
release path:

```sh
python3 -B skill_benchmark/scripts/run_rq2b_v7_first_matrix_bm25_b1_v2.py \
  --execute --authorisation path/to/explicit_one_use_phase8_root_release.json
```

Do not run it until the final Phase-8 package and an explicit user release both
exist.
