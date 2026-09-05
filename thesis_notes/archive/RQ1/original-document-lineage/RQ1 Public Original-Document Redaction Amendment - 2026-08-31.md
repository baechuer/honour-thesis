# RQ1 Public Original-Document Redaction Amendment

<!-- RQ1-RECORD-STATUS:START -->
> **RQ1 record status (2026-09-04): `HISTORICAL_OR_SUPERSEDED`.** Retained for provenance and method history. Do not use its dated status, denominator, or result as the current RQ1 claim unless the canonical RQ1 index explicitly carries it forward. Canonical index: `thesis_notes/current/RQ1/README.md`.
<!-- RQ1-RECORD-STATUS:END -->



Date: 2026-08-31  
Status: `FULL-ORIGINAL FEASIBILITY AUDIT CLOSED / INSUFFICIENT CLEAN DENOMINATOR / NO SELECTOR OR EXTERNAL EMBEDDING EXECUTION`

## Why This Amendment Exists

The original full-document rule required removal of every direct, synonymous,
or inferable target-field cue while preserving the same executable skill. Two
prompt-blind feasibility intakes showed that this is too strict for natural
skill documents: input contracts are often written through the description,
task definition, workflow, code examples, validation, and troubleshooting.

This amendment does **not** treat that entanglement as a reason to preserve the
input information. For the comparison, the selector sees the complete original
document after the **documented, candidate-distinguishing values** of one field
have been removed. The edited text may become incomplete or non-executable.
That is acceptable here: RQ1 tests whether removing documented information
weakens routing, not whether the edited text can still be used to execute the
skill.

## Revised Intervention

For each candidate in a composition:

- `FULL_ORIGINAL`: the complete frozen original text.
- `REMOVE_INPUT_VALUE_ORIGINAL`: the same full text, except explicit values
  that state an input/precondition are deleted or replaced by an identical
  neutral placeholder across candidates.

For `input_precondition`, redact specific artifact/data types, schemas,
source states, file/path names, access credentials, required prior artifact
names, and candidate-specific availability/quality constraints. Keep generic
grammar where needed, but do not leave the value that distinguishes one
candidate from another.

Examples:

| Original value | Redacted representation |
|---|---|
| `PDF`, `scanned PDF`, `password-protected PDF` | `[input material]` |
| `CSV with gene and logFC columns` | `[input material]` |
| `gsea_running_scores.csv` | `[input material]` |
| `path is ambiguous` | `the required material is unresolved` |

Use the exact same placeholder token, `[input material]`, across every
candidate only where deleting a value would make a mixed sentence
ungrammatical. Otherwise delete a target-only clause or block. Do **not**
replace a specific constraint with a broad capability claim such as “any file
is supported”; that would invent information. A generic phrase such as
“provided material” is allowed only when it makes a sentence grammatical and
does not state a new supported capability.

## What May Remain

Task/method identity, output, workflow purpose, success checks, boundaries,
and dependencies remain unless their literal span itself states a redacted
input value. Thus a method name such as `GSEA`, an output name, or a generic
reference to an input parameter may remain. These can correlate with input
requirements, and that redundancy is part of the empirical result:

- if the winner and margin remain stable, remaining task information was
  sufficient for that selector in that case;
- if the winner changes or the margin declines, the redacted documented input
  values supplied additional routing evidence.

The experiment therefore asks whether **explicit documented field values add
routing value beyond the rest of the natural document**. It does not test the
universal necessity of a field, and it does not erase general method knowledge
or every piece of correlated information from the document.

## Revised Gates

Each mask requires:

1. **Candidate synchrony:** redact the same field category for every candidate.
2. **Value removal:** a blind residual reviewer finds no candidate-specific,
   explicit value for the targeted field. It need not treat task/method names
   as target values.
3. **No capability expansion:** no redaction may claim that a candidate accepts
   a broader input type, format, or source state than the original.
4. **Non-target preservation:** unedited spans remain byte-identical; every
   deletion/rewrite appears in a span ledger.
5. **Prompt/label blindness:** mappers and residual reviewers receive no
   prompts, labels, selector outcomes, field cards, scores, or results.
6. **Human review:** every frozen composition receives an original/mask/diff
   packet before scoring.

## Effect On Earlier Feasibility Records

`CFTC-001` and `CFTC-002` are preserved as correct feasibility rejections
under the superseded “remove every semantic cue while retaining executable
skill identity” rule. They are not selector results. Their prompt-blind span
maps may be reused as source evidence under this revised rule; they must still
receive fresh residual review and human review before scoring.

## Current Scope

The removal rule and execution sequence are approved. The source-only parse
and prompt/label-blind candidate-field redaction maps have been completed over
the frozen 76-composition corpus. The immediate next gate is family-level
eligibility, followed by exact original/mask/diff review-packet construction.
No selector, external embedding/API transfer, hosted work, or thesis
LaTeX/PDF result write has occurred. Scoring remains blocked until the
field-specific masks pass their residual/value-preservation checks and the
required review records are frozen.

The first stratified residual gate found that many public originals repeat an
otherwise mapped field value in descriptions, workflow prose, or boundary text.
That is evidence that the first source map was incomplete; it is not evidence
for or against a field's routing value. The affected composition-condition
items now require a second prompt/label-blind redaction-map pass and a fresh
residual check. Items that cannot be cleared without editing an unsafe mixed
carrier remain ineligible rather than being scored with leaked information.

The completed remediation and fresh residual gate retained only 3 clear items
out of 31 rebuilt first-pass-residual items. That is insufficient for the
pre-registered single-field or group metric denominators, so this amendment is
closed as a no-selector feasibility audit. It is not a negative finding about
the routing value of the seven fields, and it does not alter the completed
public-card RQ1b experiment.
