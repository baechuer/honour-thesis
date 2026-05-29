# All Non-Core Procedural Competition Report

This report applies the Step 2 requirement-alignment idea against every non-core skill, not only the listed closest alternatives. It asks whether a background/public/support skill looks procedurally competitive with the gold skill under structured procedural fields.

Similarity backend: **embedding** using `sentence-transformers/all-MiniLM-L6-v2`.

Important limitation: this is a heuristic procedural-fit screen, not a human adjudication. A non-core score above gold means it deserves review; it does not automatically mean the gold label is wrong.

## Overall Status

- Prompts checked: 85
- Non-core skills checked per prompt: 939
- Gold/non-core prompt-skill comparisons: 79815
- Prompts with at least one non-core skill above gold: 16/85 (18.8%)
- Prompts with at least one non-core skill near or above gold: 23/85 (27.1%)
- Above-gold non-core comparisons: 354
- Near-gold non-core comparisons within 0.02 margin: 193

## Family Summary

| Prompt family | Prompts | With non-core above gold | Above-gold pairs | Near/above pairs |
|---|---:|---:|---:|---:|
| `api_backend_design` | 6 | 1/6 | 2 | 3 |
| `browser_web_automation` | 6 | 1/6 | 5 | 16 |
| `code_github_workflow` | 6 | 0/6 | 0 | 6 |
| `data_spreadsheet` | 7 | 0/7 | 0 | 0 |
| `deployment_browser_qa` | 6 | 2/6 | 2 | 3 |
| `documents_files` | 7 | 4/7 | 134 | 203 |
| `metrics_observability` | 6 | 0/6 | 0 | 0 |
| `news_monitoring` | 5 | 1/5 | 1 | 2 |
| `office_artifact_workflows` | 6 | 0/6 | 0 | 2 |
| `planning_meetings` | 5 | 1/5 | 2 | 4 |
| `reading_research` | 8 | 0/8 | 0 | 7 |
| `reply_messaging` | 5 | 0/5 | 0 | 0 |
| `security_appsec` | 6 | 1/6 | 3 | 5 |
| `skill_lifecycle` | 6 | 5/6 | 205 | 296 |

## Above-Gold Competitor Families

| Non-core family | Top-10 appearances above gold |
|---|---:|
| `background_scale` | 49 |
| `public_imported_background` | 19 |
| `email_communication` | 2 |

## Prompts With Non-Core Procedural Competitors

| Prompt | Gold | Gold score | Above-gold count | Top non-core competitors |
|---|---|---:|---:|---|
| `doc_p1_document_summary` | `document-summariser` | 0.230 | 115 | +`travel-ops-compliance-checker`/background_scale (0.401, +0.171); +`travel-ops-risk-reviewer`/background_scale (0.384, +0.154); +`travel-ops-rewrite-editor`/background_scale (0.378, +0.148); +`travel-ops-summary-writer`/background_scale (0.367, +0.136); +`travel-ops-scenario-planner`/background_scale (0.356, +0.126) |
| `skill_p4_edit_existing` | `skill-editor` | 0.499 | 108 | +`docs-ops-field-extractor`/background_scale (0.679, +0.180); +`search-ops-field-extractor`/background_scale (0.659, +0.160); +`writing-ops-field-extractor`/background_scale (0.657, +0.158); +`content-ops-field-extractor`/background_scale (0.656, +0.157); +`research-ops-field-extractor`/background_scale (0.654, +0.155) |
| `skill_p2_install_existing` | `skill-installer` | 0.283 | 73 | +`public-office-data-analysis`/public_imported_background (0.559, +0.276); +`public-office-excel-automation`/public_imported_background (0.536, +0.253); +`public-office-xlsx-manipulation`/public_imported_background (0.534, +0.251); +`public-office-sheets-automation`/public_imported_background (0.517, +0.234); +`public-xlsx`/public_imported_background (0.492, +0.209) |
| `skill_p1_find_existing` | `skill-finder` | 0.476 | 21 | +`public-office-meeting-notes`/public_imported_background (0.633, +0.157); +`meeting-ops-resource-linker`/background_scale (0.544, +0.067); +`public-openai-notion-meeting-intelligence`/public_imported_background (0.542, +0.066); +`meeting-ops-rewrite-editor`/background_scale (0.537, +0.061); +`meeting-ops-summary-writer`/background_scale (0.534, +0.058) |
| `doc_p4_field_extraction` | `document-field-extractor` | 0.490 | 17 | +`supply-chain-ops-field-extractor`/background_scale (0.571, +0.080); +`procurement-ops-field-extractor`/background_scale (0.553, +0.063); +`procurement-ops-summary-writer`/background_scale (0.546, +0.056); +`ecommerce-ops-field-extractor`/background_scale (0.544, +0.053); +`supply-chain-ops-summary-writer`/background_scale (0.536, +0.046) |
| `web_p3_ui_test` | `web-ui-tester` | 0.321 | 5 | +`email-ops-acceptance-test-builder`/background_scale (0.356, +0.035); +`ecommerce-ops-acceptance-test-builder`/background_scale (0.333, +0.012); +`facilities-ops-acceptance-test-builder`/background_scale (0.331, +0.009); +`travel-ops-acceptance-test-builder`/background_scale (0.325, +0.004); +`procurement-ops-acceptance-test-builder`/background_scale (0.322, +0.001) |
| `sec_p1_threat_model` | `security-threat-modeler` | 0.405 | 3 | +`public-openai-security-ownership-map`/public_imported_background (0.463, +0.059); +`public-anthropic-slack-gif-creator`/public_imported_background (0.421, +0.017); +`public-office-file-organizer`/public_imported_background (0.407, +0.002); ~`public-office-suspicious-email`/public_imported_background (0.390, -0.015); ~`public-office-gmail-workflows`/public_imported_background (0.386, -0.019) |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 0.456 | 2 | +`support-ops-monitoring-plan-builder`/background_scale (0.461, +0.004); +`customer-success-ops-monitoring-plan-builder`/background_scale (0.460, +0.003); ~`dashboard-ops-monitoring-plan-builder`/background_scale (0.452, -0.004) |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 0.515 | 2 | +`meeting-ops-summary-writer`/background_scale (0.571, +0.056); +`meeting-ops-quality-auditor`/background_scale (0.523, +0.008); ~`meeting-ops-rewrite-editor`/background_scale (0.513, -0.002); ~`meeting-ops-normalizer`/background_scale (0.508, -0.007) |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 0.464 | 2 | +`email-polisher`/email_communication (0.588, +0.124); +`email-drafter`/email_communication (0.502, +0.038); ~`prompt-refiner`/background_scale (0.448, -0.016); ~`email-ops-acceptance-test-builder`/background_scale (0.447, -0.017) |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 0.390 | 1 | +`public-netlify-deploy`/public_imported_background (0.526, +0.136) |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 0.460 | 1 | +`public-netlify-deploy`/public_imported_background (0.560, +0.100) |
| `doc_p2_document_rewriter` | `document-rewriter` | 0.578 | 1 | +`travel-ops-rewrite-editor`/background_scale (0.598, +0.020); ~`travel-ops-summary-writer`/background_scale (0.567, -0.012) |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 0.535 | 1 | +`legal-ops-comparison-builder`/background_scale (0.548, +0.013); ~`writing-ops-comparison-builder`/background_scale (0.531, -0.004); ~`docs-ops-comparison-builder`/background_scale (0.526, -0.008) |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 0.336 | 1 | +`public-office-crypto-report`/public_imported_background (0.347, +0.011); ~`product-ops-evidence-grounder`/background_scale (0.317, -0.019) |
| `skill_p3_create_new` | `skill-creator` | 0.578 | 1 | +`thesis-ops-timeline-builder`/background_scale (0.579, +0.000); ~`thesis-ops-normalizer`/background_scale (0.560, -0.018) |
| `code_p1_local_code_review` | `code-reviewer` | 0.266 | 0 | ~`email-ops-acceptance-test-builder`/background_scale (0.256, -0.010); ~`email-polisher`/email_communication (0.248, -0.018) |
| `code_p6_release_notes` | `release-note-writer` | 0.288 | 0 | ~`mobile-ops-monitoring-plan-builder`/background_scale (0.283, -0.005); ~`mobile-ops-risk-reviewer`/background_scale (0.278, -0.010); ~`mobile-ops-acceptance-test-builder`/background_scale (0.272, -0.017); ~`mobile-ops-compliance-checker`/background_scale (0.271, -0.018) |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 0.250 | 0 | ~`ecommerce-ops-acceptance-test-builder`/background_scale (0.233, -0.017) |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 0.484 | 0 | ~`public-xlsx`/public_imported_background (0.473, -0.011); ~`public-office-xlsx-manipulation`/public_imported_background (0.469, -0.015) |
| `read_p5_method_notes` | `method-note-builder` | 0.389 | 0 | ~`procurement-risk-summariser`/background_scale (0.371, -0.018) |
| `read_p6_grounding_check` | `citation-grounding-helper` | 0.522 | 0 | ~`research-ops-rewrite-editor`/background_scale (0.513, -0.009); ~`research-ops-summary-writer`/background_scale (0.512, -0.010); ~`research-ops-quality-auditor`/background_scale (0.512, -0.010); ~`incident-ops-rewrite-editor`/background_scale (0.506, -0.016); ~`agent-ops-summary-writer`/background_scale (0.504, -0.017) |
| `skill_p6_package_existing` | `skill-packager` | 0.476 | 0 | ~`public-anthropic-doc-coauthoring`/public_imported_background (0.466, -0.010) |

## Review Guidance

- `+` means the non-core skill scored above the gold skill on structured procedural fields.
- `~` means the non-core skill was within 0.02 of the gold score.
- Treat high counts as review pressure, not automatic invalidation.
- If a `+` competitor has the same input type, output artifact, workflow, and success criterion as gold, mark it as acceptable or remove it from the background library.
- If it only shares generic words such as summary, rewrite, rank, check, evidence, or test while missing the task-specific artifact, keep it as a semantic distractor.
