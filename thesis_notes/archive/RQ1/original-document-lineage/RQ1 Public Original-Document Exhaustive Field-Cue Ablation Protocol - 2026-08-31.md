# RQ1 Public Original-Document Exhaustive Field-Cue Ablation Protocol

<!-- RQ1-RECORD-STATUS:START -->
> **RQ1 record status (2026-09-04): `HISTORICAL_METHOD_LINEAGE`.** Retains the protocol lineage that led to Round 3. Its pending/no-selector status is superseded by the completed Round-3 scoring records. Canonical index: `thesis_notes/current/RQ1/README.md`.
<!-- RQ1-RECORD-STATUS:END -->



Date: 2026-08-31  
Status: `UNIFIED RAW ABLATION PRIMARY / 82-COMPOSITION MAPPING AND EXACT MATERIALISATION COMPLETE / FULL BLIND CLEARANCE PENDING / NO SELECTOR OR EXTERNAL EXECUTION`

## Purpose

This non-overwriting RQ1 branch tests whether routing changes when all textual
carriers of a specified operational information field are removed from complete
public skill documents. It follows the strict 82-registry deletion audit, which
showed that natural documents redundantly express the same information across
titles, descriptions, procedures, examples and resources. The strict audit is
retained as a separability finding; it is not replaced by this protocol.

The new intervention is deliberately exhaustive. A target document may become
incomplete, incoherent or non-executable. That is permitted because the outcome
is routing, not downstream execution. The intervention may delete a mixed
carrier containing non-target text, but it may not invent or broaden a
capability. The resulting condition is called an exhaustive field-cue ablation,
not "the same executable skill minus one field".

## Frozen Source Frame

- Canonical source registry: 82 compositions, 265 hash-verified public original
  skill documents.
- Fields: `use_condition`, `input_precondition`, `output_artifact`,
  `workflow_procedure`, `success_verification`, `boundary_not_for`, and
  `dependency_resource`.
- Joint groups:
  - task specification = use condition + input/precondition + output artifact;
  - execution/verification = workflow/procedure + success/verification;
  - applicability/capability = boundary/not-for + dependency/resource.
- Queries, gold labels, strict-family lineage and selector outputs remain hidden
  until all source transformations and complete-case eligibility decisions are
  frozen.

## Experimental Conditions

For each composition-field or composition-group unit:

1. `FULL`: untouched, hash-verified original candidate documents.
2. `TARGET_ABLATION`: every explicit or semantically equivalent textual carrier
   of the target field is deleted from every candidate document.
3. `DAMAGE_CONTROL_1..3`: when mechanically feasible, three deterministic
   sensitivity controls delete approximately the same number of non-target
   tokens from the same coarse document regions while protecting all mapped
   target carriers. Control feasibility is reported but is not an inclusion
   gate for the unified primary analysis.
4. `JOINT_ABLATION`: the union of all exhaustive single-field carrier spans in a
   pre-specified group, applied once to the original document.

Only deletion is allowed. No semantic replacement, summary, paraphrase, neutral
filler or generated capability statement may be inserted. Formatting-only
repair is permitted only when it adds no lexical content.

## Exhaustive Source-Only Mapping

A mapper receives anonymous original documents, the target-field definition and
the output schema. It receives no prompt, label, candidate role, source name,
historical card or result. It must map every span from which a reader could
recover a candidate-specific target-field value, including carriers in:

- title and frontmatter;
- description and trigger language;
- requirements, procedures and validation instructions;
- examples, commands, code comments, tables and troubleshooting;
- references, assets, companion skills and resource names.

Each mapped span records exact source lines and quote, deletion action, rationale
and any collateral operational fields also carried by the span. Cross-field
overlap is allowed and must be recorded. A document may be reduced to a stub or
empty body. `NO_TARGET_CUE` is allowed only when an independent source-only
review confirms that no candidate-specific target value exists.

## Target-Clearance Gate

After exact-diff materialisation, a fresh reviewer receives only anonymous
target-ablated documents and the target-field category. Every candidate in the
composition must be `CLEAR`; any residual or uncertainty excludes that
composition-condition. Residual evidence requires an exact masked-document quote
and line range.

This gate is intentionally semantic. It does not reject a mask merely because
the document is damaged or non-executable.

## Damage-Matched Controls

Controls are generated locally after the exhaustive target map is frozen.
Target spans are protected. Eligible non-target tokens are sampled with three
fixed seeds, stratified over frontmatter/early body/middle body/late body so that
deletion is not concentrated in an easy section.

For each candidate and control replicate:

- total removed proxy tokens must be within `max(5, 10%)` of the target-mask
  deletion count;
- each document-region deletion count must reach at least 90% of its target-mask
  counterpart unless that region lacks enough unprotected tokens;
- no mapped target carrier may be altered;
- the resulting control must retain independently identifiable target-field
  information.

If fewer than two of three controls pass for any candidate, the
composition-condition is tagged `NO_MATCHED_CONTROL`. It remains in the unified
`FULL` versus `TARGET_ABLATION` primary analysis, but it cannot contribute to
the damage-adjusted sensitivity estimate.

Documents whose target mask removes at least 70% of proxy tokens or leaves fewer
than 100 proxy tokens are tagged `NEAR_EMPTY`. They remain in the frozen ledger
but require a sensitivity analysis excluding them.

## Pilot and Expansion Gate

The local pilot uses `OR82-006` (three candidates) and `OR82-017` (four
candidates). Both support all seven single fields and all three joint groups in
the existing source frame. The pilot covers 14 single-field units; the six joint
units are derived from their frozen single-field maps.

Expansion to all 82 compositions requires:

1. exact original hashes and exact reconstruction for every pilot mask;
2. target clearance for every candidate in at least one pilot unit per field;
3. damage-control feasibility and target-retention status reported without
   silently excluding high-density fields;
4. correct joint-span union and overlap handling for all three groups; and
5. no access to prompts, labels or retrieval results during mapping and review.

If a field lacks matched controls in both pilot compositions, it remains in the
unified ablation study and is explicitly marked high-density/unmatched. This is
not treated as evidence of an independently isolated field effect.

## Pilot First-Clearance Checkpoint

All 14 source-only single-field maps passed independent Terra xhigh review,
main-thread validation and canonicalisation. Exact local materialisation then
produced 14 single-field units, six derived joint units and 70 candidate masks;
the reconstruction and registered-diff audit passed with zero failures.

A fresh Terra xhigh review saw only each target category and its anonymous
target-ablated documents. Four of 14 units were fully `CLEAR` and ten retained
at least one target cue. Across the 49 candidate masks, 22 were `CLEAR`, 27 were
`RESIDUAL`, and none was `UNCERTAIN`. The fully clear units were `EXA-P004`
(workflow/procedure), `EXA-P011` (workflow/procedure), `EXA-P012`
(success/verification), and `EXA-P013` (boundary/not-for).

This is a map-completeness gate, not a routing result. The ten residual units
must receive source-only addenda derived from their exact masked-document
evidence, fresh materialisation, and a new blind clearance review. They do not
enter damage-control construction or scoring in their present state.

## Pilot Remediation and Damage-Control Gate

The ten residual units were remediated without prompts, labels or selector
results. Six cleared in round two and the remaining four cleared in round
three. The frozen final ledger therefore contains 14/14 clear single-field
units and 49/49 clear candidate masks. Clearance-round counts are four in round
one, six in round two and four in round three.

Three deterministic local controls were then materialised for every candidate,
giving 147 candidate-control documents. Six of 14 units meet the mechanical
requirement that every candidate has at least two valid replicates. At least
one pilot unit is mechanically eligible for use condition, input/precondition,
success/verification, boundary/not-for and dependency/resource. Neither
output/artifact nor workflow/procedure is eligible in either pilot composition.

The failure is insufficient unprotected text, not a reconstruction or target-
protection error. For example, `EXA-P003` candidate B removes 166 target tokens
but has only 37 eligible non-target tokens; `EXA-P011` candidate D removes 746
target tokens but has only 633 eligible non-target tokens. Under the prospective
unified amendment, these cases remain primary ablations because the natural
integration of the field with the document is part of the phenomenon being
measured. The tolerance is not lowered. Their removed-token count, removed
fraction, near-empty status and lack of matched control must accompany every
reported routing effect.

## Future Scoring and Claims

No selector is authorised by this protocol. A later frozen complete-case stage
uses one primary comparison for every target-clear unit: `FULL` versus
`TARGET_ABLATION`, using paired native scores, gold-versus-best-distractor
margins, Top-1 and MRR.

Where valid controls exist, it additionally reports supporting sensitivity
comparisons for `DAMAGE_CONTROL` versus `TARGET_ABLATION` and joint ablation
versus its damage-matched control. These do not define a separate research
question, experiment population or primary result.

The primary estimate is the paired routing change after all carriers of one
information field are removed from the natural document. It measures reliance
on that information family as naturally encoded, including inseparable mixed
carriers; it is not described as a perfectly isolated slot-level causal effect.
Results must report removed tokens, removed fraction, near-empty status, field
and composition. Damage-adjusted estimates are supporting evidence where
available. Controlled RQ1 remains the cleaner isolated-field sufficiency test.
