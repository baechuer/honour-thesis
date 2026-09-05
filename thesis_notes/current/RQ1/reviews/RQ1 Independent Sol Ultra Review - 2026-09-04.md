# RQ1 Independent Sol Ultra Review

Date: 2026-09-04  
Status: `ADVISORY REVIEW COMPLETE / SELECTED WRITING REPAIRS APPLIED`  
Reviewer: `gpt-5.6-sol`, `ultra` reasoning, read-only subagent  
Review conditions: local files only; no web search; agent closed after return

## Follow-up implementation

The following review recommendations were applied after the read-only review:

- the public result is now limited to the purposefully selected, removal-eligible groups;
- the controlled summary now reports exposed Top-1 as well as improvement over the hidden baseline;
- the broad causal-attribution wording was replaced with a direct statement about the effect of showing the authored field content;
- the Methodology and Discussion now state that public removals differ in length and can remove text serving more than one function;
- the 29,292-document descriptive review now records 31 batches, `gpt-5.6-terra` with `xhigh` reasoning, the retained evidence, and the absence of retained row-level decisions or a verbatim batch prompt;
- the Discussion now distinguishes the RQ1 information study from SSL, SkillRouter, and SkillRet as representation or retrieval-system work; and
- the two stale joint-group result banners and the single-field twin result banner were corrected.

One concrete controlled intervention example and one concrete public intervention example have now been added to Appendix B. Still pending are later relocation of historical `R*`/`M*`/`B*` detail and completion of the formal AI-use declaration. These are communication and submission tasks, not missing RQ1 experiments.

## Scope

The reviewer read the University of Sydney honours assessment criteria, the current Introduction, Literature Review, Conceptual Framework, Benchmark Design, Methodology, Results, Discussion, Conclusion, RQ1 appendices, the current RQ1 index and writing records, and the named canonical RQ1 result/checkpoint files. The review focused on RQ1 while checking its consistency with the rest of the thesis.

## Verdict

RQ1 supports a defensible, bounded HD-level conclusion. The reviewer found no numerical or methodological error that invalidates the RQ1 experiments and did not recommend another experiment.

The supportable answer is:

- all seven operational fields improved routing within their own controlled suites when the field content was exposed as written;
- in the selected public original-document groups, removing use-condition and success/verification information reduced strict Top-1 under both retrievers;
- input, output, workflow, and dependency had stable effects only for BM25 in that public experiment;
- boundary/not-for had no stable positive public Top-1 effect;
- these findings do not establish a cross-field ranking, a length-independent semantic effect, or universal generalisation to all public skills.

## Findings

### P1: public-sample scope needs clearer qualification

The Methodology already states that the 1,099-source frame was not a random sample, that the 82 groups were purposefully curated, that removal eligibility varies by field, and that researcher review was not blinded. The Discussion and Conclusion should carry those restrictions forward more directly.

- Current locations: `thesis_latex/chapters/05_methodology.tex:35`, `thesis_latex/chapters/07_discussion.tex:91`, and `thesis_latex/chapters/08_conclusion.tex:15`.
- Smallest correction: refer to `the purposefully selected, removal-eligible public groups`, and state that selection and same-researcher confirmation limit external generalisation.
- Consequence: no change to the paired result inside the frozen sample; only the population to which it may be generalised becomes clearer.

### P1: the rendered RQ1 evidence is too compressed

The visible controlled summary reports lift intervals, while the individual tables are inside an inactive LaTeX block. Appendix B does not show a current RQ1 hidden-versus-exposed example or an intact-versus-removed public example.

- Current locations: `thesis_latex/chapters/06_results.tex:51-248`, summary table near line 260, and `thesis_latex/chapters/appendix_b_prompt_examples.tex:3`.
- Smallest correction: add exposed Top-1 to the compact summary and include one controlled before/after example plus one public before/after example.
- Consequence: examiner visibility and auditability only; no change to the numerical conclusion.

### P2: one attribution sentence is too broad

`thesis_latex/chapters/07_discussion.tex:122` says that the controlled clusters support causal attribution. Because field values were not length-normalised, the more accurate statement is that the design supports within-suite attribution to exposing the authored field content as a package, including its amount and specificity.

This is claim calibration, not a rejection of the observed lift.

### P2: public removals are not equal-sized or semantically pure

The thesis already says operational fields overlap, but should also say plainly that removals delete unequal amounts of text and that one line may express more than one operational function. The result is therefore a paired routing-sensitivity estimate, not a length-controlled estimate of an isolated semantic category.

### P2: the 29,292-document review is weakly reproducible

The thesis correctly treats the review as descriptive supporting evidence. Only aggregate summaries and 31 batch totals are locally retained, so the thesis should name the reviewing model, prompt or protocol version, and validation procedure where those details are available, and state that row-level judgements are unavailable for re-analysis.

This affects only the reproducibility of the supporting prevalence evidence. The routing conclusions do not depend on it.

### P2: closest-work comparison should be more explicit

The Literature Review establishes the RQ1 gap, but the Discussion should more directly contrast this thesis's field isolation, examples/tests negative control, and public removal experiment with complete structured representations such as SSL and aggregate retrieval evaluations such as SkillRouter and SkillRet. Source status should remain explicit where work is a preprint or product documentation.

### P2: historical implementation names still interrupt the main story

Detailed `R*`, `M*`, and `B*` labels and historical matrices remain in the Conceptual Framework, Methodology, and later Results. Retaining a short descriptive synthesis in the main text and moving detailed lineage to an appendix would improve RQ1/RQ2 navigation.

### P2: formal AI-use declaration remains unfinished

The chapter-level disclosure is adequate: AI assistance, researcher-defined rules, mechanical checks, and visible-label researcher approval are stated accurately. The formal submission declaration still needs to be completed consistently with that disclosure.

### P3: two checkpoint banners are stale

The joint-group BM25 and Qwen result checkpoints still contain `INDEPENDENTLY VALIDATED`, `NOT IN THESIS PDF`, and, for BM25, `QWEN NOT RUN`. These banners should be replaced with plain current wording: mechanically and source validated, reviewed by the researcher with edits visible, and integrated into the thesis.

## Checks That Passed

- RQ1 is stated consistently in the Introduction and Literature Review and is separated from RQ2 in Methodology.
- The Literature Review presents the seven fields as literature-motivated candidates and does not claim that prior work has already proved their discriminative value.
- Controlled comparisons are paired; prompt variants are handled within cluster; cluster-bootstrap intervals are used; cross-field ranking is rejected.
- Public comparisons keep prompt, candidate set, order, source identity, and gold fixed while removing specified information.
- The thesis explicitly keeps post-removal executability outside RQ1.
- Counts reconcile: 350 controlled clusters, 750 prompts, 402 scored removals, 1,078 composition-family cases, 2,156 prompts, 4,312 rows per retriever, and 946 total researcher-reviewed units.
- Public single-field and joint-group values match their canonical result records.
- AI assistance, researcher review with labels visible, absence of independent blinded review, and the controlled length/detail limitation are disclosed accurately.
- Inspected RQ1 bibliography keys exist, and the current LaTeX log contains no undefined citation or reference diagnostic.

## Rubric Estimate

| Component | RQ1-only estimate | Reviewer rationale |
| --- | ---: | --- |
| Contribution | 33-35 / 40 | Useful paired protocols, negative control, and complementary public intervention. |
| Critical analysis | 25-26 / 30 | Strong evidence boundaries and statistics; public selection and gold-confirmation implications need sharper treatment. |
| Knowledge of the area | 17-18 / 20 | Relevant synthesis; closest-work comparison remains brief. |
| Communication | 7-8 / 10 | Coherent central answer, but evidence compression and historical names hinder examination. |

Plausible RQ1-only range: **82-87, centred around 85**. The reviewer treated this as clear HD quality, not yet independently persuasive as a 90+ Medal case. Uncertainty is approximately three marks because the review was local and file-bounded, with no web verification or fresh row-level semantic audit.

## Recommended Order

1. Narrow the public-population wording.
2. Add exposed accuracy and two concrete intervention examples.
3. Replace the broad causal-attribution sentence.
4. State the unequal-size and multifunctional-line removal limitation.
5. Clarify the retained information and reproducibility limit of the 29,292 review.
6. Add a concise closest-work comparison in Discussion.
7. Move historical implementation detail away from the main story.
8. Complete the formal AI-use declaration.
9. Correct the two stale checkpoint banners.

All nine items are writing, presentation, or provenance repairs. None requires a new RQ1 experiment.
