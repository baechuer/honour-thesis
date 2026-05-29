# Current Results Summary

Date: 2026-05-28

This file consolidates the benchmark and retrieval results completed so far.

## Active Scale Update

The active local validation condition is now the 2349-skill public-expanded library. The 2089-skill results remain the current Qwen/provider comparison point because provider runs have not yet been rerun after the public expansion.

Current library:

- 2349 total skills.
- 85 controlled/evaluated core skills.
- 1800 generated background-scale skills.
- 460 public imported background skills.
- 4 support/email skills.
- 85 evaluated prompts.

Current validation:

| Step | Status | Result |
|---|---|---|
| Step 1 integrity | Done | PASS: 85 prompts and 2349 skills resolve. |
| Step 2 procedural alignment | Done | PASS field audit: 85/85 prompts; PASS prompt-specific alignment: 85/85 after prompt refinements and negation-aware scoring. |
| Step 3 semantic confusability | Done with caveat | Previous MiniLM checkpoint: PASS 75/85. Current 2349 rerun used TF-IDF fallback and produced 27/85, so it is not directly comparable. |
| Step 4 prompt leakage | Done | PASS: 0 critical exact-name leaks; 0 high-risk leaks. |
| Step 5 scale regime | Done | PASS: 2349-skill public-expanded library constructed. |
| Step 6 public-skill field audit | Mostly done | 460/460 imported public skills audited heuristically; earlier 200/200 subset audited with DeepSeek verifier and targeted disagreement adjudication. |
| Step 7 local selectors | Done | PASS: lexical/schema subset rerun on 2349; MiniLM local methods remain 2089/historical because `sentence_transformers` is unavailable in this shell. |
| Step 7 Qwen provider selectors | Partly done on 2089 | Full-skill Qwen embedding, Qwen rerank, and Qwen + local schema rerank rerun on 2089. R1/R2 provider variants remain historical 1006-scale. |
| Step 7 field ablation | Done | Local BM25/TF-IDF ablations show use conditions, outputs, and workflow/procedure drive most retrieval gains; naive not-for/dependency concatenation can hurt. |
| Step 7 non-core competition | Needs adjudication | 33/85 semantic non-core-over-gold cases; 16/85 procedural non-core-over-gold cases. |

Current 2349-scale local lexical/schema selector results:

| Method | Core Top-1 | Full Top-1 | Full Top-5 | Full Non-Core Top-1 |
|---|---:|---:|---:|---:|
| M1 BM25 flat | 76.5% | 68.2% | 87.1% | 15.3% |
| M1 TF-IDF flat | 75.3% | 58.8% | 80.0% | 28.2% |
| M3 TF-IDF schema | 84.7% | 76.5% | 94.1% | 10.6% |
| M6 BM25 -> schema rerank | 80.0% | 78.8% | 91.8% | 5.9% |
| M6 TF-IDF -> schema rerank | 84.7% | 74.1% | 87.1% | 14.1% |

Current interpretation:

- The expanded benchmark now creates real scale pressure.
- Description-only and flat retrieval remain fragile under scale; dense/MiniLM evidence is retained from the 2089 checkpoint.
- Schema-aware and hybrid methods degrade less and produce fewer non-core top-1 false positives.
- The main next validation step is targeted second-pass adjudication of non-core winners and strongest-method failures, especially in `documents_files`, `skill_lifecycle`, `deployment_browser_qa`, and `api_backend_design`.
- The public-expanded local lexical run preserves the main result: use/output/workflow fields still help, while naive constraint/dependency/resource concatenation hurts top-1.

Current 2089-scale MiniLM/local selector results, retained for comparison:

| Method | Core Top-1 | Full Top-1 | Full Top-5 | Full Non-Core Top-1 |
|---|---:|---:|---:|---:|
| M2a MiniLM description | 67.1% | 49.4% | 77.6% | 31.8% |
| M2b MiniLM full skill | 71.8% | 64.7% | 83.5% | 15.3% |
| M6 MiniLM full -> schema rerank | 90.6% | 82.3% | 89.4% | 5.9% |

Current 2089-scale Qwen provider results:

| Method | Candidate Budget | Top-1 | Accept Top-1 | Top-5 | Accept Top-5 | MRR | Non-Core Top-1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Qwen full-skill embedding only | none | 50.6% | 51.8% | 69.4% | 71.8% | 0.591 | 30.6% |
| Qwen full-skill + Qwen rerank | 20 | 63.5% | 68.2% | 69.4% | 72.9% | 0.668 | 32.9% |
| Qwen full-skill + local schema rerank | 50 | 80.0% | 81.2% | 84.7% | 85.9% | 0.822 | 12.9% |
| Qwen full-skill + local schema rerank | 100 | 84.7% | 84.7% | 89.4% | 89.4% | 0.872 | 9.4% |

Current Qwen interpretation:

- Qwen full-skill embedding-only retrieval is not enough at 2089 scale.
- Qwen's generic reranker improves top-1 but still leaves many non-core false positives.
- Qwen full-skill retrieval plus local procedural schema reranking is currently the strongest 2089-scale result.

## Public-Skill Field Audit

Current status:

- Scope: 460 imported public `SKILL.md` files.
- Originals used: 460/460.
- Mean words per skill: 1194.02.
- Median words per skill: 1141.
- Manual review packet: 15 sampled skills for the expanded public set.

Field prevalence:

| Field | Explicit | Explicit or Extractable | Provisional Read |
|---|---:|---:|---|
| routing trigger | 100.0% | 100.0% | observed |
| input/precondition | 25.2% | 81.5% | often extractable |
| output artifact | 45.2% | 85.2% | observed/extractable |
| workflow/procedure | 71.7% | 84.4% | observed/extractable |
| constraints/boundaries | 41.3% | 77.6% | partially observed/extractable |
| dependencies/tools | 72.8% | 85.0% | observed |
| resources/references | 66.7% | 82.0% | observed/extractable |
| examples/tests | 63.5% | 93.9% | observed/extractable |
| safety/side effects | 11.3% | 37.0% | proposed or weakly observed |
| portability/environment | 62.2% | 80.7% | observed/extractable |
| hierarchy/links | 25.2% | 31.1% | partially observed |

Interpretation:

- Public skills do contain many of the procedural signals used by the structured representation, especially triggers, workflows, outputs, dependencies, and examples.
- Some signals are often implicit rather than cleanly fielded, which supports the idea of a representation layer that extracts or normalizes them.
- Safety/side-effect information is weak in the sampled public corpus. Treat this as a proposed field or a quality gap, not a mature public-skill convention.
- The current audit is heuristic. The 20-skill manual review packet must be checked before using these numbers as final thesis evidence.
- A model-assisted semantic verification layer has been added and implemented. The DeepSeek checkpoint covers the earlier 200-public-skill subset and is recorded in `thesis_notes/Public Skill Model Verification Checkpoint - 200 Skills.md`. The expanded 460-skill checkpoint is heuristic only unless model verification is rerun.
- A 10-skill subagent/manual calibration pilot is complete. It confirms the main pattern but warns that resources, examples/tests, output artifacts, workflow, and dependencies can be overcounted if keyword matching is too loose.
- A targeted disagreement adjudication note is recorded in `thesis_notes/Public Skill Disagreement Adjudication - Step 6.md`. Its main conclusion is that public skills contain recoverable procedural signals, but the representation layer must normalize them rather than assuming clean author-provided schema fields.
- A draft final taxonomy is recorded in `thesis_notes/Final Representation Field Taxonomy - Draft.md`. It separates primary retrieval fields from secondary feasibility, boundary, and downstream fields.
- The public-expanded validation checkpoint is recorded in `thesis_notes/Public Expansion 2349 Validation Checkpoint.md`.

## Benchmark Status

The following section records the earlier 1006-skill v1 state.

Library:

- 1006 total skills.
- 67 controlled core skills.
- 920 generated background-scale skills.
- 15 public imported background skills.
- 4 support/email skills.
- 67 evaluated prompts.

Validation:

| Step | Status | Result |
|---|---|---|
| Step 1 integrity | Done | PASS: 67 prompts and 1006 skills resolve. |
| Step 2 procedural alignment | Done | PASS: 67/67 prompts pass field audit; 65/67 pass stricter prompt-specific alignment. |
| Step 3 semantic confusability | Done | PASS: 61/67 prompts pass local MiniLM semantic-confusability check. |
| Step 4 prompt leakage | Done | PASS: 0 critical exact-name leaks; 0 high-risk leaks. |
| Step 5 scale regime | Done | PASS: 1006-skill library constructed. |
| Step 7 local selectors | Done | PASS: useful spread from 47.8% to 80.6% top-1. |
| Step 7 Qwen provider selectors | Done | PASS: Qwen embedding and reranking tested on R1, full skill, and R2. |
| Low-information stress test | Done separately | Performance drops sharply; confirms schema reranking depends on explicit procedural evidence. |
| Failure mode analysis | Done for current strongest method | 10 failures: 4 first-stage exclusions, 6 reranking/boundary/annotation failures. |
| Step 8 M0 progressive disclosure | Done on core | PASS as baseline trace; not yet full-library stress test. |
| Step 9 downstream task validation | Not done | Plan exists; artifact generation/evaluation still pending. |

## Local Selector Results

Core scale means 67 controlled skills. Full scale means 1006 skills.

| Method | Representation | Core Top-1 | Core Top-5 | Full Top-1 | Full Top-5 | Full MRR | Full Non-Core Top-1 |
|---|---|---:|---:|---:|---:|---:|---:|
| M1 BM25 flat | R1 flat metadata | 67.2% | 94.0% | 64.2% | 86.6% | 0.733 | 16.4% |
| M1 TF-IDF flat | R1 flat metadata | 68.7% | 92.5% | 58.2% | 85.1% | 0.697 | 16.4% |
| M2a MiniLM description | R1 description embedding | 61.2% | 91.0% | 47.8% | 74.6% | 0.603 | 25.4% |
| M2b MiniLM full skill | Full `SKILL.md` embedding | 64.2% | 92.5% | 61.2% | 82.1% | 0.717 | 9.0% |
| M3 TF-IDF schema | R2 structured procedural | 74.6% | 100.0% | 71.6% | 95.5% | 0.808 | 9.0% |
| M6 BM25 -> schema rerank | Flat shortlist + schema rerank | 77.6% | 95.5% | 71.6% | 92.5% | 0.815 | 7.5% |
| M6 TF-IDF -> schema rerank | Flat shortlist + schema rerank | 80.6% | 97.0% | 70.2% | 85.1% | 0.778 | 10.4% |
| M6 MiniLM full -> schema rerank | Full-skill shortlist + schema rerank | 89.6% | 100.0% | 80.6% | 91.0% | 0.856 | 7.5% |

Best local method:

- M6 MiniLM full-skill retrieval plus deterministic schema reranking.
- Full-library top-1: 80.6%.
- Full-library top-5: 91.0%.

## Historical Qwen Provider Results

The following Qwen full-library runs use the historical 1006-skill scale. The active 2089-scale Qwen full-skill results are listed near the top of this file.

| Method | Representation | Top-1 | Accept Top-1 | Top-5 | Accept Top-5 | MRR | Non-Core Top-1 |
|---|---|---:|---:|---:|---:|---:|---:|
| Qwen embedding only | R1 flat card | 35.8% | 35.8% | 56.7% | 59.7% | 0.449 | 43.3% |
| Qwen embedding + rerank | R1 flat card | 64.2% | 67.2% | 67.2% | 70.2% | 0.649 | 31.3% |
| Qwen embedding only | Full `SKILL.md` | 46.3% | 47.8% | 71.6% | 74.6% | 0.574 | 29.8% |
| Qwen embedding + rerank | Full `SKILL.md` | 61.2% | 65.7% | 65.7% | 70.2% | 0.644 | 37.3% |
| Qwen embedding only | R2 structured card | 47.8% | 47.8% | 65.7% | 67.2% | 0.563 | 31.3% |
| Qwen embedding + rerank | R2 structured card | 65.7% | 67.2% | 71.6% | 73.1% | 0.688 | 26.9% |

## Qwen + Local Schema Reranker

This ablation uses Qwen `text-embedding-v4` for first-stage retrieval, then uses our deterministic schema reranker instead of Qwen `qwen3-rerank`.

| Method | Candidate Budget | Top-1 | Top-5 | MRR | Non-Core Top-1 |
|---|---:|---:|---:|---:|---:|
| Qwen R1 + local schema | 20 | 58.2% | 67.2% | 0.622 | 25.4% |
| Qwen full + local schema | 20 | 68.7% | 74.6% | 0.715 | 22.4% |
| Qwen full + local schema | 50 | 80.6% | 88.1% | 0.834 | 11.9% |
| Qwen full + local schema | 100 | 85.1% | 91.0% | 0.878 | 9.0% |
| Qwen R2 + local schema | 20 | 64.2% | 73.1% | 0.687 | 22.4% |
| Qwen R2 + local schema | 50 | 70.2% | 79.1% | 0.746 | 14.9% |
| Qwen R2 + local schema | 100 | 79.1% | 89.5% | 0.838 | 10.4% |

Qwen core smoke test:

- Scale: 67 controlled core skills.
- Prompts: first 5 prompts.
- Method: full `SKILL.md` embedding plus Qwen rerank.
- Result: 100.0% top-1 and 100.0% top-5.

Main Qwen interpretation:

- Qwen reranking improves top-1 over embedding-only for every representation.
- The best Qwen condition is R2 structured card plus rerank at 65.7% top-1.
- Qwen does not solve the full benchmark.
- Qwen's generic reranker underperforms the best local structure-aware M6 result.
- Qwen embeddings combined with the local schema reranker now produce the strongest current result: 85.1% top-1 with full-skill Qwen retrieval and top-100 schema reranking.

## M0 Progressive Disclosure Baseline

M0 is the normal-agent baseline where the main agent sees skill cards and chooses which full skill documents to load.

Current run:

- Scale: 67 controlled core skills.
- Strict top-1: 61.2%.
- Strict any-hit: 64.2%.
- No explicit skill loaded: 31.3%.
- Mean full skill docs loaded: 0.78.

Interpretation:

- M0 is useful as a realistic main-agent behavior baseline.
- It is not a clean retriever-only measure because the agent sometimes answers directly without loading a skill.
- Full 1006-skill M0 has not been run and should be treated as a context/cost stress test rather than a necessary immediate result.

## Step 9 Candidate Readiness

Step 9 downstream artifact generation has not been executed. A 12-prompt readiness check exists. The underlying files still use `step8` in their names from the earlier numbering.

| Method | Top-1 Gold/Accept | Top-5 Gold/Accept |
|---|---:|---:|
| M1 BM25 flat | 75.0% | 91.7% |
| M1 TF-IDF flat | 41.7% | 100.0% |
| M2b MiniLM full skill | 50.0% | 83.3% |
| M3 TF-IDF schema | 66.7% | 91.7% |
| M6 BM25 -> schema rerank | 75.0% | 91.7% |
| M6 TF-IDF -> schema rerank | 50.0% | 91.7% |
| M6 MiniLM full -> schema rerank | 83.3% | 91.7% |

Interpretation:

- Downstream validation is only fair when the correct or acceptable skill is in the candidate set.
- Missing top-5 cases should be treated as retrieval failures before judging generated artifacts.

## Low-Information Stress Test

This separate 12-prompt set uses less explicit user requests. It is not mixed into the main benchmark.

Best strict top-1 results:

- M2b MiniLM full skill: 41.7%.
- M6 MiniLM full -> schema rerank: 33.3%.
- Qwen full + qwen3-rerank: 33.3%.
- Qwen full + local schema rerank, top-100: 25.0%.

Interpretation:

- This is an anti-cheating check.
- The schema reranker does not infer hidden intent from vague prompts.
- It works best when the user request contains enough procedural evidence to match structured fields.
- Very underspecified requests may need a clarification or query-understanding stage before retrieval.

Detailed report: `thesis_notes/Low Information Stress Test.md`.

## What The Results Currently Show

1. Flat metadata is weak under scale.
2. Description-only embedding is especially fragile.
3. Full skill text helps compared with short descriptions, but does not fully solve procedural confusion.
4. Structured procedural information is useful.
5. Reranking helps when the correct skill is already in the candidate set.
6. Stronger provider embeddings/rerankers do not remove the need for good representation.
7. The current best result comes from Qwen broad semantic retrieval plus explicit schema-aware reranking.
8. Field ablations show the most retrieval-critical information is use conditions, output artifacts, and workflow/procedure; not-for and dependency/resource fields need field-aware handling because naive text concatenation can add noise.

## Current Critique And Validity Risks

The formal critique/action plan is recorded in `thesis_notes/Critique Response and Validity Improvement Plan.md`.

Main risks:

- Benchmark construction and schema scoring may be co-adapted.
- Some non-core winners may be genuinely acceptable or better than the intended gold skill.
- 85 evaluated prompts supports a controlled honours-scale benchmark, but not broad universal claims.
- Generated background skills create scale pressure but not full real-world messiness.
- MiniLM semantic-confusability checks are useful construction evidence, not final semantic authority.
- The public-skill audit grounds the field taxonomy but is not a full human annotation study.
- Downstream task success is not yet demonstrated.

Planned response:

- Freeze the representation-field taxonomy and method set before further tuning.
- Run targeted second-pass adjudication over non-core winners and strongest-method failures.
- Report public-skill findings as observed/extractable/proposed, not as clean ecosystem-wide schema prevalence.
- Optionally expand public skills as background/taxonomy validation, while keeping them separate from controlled gold skills unless manually atomized and annotated.
- Run small Step 9 downstream validation before claiming agent reliability benefits.

## Current Strongest-Method Failure Analysis

Target:

- Qwen full `SKILL.md` embedding.
- Top-100 candidate pool.
- Local schema reranker.

Failure split:

- 10 strict top-1 failures out of 67 prompts.
- 4 first-stage exclusions where Qwen did not place the gold skill in top-100.
- 6 reranking, boundary, or annotation failures where the gold was inside the top-100 but did not rank first.

Main failure types:

- first-stage embedding confuses task object with required procedure;
- schema reranker overweights secondary terms;
- negation and `not_for` handling is too weak;
- meta-skill tasks such as editing/evaluating a skill are confused with using the named skill;
- one domain-specific extractor may need acceptable-alternative adjudication.

Detailed report: `thesis_notes/Failure Mode Analysis - Qwen Full Local Schema Top100.md`.

## Not Done Yet

- Targeted second-pass adjudication over non-core winners and strongest-method failures.
- Optional model-assisted verification of the expanded 460-public-skill audit.
- Latency/cost comparison for top-20, top-50, and top-100 candidate budgets.
- Hybrid Qwen candidate text experiments, such as R2 first-stage plus full-skill rerank text.
- SkillRouter local smoke test.
- SkillRouter hosted test, only if local is infeasible and worth the cost.
- M4 tree routing.
- M5 graph retrieval.
- Full 1006-skill M0 cost/context stress test.
- Step 9 downstream artifact generation and grading.
- Final thesis results tables and written discussion.

## Current Next Step

Freeze the representation-field taxonomy and address the main validity critiques before adding more methods.

Specifically:

- classify public-skill fields as observed, extractable, or proposed normalization using the completed heuristic/model disagreement adjudication;
- use the completed field-ablation results to freeze the final representation-field set;
- run targeted second-pass adjudication on non-core winners and strongest-method failures;
- if expanding public skills, treat them as background/taxonomy validation first, not new gold tasks;
- compare top-20, top-50, and top-100 latency/cost;
- decide whether top-100 is acceptable as a retriever/reranker budget;
- decide whether to add acceptable alternatives for domain-specific near-equivalents;
- then move to Step 9 downstream validation.
