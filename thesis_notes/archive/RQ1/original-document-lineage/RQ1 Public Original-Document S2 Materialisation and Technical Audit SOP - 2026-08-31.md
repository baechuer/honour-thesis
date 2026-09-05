# RQ1 Public Original-Document S2 Materialisation and Technical Audit SOP

<!-- RQ1-RECORD-STATUS:START -->
> **RQ1 record status (2026-09-04): `HISTORICAL_OR_SUPERSEDED`.** Retained for provenance and method history. Do not use its dated status, denominator, or result as the current RQ1 claim unless the canonical RQ1 index explicitly carries it forward. Canonical index: `thesis_notes/current/RQ1/README.md`.
<!-- RQ1-RECORD-STATUS:END -->



Date: 2026-08-31  
Status: `S2 COMPLETE / LOCAL TECHNICAL MATERIALISATION / NO RESIDUAL REVIEW OR SELECTOR`

## Purpose

S2 turns only the frozen S1 `MAP_READY` source maps into deterministic masked
versions of complete original skill documents. It is a technical integrity
gate. It does not estimate retrieval effects and it does not decide whether a
masked document still contains a target-field value.

The resulting document may be incomplete or non-executable. That is permitted
because this RQ1 intervention tests routing information, not execution. No
edit may replace a removed value with a broader capability.

## Inputs and Scope

- Canonical S1 map ledger:
  `skill_benchmark/rq1_public_original_removal_v3_82_registry/eligibility_ledger/eligibility_ledger.json`.
- Canonical source-only map submissions:
  `skill_benchmark/rq1_public_original_removal_v3_82_registry/eligibility_submissions/canonical/`.
- Anonymous original document packets and source hashes:
  `skill_benchmark/rq1_public_original_removal_v3_82_registry/eligibility_packets/`.
- Seven single-field conditions and three pre-specified group conditions:
  task specification (`use_condition`, `input_precondition`,
  `output_artifact`), execution/verification (`workflow_procedure`,
  `success_verification`), and applicability/capability
  (`boundary_not_for`, `dependency_resource`).

A single-field condition may be materialised only for a composition whose
corresponding S1 condition is `MAP_READY`. A group condition may be
materialised only when every component field is `MAP_READY` for that same
composition. No composition is repaired, substituted or silently added.

## Deterministic Transformation

For each included candidate document, apply only S1 canonical edits. A
`DELETE_LINE` replaces the cited source line with the empty string. A
`REWRITE_LINE` uses its canonical literal replacement. Group conditions merge
the component edits by source line. Identical replacements may share a line;
different replacements make that composition-condition an `EDIT_CONFLICT` and
it is excluded rather than resolved by judgement.

The materialisation ledger records the original and masked SHA-256 hashes, the
source and masked paths, every changed line, field membership, edit kind and
evidence ids. It never contains a prompt, gold label, candidate provenance,
selector output or retrieval result.

## Technical Acceptance

The independent technical audit accepts a candidate mask only if:

1. its original hash matches the frozen source packet;
2. its masked text reconstructs exactly from the original plus its ledgered
   line replacements;
3. every changed line appears in the canonical edit ledger, with no
   unregistered line change; and
4. the masked hash matches the materialisation ledger.

The audit reports composition-condition and candidate-mask counts, conflicts
and failures. Passing this gate does not prove semantic field removal: it only
proves faithful implementation of the frozen map.

## Next Gate and Boundary

Only technically passing materialisations may be sent to S3. S3 is a fresh,
prompt/gold-blind residual review of anonymous masked documents. Any residual
or uncertainty prevents the relevant candidate-field condition from entering
later strict-family linkage. Group conditions require all component fields to
survive S3.

No prompt, gold label, selector, embedding/API, hosted compute, metric or
thesis LaTeX/PDF result is authorised in S2.

## S2 Closure (2026-08-31)

The deterministic materialisation and independent audit passed for all 750
candidate-mask rows with zero source-hash, reconstruction or unregistered-diff
failures. The audit recorded 1,144 ledgered no-op blank lines; these are
permitted delete-line ranges that were already empty and therefore did not
change the text. They are retained in the line ledger but are not an edit
failure because no unregistered text changed.

| Condition | Materialised compositions | Candidate masks | Technical failures |
| --- | ---: | ---: | ---: |
| Each of seven single fields | 19--37 | 64--118 | 0 |
| Task specification group | 5 | 17 | 0 |
| Execution/verification group | 18 | 60 | 0 |
| Applicability/capability group | 22 | 73 | 0 |

One task-specification composition was excluded as an `EDIT_CONFLICT`; all
other non-materialised conditions were already `NOT_MAP_READY` in S1. This is
still technical evidence only. S3 residual review remains required.

Artifacts: `skill_benchmark/rq1_public_original_removal_v3_82_registry/materialized_masks/`
and `skill_benchmark/rq1_public_original_removal_v3_82_registry/technical_audit/`.
