# RQ1b Cross-Source Round 16 C0A-C6 Closure and Round 17 M0 Discovery

**Date:** 2026-08-27  
**Status:** Round 16 C6 frozen; Round 17 discovery-first M0 complete; no RQ1b retrieval experiment run.

## Scope Boundary

Round 16 used only already pinned and locally staged public skill artefacts.
No source code was executed; no retrieval, embedding, reranking, external API,
metric, or downstream task was run. All C0--C6 records below are curation and
benchmark-admission evidence only.

## Round 16 C0A-C1

- C0A navigation-level proposals:
  `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c0a_source_agnostic_proposals_round16_2026-08-27.jsonl`
- C0B exact source packet queue:
  `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c0b_round16_source_queue_2026-08-27.jsonl`
- C0B ledger and verified summary:
  `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c0b_structural_ledger_round16_2026-08-27.jsonl`,
  `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c0b_round16_summary_2026-08-27.json`
- Seven C0A proposals: four source-backed structural passes and three
  structural rejects. The passes were codebase assessment, data orchestration,
  event automation, and PDF preparation.
- C1 passed all four retained compositions with no candidate reuse against the
  previously frozen C6 sets:
  `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c1_integrity_round16_2026-08-27.jsonl`.

## Round 16 C2-C3

- 24 direct/paraphrase drafts, six per composition:
  `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c2_prompt_drafts_round16_2026-08-27.jsonl`.
- The first literal audit found five exact-name/phrase review items. They were
  reworded solely to remove literal source overlap; changes are logged in:
  `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c2_c3_round16_revision_log_2026-08-27.md`.
- C3 v2 passed all 24 mechanically:
  `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c3_round16_literal_cue_audit_v2_2026-08-27.json`.
- Manual semantic review and its one-row-per-prompt companion:
  `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c3_round16_manual_semantic_cue_audit_2026-08-27.md`,
  `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c3_round16_manual_semantic_disposition_2026-08-27.jsonl`.
- C3 permits explicit operational context but does not claim cue-free prompts
  or prove natural implicit routing.

## Round 16 C4-C6

- Source-deidentified reviewer cards and sealed key:
  `skill_benchmark/rq1b_cross_source_public_benchmark/review_packets/c4_round16_v1_2026-08-27/`.
- Two independent model-assisted blind reviewers per packet reached 24/24
  exact singleton agreement; no reviewer was given source identities, key,
  labels, retrieval inputs, or results.
- A manual transcription error in the v1 normalisation swapped four anonymous
  card labels. C5 caught it as a sealed-intent mismatch before freeze. The
  v1 material remains as a superseded audit artefact; the correction is
  documented in `TRANSCRIPTION_CORRECTION_V2.md` and validated via
  `c4_round16_v2_combined_consensus_2026-08-27.json`.
- Corrected C5:
  `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c5_round16_v2_strata_summary_2026-08-27.json`
  reports 24 strict singletons, zero failures.
- Corrected C6:
  `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c6_round16_v2_primary_freeze_summary_2026-08-27.json`
  reports 4 frozen candidate compositions and 24 frozen primary packets,
  zero failures.

## Claim Discipline

The C4 reviewers recorded high directness for at least one reviewer on every
Round 16 prompt. These packets are usable strict public-artifact curation
cases under explicit operational constraints. They are **not** evidence that
implicit, underspecified natural language can be routed equally well, nor any
retrieval/embedding/reranking result.

## Running Total

- Prior frozen primary: 13 compositions / 82 strict prompt packets.
- Round 16 addition: 4 compositions / 24 strict prompt packets.
- Current frozen primary curation total: **17 compositions / 106 strict prompt packets**.

## Round 17 Discovery-First Status

`skill_benchmark/rq1b_cross_source_public_benchmark/manifest/discovery_round17_cross_domain_2026-08-27.md`
records 30 deduplicated public-source leads. This is M0 discovery only. The
next valid action is a bounded M1 selection, public commit pinning, sparse
artefact staging, and byte-duplicate screening before any Round 17 C0A work.
