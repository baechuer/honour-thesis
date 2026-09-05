# RQ1 Marking Criteria Audit

<!-- RQ1-RECORD-STATUS:START -->
> **RQ1 record status (2026-09-04): `CURRENT_CANONICAL`.** Current rubric audit and inconsistency register after completion of the prospective researcher-confirmation ledgers. Canonical index: `thesis_notes/current/RQ1/README.md`.
<!-- RQ1-RECORD-STATUS:END -->



Date: 2026-09-04  
Scope: RQ1 only  
Decision: `APPROVED WITH DOCUMENTED LIMITATIONS - CORE RQ1 EXPERIMENTS VALIDATE; EXAMINER-FACING COMMUNICATION HAS BEEN SIMPLIFIED`

## 1. Review Basis

This audit applies the supplied University of Sydney Honours thesis criteria in `thesis_reference/usyd_honours/hons_thesis_assessment_criteria_2014.pdf`. The four dimensions are contribution (40), critical analysis (30), knowledge of the area (20), and communication (10). The document is dated 2014, so current Canvas, School of Computer Science, and supervisor requirements take precedence.

No numerical mark is assigned here. The purpose is to test whether the current RQ1 evidence and writing exhibit the qualities named by the rubric and to identify inconsistencies that would prevent a fair examiner reading.

RQ1 is:

> Which operational information types help distinguish semantically similar but procedurally distinct agent skills?

## 2. Canonical RQ1 Evidence

RQ1 is one research question answered through two complementary experiments and one negative control.

### Descriptive public-field premise: accepted supporting evidence

- A completed model-assisted binary review covered 29,292 complete public primary documents and found field-presence rates of 64.91--83.34%.
- The review was completed in 31 batches in another task. The retained local package contains the prose summary and all 31 batch totals, and the researcher has confirmed that the review was completed.
- These aggregate results may support the descriptive claim that the proposed information types are common in the sampled public corpus. They do not test routing value and are not presented as a released per-document annotation dataset because the local package does not include the 29,292 individual judgements.
- A separate deterministic 29,292-row surface-cue census measures literal headings and phrases only. It answers a narrower question and is not a replacement for the model-assisted full-document review.
- The later optional body-only audit was not run. It asks a different, narrower question and does not invalidate the completed full-primary-document review.

### Experiment 1: controlled field isolation

- Seven field suites: use condition, input/precondition, output/artifact, workflow/procedure, success/verification, boundary/not-for, and dependency/resource.
- Each suite contains 50 three-sibling clusters created with AI assistance under a researcher-defined rubric, mechanically checked, and reviewed and approved by the researcher.
- The hidden condition exposes sibling-identical shared context. The exposed condition adds exactly one candidate-specific field value.
- The core total is 350 clusters and 750 prompt variants.
- BM25 and Qwen `text-embedding-v4` are the primary retrieval methods. Reasoning selectors are diagnostics.
- All fourteen field-by-retriever hidden-to-exposed Top-1 lifts have positive cluster-bootstrap intervals.
- This supports controlled field sufficiency. It does not show public prevalence or prove that a field is uniquely necessary in a natural document.

### Experiment 2: public original-document removal

- The discovery frame contains 1,099 preserved public original documents and an 82-composition source registry.
- The clean scoring frame contains 1,078 composition-family cases, 2,156 direct/paraphrase prompt rows, and 4,312 paired ranking rows per retriever.
- Each comparison holds prompt, candidates, candidate order, source identity, and strict gold label fixed, then removes every cited source line carrying one named field from every candidate.
- Each field has a separate clean denominator of 49-69 source compositions.
- Use condition and success/verification have stable positive Full-minus-removed Hit@1 effects under both BM25 and Qwen.
- Input/precondition, output/artifact, workflow/procedure, and dependency/resource are positive under BM25 but indeterminate under Qwen.
- Boundary/not-for has no stable positive Top-1 effect under either retriever.
- Joint removal of task specification and execution/verification is stable under both retrievers; applicability/capability is stable only under BM25.
- This supports the claim that removing documented operational information can weaken routing in natural artifacts. It does not establish executability after editing, universal field necessity, or a unique human rationale for every label.

### Negative control: examples/tests

- Fifty controlled clusters share the same operational information and differ only in examples/tests.
- Generic prompts do not improve when examples are exposed; rare exact or near-exact request-example matches attract every tested selector.
- Examples/tests are therefore support information and a negative control, not an eighth core routing field.
- No public-original examples/tests removal experiment was run.

The canonical writing source is `thesis_notes/current/Results Writing Packet - 2026-09-04.md`. The canonical public-original result source is `thesis_notes/checkpoints/methods/RQ1 Public Original Round 3 Twin Result and Failure Analysis - 2026-09-04.md`, together with the two Round-3 joint-group checkpoints. The 2026-08-30 derivative field-card ablation is historical sensitivity only and must not be pooled with the public-original result.

## 3. Rubric Assessment

### Contribution: strong foundation, but the contribution must be stated more cleanly

Current strengths:

- RQ1 addresses a concrete gap: prior work motivates structured operational information but does not isolate which information types distinguish near-neighbour skills.
- The controlled hidden-versus-exposed design is a clear mechanism test.
- The public-original removal experiment is a valuable realism check because it operates on preserved natural artifacts and keeps each comparison paired.
- The negative control prevents the thesis from claiming that every part of a skill document is useful for routing.
- The results are analysed to a bounded conclusion rather than presented as a simple leaderboard.

Current weakness:

- The thesis must make the reusable contribution explicit: a field-isolation protocol, a source-grounded removal protocol, and evidence that field usefulness depends on both field type and retriever. The novelty is this diagnostic method and evidence, not the invention of the seven-field schema.

Assessment: the two routing experiments have the ingredients expected of a strong Honours contribution, and researcher review is complete. The 29,292-document review is now correctly limited to descriptive supporting evidence, so it is no longer a submission hold.

### Critical analysis: currently the strongest RQ1 dimension

Current strengths:

- Controlled sufficiency is separated from public-document importance.
- Positive, conditional, indeterminate, and negative-control findings are distinguished.
- Confidence intervals use the cluster or source composition as the resampling unit rather than treating prompt paraphrases as independent tasks.
- Countervailing improvements after removal remain in the result rather than being discarded.
- Native BM25 and cosine margins are kept on separate scales.
- The text states that removal can make a skill incomplete or non-executable and that strict-label agreement is not universal downstream correctness.

Required strengthening:

- Do not rank fields globally from the controlled point estimates. Each field uses a separately authored 50-cluster suite, so differences between field magnitudes can reflect suite difficulty, prompt design, vocabulary, or domain mix. The valid primary claim is within-field hidden-versus-exposed lift.
- Report the controlled-suite target-field length/detail diagnostic. A longest-field heuristic receives tie-aware Top-1 credit of 1.000 for boundary/not-for and 0.760 for dependency/resource, with smaller associations for input/precondition (0.607), use condition (0.593), and output/artifact (0.490). This does not show that BM25 or Qwen used length, and it does not erase the paired lift. It means the experiment estimates the practical value of exposing field content as written, including its amount and specificity, rather than a length-normalised effect of field meaning alone. A matched sensitivity set could strengthen later work but is not required for the current bounded claim.
- Define the public-removal estimand precisely. It measures the effect of deleting every mapped line assigned to a field while holding the remaining document fixed. The amount removed varies, and one line can serve more than one semantic function, so it is not an equal-length or perfectly isolated field-token intervention.
- Treat the many 95% bootstrap intervals as descriptive stability intervals over the frozen cluster/composition sets unless a multiplicity-controlled confirmatory family is declared. Avoid using `statistically significant` as a global field-discovery claim.
- Compare the RQ1 findings directly with the closest skill-representation literature in the Discussion, especially SSL-style fields and work that reports full-body or structured-skill retrieval. The literature review motivates the gap, but the Discussion currently gives only a short SSL comparison.
- Explain the BM25/Qwen divergence as an observed interaction, not a settled causal mechanism. Lexical dependence, semantic redundancy, document pooling, and distributed duplicate evidence are plausible explanations; this experiment does not choose one conclusively.
- State clearly that joint-group removal demonstrates combined routing value but cannot allocate that effect to member fields or prove additivity.
- Keep the review boundary visible: model-assisted and source checks exist, and the researcher has reviewed and approved all 946 units. Labels or intended edits were visible, so this was not independent blinded annotation.

Assessment: the analysis is careful and appropriately bounded at the experiment level. It will align more strongly with the top rubric band after cross-suite ranking, removal-estimand, and interval-language limits are explicit and the result is compared directly with similar work.

### Knowledge of the area: well connected to RQ1

Current strengths:

- The literature review distinguishes skills from documents and atomic tools.
- It connects procedural-memory, skill-system, scalable retrieval, public ecosystem, SSL, tool retrieval, hierarchy, graph, and RAG work to the thesis problem.
- It explicitly identifies what prior work contributes and what it leaves unresolved for RQ1.
- It avoids claiming that the operational field taxonomy is wholly novel.

Remaining boundary:

- The 29,292-document result is descriptive supporting evidence from a completed 31-batch model-assisted review. Because reusable per-document labels are not in the local package, it should not be presented as a released annotation dataset.
- This repository-only audit verifies that the cited literature is used coherently; it does not certify that every key paper in the fast-moving 2026 literature has been found. A final source-status and claim-to-citation audit should distinguish peer-reviewed work, preprints, and product documentation and verify the strongest novelty wording.

Assessment: the RQ1 literature spine is relevant and synthesised rather than being a list of papers. The final novelty sentence still needs a deliberate source audit before submission.

### Communication: main story is now consistent; compression remains

Current strengths:

- RQ1 is phrased consistently in the Introduction, Literature Review, Methodology, Results, and Conclusion.
- The Results chapter clearly separates the controlled and public-original interventions.
- Tables report denominators, effect direction, and confidence intervals.
- The Conclusion gives a bounded answer and includes the examples/tests qualification.

Current weaknesses:

- Long chronological trackers still contain obsolete experiments below their current-status banners. They are now labelled as history, but they remain poor entry points for a new reader; the canonical RQ1 index must remain the first link.
- The previous RQ1 Results section repeated a full table and interpretation for every field. The main text has now been compressed to one synthesis table, while detailed tables remain preserved in source/repository records.
- The controlled synthesis must not imply a formal strongest-to-weakest ranking because the seven fields use different cluster suites. The revised prose now states this directly.
- Validation terminology must remain disciplined after the 946-unit prospective review: it supports researcher confirmation, not blinded or independent annotation. Final counts are maintained in the review workspace `STATUS.md`.

Assessment: the main RQ1 story is now coherent and substantially more examiner-facing. The revised pages have been compiled and visually checked. Remaining communication work is ordinary final editing: the formal AI-use declaration and final verification of the closest-work citations.

## 4. Findings Ordered By Priority

### RESOLVED: the 29,292-document review has a limited supporting role

Resolution: the researcher confirmed that the full-primary-document model-assisted review was completed in another task. The retained summary and 31 batch totals are accepted for the descriptive claim that the candidate information types are common in the sampled public corpus.

Boundary: the table is not routing evidence and is not described as a released per-document annotation dataset. The absent local row-level label package is a reuse limitation, not a reason to discard the completed aggregate review.

### RESOLVED: controlled results support within-field effects, not a formal field ranking

Previous text labelled some fields the `strongest controlled first-pass signals` and others `conditional or reasoning-heavy`.

Resolution: the thesis now states that every field produced positive within-suite hidden-to-exposed lift, then reports prompt and retriever qualifications. It explicitly says that the seven separately authored suites do not rank fields against one another.

Reason: the intervention is tightly paired within a field, but not matched across fields.

### DOCUMENTED P2 LIMITATION: several controlled suites contain a gold-field length/detail cue

Evidence: a reproducible audit of all 350 controlled units counts whitespace-delimited words only in the candidate-specific target-field value. The gold is uniquely longest in 50/50 boundary clusters and 37/50 dependency clusters. A tie-aware longest-field diagnostic reaches 1.000 and 0.760 Top-1 respectively; it also reaches 0.607 for input/precondition, 0.593 for use condition, and 0.490 for output/artifact. Success/verification (0.260) and workflow/procedure (0.320) do not show this pattern. The report and all cluster rows are stored under `skill_benchmark/outputs/rq1a_target_field_length_audit_2026-09-04/`.

Resolution: the thesis now says that exposing candidate-specific field content improved routing in each authored suite, while field length and detail can vary with the information. The study therefore measures the practical value of exposing the information as written, not a pure length-normalised semantic effect. A matched sensitivity set is optional future strengthening rather than required repair.

Reason: the hidden/exposed intervention remains valid, but the authored gold values are systematically richer in several suites. This threatens semantic isolation, especially for cross-field comparisons, even though a length heuristic is not the same algorithm as BM25 or Qwen.

### RESOLVED: public removal has an explicit intervention boundary

The thesis now says that edited documents may be incomplete, different removals delete different amounts of text, and one line may carry more than one function.

Resolution: the estimate is described as the change after deleting all cited source lines mapped to that field. Single-field and group removals remain separate.

Reason: this preserves the value of the natural-artifact intervention without claiming cleaner isolation than the documents allow.

### RESOLVED: interval language remains descriptive across the family of comparisons

Resolution: RQ1 uses `95% cluster/composition bootstrap interval` and `stable positive direction in this frozen set`. It does not use a global significance claim or treat all comparisons as one discovery test.

Reason: no familywise hypothesis-testing plan was frozen for RQ1, and the thesis does not need one if the intervals are presented as effect-size uncertainty with disciplined claim boundaries.

### RESOLVED P0: abstract reported the wrong public RQ1 experiment and conclusion

Current text: a 46-composition field-card study with no reliable single-field effect.

Resolution: the Abstract now describes the 82-composition public-original registry and clean paired removal frame, reports the current cross-retriever and retriever-conditional findings, and omits the old field-card null from the headline result.

Reason: an examiner should not encounter mutually incompatible headline results before reaching Chapter 6.

### RESOLVED P1: the active RQ1 tracker was superseded

Current text: RQ1a, a 460-artifact supporting audit, and a 62-cluster frozen but unexecuted RQ1b wave.

Resolution: a unified current RQ1 block and canonical index now identify controlled field isolation, the examples/tests negative control, and public original-document removal. The 460-file and 62-cluster records remain preserved under explicit historical/supporting status.

Reason: other tasks and future edits use the tracker as a source of truth; stale status can reintroduce discarded experiments into the thesis.

### RESOLVED P1: Benchmark Design omitted the second RQ1 experiment

Resolution: the chapter now includes a public-original benchmark subsection covering provenance, the 82-composition registry, strict labels, count boundaries, paired full/removed documents, direct/paraphrase grouping, and the routing-only non-executability boundary.

Reason: readers should understand where the evaluation population came from before seeing the Methodology and Results.

### RESOLVED P1 / ACTIVE LIMITATION: validation wording overstated independence

Resolution: current thesis-facing text says exactly which checks were automatic, model-assisted, or completed by the researcher. All 946 researcher-review units are approved. The researcher saw the labels or intended edits, so confirmation bias and the absence of independent agreement remain limitations rather than unfinished work.

Reason: this is both a methodological validity issue and a communication issue.

### RESOLVED: controlled and public conclusions use experiment-specific wording

Resolution: the Results, Discussion, and Conclusion now separate within-suite controlled effects, public effects found under both retrievers, and public effects found only under BM25.

Reason: input/precondition and output/artifact are very strong in controlled clusters but are not stable Qwen effects in public originals. One unqualified global field ranking would hide that difference.

### P2: historical evidence should not occupy the main RQ1 path

Required correction: preserve old artifact names and internal `rq1a` labels for provenance, but use `controlled RQ1 experiment` and `public-original RQ1 experiment` in thesis prose. Move obsolete field-card details to a compact historical note or appendix.

Reason: provenance should remain reproducible without forcing the examiner to reconstruct the project's evolution.

### P2: literature-to-result comparison should be more explicit

Required correction: add one focused Discussion paragraph comparing what RQ1 adds beyond overall structured/full-body retrieval results: field-specific controlled evidence, a negative control, and public-source removal with retriever-dependent effects.

Reason: the marking criteria explicitly reward comparison with similar work and explanation of broader importance.

### P2: reasoning-selector diagnostics should not carry the primary RQ1 claim

Required correction: keep DeepSeek and Codex rows clearly labelled as diagnostics of field intelligibility. Unless their exact prompts, model versions, settings, batch outputs, and scoring logic are packaged for reproduction, do not use their near-perfect values as confirmatory evidence.

Reason: BM25 and Qwen provide the reproducible primary retrieval comparisons; the reasoning rows answer a narrower question and can distract from the paired design.

### P2: examples/tests is an attraction diagnostic, not ordinary accuracy

Required correction: keep generic rows as `no unique operational gold` and report ambiguity/attraction behaviour rather than presenting 33.3% as conventional chance accuracy. Exact-match rows estimate how strongly examples can steer selection, not whether the selected skill is uniquely correct.

Reason: this is a useful negative control only when its endpoint is described accurately.

### RESOLVED: RQ1 construction provenance and AI assistance are disclosed

Previous text called the controlled units `researcher-authored`, while the frozen unit metadata records generated drafts and the repository documents AI-assisted construction and diagnostics. The researcher directed the design and reviewed all 350 controlled units, but that does not make the initial text generation solely human-authored.

Resolution: the thesis now says plainly that the controlled units were created with AI assistance under a researcher-defined rubric, mechanically checked, and reviewed and approved by the researcher. Public curation is likewise identified as model-assisted and source-grounded. The formal declaration still needs to follow the applicable University/unit wording before submission.

Reason: this is an authorship-provenance and communication requirement, not a criticism of using model assistance. The disclosure must match the actual construction process.

## 5. Recommended RQ1 Revision Sequence

1. `COMPLETE`: retain the 29,292-document result only as descriptive supporting evidence from 31 recorded batches.
2. `COMPLETE`: preserve the approved 350 controlled, 194 public-gold, and 402 public-removal review rows and receipts.
3. `COMPLETE`: report controlled effects within each field suite rather than ranking fields globally.
4. `COMPLETE`: disclose the target-field length/detail association as a limitation; no rerun is required for the bounded practical-exposure claim.
5. `COMPLETE`: state exactly what public removal deletes and what it does not prove.
6. `COMPLETE`: describe bootstrap intervals as uncertainty summaries over frozen units rather than a global significance screen.
7. `COMPLETE IN RQ1 PROSE`: disclose AI-assisted construction and researcher review; the formal thesis declaration remains a submission task.
8. `IN PROGRESS`: keep one direct RQ1 answer and one focused comparison with the closest literature.
9. `COMPLETE`: compress the seven detailed controlled sections into one examiner-facing synthesis while preserving detailed source records.
10. `IN PROGRESS`: recompile and visually inspect the revised RQ1 pages, then complete final source and wording checks.

## 6. Approval Boundary

The completed review records researcher confirmation but does not convert it into blinded or independent human annotation, and it does not change any RQ1 score or historical artifact. The controlled and public-removal result artifacts validate. The 29,292-document result is admitted only as descriptive supporting evidence, not as routing evidence or a released annotation dataset. The current readiness judgement is recorded separately in `thesis_notes/current/RQ1/reviews/RQ1 HD and Medal Readiness Assessment - 2026-09-04.md`.

## 7. Current Verification Record

- The prospective review workspace contains 350 controlled, 194 public-gold, and 402 public-removal rows; all `946/946` are approved. Final counts are maintained in `skill_benchmark/rq1_human_review/2026-09-04/STATUS.md`; exact batch decisions are preserved under each stream's `decision_receipts/`.
- The active controlled/public-gold route contains 24 confirmation packets with frozen gold visible; the 24 parallel gold-hidden packets are preserved but are not the user-selected workflow.
- All three canonical exact-diff audit stages pass with zero listed failures.
- All 402 scored public-removal review units pass the additional line-preserving blanking-only check.
- Gold-key field names occur in none of the controlled or public-gold blind packet files.
- All 29 top-level `RQ1*.md` records carry a current/supporting/historical status banner; the canonical index remains the entry point.
- `thesis_latex/main.pdf` was recompiled after the RQ1 communication revision on 2026-09-04. It has 112 pages, no undefined references, citations, or fatal errors. Targeted visual checks of the RQ1 benchmark, Results, and Discussion pages found no clipping, overlap, or broken tables.
- The controlled uncertainty re-analysis passes with 14 summary rows and 700 field-by-retriever cluster rows. The public single-field freeze validates at 1,078 cases and 2,156 prompts; twin synthesis and both joint-group analyses pass.
- The completed 29,292-document model-assisted review is retained as descriptive supporting evidence through its summary and 31 batch totals. The local package does not contain reusable per-document labels, so the thesis does not present it as a public annotation dataset. The separate deterministic surface-cue census remains a narrower literal-recoverability check.
- The controlled target-field length audit covers all 350 operational-field clusters and records both aggregate and cluster-level rows. It identifies a material gold-length/specificity cue in several suites, strongest for boundary/not-for and dependency/resource.
- The thesis declaration and acknowledgements are still placeholders. Before submission, the controlled benchmark must not be described as solely `researcher-authored`; the final disclosure must follow the current University/unit AI-use requirements.
