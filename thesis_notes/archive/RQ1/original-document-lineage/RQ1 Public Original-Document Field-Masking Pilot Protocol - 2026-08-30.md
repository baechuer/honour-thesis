# RQ1 Public Original-Document Field-Masking Pilot Protocol

<!-- RQ1-RECORD-STATUS:START -->
> **RQ1 record status (2026-09-04): `HISTORICAL_OR_SUPERSEDED`.** Retained for provenance and method history. Do not use its dated status, denominator, or result as the current RQ1 claim unless the canonical RQ1 index explicitly carries it forward. Canonical index: `thesis_notes/current/RQ1/README.md`.
<!-- RQ1-RECORD-STATUS:END -->



Date: 2026-08-30  
Status: `SUPERSEDED FOR FORMAL MASKS BY 2026-08-31 REDACTION AMENDMENT / PILOT PRESERVED / NO RETRIEVAL OR EXTERNAL TRANSFER`

## 1. Decision

RQ1 will be supported by two complementary experiments, not two research
questions:

1. **Controlled one-field-at-a-time experiment.** Researcher-authored
   near-neighbour skills hold all non-target information constant, then hide or
   show one operational field.
2. **Public original-document field-masking experiment.** Public
   `SKILL.original.md` documents are used as the selector-visible candidate
   text. A condition removes one operational information type from every
   candidate document in a composition, then compares routing with the intact
   originals.

This protocol replaces the field-card ablation as the intended primary public
RQ1 test **only after** the pilot and a new full execution pass all gates below.
It does not alter, delete, relabel, pool, or rerun the existing field-card
results. Those results remain preserved as `LEGACY_CARD_MASK_RESULTS` and may
be discussed later only as supplementary representation-specific evidence.

## 2. Question And Exact Intervention

The public experiment asks:

> When a documented operational information type is removed from real,
> semantically close public skill documents, does it change which candidate is
> selected for the same request?

For a composition with the same prompt, candidates, labels, and selector:

- `FULL_ORIGINAL`: the complete frozen `SKILL.original.md` text for every
  candidate, with only deterministic line-ending normalisation.
- `MASK_<FIELD>_ORIGINAL`: the same document, except every mapped statement
  that expresses the chosen field is removed or minimally rewritten so it no
  longer reveals that field.

The first pilot covers `input_precondition`. Later fields are: `use_condition`,
`output_artifact`, `workflow_procedure`, `success_verification`,
`boundary_not_for`, and `dependency_resource`.

The raw source text, not a seven-slot card, is the candidate representation.
The corpus scope is the frozen public `SKILL.original.md` files only; it does
not load scripts, execute repositories, or append source URLs, repository
paths, provenance metadata, or extracted I1/I2/I3 text to the candidate.

## 3. Pilot Scope

The first local-only pilot prepares exactly one pre-existing strict public
composition with three candidates and its direct/paraphrase prompts. It will
not run BM25, Qwen, a direct selector, hosted compute, or an external API.

The pilot must produce a human-review packet containing:

1. the three intact original documents;
2. the same three documents after `MASK_INPUT_PRECONDITION_ORIGINAL`;
3. a source-span ledger for every edit;
4. a unified diff for each candidate;
5. prompt text and frozen candidate labels, shown only in the human-review
   packet after masking has been constructed;
6. an automated source-preservation and residual-cue report; and
7. a pass/reject recommendation without retrieval scores.

No pilot output becomes a benchmark condition until the user reviews and
approves the packet.

## 4. Field-Mapping Rules

For a target field, a mapper must locate every literal or semantic occurrence
that would let a selector infer the target field. The search covers YAML/front
matter, title, headings, prose, workflow steps, examples, resource notes,
linked-file descriptions, and repeated wording elsewhere in the Markdown.

For `input_precondition`, target evidence includes the user-supplied input
object, format, source state, availability, quality, access credential, or
required prior artifact. It does **not** include runtime versions, packages,
hardware, model providers, installation commands, service configuration, or
other resources needed to execute the skill. Those belong to the separate
`dependency_resource` field and must remain visible in an
`input_precondition` condition. For example, both “scanned PDF” and “OCR image
pages” may need treatment if together they reveal an image-only input path;
the OCR package itself remains as a dependency.

Each mapped edit has one of two forms:

- **Deletion:** remove a self-contained target-field clause, bullet, or
  sentence.
- **Minimal neutral rewrite:** when a sentence jointly expresses target and
  non-target information, preserve the non-target statement but remove the
  target-specific value. The ledger must show both texts and explain why the
  rewrite retains no route-specific target clue.

Document headings may remain only when they are generic across the candidate
set. A title, description, or heading that itself reveals the target property
must also be neutralised. Neutral markers may preserve Markdown structure but
must be identical and non-discriminative across candidates.

## 5. Fairness And Leakage Gates

A field-specific composition is eligible only when all conditions pass:

1. **Candidate synchrony:** the same field is mapped and neutralised for every
   candidate, not only the intended gold candidate.
2. **Complete target removal:** a fresh residual reviewer cannot find direct,
   synonymous, or inferable target evidence that differentiates candidates.
3. **Non-target preservation:** all unedited source spans remain byte-identical;
   each changed span is in the source-span ledger.
4. **No route invention:** the mask introduces no candidate-specific fact,
   source identity, or new positive/negative routing clue.
5. **No prompt or label tailoring:** mappers and residual reviewers see raw
   candidate documents and the field definition, but not prompts, gold labels,
   prior scores, or result tables.
6. **Document completeness:** no arbitrary truncation is allowed. A later
   embedding preflight must either encode an intact document in one request or
   use a declared, lossless Markdown-block chunking rule for every condition.
7. **Reviewability:** the user can inspect the originals, masks, span ledger,
   and diffs before the composition is frozen.

Failure of any gate is a `FIELD_MASK_REJECT` for that composition and field.
It does not invalidate the source document, the broader cluster, or another
field's separately reviewed mask.

## 6. Preparation Workflow

1. Select a strict three-candidate public composition with a declared
   `input_precondition` distinction and preserved source hashes.
2. Freeze copies of the exact raw sources under a new pilot directory.
3. Build an initial span map from literal original-document evidence.
4. Draft masked documents using only the span map and target-field definition.
5. Run an independent local residual-cue and source-preservation review.
6. Produce the human-review packet and stop for user approval.
7. Only after approval, repeat the same process composition by composition.
8. Only after a frozen full corpus exists, run local BM25. A separate exact
   payload/count/cost approval is required before any raw documents or prompts
   are sent to Qwen.

## 7. Future Scoring And Interpretation

Primary comparisons will be `FULL_ORIGINAL` versus one
`MASK_<FIELD>_ORIGINAL` condition at a time, with the same prompt and candidate
composition. The eventual outcomes are Top-1, MRR, gold rank, native retriever
score, and gold-minus-best-wrong margin. Prompt variants are averaged within a
composition; uncertainty is computed at the composition level.

A performance decline after masking means that the removed information helped
that selector in these source documents. A stable winner does not show the
field was irrelevant: the same fact may remain elsewhere, other fields may be
sufficient, or the retriever may not use the removed evidence. These cases are
reported rather than forced into a positive result.

The final public RQ1 claim will therefore be bounded to real source documents
and verified field masks. It will not claim that a field is universally
necessary, that all public skills place information in clean sections, or that
the results prove downstream execution success.

## 8. Planned Workspace

`skill_benchmark/rq1_public_original_mask_v1/`

- `protocol/`: frozen protocol copy and amendments;
- `pilot/`: exact original copies, masks, span ledgers, diffs, and review
  packet for the first input/precondition composition;
- `frozen/`: later approved composition-level records;
- `outputs/`: retrieval results only after a separately approved execution.

## 9. Pilot Decision Record

On 2026-08-30, the user reviewed and approved the CFTC-064
`input_precondition` full-original masking convention. The approved review
package is:

`skill_benchmark/rq1_public_original_mask_v1/pilot/CFTC-064_input_precondition/`

This approves the intervention convention only. CFTC-064 itself remains
`NOT_SCORE_ELIGIBLE` because its technical mapper had seen its historical
prompts during pilot selection. It is not part of a future result denominator.

## 10. Supersession Note

The CFTC-064 pilot and the initial strict semantic-erasure protocol are
preserved for audit. Formal public masks now follow `thesis_notes/archive/RQ1/original-document-lineage/RQ1
Public Original-Document Redaction Amendment - 2026-08-31.md`, which redacts
explicit documented field values while retaining non-target task/method
information. No retrieval, embedding, API request, hosted job, thesis
LaTex/PDF change, or interpretation of a new result is authorised by this
superseded protocol alone.
