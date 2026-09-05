# RQ1b V3 Wave 028 Capture Quarantine

Date: 2026-08-30  
Status: `QUARANTINED / ZERO SOURCE-FRAME ADMISSION / NO CLUSTER OR RESULT`

## Facts

| Item | Recorded outcome |
| --- | --- |
| M0 navigation | 200 public metadata leads across 14 lanes; four retained `HTTP_403` outcomes. |
| M1 path census | 16 pinned public repositories; 633 visible `SKILL.md` paths. |
| Intended raw roster | 243 unique public raw URLs. |
| Quarantined manifest | 362 records for the 243 URLs; 119 URLs occur more than once. |
| Raw response bytes | 240 unique SHA-256 values among retained success records. |
| Completion report conflict | Report says 243 attempts while manifest has 362 records. |

## Decision

An execution-window detachment allowed an interrupted raw-capture process to
continue after the client stopped observing it. A subsequent resume overlapped
the first process. The protocol requires one attempt per public URL, so this
is an exact-once provenance failure. The full W28 capture stream is retained
but quarantined; it contributes zero source-frame additions and cannot be used
for D1/C1 screening or cluster construction.

## Boundary

This is a capture-integrity outcome only. It neither measures source quality
nor changes the strict cluster total. There is no prompt, gold label,
representation, selector, retrieval score, metric or thesis result.

## Evidence

- `skill_benchmark/rq1b_v3_public_source_frame/d1_source_intake_wave_028_2026-08-30/README.md`
- `.../source_intake_drafts/w28_stratified_skill_paths.jsonl`
- `.../retrieved_public_sources/retrieval_manifest.jsonl`
- `.../retrieved_public_sources/retrieval_report.json`

