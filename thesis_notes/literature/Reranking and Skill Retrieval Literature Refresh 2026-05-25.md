# Reranking and Skill Retrieval Literature Refresh

Date: 2026-05-25

Purpose: refresh the thesis framing after adding M6 hybrid reranking and optional provider-backed M7/M8 baselines to the benchmark.

## Main Finding

The newer literature supports a two-stage view of skill/tool selection:

1. Use a cheap retriever to shortlist candidates from a large skill/tool corpus.
2. Use a more expensive reranker to reorder only that shortlist using richer evidence.
3. Pass the final small candidate set to the main agent.

This matches the thesis architecture: the retriever/reranker is a separate candidate-subsetting component before the main agent loads full skill artifacts.

## Papers To Add Or Emphasize

### SkillRouter: Skill Routing for LLM Agents at Scale

Source: https://arxiv.org/abs/2603.22455

Why it matters:

- Directly targets skill routing at large scale.
- Argues that exposing every skill is infeasible when skill ecosystems grow.
- Shows that hiding the full skill body causes a large routing accuracy drop.
- Proposes a compact retrieve-and-rerank pipeline using a first-stage embedding model and reranker.

How it affects this thesis:

- Strongly supports testing full-skill representations, not only metadata descriptions.
- Supports M6 as a realistic method family: first-stage retrieval followed by reranking.
- Also warns that description-only baselines may be too weak if treated as the final embedding baseline.
- The authors appear to have released `pipizhao/SkillRouter-Embedding-0.6B` and `pipizhao/SkillRouter-Reranker-0.6B`, so these are candidates for the next stronger baseline if local memory or API access allows.

### SkillRet: A Large-Scale Benchmark for Skill Retrieval in LLM Agents

Source: https://arxiv.org/abs/2605.05726

Why it matters:

- Introduces a large skill retrieval benchmark with public skills and structured tags.
- Finds that off-the-shelf retrievers still struggle on realistic skill libraries.
- Shows task-specific fine-tuning improves skill retrieval.

How it affects this thesis:

- Supports the claim that skill retrieval is not solved by generic IR models.
- Positions this benchmark as narrower: semantic confusion between procedurally different skills, rather than only broad-scale skill retrieval.

### Skill Retrieval Augmentation for Agentic AI

Source: https://arxiv.org/abs/2604.24594

Why it matters:

- Frames dynamic skill retrieval as Skill Retrieval Augmentation.
- Builds a decomposed benchmark across retrieval, incorporation, and end-task execution.
- Finds that bottlenecks include both retrieval and whether the base model actually loads/uses retrieved skills.

How it affects this thesis:

- Strongly supports separating Step 7 retrieval evaluation from Step 8 M0 behavior and Step 9 downstream execution under the current numbering.
- Explains why M0 sometimes loads no skill: skill incorporation is itself a separate failure mode.

### ToolRet: Retrieval Models Aren't Tool-Savvy

Source: https://arxiv.org/abs/2503.01763

Why it matters:

- Shows that tool retrieval is a distinct IR problem, not ordinary document retrieval.
- Reports that even strong IR models perform poorly on tool retrieval.
- Links retrieval quality to downstream tool-use agent pass rate.

How it affects this thesis:

- Provides support for using top-k, MRR, and downstream task success rather than only qualitative examples.
- Helps justify why semantic confusability and procedural suitability require a dedicated benchmark.

### ToolRerank: Adaptive and Hierarchy-Aware Reranking for Tool Retrieval

Source: https://arxiv.org/abs/2403.06551

Why it matters:

- Explicitly studies reranking after initial tool retrieval.
- Adds adaptive truncation and hierarchy-aware reranking.
- Shows reranking can improve retrieval quality and downstream LLM execution.

How it affects this thesis:

- Supports M6 reranking and later M4/M5 tree/graph variants.
- Useful contrast: ToolRerank uses hierarchy-aware signals; our current M6 uses procedural schema signals.

## What Reranking Means Here

In normal IR and tool retrieval, reranking means:

- first-stage retriever returns a candidate pool, often top-20, top-50, or top-100
- reranker scores query-candidate pairs more carefully
- final rank is computed only inside the candidate pool

Typical rerankers:

- cross-encoder reranker: jointly reads query and candidate text
- LLM reranker: asks an LLM to compare candidates or score relevance
- hybrid lexical/dense fusion: combines sparse and dense rank signals
- structure-aware reranker: uses fields, schemas, hierarchy, dependencies, or metadata

Our current M6 is a local, deterministic structure-aware reranker:

- first stage: BM25, TF-IDF, or MiniLM full-skill retrieval
- candidate pool: top-20
- reranking evidence: description, use_when, output_shape, preconditions, workflow, dependency/resource fields
- penalty: mild overlap with `not_for`
- final score: 40% normalized first-stage score + 60% normalized schema score

This is not a neural reranker yet. It is a reproducible local baseline showing whether procedural schema information can improve a first-stage retriever.

## Provider Baselines Added

The benchmark now has an optional provider runner:

- script: `skill_benchmark/scripts/run_provider_selectors.py`
- setup note: `skill_benchmark/notes/provider_api_baselines.md`
- key template: `.env.example`

The first recommended provider baseline is Qwen:

- M7: `text-embedding-v4` embedding retrieval over full `SKILL.md`, R2 schema cards, or R1 metadata cards.
- M8: `text-embedding-v4` first-stage retrieval followed by `qwen3-rerank` over top-20 candidates.

This should be treated as a stronger neural comparison against local M6. It does not replace the representation question. It tests whether a modern embedding/reranker still benefits from full procedural artifacts or structured procedural fields when skills are semantically confusable.

## Current M6 Result

On the current 1006-skill library:

| Method | Top-1 | Top-5 | MRR | Non-core top-1 |
|---|---:|---:|---:|---:|
| M2b MiniLM full-skill | 61.2% | 82.1% | 0.717 | 9.0% |
| M3 TF-IDF schema | 71.6% | 95.5% | 0.807 | 9.0% |
| M6 BM25 -> schema rerank | 71.6% | 92.5% | 0.815 | 7.5% |
| M6 TF-IDF -> schema rerank | 70.2% | 85.1% | 0.778 | 10.4% |
| M6 MiniLM full -> schema rerank | 80.6% | 91.0% | 0.856 | 7.5% |

Interpretation:

- The best current method is M6 MiniLM full-skill first stage plus schema reranking.
- This supports the thesis direction: full procedural skill evidence helps, and reranking can turn a semantically plausible candidate pool into a better final selection.
- However, this still needs a stronger modern embedding/reranker baseline, such as Qwen3/SkillRouter-style models, before making final thesis claims.

## Updated Literature Framing

The thesis should not frame embedding retrieval as the only baseline. A stronger framing is:

- M0: progressive disclosure baseline
- M1: scalable flat metadata retrieval
- M2: embedding retrieval over description or full skill body
- M3: schema-enriched procedural retrieval
- M6: hybrid retrieve-and-rerank
- M7/M8: provider-backed neural retrieval and neural reranking

The main comparison should ask:

Does preserving procedural structure improve retrieval and reranking under semantic confusion, especially when the first-stage retriever has already found plausible but confusable candidates?

## Immediate Next Work

1. Run Qwen `text-embedding-v4` full-skill retrieval on a 5-prompt smoke test, then on the 67-prompt benchmark if the setup works.
2. Run Qwen `text-embedding-v4` plus `qwen3-rerank` over top-20 candidates.
3. Compare M7/M8 against local M1-M6 in the same 1006-skill scale condition.
4. Check whether SkillRouter released models can be run locally, quantized, or remotely without exceeding laptop memory constraints.
5. Run Step 9 downstream artifact validation on the 12-prompt sample after M7/M8 retrieval behavior is known. The downstream-plan filenames still use `step8` from the earlier numbering.
