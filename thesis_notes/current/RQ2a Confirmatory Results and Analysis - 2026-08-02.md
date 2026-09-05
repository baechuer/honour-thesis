# RQ2a Confirmatory Results and Analysis

Date: 2026-08-02

Status: **COMPLETE / USER-REVIEWED FOR THESIS INTEGRATION**

Protocol: `rq2a-matched-content-v1.0`

This is the thesis-facing source of truth for the completed RQ2a matched-content study. The user reviewed the result boundary and approved thesis integration on 2026-08-02. Earlier smoke and development observations remain implementation history and must not replace the confirmatory estimates below.

## 1. Research question and scope

RQ2a asks:

> Given the same query, the same three sibling candidates, the same reviewed operational propositions, and the same selector, how do explicit field organisation, discourse form, field order, and controlled information dilution affect selection among semantically similar skills?

RQ2a is a fixed-candidate mechanism study. It isolates representation effects and one explicit-use mechanism while the gold skill is guaranteed to be among the same three candidates. It does not test full-library candidate generation, Recall@K, graph/tree retrieval, downstream execution success, or public-library generalisation. Those questions belong to RQ2b or external validation.

## 2. Source, split, and experimental unit

The source is the seven reviewed RQ1a field-isolation suites: use condition, input/precondition, output/artifact, workflow/procedure, dependency/resource, boundary/not-for, and success/verification.

- Total source: 350 clusters, 750 prompts, and three sibling candidates per cluster.
- Development: 70 clusters and 150 prompts.
- Confirmatory: 280 clusters and 600 prompts.
- Confirmatory matrix: 22 selector-representation conditions and 13,200 unique aligned condition-prompt rows.

For the target field of each RQ1a suite, the three candidates retain their reviewed candidate-specific values. All six non-target fields use the same reviewed shared values. This makes the candidates semantically close while preserving exactly one controlled operational distinction.

## 3. Matched representations

Except for the negative control, every representation contains identical reviewed propositions. Only organisation, discourse, order, or sibling-identical padding changes.

| Representation | Selector-visible treatment |
|---|---|
| `shared-only` | Shared ambiguity anchor only; all three candidate texts are byte-identical. |
| `same-facts-flat` | All seven propositions in canonical order, without semantic field labels. |
| `same-facts-fielded` | The same propositions under seven explicit field headings. |
| `same-facts-prose` | The same propositions in one frozen connected-prose template. |
| `same-facts-order-controlled` | Fielded text with counterbalanced field-order rotations. |
| `same-facts-diluted-1x/2x/4x` | Exact fielded text plus increasing sibling-identical neutral support notes. |

The validator proved proposition-hash equivalence, candidate alignment, absence of role/gold/field-suite leakage, exact sibling identity for `shared-only`, controlled order, padding identity, and no decisive-text truncation.

## 4. Selectors and the Qwen-SkillRouter distinction

| Selector | Architecture used in RQ2a | Scoring behaviour |
|---|---|---|
| BM25 | Lexical scorer | Computes BM25 within each fixed three-sibling decision corpus. |
| Qwen single-vector | Bi-encoder embedding model: DashScope `text-embedding-v4`, 1024 dimensions | Embeds the query and complete candidate independently; ranks by cosine similarity. Candidate embeddings are reusable across queries. |
| SkillRouter | Cross-encoder reranker model: `pipizhao/SkillRouter-Reranker-0.6B` | Reads each query-candidate pair jointly and outputs a yes-minus-no relevance logit. It does not use the SkillRouter embedding model in RQ2a. |
| Qwen field-aware | Seven-component bi-encoder scorer | Embeds the query and each labelled field separately; frozen `uniform-top-two` averages the two highest field similarities. |

The current RQ2a SkillRouter condition is therefore not "another embedding condition". A bi-encoder can precompute document vectors but compresses each candidate into one vector. A cross-encoder recomputes joint token-level interaction for every new query-candidate pair, usually improving ranking accuracy at substantially higher online cost.

No SkillRouter-native field-aware condition was included. Historical SkillRouter-first-stage plus M6 field-aware rows use a separate second-stage matcher and are not equivalent. Adding a SkillRouter embedding field-aware method now would be a post-hoc exploratory extension, not part of this frozen confirmatory study.

## 5. Preregistered hypotheses and decision rule

The primary hypothesis expected `same-facts-fielded` to improve Qwen single-vector selection over matched `same-facts-flat`. Secondary hypotheses tested the same organisation effect under BM25 and SkillRouter, fielded versus prose, field-aware versus Qwen fielded single-vector, dilution, and three operational-content positive controls.

The primary deployment metric is cluster-weighted tie-adjusted Top-1. Prompt differences are paired, averaged within cluster, and then averaged across clusters. Inference uses 10,000 cluster bootstraps and 10,000 paired cluster sign-flip randomisations. The eight secondary Top-1 contrasts use full-family Holm correction. Practical support requires a gain of at least 3 percentage points and a 95% cluster-bootstrap interval excluding zero.

MRR, margin, strict confusion, tie rate, field and prompt-variant slices, order, the full dilution curve, and costs are descriptive supporting evidence.

## 6. Full confirmatory condition matrix

| Selector | Representation | Top-1 | MRR | Strict confusion | Tie rate |
|---|---|---:|---:|---:|---:|
| BM25 | diluted 1x | 0.864 | 0.920 | 0.127 | 0.023 |
| BM25 | diluted 2x | 0.863 | 0.919 | 0.128 | 0.023 |
| BM25 | diluted 4x | 0.864 | 0.920 | 0.127 | 0.023 |
| BM25 | fielded | 0.864 | 0.921 | 0.127 | 0.023 |
| BM25 | flat | 0.843 | 0.911 | 0.147 | 0.023 |
| BM25 | order-controlled | 0.864 | 0.921 | 0.127 | 0.023 |
| BM25 | prose | 0.840 | 0.908 | 0.152 | 0.023 |
| BM25 | shared-only | 0.333 | 0.611 | 0.000 | 1.000 |
| Qwen field-aware uniform top two | fielded | 0.823 | 0.901 | 0.145 | 0.057 |
| Qwen single-vector | diluted 1x | 0.778 | 0.876 | 0.228 | 0.000 |
| Qwen single-vector | diluted 2x | 0.778 | 0.872 | 0.232 | 0.000 |
| Qwen single-vector | diluted 4x | 0.763 | 0.867 | 0.247 | 0.000 |
| Qwen single-vector | fielded | 0.757 | 0.863 | 0.252 | 0.000 |
| Qwen single-vector | flat | 0.824 | 0.902 | 0.185 | 0.000 |
| Qwen single-vector | order-controlled | 0.790 | 0.880 | 0.223 | 0.000 |
| Qwen single-vector | prose | 0.782 | 0.873 | 0.233 | 0.000 |
| Qwen single-vector | shared-only | 0.333 | 0.611 | 0.000 | 1.000 |
| SkillRouter cross-encoder | diluted 2x | 0.942 | 0.967 | 0.063 | 0.000 |
| SkillRouter cross-encoder | fielded | 0.951 | 0.973 | 0.053 | 0.000 |
| SkillRouter cross-encoder | flat | 0.955 | 0.975 | 0.048 | 0.000 |
| SkillRouter cross-encoder | prose | 0.946 | 0.969 | 0.058 | 0.000 |
| SkillRouter cross-encoder | shared-only | 0.333 | 0.611 | 0.000 | 1.000 |

`shared-only` produces the designed three-way tie: tie-adjusted Top-1 is `1/3 = 0.333`, and tie-adjusted MRR is `(1 + 1/2 + 1/3) / 3 = 0.611`.

## 7. Preregistered contrasts

| Contrast | Paired Top-1 difference | 95% cluster-bootstrap CI | Raw p | Holm p | Practical support |
|---|---:|---:|---:|---:|---|
| Primary: Qwen fielded - flat | -0.067 | [-0.099, -0.036] | 0.0002 | Not applicable | No |
| BM25 fielded - flat | +0.021 | [+0.010, +0.033] | 0.0008 | 0.0040 | No |
| SkillRouter fielded - flat | -0.004 | [-0.014, +0.006] | 0.5240 | 0.5240 | No |
| Qwen fielded - prose | -0.025 | [-0.060, +0.010] | 0.1594 | 0.3188 | No |
| Field-aware - Qwen fielded | +0.066 | [+0.021, +0.111] | 0.0051 | 0.0204 | Yes |
| Qwen fielded - diluted 2x | -0.021 | [-0.036, -0.006] | 0.0101 | 0.0303 | No |
| Qwen fielded - shared-only | +0.424 | [+0.380, +0.467] | 0.0001 | 0.0008 | Yes |
| BM25 fielded - shared-only | +0.531 | [+0.506, +0.555] | 0.0001 | 0.0008 | Yes |
| SkillRouter fielded - shared-only | +0.618 | [+0.599, +0.635] | 0.0001 | 0.0008 | Yes |

The primary positive organisation hypothesis is rejected. Under Qwen single-vector pooling, explicit headings reduce Top-1 by 6.7 percentage points relative to matched flat propositions. BM25 obtains a statistically detectable 2.1-point fielded gain, but it does not meet the 3-point practical threshold. SkillRouter is insensitive to fielded versus flat form within its interval.

The frozen field-aware Qwen rule gains 6.6 points over Qwen fielded single-vector and clears the inferential and practical criteria. Its Top-1 of 0.823 is nevertheless almost identical to flat Qwen at 0.824. It recovers the fielded single-vector penalty; it does not establish superiority over the strongest Qwen serialisation.

## 8. Field-level descriptive heterogeneity

| Field | Qwen flat | Qwen fielded | Qwen field-aware | Field-aware - fielded |
|---|---:|---:|---:|---:|
| Use condition | 0.925 | 0.888 | 0.938 | +0.050 |
| Input/precondition | 0.913 | 0.888 | 0.900 | +0.013 |
| Output/artifact | 0.963 | 0.950 | 0.917 | -0.033 |
| Workflow/procedure | 0.638 | 0.600 | 0.658 | +0.058 |
| Dependency/resource | 0.963 | 0.963 | 0.771 | -0.192 |
| Boundary/not-for | 0.683 | 0.625 | 0.739 | +0.114 |
| Success/verification | 0.688 | 0.388 | 0.838 | +0.450 |

Uniform top-two especially recovers success/verification, boundary, workflow, and use-condition cases, but suppresses strong dependency and output signals. These slices were not separately multiplicity-tested. They motivate field-adaptive aggregation but are not seven additional confirmatory claims.

Prompt-variant slices show the same mechanism pattern. Qwen field-aware improves over Qwen fielded on direct (`0.848` versus `0.793`), paraphrase (`0.808` versus `0.696`), and implicit-authority (`0.608` versus `0.500`) prompts, while it is lower on the small contextual subset (`0.867` versus `1.000`). These are descriptive only.

## 9. Cost, latency, and persistence

| Primary run | New API calls | Provider tokens | Construction wall | Online time per prompt | Total wall |
|---|---:|---:|---:|---:|---:|
| BM25 | 0 | 0 | 0.000 s | 0.001100 s | 0.945 s |
| Qwen single-vector | 590 | 1,175,784 | 1,085.293 s | 0.002869 s | 1,087.359 s |
| Qwen field-aware | 77 | 13,583 | 203.259 s | 0.002398 s | 204.760 s |
| SkillRouter cross-encoder | 0 | 0 | 0.000 s | 11.099921 s | 6,666.917 s |

All 600 query embeddings were cache hits, so confirmatory sent no query text. The 667 successful DashScope calls embedded 6,661 unique new candidate/component texts and used 1,189,367 provider tokens. The dated standard-list-price estimate is USD 0.08325569. Warm verification made zero provider calls and zero new SkillRouter forward passes.

Qwen candidate construction is primarily a one-time cost followed by millisecond cosine scoring. SkillRouter's cross-encoder is much more accurate but recomputes each novel query-candidate pair; its cached lookup time must not be reported as the cost of novel inference.

## 10. Failure decomposition

- Qwen fielded helps over flat on 21 prompts.
- Qwen fielded harms relative to flat on 61 prompts.
- Both Qwen fielded and flat fail on 90 prompts.
- Field-aware recovers 84 Qwen-fielded failures.
- Field-aware harms 54 Qwen-fielded successes.

These counts are descriptive and do not form another inferential family.

## 11. RQ2a answer and claim boundary

The completed evidence supports the following bounded answer:

> In fixed-candidate near-neighbour skill routing, candidate-specific operational facts are essential, but explicit field headings are not an independent or universal source of accuracy. A pooled single-vector embedding can perform worse when the same facts are fielded. Explicit field-wise scoring can recover that pooling penalty for several conditional fields, but the frozen uniform-top-two policy does not outperform the best matched flat Qwen representation overall. Representation value is therefore conditional on retrieval architecture and field type.

The thesis may claim:

1. Operational facts strongly improve selection over shared context without those facts.
2. Field headings alone are not reliably beneficial and harm the tested Qwen single-vector condition.
3. Explicit field-wise Qwen scoring recovers the fielded single-vector deficit, with heterogeneous field effects.
4. SkillRouter cross-encoder is the strongest fixed-candidate selector in this matrix but has far higher novel-query compute cost.
5. Flat propositions remain a strong semantic-embedding baseline.

The thesis must not claim that field-aware routing universally wins, that SkillRouter-native field-aware scoring was tested, that the result establishes full-library candidate recall, or that graph/tree/downstream methods have been evaluated.

## 12. Evidence

- Frozen analysis: `skill_benchmark/outputs/rq2a_matched_content/analysis/confirmatory-complete-v1/analysis.json`, SHA-256 `189d6b20b091e2f2d3bd30f168355ccf2a73efa3eef3b082075725040fec0ce7`.
- Cost ledger: `skill_benchmark/outputs/rq2a_matched_content/analysis/confirmatory-complete-cost-v1/cost_ledger.json`, SHA-256 `980af3ff9c9106d7f43d029b69aa5a1bb07515faf2e15b0b96e70bca5332cdec`.
- Failure report: `skill_benchmark/outputs/rq2a_matched_content/analysis/confirmatory-failures-v1/failure_report.json`, SHA-256 `a0e96747f544904d424bf6fe83a656bd3b27533b4e2b2c9b8166fb91a8c6d155`.
- Execution audit: `thesis_notes/checkpoints/RQ2a Stage 5 Confirmatory Completion Audit - 2026-08-02.md`.
- Protocol and run ledger: `thesis_notes/current/RQ2a Execution Protocol and Run Ledger - 2026-07-26.md`.
