# RQ1b Cross-Source Round 38 M0-C6 Closure

**Date:** 2026-08-28  
**Scope:** Main RQ1b cross-source strict-public curation only.  
**Status:** `C6_FREEZE_PASS_NOT_A_RETRIEVAL_OR_RESULT`

## Boundary

Round 38 curated public original skill artefacts into a possible strict
naturalistic selection benchmark. It did not run BM25, embeddings, a
selector, reranking, an API/provider call, a metric, or a downstream task.
All C3/C4 review evidence is model-assisted, not human annotation. A C6
packet is a curation artefact, not a retrieval result or evidence of implicit
semantic routing.

## M0-M2: Discovery And Source Integrity

- Discovery collected 529 navigation leads. Nineteen malformed leads without
  a source path were quarantined without repair; 510 valid leads canonicalised
  to 378 roots.
- The initial historical-root calculation accidentally included its own output
  as history. The corrected, superseding M0 intake excluded `m0_round38_*`
  outputs and retained 173 historic-root-new roots; the initial outputs are
  preserved but are not a scientific input.
- M1 commit-pinned 150 roots; 23 failed pinning and are non-admissions.
  Blobless census found 15,097 `SKILL.md` paths. The declared 3-64-path cohort
  selected 974 paths from 55 origins; byte staging retained 708 canonical,
  SHA-verified originals from 52 origins, with no staging integrity failure.
- M2 metadata read 708/708 staged originals. Six C0A lanes had at least three
  origins and were eligible for navigation-only composition construction.

## C0-C1: Structural Screening

- C0A proposed five origin-diverse directions. C0B read only their exact
  original sources, retaining three source-backed drafts and rejecting two:
  a broad accessibility testing/design grouping and a Playwright/API testing
  versus Flutter-specific flake-analysis grouping.
- C1 passed all three retained drafts: each has three or four candidates,
  origin diversity, verified source hashes, and no candidate reuse against the
  prior C6 freeze.

## C2-C3: Prompts And Cue Controls

- C2 constructed 20 packets: one direct and one independent paraphrase for
  each of 10 target candidates across the three candidate compositions.
- Literal C3 initially found five copied/near-copied title, source phrase, or
  workflow cues. The five prompt strings were repaired while preserving the
  candidate, target, variant, and status. Final literal audit: 20/20 pass.
- Two independent source-informed C3 slices then recorded construction
  sensitivity for every prompt. The validated ledger has 15 `high`, three
  `medium`, and two `low` residual-risk records (18 `reworded`, two allowed
  ordinary operational-context records). All stored source-evidence strings
  were independently checked as exact original-artifact substrings.
- Parent protocol adjudication retained those model-assisted warnings. Since
  final literal C3 had no identity/title/multi-token copied phrase, it treated
  bounded user-facing operational context as allowed under the frozen protocol,
  retaining `medium` parent risk for the 18 non-low records. This is not a
  semantic-fidelity conclusion.

## C4-C6: Blinded Adequacy And Freeze

- C4 materialised source-deidentified cards and sealed the card-to-skill key.
  Two disjoint pairs of blinded model-assisted reviewers covered ten packets
  each. Their card evidence citations were exact-audited; 36 citation-only
  normalisations repaired Markdown/newline/prefix differences. No adequacy
  judgment or rationale changed.
- C4 outcome: 11 exact-singleton agreements, seven multi-adequate agreements,
  and two reviewer disagreements. Multi-adequate and disagreement packets are
  explicitly non-primary.
- C5 matched all 11 singleton choices to their sealed C2 construction targets.
  C6 rechecked C1 candidate/source-hash alignment, target membership, manual
  C3 coverage, and within-round candidate reuse, then froze three candidate
  compositions and 11 primary strict prompt packets with no integrity failure.

## Cumulative Main-Campaign State

| Item | Before Round 38 | Round 38 addition | After Round 38 |
|---|---:|---:|---:|
| Strict candidate compositions | 62 | 3 | 65 |
| Frozen primary strict prompt packets | 352 | 11 | 363 |
| Non-primary exploratory/disagreement/mismatch packets | 57 | 9 | 66 |

The user-directed next threshold is 75 strict compositions. Ten more are
needed. Continue discovery-first public-source expansion, preserve the same
C0-C6 gates, and do not force multi-adequate or reviewer-disagreement packets
into the strict top-1 stratum.

## Key Artefacts

- Protocol: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/rq1b_cross_source_main_benchmark_protocol_2026-08-26.md`
- Corrected M0 intake: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m0_round38_intake_corrected_summary_2026-08-28.json`
- M1 source inventory: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m1_round38_byte_verified_source_inventory_2026-08-28.jsonl`
- C0B/C1: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c0b_round38_agent_ledger_normalized_2026-08-28.jsonl`, `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c1_round38_integrity_2026-08-28.jsonl`
- C3: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c3_round38_literal_cue_audit_repaired_2026-08-28.json`, `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c3_round38_source_informed_manual_2026-08-28.jsonl`
- C4-C6: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c4_round38_consensus_2026-08-28.json`, `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c5_round38_strata_2026-08-28.jsonl`, `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c6_round38_frozen_primary_2026-08-28.jsonl`
