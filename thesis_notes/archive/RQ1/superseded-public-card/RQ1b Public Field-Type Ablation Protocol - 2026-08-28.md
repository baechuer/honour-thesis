# RQ1b Public Field-Type Ablation Protocol

<!-- RQ1-RECORD-STATUS:START -->
> **RQ1 record status (2026-09-04): `HISTORICAL_OR_SUPERSEDED`.** Retained for provenance and method history. Do not use its dated status, denominator, or result as the current RQ1 claim unless the canonical RQ1 index explicitly carries it forward. Canonical index: `thesis_notes/current/RQ1/README.md`.
<!-- RQ1-RECORD-STATUS:END -->



Status: `V2 SELECTOR RUNS COMPLETE / LOCAL AUDITS PASS / USER REVIEW PENDING / NO THESIS WRITE`

Date: 2026-08-28

> **2026-08-30 final-registry amendment.** The V2 public-card experiment is
> finalised as the scored RQ1b stratum in
> `skill_benchmark/rq1b_final_public_corpus_v1/`: 48 active canonical-card
> compositions, 128 materialised routing families, and 87 strict-preserved
> families scored over 174 prompts. The registry also records historical C6
> source provenance and the separate direct V3 C6 curation records, but neither
> is pooled with V2 metrics. Its 82-composition source-hash union is therefore
> an inventory rather than an RQ1b score denominator.

> **2026-08-30 V2+V3 complete-triad integration amendment.** Four direct V3
> parent triads passed a local compatibility audit against the V2 seven-field,
> strict-target and direct/paraphrase contract. They are materialised as a
> separate prospective extension: 52 candidate compositions, 99 strict routing
> families and 198 prompts. Two V3 partial triads remain quarantined. This does
> not change or pool the completed V2 results; later scoring must separately
> report native V2, imported V3 and the harmonised extension. Full SOP:
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b V2 Plus V3 Complete-Triad Integration Amendment - 2026-08-30.md`.

## 1. Purpose And Claim Boundary

RQ1 asks:

> Which operational information types help distinguish semantically similar
> but procedurally distinct agent skills?

RQ1a answers the controlled part of that question: one field is varied among
otherwise shared sibling skills. RQ1b tests the complementary public-artifact
setting. It does not try to identify one uniquely decisive field in a naturally
authored document. Natural skills commonly express related operational facts
jointly in use conditions, inputs, outputs, workflows, boundaries, resources,
and verification text.

The RQ1b intervention is a **field-type availability ablation** on a
source-grounded field-card representation. For a strict public candidate
cluster, it asks whether withholding one field type from every candidate card
changes the gold skill's separation from its closest incorrect neighbour.

RQ1b can support this bounded conclusion:

> In a source-grounded operational field-card representation of strict public
> skill clusters, making information type `f` unavailable changes, preserves,
> or improves gold-versus-neighbour routing separation by the reported amount.

It cannot establish a universal effect for unedited full public documents, a
unique human decision rationale, an effect for every skill library, or an RQ2
representation/retrieval-pipeline result.

## 2. Relation To Earlier RQ1b Work

| Record | Role | Status |
|---|---|---|
| RQ1b-N | Untouched public `SKILL.original.md` strict-routing corpus and source evidence. | Retained as the natural-artifact frame and strict-label source. |
| Primary-field field-card pilot | Tried to transfer a raw-document primary-field lock into a field card before winner-only target/sham masking. | Stopped. It preserved strict gold selection but not old field attribution. It is not a selector result. |
| This protocol | All-candidate, one-field-type-at-a-time availability ablation on source-grounded field cards. | Six-family pilot passed; source-card construction and pre-review surface-cue remediation are complete. The active freeze has 48 compositions, 128 routing families and 256 prompt variants; full-card preservation is pending. |

The stopped pilot remains at:

- `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_card_pilot_2026-08-28/RQ1B_S_FIELD_CARD_PILOT_CHECKPOINT_2026-08-28.md`

It must not be relabelled as a failed field-value result. Its only consequence
is that this protocol does not require, collect, or use a primary-field label.
The earlier raw-full-document masking workflow remains a feasibility audit, not
an RQ1b outcome or a gate for this protocol.

## 3. Frozen Experimental Units

RQ1b has two linked units, kept separate to prevent different cards from being
constructed for the same library candidate set:

- A **candidate composition** is one unordered set of three or four
  hash-verified original public skill artifacts. It is the representation unit:
  exactly one pair of independent source-card builders creates the shared cards
  and all eight conditions for that composition.
- A **routing family** is one candidate composition plus one strict gold skill
  and its direct/paraphrase prompt pair. It is the evaluation unit: the shared
  cards are reviewed and later scored separately for each sealed prompt pair.

Each routing family has:

- three or four hash-verified original public `SKILL.original.md` artifacts;
- a frozen strict gold skill;
- a direct prompt and a meaning-preserving paraphrase prompt; and
- a candidate set whose membership, source hashes, prompt text, strict label,
  and cue-risk record are fixed before card construction or scoring.

Before any pilot or score, a dedicated RQ1b input manifest must derive the
exact cluster and prompt identities from the live C6 roster. Historical prose
counts are not an input contract. The manifest is the only source of truth for
the scored population, exclusions, and per-field coverage denominators.

Only strict-singleton routing families enter the primary analysis. Existing multi-adequate
or unresolved packets remain exploratory material and are not converted into
strict labels.

The frozen P0 roster has 209 composition-plus-gold groups over 76 candidate
compositions. After six pilot-family and ten incomplete-pair exclusions, the
non-pilot input has 193 paired routing families over 74 unique candidate
compositions. These are not 193 independent libraries; reporting retains
composition/candidate reuse and uses a routing-family or composition-aware
aggregate as specified before scoring.

## 4. Source-Grounded Field Cards

Every candidate composition uses this fixed card order:

```text
USE CONDITION
INPUT / PRECONDITION
OUTPUT / ARTIFACT
WORKFLOW / PROCEDURE
SUCCESS / VERIFICATION
BOUNDARY / NOT FOR
DEPENDENCY / RESOURCE
```

Each non-marker value is an exact contiguous excerpt from that candidate's
hash-verified original source. Cards omit titles, skill IDs, repository names,
URLs, provenance, and newly written summaries. `NOT_STATED` is allowed only
when source-only review finds no evidence for that slot.

### 4.1 Construction And Canonicalisation

1. Two independent builders receive only one anonymous candidate-composition
   source packet. They do not
   receive prompts, strict labels, source provenance, other cards, masks,
   selectors, or results.
2. Each builder may locally validate only its own card against its assigned
   sources for exact-substring and schema correctness.
3. A source-only auditor validates literal evidence, disallowed surface cues,
   and slot completeness independently of both builder responses.
4. Before prompts or labels are unsealed, the coordinator applies the
   pre-recorded builder-order rule: retain the first literal-valid complete
   builder card; use the second only if the first is invalid. The retained
   card, source hashes, and audit are then frozen.

This produces one reproducible derivative representation per candidate
composition. It does not claim that
a source sentence belongs uniquely to one conceptual information type.

### 4.2 Baseline Route Preservation

Two independent blinded, selection-only reviewers receive an anonymous shared
full field-card composition and one frozen routing-family prompt. They select the unique fully adequate
candidate or record `MULTIPLE_ADEQUATE` / `NONE_ADEQUATE`. They are not asked
which field is decisive and do not see gold labels, sources, provenance, masks,
selectors, or results.

### 4.3 Pre-Review Surface-Cue Integrity Amendment (2026-08-29)

Before any blinded selection or residual review, the opaque-packet verifier was
strengthened to reject source-locating surface artifacts in card excerpts:
URLs, markdown link targets, local `SKILL.md` / `README.md` references, and
copied markdown heading blocks. This is an integrity amendment, not a change to
the field definitions, candidate compositions, prompts, gold mapping, or later
analysis. Product and domain names that are operational content are not removed
merely because they are named.

The strengthened preflight found a non-empty remediation set. Each affected
composition is processed before any review as follows:

1. Two independent source-only repair builders receive the anonymous candidate
   sources and the flagged candidate-slot locations, but never prompts, gold
   labels, provenance, masks, selectors, or previous review results. For every
   flagged location, each returns either a complete replacement with one or
   more exact contiguous source excerpts or `NO_SAFE_ALTERNATIVE`.
2. The source-only auditor verifies source contiguity, the same cue exclusion,
   candidate/slot completeness, and that all unflagged canonical values remain
   byte-identical. The original builder-order rule applies: retain the first
   complete literal-valid repair; use the second only if the first fails.
3. If neither repair is complete and literal-valid, strictly exclude the whole
   composition rather than editing, paraphrasing, or treating a known source
   value as `NOT_STATED`.
4. After all outcomes are recorded, regenerate the opaque selection and
   residual packets and their private maps from the repaired/excluded canonical
   cards; retain the former packet artifacts as quarantined pre-amendment
   construction material. Re-run binding audit and write a new input freeze
   that includes the canonical card bytes and opaque packets before dispatch.

The surface-cue amendment was frozen before blinded FULL-card dispatch. The
subsequent preservation reviews are a separate eligibility gate: their records
do not become routing, mask-effect, retrieval, embedding, or selector results.

A cluster is eligible for scoring only when both reviewers select the sealed
strict gold for both direct and paraphrase prompts. These are model-assisted
blind reviews unless a separate human study is later approved. They must never
be described as human annotation.

### 4.4 Non-Pilot Construction Completion And Active Freeze (2026-08-29)

The upstream C6 roster contained 74 non-pilot candidate compositions and 193
paired routing families. Literal source-card construction materialised 58
compositions and excluded 16 before any review. The strengthened surface-cue
audit then flagged 20 of those 58: 10 received complete, literal-safe,
same-slot repairs and 10 were strictly excluded. The active frozen input set
therefore contains 48 candidate compositions, 128 routing families, and 256
direct/paraphrase prompt variants. It includes 95 triads and 33 quartets.

The amended freeze verifies 38 byte-identical unmodified cards and 10 repaired
cards. It contains 128 opaque selection packets and 48 opaque residual packets
(994 candidate-slot targets). The per-field pre-preservation eligibility counts
are use condition 115, input/precondition 119, output/artifact 125,
workflow/procedure 126, success/verification 109, boundary/not-for 111, and
dependency/resource 115. Before any selector work, every family must pass the
two-reviewer FULL-card preservation gate.

Construction evidence and the active freeze are recorded at:

- `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_SURFACE_CUE_AMENDMENT_COMPLETION_2026-08-29.md`
- `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/opaque_review_input_freeze_amendment_2026-08-29.json`

These counts are not accuracy, semantic-fidelity, mask-effect, embedding, or
retrieval results. They only define the source-grounded population that may
proceed to the two-reviewer full-card preservation gate.

### 4.5 FULL-Card Preservation Wave 001 (2026-08-29)

The first 18 packets were dispatched in private-map order, independently read
twice, schema/evidence audited, and compared against the sealed gold. Six
families (`CFTF-007`, `CFTF-010`, `CFTF-019`, `CFTF-020`, `CFTF-025`, and
`CFTF-026`) passed both direct and paraphrase prompts. Twelve did not: nine had
two `NONE_ADEQUATE` reviews, two had a `NONE_ADEQUATE`/singleton disagreement,
and one was consistently multi-adequate. Failed families are excluded from
scoring rather than relabelled or repaired. Because this batch follows packet
order rather than a sampling plan, `6/18` is not a population rate or a
scientific result. Detailed evidence is checkpointed at
`skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_FULL_CARD_PRESERVATION_WAVE_001_CHECKPOINT_2026-08-29.md`.

### 4.6 FULL-Card Preservation Wave 002 (2026-08-29)

The next 18 packet-ordered families were independently reviewed twice under
the same opaque-packet isolation rule. Thirteen passed; three had
`NONE_ADEQUATE`/sealed-singleton reviewer disagreement, one lost preservation
for the paraphrase wording, and one received two `NONE_ADEQUATE` reviews. The
cumulative gate status is therefore 36 adjudicated, 19 strict-preserved, 17
excluded and 92 pending. These are validity-gate counts, not a pass-rate
estimate, a selector metric, or a field effect. See
`skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_FULL_CARD_PRESERVATION_WAVE_002_CHECKPOINT_2026-08-29.md`.

### 4.7 FULL-Card Preservation Wave 003 (2026-08-29)

Eighteen further packets yielded 12 passes and six exclusions: one lost
preservation for one prompt wording, one was consistently multi-adequate, two
had paired `NONE_ADEQUATE` reviews, and two had reviewer disagreement. Four
initial response files failed only mechanical exact-evidence validation and
were superseded by independent valid replacement reviews while retained as
audit history. The cumulative gate status is 54 adjudicated, 31
strict-preserved, 23 excluded and 74 pending. These counts remain eligibility
control, not an RQ1 effect or a model-performance estimate. Evidence:
`skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_FULL_CARD_PRESERVATION_WAVE_003_CHECKPOINT_2026-08-29.md`.

### 4.8 FULL-Card Preservation Wave 004 (2026-08-29)

Seventeen packets had valid two-reviewer records: 14 passed, two had paired
`NONE_ADEQUATE` reviews, and one had reviewer disagreement. A separate family,
`CFTF-099`, remains `UNADJUDICATED_FORMAT_HOLD` after three independent A-side
responses each failed the mechanical exact-substring audit; it has no B review
or sealed-label decision. Cumulatively, 71 families are adjudicated (45
strict-preserved and 26 excluded), one is held, and 56 have not yet been
dispatched. These remain eligibility counts, not a selector or field-effect
result. Evidence:
`skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_FULL_CARD_PRESERVATION_WAVE_004_CHECKPOINT_2026-08-29.md`.

### 4.9 FULL-Card Preservation Wave 005 (2026-08-29)

The next 18 packets yielded 15 strict-preserved families and three exclusions:
one reviewer disagreement, one paired `NONE_ADEQUATE` case, and one prompt or
review non-preservation case. The cumulative state is 89 adjudicated, 60
strict-preserved, 29 excluded, 38 undispatched and one separate format hold.
These are gate counts only, not a retrieval or field-effect result. Evidence:
`skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_FULL_CARD_PRESERVATION_WAVE_005_CHECKPOINT_2026-08-29.md`.

### 4.10 FULL-Card Preservation Wave 006 (2026-08-29)

The next 18 packets produced 13 strict-preserved families and five exclusions.
The cumulative state is 107 adjudicated, 73 strict-preserved, 34 excluded, 20
undispatched, and the separately retained `CFTF-099` format hold. These counts
are only pre-scoring validity control. Evidence:
`skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_FULL_CARD_PRESERVATION_WAVE_006_CHECKPOINT_2026-08-29.md`.

### 4.11 FULL-Card Preservation Wave 007 (2026-08-29)

Eighteen packets added 12 strict-preserved families and six exclusions. Ten
A-side and four B-side initial response files failed only the exact-card-
substring mechanics audit and were replaced independently before adjudication;
the invalid payloads remain audit history. The cumulative state is 125
adjudicated, 85 strict-preserved, 40 excluded, two undispatched, and the
separately retained `CFTF-099` format hold. This is pre-scoring eligibility
control, not selector, retrieval or field-effect evidence. Checkpoint:
`skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_FULL_CARD_PRESERVATION_WAVE_007_CHECKPOINT_2026-08-29.md`.

### 4.12 FULL-Card Preservation Completion (2026-08-29)

The 128 active selection packets are now exhausted: 87 strict singleton
preservations, 40 strict exclusions, and the separate `CFTF-099`
`UNADJUDICATED_FORMAT_HOLD`. The completion audit verifies every adjudicated
ledger's response/audit hash chain, all selection and residual packet bindings,
and post-preservation field coverage. The next local pre-scoring operation is
two-reviewer residual-redundancy classification; no selector score, embedding,
retrieval metric, API operation, or thesis result exists yet. Completion
evidence:
`skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_FULL_CARD_PRESERVATION_COMPLETION_CHECKPOINT_2026-08-29.md`.

### 4.13 Residual-Redundancy Wave 001 (2026-08-29)

Six source-card-only residual packets (124 candidate-field targets) completed
two independent review and local consensus binding: 58 `none`, 35 `partial`,
three `substantial`, and 28 retained `disagreed` labels. This characterises
cross-slot redundancy, not field contribution or model performance. Forty-two
frozen packets remain. Checkpoint:
`skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_RESIDUAL_REDUNDANCY_WAVE_001_CHECKPOINT_2026-08-29.md`.

### 4.14 Residual-Redundancy Wave 002 (2026-08-29)

Six further source-card-only packets covered 142 targets: 43 `none`, 54
`partial`, 14 `substantial`, and 31 retained disagreements. Twelve of 48
packets are now consensus-bound; this remains redundancy auditing only.
Checkpoint:
`skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_RESIDUAL_REDUNDANCY_WAVE_002_CHECKPOINT_2026-08-29.md`.

### 4.15 Residual-Redundancy Wave 003 (2026-08-29)

Six more source-card-only packets cover 117 targets (28 `none`, 44 `partial`,
19 `substantial`, 26 disagreements). Cumulative coverage is 18/48 packets and
383/994 targets; no selector or field-effect result exists. Checkpoint:
`skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_RESIDUAL_REDUNDANCY_WAVE_003_CHECKPOINT_2026-08-29.md`.

### 4.16 Residual-Redundancy Wave 004 (2026-08-29)

Six further source-card-only packets cover 123 targets: 26 `none`, 48
`partial`, 13 `substantial`, and 36 retained disagreements. Cumulative
coverage is 24/48 packets and 506/994 targets. Mechanically invalid review
payloads were independently replaced before consensus binding; these are
response-format history, not source-card, strict-gold, selector, or
field-effect evidence. Checkpoint:
`skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_RESIDUAL_REDUNDANCY_WAVE_004_CHECKPOINT_2026-08-29.md`.

### 4.17 Residual-Redundancy Wave 005 (2026-08-29)

Six source-card-only packets cover 113 targets: 47 `none`, 26 `partial`, nine
`substantial`, and 31 retained disagreements. Cumulative coverage is 30/48
packets and 619/994 targets. Mechanically invalid response-schema or
literal-quote payloads were retained and independently replaced before
consensus; these remain formatting history, not source-card, strict-gold,
selector, or field-effect evidence. Checkpoint:
`skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_RESIDUAL_REDUNDANCY_WAVE_005_CHECKPOINT_2026-08-29.md`.

### 4.18 Residual-Redundancy Wave 006 (2026-08-29)

Six source-card-only packets cover 120 targets: 54 `none`, 25 `partial`, 12
`substantial`, and 29 retained disagreements. Cumulative coverage is 36/48
packets and 739/994 targets, with 91 exact independent-review agreements in
this wave. Mechanically invalid response-schema or literal-quote payloads were
retained and independently replaced before consensus; they remain response
format history, not source-card, strict-gold, selector, or field-effect
evidence. Checkpoint:
`skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_RESIDUAL_REDUNDANCY_WAVE_006_CHECKPOINT_2026-08-29.md`.

### 4.19 Residual-Redundancy Wave 007 (2026-08-29)

Six source-card-only packets cover 128 targets: 83 `none`, 24 `partial`, eight
`substantial`, and 13 retained disagreements. Cumulative coverage is 42/48
packets and 867/994 targets, with 115 exact independent-review agreements in
this wave. Replaced payloads address mechanical response-schema or
literal-quote errors only; they are not source-card, strict-gold, selector, or
field-effect evidence. Checkpoint:
`skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_RESIDUAL_REDUNDANCY_WAVE_007_CHECKPOINT_2026-08-29.md`.

### 4.20 Residual-Redundancy Wave 008 (2026-08-29)

The final six source-card-only packets cover 127 targets: 52 `none`, 31
`partial`, 19 `substantial`, and 25 retained disagreements, with 102 exact
independent-review agreements. The completed ledger is 48/48 packets and
994/994 targets: 391 `none`, 287 `partial`, 97 `substantial`, and 219
disagreements (775 exact agreements). These labels are redundancy strata only,
not field effects or routing results. Checkpoint:
`skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_RESIDUAL_REDUNDANCY_WAVE_008_CHECKPOINT_2026-08-29.md`.

### 4.21 Local Pre-BM25 Gate (2026-08-29)

All local pre-scoring checks pass. The immutable original opaque-review core
still binds 128 selection packets and 48 residual packets. A separate
condition-materialisation freeze amendment locks the newly derived conditions
without rewriting the original review freeze. Conditions are derived only from
the 48 frozen-corpus canonical cards (not rebuilt from builder responses), and
all 48 pass the candidate-synchronous one-field mask audit. `CFTC-005` has a
canonical card but is not in the frozen opaque corpus; any pre-existing
untracked condition directory is excluded from eligibility and must never be
scored.

The valid primary strict subset is 87 preserved routing families; 40 failed
strict preservation and one is an unadjudicated response-format hold. Eligible
family counts are use 79, input 82, output 86, workflow 85, success 78,
boundary 79, and dependency 77. The next operation is local BM25 only, and is
blocked pending the user's explicit go-ahead. No BM25 score, retrieval metric,
embedding, external transfer, or thesis result exists. Checkpoint:
`skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_LOCAL_PRE_BM25_READINESS_CHECKPOINT_2026-08-29.md`.

### 4.22 Completed Selector Runs (2026-08-29)

The frozen v2 subset has now been scored by the two predeclared simple
first-stage selectors: local BM25 and the separately authorised Qwen
`text-embedding-v4` single-vector comparator. Both produced exactly 1,392
rows over the same 87 strict families, 174 prompt variants and eight
conditions. The Qwen run sent the authorised 1,246 raw card/prompt texts in
126 serial no-retry requests, persisted all embeddings locally, and passed the
post-run row, receipt, hash, strict-gold, ranking and denominator audit.

For Qwen, every all-eligible composition-bootstrap `FULL-MASK` Top-1 interval
crosses zero. The largest directional differences are boundary/not-for
`+0.015` (95% CI `[-0.035, 0.067]`) and output/artifact `-0.025`
(`[-0.071, 0.019]`), so neither is a stable main effect. The low-residual
input/precondition stratum is positive but descriptive only. Together with
BM25, this is evidence about availability and redundancy in combined public
field cards, not a universal field ranking or isolated causal attribution.
Complete results and exact execution provenance are at:
`skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_confirmatory_v2_qwen_2026-08-29/QWEN_RESULT_CHECKPOINT_2026-08-29.md`.

### 4.23 Prospective Joint Field-Set Extension (2026-08-29)

The v2 single-field results motivate, but do not determine, a separately
frozen v2.1 joint-mask extension. It has three predeclared coherent sets:
task specification (use, input and output), execution/verification (workflow
and success), and applicability/capability (boundary and dependency). It will
mask each complete set candidate-synchronously and score only the intersection
of its v2 field-eligible strict families. This tests joint non-redundant
availability under combined public cards; it cannot attribute a result to one
member field. Its protocol and independent execution gates are at
`thesis_notes/archive/RQ1/superseded-public-card/RQ1b Joint Field-Set Availability Amendment - 2026-08-29.md`.

### 4.24 Joint Extension Local Result And Qwen Gate (2026-08-29)

The joint-card freeze passed all source-v2 binding, all-candidate masking,
unchanged-slot and group-intersection checks. Local BM25 then produced 696
rows, zero network calls and a passed independent audit. The three directional
`FULL-MASK` Top-1 effects are task specification `+0.089` (95% CI
`[-0.005, 0.188]`), execution/verification `+0.035` (`[-0.022, 0.090]`) and
applicability/capability `+0.039` (`[-0.050, 0.143]`); all cross zero. A
cache-aware Qwen preflight finds that only 402 new joint-mask card texts need
external embedding. Qwen remains blocked until its exact new scope is
authorised. Checkpoints:
`skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_joint_mask_v21_bm25_2026-08-29/BM25_RESULT_CHECKPOINT_2026-08-29.md` and
`skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_joint_mask_v21_qwen_preflight_2026-08-29/QWEN_PREFLIGHT_CHECKPOINT_2026-08-29.md`.

## 5. Field-Type Availability Conditions

For every eligible routing-family prompt, the same composition's candidate cards appear in eight
conditions:

| Condition | Intervention |
|---|---|
| `FULL` | No change to the frozen source-grounded cards. |
| `MASK_USE` | Replace the value under `USE CONDITION` in every candidate card with the same marker. |
| `MASK_INPUT` | Replace the value under `INPUT / PRECONDITION` in every candidate card with the same marker. |
| `MASK_OUTPUT` | Replace the value under `OUTPUT / ARTIFACT` in every candidate card with the same marker. |
| `MASK_WORKFLOW` | Replace the value under `WORKFLOW / PROCEDURE` in every candidate card with the same marker. |
| `MASK_SUCCESS` | Replace the value under `SUCCESS / VERIFICATION` in every candidate card with the same marker. |
| `MASK_BOUNDARY` | Replace the value under `BOUNDARY / NOT FOR` in every candidate card with the same marker. |
| `MASK_DEPENDENCY` | Replace the value under `DEPENDENCY / RESOURCE` in every candidate card with the same marker. |

The exact marker is:

```text
[FIELD WITHHELD IN THIS REPRESENTATION]
```

It is a representation-level absence marker, not a claim about the source. The
slot label, candidate order, non-target slot values, and all prompts remain
unchanged. Every candidate receives the same field-level marker, so the
condition does not single out the gold skill as a card with missing information.

No random, fabricated, or semantically meaningful filler is introduced to claim
token-length equality. Selector-visible token change is recorded as part of the
intervention. RQ1b makes a field-availability claim, not a length-controlled
text-noise claim; RQ1a remains the controlled-sufficiency evidence.

### 5.1 Per-Field Eligibility

A cluster contributes to field `f` only if the gold has non-marker source
evidence for `f` and at least one incorrect candidate has a different value for
`f`, including `NOT_STATED` versus source evidence. Field-ineligible clusters
are excluded from that field's primary denominator, not silently counted as
zero effect.

## 6. Residual-Redundancy Audit

Removing a slot may not remove every expression of the same operational fact.
That is expected in public artifacts and is part of RQ1b's naturalistic
evidence. For every eligible gold-field value, two source-card-only reviewers
classify whether an operationally equivalent proposition remains in another slot
of that candidate:

| Label | Meaning |
|---|---|
| `none` | No corresponding proposition remains. |
| `partial` | Another slot retains some, but not all, removed operational content. |
| `substantial` | Another slot substantially restates the removed operational content. |

Exact cross-slot substring reuse is recorded mechanically. Residual labels are
not primary-field labels and do not decide gold adequacy. Analysis reports all
eligible clusters and the `none`/`partial` subset separately.

Two source-card-only reviewers independently label every non-`NOT_STATED`
candidate-slot value in the validation and confirmatory cards; the sealed gold
mapping is applied only afterwards to select the eligible gold-field records.
An exact agreement becomes the residual label. A disagreement is retained as
`disagreed` in the complete ledger and remains in the all-eligible analysis,
but is excluded from the `none`/`partial` redundancy-reduced subset. This rule
does not turn residual agreement into a field-attribution or gold-adequacy
decision.

## 7. Pilot And Scaling Gates

The existing six pilot families are rebuilt under this protocol; earlier
primary-field reviews remain historical records and are not reused as
selection-only decisions. The pilot performs no retrieval scoring.

It passes when at least four of six families meet every applicable gate below,
with no repeated card-preservation or masking-mechanics failure:

1. source hashes, candidates, prompts, and sealed gold match the RQ1b input
   manifest;
2. every non-marker excerpt passes literal source audit and cue exclusion;
3. both selection-only reviewers preserve strict gold for direct and paraphrase
   full cards;
4. the eight card conditions have byte-level diffs limited to their designated
   slot values, and each mask marker is identical across every candidate;
5. the per-field eligibility table and residual-redundancy ledger are complete;
6. no source, prompt, label, candidate membership, or selector setting has
   been altered to obtain the pass.

The pilot has no performance acceptance threshold. A field need not cause a
large score change for the measurement instrument to be valid.

The six-family pilot passed all applicable gates: five families completed every
applicable card, preservation, mask, eligibility, and residual step; the sixth
had no literal-valid card and was excluded without a repeated mechanics or
preservation failure. It generated no selector score, retrieval metric, API
call, or external transfer. Checkpoint:
`skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_pilot_2026-08-28/RQ1B_FIELD_TYPE_ABLATION_PILOT_CHECKPOINT_2026-08-28.md`.

No card-builder response from a pilot family is reused. All non-pilot C6
candidate compositions now undergo the same construction exactly once; every
retained non-pilot routing family then undergoes baseline preservation,
mask-mechanics, and residual audits. Pilot families are excluded from
confirmatory effect estimates. A field with fewer than 20 eligible
confirmatory clusters is coverage-limited descriptive evidence, not a primary
field-level estimate.

## 8. Retrieval Scope And Metrics

RQ1b uses simple first-stage selectors so it does not drift into RQ2 pipeline
comparison:

| Retriever | Role | Execution boundary |
|---|---|---|
| BM25 | Lexical operational-information discrimination. | Local only. |
| Qwen dense embedding | Semantic operational-information discrimination. | Requires separate exact external-text transfer authorisation. |

Rerankers, query rewriting, field-aware parsing, graph/tree routing, and
downstream task execution are excluded. They change the retrieval pipeline and
belong to RQ2.

For prompt `q`, gold `g`, selector `r`, and condition `c`, let `s_r(q, x, c)`
be the selector's native higher-is-better score and let `d*` be the highest
scoring incorrect candidate:

```text
margin_r(q, c) = s_r(q, g, c) - max_wrong s_r(q, wrong, c)
delta_margin_r(q, f) = margin_r(q, FULL) - margin_r(q, MASK_f)
```

Primary outcomes are strict Top-1 gold rate, conditional Top-1 loss from
`FULL`-correct to masked-wrong, gold rank and MRR change, selector-native paired
margin change, post-mask winner identity, and residual-redundancy stratum.

Native margins are interpreted only within one selector. BM25 margins, embedding
cosine margins, and any future reranker scores are never pooled on a common
numeric scale. Cross-selector comparisons use Top-1, rank, MRR, and conditional
loss. The cluster is the inferential unit: direct and paraphrase outcomes are
retained separately and aggregated within cluster before field-level summaries.
Report effect sizes and cluster-bootstrap confidence intervals, not post-hoc raw
score thresholds as the main claim.

## 9. Interpretation Rules

| Observation after masking `f` | Permitted interpretation |
|---|---|
| Top-1 flips and margins fall | `f` supplied non-redundant routing support in those field-card clusters. |
| Gold remains Top-1 but margins fall | `f` supported separation, but remaining fields retained enough support. |
| Ranking and margins remain stable | `f` was non-discriminative in that subset or redundant there; this is not proof of universal uselessness. |
| Ranking improves | `f` may introduce noise or an adverse association for that selector and subset. |

RQ1a establishes controlled individual-field sufficiency. RQ1b establishes
conditional contribution and redundancy in a public combined-information
representation. Neither supports a universal or uniquely decisive routing-rule
claim.

## 10. Execution Sequence And Stop Rules

1. Derive and hash-freeze the RQ1b input manifest from the current C6 roster.
2. Rebuild the six selection-only pilot cards under this protocol.
3. Stop and report if pilot card preservation or masking mechanics fail. Do not
   score or change frozen inputs.
4. On pilot pass, materialise and validate the non-pilot confirmatory corpus.
5. Freeze validated cards, masks, eligibility denominators, residual ledger,
   selector versions, and score ledger before BM25 scoring.
6. Run local BM25 and analyse it under Section 8.
7. Seek separate approval before any Qwen document text leaves the workspace.
8. Run authorised Qwen scoring, then the same paired analysis.
9. Do not write results into thesis LaTeX/PDF until the user reviews final
   results and claim boundaries.

No external service, API, embedding call, retrieval score, metric, or thesis
result is created by this protocol document itself.

## 11. v2.1 Joint Field-Set Availability Amendment (2026-08-29)

The completed v2 single-slot experiment found no stable all-eligible
field-level effect. A separately labelled, prospective-before-joint-results
amendment therefore masks coherent field **sets** synchronously from every
candidate card: task specification (use/input/output), execution/verification
(workflow/success), and applicability/capability (boundary/dependency). The
unchanged `FULL` card, prompt, candidate membership, gold label, remaining
slots, selector, and score rule are fixed. Each set uses the intersection of
its constituent-field eligibility sets.

This tests joint non-redundant availability in naturally combined public
cards; it cannot identify an individual decisive field. The local BM25 and
separately authorised Qwen single-vector twins both completed 696 rows and
passed independent audits. Each group has directional `FULL-MASK` loss, but
all primary Top-1 and MRR composition-bootstrap intervals cross zero for both
selectors. This is a public-card redundancy/uncertainty finding, not a
confirmed joint-set contribution or a revision of RQ1a's controlled
field-sufficiency result. Machine evidence and the exact recovery chain are
at:
`skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_joint_mask_v21_qwen_2026-08-29/QWEN_RESULT_CHECKPOINT_2026-08-29.md`.
