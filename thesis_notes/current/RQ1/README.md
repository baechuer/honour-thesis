# RQ1 Canonical Index and Review Status

Date: 2026-09-04  
Status: `SCIENTIFICALLY COMPLETE / THESIS-INTEGRATED / RESEARCHER REVIEW COMPLETE / FINAL SUBMISSION EDITING ONLY`

## Research Question

> Which operational information types help distinguish semantically similar but procedurally distinct agent skills?

RQ1 is one research question with two complementary experiments and one negative control. The old names `RQ1a` and `RQ1b` remain in paths only for provenance.

## Closure State

RQ1 is scientifically complete under the current thesis scope. The canonical inputs, selector outputs, paired analyses, researcher review, thesis integration, and communication review are complete. No further RQ1 experiment is required before the thesis proceeds to RQ2, and the canonical RQ1 evidence should now remain frozen unless a genuine error is found.

The remaining RQ1 work is final submission editing only: complete the formal AI-use declaration, optionally move or compress historical implementation detail in the thesis manuscript, and perform a final citation, count, and claim-consistency check. These are presentation and compliance tasks, not missing scientific evidence.

## Current Evidence

| Component | Design | Current evidence | Human-review state |
| --- | --- | --- | --- |
| Controlled field isolation | 7 fields x 50 three-sibling clusters; shared context versus the same context plus one candidate-specific field | 350 clusters, 750 prompts; all 14 field-by-retriever Top-1 lift intervals are positive | The researcher reviewed and approved all 350 rows with the labels visible; this was not an independent blinded review. |
| Examples/tests negative control | 50 three-sibling clusters with shared operational content and only examples/tests varied | Generic examples do not improve routing; rare near-exact matches attract selectors | Supporting controlled result; not an eighth field and not part of public removal. |
| Public original-document removal | Same public originals scored intact and after cited source-line content for one field is blanked in every candidate | 82 source compositions, 1,078 composition-family cases, 2,156 prompts, and 4,312 ranking rows per retriever | The researcher reviewed and approved all 194 scored gold-label cases and all 402 scored removals with the labels or edits visible. |
| Public joint-group removal | Exact unions for task specification, execution/verification, and applicability/capability | Supporting combined-information effects; no single-field attribution or additivity claim | Uses the same underlying gold families and reviewed component transformations. |

## Counting Boundaries

These counts describe different sets and must not be substituted for one another:

| Count | Meaning |
| ---: | --- |
| 1,099 | Preserved public originals in the discovery frame. This is not a scored denominator or a complete human field audit. |
| 82 / 265 | Source-composition registry / candidate originals. |
| 574 | All composition-field transformations generated and technically cleared in Round 3. |
| 439 | Transformations where every candidate received a Round-3 `CLEAR` decision. |
| 402 | All-candidate-clear transformations that also have a paired prompt/gold binding and appear in the scoring freeze. This is the removal-review denominator. |
| 199 | Upstream paired prompt/gold families linked to the registry. |
| 194 | Families that occur in at least one clean scored field condition. This is the public-gold review denominator. Five upstream families never enter a scored condition. |
| 1,078 | Field-specific composition-family cases. A family can appear under several eligible fields. |
| 2,156 | Direct/paraphrase prompt rows: exactly two per case. |
| 4,312 | Full/removed ranking rows per retriever. |

## Human Review

Start here:

`skill_benchmark/rq1_human_review/2026-09-04/README.md`

Decision format and claim rules:

`skill_benchmark/rq1_human_review/2026-09-04/REVIEW_GUIDE.md`

Recommended order:

1. `public_gold/confirmation_packets/public_gold_confirmation_batch_01.md`: compare all candidates and confirm, revise, or exclude the displayed frozen gold.
2. `controlled/confirmation_packets/`: confirm the displayed controlled gold, neighbour plausibility, field isolation, prompt fidelity, and leakage.
3. `public_removal/packets/`: verify source deletion fidelity for the transformations used in scoring.

The review is complete at `946/946`: 350 controlled field-isolation rows, 194 scored public-gold rows, and 402 scored public-removal transformations. Exact approved ranges and instructions are preserved in each stream's `decision_receipts/`, and the reconciled totals are maintained in `skill_benchmark/rq1_human_review/2026-09-04/STATUS.md`. The clear reporting wording is: `reviewed and approved by the researcher with the labels visible` for controlled/public-gold cases, and `field-removal transformations reviewed by the researcher` for removal fidelity. This was not an independent blinded review and does not support inter-rater agreement. The unused gold-hidden packets remain preserved for provenance.

## Supporting Public-Field Evidence

A separate model-assisted review covered all 29,292 complete primary documents in the frozen public-source frame. The retained package contains a summary and 31 batch totals. The researcher has confirmed that this review was completed in another task, so its aggregate rates are accepted as descriptive supporting evidence that the candidate information types recur in public skills. It is not routing evidence and is not presented as a released per-document annotation dataset because the local package does not contain the 29,292 individual judgements.

No separate body-only follow-up was executed or retained as part of the current RQ1 evidence.

## Canonical Files

| Role | File |
| --- | --- |
| Independent RQ1 examiner review | `thesis_notes/current/RQ1/reviews/RQ1 Independent Sol Ultra Review - 2026-09-04.md` |
| Current values and claim limits | `thesis_notes/current/Results Writing Packet - 2026-09-04.md` |
| RQ1 rubric and consistency audit | `thesis_notes/current/RQ1/reviews/RQ1 Marking Criteria Audit - 2026-09-04.md` |
| HD/Medal readiness assessment | `thesis_notes/current/RQ1/reviews/RQ1 HD and Medal Readiness Assessment - 2026-09-04.md` |
| Controlled design | `thesis_notes/current/RQ1/protocols/RQ1 Field Targeted Test Plan.md` (controlled sections only) |
| Controlled target-field length diagnostic | `skill_benchmark/outputs/rq1a_target_field_length_audit_2026-09-04/README.md` and `length_audit.json` |
| Public full-document field-presence summary | `skill_benchmark/outputs/rq1_v3_full_document_binary_review_summary_2026-09-04.md` and its 31-batch totals CSV |
| Public single-field protocol | `thesis_notes/current/RQ1/protocols/RQ1 Public Original Round 3 Clean-Only Scoring Freeze and Test SOP - 2026-09-04.md` |
| Public joint-group protocol | `thesis_notes/current/RQ1/protocols/RQ1 Public Original Round 3 Joint Group Extension SOP - 2026-09-04.md` |
| Public single-field results | `thesis_notes/checkpoints/methods/RQ1 Public Original Round 3 Twin Result and Failure Analysis - 2026-09-04.md` |
| Public group results | `thesis_notes/checkpoints/methods/RQ1 Public Original Round 3 Joint Group BM25 Result - 2026-09-04.md` and `RQ1 Public Original Round 3 Joint Group Qwen Result - 2026-09-04.md` |
| Human-review workspace | `skill_benchmark/rq1_human_review/2026-09-04/` |
| Researcher-review completion checkpoint | `thesis_notes/checkpoints/methods/RQ1 Prospective Researcher Confirmation Complete - 2026-09-04.md` |

## Information Inconsistencies

The following are record or wording inconsistencies, not evidence that the experiment failed. Items marked `RESOLVED` were corrected on 2026-09-04; the count and review boundaries remain active reporting rules.

1. `RESOLVED`: the Abstract described the superseded 46-composition derivative field-card null result. It now reports the public original-document removal experiment and its current findings.
2. `RESOLVED`: trackers called the 460-file recoverability audit or 62-cluster unexecuted wave the current public RQ1 experiment. Current-status banners and tracker front matter now identify them as supporting or historical only.
3. `ACTIVE COUNT RULE`: `199 paired families` names the upstream linked pool, while only 194 families occur in the clean scoring cases.
4. `ACTIVE COUNT RULE`: `574 transformations` names the full technical processing frame; 439 are all-candidate clear, and 402 both satisfy that gate and occur in scored cases.
5. `ACTIVE CLAIM RULE`: `independently validated` can be mistaken for independent human annotation. Say exactly what happened: the files were source-checked and mechanically validated, then reviewed and approved by the researcher with the labels visible. Do not call this review blinded or independent.
6. `RESOLVED / DESCRIPTIVE ONLY`: the completed 29,292-document model-assisted review is accepted as supporting evidence using its retained summary and 31 batch totals. It may support the claim that the candidate information types are common in the sampled public corpus. It must not be used as routing evidence or described as a released per-document annotation dataset.
7. `DOCUMENTED CONTROLLED LIMITATION`: a 350-cluster target-field length audit finds that the gold wording is longer or more detailed in several suites, especially boundary/not-for and dependency/resource. This does not invalidate the hidden-versus-exposed comparison. It means the result measures the practical value of exposing the field content as written, including its amount and specificity, rather than a length-normalised effect of field meaning alone.
8. `RESOLVED AUTHORSHIP WORDING`: controlled units are now described as created with AI assistance under a researcher-defined rubric, mechanically checked, and reviewed and approved by the researcher. They are not described as solely researcher-authored. The formal thesis AI-use declaration still needs to follow the applicable submission rules.

One genuine scientific difference is retained deliberately: the older derivative field-card experiment found no stable individual-field effect, whereas the newer original-document removal experiment finds several stable effects. They use different selector-visible representations and must not be pooled. The older result is a historical sensitivity analysis, not the current headline result.

## Historical and Supporting Records

No RQ1 record was deleted. Current material is grouped under `thesis_notes/current/RQ1/`, while superseded method branches are grouped under `thesis_notes/archive/RQ1/`. Use archived material for provenance only; its old status language does not override this index.

### Current supporting

- `thesis_notes/current/RQ1/protocols/`: the current controlled and public-removal experiment protocols.
- `thesis_notes/current/RQ1/reviews/`: current criteria, readiness, and independent advisory reviews.
- `thesis_notes/current/RQ1/supporting/`: source-accounting material that remains useful but is not a primary experiment.

### Historical method lineage

- `thesis_notes/archive/RQ1/original-document-lineage/`: early full-document pilots, redaction amendments, clearance protocols, and the retrospective review protocol that led to the final Round-3 design.

### Superseded public-card and discovery path

- `thesis_notes/archive/RQ1/superseded-public-card/`: the derivative field-card, public-source discovery, triad, and earlier joint-mask branch. Its completed null and sensitivity findings remain reportable historical context but are not the primary public RQ1 experiment.

See `thesis_notes/archive/RQ1/README.md` for the archive boundary and directory map.
