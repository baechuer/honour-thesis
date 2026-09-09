# V7 Phase-8 final execution-root builder

Status: `IMPLEMENTED_AWAITING_FINAL_V4_1_5_QA_V6_RETURN_FREEZE`.

The exact zero-inference builder/test freeze is recorded in
`integrity_report.json`; its prose boundary is mirrored in
`integrity_report.md`.

`build_rq2b_v7_phase8_execution_root.py` is a zero-inference finaliser. It does
not run BM25, providers, embedding/reranking models, validators that could open
results, or offline analysis. The V4.1 warning disposition, V4.1.5 full-corpus
repair, and fresh QA v6 packet now exist. Formal root creation remains blocked
until three independent QA v6 return sets pass the frozen finalizer. The
Phase-8-compatible BM25 v2, Qwen embedding v3, SkillRouter embedding v1, Qwen
reranker v1 and SkillRouter reranker v1 runners now exist, but remain inert
until the final root binds their exact hashes and a later one-use release is
explicitly authorised. No legacy payload, representation or runner is silently
substituted.

## Intake and gates

Already approved authorities are closed-intake constants with exact paths and
SHA-256 values: the approved plan and master SOP, final 1,077-group library
freeze, source and matrix manifests, U0323 exclusion evidence, analysis freeze,
I1/I2 v2, runtime inventory, Qwen B1 preflight lineage, official output schemas
and label-free validator. The final prompt manifest, exclusion ledger, offline
label adapter and reviewed-neighbour ledger are opaque review-provenance files:
the builder only streams their bytes for SHA-256 and records byte size. It never
parses, counts, searches, copies or interprets their contents.

The explicit `--bindings` file must supply exact canonical path+SHA pairs for:

- V4.1 selection report/ledger, warning build/final reports and disposition
  ledger, the preserved failed QA v4 and v5 lineages, the V4.1.4 intermediate
  repair, and the final V4.1.5 merge manifest and I3 views;
- the fresh V4.1.5 QA v6 packet and final PASS report;
- the 7,500-content-token/256-overlap method amendment and a separate explicit
  approval record that is not itself execution authority. The template points
  to the versioned
  `v7_skillrouter_embedding_window_approval_2026_09_09_v1/method_approval.json`
  path, but its SHA-256 must still be supplied explicitly with the final
  bindings;
- final split, cue, duplication, semantic-near-copy and coverage PASS reports;
  each uses `rq2b-v7-phase8-quality-gate-v2`, binds the source union, prompt
  manifest, exact counts, a gate-specific all-PASS assertion roster, replayed
  path/hash evidence and the exact quality-builder implementation. Split, cue,
  duplication and semantic-near-copy reports additionally bind an opaque final
  adjudication receipt; aggregate prose or the earlier six-field v1 placeholder
  cannot satisfy this contract; and
- five Phase-8-compatible runners. Each script is inspected with Python AST
  only and must expose literal `RUNNER_VERSION`, `PAYLOAD_SCHEMA` and
  `AUTHORISATION_SCHEMA` constants. The two SkillRouter runners must also expose
  literal `MODEL`, `REVISION` and `MODEL_FILE_SHA256` values identical to the
  replayed runtime inventory. The builder never accepts an alternate
  self-consistent path or falls back to an earlier job.

The builder recomputes every supplied hash and cross-checks selection, warning,
merge and QA lineage. It reads only source identities and selector-visible
representation structure to prove exact 3,798-source coverage. A warning-final
state other than
`PASS_ALL_WARNINGS_SOURCE_ONLY_DISPOSITIONED_PENDING_MERGE_AND_BLINDED_QA`, or
a fresh QA v6 state other than `PASS_CURRENT_I1_I3_SEMANTIC_QA` with
`formal_execution_ready=true`, raises before the output directory is created.

## Output boundary

On a valid future intake, the builder creates a new versioned package with:

- `root_manifest.json` and `root_manifest.sha256`;
- `phase8_readiness_receipt.json`;
- `FORMAL_EXPERIMENT_READINESS_REPORT.md`;
- a traceable `build_attempt.json`; and
- five `authorisations/*.pending.json` templates for BM25 B1, Qwen B1,
  SkillRouter B1, Qwen B2 and SkillRouter B2.

`READY_FOR_FORMAL_EXPERIMENT` is readiness, not execution permission. Every
template has `execution_authorised=false`, a PENDING state and null release
fields. A later explicit user decision must bind a unique run/attempt identity,
an exact label-free payload, destinations and ceilings. B2 templates also
require complete persisted B1 Top-20 artifacts plus a fresh official B1
validation receipt. The builder never turns a template into an authorisation.

## Safe commands

Print the incomplete bindings skeleton (stdout only):

```sh
python3 -B skill_benchmark/scripts/build_rq2b_v7_phase8_execution_root.py \
  --print-bindings-template
```

Run synthetic checks only:

```sh
python3 -B skill_benchmark/scripts/build_rq2b_v7_phase8_execution_root.py --self-test
python3 -B skill_benchmark/scripts/test_build_rq2b_v7_phase8_execution_root.py
```

Future materialisation requires a new output path and a completed explicit
bindings file:

```sh
python3 -B skill_benchmark/scripts/build_rq2b_v7_phase8_execution_root.py \
  --root /ABSOLUTE/CLEAN/REPOSITORY \
  --bindings skill_benchmark/cache/EXPLICIT_PHASE8_BINDINGS.json \
  --output-dir skill_benchmark/rq2b_naturalistic_confusability/preparation/RQ2b-NC-final-YYYY-MM-DD-vN
```

This command still does not run a selector or authorise a later run. It refuses
to overwrite an existing package and preserves a staging attempt if a write
fails after all gates pass.
