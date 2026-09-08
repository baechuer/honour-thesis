# V7 first-matrix BM25 B1 run v1

Status: `PASS_B01_B04_B07_B10_LABEL_FREE_LOCAL_BM25_EXECUTION`.

This package contains exactly the four local BM25 first-stage cells requested
for the frozen V7 first matrix: B01/I1-discovery, B04/I2-original,
B07/I3C-fielded and B10/I3-flat. Each cell covers all 1,077 label-free runtime
queries against all 3,798 frozen source identities and persists Top-100.

The runner reads no target, gold, acceptable-set, judgement, review-outcome,
offline-label or prior selector-output artifact. It performs no network,
provider, embedding, reranking or offline-scoring call.

BM25 is lowercase `[a-z0-9]+`, k1=1.5, b=0.75, with multiplicative query-term
frequency. Rankings use descending score and ascending `source_sha256` as the
stable tie-break. Row-level cost records measured local query wall time; all
provider/token/window/retry/timeout/failure counters are zero.

## Artifacts

- `b1.jsonl`: 4,308 strict `rq2b-v7-b1-runner-output-v1` rows; SHA-256 `5a6594163b69a5cda269658c4a106bd5d6c4241f3768e68f4055e9e32972b298`.
- `run_receipt.json`: exact input, runner, parameter, coverage, cost and output bindings.
- runner: `skill_benchmark/scripts/run_rq2b_v7_first_matrix_bm25_b1.py`; SHA-256 `1d24768add06e363a1a6dd95bb0a7df54ed273f5983b75cc1e6c466a9e6f7c6e`.

## Replay

From the repository root, verification is label-free and read-only:

```sh
python3 -B skill_benchmark/scripts/run_rq2b_v7_first_matrix_bm25_b1.py --verify
python3 -B skill_benchmark/scripts/validate_rq2b_v7_runner_outputs.py \
  --b1 skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_first_matrix_bm25_b1_run_2026_09_09_v1/b1.jsonl \
  --b2 /dev/null --allow-incomplete
```

The official validator's incomplete mode is intentional: this package is the
four BM25-cell B1 shard only and does not fabricate the other eight B1 cells or
any B2 rows.
