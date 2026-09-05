# RQ1 Public Original Round 3 Joint Group Qwen Preflight

Date: 2026-09-04  
Status: `HISTORICAL PRE-EXECUTION EVIDENCE / SUPERSEDED BY COMPLETED QWEN RESULT`

## Purpose

This preflight inventories the exact texts needed for the Qwen dense twin of
the original-source joint group-removal comparison. It reads frozen public
source/mask files and the already authorised local embedding cache, but does
not read an API key, issue a network request, or send any text.

## Frozen Scope

- Group freeze SHA-256: `7a73a3d4026ffa32b855ae3844cf3d63046aff9535435294a2cf742f84cc9062`
- Qwen payload SHA-256: `8d9d87e791a0f34807f4a2ae8f85ec43798a7df356bffd8a38a4db22520bb2ea`
- Model: DashScope international `text-embedding-v4`, 1024 dimensions.
- 369 composition-family cases; 1,476 planned dense ranking rows.
- No query rewrite, reranker, automatic retry, network call, or text transfer.

## Cache-Aware Inventory

| Text type | Unique total | Cache hits | New outbound texts |
| --- | ---: | ---: | ---: |
| Original or group-masked candidate documents | 646 | 304 | 342 |
| Frozen direct/paraphrase prompts | 336 | 336 | 0 |
| Total | 982 | 640 | 342 |

The only possible new external payload is 342 group-masked candidate documents:
1,222,989 UTF-8 bytes and a local lexical-token proxy of 155,923. This proxy is
an audit estimate, not provider billing usage. With batches of at most ten
texts, the no-retry ceiling is 35 request attempts and 35 successful calls.

## Integrity

The preflight validator verified each text hash, source/mask binding, group
binding, inventory partition, cached embedding binding, request ceiling and
zero network activity. `SHA256SUMS` verification passed. A first local-only
draft missed the `group` provenance key on query records; it was retained in
`round3_clean_only_joint_group_qwen_preflight_invalid_schema_20260904/` and
not used. The canonical payload above was regenerated after the schema repair.

## Required Authorisation Before Execution

The user explicitly authorised the exact 342 new candidate-card texts. Qwen
then completed with 35 successful no-retry calls, zero query transfers and
283,526 provider-reported input tokens. This preflight remains the binding
scope record; the completed result is recorded separately and remains out of
thesis LaTeX/PDF pending user review.

## Canonical Artifacts

- Preflight: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/round3_clean_only_joint_group_qwen_preflight/`
- Preflight builder: `skill_benchmark/scripts/prepare_rq1_public_original_round3_joint_group_qwen_preflight.mjs`
- Validator: `skill_benchmark/scripts/validate_rq1_public_original_round3_joint_group_qwen_preflight.mjs`
