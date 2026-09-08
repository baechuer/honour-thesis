# V7 B36+C6 runtime preflight v1

Status: `PASS_ZERO_INFERENCE_RUNTIME_INVENTORY_EXECUTION_NOT_AUTHORISED`.

This package binds the V7 36-condition core matrix plus six fixed-candidate bridges to one exact local Python environment, two pinned local SkillRouter snapshots, the two DashScope request contracts, and the supplied verified smoke dispositions. It is a runtime inventory and fail-closed execution contract, not a retrieval/reranking runner or an authorisation receipt.

## Frozen scientific local runtime

- device: `mps`
- attention implementation: default SDPA
- dtype: `bfloat16`
- batching: exact input-token-length buckets only, no padding, maximum batch size 16
- SkillRouter embedding output: exactly 1,024 finite coordinates before caching or scoring
- SkillRouter reranker output: finite yes-logit-minus-no-logit score before persistence or ranking
- no heterogeneous left-padded batch, float16, silent fp32/eager substitution or silent CPU fallback
- deterministic CPU eager/fp32 sensitivity spot-check: eight lowest hash-bound stable IDs per representation and local model; record score deltas and rank/tie changes without treating CPU as a silent substitute

The corrected smoke evidence localises the default-attention failure to heterogeneous left-padded batches. Default-SDPA MPS bfloat16 is finite for short exact-token-length unpadded batches; embedding identical-row cosine was 1.0. The short reranker probe was finite, but its relevant yes-minus-no score quantised to 0 while the irrelevant example was about -5.25. That is a numerical/tie limitation, so exact ties and CPU-fp32 sensitivity must be reported. Eager and fp32 results remain diagnostic/reference evidence, not the primary setting. The builder records these supplied dispositions but deliberately does not rerun a model.

The supplied token audit records I1 max 419 tokens and I2 max 56,648 tokens. I2 has 28 sources above 7,500, four above 16,000 and one above the embedding model's 32,768-position limit; I3C and I3-flat still need the same audit. A 30k fp32 probe failed with `Invalid buffer size 53.64 GiB`; fp32 at 4,096 was finite but took 78.83 seconds, while bfloat16 was finite at 4,096 (2.81--3.88 seconds) and 7,500 (10.65 seconds).

The suggested 7,500-token/256-overlap/max-window approach for only over-threshold documents is recorded as `PROPOSED_NOT_APPROVED_HARD_GATE`. It must preserve every token and be classified as a pipeline hardware adaptation. It cannot be silently truncated, excluded, substituted or executed until the remaining length audit and prospective amendment are approved and sealed.

## Current-process observations

- `DASHSCOPE_API_KEY` present: `false` (boolean only; no value is serialised and no dotenv is scanned)
- PyTorch MPS built: `true`
- PyTorch MPS available in this verifier process: `false`

These observations do not override the smoke evidence. Any absent credential or unavailable MPS backend blocks execution in that process; it does not license a fallback. A later execution attempt must reissue or extend the preflight if the bound environment changes.

## Exact replay

From the repository root:

```sh
.venv-rq2b-v7/bin/python -B skill_benchmark/scripts/verify_rq2b_v7_first_matrix_runtime_preflight.py
.venv-rq2b-v7/bin/python -B skill_benchmark/scripts/test_rq2b_v7_first_matrix_runtime_preflight.py
git diff --check
```

The replay hashes only named tracked inputs and named ignored snapshot files. It does not read `.env`, model tensors, benchmark labels, acceptable sets or result files. It makes zero network calls and zero model forward passes.

## Boundary

The pinned V3 SkillRouter constants and model semantics are lineage inputs only. Existing V3 hosted CUDA/bfloat16 runners embed old 2,433-skill/381-prompt payload assumptions and are not valid V7 B36+C6 runners. Likewise, this package freezes provider endpoints and payload/response gates but does not authorise DashScope use. A separate V7 payload, runner and explicit execution receipt remain required.
