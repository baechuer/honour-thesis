# Methodology Deep Critique and Improvement Plan - 2026-06-05

Purpose: record the detailed methodology critique so future work does not drift into more provider testing without fixing the actual experimental risks.

## Examiner Summary

The methodology is defensible, but the strongest claims currently run ahead of the cleanest evidence. The central risk is conflation: the current experiments can mix together field usefulness, field extraction quality, lexical cue overlap, authored-skill cleanliness, and candidate-budget effects.

The thesis should not claim that the current deterministic field-aware matcher is generally superior to neural skill reranking. The safer and stronger claim is:

> Preserving task/use condition, output, and workflow information improves controlled retrieval among semantically similar skills when that information is available and used field-to-field. Dense retrieval is useful for high-recall candidate generation, but final selection still benefits from explicit procedural evidence. Public-authored skills show that extraction and semantic field matching remain unsolved.

## Priority Fixes

| Priority | Issue | Why it matters | Action |
|---|---|---|---|
| 1 | Candidate-budget unfairness | SkillRouter rerank is currently top-20, while the strongest M6-v1 result is top-100. | Treat top-20 as the fair reranker comparison. Report top-100 M6-v1 as a larger-candidate-budget result unless SkillRouter rerank top-100 is also run. |
| 2 | Missing uncertainty estimates | On 137 prompts, a 3.7 point gain is only about five prompts. | Add confidence intervals and paired tests: McNemar for top-1, bootstrap/randomization for MRR and top-k. |
| 3 | Strict gold vs acceptable alternatives | The evaluator computes strict and acceptable variants separately, but some thesis wording collapses them. | Report strict top-1/top-k as primary. Report gold-or-acceptable separately. |
| 4 | Public-gold false-positive metric | `non-main top-1` is misleading when the gold skill is public/background. | Replace with stratum-aware labels: wrong background, wrong controlled, wrong public wrapper, broad parent/router, duplicate/acceptable. |
| 5 | M6-v1 is lexical | Current field matching is transparent lexical overlap plus cue extraction, not robust semantic understanding. | Name it `M6-v1-local lexical field-aware prototype`. Add request-field parser audit with manual labels. |
| 6 | Field extraction validity | Public skills are messy, and the field-aware method fails on public-gold top-1. | Measure extraction precision/recall by field on a manually annotated public subset. |
| 7 | Length and field-count bias | Cumulative field ablations add more tokens, so gains may reflect more text rather than field identity. | Add matched-token ablations, shuffled field labels, field dropout, and length-normalized scoring. |
| 8 | Boundary/negation brittleness | Current `not_for` handling is regex/token-overlap based. | Build a small negation/contradiction stress set and report boundary-field performance separately. |
| 9 | Public-gold cleanup | Completed as an 82-prompt cleaned public-gold stratum, and provider/SkillRouter reruns are now complete on that stratum. | Use the cleaned 82-case stratum for final public-gold evidence and analyze public-gold failures before final reporting. |
| 10 | Post-hoc field-set choice | Best field set is selected after trying variants. | Use train/dev/test or pre-register the final field set. Otherwise call it exploratory/post-hoc. |

## What Is Currently Supported

Supported:

- The controlled benchmark contains useful semantic-confusion pressure at 2401-skill scale.
- Flat metadata and generic dense retrieval remain brittle under scale and near-neighbour skill overlap.
- Task/use condition, output artifact, and workflow/procedure are the strongest current positive selection fields.
- Dependencies, resources, boundaries, and hierarchy are conditional signals and should not be treated as plain positive text.
- SkillRouter is a strong first-stage candidate generator; candidate recall is high on controlled prompts.
- M6-v1-local can improve controlled ordering when the gold skill is already in a strong candidate set.

Not yet supported:

- That deterministic field matching is generally better than SkillRouter neural reranking.
- That public-authored skills are reliably handled by the current extraction and matching layer.
- That retrieval improvements translate into downstream task success.
- That graph or tree retrieval adds value, because M4/M5 have not been evaluated.

## Methodology Hardening Plan

### A. Freeze a Fair Final Comparison Matrix

Report methods by exact architecture:

- representation: R1, full artifact, R2/R3, R4
- first-stage selector: lexical, dense, SkillRouter
- candidate budget: top-20, top-50, top-100
- reranker: none, neural, M6-v0, M6-v1-local, future semantic M6-v2
- scoring label: strict gold or gold-or-acceptable

Do not compare a top-100 reranker result directly against a top-20 reranker result as if only the reranker changed.

### B. Add Statistical Reporting

For the final method table:

- report 95 percent bootstrap confidence intervals for top-1, top-5, and MRR
- run paired McNemar tests for strict top-1 between selected method pairs
- run paired bootstrap/randomization tests for MRR
- report exact prompt-count difference, not only percentage difference

### C. Audit the Request Parser

Create a manually labelled sample of request fields:

- 20 controlled high-information prompts
- 10 low-information prompts
- 10 implicit-field prompts
- 10 public-gold prompts

For each prompt, label task, input, output, workflow, dependency, boundary, and hierarchy evidence. Compare against M6-v1 extraction. This tells us whether M6-v1 fails because the fields are not useful or because the parser extracts them badly.

### D. Audit Skill-Field Extraction

For public skills, annotate a small subset by field with evidence spans:

- routing trigger
- input/precondition
- output artifact
- workflow/procedure
- dependency/tool
- resource/reference
- boundary/not-for
- hierarchy/link

Compute precision/recall against heuristic and DeepSeek extraction. This protects the thesis from claiming field prevalence based only on keyword heuristics.

### E. Control Length Bias

Run at least three ablations:

- matched-token summaries: keep approximately equal token budgets across field conditions
- shuffled field labels: preserve text but remove correct field assignment
- field dropout: remove one field at a time from a fixed full schema

If full schema improves only because it is longer, the thesis should frame the result as a context/information quantity effect rather than a field-identity effect.

### F. Build Boundary and Negation Stress Cases

Add or isolate prompts where the correct decision depends on:

- explicit "do not use this when..." boundaries
- user requests that exclude a procedure
- skills with similar positive triggers but incompatible negative conditions
- broad parent/router skills that should not be selected as atomic execution skills

Evaluate boundary precision separately from global top-1.

### G. Clean Public-Gold Before Final Claims

Apply the manual adjudication outcomes:

- strict keep cases remain strict
- keep-with-acceptable cases get acceptable-alternative labels
- revise/exclude cases are removed or rewritten

Then rerun public-gold methods and report strict and acceptable scores separately.

## Recommended Next Work Order

1. Patch thesis wording to enforce budget-fair and strict/acceptable reporting.
2. Clean public-gold labels and rerun public-gold summaries.
3. Implement statistical uncertainty for final controlled result tables.
4. Run request-field parser audit.
5. Run matched-token and field-label ablations.
6. Decide whether M6-v2 semantic field matching is needed before M4/M5.
7. Only after those are stable, run downstream validation.
