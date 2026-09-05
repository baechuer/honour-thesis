# RQ1b V3 C4 Source-Grounded Field-Card And Blind Review SOP

<!-- RQ1-RECORD-STATUS:START -->
> **RQ1 record status (2026-09-04): `HISTORICAL_OR_SUPERSEDED`.** Retained for provenance and method history. Do not use its dated status, denominator, or result as the current RQ1 claim unless the canonical RQ1 index explicitly carries it forward. Canonical index: `thesis_notes/current/RQ1/README.md`.
<!-- RQ1-RECORD-STATUS:END -->



Status: `AMENDED BEFORE ANY C4A REBUILD / LOCAL ONLY / C3-ALLOW-C4 PACKETS ONLY / NO SELECTOR OR METRIC`

## Purpose

C4 determines whether a cue-controlled C2 request has exactly one fully
adequate candidate **when candidates are presented as source-grounded seven-slot
cards**. It deliberately separates two checks:

1. **C4A card preservation:** can each anonymous source become a faithful,
   fixed-schema representation without invented information or source identity?
2. **C4B key-blind adequacy:** given the prompt and those anonymous cards, do
   two independent reviewers select the same one fully adequate candidate?

Neither check uses a selector, embedding, API, past routing result, or a sealed
C2 construction target. A C4 result is still not frozen until C5 compares its
consensus with the sealed construction target and C6 validates all lineage.

## Seven-Slot Card Schema

Each candidate card has these slots in this fixed order:

1. `use_condition`
2. `input_precondition`
3. `output_artifact`
4. `workflow_procedure`
5. `success_verification`
6. `boundary_not_for`
7. `dependency_resource`

A slot is either `EVIDENCE`, with one or more exact contiguous excerpts from
the original source body, or `NOT_STATED`. `NOT_STATED` is an absence marker,
not a claim that the skill forbids or lacks the capability. Builders may not
paraphrase, infer a fact, merge non-contiguous fragments, copy a source title,
URL, repository name, YAML title, source heading line, local path, or stable
source identifier into a card.

### Slot-Assignment Rule (C4A v1.1)

The seven slots are **not mutually exclusive**. A single exact contiguous
excerpt may, and must, be cited in every slot that it explicitly supports. The
builder must not choose one arbitrary slot for a sentence that jointly names a
material request, action, and resulting artifact.

Apply these inclusion rules mechanically:

| Slot | Include an exact source excerpt when it explicitly states... |
|---|---|
| `use_condition` | the situation, task class or decision context for which the skill is appropriate. |
| `input_precondition` | an artifact, datum, state, authority, dependency or environment that must be available before the core action. |
| `output_artifact` | a deliverable, decision, created/returned object, state change or final result. |
| `workflow_procedure` | an action, transformation, analysis or ordered step that the skill performs. |
| `success_verification` | an explicit test, acceptance condition, quality threshold or verification action. |
| `boundary_not_for` | an explicit exclusion, route-out, unsupported case or stop condition. |
| `dependency_resource` | a named runtime, package, service, credential, template, file, tool or other resource needed to perform the work. |

If one sentence says, for example, that a provided artifact is transformed by
an action into a returned deliverable, that **same literal sentence** belongs
in input, workflow and output. A slot is `NOT_STATED` only when no literal
source excerpt meets its inclusion rule. This rule does not infer unstated
facts and does not use prompts or construction targets.

## C4A: Anonymous Card Construction And Literal Audit

1. The coordinator creates a private lineage manifest and a separate builder
   packet for each C3-allowed composition. The public packet contains only
   anonymous candidate labels and hash-verified copies of the assigned original
   source bodies. It contains no prompt, C2 target, provenance, title map,
   selector output, metric or result.
2. Two independent local builders each return one seven-slot card per
   anonymous candidate. They may read only their packet and must report exact
   excerpts or `NOT_STATED`; they may not decide a winner.
3. A separate literal auditor checks every non-marker excerpt against its
   assigned original, confirms that headings/identity lines are excluded, and
   checks schema coverage. A source-only coordinator applies the v1.1
   inclusion rule before canonicalisation; an unsupported or arbitrary slot
   assignment remains unsafe.
4. A deterministic canonicaliser may use a builder only if its card passes the
   literal audit and conforms to the v1.1 inclusion rule. If no independently
   constructed card passes, the composition is excluded. When both pass but
   materially disagree in a way that changes the operational chain, the
   composition is held for source-only repair rather than silently choosing a
   convenient card.

This preserves source evidence in a representation; it does not extract a
universal taxonomy or claim that all public sources contain every field.

## C4B: Key-Blind Strict-Adequacy Review

For each C3-allowed direct/paraphrase packet whose candidate cards passed C4A,
the coordinator materialises a review packet containing only:

- the prompt text;
- three or four randomly labelled, source-deidentified seven-slot cards; and
- the allowed response labels: `ONE_FULLY_ADEQUATE`,
  `MULTIPLE_ADEQUATE`, `NONE_ADEQUATE`, or `UNCERTAIN`.

Two independent reviewers receive distinct label permutations. They may not
read original sources, source maps, C1/C2/C3 records, any sealed target,
selectors, embeddings, scores, metrics, or other reviewer's response. A
strict C4B pass requires both to select a one fully adequate candidate and to
agree after unpermutation. `MULTIPLE_ADEQUATE`, `NONE_ADEQUATE`, `UNCERTAIN`,
disagreement, unsafe card construction, or high cue risk that a reviewer judges
source-identifying is an exclusion from strict Top-1.

## Acceptance And Freeze Boundary

The C4 output may enter C5 only when all of the following hold:

1. C3 is `ALLOW_C4_WITH_RISK_ANNOTATION` for the packet;
2. every candidate has a literal-valid seven-slot card;
3. no source identifier or copied title/heading survives in a card;
4. two C4B reviewers agree on one fully adequate anonymous candidate; and
5. the card and review mappings are hash-bound to the C3 r1 lineage.

C5 unseals the C2 construction target only after both C4B reviews are final.
If the C4 consensus differs from the sealed target, it is `TARGET_MISMATCH`,
not a gold label. C6 then freezes the source hashes, prompt lineage,
residual-cue annotation, cards, reviews, target-consistency decision and any
exclusion reason. No selector experiment may use the composition beforehand.

## Claim Boundary

C4 can establish a source-card strict-singleton curation decision for one
packet. It does not by itself establish human annotation, broad ecological
validity, implicit semantic routing, a causal field effect, retrieval
performance or an RQ1 aggregate result. High residual cue risk must remain
visible in every later reporting stratum.
