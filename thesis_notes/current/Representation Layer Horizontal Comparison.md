# Information Layer Horizontal Comparison

Last updated: 2026-06-18

> **2026-07-26 RQ2 protocol supersession.** This file is now `SUPERSEDED / HISTORICAL` as an active RQ2 protocol. RQ1a's reviewed facts feed the new matched-content RQ2a design, which is not yet implemented. RQ2b is a draft and has not been reviewed. Use `thesis_notes/current/RQ2 Current Status and Implementation Tracker - 2026-07-26.md` for current state and interpret every matrix below as exploratory or diagnostic evidence.

Update note, 2026-06-23: the detailed Qwen/public-gold rows in this file predate the public-original source correction and messier public-style controlled regeneration. Use `skill_benchmark/outputs/frozen_v0_4_refreshed_matrix_summary_2026_06_23.md`, `thesis_notes/current/Active Benchmark Snapshot.md`, and `thesis_notes/current/Current Results Summary.md` for current refreshed Qwen/local numbers. Keep this file mainly as historical horizontal interpretation until it is fully rewritten.

This note compares retrieval architectures horizontally by information layer. It was originally named "Representation Layer Horizontal Comparison"; the old filename is retained for continuity, but thesis prose should now use "information layer".

Canonical framing note: see `thesis_notes/current/Information Layer Framework.md`.

Purpose: keep the thesis focused on what operational information is available to the selector, then compare how different architectures preserve, organize, or exploit routing-relevant information. Do not assume every architecture carries the exact same I3 fields unless that mapping is explicitly implemented.

## How To Read This

Rows are information layers as implemented by existing representation artifacts. Columns are retrieval/reranking architectures.

Do not read this as a pure model leaderboard unless the representation and stratum match. The main thesis interpretation should be:

1. Does an information layer preserve enough selection information?
2. Which architectures can exploit that information?
3. Where does failure come from: information loss, first-stage candidate recall, reranker ordering, relation/hierarchy errors, or public-skill messiness?

Current terminology mapping:

| Thesis term | Existing artifact label |
|---|---|
| I1 flat skill card | R1 |
| I2 full skill artifact | RFULL |
| I3 structured selection fields | R2/R3 |
| I4 skill-relation information | planned R4 |
| I5 hierarchy/grouping information | planned M4 tree/DAG |

## Active Public-Gold Stratum, 144 Prompts, 2433 Skills

This is the current public-gold representation-horizontal matrix. It should be reported separately from controlled results because public-authored skills contain provider cues, broad public artifacts, duplicate capabilities, and messier artifact structure. Public full-text rows that used normalized import wrappers should be treated as historical until rerun against upstream `source/SKILL.original.md` files.

| Representation | Information encoded | Qwen embedding only | Qwen + Qwen rerank top-20 | SkillRouter embedding only | SkillRouter + SkillRouter rerank top-20 |
|---|---|---:|---:|---:|---:|
| R1 flat metadata | name, family, short description | 57.6% strict top-1 / 82.6% top-5 / 0.687 MRR | 74.3% strict top-1 / 92.4% top-5 / 0.820 MRR | 68.8% strict top-1 / 93.8% top-5 / 0.794 MRR | 70.8% strict top-1 / 92.4% top-5 / 0.804 MRR |
| R2 structured procedural | use conditions, avoid conditions, workflow, outputs, procedural summaries | 63.2% strict top-1 / 86.8% top-5 / 0.738 MRR | 72.9% strict top-1 / 97.9% top-5 / 0.832 MRR | 75.0% strict top-1 / 94.4% top-5 / 0.831 MRR | 71.5% strict top-1 / 93.1% top-5 / 0.805 MRR |
| RFULL full skill document | entire `SKILL.md` | 36.1% strict top-1 / 59.7% top-5 / 0.480 MRR | 65.3% strict top-1 / 79.9% top-5 / 0.716 MRR | 75.0% strict top-1 / 93.1% top-5 / 0.833 MRR | 70.1% strict top-1 / 92.4% top-5 / 0.804 MRR |

Public-gold interpretation:

- Full `SKILL.md` embedding is weak for Qwen on public skills, but strong for SkillRouter. This is a representation-model interaction, not a universal rule.
- R2 is strongest for Qwen embedding-only, while R1 plus Qwen reranking has the highest Qwen strict top-1.
- SkillRouter embedding-only is strongest on R2/full, but SkillRouter reranking reduces strict top-1 on R2/full public-gold cases. Public-gold therefore remains a reranker-ordering and public-cue stress test.
- Local field-aware methods remain diagnostic and are reported separately because they vary candidate generation, field extraction, and field matching.

### Public-Gold Lexical Control

This control runs the same lexical retriever over each information layer artifact. It helps separate information effects from neural model effects.

| Representation | BM25 strict top-1 / cand R@20 | TF-IDF strict top-1 / cand R@20 |
|---|---:|---:|
| R1 flat metadata | 55.6% / 87.5% | 56.9% / 92.4% |
| R2 structured procedural | 53.5% / 97.9% | 48.6% / 95.1% |
| RFULL full skill document | 34.0% / 81.9% | 36.8% / 82.6% |

Public-gold lexical interpretation:

- R2 improves shortlist recall, but simple lexical scorers often order flat public/provider cues better at rank 1.
- This means public-gold evidence should report both candidate recall and final top-1.
- Full documents are noisy under lexical scoring.

## Controlled Stratum, Historical 85 Prompts, 2349 Skills

This is not the active final controlled set, but it is useful because it contains Qwen R1/R2/RFULL representation comparisons on the same stratum.

| Representation | Qwen embedding only | Qwen + Qwen rerank top-20 | Qwen + local schema top-100 | Best architecture in this row |
|---|---:|---:|---:|---|
| R1 flat metadata | 35.3% top-1 / 48.2% top-5 / 0.426 MRR | 60.0% top-1 / 63.5% top-5 / 0.615 MRR | 69.4% top-1 / 74.1% top-5 / 0.719 MRR | local schema |
| R2 structured procedural | 50.6% top-1 / 64.7% top-5 / 0.571 MRR | 65.9% top-1 / 70.6% top-5 / 0.682 MRR | 80.0% top-1 / 84.7% top-5 / 0.820 MRR | local schema |
| RFULL full skill document | 50.6% top-1 / 69.4% top-5 / 0.590 MRR | 61.2% top-1 / 68.2% top-5 / 0.648 MRR | 84.7% top-1 / 89.4% top-5 / 0.872 MRR | local schema |

Historical controlled interpretation:

- R2 improves substantially over R1 for embedding-only retrieval. This supports the claim that procedural fields reduce representation loss.
- Local schema reranking helps more on controlled skills than public-gold skills because controlled skills expose cleaner fields and more stable procedural distinctions.
- RFULL plus local schema performs best here because the first stage can recover broad semantic candidates and the reranker then uses extracted structured fields.
- This matrix should not be used as the final controlled result because the active set is now 137 prompts and 2401 skills.

## Active Controlled Stratum, 245 Prompts, 2433 Skills

This is the current controlled representation-horizontal matrix. It is the cleanest evidence for representation effects because the controlled prompts were designed around procedural near-neighbour distinctions.

| Representation | Qwen embedding only | Qwen + Qwen rerank top-20 | SkillRouter embedding only | SkillRouter + SkillRouter rerank top-20 |
|---|---:|---:|---:|---:|
| R1 flat metadata | 34.3% top-1 / 62.5% top-5 / 0.470 MRR | 51.4% top-1 / 74.7% top-5 / 0.612 MRR | 62.9% top-1 / 93.5% top-5 / 0.763 MRR | 65.7% top-1 / 94.7% top-5 / 0.780 MRR |
| R2 structured procedural | 40.0% top-1 / 71.8% top-5 / 0.538 MRR | 58.0% top-1 / 80.4% top-5 / 0.679 MRR | 64.5% top-1 / 94.7% top-5 / 0.783 MRR | 71.0% top-1 / 96.7% top-5 / 0.823 MRR |
| RFULL full skill document | 44.1% top-1 / 75.5% top-5 / 0.575 MRR | 58.8% top-1 / 80.8% top-5 / 0.686 MRR | 59.2% top-1 / 91.4% top-5 / 0.737 MRR | 71.8% top-1 / 95.9% top-5 / 0.827 MRR |

Active controlled interpretation:

- R2 improves over R1 under both Qwen and SkillRouter on controlled prompts.
- Full skill text is only slightly stronger than R2 after reranking, and weaker than R2 for SkillRouter embedding-only.
- The controlled result supports the core thesis claim that structured procedural cards preserve useful selection information without simply exposing the entire artifact.

### Controlled Lexical Control

This control runs BM25 and TF-IDF over R1, R2, and full skill text with the retriever held fixed.

| Representation | BM25 top-1 / cand R@20 | TF-IDF top-1 / cand R@20 |
|---|---:|---:|
| R1 flat metadata | 55.9% / 94.3% | 53.9% / 91.8% |
| R2 structured procedural | 62.9% / 98.0% | 64.5% / 97.1% |
| RFULL full skill document | 63.3% / 98.4% | 61.2% / 95.9% |

Controlled lexical interpretation:

- With the retriever fixed, R2 substantially improves controlled top-1 and candidate recall over R1.
- Full text is slightly stronger than R2 for BM25, but weaker than R2 for TF-IDF and much more expensive.
- This is clean evidence for the representation-layer claim because the architecture is unchanged.

### M6-v2 Semantic Field Calibration

M6-v2 is a no-rewrite semantic field-aware reranker over fixed Qwen or SkillRouter top-20 candidates. It embeds the raw request and compares it to individual selector-visible skill fields. A fine score sweep now exists at `skill_benchmark/outputs/frozen_v0_4_m6v2_blend_sweep_fine.md`.

| Candidate source | Stratum | Representation | Full-sweep best top-1 | Dev-selected test top-1 | Interpretation |
|---|---|---|---:|---:|---|
| Qwen | controlled | R2 | 42.9% | 42.4% | Field signal helps only modestly; learned Qwen rerank remains stronger. |
| Qwen | public-gold | R2 | 69.4% | 66.7% | Field-heavy task matching helps public-gold R2 but needs held-out reporting. |
| SkillRouter | controlled | R2 | 65.3% | 64.4% | Strong first-stage ranking should not be overwritten heavily. |
| SkillRouter | public-gold | R2 | 77.1% | 66.7% | Full-set tuning overfits; use dev/test or cross-validation. |

M6-v2 interpretation:

- The first-stage score was too dominant in the old default for some Qwen rows.
- More precise second-stage weighting can help, especially when the first-stage candidate set is broad but not well ordered.
- However, field-aware scoring is not uniformly better than a strong learned reranker or SkillRouter ordering. Treat M6-v2 as evidence that fields contain usable signal and that combination strategy matters, not as the final winning architecture yet.

### M6-v2 Explicit Field-Use Sweep

This sweep uses the field-specific M6-v2 outputs. It compares request-side task/input/output/workflow/dependency spans to matching skill-side fields, then recomputes weights from saved component scores without new embedding API calls. The R2 rows below use the focused R2 calibration report.

The thesis-facing fixed method should use one global setting rather than the tuned rows below: 0.30 first-stage score, 0.70 semantic-field score, 0.25 penalty/bonus adjustment, `semantic_all`, cue-gated activation, and task-heavy field weights: task 0.50, output 0.20, workflow 0.15, input 0.10, dependency 0.05. This task-heavy scheme was selected by fixed-method internal-weight ablation.

| Candidate source | Stratum | Rep. | M6-v2-fixed top-1 | Accept top-1 | Top-5 | MRR |
|---|---|---|---:|---:|---:|---:|
| Qwen | controlled | R2 | 37.5% | 38.0% | 72.7% | 0.524 |
| Qwen | public-gold | R2 | 59.0% | 67.4% | 86.8% | 0.709 |
| SkillRouter | controlled | R2 | 54.3% | 55.1% | 91.4% | 0.701 |
| SkillRouter | public-gold | R2 | 68.1% | 76.4% | 91.7% | 0.775 |

Fixed internal-weight ablation average across the four main R2 rows:

| Internal scheme | Avg top-1 | Avg accept top-1 | Avg top-5 | Avg MRR | Worst top-1 |
|---|---:|---:|---:|---:|---:|
| task-heavy | 54.7% | 59.2% | 85.6% | 0.677 | 37.5% |
| dependency-balanced | 53.4% | 57.3% | 83.7% | 0.662 | 36.3% |
| global-core | 51.9% | 56.4% | 83.0% | 0.650 | 37.1% |
| workflow-heavy | 51.7% | 56.6% | 83.1% | 0.650 | 37.1% |
| balanced-input | 50.8% | 55.2% | 82.8% | 0.642 | 36.7% |

| Candidate source | Stratum | Rep. | Fixed field-specific top-1 | Tuned full-set top-1 | Dev-selected test top-1 | Best tuned setting |
|---|---|---|---:|---:|---:|---|
| Qwen | controlled | R1 | 35.5% | 38.4% | 33.9% | semantic core, dependency-light, base 0.25 |
| Qwen | controlled | R2 | 40.0% | 41.6% | 40.7% | semantic core boundary, balanced core, base 0.90 |
| Qwen | controlled | full | 45.3% | 45.3% | 49.1% | task/output/workflow, base 0.75 |
| Qwen | public-gold | R1 | 61.8% | 66.7% | 65.4% | task-only, base 0.25 |
| Qwen | public-gold | R2 | 61.8% | 68.8% | 66.7% | task-only, base 0.25 |
| Qwen | public-gold | full | 41.7% | 57.6% | 55.1% | task-only, base 0.00 |
| SkillRouter | controlled | R1 | 62.9% | 63.7% | 64.4% | task-only, base 1.00 |
| SkillRouter | controlled | R2 | 64.5% | 66.1% | 63.6% | semantic core boundary, dependency-light, base 0.70 |
| SkillRouter | controlled | full | 59.2% | 61.2% | 61.9% | output/workflow-heavy, base 0.50 |
| SkillRouter | public-gold | R1 | 70.1% | 75.7% | 70.5% | task-only, base 0.50 |
| SkillRouter | public-gold | R2 | 73.6% | 76.4% | 71.8% | task-only, base 0.40 |
| SkillRouter | public-gold | full | 73.6% | 77.8% | 73.1% | task-only, base 0.50 |

Explicit field-use interpretation:

- The strongest held-out Qwen controlled row is full-skill field-specific matching, but the central R2 row remains modest.
- Public-gold benefits from recalibration, especially for Qwen R2 and SkillRouter full, but held-out results are lower than full-set best rows.
- The current M6-v2 evidence supports selective field use, not naive "more fields is always better". Output and workflow help in some full/controlled settings; task evidence remains dominant across R2.

## Representation-Level Findings So Far

### R1 Flat Metadata

R1 is a useful scalable baseline. It can work surprisingly well on public-gold because public skill names/descriptions often contain source/platform cues. However, it is fragile on controlled near-neighbour skills where the difference is procedural rather than topical.

Current evidence:

- Public-gold Qwen R1 embedding: 57.6% strict top-1.
- Public-gold Qwen R1 + Qwen rerank: 74.3% strict top-1.
- Controlled Qwen R1 embedding: 34.3% top-1.
- Controlled SkillRouter R1 rerank: 65.7% top-1.

Interpretation: R1 can be strong when names/descriptions are discriminative, but it is not enough for procedural near-neighbour selection.

### R2 Structured Procedural

R2 is the main thesis representation claim. It preserves use conditions, workflow, outputs, and boundaries.

Current evidence:

- Controlled Qwen R2 improves over R1 under embedding-only retrieval and Qwen reranking.
- Controlled SkillRouter R2 improves over SkillRouter R1 under embedding-only retrieval and SkillRouter reranking.
- Public-gold SkillRouter R2 embedding reaches 75.0% strict top-1, but public-gold Qwen reranking remains strongest on R1. R2 helps, but architecture and public cueing matter.

Interpretation: structured procedural information is useful, especially when a reranker can read and compare it. But the current local lexical field matcher is not good enough for messy public skills.

### RFULL Full Skill Document

Full documents preserve the most raw information, but they are not automatically the best selection representation.

Current evidence:

- Public-gold Qwen full embedding: 36.1% strict top-1, much worse than R1/R2.
- Public-gold Qwen full + Qwen rerank: 65.3% strict top-1, so reranking can recover some signal.
- Controlled SkillRouter full embedding: 59.2% top-1, lower than SkillRouter R2 embedding.
- Controlled SkillRouter full + rerank: 71.8% top-1, slightly higher than SkillRouter R2 + rerank.

Interpretation: full skill documents are high-information but high-noise. They need either a skill-specific retriever, a strong reranker, or an extraction/normalization layer.

## Architecture-Level Findings Inside Information Layers

| Architecture | What it seems good at | Current weakness |
|---|---|---|
| Embedding only | Fast first-stage candidate generation; strong top-k recall when representation is good. | Often confuses near-neighbour skills at top-1. |
| Qwen neural reranker | Strong generic reranking, especially on compact R1/R2 public-gold cards. | Does not directly test our proposed field-aware scoring; may exploit lexical/source cues. |
| SkillRouter embedding/reranker | Strong skill-specific retrieval baseline across R1/R2/RFULL; confirms benchmark remains non-trivial under a prior-work-aligned model. | Reranking does not uniformly improve public-gold top-1; remaining controlled failures are mostly candidate ordering among near-neighbour skills. |
| Local schema / M6-v1 field-aware | Strong diagnostic evidence on controlled skills; separates candidate recall from reranking failure. | Too lexical and too tuned to clean fields; weak on public-gold. Needs semantic field matching. |
| M6-v2 semantic field-aware | Uses proposed fields explicitly with semantic similarity and no query rewrite; useful for testing field signal and blend sensitivity. | Calibration-sensitive; does not consistently beat learned rerankers; full-set tuned weights cannot be used as headline results. |
| Tree/graph methods | Not yet evaluated. Could test relational/hierarchical encoding directly. | Must avoid becoming architecture sprawl unless tied to representation claim. |

## What Must Be Run Next For A Fair Horizontal Comparison

Priority:

1. Add statistical uncertainty estimates and paired comparisons for final selected representation comparisons.
2. Run failure-mode analysis grouped by whether the error is first-stage recall failure, reranker-ordering failure, provider/name cueing, public-wrapper messiness, or genuine ambiguous gold label.
3. Decide whether M4 tree and M5 graph runs add enough evidence for the final thesis, or whether they should remain proposed future work.
4. Optional exact combined report after strata are clean.
5. If M6-v2 is kept as a final method, tune weights only on a dev split and report held-out test results.

The most important missing table is:

| Representation | BM25/TF-IDF | Qwen embedding | Qwen + Qwen rerank | SkillRouter embedding | SkillRouter + SkillRouter rerank | M6-v2 field-aware |
|---|---:|---:|---:|---:|---:|---:|
| R1 | run | run | run | run | run | run |
| R2 | run | run | run | run | run | run |
| RFULL | run | run | run | run | run | run |

The remaining gap is no longer basic crossed coverage for R1/R2/full. The remaining gap is methodological hardening: statistical testing, failure-mode analysis, and deciding whether M4/M5 graph/tree methods add a real representation claim.
