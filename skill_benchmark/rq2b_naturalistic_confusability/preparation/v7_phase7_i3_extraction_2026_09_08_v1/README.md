# V7 Phase-7 I3 extraction preparation

Status: `PASS_I3_REUSE_AND_FRESH_INPUTS_PREPARED_PENDING_1368_EXTRACTIONS_AND_FRESH_QA`.

This package is source-only representation work. It contains no query, target, acceptable set, candidate role, review decision or retrieval outcome. It cannot produce a scientific result and does not authorise a selector.

## Exact split

- Current source-hash-unique scope: 3,798.
- Historical V3 extraction rows preserved: 2,433 / 2,431 unique source hashes.
- Source-hash-identical, semantically unambiguous historical extraction payloads rebound as current worker rows: 2,430.
- Fresh extraction: 1,368 rows in 35 immutable input batches (40 rows except the last eight).
- One exact source hash had two different historical extractions; it is deliberately fresh, not arbitrarily selected.

Every reused row was revalidated against the complete current source bytes and exact-substring rules. Reuse means extraction-work reuse only; all 2,430 remain pending fresh current semantic QA.

The package preserves the old final manifest, automatic-integrity report and invalid manual-QA attempt with exact hashes. The historical automatic integrity passed, but the historical 120-row review attempt was explicitly protocol-invalid and wrote no fidelity decision. It is not treated as QA evidence.

## Local input/output locations

The tracked `fresh_assignment_manifest.jsonl` binds each batch to an input hash, V3 instruction hash and unique expected output. Full inputs are regenerated in the ignored `skill_benchmark/cache/rq2b_v7_phase7_i3_extraction_2026_09_08_v1/inputs/`; source text therefore is not duplicated in Git. Worker outputs go only to the paired `outputs/` path and never overwrite another batch.

For an assigned `I3-NNN`, read only its input and `skill_benchmark/extraction_prompts/I3C_SUBAGENT_EXTRACTION_V3.md`; write exactly one V2-schema object per input row in input order. Do not inspect benchmark prompts, labels or other skills. Then run:

```sh
python3 -B skill_benchmark/scripts/validate_rq2b_v7_i3_batch.py I3-NNN
```

The validator checks input hash, row/order/identity/schema, all seven field containers, absent-field equality, warning schema and every evidence substring. A passing batch is still an extraction output, not semantic-QA approval.

## Replay

Initial historical import was exact-hash bound to the preserved local V3 artifacts. Once this package exists, verification uses only the preserved copies and frozen current sources:

```sh
python3 -B skill_benchmark/scripts/prepare_rq2b_v7_i3_extraction.py --verify
```

After all 35 outputs validate, a separate merger must combine 2,430 reused and 1,368 fresh rows, derive matched I3C/I3-flat views, run automatic integrity, and prepare a new unambiguous stratified blinded QA of at least 120 current rows. Only its valid decision can satisfy Phase 7.
