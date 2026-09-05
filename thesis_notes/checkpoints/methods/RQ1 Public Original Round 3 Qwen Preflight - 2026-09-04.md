# RQ1 Public Original Round 3 Qwen Preflight

Date: 2026-09-04

## Status

`F2 LOCAL PREFLIGHT COMPLETE / EXTERNAL EXECUTION NOT AUTHORISED`

## Binding

This preflight is derived from the same frozen clean-only RQ1 frame used for
the validated BM25 result. It prepares the dense-retrieval twin only; it does
not change source documents, masks, prompts, gold labels, candidate order, or
the BM25 result.

| Property | Value |
| --- | --- |
| Endpoint | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1/embeddings` |
| Model | `text-embedding-v4` |
| Dimensions | 1024 |
| Retry policy | No automatic retry; first request failure stops the run. |
| Max texts per request | 10 |
| Dense ranking rows after success | 4,312 |

## Exact Potential External Payload

| Item | Count |
| --- | ---: |
| Candidate document instances in scored cases | 7,068 |
| Prompt instances in scored cases | 2,156 |
| Unique candidate document texts | 1,510 |
| Unique prompt texts | 388 |
| Valid cache hits | 0 |
| New external texts | 1,898 |
| New document texts | 1,510 |
| New prompt texts | 388 |
| UTF-8 bytes | 10,109,779 |
| Local lexical token proxy | 1,341,769 |
| Maximum request attempts and successful calls | 190 each |

The local token proxy is an audit ceiling and is not a provider billing token
count. There is no cache reuse because none of the required text hash/model/
dimension/schema-bound embeddings exists in the dedicated RQ1 Round-3 cache.

Payload SHA-256:

```text
38a8bab9938f884390caae6c0c062aac7ff7d08510b7e380156cf7fa6dba16d2
```

## Local Validation

The independent preflight validator passed all of the following without
network activity:

- payload hash and frozen-frame hash;
- 1,078 cases and 4,312 planned dense result rows;
- all 7,068 document instances and 2,156 query instances;
- text SHA-256 values, role bindings and deduplicated inventory;
- document/query partition totals;
- zero cache hits; and
- zero network calls and zero transmitted texts.

## Required Authorisation Before Execution

The next execution would send the 1,898 unique texts above to DashScope
international. It needs an explicit approval naming this payload SHA-256,
`text-embedding-v4`, 1024 dimensions, the no-retry 190-call ceiling, and the
dedicated local cache. No API key has been read and no external text transfer
has occurred during F2.

## Evidence

- Payload: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/round3_clean_only_qwen_preflight/payload.json`
- Manifest/checksums: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/round3_clean_only_qwen_preflight/`
- Builder: `skill_benchmark/scripts/prepare_rq1_public_original_round3_clean_qwen_preflight.mjs`
- Validator: `skill_benchmark/scripts/validate_rq1_public_original_round3_clean_qwen_preflight.mjs`
