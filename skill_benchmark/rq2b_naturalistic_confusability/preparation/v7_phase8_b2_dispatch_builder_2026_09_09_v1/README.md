# V7 Phase-8 B2 dispatch builder

Status: `IMPLEMENTED_NO_B2_PAYLOAD_OR_RELEASE_MATERIALISED`.

This prospective package prepares the deterministic B2 handoff. It does not
contain a fabricated B1 receipt, executable approval, payload, release,
provider response, model output, metric, or result. The included approval file
is deliberately `PENDING` and cannot satisfy the builder.

The builder has two fail-closed stages. First, it replays the current official
label-free output validator over exactly the 12 persisted B1 cells (12,924
rows) and writes a new hash-bound receipt. Second, it replays that receipt and
the final Phase-8 root, then materialises the two runner-native B2 payloads and
unused one-use releases. Any missing cell, duplicate row, Top-20 drift,
representation/hash drift, stale validator, non-PASS root, or non-approved
scope stops before B2 execution.

Each executable release also embeds the exact path/SHA, decision and scope of
the approved B2 record, and the runner replays that record at execution time.
The SkillRouter runner additionally requires its score-cache namespace to be
absent both when validating the release and immediately before model loading;
pre-populated scores cannot be inherited across the release boundary.

## Frozen outcome scope

- Existing B1: 12 core cells, 12,924 persisted query rows.
- Qwen B2: 12 core `GQ` plus C1-Q/C3-Q/C4-Q = 15 materialised conditions.
- SkillRouter B2: 12 core `GS` plus C1-S/C3-S/C4-S = 15 materialised conditions.
- C2-Q and C2-S are exact aliases of B05-GQ and B05-GS; they are not rerun.
- Together this yields exactly the frozen 36 core plus 6 diagnostic outcomes.

Both payloads bind the final Phase-8 root, all four current representations,
the complete persisted B1 artifacts and their Top-20 bindings, condition
authority, runner hashes, method contracts, and the current output validator.
The Qwen path additionally binds its helper and both exact chunkers; the local
path binds the pinned SkillRouter reranker model snapshot and tokenizer.

## Exact future commands

Run from the repository root. Replace placeholders with new paths; every output
is create-only.

Create a fresh official B1 receipt after the 12 B1 cells have completed:

```sh
.venv-rq2b-v7/bin/python3 -B \
  skill_benchmark/scripts/build_rq2b_v7_phase8_b2_dispatch.py \
  --write-b1-receipt \
  --phase8-receipt REQUIRED_FINAL_PHASE8_PACKAGE/phase8_readiness_receipt.json \
  --b1-artifact PATH_TO_BM25_B1.jsonl.gz \
  --b1-artifact PATH_TO_QWEN_B1.jsonl.gz \
  --b1-artifact PATH_TO_SKILLROUTER_B1.jsonl.gz \
  --b1-validation-receipt \
    skill_benchmark/rq2b_naturalistic_confusability/preparation/B1_RECEIPT_PACKAGE/b1_validation_receipt.json
```

Capture the already-given user approval in a separate versioned record using
the pending file only as a schema guide. Do not place secrets in that record.
Then materialise the B2 dispatch:

```sh
.venv-rq2b-v7/bin/python3 -B \
  skill_benchmark/scripts/build_rq2b_v7_phase8_b2_dispatch.py \
  --materialize \
  --phase8-receipt REQUIRED_FINAL_PHASE8_PACKAGE/phase8_readiness_receipt.json \
  --b1-validation-receipt \
    skill_benchmark/rq2b_naturalistic_confusability/preparation/B1_RECEIPT_PACKAGE/b1_validation_receipt.json \
  --approval-record PATH_TO_APPROVED_B2_RECORD.json \
  --output-dir \
    skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase8_b2_dispatch_YYYY_MM_DD_vN
```

The deterministic cache prefix is reported by
`cache_prefix(root_manifest_sha256, b1_validation_receipt_sha256)`; the CLI
derives the Qwen preflight path automatically. An explicit
`--qwen-preflight-receipt` is accepted only when it equals that derived path.

The materialisation step performs local tokenisation only. Qwen ceilings for
request attempts, calls, documents, submission proxy tokens and bytes equal
the exact no-provider workload; provider-reported tokens have a 2x proxy-token
fail-closed ceiling. SkillRouter ceilings equal the exact unique pair, token,
and exact-length batch inventory for its new empty score-cache namespace. Both
have zero automatic retries and seven-day wall-time guards.

If materialisation passes, its generated `README.md` contains the two exact
execution commands. Qwen and SkillRouter use distinct output/attempt paths;
SkillRouter also uses a distinct score-cache path. A release becomes spent as
soon as an attempt receipt exists and must never be reused.

## No-inference verification

```sh
python3 -m py_compile \
  skill_benchmark/scripts/build_rq2b_v7_phase8_b2_dispatch.py \
  skill_benchmark/scripts/test_build_rq2b_v7_phase8_b2_dispatch.py
python3 -B skill_benchmark/scripts/build_rq2b_v7_phase8_b2_dispatch.py --self-test
python3 -B skill_benchmark/scripts/test_build_rq2b_v7_phase8_b2_dispatch.py
python3 -B skill_benchmark/scripts/test_rq2b_v7_qwen_reranker_b2.py
python3 -B skill_benchmark/scripts/test_rq2b_v7_skillrouter_reranker_b2.py
git diff --check
```

The builder never imports a provider client, opens label or acceptable-set
files, executes either reranker, or calls the offline scorer. CPU-fp32
sensitivity remains a separate later authorisation.
