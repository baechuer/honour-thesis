# RQ1 Public Original Round 3 Clean-Only Scoring Freeze and Test SOP

<!-- RQ1-RECORD-STATUS:START -->
> **RQ1 record status (2026-09-04): `CURRENT_CANONICAL`.** Current single-field public-original experiment protocol and scoring boundary. Canonical index: `thesis_notes/current/RQ1/README.md`.
<!-- RQ1-RECORD-STATUS:END -->



Date: 2026-09-04  
Status: `F1--F3 EXECUTED AND VALIDATED / USER RESULT REVIEW REQUIRED / NO THESIS PDF WRITE`

## Question and Scope

This is the source-based, naturalistic part of RQ1. It asks a deliberately
narrow question: when a documented information field is completely removed
from otherwise identical public skill documents, does within-composition skill
routing become weaker?

The experiment begins with the verified original documents. For each
composition and one target field, the `FULL_ORIGINAL` condition uses the exact
source packet, while `REMOVE_<FIELD>_R3` uses the corresponding Round-3 forced
mask. The latter may be incomplete or non-executable. That is allowed here:
the intervention tests selection information, not whether an artificially
edited skill still runs.

This is not a whole-library stress test, a representation comparison, a
reranker study, or a claim that all public skills expose the seven fields in a
separable way. Those belong to RQ2 or to the stated feasibility boundary.

## Frozen Inputs

The clean-only scoring freeze is built only from these existing, immutable
inputs:

1. The 82-composition, 265-document original-source registry at
   `skill_benchmark/rq1_public_original_removal_v3_82_registry/`.
2. The Round-3 mask manifest at
   `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/forced_round3_masks/FORCED_ROUND3_MASK_MANIFEST.json`.
3. The canonical Round-3 blind-clearance records at
   `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/forced_round3_clearance/canonical_round3/`.
4. The previously frozen strict prompt/gold roster at
   `skill_benchmark/rq1b_cross_source_public_benchmark/working/masked_execution/p0_master_roster_2026-08-28.json`.

No source document, target span, prompt, gold label, candidate order, or
clearance decision may be changed after the freeze. The freeze builder writes
their exact SHA-256 hashes and a separate exclusion ledger. It is not a
selector and produces no retrieval score.

## Clean-Only Eligibility Rule

The primary denominator is field-specific. A scoring case is included only
when all of the following hold:

1. The composition contains a complete three- or four-candidate source set.
2. Every original candidate file still matches its frozen source SHA-256.
3. Every Round-3 masked candidate file still matches its frozen Round-3
   SHA-256.
4. The canonical Round-3 record marks **every** candidate in that
   composition-field unit as `CLEAR`.
5. The candidate set can be bound deterministically to a frozen strict routing
   family with one singleton gold skill.
6. That family has exactly one frozen `direct` prompt and one frozen
   `paraphrase` prompt, both targeting the same gold skill.

`RESIDUAL` and `UNCERTAIN` units are retained in the exclusion ledger and
reported as overlap/feasibility evidence. They are never silently treated as
clean, and they are never mixed into the primary denominator. A failure to
enter the denominator does not mean that a field has no routing value.

Primary results retain each field's own eligible denominator. A separate
all-seven-fields-complete subset may be reported only as a labelled
cross-field sensitivity analysis; it must not replace the field-specific
primary results.

## Conditions and Test Unit

For each eligible `composition x routing family x target field` case, score
the same candidate set twice:

| Condition | Candidate text |
| --- | --- |
| `FULL_ORIGINAL` | Exact hash-verified public original for every candidate. |
| `REMOVE_<FIELD>_R3` | Exact hash-verified Round-3 mask for every candidate. |

Each case has a frozen singleton gold label and two repeated prompt variants:
`direct` and `paraphrase`. A prompt variant is not an independent composition:
within a composition-family it is a repeated measurement. Candidate ordering
and deterministic tie breaking are held fixed across the two conditions.

No joint/group mask enters this primary run. Such a condition would need its
own materialisation, fresh clearance, and freeze rather than being assembled
after seeing single-field results.

## Execution Order

### F0. Freeze and validation

1. Build the machine-readable clean-only freeze and exclusion ledger.
2. Independently verify all listed source and mask hashes, clearance statuses,
   candidate labels, prompt variants, and gold-label bindings.
3. Record the actual eligible case count for each field before scoring.

If a field has fewer than 30 eligible composition-family cases (60 prompt
rows), it remains descriptive/feasibility evidence rather than a primary
field result. This threshold is declared before selectors run.

### F1. Local BM25

Run the frozen `FULL_ORIGINAL` and `REMOVE_<FIELD>_R3` cases locally. BM25
scores only candidates within the same frozen composition and uses identical
preprocessing and deterministic label tie breaking in both conditions. It is
the lexical retrieval check; it sends no data externally.

### F2. Qwen dense-retrieval preflight

After local BM25, construct an exact payload inventory for `text-embedding-v4`:
document/query hashes, cache hits, new outbound texts, request count, token
estimate, endpoint, dimensions, and no-retry rule. Constructing the inventory
does not transmit text.

The user must explicitly authorise the exact new payload before any candidate
or prompt text is sent to DashScope. Cached embeddings may be reused only when
the content hash, model, dimensions, and preprocessing identity match exactly.
There is no query rewriting and no reranking in this RQ1 primary test: both
would add another model layer that could conceal or recreate a first-stage
field signal. Reranker and representation comparisons are RQ2 work.

### F3. Analysis

For each field, pair `FULL_ORIGINAL` with `REMOVE_<FIELD>_R3` within the same
composition-family-prompt row. First average direct/paraphrase measurements
within each composition-family. Then average a composition's eligible
families, giving each composition one equal-weight primary contribution. Use a
composition-clustered paired bootstrap (10,000 resamples) for confidence
intervals, resampling whole compositions and retaining their internal family
structure. Thus prompt variants and compositions with several routing
families do not inflate the apparent sample size.

No result enters thesis LaTex/PDF until the user has reviewed the frozen
result package.

## Metrics

Primary metric:

- **Paired Hit@1 change**: `Hit@1(FULL_ORIGINAL) - Hit@1(REMOVE_<FIELD>_R3)`.
  A positive value means that removing the cleanly isolated field made the
  strict gold less likely to rank first under the same prompt and candidates.

Secondary diagnostics:

- MRR over the complete three- or four-candidate set;
- gold rank;
- native gold score and the leading-negative score;
- gold-vs-leading-negative native margin;
- `full-correct -> removed-wrong` winner transitions;
- direct and paraphrase slices;
- text length, token proxy, cache state, and runtime/cost ledger.

The native score and margin are interpreted only within one retriever. BM25
and dense cosine scores are not put on a common numeric scale. Recall@k is not
a primary RQ1 metric because every strict routing family has one gold skill and
a deliberately small candidate set; Top-1, rank and margin directly address
the routing question.

## What a Result Can Establish

A positive paired effect on a clean-only field-specific denominator supports a
modest claim: the removed, documented field carried useful routing information
for these public-source compositions under the tested retriever.

It does not establish that the field is the only reason the original skill was
selected, that every real skill library makes the field separable, that the
masked skill remains runnable, or that another retriever will show the same
effect. A null or weak effect likewise does not show that the field is useless:
other information in a real document can still identify the skill, and the
exclusion ledger makes that overlap explicit.

## Stop Rules

- A hash, lineage, clearance, candidate-order, prompt-pair, or singleton-gold
  mismatch blocks the affected case; it is placed in the exclusion ledger.
- A `RESIDUAL` or `UNCERTAIN` candidate blocks the full composition-field unit.
- Do not repair prompts, labels, masks, or candidate documents after the
  freeze to improve a result.
- Do not combine field denominators, group masks, historical derivative-card
  results, or RQ2 numbers with this primary result.

## Evidence Produced by F0

`skill_benchmark/rq1_public_original_exhaustive_ablation_v1/round3_clean_only_scoring_freeze/`

- `clean_only_scoring_freeze_v1.json`
- `eligibility_exclusions.json`
- `freeze_summary.json`
- `SHA256SUMS`

The local-only F1 runner is
`skill_benchmark/scripts/run_rq1_public_original_round3_clean_bm25.mjs`. Its
synthetic tie-break self-test and real-freeze dry run must pass before the
first result-producing invocation.

The freeze is valid only when its companion validator passes with zero
identity, hash, clearance, prompt-pair, and duplicate-case failures.

## Execution Record: F1--F3 (2026-09-04)

The frozen frame was executed without changing any input, prompt, candidate
order, gold label, field mask or eligibility decision.

### F1: local BM25

The local BM25 twin completed 4,312 ranking rows. Its result and paired
analysis validators passed; the result SHA-256 is
`010fee2f8f548bcd22c08f2eb8b65bdece0850c2cce231fdad58f178967ee1d3`.

### F2/F3: Qwen dense-retrieval twin

The user explicitly authorised the sealed preflight payload SHA-256
`38a8bab9938f884390caae6c0c062aac7ff7d08510b7e380156cf7fa6dba16d2`.
The executed Qwen condition used DashScope international `text-embedding-v4`,
1024 dimensions, no query rewrite, no reranker and no automatic retry. It
embedded 1,510 unique candidate texts and 388 unique prompt texts (1,898
cache misses) in 190 successful calls. Provider-reported input usage was
2,394,292 tokens. All embeddings were persisted to the authorised local cache.
The 4,312 Qwen rows and its paired analysis passed separate local validator
scripts; this was technical validation, not independent human review;
the result SHA-256 is
`8c7f058106de376e92b6cd1381fdd0491fbbdb9836ab9b0a759d4efa36637f06`.

### Composition-level paired result summary

Each value is `Hit@1(FULL_ORIGINAL) - Hit@1(REMOVE_FIELD)` after averaging
direct/paraphrase within a routing family and families within a composition.
Intervals are 10,000-resample composition-clustered paired bootstrap 95% CIs.

| Field | Eligible compositions | BM25 delta [95% CI] | Qwen delta [95% CI] |
| --- | ---: | --- | --- |
| Use condition | 57 | +0.114 [+0.067, +0.167] | +0.058 [+0.031, +0.092] |
| Input/precondition | 53 | +0.098 [+0.051, +0.149] | +0.016 [-0.017, +0.052] |
| Output/artifact | 49 | +0.122 [+0.065, +0.187] | +0.003 [-0.036, +0.036] |
| Workflow/procedure | 63 | +0.151 [+0.086, +0.215] | +0.040 [-0.024, +0.100] |
| Success/verification | 59 | +0.117 [+0.059, +0.182] | +0.027 [+0.005, +0.054] |
| Boundary/not-for | 69 | +0.024 [-0.014, +0.064] | -0.022 [-0.054, +0.008] |
| Dependency/resource | 52 | +0.091 [+0.046, +0.139] | +0.013 [-0.048, +0.067] |

The conservative cross-retriever reading is that use condition and
success/verification have stable positive Top-1 evidence under both tested
first-stage retrievers. The other four positive BM25 results are
retriever-conditional; Qwen's intervals include zero. Boundary/not-for is not
a stable positive Top-1 result in either twin. Native score margins are kept
only within retriever and are not compared numerically across BM25 and cosine
similarity.

The twin synthesis and transition-based failure interpretation are stored in
`skill_benchmark/rq1_public_original_exhaustive_ablation_v1/round3_clean_only_twin_synthesis/`.
No result has been added to thesis LaTeX or PDF pending user review.
