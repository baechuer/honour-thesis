# RQ1b Cross-Source Round 37 M0-M2 Closure

Date: 2026-08-28

## Boundary

This checkpoint records public-source discovery, provenance pinning, local
byte staging, and navigation metadata only. It creates no candidate
composition, prompt, label, adequacy decision, retrieval input, embedding,
reranking, model/API result, metric, or downstream-task result.

## M0 Discovery

- Eight independent discovery lanes recorded 264 public navigation leads. Local
  canonicalisation yielded 82 repository roots; 52 are exact roots already
  recorded in historic M0 manifests, leaving 30 exact-new roots.

## M1 Pin, Census, and Staging

- The initial sandbox probe failed 30/30 before GitHub hostname resolution. It
  is preserved as a uniform transport failure, not as 30 repository failures.
  One real no-retry HEAD probe then pinned 29 roots; one repository-not-found
  root remains a durable non-admission.
- Blob-filtered pinned-tree census completed for all 29 sources and counted
  852 `SKILL.md` paths. The declared 3--64 path rule selected 11 origins with
  273 paths. Local source-only staging materialised only those paths and their
  visible root licence files, never executing them.
- The stage preserved 216 canonical, hash-verified originals from 11 origins.
  The remaining selected paths were excluded by exact-byte duplicate or
  frontmatter eligibility handling. The final stage has zero integrity failures
  and zero staged-origin failures.

## M2 Navigation

- M2 hash-rechecked all 216 preserved originals and extracted only source
  frontmatter name/description and heading previews. The metadata pool is split
  into six mutually exclusive C0A lanes by the alphabetically first frozen M0
  discovery domain, which is an anti-overlap convention rather than semantic
  classification.
- C0A can now propose navigation-only 3--4 candidate directions. Every such
  direction must still pass exact-original C0B, C1, C2/C3, two independent
  model-assisted blinded C4 reviews, C5, and C6 before changing the strict
  count.

## Evidence

- M0: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m0_round37_intake_summary_2026-08-28.json`
- M1: `m1_round37_head_probe_summary_2026-08-28.json`, `m1_round37_tree_census_summary_2026-08-28.json`, `m1_round37_staging_selection_summary_2026-08-28.json`, and `m1_round37_byte_verified_source_inventory_summary_2026-08-28.json` in the same manifest directory.
- M2/C0 pool: `m2a_round37_navigation_summary_2026-08-28.json` and `c0a_round37_lanes_summary_2026-08-28.json`.
