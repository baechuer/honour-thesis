# V7 Qwen label-free B1 preflight 2026_09_09_v2

Status: `PASS_LABEL_FREE_PAYLOAD_AND_CACHE_PREFLIGHT_AWAITING_PHASE7_QA_AND_ROOT_RELEASE`.

This package prepares B02/B05/B08/B11 only. It uses the frozen 1,077 label-free
queries, 3,798-source manifest, four representation artifacts, and first-matrix
conditions. It reads no target/gold/A_q/J_q/D_q/result artifact and performs no
provider request.

The payload uses Qwen `text-embedding-v4` at 1,024 dimensions and the versioned
`rq2b-v7-exact-markdown-chunker-v2-short-boundary-progress-fix` exact-substring correction with 7500-proxy-token
windows and at most 256 overlap tokens. It preserves lossless
character coverage and fixes the v1 short-boundary one-character-progress bug.
Maximum-window cosine is the B1 outcome, ties use ascending `source_sha256`, and
Top-100 is persisted. Mean-window cosine is a separate non-core sensitivity.
Cold query latency requires one single-text request per unique query even when a
query cache entry exists.

Formal B1 and sensitivity outputs are condition-sharded deterministic gzip
(`mtime=0`) containing canonical compact JSONL. Compression changes neither row
semantics nor the Top-20 binding hash, and the Qwen validator reads `.jsonl.gz`
directly.

The old V3 exact cache is inspected read-only for expected payload keys. Each hit
is schema/model/dimension/chunker/text/vector checked and byte-hash bound in the
ignored payload inventory. Only the clean V7-v2 cache may receive new entries.

No execution command is valid yet. `pending_authorisation.json` deliberately has
a non-executable state. After Phase-7 QA passes, a separate root release must bind
the exact payload hash, ceilings, run ID, output directory, timeout and QA receipt.

Offline replay:

```bash
.venv-rq2b-v7/bin/python -B skill_benchmark/scripts/build_rq2b_v7_qwen_b1_preflight.py --verify
.venv-rq2b-v7/bin/python -B skill_benchmark/scripts/test_rq2b_v7_qwen_b1.py
.venv-rq2b-v7/bin/python -B skill_benchmark/scripts/validate_rq2b_v7_qwen_b1_shards.py --run-manifest /ABSOLUTE/PATH/manifest.json
```
