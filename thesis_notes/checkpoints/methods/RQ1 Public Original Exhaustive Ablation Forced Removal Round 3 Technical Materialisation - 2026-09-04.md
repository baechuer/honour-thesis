# RQ1 Public-Original Exhaustive Ablation: Forced-Removal Round 3 Technical Materialisation

Date: 2026-09-04

## Status

`TECHNICAL MATERIALISATION COMPLETE / FRESH BLIND CLEARANCE ACTIVE / NO SCORING`

## Purpose and Boundary

Round 3 is a routing-only follow-up to the complete Round-2 clearance ledger.
For a Round-2 `RESIDUAL` card, it deletes only the exact current-card line
spans cited by that ledger. A Round-2 `CLEAR` or `UNCERTAIN` card is copied
byte-for-byte. This can leave a skill incomplete or non-executable. That is
allowed because the intervention tests routing information, not execution.

This checkpoint is implementation-integrity evidence only. It does not prove
that target-field information is absent, freeze a selector denominator, or
report a routing result.

## Deterministic Result

| Item | Count |
| --- | ---: |
| Composition-field units | 574 |
| Candidate cards | 1,855 |
| Round-2 `RESIDUAL` cards changed | 383 |
| Round-2 `CLEAR` cards copied unchanged | 1,464 |
| Round-2 `UNCERTAIN` cards copied unchanged | 8 |
| Exact cited lines deleted | 573 |
| Exact-diff audit failures | 0 |

The materialisation manifest SHA-256 is
`44a479e3f326921006924921e1842365ebd7f008bfe4649e49ac2aed0988e55d`.

## Evidence

- SOP: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/FORCED_REMOVAL_ROUND3_SOP.md`
- Manifest: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/forced_round3_masks/FORCED_ROUND3_MASK_MANIFEST.json`
- Exact-diff audit: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/forced_round3_masks/audit/exact_diff_audit.json`
- Fresh anonymous packets: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/forced_round3_clearance_packets/`
- Canonical fresh-clearance destination: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/forced_round3_clearance/canonical_round3/`

## Next Gate

Fresh reviewers may see only anonymous Round-3 cards and the target-field
name. They must not see sources, prompts, gold labels, maps, earlier ledgers,
selectors, or results. Each returned record must be parent-validated before
canonical ingest. No selector, external API, hosted job, metric calculation or
thesis/PDF result writing may proceed until a later complete-case decision.
