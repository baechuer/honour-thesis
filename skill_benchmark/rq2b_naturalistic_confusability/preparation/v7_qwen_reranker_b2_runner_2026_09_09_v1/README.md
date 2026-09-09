# V7 Qwen qwen3-rerank B2 runner

Status: `IMPLEMENTED_NO_PROVIDER_CALL_NO_SCIENTIFIC_OUTPUT`.

This package documents `run_rq2b_v7_qwen_reranker_b2.py`. The runner is the
label-free Qwen B2 execution surface for the approved V7 B36+C6 matrix. It does
not grant execution authority, and no provider request was made while building
or testing it.

## Scientific scope

The runner materialises exactly 15 conditions over the frozen 1,077 queries:

- `B01-GQ` through `B12-GQ`;
- `C1-Q`, `C3-Q`, and `C4-Q`; and
- 16,155 B2 rows in total, each with exactly 20 input and 20 reranked
  candidates.

`C2-Q` is the approved exact alias of `B05-GQ`; it is never materialised. The
runner obtains every candidate list from persisted, officially validated B1
Top-20 rows. It has no candidate-generation code and rejects missing,
duplicated, reordered, or hash-drifted B1 rows.

The only selector-visible document bytes are the four Phase-8 source
representations. I1/I2 are pinned to the authoritative Phase-7 V2 artifacts;
both final I3 paths and hashes must be supplied by the later Phase-8 package
with extraction protocol `I3C_SUBAGENT_EXTRACTION_V4_1`. The runner rejects a
payload unless all four representations have exact 3,798-source coverage and
their `selector_text_sha256` values match the UTF-8 selector bytes.

## Frozen Qwen contract

The runner imports the existing `rq2b_qwen_reranker.py` contract without
changing its method parameters:

- endpoint:
  `https://dashscope-intl.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank`;
- model: `qwen3-rerank`;
- request: `model`, `input.query`, `input.documents`, then
  `parameters.instruct`, `return_documents=false`, and
  `top_n=document_count`;
- response: `output.results` must cover each requested index exactly once with
  a finite `relevance_score`;
- proxy document window: 3,500 tokens with at most 256 proxy-token overlap;
- request ceiling: 500 documents and 120,000 proxy tokens, including the
  frozen 1,000-token request allowance;
- a complete first-candidate anchor is duplicated after every request split,
  with absolute cross-request score tolerance `1e-6`;
- candidate score: maximum exact-window score; mean score is retained only in
  the window audit; and
- exact score ties use ascending `source_sha256`, never B1 rank.

The pinned local proxy tokenizer is
`pipizhao/SkillRouter-Embedding-0.6B@c03c9bcee9fce92ab0262bb6dcf54d174a8ba558`;
`tokenizer.json` is bound to
`def76fb086971c7867b829c23a26261e38d9d74e02139253b38aeb9df8b4b50a`.
The runner uses `local_files_only=true` and never downloads a tokenizer.

## Mandatory no-provider preflight

Execution needs a fresh preflight receipt. A non-executable pending-release
JSON must use schema `rq2b-v7-qwen-reranker-b2-pending-release-v1`, state
`PENDING_NO_PROVIDER_PREFLIGHT_NOT_EXECUTABLE`, and bind:

- the exact Phase-8/B1 payload path and SHA;
- the frozen endpoint/model/API-key variable/120-second timeout/zero-retry
  provider object;
- the future output and attempt destinations; and
- all seven ceilings: attempts, successful calls, submitted documents, local
  proxy tokens, UTF-8 request bytes, provider-reported total tokens, and wall
  time.

Run the preflight only after the final Phase-8 I3 artifacts and official B1
validation receipt exist:

```sh
python3 -B skill_benchmark/scripts/run_rq2b_v7_qwen_reranker_b2.py \
  --preflight \
  --pending-release skill_benchmark/cache/EXPLICIT_QWEN_B2_PENDING_RELEASE.json \
  --preflight-receipt skill_benchmark/cache/NEW_QWEN_B2_PREFLIGHT_RECEIPT.json
```

This command does not read a credential and cannot call `request_once`. It
reconstructs all 16,155 rows and reports exact planned request, submitted
document, local proxy-token, UTF-8 byte, candidate-window, duplicate-anchor,
and split-row counts. It also reports headroom for every ceiling. Provider
reported tokens and execution wall time are explicitly runtime-only rather
than guessed.

The preflight additionally compares the frozen V1 exact chunker and the V2
short-boundary-progress correction on the actual four Phase-8 representations
and actual persisted B1 lists. It hashes ordered window and request signatures
for every row. A receipt is executable only when both window boundaries and
request partitioning have exact V1/V2 parity. Any difference produces
`FAIL_METHOD_PARITY_REVIEW_REQUIRED`, preserves up to 25 difference examples
plus a hash of the full difference docket, and stops. The runner never silently
switches chunkers.

The clean worktree currently has no final merged Phase-8 I3 views or root
package, so the actual four-representation parity preflight is intentionally
not run here. Batch extraction outputs are not substituted for final views.

## Root release and execution

A later one-use root release must use schema
`rq2b-v7-qwen-reranker-b2-root-release-v1`, state
`EXPLICITLY_AUTHORISED_FOR_ONE_PHASE8_B1_BOUND_EXECUTION`, and bind the exact
payload, Phase-8 receipt, official B1 receipt, pending-release, PASS preflight
receipt, run/attempt IDs, destinations, provider contract, and ceilings. The
runner revalidates every binding and refuses a stale preflight or a destination
that already exists.

Only after that separate release may the execution command be used:

```sh
python3 -B skill_benchmark/scripts/run_rq2b_v7_qwen_reranker_b2.py \
  --execute \
  --authorisation skill_benchmark/cache/EXPLICIT_QWEN_B2_ROOT_RELEASE.json
```

The API key is read only from `DASHSCOPE_API_KEY`; no dotenv path is scanned
and no credential is serialized. Before each provider call, the runner writes
an immutable attempt receipt containing the request hash, ordered document
hashes, counts, timeout and zero-retry policy. Each attempt receives exactly
one completion or failure receipt. There is no automatic retry. A timeout,
transport error, malformed response, incomplete index coverage, non-finite
score, anchor disagreement, token-ceiling breach, or wall-time breach stops the
run. The attempt directory and any staging directory remain for diagnosis, and
no completed output directory is published.

Successful publication uses deterministic gzip and contains:

- official-schema `qwen_b2.jsonl.gz` rows;
- exact-tie, window/input-binding, and request-receipt-index audits;
- a cost ledger with attempted/successful calls, timeouts, failures, submitted
  documents, proxy tokens, UTF-8 bytes, and provider-reported input/output/total
  tokens; and
- a run receipt and manifest bound to Phase-8, B1 validation, the payload, and
  the one-use root release.

The official B2 `input_tokens` field is the declared local proxy submission
count including request allowance and duplicate anchors. Provider-reported
token fields remain separately recorded. Monetary amount and currency are
`null` with an explicit `NOT_RETURNED...NOT_ESTIMATED` status because neither
the approved plan nor response contract freezes a price. The runner does not
invent a historical or current price.

Final scientific acceptance still requires combining these 15 Qwen rows with
the 15 independently produced SkillRouter B2 rows and running the official
label-free validator over the complete 30-condition B2 scope. Labels,
acceptable sets, and metrics remain outside this runner.

## No-provider verification

```sh
python3 -m py_compile \
  skill_benchmark/scripts/run_rq2b_v7_qwen_reranker_b2.py \
  skill_benchmark/scripts/test_rq2b_v7_qwen_reranker_b2.py
python3 -B skill_benchmark/scripts/run_rq2b_v7_qwen_reranker_b2.py --self-test
python3 -B skill_benchmark/scripts/test_rq2b_v7_qwen_reranker_b2.py
```

The focused tests cover official B2 schema compatibility, exact source/query/
candidate binding, ascending-SHA tie handling, strict response coverage,
request shape and timeout using a mocked transport, zero retry with immutable
failure receipts, stale-preflight rejection, insufficient-ceiling rejection,
full 15-by-1,077 preflight accounting with the provider call patched to fail if
invoked, and C2-Q non-materialisation.

The existing helper's `validate_condition` was specifically regression-tested:
an unchanged ordered source-window list passes, while changed window bytes even
with a recomputed local text hash fail against the independent trusted binding.
No helper code change was needed; the initially suspected duplicate
comprehension was not present in the file after an exact line-number check.
