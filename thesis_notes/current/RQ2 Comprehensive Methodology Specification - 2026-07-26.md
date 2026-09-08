# RQ2 Comprehensive Methodology Specification

> **2026-09-08 authority update.** The approved new V7 research plan is `thesis_notes/current/RQ2 Approved Research Plan - 2026-09-08.zh-CN.md`, with its hash-bound research-plan freeze. This older specification retains historical RQ2a/V3 implementation and result provenance; it does not override the new B36+C6 / P1–P5 plan. The future approximately 20k-background scale-out is not part of the current matrix or a claim of proven scalability.

Date: 2026-07-26

Status: RQ2a protocol, representations, selectors, development choice, confirmatory matrix, frozen analysis, cost ledger, user review, and thesis integration are **complete** and remain closed. The completed study contains 280 confirmatory clusters, 600 prompts, 22 conditions, and 13,200 aligned rows. RQ2b's base-v1 B0G full-pool semantic audit completed mechanically, but its acceptable-set freeze is **BLOCKED BEFORE RETRIEVAL**: across 7,710 resolved reviewed units for 389 scored prompts, 14 strict-gold rows are not fully acceptable and eight prompts have no fully acceptable reviewed candidate. A later user-directed review of only those 14 labels retains six gold label skills and excludes eight material workflow mismatches. The v1.1 strict-gold-only overlay therefore has 381 scored prompts and no acceptable endpoint. V3 automatically froze a 2,433-skill I3C corpus after source/coverage correction; its manual semantic QA was explicitly waived and must not be implied. All three B1 retrievers have complete, post-run-verified 1,524-row matrices. Both frozen B2 rerankers completed 4,572 strict rows over the same persisted B1 Top-20 lists and passed local integrity verification. B3-v2 synthesis, B4 review, user review, and B5 thesis integration are complete; the compiled thesis records the bounded accuracy--compression conclusion. The readable B2 record is `skill_benchmark/rq2bv1/results/B2_DUAL_RERANKER_V3_RESULTS.md`.

Operational status, implementation tasks, and supersession decisions are governed by `thesis_notes/current/RQ2 Current Status and Implementation Tracker - 2026-07-26.md`.

Confirmatory outcome, 2026-08-02: the primary positive field-organisation hypothesis is rejected under Qwen single-vector selection (`fielded - flat = -6.7pp`, 95% CI `[-9.9pp,-3.6pp]`). Frozen Qwen `uniform-top-two` field-aware scoring recovers `+6.6pp` over fielded single-vector (95% CI `[+2.1pp,+11.1pp]`) but is descriptively level with flat Qwen (`0.823` versus `0.824`). Operational facts strongly beat `shared-only` under BM25, Qwen, and SkillRouter. Detailed final analysis: `thesis_notes/current/RQ2a Confirmatory Results and Analysis - 2026-08-02.md`.

## 1. Executive Decision

RQ2 should remain one central research question, paired equally with RQ1, but it should be answered through two linked studies:

1. **RQ2a: representation mechanism** uses oracle-controlled field values to isolate whether the same operational facts become more usable when they are explicitly organised, compact, or less diluted.
2. **RQ2b: end-to-end retrieval validation (V3 execution and B5 integration complete)** tests whether selected representations remain useful when the gold skill must first be retrieved from the full library, and measures accuracy, candidate recall, latency, and context cost.

Downstream task success is retained only as a small secondary validation. Relation-aware graphs, hierarchy traversal, multi-skill composition, and prerequisite planning are excluded from the core RQ2 because they introduce inter-skill information that RQ1 did not study and require relation-sensitive gold tasks.

## 2. Proposed Research Question

> **RQ2: How do skill representation and retrieval-pipeline choices affect the preservation and use of the routing-relevant operational information identified in RQ1 under semantic confusability, and what accuracy, candidate-recall, and retrieval-cost trade-offs result?**

### RQ2a: Representation mechanism

> Given the same query, candidates, operational propositions, and selector, how do explicit field organisation and controlled information dilution affect a selector's ability to distinguish near-neighbour skills?

RQ2a asks why a representation works. It is not a full-corpus retrieval benchmark. The gold skill is guaranteed to be present, so candidate-generation failure cannot obscure the representation effect.

### RQ2b: End-to-end retrieval validation

**Protocol status: V3 executes 381 strict-gold prompts over a 2,433-skill source-grounded library. B1L BM25, B1E-Q Qwen single-vector, and B1E-SR native SkillRouter candidate generation each completed 1,524 strict rows; Qwen B2 and SkillRouter B2 each completed 4,572 post-run-verified reranked rows over the same persisted B1 Top-20 lists. B3-v2 full-matrix synthesis and B4 information-availability review completed locally, user review authorised B5, and the bounded method/results/cost/limitation statements are integrated in `thesis_latex/main.pdf`. The primary conclusion is an accuracy--compression trade-off rather than a universal I3C accuracy gain. Base-v1 acceptable endpoints remain blocked, so V3 reports strict-gold-only endpoints; V3 manual semantic QA was waived and must not be implied. Secondary field-aware B1E-F remains a negative diagnostic outside the primary matrix.**

> When the candidate set is not guaranteed, how do compact metadata, original full skill artifacts, and explicit operational-fact representations interact with lexical retrieval, dense retrieval, and reranking?

RQ2b asks whether a representation remains useful in a practical retrieve-then-rerank pipeline. It separates first-stage exclusion from downstream ordering failure.

## 3. Relationship to RQ1

RQ1 supplies a bounded set of intrinsic, per-skill operational information:

- use condition;
- input/precondition;
- output/artifact;
- workflow/procedure;
- dependency/resource or capability compatibility;
- boundary/not-for;
- success/verification.

Examples/tests remain a support-information or negative-control category rather than an eighth operational field.

RQ2 does **not** require RQ1 to prove that these are all possible routing signals. The thesis claim is restricted to the studied operational fields. It must not claim a universal or exhaustive skill schema.

The following information remains outside the core scope:

- prerequisite relations between skills;
- composition and output-to-input relations;
- alternative/substitute relations;
- parent-child taxonomy and multi-parent category membership;
- historical skill performance or user-specific preference;
- multi-skill workflow roles;
- learned graph edges or manually authored ontology relations.

These are inter-skill or system-context signals. Testing them fairly would require relation-sensitive prompts and a new gold standard.

## 4. Unit of Analysis

The primary inferential unit is the **near-neighbour skill cluster**, not an individual repeated prompt or model call.

Each RQ2a test unit contains:

- one frozen user query;
- one three-sibling near-neighbour cluster;
- one gold skill;
- two operationally incompatible but topically plausible siblings;
- the same candidate identities in every representation condition;
- a deterministic candidate-order randomisation;
- one representation condition;
- one frozen selector and scoring rule.

All prompt variants belonging to the same cluster remain grouped during resampling and statistical analysis.

RQ2b uses a query as the ranking unit but reports cluster- or family-grouped confidence intervals where family labels are available.

## 5. Source Data

### 5.1 RQ2a controlled source

Reuse the completed RQ1 field-isolation suites:

| Field suite | Clusters | Prompt variants |
|---|---:|---:|
| Use condition | 50 | 100 |
| Input/precondition | 50 | 100 |
| Output/artifact | 50 | 100 |
| Dependency/resource | 50 | 100 |
| Boundary/not-for | 50 | 150 |
| Success/verification | 50 | 100 |
| Workflow/procedure | 50 | 100 |
| **Total** | **350** | **750** |

Use a cluster-level 20/80 protocol split before any RQ2 tuning:

- development: 10 clusters per field, 70 clusters and approximately 150 prompts;
- confirmatory test: 40 clusters per field, 280 clusters and approximately 600 prompts.

This is a tuning-discipline split, not a claim that the clusters are previously unseen. RQ1 has already analysed their field discriminability. RQ2 tests a different intervention: representation of the already established propositions.

The RQ2a source of truth is each cluster's reviewed `unit.json`, not a new model extraction. These files already contain the shared non-target fields and the exact sibling-specific target value. Using them creates an oracle representation experiment in which extraction quality cannot explain the result.

The controlled `SKILL.md` files already expose the seven fields through regular headings. They are therefore structured canonical cards, not realistic noisy I2 documents. They may be retained as a diagnostic, but they must not be presented as the natural-full-document baseline used in RQ2b.

The examples/tests suite may be added as a negative-control diagnostic after all primary RQ2a decisions are frozen.

### 5.2 RQ2b local full-library source

Base RQ2b on a new date-stamped, prospectively frozen corpus version built from the audited current workspace. Do **not** reuse `benchmark-v0.4-2026-06-16`: its 126 recorded files now include 47 hash drifts and it does not bind per-skill source hashes. The prefreeze inventory is:

- 245 controlled prompts;
- 144 public-gold prompts;
- 12 low-information stress prompts, reported separately;
- 2,433 skills;
- 1,800 background-scale distractors;
- 460 imported public skills.

The headline strata remain separate:

- controlled;
- public-gold;
- low-information/underspecified stress.

For imported public skills, the I2 source must be the upstream `source/SKILL.original.md`, not the local normalised wrapper. All other skills use their authored `SKILL.md`. The new manifest must bind every approved source, prompt, acceptable-set annotation, serializer, runner, and analysis script by SHA-256. The canonical implementation contract is `RQ2b Full-Library Retrieval Execution Protocol and Run Ledger - 2026-08-02.md`.

### 5.3 Optional external portability source

The SkillRouter-Eval-Core corpus may be used as a portability appendix:

- 75 default scored tasks;
- 78,361 Easy skills;
- 79,141 Hard skills;
- 780 Hard-only distractors;
- complete cleaned I3C V2 extraction for 79,141 skills.

This external corpus is not required to answer the core RQ2. Full neural reruns are expensive and the current I2 neural comparator is incomplete. Existing FTS/BM25 and recovered neural rows must be labelled according to their actual completion and provenance.

## 6. Representation Conditions

All new representation artifacts require a dedicated manifest, serializer version, source hash, and identity alignment check.

Common identity policy:

- every candidate representation retains the same skill name or neutral controlled identifier;
- candidate IDs, gold/alternative roles, and benchmark labels are never inserted into selector-visible text;
- controlled names must remain semantically neutral;
- RQ2b I3C and I3-flat retain the same skill-name header so the matched comparison changes only field organisation;
- an empty extracted field is omitted in both I3C and I3-flat unless the source explicitly states a negative value; do not insert a synthetic “none” statement.

Canonical field order, before any order diagnostic, is: use condition, input/precondition, output/artifact, workflow/procedure, dependency/resource, boundary/not-for, success/verification.

### 6.1 RQ2a reviewed-fact controlled representations

| Label | Definition | Purpose |
|---|---|---|
| `shared-only` | The shared neutral skill description/context, identical among siblings except for identity. | Ambiguity anchor without the decisive operational distinction. |
| `same-facts-fielded` | The exact reviewed values in `unit.json`, serialised with explicit field labels and boundaries. | Explicit operational-fact representation without extraction error. |
| `same-facts-flat` | The exact same values concatenated with neutral separators; labels and headings removed. | Isolate labels and field boundaries. |
| `same-facts-prose` | Deterministic natural-language templates expressing the same reviewed propositions, with no added or omitted proposition. | Compare explicit fields with concise prose. |
| `same-facts-order-controlled` | The same fielded values with field order counterbalanced across clusters using a frozen seed. | Detect positional bias. |
| `same-facts-diluted-1x/2x/4x` | The same fielded values plus increasing shared, non-discriminative execution-support text. | Measure information dilution. |

The existing controlled full `SKILL.md` is a diagnostic serialisation of the oracle fields, not a natural I2 baseline.

`shared-only` reproduces the shared-context ambiguity established in RQ1 and serves only as an anchor; it is not a same-information representation comparison. The genuinely new RQ2a evidence comes from comparisons among `same-facts-fielded`, `same-facts-flat`, `same-facts-prose`, and `same-facts-diluted` conditions.

#### 6.1.1 Worked example for every RQ2a representation

The following worked example uses the reviewed RQ1 cluster
`skill_benchmark/rq1a_field_discriminability/input_precondition/clusters/ip01_pdf_scanned_tables/unit.json`.
It explains the intended information treatment. It is not yet the frozen byte-level serializer specification; exact templates, separators, whitespace, candidate identifiers, and padding blocks must be versioned and frozen before scoring.

Frozen direct query:

```text
Extract the invoice table rows from this scanned PDF image and return the shared structured report.
```

The three candidates have identical non-target facts. Only the reviewed input/precondition value differs:

| Candidate | Role | Input/precondition |
|---|---|---|
| A | Gold | scanned or image-based PDF invoice packet |
| B | Incompatible sibling | native PDF invoice packet with embedded selectable text |
| C | Incompatible sibling | photographed invoice images supplied as separate image files |

**`shared-only`**

Selector-visible Candidate A:

```text
Skill: Candidate A
PDF invoice table normalization skill.
```

Candidates B and C contain the same description and differ only in their neutral candidate identifier. The decisive input fact is absent, so this condition is an ambiguity anchor rather than a matched-content representation comparison.

**`same-facts-fielded`**

Selector-visible Candidate A:

```text
Skill: Candidate A

Use Condition
Use when the user needs pdf invoice table normalization skill over a provided input artifact.

Input / Precondition
scanned or image-based PDF invoice packet

Output Artifact
A structured result report with normalized findings, evidence references, input-fit notes, and unresolved assumptions.

Workflow / Procedure
1. Confirm that the provided material matches the stated input/precondition.
2. Inspect the provided material for the shared task without changing the task scope.
3. Extract or assess the relevant information using the same analysis checklist.
4. Return the shared structured result report with evidence references and caveats.

Success / Verification
- The report addresses the requested task using only the provided material.
- The report cites the evidence used for each finding or extracted record.
- The report flags missing or mismatched input instead of silently switching tasks.

Boundary / Not For
- Do not select this skill when the provided material does not match its input/precondition.
- Do not change the requested output format or workflow because of the input variant.

Dependency / Resource
- Access to the provided artifact or data source.
```

Candidates B and C contain the exact same headings and non-target values; only the text under `Input / Precondition` changes to the reviewed value in the table above.

**`same-facts-flat`**

Selector-visible Candidate A contains the exact same field values in the same canonical order, but no field names or headings:

```text
Skill: Candidate A
Use when the user needs pdf invoice table normalization skill over a provided input artifact. |
scanned or image-based PDF invoice packet |
A structured result report with normalized findings, evidence references, input-fit notes, and unresolved assumptions. |
Confirm that the provided material matches the stated input/precondition. Inspect the provided material for the shared task without changing the task scope. Extract or assess the relevant information using the same analysis checklist. Return the shared structured result report with evidence references and caveats. |
The report addresses the requested task using only the provided material. The report cites the evidence used for each finding or extracted record. The report flags missing or mismatched input instead of silently switching tasks. |
Do not select this skill when the provided material does not match its input/precondition. Do not change the requested output format or workflow because of the input variant. |
Access to the provided artifact or data source.
```

The neutral separators preserve value boundaries for deterministic parsing but do not identify which value is an input, output, boundary, or dependency. Candidates B and C again change only the reviewed input value.

**`same-facts-prose`**

Selector-visible Candidate A expresses the same reviewed propositions through one frozen natural-language template:

```text
Candidate A is used when the user needs pdf invoice table normalization skill over a provided input artifact. It accepts a scanned or image-based PDF invoice packet and returns a structured result report with normalized findings, evidence references, input-fit notes, and unresolved assumptions. It first confirms that the material matches the stated input/precondition, inspects it without changing task scope, extracts or assesses the relevant information using the shared checklist, and returns the report with evidence references and caveats. Success requires the report to address the requested task using only the provided material, cite the evidence used for each finding or extracted record, and flag missing or mismatched input rather than silently switching tasks. It must not be selected when the material does not match its input/precondition, and it must not change the requested output format or workflow because of the input variant. It requires access to the provided artifact or data source.
```

The prose template adds only grammatical connectors such as “accepts”, “returns”, and “requires”; it may not add a new operational proposition. This is a secondary comparison because those connectors themselves communicate semantic roles.

**`same-facts-order-controlled`**

This condition uses the same fielded text and exact values, but a frozen counterbalancing schedule changes only field order. One illustrative order is:

```text
Skill: Candidate A
Workflow / Procedure: [the same four reviewed steps]
Boundary / Not For: [the same two reviewed boundaries]
Output Artifact: [the same reviewed output value]
Dependency / Resource: [the same reviewed dependency]
Input / Precondition: scanned or image-based PDF invoice packet
Success / Verification: [the same three reviewed criteria]
Use Condition: [the same reviewed use-condition value]
```

Bracketed references above are explanatory shorthand, not literal selector-visible text. The implemented serializer must insert the full values shown in `same-facts-fielded`; only their order may change.

**`same-facts-diluted-1x/2x/4x`**

Each diluted condition begins with the complete `same-facts-fielded` text and appends a frozen amount of readable, sibling-identical, non-discriminative support text. Illustrative padding blocks are:

```text
P1: Review the provided material carefully and preserve evidence references in the final report.
P2: Record unresolved assumptions and note any limitations affecting interpretation.
P3: Use a consistent reporting structure and check the report for internal consistency.
P4: Avoid unsupported claims and retain traceability from findings to source material.
```

- `same-facts-diluted-1x` appends P1;
- `same-facts-diluted-2x` appends P1 and P2;
- `same-facts-diluted-4x` appends P1 through P4.

The final padding must be automatically checked against all sibling-specific decisive values and leakage terms. Every sibling in a cluster receives byte-identical padding. Therefore the treatment changes information dilution, not candidate relevance.

Across all same-facts conditions, the underlying operational propositions and candidate identities remain fixed. The controlled variables are field labels, discourse form, order, or the quantity of shared support text.

### 6.2 RQ2b practical representations

| Label | Definition | Isolated question |
|---|---|---|
| `I1` | Source-native frontmatter name plus source-native frontmatter description only; no category/tag or benchmark metadata. | Compact progressive-disclosure baseline. |
| `I2` | Complete original skill artifact from the approved source policy. | Maximum natural information and natural noise baseline. |
| `I3C-fielded` | Source-native name/description plus exact source evidence spans selected into the seven operational fields from the same I2 artifact. Generated normalized parser statements remain QA-only. Empty fields remain empty. | Explicit operational-fact representation without generated selector vocabulary. |
| `I3-flat` | Exact same selector-visible evidence spans as I3C, concatenated with neutral separators; all field labels and headings removed. | Do explicit labels/boundaries help beyond the extracted facts? |

`I2+I3C` is excluded from the minimal RQ2b study. It may be proposed later only as a separately approved deployment diagnostic.

`same-facts-diluted` must not use random characters, gibberish, or unique candidate-specific filler. Padding must be readable support text, identical among siblings within a cluster, and verified not to mention the decisive field values.

Matched-content means matched propositions, not mechanically identical token counts. Field labels are part of the structural treatment and therefore necessarily add a small number of tokens. Report the exact token/character distribution for every condition. If fielded versus flat/prose length differs by more than 10% on the median test unit, add a predeclared length-matched sensitivity condition using shared neutral text; do not silently pad only the condition expected to lose.

### 6.3 Extraction provenance rule

The existing local frozen-v0.4 `R2/I3` condition is `I3H`, a heuristic extraction. The local paid-model artifact is `I3M`. Neither may be relabelled as `I3C`.

Before the new local RQ2 headline matrix:

1. generate local I3C from the exact approved I2 artifacts using the frozen V2 extraction prompt;
2. require exactly one row per skill;
3. preserve `skill_id` and source identity;
4. validate JSON parsing and schema;
5. validate every evidence span against the source;
6. permit sparse and empty fields rather than hallucinating content;
7. record field-level missing, generic, and uncertainty flags;
8. expose only whitespace-normalized exact evidence spans to selectors, never the parser's generated normalized statement;
9. create `I3-flat` deterministically from this one I3C artifact; use the oracle-controlled variants, rather than model-extracted variants, for RQ2a.

## 7. Selector and Pipeline Conditions

### 7.1 RQ2a selectors

Primary selector:

- Qwen `text-embedding-v4`, frozen configuration, cosine similarity, no query rewriting.

Required replication selectors:

- BM25 lexical ranking;
- one frozen skill-capable cross-encoder reranker, preferably `pipizhao/SkillRouter-Reranker-0.6B`, directly scoring every candidate in the fixed set.

Required secondary mechanism selector:

- one Qwen semantic field-aware selector over `same-facts-fielded`.

The repository already contains M6-v1 and M6-v2 field-aware prototypes, but neither is a compliant RQ2a selector. M6-v1 is lexical and tied to persisted first-stage candidates. M6-v2 separately embeds selected fields, but it uses the old frozen-v0.4 representations, request parsing, calibrated field weights, boundary penalties, and first-stage-score blending. The RQ2a method will therefore adapt reusable M6-v2 components rather than report the old M6-v2 rows or claim a from-scratch implementation.

The RQ2a field-aware adapter must:

1. consume `same-facts-fielded` directly;
2. embed all seven operational fields separately;
3. embed the raw query without receiving the benchmark target-field label;
4. score all three fixed candidates directly, without candidate exclusion or first-stage-score blending;
5. receive no gold, candidate-role, cluster-field, or alternative metadata;
6. emit per-field similarities, one aggregate candidate score, the selected candidate, rank margin, and latency;
7. cache each unique query and field embedding;
8. use one target-agnostic aggregation rule across all seven field suites.

Only two aggregation candidates may be compared on the 70-cluster development split: maximum field similarity and uniform top-two average field similarity. Exactly one must then be documented and frozen. Field-specific weights, target-field oracle scoring, and confirmatory-set tuning are prohibited.

For RQ2a BM25, score each query only against its fixed three-sibling decision corpus. This is the behaviour of the completed runner and means BM25 term statistics are local to each decision rather than global to the 280-cluster split. Qwen document embeddings are computed once per representation and reused across every query. The global-index sentence in an earlier draft was never the behaviour of the completed RQ2a runner and is superseded by this correction.

Optional diagnostic:

- one frozen LLM selector prompt over all sibling candidates. This is a reasoning diagnostic, not a primary leaderboard row.

No selector is trained or tuned on the confirmatory clusters. All templates, truncation, pooling, field order, and tie rules are frozen after development.

### 7.2 RQ2b first-stage retrieval

Required:

- BM25;
- Qwen `text-embedding-v4`;
- prospectively amended `pipizhao/SkillRouter-Embedding-0.6B` as a required secondary replication.

The SkillRouter-embedding replication uses the released query instruction, last-token pooling, 1,024-dimensional L2-normalized vectors, cosine scoring, and one complete representation up to the pinned model configuration's 32,768-token ceiling. It forbids truncation and chunk aggregation and aborts on any overlength text. Exact model/revision/file hashes, caches, latency, and zero-forward warm reproduction are required.

Qwen `text-embedding-v4` and `SkillRouter-Embedding-0.6B` are both bi-encoder-style embedding retrievers, but they are different trained models. Qwen is the generic-provider, max-chunk primary dense condition. SkillRouter embedding is the skill-tuned, full-context required secondary replication and does not enter the frozen eight-hypothesis multiplicity family. The later B2 condition uses the separate `SkillRouter-Reranker-0.6B`: it jointly scores each query-candidate pair as a cross-encoder-style reranker and does not create reusable document embeddings.

**Current execution state (2026-08-21).** The V3 Qwen primary max-chunk run at
`skill_benchmark/rq2bv1/results/qwen_primary_v3/` is complete. It bound the
four existing representations, 2,433 candidates, 381 strict prompts, 9,735
lossless chunks, and 1,524 strict result rows. The approved run made 1,276
successful no-retry calls for 8,945 documents and 381 separately measured cold
queries; post-run verification revalidated all strict rows, 3,828 request
record hashes, candidate identities, and all warm replays. The Qwen field-aware
`uniform-top-two` method remains a separately registered post-freeze B1E-F
amendment; it does not change this primary single-vector/max-chunk condition,
any existing B1L result, or the interpretation of the completed Qwen run.

### 7.3 RQ2b reranking

The intended B2 comparator set has three branches for every B1 condition:

- first-stage retrieval only;
- first-stage retrieval plus `SkillRouter-Reranker-0.6B`;
- first-stage retrieval plus generic Qwen `qwen3-rerank`.

The two rerankers are separate comparators, not an ensemble. Each must receive the identical raw query, representation text, persisted Top-20 candidate IDs, candidate order, and `K` for a given B1 condition. Neither may regenerate candidates, rewrite a query, use label metadata, or silently apply a different truncation policy. Candidate sets must be persisted before either reranker runs.

Primary rerank budget:

- `K=20`.

`K=5` is a zero-new-forward-pass sensitivity obtained by slicing persisted K=20 scores. `K=50` is excluded from the minimal study unless prospectively amended and separately authorised.

Each first-stage condition must reuse its own document/query embeddings or lexical scores and persisted candidate lists between retrieval-only and retrieval-plus-reranker branches. SkillRouter reranking and Qwen reranking each perform new query-candidate scoring, but both must consume that same exact persisted candidate list. They require separate score caches, token accounting, latency logs, and warm-cache verification. Qwen execution remains conditional on B0F-A2 review, approval, and a matching implementation seal.

## 8. RQ2a Experimental Matrix

### 8.1 Confirmatory core matrix

| Axis | Confirmatory conditions |
|---|---|
| Prompt set | 280 test clusters, approximately 600 prompts |
| Candidate regime | Three-sibling family-only set |
| Representations | shared-only, same-facts-fielded, same-facts-flat, same-facts-prose, same-facts-diluted-2x |
| Core selectors | Qwen single-vector embedding; BM25; fixed cross-encoder |
| Required secondary selector | Qwen semantic field-aware adapter on `same-facts-fielded` |
| Reasoning diagnostic | One frozen LLM A/B/C/ABSTAIN selector; not a core leaderboard condition |
| Gold | Existing cluster gold |
| Primary outcome | Paired top-1 accuracy |
| Secondary outcomes | MRR, near-neighbour confusion, rank margin, selector-visible tokens |

Approximate scoring volume:

- 600 prompts x 5 representations x 3 candidates = 9,000 query-candidate scores per selector;
- 27,000 scores across the three core selectors;
- 1,800 additional candidate scores for the required field-aware comparison on `same-facts-fielded`, excluding its seven component-field similarities and the optional LLM diagnostic.

This is feasible without building a new corpus.

### 8.2 RQ2a diagnostics

Run only after the core matrix:

| Diagnostic | Conditions | Purpose |
|---|---|---|
| Field order | same-facts-fielded canonical versus same-facts-order-controlled | Detect positional bias. |
| Dilution curve | 0x, 1x, 2x, 4x padding | Estimate robustness to increasing context noise. |
| Irrelevant candidates | Three siblings plus five fixed unrelated skills | Check whether broad distractors change the representation effect. |
| Controlled full card | Existing controlled `SKILL.md` versus oracle-fielded serialisation | Verify that the authored canonical card behaves as expected; do not interpret it as natural I2. |
| Negative-control information | Generic examples/tests only | Test whether support text provides stable routing value. |

### 8.3 RQ2a primary comparison

Pre-register one primary contrast:

> `same-facts-fielded` versus `same-facts-flat` under Qwen embedding on the confirmatory test clusters.

Required replications:

- the same paired contrast under BM25;
- the same paired contrast under the fixed cross-encoder.

Key secondary contrasts:

- same-facts-fielded versus same-facts-prose;
- same-facts-fielded versus same-facts-diluted-2x;
- same-facts-fielded versus shared-only;
- Qwen field-aware versus Qwen single-vector on the identical `same-facts-fielded` text.

## 9. RQ2b Experimental Matrix (Frozen Core)

The broad parking design formerly in this section has been reduced to a minimal B1/B2 study. Exact representation bytes, acceptable-set closure, chunking, hypotheses, inference, approvals, and stop rules live in `RQ2b Full-Library Retrieval Execution Protocol and Run Ledger - 2026-08-02.md`. That execution protocol is canonical when this overview is less specific and is now frozen under the recorded B0F approval hashes.

### 9.1 Stage B1: full-library first-stage retrieval

| Axis | Conditions |
|---|---|
| Corpus | 2,433-skill approved full library |
| Prompt strata | Current v1.1 strict-gold execution overlay: 243 controlled; 138 public-gold; 12 stress separately |
| Representations | I1, I2, I3C-fielded, I3-flat |
| Retrievers | BM25; Qwen max-chunk embedding; SkillRouter full-context embedding as a required secondary replication |
| Candidate budgets | Ranks at 1, 5, 20, 50, 100 |
| Primary metrics | strict Recall@20 and strict Hit@1; acceptable endpoints are unavailable in v1.1 |
| Secondary metrics | strict MRR@10, strict Recall@5/50/100, rank summaries, and recorded cost/latency; base-v1 acceptable/role-derived miss classes are not v1.1 endpoints |

All retrieval rankings are persisted once and reused downstream.

### 9.1A Secondary B1E-F field-aware amendment

The frozen 12-cell B1 matrix is unchanged. On 2026-08-21, the project recorded
`B1E-F` as a separately labelled, Qwen-only secondary candidate-generation
method. It does not compare I3C-fielded and I3-flat as pooled serialisations.
Instead, it embeds the raw query once, embeds each of the seven labelled I3C
candidate fields separately, and uses the frozen target-agnostic
`uniform-top-two` aggregation rule. Because this field-aware full-library cell
was registered after B1L results were seen, it cannot be called a primary
pre-registered condition, cannot rewrite B1L, and requires a separate V3
payload, preflight, external approval, and result section. Its exact protocol is
`skill_benchmark/rq2bv1/amendments/B1E-F_Field_Aware_Secondary_Amendment.md`.

### 9.2 Stage B2: fixed reranker over persisted candidates

| Axis | Conditions |
|---|---|
| First stage | BM25; Qwen embedding; SkillRouter embedding |
| Representations | I1, I2, I3C-fielded, I3-flat |
| Primary K | 20 |
| Sensitivity K | 5 by slicing K=20 scores; no K=50 in the minimal study |
| Rerankers | SkillRouter cross-encoder and generic Qwen `qwen3-rerank`; each independently reranks the identical persisted Top-20 candidates. Qwen is mandatory in the intended comparator set but awaits B0F-A2 review/approval/seal before execution. |
| Metrics | conditional strict Hit@1, end-to-end strict Hit@1/MRR, reranker gain/regression, rerank latency/tokens; acceptable endpoints are unavailable in v1.1 |

The minimal RQ2b study excludes nested-scale pools, graph/tree routing, external SkillRouter-Eval-Core portability, I2+I3C, downstream task execution, and K=50 reranking. Native SkillRouter embedding is included through B0F-A1. Generic Qwen `qwen3-rerank` is a required, pre-specified B2 comparator through B0F-A2; its results are reported separately from SkillRouter reranking and neither model is treated as an ensemble. B0F-A3's base-v1 B0G audit tested whether acceptable endpoints had adequate label coverage and stopped before retrieval: strict-gold coverage fails for 14 rows and fully-acceptable coverage fails for eight prompts. The user-directed 14-case remediation retains six strict gold labels and excludes eight material mismatches, leaving a strict-gold-only v1.1 path after its manifest is materialised; it cannot support acceptable endpoints. The other extensions may be proposed only after a complete, separately approved B1/B2 analysis; they are not required for answering the current RQ2b.

## 10. Gold and Ambiguity Policy

### Controlled clusters

- retain the frozen RQ1 gold;
- candidate identities remain fixed;
- prompt variants inherit the same cluster identity;
- do not manufacture a unique gold when the prompt lacks the decisive requirement.

### Public-gold

- strict gold: the designated source skill;
- acceptable gold: strict gold plus documented functionally valid alternatives;
- ambiguous: more than one candidate is equally suitable and no tie-breaker exists;
- no-valid-skill: no candidate satisfies the documented preconditions/output requirements.

Public gold is defined by operational suitability, not lexical similarity.

The ideal validity standard is dual independent annotation with adjudication. If ethics approval, time, or recruitment prevents this, use a documented researcher-curated audit and explicitly label the resulting limitation. Do not present agent-generated labels as independent human validation.

### Low-information prompts

Report separately as an abstention/clarification stress test. Do not merge them into ordinary top-1 accuracy.

## 11. Metrics

### RQ2a primary

- paired top-1 accuracy difference;
- 95% cluster-bootstrap confidence interval.

### RQ2a secondary

- MRR;
- gold-versus-best-sibling score margin;
- near-neighbour confusion rate;
- performance by RQ1 field;
- performance by direct/paraphrase/contextual/implicit-authority variant;
- selector-visible tokens or characters;
- latency by selector.

### RQ2b first stage

- strict and acceptable Hit@1;
- strict and acceptable Recall@5/20/50/100;
- MRR;
- candidate full-coverage where multiple acceptable skills exist;
- error destination: annotated near neighbour, unrelated distractor, or missing gold.

### RQ2b reranking

- conditional Hit@1 given that at least one valid gold is in top-K;
- end-to-end strict and acceptable Hit@1;
- end-to-end MRR;
- reranker gain over its exact persisted first-stage candidate list;
- reranker regression rate: first-stage top-1 was valid but reranker displaced it.

### Cost and efficiency

- source and representation characters/tokens;
- offline extraction calls, tokens, time, and failures;
- document embedding compute time;
- index build time and index size;
- query embedding latency;
- search latency;
- reranker pairs, tokens, and latency;
- selector-visible tokens;
- median and p95 online routing time;
- cold-cache and warm-cache measurements.

Use three distinct token terms:

- **index-visible tokens**: total representation text processed during document embedding or lexical indexing;
- **reranker-visible tokens**: query plus top-K candidate representation text processed per request;
- **agent-visible tokens**: the selected full skill artifact loaded after routing for execution.

Do not call all three “selector tokens”. RQ2 primarily compares index-visible and reranker-visible cost. Agent-visible tokens belong to the secondary incorporation/execution stage unless the loading policy itself changes.

Monetary cost may be reported as a date-stamped supplement, not the primary efficiency measure.

## 12. Cost Model

Separate one-time and per-query costs.

Let:

- `C_extract` = one-time I3C extraction cost;
- `C_doc_embed` = one-time document embedding cost;
- `C_index` = one-time index construction/storage cost;
- `C_query_embed` = per-query embedding cost;
- `C_search` = per-query retrieval cost;
- `C_rerank(K)` = per-query reranking cost at candidate budget K;
- `N` = number of queries served by the fixed library version.

Then:

```text
amortised_cost_per_query(N)
= (C_extract + C_doc_embed + C_index) / N
  + C_query_embed
  + C_search
  + C_rerank(K)
```

Report break-even curves over plausible `N` values rather than assuming one usage volume. Recompute offline costs when the source skill changes; reuse them across queries while the representation version remains valid.

## 13. Hypotheses

### RQ2a hypotheses

**H2a-Content.** Reviewed-fact representations that preserve the RQ1 operational facts will outperform `shared-only` on near-neighbour discrimination, especially for strong RQ1 fields.

**H2a-Organisation.** `same-facts-fielded` will outperform `same-facts-flat` and `same-facts-prose` when the selector can exploit field boundaries. The effect may be small or model-specific; a null result would show that the facts, rather than literal labels, carry most value.

**H2a-Explicit field use.** On identical `same-facts-fielded` text, a target-agnostic field-aware Qwen selector will outperform the Qwen single-vector selector if separate field scoring preserves useful query-to-field matches that are diluted by one-vector pooling. A null result would show that explicit segmentation, as currently aggregated, adds no measurable value beyond exposing the fielded text.

**H2a-Dilution.** Holding decisive facts fixed, routing accuracy and score margin will decrease as non-discriminative support text increases.

**H2a-Reasoning interaction.** Boundary, success/verification, and workflow/procedure will benefit more from a cross-encoder or reasoning selector than from lexical or single-vector embedding retrieval.

**H2a-Field interaction.** Input/precondition, use condition, and output/artifact are expected to remain robust under paraphrase, while implicit boundary and fine-grained workflow/success distinctions will remain harder.

**H2a-Oracle validity.** Because RQ2a uses reviewed oracle values, any performance difference among fielded, flat, prose, and diluted conditions can be attributed to representation rather than extraction quality.

### RQ2b strict-only v1.1 analysis objectives (not yet executed)

**H2b-Compression.** Compare I3C with I2 on separate-stratum strict Recall@20, strict Hit@1, strict MRR@10, and index-visible/reranker-visible text. Do not reuse base-v1 acceptable endpoints or its margin without a refreshed strict-only inference seal.

**H2b-Discovery.** Compare I3C with I1 on strict candidate recall across the controlled and public-gold strata. The study does not claim an unannotated “description lacks evidence” subset.

**H2b-Organisation.** I3C-fielded versus I3-flat may differ under Qwen because field boundaries change how the same evidence is encoded; the direction is not assumed.

**H2b-Pipeline decomposition.** SkillRouter and generic Qwen rerankers are distinct B2 comparators over an immutable Top-20 list: either may improve conditional ordering but neither can repair queries whose strict gold is absent from the candidate set. Compare their conditional strict Hit@1, end-to-end strict Hit@1, regression rate, latency, visible tokens, and cost separately. Their comparison is secondary and must hold the candidate list fixed.

**H2b-Retriever interaction.** BM25 will be stronger on direct terminology, while dense retrieval will be more robust to paraphrases; representation rankings may therefore differ by retriever.

**H2b-Efficiency.** I3C is expected to use substantially fewer index-visible and reranker-visible tokens than I2. Its extraction cost must be reported separately and amortised over repeated queries.

### Secondary downstream hypothesis

**H2-Downstream.** Correct routing should be associated with higher task success, but routing accuracy will not perfectly determine execution success because skill quality, agent reasoning, tools, and environment also intervene.

## 14. Expected Result Patterns

Expected results are prospectively specified interpretations, not claims that the result has already occurred.

| Possible pattern | Interpretation |
|---|---|
| same-facts-fielded > same-facts-flat and same-facts-prose | Explicit field organisation adds selector-usable structure beyond facts alone. |
| same-facts-fielded approximately same-facts-flat, both > shared-only | Operational content matters; literal labels are not necessary. |
| same-facts-fielded approximately same-facts-prose | The compact facts matter, but schema formatting does not add measurable value. |
| field-aware Qwen > single-vector Qwen on same-facts-fielded | Explicit field-wise use adds value beyond merely displaying field boundaries. |
| field-aware Qwen approximately single-vector Qwen | Separate field scoring and target-agnostic aggregation add no measurable benefit in this setting. |
| I2 > I3C | Extraction/compression removes useful evidence, or natural context supplies interactions not captured by the fields. |
| I3C > I2 with much lower tokens | Explicit fact preservation reduces dilution and improves the accuracy-cost trade-off. |
| I3C helps cross-encoder but not BM25/Qwen embedding | Structure requires interaction or field-sensitive reasoning rather than simple matching. |
| Dilution curve is flat | The selector is robust to added support text; full-document noise is not the main bottleneck in this setting. |
| Recall improves but Hit@1 does not | Representation helps candidate generation but not final disambiguation. |
| Conditional reranking improves but end-to-end does not | First-stage candidate exclusion is the bottleneck. |
| Unrelated scale has little effect but hard-neighbour count hurts | Semantic confusability, rather than corpus size alone, drives failure. |
| No representation consistently wins | There is no universal best layer; representation should be selected by retriever, field type, and cost budget. |

Based on existing exploratory evidence, mixed results are more plausible than a universal I3C victory. Current local controlled rows often place I3H between I1 and I2, while public-original full text can be strong. Conversely, the external 79K-skill lexical result shows cleaned I3C matching or exceeding I2 on several metrics at roughly one tenth of I2 token volume. These observations motivate, but do not answer, the new matched-content experiment.

## 15. Statistical Analysis

### Confirmatory analysis

- preserve cluster grouping;
- compute paired top-1 differences per representation contrast;
- use cluster bootstrap with at least 10,000 resamples;
- report effect size in percentage points and 95% confidence intervals;
- use Holm correction for the predeclared family of key secondary contrasts;
- report all null and negative results.

These bullets describe the completed RQ2a analysis. RQ2b instead uses the eight atomic hypotheses, prompt-weighted grouped bootstrap, grouped paired sign-flip randomisation, equal-group sensitivity, and non-inferiority intersection rule frozen in its canonical execution protocol. Ordinary prompt-level McNemar inference is not used for RQ2b because prompts share family-level dependence.

Suggested smallest effect of practical interest:

- 3 percentage points in top-1, subject to supervisor approval before confirmatory analysis.

### Sensitivity analysis

- mixed-effects logistic regression with representation as a fixed effect and cluster as a random intercept;
- representation-by-selector interaction;
- representation-by-field interaction;
- separate direct, paraphrase, contextual, and implicit-authority strata;
- strict versus acceptable public-gold scoring;
- document-length and extraction-completeness strata.

Repeated API calls do not create independent observations. If stochastic selectors are used, average repeated calls within the test unit and keep the cluster as the inferential unit.

## 16. Secondary Downstream Validation

Do not remove existing task-success and execution-time evidence, but do not use it as primary proof of representation quality.

If provenance is sound, run or retain a small stratified subset:

- 30–50 tasks;
- prioritise tasks where two routing pipelines select different skills;
- freeze the agent model, tool environment, skill artifact, execution budget, and evaluator;
- compare routed skill identity before execution;
- measure task success, end-to-end time, environment interactions, and failure type;
- analyse success conditional on routing correctness.

Separate:

- routing latency;
- skill loading/context time;
- skill execution time;
- total task completion time.

The downstream section answers whether routing improvements translate into practical benefit. It does not establish the causal representation effect.

## 17. Graph, Tree, and Relation Scope

### Excluded from the core

- typed prerequisite/composition graphs;
- DAG planning;
- multi-skill retrieval;
- ontology construction;
- learned relation extraction;
- hierarchy training;
- branch-routing optimisation.

These methods carry or construct information beyond RQ1's per-skill fields.

### Permissible optional extension

A small graph-as-index experiment is permissible only if:

- nodes expose exactly the same approved representation as the flat baseline;
- edges are deterministically derived from that same information;
- no extra manual or model-generated relation labels are introduced;
- the task remains single-skill routing;
- the claim is limited to search efficiency, branch/candidate recall, and early-exclusion failure.

It must not be described as evidence that relation-aware skill routing is solved.

## 18. Novelty Evaluation

Closest work creates a real overlap risk:

- [SkillRouter](https://arxiv.org/abs/2603.22455) shows that full skill bodies can be decisive and proposes a large-scale retrieve-and-rerank router.
- [SSL](https://arxiv.org/abs/2604.24026) introduces Scheduling-Structural-Logical representations and evaluates structured skill discovery and risk assessment.
- [Tool-DE](https://arxiv.org/abs/2510.22670) enriches tool documentation with structured fields and analyses individual field contributions.
- [ToolRet](https://aclanthology.org/2025.findings-acl.1258/) shows that generic information retrieval competence does not guarantee strong capability retrieval.
- [SkillRet](https://arxiv.org/abs/2605.05726) provides a large public-skill benchmark with tags, taxonomy, and retrieval training data.
- [Skill Retrieval Augmentation](https://arxiv.org/abs/2604.24594) decomposes the wider pipeline into retrieval, incorporation, and application.
- [SkillNet](https://arxiv.org/abs/2603.04448) organises skills through ontology and rich relations.
- [Task Decomposition-Guided Reranking](https://arxiv.org/abs/2607.06283) uses subtask/state decomposition and a DAG-style skill reranking framework with downstream environment evaluation.

The thesis must not claim:

- the first structured skill representation;
- the first field expansion or field ablation for capability retrieval;
- the first retrieve-then-rerank skill router;
- the first large-scale skill benchmark;
- the first graph, hierarchy, or DAG representation of skills;
- that seven operational fields are universally sufficient;
- that I3C is a universally superior representation.

The defensible candidate novelty is:

> A controlled, field-grounded evaluation of single-skill pre-execution routing that separates operational-fact content, explicit field organisation, information dilution, first-stage candidate recall, and conditional reranking under deliberately near-neighbour skill confusions.

More specifically, the contribution is the combination of:

1. RQ1-derived operational distinctions rather than generic metadata categories;
2. same-fact matched-content controls;
3. explicit separation of candidate-generation and reranker failure;
4. provenance-correct original artifacts, immutable candidate sets, and strict/acceptable duplicate closure;
5. an amortised offline/online cost model;
6. source-grounded extraction QA and explicit long-document length-bias sensitivity.

The phrase “first” should not be used in the final thesis without a final systematic literature check.

## 19. Research-Question Evaluation

| Criterion | Evaluation | Reason |
|---|---|---|
| Importance | High | Skill libraries are growing, and near-neighbour applicability cannot be solved reliably by topic matching alone. |
| Internal coherence | High | RQ1 identifies useful information; RQ2 tests how systems expose and use it. |
| Answerability | High if scoped | The main variables can be manipulated with existing clusters and library artifacts. |
| Novelty | Moderate to strong diagnostic novelty | Related work already covers full bodies, structured layers, document expansion, and reranking; novelty comes from causal separation and matched controls. |
| Feasibility | High for RQ2a; provisionally high for minimal RQ2b | B0 confirms 2,433 valid sources and 401 prompts; the reviewed B1/B2 design reuses existing infrastructure, but extraction and neural stages require separate approvals and cost seals. |
| External validity | Medium | Public originals and optional external SkillRouter data help, but controlled clusters remain synthetic. |
| Risk | Manageable | Main risks are provenance, extraction error, public gold ambiguity, and over-broad claims. |

The question becomes infeasible if graph/tree construction, a new public benchmark, complete 80K-skill neural reruns, many rerankers, and large downstream execution are all treated as mandatory.

## 20. Feasibility and Work Estimate

### Already available

- 350 RQ1 controlled clusters and 750 prompt variants;
- historical frozen-v0.4 benchmark plus the new RQ2b prefreeze source/prompt inventories and drift audit;
- BM25 and Qwen retrieval runners;
- Qwen and SkillRouter-style reranking infrastructure;
- I1, I2, I3H, and local I3M artifacts;
- complete external 79,141-row I3C V2;
- current result aggregation and failure-mode tooling.

### Final RQ2a work state

- deterministic same-facts fielded/flat/prose/order/dilution serializers: `COMPLETE / FROZEN`;
- representation-equivalence validator: `COMPLETE / PASS`;
- fixed-candidate runner and BM25, Qwen, and SkillRouter adapters: `COMPLETE / CONFIRMATORY PASS`;
- leakage-free semantic field-aware adapter and target-agnostic aggregation choice: `COMPLETE / UNIFORM-TOP-TWO FROZEN`;
- development and confirmatory cost and latency ledgers: `COMPLETE`;
- paired statistical analysis, confirmatory freeze, and full-family inference: `COMPLETE / PASS`;
- confirmatory scoring: `COMPLETE / 280 CLUSTERS / 600 PROMPTS / 22 CONDITIONS / 13,200 ROWS`;
- thesis result tables and interpretation: `COMPLETE / USER-REVIEWED / THESIS-INTEGRATED`.

### RQ2b work state (protocol frozen, execution stage-gated)

- source/prompt/provenance and legacy-drift audit: `COMPLETE / PASS`;
- offline token-limit audit: `COMPLETE / PASS`;
- independent adversarial protocol review and focused rereview: `COMPLETE / FINAL PASS`;
- scientific protocol freeze: `COMPLETE / USER-APPROVED B0F`;
- B1X I3C transfer packet: `COMPLETE / 2,433 ROWS / 57 CHUNKS / UNTRANSMITTED`;
- B1S local I1/I2 and pipeline implementation: `PRE-V1.1/PRE-A2 SCOPE COMPLETE / V17 SMOKE PASS / INDEPENDENT PASS 13 ELIGIBLE / IMPLEMENTATION SEAL VERIFIED`; v1.1 strict result schemas, BM25 serializer, shared rerank aggregator, strict analysis binding, and their synthetic smoke tests are `COMPLETE / ZERO NETWORK / NOT SCIENCE`. The first v1.1 independent review failed, its rank/binding/reporting/finite-score defects were remediated locally, a fresh review passed with no P0/P1, and a narrow strict-contract seal is complete; Qwen/SkillRouter adapters remain later B1/B2 requirements;
- B1R source-text extraction and automatic merge: `COMPLETE / 2,433 ROWS / 57 CHUNKS / 63 EXPLICIT ASSIGNMENTS`; all automatic JSONL, row, identity, literal-evidence, heading-only, duplicate-ID, and missing-ID gates pass. The six recorded failed/replacement attempts stay within the approved ceilings; no network or external API call occurred;
- V3 I3C integrity: `AUTOMATIC INTEGRITY FROZEN / 2,433 ROWS / 57 CHUNKS`; after whole-chunk root-coverage repair, the frozen report replays source hashes, exact evidence, heading exclusion, identity, serialisation, root coverage, duplicate observation, and scaffold lint. The protocol-invalid V3 120-row manual-QA attempt is quarantined and unscored; a replacement manual review is explicitly waived, so this is not an independent semantic-completeness claim;
- B1L local BM25: `COMPLETE / POST-RUN INTEGRITY VERIFIED / USER RESULT REVIEW REQUIRED`; approved packet `caf10c...e8ec` and receipt `def03cd...f255` produced four V3-bound 2,433-row indexes and 1,524 strict rankings over 381 prompts. Every Top-100 was persisted; a separate verifier revalidated all rows and all 1,524 disk-index replays (`3ec257...77cc`, `029b80...3506`). This is a local lexical baseline only: no network, external API, embedding, reranking, provider call, or thesis-result writing occurred;
- embeddings, reranking, and final cost ledger: `NOT STARTED / NOT AUTHORISED`.

### Approximate compute scale

- RQ2a core: approximately 27,000 query-candidate scores across three core selectors, plus 1,800 candidate scores for the required field-aware comparison;
- RQ2b document embeddings: at most 4 x 2,433 = 9,732 document representations, reusable across all queries;
- local headline prompts: 389 controlled plus public-gold queries, with 12 stress prompts separate;
- top-20 reranking across two first stages and four representations: at most 62,240 query-candidate pairs before staged reduction;
- reranking only I2/I3C in sensitivity runs halves the expensive portion.

This is honours-feasible if embeddings are cached, conditions are staged, and the optional external/downstream/graph extensions remain non-blocking.

## 21. Validity Threats and Mitigations

| Threat | Consequence | Mitigation |
|---|---|---|
| Synthetic controlled language | Inflated regularity and lexical overlap | Keep public-original RQ2b separate; report controlled and public strata independently. |
| Public gold ambiguity | False negatives | Strict plus acceptable gold; documented operational rationale; adjudication where possible. |
| Extraction hallucination/omission | I3C effect confounded with extraction quality | Exact evidence validation; sparse fields allowed; corrected stratified subset. |
| I3C formatting affinity | One model may prefer Markdown/JSON | Same-fact flat/prose controls; BM25, dense, and cross-encoder replication. |
| Information-length confound | Shorter documents may appear better | Matched-content controls, token reporting, dilution curve, length-stratified analysis. |
| Field-order bias | Early fields receive disproportionate attention | Counterbalanced order diagnostic. |
| Query leakage | Prompts repeat exact field wording | Direct and paraphrase strata; no query generation from the evaluated serialisation. |
| Target-field oracle leakage | The field-aware selector is told which suite or field to favour | Supply only the raw query and seven candidate fields; use one target-agnostic aggregation rule frozen on development clusters. |
| Candidate-set drift | Reranker comparisons become unfair | Persist candidate identities and scores before reranking. |
| Truncation | Long I2 or I3C text silently loses evidence | Record model limits; chunk/aggregate only under a frozen policy; report truncation rate. |
| Provider/model drift | Results cannot be reproduced | Record model identifier, date, API settings, code hash, and cache key. |
| Repeated prompts treated as independent | Confidence intervals too narrow | Cluster-level inference. |
| Cost measurement inconsistency | Misleading efficiency claims | Separate cold/warm, offline/online, retrieval/rerank/execution. |
| Researcher-designed representation | Confirmation bias | Freeze serializers before scoring; retain null/negative outcomes. |

## 22. Quality Gates

### Gate 0: protocol freeze

- exact RQ wording approved;
- core versus optional experiments approved;
- primary comparisons and metrics frozen;
- no confirmatory results inspected during design changes.

### Gate 1: source provenance

- one approved I2 source per skill;
- public originals, not wrappers;
- skill identity and hash manifest complete;
- benchmark version declared.

### Gate 2: I3C extraction

- 2,433/2,433 identity-aligned rows;
- 100% JSON parse success;
- zero duplicate or missing skill IDs;
- exact source evidence validation;
- empty fields allowed and recorded;
- extraction prompt and schema version frozen.

### Gate 3: matched-content equivalence

- same-facts-fielded, same-facts-flat, and same-facts-prose carry the same reviewed field-value propositions;
- no serializer invents or drops a fact;
- field labels/order are the only intended structural changes;
- dilution padding contains no sibling-discriminating cue.

### Gate 4: candidate identity

- identical candidate IDs across representation conditions;
- deterministic ordering seed stored;
- gold and acceptable alternatives verified.

### Gate 5: runner reproducibility

- query and document caches stored;
- model and truncation settings recorded;
- reranker consumes persisted first-stage lists;
- the RQ2a field-aware selector sees no target-field, gold, role, or alternative metadata and uses one frozen aggregation rule;
- smoke tests pass before full runs.

### Gate 6: analysis reproducibility

- row-level results retained;
- aggregation script regenerates every table;
- cluster bootstrap and multiple-comparison policy frozen;
- strict and acceptable metrics not mixed.

## 23. Stop Rules

Stop expanding the experiment when:

- the RQ2a core matrix, required field-aware comparison, and required replications are complete;
- the RQ2a cost ledger and failure decomposition are complete;
- result conclusions remain stable under the declared sensitivity checks.

RQ2b has its own canonical stop rules covering source hashes, selector-visible leakage, lossless chunk coverage, immutable candidates, external ceilings, checkpoint validity, and complete-matrix analysis. B0F is approved, B1X is complete without transmission, and B1S local smoke passes; no scientific run may begin until the remaining independent-review, seal, and stage-specific authorisation gates pass.

Do not add graph/tree, ToolRet transfer, another reranker, another embedding model, or an 80K-skill neural rerun unless it resolves a specific unresolved claim.

Stop a hosted run if:

- source or representation hashes do not match the manifest;
- progress logging cannot identify the active condition;
- embeddings are being recomputed instead of reused;
- results are not checkpointed after each completed condition;
- the estimated remaining cost exceeds the approved budget.

## 24. Required Artifacts and Deliverables

Current RQ2a deliverables:

1. RQ2a protocol manifest.
2. Same-facts fielded/flat/prose/dilution serializers.
3. Representation-equivalence QA report.
4. RQ2a development/test cluster manifest.
5. Fixed-candidate ranking rows for BM25, Qwen single-vector, the cross-encoder, and the field-aware Qwen selector.
6. Field-aware aggregation development report and frozen rule.
7. Cost and latency ledger.
8. Cluster-bootstrap and sensitivity-analysis report.
9. Failure-mode examples with exact query/skill evidence.
10. Thesis-ready RQ2a methodology and result tables.
11. Claim-boundary and limitations table.

RQ2b deliverables under the approved protocol, with execution still stage-gated:

1. Local I3C JSONL with extraction QA.
2. RQ2b I1/I2/I3C/I3-flat serializers.
3. Full-library retrieval rows.
4. Persisted top-5/top-20/top-50 first-stage candidate views; K=20 is the only core reranking budget.
5. Reranker row-level outputs.
6. Grouped inference, length-bias sensitivity, and failure-decomposition outputs.
7. Thesis-ready RQ2b result tables, written only after user result review.

## 25. Thesis Chapter Structure

### Methodology

1. RQ2 scope and relationship to RQ1.
2. Source corpus and provenance.
3. Representation construction.
4. RQ2a fixed-candidate design.
5. RQ2b retrieve-then-rerank design, executed only after protocol and stage-specific approvals.
6. Gold and ambiguity policy.
7. Metrics, statistics, and cost model.
8. Secondary downstream validation.
9. Validity threats.

### Results

1. Representation integrity and token statistics.
2. RQ2a matched-content results.
3. Field- and selector-specific interactions.
4. Dilution and ordering diagnostics.
5. RQ2b first-stage candidate recall, only after the separately authorised study is completed and user-reviewed.
6. Conditional reranking and end-to-end accuracy, only if RQ2b is completed.
7. Accuracy-context-latency and amortised-cost analysis.
8. Extraction QA, length-bias sensitivity, and failure analysis, only if RQ2b is completed.
9. Secondary downstream validation, if retained.

### Discussion

1. Whether operational content or explicit structure explains gains.
2. When full text is worth its cost.
3. Where reranking helps and where first-stage recall dominates.
4. Which RQ1 fields require reasoning-heavy selection.
5. Implications for skill authors and routing-system designers.
6. Why relation-aware graph routing remains future work.

## 26. Claim Discipline

Permitted claims, if supported:

- studied operational facts improve near-neighbour routing relative to compact metadata;
- explicit field organisation adds value, has no effect, or is model-specific under matched content;
- full text and structured facts occupy different accuracy-cost positions;
- reranking cannot compensate for missing first-stage candidates;
- extraction fidelity places an upper bound on structured-representation performance.

Prohibited claims:

- all routing-relevant information has been identified;
- I3C always beats full documents;
- structured fields are the only correct skill representation;
- graph/tree methods are inferior without running relation-sensitive tests;
- improved routing proves improved task execution;
- provider-priced monetary cost is stable across time;
- incomplete external neural rows form a complete comparison.

## 27. Decision Points Requiring Approval

Before implementation, approve:

1. the exact RQ2 wording;
2. RQ2a/RQ2b as substudies rather than a new formal RQ3;
3. Qwen embedding as the RQ2a primary selector;
4. the selected frozen cross-encoder reranker;
5. the 20/80 cluster split;
6. same-facts-fielded, same-facts-flat, same-facts-prose, and same-facts-diluted as core matched controls;
7. the RQ2a field-aware adapter requirements and the development-only choice between maximum and uniform top-two aggregation;
8. downstream execution as secondary only;
9. graph/tree and external 80K neural reruns as optional/future work.

The RQ2b base-v1 corpus and parent B1/B2 protocol are frozen. B0F-A1 is exact-hash approved. The user-authorised B0G semantic audit is complete, but its base-v1 hard stops fail: 14 strict-gold rejections and eight prompts without a fully acceptable reviewed candidate. The focused remediation retains six labels and excludes eight prompts without creating an acceptable set, yielding the strict-gold-only v1.1 overlay. V3 then rebuilt and finalised 2,433 canonical I3C rows across 57 hash-bound chunks. Its automatic integrity freeze passes source hash, exact evidence, heading, identity, serialisation, root-coverage, duplicate, and scaffold checks; its one under-specified manual-QA attempt is quarantined and, by explicit user direction, not repeated. Therefore the corpus is eligible only for deterministic-integrity claims, not independent semantic-completeness claims. B1L, B1E-Q, and B1E-SR each contain 1,524 post-run-verified strict rankings. Both frozen B2 rerankers then completed 4,572 strict rows over the same persisted B1 Top-20 lists and passed local integrity verification. This authorises neither an acceptable-set endpoint nor thesis result writing: the next gates are the registered RQ2b statistical/cost synthesis and user result review.

## 28. Bottom-Line Assessment

This RQ2 is strong enough for an ambitious honours thesis because it asks a clear mechanism question and validates the answer in a practical retrieval pipeline. Its novelty is diagnostic rather than architectural: it does not invent the first structured skill schema or router, but it can show which part of the observed benefit comes from operational content, explicit organisation, reduced dilution, candidate recall, or reranking.

RQ2a is complete through untouched confirmatory scoring, frozen analysis, cost accounting, user review, and thesis integration. Its bounded result is that operational facts matter consistently, while literal field organisation and explicit field-wise use interact with selector architecture and field type. RQ2b B0F, B0F-A1, B0G-M, the v1.1 strict-contract seal, V3 automatic integrity freeze, all three B1 retrievers, and both B2 rerankers are complete; base-v1 acceptable endpoints remain blocked and the v1.1 overlay is strict-gold-only. The completed B2 matrix is descriptive pending synthesis and user review, with I2-original strongest in every current reranked first-stage family rather than I3C. The next implementation work is paired statistical analysis, cost synthesis, and failure analysis before any thesis integration. V3 extraction cannot be claimed independently semantic-QA-complete.
