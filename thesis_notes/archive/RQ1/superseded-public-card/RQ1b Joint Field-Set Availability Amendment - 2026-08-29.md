# RQ1b Joint Field-Set Availability Amendment

<!-- RQ1-RECORD-STATUS:START -->
> **RQ1 record status (2026-09-04): `HISTORICAL_OR_SUPERSEDED`.** Retained for provenance and method history. Do not use its dated status, denominator, or result as the current RQ1 claim unless the canonical RQ1 index explicitly carries it forward. Canonical index: `thesis_notes/current/RQ1/README.md`.
<!-- RQ1-RECORD-STATUS:END -->



Status: `BOTH SELECTOR TWINS COMPLETE / LOCAL AUDITS PASS / USER REVIEW PENDING / NO THESIS WRITE`

## Purpose

RQ1b v2 found no stable all-eligible effect when one field type was withheld
from every candidate card. That result is compatible with public cards carrying
the same operational fact in several slots. This amendment therefore tests
whether coherent **sets** of fields contribute jointly to strict routing after
the remaining information is still available.

This is a prospective amendment made after the v2 single-field results were
observed but before any joint-mask score is created. It must not be described
as preregistered before v2, pooled with v2 field estimates, or used to relabel
the frozen corpus.

## Frozen Joint Conditions

Every joint condition replaces the listed fields with the same absence marker
in **every** candidate of a composition. Candidate membership, prompt, gold
label, remaining fields, card order, selector version, and scoring rule remain
fixed.

| Condition | Withheld field set | Question |
|---|---|---|
| `MASK_TASK_SPECIFICATION` | use condition + input/precondition + output/artifact | Does the joint task-specification set retain non-redundant routing support beyond the remaining procedural and constraint information? |
| `MASK_EXECUTION_VERIFICATION` | workflow/procedure + success/verification | Does the joint execution-and-acceptance set retain non-redundant support beyond task, output and applicability information? |
| `MASK_APPLICABILITY_CAPABILITY` | boundary/not-for + dependency/resource | Does the joint scope-and-capability set retain non-redundant support beyond task and procedure information? |

`FULL` is the unchanged v2 full card. Each group is scored only for routing
families that were individually eligible for **all** of its constituent fields.
The group denominator is therefore the intersection of the corresponding v2
eligibility sets, fixed before scoring.

## Selectors, Metrics And Inference

The selector scope remains deliberately simple:

1. local BM25;
2. Qwen `text-embedding-v4` single-vector dense retrieval, after a new exact
   text-transfer preflight and separate explicit authorisation.

There are no rerankers, query rewrites, query parsers, field-aware scoring,
graph/tree strategies or downstream agent executions. For each selector and
joint condition, report strict Top-1, MRR, native gold-minus-best-wrong margin,
`FULL`-correct to masked-wrong transitions, and composition-bootstrap
`FULL-MASK` confidence intervals. Direct/paraphrase rows are retained but
aggregated within composition for inference.

A positive effect with a 95% composition-bootstrap interval excluding zero
supports non-redundant contribution of that **field set in these public cards**.
It does not identify which member field was decisive, rank the three sets
universally, establish isolated field causality, or validate end-to-end agent
success. A null effect means the retained slots were sufficient for the simple
selector in this corpus; it does not prove the withheld information is useless.

## Execution Gates

1. Derive all four conditions only from v2 immutable `FULL` cards and bind
   their hashes to a separate v2.1 joint-mask freeze.
2. Verify candidate-synchronous masking, unchanged non-withheld slots,
   unchanged `FULL` cards, source-v2 binding, group-eligibility intersections,
   and exact row coverage locally.
3. Run and independently audit local BM25.
4. Build a Qwen payload preflight that reports new versus cache-hit texts,
   byte and token proxies, batch/call ceilings and expected row count.
5. Obtain separate approval for that exact Qwen payload. Do not transmit text
   or write a Qwen result before it.
6. Run Qwen once with no automatic retry, audit it, then record both selector
   results in trackers. Do not modify thesis LaTeX/PDF until user review.

The canonical v2 single-field result and its artifacts remain immutable at
`skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_confirmatory_v2_{bm25,qwen}_2026-08-29/`.

## Current Execution Record

The joint freeze/mechanics audit passed for 87 strict families and 42
compositions. The pre-frozen group denominators are 73 task-specification, 77
execution/verification and 70 applicability/capability families. Local BM25
completed 696 rows with zero network calls and passed its independent audit.
All three BM25 composition-bootstrap Top-1 intervals cross zero; task
specification is directionally largest (`+0.089`, 95% CI `[-0.005, 0.188]`).
This is not a confirmed joint-field finding until its predeclared Qwen twin has
run and been audited. Checkpoint:
`skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_joint_mask_v21_bm25_2026-08-29/BM25_RESULT_CHECKPOINT_2026-08-29.md`.

The separately authorised Qwen twin is complete and independently audited. It
transmitted only 402 new joint-mask candidate cards in 41/41 no-retry calls;
the 174 queries and 134 unchanged `FULL` cards were cache hits. Qwen is
directionally degraded by each joint mask, but all three primary
composition-bootstrap Top-1 and MRR intervals span zero: task specification
`+0.079` Top-1, 95% CI `[-0.023, +0.193]`; execution/verification `+0.057`
`[-0.006, +0.123]`; applicability/capability `+0.032` `[-0.025, +0.090]`.
Thus the Qwen twin reproduces the bounded BM25 pattern rather than confirming
a non-redundant joint-set Top-1/MRR effect. Its Qwen-native task-specification
margin does decline by `+0.0241`, 95% CI `[+0.0045, +0.0445]`, showing reduced
gold-versus-nearest-wrong cosine separation without a confirmed winner-change
effect. The external receipt stage was complete but
its runner did not create local rows; the frozen receipts and cached vectors
were audit-bound and finalised locally without another request. Full evidence:
`skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_joint_mask_v21_qwen_2026-08-29/QWEN_RESULT_CHECKPOINT_2026-08-29.md`.
