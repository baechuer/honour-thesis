# RQ1b Cross-Source Round 39 M0-C6 Closure

**Date:** 2026-08-28  
**Scope:** Main RQ1b cross-source strict-public curation only.  
**Status:** `C6_FREEZE_PASS_NOT_A_RETRIEVAL_OR_RESULT`

## Boundary

Round 39 curated original public skill artefacts into possible strict
naturalistic selection units. It did not run BM25, embeddings, a selector,
reranking, a model provider, a metric, or a downstream task. C3/C4 review
records are model-assisted rather than human annotation. A C6 packet is a
curation artefact, not retrieval performance or evidence of implicit semantic
routing.

## M0-M1: Discovery And Byte-Preserved Sources

- Six public-navigation lanes supplied 157 repository leads and 191 path-hint
  leads. Normalisation retained 147 canonical roots after excluding 82 roots
  already represented in historic intake; 65 roots were net new. This was
  navigation metadata only, not source admission.
- M1 commit-pinned all 65 new roots. Blob-free tree census found 2,109
  `SKILL.md` paths. The bounded 3--64 path selection covered 36 origins and
  843 paths; byte staging retained 698 canonical SHA-verified original skill
  files from 34 origins. Forty-nine exact duplicate source bodies were
  excluded without changing source text.

## C0-C1: Composition And Structural Screening

- C0A used source metadata only and proposed 14 origin-diverse directions.
  C0B reviewers read only the exact copied source packets. Their local
  literal-evidence audit verified all 139/139 cited substrings and retained
  one source-backed draft; 13 directions were structurally rejected.
- C1 passed the single draft: its four candidates retained verified hashes,
  origin diversity, and no reuse against the preceding C6 freezes.

## C2-C3: Prompts And Cue Controls

- C2 constructed eight packets: one direct and one paraphrase for each of the
  four intended targets. All passed C2 structural validation.
- Literal C3 passed 8/8. A separate source-informed, model-assisted review
  recorded construction-sensitivity metadata: six `high` and two `medium`
  residual-risk records. The parent protocol allowed all eight after literal
  cue control, retaining `medium` parent residual risk. These are warnings,
  not human judgments or semantic-fidelity evidence.

## C4-C6: Blinded Adequacy And Freeze

- C4 materialised source-deidentified candidate cards and a sealed
  card-to-skill key. Four disjoint model-assisted reviewers reviewed two
  packet slices. One citation heading marker was normalised from `###` to
  `##` after comparing the blind card to the cited review; no membership,
  adequacy choice, or rationale changed.
- C4 yielded four exact singleton agreements, two multi-adequate packets, and
  two disagreements. Only singleton packets could enter the primary stratum.
- C5 matched all four singletons to their sealed C2 targets. C6 rechecked
  source/hash alignment, candidate membership, C3 coverage, and within-round
  reuse, then froze one candidate composition and four strict primary packets.
  Two multi-adequate and two disagreement packets remain non-primary.

## Cumulative Main-Campaign State

| Item | Before Round 39 | Round 39 addition | After Round 39 |
|---|---:|---:|---:|
| Strict candidate compositions | 65 | 1 | 66 |
| Frozen primary strict prompt packets | 363 | 4 | 367 |
| Non-primary exploratory/disagreement/mismatch packets | 66 | 4 | 70 |

The current user-directed goal is 75 strict compositions, leaving nine more.
The next cohort must begin with new public-source discovery, retain strict
3--4-candidate cross-source construction, and preserve C0--C6. Do not force
weak, multi-adequate, or reviewer-disagreement groups into the primary set.

## Key Artefacts

- Protocol: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/rq1b_cross_source_main_benchmark_protocol_2026-08-26.md`
- M0 intake: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m0_round39_intake_summary_2026-08-28.json`
- M1 inventory: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m1_round39_byte_verified_source_inventory_2026-08-28.jsonl`
- C0B/C1: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c0b_round39_agent_ledger_normalized_2026-08-28.jsonl`, `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c1_round39_integrity_2026-08-28.jsonl`
- C3: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c3_round39_literal_cue_audit_2026-08-28.json`, `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c3_round39_source_informed_manual_2026-08-28.jsonl`
- C4-C6: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c4_round39_consensus_2026-08-28.json`, `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c5_round39_strata_2026-08-28.jsonl`, `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c6_round39_frozen_primary_2026-08-28.jsonl`
