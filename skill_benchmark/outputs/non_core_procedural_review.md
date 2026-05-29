# Non-Core Procedural Review

Superseded note: this earlier review was based on the pre-cleaned 26 semantic-over-gold cases. Use `non_core_human_adjudication.md` and `all_non_core_procedural_review.md` for the current cleaned-export human adjudication.

This report reviews the 26 prompts where the MiniLM description-card similarity check found a non-core skill scoring above the gold core skill.

Purpose: determine whether those non-core skills are actually better procedural fits, or whether they are useful semantic distractors.

## Overall Status

- Reviewed non-core-over-gold cases: 26
- Clear semantic distractors, not better procedural fits: 19
- Borderline or acceptable-but-not-gold procedural fits: 7
- Clear cases where the non-core skill is strictly better than the gold skill: 0

Interpretation: the 1006-skill benchmark is creating real semantic confusion. Most non-core winners are not better skills; they are plausible description-level false positives. However, several cases are borderline enough that they should be treated carefully in final evaluation, especially if using strict top-1 accuracy.

## Decision Rules

- `safe distractor`: the non-core skill shares surface vocabulary but has the wrong input, output artifact, workflow, or success criterion.
- `borderline`: the non-core skill could plausibly complete the task, but the controlled gold skill is more specific to the benchmark cluster.
- `problem`: the non-core skill is at least as procedurally correct as the gold skill and should be added as an acceptable alternative, removed from the scale set, or handled with graded relevance.

## Summary Table

| Prompt | Gold | Best non-core | Decision | Reason |
|---|---|---|---|---|
| `web_p2_form_filling` | `web-form-filler` | `finance-ops-acceptance-test-builder` | safe distractor | The prompt asks for delegated browser form completion; acceptance-test generation is the wrong artifact. |
| `web_p3_ui_test` | `web-ui-tester` | `email-ops-acceptance-test-builder` | safe distractor | The prompt asks for UI behavior validation, not acceptance-test writing for email workflows. |
| `code_p1_local_code_review` | `code-reviewer` | `email-ops-acceptance-test-builder` | safe distractor | The prompt asks for code risk review before commit; email acceptance checks are unrelated procedurally. |
| `code_p6_release_notes` | `release-note-writer` | `security-ops-failure-diagnoser` | safe distractor | The prompt asks for user-facing release notes, not failure diagnosis. |
| `data_p3_validation` | `data-analysis-with-validation` | `dataset-ops-quality-auditor` | borderline | The non-core skill could audit dataset quality, but the gold skill is the controlled spreadsheet-analysis validation skill. |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | `media-ops-failure-diagnoser` | safe distractor | The prompt asks for spreadsheet/data driver analysis; media failure diagnosis is the wrong domain and artifact. |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | `priority-sorter` | borderline | Both can rank options, but the gold skill is tied to spreadsheet evidence and decision-risk checks. |
| `doc_p1_document_summary` | `document-summariser` | `travel-ops-summary-writer` | borderline | The source is a travel-policy document, so the non-core skill is semantically plausible; the gold skill is still the intended general document summarisation procedure. |
| `doc_p2_document_rewriter` | `document-rewriter` | `travel-ops-rewrite-editor` | borderline | The source is a travel request note and both involve rewriting; the gold skill is the controlled document-rewriting skill. |
| `doc_p3_document_normaliser` | `document-normaliser` | `travel-ops-rewrite-editor` | safe distractor | The prompt explicitly asks for structural normalisation while preserving wording, not prose rewriting. |
| `doc_p4_field_extraction` | `document-field-extractor` | `receipt-extractor` | safe distractor | The source is an invoice and asks for general reusable document fields; receipt extraction is close but narrower and wrong for invoice-specific fields. |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | `privacy-policy-drafter` | safe distractor | The prompt asks for a comparison matrix, not policy drafting. |
| `obs_p6_incident_summary` | `incident-summary-writer` | `incident-ops-summary-writer` | borderline | This is a near-duplicate by procedure and domain; gold remains more specific to the controlled observability cluster. |
| `news_p2_briefing` | `news-briefing-writer` | `events-ops-summary-writer` | safe distractor | The prompt asks for a news decision memo with current-state and significance framing, not generic event summarisation. |
| `news_p3_grounded_claims` | `source-grounding-extractor` | `product-ops-evidence-grounder` | borderline | Both can ground claims in evidence, but the gold skill is source-grounding over article claims rather than product-ops evidence review. |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | `meeting-ops-summary-writer` | safe distractor | The prompt asks for a meeting-use agenda, not a summary of past meeting material. |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | `meeting-ops-summary-writer` | borderline | The non-core skill may summarize decisions, but the prompt specifically asks to extract next actions and unresolved attention items. |
| `read_p2_general_source_summary` | `general-source-summariser` | `research-ops-evidence-grounder` | safe distractor | The prompt asks for a plain-language source report, not claim-evidence grounding. |
| `read_p5_method_notes` | `method-note-builder` | `thesis-ops-summary-writer` | safe distractor | The prompt asks for method/evaluation/assumption notes, not a thesis operations summary. |
| `sec_p1_threat_model` | `security-threat-modeler` | `security-ops-resource-linker` | safe distractor | The prompt asks for assets, actors, abuse scenarios, mitigations, and residual risk; resource linking is the wrong output. |
| `sec_p2_security_code_review` | `security-code-reviewer` | `api-ops-rewrite-editor` | safe distractor | The prompt asks for security review of an API handler, not rewriting API material. |
| `skill_p1_find_existing` | `skill-finder` | `meeting-ops-rewrite-editor` | safe distractor | The prompt asks to search and decide whether an existing skill covers a workflow, not rewrite meeting text. |
| `skill_p2_install_existing` | `skill-installer` | `public-xlsx` | safe distractor | The public spreadsheet skill is the object being installed, not the installation procedure itself. |
| `skill_p4_edit_existing` | `skill-editor` | `course-ops-field-extractor` | safe distractor | The prompt asks to revise a skill boundary, not extract fields from course material. |
| `skill_p5_evaluate_existing` | `skill-evaluator` | `email-polisher` | safe distractor | The prompt asks to evaluate whether a reply-polishing skill triggers appropriately, not polish an email. |
| `skill_p6_package_existing` | `skill-packager` | `docs-ops-summary-writer` | safe distractor | The prompt asks to prepare a skill for sharing, not summarize document content. |

## Implications

The benchmark is healthy in the main sense: non-core skills do compete semantically, and most of them are wrong for procedural reasons. This is exactly the target failure mode.

The borderline cases should not be ignored. They suggest two options for later thesis evaluation:

1. Keep strict gold labels for the controlled core, but report a secondary “acceptable non-core” analysis for borderline cases.
2. Add graded relevance for a small number of near-equivalent non-core skills so that retrieval metrics distinguish “wrong artifact” from “reasonable but less controlled alternative.”

For now, no prompt needs immediate removal. The borderline cases are useful stress cases, but they should be documented when interpreting top-1 accuracy.
