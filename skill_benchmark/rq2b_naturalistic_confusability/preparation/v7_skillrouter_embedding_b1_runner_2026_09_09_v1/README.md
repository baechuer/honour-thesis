# V7 SkillRouter embedding B1 runner v1

Status: `IMPLEMENTED_ZERO_INFERENCE_AWAITING_FINAL_PHASE8_PAYLOAD_AND_ROOT_RELEASE`.

The implementation prepares the executable boundary for B03, B06, B09 and
B12 only. It has not loaded a model, made a forward pass, called a network, or
read an acceptable set, target, judgement, reviewer return or selector result.

The runner has one scientific-data intake: a later Phase-8 payload named by a
one-use root-release authorisation. The payload must bind the exact label-free
query runtime, source manifest, first-matrix conditions, and all four final
representation artifacts. I1/I2 are bound only to the authoritative
`rq2b_v7_phase7_i1_i2_2026_09_09_v2` artifacts: I1 SHA-256
`0fc34abe8ca3f5d23bcc563f496831e37628491ddc65caeb9c7a284d5d1ff8dd`
and I2 SHA-256
`8860e415fa7ae6718e5e2b6ca3e57605150120f30a8414e6c6931a99355952ec`.
The final V4.1 I3C-fielded and I3-flat paths and hashes are intentionally
absent from the runner and must be supplied by the final Phase-8 payload with
`extraction_protocol=I3C_SUBAGENT_EXTRACTION_V4_1` and
`phase8_final=true`.

## Runtime contract

- model `pipizhao/SkillRouter-Embedding-0.6B`, revision
  `c03c9bcee9fce92ab0262bb6dcf54d174a8ba558`, with all local snapshot files
  checked against the runtime-preflight hashes;
- exact released query instruction, last non-padding token pooling, exactly
  1,024 finite coordinates, and L2-normalised cache vectors;
- MPS bfloat16 with default SDPA only; CPU, float16, float32 and eager are not
  silent substitutes;
- complete exact-substring Markdown windows of at most 7,500 content tokens
  and at most 256 content-token overlap, both counted by
  `tokenizer.encode(..., add_special_tokens=false)`, followed by maximum
  query-to-window cosine per source;
- a separate model-input binding for every query/window using
  `add_special_tokens=true`: its actual token IDs, SHA-256 and length are
  cached and audited, may exceed the content count by tokenizer specials, and
  must remain at or below the checkpoint limit of 32,768;
- exact actual model-input-token-length buckets, at most 16 rows,
  `padding=false`;
- descending score with ascending `source_sha256` for exact ties; Top-100 rows
  use `rq2b-v7-b1-runner-output-v1` and bind their ordered Top-20;
- no automatic retries. Started/completed forward receipts, immutable exact
  cache entries, cache inventory, separated offline/online cost ledger and a
  unique attempt directory are retained. A failure preserves its receipts and
  staging state and produces no completed scientific package.

Each B1 output row reports only the online query path: one logical query input
in `window_forwards`, that query's special-inclusive model-input token count,
query-only initial cache hit (0 or 1), and query embedding plus scoring wall
time. It never repeats the 3,798-document/window preprocessing cost on every
query row. Document windows, document cache hits/misses and document token
work remain in the receipt's `cost.offline` ledger; actual combined model
instances/batches/tokens remain in `cost.execution`. The online ledger records
both uncached query token work and the logical all-query input total.

## Required later bindings

The payload schema is
`rq2b-v7-skillrouter-embedding-b1-phase8-payload-v1`. It must contain only:

1. runner and exact-chunker paths/hashes;
2. a PASS Phase-8 receipt path/hash and
   `final_v4_1_i3_hashes_bound=true`;
3. the three fixed authority artifacts plus four representation artifacts;
4. the exact method dictionary enforced in `validate_payload`;
5. the frozen counts and label-isolation declaration.

The authorisation schema is
`rq2b-v7-skillrouter-embedding-b1-root-release-v1`. An executable record must
use state
`EXPLICITLY_AUTHORISED_FOR_ONE_PHASE8_ROOT_RELEASED_EXECUTION` and bind the
payload SHA, Phase-8 receipt SHA, explicit approval of the existing window
amendment, the pinned snapshot path and file hashes, exact runtime, unique
run/attempt/root-release IDs, cache/output/attempt directories under
`skill_benchmark/cache/`, and ceilings for new cache entries, model input
instances/tokens, forward batches and wall time. A pending template is not an
authorisation.

There is deliberately no example containing invented I3 hashes. The release
producer should derive them from the final Phase-8 representation artifacts,
write a new payload, compute its SHA-256, and then issue a separate one-use
root release.

## Zero-inference checks

From the clean repository root:

```sh
.venv-rq2b-v7/bin/python -B skill_benchmark/scripts/run_rq2b_v7_skillrouter_embedding_b1.py --self-test
.venv-rq2b-v7/bin/python -B skill_benchmark/scripts/test_rq2b_v7_skillrouter_embedding_b1.py
PYTHONPYCACHEPREFIX=/private/tmp/rq2b-skillrouter-b1-pycache .venv-rq2b-v7/bin/python -B -m py_compile skill_benchmark/scripts/run_rq2b_v7_skillrouter_embedding_b1.py skill_benchmark/scripts/test_rq2b_v7_skillrouter_embedding_b1.py
git diff --check
```

Only after the later payload and root release exist is the execution entrypoint
syntactically available:

```sh
.venv-rq2b-v7/bin/python -B skill_benchmark/scripts/run_rq2b_v7_skillrouter_embedding_b1.py \
  --execute --authorisation path/to/one_use_root_release.json
```

Do not run that command from this implementation task. The completed B1 gzip
can later be checked without labels using
`validate_rq2b_v7_runner_outputs.py --allow-incomplete` with an empty B2 file.
