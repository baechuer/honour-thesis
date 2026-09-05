# RQ1b Cross-Source Round 36 M1-M2 Closure

Date: 2026-08-28

## Boundary

This checkpoint records commit pinning, blobless tree census, bounded local
original-byte staging, byte verification, and navigation metadata only. It
does not record a candidate composition, prompt, gold label, acceptable-set
judgement, embedding, selector call, retrieval score, metric, or result.

## M1

- The first sandbox-only probe attempt failed uniformly before DNS resolution.
  That environment failure is preserved separately and was not treated as 51
  repository non-admissions.
- Under real network access, 50/51 fresh roots were pinned to `HEAD` commits;
  one failed pin remains a recorded non-admission without automatic retry.
- Blobless census completed for all 50 pinned roots and found 2,809
  `SKILL.md` paths. The predeclared 3--64 path bound selected 34 origins and
  602 paths for local staging; the other completed roots are unselected, not
  rejected for quality.
- Local staging completed with zero stage failures. Byte rehashing retained
  477 canonical originals from 32 origins after exact-byte de-duplication.
  `integrity_failures=[]`.

## M2

- M2 derived only frontmatter name/description and heading previews from all
  477 preserved originals. All 477 records had source-provided frontmatter
  name and description; 473 had heading previews. `integrity_failures=[]`.

## Next Gate

Round 36 C0A may use only provenance-partitioned navigation queues to propose
3--4-candidate directions. It must not claim source-backed peerhood. Each
proposal must subsequently pass source-isolated C0B, C1 integrity, cue-safe
C2/C3, two source-deidentified model-assisted blinded C4 reviews, C5, and C6
before it changes the frozen strict benchmark count.

## Evidence

- M1: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m1_round36_byte_verified_source_inventory_summary_2026-08-28.json`
- M2: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m2a_round36_navigation_summary_2026-08-28.json`
- Sandbox transport record: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m1_round36_sandbox_dns_transport_failure_2026-08-28.json`
