# RQ2a Execution Protocol and Run Ledger

Date: 2026-07-26

Protocol version: `rq2a-matched-content-v1.0`

Status: **COMPLETE / USER-REVIEWED / THESIS-INTEGRATED**

Authority: the user authorised RQ2a implementation and execution on 2026-07-26. This document operationalises the approved RQ2a design in `RQ2 Current Status and Implementation Tracker - 2026-07-26.md`.

Scope boundary:

- implement and run RQ2a only;
- do not implement or run RQ2b;
- do not start graph, tree, relation, full-library, or downstream-execution studies;
- do not insert new RQ2a methods, results, or interpretations into the thesis LaTeX/PDF until the user reviews them; this gate was satisfied on 2026-08-02;
- preserve every development and confirmatory artifact rather than overwriting it.

## 1. RQ2a Question

> Given the same query, the same three sibling candidates, the same reviewed operational propositions, and the same selector, how do explicit field organisation, discourse form, field order, and controlled information dilution affect selection among semantically similar skills?

RQ2a is a fixed-candidate mechanism study. It does not test full-library candidate generation.

## 2. Frozen Source

The source is the seven reviewed RQ1a operational-field suites:

| Suite | Clusters | Prompt rows |
|---|---:|---:|
| `use_condition` | 50 | 100 |
| `input_precondition` | 50 | 100 |
| `output_artifact` | 50 | 100 |
| `dependency_resource` | 50 | 100 |
| `boundary_not_for` | 50 | 150 |
| `success_verification` | 50 | 100 |
| `workflow_procedure` | 50 | 100 |
| **Total** | **350** | **750** |

`examples_test` is a supporting negative control and is excluded from the primary RQ2a source. It may be added only after all primary decisions are frozen.

Source policy:

- read each cluster's reviewed `unit.json`;
- read the corresponding suite `prompts.jsonl`;
- do not infer or rewrite a field value;
- do not use generated `SKILL.md` prose as the canonical proposition source;
- preserve source paths and SHA-256 hashes.

## 3. Frozen Split

Split seed: `rq2a-v1-2026-07-26`

Algorithm:

1. group clusters by the seven field suites;
2. compute SHA-256 over `seed + "\n" + field + "\n" + cluster_id`;
3. sort each field by the digest and then by `cluster_id`;
4. assign the first 10 clusters in each field to `development`;
5. assign the remaining 40 clusters in each field to `confirmatory`.

Expected split:

- development: 70 clusters and approximately 150 prompt rows;
- confirmatory: 280 clusters and approximately 600 prompt rows.

The development split may be used for implementation QA and the single field-aware aggregation decision. Confirmatory results may not be inspected until representation and selector gates pass and the protocol/hash manifest is frozen.

## 4. Canonical Proposition Mapping

Each candidate has exactly seven canonical fields:

1. `use_condition`
2. `input_precondition`
3. `output_artifact`
4. `workflow_procedure`
5. `dependency_resource`
6. `boundary_not_for`
7. `success_verification`

For the target field of a suite, use the candidate-specific value from `unit["skills"]`. For every non-target field, use the corresponding shared value:

| Canonical field | Shared source |
|---|---|
| `use_condition` | `shared_use_condition` |
| `input_precondition` | `shared_input_precondition` |
| `output_artifact` | `shared_output_artifact` |
| `workflow_procedure` | `shared_workflow_steps` |
| `dependency_resource` | `shared_dependencies` |
| `boundary_not_for` | `shared_boundaries` |
| `success_verification` | `shared_success_criteria` |

Missing non-target shared fields are an error. Scalar values become one-item proposition arrays. List values preserve source order. Empty strings and empty lists are errors.

`shared_context` is an ambiguity-anchor description. It is not an eighth operational proposition.

## 5. Frozen Representation Serialisers

Serializer version: `rq2a-serialiser-v1.4`

All selector-visible representations use the identical neutral header `Skill candidate`. Candidate IDs, Option A/B/C labels, roles, target fields, field-suite names, and gold labels are metadata only and must never appear in selector-visible text.

Canonical field order:

1. Use Condition
2. Input / Precondition
3. Output Artifact
4. Workflow / Procedure
5. Dependency / Resource
6. Boundary / Not For
7. Success / Verification

### 5.1 `shared-only`

```text
Skill candidate

{shared_context}
```

All three siblings in a cluster must be byte-identical.

### 5.2 `same-facts-fielded`

```text
Skill candidate

Use Condition
{value}

Input / Precondition
{value}

Output Artifact
{value}

Workflow / Procedure
1. {item}
2. {item}

Dependency / Resource
- {item}

Boundary / Not For
- {item}

Success / Verification
- {item}
```

Scalar fields are printed without bullets. Multi-item workflow values are numbered. Other multi-item fields use bullets. Source proposition text is not paraphrased.

### 5.3 `same-facts-flat`

Use the exact same proposition arrays and canonical order as `same-facts-fielded`, remove all field labels, and separate the seven value blocks with:

```text

---

```

The identical neutral `Skill candidate` header remains. The separator conveys a boundary but not a semantic field identity.

### 5.4 `same-facts-prose`

Use this fixed connector template and insert each source proposition unchanged:

```text
Skill candidate

This skill is used under these conditions: {use_condition}. Its input or precondition is: {input_precondition}. It produces this output artifact: {output_artifact}. It follows this workflow or procedure: {workflow_procedure}. It depends on these resources or capabilities: {dependency_resource}. It is outside scope under these boundaries: {boundary_not_for}. Success is verified by: {success_verification}.
```

Each source proposition remains verbatim and in source order. If a proposition has no terminal `.`, `!`, or `?`, the serialiser appends one grammatical full stop; otherwise it adds no punctuation. Multiple propositions are joined with one space. This v1.3 rule replaces the pre-score v1.2 template, which created duplicate punctuation after already punctuated source values. Connectors and added terminal punctuation are frozen and are not treated as source propositions.

### 5.5 `same-facts-order-controlled`

Use the exact `same-facts-fielded` renderer while rotating only field order.

Counterbalancing:

1. sort clusters within each field by the frozen split digest;
2. let `field_index` be the field's index in canonical order;
3. assign rotation `(rank_within_field + field_index) mod 7`;
4. rotate the canonical seven-field order left by that amount.

This yields 50 uses of each rotation across 350 clusters and prevents one target field from always occupying one position.

### 5.6 Length-Sensitivity Decision

The initial v1 prose renderer added duplicate terminal punctuation and produced a 15.5% median audit-token difference from fielded, provisionally triggering a length control. The independent leakage validator then rejected two trial control words, and human review identified the duplicate-punctuation cause. After the prose renderer was corrected without changing any source proposition, final v1.4 prose has 205 median audit tokens versus 187 for fielded, a 9.6% difference. This is below the frozen 10% trigger. Therefore no separate prose-length-control representation is included in scoring. The failed and intermediate artifacts remain archived for provenance.

### 5.7 Dilution Conditions

Each condition starts with byte-identical `same-facts-fielded` text and appends a `Support Notes` section. The blocks are:

- `P1`: `Carry out the assigned work carefully and consistently.`
- `P2`: `Keep an orderly account of progress during completion.`
- `P3`: `Check the finished material before delivery.`
- `P4`: `State any remaining caveats clearly for the recipient.`

Conditions:

- `same-facts-diluted-1x`: P1
- `same-facts-diluted-2x`: P1 + P2
- `same-facts-diluted-4x`: P1 + P2 + P3 + P4

Padding must be byte-identical among siblings. The validator must reject a cluster if a padding block contains any reviewed leakage term or any complete sibling-specific target value under case-folded phrase matching.

## 6. Representation Output Contract

Each representation contains exactly 1,050 candidate rows: 350 clusters x 3 siblings. Final serializer v1.4 emits the eight preregistered conditions.

Each row records:

- protocol and serializer versions;
- representation label and split;
- field suite, cluster ID, skill ID, role, and source path;
- source-unit and source-prompt hashes;
- canonical proposition arrays and proposition hashes;
- selector-visible text and text hash;
- field order and padding blocks;
- character, UTF-8 byte, word, and fixed audit-token counts.

Prompt manifest contains exactly 750 rows and records query text, optional routing context, prompt variant, candidate identities, gold identity, split, and source hash.

The fixed audit tokenizer is the regex `\w+|[^\w\s]` with Unicode enabled. It supports comparable representation-length reporting; it is not claimed to equal provider billing tokens. Provider-returned usage is recorded separately when available.

## 7. Representation Quality Gates

Representation implementation passes only if:

1. source coverage is 350 clusters, 750 prompts, and three candidates per cluster;
2. every representation has 1,050 unique `(cluster_id, skill_id)` rows;
3. every prompt references one known cluster, three aligned candidates, and exactly one gold candidate;
4. all candidate proposition arrays equal the canonical source mapping;
5. fielded, flat, prose, order-controlled, and diluted variants have identical proposition hashes;
6. no selector-visible text contains skill IDs, role labels, Option A/B/C labels, target-field metadata, or suite metadata;
7. `shared-only` is byte-identical among siblings;
8. flat text contains no canonical field label;
9. prose contains every source proposition verbatim after whitespace normalisation;
10. order-controlled positions follow the frozen rotation schedule;
11. each dilution condition begins with exact fielded text;
12. padding is byte-identical among siblings and passes the leakage check;
13. source and output hashes are present;
14. no row is empty or duplicated;
15. a sample review covers at least one development and one confirmatory cluster per field;
16. median length differences are reported; if fielded versus flat or prose differs by more than 10%, a length-matched sensitivity is designed before confirmatory scoring rather than silently changing the core condition.

## 8. Frozen Selectors

### 8.1 BM25

- tokenizer: lowercase ASCII alphanumeric regex `[a-z0-9]+`;
- `k1 = 1.5`;
- `b = 0.75`;
- corpus for each decision: the three sibling candidate documents only;
- query: raw prompt plus `Routing context:` only where the reviewed source prompt already contains routing context.

Purpose: lexical baseline and a check of whether labels or dilution alter exact-term matching.

### 8.2 Qwen Single-Vector Embedding

- provider: Qwen/DashScope OpenAI-compatible endpoint;
- model: `text-embedding-v4`;
- output dimension: 1024;
- one vector for each complete candidate representation;
- one vector for each raw query;
- score: cosine similarity;
- persistent cache keyed by provider, endpoint, model, dimension, and exact text;
- no truncation is permitted; token/length audit must establish that every input is within the model limit before scoring.
- implementation guard: reject any input above 8,192 fixed audit tokens before an API call; provider acceptance and returned usage are additionally recorded because the audit tokenizer is not the provider tokenizer.

Purpose: primary generic semantic selector.

### 8.3 SkillRouter Cross-Encoder

- model: `pipizhao/SkillRouter-Reranker-0.6B`;
- frozen model revision: `78986e1142d12857cfd85b8005e62902cd42d858`;
- direct query-document scoring for all three candidates;
- no embedding first stage;
- no candidate exclusion;
- maximum input length: 2048 model tokens;
- no decisive text may be truncated;
- score: released model's `yes` logit minus `no` logit;
- persistent query-document score cache.

Purpose: stronger joint query-document interaction and reasoning-sensitive replication.

### 8.4 Qwen Semantic Field-Aware Selector

- input representation: `same-facts-fielded`;
- separately embed the reviewed `query_text` and each of the seven candidate fields;
- component text is the exact labelled field block already present in `same-facts-fielded`, for example `Input / Precondition\n{verbatim proposition}`; multi-item formatting remains numbered for workflow and bulleted for other fields;
- component score: cosine similarity;
- no target-field, suite, gold, role, or alternative metadata;
- no first-stage score;
- no field-specific weight;
- development candidates:
  - maximum of seven field similarities;
  - uniform mean of the highest two field similarities;
- choose one aggregation on development by higher cluster-level tie-adjusted Top-1; break an exact tie by higher tie-adjusted MRR, then prefer uniform top-two;
- freeze the selected rule before confirmatory scoring;
- persist all seven component scores, aggregate score, selected rule, latency, and cache usage.

Purpose: isolate explicit field-wise use from single-vector pooling on identical fielded facts.

### 8.5 Fixed LLM Selector Diagnostic

The LLM selector remains secondary and does not block the primary BM25/Qwen/cross-encoder/field-aware matrix. Before it is run, its model, prompt, candidate-order randomisation, abstention rule, temperature, cache, and sample scope must be appended to this ledger. It may not be selected using confirmatory results.

## 9. Frozen Matrix

Core representations:

- `shared-only`
- `same-facts-fielded`
- `same-facts-flat`
- `same-facts-prose`
- `same-facts-diluted-2x`

Core selectors:

- BM25
- Qwen single-vector
- SkillRouter cross-encoder

Required mechanism comparison:

- Qwen field-aware on `same-facts-fielded`

Diagnostics after core freeze:

- Qwen and BM25 on `same-facts-order-controlled`;
- Qwen and BM25 on the 0x/1x/2x/4x dilution curve;
- optional fixed LLM diagnostic.

## 10. Metrics and Why They Matter

### Primary metric

**Tie-adjusted Top-1 accuracy**

- gold receives `1 / tie_size` when tied for the highest score;
- gold receives zero when any alternative has a strictly higher score;
- report the paired difference between representations on the same prompts;
- aggregate and bootstrap by cluster, preserving all prompt variants within a resampled cluster.

Why: deployment normally selects one skill, while tie adjustment prevents the always-Option-A controlled data from receiving artificial credit through deterministic tie-breaking.

Primary contrast:

> `same-facts-fielded - same-facts-flat` under Qwen single-vector on confirmatory clusters.

### Secondary metrics

| Metric | Meaning and significance |
|---|---|
| Tie-adjusted MRR | Uses the full within-cluster rank and detects improvements that move gold upward without reaching rank 1. |
| Gold margin | Gold score minus the maximum alternative score; measures decision confidence within one selector. Raw margins are not compared across differently scaled selectors. |
| Near-neighbour confusion rate | Fraction where a non-gold sibling strictly outranks gold; distinguishes active confusion from exact ties. |
| Tie rate and mean tie size | Reveals whether a method truly discriminates or merely returns equal scores. |
| Per-field accuracy | Tests whether effects concentrate in input/output/dependency versus workflow/boundary/success fields. |
| Prompt-variant accuracy | Detects dependence on direct wording, paraphrase, contextual dependency cues, or implicit authority cues. |
| Characters, bytes, words, audit tokens | Measures representation size without pretending one tokenizer is universal. |
| Cold/warm latency | Separates one-time encoding/cache construction from repeated routing cost. |
| API calls, cache hits/misses, provider usage | Supports reproducibility and cost accounting. |

Recall@K and candidate recall are not RQ2a metrics because all three sibling candidates, including gold, are guaranteed present. Reporting Recall@K here would be structurally uninformative.

## 11. Statistical Inference

- unit of resampling: cluster;
- bootstrap resamples: 10,000;
- confidence interval: percentile 95%;
- primary contrast: one preregistered contrast, no multiplicity correction;
- confirmatory Top-1 p-values: paired cluster sign-flip randomisation with 10,000 resamples;
- secondary Top-1 contrast family: eight contrasts frozen in `analysis_spec.json`, with Holm correction across the full family;
- MRR, margins, field/variant slices, order, the complete dilution curve, and cost remain descriptive supporting evidence rather than additional claim-selection tests;
- report effect size even when the interval includes zero;
- practical-support threshold: at least +3 percentage points paired Top-1 and a 95% cluster-bootstrap interval excluding zero;
- null and negative results remain valid when quality gates pass.

The 3 percentage-point threshold is an interpretation rule, not a software pass/fail rule.

## 12. Expected Patterns and Interpretation

| Result pattern | Initial interpretation |
|---|---|
| All same-facts variants beat `shared-only` | The reviewed operational facts remain necessary and the runner is behaving coherently. |
| Fielded > flat under Qwen by at least 3pp with CI above zero | Explicit labels/boundaries add usable organisation for a generic semantic selector. |
| Fielded approximately flat, both > shared-only | Operational content matters more than literal field labels. |
| Prose approximately fielded | Compact proposition-preserving prose can carry the same routing information. |
| Prose < fielded | Explicit boundaries reduce discourse ambiguity or pooling dilution. |
| Accuracy or margin declines along 0x/1x/2x/4x | Shared support text dilutes decisive information. |
| Field-aware > single-vector on identical fielded text | Explicit field-wise comparison uses structure that one-vector pooling loses. |
| Field-aware approximately single-vector | Field boundaries alone do not help under the frozen target-agnostic aggregation. |
| Cross-encoder gains mainly on workflow/boundary/success | Joint reasoning helps conditional or procedural fields. |
| Same-facts fails to beat `shared-only` | Treat first as a representation/runner validity failure; investigate before scientific interpretation. |

No representation is required to win for RQ2a to be scientifically complete.

## 13. State Ledger

| ID | Stage | State | Completion evidence |
|---|---|---|---|
| A0 | Protocol and scope freeze | `COMPLETE` | This versioned ledger and user authorisation. |
| A1 | Deterministic split | `COMPLETE` | Split JSON/MD, counts, seed, hashes. |
| A2 | Canonical source loader | `COMPLETE` | 350/750/1,050 source audit. |
| A3-A7 | Representation serialisers | `COMPLETE / V1.4 FROZEN` | Eight representation JSONL files and manifest. |
| A8 | Representation validator | `COMPLETE / PASS` | Machine validation and 14-cluster manual sample review. |
| A9 | Shared result schema/runner | `COMPLETE / LOCAL TEST PASS` | Common schema, metrics, artifact loader, row hashes, manifests, and offline adapter tests. |
| A10 | BM25 adapter | `COMPLETE / REAL SMOKE PASS` | 15 prompts, 7 clusters, 30 persisted result rows with aligned candidates. |
| A11 | Qwen single-vector adapter | `COMPLETE / REAL COLD+WARM SMOKE PASS` | 30 aligned cold rows, 28 new document embeddings, 15 query-cache hits, and 43/43 warm-cache hits with zero API calls. |
| A12 | Cross-encoder adapter | `COMPLETE / REAL LOCAL SMOKE PASS` | Pinned released model, direct three-candidate scoring, 45-pair cold run, 45/45 warm-cache reuse, and zero truncation. |
| A13 | Field-aware adapter | `COMPLETE / REAL COLD+WARM SMOKE PASS` | 30 aligned cold rows, exact seven-field blocks, 55 new component embeddings, 70/70 warm-cache hits, and a provisional non-frozen smoke comparison. |
| A14 | LLM diagnostic | `OPTIONAL / DEFERRED` | Additional freeze record required before execution. |
| A15 | Development run | `COMPLETE / PASS` | All 21 fixed core conditions plus both field-aware aggregation candidates cover 70 clusters and 150 prompts; four canonical primary runs contain 3,450 aligned rows. |
| A16 | Confirmatory freeze | `COMPLETE / REPAIRED FREEZE` | The unchanged 22/22 scientific conditions pass under safety amendment v2; current manifest SHA-256 `70d29cd1c2fa74b73e875daafa7d973508c181f5f7a1da43c7eef6561a68bf0c`. |
| A16P | Confirmatory payload and paid-run approval | `COMPLETE / REPAIRED SEAL REAUTHORISED` | The repaired seal and packet passed full/narrow independent review and exact fresh user authorisation. |
| A17 | Confirmatory run | `COMPLETE / PASS / USER-REVIEWED` | Four primary runs contain 13,200 aligned rows; three warm runs reproduce all neural rows exactly from cache; the user approved thesis integration on 2026-08-02. |
| A18 | Statistical analysis | `CONFIRMATORY COMPLETE / PASS` | All nine preregistered contrasts use 10,000 cluster bootstraps, 10,000 paired sign-flips, and full-family Holm correction. |
| A19 | Cost and latency ledger | `CONFIRMATORY COMPLETE / PASS` | The final ledger separates construction, online, primary, verification, provider, cache, model-compute, storage, and representation-size costs. |
| A20 | Thesis update | `COMPLETE / USER-REVIEWED` | User instructed thesis integration on 2026-08-02; methodology, results, discussion, conclusion, and PDF were updated without changing scientific evidence. |

## 14. Stage Report Template

At the end of every stage, report:

1. what was implemented or run;
2. which requirement and artifact prove completion;
3. which metrics/checks were used and why;
4. the measured result;
5. failures, caveats, and whether the gate passed;
6. the next step.

The same report is appended below before moving to the next stage.

## 15. Run Log

### Stage 0: protocol and acceptance freeze

- **State:** `PASS / COMPLETE`
- **What was done:** froze RQ2a-only scope, source suites, deterministic 20/80 cluster split, proposition mapping, byte-level serialiser rules, padding blocks, selector settings, core/diagnostic matrix, metrics, inference policy, practical-effect threshold, output contracts, and no-thesis-write boundary.
- **Source audit before implementation:** 350 core `unit.json` files, 750 core prompt rows, and three sibling candidates per cluster are expected.
- **Why these metrics:** tie-adjusted Top-1 measures the one-skill decision without Option-A tie bias; MRR and margin measure ranking quality/confidence; cluster bootstrap respects dependence between prompt variants; length, latency, API, and cache metrics measure cost rather than only accuracy.
- **Result:** Gate 0 is satisfied. No representation, selector output, or experimental score existed at freeze time.
- **Next:** implement the deterministic split, canonical source loader, and all matched-content representations.

### Stage 1: source, split, and representation build

- **State:** `PASS FOR BUILD / VALIDATION PENDING`
- **What was done:** implemented `skill_benchmark/scripts/build_rq2a_matched_representations.py`; generated the frozen 70/280 split, 750 prompt rows, eight representation files, protocol and representation manifests, hashes, length summaries, and one development plus one confirmatory review sample per field.
- **Coverage result:** 350 clusters, 750 prompts, 1,050 candidates per representation, and eight representations.
- **Split result:** 70 development clusters/150 prompts and 280 confirmatory clusters/600 prompts.
- **Order-control result:** each of the seven field rotations occurs exactly 50 times.
- **Length metrics:** median audit tokens are 6 for `shared-only`, 187 for fielded, 173 for flat, 216 for prose, 199/209/227 for diluted 1x/2x/4x, and 187 for order-controlled.
- **Why length is measured:** representation effects can otherwise be confused with context size or pooling dilution. Fielded versus flat differs by about 8.1% at the median and stays below the 10% sensitivity trigger. Prose is about 15.5% longer than fielded and therefore triggers the preregistered length-matched sensitivity requirement before confirmatory scoring.
- **Artifacts:** `skill_benchmark/rq2a_matched_content/protocol.json`, `split.json`, `split.md`, `prompts.jsonl`, `manifest.json`, `representation_samples.md`, and `representations/*.jsonl`.
- **Caveat:** build success proves deterministic output counts, not proposition equivalence or leakage safety. Those are Gate 3 checks in the next stage.
- **Next:** implement and run the independent representation validator; review failures; add the required prose-length sensitivity before any selector scoring.

### Stage 2: representation validation and approval

- **State:** `PASS / COMPLETE`
- **Machine validation:** final serializer v1.4 passes with 0 errors and 0 warnings across 8,400 candidate-representation rows and 750 prompts.
- **Checks:** row counts, unique identities, source hashes, proposition equality, text hashes, split alignment, gold/candidate alignment, selector-metadata leakage, shared-only sibling identity, flat label removal, prose proposition retention and punctuation, order rotation, fielded-prefix dilution, sibling-identical padding, and padding leakage.
- **Human review:** one development and one confirmatory cluster per field, 14 clusters total, all pass. Review artifact: `skill_benchmark/rq2a_matched_content/manual_sample_review.md`.
- **Corrections before scoring:** false-positive phrase matching in the validator was fixed without changing data; a trial length-control suffix was rejected for two leakage terms and archived; human review removed duplicate prose punctuation; final fielded-versus-prose length difference fell below the frozen trigger.
- **Final length result:** median audit tokens are 6 shared-only, 187 fielded, 173 flat, 205 prose, 187 order-controlled, and 199/209/227 for diluted 1x/2x/4x. Fielded-flat differs by 7.5%; fielded-prose differs by 9.6%; neither exceeds 10%.
- **Why these checks matter:** proposition equality protects the causal treatment; leakage checks prevent selectors from reading benchmark metadata; order and padding checks ensure diagnostics change only the intended variable; length checks identify context-size confounds before scores exist.
- **Artifacts:** `validation_report.json`, `validation_report.md`, `manual_sample_review.md`, `manifest.json`, and archived intermediate serializer outputs.
- **Decision:** representation gate passes. Serializer v1.4 is approved for development selector runs.
- **Next:** implement the common result schema plus BM25, Qwen single-vector, SkillRouter cross-encoder, and Qwen field-aware adapters; smoke-test on development clusters only.

### Stage 3: selector adapters and smoke tests

- **State:** `PARTIAL PASS / REAL NEURAL SMOKES BLOCKED BY EXTERNAL-DATA AUTHORISATION`
- **What was implemented:** added `rq2a_selector_common.py`, `run_rq2a_fixed_candidate_matrix.py`, `run_rq2a_field_aware_selector.py`, and `test_rq2a_selector_adapters.py`. The fixed runner supports BM25, Qwen single-vector, and direct SkillRouter cross-encoder scoring under one row schema. The field-aware runner separately scores the exact seven labelled field blocks with maximum and uniform-top-two aggregation.
- **Shared result contract:** every result records protocol/serialiser/run IDs, split, selector configuration hash, representation, prompt/cluster/field/variant, query hash, aligned candidate and text hashes, all three scores, tie-adjusted Top-1/MRR, deterministic sensitivity, rank interval, gold margin, strict confusion, top-tie metrics, selector-visible lengths, and score latency.
- **Offline tests:** common metric self-tests pass; a synthetic OpenAI-compatible provider verifies batching, actual provider-usage aggregation, persistent exact-text cache reuse, vector dimensions, and the 8,192-audit-token hard guard; a model-free cross-encoder preflight verifies that overlength pairs fail rather than truncate; all eight real artifacts align for one development cluster per field and every field-aware component is an exact substring of the fielded text.
- **Real BM25 smoke:** 7 development clusters, 15 prompts, two representations, and 30 unique rows pass parsing and identity checks. `shared-only` returns the expected three-way tie (cluster-weighted tie-adjusted Top-1 `0.333`, tie rate `1.000`); fielded returns `1.000` Top-1 and zero strict confusions in this deliberately small smoke. These values validate direction and tie handling; they are not scientific results.
- **Detected and fixed implementation failure:** the first BM25 smoke generated valid row scores but failed while grouping prompt variants in the summary. The grouping implementation was corrected and the same smoke reran successfully. The failed attempt is not treated as evidence.
- **External-data boundary:** the real Qwen smoke attempted no successful external transfer. Sandbox review blocked sending unpublished benchmark prompts and representation text to DashScope without explicit user approval for that destination and payload. No workaround was attempted.
- **Cross-encoder boundary at this checkpoint:** only the released model configuration was present and the active Python environment lacked a complete runtime. This was subsequently resolved locally without uploading benchmark text; see the Stage 3 continuation below.
- **Artifacts:** `skill_benchmark/outputs/rq2a_matched_content/development/smoke-bm25-v1/` plus the four scripts listed above.
- **Why these checks matter:** the shared schema makes later selector comparisons paired and auditable; tie tests remove Option-A bias; exact component checks prevent field-aware leakage; cache/usage tests support cost accounting; hard length failure protects the no-truncation causal condition.
- **Decision at this checkpoint:** A9 and A10 passed; A11-A13 remained open. A12 was subsequently completed in the Stage 3 continuation below. Full development calibration still must not begin until A11 and A13 pass.
- **Next:** obtain explicit authorisation to send the reviewed RQ2a query and candidate text to DashScope and, separately, choose/authorise the SkillRouter model execution destination; then run the neural smokes and complete Stage 3.

#### Stage 3 continuation: local SkillRouter gate

- **State:** `A12 PASS / COMPLETE`
- **Runtime preparation:** created the ignored workspace-local `.venv-rq2a`, reused the existing public Torch/Transformers installation with its required public dependencies, and downloaded only the pinned public SkillRouter model snapshot. No benchmark text was uploaded.
- **Offline loading correction:** the first `local_files_only` attempt revealed that Transformers still queried Hugging Face metadata when given a remote model ID. The adapter now resolves the pinned cache snapshot to an absolute local path before tokenizer/model loading; the rerun made no network request.
- **Shared-only control:** 15 prompts across seven development clusters reduced to 15 unique query-document pairs because sibling text is byte-identical. All decisions produced the required three-way tie: tie-adjusted Top-1 `0.333`, MRR `0.611`, top-tie rate `1.000`.
- **Fielded smoke:** 45 unique query-document pairs across the same 15 prompts scored successfully. Maximum model length was 333 tokens, minimum 246, and truncated pairs were zero. Tie-adjusted Top-1 and MRR were both `1.000`, mean gold margin was `3.826`, strict confusion was zero, and top-tie rate was zero. This remains implementation evidence, not a development or confirmatory claim.
- **Cold/warm cost:** the cold fielded forward passes consumed 17.875 model seconds and 20.519 total wall seconds. An exact rerun hit 45/45 persistent score-cache entries, executed zero forward passes, spent 0.003 seconds in pair preparation/lookup, and 2.742 seconds total including model startup.
- **Complete no-truncation audit:** `audit_rq2a_selector_lengths.py` constructed all 18,000 SkillRouter query-document inputs across 750 prompts, eight representations, and three candidates. Model-token median/P95/maximum were 297/346/389 against the frozen 2,048 limit; violations and truncations were zero. Qwen fixed-audit maxima were 55 for queries, 262 for complete representations, and 63 for field components against the 8,192 guard; all violation counts were zero.
- **Existing Qwen cache audit:** the legacy provider cache contains exact request-key hits for all 750 reviewed queries, but zero hits for the 7,398 new unique representation texts and zero for the 1,063 unique field components. The new client may import only SHA-256 exact request matches after verifying 1,024 returned dimensions and recording source provenance. All 750 query vectors were migrated locally with zero API calls; no candidate text was transferred.
- **Artifacts:** `smoke-skillrouter-shared-v1`, `smoke-skillrouter-fielded-v1`, and `smoke-skillrouter-fielded-warm-v1` under the development output directory; `selector_length_audit.json` and `selector_length_audit.md` under `skill_benchmark/rq2a_matched_content/`.
- **Decision update:** A9, A10, and A12 pass. A11 and A13 still require real Qwen scoring; Stage 3 as a whole remains open.
- **Next:** after explicit DashScope transfer authorisation, run Qwen single-vector and field-aware smokes on the identical 15 prompts, then start the complete development matrix.

#### Stage 3 continuation: analysis and confirmatory safety infrastructure

- **State:** `IMPLEMENTATION PASS / NO NEW EXPERIMENT STARTED`
- **Inference freeze:** added `analysis_spec.json` before confirmatory scoring. It fixes one primary Top-1 contrast, eight secondary Top-1 contrasts, cluster aggregation, 10,000 percentile-bootstrap resamples, 10,000 paired cluster sign-flips, full-family Holm correction, the 3pp practical threshold, and which measures are descriptive only.
- **Analysis implementation:** `analyze_rq2a_matched_content.py` validates run/row hashes and unique condition-prompt identities, pairs the same prompt across conditions, averages prompt differences within cluster, bootstraps clusters, computes paired sign-flip p-values, applies Holm across all eight secondary slots, and preserves runtime provenance. It blocks confirmatory input unless an explicit frozen manifest is supplied.
- **Smoke analysis test:** 60 rows from the BM25 and local SkillRouter shared/fielded smokes passed. The two available positive-control differences were both `+0.667` with degenerate smoke CIs `[+0.667,+0.667]`; raw sign-flip p-values were approximately `0.015-0.017`, but full-family Holm values were `0.122`, so the seven-cluster smoke is correctly not treated as formal significant evidence.
- **Confirmatory gate:** added `freeze_rq2a_confirmatory_protocol.py`. Its dry audit ignores all runs with `clusters_per_field` set, confirms the representation and length gates, and currently refuses to freeze because the full development matrix, frozen field-aware choice, and complete development analysis do not yet exist. The confirmatory output directory remains empty.
- **Why this matters:** cluster pairing respects dependence among prompt variants; tie-adjusted Top-1 remains the deployment decision metric; the sign-flip test supplies a paired null distribution; Holm prevents selective claims across planned secondary contrasts; the freeze gate prevents confirmatory leakage or post-hoc tuning.
- **Artifacts:** `analysis_spec.json`; `smoke-analysis-v1/analysis.json` and `.md`; `analyze_rq2a_matched_content.py`; `freeze_rq2a_confirmatory_protocol.py`.
- **Next:** unchanged: obtain explicit DashScope candidate-text transfer authorisation, finish A11/A13 smokes, then execute complete development scoring and freeze the field-aware rule.

#### Stage 3 final offline audit and authorisation boundary

- **State:** `OFFLINE GATES PASS / EXTERNAL QWEN GATE BLOCKED`
- **Code verification:** all nine RQ2a build, validation, selector, length-audit, analysis, and freeze scripts compile successfully with `py_compile`.
- **Adapter verification:** `test_rq2a_selector_adapters.py` passes again, including synthetic provider batching/usage accounting, exact cache reuse, no-truncation enforcement, and alignment against the real frozen representation artifacts.
- **Freeze verification:** the confirmatory dry audit remains `not_ready_to_freeze`. It correctly reports `0/21` complete full-development conditions, a missing frozen field-aware aggregation choice, and a missing complete development analysis. It ignores the four smoke runs and confirms that the confirmatory output directory contains no files.
- **Thesis boundary:** no RQ2a result from this stage is written to the thesis. The thesis worktree already contains earlier unrelated edits and remains outside this execution stage.
- **Blocking condition:** the remaining A11/A13 smoke payload contains unpublished RQ2a candidate representations and field-component text. Sending that payload to DashScope `text-embedding-v4` requires explicit user authorisation naming the destination and purpose. Existing exact query embeddings may be reused locally, but no candidate-document or field-component vector exists in the cache.
- **Why work stops here:** the frozen sequence prohibits starting the full development matrix until the real Qwen single-vector and field-aware smoke gates pass. Running BM25 or SkillRouter development early would violate the preregistered stage order and leave a partially observed development matrix.
- **Required authorisation to resume:** explicit permission to send the RQ2a candidate-representation and field-component text to DashScope `text-embedding-v4` for smoke, development, and, only after development freeze, confirmatory evaluation.
- **Next after authorisation:** run the 15-prompt Qwen single-vector and field-aware smokes, validate their persisted rows/manifests, mark A11/A13 complete, and begin the full development matrix.

#### 2026-08-01 status synchronisation and real-smoke authorisation check

- **Documentation synchronisation:** the canonical RQ2 tracker, high-level thesis trackers, methodology tracker, roadmap, active snapshot, results summary, risk register, information-layer framework, and thesis status/methodology passages now agree that RQ2a Stages 0--2 are complete and Stage 3 is partial.
- **Historical/current separation:** pre-2026-07-26 I1/I2/I3, M6, external SkillRouter, graph/tree, and downstream material remains available but is explicitly labelled historical, exploratory, diagnostic, portability, or future evidence. It is not counted as matched-content RQ2a confirmatory evidence.
- **Thesis claim boundary at this historical checkpoint:** the thesis then recorded implemented representations, QA, selector adapters, and technical smoke state while stating that no full development or confirmatory RQ2a result yet existed. No Qwen smoke score or unreviewed scientific claim was inserted at that stage. The later Stage 7 entry records the completed thesis integration.
- **Thesis verification:** `pdflatex` completes twice without error and produces a 79-page PDF. Visual inspection of the updated methodology status page and RQ2a result-status table shows no clipping, overlap, or unreadable rows; existing non-fatal box/float warnings remain unrelated to this status patch.
- **Attempted next action:** requested a controlled run of `smoke-qwen-v1` on one development cluster per field, using 15 prompts, cached query vectors, and only `shared-only` plus `same-facts-fielded` candidate texts.
- **Result:** external execution was rejected before process launch because the user instruction to finish Stage 3 did not explicitly name and approve sending the unpublished candidate/field-component payload to DashScope. No API request was made and no new embedding or result file was created. The path `smoke-qwen-v1` already existed as an empty directory from the 2026-07-27 DNS-failed attempt; it remains empty and is not counted as a run.
- **Gate state:** A11 and A13 remain `IMPLEMENTED / REAL API SMOKE BLOCKED`; Stage 3 remains open. The full development matrix must not start.
- **Required next step:** obtain explicit approval for sending the RQ2a candidate-representation and field-component text to DashScope `text-embedding-v4`, then run and validate the two real smokes only.

#### Stage 3 completion: Qwen single-vector and semantic field-aware real smokes

- **State:** `PASS / STAGE 3 COMPLETE`
- **Authorised scope:** the user explicitly authorised sending only the Stage 3 smoke candidate-representation and seven field-component texts to DashScope `text-embedding-v4`, with local embedding persistence. No full development or confirmatory scoring was authorised or run.
- **Qwen single-vector cold smoke:** `smoke-qwen-v1` scored `shared-only` and `same-facts-fielded` for 15 prompts from seven development clusters, producing 30/30 unique aligned rows. All 15 query embeddings were exact cache hits. The 28 unique candidate documents required three API calls, 4,175 provider-reported prompt tokens, and 3.392 API seconds; total wall time was 3.514 seconds.
- **Qwen positive/negative controls:** `shared-only` produced the required three-way tie with cluster-weighted tie-adjusted Top-1 `0.333`, MRR `0.611`, and tie rate `1.000`. `same-facts-fielded` produced cluster-weighted Top-1 `0.786`, prompt-weighted Top-1 `0.800`, MRR `0.889`, mean gold margin `0.0334`, strict near-neighbour confusion `0.200`, and no top ties. These are smoke diagnostics, not confirmatory estimates.
- **Qwen warm-cache proof:** `smoke-qwen-warm-v1` reused 43/43 exact embeddings, made zero API calls, and completed in 0.072 seconds. After removing run ID and latency, its canonical row-level scientific-output hash exactly matched the cold run.
- **Field-aware cold smoke:** `smoke-field-aware-v1` scored both preregistered aggregations over the same 15 prompts and seven clusters, producing 30/30 unique aligned rows. All 15 query embeddings were cache hits. The 55 unique exact labelled field blocks required six API calls, 1,504 provider-reported prompt tokens, and 5.815 API seconds; total wall time was 5.946 seconds.
- **Field-aware smoke comparison:** maximum field similarity reached cluster-weighted Top-1 `0.810` and MRR `0.889`; uniform top-two reached `0.929` and `0.958`. The generated choice is marked `provisional_smoke_choice_not_frozen`. It is not a development decision and must not be carried into confirmatory scoring without the complete 70-cluster development comparison.
- **Field-aware warm-cache proof:** `smoke-field-aware-warm-v1` reused 70/70 exact embeddings, made zero API calls, and completed in 0.086 seconds. Its canonical scientific-output hash exactly matched the cold run after removing run ID and latency.
- **Independent QA:** both cold manifests report `state=complete`, exact expected/actual row counts, unique result identities, finite scores, candidate alignment, and no thesis write. Field-aware QA additionally passes seven-component count, exact fielded blocks, absent field-specific weights, and absent first-stage scores. Independent JSONL checks confirm three candidate IDs and scores per row, gold inclusion, development-only split, protocol/serialiser alignment, and provisional aggregation state. Both 30-row runs pass the independent analysis validator. The selector adapter test suite also passes again.
- **Why these metrics:** the shared-only tie tests unbiased tie handling; fielded lift tests that reviewed facts remain usable; MRR and margin reveal ordering strength even when Top-1 is wrong; strict confusion distinguishes decisive near-neighbour errors; provider tokens/API calls and cold/warm latency establish reusable-cost accounting; row/hash/cache checks prove reproducibility rather than only accuracy.
- **Freeze safety:** a post-smoke dry audit skips all eight smoke run directories, reports `0/21` complete full-development conditions, finds no frozen aggregation or development analysis, and confirms an empty confirmatory directory. It correctly remains `not_ready_to_freeze`.
- **Decision:** A9--A13 satisfy their required Stage 3 artifact and smoke gates; A14 remains optional/deferred. Stage 3 is complete. No claim about which representation or field-aware aggregation is better is scientifically supported by this seven-cluster smoke.
- **Next boundary:** stop before Stage 4. Full development must begin only after the user reviews this Stage 3 report and explicitly authorises the development matrix.

### Stage 4 checkpoint: local development conditions

- **State:** `IN PROGRESS / LOCAL CONDITIONS PASS / 13 OF 21`.
- **Authorisation interpretation:** the user resumed the existing RQ2a goal after reviewing Stage 3. This permits local Stage 4 work. The earlier transfer authorisation explicitly covered only the Qwen smokes, so this checkpoint does not send the complete development payload to DashScope and does not touch confirmatory data.
- **BM25 run:** `development-bm25-all-v1` scored all eight representations over 70 development clusters and 150 prompts, producing 1,200/1,200 unique aligned rows. `shared-only` gives the required three-way-tie control at cluster Top-1 `0.3333` and MRR `0.6111`. The seven operational-content variants range from `0.8607` to `0.8702` cluster Top-1. These are development diagnostics, not confirmatory estimates.
- **SkillRouter cold run:** `development-skillrouter-core-v1` scored the five core representations, producing 750/750 unique aligned rows. It used 60 cached and 1,890 newly computed unique query-document scores, 860.6 model seconds, and zero truncations; observed model lengths were 92--358 tokens against the 2,048 limit. `shared-only` is `0.3333`; fielded, flat, prose, and diluted-2x each reach cluster Top-1 `0.9381`, while their margins differ.
- **SkillRouter warm verification:** `development-skillrouter-core-warm-v1` reused 1,950/1,950 unique score entries, made zero forward passes, and completed in 4.69 wall seconds including model startup. Its 750 scientific rows exactly equal the cold rows after removing run ID and per-row latency.
- **Gate defect and correction:** the first post-warm freeze audit treated the cold and warm manifests as duplicate primary evidence and therefore rejected every condition. Both selector runners now write an explicit `evidence_role` (`primary` or `verification`); the freeze scanner defaults older manifests to `primary` and skips explicit verification runs. The warm manifest is marked `verification`. Compilation, adapter tests, and a repeat dry audit pass; the audit now reports exactly 13/21 complete conditions and no incomplete conditions.
- **Qwen cache/payload audit:** the eight single-vector representations contain 1,502 unique development documents, of which 28 are cached and 1,474 are missing; the missing documents total 276,074 fixed audit tokens and imply about 148 batches of 10. All 150 query vectors are cached. Field-aware development has 298 unique exact labelled field components, of which 55 are cached and 243 are missing; the misses total 4,187 fixed audit tokens and imply about 25 batches of 10.
- **Why these checks matter:** row and identity counts prove complete paired coverage; the shared-only control checks unbiased tie handling; no-truncation checks protect the representation comparison; cold/warm equality proves persistence; explicit evidence roles prevent reproducibility runs from contaminating freeze counts; the local payload audit makes the remaining external transfer and cost boundary auditable before execution.
- **Current freeze state:** `not_ready_to_freeze`, 13/21 core conditions, no frozen field-aware aggregation, no complete development analysis, and an empty confirmatory output directory.
- **Next authorisation boundary:** full development now requires explicit permission to send the 1,474 missing candidate-document texts and 243 missing field-component texts to DashScope `text-embedding-v4`, solely for Qwen single-vector and field-aware development scoring with local persistence. This does not authorise confirmatory scoring.

#### Stage 4 continuation: multi-run analysis and cost infrastructure

- **State:** `IMPLEMENTATION PASS / PARTIAL DEVELOPMENT EVIDENCE ONLY`.
- **Multi-run analysis:** the existing analyser already accepts repeated `--run-dir` arguments. `development-local-partial-v1` combines the two canonical local primary runs into 1,950 unique rows and makes four preregistered secondary contrasts available. It is not the complete development analysis.
- **Primary-evidence guard:** the analyser now rejects manifests whose explicit `evidence_role` is not `primary`. A negative test against `development-skillrouter-core-warm-v1` fails as required rather than double-counting warm rows.
- **Freeze-analysis guard:** A16 now requires the supplied analysis to contain every expected selector/representation condition and to cite exactly the same primary run IDs, manifest hashes, and row hashes discovered by the freeze scanner. Supplying the partial local report correctly leaves the eight Qwen conditions missing. This closes the earlier loophole where a 70-cluster partial report could satisfy the shallow cluster-count check.
- **Cost ledger implementation:** added `build_rq2a_cost_ledger.py`. It validates run hashes, separates `primary`, `smoke`, and `verification` evidence, records representation size, fixed document/component construction time, observed online selector time, provider calls/tokens, embedding and cross-encoder cache behaviour, model pairs/time, cache storage, and total wall time.
- **Partial cost artifact:** `development-partial-cost-v2` scans 11 current development-root runs: two primary, eight smoke, and one verification. Current primary evidence contains 1,950 result rows, 1,890 newly scored SkillRouter pairs, 60 cold cache hits, 860.6 model seconds, and no provider calls because Qwen full development has not begun. The Qwen embedding cache currently has 833 files/22,924,730 bytes; the SkillRouter score cache has 1,950 files/1,146,406 bytes.
- **Latency interpretation:** observed BM25 online compute is approximately 0.00113 seconds per prompt over eight representations. SkillRouter cold pair preparation, inference, and lookup are approximately 5.751 seconds per prompt over five representations on local CPU; exact warm-cache reuse is approximately 0.00167 seconds per prompt, excluding model startup from the online path but retaining it in total wall time.
- **Currency discipline:** provider tokens and calls are measured directly. Monetary conversion remains null unless a dated price source and per-million-token rate are supplied, preventing a mutable external price from being silently hard-coded into the experiment.
- **Reproducible external-payload preflight:** added `audit_rq2a_qwen_cache.py` and generated `development-qwen-cache-preflight-v1`. It performs zero network requests, validates every existing vector dimension and exact-text cache key, verifies field components remain exact fielded-text substrings, and stores only SHA-256 values for missing texts. It reproduces 1,474 missing documents, zero missing queries, 243 missing components, and 1,717 missing texts across the de-duplicated union.
- **Verification:** all modified/new scripts compile; `test_rq2a_stage_gates.py` passes its isolated primary/verification regression cases; the existing selector adapter suite passes; the 1,950-row partial analysis passes; the warm-evidence rejection test passes by failing with the expected role error; the strengthened freeze audit remains `not_ready_to_freeze` at 13/21; the cost ledger JSON and Markdown parse cleanly. No confirmatory result was read and no thesis PDF was changed.
- **Initial local development interpretation:** the operational-content positive controls are strong: BM25 fielded-minus-shared is `+0.5321` cluster Top-1 (95% development bootstrap interval `[+0.4810,+0.5786]`), and SkillRouter fielded-minus-shared is `+0.6048` (`[+0.5548,+0.6452]`). In contrast, BM25 fielded-minus-flat is only `+0.0048` (`[0,+0.0143]`, no practical support), while SkillRouter fielded-minus-flat is exactly `0.0000` Top-1 difference. BM25 diluted-1x/2x/4x share the same `0.8702` cluster Top-1, so the current lexical development slice does not show a dilution decline. SkillRouter fielded, flat, prose, and diluted-2x all share `0.9381` Top-1, although within-selector margins differ. These results currently support content visibility, not a field-label or organisation advantage. They are development-only and cannot answer the primary Qwen contrast.
- **Next:** unchanged external boundary: obtain explicit full-development DashScope authorisation, execute Qwen 8/8 and both field-aware aggregations, freeze one aggregation by the preregistered rule, then regenerate the complete development analysis and cost ledger.

After explicit development-only transfer authorisation, execute in this order:

1. `development-qwen-all-v1`: Qwen single-vector over all eight representations, role `primary`;
2. `development-qwen-all-warm-v1`: identical Qwen run, role `verification`, expecting zero API calls and identical scientific rows;
3. `development-field-aware-v1`: both aggregations over all 70 development clusters with `--freeze-aggregation-choice`, role `primary`;
4. `development-field-aware-warm-v1`: identical field-aware cache verification without rewriting the frozen choice, role `verification`;
5. combine the four primary runs into the complete analysis, regenerate the cost ledger, and run the A16 dry audit;
6. stop again before confirmatory and request a separate confirmatory authorisation.

#### Stage 4 continuation: confirmatory and aggregation provenance hardening

- **State:** `IMPLEMENTATION PASS / DEVELOPMENT EVIDENCE UNCHANGED`.
- **Problem found before paid scoring:** confirmatory runners previously required a freeze-manifest path but did not prove that the supplied JSON was genuinely frozen or that its recorded files remained unchanged. The freeze audit also checked the selected aggregation's state and sample size, but did not prove that the supplied choice file was the exact artifact produced by the canonical primary 70-cluster field-aware run.
- **Confirmatory integrity fix:** the shared validator now checks freeze schema, state, protocol and serialiser versions; every recorded input and implementation hash; every representation hash; the frozen development-analysis hash; the aggregation-choice path/hash/selector; and the fixed confirmatory output root. Both scoring runners call this validator before loading prompts or models. Future confirmatory run manifests persist the freeze-manifest hash, and confirmatory analysis rejects rows that do not reference that same frozen manifest.
- **Aggregation provenance fix:** a development aggregation can freeze only when maximum and uniform-top-two have identical prompt identities. Seven-field aggregation now rejects any score vector that is not exactly seven components. A16 requires exactly one canonical primary field-aware development run, the exact choice artifact and manifest-embedded choice to agree, both selectors to cover 150 prompts and 70 clusters, and every row's selected flag/state to agree with the frozen rule.
- **Why this matters:** the primary and field-aware contrasts would otherwise be vulnerable to a copied smoke choice, a hand-edited choice file, code drift after freeze, or results generated against a different representation snapshot. The new checks turn the freeze from a filename convention into an executable provenance boundary.
- **Verification:** compilation and `git diff --check` pass. Adapter tests now cover seven-component enforcement, identical-prompt aggregation comparison, Top-1 precedence, MRR tie-breaking, and the final uniform-top-two tie rule. Stage-gate tests include a valid synthetic freeze, deliberate post-freeze implementation mutation, canonical aggregation provenance, and a copied-choice rejection. The real dry audit still reports `not_ready_to_freeze`, 13/21 complete core conditions, precisely eight missing Qwen conditions, no incomplete conditions, all smoke/warm runs excluded, and zero confirmatory files.
- **Scientific result:** unchanged. This is a protocol-integrity improvement, not another development observation, and it does not modify the existing partial metrics.
- **External boundary:** unchanged. No DashScope request was made and the thesis PDF was not edited.

### Stage 4 completion: full development scoring, analysis, cost, and freeze

- **State:** `PASS / DEVELOPMENT COMPLETE / CONFIRMATORY FROZEN BUT NOT RUN`.
- **Authorised scope:** the user explicitly authorised sending the 1,474 missing development candidate-representation texts and 243 missing seven-field component texts to DashScope `text-embedding-v4`, only for Qwen single-vector and field-aware development scoring with local persistence. This authorisation excluded confirmatory scoring, and no confirmatory query, candidate, embedding, or result was read or produced.
- **Qwen single-vector primary run:** `development-qwen-all-v1` produced 1,200/1,200 unique aligned rows over all eight representations, 70 clusters, and 150 prompts. It reused 28 document and all 150 query embeddings, created 1,474 missing document embeddings in 148 API calls, recorded 290,159 provider-reported tokens, spent 154.405 seconds in provider calls, and completed in 156.456 wall seconds.
- **Qwen warm verification:** `development-qwen-all-warm-v1` reused all 1,652 required embeddings, made zero API calls, completed in 1.149 seconds, and reproduced the cold scientific rows exactly after removing run ID and latency.
- **Field-aware primary run:** `development-field-aware-v1` produced 300/300 aligned rows for maximum and uniform-top-two aggregation. It reused 55 component and all 150 query embeddings, created 243 missing components in 25 API calls, recorded 4,814 provider tokens, spent 24.792 seconds in provider calls, and completed in 25.446 wall seconds. Exact seven-field, no-first-stage, no-weight, identity, and choice-provenance checks pass.
- **Frozen aggregation:** uniform-top-two won the preregistered development selection rule with cluster-weighted tie-adjusted Top-1 `0.8730` and prompt-weighted MRR `0.9298`, versus maximum at `0.7333` and `0.8509`. The canonical choice artifact is `development-field-aware-v1/aggregation_choice.json`, SHA-256 `52d94aa3d70a19021152a88324a4fe3c50b7b35307ec00b7f24eb6a99b9684f4`.
- **Field-aware warm verification:** `development-field-aware-warm-v1` reused all 448 required embeddings, made zero API calls, completed in 0.492 seconds, and reproduced both scientific rows and the aggregation decision exactly after removing run ID and latency.
- **Complete development analysis:** `development-complete-v1` combines the four canonical primary runs into 3,450 unique condition-prompt rows and makes all nine preregistered contrasts available. Run hashes, paired identities, primary-evidence roles, and unique condition-prompt rows all pass.
- **Primary development contrast:** Qwen fielded minus flat is `-5.48pp` cluster-weighted tie-adjusted Top-1, 95% cluster-bootstrap interval `[-12.62pp,+1.19pp]`, paired sign-flip `p=0.144`. The expected direction is not met and there is no practical support. Fielded Top-1 is `0.8310`; flat is `0.8857`.
- **Organisation and explicit-use diagnostics:** BM25 fielded minus flat is `+0.48pp` with no practical support; SkillRouter is exactly `0.00pp`; Qwen fielded minus prose is `-4.05pp`; Qwen fielded minus diluted-2x is `-2.62pp`. Frozen field-aware uniform-top-two minus Qwen single-vector fielded is `+4.21pp`, but its interval `[-3.25pp,+11.90pp]` includes zero and Holm-adjusted `p=0.946`, so it is not supported as a development claim.
- **Positive controls:** operational field content strongly beats shared-only under Qwen (`+49.76pp`, 95% interval `[+42.14pp,+56.67pp]`), BM25 (`+53.21pp`), and SkillRouter (`+60.48pp`); all three secondary positive controls survive the frozen Holm family. This validates that the reviewed facts remain usable while suggesting that content availability matters more than literal field headings in this development split.
- **Cost ledger:** `development-complete-cost-v1` records four primary runs, 3,450 rows, 173 provider calls, 294,973 provider tokens, 1,717 new and 383 reused embeddings, 1,890 newly scored SkillRouter pairs, 860.614 model seconds, and 1,053.335 aggregate primary wall seconds. Verification runs make zero provider calls and zero new model forward passes. Currency remains intentionally unset without a dated price snapshot.
- **Freeze result:** the A16 dry audit reports `ready_to_freeze`, 22/22 expected frozen conditions, zero missing/incomplete conditions, all smoke and verification runs excluded, and an empty confirmatory output directory. After the authorised safety-only hardening amendment, the immutable manifest is `skill_benchmark/rq2a_matched_content/confirmatory_freeze_manifest.json`, SHA-256 `f31fec56a424853b4ffe3c846bd2f3f131bf5ad34ffcd9fba71105a2473d25af`.
- **Completion audit:** `thesis_notes/checkpoints/RQ2a Stage 4 Development Completion Audit - 2026-08-01.md` maps every requirement in the active implementation/development goal to current artifacts and distinguishes goal completion from the still-unrun confirmatory study.
- **Interpretation boundary:** these are development observations used to select and freeze the protocol. They are not confirmatory estimates and must not be written into the thesis results chapter before user review. A null or negative organisation result remains scientifically valid if the confirmatory quality gates pass.
- **Next:** stop at the authorisation boundary. A17 may begin only after separate explicit permission for the confirmatory DashScope payload and run.

### Stage 5A specification and checkpoint: confirmatory payload and paid-run approval

- **Current state:** `OFFLINE GATES PASS / USER AUTHORISATION PENDING`.
- **Purpose:** make the external-data and spending decision auditable without inspecting confirmatory scores or sending any text before approval.
- **Frozen scientific boundary:** the immutable A16 manifest, 22 selector/representation conditions, `uniform-top-two` field aggregation, model IDs, serialisers, prompts, tie rules, and analysis rules must remain byte-identical. Any hash mismatch stops the stage and requires a new explicit freeze review.
- **Offline preflight:** run `audit_rq2a_qwen_cache.py --split confirmatory` only. It may read frozen artifacts locally to validate exact cache keys and emit hashes/counts; it must make zero network requests and must not output raw missing text. The accepted v2 audit additionally freezes every accepted current-cache file hash and distinguishes legacy entries.
- **Approval packet:** record the freeze hash, payload-audit hash, destination `DashScope text-embedding-v4`, exact uncached query/document/component counts, fixed audit-token totals, batch-size/call ceilings, purpose, local persistence location, commands, stop conditions, and exclusions.
- **Independent review:** a read-only subagent may inspect only the protocol, freeze, audit artifacts, command plan, and approval packet. A separate PASS record must bind the immutable packet, execution seal, and approval-scope digest. The reviewer cannot grant user consent, authorise data transfer, or authorise spending.
- **Required user approval:** one explicit message must name DashScope `text-embedding-v4`, the confirmatory split, the exact or hash-bound payload, the permitted Qwen single-vector and field-aware purposes, local persistence, and a call/token or monetary ceiling. It must state whether local BM25/SkillRouter runs and warm verification may proceed in the same closed confirmatory sequence. General instructions to continue do not substitute for this payload-specific consent.
- **Closed-sequence rule after approval:** run frozen BM25, SkillRouter, Qwen single-vector, and selected field-aware conditions without changing code or interpreting partial scores. Warm-cache verification follows. Formal interpretation begins only after all primary manifests and hashes pass.
- **Stop conditions:** provider/model mismatch; freeze/hash drift; unexpected text/call/token count above the approved ceiling; an unauthorised pre-existing confirmatory result; truncation; malformed or non-finite rows; cache schema, metadata, dimension, text, vector, file-hash, or guarded-attempt provenance mismatch; incomplete resumed-result identity validation; paid-usage ledger mismatch; failed independent review; or user-authorisation mismatch.
- **Acceptance gate:** Stage 5A passes only when the offline audit and independent review pass, the exact authorisation packet is recorded, and the user supplies matching explicit approval. Until then A17 remains `NOT STARTED / NOT AUTHORISED`.

#### Stage 5A offline checkpoint, 2026-08-01

- **Frozen study:** 280 confirmatory clusters, 600 prompts, three candidates, 22 primary conditions, and 13,200 expected primary rows. The field-aware rule remains `qwen-field-aware-uniform-top-two`.
- **Exact payload audit:** v2 audit SHA-256 `75b80b66520109f0fb93a661d23ac3dc5e08ab1c389777746e1ebd732fb8413c`; 600/600 queries are current-cache hits and zero query texts may be sent. At most 5,896 single-vector documents plus 765 field components, 6,661 de-duplicated new texts, 667 outbound attempts with no automatic retry, 1,130,034 local audit tokens, and 1.5 million provider tokens are permitted. The standard-list-price ceiling is USD 0.11.
- **Immutable approval artifacts:** authorisation packet SHA-256 `e344cb210b4bb11939536ea509f78a2fda564a15a8a0d8240babe8712db0523d`; execution seal SHA-256 `ea52ce5924e3c2da8783b49e84c92335475f728f089790dc1c58c3157ada2037`; approval-scope digest SHA-256 `def539f00d8f5bd473aba2cdace2da581448e31676bbaf0fc05010e4a04a13e4`.
- **Independent review:** the full A-I read-only review passes with no blocking finding. The formal non-authorising PASS record SHA-256 is `b979088e7d2503da35207b29cc40f3fab85c73213feed1e57170ffc5cfbadb6a`; a second narrow read-only reviewer independently verified its bindings. Both reviewers recorded `network_or_scoring_performed=false` and `can_authorise_spending=false`, and both were closed after completion.
- **Regression and gate checks:** compilation, controller regression tests, stage-gate tests, selector-adapter tests, `git diff --check`, 22/22 exact dry freeze audit, live v2 payload-state validation, seal validation, and both no-grant runner rejection tests pass. The real controller `--preflight-only` reports `PASS`, `network_requests=0`, `user_authorised=false`, and an absent confirmatory root.
- **Resume and cost controls:** a complete result can resume only when its manifest binds the current grant and its frozen prompts, candidate IDs/texts, selector configuration, rows, and recomputed summary all match. New current-cache entries require a matching complete guarded-attempt record. Guarded-attempt history is authoritative for paid calls and provider-token usage, including crash-restored responses.
- **Next gate:** no confirmatory request is authorised yet. A17 begins only after Jacky Zhang explicitly approves the exact packet, seal, review record, destination, model, purposes, local persistence, payload/call/token/cost ceilings, local BM25/SkillRouter work, and warm verification.

#### Stage 5A user-authorisation checkpoint, 2026-08-02

- **Authorisation received:** Jacky Zhang explicitly approved the exact packet SHA-256 `e344cb210b4bb11939536ea509f78a2fda564a15a8a0d8240babe8712db0523d`, seal SHA-256 `ea52ce5924e3c2da8783b49e84c92335475f728f089790dc1c58c3157ada2037`, and independent-review SHA-256 `b979088e7d2503da35207b29cc40f3fab85c73213feed1e57170ffc5cfbadb6a`, together with every external-text, request, token, cost, persistence, local-selector, warm-verification, and no-thesis-write boundary in the packet.
- **Structured evidence:** `skill_benchmark/rq2a_matched_content/confirmatory_user_authorisation.json`, SHA-256 `0dd19780d9d020c4db6a63cd4f025b30c2e1b09cf72ba9614a54e4a39b53d0c5`, passes the sealed controller's exact packet/seal/scope validation.
- **State transition:** A16P is complete. A17 is authorised to run only through the sealed controller; no manual runner invocation, scientific change, automatic retry, or thesis write is permitted.

#### A17 attempt 1 incident and safety repair, 2026-08-02

- **Observed failure:** `confirmatory-bm25-all-v1` completed locally, but controller `validate_run()` raised `NameError: name 'summarise_result_rows' is not defined` before accepting the run. This was a missing import in the post-child summary-validation path, not a data, selector, model, or provider failure.
- **Fail-safe behaviour:** execution stopped immediately; `completed_steps` remained empty; the 4,800-row BM25 artifact was moved intact to `analysis/confirmatory-controller-v1/quarantine/confirmatory-bm25-all-v1-20260802T013430Z`; the formal confirmatory directory is empty. No SkillRouter or Qwen step started, the Qwen guard directory was never created, external requests were `0`, and provider tokens were `0`.
- **Repair boundary:** safety amendment v2 permits only the existing deterministic summary-helper import, a directly exercised valid/tampered-summary regression, and freeze-gate recognition of a post-authorisation repair when formal output is empty, scientific interpretation is false, and external usage remains zero. Prompts, representations, split, selectors, scores, tie rules, aggregation, metrics, contrasts, and analysis rules are unchanged.
- **Verification:** controller summary regression, controller tests, stage-gate v1/v2 amendment tests, selector-adapter tests, and 22/22 dry freeze audit pass. Current freeze SHA-256 is `70d29cd1c2fa74b73e875daafa7d973508c181f5f7a1da43c7eef6561a68bf0c`; repaired seal SHA-256 is `839367521039a41b422a6a3ee9bd69d0c62b2515f187c280d40a187c1674d924`; repaired packet SHA-256 is `8766a9e3e2c6e682a1d795a7ae3ec3614d53bc30e1da42227e6e4f18b0f4828b`.
- **Authorisation reset:** the prior packet, seal, review, and authorisation are archived and cannot authorise the repaired controller. A16P is reopened. A17 cannot resume until a new independent PASS and fresh exact user authorisation bind the repaired packet and seal.
- **Fresh review result:** the repaired packet/seal received a full independent A-I PASS with 814 hash checks and zero failures, followed by a second narrow binding PASS. Formal review SHA-256 is `c1fc7e5413db7fb3f801d0679afafe49f63f92da1242503a5c005ced5d446095`. Controller `--preflight-only` passes with zero network requests, zero formal runs, and `user_authorised=false`. A16P now waits only for fresh exact user authorisation.

#### A17 repaired-seal reauthorisation, 2026-08-02

- **Fresh authorisation:** Jacky Zhang explicitly approved repaired packet `8766a9e3e2c6e682a1d795a7ae3ec3614d53bc30e1da42227e6e4f18b0f4828b`, seal `839367521039a41b422a6a3ee9bd69d0c62b2515f187c280d40a187c1674d924`, review `c1fc7e5413db7fb3f801d0679afafe49f63f92da1242503a5c005ced5d446095`, every unchanged payload/call/token/cost boundary, and rerunning the quarantined local BM25 step.
- **Structured evidence:** `skill_benchmark/rq2a_matched_content/confirmatory_user_authorisation.json`, SHA-256 `d2b96498cf41bcba028220e5987e71064d2e492b2bfd793c2b5ca7bedef21769`, passes exact packet/seal/scope validation.
- **State:** A16P is complete again. A17 may resume only through the repaired sealed controller; no manual run, automatic retry, scientific change, or thesis write is authorised.
- **Superseded-grant cleanup:** the first repaired invocation stopped before any child process because the preserved BM25 grant still bound the superseded seal. The controller correctly refused to overwrite it. That old grant, its log, and the intervening controller state were moved into the superseded-attempt archive without deletion. No model, result, guard, or external request was created; the current seal and authorisation remain unchanged and valid.

#### Stage 5B confirmatory completion, 2026-08-02

- **Controller result:** the repaired sealed sequence completed with `PASS` and state `complete_pending_user_results_review`. A17, A18, and A19 are complete; A20 remains blocked. No thesis LaTeX or PDF result was written.
- **Matrix gate:** four primary runs contain exactly 13,200 unique condition-prompt rows over 280 clusters, 600 prompts, and 22 conditions: BM25 4,800, SkillRouter 3,000, Qwen single-vector 4,800, and frozen field-aware 600. The complete-matrix gate passed identity, hash, role, condition-set, and row-count checks.
- **Warm verification:** SkillRouter warm reused 7,800/7,800 pair scores with zero forward passes; Qwen warm reused 6,533/6,533 embeddings with zero provider calls; field-aware warm reused 1,488/1,488 embeddings with zero provider calls. All three warm scientific-row digests exactly match their primary run.
- **External guard:** 667 attempts, 667 successes, 6,661 unique new texts, 1,130,034 local audit tokens, and 1,189,367 provider tokens. The payload was exactly 5,896 single-vector documents plus 765 field components; 600 queries were cache hits and no query text was transferred. The USD 0.07 per million token snapshot yields USD 0.08325569, below the USD 0.11 ceiling.
- **Primary contrast:** under Qwen single-vector, fielded minus matched flat Top-1 is `-0.067`, 95% cluster-bootstrap CI `[-0.099,-0.036]`, raw `p=0.0002`; the preregistered positive organisation hypothesis is not supported.
- **Key secondary contrasts:** frozen field-aware minus Qwen fielded is `+0.066`, CI `[+0.021,+0.111]`, Holm `p=0.0204`, practical support `true`; BM25 fielded minus flat is `+0.021`, CI `[+0.010,+0.033]`, Holm `p=0.0040`, below the 3pp practical threshold; SkillRouter fielded minus flat is `-0.004`, CI `[-0.014,+0.006]`, Holm `p=0.5240`. Descriptively, field-aware Top-1 `0.823` nearly equals Qwen flat `0.824`, so field-aware scoring recovers the fielded single-vector deficit rather than beating the best flat Qwen condition.
- **Content controls:** fielded versus shared-only is `+0.424` for Qwen, `+0.531` for BM25, and `+0.618` for SkillRouter; all clear the practical threshold and have Holm `p=0.0008`. This confirms that operational content matters even though headings alone do not universally help.
- **Failure decomposition:** 21 `qwen_fielded_help`, 61 `qwen_fielded_harm`, 90 `qwen_fielded_and_flat_both_fail`, 84 `field_aware_recovery`, and 54 `field_aware_harm` prompt cases. This report is deterministic descriptive evidence only.
- **Latency and construction:** primary wall time is 0.945s BM25, 6,666.917s SkillRouter, 1,087.359s Qwen single-vector, and 204.760s field-aware. Warm online selector time per prompt is about 1.10ms BM25, 2.87ms Qwen, 2.28ms field-aware, and 2.07ms cached SkillRouter lookup; uncached SkillRouter inference is 11.10s per prompt in this local run. Qwen construction is a one-time embedding cost and cached query vectors do not establish uncached query-provider latency.
- **Evidence hashes:** analysis `189d6b20b091e2f2d3bd30f168355ccf2a73efa3eef3b082075725040fec0ce7`; cost `980af3ff9c9106d7f43d029b69aa5a1bb07515faf2e15b0b96e70bca5332cdec`; failure report `a0e96747f544904d424bf6fe83a656bd3b27533b4e2b2c9b8166fb91a8c6d155`.
- **Metadata correction:** final completion state, step records, matrix, guard, and scientific artifact hashes were valid, but `controller_state.json` retained stale `failed_step` and `failure` fields from the superseded first attempt. The original state is archived unchanged at SHA-256 `19e3c6...9706`; the corrected terminal state removes only those two keys and has SHA-256 `7719d9...0560`. A machine-readable correction record preserves the before/after binding. The controller now clears failure-only fields at fresh and successful transitions, and all three regression suites pass. The exact controller used for the paid run is archived at its sealed SHA-256 `ba60ff...9f77`; the post-run hygiene version cannot be used under the old seal.
- **Next gate:** user reviews the confirmatory evidence and interpretation. Only explicit approval may unblock A20 and thesis-result writing.

### Stage 7 completion: user-reviewed thesis integration, 2026-08-02

- **State:** `PASS / A20 COMPLETE / RQ2A CLOSED`.
- **User decision:** the user approved recording the completed RQ2a result and analysis in the canonical Markdown documents and thesis.
- **Scientific boundary:** no selector was rerun, no external request was made, no embedding or frozen protocol artifact changed, and the analysis, cost, and failure-report hashes remain unchanged.
- **Documentation result:** the current trackers, snapshot, roadmap, methodology records, risk register, English/Chinese specifications, and thesis README now identify RQ2a as complete and user-reviewed. The detailed thesis-facing source is `RQ2a Confirmatory Results and Analysis - 2026-08-02.md`.
- **Thesis result:** the abstract, methodology, results, discussion, limitations, and conclusion now contain the matched-content design, correct selector architectures, complete 22-condition matrix, preregistered contrasts, descriptive field slices, cost ledger, interpretation, and claim boundaries. The methodology corrects BM25 to a fixed three-sibling decision corpus and distinguishes Qwen bi-encoder embedding from SkillRouter cross-encoder scoring.
- **Build and visual QA:** `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` passes. `thesis_latex/main.pdf` contains 82 A4 pages and has SHA-256 `2a4a30715d59b38862d451efd708e317c1ed4a7540a99f70d64c7f30be51fd02`. Poppler renders of the abstract, methodology, RQ2a results, discussion, limitations, and conclusion show no clipping, overlap, or unreadable RQ2a tables.
- **Checkpoint:** `thesis_notes/checkpoints/RQ2a Stage 7 Thesis Integration Completion - 2026-08-02.md`.
- **Final boundary:** RQ2a is complete. RQ2b remains a separate study and is now frozen/locally hardened but scientifically unexecuted; full-library Recall@K, graph/tree retrieval, downstream execution, and public-library generalisation are not RQ2a conclusions.
