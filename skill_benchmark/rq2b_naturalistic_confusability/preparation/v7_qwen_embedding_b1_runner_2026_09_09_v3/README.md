# V7 Qwen embedding B1, Phase-8-compatible V3

Status: implementation and no-provider tests only. No payload, provider request,
embedding, or scientific result was produced by this preparation task.

## Authoritative scope

`first_matrix_conditions.jsonl` is authoritative. Qwen `text-embedding-v4`
materialises exactly four B1 cells across all 1,077 queries:

| Representation | Qwen B1 condition |
|---|---|
| I1-discovery | B02-G0 |
| I2-original | B05-G0 |
| I3C-fielded | B08-G0 |
| I3-flat | B11-G0 |

B03/B06/B09/B12-G0 belong to SkillRouter and are rejected by the Qwen
preflight. The focused regression test makes this separation explicit.

I1 and I2 are pinned to the authoritative 2026-09-09 V2 bytes:

- I1-discovery: `0fc34abe8ca3f5d23bcc563f496831e37628491ddc65caeb9c7a284d5d1ff8dd`
- I2-original: `8860e415fa7ae6718e5e2b6ca3e57605150120f30a8414e6c6931a99355952ec`

I3C-fielded and I3-flat have no hard-coded content hash. They are accepted
only from the final V4.1 artifact bindings in a PASS Phase-8 readiness receipt
and its byte-bound root manifest. If those final artifacts, the root, or the
runner hash are absent or stale, preflight fails closed.

## Frozen method

- Provider contract: DashScope international OpenAI-compatible
  `/embeddings`, `text-embedding-v4`, 1,024 dimensions, float encoding, at
  most 10 texts per request.
- Windowing: `rq2b_v7_exact_chunking_v2.py`, 7,500 content tokens and 256
  content-token overlap. Content-token, model-input token (with special
  tokens), special-token delta, text-byte, and full request-body byte counts
  remain separate.
- Primary score: maximum window cosine. Cosine of the L2-normalised window
  mean is written only as a non-core sensitivity artifact.
- Ranking: Top 100 with `source_sha256` ascending as the exact stable tie
  break. Each row's first 20 identities are hash-bound using the official B1
  Top-20 binding method.
- Official B1 row cost: only the online cold query request and its local
  ranking step. It records one provider call, query model-input proxy tokens,
  one query forward, zero cache hits, and zero retries. Offline document
  embedding and cache work is kept in the run receipt ledger, not charged to
  every scientific row.

## Two-stage execution gate

`build_rq2b_v7_qwen_b1_phase8_v3_preflight.py --preflight` is local-only. It
verifies the final Phase-8 bindings, materialises immutable payload artifacts,
inventories only the V3 exact cache, and computes exact unique-text, hit/miss,
request-attempt, external-text, proxy-token, UTF-8 text-byte, and complete
request-body-byte counts. It writes a PASS receipt bound to the payload,
Phase-8 receipt/root, runner, builder, chunker, provider helper, tokenizer,
official validator, and tests.

Execution then requires `run_rq2b_v7_qwen_b1_phase8_v3.py --execute` and a
separate root release with schema
`rq2b-v7-qwen-b1-phase8-root-release-v3`. The release is one-use, binds the
exact PASS preflight and payload hashes, exact run/destination/provider fields,
all predictable ceilings, a provider-reported-token ceiling, and a wall-time
ceiling. Reuse is prevented by an immutable, release-bound attempt directory;
outputs and exact-cache entries are never overwritten. A request has one
attempt and zero automatic retries. The started, success, and failure receipts
remain on disk independently of scientific-output completion.

The preflight must be regenerated after any runner, helper, tokenizer,
Phase-8, representation, payload, or cache-state change. Execution accepts
only the corresponding current PASS receipt.

## No-provider verification

The intended preparation checks are:

```text
python3 -B -m py_compile \
  skill_benchmark/scripts/build_rq2b_v7_qwen_b1_phase8_v3_preflight.py \
  skill_benchmark/scripts/run_rq2b_v7_qwen_b1_phase8_v3.py \
  skill_benchmark/scripts/test_rq2b_v7_qwen_b1_phase8_v3.py
python3 -B skill_benchmark/scripts/build_rq2b_v7_qwen_b1_phase8_v3_preflight.py --self-test
python3 -B skill_benchmark/scripts/run_rq2b_v7_qwen_b1_phase8_v3.py --self-test
python3 -B skill_benchmark/scripts/test_rq2b_v7_qwen_b1_phase8_v3.py
git diff --check
```

Do not run `--preflight` until the final Phase-8 V4.1 receipt/root exists. Do
not run `--execute` without the independently issued one-use root release.
