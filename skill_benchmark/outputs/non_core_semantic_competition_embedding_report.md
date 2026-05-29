# Non-Core Semantic Competition Report

This report checks whether background/public/support skills look more semantically similar to benchmark prompts than the gold core skill under a description-card similarity backend.

Similarity backend: **embedding** using `sentence-transformers/all-MiniLM-L6-v2`.

## Overall Status

- Prompts: 85
- Gold ranked top-1 among all skills: 46/85 (54.1%)
- Non-core skill ranked top-1: 24/85 (28.2%)
- Best non-core skill scores above gold: 33/85 (38.8%)

Interpretation: a non-core skill beating the gold does not automatically mean the gold label is wrong. It means the compressed semantic representation has a plausible scale distractor that may need reranking or richer procedural representation.

## Family Summary

| Prompt family | Prompts | Non-core top-1 | Best non-core beats gold |
|---|---:|---:|---:|
| `api_backend_design` | 6 | 2/6 | 2/6 |
| `browser_web_automation` | 6 | 1/6 | 2/6 |
| `code_github_workflow` | 6 | 2/6 | 3/6 |
| `data_spreadsheet` | 7 | 1/7 | 3/7 |
| `deployment_browser_qa` | 6 | 3/6 | 4/6 |
| `documents_files` | 7 | 6/7 | 6/7 |
| `metrics_observability` | 6 | 1/6 | 1/6 |
| `news_monitoring` | 5 | 2/5 | 2/5 |
| `office_artifact_workflows` | 6 | 0/6 | 0/6 |
| `planning_meetings` | 5 | 0/5 | 1/5 |
| `reading_research` | 8 | 2/8 | 2/8 |
| `reply_messaging` | 5 | 0/5 | 0/5 |
| `security_appsec` | 6 | 2/6 | 2/6 |
| `skill_lifecycle` | 6 | 2/6 | 5/6 |

## Non-Core Families That Beat Gold

| Non-core family | Count |
|---|---:|
| `background_scale` | 24 |
| `public_imported_background` | 8 |
| `email_communication` | 1 |

## Prompts Where Non-Core Beats Gold

| Prompt | Gold | Gold rank | Best non-core | Non-core rank | Scores |
|---|---|---:|---|---:|---|
| `api_p2_external_api_integration` | `external-api-integration-planner` | 3 | `api-integration-planner` (`background_scale`) | 1 | gold 0.426; non-core 0.479 |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 214 | `customer-feedback-analyser` (`background_scale`) | 1 | gold 0.358; non-core 0.477 |
| `web_p2_form_filling` | `web-form-filler` | 3 | `identity-ops-acceptance-test-builder` (`background_scale`) | 2 | gold 0.393; non-core 0.419 |
| `web_p3_ui_test` | `web-ui-tester` | 120 | `email-ops-acceptance-test-builder` (`background_scale`) | 1 | gold 0.239; non-core 0.380 |
| `code_p1_local_code_review` | `code-reviewer` | 2 | `email-ops-acceptance-test-builder` (`background_scale`) | 1 | gold 0.303; non-core 0.318 |
| `code_p5_changelog_entry` | `changelog-writer` | 3 | `public-office-changelog-generator` (`public_imported_background`) | 2 | gold 0.432; non-core 0.459 |
| `code_p6_release_notes` | `release-note-writer` | 173 | `identity-ops-failure-diagnoser` (`background_scale`) | 1 | gold 0.215; non-core 0.397 |
| `data_p3_validation` | `data-analysis-with-validation` | 21 | `real-estate-ops-failure-diagnoser` (`background_scale`) | 2 | gold 0.320; non-core 0.358 |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 81 | `media-ops-failure-diagnoser` (`background_scale`) | 3 | gold 0.230; non-core 0.343 |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 31 | `priority-sorter` (`background_scale`) | 1 | gold 0.443; non-core 0.568 |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 4 | `ecommerce-ops-failure-diagnoser` (`background_scale`) | 2 | gold 0.321; non-core 0.345 |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 2 | `public-netlify-deploy` (`public_imported_background`) | 1 | gold 0.410; non-core 0.518 |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 2 | `public-netlify-deploy` (`public_imported_background`) | 1 | gold 0.483; non-core 0.632 |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 2 | `mobile-ops-summary-writer` (`background_scale`) | 1 | gold 0.453; non-core 0.463 |
| `doc_p1_document_summary` | `document-summariser` | 566 | `travel-ops-summary-writer` (`background_scale`) | 1 | gold 0.159; non-core 0.457 |
| `doc_p2_document_rewriter` | `document-rewriter` | 7 | `travel-ops-rewrite-editor` (`background_scale`) | 1 | gold 0.431; non-core 0.574 |
| `doc_p3_document_normaliser` | `document-normaliser` | 2 | `travel-ops-rewrite-editor` (`background_scale`) | 1 | gold 0.454; non-core 0.515 |
| `doc_p4_field_extraction` | `document-field-extractor` | 12 | `receipt-extractor` (`background_scale`) | 1 | gold 0.406; non-core 0.536 |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 2 | `privacy-policy-drafter` (`background_scale`) | 1 | gold 0.470; non-core 0.488 |
| `doc_p6_conversion` | `document-converter` | 2 | `public-markitdown` (`public_imported_background`) | 1 | gold 0.413; non-core 0.428 |
| `obs_p6_incident_summary` | `incident-summary-writer` | 6 | `incident-ops-summary-writer` (`background_scale`) | 1 | gold 0.381; non-core 0.413 |
| `news_p2_briefing` | `news-briefing-writer` | 2 | `events-ops-summary-writer` (`background_scale`) | 1 | gold 0.463; non-core 0.498 |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 24 | `product-ops-evidence-grounder` (`background_scale`) | 1 | gold 0.392; non-core 0.545 |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 6 | `meeting-ops-summary-writer` (`background_scale`) | 2 | gold 0.477; non-core 0.521 |
| `read_p2_general_source_summary` | `general-source-summariser` | 2 | `research-ops-evidence-grounder` (`background_scale`) | 1 | gold 0.498; non-core 0.504 |
| `read_p5_method_notes` | `method-note-builder` | 14 | `manufacturing-ops-summary-writer` (`background_scale`) | 1 | gold 0.383; non-core 0.415 |
| `sec_p1_threat_model` | `security-threat-modeler` | 12 | `public-openai-security-ownership-map` (`public_imported_background`) | 1 | gold 0.337; non-core 0.428 |
| `sec_p2_security_code_review` | `security-code-reviewer` | 4 | `api-ops-rewrite-editor` (`background_scale`) | 1 | gold 0.401; non-core 0.440 |
| `skill_p1_find_existing` | `skill-finder` | 7 | `public-anthropic-doc-coauthoring` (`public_imported_background`) | 3 | gold 0.413; non-core 0.436 |
| `skill_p2_install_existing` | `skill-installer` | 201 | `public-office-data-analysis` (`public_imported_background`) | 1 | gold 0.244; non-core 0.609 |
| `skill_p4_edit_existing` | `skill-editor` | 74 | `course-ops-field-extractor` (`background_scale`) | 2 | gold 0.434; non-core 0.559 |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 8 | `email-polisher` (`email_communication`) | 3 | gold 0.387; non-core 0.528 |
| `skill_p6_package_existing` | `skill-packager` | 6 | `public-anthropic-doc-coauthoring` (`public_imported_background`) | 1 | gold 0.388; non-core 0.475 |

## Prompt Detail

### `api_p1_openapi_contract_review`

- Gold: `openapi-contract-reviewer`; rank 1; score 0.681
- Best non-core: `openapi-contract-tester`; rank 2; score 0.541
- Top neighbours: `openapi-contract-reviewer`/api_backend_design (0.681), `openapi-contract-tester`/background_scale (0.541), `external-api-integration-planner`/api_backend_design (0.483), `api-ops-summary-writer`/background_scale (0.473), `api-integration-planner`/background_scale (0.455)

### `api_p2_external_api_integration`

- Gold: `external-api-integration-planner`; rank 3; score 0.426
- Best non-core: `api-integration-planner`; rank 1; score 0.479
- Top neighbours: `api-integration-planner`/background_scale (0.479), `auth-flow-reviewer`/security_appsec (0.440), `external-api-integration-planner`/api_backend_design (0.426), `public-office-subscription-management`/public_imported_background (0.396), `api-ops-summary-writer`/background_scale (0.385)

### `api_p3_webhook_contract`

- Gold: `webhook-contract-planner`; rank 1; score 0.463
- Best non-core: `events-ops-acceptance-test-builder`; rank 2; score 0.423
- Top neighbours: `webhook-contract-planner`/api_backend_design (0.463), `events-ops-acceptance-test-builder`/background_scale (0.423), `events-ops-intake-classifier`/background_scale (0.420), `invoice-payment-checker`/background_scale (0.398), `customer-success-ops-intake-classifier`/background_scale (0.396)

### `api_p4_architecture_boundary`

- Gold: `architecture-boundary-reviewer`; rank 1; score 0.725
- Best non-core: `public-architecture-patterns`; rank 2; score 0.511
- Top neighbours: `architecture-boundary-reviewer`/api_backend_design (0.725), `public-architecture-patterns`/public_imported_background (0.511), `openapi-contract-reviewer`/api_backend_design (0.450), `service-dependency-mapper`/api_backend_design (0.444), `database-migration-risk-assessor`/api_backend_design (0.440)

### `api_p5_database_migration_risk`

- Gold: `database-migration-risk-assessor`; rank 1; score 0.674
- Best non-core: `migration-risk-auditor`; rank 2; score 0.615
- Top neighbours: `database-migration-risk-assessor`/api_backend_design (0.674), `migration-risk-auditor`/background_scale (0.615), `deployment-rollback-planner`/background_scale (0.578), `public-office-subscription-management`/public_imported_background (0.487), `database-backup-planner`/background_scale (0.469)

### `api_p6_service_dependency_map`

- Gold: `service-dependency-mapper`; rank 214; score 0.358
- Best non-core: `customer-feedback-analyser`; rank 1; score 0.477
- Top neighbours: `customer-feedback-analyser`/background_scale (0.477), `analytics-ops-compliance-checker`/background_scale (0.474), `dashboard-ops-compliance-checker`/background_scale (0.468), `dashboard-ops-quality-auditor`/background_scale (0.463), `analytics-ops-quality-auditor`/background_scale (0.456)

### `web_p1_page_snapshot`

- Gold: `web-page-snapshotter`; rank 2; score 0.418
- Best non-core: `analytics-ops-acceptance-test-builder`; rank 3; score 0.370
- Top neighbours: `visual-regression-checker`/deployment_browser_qa (0.445), `web-page-snapshotter`/browser_web_automation (0.418), `analytics-ops-acceptance-test-builder`/background_scale (0.370), `dashboard-ops-acceptance-test-builder`/background_scale (0.350), `dataset-ops-acceptance-test-builder`/background_scale (0.347)

### `web_p2_form_filling`

- Gold: `web-form-filler`; rank 3; score 0.393
- Best non-core: `identity-ops-acceptance-test-builder`; rank 2; score 0.419
- Top neighbours: `web-ui-tester`/browser_web_automation (0.433), `identity-ops-acceptance-test-builder`/background_scale (0.419), `web-form-filler`/browser_web_automation (0.393), `marketing-ops-acceptance-test-builder`/background_scale (0.390), `web-ops-acceptance-test-builder`/background_scale (0.388)

### `web_p3_ui_test`

- Gold: `web-ui-tester`; rank 120; score 0.239
- Best non-core: `email-ops-acceptance-test-builder`; rank 1; score 0.380
- Top neighbours: `email-ops-acceptance-test-builder`/background_scale (0.380), `facilities-ops-acceptance-test-builder`/background_scale (0.375), `contract-ops-acceptance-test-builder`/background_scale (0.360), `grant-ops-acceptance-test-builder`/background_scale (0.356), `crm-ops-acceptance-test-builder`/background_scale (0.356)

### `web_p4_data_extraction`

- Gold: `web-data-extractor`; rank 1; score 0.493
- Best non-core: `product-ops-field-extractor`; rank 2; score 0.425
- Top neighbours: `web-data-extractor`/browser_web_automation (0.493), `product-ops-field-extractor`/background_scale (0.425), `receipt-extractor`/background_scale (0.377), `sales-ops-field-extractor`/background_scale (0.366), `product-ops-summary-writer`/background_scale (0.359)

### `web_p5_frontend_debugging`

- Gold: `frontend-debugger`; rank 1; score 0.385
- Best non-core: `api-ops-failure-diagnoser`; rank 2; score 0.329
- Top neighbours: `frontend-debugger`/browser_web_automation (0.385), `api-ops-failure-diagnoser`/background_scale (0.329), `publishing-ops-failure-diagnoser`/background_scale (0.282), `property-ops-failure-diagnoser`/background_scale (0.281), `playwright-flow-debugger`/deployment_browser_qa (0.278)

### `web_p6_accessibility_check`

- Gold: `accessibility-checker`; rank 2; score 0.478
- Best non-core: `terms-of-service-drafter`; rank 3; score 0.323
- Top neighbours: `accessibility-interaction-auditor`/deployment_browser_qa (0.519), `accessibility-checker`/browser_web_automation (0.478), `terms-of-service-drafter`/background_scale (0.323), `meeting-ops-failure-diagnoser`/background_scale (0.319), `public-office-customer-success`/public_imported_background (0.318)

### `code_p1_local_code_review`

- Gold: `code-reviewer`; rank 2; score 0.303
- Best non-core: `email-ops-acceptance-test-builder`; rank 1; score 0.318
- Top neighbours: `email-ops-acceptance-test-builder`/background_scale (0.318), `code-reviewer`/code_github_workflow (0.303), `localization-ops-acceptance-test-builder`/background_scale (0.300), `repo-ops-acceptance-test-builder`/background_scale (0.282), `email-ops-failure-diagnoser`/background_scale (0.278)

### `code_p2_pr_review`

- Gold: `pr-reviewer`; rank 2; score 0.477
- Best non-core: `pr-description-writer`; rank 3; score 0.431
- Top neighbours: `auth-flow-reviewer`/security_appsec (0.511), `pr-reviewer`/code_github_workflow (0.477), `pr-description-writer`/background_scale (0.431), `public-openai-gh-address-comments`/public_imported_background (0.416), `api-ops-acceptance-test-builder`/background_scale (0.403)

### `code_p3_review_comment_resolution`

- Gold: `review-comment-resolver`; rank 1; score 0.495
- Best non-core: `sre-ops-failure-diagnoser`; rank 5; score 0.329
- Top neighbours: `review-comment-resolver`/code_github_workflow (0.495), `pr-reviewer`/code_github_workflow (0.424), `ci-failure-debugger`/code_github_workflow (0.417), `code-reviewer`/code_github_workflow (0.374), `sre-ops-failure-diagnoser`/background_scale (0.329)

### `code_p4_ci_failure_debugging`

- Gold: `ci-failure-debugger`; rank 1; score 0.497
- Best non-core: `api-ops-failure-diagnoser`; rank 2; score 0.340
- Top neighbours: `ci-failure-debugger`/code_github_workflow (0.497), `api-ops-failure-diagnoser`/background_scale (0.340), `identity-ops-failure-diagnoser`/background_scale (0.330), `recruiting-ops-failure-diagnoser`/background_scale (0.326), `grant-ops-failure-diagnoser`/background_scale (0.323)

### `code_p5_changelog_entry`

- Gold: `changelog-writer`; rank 3; score 0.432
- Best non-core: `public-office-changelog-generator`; rank 2; score 0.459
- Top neighbours: `release-note-writer`/code_github_workflow (0.494), `public-office-changelog-generator`/public_imported_background (0.459), `changelog-writer`/code_github_workflow (0.432), `repo-ops-failure-diagnoser`/background_scale (0.364), `git-commit-writer`/background_scale (0.352)

### `code_p6_release_notes`

- Gold: `release-note-writer`; rank 173; score 0.215
- Best non-core: `identity-ops-failure-diagnoser`; rank 1; score 0.397
- Top neighbours: `identity-ops-failure-diagnoser`/background_scale (0.397), `auth-flow-reviewer`/security_appsec (0.394), `identity-ops-timeline-builder`/background_scale (0.351), `security-ops-failure-diagnoser`/background_scale (0.339), `identity-ops-monitoring-plan-builder`/background_scale (0.336)

### `data_p1_overview`

- Gold: `data-analysis-overview`; rank 1; score 0.432
- Best non-core: `dashboard-ops-summary-writer`; rank 4; score 0.399
- Top neighbours: `data-analysis-overview`/data_spreadsheet (0.432), `news-briefing-writer`/news_monitoring (0.422), `news-theme-extractor`/news_monitoring (0.405), `dashboard-ops-summary-writer`/background_scale (0.399), `data-analysis-for-reporting`/data_spreadsheet (0.399)

### `data_p2_anomaly_focus`

- Gold: `data-analysis-with-anomaly-focus`; rank 1; score 0.546
- Best non-core: `debugging-root-cause-helper`; rank 3; score 0.395
- Top neighbours: `data-analysis-with-anomaly-focus`/data_spreadsheet (0.546), `latency-anomaly-detector`/metrics_observability (0.520), `debugging-root-cause-helper`/background_scale (0.395), `churn-risk-analyser`/background_scale (0.361), `metrics-root-cause-diagnoser`/metrics_observability (0.342)

### `data_p3_validation`

- Gold: `data-analysis-with-validation`; rank 21; score 0.320
- Best non-core: `real-estate-ops-failure-diagnoser`; rank 2; score 0.358
- Top neighbours: `latency-anomaly-detector`/metrics_observability (0.399), `real-estate-ops-failure-diagnoser`/background_scale (0.358), `dataset-ops-quality-auditor`/background_scale (0.351), `finance-ops-failure-diagnoser`/background_scale (0.346), `data-analysis-with-anomaly-focus`/data_spreadsheet (0.338)

### `data_p4_root_cause`

- Gold: `data-analysis-for-root-cause-diagnosis`; rank 81; score 0.230
- Best non-core: `media-ops-failure-diagnoser`; rank 3; score 0.343
- Top neighbours: `metrics-root-cause-diagnoser`/metrics_observability (0.375), `latency-anomaly-detector`/metrics_observability (0.366), `media-ops-failure-diagnoser`/background_scale (0.343), `energy-ops-failure-diagnoser`/background_scale (0.318), `dataset-ops-failure-diagnoser`/background_scale (0.311)

### `data_p5_reporting`

- Gold: `data-analysis-for-reporting`; rank 1; score 0.508
- Best non-core: `dashboard-ops-summary-writer`; rank 2; score 0.500
- Top neighbours: `data-analysis-for-reporting`/data_spreadsheet (0.508), `dashboard-ops-summary-writer`/background_scale (0.500), `news-briefing-writer`/news_monitoring (0.493), `media-ops-summary-writer`/background_scale (0.471), `incident-summary-writer`/metrics_observability (0.464)

### `data_p6_forecasting`

- Gold: `data-analysis-for-forecasting`; rank 1; score 0.489
- Best non-core: `deadline-reminder-planner`; rank 2; score 0.331
- Top neighbours: `data-analysis-for-forecasting`/data_spreadsheet (0.489), `deadline-reminder-planner`/background_scale (0.331), `capacity-risk-forecaster`/metrics_observability (0.321), `tech-news-trend-extractor`/news_monitoring (0.309), `news-theme-extractor`/news_monitoring (0.276)

### `data_p7_ranking_selection`

- Gold: `data-analysis-for-ranking-selection`; rank 31; score 0.443
- Best non-core: `priority-sorter`; rank 1; score 0.568
- Top neighbours: `priority-sorter`/background_scale (0.568), `travel-ops-priority-ranker`/background_scale (0.502), `risk-ops-priority-ranker`/background_scale (0.495), `robotics-ops-priority-ranker`/background_scale (0.486), `decision-matrix-builder`/background_scale (0.486)

### `deploy_p1_playwright_flow_debug`

- Gold: `playwright-flow-debugger`; rank 4; score 0.321
- Best non-core: `ecommerce-ops-failure-diagnoser`; rank 2; score 0.345
- Top neighbours: `frontend-debugger`/browser_web_automation (0.350), `ecommerce-ops-failure-diagnoser`/background_scale (0.345), `ads-ops-failure-diagnoser`/background_scale (0.325), `playwright-flow-debugger`/deployment_browser_qa (0.321), `grant-ops-failure-diagnoser`/background_scale (0.319)

### `deploy_p2_visual_regression`

- Gold: `visual-regression-checker`; rank 1; score 0.613
- Best non-core: `mobile-ops-comparison-builder`; rank 2; score 0.419
- Top neighbours: `visual-regression-checker`/deployment_browser_qa (0.613), `mobile-ops-comparison-builder`/background_scale (0.419), `dashboard-ops-comparison-builder`/background_scale (0.403), `contract-ops-comparison-builder`/background_scale (0.391), `mobile-ops-rewrite-editor`/background_scale (0.385)

### `deploy_p3_accessibility_interaction`

- Gold: `accessibility-interaction-auditor`; rank 1; score 0.600
- Best non-core: `writing-ops-quality-auditor`; rank 5; score 0.325
- Top neighbours: `accessibility-interaction-auditor`/deployment_browser_qa (0.600), `accessibility-checker`/browser_web_automation (0.484), `visual-regression-checker`/deployment_browser_qa (0.342), `pdf-layout-reviewer`/office_artifact_workflows (0.327), `writing-ops-quality-auditor`/background_scale (0.325)

### `deploy_p4_build_log_triage`

- Gold: `deployment-build-triager`; rank 2; score 0.410
- Best non-core: `public-netlify-deploy`; rank 1; score 0.518
- Top neighbours: `public-netlify-deploy`/public_imported_background (0.518), `deployment-build-triager`/deployment_browser_qa (0.410), `ci-failure-debugger`/code_github_workflow (0.340), `devops-ops-failure-diagnoser`/background_scale (0.313), `publishing-ops-failure-diagnoser`/background_scale (0.302)

### `deploy_p5_release_verification`

- Gold: `deployment-release-verifier`; rank 2; score 0.483
- Best non-core: `public-netlify-deploy`; rank 1; score 0.632
- Top neighbours: `public-netlify-deploy`/public_imported_background (0.632), `deployment-release-verifier`/deployment_browser_qa (0.483), `deployment-build-triager`/deployment_browser_qa (0.464), `public-openai-vercel-deploy`/public_imported_background (0.360), `publishing-ops-failure-diagnoser`/background_scale (0.340)

### `deploy_p6_performance_budget`

- Gold: `web-performance-budget-checker`; rank 2; score 0.453
- Best non-core: `mobile-ops-summary-writer`; rank 1; score 0.463
- Top neighbours: `mobile-ops-summary-writer`/background_scale (0.463), `web-performance-budget-checker`/deployment_browser_qa (0.453), `mobile-ops-quality-auditor`/background_scale (0.447), `mobile-ops-resource-linker`/background_scale (0.440), `mobile-ops-monitoring-plan-builder`/background_scale (0.430)

### `doc_p1_document_summary`

- Gold: `document-summariser`; rank 566; score 0.159
- Best non-core: `travel-ops-summary-writer`; rank 1; score 0.457
- Top neighbours: `travel-ops-summary-writer`/background_scale (0.457), `travel-ops-risk-reviewer`/background_scale (0.416), `travel-ops-compliance-checker`/background_scale (0.385), `travel-ops-dependency-mapper`/background_scale (0.381), `travel-ops-rewrite-editor`/background_scale (0.366)

### `doc_p2_document_rewriter`

- Gold: `document-rewriter`; rank 7; score 0.431
- Best non-core: `travel-ops-rewrite-editor`; rank 1; score 0.574
- Top neighbours: `travel-ops-rewrite-editor`/background_scale (0.574), `travel-ops-summary-writer`/background_scale (0.507), `method-note-builder`/reading_research (0.484), `travel-ops-handoff-brief-writer`/background_scale (0.441), `citation-note-extractor`/reading_research (0.437)

### `doc_p3_document_normaliser`

- Gold: `document-normaliser`; rank 2; score 0.454
- Best non-core: `travel-ops-rewrite-editor`; rank 1; score 0.515
- Top neighbours: `travel-ops-rewrite-editor`/background_scale (0.515), `document-normaliser`/documents_files (0.454), `method-note-builder`/reading_research (0.435), `public-office-meeting-notes`/public_imported_background (0.432), `facilities-ops-rewrite-editor`/background_scale (0.429)

### `doc_p4_field_extraction`

- Gold: `document-field-extractor`; rank 12; score 0.406
- Best non-core: `receipt-extractor`; rank 1; score 0.536
- Top neighbours: `receipt-extractor`/background_scale (0.536), `public-office-invoice-organizer`/public_imported_background (0.439), `procurement-ops-field-extractor`/background_scale (0.439), `finance-ops-artifact-packager`/background_scale (0.435), `public-office-invoice-generator`/public_imported_background (0.434)

### `doc_p5_comparison_preparation`

- Gold: `multi-document-comparison-preparer`; rank 2; score 0.470
- Best non-core: `privacy-policy-drafter`; rank 1; score 0.488
- Top neighbours: `privacy-policy-drafter`/background_scale (0.488), `multi-document-comparison-preparer`/documents_files (0.470), `writing-ops-comparison-builder`/background_scale (0.400), `legal-ops-comparison-builder`/background_scale (0.392), `terms-of-service-drafter`/background_scale (0.391)

### `doc_p6_conversion`

- Gold: `document-converter`; rank 2; score 0.413
- Best non-core: `public-markitdown`; rank 1; score 0.428
- Top neighbours: `public-markitdown`/public_imported_background (0.428), `document-converter`/documents_files (0.413), `layout-preserving-converter`/documents_files (0.401), `office-to-markdown-converter`/office_artifact_workflows (0.399), `public-office-form-builder`/public_imported_background (0.390)

### `doc_p7_layout_preserving_conversion`

- Gold: `layout-preserving-converter`; rank 1; score 0.424
- Best non-core: `public-office-form-builder`; rank 3; score 0.372
- Top neighbours: `layout-preserving-converter`/documents_files (0.424), `method-note-builder`/reading_research (0.397), `public-office-form-builder`/public_imported_background (0.372), `document-converter`/documents_files (0.371), `pdf-layout-reviewer`/office_artifact_workflows (0.340)

### `obs_p1_metrics_overview`

- Gold: `metrics-overview`; rank 1; score 0.468
- Best non-core: `cloud-ops-summary-writer`; rank 2; score 0.438
- Top neighbours: `metrics-overview`/metrics_observability (0.468), `cloud-ops-summary-writer`/background_scale (0.438), `cloud-ops-quality-auditor`/background_scale (0.409), `iot-ops-quality-auditor`/background_scale (0.406), `public-office-subscription-management`/public_imported_background (0.395)

### `obs_p2_latency_anomaly`

- Gold: `latency-anomaly-detector`; rank 1; score 0.606
- Best non-core: `cloud-ops-quality-auditor`; rank 2; score 0.467
- Top neighbours: `latency-anomaly-detector`/metrics_observability (0.606), `cloud-ops-quality-auditor`/background_scale (0.467), `cloud-ops-failure-diagnoser`/background_scale (0.453), `cloud-ops-intake-classifier`/background_scale (0.449), `api-ops-monitoring-plan-builder`/background_scale (0.448)

### `obs_p3_slo_breach`

- Gold: `slo-breach-checker`; rank 1; score 0.564
- Best non-core: `sre-ops-risk-reviewer`; rank 3; score 0.475
- Top neighbours: `slo-breach-checker`/metrics_observability (0.564), `metrics-overview`/metrics_observability (0.486), `sre-ops-risk-reviewer`/background_scale (0.475), `incident-ops-risk-reviewer`/background_scale (0.474), `sre-ops-failure-diagnoser`/background_scale (0.466)

### `obs_p4_capacity_risk`

- Gold: `capacity-risk-forecaster`; rank 1; score 0.546
- Best non-core: `risk-ops-failure-diagnoser`; rank 3; score 0.427
- Top neighbours: `capacity-risk-forecaster`/metrics_observability (0.546), `slo-breach-checker`/metrics_observability (0.446), `risk-ops-failure-diagnoser`/background_scale (0.427), `cloud-ops-scenario-planner`/background_scale (0.422), `support-ops-scenario-planner`/background_scale (0.396)

### `obs_p5_root_cause`

- Gold: `metrics-root-cause-diagnoser`; rank 1; score 0.486
- Best non-core: `support-ops-failure-diagnoser`; rank 2; score 0.465
- Top neighbours: `metrics-root-cause-diagnoser`/metrics_observability (0.486), `support-ops-failure-diagnoser`/background_scale (0.465), `cloud-ops-failure-diagnoser`/background_scale (0.461), `platform-ops-failure-diagnoser`/background_scale (0.447), `latency-anomaly-detector`/metrics_observability (0.444)

### `obs_p6_incident_summary`

- Gold: `incident-summary-writer`; rank 6; score 0.381
- Best non-core: `incident-ops-summary-writer`; rank 1; score 0.413
- Top neighbours: `incident-ops-summary-writer`/background_scale (0.413), `incident-ops-failure-diagnoser`/background_scale (0.409), `incident-ops-resource-linker`/background_scale (0.394), `incident-ops-timeline-builder`/background_scale (0.388), `public-office-microsoft-teams`/public_imported_background (0.386)

### `news_p1_plain_summary`

- Gold: `news-summariser`; rank 1; score 0.503
- Best non-core: `journalism-ops-summary-writer`; rank 5; score 0.426
- Top neighbours: `news-summariser`/news_monitoring (0.503), `news-briefing-writer`/news_monitoring (0.462), `paper-summariser`/reading_research (0.449), `general-source-summariser`/reading_research (0.434), `journalism-ops-summary-writer`/background_scale (0.426)

### `news_p2_briefing`

- Gold: `news-briefing-writer`; rank 2; score 0.463
- Best non-core: `events-ops-summary-writer`; rank 1; score 0.498
- Top neighbours: `events-ops-summary-writer`/background_scale (0.498), `news-briefing-writer`/news_monitoring (0.463), `events-ops-priority-ranker`/background_scale (0.441), `incident-summary-writer`/metrics_observability (0.432), `events-ops-handoff-brief-writer`/background_scale (0.423)

### `news_p3_grounded_claims`

- Gold: `source-grounding-extractor`; rank 24; score 0.392
- Best non-core: `product-ops-evidence-grounder`; rank 1; score 0.545
- Top neighbours: `product-ops-evidence-grounder`/background_scale (0.545), `vendor-ops-evidence-grounder`/background_scale (0.477), `marketing-ops-evidence-grounder`/background_scale (0.476), `ads-ops-evidence-grounder`/background_scale (0.471), `manufacturing-ops-evidence-grounder`/background_scale (0.454)

### `news_p4_theme_extraction`

- Gold: `news-theme-extractor`; rank 1; score 0.644
- Best non-core: `public-office-twitter-automation`; rank 8; score 0.388
- Top neighbours: `news-theme-extractor`/news_monitoring (0.644), `tech-news-trend-extractor`/news_monitoring (0.570), `news-summariser`/news_monitoring (0.455), `related-work-synthesiser`/reading_research (0.449), `news-briefing-writer`/news_monitoring (0.433)

### `news_p5_trend_signal`

- Gold: `tech-news-trend-extractor`; rank 1; score 0.719
- Best non-core: `social-ops-summary-writer`; rank 3; score 0.447
- Top neighbours: `tech-news-trend-extractor`/news_monitoring (0.719), `news-briefing-writer`/news_monitoring (0.474), `social-ops-summary-writer`/background_scale (0.447), `news-theme-extractor`/news_monitoring (0.445), `public-office-news-monitor`/public_imported_background (0.438)

### `office_p1_pdf_layout_review`

- Gold: `pdf-layout-reviewer`; rank 1; score 0.543
- Best non-core: `public-office-pdf-watermark`; rank 2; score 0.489
- Top neighbours: `pdf-layout-reviewer`/office_artifact_workflows (0.543), `public-office-pdf-watermark`/public_imported_background (0.489), `public-office-pdf-form-filler`/public_imported_background (0.466), `pdf-ocr-extractor`/office_artifact_workflows (0.449), `public-office-pdf-extraction`/public_imported_background (0.434)

### `office_p2_scanned_pdf_ocr`

- Gold: `pdf-ocr-extractor`; rank 1; score 0.642
- Best non-core: `public-office-pdf-ocr`; rank 2; score 0.570
- Top neighbours: `pdf-ocr-extractor`/office_artifact_workflows (0.642), `public-office-pdf-ocr`/public_imported_background (0.570), `public-office-smart-ocr`/public_imported_background (0.518), `public-office-pdf-extraction`/public_imported_background (0.448), `receipt-extractor`/background_scale (0.420)

### `office_p3_docx_redline`

- Gold: `docx-redline-editor`; rank 1; score 0.643
- Best non-core: `vendor-ops-rewrite-editor`; rank 2; score 0.561
- Top neighbours: `docx-redline-editor`/office_artifact_workflows (0.643), `vendor-ops-rewrite-editor`/background_scale (0.561), `pdf-layout-reviewer`/office_artifact_workflows (0.532), `docs-ops-risk-reviewer`/background_scale (0.531), `public-docx`/public_imported_background (0.514)

### `office_p4_formula_audit`

- Gold: `spreadsheet-formula-auditor`; rank 1; score 0.511
- Best non-core: `public-xlsx`; rank 2; score 0.479
- Top neighbours: `spreadsheet-formula-auditor`/office_artifact_workflows (0.511), `public-xlsx`/public_imported_background (0.479), `public-office-xlsx-manipulation`/public_imported_background (0.414), `data-analysis-with-validation`/data_spreadsheet (0.394), `public-office-financial-modeling`/public_imported_background (0.383)

### `office_p5_slide_visual_audit`

- Gold: `slide-deck-visual-auditor`; rank 1; score 0.668
- Best non-core: `public-office-ppt-visual`; rank 2; score 0.583
- Top neighbours: `slide-deck-visual-auditor`/office_artifact_workflows (0.668), `public-office-ppt-visual`/public_imported_background (0.583), `slide-outline-builder`/background_scale (0.434), `pdf-layout-reviewer`/office_artifact_workflows (0.418), `speaker-notes-writer`/background_scale (0.417)

### `office_p6_office_to_markdown`

- Gold: `office-to-markdown-converter`; rank 1; score 0.543
- Best non-core: `public-markitdown`; rank 3; score 0.446
- Top neighbours: `office-to-markdown-converter`/office_artifact_workflows (0.543), `docx-redline-editor`/office_artifact_workflows (0.541), `public-markitdown`/public_imported_background (0.446), `layout-preserving-converter`/documents_files (0.443), `public-docx`/public_imported_background (0.443)

### `plan_p1_meeting_agenda`

- Gold: `meeting-agenda-builder`; rank 1; score 0.618
- Best non-core: `meeting-ops-summary-writer`; rank 4; score 0.515
- Top neighbours: `meeting-agenda-builder`/planning_meetings (0.618), `task-extractor`/planning_meetings (0.534), `meeting-summary-writer`/planning_meetings (0.526), `meeting-ops-summary-writer`/background_scale (0.515), `meeting-followup-extractor`/planning_meetings (0.513)

### `plan_p2_meeting_summary`

- Gold: `meeting-summary-writer`; rank 1; score 0.631
- Best non-core: `meeting-ops-summary-writer`; rank 2; score 0.584
- Top neighbours: `meeting-summary-writer`/planning_meetings (0.631), `meeting-ops-summary-writer`/background_scale (0.584), `meeting-agenda-builder`/planning_meetings (0.530), `meeting-ops-rewrite-editor`/background_scale (0.520), `meeting-followup-extractor`/planning_meetings (0.496)

### `plan_p3_meeting_followup`

- Gold: `meeting-followup-extractor`; rank 6; score 0.477
- Best non-core: `meeting-ops-summary-writer`; rank 2; score 0.521
- Top neighbours: `meeting-summary-writer`/planning_meetings (0.525), `meeting-ops-summary-writer`/background_scale (0.521), `meeting-agenda-builder`/planning_meetings (0.484), `public-office-meeting-notes`/public_imported_background (0.484), `meeting-ops-rewrite-editor`/background_scale (0.479)

### `plan_p4_task_extractor`

- Gold: `task-extractor`; rank 2; score 0.549
- Best non-core: `meeting-ops-rewrite-editor`; rank 6; score 0.418
- Top neighbours: `weekly-planner`/planning_meetings (0.571), `task-extractor`/planning_meetings (0.549), `meeting-summary-writer`/planning_meetings (0.481), `meeting-followup-extractor`/planning_meetings (0.448), `meeting-agenda-builder`/planning_meetings (0.435)

### `plan_p5_weekly_planner`

- Gold: `weekly-planner`; rank 1; score 0.642
- Best non-core: `meeting-ops-scenario-planner`; rank 2; score 0.499
- Top neighbours: `weekly-planner`/planning_meetings (0.642), `meeting-ops-scenario-planner`/background_scale (0.499), `ux-ops-scenario-planner`/background_scale (0.483), `thesis-ops-scenario-planner`/background_scale (0.483), `repo-ops-scenario-planner`/background_scale (0.466)

### `read_p1_paper_summary`

- Gold: `paper-summariser`; rank 1; score 0.669
- Best non-core: `research-ops-summary-writer`; rank 3; score 0.439
- Top neighbours: `paper-summariser`/reading_research (0.669), `general-source-summariser`/reading_research (0.484), `research-ops-summary-writer`/background_scale (0.439), `citation-note-extractor`/reading_research (0.436), `multi-source-comparison-builder`/reading_research (0.430)

### `read_p2_general_source_summary`

- Gold: `general-source-summariser`; rank 2; score 0.498
- Best non-core: `research-ops-evidence-grounder`; rank 1; score 0.504
- Top neighbours: `research-ops-evidence-grounder`/background_scale (0.504), `general-source-summariser`/reading_research (0.498), `paper-summariser`/reading_research (0.471), `thesis-ops-evidence-grounder`/background_scale (0.470), `research-ops-summary-writer`/background_scale (0.447)

### `read_p3_citation_notes`

- Gold: `citation-note-extractor`; rank 1; score 0.718
- Best non-core: `note-linker`; rank 5; score 0.492
- Top neighbours: `citation-note-extractor`/reading_research (0.718), `citation-grounding-helper`/reading_research (0.566), `method-note-builder`/reading_research (0.519), `general-source-summariser`/reading_research (0.502), `note-linker`/background_scale (0.492)

### `read_p4_document_extraction`

- Gold: `document-extractor`; rank 2; score 0.559
- Best non-core: `finance-ops-field-extractor`; rank 3; score 0.501
- Top neighbours: `document-field-extractor`/documents_files (0.592), `document-extractor`/reading_research (0.559), `finance-ops-field-extractor`/background_scale (0.501), `database-ops-field-extractor`/background_scale (0.482), `web-data-extractor`/browser_web_automation (0.479)

### `read_p5_method_notes`

- Gold: `method-note-builder`; rank 14; score 0.383
- Best non-core: `manufacturing-ops-summary-writer`; rank 1; score 0.415
- Top neighbours: `manufacturing-ops-summary-writer`/background_scale (0.415), `energy-ops-summary-writer`/background_scale (0.411), `thesis-ops-summary-writer`/background_scale (0.408), `hr-ops-summary-writer`/background_scale (0.402), `ux-ops-summary-writer`/background_scale (0.400)

### `read_p6_grounding_check`

- Gold: `citation-grounding-helper`; rank 1; score 0.487
- Best non-core: `agent-ops-summary-writer`; rank 2; score 0.460
- Top neighbours: `citation-grounding-helper`/reading_research (0.487), `agent-ops-summary-writer`/background_scale (0.460), `citation-note-extractor`/reading_research (0.452), `qa-ops-summary-writer`/background_scale (0.440), `incident-ops-rewrite-editor`/background_scale (0.440)

### `read_p7_multi_source_comparison`

- Gold: `multi-source-comparison-builder`; rank 1; score 0.574
- Best non-core: `research-ops-comparison-builder`; rank 3; score 0.496
- Top neighbours: `multi-source-comparison-builder`/reading_research (0.574), `citation-note-extractor`/reading_research (0.516), `research-ops-comparison-builder`/background_scale (0.496), `related-work-synthesiser`/reading_research (0.496), `citation-grounding-helper`/reading_research (0.483)

### `read_p8_related_work_synthesis`

- Gold: `related-work-synthesiser`; rank 1; score 0.733
- Best non-core: `note-linker`; rank 4; score 0.454
- Top neighbours: `related-work-synthesiser`/reading_research (0.733), `multi-source-comparison-builder`/reading_research (0.492), `general-source-summariser`/reading_research (0.490), `note-linker`/background_scale (0.454), `method-note-builder`/reading_research (0.454)

### `reply_p1_professor_reply`

- Gold: `professor-email-reply`; rank 1; score 0.576
- Best non-core: `email-drafter`; rank 4; score 0.428
- Top neighbours: `professor-email-reply`/reply_messaging (0.576), `reply-polisher`/reply_messaging (0.441), `reply-drafter`/reply_messaging (0.437), `email-drafter`/email_communication (0.428), `groupwork-reply`/reply_messaging (0.412)

### `reply_p2_polish_supervisor`

- Gold: `reply-polisher`; rank 1; score 0.481
- Best non-core: `partnerships-ops-rewrite-editor`; rank 3; score 0.438
- Top neighbours: `reply-polisher`/reply_messaging (0.481), `followup-reply-writer`/reply_messaging (0.461), `partnerships-ops-rewrite-editor`/background_scale (0.438), `email-polisher`/email_communication (0.432), `groupwork-reply`/reply_messaging (0.398)

### `reply_p3_groupwork_coordination`

- Gold: `groupwork-reply`; rank 1; score 0.518
- Best non-core: `meeting-ops-summary-writer`; rank 2; score 0.381
- Top neighbours: `groupwork-reply`/reply_messaging (0.518), `meeting-ops-summary-writer`/background_scale (0.381), `meeting-summary-writer`/planning_meetings (0.378), `partnerships-ops-handoff-brief-writer`/background_scale (0.371), `partnerships-ops-failure-diagnoser`/background_scale (0.355)

### `reply_p4_followup_commitment`

- Gold: `followup-reply-writer`; rank 1; score 0.617
- Best non-core: `email-action-extractor`; rank 2; score 0.464
- Top neighbours: `followup-reply-writer`/reply_messaging (0.617), `email-action-extractor`/email_communication (0.464), `reply-polisher`/reply_messaging (0.444), `groupwork-reply`/reply_messaging (0.431), `meeting-followup-extractor`/planning_meetings (0.410)

### `reply_p5_generic_fresh_draft`

- Gold: `reply-drafter`; rank 2; score 0.553
- Best non-core: `email-polisher`; rank 3; score 0.541
- Top neighbours: `reply-polisher`/reply_messaging (0.604), `reply-drafter`/reply_messaging (0.553), `email-polisher`/email_communication (0.541), `followup-reply-writer`/reply_messaging (0.529), `groupwork-reply`/reply_messaging (0.490)

### `sec_p1_threat_model`

- Gold: `security-threat-modeler`; rank 12; score 0.337
- Best non-core: `public-openai-security-ownership-map`; rank 1; score 0.428
- Top neighbours: `public-openai-security-ownership-map`/public_imported_background (0.428), `privacy-risk-reviewer`/security_appsec (0.413), `auth-flow-reviewer`/security_appsec (0.377), `identity-ops-resource-linker`/background_scale (0.374), `privacy-ops-resource-linker`/background_scale (0.369)

### `sec_p2_security_code_review`

- Gold: `security-code-reviewer`; rank 4; score 0.401
- Best non-core: `api-ops-rewrite-editor`; rank 1; score 0.440
- Top neighbours: `api-ops-rewrite-editor`/background_scale (0.440), `auth-flow-reviewer`/security_appsec (0.432), `security-ops-rewrite-editor`/background_scale (0.402), `security-code-reviewer`/security_appsec (0.401), `api-ops-risk-reviewer`/background_scale (0.392)

### `sec_p3_dependency_risk`

- Gold: `dependency-risk-auditor`; rank 1; score 0.535
- Best non-core: `risk-ops-artifact-packager`; rank 2; score 0.480
- Top neighbours: `dependency-risk-auditor`/security_appsec (0.535), `risk-ops-artifact-packager`/background_scale (0.480), `risk-ops-dependency-mapper`/background_scale (0.470), `supply-chain-ops-risk-reviewer`/background_scale (0.391), `security-ops-dependency-mapper`/background_scale (0.381)

### `sec_p4_secret_leak`

- Gold: `secret-leak-scanner`; rank 1; score 0.470
- Best non-core: `environment-config-auditor`; rank 2; score 0.463
- Top neighbours: `secret-leak-scanner`/security_appsec (0.470), `environment-config-auditor`/background_scale (0.463), `security-ops-rewrite-editor`/background_scale (0.427), `deployment-build-triager`/deployment_browser_qa (0.401), `security-ops-artifact-packager`/background_scale (0.398)

### `sec_p5_auth_flow`

- Gold: `auth-flow-reviewer`; rank 1; score 0.380
- Best non-core: `identity-ops-failure-diagnoser`; rank 2; score 0.284
- Top neighbours: `auth-flow-reviewer`/security_appsec (0.380), `identity-ops-failure-diagnoser`/background_scale (0.284), `identity-ops-summary-writer`/background_scale (0.252), `identity-ops-resource-linker`/background_scale (0.232), `identity-ops-risk-reviewer`/background_scale (0.220)

### `sec_p6_privacy_review`

- Gold: `privacy-risk-reviewer`; rank 1; score 0.492
- Best non-core: `analytics-ops-compliance-checker`; rank 2; score 0.469
- Top neighbours: `privacy-risk-reviewer`/security_appsec (0.492), `analytics-ops-compliance-checker`/background_scale (0.469), `analytics-ops-risk-reviewer`/background_scale (0.462), `analytics-ops-quality-auditor`/background_scale (0.447), `dataset-ops-compliance-checker`/background_scale (0.415)

### `skill_p1_find_existing`

- Gold: `skill-finder`; rank 7; score 0.413
- Best non-core: `public-anthropic-doc-coauthoring`; rank 3; score 0.436
- Top neighbours: `meeting-followup-extractor`/planning_meetings (0.458), `method-note-builder`/reading_research (0.445), `public-anthropic-doc-coauthoring`/public_imported_background (0.436), `meeting-summary-writer`/planning_meetings (0.435), `meeting-ops-rewrite-editor`/background_scale (0.421)

### `skill_p2_install_existing`

- Gold: `skill-installer`; rank 201; score 0.244
- Best non-core: `public-office-data-analysis`; rank 1; score 0.609
- Top neighbours: `public-office-data-analysis`/public_imported_background (0.609), `public-office-sheets-automation`/public_imported_background (0.497), `data-analysis-for-reporting`/data_spreadsheet (0.479), `data-analysis-overview`/data_spreadsheet (0.459), `public-xlsx`/public_imported_background (0.457)

### `skill_p3_create_new`

- Gold: `skill-creator`; rank 1; score 0.573
- Best non-core: `public-anthropic-doc-coauthoring`; rank 6; score 0.380
- Top neighbours: `skill-creator`/skill_lifecycle (0.573), `skill-editor`/skill_lifecycle (0.498), `task-extractor`/planning_meetings (0.438), `skill-finder`/skill_lifecycle (0.427), `meeting-followup-extractor`/planning_meetings (0.397)

### `skill_p4_edit_existing`

- Gold: `skill-editor`; rank 74; score 0.434
- Best non-core: `course-ops-field-extractor`; rank 2; score 0.559
- Top neighbours: `document-field-extractor`/documents_files (0.616), `course-ops-field-extractor`/background_scale (0.559), `docs-ops-field-extractor`/background_scale (0.558), `writing-ops-field-extractor`/background_scale (0.554), `thesis-ops-field-extractor`/background_scale (0.551)

### `skill_p5_evaluate_existing`

- Gold: `skill-evaluator`; rank 8; score 0.387
- Best non-core: `email-polisher`; rank 3; score 0.528
- Top neighbours: `reply-polisher`/reply_messaging (0.601), `reply-drafter`/reply_messaging (0.576), `email-polisher`/email_communication (0.528), `followup-reply-writer`/reply_messaging (0.494), `email-drafter`/email_communication (0.440)

### `skill_p6_package_existing`

- Gold: `skill-packager`; rank 6; score 0.388
- Best non-core: `public-anthropic-doc-coauthoring`; rank 1; score 0.475
- Top neighbours: `public-anthropic-doc-coauthoring`/public_imported_background (0.475), `document-summariser`/documents_files (0.430), `public-office-content-writer`/public_imported_background (0.422), `docs-ops-summary-writer`/background_scale (0.397), `public-skill-installer`/public_imported_background (0.392)
