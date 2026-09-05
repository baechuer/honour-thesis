# RQ1b Cross-Source Round 41 M0-C6 Closure

**Date:** 2026-08-28  
**Scope:** Main RQ1b cross-source strict-public curation only.  
**Status:** `C6_FREEZE_PASS_NOT_A_RETRIEVAL_OR_RESULT`

## Boundary

Round 41 curated exact-byte-preserved public original skill artefacts into
possible strict naturalistic selection units. It did not run BM25, embeddings,
a selector, reranking, an external model/API, a metric, or a downstream task.
C3/C4 records are model-assisted rather than human annotation. A C6 packet is
a curation artefact, not retrieval performance, semantic fidelity, or evidence
of implicit semantic routing.

## M0-M1: Aggregate Source Pool And Exact Originals

- M0 retained 124 valid navigation leads, 121 canonical leads, and 36 new
  roots after prior-root exclusion. M1 commit-pinned and byte-staged 157
  canonical original artefacts from nine origins; three source records were
  non-admitted.
- To support cross-source construction, an existing SHA-preserved corpus was
  aggregated without treating a source count as a cluster count: 29,554 raw
  rows reduced to 19,083 unscreened original artefacts from 737 origins after
  excluding 881 previously reviewed or frozen candidate identities.

## C0-C3: Source Screening And Cue Control

- Aggregate C0A proposed seven structurally valid directions. Exact-source
  C0B verified all 44 retained evidence substrings, rejected three structural
  non-peer, container, or asymmetric directions, and retained four
  source-backed triads. C1 passed all four for source hashes, origin diversity,
  candidate size, and prior-C6 candidate non-reuse.
- C2 created 24 direct/paraphrase packets. Automatic literal cue screening
  passed after declared revisions. The initial semantic C3 review marked 16
  prompt constructions as source-specific workflow/output combinations. A
  first minimal rewrite and independent recheck cleared 13; three paper-to-
  presentation prompts then received a second minimal rewrite and independent
  post-review. The immutable final C3 lineage contains 24 allowed records,
  with exact source-evidence validation and 17 low / 7 medium residual-risk
  records. Prior dispositions are retained separately and were not overwritten.

## C4-C6: Blind Review, Strata, And Freeze

- Two independent source-deidentified model-assisted C4 reviewers each
  evaluated all 24 anonymous three-card packets. The pre-unseal evidence audit
  passed with 18 exact singleton agreements, three multiple-adequate
  agreements, and three disagreements.
- C5 confirmed all 18 agreed singletons matched their sealed C2 targets. C6
  rechecked C1 hashes, candidate composition, candidate reuse, literal C3
  status, final manual C3 coverage, and sealed C4/C5 chain. It froze three
  candidate compositions and 18 strict primary packets. The three
  multiple-adequate packets remain exploratory; the three disagreements remain
  non-primary.

## Cumulative Main-Campaign State

| Item | Before Round 41 | Round 41 addition | After Round 41 |
|---|---:|---:|---:|
| Strict candidate compositions | 69 | 3 | 72 |
| Frozen primary strict prompt packets | 383 | 18 | 401 |
| Non-primary exploratory/disagreement/mismatch packets | 72 | 6 | 78 |

The user-directed target is 75 strict candidate compositions, leaving three.
The next cohort must begin with fresh public-source discovery and preserve the
strict 3--4-candidate cross-source, C0--C6 protocol. Do not force
multiple-adequate or reviewer-disagreement packets into strict top-1 merely to
reach the numerical target.

## Key Artefacts

- Protocol: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/rq1b_cross_source_main_benchmark_protocol_2026-08-26.md`
- M1 inventory: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m1_round41_byte_verified_source_inventory_2026-08-28.jsonl`
- C1: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c1_round41_integrity_2026-08-28.jsonl`
- Final C3 lineage: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c3_round41_final_semantic_lineage_validated_2026-08-28.jsonl`
- C4-C6: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c4_round41_blind_consensus_preunseal_2026-08-28.json`, `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c5_round41_strata_2026-08-28.jsonl`, `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c6_round41_frozen_primary_2026-08-28.jsonl`
