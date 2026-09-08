# V7 B36+C6 sanitised provider-connectivity receipt v1

Status: `PASS_SANITISED_SYNTHETIC_CONNECTIVITY_RECEIPT_NOT_SCIENTIFIC_EXECUTION`.

Under explicit synthetic-only authorisation, two connectivity calls were completed:

- DashScope `text-embedding-v4`: one synthetic text, 1024 dimensions, 11 prompt/total tokens.
- DashScope `qwen3-rerank`: one synthetic query and two synthetic documents, total tokens 60, scores `[0.7933007406217729, 0.44544158349861485]`.

Transferred benchmark prompts, benchmark queries, benchmark source documents and benchmark candidate texts: **zero**. The synthetic input text, raw request/response, credential value and authorisation header are not retained. Only the credential variable name `DASHSCOPE_API_KEY` is recorded.

This receipt establishes endpoint/model connectivity for the two frozen request contracts. It is not a scientific or benchmark result, does not establish full-matrix readiness, does not authorise another call, and does not modify the zero-inference runtime preflight.

## Bound evidence

- Zero-inference preflight report SHA-256: `93e047af9e92ead168b53a1b47b17ff5839b36ee3f900d47e5254e2694214279`
- Qwen embedding contract script SHA-256: `ad9016cf14c20c3935c84482d9c9499be3e86f0272a6105a7ab3fa2238a7c05f`
- Qwen reranker contract script SHA-256: `d7f83d25076dbec12750d8c7dad687b69545f335bddf7a1889bc9f3a5a598f7a`

## Exact zero-network replay

```sh
python3 -B skill_benchmark/scripts/verify_rq2b_v7_first_matrix_provider_connectivity_receipt.py
python3 -B skill_benchmark/scripts/test_rq2b_v7_first_matrix_provider_connectivity_receipt.py
git diff --check
```

These replay commands validate the sanitised receipt and its local bindings. They make no provider call and read no key.
