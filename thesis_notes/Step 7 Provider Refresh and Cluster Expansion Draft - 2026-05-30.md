# Step 7 Provider Refresh And Cluster Expansion Draft

Date: 2026-05-30

Purpose: refresh stale provider runs on the 2349-skill public-expanded library, then define the next controlled-core expansion so the benchmark is less dependent on a small hand-built set of clusters.

## What Was Rerun

All runs below use:

- 85 evaluated prompts.
- 2349 total skills.
- 85 controlled/evaluated core skills.
- 1800 generated background skills.
- 460 imported public skills.
- 4 support/email skills.
- Qwen `text-embedding-v4` as the dense embedding model.

| Method | Top-1 | Top-5 | MRR | Public top-1 | Non-main top-1 | Notes |
|---|---:|---:|---:|---:|---:|---|
| Qwen R1 flat-card embedding | 35.3% | 48.2% | 0.426 | 14.1% | 50.6% | Flat descriptions are highly vulnerable to background/public collisions. |
| Qwen R1 + Qwen rerank top-20 | 60.0% | 63.5% | 0.615 | 16.5% | 36.5% | Generic reranking helps, but still leaves many non-main winners. |
| Qwen R1 + local schema rerank top-100 | 69.4% | 74.1% | 0.719 | 1.2% | 21.2% | Schema reranking repairs many flat-card failures if gold is in the candidate set. |
| Qwen R2 structured-card embedding | 50.6% | 64.7% | 0.571 | 9.4% | 36.5% | Structured text helps over R1, but embedding alone is still not enough. |
| Qwen R2 + Qwen rerank top-20 | 65.9% | 70.6% | 0.682 | 9.4% | 27.1% | Best generic reranker condition among R1/R2/full. |
| Qwen R2 + local schema rerank top-100 | 80.0% | 84.7% | 0.820 | 4.7% | 14.1% | Strong structured-representation result. |
| Qwen full-skill embedding | 50.6% | 69.4% | 0.590 | 1.2% | 30.6% | Full artifact embeddings improve top-5 over R2, but not top-1. |
| Qwen full-skill + Qwen rerank top-20 | 61.2% | 68.2% | 0.648 | 3.5% | 34.1% | Generic reranking improves top-1 but does not reduce non-main failures. |
| Qwen full-skill + local schema rerank top-50 | 80.0% | 84.7% | 0.822 | 2.4% | 12.9% | Strong hybrid result with smaller candidate budget. |
| Qwen full-skill + local schema rerank top-100 | 84.7% | 89.4% | 0.872 | 1.2% | 9.4% | Current strongest 2349-scale method. |

## Interpretation

The refreshed provider runs strengthen the current thesis framing:

- Dense retrieval is useful for broad candidate generation, but it is not sufficient for final skill selection under semantic similarity and scale.
- R1 flat metadata is fragile in a public-expanded library: it has the highest non-main top-1 rate and frequent public-skill collisions.
- R2 structured cards improve over R1, which suggests that preserving procedural fields changes retrieval behavior even before reranking.
- Qwen's generic reranker improves top-1, but it does not consistently reduce public/background false positives.
- The local schema reranker is currently strongest, but it depends on the first-stage retriever surfacing the gold skill. This means the final thesis should report both first-stage candidate quality and final reranking accuracy.

## Strongest-Method Failure Pattern

For Qwen full-skill embedding plus local schema rerank top-100, there are 13 strict top-1 failures.

First-stage exclusion failures, where gold is outside the top-100 and reranking cannot recover it:

- `web_p5_frontend_debugging`: gold `frontend-debugger`, first-stage rank 428.
- `code_p1_local_code_review`: gold `code-reviewer`, first-stage rank 903.
- `doc_p1_document_summary`: gold `document-summariser`, first-stage rank 134.
- `doc_p7_layout_preserving_conversion`: gold `layout-preserving-converter`, first-stage rank 1251.
- `office_p6_office_to_markdown`: gold `office-to-markdown-converter`, first-stage rank 711.
- `skill_p2_install_existing`: gold `skill-installer`, first-stage rank 297.
- `skill_p4_edit_existing`: gold `skill-editor`, first-stage rank 484.

Reranking or ambiguity failures, where gold is in the top-100 but not ranked first:

- `web_p6_accessibility_check`: `accessibility-checker` is ranked second behind `accessibility-interaction-auditor`.
- `code_p2_pr_review`: `pr-reviewer` is ranked second.
- `doc_p4_field_extraction`: `document-field-extractor` is ranked seventeenth.
- `read_p4_document_extraction`: `document-extractor` starts first-stage rank 1 but is reranked below `web-data-extractor`.
- `reply_p5_generic_fresh_draft`: `reply-drafter` is ranked second behind `reply-polisher`.
- `skill_p5_evaluate_existing`: `skill-evaluator` is ranked second behind `reply-polisher`.

Implication: future work should not only add more methods. It should harden the benchmark and representation design around two separate questions:

- Does the first-stage representation include enough information for candidate recall?
- Does the final representation include enough procedural information for reranking among near-neighbours?

## New Controlled Cluster Drafts

The current controlled core has 85 prompts. To answer the criticism that the testing clusters are still small, the next expansion should add around 8 clusters with 5-6 prompts each. That would move the controlled core toward roughly 125-135 prompts without making manual adjudication impossible.

Each proposed cluster below is grounded in patterns observed in the imported public skills, but the evaluated skills should remain atomic. Public skills can be used as background competitors or inspiration, while controlled skills should avoid hierarchical "if finance, go to this other document" routing.

### Cluster A: PDF And Document Operations

Public grounding:

- `public-office-chat-with-pdf`
- `public-office-pdf-extraction`
- `public-office-pdf-ocr`
- `public-office-pdf-form-filler`
- `public-office-pdf-to-docx`
- `public-openai-pdf`
- `public-markitdown`

Controlled atomic skills to add:

- `pdf-question-answerer`: answers user questions from PDF content with citations.
- `pdf-layout-table-extractor`: extracts tables/fields while preserving page and cell structure.
- `pdf-ocr-cleaner`: handles scanned PDFs, OCR, deskew/noise cleanup, and confidence warnings.
- `pdf-form-filler`: writes values into existing form fields and validates required fields.
- `pdf-redaction-reviewer`: identifies sensitive text and produces a redaction plan, not extraction.
- `pdf-to-docx-converter`: converts PDF to editable DOCX while preserving headings/layout as much as possible.

Key differentiating fields:

- Input state: scanned PDF vs digital PDF vs form PDF.
- Output artifact: answer, table, cleaned text, filled PDF, redaction report, converted DOCX.
- Workflow: OCR, layout analysis, form validation, citation grounding, conversion.
- Constraints: do not summarize when field extraction or redaction is requested.

Example prompt pressure:

- "Extract invoice line items from this scanned PDF and keep page/row references."
- "Fill the provided tax form PDF using these supplied values."

### Cluster B: Web Quality, Testing, And Browser Automation

Public grounding:

- `public-addy-web-accessibility`
- `public-addy-web-core-web-vitals`
- `public-addy-web-performance`
- `public-addy-web-seo`
- `public-addy-web-web-quality-audit`
- `public-anthropic-webapp-testing`
- `public-openai-playwright`
- `public-office-browser-automation`

Controlled atomic skills to add:

- `web-accessibility-auditor`: checks WCAG/accessibility issues and gives remediation.
- `web-performance-profiler`: measures load/runtime performance and identifies bottlenecks.
- `seo-metadata-auditor`: checks title/meta/schema/indexing/search snippets.
- `browser-flow-tester`: executes a user flow and verifies interaction states.
- `visual-regression-comparator`: compares screenshots against a baseline.
- `web-quality-summary-auditor`: produces a broad triage report across accessibility/performance/SEO without deep fixes.

Key differentiating fields:

- Required tools: browser, Playwright, Lighthouse, accessibility checker, screenshot diff.
- Output artifact: test trace, audit report, optimization plan, screenshot diff, metadata checklist.
- Success criterion: passing interaction vs lower LCP/CLS vs WCAG issue list vs SEO compliance.

Example prompt pressure:

- "The checkout page loads slowly after login; find the frontend bottleneck, not SEO issues."
- "Compare this new landing page screenshot against the approved design."

### Cluster C: GitHub, CI, And Repository Maintenance

Public grounding:

- `public-openai-gh-fix-ci`
- `public-openai-gh-address-comments`
- `public-openai-yeet`
- `public-n-skills-open-source-maintainer`
- `public-swebench-analyze-ci`
- `public-swebench-github-actions-templates`
- `public-mattpocock-review`

Controlled atomic skills to add:

- `ci-log-root-cause-debugger`: diagnoses failing CI from logs and proposes a fix.
- `pr-review-comment-resolver`: maps reviewer comments to code changes and responds.
- `repo-code-reviewer`: reviews a diff for bugs and maintainability without applying changes.
- `github-issue-triager`: classifies issues and requests missing reproduction details.
- `release-changelog-generator`: writes release notes from commits/PRs.
- `git-safety-guardrail-installer`: configures hooks or guardrails against dangerous commands.

Key differentiating fields:

- Input artifact: CI logs, PR review comments, git diff, issue queue, commit list, local repo config.
- Output artifact: root-cause diagnosis, patch plan, review findings, triage labels, changelog, hook config.
- Side effects: whether the skill may modify files, post replies, or configure hooks.

Example prompt pressure:

- "The CI failed after this PR; inspect the logs and identify the failing check."
- "Address these reviewer comments and prepare a concise response."

### Cluster D: Hugging Face And ML Workflow Skills

Public grounding:

- `public-huggingface-datasets`
- `public-huggingface-huggingface-local-models`
- `public-huggingface-train-sentence-transformers`
- `public-huggingface-huggingface-gradio`
- `public-huggingface-huggingface-community-evals`
- `public-huggingface-huggingface-zerogpu`
- `public-huggingface-huggingface-papers`

Controlled atomic skills to add:

- `hf-dataset-viewer-inspector`: fetches dataset metadata/splits/rows.
- `hf-local-model-selector`: selects a model and quantization for local hardware.
- `sentence-transformer-finetuner`: plans or runs embedding model fine-tuning/evaluation.
- `gradio-demo-builder`: builds a Gradio UI around a model or pipeline.
- `zerogpu-space-deployer`: prepares a Hugging Face Space for ZeroGPU constraints.
- `community-eval-runner`: runs or prepares model evaluation with defined benchmarks.

Key differentiating fields:

- Input artifact: dataset id, model id, hardware budget, training pairs, demo spec, eval suite.
- Dependencies/tools: Hugging Face Hub APIs, `hf` CLI, TRL, sentence-transformers, Gradio, lighteval/inspect.
- Output artifact: dataset report, model recommendation, training config, app scaffold, deployment plan, eval report.

Example prompt pressure:

- "I need an embedding model for semantic skill routing on an 8 GB Mac; choose a local candidate."
- "Build a Gradio demo for this classifier, not a training script."

### Cluster E: API, MCP, And Tool Integration

Public grounding:

- `public-addy-agent-api-and-interface-design`
- `public-api-design-principles`
- `public-anthropic-mcp-builder`
- `public-swebench-mcp-builder`
- `public-office-webhook-automation`
- `public-oh-my-authentication-setup`

Controlled atomic skills to add:

- `rest-api-contract-designer`: designs REST endpoints, schemas, status codes, pagination, and errors.
- `openapi-contract-reviewer-v2`: reviews an existing OpenAPI spec for compatibility and examples.
- `mcp-server-builder`: builds MCP server tools/resources with schema validation.
- `webhook-integration-planner`: designs event subscriptions, retries, signing, and idempotency.
- `auth-flow-integrator`: implements or audits OAuth/API-key/session authentication flows.
- `api-documentation-writer`: produces developer-facing docs from an existing API contract.

Key differentiating fields:

- Output artifact: API design, review report, MCP implementation, webhook plan, auth integration, documentation.
- Dependencies: OpenAPI, OAuth provider, MCP SDK, webhook platform.
- Preconditions: new design vs existing spec vs running service.

Example prompt pressure:

- "Review this OpenAPI contract for client-breaking issues; do not design a new API."
- "Create an MCP server wrapper for these two file operations."

### Cluster F: Observability And Reliability

Public grounding:

- `public-swebench-prometheus-configuration`
- `public-swebench-grafana-dashboards`
- `public-swebench-distributed-tracing`
- `public-swebench-python-observability`
- `public-swebench-service-mesh-observability`
- `public-swebench-python-resilience`

Controlled atomic skills to add:

- `prometheus-alert-rule-writer`: writes alerting rules from SLO/metric definitions.
- `grafana-dashboard-builder`: builds dashboard panels and variables for service metrics.
- `distributed-trace-investigator`: diagnoses request latency/failure from traces.
- `slo-breach-narrative-writer`: summarizes SLO breach impact and timeline.
- `resilience-pattern-reviewer`: checks retries, timeouts, circuit breakers, and fallback behavior.
- `service-mesh-traffic-debugger`: inspects mesh routing, retries, mTLS, and traffic splits.

Key differentiating fields:

- Input artifact: metrics, dashboard requirements, trace spans, incident timeline, code/config, mesh manifests.
- Output artifact: alert rules, dashboard JSON, trace diagnosis, incident narrative, resilience review, mesh fix plan.
- Success criterion: actionable operational artifact, not generic observability advice.

Example prompt pressure:

- "Create Prometheus alerts for this latency SLO; do not build a dashboard."
- "Use trace spans to find why checkout requests are slow."

### Cluster G: Office And Business Automation

Public grounding:

- `public-office-xlsx-manipulation`
- `public-office-airtable-automation`
- `public-office-notion-automation`
- `public-office-calendar-automation`
- `public-office-meeting-notes`
- `public-office-email-classifier`
- `public-office-data-extractor`

Controlled atomic skills to add:

- `xlsx-formula-model-builder`: creates spreadsheet formulas/models from tabular requirements.
- `airtable-workflow-automator`: creates Airtable fields/views/automations.
- `notion-research-database-builder`: organizes research notes into Notion database properties.
- `calendar-scheduling-optimizer`: proposes meeting times and time blocks.
- `meeting-notes-action-extractor`: extracts decisions/actions from meeting transcripts.
- `email-classification-router`: classifies and routes emails into categories/actions.

Key differentiating fields:

- Input artifact: spreadsheet, Airtable base, Notion workspace, calendar constraints, transcript, email inbox/export.
- Output artifact: workbook, automation plan, database schema, schedule proposal, action list, classification labels.
- Dependencies: Excel/openpyxl, Airtable API, Notion API, calendar APIs, email client.

Example prompt pressure:

- "Turn these meeting notes into owners and due dates; do not draft follow-up emails."
- "Build a workbook formula model for these revenue assumptions."

### Cluster H: Agent Skill Lifecycle And Representation

Public grounding:

- `public-anthropic-skill-creator`
- `public-mattpocock-write-a-skill`
- `public-addy-agent-using-agent-skills`
- `public-mattpocock-setup-matt-pocock-skills`
- `public-skill-installer`
- `public-oh-my-agentic-skills`

Controlled atomic skills to add:

- `skill-authoring-guide`: creates or revises a `SKILL.md` artifact.
- `skill-field-auditor`: extracts representation fields from an existing skill.
- `skill-installer-wrapper`: installs a public skill into a local skill directory.
- `skill-router-policy-designer`: designs routing rules and candidate selection policy.
- `skill-hierarchy-flattener`: converts broad hierarchical skills into atomic child skills.
- `skill-benchmark-evaluator`: evaluates skills against prompts and gold labels.

Key differentiating fields:

- Input artifact: new skill request, existing skill file, GitHub source, routing spec, hierarchy, benchmark results.
- Output artifact: skill file, field audit JSON, installed skill, policy spec, atomic skill set, evaluation report.
- Side effects: file writes, installation, benchmark execution.

Example prompt pressure:

- "Audit this existing skill and extract input/output/workflow/dependency fields."
- "Flatten this broad skill into atomic children, preserving cross-references."

## Fields To Stress In The Next Expansion

The next clusters should deliberately include cases where the key distinction is not only visible in a clean heading. This addresses the concern that the current schema reranker may be too aligned with how the old controlled skills were authored.

Add prompts and skills that test:

- implicit input/precondition: the required input is implied by commands, examples, or artifact names rather than an `inputs` heading.
- output artifact distinction: summary vs patch vs JSON vs dashboard vs filled PDF vs deployed app.
- tool/dependency distinction: Playwright vs Lighthouse vs OCR vs Hugging Face Hub vs MCP SDK vs Airtable API.
- side-effect distinction: read-only review vs file modification vs deploy/post/install.
- hierarchy flattening: broad public skills that link to subskills should be represented as atomic controlled skills for evaluation.
- boundary/negative information: keep `not_for` as evidence, but avoid making it the only reason a gold label is correct.

## Recommended Next Action

Before implementing all clusters, add one pilot expansion with two clusters:

1. PDF/document operations, because public skills strongly support this domain and current document failures remain common.
2. Hugging Face/ML workflows, because these public skills contain concrete dependencies and procedures that are not already dominant in the controlled core.

After adding the pilot:

1. Export R1-R3 representations.
2. Rerun Steps 1-4.
3. Rerun Step 7 lexical/schema and Qwen full-skill + local schema top-100.
4. Manually inspect new non-core/public winners.
5. Only then add the remaining clusters.

