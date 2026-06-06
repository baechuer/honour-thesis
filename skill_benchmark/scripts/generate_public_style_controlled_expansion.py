#!/usr/bin/env python3

from __future__ import annotations

import json
import shutil
from pathlib import Path


FAMILY = "public_style_controlled"


SHARED_CONTEXT = {
    "psc_pdf_document_work": "PDF document workflow involving extraction, OCR recovery, evidence answering, redaction, document packets, page anchors, and external sharing.",
    "psc_browser_quality": "Browser quality workflow involving web pages, interactions, screenshots, accessibility, runtime evidence, and regression checks.",
    "psc_huggingface_workflow": "Hugging Face machine-learning workflow involving datasets, models, embedding training, demos, Spaces, deployment, and evaluation.",
    "psc_github_maintenance": "GitHub repository maintenance workflow involving CI, pull requests, review threads, hooks, releases, changed code, and verification.",
    "psc_security_appsec": "Application-security workflow involving risks, code, features, dependencies, privacy, data handling, and mitigations.",
    "psc_research_reading": "Research-reading workflow involving papers, sources, claims, methods, evidence, comparison, synthesis, and thesis writing.",
    "psc_skill_representation": "Skill-library workflow involving skill artifacts, routing, fields, atomization, benchmark results, candidates, and evaluation.",
    "psc_data_analysis_intent": "Spreadsheet analysis workflow involving CSV data, metrics, data quality, anomalies, decision ranking, reporting, and business interpretation.",
}


CLUSTERS: list[dict[str, object]] = [
    {
        "cluster_id": "psc_pdf_document_work",
        "intent": "Public-style PDF work where extraction, OCR, question answering, and redaction sound close.",
        "skills": [
            {
                "name": "psc-pdf-native-extraction-pack",
                "description": "Extract native PDF text, tables, metadata, and anchors from born-digital PDFs for downstream structured use.",
                "good_fit": "Use this when the PDF already has selectable text or embedded table structure and the user wants reusable extracted content.",
                "requirements": ["Born-digital PDF or extracted page text", "Requested fields, tables, or metadata", "Need for page/table anchors"],
                "instructions": ["Check whether text is selectable before assuming OCR.", "Extract text blocks, table cells, metadata, and page anchors.", "Return JSON or tables with uncertainty notes."],
                "deliverables": ["Structured text/table/metadata extraction", "Page and table anchors", "Extraction caveats"],
                "watch_out": "Not the right tool for scanned-image OCR, redaction review, or answering one prose question from the PDF.",
                "dependencies": ["pdfplumber or equivalent native PDF parser"],
                "prompts": [
                    {
                        "level": "L2_natural",
                        "provider": "provider_implicit",
                        "text": "The vendor packet PDF has selectable text and tables. Pull out the document metadata, section text, and invoice rows into structured JSON with page anchors.",
                    },
                    {
                        "level": "L3_high_information",
                        "provider": "provider_explicit",
                        "text": "Use a pdfplumber-style native extraction workflow on the vendor packet. I need embedded text, table cells, metadata, and page anchors, not OCR or a prose answer.",
                    },
                ],
            },
            {
                "name": "psc-pdf-scan-ocr-recovery",
                "description": "Recover text from scanned PDF images while preserving page order, low-confidence spans, and manual-review regions.",
                "good_fit": "Use this when the PDF is image-based, photographed, faxed, or has no selectable text.",
                "requirements": ["Scanned PDF or page images", "Need to mark uncertain characters or regions", "Page-by-page recovery"],
                "instructions": ["Detect image-only pages.", "Run OCR or describe OCR recovery steps.", "Mark low-confidence tokens, signatures, handwriting, and unreadable regions."],
                "deliverables": ["Recovered page text", "Uncertainty markers", "Manual-review list"],
                "watch_out": "Not for native table extraction, form filling, or redaction planning when text is already available.",
                "dependencies": ["OCR engine", "image preprocessing when needed"],
                "prompts": [
                    {
                        "level": "L2_natural",
                        "provider": "provider_implicit",
                        "text": "This signed PDF packet looks like photographed scans. Recover the readable text page by page and flag uncertain handwriting or blurred regions.",
                    },
                    {
                        "level": "L3_high_information",
                        "provider": "provider_implicit",
                        "text": "Run an OCR recovery workflow for the scanned receipt PDF. Preserve page order and confidence notes instead of treating it as a born-digital table extraction.",
                    },
                ],
            },
            {
                "name": "psc-pdf-evidence-qa",
                "description": "Answer focused questions from PDF evidence with page-grounded support and uncertainty notes.",
                "good_fit": "Use this when the PDF is a source of truth and the user asks a question whose answer must be supported by document evidence.",
                "requirements": ["A focused question", "Readable PDF content", "Need for page or section evidence"],
                "instructions": ["Identify the question first.", "Find relevant pages or sections.", "Answer directly and attach evidence anchors.", "Flag unsupported claims."],
                "deliverables": ["Short answer", "Evidence with page anchors", "Unsupported or uncertain points"],
                "watch_out": "Do not convert the full PDF, extract every table, or perform OCR unless that is needed to answer the question.",
                "dependencies": ["PDF reader or extracted page text"],
                "prompts": [
                    {
                        "level": "L2_natural",
                        "provider": "provider_implicit",
                        "text": "From the policy PDF, tell me whether delayed-travel meals are reimbursable and point to the page evidence that supports the answer.",
                    },
                    {
                        "level": "L3_high_information",
                        "provider": "provider_implicit",
                        "text": "Answer a narrow question from the PDF with cited page evidence. I only need the supported answer and uncertainty notes, not a converted document or extracted table.",
                    },
                ],
            },
            {
                "name": "psc-pdf-redaction-pass",
                "description": "Review PDFs for sensitive data that must be redacted before external sharing.",
                "good_fit": "Use this before sending a contract, form, invoice, or legal packet outside the organization.",
                "requirements": ["Sharing context", "Sensitive categories to look for", "PDF or extracted text with page positions"],
                "instructions": ["Scan for names, IDs, addresses, pricing, signatures, confidential clauses, and account details.", "Classify risk by sensitivity and sharing context.", "Return a redaction checklist with anchors."],
                "deliverables": ["Redaction target list", "Risk category", "Page/section anchors", "Review notes"],
                "watch_out": "Not for general privacy policy review, native table extraction, or question answering.",
                "dependencies": ["PDF text/layout inspection", "sensitivity taxonomy"],
                "prompts": [
                    {
                        "level": "L2_natural",
                        "provider": "provider_implicit",
                        "text": "Before I send this contract PDF to a vendor, identify the page-level items that should be hidden, including names, addresses, pricing, IDs, and confidential clauses.",
                    },
                    {
                        "level": "L3_high_information",
                        "provider": "provider_implicit",
                        "text": "Prepare a PDF redaction checklist for external sharing. I need sensitive targets with page anchors, not a summary or field extraction table.",
                    },
                ],
            },
        ],
    },
    {
        "cluster_id": "psc_browser_quality",
        "intent": "Browser tasks where testing, visual inspection, DevTools diagnosis, and accessibility are easy to confuse.",
        "skills": [
            {
                "name": "psc-devtools-runtime-diagnoser",
                "description": "Diagnose broken web interactions using DOM state, console errors, network requests, screenshots, and runtime clues.",
                "good_fit": "Use this when an interaction fails and browser evidence is needed to identify likely cause.",
                "requirements": ["A target page or flow", "Symptom to reproduce", "Access to browser/runtime evidence"],
                "instructions": ["Reproduce the interaction.", "Collect console, network, DOM, and screenshot evidence.", "Separate UI state, API, timing, and JavaScript failure hypotheses."],
                "deliverables": ["Reproduction trace", "Evidence packet", "Likely cause", "Verification step"],
                "watch_out": "Not just screenshot capture, accessibility review, or a scripted regression suite.",
                "dependencies": ["Browser DevTools or equivalent runtime inspector"],
                "prompts": [
                    {
                        "level": "L2_natural",
                        "provider": "provider_implicit",
                        "text": "The checkout Apply Coupon button stops responding after the first click. Reproduce the path and use browser evidence to explain whether it is DOM state, network, or JavaScript logic.",
                    },
                    {
                        "level": "L3_high_information",
                        "provider": "provider_explicit",
                        "text": "Use Chrome DevTools-style evidence for the broken checkout interaction: console errors, network failures, DOM state, and screenshots. Do not only write Playwright assertions.",
                    },
                ],
            },
            {
                "name": "psc-playwright-regression-suite",
                "description": "Create or run Playwright interaction tests with navigation, form actions, assertions, screenshots, and reproducible failure output.",
                "good_fit": "Use this when the desired artifact is an automated browser test or regression check.",
                "requirements": ["Target route or flow", "Expected behavior", "Assertions and test data"],
                "instructions": ["Define the browser path.", "Add interactions and assertions.", "Capture screenshots or traces on failure.", "Return test code or test report."],
                "deliverables": ["Playwright test steps or code", "Expected/actual result", "Trace or screenshot evidence"],
                "watch_out": "Not for one-off visual review, manual DevTools debugging, or accessibility-only audits.",
                "dependencies": ["Playwright"],
                "prompts": [
                    {
                        "level": "L2_natural",
                        "provider": "provider_implicit",
                        "text": "Build a repeatable browser regression check for the checkout form: navigate, fill fields, apply the coupon, assert the discount message, and capture failure evidence.",
                    },
                    {
                        "level": "L3_high_information",
                        "provider": "provider_explicit",
                        "text": "Write a Playwright test for the checkout coupon flow with assertions and screenshots. I need reusable regression coverage, not just a manual DevTools diagnosis.",
                    },
                ],
            },
            {
                "name": "psc-visual-screenshot-reviewer",
                "description": "Compare page screenshots or visual states for layout shifts, clipping, spacing, typography, and responsive regressions.",
                "good_fit": "Use this when the input is screenshot evidence or expected/current visual states.",
                "requirements": ["Baseline/current screenshots or rendered states", "Viewport or device context", "Visual acceptance criteria"],
                "instructions": ["Compare layout, spacing, clipping, contrast, and text overflow.", "Group issues by viewport and severity.", "Avoid inferring runtime cause without evidence."],
                "deliverables": ["Visual difference list", "Viewport-specific severity", "Screenshot anchors"],
                "watch_out": "Not for full browser test automation or DOM/network diagnosis unless screenshots point there.",
                "dependencies": ["Screenshot artifacts"],
                "prompts": [
                    {
                        "level": "L2_natural",
                        "provider": "provider_implicit",
                        "text": "Compare the old and new pricing-page screenshots and call out visible layout regressions, spacing changes, clipped content, and mobile text overflow.",
                    },
                    {
                        "level": "L3_high_information",
                        "provider": "provider_implicit",
                        "text": "Do a visual regression review from screenshot pairs across desktop and mobile. I need layout differences and severity, not browser interaction debugging.",
                    },
                ],
            },
            {
                "name": "psc-accessibility-interaction-auditor",
                "description": "Audit web interactions for keyboard access, focus order, labels, ARIA state, contrast, and screen-reader usability.",
                "good_fit": "Use this when the success criterion is accessibility rather than visual polish or generic UI behavior.",
                "requirements": ["Target component or flow", "Interaction states", "Accessibility criteria such as WCAG or keyboard/screen-reader checks"],
                "instructions": ["Check labels, roles, focus behavior, keyboard path, contrast, and error announcement.", "Separate blocker, serious, and minor issues.", "Return remediation steps."],
                "deliverables": ["Accessibility findings", "Affected element/state", "Severity", "Recommended fix"],
                "watch_out": "Not for only screenshot comparison, generic UI testing, or performance profiling.",
                "dependencies": ["Browser accessibility tree or manual keyboard inspection"],
                "prompts": [
                    {
                        "level": "L2_natural",
                        "provider": "provider_implicit",
                        "text": "Audit the account settings modal for keyboard navigation, focus trapping, labels, contrast, and whether form errors are announced clearly.",
                    },
                    {
                        "level": "L3_high_information",
                        "provider": "provider_implicit",
                        "text": "Review this web form specifically for accessibility interaction quality: keyboard path, accessible names, ARIA state, focus order, and screen-reader error feedback.",
                    },
                ],
            },
        ],
    },
    {
        "cluster_id": "psc_huggingface_workflow",
        "intent": "Hugging Face tasks where dataset inspection, local model selection, training, and deployment share vocabulary.",
        "skills": [
            {
                "name": "psc-hf-dataset-card-inspector",
                "description": "Inspect Hugging Face dataset cards, subsets, splits, columns, labels, examples, licensing, and schema caveats.",
                "good_fit": "Use before modelling when the user needs to understand data shape and suitability.",
                "requirements": ["Dataset id/card or dataset description", "Need for splits, columns, row examples, or labels"],
                "instructions": ["Inspect dataset metadata.", "Check subsets/splits/features.", "List examples and caveats.", "Identify readiness risks."],
                "deliverables": ["Dataset readiness summary", "Schema and split table", "Risks"],
                "watch_out": "Not for local model selection, fine-tuning, Gradio UI, or Spaces deployment.",
                "dependencies": ["Hugging Face Dataset Viewer or dataset card"],
                "prompts": [
                    {
                        "level": "L2_natural",
                        "provider": "provider_explicit",
                        "text": "Use Hugging Face dataset information to inspect the ticket dataset's splits, columns, labels, row examples, and licensing caveats before we model it.",
                    },
                    {
                        "level": "L3_high_information",
                        "provider": "provider_implicit",
                        "text": "Before training anything, audit the dataset card: subsets, train/validation/test split, feature schema, example rows, labels, and data caveats.",
                    },
                ],
            },
            {
                "name": "psc-local-model-fit-selector",
                "description": "Choose local model candidates by task, memory, quantization, runtime, latency, and installation constraints.",
                "good_fit": "Use when hardware limits are central to model choice.",
                "requirements": ["Task type", "Memory/runtime budget", "Quality and latency tradeoff"],
                "instructions": ["Translate task needs into model family constraints.", "Compare model sizes and quantization options.", "Recommend candidates with fallback checks."],
                "deliverables": ["Model shortlist", "Quantization choice", "Hardware fit reasoning", "Setup checks"],
                "watch_out": "Not for dataset schema inspection, fine-tuning plans, or hosted demo deployment.",
                "dependencies": ["Local runtime such as GGUF, llama.cpp, transformers, or MLX"],
                "prompts": [
                    {
                        "level": "L2_natural",
                        "provider": "provider_implicit",
                        "text": "I need a support-ticket classifier that can run locally on an 8 GB laptop. Shortlist realistic model sizes, quantization choices, and latency tradeoffs.",
                    },
                    {
                        "level": "L3_high_information",
                        "provider": "provider_explicit",
                        "text": "Choose Hugging Face or GGUF local model candidates for an 8 GB Mac. I need memory-fit and quantization reasoning, not a dataset card audit.",
                    },
                ],
            },
            {
                "name": "psc-sentence-embedding-trainer",
                "description": "Plan sentence embedding fine-tuning with positive pairs, hard negatives, loss choice, splits, and retrieval metrics.",
                "good_fit": "Use when the user has labelled query-document or skill-query pairs and wants a better embedding model.",
                "requirements": ["Training pairs or triplets", "Retrieval objective", "Evaluation labels or split"],
                "instructions": ["Define positives, negatives, and leakage controls.", "Choose a base model and contrastive/ranking loss.", "Specify top-k and MRR evaluation."],
                "deliverables": ["Training plan", "Loss and data format", "Evaluation setup", "Risk notes"],
                "watch_out": "Not for choosing an off-the-shelf local LLM or building a demo UI.",
                "dependencies": ["sentence-transformers or equivalent embedding training stack"],
                "prompts": [
                    {
                        "level": "L2_natural",
                        "provider": "provider_implicit",
                        "text": "We have labelled skill queries, gold skills, and hard negatives. Design the embedding fine-tuning setup and retrieval evaluation for a skill router.",
                    },
                    {
                        "level": "L3_high_information",
                        "provider": "provider_explicit",
                        "text": "Plan a SentenceTransformer fine-tuning run with positives, hard negatives, loss function, splits, top-k recall, and MRR. Do not choose a local chatbot model.",
                    },
                ],
            },
            {
                "name": "psc-hf-space-deployment-preparer",
                "description": "Prepare Hugging Face Space deployment with app files, requirements, hardware tier, queue behavior, secrets, and verification.",
                "good_fit": "Use when a demo or model app needs to be published on Spaces.",
                "requirements": ["App or demo code", "Space hardware/runtime choice", "Dependencies and secrets"],
                "instructions": ["Check app entrypoint and requirements.", "Select CPU/GPU/ZeroGPU assumptions.", "Plan secrets, queues, and sleep behavior.", "Verify public launch."],
                "deliverables": ["Space file checklist", "Runtime constraints", "Deployment verification"],
                "watch_out": "Not for model training, dataset inspection, or local-only model selection.",
                "dependencies": ["Hugging Face Spaces", "Gradio or Streamlit when relevant"],
                "prompts": [
                    {
                        "level": "L2_natural",
                        "provider": "provider_explicit",
                        "text": "Prepare the classifier demo for Hugging Face Spaces with requirements, app entrypoint, secrets, hardware tier, queue behavior, and verification after launch.",
                    },
                    {
                        "level": "L3_high_information",
                        "provider": "provider_implicit",
                        "text": "Package this model demo for a hosted Space-style deployment. Focus on runtime files, dependency pins, GPU/queue assumptions, and launch checks rather than training.",
                    },
                ],
            },
        ],
    },
    {
        "cluster_id": "psc_github_maintenance",
        "intent": "GitHub maintenance where CI failure, review resolution, guardrail installation, and release communication share repository language.",
        "skills": [
            {
                "name": "psc-ci-log-first-failure-reader",
                "description": "Read CI logs to find the first meaningful failure, likely root cause, minimal fix, and rerun path.",
                "good_fit": "Use when the starting artifact is a failed build or test log.",
                "requirements": ["Failed job output", "Need for first meaningful error", "Rerun or fix sequence"],
                "instructions": ["Ignore cascading failures until the first root error is found.", "Quote log evidence.", "Map the error to dependency, config, test, or code cause."],
                "deliverables": ["Failing job", "Root-cause hypothesis", "Evidence", "Fix/rerun plan"],
                "watch_out": "Not a fresh code review, PR-comment resolver, or changelog writer.",
                "dependencies": ["CI logs", "GitHub Actions or equivalent CI"],
                "prompts": [
                    {
                        "level": "L2_natural",
                        "provider": "provider_implicit",
                        "text": "The build failed after the last push. Read the CI output, identify the first real error, explain the likely cause, and give the smallest rerun sequence.",
                    },
                    {
                        "level": "L3_high_information",
                        "provider": "provider_explicit",
                        "text": "Analyze the failed GitHub Actions log for the first meaningful failure and minimal fix path. Do not turn this into a PR review or release note.",
                    },
                ],
            },
            {
                "name": "psc-pr-thread-fix-planner",
                "description": "Convert existing pull request review threads into required code changes, response notes, and verification steps.",
                "good_fit": "Use when reviewer comments already exist and the task is to address them.",
                "requirements": ["Review comments or PR threads", "Code context", "Need for response/action mapping"],
                "instructions": ["Group comments by requested change.", "Map each thread to code/test action.", "Separate accepted fixes from clarification questions.", "Prepare response notes."],
                "deliverables": ["Thread action map", "Patch plan", "Verification", "Reply notes"],
                "watch_out": "Not for fresh code review or CI log diagnosis unless those are requested in the comments.",
                "dependencies": ["GitHub PR review threads"],
                "prompts": [
                    {
                        "level": "L2_natural",
                        "provider": "provider_implicit",
                        "text": "Use the review threads on this PR to plan the required fixes, tests, and replies. The comments already exist; I need an action map.",
                    },
                    {
                        "level": "L3_high_information",
                        "provider": "provider_explicit",
                        "text": "Address unresolved GitHub PR review comments by mapping each thread to code/test changes and response text. Do not perform a fresh review from scratch.",
                    },
                ],
            },
            {
                "name": "psc-repo-guardrail-hook-installer",
                "description": "Set up repository guardrails such as pre-commit hooks, protected commands, secret checks, and verification commands.",
                "good_fit": "Use when the output is workflow safety configuration rather than analysis of a current failure.",
                "requirements": ["Repository tooling", "Risky operations to block", "Verification commands"],
                "instructions": ["Choose hook or guardrail mechanism.", "Define blocked operations and checks.", "Document bypass/maintenance policy.", "Verify with safe dry runs."],
                "deliverables": ["Hook/config plan", "Blocked actions", "Verification", "Maintenance notes"],
                "watch_out": "Not for analyzing CI logs or writing release notes.",
                "dependencies": ["Git hooks, Husky, pre-commit, or local command wrapper"],
                "prompts": [
                    {
                        "level": "L2_natural",
                        "provider": "provider_implicit",
                        "text": "Set up repository safeguards so contributors cannot accidentally commit secrets or run destructive git operations without confirmation.",
                    },
                    {
                        "level": "L3_high_information",
                        "provider": "provider_implicit",
                        "text": "Design git hook guardrails for secret commits, force pushes, reset --hard, branch deletion, and unsafe clean commands, including verification steps.",
                    },
                ],
            },
            {
                "name": "psc-release-communication-packager",
                "description": "Turn merged changes into audience-appropriate release notes, changelog sections, upgrade notes, and breaking-change warnings.",
                "good_fit": "Use after changes are merged or ready to ship and the user needs release communication.",
                "requirements": ["Merged PRs, commits, or change list", "Audience", "Release categories"],
                "instructions": ["Group features, fixes, breaking changes, and migrations.", "Adjust language to user/developer audience.", "Keep implementation details only when useful."],
                "deliverables": ["Release notes", "Changelog bullets", "Upgrade caveats"],
                "watch_out": "Not for code review, review-thread resolution, or CI failure debugging.",
                "dependencies": ["Commit or PR summary"],
                "prompts": [
                    {
                        "level": "L2_natural",
                        "provider": "provider_implicit",
                        "text": "Turn the merged PR list into release notes grouped by features, fixes, and breaking changes, with upgrade notes where needed.",
                    },
                    {
                        "level": "L3_high_information",
                        "provider": "provider_implicit",
                        "text": "Prepare user-facing release communication from completed changes. I need release notes/changelog language, not bug-finding or CI triage.",
                    },
                ],
            },
        ],
    },
    {
        "cluster_id": "psc_security_appsec",
        "intent": "Security workflows where threat modeling, code review, dependency auditing, and privacy review all look like risk analysis.",
        "skills": [
            {
                "name": "psc-feature-threat-modeler",
                "description": "Threat-model a planned feature by identifying assets, actors, trust boundaries, abuse cases, and mitigations before implementation.",
                "good_fit": "Use during design, before code exists or before implementation choices are fixed.",
                "requirements": ["Feature design", "Actors/assets", "Trust boundaries or data flows"],
                "instructions": ["Identify assets, actors, boundaries, entry points, and misuse cases.", "Prioritize threats and mitigations.", "List assumptions and follow-up checks."],
                "deliverables": ["Threat model", "Abuse cases", "Mitigations", "Assumptions"],
                "watch_out": "Not for reviewing one code handler, dependency supply-chain risk, or data-retention policy.",
                "dependencies": ["Feature notes or architecture sketch"],
                "prompts": [
                    {
                        "level": "L2_natural",
                        "provider": "provider_implicit",
                        "text": "Before building invite-by-link file sharing, map what needs protection, who can interact with it, where control changes hands, how it could be abused, and what safeguards we should add.",
                    },
                    {
                        "level": "L3_high_information",
                        "provider": "provider_implicit",
                        "text": "Create a design-stage threat model for the new collaborator-invite feature. I need abuse paths and mitigations, not a code-level vulnerability review.",
                    },
                ],
            },
            {
                "name": "psc-handler-vulnerability-reviewer",
                "description": "Review a specific code path for concrete security vulnerabilities, exploitability, and implementation-level fixes.",
                "good_fit": "Use when code or a diff exists and the user wants vulnerabilities tied to implementation behavior.",
                "requirements": ["Code snippet, diff, or handler", "Security concern", "Fix and test expectation"],
                "instructions": ["Trace inputs, auth checks, validation, output, and side effects.", "Identify exploitable flaws.", "Suggest minimal fixes and tests."],
                "deliverables": ["Vulnerability finding", "Affected code path", "Exploit condition", "Fix/test"],
                "watch_out": "Not for broad design threat modeling or privacy retention policy review.",
                "dependencies": ["Code or diff"],
                "prompts": [
                    {
                        "level": "L2_natural",
                        "provider": "provider_implicit",
                        "text": "Review this redirect handler for concrete security bugs around user input, auth checks, URL validation, and test coverage.",
                    },
                    {
                        "level": "L3_high_information",
                        "provider": "provider_implicit",
                        "text": "Do an implementation-level security review of the API handler. Focus on exploitable flaws and code fixes, not feature-level threat modeling.",
                    },
                ],
            },
            {
                "name": "psc-dependency-supply-chain-auditor",
                "description": "Assess third-party dependency risk from package metadata, maintainer signals, install scripts, transitive dependencies, and version history.",
                "good_fit": "Use before adding or upgrading packages where supply-chain risk matters.",
                "requirements": ["Package name/version or lockfile diff", "Dependency tree", "Risk tolerance"],
                "instructions": ["Check package purpose, maintainers, scripts, permissions, old transitive dependencies, and update cadence.", "Return risk level and mitigation."],
                "deliverables": ["Dependency risk summary", "Risk evidence", "Mitigation or alternative"],
                "watch_out": "Not for reviewing first-party code logic or privacy data collection.",
                "dependencies": ["Package registry, lockfile, dependency tree"],
                "prompts": [
                    {
                        "level": "L2_natural",
                        "provider": "provider_implicit",
                        "text": "We are about to add an npm package with a postinstall script and many transitive dependencies. Assess the supply-chain risk and mitigation options.",
                    },
                    {
                        "level": "L3_high_information",
                        "provider": "provider_implicit",
                        "text": "Audit a third-party dependency before adoption: maintainer health, install scripts, transitive risk, old packages, and safer alternatives.",
                    },
                ],
            },
            {
                "name": "psc-privacy-telemetry-reviewer",
                "description": "Review data collection or telemetry plans for privacy, retention, minimization, consent, re-identification, and compliance concerns.",
                "good_fit": "Use when the risk is personal data handling rather than code exploitability.",
                "requirements": ["Data fields to collect", "Retention/sharing plan", "Purpose and user context"],
                "instructions": ["Classify data sensitivity.", "Check minimization, retention, consent, access, and re-identification risk.", "Recommend safer collection boundaries."],
                "deliverables": ["Privacy risks", "Data-field table", "Mitigations", "Retention/access notes"],
                "watch_out": "Not for generic security threat modeling or dependency risk.",
                "dependencies": ["Telemetry/data-flow description"],
                "prompts": [
                    {
                        "level": "L2_natural",
                        "provider": "provider_implicit",
                        "text": "Review the analytics plan that logs search queries, account region, role, clicked filters, and partial email domains for 18 months.",
                    },
                    {
                        "level": "L3_high_information",
                        "provider": "provider_implicit",
                        "text": "Assess privacy risk for a telemetry change: data minimization, retention, consent, access controls, and re-identification. Do not focus on code exploits.",
                    },
                ],
            },
        ],
    },
    {
        "cluster_id": "psc_research_reading",
        "intent": "Research reading tasks where summary, method extraction, citation grounding, and synthesis share academic language.",
        "skills": [
            {
                "name": "psc-paper-method-mapper",
                "description": "Extract a paper's method design, data, baselines, experimental setup, assumptions, and evaluation limitations.",
                "good_fit": "Use when the user cares about how a paper was carried out rather than only its conclusion.",
                "requirements": ["Paper or method excerpt", "Need for experiment/setup detail"],
                "instructions": ["Identify method components, data, baselines, metrics, and assumptions.", "Separate reported results from evaluation design.", "List limitations."],
                "deliverables": ["Method map", "Evaluation setup", "Assumptions", "Limitations"],
                "watch_out": "Not a general summary, citation support audit, or multi-paper synthesis.",
                "dependencies": ["Paper text"],
                "prompts": [
                    {
                        "level": "L2_natural",
                        "provider": "provider_implicit",
                        "text": "For this paper, map how the study was carried out: data, method components, baselines, metrics, assumptions, and evaluation limits.",
                    },
                    {
                        "level": "L3_high_information",
                        "provider": "provider_implicit",
                        "text": "Extract method and evaluation details from the paper. I need setup, baselines, metrics, assumptions, and limitations, not a broad summary.",
                    },
                ],
            },
            {
                "name": "psc-citation-claim-support-auditor",
                "description": "Check whether a draft claim is supported by a source and record quoted/paraphrased evidence, caveats, and citation risk.",
                "good_fit": "Use when the user has a claim and needs to know whether the source supports it.",
                "requirements": ["Draft claim", "Source text", "Need for support/caveat judgment"],
                "instructions": ["Locate source evidence.", "Judge support strength.", "Identify overclaiming or missing caveats.", "Return safe wording."],
                "deliverables": ["Support verdict", "Evidence", "Caveat", "Safer wording"],
                "watch_out": "Not for summarizing the whole paper or extracting all methods.",
                "dependencies": ["Source text and draft claim"],
                "prompts": [
                    {
                        "level": "L2_natural",
                        "provider": "provider_implicit",
                        "text": "Check whether this source really supports my sentence about skill libraries improving agent reliability, and suggest safer wording if it overclaims.",
                    },
                    {
                        "level": "L3_high_information",
                        "provider": "provider_implicit",
                        "text": "Perform a citation-grounding audit for one draft claim: support strength, exact evidence, caveats, and revised claim wording.",
                    },
                ],
            },
            {
                "name": "psc-related-work-synthesizer",
                "description": "Synthesize multiple papers into related-work themes, contrasts, unresolved gaps, and positioning for a thesis argument.",
                "good_fit": "Use when there are multiple sources and the output should connect them into a research narrative.",
                "requirements": ["Two or more sources", "Need for thematic comparison and gap framing"],
                "instructions": ["Group approaches by theme.", "Compare assumptions and evidence.", "Identify tensions and gaps.", "Write positioning notes."],
                "deliverables": ["Related-work synthesis", "Theme comparison", "Gap statement"],
                "watch_out": "Not for single-paper method extraction or claim-level citation checking.",
                "dependencies": ["Multiple source notes"],
                "prompts": [
                    {
                        "level": "L2_natural",
                        "provider": "provider_implicit",
                        "text": "Use these three papers to write related-work notes that compare approaches, show where they agree or diverge, and identify the gap my thesis targets.",
                    },
                    {
                        "level": "L3_high_information",
                        "provider": "provider_implicit",
                        "text": "Synthesize multiple sources into a related-work argument with themes, contrasts, unresolved limitations, and thesis positioning.",
                    },
                ],
            },
            {
                "name": "psc-source-field-table-extractor",
                "description": "Extract specific fields from sources into a structured table for later comparison or coding.",
                "good_fit": "Use when the user wants reusable fields, not prose summary.",
                "requirements": ["Source text", "Field list or extraction schema", "Need for structured output"],
                "instructions": ["Identify requested fields.", "Extract values with evidence snippets.", "Mark missing or ambiguous fields.", "Return a table."],
                "deliverables": ["Field-value table", "Evidence snippets", "Missing-field notes"],
                "watch_out": "Not for broad synthesis, citation support, or method-only reading unless those are requested fields.",
                "dependencies": ["Source text and field schema"],
                "prompts": [
                    {
                        "level": "L2_natural",
                        "provider": "provider_implicit",
                        "text": "Extract each paper's dataset, task, model, baseline, metric, result, and limitation into a comparison table with source evidence.",
                    },
                    {
                        "level": "L3_high_information",
                        "provider": "provider_implicit",
                        "text": "Turn the source into a structured field table. I need field values and evidence snippets, not a narrative summary or related-work synthesis.",
                    },
                ],
            },
        ],
    },
    {
        "cluster_id": "psc_skill_representation",
        "intent": "Skill-library maintenance where field extraction, atomization, routing policy, and result adjudication are easily conflated.",
        "skills": [
            {
                "name": "psc-messy-skill-field-extractor",
                "description": "Extract triggers, inputs, outputs, workflow, dependencies, resources, examples, and boundaries from messy public-style skill files.",
                "good_fit": "Use when the source is an existing skill artifact and the output is a field audit.",
                "requirements": ["One or more skill files", "Field taxonomy", "Need for evidence spans"],
                "instructions": ["Read the raw skill body.", "Extract explicit and implicit fields.", "Quote evidence and mark missing fields.", "Separate artifact fields from inferred selector fields."],
                "deliverables": ["Field audit", "Evidence spans", "Explicit/implicit/missing labels"],
                "watch_out": "Not for authoring a new skill, installing a package, or evaluating retrieval results.",
                "dependencies": ["Raw skill artifacts"],
                "prompts": [
                    {
                        "level": "L2_natural",
                        "provider": "provider_implicit",
                        "text": "Review this rough capability note and produce a selector-facing inventory: when it should trigger, required inputs, expected artifact, steps, tools, examples, and gaps.",
                    },
                    {
                        "level": "L3_high_information",
                        "provider": "provider_implicit",
                        "text": "Perform a field-taxonomy audit of an existing skill artifact with evidence spans. Do not write or install a new skill.",
                    },
                ],
            },
            {
                "name": "psc-public-skill-atomizer",
                "description": "Split broad or hierarchical public skills into atomic skill candidates while preserving shared resources and routing boundaries.",
                "good_fit": "Use when one public skill contains multiple internal workflows or domain branches.",
                "requirements": ["Broad skill artifact", "Subworkflow boundaries", "Shared resources or links"],
                "instructions": ["Identify internal branches.", "Create atomic child-skill candidates.", "Preserve shared resources and parent links.", "State routing boundaries."],
                "deliverables": ["Atomic skill list", "Shared resources", "Parent/child mapping", "Boundary notes"],
                "watch_out": "Not for simple field extraction or retrieval-result scoring.",
                "dependencies": ["Broad skill file and linked resources"],
                "prompts": [
                    {
                        "level": "L2_natural",
                        "provider": "provider_implicit",
                        "text": "This public skill has separate finance, document, and research branches inside one file. Split it into atomic skill candidates and keep shared resources linked.",
                    },
                    {
                        "level": "L3_high_information",
                        "provider": "provider_implicit",
                        "text": "Atomize a broad hierarchical skill into standalone child skills with preserved resource references and routing boundaries.",
                    },
                ],
            },
            {
                "name": "psc-skill-routing-budget-planner",
                "description": "Design candidate-generation, representation, reranking, budget, fallback, and clarification policy for large skill libraries.",
                "good_fit": "Use when the requested artifact is a selector or routing policy.",
                "requirements": ["Skill library scale", "Candidate budget", "Representation/retrieval choices"],
                "instructions": ["Define first-stage retrieval.", "Choose representation fields.", "Set reranking and fallback policy.", "Specify metrics and cost controls."],
                "deliverables": ["Routing stages", "Budgets", "Representation fields", "Fallback/metrics"],
                "watch_out": "Not for auditing one skill's fields or splitting a hierarchical skill.",
                "dependencies": ["Skill library inventory or scale assumptions"],
                "prompts": [
                    {
                        "level": "L2_natural",
                        "provider": "provider_implicit",
                        "text": "Design a routing policy for a 2000-skill library: candidate generation, representation fields, reranking, fallback, and cost controls.",
                    },
                    {
                        "level": "L3_high_information",
                        "provider": "provider_implicit",
                        "text": "Specify a candidate-subsetting architecture for skill retrieval with top-k budgets, field-aware reranking, fallback, and evaluation metrics.",
                    },
                ],
            },
            {
                "name": "psc-retrieval-result-adjudicator",
                "description": "Adjudicate skill retrieval results with strict gold labels, acceptable alternatives, failure categories, top-k, MRR, and non-core false positives.",
                "good_fit": "Use after retrieval has already produced rankings and the task is evaluation.",
                "requirements": ["Prompt/gold set", "Ranked retrieval output", "Acceptable alternative policy"],
                "instructions": ["Score strict and acceptable labels separately.", "Compute top-k and MRR.", "Classify failures by candidate miss, reranker ordering, ambiguity, or better-than-gold."],
                "deliverables": ["Metrics", "Failure categories", "Adjudication notes", "Revision queue"],
                "watch_out": "Not for designing a router policy from scratch or extracting fields from raw skills.",
                "dependencies": ["Retrieval result JSON", "Gold labels"],
                "prompts": [
                    {
                        "level": "L2_natural",
                        "provider": "provider_implicit",
                        "text": "Evaluate these skill retrieval rankings with strict gold labels, acceptable alternatives, top-1, top-5, MRR, and failure categories.",
                    },
                    {
                        "level": "L3_high_information",
                        "provider": "provider_implicit",
                        "text": "Adjudicate retrieval results: separate strict and acceptable scoring, identify candidate misses versus reranker losses, and flag better-than-gold cases.",
                    },
                ],
            },
        ],
    },
    {
        "cluster_id": "psc_data_analysis_intent",
        "intent": "Same spreadsheet or dataset, different analytical intent: trust audit, anomaly watchlist, decision ranking, or executive narrative.",
        "skills": [
            {
                "name": "psc-data-trust-auditor",
                "description": "Audit whether tabular data is trustworthy by checking missing values, duplicates, invalid ranges, schema drift, and calculation assumptions.",
                "good_fit": "Use before acting on a dataset when the user asks whether the numbers can be trusted.",
                "requirements": ["Spreadsheet/CSV", "Expected fields or assumptions", "Need for quality checks"],
                "instructions": ["Check missingness, duplicates, invalid values, and schema drift.", "Flag formula or aggregation assumptions.", "Return trust verdict and fixes."],
                "deliverables": ["Data-quality findings", "Affected fields", "Severity", "Fix/check"],
                "watch_out": "Not for ranking options, executive storytelling, or root-cause explanation unless trust is established.",
                "dependencies": ["CSV/spreadsheet parser"],
                "prompts": [
                    {
                        "level": "L2_natural",
                        "provider": "provider_implicit",
                        "text": "Before we make a decision from this weekly channel CSV, check whether the data is trustworthy: missing values, duplicate rows, invalid ranges, and schema issues.",
                    },
                    {
                        "level": "L3_high_information",
                        "provider": "provider_implicit",
                        "text": "Audit the spreadsheet's data quality and assumptions. I need trustworthiness checks, not a ranking recommendation or executive summary.",
                    },
                ],
            },
            {
                "name": "psc-anomaly-watchlist-builder",
                "description": "Find unusual spikes, drops, outliers, concentration, and abrupt changes in tabular metrics for follow-up investigation.",
                "good_fit": "Use when the task is to identify what looks unusual rather than explain the final cause.",
                "requirements": ["Time series or metric table", "Baseline or comparison window", "Need for follow-up prioritization"],
                "instructions": ["Compare current values to baseline.", "Flag spikes, dips, outliers, and concentration.", "Rank anomalies by severity and confidence."],
                "deliverables": ["Anomaly watchlist", "Evidence metric/window", "Priority", "Next check"],
                "watch_out": "Not for data trust auditing, forecasting, or final executive narrative.",
                "dependencies": ["Tabular metrics"],
                "prompts": [
                    {
                        "level": "L2_natural",
                        "provider": "provider_implicit",
                        "text": "Scan the weekly channel metrics for unusual spikes, drops, outliers, or concentrated deviations that deserve follow-up.",
                    },
                    {
                        "level": "L3_high_information",
                        "provider": "provider_implicit",
                        "text": "Build an anomaly watchlist from the CSV with evidence windows and priorities. Do not turn it into a broad reporting brief.",
                    },
                ],
            },
            {
                "name": "psc-decision-ranking-analyst",
                "description": "Rank options for action using criteria, tradeoffs, evidence, constraints, and recommendation confidence.",
                "good_fit": "Use when the dataset represents alternatives and the output should choose or rank options.",
                "requirements": ["Candidate options", "Decision criteria", "Constraints and tradeoffs"],
                "instructions": ["Define criteria.", "Score and compare options.", "Explain tradeoffs and uncertainty.", "Recommend first action."],
                "deliverables": ["Ranked options", "Criteria", "Recommendation", "Tradeoffs"],
                "watch_out": "Not for general data quality checks or anomaly detection unless those affect the decision.",
                "dependencies": ["Option table or decision matrix"],
                "prompts": [
                    {
                        "level": "L2_natural",
                        "provider": "provider_implicit",
                        "text": "Compare the pilot options and rank which one we should act on first, using cost, impact, risk, confidence, and time-to-value.",
                    },
                    {
                        "level": "L3_high_information",
                        "provider": "provider_implicit",
                        "text": "Use the option table to produce a decision ranking with criteria, tradeoffs, and first-choice recommendation. Do not just summarize the dataset.",
                    },
                ],
            },
            {
                "name": "psc-executive-metric-narrator",
                "description": "Turn tabular metrics into an upward-facing executive brief with headline, key takeaways, risks, and recommended next steps.",
                "good_fit": "Use when the audience is leadership and the requested output is communication, not exploration.",
                "requirements": ["Metric table", "Business audience", "Need for concise takeaway narrative"],
                "instructions": ["Identify headline and key movements.", "Translate metrics into business implications.", "List risks and recommended next steps."],
                "deliverables": ["Executive headline", "Key takeaways", "Risks", "Recommended actions"],
                "watch_out": "Not for deep anomaly scanning, data-quality auditing, or option ranking unless requested.",
                "dependencies": ["Metric summary or spreadsheet"],
                "prompts": [
                    {
                        "level": "L2_natural",
                        "provider": "provider_implicit",
                        "text": "Turn the weekly performance table into a leadership-ready brief: headline, key movements, risks, and two recommended next steps.",
                    },
                    {
                        "level": "L3_high_information",
                        "provider": "provider_implicit",
                        "text": "Write an executive metric narrative from the spreadsheet. I need business takeaways and actions, not data validation or anomaly hunting.",
                    },
                ],
            },
        ],
    },
]


def bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def render_skill(skill: dict[str, object], cluster_id: str, intent: str) -> str:
    title = str(skill["name"]).replace("psc-", "").replace("-", " ").title()
    description = f"{SHARED_CONTEXT.get(cluster_id, '')} {skill['description']}".strip()
    return (
        f"---\n"
        f"name: {skill['name']}\n"
        f"description: {json.dumps(description)}\n"
        f"metadata:\n"
        f"  source_style: public_style_controlled\n"
        f"  cluster_id: {cluster_id}\n"
        f"---\n\n"
        f"# {title}\n\n"
        f"This is a public-style controlled skill used for retrieval evaluation. It is written as a practical capability note rather than a neat benchmark schema.\n\n"
        f"Cluster intent: {intent}\n\n"
        f"## When to use\n\n"
        f"{skill['good_fit']}\n\n"
        f"## Requirements\n\n"
        f"{bullets(skill['requirements'])}\n\n"
        f"## Instructions\n\n"
        f"{bullets(skill['instructions'])}\n\n"
        f"## Deliverables\n\n"
        f"{bullets(skill['deliverables'])}\n\n"
        f"## When not to use\n\n"
        f"{skill['watch_out']}\n\n"
        f"## External dependencies to preserve\n\n"
        f"{bullets(skill['dependencies'])}\n\n"
        f"## Example use\n\n"
        f"A good request names the artifact or situation, gives enough operational context to choose this capability, and asks for the deliverable above.\n"
    )


def prompt_rows(cluster: dict[str, object]) -> list[dict[str, object]]:
    cluster_id = str(cluster["cluster_id"])
    skills: list[dict[str, object]] = cluster["skills"]  # type: ignore[assignment]
    skill_names = [str(skill["name"]) for skill in skills]
    rows: list[dict[str, object]] = []
    for skill_index, skill in enumerate(skills, start=1):
        gold = str(skill["name"])
        alternatives = [name for name in skill_names if name != gold]
        for prompt_index, prompt in enumerate(skill["prompts"], start=1):  # type: ignore[index]
            axes = ["workflow_or_procedure", "output_artifact"]
            if skill["dependencies"]:
                axes.append("dependency_or_tool")
            if skill["requirements"]:
                axes.append("input_or_precondition")
            rows.append(
                {
                    "id": f"{cluster_id}_p{skill_index:02d}_{prompt_index}_{gold.replace('-', '_')}",
                    "family": FAMILY,
                    "cluster_id": cluster_id,
                    "source_style": "public_style_controlled",
                    "prompt_information_level": prompt["level"],
                    "provider_cue": prompt["provider"],
                    "gold_skill": gold,
                    "closest_alternatives": alternatives[:4],
                    "field_axes": axes,
                    "ambiguity_risk": "low" if prompt["level"] == "L3_high_information" else "medium",
                    "gold_rationale": f"The request asks for the {skill['deliverables'][0].lower()} produced by `{gold}`, with requirements matching its operating context.",
                    "rejection_rationale": {
                        alt: "Plausible same-cluster alternative, but it optimizes for a different artifact, workflow, dependency, or success criterion."
                        for alt in alternatives[:4]
                    },
                    "prompt": prompt["text"],
                }
            )
    return rows


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    skills_root = repo_root / "skills" / FAMILY
    prompts_path = repo_root / "prompts" / f"{FAMILY}_confusability.json"
    fixtures_root = repo_root / "fixtures" / FAMILY

    if skills_root.exists():
        shutil.rmtree(skills_root)
    skills_root.mkdir(parents=True)

    all_prompts: list[dict[str, object]] = []
    for cluster in CLUSTERS:
        cluster_id = str(cluster["cluster_id"])
        intent = str(cluster["intent"])
        for skill in cluster["skills"]:  # type: ignore[index]
            skill_dir = skills_root / str(skill["name"])
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(render_skill(skill, cluster_id, intent), encoding="utf-8")
            resources_dir = skill_dir / "resources"
            resources_dir.mkdir()
            (resources_dir / "operating_notes.md").write_text(
                f"# Operating Notes\n\nCluster: {cluster_id}\n\n{intent}\n",
                encoding="utf-8",
            )
        all_prompts.extend(prompt_rows(cluster))

    prompts_path.write_text(json.dumps(all_prompts, indent=2) + "\n", encoding="utf-8")
    fixtures_root.mkdir(parents=True, exist_ok=True)
    (fixtures_root / "README.md").write_text(
        "# Public-Style Controlled Fixtures\n\n"
        "These placeholder fixtures represent public-style requests where raw skill files are less schema-like than the original controlled benchmark.\n",
        encoding="utf-8",
    )

    print(f"Generated {len(CLUSTERS)} public-style controlled clusters.")
    print(f"Generated {sum(len(cluster['skills']) for cluster in CLUSTERS)} skills.")
    print(f"Generated {len(all_prompts)} prompts at {prompts_path}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
