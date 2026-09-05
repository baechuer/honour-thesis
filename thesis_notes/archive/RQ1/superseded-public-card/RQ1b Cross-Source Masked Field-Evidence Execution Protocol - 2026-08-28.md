# RQ1b Cross-Source Masked Field-Evidence Execution Protocol

<!-- RQ1-RECORD-STATUS:START -->
> **RQ1 record status (2026-09-04): `HISTORICAL_OR_SUPERSEDED`.** Retained for provenance and method history. Do not use its dated status, denominator, or result as the current RQ1 claim unless the canonical RQ1 index explicitly carries it forward. Canonical index: `thesis_notes/current/RQ1/README.md`.
<!-- RQ1-RECORD-STATUS:END -->



> **2026-08-28 archival status.** This raw-full-document masking workflow is
> retained only as a feasibility audit. The active public RQ1b execution method
> is `thesis_notes/archive/RQ1/superseded-public-card/RQ1b Public Field-Type Ablation Protocol - 2026-08-28.md`.
> Do not interpret any `ORIGINAL_ONLY` or raw-mask feasibility outcome here as
> a field-availability selector result.

Status: `RAW-FULL-DOCUMENT MASK FEASIBILITY AUDIT ONLY / NO MASKS OR SELECTOR RESULTS`

> **2026-08-28 amendment.** This protocol is retained as the bounded
> feasibility audit for direct masking of original public full documents. It
> no longer gates the RQ1b primary experiment. The active RQ1b-N
> natural-artifact validation and RQ1b-S source-grounded field-card
> winner-ablation protocol is
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b Natural-Artifact And Source-Grounded Field-Card Protocol - 2026-08-28.md`.
> No historical P0--P3 record is altered by this amendment.

This is the prospective execution protocol for the separately curated
cross-source strict-public corpus at
`skill_benchmark/rq1b_cross_source_public_benchmark/`. It does not revise the
historical `rq1b_naturalistic_public_replication` Wave 001/Wave 002
original-only records. It creates no masked artifact, retrieval result,
embedding, external transfer, API call, selector result, or thesis result.

## 1. Purpose And Claim Boundary

RQ1a already establishes controlled field sufficiency: when all other skill
context is shared, exposing a selected operational field can resolve a
near-neighbour ambiguity. This protocol asks a narrower natural-artifact
question:

> Among semantically close, real public original skill artifacts, does
> evidence for the user-required operational field causally improve strict
> within-cluster selection when that evidence is masked while the prompt,
> candidate set, shared task, and selector are held fixed?

An original-versus-masked delta supports a causal claim only for a cluster that
passes every masking gate below. An original-only result is descriptive
natural-artifact selection evidence, not a causal field result. Neither result
is a full-library retrieval, I1/I2/I3/I3C representation, graph/tree, reranker,
task-success, or human-annotation result.

## 2. Frozen Curation Input

The live curation input is the Round 42 C6 strict-public closure:

- 76 frozen cross-source candidate compositions;
- 209 frozen strict routing-test families, where a family is one candidate
  composition paired with one strict-gold target and its one or two frozen
  prompt variants;
- 408 frozen strict prompt packets, each a single direct/paraphrase variant
  within a routing-test family;
- 119 non-primary multi-adequate, disagreement, or mismatch packets excluded
  from strict Top-1 scoring;
- original `SKILL.original.md` candidates only, each bound to the C6 source
  hash and existing C1 identity record;
- one primary distinguishing field must be locked per routing-test family
  before that family can be masked;
- two prompt variants where available: `direct` and `paraphrase`.

The strict gold skill is the existing C4 exact-singleton, C5
sealed-target-matched selection label. It is model-assisted blinded curation
evidence, not human annotation. A routing-test family is a selection task, but
families sharing one candidate composition are correlated. The 408 packets are
repeated prompt measurements and must not be treated as 408 independent routing
tasks. Primary paired summaries therefore aggregate at the routing-test-family
level and use composition-clustered resampling or paired summaries.

## 3. Experimental Conditions

For each mask-eligible routing-test family `f`, frozen prompt `p`, and selector
`s`:

| Selector | Candidate document condition | Role |
|---|---|---|
| BM25 | `natural_original` | Local lexical baseline over original public artifacts. |
| BM25 | `target_evidence_masked` | Paired lexical field-evidence control. |
| Qwen `text-embedding-v4` | `natural_original` | Semantic original-artifact condition; external transfer requires separate approval. |
| Qwen `text-embedding-v4` | `target_evidence_masked` | Paired semantic field-evidence control; external transfer requires separate approval. |

The prompt, candidate membership/order, strict gold, scoring configuration, and
tie-break rule are identical within an original/masked pair. A query scores only
the three or four candidates in its own frozen cluster. No query rewriting,
reranking, direct-reasoner selection, I1/I2/I3/I3C conversion, or global
candidate-pool stress test is part of this RQ1b primary comparison.

Primary metric: cluster-level strict Hit@1. Secondary metrics: strict MRR,
paired original-minus-masked delta, direct/paraphrase slices, field slices only
where their post-audit sample size is adequate, and an error taxonomy. Cluster
summaries or cluster-level resampling are required; packet rows are not assumed
independent.

## 4. Pre-Scoring SOP

### P0. Protocol And Input Boundary

1. Keep this protocol separate from historical Wave 001/Wave 002
   natural-original records and from RQ1a/RQ2.
2. Materialize a read-only roster from C6 strict packets only, then group it
   into routing-test families by candidate composition plus strict-gold target.
3. Verify every candidate path, `skill_id`, candidate-set membership, source
   SHA-256, prompt text, strict gold, family membership, and direct/paraphrase
   designation against its C1-C6 lineage.
4. Fail closed on any missing, changed, duplicate, or non-primary packet.

Acceptance: the roster contains exactly 76 candidate compositions, 209
routing-test families, and 408 strict packets; has no non-primary packet; and
has source bytes equal to their recorded hashes.

### P0.5. Blind Field-Contrast Coding

The historical C6 records freeze candidate identity, prompt packet, and strict
gold lineage, but do not consistently encode a machine-readable
`primary_distinguishing_field`. A candidate composition can also contain
multiple strict-gold targets. It is not acceptable to infer a convenient field
after seeing selector results or assume that one field applies to every target
within a candidate composition.

Two independent field coders receive one frozen routing-test family: its one or
two frozen prompts and anonymised original candidates. They do not receive
strict gold, C4/C5 outcomes, source provenance, intended candidate, prior
curation rationale, masks, or selector results. Each coder must choose exactly
one of the following for each prompt, or fail closed:

- `use_condition`: the task trigger or user goal;
- `input_precondition`: required input object, state, or prerequisite;
- `output_artifact`: required deliverable or output form;
- `workflow_procedure`: required operation path or ordering;
- `boundary_not_for`: exclusion, authority, or prohibited use;
- `dependency_resource`: required environment, tool, access, version, or
  external resource; or
- `success_verification`: required acceptance or validation condition.

The coder returns the exact prompt clause that encodes the requirement, the
field value/evidence it seeks in each anonymised candidate, and either one
field code or `MULTI_FIELD_OR_NONCODEABLE`. It does not issue a gold judgment.
The required response envelope is one JSON object with `family_id` and a
`per_prompt` array containing exactly one object per frozen packet variant.
Every array object has `variant`, `code`, `prompt_clauses`,
`candidate_evidence`, and `reason`; `candidate_evidence` may name only labels
present in its packet and must omit labels without an exact quote. Alternative
keys such as `prompt_codings`, `prompt_clause`, `field_code`, or
`operational_requirement` are invalid, even where their prose appears
compatible. This is a process-level schema requirement, not a scientific input
or a change to any frozen source, prompt, or label.
Before a coding record counts, a local validator must parse its JSON and find
every quoted prompt clause and candidate excerpt as a literal contiguous
substring in the corresponding blind packet. A paraphrase, normalised
punctuation, malformed escape sequence, or missing evidence quote makes that
coder record invalid for consensus; it may be retained as a raw audit trail but
cannot support a field lock.

The coordinator accepts a `FIELD_CONTRAST_LOCKED` record only when both coders
choose the same single field and same operational query requirement for every
prompt variant in the family, and the resulting field-evidence account is
compatible with the pre-existing sealed strict gold after unblinding. Any
multi-field reading, coding disagreement, direct/paraphrase field mismatch, or
strict-gold incompatibility is `ORIGINAL_ONLY`; it is not repaired by choosing
a different field after the fact.

This is model-assisted coding of a pre-retrieval field contrast, not human
annotation, a retrieval result, or a new gold label. Only
`FIELD_CONTRAST_LOCKED` clusters advance to P1.

### P1. Target-Field Evidence Mapping

For each `FIELD_CONTRAST_LOCKED` routing-test family, an evidence-mapping
reviewer receives only: the original candidate artifacts, anonymised candidate
IDs, the locked primary field, and the locked field-value contrast. The reviewer
does not receive prompt text, strict gold, C4/C5 outcomes, model scores, or
prior mapper output.

The reviewer must:

1. enumerate every exact source span that directly states, operationalises,
   negates, presupposes, or verifies the target-field value;
2. assign each span to a carrier surface: title/heading, description,
   use-condition, input/precondition, output/artifact, workflow/procedure,
   boundary/not-for, dependency/resource, success/verification, example, or
   resource/reference;
3. distinguish shared task-envelope text from differential target-field text;
4. propose a local neutral replacement for each differential span; and
5. identify any inseparable or structural cue that would make safe masking
   impossible.

Every cited span must be an exact substring of the hash-verified original. A
local deterministic preflight may enumerate headings and literal field terms,
but it is a review aid only and is never treated as evidence-map completion.
A mapper may also run the local literal-evidence validator against only its own
JSON response and the anonymous packet candidate copies before submission. This
preflight has no access to prompts, gold labels, provenance, prior maps,
selectors, or results; it prevents transcription mistakes but does not approve
an evidence map or relax the independent audit requirement.

### P2. Independent Red-Team Mapping

A second reviewer independently performs P1 from the same allowed materials.
It must actively seek indirect cues: prerequisite chains, output contracts,
workflow order, negative instructions, tool/resource names, examples, headings,
and structural carrier patterns. It does not see the first map.

The coordinator takes the union of both maps. Any span raised by either reviewer
must be resolved as `MASK`, `SHARED_NON_TARGET`, or `UNRESOLVED`. An unresolved
span fails closed to `ORIGINAL_ONLY`; it may not be silently omitted.

### P3. Mask Construction And Fidelity Check

Only clusters with a complete P1/P2 union map may receive provisional masked
copies. A mask changes only approved target-evidence spans. Each replacement
uses a deterministic neutral field marker with whitespace padding sufficient to
avoid a material length cue; it cannot encode the original value, polarity, or
candidate identity. When a field-bearing heading or line has no neutral local
replacement, the corresponding carrier must be neutralised consistently across
all candidates or the cluster is `ORIGINAL_ONLY`.

A deterministic diff check must prove that every changed byte lies inside an
approved map span or its defined padding. The fidelity reviewer verifies that:

1. no unapproved text was changed;
2. all mapped differential spans were neutralised;
3. the shared task envelope and non-target operational information remain;
4. the artifact remains structurally readable; and
5. marker count, placement, heading structure, or document length does not
   itself reveal a target-field value or candidate identity.

### P4. Residual-Cue Challenge

Two independent red-team reviewers receive the frozen prompt and anonymised
masked candidates, but no source provenance, C4/C5 selection label, intended
candidate, original documents, or selector output. They answer only whether a
candidate uniquely satisfies the prompt's target operational requirement and
must quote any masked-text evidence that permits such a choice.

`MASK_ELIGIBLE` requires both reviewers to find no unique target-field route
from the masked text and the coordinator to verify that every quoted concern is
absent, neutralised, or correctly classified as shared non-target context.
Any surviving field-specific cue, a cue-bearing mask structure, or reviewer
disagreement about a plausible residual cue produces `ORIGINAL_ONLY`.

This is a conservative construction-sensitivity control, not proof that no
semantic cue exists. It is deliberately fail-closed.

### P5. Final Execution Freeze

Before any selector result is viewed, freeze:

- the strict execution roster;
- original and masked candidate paths and SHA-256 hashes;
- evidence maps, changes, and residual-cue dispositions;
- mask eligibility/exclusion reasons;
- BM25 implementation, tokenisation, and deterministic tie-break;
- Qwen model name, dimensions, cache keying, request budget, and no-retry
  policy; and
- analysis code/version and metric definitions.

No source, prompt, gold, field assignment, mask, selector configuration, or
acceptance rule may change after P5. A discovered defect requires a versioned
amendment and a fresh freeze, not silent repair.

## 5. Reviewer Workflow And Agent Limits

This is local curation, not model evaluation. A reviewer task handles at most
one routing-test family for P0.5/P1/P2/P4. At most six reviewer agents are
active at once. Each reviewer is closed after its structured response is
independently checked and its exact evidence spans are validated. No reviewer
may use online search, external APIs, retrieval results, embeddings, prompt
labels, or candidate provenance outside the allowed packet.

Suggested batch sequence:

1. Local deterministic roster/source preflight for up to six routing-test
   families.
2. Six P0.5 field coders in parallel, one family each; validate and close.
3. Six independent P0.5 coders in parallel for the same batch; validate and
   close. Only `FIELD_CONTRAST_LOCKED` families advance.
4. Six P1 evidence mappers in parallel for locked families; validate and close.
5. Six independent P2 challengers in parallel for the same batch; validate and
   close.
6. Coordinator constructs provisional masks only for union-map-complete
   clusters, then runs deterministic diff/source checks.
7. Six P4 masked-text red teams in parallel only for provisional masks;
   validate and close.
8. Batch-write the reviewed ledger and advance only passed clusters. Do not
   create selector scores or alter C6 inputs during this workflow.

## 6. Per-Cluster Acceptance States

| State | Requirements | Permitted use |
|---|---|---|
| `MASK_ELIGIBLE` | C6 strict lineage, locked P0.5 family field contrast, exact complete union map, mask fidelity pass, and two P4 no-residual-route passes. | Primary paired original-vs-masked RQ1b analysis. |
| `ORIGINAL_ONLY` | C6 strict lineage is intact but no single family field can be locked, target evidence cannot be safely isolated, or masking damages the shared task. | Descriptive original-artifact selection only; never causal delta. |
| `EXCLUDE` | Integrity, prompt, candidate-set, or strict-label lineage fails. | No RQ1b selector analysis. |

Proposed interpretation threshold, to be frozen before P1 begins:

- 50 or more `MASK_ELIGIBLE` routing-test families from at least 30 candidate
  compositions: primary strict public paired result;
- 30-49 eligible families or fewer than 30 represented compositions: scoped
  masked-field feasibility result; field slices are exploratory;
- below 30: report masking feasibility and original-only association only, not a
  broad causal field claim.

## 7. Selector Execution And Claims

After P5 only:

1. Run local BM25 over original then masked artifacts. Persist per-packet ranks
   and candidate scores with no tuning after viewing results.
2. Review local BM25 results and the frozen ledger before any external work.
3. Request a separate explicit authorization that states Qwen text count,
   original/masked artifact and prompt scope, model, dimensions, request/cost
   budget, cache path, and no-retry policy.
4. Run Qwen original then masked under that authorization only.
5. Aggregate paired cluster outcomes, not packet rows as independent trials.

Interpretation:

- original better than masked in an eligible cluster supports target-field
  evidence as a causal selection signal for that selector and cluster;
- equal/high masked performance triggers residual-cue and shared-envelope
  inspection before any positive claim;
- low original performance means the selector did not reliably exploit the
  available natural evidence; it does not show the field is useless;
- original-only results remain ecological association evidence and cannot be
  pooled into the causal masked estimate.
