# RQ1b V3 C2 Prompt Construction And Cue-Control Handoff SOP

<!-- RQ1-RECORD-STATUS:START -->
> **RQ1 record status (2026-09-04): `HISTORICAL_OR_SUPERSEDED`.** Retained for provenance and method history. Do not use its dated status, denominator, or result as the current RQ1 claim unless the canonical RQ1 index explicitly carries it forward. Canonical index: `thesis_notes/current/RQ1/README.md`.
<!-- RQ1-RECORD-STATUS:END -->



Status: `PROSPECTIVE / LOCAL ONLY / C1-ADVANCED SOURCE TRIADS ONLY / NO SELECTOR OR METRIC`

## Purpose And Boundary

C2 turns a C1-approved, source-grounded three- or four-skill composition into
candidate prompt packets for later **cue control** and **strict singleton
review**. C2 is not an annotation of a final gold label and is not a routing
experiment. A C2 prompt can be discarded at C3 or C4 without changing the C1
source finding.

Only a `ADVANCE_C2_PROMPT_CONSTRUCTION` record in a frozen C1 ledger may enter
this SOP. The C2 curator may read the cited source originals and C1 evidence
card, but may not use selector results, embeddings, prior retrieval outcomes,
or online material.

## Unit And Outputs

For every C1-approved composition, construct up to six prompt packets:

- one **direct** and one **intent-preserving paraphrase** for each candidate;
- an internal sealed target-source ID used only after key-blind review; and
- an unlabelled prompt-and-candidate-card packet for later C3/C4.

The target ID is a construction hypothesis, not a gold label. A packet becomes
a strict gold-labelled routing case only if C3 passes cue control, two
independent C4 selection-only reviewers choose the same single fully adequate
candidate, C5 agrees with the sealed construction target, and C6 freezes the
entire lineage.

## C2 Construction Rules

1. State a realistic request using the target's operational need: required
   input, desired output artifact, applicable constraint, or workflow boundary.
   It must not state a source title, repository, URL, local source path, or
   copied heading.
2. Retain genuine user-facing constraints where necessary for routing. Examples
   include a required native deliverable, an interactive rather than static
   artifact, or a needed deal context. They are not removed merely because a
   source uses the same general term.
3. Exclude accidental source identifiers: package/library names, command names,
   template names, source-only directory names, exact distinctive source
   clauses, version strings, and copied title tokens when a plain-language
   description can express the same request.
4. Write a second prompt that preserves the same intended operation and
   constraints but changes syntax, surface wording and sentence structure. It
   must not add a new requirement, weaken a required constraint, or use a
   different candidate's distinctive feature.
5. Record a short construction rationale citing the source-card elements that
   informed the request. This rationale stays outside the later blind packet.
6. If a target-specific request cannot be written without a source-identifying
   cue, or if the request plainly makes several candidates fully adequate,
   record `C2_REJECT_UNSAFE_OR_MULTI_ADEQUATE_RISK`; do not force a packet.

## Required C2 Record

Each draft record must include:

- immutable C1 review ID, composition ID and member source IDs;
- `packet_id`, `variant` (`direct` or `paraphrase`) and sealed target source ID;
- plain-language prompt text;
- source-grounded intended constraints and construction rationale;
- an explicit list of removed/avoided source cues;
- `C2_DRAFT_FOR_C3` or `C2_REJECT_UNSAFE_OR_MULTI_ADEQUATE_RISK`; and
- a statement that no selector, embedding, scoring, API or external text
  transfer occurred.

## C3 Handoff And Acceptance

C3 performs two separate checks before C4:

1. **Mechanical cue scan:** source names, titles, URLs, repository labels,
   command/package/template strings, copied headings and distinctive exact
   source phrases; and
2. **Manual residual-risk review:** whether retained genuine operational detail
   nevertheless functions as a high source-identifying cue.

C3 may rewrite only cue-only wording while retaining the same sealed target
and operational intent. A substantive change to a request creates a new C2
revision; it never overwrites the old record. High residual cue risk can be
retained only with explicit annotation and must not later be described as
evidence of implicit semantic routing.

## C4 And Freeze Boundary

Each C3-passed packet is shown to two independent, source-deidentified,
selection-only reviewers. They receive the request and candidate field cards,
but no source IDs, titles, construction target, selector result or metric. The
allowed dispositions are one fully adequate candidate, multiple adequate,
none adequate, or uncertain. Only exact singleton consensus can enter C5;
the sealed C2 target is checked only after both reviews. C6 freezes source
hashes, prompt lineage, cue-risk record, reviews, and final disposition.

## Claims This SOP Does Not Support

The number of C2 drafts is not a valid-cluster count, a public prevalence
estimate, a human annotation count, or evidence for any information field.
No retrieval quality, representation effect, selector result, cost, embedding,
mask, API, or thesis result exists at C2.
