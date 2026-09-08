# V7 Phase-7 I1/I2 preparation

Status: `PASS_I1_I2_MECHANICAL_MATERIALISATION_PENDING_PHASE7_QA_AND_I3`.

This is actual local preparation, not an inference run or completed representation QA. It produces 3,798 native-frontmatter I1 rows and 3,798 byte-exact I2 rows using only frozen sources. No labels, prompt text, cluster roles or reviewer rationales enter the materialiser. Historical V3 artifacts are not changed.

`source_view_inventory.jsonl` and `mechanical_report.json` are tracked. The full derived views live under the already-ignored `skill_benchmark/cache/rq2b_v7_phase7_i1_i2_2026_09_08_v1/`; their hashes and exact regeneration script are tracked, avoiding duplicate raw-corpus dumps in Git.

## Reproduce from a clean checkout

Python 3.10+; standard library only; no network or model downloads:

```sh
python3 -B skill_benchmark/scripts/prepare_rq2b_v7_first_matrix.py --verify
python3 -B skill_benchmark/scripts/prepare_rq2b_v7_phase7_i1_i2.py --restore-payloads
python3 -B skill_benchmark/scripts/prepare_rq2b_v7_phase7_i1_i2.py --verify
python3 -B -m unittest discover -s skill_benchmark/scripts -p test_rq2b_v7_preparation.py -v
```

`--restore-payloads` validates the versioned report first and creates only absent derived cache files. Existing files must match exactly; no overwrite/normalisation is permitted. `--verify` is read-only and requires the local payloads. Only `selector_text`, not envelope metadata, is a proposed selector-visible document.

All four narrow tests passed during preparation: exact UTF-8/minimal view envelope, no-overwrite behaviour, full local view/report replay, and approved-plan versus future/inference authority separation. These are mechanical tests, not independent semantic QA.

## What passed and what did not yet pass

- PASS: source identity uniqueness, full source coverage, exact SHA/byte replay, UTF-8 roundtrip, nonempty parsed source-native names/descriptions, existing I1 serializer, deterministic row order, output hash replay.
- NOT YET QA APPROVAL: the inherited frontmatter parser is deliberately limited. Nonempty fields do not prove full YAML fidelity or semantic identity correctness; this remains in representation QA.
- NOT MATERIALISED HERE: I3C/I3-flat; no evidence spans are invented, no old navigation profiles are substituted for extraction.
- STILL REQUIRED: extraction/reuse lineage, matched span-multiset integrity, master-SOP stratified blinded QA, dependency/exposure ledger, exact tokenizer/window and model/budget preflight, final runtime root.

Storage inventory is 19,662,831 UTF-8 bytes / 19,460,827 characters for I2. These are not model token counts, measured inference cost, context-window feasibility or evidence of scalability. Tokenisation and model-specific limits remain a separate local preflight.

An initial read-only inventory of the original workspace's historical `rq2b-i3c-v3-2026-08-18/i3c_merged_final/canonical_extractions.jsonl` found 2,431 current source hashes with an old extraction row and 1,367 without one. Historical file SHA-256: `0f9f1e717e7236c033a093303a03340de739c702023aaf084c18429969b22588`. This is a reuse-investigation lead only: the old file was not imported here and no old extraction or QA status has been adopted as current evidence. Before reuse, restore and hash-replay the historical artifacts and their QA/serializer lineage, check duplicate aliases, then rebind only source-identical rows. Do not report 2,431 rows as current I3 QA-complete.

The controlling new research plan is `thesis_notes/current/RQ2 Approved Research Plan - 2026-09-08.zh-CN.md`. Future 20k-background scale-out does not change this package or its 3,798-source scope.
