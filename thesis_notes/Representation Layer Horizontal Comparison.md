# Representation Layer Horizontal Comparison

Last updated: 2026-06-06

This note compares retrieval architectures horizontally by representation layer. The purpose is to keep the thesis focused on what information is encoded, then compare how different architectures use that representation.

## How To Read This

Rows are representation layers. Columns are architectures.

Do not read this as a pure model leaderboard unless the representation and stratum match. The main thesis interpretation should be:

1. Does a representation preserve enough selection information?
2. Which architectures can exploit that information?
3. Where does failure come from: representation loss, first-stage candidate recall, reranker ordering, or public-skill messiness?

## Public-Gold Stratum, 82 Prompts, 2401 Skills

This is currently the cleanest representation-horizontal matrix because Qwen was run on R1, R2, and full-skill representations on the same prompt stratum and library scale.

| Representation | Information encoded | Qwen embedding only | Qwen + Qwen rerank top-20 | Qwen + local schema top-100 | Best architecture in this row |
|---|---|---:|---:|---:|---|
| R1 flat metadata | name, family, short description | 62.2% top-1 / 84.2% top-5 / 0.720 MRR | 74.4% top-1 / 96.3% top-5 / 0.837 MRR | 40.2% top-1 / 85.4% top-5 / 0.592 MRR | Qwen rerank |
| R2 structured procedural | use conditions, avoid conditions, workflow, outputs, procedural summaries | 59.8% top-1 / 82.9% top-5 / 0.714 MRR | 76.8% top-1 / 100.0% top-5 / 0.861 MRR | 39.0% top-1 / 85.4% top-5 / 0.600 MRR | Qwen rerank |
| RFULL full skill document | entire `SKILL.md` | 31.7% top-1 / 58.5% top-5 / 0.448 MRR | 68.3% top-1 / 80.5% top-5 / 0.739 MRR | 25.6% top-1 / 72.0% top-5 / 0.454 MRR | Qwen rerank |

Public-gold interpretation:

- Full `SKILL.md` embedding is weak for Qwen on public skills. The full artifact contains more information but also much more noise.
- R1 and R2 compact cards are much stronger than full-document embedding in this stratum.
- R2 does not beat R1 by embedding alone, but R2 plus a neural reranker is the strongest public-gold method. This suggests the structured procedural card gives the reranker useful evidence even when the embedding model alone does not exploit it.
- The local schema reranker performs poorly on public-gold across all representations. This means the current local matcher is not robust enough for externally authored/public skills; it should be treated as a lexical prototype, not the final field-aware method.

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

## Active Controlled Stratum, 137 Prompts, 2401 Skills

The active controlled condition currently has complete full-skill results but not complete current R1/R2 provider reruns.

| Representation | Architecture | Top-1 | Top-5 | MRR | Interpretation |
|---|---|---:|---:|---:|---|
| RFULL | Qwen embedding only | 52.5% | 73.7% | 0.617 | Modern generic dense retrieval over full skills remains imperfect. |
| RFULL | Qwen + Qwen rerank top-20 | 62.0% | 75.2% | 0.684 | Generic reranking helps, but less than field-aware reranking. |
| RFULL first stage + R1/R2/R3 rerank | Qwen + local schema top-100 | 77.4% | 91.2% | 0.840 | Extracted fields substantially improve controlled selection. |
| RFULL | SkillRouter embedding only | 73.0% | 94.2% | 0.827 | Skill-specific embedding is much stronger than Qwen full embedding. |
| RFULL | SkillRouter + SkillRouter rerank top-20 | 83.2% | 97.8% | 0.898 | Strongest budget-fair full-skill neural architecture. |
| RFULL first stage + R1/R2/R3 rerank | SkillRouter + M6-v1 local top-100 | 86.9% | 98.5% | 0.927 | Strongest current controlled result, but uses top-100 budget. |

Active controlled interpretation:

- SkillRouter is not harshly defeated when representation is held to full-skill text. It beats Qwen full-skill embedding and Qwen full-skill reranking on controlled prompts.
- The strongest controlled result combines a strong skill-specific first stage with field-aware reranking, but this uses a larger candidate budget.
- Current active controlled results cannot yet answer whether R2 beats RFULL under SkillRouter because SkillRouter R1/R2 runs have not been completed.

## Representation-Level Findings So Far

### R1 Flat Metadata

R1 is a useful scalable baseline. It can work surprisingly well on public-gold because public skill names/descriptions often contain source/platform cues. However, it is fragile on controlled near-neighbour skills where the difference is procedural rather than topical.

Current evidence:

- Public-gold Qwen R1 embedding: 62.2% top-1.
- Public-gold Qwen R1 + Qwen rerank: 74.4% top-1.
- Historical controlled Qwen R1 embedding: 35.3% top-1.

Interpretation: R1 can be strong when names/descriptions are discriminative, but it is not enough for procedural near-neighbour selection.

### R2 Structured Procedural

R2 is the main thesis representation claim. It preserves use conditions, workflow, outputs, and boundaries.

Current evidence:

- Public-gold Qwen R2 + Qwen rerank is the strongest public-gold result at 76.8% top-1 and 100.0% top-5.
- Historical controlled R2 improves over R1 under Qwen embedding and Qwen reranking.
- R2 alone does not guarantee improvement; architecture matters.

Interpretation: structured procedural information is useful, especially when a reranker can read and compare it. But the current local lexical field matcher is not good enough for messy public skills.

### RFULL Full Skill Document

Full documents preserve the most raw information, but they are not automatically the best selection representation.

Current evidence:

- Public-gold Qwen full embedding: 31.7% top-1, much worse than R1/R2.
- Public-gold Qwen full + Qwen rerank: 68.3% top-1, so reranking can recover some signal.
- Controlled SkillRouter full embedding: 73.0% top-1, showing that a skill-specific model can use full artifacts much better than generic Qwen embedding.

Interpretation: full skill documents are high-information but high-noise. They need either a skill-specific retriever, a strong reranker, or an extraction/normalization layer.

## Architecture-Level Findings Inside Representations

| Architecture | What it seems good at | Current weakness |
|---|---|---|
| Embedding only | Fast first-stage candidate generation; strong top-k recall when representation is good. | Often confuses near-neighbour skills at top-1. |
| Qwen neural reranker | Strong generic reranking, especially on compact R1/R2 public-gold cards. | Does not directly test our proposed field-aware scoring; may exploit lexical/source cues. |
| SkillRouter embedding/reranker | Strong on full-skill controlled selection; good skill-specific retrieval baseline. | Current runs only use RFULL, so R1/R2 fairness gap remains. Public-gold reranker did not improve top-1. |
| Local schema / M6-v1 field-aware | Strong diagnostic evidence on controlled skills; separates candidate recall from reranking failure. | Too lexical and too tuned to clean fields; weak on public-gold. Needs semantic field matching. |
| Tree/graph methods | Not yet evaluated. Could test relational/hierarchical encoding directly. | Must avoid becoming architecture sprawl unless tied to representation claim. |

## What Must Be Run Next For A Fair Horizontal Comparison

Priority:

1. Controlled 137 / 2401 Qwen R1 and R2 reruns.
2. SkillRouter R1 and R2 on controlled 137 / 2401.
3. SkillRouter R1 and R2 on public-gold 82 / 2401.
4. Per-source-family public-gold analysis.
5. Optional exact combined 219 report after strata are clean.

The most important missing table is:

| Representation | Qwen embedding | Qwen + Qwen rerank | SkillRouter embedding | SkillRouter + SkillRouter rerank | Hybrid field-aware rerank |
|---|---:|---:|---:|---:|---:|
| R1 | needs current controlled rerun | needs current controlled rerun | not run | not run | partial |
| R2 | needs current controlled rerun | needs current controlled rerun | not run | not run | partial |
| RFULL | run | run | run | run | run |

Once this table is complete, the thesis can more cleanly claim whether the gain comes from representation, retrieval architecture, or their interaction.
