#!/usr/bin/env python3

from __future__ import annotations

import json
import shutil
from pathlib import Path


SKILL_TEMPLATE = """---
name: {name}
description: {description_json}
---

# {title}

{overview}

## Use when

{use_when}

## Not for

{not_for}

## Preconditions

{preconditions}

## Workflow

{workflow}

## Writing rules

{writing_rules}

## Default shape

{default_shape}
"""


IMPLICIT_TEMPLATE = """---
name: {name}
description: {description_json}
---

# {title}

{body}
"""


def bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def numbered(items: list[str]) -> str:
    return "\n".join(f"{index}. {item}" for index, item in enumerate(items, start=1))


def title_from_name(name: str) -> str:
    return " ".join(part.capitalize() for part in name.split("-"))


CONTROLLED_CLUSTERS: list[dict[str, object]] = [
    {
        "family": "pdf_document_operations",
        "fixture_dir": "pdf_document_operations",
        "fixture": "sample_packet.pdf",
        "skills": [
            {
                "name": "pdf-question-answerer",
                "description": "Answers specific questions from PDF content while citing page or section evidence.",
                "overview": "Uses a PDF as an evidence source for question answering, not as a conversion or extraction task.",
                "use_when": ["The user asks a focused question about PDF content.", "The answer must be grounded in page, section, or quoted evidence."],
                "not_for": ["Extracting tables or fields as a reusable dataset.", "Converting the PDF into DOCX or Markdown.", "Filling a PDF form."],
                "preconditions": ["A readable PDF or extracted page text is available.", "The user asks a question whose answer should come from the PDF."],
                "workflow": ["Identify the question and relevant pages.", "Find supporting evidence in the PDF.", "Answer directly with citations or page anchors.", "Flag uncertainty if evidence is missing."],
                "writing_rules": ["Do not invent facts beyond the PDF.", "Keep citations attached to claims."],
                "default_shape": ["Answer", "Evidence with page or section anchors", "Uncertainty or missing evidence"],
                "prompt": "Please answer this from `/workspace/fixtures/pdf_document_operations/sample_packet.pdf`: what evidence does the policy give for reimbursing delayed travel meals? Cite the page or section evidence rather than converting the whole document.",
            },
            {
                "name": "pdf-layout-table-extractor",
                "description": "Extracts tables and repeated fields from PDFs while preserving page, row, column, and layout evidence.",
                "overview": "Turns layout-sensitive PDF content into structured data with traceable table coordinates.",
                "use_when": ["The user needs tabular values or repeated fields from a PDF.", "Row, column, page, or layout position matters to correctness."],
                "not_for": ["Answering a prose question from the PDF.", "Running OCR as the central task.", "Compressing or watermarking the PDF."],
                "preconditions": ["A PDF with tables, forms, invoices, or repeated fields is available.", "The requested fields or table boundaries are known."],
                "workflow": ["Inspect page layout and table boundaries.", "Extract rows, columns, labels, and values.", "Preserve page anchors and uncertain cells.", "Return structured data with verification notes."],
                "writing_rules": ["Do not flatten row relationships into prose.", "Mark merged cells or ambiguous labels."],
                "default_shape": ["Table or field set", "Page/row/column anchors", "Uncertain cells", "Validation notes"],
                "prompt": "From `/workspace/fixtures/pdf_document_operations/vendor_statement.pdf`, extract the invoice table into structured rows with invoice id, date, subtotal, tax, total, and page/row anchors. Do not answer it as a general PDF question.",
            },
            {
                "name": "pdf-ocr-cleaner",
                "description": "Recovers text from scanned or image-based PDFs and marks OCR uncertainty, unreadable regions, and page anchors.",
                "overview": "Handles scanned PDF text recovery where confidence and manual verification matter.",
                "use_when": ["The PDF is scanned, image-based, or not selectable.", "The user needs recovered text with uncertainty rather than a polished summary."],
                "not_for": ["Extracting clean born-digital tables.", "Filling form fields.", "Reviewing redaction risk."],
                "preconditions": ["A scanned PDF or page image exists.", "OCR uncertainty should be preserved."],
                "workflow": ["Identify scanned pages.", "Recover text page by page.", "Mark low-confidence spans.", "Preserve page anchors and manual-check regions."],
                "writing_rules": ["Do not silently correct uncertain OCR.", "Keep doubtful tokens visible."],
                "default_shape": ["Page", "Recovered text", "Confidence or uncertainty", "Manual check needed"],
                "prompt": "The file `/workspace/fixtures/pdf_document_operations/scanned_receipts.pdf` is mostly images. Recover the text page by page and mark uncertain OCR regions; do not treat it as a normal digital table extraction.",
            },
            {
                "name": "pdf-form-filler",
                "description": "Fills existing PDF form fields from supplied values and checks missing required fields or validation constraints.",
                "overview": "Writes values into a PDF form rather than extracting or summarising its content.",
                "use_when": ["The user has a fillable form and values to enter.", "The output should be a completed form or a field-completion checklist."],
                "not_for": ["Extracting fields from an invoice.", "Answering questions from a PDF.", "Converting a PDF to DOCX."],
                "preconditions": ["A form PDF and source values are available.", "Required fields and validation rules are known or discoverable."],
                "workflow": ["Map supplied values to form fields.", "Check required fields and allowed formats.", "Fill or prepare field-value instructions.", "Report missing values and validation risks."],
                "writing_rules": ["Do not invent missing form values.", "Separate filled values from missing required fields."],
                "default_shape": ["Field", "Value", "Status", "Missing or validation issue"],
                "prompt": "Use `/workspace/fixtures/pdf_document_operations/reimbursement_form.pdf` and the supplied employee details to prepare a field-entry checklist for the reimbursement packet. Identify required blanks that still need values; do not summarize the packet.",
            },
            {
                "name": "pdf-redaction-reviewer",
                "description": "Reviews PDF content for sensitive information and prepares a redaction plan with evidence and risk categories.",
                "overview": "Finds what should be hidden before sharing a PDF externally.",
                "use_when": ["The user wants to share a PDF but avoid exposing sensitive data.", "The output should list redaction targets and reasons."],
                "not_for": ["Extracting all document fields.", "Filling a PDF form.", "Compressing the PDF file."],
                "preconditions": ["A PDF or text extraction is available.", "The sharing context or sensitivity categories are known."],
                "workflow": ["Identify sensitive names, IDs, addresses, financial data, or confidential clauses.", "Classify redaction risk.", "Anchor each target to page or section evidence.", "Return a redaction checklist."],
                "writing_rules": ["Do not replace redaction review with generic privacy advice.", "Keep redaction targets specific."],
                "default_shape": ["Page or section", "Sensitive item", "Risk category", "Redaction recommendation"],
                "prompt": "Before we send `/workspace/fixtures/pdf_document_operations/client_contract.pdf` to an external vendor, identify page-specific redaction targets such as IDs, addresses, pricing, and confidential clauses.",
            },
            {
                "name": "pdf-to-docx-converter",
                "description": "Converts a PDF into an editable DOCX-style document while preserving headings, paragraphs, tables, and basic reading order.",
                "overview": "Creates an editable Word-style artifact from PDF content.",
                "use_when": ["The user wants a PDF converted into an editable Word document.", "Headings, paragraphs, and tables should remain usable after conversion."],
                "not_for": ["Answering questions from the PDF.", "Filling a form PDF.", "Finding redaction targets."],
                "preconditions": ["A PDF exists and the desired output is DOCX or Word-compatible structure.", "Some layout simplification is acceptable."],
                "workflow": ["Identify headings, paragraphs, tables, and page order.", "Convert content into DOCX-compatible structure.", "Preserve tables and labels where possible.", "Flag elements that may require manual repair."],
                "writing_rules": ["Do not summarize away source content.", "Keep editable structure more important than visual perfection."],
                "default_shape": ["Converted DOCX structure", "Preserved elements", "Repair notes"],
                "prompt": "Convert `/workspace/fixtures/pdf_document_operations/training_manual.pdf` into an editable DOCX-style structure with headings and tables preserved. Do not just answer questions from it.",
            },
        ],
    },
    {
        "family": "huggingface_ml_workflows",
        "fixture_dir": "huggingface_ml_workflows",
        "fixture": "model_requirements.md",
        "skills": [
            {
                "name": "hf-dataset-viewer-inspector",
                "description": "Inspects Hugging Face dataset metadata, splits, subsets, row examples, and schema risks.",
                "overview": "Uses dataset viewer information to understand a dataset before modelling.",
                "use_when": ["The user provides a dataset id or dataset task.", "They need splits, columns, examples, or schema constraints."],
                "not_for": ["Choosing a local model for hardware.", "Training sentence transformers.", "Building a Gradio demo."],
                "preconditions": ["A dataset id, dataset card, or expected dataset schema exists.", "The goal is dataset inspection rather than model deployment."],
                "workflow": ["Fetch or inspect dataset metadata.", "Check subsets, splits, columns, and row examples.", "Identify licensing or schema caveats.", "Return a dataset readiness summary."],
                "writing_rules": ["Do not recommend models before checking dataset shape.", "Separate metadata facts from assumptions."],
                "default_shape": ["Dataset overview", "Splits/subsets", "Columns/examples", "Risks"],
                "prompt": "For the dataset described in `/workspace/fixtures/huggingface_ml_workflows/customer_tickets_dataset.md`, inspect expected subsets, splits, columns, and row examples before we choose any model.",
            },
            {
                "name": "hf-local-model-selector",
                "description": "Selects Hugging Face or GGUF models for local hardware based on memory, quantization, task, latency, and quality tradeoffs.",
                "overview": "Chooses a model that can actually run on the user's local machine.",
                "use_when": ["The user gives hardware constraints or local inference requirements.", "The decision depends on memory, quantization, model family, or latency."],
                "not_for": ["Inspecting dataset rows.", "Fine-tuning an embedding model.", "Publishing a paper page."],
                "preconditions": ["Hardware budget and task type are known.", "The user wants model selection rather than training."],
                "workflow": ["Identify task and local hardware limits.", "Compare model sizes, quantization, runtime, and quality.", "Recommend candidates and fallback options.", "Give install or verification checks."],
                "writing_rules": ["Do not choose a model larger than the stated memory budget.", "State quality/speed tradeoffs."],
                "default_shape": ["Recommended model", "Why it fits hardware", "Tradeoffs", "Setup check"],
                "prompt": "I need a local model for classifying support tickets on an 8 GB Mac. Choose realistic Hugging Face/GGUF candidates and quantization options; do not design a dataset audit.",
            },
            {
                "name": "sentence-transformer-finetuner",
                "description": "Plans sentence-transformer fine-tuning for retrieval or similarity with training pairs, losses, evaluation splits, and embedding checks.",
                "overview": "Improves an embedding model for a specific retrieval task.",
                "use_when": ["The user has positive/negative pairs, triplets, or retrieval labels.", "The output should be a fine-tuning/evaluation plan for embeddings."],
                "not_for": ["Selecting an off-the-shelf local LLM.", "Building a Gradio interface.", "Inspecting only dataset columns."],
                "preconditions": ["Training examples or labels are available.", "The target metric is retrieval or semantic similarity."],
                "workflow": ["Identify labels and retrieval objective.", "Choose base model, loss, negatives, and split strategy.", "Define evaluation metrics.", "Return training config and risks."],
                "writing_rules": ["Do not promise improved retrieval without eval design.", "Keep leakage and hard negatives explicit."],
                "default_shape": ["Training data", "Model/loss", "Evaluation", "Risks"],
                "prompt": "We have labelled skill-query pairs and hard negatives for agent skill routing. Plan a sentence-transformer fine-tuning setup with losses, splits, and retrieval metrics.",
            },
            {
                "name": "gradio-demo-builder",
                "description": "Builds a Gradio demo interface around a model, dataset, or inference pipeline with inputs, outputs, examples, and launch constraints.",
                "overview": "Creates an interactive demo rather than training or evaluating a model.",
                "use_when": ["The user wants a web demo for a model or pipeline.", "Inputs, outputs, examples, and UI behavior matter."],
                "not_for": ["Choosing a model for local hardware.", "Running benchmark evaluation.", "Publishing a research paper page."],
                "preconditions": ["A model/pipeline or callable function exists.", "The desired demo inputs and outputs are known."],
                "workflow": ["Identify model inputs and outputs.", "Design Gradio components and examples.", "Add validation and error display.", "Return app scaffold and launch instructions."],
                "writing_rules": ["Do not turn a demo request into a training plan.", "Keep UI components aligned with model I/O."],
                "default_shape": ["Components", "Examples", "App scaffold", "Launch checks"],
                "prompt": "Create a small Python web UI plan for a ticket classifier with a text box, confidence display, sample inputs, and launch checks. We already have the model; do not discuss fine-tuning.",
            },
            {
                "name": "hf-zerogpu-space-deployer",
                "description": "Prepares Hugging Face Spaces ZeroGPU deployments with runtime constraints, sleep behavior, dependency files, and queue expectations.",
                "overview": "Handles deployment constraints for ZeroGPU Spaces.",
                "use_when": ["The user wants to deploy a demo to Hugging Face Spaces ZeroGPU.", "GPU availability, requirements files, and queueing behavior matter."],
                "not_for": ["Building the demo UI itself.", "Selecting a local GGUF model.", "Running community evaluations."],
                "preconditions": ["A Space/app exists or is planned.", "ZeroGPU constraints and dependencies are relevant."],
                "workflow": ["Check app runtime and GPU calls.", "Prepare dependency and Space configuration.", "Plan queueing/sleep behavior.", "Return deployment checklist and verification steps."],
                "writing_rules": ["Do not assume always-on GPU.", "Flag packages that may not fit the runtime."],
                "default_shape": ["Space setup", "Dependencies", "ZeroGPU constraints", "Verification"],
                "prompt": "Prepare our Gradio classifier for Hugging Face ZeroGPU Spaces. Focus on dependency files, GPU queue behavior, sleep constraints, and deployment verification.",
            },
            {
                "name": "hf-community-eval-runner",
                "description": "Runs or plans Hugging Face model evaluations using benchmark tasks, metrics, hardware assumptions, and reproducible result reporting.",
                "overview": "Evaluates model quality instead of building a demo or selecting local hardware.",
                "use_when": ["The user wants to compare models with a benchmark or eval suite.", "Metrics, reproducibility, and result artifacts matter."],
                "not_for": ["Inspecting dataset rows.", "Deploying to ZeroGPU.", "Building a UI demo."],
                "preconditions": ["Candidate models and evaluation task are known.", "Metrics and dataset split are specified or can be chosen."],
                "workflow": ["Identify models, tasks, metrics, and hardware.", "Prepare evaluation commands or scripts.", "Run or describe reproducible evaluation.", "Report scores and caveats."],
                "writing_rules": ["Do not infer model quality from popularity alone.", "Keep benchmark limitations explicit."],
                "default_shape": ["Models", "Eval setup", "Metrics/results", "Caveats"],
                "prompt": "Compare two Hugging Face classifiers on a held-out ticket dataset using reproducible metrics. I need an evaluation plan and result table, not a Gradio app.",
            },
        ],
    },
    {
        "family": "github_ci_maintenance",
        "fixture_dir": "github_ci_maintenance",
        "fixture": "ci_log.txt",
        "skills": [
            {
                "name": "ci-log-root-cause-debugger",
                "description": "Diagnoses CI failures from logs, failing commands, environment assumptions, and dependency or test errors.",
                "overview": "Finds the first meaningful CI failure and a minimal verification path.",
                "use_when": ["The user provides CI logs or failing check output.", "The output should identify root cause and fix sequence."],
                "not_for": ["Reviewing code quality generally.", "Writing release notes.", "Triage of user issues without CI evidence."],
                "preconditions": ["CI logs, job name, or failing command are available.", "The user wants diagnosis rather than broad repository maintenance."],
                "workflow": ["Find the first meaningful error.", "Map it to test, dependency, environment, or build cause.", "Propose smallest fix.", "Give rerun checks."],
                "writing_rules": ["Do not chase cascading errors first.", "Quote log evidence."],
                "default_shape": ["Failing job", "Root cause", "Evidence", "Fix and rerun"],
                "prompt": "Inspect `/workspace/fixtures/github_ci_maintenance/ci_log.txt` and identify the CI root cause, the first meaningful error, and the smallest rerun sequence.",
            },
            {
                "name": "pr-review-comment-resolver",
                "description": "Turns pull request review comments into specific code changes, reply points, and verification steps.",
                "overview": "Acts on reviewer feedback rather than conducting a fresh review.",
                "use_when": ["The user provides PR review comments.", "The task is to resolve requested changes and prepare replies."],
                "not_for": ["Finding CI root cause.", "Writing changelog entries.", "Installing git safety hooks."],
                "preconditions": ["Review comments and relevant code context are available.", "The user wants implementation or response planning."],
                "workflow": ["Group comments by required change.", "Map each comment to file/code action.", "Identify disagreements or questions.", "Return patch plan and response summary."],
                "writing_rules": ["Do not ignore unresolved reviewer requests.", "Separate actioned comments from clarification needed."],
                "default_shape": ["Comment", "Required action", "Verification", "Reply"],
                "prompt": "Use `/workspace/fixtures/github_ci_maintenance/pr_review_comments.md` to plan how to resolve the review comments and what response to leave. Do not perform a general code review.",
            },
            {
                "name": "repo-code-reviewer",
                "description": "Reviews a repository diff for bugs, regressions, maintainability risks, missing tests, and behavioral concerns.",
                "overview": "Performs fresh code review on a change.",
                "use_when": ["The user provides a diff, branch, or changed files.", "They want findings ordered by severity."],
                "not_for": ["Resolving existing review comments.", "Debugging CI logs only.", "Generating release notes."],
                "preconditions": ["A diff or changed files are available.", "The user expects review findings, not implementation."],
                "workflow": ["Inspect changed behavior.", "Identify bugs and missing tests.", "Prioritize findings by severity.", "Return concise review comments."],
                "writing_rules": ["Lead with findings.", "Avoid style-only comments unless they hide risk."],
                "default_shape": ["Finding", "File/evidence", "Risk", "Suggested test/fix"],
                "prompt": "Review the diff described in `/workspace/fixtures/github_ci_maintenance/payment_diff.patch` for bugs and missing tests. This is a fresh code review, not a CI log diagnosis.",
            },
            {
                "name": "github-issue-triager",
                "description": "Classifies GitHub issues by type, severity, reproducibility, ownership, labels, and missing information.",
                "overview": "Sorts issue reports into actionable categories.",
                "use_when": ["The user provides issue text or an issue queue.", "They need labels, priority, owner, or reproduction requests."],
                "not_for": ["Addressing PR comments.", "Reviewing a code diff.", "Writing changelog notes."],
                "preconditions": ["Issue titles/bodies are available.", "Project labels or triage criteria are known or can be proposed."],
                "workflow": ["Read issue symptoms and environment.", "Assign type/severity/owner labels.", "Identify missing reproduction details.", "Return triage actions."],
                "writing_rules": ["Do not assume root cause from vague symptoms.", "Ask for minimal reproduction when needed."],
                "default_shape": ["Issue", "Labels", "Priority", "Missing info/action"],
                "prompt": "Triage the issues in `/workspace/fixtures/github_ci_maintenance/issues.md` into bug/feature/support labels, priority, owner guess, and missing reproduction details.",
            },
            {
                "name": "release-changelog-generator",
                "description": "Generates release notes or changelog entries from commits, pull requests, categories, and breaking-change markers.",
                "overview": "Summarizes shipped changes for users or developers.",
                "use_when": ["The user provides commits, PR titles, or version changes.", "The output should be a changelog or release note."],
                "not_for": ["Debugging CI.", "Triage of issues.", "Reviewing code for defects."],
                "preconditions": ["Commit/PR list and target audience are available.", "Release categories are known or inferable."],
                "workflow": ["Group changes by category.", "Identify breaking changes and migrations.", "Write concise notes.", "List verification or upgrade caveats."],
                "writing_rules": ["Do not include internal noise unless relevant.", "Mark breaking changes clearly."],
                "default_shape": ["Highlights", "Fixes", "Breaking changes", "Upgrade notes"],
                "prompt": "Turn `/workspace/fixtures/github_ci_maintenance/merged_prs.md` into release notes grouped by features, fixes, and breaking changes. Do not review the code.",
            },
            {
                "name": "git-safety-guardrail-installer",
                "description": "Configures repository hooks or guardrails that prevent dangerous git operations, secret commits, or unsafe workflow commands.",
                "overview": "Adds workflow safety controls to a repository.",
                "use_when": ["The user wants hooks or safeguards against risky git commands.", "The output is a guardrail setup plan or config."],
                "not_for": ["Writing changelogs.", "Reviewing code.", "Triaging issues."],
                "preconditions": ["Repository tooling and desired blocked operations are known.", "The user accepts local workflow configuration changes."],
                "workflow": ["Identify risky operations and repo tooling.", "Choose hook/guardrail mechanism.", "Define blocked commands or secret checks.", "Return setup and verification commands."],
                "writing_rules": ["Do not install destructive guardrails without explaining impact.", "Keep bypass procedure explicit."],
                "default_shape": ["Guardrail", "Config/action", "Verification", "Bypass or maintenance note"],
                "prompt": "Design repository guardrails to block accidental `git push`, `reset --hard`, and secret commits. I need hook/config steps and verification, not issue triage.",
            },
        ],
    },
    {
        "family": "api_mcp_tooling",
        "fixture_dir": "api_mcp_tooling",
        "fixture": "integration_notes.md",
        "skills": [
            {
                "name": "rest-api-contract-designer",
                "description": "Designs REST API resources, endpoints, request/response schemas, status codes, pagination, and error behavior.",
                "overview": "Creates a new API contract rather than reviewing an existing one.",
                "use_when": ["The user needs a new REST API design.", "Resources, schemas, status codes, and errors must be specified."],
                "not_for": ["Building an MCP server.", "Writing developer documentation from an existing API.", "Planning webhook delivery."],
                "preconditions": ["Domain objects and client needs are known.", "The API does not already have a final contract."],
                "workflow": ["Identify resources and operations.", "Define schemas and status codes.", "Specify pagination/filtering/errors.", "Return contract outline and examples."],
                "writing_rules": ["Do not skip error models.", "Separate API design from implementation details."],
                "default_shape": ["Resources", "Endpoints", "Schemas", "Errors/examples"],
                "prompt": "Specify a new client-facing HTTP interface for subscription invoices, including resources, endpoints, request and response shapes, status codes, pagination, and error examples. This is not an MCP wrapper.",
            },
            {
                "name": "mcp-server-builder",
                "description": "Builds MCP server tools or resources with schemas, transport assumptions, capability boundaries, and client usage examples.",
                "overview": "Wraps capabilities for model clients through MCP.",
                "use_when": ["The user wants an MCP server or tool/resource definitions.", "Tool schemas, resources, and client invocation matter."],
                "not_for": ["Designing a REST API for external clients.", "Planning webhook retries.", "Writing generic auth docs."],
                "preconditions": ["The local/service capabilities to expose are known.", "MCP client and transport assumptions are relevant."],
                "workflow": ["Identify tools/resources to expose.", "Define input/output schemas.", "Specify transport and auth assumptions.", "Return server structure and usage examples."],
                "writing_rules": ["Do not expose overly broad filesystem or network access.", "Keep tool boundaries narrow."],
                "default_shape": ["Tools/resources", "Schemas", "Server structure", "Client examples"],
                "prompt": "Create an MCP server design that exposes two local file-inspection tools with narrow schemas and resource boundaries. Do not design a public REST API.",
            },
            {
                "name": "webhook-integration-planner",
                "description": "Plans webhook event subscriptions, signature verification, idempotency keys, retries, ordering, and dead-letter handling.",
                "overview": "Designs event callback behavior between systems.",
                "use_when": ["The user receives or sends event callbacks.", "Retries, signatures, ordering, or idempotency are central."],
                "not_for": ["Designing REST CRUD endpoints.", "Building an MCP server.", "Documenting an existing API only."],
                "preconditions": ["Event source and event types are known.", "Receiver behavior and failure handling matter."],
                "workflow": ["Select events and payloads.", "Define signature/idempotency validation.", "Plan retries and ordering.", "Return receiver contract and tests."],
                "writing_rules": ["Do not ignore duplicate deliveries.", "State failure storage behavior."],
                "default_shape": ["Events", "Validation", "Retry/idempotency", "Tests"],
                "prompt": "Plan webhook handling for payment events: accepted event types, signature checks, idempotency, retry behavior, ordering, and dead-letter storage.",
            },
            {
                "name": "auth-flow-integrator",
                "description": "Integrates OAuth, API keys, sessions, token refresh, scopes, secret storage, and authorization checks into an application flow.",
                "overview": "Focuses on authentication and authorization mechanics.",
                "use_when": ["The user asks about OAuth, API keys, sessions, scopes, or token refresh.", "Secrets and permission boundaries matter."],
                "not_for": ["Planning generic webhook retries.", "Writing API documentation.", "Building MCP tools."],
                "preconditions": ["Provider/auth method and app flow are known.", "Security and token handling are relevant."],
                "workflow": ["Map auth actors and token lifecycle.", "Define scopes, storage, refresh, and revocation.", "Identify authorization checks.", "Return integration and test plan."],
                "writing_rules": ["Do not put secrets in client-side storage.", "Separate authentication from authorization."],
                "default_shape": ["Auth flow", "Token/scopes", "Storage/security", "Tests"],
                "prompt": "Integrate OAuth login for a dashboard app, covering scopes, token refresh, secret storage, logout, and authorization checks. Do not turn it into webhook planning.",
            },
            {
                "name": "api-documentation-writer",
                "description": "Writes developer-facing API documentation from an existing contract, including quickstarts, examples, auth notes, and error explanations.",
                "overview": "Produces docs for an already-designed API.",
                "use_when": ["The API contract exists and the user needs developer docs.", "Examples, quickstarts, and error explanations matter."],
                "not_for": ["Designing the API from scratch.", "Building an MCP server.", "Auditing security architecture."],
                "preconditions": ["Endpoints, schemas, and auth behavior are already known.", "Target developer audience is identified."],
                "workflow": ["Read existing contract.", "Create quickstart and endpoint docs.", "Add examples and errors.", "Return docs with missing-contract questions."],
                "writing_rules": ["Do not invent undocumented endpoint behavior.", "Keep examples consistent with schema."],
                "default_shape": ["Quickstart", "Endpoint docs", "Examples", "Errors/questions"],
                "prompt": "Write developer docs for the existing billing API contract in `/workspace/fixtures/api_mcp_tooling/billing_contract.yaml`, including quickstart, examples, auth notes, and errors.",
            },
            {
                "name": "api-security-threat-reviewer",
                "description": "Reviews API designs for authentication, authorization, input validation, rate limiting, data exposure, and abuse cases.",
                "overview": "Threat-models an API rather than documenting or designing it.",
                "use_when": ["The user asks about API security risks.", "Authz, validation, rate limits, abuse, or sensitive data exposure are central."],
                "not_for": ["Writing developer docs.", "Building MCP tools.", "Creating a normal REST contract without security focus."],
                "preconditions": ["API endpoints, data classes, or architecture are known.", "Security review is the requested outcome."],
                "workflow": ["Identify assets, actors, and trust boundaries.", "Check authn/authz and validation risks.", "Assess abuse/rate-limit/data-exposure issues.", "Return prioritized mitigations."],
                "writing_rules": ["Do not provide only generic security advice.", "Tie each risk to endpoint or data exposure."],
                "default_shape": ["Risk", "Affected endpoint/data", "Impact", "Mitigation"],
                "prompt": "Threat-review the billing API for authorization gaps, sensitive data exposure, rate-limit abuse, and validation risks. I need security findings, not user-facing docs.",
            },
        ],
    },
    {
        "family": "observability_reliability",
        "fixture_dir": "observability_reliability",
        "fixture": "trace.json",
        "skills": [
            {
                "name": "prometheus-alert-rule-writer",
                "description": "Writes Prometheus alert rules from SLOs, metric names, thresholds, windows, labels, and severity policies.",
                "overview": "Produces alerting rules rather than dashboards or incident summaries.",
                "use_when": ["The user has SLOs or metric thresholds.", "They need alert expressions, labels, and routing severity."],
                "not_for": ["Building Grafana dashboards.", "Diagnosing traces.", "Writing an incident narrative."],
                "preconditions": ["Metric names and SLO thresholds are known.", "Alert windows and severity rules are available or can be proposed."],
                "workflow": ["Map SLO to metric expression.", "Choose burn-rate/window strategy.", "Write alert rule and labels.", "Add verification query."],
                "writing_rules": ["Do not invent metric names without marking assumptions.", "Avoid noisy alerts without window logic."],
                "default_shape": ["Alert rule", "Labels/severity", "Verification", "Noise risk"],
                "prompt": "Produce PromQL alerting expressions for checkout latency and error-budget burn using `/workspace/fixtures/observability_reliability/metrics.md`. Include windows, labels, severity, and verification queries; do not build a dashboard.",
            },
            {
                "name": "grafana-dashboard-builder",
                "description": "Builds Grafana dashboard structure with panels, variables, queries, thresholds, and operator-facing layout.",
                "overview": "Creates observability dashboards for scanning service health.",
                "use_when": ["The user wants a dashboard or panel layout.", "Queries, variables, thresholds, and visual grouping matter."],
                "not_for": ["Writing alert rules only.", "Diagnosing one trace.", "Writing post-incident narrative."],
                "preconditions": ["Metrics and dashboard audience are known.", "Panel grouping or service scope is specified."],
                "workflow": ["Identify dashboard purpose and variables.", "Design panels and queries.", "Set thresholds and legends.", "Return dashboard plan or JSON outline."],
                "writing_rules": ["Do not overload dashboards with every metric.", "Prioritize operator scanability."],
                "default_shape": ["Dashboard sections", "Panels/queries", "Thresholds", "Notes"],
                "prompt": "Design a Grafana dashboard for checkout service health with panels, variables, queries, thresholds, and operator layout. This is not an alert-rule task.",
            },
            {
                "name": "distributed-trace-investigator",
                "description": "Investigates distributed traces to locate latency, retries, failing spans, dependency calls, and propagation gaps.",
                "overview": "Uses trace spans to explain a request path problem.",
                "use_when": ["The user provides trace spans or tracing output.", "The task is to locate latency or failure across services."],
                "not_for": ["Building dashboards.", "Writing alerts.", "Reviewing resilience code without trace evidence."],
                "preconditions": ["Trace spans or service timing data are available.", "The target request or symptom is known."],
                "workflow": ["Read trace hierarchy and critical path.", "Identify slow or failing spans.", "Connect spans to dependencies.", "Return diagnosis and missing instrumentation."],
                "writing_rules": ["Do not infer causality from one span without caveat.", "Keep timing evidence visible."],
                "default_shape": ["Trace path", "Bottleneck/failure", "Evidence", "Next check"],
                "prompt": "Use `/workspace/fixtures/observability_reliability/checkout_trace.json` to find where checkout latency is introduced across services. I need trace-based diagnosis, not a dashboard.",
            },
            {
                "name": "slo-breach-narrative-writer",
                "description": "Writes SLO breach summaries with timeline, user impact, error budget effect, mitigation, and follow-up actions.",
                "overview": "Turns incident/SLO data into stakeholder-readable narrative.",
                "use_when": ["The user has incident notes or SLO breach data.", "They need a timeline, impact, mitigation, and follow-ups."],
                "not_for": ["Writing alert rules.", "Building dashboards.", "Deep trace debugging."],
                "preconditions": ["Timeline, metrics, or incident notes are available.", "Audience and reporting level are known."],
                "workflow": ["Extract timeline and impact.", "Connect metrics to SLO breach.", "Summarize mitigation and current status.", "List follow-up actions."],
                "writing_rules": ["Do not overclaim root cause if not established.", "Keep user impact explicit."],
                "default_shape": ["Summary", "Timeline", "Impact", "Mitigation/follow-up"],
                "prompt": "Using `/workspace/fixtures/observability_reliability/incident_notes.md`, write an SLO breach narrative with timeline, user impact, mitigation, and follow-up actions.",
            },
            {
                "name": "resilience-pattern-reviewer",
                "description": "Reviews service code or configuration for retries, timeouts, circuit breakers, fallbacks, backoff, and failure containment.",
                "overview": "Checks whether service behavior handles failures safely.",
                "use_when": ["The user asks about resilience patterns in code or config.", "Retries, timeouts, fallback, or circuit breakers are relevant."],
                "not_for": ["Investigating trace output.", "Writing SLO narratives.", "Building dashboards."],
                "preconditions": ["Code/config or architecture notes are available.", "Failure containment is the review objective."],
                "workflow": ["Identify external calls and failure modes.", "Check timeouts/retries/backoff/fallbacks.", "Assess cascading-failure risk.", "Return prioritized fixes and tests."],
                "writing_rules": ["Do not recommend infinite retries.", "Tie patterns to concrete failure modes."],
                "default_shape": ["Call/failure mode", "Current risk", "Recommended pattern", "Test"],
                "prompt": "Review `/workspace/fixtures/observability_reliability/payment_client.py` for retry, timeout, backoff, fallback, and cascading-failure risks.",
            },
            {
                "name": "service-mesh-traffic-debugger",
                "description": "Debugs service mesh traffic routing, mTLS, retries, traffic splits, destination rules, and sidecar configuration.",
                "overview": "Handles mesh-specific operational failures.",
                "use_when": ["The user provides service mesh manifests or routing symptoms.", "Traffic splits, mTLS, sidecars, retries, or destination rules matter."],
                "not_for": ["Writing Prometheus alerts.", "Reviewing app-level retries only.", "Writing incident narrative."],
                "preconditions": ["Mesh config or symptoms are available.", "The environment uses a service mesh."],
                "workflow": ["Inspect virtual services, destination rules, policies, and sidecars.", "Check traffic routing and mTLS assumptions.", "Identify retry/split conflicts.", "Return fix and verification checks."],
                "writing_rules": ["Do not treat mesh config as plain app code.", "State namespace and service assumptions."],
                "default_shape": ["Mesh object", "Traffic issue", "Evidence", "Fix/verification"],
                "prompt": "Debug the service-mesh routing notes in `/workspace/fixtures/observability_reliability/mesh_config.yaml`, focusing on traffic split, mTLS, retries, and destination rules.",
            },
        ],
    },
    {
        "family": "office_business_automation",
        "fixture_dir": "office_business_automation",
        "fixture": "workflow_notes.md",
        "skills": [
            {
                "name": "xlsx-formula-model-builder",
                "description": "Builds spreadsheet formula models from assumptions, inputs, outputs, formulas, sheet structure, and validation checks.",
                "overview": "Creates spreadsheet logic rather than auditing an existing file.",
                "use_when": ["The user wants a workbook model or formulas built.", "Inputs, assumptions, outputs, and validation formulas matter."],
                "not_for": ["Automating Airtable.", "Extracting meeting action items.", "Classifying emails."],
                "preconditions": ["Business assumptions and desired outputs are available.", "Spreadsheet formulas are the desired artifact."],
                "workflow": ["Map assumptions and outputs.", "Design sheets and formulas.", "Add checks and sensitivities.", "Return formula model outline."],
                "writing_rules": ["Do not hard-code assumptions without labelling them.", "Keep formulas auditable."],
                "default_shape": ["Sheets", "Inputs", "Formulas", "Checks"],
                "prompt": "Build a spreadsheet formula model for subscription revenue using `/workspace/fixtures/office_business_automation/revenue_assumptions.md`. I need formulas and validation checks, not Airtable automation.",
            },
            {
                "name": "airtable-workflow-automator",
                "description": "Designs Airtable bases, fields, views, automations, triggers, and integrations for operational workflows.",
                "overview": "Automates work inside Airtable rather than spreadsheets or Notion.",
                "use_when": ["The user has an Airtable workflow or wants a base automation.", "Fields, views, triggers, and integrations matter."],
                "not_for": ["Building Excel formulas.", "Creating Notion research databases.", "Scheduling meetings."],
                "preconditions": ["Airtable workspace/base context exists.", "Trigger and desired automation action are known."],
                "workflow": ["Map records, fields, and views.", "Define trigger conditions.", "Plan automation actions and integrations.", "Return setup checklist."],
                "writing_rules": ["Do not assume spreadsheet formulas transfer directly.", "Keep trigger conditions precise."],
                "default_shape": ["Base/fields", "Views", "Automation trigger", "Actions/tests"],
                "prompt": "Design an Airtable automation for inbound partner requests: fields, views, trigger conditions, Slack notification, and testing steps.",
            },
            {
                "name": "notion-research-database-builder",
                "description": "Creates Notion research databases with properties, relations, status fields, templates, and capture workflows.",
                "overview": "Organizes research notes into a Notion database.",
                "use_when": ["The user wants a Notion database for research tracking.", "Properties, relations, views, templates, and capture flow matter."],
                "not_for": ["Airtable operational automation.", "Spreadsheet formula modelling.", "Academic paper search itself."],
                "preconditions": ["Research entities and workflow needs are known.", "Notion database structure is the desired artifact."],
                "workflow": ["Identify research objects and statuses.", "Design properties, relations, and views.", "Create templates and capture workflow.", "Return database blueprint."],
                "writing_rules": ["Do not substitute a plain literature review.", "Keep properties useful for retrieval and filtering."],
                "default_shape": ["Database schema", "Views", "Templates", "Capture workflow"],
                "prompt": "Create a Notion research database structure for thesis papers with properties, relations, review status, tags, and capture templates.",
            },
            {
                "name": "calendar-scheduling-optimizer",
                "description": "Optimizes calendars by proposing meeting times, time blocks, constraints, buffers, and conflict-resolution options.",
                "overview": "Solves scheduling constraints rather than summarising meetings.",
                "use_when": ["The user gives availability, constraints, attendees, or calendar conflicts.", "The output should propose times or time blocks."],
                "not_for": ["Extracting action items from meeting notes.", "Automating Airtable.", "Classifying emails."],
                "preconditions": ["Availability and constraints are available.", "The goal is scheduling rather than note processing."],
                "workflow": ["Collect constraints and priorities.", "Find feasible slots.", "Add buffers and conflict notes.", "Return recommended schedule."],
                "writing_rules": ["Do not ignore time zones or hard constraints.", "State tradeoffs between options."],
                "default_shape": ["Recommended slot", "Constraints satisfied", "Tradeoffs", "Alternatives"],
                "prompt": "Use these availability notes to propose two meeting slots with buffers and conflict tradeoffs. This is scheduling, not meeting-note extraction.",
            },
            {
                "name": "meeting-notes-action-extractor",
                "description": "Extracts decisions, action items, owners, due dates, open questions, and follow-up risks from meeting notes or transcripts.",
                "overview": "Turns meeting content into accountable follow-up items.",
                "use_when": ["The user provides meeting notes or a transcript.", "They need actions, decisions, owners, due dates, and open questions."],
                "not_for": ["Scheduling the meeting.", "Classifying emails.", "Creating a Notion database from scratch."],
                "preconditions": ["Meeting notes or transcript text exists.", "Action ownership or follow-up extraction is the target."],
                "workflow": ["Identify decisions and commitments.", "Extract action items with owners and due dates.", "List open questions.", "Return follow-up risks."],
                "writing_rules": ["Do not invent owners or due dates.", "Mark missing ownership explicitly."],
                "default_shape": ["Decision", "Action/owner/due date", "Open question", "Risk"],
                "prompt": "From `/workspace/fixtures/office_business_automation/meeting_notes.md`, extract decisions, actions, owners, due dates, and open questions. Do not draft a calendar schedule.",
            },
            {
                "name": "email-classification-router",
                "description": "Classifies emails into categories, priority, routing destination, required action, and escalation risk.",
                "overview": "Routes incoming emails for workflow handling.",
                "use_when": ["The user provides email content or an inbox export.", "They need categories, priorities, routing, or escalation flags."],
                "not_for": ["Writing a polished email reply.", "Extracting meeting notes.", "Building an Airtable base."],
                "preconditions": ["Email text and category scheme are available or can be proposed.", "The goal is classification/routing rather than drafting."],
                "workflow": ["Read sender, subject, body, and attachments clues.", "Classify category and urgency.", "Choose routing/action.", "Flag escalation or missing info."],
                "writing_rules": ["Do not answer emails when asked only to classify.", "Keep categories consistent."],
                "default_shape": ["Email", "Category", "Priority", "Route/action"],
                "prompt": "Classify the emails in `/workspace/fixtures/office_business_automation/inbox_sample.md` by category, priority, routing destination, and escalation risk. Do not write replies.",
            },
        ],
    },
    {
        "family": "skill_representation_analysis",
        "fixture_dir": "skill_representation_analysis",
        "fixture": "skill_samples.md",
        "skills": [
            {
                "name": "skill-field-auditor",
                "description": "Extracts representation fields from existing skills, including triggers, inputs, outputs, workflow, constraints, dependencies, resources, and examples.",
                "overview": "Audits what information a skill artifact contains.",
                "use_when": ["The user provides existing skill files.", "The output should be a field audit or extraction table."],
                "not_for": ["Writing a new skill from scratch.", "Installing a public skill.", "Evaluating retrieval accuracy."],
                "preconditions": ["One or more skill artifacts are available.", "The target field taxonomy is known."],
                "workflow": ["Read each skill artifact.", "Extract explicit and implicit fields.", "Mark evidence and confidence.", "Return structured audit."],
                "writing_rules": ["Do not assume missing fields are present.", "Quote evidence where possible."],
                "default_shape": ["Skill", "Field", "Evidence", "Explicit/implicit/missing"],
                "prompt": "Audit `/workspace/fixtures/skill_representation_analysis/public_skill_sample.md` and extract triggers, inputs, outputs, workflow, dependencies, resources, examples, and missing fields.",
            },
            {
                "name": "skill-authoring-guide",
                "description": "Creates or revises an agent skill artifact with trigger conditions, procedural steps, resources, constraints, and examples.",
                "overview": "Writes a usable skill document.",
                "use_when": ["The user wants to create or revise a skill.", "The output is a skill artifact, not an evaluation report."],
                "not_for": ["Auditing existing skills only.", "Installing a skill package.", "Designing a router policy."],
                "preconditions": ["Skill purpose, target tasks, and constraints are known.", "A local skill format is available or can be assumed."],
                "workflow": ["Clarify skill scope.", "Write trigger and boundaries.", "Define workflow, resources, and examples.", "Return skill file draft."],
                "writing_rules": ["Keep skills atomic.", "Avoid broad hierarchical routing inside one skill."],
                "default_shape": ["Skill frontmatter", "Use conditions", "Workflow", "Resources/examples"],
                "prompt": "Draft a new atomic skill for reviewing database migrations, including triggers, boundaries, workflow, dependencies, and examples. Do not just audit an existing skill.",
            },
            {
                "name": "skill-router-policy-designer",
                "description": "Designs skill routing policies, candidate-generation stages, reranking rules, budgets, and fallback behavior.",
                "overview": "Specifies how a retriever or selector should choose skills.",
                "use_when": ["The user wants a retrieval or routing policy.", "Candidate budgets, stages, and fallback behavior matter."],
                "not_for": ["Writing a single skill file.", "Installing public skills.", "Evaluating a completed benchmark only."],
                "preconditions": ["Skill library structure and constraints are known.", "Selection policy is the requested artifact."],
                "workflow": ["Define candidate generation.", "Choose representation fields.", "Specify reranking and fallback.", "Return routing policy and metrics."],
                "writing_rules": ["Do not collapse retriever and main agent roles.", "Make candidate budget explicit."],
                "default_shape": ["Stages", "Representation fields", "Budgets", "Fallback/metrics"],
                "prompt": "Design a two-stage skill routing policy for a 2000-skill library, including candidate budget, representation fields, reranking, and fallback behavior.",
            },
            {
                "name": "skill-hierarchy-flattener",
                "description": "Converts broad or hierarchical skills into atomic child skills while preserving links, shared resources, and routing boundaries.",
                "overview": "Atomizes broad skills for evaluation or retrieval.",
                "use_when": ["A skill contains multiple subskills or internal routing.", "The output should be atomic skill definitions."],
                "not_for": ["Installing a skill unchanged.", "Evaluating retrieval results.", "Writing a new unrelated skill."],
                "preconditions": ["A broad skill or linked-skill set is available.", "Atomic evaluation or retrieval is the target."],
                "workflow": ["Identify subprocedures and shared resources.", "Split into atomic skills.", "Preserve cross-links and boundaries.", "Return child skill set."],
                "writing_rules": ["Do not hide domain routing inside one broad skill.", "Keep shared resources referenced explicitly."],
                "default_shape": ["Parent scope", "Child skills", "Shared resources", "Routing boundaries"],
                "prompt": "Decompose the broad all-in-one skill in `/workspace/fixtures/skill_representation_analysis/hierarchical_skill.md` into atomic standalone skill definitions while preserving cross-references, common resources, and routing boundaries.",
            },
            {
                "name": "skill-installer-wrapper",
                "description": "Installs public skills into a local skill directory, preserving source metadata, files, resources, and compatibility checks.",
                "overview": "Moves a public skill into the local library.",
                "use_when": ["The user provides a public skill source or repository.", "The output is an installed skill with import metadata and compatibility notes."],
                "not_for": ["Auditing fields without installing.", "Designing router policy.", "Evaluating benchmark accuracy."],
                "preconditions": ["Source URL/path and target skill directory are known.", "Licensing/tool assumptions or compatibility need checking."],
                "workflow": ["Inspect source layout.", "Copy skill files and resources.", "Record source metadata.", "Check compatibility and missing dependencies."],
                "writing_rules": ["Do not silently drop resources.", "Keep source provenance."],
                "default_shape": ["Installed path", "Copied files", "Source metadata", "Compatibility notes"],
                "prompt": "Install the public skill from `/workspace/fixtures/skill_representation_analysis/public_skill_repo/` into the local library, preserving resources and source metadata.",
            },
            {
                "name": "skill-benchmark-evaluator",
                "description": "Evaluates skill retrieval benchmarks using gold labels, acceptable alternatives, top-k metrics, MRR, false positives, and failure modes.",
                "overview": "Assesses benchmark results rather than authoring or installing skills.",
                "use_when": ["The user has retrieval outputs or benchmark prompts.", "The output should be metrics and failure analysis."],
                "not_for": ["Creating a skill file.", "Installing public skills.", "Flattening hierarchy."],
                "preconditions": ["Prompt/gold labels and retrieval rankings are available.", "Metrics and acceptable-alternative policy are known."],
                "workflow": ["Load rankings and gold labels.", "Compute top-k, MRR, and false positives.", "Inspect failure modes.", "Return evaluation summary."],
                "writing_rules": ["Do not tune benchmark after seeing results without logging it.", "Separate strict and acceptable accuracy."],
                "default_shape": ["Metrics", "Failure modes", "Risk/caveats", "Next validation"],
                "prompt": "Evaluate `/workspace/fixtures/skill_representation_analysis/retrieval_results.json` with top-1, top-5, MRR, non-core false positives, and failure-mode categories.",
            },
        ],
    },
]


IMPLICIT_STRESS_SKILLS: list[dict[str, object]] = [
    {
        "name": "implicit-pdf-evidence-answerer",
        "description": "Works with PDF packets when the user needs a direct answer grounded in page evidence rather than conversion or extraction.",
        "body": "This routine is for the moment when a PDF is acting as the source of truth. The operator reads the question first, hunts for the relevant pages, and then gives a direct answer with page anchors. If the request starts drifting toward tables, OCR cleanup, or form entry, this is the wrong routine. A typical response contains the answer, a short evidence trail, and any uncertainty where the PDF does not support the claim.",
    },
    {
        "name": "implicit-pdf-table-reconstructor",
        "description": "Works with PDF packets where row, column, label, and page relationships must be reconstructed as structured data.",
        "body": "This routine begins by treating the PDF as a spatial object. It looks for tables, repeated labels, invoice-like fields, and relationships between rows and columns. The deliverable is not prose. It is a structured extraction with page and row anchors, plus notes for merged cells or uncertain labels. It is a poor fit when the user only asks a question or wants a Word conversion.",
    },
    {
        "name": "implicit-browser-flow-investigator",
        "description": "Investigates a web interaction by reproducing clicks, state transitions, console output, network calls, and screenshots.",
        "body": "Use this routine when the story is an interaction that breaks. The path normally starts with opening the target page, reproducing the user's clicks, collecting console and network evidence, and deciding whether the failure is selector, timing, state, data, or app logic. The output is a reproduction trace and fix hypothesis, not a visual design review.",
    },
    {
        "name": "implicit-visual-diff-reviewer",
        "description": "Compares expected and current visual states across screenshots and viewports to classify layout regressions.",
        "body": "This routine assumes there is an expected visual state and a current visual state. It compares spacing, clipping, text overflow, contrast changes, responsive layout, and image placement. It ignores backend guesses unless the screenshots support them. The useful artifact is a viewport-specific list of visual differences and severity.",
    },
    {
        "name": "implicit-ci-failure-reader",
        "description": "Reads CI output to identify the first meaningful failure, likely root cause, and rerun or fix sequence.",
        "body": "The routine starts in the logs, not the source diff. It looks for the first non-cascading error, then connects that error to tests, dependencies, environment variables, build commands, or platform assumptions. The answer should quote log evidence and propose the smallest rerun sequence. Release-note writing and normal code review belong elsewhere.",
    },
    {
        "name": "implicit-review-comment-planner",
        "description": "Turns existing review comments into an action plan and response map.",
        "body": "This routine is for already-written reviewer feedback. It groups comments, identifies required code changes, marks questions or disagreements, and prepares a response for each thread. It is not a fresh code review because the starting object is the comment set rather than the diff itself.",
    },
    {
        "name": "implicit-hf-dataset-inspector",
        "description": "Inspects dataset cards, splits, subsets, columns, examples, and schema caveats before modelling decisions.",
        "body": "This routine works before training or deployment. It checks what data exists: subsets, splits, rows, labels, columns, licensing notes, and odd schema details. Its result is a dataset readiness summary. If the user already has a model and wants a demo, or asks for quantization on a laptop, this routine is not the fit.",
    },
    {
        "name": "implicit-hf-local-model-chooser",
        "description": "Chooses local Hugging Face or GGUF models by task, memory budget, quantization, runtime, and latency constraints.",
        "body": "This routine starts from hardware reality. It compares model size, quantization, runtime, task fit, and expected latency, then recommends candidates that fit the user's machine. It does not audit dataset rows, build demos, or run benchmark evaluations unless those are explicitly the next step.",
    },
    {
        "name": "implicit-slo-alert-author",
        "description": "Produces alerting rules from SLOs, metric names, windows, labels, and severity policy.",
        "body": "This routine translates reliability goals into alerts. It needs metric names, thresholds, windows, and severity labels. The output is an alert rule and verification query. If the user wants a dashboard, an incident narrative, or trace diagnosis, choose a different routine.",
    },
    {
        "name": "implicit-trace-path-diagnoser",
        "description": "Uses distributed trace spans to locate latency, failed calls, dependency bottlenecks, and missing instrumentation.",
        "body": "This routine follows spans across services. It reads timing, parent-child relationships, failed spans, retries, and dependency calls, then identifies the critical path. The output is a trace-based diagnosis with caveats. It is not for writing dashboard panels or Prometheus alert rules.",
    },
]


EXTRA_ALTERNATIVES: dict[str, list[str]] = {
    "webhook-integration-planner": ["public-office-webhook-automation", "webhook-contract-planner"],
    "api-security-threat-reviewer": ["public-security-threat-model", "public-openai-security-best-practices", "security-threat-modeler"],
    "hf-dataset-viewer-inspector": ["public-huggingface-datasets", "public-huggingface-huggingface-tool-builder"],
    "hf-local-model-selector": ["public-huggingface-huggingface-local-models", "public-huggingface-huggingface-best"],
    "sentence-transformer-finetuner": ["public-huggingface-train-sentence-transformers", "public-swebench-similarity-search-patterns"],
    "prometheus-alert-rule-writer": ["public-swebench-prometheus-configuration", "slo-breach-checker"],
    "grafana-dashboard-builder": ["public-swebench-grafana-dashboards", "public-swebench-python-observability", "metrics-overview"],
    "distributed-trace-investigator": ["public-swebench-distributed-tracing", "public-swebench-python-observability", "metrics-root-cause-diagnoser"],
    "slo-breach-narrative-writer": ["incident-summary-writer", "slo-breach-checker"],
    "resilience-pattern-reviewer": ["public-swebench-python-resilience", "dependency-risk-auditor"],
    "service-mesh-traffic-debugger": ["public-swebench-service-mesh-observability", "public-swebench-istio-traffic-management", "public-swebench-linkerd-patterns"],
    "xlsx-formula-model-builder": ["public-office-xlsx-manipulation", "public-swebench-xlsx", "public-office-data-analysis"],
    "airtable-workflow-automator": ["public-office-airtable-automation", "public-office-crm-automation"],
    "notion-research-database-builder": ["public-office-notion-automation", "public-openai-notion-research-documentation"],
    "calendar-scheduling-optimizer": ["public-office-calendar-automation", "meeting-agenda-builder"],
    "meeting-notes-action-extractor": ["public-office-meeting-notes", "meeting-followup-extractor"],
    "email-classification-router": ["public-office-email-classifier", "public-office-gmail-workflows", "public-office-suspicious-email"],
    "pdf-form-filler": ["public-office-pdf-form-filler", "document-field-extractor"],
    "pdf-redaction-reviewer": ["privacy-risk-reviewer", "public-office-contract-review", "public-openai-pdf"],
    "visual-regression-checker": ["public-openai-screenshot", "public-anthropic-webapp-testing", "public-addy-web-web-quality-audit"],
    "accessibility-interaction-auditor": ["public-addy-web-accessibility", "public-addy-web-web-quality-audit", "accessibility-checker"],
    "pr-review-comment-resolver": ["public-openai-gh-address-comments", "review-comment-resolver"],
    "git-safety-guardrail-installer": ["public-mattpocock-git-guardrails-claude-code", "public-mattpocock-setup-pre-commit"],
}


IMPLICIT_STRESS_PROMPTS: list[dict[str, object]] = [
    {
        "id": "implicit_p1_pdf_answer",
        "family": "implicit_field_stress",
        "gold_skill": "implicit-pdf-evidence-answerer",
        "closest_alternatives": ["implicit-pdf-table-reconstructor", "pdf-question-answerer", "pdf-layout-table-extractor"],
        "prompt": "Read the PDF packet and answer whether travel meals after a delay are reimbursable. I need the answer and page evidence, not a reconstructed table.",
    },
    {
        "id": "implicit_p2_pdf_table",
        "family": "implicit_field_stress",
        "gold_skill": "implicit-pdf-table-reconstructor",
        "closest_alternatives": ["implicit-pdf-evidence-answerer", "pdf-layout-table-extractor", "pdf-question-answerer"],
        "prompt": "Pull the invoice rows from the PDF with page and row anchors. Keep it as structured data rather than a prose answer.",
    },
    {
        "id": "implicit_p3_browser_flow",
        "family": "implicit_field_stress",
        "gold_skill": "implicit-browser-flow-investigator",
        "closest_alternatives": ["implicit-visual-diff-reviewer", "playwright-flow-debugger", "visual-regression-checker"],
        "prompt": "The checkout button stops working after a coupon is applied. Reproduce the click path and use console or network evidence to explain the failure.",
    },
    {
        "id": "implicit_p4_visual_diff",
        "family": "implicit_field_stress",
        "gold_skill": "implicit-visual-diff-reviewer",
        "closest_alternatives": ["implicit-browser-flow-investigator", "visual-regression-checker", "playwright-flow-debugger"],
        "prompt": "Compare the baseline and new screenshots for layout shifts, clipping, spacing, and text overflow across desktop and mobile.",
    },
    {
        "id": "implicit_p5_ci_failure",
        "family": "implicit_field_stress",
        "gold_skill": "implicit-ci-failure-reader",
        "closest_alternatives": ["implicit-review-comment-planner", "ci-log-root-cause-debugger", "repo-code-reviewer"],
        "prompt": "Look at the CI log and find the first meaningful error plus the smallest fix and rerun sequence.",
    },
    {
        "id": "implicit_p6_review_comments",
        "family": "implicit_field_stress",
        "gold_skill": "implicit-review-comment-planner",
        "closest_alternatives": ["implicit-ci-failure-reader", "pr-review-comment-resolver", "repo-code-reviewer"],
        "prompt": "Use the existing reviewer feedback to group required fixes, note any questions, and prepare responses for each thread; do not do a fresh code review.",
    },
    {
        "id": "implicit_p7_hf_dataset",
        "family": "implicit_field_stress",
        "gold_skill": "implicit-hf-dataset-inspector",
        "closest_alternatives": ["implicit-hf-local-model-chooser", "hf-dataset-viewer-inspector", "hf-local-model-selector"],
        "prompt": "Before modelling, inspect the dataset splits, columns, row examples, labels, and schema caveats.",
    },
    {
        "id": "implicit_p8_hf_model",
        "family": "implicit_field_stress",
        "gold_skill": "implicit-hf-local-model-chooser",
        "closest_alternatives": ["implicit-hf-dataset-inspector", "hf-local-model-selector", "hf-dataset-viewer-inspector"],
        "prompt": "Choose a local model and quantization that can run on an 8 GB laptop for ticket classification.",
    },
    {
        "id": "implicit_p9_alert_rule",
        "family": "implicit_field_stress",
        "gold_skill": "implicit-slo-alert-author",
        "closest_alternatives": ["implicit-trace-path-diagnoser", "prometheus-alert-rule-writer", "distributed-trace-investigator"],
        "prompt": "Create alert rules from these checkout SLO metrics with windows, severity labels, and verification queries.",
    },
    {
        "id": "implicit_p10_trace_path",
        "family": "implicit_field_stress",
        "gold_skill": "implicit-trace-path-diagnoser",
        "closest_alternatives": ["implicit-slo-alert-author", "distributed-trace-investigator", "prometheus-alert-rule-writer"],
        "prompt": "Use these distributed trace spans to locate where checkout latency is introduced across services.",
    },
]


FIXTURES: dict[str, str] = {
    "pdf_document_operations/sample_packet.pdf": "Pseudo fixture for PDF question answering with policy sections and page anchors.\n",
    "pdf_document_operations/vendor_statement.pdf": "Pseudo fixture for a PDF statement with invoice rows and page layout clues.\n",
    "pdf_document_operations/scanned_receipts.pdf": "Pseudo fixture for scanned receipts requiring OCR and confidence markings.\n",
    "pdf_document_operations/reimbursement_form.pdf": "Pseudo fixture for a fillable reimbursement form.\n",
    "pdf_document_operations/client_contract.pdf": "Pseudo fixture for a contract containing names, addresses, prices, IDs, and confidential clauses.\n",
    "pdf_document_operations/training_manual.pdf": "Pseudo fixture for a PDF manual requiring editable DOCX conversion.\n",
    "huggingface_ml_workflows/customer_tickets_dataset.md": "# Dataset\nSubsets: default. Splits: train/validation/test. Columns: text, label, product, created_at.\n",
    "github_ci_maintenance/ci_log.txt": "Run pytest\nERROR tests/test_billing.py::test_invoice_total - AssertionError: expected 120.00 got 119.00\n",
    "github_ci_maintenance/pr_review_comments.md": "- Reviewer A: Please handle empty invoice lines.\n- Reviewer B: Add a regression test for tax rounding.\n",
    "github_ci_maintenance/payment_diff.patch": "diff --git a/payment.py b/payment.py\n+ total = subtotal + int(tax)\n",
    "github_ci_maintenance/issues.md": "# Issues\n1. Checkout fails on Safari.\n2. Please add CSV export.\n",
    "github_ci_maintenance/merged_prs.md": "- Add subscription pause API\n- Fix tax rounding bug\n- Remove legacy invoice endpoint\n",
    "api_mcp_tooling/billing_contract.yaml": "paths:\n  /subscriptions:\n    get:\n      responses:\n        '200': {description: ok}\n",
    "observability_reliability/metrics.md": "checkout_request_duration_seconds, checkout_error_rate, checkout_requests_total\n",
    "observability_reliability/checkout_trace.json": "{\"trace\": [{\"span\":\"checkout\",\"duration_ms\":820},{\"span\":\"payment\",\"duration_ms\":610}]}\n",
    "observability_reliability/incident_notes.md": "10:05 error rate > 5%; 10:12 rollback started; impact: checkout failures for AU users.\n",
    "observability_reliability/payment_client.py": "requests.post(url, json=payload)\n",
    "observability_reliability/mesh_config.yaml": "trafficSplit: 90/10\nmtls: STRICT\nretries: 3\n",
    "office_business_automation/revenue_assumptions.md": "Inputs: price, churn, expansion, seats, conversion rate. Outputs: MRR, ARR, cohort revenue.\n",
    "office_business_automation/meeting_notes.md": "Decision: launch beta. Action: Jacky draft evaluation plan by Friday. Open: API budget.\n",
    "office_business_automation/inbox_sample.md": "Subject: URGENT invoice issue\nSubject: Partnership request\nSubject: Meeting follow-up\n",
    "skill_representation_analysis/public_skill_sample.md": "Pseudo public skill with triggers, scripts, examples, and implicit constraints.\n",
    "skill_representation_analysis/hierarchical_skill.md": "Broad skill: analyse documents. If finance, use finance worksheet. If legal, use clause checklist.\n",
    "skill_representation_analysis/retrieval_results.json": "{\"results\": []}\n",
    "skill_representation_analysis/public_skill_repo/SKILL.md": "---\nname: example-public-skill\ndescription: Example public skill.\n---\n# Example\n",
}


def render_skill(skill: dict[str, object]) -> str:
    return SKILL_TEMPLATE.format(
        name=skill["name"],
        title=title_from_name(str(skill["name"])),
        description_json=json.dumps(skill["description"]),
        overview=skill["overview"],
        use_when=bullets(skill["use_when"]),  # type: ignore[arg-type]
        not_for=bullets(skill["not_for"]),  # type: ignore[arg-type]
        preconditions=bullets(skill["preconditions"]),  # type: ignore[arg-type]
        workflow=numbered(skill["workflow"]),  # type: ignore[arg-type]
        writing_rules=bullets(skill["writing_rules"]),  # type: ignore[arg-type]
        default_shape=bullets(skill["default_shape"]),  # type: ignore[arg-type]
    )


def render_implicit_skill(skill: dict[str, object]) -> str:
    return IMPLICIT_TEMPLATE.format(
        name=skill["name"],
        title=title_from_name(str(skill["name"])),
        description_json=json.dumps(skill["description"]),
        body=skill["body"],
    )


def build_prompts(cluster: dict[str, object]) -> list[dict[str, object]]:
    family = str(cluster["family"])
    skills: list[dict[str, object]] = cluster["skills"]  # type: ignore[assignment]
    prompts: list[dict[str, object]] = []
    names = [str(skill["name"]) for skill in skills]
    for index, skill in enumerate(skills, start=1):
        name = str(skill["name"])
        alternatives: list[str] = []
        for candidate in EXTRA_ALTERNATIVES.get(name, []):
            if candidate != name and candidate not in alternatives:
                alternatives.append(candidate)
        for other in names:
            if other != name and other not in alternatives:
                alternatives.append(other)
        prompts.append(
            {
                "id": f"{family}_p{index}_{name.replace('-', '_')}",
                "family": family,
                "gold_skill": name,
                "closest_alternatives": alternatives[:4],
                "prompt": skill["prompt"],
            }
        )
    return prompts


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    skills_root = repo_root / "skills"
    prompts_root = repo_root / "prompts"
    stress_prompts_root = repo_root / "stress_prompts"
    fixtures_root = repo_root / "fixtures"

    for cluster in CONTROLLED_CLUSTERS:
        family = str(cluster["family"])
        family_dir = skills_root / family
        if family_dir.exists():
            shutil.rmtree(family_dir)
        family_dir.mkdir(parents=True)
        for skill in cluster["skills"]:  # type: ignore[index]
            skill_dir = family_dir / str(skill["name"])
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(render_skill(skill), encoding="utf-8")
        prompts = build_prompts(cluster)
        (prompts_root / f"{family}_confusability.json").write_text(
            json.dumps(prompts, indent=2) + "\n",
            encoding="utf-8",
        )

    implicit_dir = skills_root / "implicit_field_stress"
    if implicit_dir.exists():
        shutil.rmtree(implicit_dir)
    implicit_dir.mkdir(parents=True)
    for skill in IMPLICIT_STRESS_SKILLS:
        skill_dir = implicit_dir / str(skill["name"])
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(render_implicit_skill(skill), encoding="utf-8")

    stress_prompts_root.mkdir(parents=True, exist_ok=True)
    implicit_prompt_text = json.dumps(IMPLICIT_STRESS_PROMPTS, indent=2) + "\n"
    (stress_prompts_root / "implicit_field_stress.json").write_text(
        implicit_prompt_text,
        encoding="utf-8",
    )
    (prompts_root / "implicit_field_stress_confusability.json").write_text(
        implicit_prompt_text,
        encoding="utf-8",
    )

    for relative_path, content in FIXTURES.items():
        path = fixtures_root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    controlled_prompt_count = sum(len(cluster["skills"]) for cluster in CONTROLLED_CLUSTERS)  # type: ignore[arg-type]
    print(f"Generated {controlled_prompt_count} new controlled prompts.")
    print(f"Generated {len(IMPLICIT_STRESS_PROMPTS)} implicit stress prompts outside the main prompt glob.")
    print(f"Generated {controlled_prompt_count + len(IMPLICIT_STRESS_SKILLS)} new skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
