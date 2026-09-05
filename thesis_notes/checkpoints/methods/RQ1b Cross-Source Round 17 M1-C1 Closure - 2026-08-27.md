# RQ1b Cross-Source Round 17 M1-C1 Closure

Date: 2026-08-27

## Boundary

This checkpoint records public-source discovery, provenance-pinned exact-original
staging, source-only navigation, source-screening, and C1 composition integrity.
It is not a retrieval, representation, embedding, reranking, model/API, metric,
or downstream-task result.

## M1 and M2

- 32 public repositories were commit-pinned and sparse-staged without executing
  any source code.
- 1,704 staged frontmatter-valid bodies were observed. Canonical M1 navigation
  retained 1,322 byte-verified originals from 31 origins after excluding 382
  repeated paths across 362 exact SHA-256 duplicate groups; full duplicate
  provenance remains available in the pre-canonicalisation audit artefacts.
- M2A produced only name, description, and heading navigation fields. It made
  no semantic suitability or cluster claim.
- The combined source-only C0 pool contains 3,223 exact public originals.

## C0A to C1

- C0A created 29 3--4 candidate source-navigation proposals.
- C0B constructed 101 exact-source review copies. The source-screen ledger has
  29 complete rows: 10 source-backed drafts and 19 structural rejects.
- The C0B validator found 101 exact evidence substrings, all present in their
  corresponding packet `SKILL.original.md`, and no identity or JSONL failure.
- C1 passed all 10 retained drafts: 3--4 candidates, at least two origins,
  source hashes intact, unique candidate source hashes, no within-round reuse,
  and no candidate reuse against all prior C6 freezes.

## Current Gate

The 10 C1-passed drafts are eligible for C2 direct/paraphrase construction.
They are not yet prompt packets, gold labels, acceptable sets, strict singleton
decisions, frozen benchmark clusters, or experimental cases. The running frozen
benchmark remains 17 candidate compositions and 106 strict prompt packets.

## Artefacts

- `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m1_round17_staged_source_summary_2026-08-27.json`
- `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m1_round17_staged_source_manifest_2026-08-27.jsonl`
- `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m2a_round17_navigation_summary_2026-08-27.json`
- `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c0_source_pool_round17_summary_2026-08-27.json`
- `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c0b_structural_ledger_round17_2026-08-27.jsonl`
- `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c0b_structural_ledger_round17_validation_2026-08-27.json`
- `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c1_round17_integrity_2026-08-27.jsonl`
- `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c1_round17_integrity_summary_2026-08-27.json`
