# RQ1b Cross-Source Round 18 M0-M1 Small-Source Intake

Date: 2026-08-27

## Boundary

This checkpoint records public-source discovery, pinned-source scheduling, and
local byte staging for the small-source portion of Round 18. It does not
record a candidate composition, a prompt, a label, an adequacy decision,
retrieval, representation scoring, embedding, reranking, API use, a metric, or
downstream-task success.

## M0 Discovery and Source Census

- M0 collected 112 raw public-source leads across engineering, data,
  legal/finance/business, operations/security, product/design, and science.
  Canonicalisation retained 83 GitHub repository roots.
- A remote commit-tree-only census confirmed all 83 pinned roots were
  reachable and found 16,208 `SKILL.md` paths. It neither read artefact bodies
  nor assessed their semantic suitability.
- To keep the next full-source review tractable and auditable, the small-source
  schedule selected 56 roots with at most 100 discovered paths each. The other
  27 roots were deferred by size only, not rejected for quality or eligibility.

## M1 Small-Source Staging

- Sparse local staging materialised only pinned `SKILL.md` files and a root
  licence blob; no source code was executed.
- The seven small-source batches discovered 1,689 paths and stage-eligible
  1,157 bodies. There were 518 exact duplicate-path skips and 14
  missing-frontmatter skips, with no staging failure.
- The M1 flattener retained 1,120 canonical SHA-256-verified originals from
  44 origins. It preserves 259 reference-only records and records 37 exact
  duplicate paths separately, rather than counting them as independent
  originals.

## Explicit Holds

- `Amey-Thakur/AI-SKILLS` was locally byte-staged as a separate 1,000-skill
  large-source operation. It is not part of the Round 18 small-source M1
  aggregate or navigation inventory until a separate large-source integrity
  plan admits it.
- `CaseMark/skills` was deliberately interrupted after partial materialisation
  during an earlier oversized batch attempt. It has no completed M1 staging
  manifest and is excluded from this cohort.

## Next Gate

M2 will derive only names, descriptions, and Markdown-heading previews from
the 1,120 local originals. Its navigation inventory will not infer similarity
or form a candidate unit. C0A may then propose possible 3--4-skill
cross-source compositions from that inventory; C0B remains the later
full-source structural gate.

## Artefacts

- `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m0_round18_raw_discovery_leads_2026-08-27.jsonl`
- `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m0_round18_canonical_source_leads_2026-08-27.jsonl`
- `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m0_round18_discovery_summary_2026-08-27.json`
- `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m1_round18_tree_census_summary_2026-08-27.json`
- `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m1_round18_small_source_schedule_2026-08-27.json`
- `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m1_round18_small_staging_summary_2026-08-27.json`
- `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m1_round18_small_staged_source_manifest_2026-08-27.jsonl`
- `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m1_round18_small_staged_source_summary_2026-08-27.json`
