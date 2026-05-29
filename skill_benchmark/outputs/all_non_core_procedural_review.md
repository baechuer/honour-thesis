# All Non-Core Procedural Review

This report reviews the every-skill procedural competition screen from `all_non_core_procedural_competition_report.md`.

Purpose: answer whether background/public/support skills are actually better fits for benchmark prompts than the gold labels, or whether they are only false positives under scale.

Important: before this review, exported representation files were cleaned so selector-facing text no longer exposes artificial benchmark hints such as "gold-label", "controlled core", "scale distractor", or "confusable evaluation".

## Scope

- Prompts reviewed: 67
- Total skills in library: 1006
- Non-core skills checked per prompt: 939
- Gold/non-core comparisons: 62913
- Prompts with at least one non-core skill above gold on structured procedural fields: 11/67
- Above-gold non-core comparisons: 154

## Decision Rules

- `safe distractor`: the non-core skill shares surface or domain vocabulary but has the wrong task, output artifact, workflow, or selection target.
- `borderline`: the non-core skill could plausibly help, but the controlled gold skill is still more specific to the prompt's intended procedure.
- `gold-label threat`: the non-core skill is equally or more procedurally correct than the gold label, so strict top-1 scoring would be misleading unless it is handled as acceptable or the prompt/library is refined.

## Overall Judgment

- Clear safe distractor prompts: 5
- Borderline prompts needing documentation or graded relevance: 4
- Gold-label threat / near-equivalent prompts: 2

Interpretation: the current 1006-skill benchmark is creating scale pressure, but two cases are not human-obvious enough under strict gold-only scoring. These should be treated as acceptable alternatives or refined before final thesis evaluation.

## Reviewed Above-Gold Cases

| Prompt | Gold | Strongest non-core competitors | Decision | Reason |
|---|---|---|---|---|
| `web_p3_ui_test` | `web-ui-tester` | `email-ops-acceptance-test-builder`, `travel-ops-acceptance-test-builder` | safe distractor | The prompt asks to test a web checkout validation message. The non-core skills write acceptance checks for other operational domains, not browser UI behavior. |
| `doc_p1_document_summary` | `document-summariser` | `travel-ops-compliance-checker`, `travel-ops-risk-reviewer`, `travel-ops-summary-writer` | borderline | The source is travel-policy material, so travel-domain skills are naturally competitive. Gold is still better because the task is to understand a practical document/policy update, not perform travel planning, compliance, or risk operations. |
| `doc_p2_document_rewriter` | `document-rewriter` | `travel-ops-rewrite-editor` | gold-label threat | The source is a travel request note and the requested artifact is a polished prose rewrite. A human could reasonably choose the domain-specific travel rewrite skill. Treat as acceptable or change the fixture/domain. |
| `doc_p4_field_extraction` | `document-field-extractor` | `vendor-ops-field-extractor`, `finance-ops-field-extractor`, `receipt-extractor` | borderline | The prompt asks for structured fields from an invoice. Domain-specific financial/vendor extractors are close, but the gold remains defensible because it asks for reusable document fields across supplier, invoice number, line items, totals, and payment details. |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | `legal-ops-comparison-builder` | gold-label threat | The prompt compares two policy drafts. The legal/policy comparison skill is procedurally very close and arguably as good as the generic multi-document comparison skill. Treat as acceptable or use non-legal documents. |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | `meeting-ops-summary-writer`, `meeting-ops-quality-auditor` | borderline | The non-core summary skill can help, but the prompt specifically asks for next actions, unresolved items, owners, and deadlines. Gold is more action-extraction focused. |
| `skill_p1_find_existing` | `skill-finder` | `meeting-ops-resource-linker`, `meeting-ops-rewrite-editor`, `meeting-ops-summary-writer` | safe distractor | The meeting workflow is the object being searched for. The requested task is to inspect the skill library and recommend reuse, not to perform meeting-note work. |
| `skill_p2_install_existing` | `skill-installer` | `public-xlsx`, `public-skill-installer`, `dataset-ops-resource-linker` | borderline | `public-xlsx` is the object/source capability, not the installation operation. `public-skill-installer` is a genuine acceptable alternative and should be handled as such if selected. |
| `skill_p3_create_new` | `skill-creator` | `thesis-ops-timeline-builder` | safe distractor | The thesis action-list workflow is the content of the new skill being requested. The actual task is to create a skill artifact, not build a thesis timeline. |
| `skill_p4_edit_existing` | `skill-editor` | many `*-ops-field-extractor` skills | safe distractor | The prompt asks to revise a skill boundary that over-triggers on field extraction. Field extraction is the problem being edited, not the requested operation. |
| `skill_p5_evaluate_existing` | `skill-evaluator` | `email-polisher`, `email-drafter` | safe distractor | The prompt asks to evaluate whether a reply-polishing skill triggers correctly. It does not ask to polish or draft an email. |

## Recommended Evaluation Treatment

Use strict gold-label metrics for the main controlled benchmark, but add a secondary interpretation column for selected outputs:

- `correct`: selected skill equals the controlled gold skill.
- `acceptable_borderline`: selected skill is documented as plausible but less controlled.
- `near_equivalent`: selected skill is effectively as reasonable as the gold under human adjudication.
- `wrong_semantic_distractor`: selected skill sounds related but misses the required procedure.

For final thesis evaluation, do not count `doc_p2_document_rewriter` with `travel-ops-rewrite-editor`, or `doc_p5_comparison_preparation` with `legal-ops-comparison-builder`, as ordinary wrong retrieval errors unless the benchmark is refined first.

## Follow-Up Actions

1. Keep the 1006-skill scale condition: it creates real semantic pressure.
2. Keep strict gold labels for controlled development, but report acceptable/near-equivalent selections separately.
3. Consider refining `doc_p2_document_rewriter` by using a non-travel document, or mark `travel-ops-rewrite-editor` as an acceptable alternative.
4. Consider refining `doc_p5_comparison_preparation` by using non-legal/non-policy documents, or mark `legal-ops-comparison-builder` as an acceptable alternative.
5. Re-run this review after adding stronger embedding/reranking methods, because stronger methods may select near-equivalent public/domain skills more often.
