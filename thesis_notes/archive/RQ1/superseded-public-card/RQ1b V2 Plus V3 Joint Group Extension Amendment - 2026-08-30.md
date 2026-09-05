# RQ1b V2+V3 Joint Group Extension Amendment

<!-- RQ1-RECORD-STATUS:START -->
> **RQ1 record status (2026-09-04): `HISTORICAL_OR_SUPERSEDED`.** Retained for provenance and method history. Do not use its dated status, denominator, or result as the current RQ1 claim unless the canonical RQ1 index explicitly carries it forward. Canonical index: `thesis_notes/current/RQ1/README.md`.
<!-- RQ1-RECORD-STATUS:END -->



Status: `BM25 + QWEN COMPLETE / SUPPORTING RESULT / THESIS PDF UNCHANGED`

Date: 2026-08-30

## Purpose

Extend the already completed V2 joint-field supporting analysis to the four
complete V3 triads. This does **not** replace the primary V2+V3 single-field
experiment. It tests whether removing complementary groups of operational
information produces a clearer routing-loss signal than removing one field.

## Conditions

Every candidate in a V3 composition receives the same group-specific marker in
each withheld slot. All other slots remain byte-identical to V3 `FULL`.

| Group condition | Withheld fields | V2 eligible families | New V3 families | Combined families / prompts |
| --- | --- | ---: | ---: | ---: |
| `MASK_TASK_SPECIFICATION` | use condition + input/precondition + output/artifact | 73 | 12 | 85 / 170 |
| `MASK_EXECUTION_VERIFICATION` | workflow/procedure + success/verification | 77 | 12 | 89 / 178 |
| `MASK_APPLICABILITY_CAPABILITY` | boundary/not-for + dependency/resource | 70 | 12 | 82 / 164 |

The V2 eligibility sets are immutable and come from
`working/field_type_joint_mask_v21_2026-08-29/joint_mask_freeze.json`.
All 12 V3 families are eligible because their imported seven-slot cards carry
the required, candidate-synchronous group-mask materialisation.

## Execution Sequence

1. Materialise and hash the 12 V3 `FULL` plus 36 V3 joint-group candidate
   cards; validate candidate membership, unchanged non-withheld slots and exact
   marker placement.
2. Reuse exact V3 `FULL` result rows after manifest/hash verification; score
   only the 72 new V3 mask prompt rows locally with BM25.
3. Combine each group with the frozen V2 joint-group output using only that
   group's immutable eligibility set. Each group remains a separate paired
   comparison; `FULL` rows therefore legitimately recur across groups.
4. Run composition-level paired bootstrap: average direct/paraphrase and any
   multiple families within a composition, then resample compositions 5,000
   times. Report Top-1, MRR, gold rank, native margin and transition counts.
5. Produce a local Qwen preflight. It may reuse 24 query and 12 V3 `FULL`
   embeddings from the exact-text cache, but it must identify the 36 new
   group-mask card texts and require a fresh exact-payload authorisation before
   any provider request.

## Boundaries

- The group extension is a supporting field-set availability analysis; it does
  not identify a universally decisive individual field.
- V2/V3 rows are one group-specific estimator after combination, while their
  row-level source tag remains for provenance and heterogeneity audit.
- No thesis LaTeX/PDF result is written before review.

## Local BM25 Result

The local run passed source-manifest hashes, candidate membership, exact V2
eligibility reuse, V3 condition hashes and paired row-coverage checks. It
reused 696 V2 joint-mask rows, scored 96 V3 rows, and produced 1,024 rows
across three deliberately separate comparisons. A `FULL` row is repeated only
because each group has a different frozen eligibility denominator.

| Group | Families / prompts / compositions | FULL Top-1 -> masked | Mean composition Top-1 delta [95% bootstrap CI] | FULL MRR -> masked | Mean margin delta [95% bootstrap CI] |
| --- | ---: | ---: | ---: | ---: | ---: |
| Task specification | 85 / 170 / 41 | 0.6765 -> 0.5941 | +0.0965 [+0.0081, +0.1911] | 0.8265 -> 0.7789 | +1.6072 [+0.9590, +2.2659] |
| Execution / verification | 89 / 178 / 44 | 0.7022 -> 0.6348 | +0.0511 [-0.0019, +0.1032] | 0.8399 -> 0.7978 | +1.1082 [+0.6022, +1.6514] |
| Applicability / capability | 82 / 164 / 41 | 0.6646 -> 0.6402 | +0.0356 [-0.0437, +0.1270] | 0.8186 -> 0.8054 | +0.5680 [+0.1185, +1.0379] |

The task-specification set has a positive composition-bootstrap Top-1 interval.
Execution/verification is strongest in native BM25 margin and has a positive
MRR interval; applicability/capability has a positive margin interval but no
stable Top-1 or MRR effect. These are *joint availability* results: they cannot
identify which member field caused a change or replace the primary V2+V3
single-field analysis.

## Qwen Dense-Retrieval Twin

The preflight established that all 24 V3 prompts and all 12 V3 `FULL` cards
already had exact-text cache entries. The authorised execution sent only 36
new group-mask candidate cards (4,166 local lexical-token proxy; 30,138 UTF-8
bytes) to `text-embedding-v4` at 1024 dimensions. It completed four of four
no-retry calls and used 6,428 provider tokens. No query text or existing V3
`FULL` card was transmitted. The exact payload SHA-256 was
`5d08375f048161cda73abba0792d8f05e14f7eced69fd21379027e68a12cdc33`.

| Group | FULL Top-1 -> masked | Mean composition Top-1 delta [95% bootstrap CI] | FULL MRR -> masked | Mean margin delta [95% bootstrap CI] |
| --- | ---: | ---: | ---: | ---: |
| Task specification | 0.8471 -> 0.7765 | +0.0874 [-0.0091, +0.1961] | 0.9186 -> 0.8725 | +0.0258 [+0.0078, +0.0444] |
| Execution / verification | 0.8371 -> 0.7753 | +0.0634 [+0.0038, +0.1269] | 0.9120 -> 0.8811 | +0.0061 [+0.0000, +0.0118] |
| Applicability / capability | 0.8415 -> 0.8293 | +0.0244 [-0.0244, +0.0772] | 0.9167 -> 0.9065 | +0.0059 [-0.0003, +0.0122] |

Qwen corroborates a reliable joint execution/verification effect across Top-1,
MRR and margin. Task specification reliably reduces MRR and margin but has an
unstable Top-1 interval in this corpus; applicability/capability is not stable
under Qwen. The agreement is partial rather than universal, which is the
appropriate conclusion for this supporting analysis.

## Result Files

- Materialisation freeze: `skill_benchmark/rq1b_cross_source_public_benchmark/working/rq1b_v2_v3_joint_group_extension_2026-08-30/`
- Local runner: `skill_benchmark/scripts/run_rq1b_v2_v3_joint_group_extension.py`
- BM25 result: `skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_joint_mask_v21_v3_extension_2026-08-30/bm25/`
- Qwen local preflight: `skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_joint_mask_v21_v3_extension_2026-08-30/qwen_preflight/`
- Qwen result: `skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_joint_mask_v21_v3_extension_2026-08-30/qwen/`
