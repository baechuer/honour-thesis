# RQ1b V3 Legacy Mapping And Wave 007 Discovery Checkpoint

Status: `LOCAL-ONLY PROVENANCE MAPPING PASS / WAVE 007 MATERIALISED / NO NEW STRICT CLUSTER / NO PROMPT, SELECTOR, EMBEDDING, OR METRIC`

## Purpose

This checkpoint records two related but deliberately non-pooled actions:

1. byte-level provenance mapping from the historical cross-source RQ1b C6
   records into the new V3 source frame; and
2. materialisation of a fresh, disjoint C0 source-only triage queue from that
   frame.

Neither action is semantic validation or routing evaluation.

## Source-Frame Boundary

The V3 frame contains 29,292 canonical SHA-256-unique local public originals,
2,476 alias paths and 1,613 origins. It is a snapshot-dated, provenance-bound
discovery and structural-census frame. The seven operational fields retain
their conceptual, literature and RQ1a basis. Heading counts over this frame
are structural markers, not semantic prevalence or field induction.

## Legacy C6 To V3 Mapping

The local audit command was:

```zsh
python3 skill_benchmark/scripts/audit_rq1b_legacy_c6_to_v3_source_frame.py \
  --legacy-manifest-dir skill_benchmark/rq1b_cross_source_public_benchmark/manifest \
  --v3-source-manifest skill_benchmark/rq1b_v3_public_source_frame/source_frame_2026-08-29/canonical_sources.jsonl \
  --output skill_benchmark/rq1b_v3_public_source_frame/legacy_c6_mapping_2026-08-29/legacy_c6_to_v3_source_frame_mapping.json
```

Outcome:

| Check | Result |
|---|---:|
| C6 JSONL manifests scanned | 26 |
| `C6_FROZEN_PRIMARY` rows | 408 |
| Distinct legacy review-packet IDs | 391 |
| Distinct candidate compositions | 76 |
| Triads / quartets | 57 / 19 |
| Fully SHA-mapped compositions | 76 / 76 |
| Unmapped compositions | 0 |
| Network calls / transmitted texts | 0 / 0 |

The output status is
`RQ1B_LEGACY_C6_TO_V3_SOURCE_FRAME_MAPPING_PASS_NOT_MERGED`.

This demonstrates only that all legacy candidate originals are present within
the V3 source population. The old campaign remains a separate historical
curation protocol: its model-assisted C3/C4 review records, prompt packets and
counts are not imported into V3. A mapped composition needs a future explicit
compatibility amendment plus the normal V3 C4A--C6 gates before it can be
called a V3 strict cluster.

## C0 Wave 007 Materialisation

`skill_benchmark/rq1b_v3_public_source_frame/c0_source_review_wave_007_2026-08-29/`
contains 30 new lexical candidate triads / 90 canonical originals. It excludes
every source used by completed C0 Waves 001--006. Its source-binding and
disjointness audit passes with zero errors; its roster SHA-256 is
`70dd6a60d6d8906d917a545cc1d4038dad5fda0293a55cd00879fa733f436a6f`.

Wave 007 is a **review queue only**. It has no source-only semantic decision
yet, so it is excluded from the completed 180-triad C0 feasibility tally. The
next permitted step is independent C0 source review without prompts, labels,
selectors, results, C2/C3/C4 material, or external transmission.

## Fresh D1 Source-Only Prospect Triage

Four independent local source-only screens supplied the following prospective
drafts. They are recorded to preserve their evidence and risks; none has a C1
card, prompt, gold label or valid-cluster status.

| Draft | Provisional disposition | Why |
|---|---|---|
| CI platform pipeline authoring: GitHub Actions / GitLab CI / Jenkins | `C1_CANDIDATE` | Cross-origin peer routes bind repository automation to distinct native pipeline platforms and configuration artifacts. Later C1 must fail closed when the repository is already platform-bound or more than one platform is fully adequate. |
| Markdown to HTML / DOCX / presentation | `C1_CANDIDATE` | Cross-origin Markdown transformation routes have a visible target-artifact contrast. C1 must reject it if the presentation artifact acts as a broad authoring container rather than a peer transformation route. |
| Statistical plotting / Matplotlib / Plotly | `NEEDS_PARENT_REVIEW` | The static-control versus interactive-delivery distinction is source-visible, but Seaborn is built on Matplotlib and may be an overlapping implementation rather than a strict peer route. |
| Generic content audit / ecommerce catalogue audit / social-account audit | `NEEDS_PARENT_REVIEW` | Cross-origin and natural, but the shared envelope may be only an overly broad taxonomy of complementary review forms. |
| Scikit-learn / PyTorch Lightning / TensorFlow | `HOLD_OR_REJECT` | Two candidates share one origin and the classical-versus-neural envelope risks nonparallel applicability. |
| Accessibility / SEO / performance web-quality review | `HOLD_OR_REJECT` | Same-origin coordinated quality components create a family/template and compositional-risk problem, despite clear target-specific checks. |

These are discovery aids. C1 may later retain, refine or reject only after
fresh source hash and literal-evidence checks; it must not use this table as a
sealed target or route label.

## Excluded Actions

- No web/API calls, model calls or external text transfer.
- No source document changed.
- No prompt, strict gold, acceptable set, field card, representation, selector,
  embedding, reranker, cost or metric was produced.
- No thesis LaTeX/PDF was changed.
