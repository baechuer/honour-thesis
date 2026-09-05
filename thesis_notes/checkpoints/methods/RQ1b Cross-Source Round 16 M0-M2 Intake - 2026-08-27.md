# RQ1b Cross-Source Round 16 M0-M2 Intake

Date: 2026-08-27

Status: `M0-M2 COMPLETE / SOURCE-ONLY NAVIGATION / NO C0A PROPOSAL / NO CLUSTER / NO RESULT`

## Purpose

This checkpoint applies the RQ1b discovery-first curation cadence before the
next source-screening cohort. It records public-source discovery, provenance
pinning, local byte staging, exact-duplicate/frontmatter screening, and
source-provided navigation metadata. It does not assess semantic peerhood or
create a cluster, prompt, label, acceptable set, model input, retrieval run,
metric, or thesis result.

## M0 Discovery

Three independent domain passes recorded 37 new public repository leads with
no repository overlap: 12 business/writing, 13 science/data, and 12
engineering/operations. Discovery recorded navigation paths and M1 checks but
did not copy raw source bodies.

Evidence:

- `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/discovery_round16_business_writing_2026-08-27.md`
- `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/discovery_round16_science_data_2026-08-27.md`
- `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/discovery_round16_engineering_ops_2026-08-27.md`

## M1 Pinned Source Intake

The M1 batch plan selected 15 domain-diverse leads from the discovery set. For
each, the public GitHub HEAD was recorded as a full commit SHA; a local sparse
clone fetched only `SKILL.md` files and root licence metadata. No repository
code was executed.

| M1 outcome | Count |
| --- | ---: |
| Planned/pinned source origins | 15 |
| `SKILL.md` files discovered at pins | 2,249 |
| Exact-byte duplicates of already staged sources | 340 |
| Files skipped for missing required frontmatter | 8 |
| New byte-staged original artefacts | 1,901 |
| Origins with at least one new staged artefact | 10 |

`astDeniss/business-skills` was the only planned source with no root licence
file, and all 69 of its files were already exact-byte duplicates. Therefore
this particular intake contributes zero new reference-only rows. The protocol
rule remains unchanged: a no-declared-licence original is reference-only for
release provenance, not a scientific admission exclusion.

Evidence:

- Batch plan: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m1_round16_source_batch_plan_2026-08-27.json`
- Per-origin staging aggregate: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m1_round16_staging_summary_2026-08-27.json`
- Flattened M1 records: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m1_round16_staged_source_manifest_2026-08-27.jsonl`
- M1 integrity summary: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m1_round16_staged_source_summary_2026-08-27.json`

## M2A Navigation Metadata

Every one of the 1,901 staged originals passed a local SHA-256 recheck before
the navigation builder extracted only source-provided name, description, and
up to six Markdown headings. The resulting inventory has name and description
metadata for all 1,901 entries, headings for 1,892, and no integrity failure.

Evidence:

- `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m2a_round16_navigation_inventory_2026-08-27.jsonl`
- `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m2a_round16_navigation_summary_2026-08-27.json`

## Explicit Boundary

This intake does **not** add 1,901 benchmark clusters. It is a larger
source-only pool for later source-agnostic C0A sorting and full-source C0B
review. The prior strict curation total remains 13 frozen candidate
compositions and 82 frozen strict prompt packets; no retrieval, embedding,
reranking, API call, metric, or empirical thesis result was run in this round.

## Next Gate

Round 16 C0A may now sort this source inventory into tentative 3--4 candidate
proposals. Each proposed composition still requires C0B full-source peer-route
evidence, C1 integrity, C2/C3 cue-safe prompts, two independent blinded C4
reviews, C5 stratum assignment, and C6 freeze before it can become an RQ1b
strict benchmark packet.
