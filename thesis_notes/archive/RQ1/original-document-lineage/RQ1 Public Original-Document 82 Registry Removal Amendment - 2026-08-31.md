# RQ1 Public Original-Document 82 Registry Removal Amendment

<!-- RQ1-RECORD-STATUS:START -->
> **RQ1 record status (2026-09-04): `HISTORICAL_OR_SUPERSEDED`.** Retained for provenance and method history. Do not use its dated status, denominator, or result as the current RQ1 claim unless the canonical RQ1 index explicitly carries it forward. Canonical index: `thesis_notes/current/RQ1/README.md`.
<!-- RQ1-RECORD-STATUS:END -->



Date: 2026-08-31  
Status: `S1--S3 COMPLETE / FULL-ORIGINAL REMOVAL FEASIBILITY CLOSED / NO SELECTOR OR EXTERNAL EXECUTION`

## Purpose

This amendment starts a new, non-overwriting source-only eligibility pass on
the canonical 82-composition public registry. It does not reopen or replace
the earlier 76-composition redaction-feasibility closure. That closure remains
evidence that selective deletion is difficult in full public documents. The
new pass tests the complete merged registry under one uniform packet,
validation, and attrition procedure before any retrieval condition can exist.

The intervention removes explicitly documented values from a complete original
skill document. It is routing-only: a masked document may be incomplete or
non-executable. It must never broaden the documented capability. For example,
removing a `PDF` requirement may delete or neutralise that value, but may not
replace it with `file`, `document`, or `any input`.

## Frozen Scope

- Source frame: 82 deduplicated compositions and 265 hash-verified public
  original skill documents.
- Parsed field evidence: 1,860 exact source spans, verified by the S0 audit.
- Fields: `use_condition`, `input_precondition`, `output_artifact`,
  `workflow_procedure`, `success_verification`, `boundary_not_for`, and
  `dependency_resource`.
- No mapper or residual reviewer receives a prompt, gold label, candidate
  provenance, historical card, selector output, or result.

The two direct-V3 compositions with partial prompt coverage remain in S1
because S1 is source-only. They cannot enter a later complete-case scoring
denominator unless a separate lineage decision permits it.

## S1: Candidate-Field Removal Mapping

For every candidate document and every field, a source-only mapper receives
the original document plus exact direct-value evidence. It returns exactly one
of the following dispositions:

- `SAFE_MAP`: all explicit values for the field can be removed by exact
  delete/rewrite edits without broadening the capability. Every supplied
  direct-value span must be covered; any extra direct occurrence found during
  the full-document inspection is added to the map and covered too.
- `NO_DIRECT_VALUE`: no explicit field value is present. It carries no edit.
- `UNSAFE_MIXED_CARRIER`: at least one required removal is inseparable from
  non-target content in the same textual carrier. It carries no edit and must
  cite the blocking source lines plus the non-target content that would be
  lost.
- `UNCERTAIN`: the source does not justify a safe decision. It carries no
  edit and states the source-specific uncertainty.

`SAFE_MAP` is not mask approval. It only permits deterministic materialisation
and a later fresh residual review.

## Mechanical Acceptance Rules

The coordinator accepts a mapper submission only when it has complete batch,
candidate, and seven-field coverage; every cited line is within the original
document; every pre-mapped direct-value id is covered by a `SAFE_MAP`; and
every proposed edit is limited to mapped direct-value lines. A `REWRITE_LINE`
may use only a literal deletion or `[information removed]` where grammar
requires it. It cannot introduce a broader type, format, task, method,
resource, or capability.

At the composition-field level, `MAP_READY` requires every candidate to be
either `SAFE_MAP` or `NO_DIRECT_VALUE`, with at least one real edit across the
composition. Any `UNSAFE_MIXED_CARRIER` or `UNCERTAIN` marks that field
`ORIGINAL_ONLY`. This pre-prompt map does not decide whether a field is
relevant to a particular strict routing family; that linkage occurs only after
the source-only map is frozen.

An unsafe map may retain the supplied evidence ids it examined, but it may not
contain a proposed edit or newly discovered removable span. Those ids are
audit context only and never authorise a mask.

## Gates After S1

1. Deterministically materialise only `MAP_READY` conditions and audit exact
   source hashes and diffs.
2. Give separate prompt/gold-blind residual reviewers only the masked
   documents and target field category. Any remaining direct value rejects the
   candidate-field condition.
3. Join the surviving source-only conditions to frozen strict family lineage,
   freeze one complete-case denominator, then seek any needed selector/API
   approval. Group conditions require all component fields to survive.

No BM25, Qwen embedding, hosted compute, thesis LaTeX/PDF result write, or
field-effect claim is authorised by this amendment.

## S1 Closure (2026-08-31)

All 82 compositions and 265 hash-verified original documents completed the
source-only mapping gate. Twenty-eight canonical mapping batches passed the
mechanical validator after one mapper-quality remediation: the initial six
batches were remapped because their unsafe decisions did not name the
line-addressable non-target content that made deletion unsafe. This correction
improved evidence quality only; it is not a field disposition or retrieval
result.

| Field | MAP_READY | No editable value | Original only |
| --- | ---: | ---: | ---: |
| Use condition | 21 | 0 | 61 |
| Input/precondition | 19 | 1 | 62 |
| Output artifact | 25 | 1 | 56 |
| Workflow/procedure | 22 | 0 | 60 |
| Success/verification | 32 | 0 | 50 |
| Boundary/not-for | 37 | 1 | 44 |
| Dependency/resource | 27 | 0 | 55 |

`MAP_READY` means that a deterministic, non-broadening document edit can now
be constructed and audited. It does not mean the masked document is
residual-free, relevant to every strict family, or suitable for selector
scoring. `ORIGINAL_ONLY` is a conservative source-structure result: at least
one candidate's documented value shares a textual carrier with content that
cannot be removed under this protocol.

Closure artifacts: `skill_benchmark/rq1_public_original_removal_v3_82_registry/eligibility_ledger/` and
`thesis_notes/checkpoints/methods/RQ1 82 Registry S1 Eligibility Closure - 2026-08-31.md`.

## S2--S3 Closure (2026-08-31)

S2 materialised 750 candidate-mask rows from the frozen maps and passed exact
source-hash, reconstruction and unregistered-diff checks. S3 then reviewed all
183 materialised single-field composition conditions in prompt/gold/source-map
blind packets. Only 33 conditions were `CLEAR`: 2 use-condition, 2
input/precondition, 3 output-artifact, 0 workflow/procedure, 11
success/verification, 15 boundary/not-for and 0 dependency/resource. The
three joint groups have zero survivors because every group contains at least
one component field that did not clear S3.

The planned strict-family linkage and selector comparison are therefore not
started. A survivor-only comparison would discard most fields and all groups,
so it could not answer the intended full public RQ1 comparison. This is a
full-original, non-broadening deletion feasibility result. It does not measure
routing, does not imply that a field lacks routing value, and does not replace
the controlled or derivative-card experiments.

Closure artifacts: `skill_benchmark/rq1_public_original_removal_v3_82_registry/blind_residual_ledger/`,
`thesis_notes/archive/RQ1/original-document-lineage/RQ1 Public Original-Document S3 Blind Residual Review SOP - 2026-08-31.md`, and
`thesis_notes/checkpoints/methods/RQ1 82 Registry S3 Blind Residual Closure - 2026-08-31.md`.

## Interpretation Boundary

If few conditions survive, that is a public-document redaction feasibility
result: natural skill documents distribute the same operational information
across titles, descriptions, procedures, examples, and resources. It is not a
retrieval result and does not show that the field lacks routing value.
