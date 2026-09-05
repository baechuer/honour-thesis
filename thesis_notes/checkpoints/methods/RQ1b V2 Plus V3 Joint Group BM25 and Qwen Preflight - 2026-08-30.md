# RQ1b V2+V3 Joint-Group Extension Checkpoint

Date: 2026-08-30

Status: `BM25 + QWEN COMPLETE / SUPPORTING RESULT / THESIS UNCHANGED`

## What This Tests

This supporting RQ1b analysis removes complementary information sets from all
candidates in the same natural public-skill composition. It asks whether the
availability of a *set* of operational information produces a clearer routing
loss than a single-field mask. It does not establish that any individual field
is uniquely causal.

The three comparisons remain separate: each compares `FULL` to one group mask,
using the V2 group-specific frozen eligibility intersection plus all 12
complete V3 routing families. `FULL` rows therefore recur across comparisons by
design; they are never pooled into a fictitious common denominator.

## Local Completion

| Item | Value |
| --- | ---: |
| V3 group-mask cards materialised | 36 |
| V2 rows hash-verified and reused | 696 |
| New V3 local BM25 rows | 96 |
| Rows across the three separate analyses | 1,024 |
| Network calls / external texts | 0 / 0 |

All source, card, mask, eligibility and output hashes passed. The local BM25
summary is recorded in the linked amendment. The current directional evidence
is strongest for task specification (Top-1 and margin) and for
execution/verification (MRR and margin). Applicability/capability only retains
a stable margin loss. This is not yet a dense-retrieval conclusion.

## Qwen Completion

The exact V3 `FULL` and prompt embeddings were cached locally. The Qwen twin
sent exactly 36 newly rendered group-mask cards, completed four no-retry
requests and consumed 6,428 provider tokens. No query or `FULL` text was sent.
Its payload SHA-256 is
`5d08375f048161cda73abba0792d8f05e14f7eced69fd21379027e68a12cdc33`.

After output-hash and row-coverage validation, Qwen has 1,024 group-analysis
rows (340 task-specification, 356 execution/verification, 328
applicability/capability). Execution/verification has positive
composition-bootstrap 95% intervals for Top-1 (`+0.0634`), MRR (`+0.0341`) and
margin (`+0.0061`). Task specification has positive MRR/margin intervals but
an inconclusive Top-1 interval; applicability/capability is inconclusive. This
does not convert the supporting joint-field test into a universal causal claim.

## Evidence

- [Joint-group amendment](/Users/jackyzhang/Work/Honour%20Thesis/thesis_notes/archive/RQ1/superseded-public-card/RQ1b%20V2%20Plus%20V3%20Joint%20Group%20Extension%20Amendment%20-%202026-08-30.md)
- [BM25 summary](/Users/jackyzhang/Work/Honour%20Thesis/skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_joint_mask_v21_v3_extension_2026-08-30/bm25/summary.json)
- [Qwen payload](/Users/jackyzhang/Work/Honour%20Thesis/skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_joint_mask_v21_v3_extension_2026-08-30/qwen_preflight/payload.json)
