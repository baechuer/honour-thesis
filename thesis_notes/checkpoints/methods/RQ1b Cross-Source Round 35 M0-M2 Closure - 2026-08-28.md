# RQ1b Cross-Source Round 35 M0-M2 Closure

Date: 2026-08-28

## Boundary

This checkpoint records discovery, provenance pinning, local byte staging,
byte-integrity verification, and source-navigation metadata only. It does not
record a candidate composition, prompt, gold label, acceptable-set judgement,
embedding, selector call, retrieval score, metric, or empirical result.

## M0-M1

- Public GitHub repository-search discovery recorded 697 navigation leads and
  retained 691 exact-new roots after six prior-root exclusions.
- M1 commit-pinned all 691 roots. Blobless tree census completed for 435 roots,
  kept 256 fetch failures as durable non-admissions without automatic retry,
  and recorded 17,601 `SKILL.md` paths.
- The predeclared bounded 3--64-path selection admitted 140 origins and 2,411
  paths into 47 independent three-source staging batches. Every batch completed
  with zero staging failure; no source content was executed.
- Final byte-integrity rehashing retained 2,158 canonical original artefacts
  from 134 origins. It excluded 128 missing-frontmatter paths and 125
  exact-byte duplicates from navigation. No integrity failure was found.

## M2 and C0A Preparation

- M2 extracted only source-provided frontmatter names/descriptions and heading
  previews from all 2,158 retained originals. It made no similarity judgement.
- The Round 35 C0 pool contains the same 2,158 provenance-preserved navigation
  records. The C0A anti-overlap partition uses the exact M0 discovery-query
  provenance lane rather than semantically remapping a source: broad agent
  skills (439 records), Claude Code skills (332), Codex skills (277), documents
  and creative (301), data and research (168), product and collaboration (168),
  business operations (136), software systems (152), OpenAI skill format (156),
  and scientific specialist (29).
- An initial C0A lane implementation could not parse the new Round 35 discovery
  ID format. It was fixed locally, compiled, and coverage-tested against all
  691 new roots before the lane files were materialised. This was a local
  navigation implementation repair; it did not alter source artefacts or
  scientific inputs.

## Next Gate

Independent C0A workers may propose only navigation-level 3--4-candidate
directions inside disjoint provenance lanes. C0B must later read the exact
source packets without receiving prompts, labels, results, or C0A envelope
arguments. A C0A proposal is not a source-backed draft or a valid cluster.

## Evidence

- M0: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m0_round35_intake_summary_2026-08-28.json`
- M1 final: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m1_round35_byte_verified_source_inventory_summary_2026-08-28.json`
- M2: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m2a_round35_navigation_summary_2026-08-28.json`
- C0 pool: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c0_round35_source_pool_summary_2026-08-28.json`
- C0A lanes: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c0a_round35_lane_summary_2026-08-28.json`
