# RQ1 Public Original-Document Information-Removal Execution SOP

<!-- RQ1-RECORD-STATUS:START -->
> **RQ1 record status (2026-09-04): `HISTORICAL_OR_SUPERSEDED`.** Retained for provenance and method history. Do not use its dated status, denominator, or result as the current RQ1 claim unless the canonical RQ1 index explicitly carries it forward. Canonical index: `thesis_notes/current/RQ1/README.md`.
<!-- RQ1-RECORD-STATUS:END -->



Date: 2026-08-31  
Status: `FULL-ORIGINAL FIELD-REMOVAL FEASIBILITY AUDIT CLOSED / INSUFFICIENT CLEAN DENOMINATOR / NO SELECTOR OR EXTERNAL EMBEDDING EXECUTION`

## Purpose

This SOP executes the approved RQ1 public-original comparison. It asks whether
removing explicitly documented, candidate-distinguishing operational
information from the original public skill documents weakens within-composition
routing. The edited document is a selection-only experimental condition. It
may be incomplete or non-executable and must never be presented as a usable
replacement skill.

The experiment does not claim to remove all knowledge correlated with a field.
It tests the additional routing value of the field values that are explicitly
written in the original documents.

## Frozen Source Scope

The starting input is the 76-composition / 209 strict-family / 408 strict-prompt
public-original roster at:

`skill_benchmark/rq1b_cross_source_public_benchmark/working/masked_execution/p0_master_roster_2026-08-28.json`

Only source paths and hashes declared by that roster may be copied into this
execution. The source-only parse deduplicates repeated prompt families to one
anonymous candidate packet per composition. Prompt text, gold labels, source
provenance, historical selector rows, field-card text, and result files are not
included in the parser packets.

## Conditions

Each score-eligible family will later use the same candidates, prompt, gold
label, tie-break rule, and scorer under:

- `FULL_ORIGINAL`: complete hash-verified original documents.
- `REMOVE_<FIELD>_ORIGINAL`: complete originals after the explicit,
  candidate-distinguishing values of one field have been removed.

The seven single-field conditions are `USE`, `INPUT`, `OUTPUT`, `WORKFLOW`,
`SUCCESS`, `BOUNDARY`, and `DEPENDENCY`. Group-field conditions are created
only after their component single-field removals pass review:

- `REMOVE_TASK_SPECIFICATION_ORIGINAL`: `USE + INPUT + OUTPUT`.
- `REMOVE_EXECUTION_VERIFICATION_ORIGINAL`: `WORKFLOW + SUCCESS`.
- `REMOVE_APPLICABILITY_CAPABILITY_ORIGINAL`: `BOUNDARY + DEPENDENCY`.

Groups are a separate, predeclared comparison of combined documented
information. They are not used to repair an unsuccessful single-field result.

## S0: Source Roster and Anonymous Packets

1. Reconstruct unique compositions from the frozen roster.
2. Verify every original candidate source hash before copying its exact bytes.
3. Materialise one anonymous packet per composition with `candidate_a.md` to
   `candidate_d.md`; copy no prompt, label, provenance, field-card, score, or
   result material into it.
4. Partition the packets into non-overlapping batches of at most three
   compositions for a parser agent.

Failure of a hash, membership, or composition-consistency check stops that
composition before parsing. It does not change the historic roster.

## S1: Source-Only Seven-Field Parse

Each parser agent receives the SOP and only its anonymous source packets. It
does not see prompts, gold labels, source locations, historical curation,
retrieval outcomes, or prior parses.

For every candidate document, the parser records each exact evidence span for:

1. `use_condition`: goal, trigger, or situation in which the skill should be
   chosen.
2. `input_precondition`: input object, format, schema, state, access, quality,
   prerequisite, path, credential, or required prior artefact.
3. `output_artifact`: deliverable, output form, or produced artefact.
4. `workflow_procedure`: required operation, path, order, or transformation.
5. `success_verification`: acceptance check, validation, threshold, or proof.
6. `boundary_not_for`: exclusion, authority limit, prohibited use, or route-out.
7. `dependency_resource`: required tool, runtime, package, version, service,
   permission, environment, or external resource.

The required parse has an inclusive original-source line range, a carrier
(`title`, `heading`, `prose`, `step`, `example`, `code`, `resource`, or
`other`), and one of: `DIRECT_VALUE`, `GENERIC_CONTEXT`,
`CORRELATED_CONTEXT`, or `NOT_PRESENT`. The local validator derives the
official literal quote from the cited lines of the hash-verified source; a
parser never supplies a manually transcribed quote.
It records uncertainty instead of inventing a span. It never names a preferred
candidate or makes a routing judgment.

## S2: Family Field Lock and Removal Map

The coordinator combines the source-only parse with the already frozen strict
family lineage without looking at selector outcomes. A family advances for one
field only if its prompt requirement and its existing strict target are
compatible with an explicit source-only map for that field.

For each advancing candidate, create a removal map that lists every edited span
and its exact replacement. Apply the same field category to every candidate:

- delete a target-only clause, bullet, title fragment, code filename, or block;
- use `[input material]` only where removal would leave a mixed sentence
  ungrammatical; and
- never generalise a restriction. `PDF`, for example, may be deleted or
  neutralised, but cannot become “file” or “any file”.

Task/method names, ordinary workflow prose, outputs, and other non-target
fields remain unless the literal text itself states the target value. The
removal can therefore leave method-correlated information visible. That is
intentional and limits the claim to explicit documented values beyond the
remaining natural text.

## S3: Audits and Freeze

Every provisional removal must pass:

1. source hash and candidate membership preservation;
2. exact diff coverage: each changed byte is in the removal map;
3. target-value residual check by a reviewer blind to prompts, gold, and
   results;
4. no capability expansion;
5. readability check only, not executability; and
6. original/mask/diff human review packet.

Every family is field-specific: it may be eligible for `INPUT` and ineligible
for `WORKFLOW`. A group condition includes only families that pass every
component field audit. A rejected map is recorded as `ORIGINAL_ONLY` for that
field, never silently repaired after a result is known.

## S4: Scoring and Metrics

Only after a score freeze:

1. run local BM25 over each family’s own three or four candidates;
2. run Qwen `text-embedding-v4` only after a separate external-text payload
   approval; and
3. execute the three group conditions after the corresponding single-field
   conditions are frozen.

For each retriever and condition, retain strict Hit@1, MRR, gold rank, native
score, gold-versus-leading-negative margin, original-minus-removed deltas,
winner-transition counts, direct/paraphrase slices, field/group slices, and
composition-clustered paired bootstrap intervals. Prompt variants are repeated
measurements, not independent routing tasks.

The final analysis distinguishes a stable winner with reduced score/margin
from a winner change. A stable Top-1 does not show that the removed information
had no routing value; it can indicate redundancy in the remaining original
text.

## Stop Rules

No selector, API call, hosted job, thesis LaTeX/PDF result write, or claim
update may begin during S0--S3. Any ambiguity about a field definition,
candidate membership, source hash, capability expansion, or residual explicit
value stops the affected field/family and is reported before scoring.

## 2026-08-31 First-Pass Residual-Cue Gate

The first stratified, prompt-blind residual review covered all seven single
fields and all three pre-registered groups across 14 review batches (42
composition-condition items). It found at least one explicit residual in 35
items and no residual in 7. This is a **redaction-map completeness finding**,
not a retrieval result or an RQ1 effect estimate: all selector, query, gold,
and result information remained unavailable to reviewers, and no scoring has
run.

Before S4, any item with `RESIDUAL_FOUND` must receive a second source-only
mapping pass that captures the cited explicit duplicate(s) and any same-field
values in the corresponding candidate documents. The revised maps must again
pass exact-diff reconstruction and a fresh prompt-blind residual review. An
item that remains residual or becomes an unsafe mixed carrier is excluded from
the relevant condition. Only re-cleared items may enter a metric denominator.

## 2026-08-31 Closure

The remediation pass mapped 35 first-pass residual items: 32 received a
supplemental source-line map and 3 were excluded as unsafe mixed carriers. One
additional item was excluded for an edit conflict. The 31 rebuilt masks passed
technical hash/diff audit, then received a fresh prompt-blind residual review
from reviewers that saw only the revised masked documents. That recheck found
`28 RESIDUAL_FOUND / 3 CLEAR` items. The original 7 first-pass-clear items did
not enter this fresh-recheck denominator.

Therefore this full-original field-removal intervention has too few verified
clean composition-condition items to support single-field or group retrieval
metrics. It closes as a feasibility result: complete public skill documents
repeat operational information across sections, making reliable selective
field removal impractical under the current no-capability-expansion rule. This
does **not** estimate a field effect, does **not** show that fields lack routing
value, and does not replace the existing public-card RQ1b experiment. No
selector, external embedding/API call, hosted job, human review packet, or
thesis LaTeX/PDF result write was performed.
