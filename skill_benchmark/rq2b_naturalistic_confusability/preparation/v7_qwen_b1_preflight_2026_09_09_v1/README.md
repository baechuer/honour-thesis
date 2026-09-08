# V7 Qwen label-free B1 preflight 2026_09_09_v1

+Status: `PASS_LABEL_FREE_PAYLOAD_AND_CACHE_PREFLIGHT_AWAITING_PHASE7_QA_AND_ROOT_RELEASE`.

+This package prepares B02/B05/B08/B11 only. It uses the frozen 1,077 label-free
+queries, 3,798-source manifest, four representation artifacts, and first-matrix
+conditions. It reads no target/gold/A_q/J_q/D_q/result artifact and performs no
+provider request.

+The payload uses Qwen `text-embedding-v4` at 1,024 dimensions, the existing
+`rq2b-exact-markdown-chunker-v1` exact-substring chunker with 7500-proxy-token
+windows and 256-token overlap, maximum-window cosine as the B1
+outcome, stable `source_sha256` ties, and Top-100. Mean-window cosine is
+persisted separately as a non-core sensitivity. Cold query latency requires one
+single-text provider request per unique query even when a query cache entry exists.

+The old V3 exact cache is inspected read-only for expected payload keys. Each hit
+is schema/model/dimension/chunker/text/vector checked and byte-hash bound in the
+ignored payload inventory. Only the clean V7 cache may receive new entries.

+No execution command is valid yet. `pending_authorisation.json` deliberately has
+a non-executable state. After Phase-7 QA passes, a separate root release must bind
+the exact payload hash, ceilings, run ID, output directory, timeout and QA receipt.

+Offline replay:
+
+```bash
+.venv-rq2b-v7/bin/python -B skill_benchmark/scripts/build_rq2b_v7_qwen_b1_preflight.py --verify
+.venv-rq2b-v7/bin/python -B skill_benchmark/scripts/test_rq2b_v7_qwen_b1.py
+```
+