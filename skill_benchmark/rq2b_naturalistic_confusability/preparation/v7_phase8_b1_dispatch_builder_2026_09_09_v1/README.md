# V7 Phase-8 B1 dispatch builder

Status: `IMPLEMENTED_AWAITING_FINAL_PHASE8_ROOT_AND_APPROVAL_RECORD`.

This package documents the deterministic B1 dispatch builder. It contains no
fabricated root hash, executable approval, payload, release, result, or
model/provider output. The included approval file is deliberately `PENDING`
and cannot pass the builder's release gate.

The builder fails closed until the supplied Phase-8 readiness receipt binds a
`READY_FOR_FORMAL_EXPERIMENT` root with exactly 1,077 queries, 3,798 sources,
36 core conditions, six fixed diagnostics, the final four representation
artifacts, and the current hashes of all three B1 runners. It separately
requires an approved record created by the task that holds the user's actual
execution authority; the pending template must not be renamed and reused as
approval.

Once both inputs exist, use:

```sh
.venv-rq2b-v7/bin/python3 -B \
  skill_benchmark/scripts/build_rq2b_v7_phase8_b1_dispatch.py \
  --materialize \
  --phase8-receipt PATH_TO_FINAL_PHASE8_PACKAGE/phase8_readiness_receipt.json \
  --approval-record PATH_TO_SEPARATE_EXPLICIT_APPROVAL_RECORD.json \
  --output-dir \
    skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase8_b1_dispatch_2026_09_09_v1
```

The builder derives a root-SHA cache namespace and materialises:

- exact label-free BM25 and SkillRouter payloads;
- the existing Qwen V3 zero-network payload/preflight under ignored cache;
- an exact local-tokenisation/no-model-forward SkillRouter preflight;
- three independent unused one-use releases;
- a release ledger, runnable commands, and an integrity report.

Ceilings are bounded rather than open-ended. BM25 cardinalities are exact;
Qwen's predictable request ceilings equal its preflight plan and its provider
reported-token cap is twice the local model-input proxy ceiling; SkillRouter's
instance, token, and exact-length batch ceilings equal the preflight's current
cache-miss plan. Qwen and SkillRouter each receive a 72-hour hard wall limit,
while BM25 receives six hours. All three use zero automatic retries.

The generated commands consume each release at most once. After all three B1
runs complete, the 12 B1 cells must pass the official validator before any B2
payload or release is created.

No API key or other secret is stored. The Qwen runner reads only the named
`DASHSCOPE_API_KEY` environment variable at execution time.
