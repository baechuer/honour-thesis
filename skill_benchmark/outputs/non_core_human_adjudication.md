# Non-Core Human Adjudication

This is the manual review of scale competitors that beat the gold skill under description-card semantic retrieval in the 2089-skill library.

The review intentionally ignores artificial benchmark-wrapper text in generated/public background skills. It asks: if a careful human read the user prompt and the actual skill capability, would the controlled gold still be the better choice?

## Summary

- Semantic-over-gold cases reviewed: 33
- Clear cases where gold is human-obviously better: 18
- Borderline cases where gold is defensible but not trivial: 5
- Acceptable alternatives or near-equivalents: 5
- Object-confusion cases: 5
- Additional procedural-only watch items: 2

Interpretation: the benchmark remains valid. Most non-core winners are not actually better skills; they are lexical or domain distractors created by scale. A small number are acceptable alternatives and should be counted separately from strict gold-only accuracy.

## Verdict Categories

- `gold_clear`: a careful human should choose the controlled gold skill.
- `gold_defensible`: gold is still preferred, but the non-core winner is plausible enough to mention.
- `acceptable_alternative`: the non-core skill is a genuinely acceptable substitute in the scaled-library setting.
- `object_confusion`: the non-core skill matches an object mentioned in the prompt, but the requested operation is a meta-task or different procedure.

## Semantic Winners

| Prompt | Semantic winner | Human verdict | Reason |
|---|---|---|---|
| `api_p2_external_api_integration` | `api-integration-planner` | `acceptable_alternative` | The background skill is a near-duplicate of the controlled external API integration planner. |
| `api_p6_service_dependency_map` | `customer-feedback-analyser` | `gold_clear` | The prompt asks for service dependency mapping, not customer-feedback analysis. |
| `web_p2_form_filling` | `identity-ops-acceptance-test-builder` | `gold_clear` | The user asks to complete a signup form and pause before submission; acceptance-test writing is the wrong artifact. |
| `web_p3_ui_test` | `email-ops-acceptance-test-builder` | `gold_clear` | The user asks to test checkout-page validation behavior, not build email workflow tests. |
| `code_p1_local_code_review` | `email-ops-acceptance-test-builder` | `gold_clear` | The user asks for code review before commit, not acceptance checks for email workflows. |
| `code_p5_changelog_entry` | `public-office-changelog-generator` | `acceptable_alternative` | A public changelog generator is a genuine substitute for the controlled changelog writer. |
| `code_p6_release_notes` | `identity-ops-failure-diagnoser` | `gold_clear` | The user asks for user-facing release notes; failure diagnosis is a different task. |
| `data_p3_validation` | `real-estate-ops-failure-diagnoser` | `gold_clear` | The prompt asks whether spreadsheet conclusions are safe; real-estate workflow failure diagnosis is the wrong object and output. |
| `data_p4_root_cause` | `media-ops-failure-diagnoser` | `gold_clear` | The prompt asks for spreadsheet driver analysis. Media workflow failure diagnosis is unrelated procedurally. |
| `data_p7_ranking_selection` | `priority-sorter` | `gold_defensible` | Priority sorting is plausible, but gold is better because the task ranks spreadsheet options using data evidence and tradeoffs. |
| `deploy_p1_playwright_flow_debug` | `ecommerce-ops-failure-diagnoser` | `gold_clear` | The prompt requires browser interaction evidence and frontend/deploy debugging, not ecommerce workflow failure diagnosis. |
| `deploy_p4_build_log_triage` | `public-netlify-deploy` | `gold_defensible` | Netlify is the deployment platform, but the requested operation is failed-build log triage rather than deploying a project. |
| `deploy_p5_release_verification` | `public-netlify-deploy` | `gold_defensible` | Netlify deployment knowledge is relevant, but the controlled gold better matches post-release verification and rollback notes. |
| `deploy_p6_performance_budget` | `mobile-ops-summary-writer` | `gold_clear` | The prompt asks for a mobile web performance-budget check, not a mobile operations summary. |
| `doc_p1_document_summary` | `travel-ops-summary-writer` | `gold_defensible` | The source is travel-policy material, but the task is general practical-document understanding. |
| `doc_p2_document_rewriter` | `travel-ops-rewrite-editor` | `acceptable_alternative` | The source is a travel request note and the requested artifact is a polished prose rewrite. |
| `doc_p3_document_normaliser` | `travel-ops-rewrite-editor` | `gold_clear` | The prompt explicitly asks to preserve wording and normalize headings/spacing/list style, not rewrite prose. |
| `doc_p4_field_extraction` | `receipt-extractor` | `gold_clear` | The source is an invoice, not a receipt, and asks for reusable document fields. |
| `doc_p5_comparison_preparation` | `privacy-policy-drafter` | `gold_clear` | The prompt asks for a side-by-side comparison matrix, not drafting privacy-policy text. |
| `doc_p6_conversion` | `public-markitdown` | `acceptable_alternative` | The prompt asks to convert a form into clean Markdown notes, which a MarkItDown-style skill can reasonably do. |
| `obs_p6_incident_summary` | `incident-ops-summary-writer` | `acceptable_alternative` | Both skills produce incident summaries from operational material. |
| `news_p2_briefing` | `events-ops-summary-writer` | `gold_clear` | The prompt asks for a news briefing, not event-planning operational summary. |
| `news_p3_grounded_claims` | `product-ops-evidence-grounder` | `gold_clear` | The prompt asks for source-backed news claims and named facts, not product-ops evidence grounding. |
| `plan_p3_meeting_followup` | `meeting-ops-summary-writer` | `gold_defensible` | The summary skill is plausible, but the user specifically asks for next actions and unresolved attention items. |
| `read_p2_general_source_summary` | `research-ops-evidence-grounder` | `gold_clear` | The user asks for a plain-language source report, not claim-evidence grounding. |
| `read_p5_method_notes` | `manufacturing-ops-summary-writer` | `gold_clear` | The prompt asks for method/evaluation/assumptions from a study. Manufacturing summary is only lexically overlapping. |
| `sec_p1_threat_model` | `public-openai-security-ownership-map` | `gold_clear` | Ownership mapping may support security work, but the requested artifact is a threat model. |
| `sec_p2_security_code_review` | `api-ops-rewrite-editor` | `gold_clear` | The prompt asks for code-level security vulnerabilities and fixes, not API text rewriting. |
| `skill_p1_find_existing` | `public-anthropic-doc-coauthoring` | `object_confusion` | The requested operation is skill-library discovery; document coauthoring is not the operation. |
| `skill_p2_install_existing` | `public-office-data-analysis` | `object_confusion` | The spreadsheet skill is the object/source capability to install, not the installation procedure. |
| `skill_p4_edit_existing` | `course-ops-field-extractor` | `object_confusion` | Field extraction is the over-triggering behavior being fixed; the requested operation is editing a skill boundary. |
| `skill_p5_evaluate_existing` | `email-polisher` | `object_confusion` | The email-polishing skill is the object under evaluation. |
| `skill_p6_package_existing` | `public-anthropic-doc-coauthoring` | `object_confusion` | `paper-summariser` is the skill being packaged; the task is packaging, not document coauthoring. |

## Procedural-Only Watch Items

These surfaced in the all-non-core procedural audit even when they were not the top semantic winner.

| Prompt | Procedural competitor | Human verdict | Reason |
|---|---|---|---|
| `doc_p5_comparison_preparation` | `legal-ops-comparison-builder` | `acceptable_alternative` | The prompt compares policy drafts. Legal/policy comparison is close enough that strict gold-only scoring is misleading. |
| `skill_p3_create_new` | `thesis-ops-timeline-builder` | `object_confusion` | The thesis workflow is the content of the new skill being requested. The requested operation is skill creation. |

## Evaluation Implication

For strict top-1 metrics, use the controlled gold label. For interpretation, also report `Accept Top-1`, `Accept Top-5`, and `Accept MRR` where documented acceptable alternatives count as correct.

Current documented acceptable alternatives live in `skill_benchmark/annotations/acceptable_alternatives.json`.
