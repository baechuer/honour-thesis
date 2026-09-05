# RQ1b V3 C1 Source-Evidence Card SOP

<!-- RQ1-RECORD-STATUS:START -->
> **RQ1 record status (2026-09-04): `HISTORICAL_OR_SUPERSEDED`.** Retained for provenance and method history. Do not use its dated status, denominator, or result as the current RQ1 claim unless the canonical RQ1 index explicitly carries it forward. Canonical index: `thesis_notes/current/RQ1/README.md`.
<!-- RQ1-RECORD-STATUS:END -->



Status: `ACTIVE FOR FUTURE WAVES / D1 W1 COMPLETE / LOCAL SOURCE-ONLY / NO PROMPT OR GOLD LABEL`

## Purpose

This SOP turns a V3 C0 `ADVANCE_C1_SOURCE_EVIDENCE` triad into either a
source-grounded C1 card set or an explicit C1 rejection. It is an evidence
construction and peer-role check, not a routing experiment.

It separates two questions that must not be conflated:

1. **C0:** does a lexical draft plausibly contain three related but operationally
   different natural sources?
2. **C1:** do exact spans in every source actually support three peer
   input-to-operation-to-output chains under one shared envelope?

## Inputs And Permitted Reading

- A completed C0 final ledger row whose `final_c0_outcome` is
  `ADVANCE_C1_SOURCE_EVIDENCE`.
- The three immutable original source artifacts named in that row.
- The frozen V3 source manifest only for source ID/hash/path binding.

The reviewer must not read or create prompts, labels, acceptable sets, selector
outputs, field representations, scores, result tables, or web-search results.
No source text leaves the local workspace.

## Card Schema

For each source member, capture only exact source substrings and their location:

| Card element | Required content |
|---|---|
| Source binding | source ID, title, SHA-256, original local path |
| Envelope evidence | exact span that supports the shared broad task envelope |
| Input/trigger | exact span naming a material request condition, input, or trigger |
| Operation | exact span describing the core procedure or action |
| Output | exact span naming a deliverable, decision, state change, or result |
| Boundary | exact span for `not for`, prerequisite, dependency, or route-out when present; otherwise explicitly `NOT STATED` |
| Peer-role rationale | one concise source-grounded statement; no invented task prompt |

The card can record multiple candidate operational fields, because C1 is not a
single-field causal attribution step. Its job is to preserve the distributed,
natural evidence needed for the later strict-routing gates.

## C1 Acceptance Criteria

Advance only when every criterion holds:

1. All three original sources are canonically bound and their hashes match the
   V3 source frame.
2. All three expose a non-empty input/trigger, operation and output chain in
   their own source text.
3. One common broad envelope is evidenced without relying only on a shared
   title token or provider/product name.
4. Each candidate has a distinct first-route role; no candidate is merely a
   component, lifecycle step, generic fallback, wrapper, duplicate, interface
   variant, or broad container of another.
5. Exact spans are literal substrings of the immutable originals.

Allowed outcomes are `ADVANCE_C2_PROMPT_CONSTRUCTION`,
`REJECT_SOURCE_BINDING`, `REJECT_ABSENT_OPERATIONAL_CHAIN`,
`REJECT_NO_COMMON_ENVELOPE`, `REJECT_NONPARALLEL_OR_COMPONENT`,
`REJECT_INSUFFICIENT_OPERATIONAL_CONTRAST`, and `NEEDS_PARENT_REVIEW`.

## What A C1 Pass Does Not Establish

A C1 pass does not establish a gold skill, singleton adequacy, human agreement,
implicit semantic difficulty, a field effect, retrieval accuracy, embedding
performance, cost, or general public-skill prevalence. Those claims remain
blocked until C2--C6 and a separately frozen execution amendment.

## D1 Wave 001 Calibration Result

The first directed D1 C1 wave reviewed four mechanically bound, same-origin
triads. Only the typed PDF/DOCX/XLSX-to-Markdown triad advanced to C2. A
serial Browser-SDK upgrade chain was rejected as nonparallel, and Sentry
language SDK plus documentation-generator triads were rejected because a
runtime/framework label did not create a distinct operational route. The
result calibrates this C1 gate only; it is neither a valid-cluster count nor
an information-field or retrieval result. See
`skill_benchmark/rq1b_v3_public_source_frame/d1_directed_discovery_wave_001_2026-08-29/c1_source_evidence_wave_001/C1_SOURCE_EVIDENCE_WAVE_001_CHECKPOINT.md`.

## Review Procedure

1. Materialise a packet with three original paths and C0 source IDs; do not
   include a prompt or any outcome beyond the C0 status.
2. Assign one reviewer at most three non-overlapping packets. The reviewer
   returns a structured card or one allowed rejection with exact source spans.
3. The main thread validates every cited span as a literal substring, source
   hash binding, all-member coverage, and no candidate reuse.
4. The main thread records a final C1 ledger and closes the reviewer. Do not
   generate a prompt for a rejected C1 packet.
5. Only C1 passes move to C2; no C1 status may be reported as a valid V3
   cluster.
