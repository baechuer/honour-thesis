# Comprehensive Thesis Claim And Readiness Review

Date: 2026-08-30  
Status: `READ-ONLY REVIEW / NO SCIENTIFIC INPUT, RESULT, OR THESIS TEXT CHANGED`

## Purpose

This review reconciles the current thesis PDF, current trackers, frozen RQ1/RQ2
artifacts, and two independent Sol reviews. It is a claim-and-readiness audit,
not a new experiment or an authorisation to rerun anything.

The current state requires one important correction of language: RQ2a and RQ2b
have already been executed, analysed, and integrated into the PDF. The next
task is therefore not to start a fresh RQ2 run. It is to complete a
retrospective validity and reporting consolidation before presenting either RQ2
study as final thesis evidence or proposing a new extension.

## Authoritative Evidence Layers

| Layer | Current evidence | What it supports | What it does not support |
| --- | --- | --- | --- |
| RQ1a | 350 researcher-authored, mechanically checked, author-reviewed controlled units; seven field-isolation suites | A tested field can be sufficient to break an otherwise tied three-sibling decision | Public-population field prevalence, independent human validation, or an unconditional field-importance ranking |
| RQ1b | 1,099-artifact source-discovery frame; 46 scored source-grounded derivative-card compositions, 99 strict families, 198 prompts | In this frozen public-card sample, individual-field removal has no statistically reliable Top-1/MRR effect while evidence may be redundant or joint | A native unedited-public-document ablation, prevalence in all public skills, or end-to-end routing/task success |
| RQ2a | Fixed-content 70-cluster development and 280-cluster untouched confirmatory split; 600 prompts and 22 conditions | How organisation and field-wise scoring affect selection when propositions and candidates are held fixed | Independent validation of the RQ1 construct or full-library candidate recall |
| RQ2b | 2,433-skill source-grounded library; 381 strict-gold prompts; B1 candidate generation and fixed-Top-20 B2 reranking | Strict-label retrieval, candidate inclusion, fixed-list reranking, and recorded selector-surface/index trade-offs in this benchmark | Unique task correctness, acceptable-alternative performance, independent semantic completeness of I3C, complete I3 extraction cost, or a universal I3C advantage |

## What Is Strong

1. The core reasoning sequence is coherent when stated as four evidence layers:
   controlled field sufficiency, public-card field availability, matched-content
   selector mechanism, and full-library pipeline trade-offs.
2. RQ1a has an unusually clear causal contrast: all non-target facts are held
   fixed and the target field changes. Cluster-level bootstrap intervals respect
   paired prompt variants rather than treating them as independent tasks.
3. RQ1b does not promote directional public-card effects as a positive
   individual-field claim. Its non-reliable single-field result is a useful
   qualification of RQ1a, not a failure to be hidden.
4. RQ2a is the strongest confirmatory component. It separates proposition
   content from headings, prose form, order, dilution, and a frozen field-aware
   aggregation rule. The negative primary result is informative: headings are
   not an inherent benefit to pooled Qwen vectors.
5. RQ2b separates B1 candidate inclusion from B2 ordering. It also records the
   crucial accuracy--selector-surface/index-burden trade-off rather than
   claiming a universal I3C accuracy gain.

## Verified Corrections Required Before Final Thesis Presentation

### 1. Correct RQ2b row counts

The frozen contract defines three B1 retrievers, four representations, and 381
strict prompts:

- total B1 result rows: `3 x 4 x 381 = 4,572`;
- per-retriever B1 submatrix: `4 x 381 = 1,524` rows;
- total B2 result rows: `2 x 4,572 = 9,144`;
- per-reranker B2 submatrix: `4,572` rows.

Current thesis wording that presents `1,524` as the whole first-stage total and
`4,572` as the whole reranked total is inaccurate. It must say whether it is
describing a per-retriever/per-reranker submatrix or the complete crossed
matrix. Source: `skill_benchmark/rq2b_full_library/rq2b-full-library-v1.1-2026-08-15/v11_strict_endpoint_contract.json`.

### 2. Correct the Recall@20 sentence

The current Results prose says I2 is higher than I3C in every Recall@20 row
except controlled SkillRouter. The table directly below shows I2 `0.980` and
I3C `0.974` for that row. The accurate statement is that I2 is higher in all
six reported Recall@20 rows.

### 3. Nominate one canonical RQ1b result package

Two packages use final-looking names:

- `field_type_ablation_confirmatory_v2_v3_final_2026-08-30/`;
- `field_type_ablation_final_result_ledger_2026-08-30/`.

They agree on the primary 46-composition/99-family/198-prompt design and its
bounded individual-field conclusion, but their supporting bootstrap/joint-group
reporting is not byte-identical. The final thesis needs one canonical manifest,
seed, estimator, and claim ledger. The other package should be labelled as a
supplementary analysis or superseded record, not another final endpoint.

### 4. Make automatic-I3 and strict-label limits prominent

RQ2b is a comparison of automatic, source-grounded I3 extraction under a
strict-label endpoint. Manual semantic completeness of I3C was waived and the
acceptable-set endpoint remains blocked. The thesis must not infer that a field
with sparse retained spans has little routing value, nor that strict-label
Hit@1 is unique task correctness. The extraction asymmetry belongs in the
abstract-level RQ2b limitation, not only the tracker.

## Framing Repairs Needed

### RQ1 claim boundary

Use this thesis-level answer:

> Within researcher-authored controlled near-neighbour units, each tested
> operational field can be sufficient to resolve an otherwise tied decision,
> with performance varying by field, prompt form, and selector. In selected
> source-grounded derivative cards, no individual-field Top-1 or MRR effect was
> statistically reliable; operational evidence was often distributed across
> fields.

Do not turn the RQ1a field order into a natural-library importance ranking.
RQ1a author review is real researcher review but is not independent or blind
annotation. Independent de-identified review would strengthen the thesis, but
is an optional evidence upgrade rather than a reason to silently reopen frozen
RQ2 results.

### RQ1b name

The accurate label is **source-grounded derivative-card field-availability
study** or **source-grounded derivative-card field ablation**. Avoid calling it
a native public-artifact replication or a test on unedited public skill
documents.

### RQ2a interpretation

The `shared-only` condition is intentionally byte-identical across candidates.
Its large fielded lift validates tie handling and selector usability under the
constructed contrast. It is not an independent external replication of RQ1.
`Confirmatory` should describe the frozen 70/280 split and planned selector
comparison, not claim independent semantic validation of the author-designed
clusters.

### RQ2b cost interpretation

The defensible wording is **strict-label accuracy versus selector-visible
surface and measured document/index burden**. It is not a full lifecycle cost
comparison because the durable I3 extraction time/invoice is unavailable.
Also report B2 reranking cost/latency separately if these values are available
in the ledger; do not let the B1 cost table imply that it covers reranking.

## Literature And Novelty Repairs

The novelty is incremental but defensible. Do not claim the first structured
skill schema, the first metadata-versus-body study, or the first large-scale
retrieve-then-rerank pipeline. Closest work already includes structured skill
representations, metadata/full-body comparisons, large-skill retrieval, and
retrieval-to-execution decomposition.

State the contribution instead as:

> The thesis contributes candidate-synchronous field isolation and
> matched-content experiments that separate operational content, field
> labelling, selector architecture, candidate inclusion, and recorded retrieval
> cost under semantically confusable skill choices.

Required literature repairs:

1. Treat SkillsBench as evidence about task-specific skill exposure and
   conflicting documentation, not as a large-library scale experiment.
2. Do not attribute broad-wrapper prevalence or authoring-style claims to a
   citation unless its primary text directly establishes them. Present such
   observations as corpus observations where applicable.
3. Add or more clearly use methods literature for lexical/dense/cross-encoder
   retrieval, annotation/graded relevance, paired cluster inference, and
   multiplicity. The current review is strong on adjacent skill systems but
   thinner on the methodological basis of its evaluation choices.

## Structural Repairs

The main narrative should be organised around the four evidence layers above.
The historical R1--R4/M0--M8 taxonomy, M4 tree, M5 graph, M6 prototypes,
historical frozen-v0.4 matrices, and external portability records should move
to an appendix or a short historical-method note. They are valuable
reproducibility context but currently obscure the completed thesis answer.

Also fix the small Introduction defects:

- it says four contributions but lists five;
- it says Results contains "current and planned results" even though the core
  thesis-facing studies are now complete;
- use `skill artifact` only for a stored package; use `skill document` or
  `full-body representation` when the experiment used only `SKILL.md` text.

## Readiness Decision

`RQ1 editorial closure: NOT YET COMPLETE.` The experiments need not be rerun,
but the canonical RQ1b package, final wording, and thesis structure must be
resolved.

`RQ2 execution: ALREADY COMPLETE.` No fresh core RQ2 experiment should start
until the reporting/validity consolidation above is completed. Any further
field-aware, graph/tree, acceptable-alternative, or downstream study is a new,
clearly labelled extension, not a repair to frozen RQ2a/RQ2b results.

## Recommended Order Of Work

1. Select and record the canonical RQ1b primary package and correct the three
   numerical/wording errors.
2. Rewrite the RQ1/RQ2 claim paragraphs using the boundaries above.
3. Restructure the thesis so core evidence is distinct from historical work.
4. Repair literature novelty and citation scope.
5. Decide whether to add an independent/de-identified review of RQ1a. If not,
   retain the explicit author-review limitation and do not overclaim.
6. Only then decide whether an RQ2 extension is scientifically worthwhile.

## Review Provenance

Two read-only independent Sol reviews were completed and closed on 2026-08-30:

- comprehensive examiner audit;
- literature/novelty and claim-support audit.

No external search, model/API call, result rewrite, or thesis PDF edit occurred
as part of this review.
