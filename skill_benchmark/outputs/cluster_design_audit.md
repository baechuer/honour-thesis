# Step 4b Manual Cluster Design Audit

Date: 2026-06-06

Purpose: manually inspect whether the benchmark clusters are defensible semantic-confusion units before adding more prompts. This audit uses prompt text, gold labels, alternatives, skill descriptions, and representative skill bodies. It is not a replacement for the automated Step 1-4 reports; it is the reasoning layer that decides whether expansion would improve the benchmark or merely add more volume.

Evaluation rule: a cluster is useful when a compressed selector could plausibly confuse several skills, but a careful procedural reading makes the gold skill better than the alternatives.

Status summary:

- Controlled clusters audited: 22/22.
- Public-gold source families triaged: 34/34.
- Overall decision: the benchmark is valid enough to continue experiments, but the next expansion should be targeted rather than broad.
- Highest-priority expansion targets: implicit-field stress, PDF/document operations, browser/deployment QA, Hugging Face workflows, skill representation analysis, API/tooling, GitHub/CI, and public-authored workflow clusters.
- Main risk: some clusters rely too much on explicit platform names or negative boundary phrases. These are still useful for retrieval, but they should not dominate final claims about procedural information.

## Controlled Cluster Audit

| Cluster | User-intent family | Main confusion source | Primary procedural axes | Manual judgment | Expansion decision |
|---|---|---|---|---|---|
| `api_backend_design` | Backend API and architecture work: OpenAPI review, external API integration, webhooks, service boundaries, migrations, dependency maps. | All prompts mention backend services, APIs, contracts, integration, or production risk. | Input artifact, workflow, output artifact, dependency direction, rollout risk, success criterion. | Strong cluster. Gold labels are usually obvious after reading the requested artifact and output: review an existing contract, plan an integration, design a webhook receiver, assess a migration, or map dependencies. | Expand carefully. Good candidate for 6-10 more prompts, especially cases where API, webhook, migration, and dependency-map wording overlaps more naturally. |
| `api_mcp_tooling` | Tool/API construction: REST contracts, MCP servers, webhook plans, auth integration, API docs, API security review. | Many alternatives share "API", "tools", "contract", "auth", and "integration" vocabulary. | Output artifact, dependency/tool, workflow, security success criterion. | Strong cluster. It tests the difference between public REST API design, MCP tool exposure, webhook handling, OAuth integration, documentation, and threat review. | Expand. Add prompts where the same source artifact could support docs, security review, and contract design to reduce reliance on explicit "do not" clauses. |
| `browser_web_automation` | Browser interaction tasks: snapshot, form fill, UI test, data extraction, debugging, accessibility. | All involve opening a web page and inspecting browser state. | Output artifact, action side effects, evidence type, success criterion. | Strong and realistic. The cluster has clean procedural boundaries: capture state, manipulate form, assert behavior, extract structured data, debug console/network failure, or audit accessibility. | Expand. Add more mixed browser requests where screenshot, test, and debugging are all plausible. |
| `code_github_workflow` | Repository work: local code review, PR review, resolving review comments, CI failure debugging, changelog, release notes. | All are software-change workflows and use similar GitHub/review language. | Input/precondition, output audience, workflow, side effects. | Strong, but overlaps with `github_ci_maintenance`. The two clusters can stay separate if framed as local/core workflow versus GitHub/CI maintenance. | Keep and expand only if new prompts clearly separate local patch review, PR review, review resolution, and CI diagnosis. |
| `data_spreadsheet` | Spreadsheet/data interpretation: overview, anomaly watchlist, validation, root cause, reporting, forecasting, ranking. | Same CSV can support many analysis styles, so descriptions are semantically close. | Success criterion, output artifact, workflow, decision purpose. | Very strong. This is one of the best clusters for the thesis because the same input artifact changes gold skill depending on analytical intent. | Expand. Add more cases with the same dataset but different requested decision outputs; include public spreadsheet skills as distractors. |
| `deployment_browser_qa` | Deployment, browser QA, release verification, build triage, visual regression, performance budgets. | All concern web app readiness or browser/deploy failures. | Input artifact, tool/dependency, evidence type, output artifact, success criterion. | Strong. The cluster is realistic and procedurally diverse, but some prompts contain explicit boundaries that make selection easier. | Expand with lower-boundary prompts. Add cases where release verification, visual regression, performance, and browser debugging are all plausible without overusing "not X" wording. |
| `documents_files` | General document workflows: summarize, rewrite, normalize, extract fields, compare documents, convert, preserve layout. | All use document-processing vocabulary and overlapping source artifacts. | Output artifact, transformation type, preservation constraint, workflow. | Strong. Gold choices are usually stable because output shapes differ sharply. | Expand. Good for more semantic-neighbour cases, especially conversion vs normalization vs layout-preserving conversion. |
| `github_ci_maintenance` | GitHub operational workflows: CI logs, PR comments, repo review, issue triage, release changelog, git guardrails. | All use GitHub/repo/PR/CI vocabulary. Public imported skills create realistic near-neighbours. | Input/precondition, dependency/tool, workflow, output audience, side effects. | Strong but partially redundant with `code_github_workflow`. Valuable because it includes public skills and tool-specific workflows. | Expand moderately. Add public-derived cases but keep duplicate/equivalent skills as acceptable alternatives when needed. |
| `huggingface_ml_workflows` | Hugging Face and ML workflow tasks: dataset inspection, local model choice, fine-tuning, Gradio, ZeroGPU deployment, evaluation. | All mention Hugging Face, models, datasets, demos, or evaluation. | Dependency/tool, input/precondition, workflow, output artifact, resource constraint. | Strong. Especially good for testing dependencies and resource constraints, such as 8 GB local model selection versus training or deployment. | Expand. Add more public Hugging Face skills and prompts where model selection, dataset inspection, evaluation, and deployment are easily confused. |
| `implicit_field_stress` | Prose-only skills where fields must be inferred: PDF evidence/table tasks, browser visual/flow tasks, metrics alerts/dashboards/traces/narratives. | Raw skills do not expose neat fields directly; selectors must infer procedural information. | Inferred workflow, output artifact, evidence type, success criterion. | Very important cluster. It directly tests whether a representation layer can recover hidden procedural information rather than relying on hand-authored schema fields. | Highest-priority expansion. Add more implicit cases and keep raw skill files prose-like. |
| `metrics_observability` | Metric interpretation and incident reporting: overview, anomalies, SLO breach, root cause, capacity, incident summary. | All talk about metrics, incidents, anomalies, and operational health. | Analytical goal, output artifact, time horizon, success criterion. | Strong. It distinguishes summary, diagnosis, forecasting, SLO checking, and incident narrative. | Expand slightly. Add prompts where anomaly detection and root-cause diagnosis are both plausible. |
| `news_monitoring` | News processing: summary, briefing, source grounding, trends, themes. | All involve news articles and summarization-like language. | Output audience, evidence grounding, aggregation scope, success criterion. | Medium. Useful but smaller and more writing-oriented; semantic confusion is real, but procedural differences can become audience/style differences. | Revise before expansion. Add stronger evidence-grounding and multi-source trend cases if expanded. |
| `observability_reliability` | SRE/observability construction and diagnosis: Prometheus alerts, Grafana dashboards, traces, SLO narrative, resilience review, service mesh. | All concern system reliability and observability artifacts. | Dependency/tool, input artifact, output artifact, diagnostic workflow. | Strong. Good external validity because public SWE skills act as realistic distractors. | Expand. Add cases with overlapping observability terms but different artifacts: alert rules, dashboard, trace diagnosis, resilience code review. |
| `office_artifact_workflows` | Office artifact operations: rendered PDF layout, OCR, DOCX redline, XLSX formula audit, slide visual audit, office-to-Markdown conversion. | All involve office/document artifacts and conversion/review terms. | File type, output artifact, preservation constraint, tool dependency, workflow. | Strong. Good thesis examples because file type and transformation constraints matter. | Expand. Add more public-derived cases and make some prompts less file-extension-obvious. |
| `office_business_automation` | Business tool automation: Excel formulas, Airtable, Notion, calendar scheduling, meeting action extraction, email classification. | All are office/business productivity automations. | Platform dependency, output artifact, workflow, side effects. | Medium-strong. Realistic, public-grounded, but many cases are selected by platform name, which can be too easy. | Expand only with care. Add cross-platform prompts where workflow requirements distinguish skills beyond the product name. |
| `pdf_document_operations` | Atomic PDF operations: question answering, table extraction, OCR, form filling, redaction review, PDF-to-DOCX conversion. | All mention PDFs and information extraction/conversion. | Input state, output artifact, workflow, evidence anchors, safety constraint. | Very strong. This is one of the clearest thesis clusters: same artifact family, different procedural goal. | Expand. Good candidate for a thesis example table and additional prompts. |
| `planning_meetings` | Planning and meeting note workflows: agenda, recap, follow-up, task extraction, weekly plan. | All involve meetings, notes, tasks, plans, and scheduling. | Temporal stage, output artifact, actionability, scope. | Medium. Valid but less technical; some distinctions are writing-output differences rather than deep procedural constraints. | Keep but do not prioritize expansion unless adding stronger calendar/meeting-resource dependencies. |
| `reading_research` | Research reading workflows: paper summary, general source summary, citation notes, field extraction, method notes, grounding check, comparison, synthesis. | All are source-reading and literature-review tasks. | Output artifact, evidence use, analytical lens, number of sources, success criterion. | Strong. This cluster is highly relevant to academic-agent use and has stable procedural distinctions. | Expand. Add more public/literature-grounded cases; use it as a thesis-friendly example cluster. |
| `reply_messaging` | Message drafting and editing: professor reply, polish existing draft, group coordination, follow-up commitments, generic draft. | All involve email or message generation. | Input/precondition, tone/audience, output artifact, commitment focus. | Medium. Useful near-boundary cluster, but gold choices can be tone-dependent and prompt wording often strongly signals the answer. | Keep small. Do not expand heavily unless adding more concrete preconditions, such as existing draft versus source message versus multi-party coordination. |
| `security_appsec` | Security workflows: threat model, code review, dependency risk, secret leak, auth flow, privacy review. | All use security/risk language. | Threat scope, input artifact, workflow, output artifact, success criterion. | Strong. Very useful because the wrong skill can be plausible and materially wrong. | Expand. Add public security skills and more prompts where privacy, auth, code review, and threat modeling overlap. |
| `skill_lifecycle` | Skill management lifecycle: find, install, create, edit, evaluate, package. | All are about skills and skill libraries. | Operation stage, side effects, output artifact, precondition. | Medium-strong. Central to thesis but self-referential; some prompts become easy because verbs like "install" or "create" are explicit. | Expand carefully. Use less verb-obvious prompts and include public skill cases only after acceptable alternatives are documented. |
| `skill_representation_analysis` | Meta-analysis of skill artifacts: field audit, authoring, routing policy, hierarchy flattening, installation wrapper, benchmark evaluation. | All mention skills, representation, routing, and benchmark concepts. | Output artifact, workflow, evaluation target, dependency/resource handling. | Very important but high co-adaptation risk. It directly targets the thesis concept, so it can accidentally encode the proposed field taxonomy too neatly. | Expand with caution. Add public-authored messy skill artifacts and implicit/hierarchical cases; avoid using only our own schema vocabulary. |

## Controlled Expansion Queue

Priority 1 expansion:

- `implicit_field_stress`
- `pdf_document_operations`
- `documents_files`
- `browser_web_automation`
- `deployment_browser_qa`
- `huggingface_ml_workflows`
- `reading_research`
- `security_appsec`
- `skill_representation_analysis`

Priority 2 expansion:

- `api_backend_design`
- `api_mcp_tooling`
- `github_ci_maintenance`
- `observability_reliability`
- `data_spreadsheet`
- `office_artifact_workflows`

Freeze or revise before expansion:

- `reply_messaging`: useful but too tone/style dependent unless prompts include clearer preconditions.
- `planning_meetings`: useful but currently less central to technical skill retrieval.
- `news_monitoring`: revise with stronger grounding, trend, and multi-source evidence tasks.
- `office_business_automation`: platform-name cues are strong; add cross-platform ambiguity before expansion.
- `skill_lifecycle`: central but verb cues are strong; add less explicit prompts and acceptable alternatives.

## Public-Gold Source-Family Triage

Public-gold cases should remain a separate external-validity stratum. Many public skills are broad, duplicated, or platform-specific. A source family can support expansion only when the gold label is stable after reading alternatives and when the distinguishing field is not merely the platform name.

| Source family | Cases | Manual judgment | Expansion decision |
|---|---:|---|---|
| `agent-workflow` | 4 | Strong procedural differences: context preparation, spec-driven work, test-driven work, source-driven work. Some boundary phrases are strong, but the workflows are genuinely different. | Expand. Good for public-authored procedural workflows. |
| `api-docs` | 1 | Stable but provider-name-driven. Useful as dependency/tool case, weak as procedural-confusion evidence alone. | Keep; expand only with multiple API-doc providers and similar tool-use requests. |
| `api-mcp` | 3 | Strong: MCP server, ChatGPT app, CLI generator differ in output artifact and tool dependency. | Expand. |
| `audio` | 2 | Clear input/output polarity: transcription versus speech generation. Useful but relatively easy. | Keep; add harder audio cases only if needed. |
| `browser-qa` | 3 | Strong: DevTools diagnosis, Playwright test, screenshot capture. Good public analogue of controlled browser clusters. | Expand. |
| `codex-migration` | 1 | Stable but singleton; risk of overlap with skill creator/installer. | Keep as external case, not expansion priority. |
| `commerce-automation` | 1 | Platform-name-driven Shopify case; alternatives are near-domain commerce platforms. | Keep with caveat; expand only if adding workflow-specific commerce cases. |
| `data-analysis` | 1 | Jupyter output artifact is clear. Singleton and tool-name-driven. | Keep. |
| `data-office` | 2 | ETL pipeline versus database sync is procedurally strong. | Expand moderately. |
| `deployment` | 3 | Strong provider-specific deploy tasks; distinction is mostly platform/tool plus output artifact. | Expand but add platform-ambiguous deployment planning cases. |
| `document-conversion` | 1 | MarkItDown mixed-format conversion is stable but broad. | Keep; possible expansion with mixed-file conversion versus office-specific conversion. |
| `figma` | 4 | Strong but sometimes close: implement design, Code Connect, generate library, create rules. `generate_library` remains a known hard case. | Expand after manual examples; good for output-artifact distinctions. |
| `finance-analytics` | 3 | Strong: SaaS metrics, stock analysis, DCF valuation. Uses distinct analytical outputs and success criteria. | Expand. |
| `github-ci` | 4 | Strong and public-grounded: CI analysis, pre-commit setup, git guardrails, PR comments. Some duplicates with controlled skills need acceptable alternatives. | Expand with acceptable-alternative tracking. |
| `github-workflow` | 1 | Stable OpenAI `yeet` workflow, but singleton and product-specific. | Keep. |
| `huggingface` | 12 | Strongest public family. Many near-neighbour HF skills differ by dataset/model/training/demo/deployment/evaluation. | Highest-priority public expansion. |
| `issue-tracking` | 1 | Stable Linear-specific workflow but singleton/platform-driven. | Keep. |
| `notion-workflow` | 3 | Strong: knowledge capture, meeting intelligence, spec-to-implementation. | Expand moderately. |
| `observability` | 1 | Sentry issue workflow is stable but singleton/tool-driven. | Keep; combine with observability controlled expansion. |
| `obsidian` | 3 | Strong output/tool differences: JSON Canvas, Bases, CLI. | Expand if more Obsidian/public notes cases are available. |
| `office-artifact` | 1 | AI slide generation is stable but singleton. | Keep; combine with controlled office artifact workflows. |
| `office-automation` | 3 | Excel, Sheets, Airtable are platform-specific but workflow/output distinctions are clear. | Expand carefully; avoid only platform-name prompts. |
| `office-business` | 3 | Contract review, suspicious email, invoice automation are realistic and distinct. | Expand. |
| `office-document` | 4 | Strong PDF public cases: extraction, OCR, form fill, merge/split. | Expand; good external version of controlled PDF cluster. |
| `openai-api` | 1 | Stable official-docs dependency case, but provider-name-driven. | Keep as dependency/tool case. |
| `sales-automation` | 1 | Lead routing versus qualification/research is plausible. Singleton. | Keep; expand if more CRM/sales public skills are imported. |
| `security` | 1 | Public threat model is stable but broad; overlaps with controlled security cluster. | Keep with acceptable alternatives. |
| `skill-lifecycle` | 1 | Public skill creator overlaps with local skill creator and is a known ambiguity risk. | Do not expand until duplicate/local equivalent handling is explicit. |
| `software-design` | 3 | Strong enough: API/interface design, deprecation migration, ADR documentation. | Expand moderately. |
| `software-maintenance` | 1 | Systematic debugging is stable but broad. | Keep; potential near-neighbours with browser/code debugging. |
| `support-automation` | 1 | Zendesk automation is stable but platform-name-driven. | Keep; expand only with support workflow variants. |
| `visual-design` | 2 | Canvas design versus theme factory is useful but broad/design-output oriented. | Keep as public externality, not core expansion. |
| `web-quality` | 5 | Strong public cluster: accessibility, Core Web Vitals, SEO, performance, quality audit. | Expand. |
| `writing` | 1 | Doc coauthoring is broad and writing-style dependent. | Keep, not expansion priority. |

## Recommended Next Construction Actions

1. Expand controlled benchmark to 180-220 prompts only after selecting clusters from the Priority 1 and Priority 2 queues.
2. Add 40-60 new controlled prompts with less explicit negation, especially for implicit-field stress and public-derived hard cases.
3. Add 30-50 public-gold prompts from high-confidence public families: Hugging Face, browser QA, GitHub/CI, office-document, web-quality, Figma, deployment, and agent-workflow.
4. For every new prompt, store:
   - gold rationale;
   - alternative rejection rationale;
   - field axes;
   - acceptable alternatives;
   - ambiguity risk.
5. Do not expand clusters whose main distinction is only platform name unless the prompt also tests workflow, output, or dependency constraints.
6. Do not use broad router/hierarchical public skills as strict gold labels unless the request explicitly asks for routing or orchestration.
7. Preserve some low-information and implicit-field prompts, but score them separately so they do not obscure the main controlled evidence.

## Thesis-Ready Interpretation

This audit supports the benchmark design claim, with caveats:

- The controlled benchmark is not merely a collection of unrelated skills; most clusters contain semantically close skills with meaningful procedural differences.
- The strongest evidence clusters are those where the same high-level domain and often the same input artifact can lead to different correct skills depending on requested output, workflow, evidence type, or success criterion.
- Public skills improve external validity, but public-gold cases must be separated because public skills are often broad, duplicated, platform-specific, or hierarchical.
- Future expansion should increase confusability quality, not just prompt count.

