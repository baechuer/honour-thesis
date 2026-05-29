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


def bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def numbered(items: list[str]) -> str:
    return "\n".join(f"{index}. {item}" for index, item in enumerate(items, start=1))


SKILLS = [
    {
        "family": "office_artifact_workflows",
        "name": "pdf-layout-reviewer",
        "title": "PDF Layout Reviewer",
        "description": "Reviews rendered PDF pages for layout fidelity, page order, visual artifacts, form placement, table alignment, and page-level reading risks.",
        "overview": "Inspects a PDF as a visual artifact rather than only as extracted text.",
        "use_when": [
            "The user cares about page-level visual fidelity, reading order, or layout defects.",
            "The PDF contains forms, tables, signatures, columns, figures, or generated pages that may render incorrectly.",
            "The desired output is a layout review with evidence by page or region.",
        ],
        "not_for": [
            "Extracting a fixed list of fields into a table.",
            "Running OCR on scanned pages as the main task.",
            "Converting an office file into Markdown as the main deliverable.",
        ],
        "preconditions": [
            "A PDF or rendered page evidence is available.",
            "The user asks for visual/layout correctness, not only content meaning.",
            "Important page regions, forms, or layout expectations are stated or inferable.",
        ],
        "workflow": [
            "Render or inspect representative pages before judging correctness.",
            "Check page order, headers, footers, tables, forms, columns, and cropped regions.",
            "Compare visual structure against the stated purpose of the document.",
            "Record defects with page or region anchors.",
            "Separate visual/layout problems from content-summary issues.",
        ],
        "writing_rules": [
            "Use page or region references when possible.",
            "Do not infer missing field values from layout alone.",
            "Prioritize visual issues that could change interpretation or usability.",
        ],
        "default_shape": [
            "Page or region",
            "Observed layout issue",
            "Why it matters",
            "Recommended fix or verification",
        ],
    },
    {
        "family": "office_artifact_workflows",
        "name": "pdf-ocr-extractor",
        "title": "PDF OCR Extractor",
        "description": "Extracts text from scanned or image-based PDFs where OCR uncertainty, page anchors, and unreadable regions must be preserved.",
        "overview": "Handles PDFs where the core problem is text recovery from images or scans.",
        "use_when": [
            "The source PDF is scanned, image-heavy, or has text that cannot be reliably selected.",
            "The user wants recovered text with uncertain or low-confidence regions marked.",
            "The output should preserve page anchors for later verification.",
        ],
        "not_for": [
            "Reviewing layout fidelity of a rendered PDF.",
            "Summarising a readable document.",
            "Converting a born-digital office document where OCR is unnecessary.",
        ],
        "preconditions": [
            "A scanned PDF, image PDF, or page images are available.",
            "The user accepts OCR uncertainty rather than expecting perfect structured fields.",
            "Page order or page numbers are available for anchoring.",
        ],
        "workflow": [
            "Identify whether the source is scanned or image-based.",
            "Run or simulate OCR extraction page by page.",
            "Mark unreadable, ambiguous, or low-confidence text spans.",
            "Preserve page anchors and important spatial clues.",
            "Return recovered text or extracted fields only when evidence is strong.",
        ],
        "writing_rules": [
            "Do not silently correct uncertain OCR output.",
            "Keep page anchors attached to recovered text.",
            "Flag areas that require manual inspection.",
        ],
        "default_shape": [
            "Page",
            "Recovered text or field",
            "Confidence or uncertainty note",
            "Manual check needed",
        ],
    },
    {
        "family": "office_artifact_workflows",
        "name": "docx-redline-editor",
        "title": "DOCX Redline Editor",
        "description": "Prepares tracked changes, comments, or revision instructions for a Word document while preserving document structure and author-facing edit rationale.",
        "overview": "Edits a DOCX-style document as a review artifact with revisions, not as a plain prose rewrite.",
        "use_when": [
            "The user asks for tracked changes, comments, or redline-style edits.",
            "The document structure, headings, comments, or reviewer rationale should be preserved.",
            "The output is an edit plan, change log, or revised Word-compatible document.",
        ],
        "not_for": [
            "Summarising the document.",
            "Converting the document to Markdown.",
            "Auditing spreadsheet formulas or slide layout.",
        ],
        "preconditions": [
            "A DOCX-style document, extracted Word content, or revision target is available.",
            "The user provides editing goals, reviewer stance, or change policy.",
            "The document has sections that need traceable edits.",
        ],
        "workflow": [
            "Identify the document structure and review objective.",
            "Separate direct edits from comments or author queries.",
            "Preserve headings, numbering, cross-references, and document flow.",
            "Explain edits that materially change meaning.",
            "Return changes in a traceable format suitable for Word review.",
        ],
        "writing_rules": [
            "Do not flatten structured documents into generic notes.",
            "Keep author-facing comments concise and actionable.",
            "Distinguish wording edits from substantive changes.",
        ],
        "default_shape": [
            "Section",
            "Proposed edit or comment",
            "Reason",
            "Risk or author decision needed",
        ],
    },
    {
        "family": "office_artifact_workflows",
        "name": "spreadsheet-formula-auditor",
        "title": "Spreadsheet Formula Auditor",
        "description": "Audits spreadsheet formulas, references, assumptions, sheet dependencies, and calculation risks without changing the workbook's analysis goal.",
        "overview": "Checks spreadsheet calculation logic rather than extracting rows or designing charts.",
        "use_when": [
            "The user asks whether formulas, references, assumptions, or linked sheets are correct.",
            "The workbook contains calculation chains, named assumptions, lookup formulas, or summary tabs.",
            "The output should identify formula risk and verification checks.",
        ],
        "not_for": [
            "Summarising a spreadsheet as a business report.",
            "Creating a visual chart from clean data.",
            "Extracting document fields from PDFs or forms.",
        ],
        "preconditions": [
            "A workbook, CSV plus formula notes, or sheet description is available.",
            "The task includes formula correctness, dependency, or assumption risk.",
            "Expected outputs or validation criteria are stated or inferable.",
        ],
        "workflow": [
            "Map sheets, inputs, formulas, outputs, and linked assumptions.",
            "Check formulas for broken references, inconsistent ranges, hard-coded values, and copy errors.",
            "Trace material outputs back to input assumptions.",
            "Identify checks that can confirm or falsify the calculation.",
            "Report risks by impact and required verification.",
        ],
        "writing_rules": [
            "Do not treat formula audit as general data analysis.",
            "Call out assumptions separately from formula errors.",
            "Preserve sheet and cell references when available.",
        ],
        "default_shape": [
            "Sheet or formula area",
            "Issue or risk",
            "Evidence",
            "Verification or fix",
        ],
    },
    {
        "family": "office_artifact_workflows",
        "name": "slide-deck-visual-auditor",
        "title": "Slide Deck Visual Auditor",
        "description": "Reviews presentation slides for visual consistency, text overflow, hierarchy, alignment, theme use, speaker-note fit, and export readiness.",
        "overview": "Checks an existing deck as a visual communication artifact.",
        "use_when": [
            "The user wants a slide deck checked for polish, consistency, or presentation readiness.",
            "The deck already exists and needs visual/layout feedback rather than new slide generation.",
            "The output should identify slide-level issues and fixes.",
        ],
        "not_for": [
            "Writing a full oral presentation script.",
            "Converting slides into Markdown notes.",
            "Debugging a browser UI or deployment failure.",
        ],
        "preconditions": [
            "A slide deck, slide images, or slide outline with visual constraints is available.",
            "The user cares about visual hierarchy, alignment, density, or export quality.",
            "Audience, format, or presentation purpose is known enough to judge fit.",
        ],
        "workflow": [
            "Inspect slide structure, theme, title hierarchy, and text density.",
            "Check alignment, spacing, image fit, chart legibility, and contrast.",
            "Identify text overflow or speaker-note mismatches.",
            "Prioritize fixes that improve oral delivery or audience comprehension.",
            "Return slide-level findings rather than rewriting the whole talk.",
        ],
        "writing_rules": [
            "Use slide numbers or titles when possible.",
            "Focus on visible deck problems, not the research argument unless asked.",
            "Keep recommendations implementable in slide software.",
        ],
        "default_shape": [
            "Slide",
            "Visual or communication issue",
            "Impact",
            "Recommended adjustment",
        ],
    },
    {
        "family": "office_artifact_workflows",
        "name": "office-to-markdown-converter",
        "title": "Office To Markdown Converter",
        "description": "Converts Office-style documents, slides, spreadsheets, or mixed files into Markdown while preserving content hierarchy, labels, tables, and source traceability.",
        "overview": "Turns office artifacts into Markdown for repositories, notes, or downstream text workflows.",
        "use_when": [
            "The user wants an Office or PDF-derived artifact converted into Markdown.",
            "The priority is reusable text structure, headings, tables, and traceability.",
            "The output should be Markdown rather than a visual layout review.",
        ],
        "not_for": [
            "Checking rendered PDF page fidelity.",
            "Auditing spreadsheet formulas.",
            "Producing tracked changes in a Word document.",
        ],
        "preconditions": [
            "A source file or extracted content is available.",
            "The target format is Markdown or Markdown-compatible notes.",
            "The user accepts some layout simplification unless they explicitly require pixel-level fidelity.",
        ],
        "workflow": [
            "Identify source format, content hierarchy, tables, and embedded artifacts.",
            "Convert headings, lists, labels, and tables into clean Markdown.",
            "Preserve source traceability for important sections or pages.",
            "Flag content that cannot be safely represented in Markdown.",
            "Return a clean Markdown artifact or conversion plan.",
        ],
        "writing_rules": [
            "Do not summarize away source content during conversion.",
            "Keep tables readable in Markdown.",
            "Mark omitted or unconvertible visual material explicitly.",
        ],
        "default_shape": [
            "Markdown output",
            "Conversion notes",
            "Unconverted or uncertain elements",
        ],
    },
    {
        "family": "deployment_browser_qa",
        "name": "playwright-flow-debugger",
        "title": "Playwright Flow Debugger",
        "description": "Reproduces a broken browser interaction flow with Playwright-style steps, selectors, console/network evidence, screenshots, and a failure hypothesis.",
        "overview": "Debugs an interactive web flow through browser automation evidence.",
        "use_when": [
            "The user reports a broken UI flow, flaky interaction, selector failure, or unexpected browser state.",
            "The task needs reproduction steps, screenshots, console logs, or network evidence.",
            "The output should explain why the interaction fails and how to fix or verify it.",
        ],
        "not_for": [
            "Comparing visual screenshots without an interaction failure.",
            "Checking deployment health after a successful build.",
            "Reviewing backend API contract design.",
        ],
        "preconditions": [
            "A target URL, local app, or browser reproduction path is available.",
            "The failing interaction, expected outcome, and observed behavior are known.",
            "Browser automation or equivalent evidence can be collected.",
        ],
        "workflow": [
            "Open the target flow in a controlled browser session.",
            "Reproduce the interaction with stable selectors and state notes.",
            "Capture console, network, screenshot, and DOM evidence around the failure.",
            "Identify whether the issue is selector, state, timing, data, accessibility, or app logic.",
            "Propose a fix and a verification path.",
        ],
        "writing_rules": [
            "Separate observed evidence from hypotheses.",
            "Prefer stable selectors and reproducible steps.",
            "Do not present visual preference feedback as a functional failure.",
        ],
        "default_shape": [
            "Reproduction steps",
            "Evidence captured",
            "Failure hypothesis",
            "Fix or verification",
        ],
    },
    {
        "family": "deployment_browser_qa",
        "name": "visual-regression-checker",
        "title": "Visual Regression Checker",
        "description": "Compares baseline and current screenshots across viewports to identify visual regressions, layout shifts, clipping, contrast changes, and unexpected differences.",
        "overview": "Detects visual changes between expected and current UI states.",
        "use_when": [
            "The user has baseline and current screenshots or wants a visual diff check.",
            "The main concern is layout shift, clipping, text overflow, contrast, or responsive rendering.",
            "The output should classify visual differences and their severity.",
        ],
        "not_for": [
            "Debugging why a button click fails.",
            "Running a deployment smoke test.",
            "Auditing slide decks or PDF documents.",
        ],
        "preconditions": [
            "Baseline and current screenshots, or a repeatable screenshot capture flow, are available.",
            "Relevant viewport sizes or pages are specified.",
            "Visual tolerance or acceptance criteria are known or can be stated.",
        ],
        "workflow": [
            "Collect comparable screenshots for each target viewport or state.",
            "Compare layout, text fit, image rendering, color, spacing, and clipping.",
            "Filter expected content differences from regressions.",
            "Rank issues by user impact and reproducibility.",
            "Return evidence with viewport and page/state references.",
        ],
        "writing_rules": [
            "Do not diagnose backend logic unless visual evidence supports it.",
            "Name the viewport or state for every finding.",
            "Separate cosmetic differences from usability regressions.",
        ],
        "default_shape": [
            "Page or state",
            "Viewport",
            "Observed difference",
            "Severity and suggested fix",
        ],
    },
    {
        "family": "deployment_browser_qa",
        "name": "accessibility-interaction-auditor",
        "title": "Accessibility Interaction Auditor",
        "description": "Audits keyboard navigation, focus order, accessible names, ARIA state, contrast clues, and interaction accessibility for a web interface.",
        "overview": "Checks whether a UI can be operated and understood through accessible interactions.",
        "use_when": [
            "The user asks about keyboard use, focus traps, screen-reader labels, ARIA state, or interaction accessibility.",
            "The interface has forms, modals, menus, controls, or dynamic state changes.",
            "The output should list accessibility barriers and verification steps.",
        ],
        "not_for": [
            "General visual regression comparison.",
            "Deployment log triage.",
            "PDF layout review.",
        ],
        "preconditions": [
            "A target page or UI state is available.",
            "The relevant controls, flow, or accessibility concern is stated.",
            "Keyboard, accessibility tree, or DOM evidence can be inspected.",
        ],
        "workflow": [
            "Identify the target flow and interactive controls.",
            "Check keyboard reachability, focus order, focus visibility, and escape paths.",
            "Inspect accessible names, roles, states, labels, and error messages.",
            "Assess contrast or visual cues where they affect interaction.",
            "Return barriers with concrete verification steps.",
        ],
        "writing_rules": [
            "Tie findings to user tasks, not abstract compliance only.",
            "Do not conflate visual polish with accessibility failure.",
            "Include retest instructions for each serious issue.",
        ],
        "default_shape": [
            "Control or flow",
            "Accessibility issue",
            "User impact",
            "Verification and fix",
        ],
    },
    {
        "family": "deployment_browser_qa",
        "name": "deployment-build-triager",
        "title": "Deployment Build Triager",
        "description": "Diagnoses build or deployment failures from logs, environment variables, dependency versions, package scripts, and hosting-platform error context.",
        "overview": "Finds why a deployment failed before the app can be verified in production.",
        "use_when": [
            "The user provides build logs, CI deploy logs, hosting errors, or package-script output.",
            "The task is to identify failure cause and remediation steps.",
            "The output should separate environment, dependency, build, and platform issues.",
        ],
        "not_for": [
            "Verifying a deployed URL after build success.",
            "Debugging an in-browser UI interaction.",
            "Reviewing API design quality.",
        ],
        "preconditions": [
            "Build or deployment logs are available.",
            "The target platform, build command, and relevant environment are known or inferable.",
            "The user wants diagnosis rather than a polished release announcement.",
        ],
        "workflow": [
            "Identify the failing stage and first meaningful error.",
            "Map errors to build scripts, dependencies, runtime versions, or platform settings.",
            "Check environment variable and configuration assumptions.",
            "Propose the smallest fix and a rerun/verification sequence.",
            "List residual risks if logs are incomplete.",
        ],
        "writing_rules": [
            "Do not chase later cascading errors before the first root error.",
            "Keep commands and config changes explicit.",
            "Call out missing logs or environment context.",
        ],
        "default_shape": [
            "Failing stage",
            "Likely root cause",
            "Evidence from logs",
            "Fix and rerun check",
        ],
    },
    {
        "family": "deployment_browser_qa",
        "name": "deployment-release-verifier",
        "title": "Deployment Release Verifier",
        "description": "Verifies a completed deployment through URL checks, smoke tests, environment sanity, asset loading, version evidence, and rollback readiness.",
        "overview": "Checks whether a release is safely live after build/deploy completes.",
        "use_when": [
            "The deployment appears successful and the user wants release verification.",
            "The task includes smoke tests, environment checks, version confirmation, or rollback readiness.",
            "The output should be a release verification checklist with evidence.",
        ],
        "not_for": [
            "Diagnosing a failed build log.",
            "Performing a visual regression diff as the main task.",
            "Planning API integration architecture.",
        ],
        "preconditions": [
            "A deployed URL, environment, or release artifact is available.",
            "Expected smoke-test behavior and critical pages are known.",
            "The user wants readiness evidence, not implementation changes.",
        ],
        "workflow": [
            "Confirm deployment URL, version, environment, and critical config.",
            "Run smoke checks for key routes, assets, forms, auth boundaries, and console errors.",
            "Check monitoring or logs for immediate failures.",
            "Confirm rollback path or previous stable release reference.",
            "Return pass/fail evidence and release risks.",
        ],
        "writing_rules": [
            "Do not treat build success as release success.",
            "Record exact URLs, versions, or checks when available.",
            "Separate blocking release issues from follow-up improvements.",
        ],
        "default_shape": [
            "Check",
            "Evidence",
            "Status",
            "Release risk or next action",
        ],
    },
    {
        "family": "deployment_browser_qa",
        "name": "web-performance-budget-checker",
        "title": "Web Performance Budget Checker",
        "description": "Evaluates a web page against performance budgets using load metrics, bundle clues, trace evidence, network weight, and user-impact prioritization.",
        "overview": "Checks whether a page meets speed and budget expectations.",
        "use_when": [
            "The user asks about load time, performance budget, bundle size, Core Web Vitals, or trace evidence.",
            "The task requires performance diagnosis rather than functional interaction debugging.",
            "The output should prioritize performance fixes by user impact.",
        ],
        "not_for": [
            "Visual screenshot regression comparison.",
            "Deployment smoke verification.",
            "Accessibility interaction auditing.",
        ],
        "preconditions": [
            "A target page, performance report, trace, or network evidence is available.",
            "Budget thresholds or performance goals are stated or can be proposed.",
            "The user wants diagnosis or prioritization, not a broad UI review.",
        ],
        "workflow": [
            "Identify target pages, devices, and performance budgets.",
            "Review load metrics, bundle size, blocking resources, images, and network waterfalls.",
            "Separate lab data, field data, and configuration assumptions.",
            "Prioritize bottlenecks by user impact and implementation effort.",
            "Return concrete performance checks and fixes.",
        ],
        "writing_rules": [
            "Do not claim field performance from lab-only evidence.",
            "Attach findings to a metric or trace clue.",
            "Avoid generic optimization advice without evidence.",
        ],
        "default_shape": [
            "Metric or budget",
            "Observed issue",
            "Evidence",
            "Priority fix",
        ],
    },
    {
        "family": "api_backend_design",
        "name": "openapi-contract-reviewer",
        "title": "OpenAPI Contract Reviewer",
        "description": "Reviews OpenAPI or endpoint contracts for schema correctness, status codes, auth behavior, examples, error models, pagination, and client compatibility.",
        "overview": "Audits an API contract as a client-facing specification.",
        "use_when": [
            "The user provides an OpenAPI spec, endpoint documentation, or API contract.",
            "The task is to find contract ambiguity, schema mismatch, or client integration risk.",
            "The output should be contract findings tied to endpoints and fields.",
        ],
        "not_for": [
            "Planning a third-party API integration from scratch.",
            "Designing webhook processing and retry behavior.",
            "Reviewing high-level service architecture boundaries.",
        ],
        "preconditions": [
            "Endpoint paths, schemas, status codes, examples, or auth rules are available.",
            "The user wants contract quality, not implementation debugging.",
            "Client compatibility or API behavior expectations are known enough to assess.",
        ],
        "workflow": [
            "Identify endpoints, schemas, examples, status codes, and auth requirements.",
            "Check request/response schema consistency and missing examples.",
            "Review error behavior, pagination, filtering, versioning, and backward compatibility.",
            "Flag ambiguous or unsafe contract assumptions for clients.",
            "Return endpoint-level findings with recommended contract changes.",
        ],
        "writing_rules": [
            "Cite endpoint paths, fields, or status codes when possible.",
            "Do not redesign service architecture unless contract behavior requires it.",
            "Separate breaking contract issues from documentation polish.",
        ],
        "default_shape": [
            "Endpoint or schema",
            "Contract issue",
            "Client impact",
            "Recommended change",
        ],
    },
    {
        "family": "api_backend_design",
        "name": "external-api-integration-planner",
        "title": "External API Integration Planner",
        "description": "Plans integration with an external API by mapping authentication, endpoints, payload transformations, rate limits, retries, pagination, and failure handling.",
        "overview": "Turns external API documentation into an implementation plan.",
        "use_when": [
            "The user wants to connect to a third-party or external API.",
            "The task includes auth, endpoints, payload mapping, rate limits, retries, or pagination.",
            "The output should be an integration plan rather than a contract review.",
        ],
        "not_for": [
            "Reviewing an already-authored OpenAPI contract for quality.",
            "Designing webhook receiver semantics only.",
            "Mapping internal service dependencies without a specific external API.",
        ],
        "preconditions": [
            "External API docs, endpoint examples, auth method, or provider constraints are available.",
            "The desired product workflow or data mapping is known.",
            "Failure handling and rate-limit concerns are relevant.",
        ],
        "workflow": [
            "Identify auth method, endpoints, payloads, pagination, and provider limits.",
            "Map user workflow data to API request and response shapes.",
            "Plan retries, idempotency, caching, error handling, and observability.",
            "List secrets, environment variables, and permission requirements.",
            "Return implementation sequence and verification cases.",
        ],
        "writing_rules": [
            "Do not assume provider behavior absent from docs.",
            "Separate required calls from optional enhancements.",
            "Include failure and rate-limit behavior explicitly.",
        ],
        "default_shape": [
            "Integration goal",
            "Endpoint and auth plan",
            "Data mapping",
            "Failure handling and tests",
        ],
    },
    {
        "family": "api_backend_design",
        "name": "webhook-contract-planner",
        "title": "Webhook Contract Planner",
        "description": "Designs webhook receiver contracts with event selection, payload validation, signature verification, idempotency, retries, ordering, and dead-letter behavior.",
        "overview": "Plans inbound event handling where external systems call back into the application.",
        "use_when": [
            "The user asks how to receive, validate, process, or retry webhook events.",
            "The task includes signatures, event schemas, idempotency, ordering, or dead-letter handling.",
            "The output should be a webhook contract and processing plan.",
        ],
        "not_for": [
            "General third-party API polling integration.",
            "OpenAPI endpoint documentation review.",
            "Database migration risk analysis.",
        ],
        "preconditions": [
            "Webhook provider docs, event examples, or expected event types are available.",
            "Receiver endpoint, persistence model, or processing goal is known.",
            "The user needs event reliability and security behavior specified.",
        ],
        "workflow": [
            "Identify event types, payload shape, signature scheme, and delivery behavior.",
            "Define receiver endpoint contract, validation, and auth checks.",
            "Plan idempotency keys, retry behavior, ordering assumptions, and dead-letter handling.",
            "Map events to internal state changes and audit records.",
            "Return test cases for duplicate, delayed, invalid, and failed events.",
        ],
        "writing_rules": [
            "Do not ignore duplicate or replay events.",
            "Keep provider guarantees separate from application assumptions.",
            "Include security verification for signatures or shared secrets.",
        ],
        "default_shape": [
            "Event type",
            "Receiver contract",
            "Reliability behavior",
            "Security and test cases",
        ],
    },
    {
        "family": "api_backend_design",
        "name": "architecture-boundary-reviewer",
        "title": "Architecture Boundary Reviewer",
        "description": "Reviews backend architecture boundaries, dependency direction, module ownership, service responsibilities, and maintainability risks.",
        "overview": "Checks whether system structure has clear boundaries and sustainable dependency flow.",
        "use_when": [
            "The user asks whether modules, services, layers, or architecture patterns are well separated.",
            "The task involves dependency direction, ownership, coupling, or boundary violations.",
            "The output should be architecture findings and refactoring recommendations.",
        ],
        "not_for": [
            "Reviewing OpenAPI schema details.",
            "Planning external API auth and endpoint calls.",
            "Auditing database migration rollout risk only.",
        ],
        "preconditions": [
            "A codebase map, architecture summary, module list, or dependency evidence is available.",
            "The user wants structural feedback, not endpoint contract polish.",
            "Relevant business/domain responsibilities can be identified.",
        ],
        "workflow": [
            "Map modules, services, layers, owners, and dependency direction.",
            "Identify boundary leaks, cyclic dependencies, misplaced responsibilities, and coupling hotspots.",
            "Relate findings to maintainability, testability, and change risk.",
            "Recommend refactoring sequence with verification checks.",
            "Call out uncertainties where architecture evidence is incomplete.",
        ],
        "writing_rules": [
            "Avoid pattern name-dropping without evidence.",
            "Tie each recommendation to a boundary or dependency problem.",
            "Prefer incremental changes over broad rewrites.",
        ],
        "default_shape": [
            "Boundary or dependency",
            "Observed risk",
            "Impact",
            "Refactoring recommendation",
        ],
    },
    {
        "family": "api_backend_design",
        "name": "database-migration-risk-assessor",
        "title": "Database Migration Risk Assessor",
        "description": "Assesses database migration plans for locking, data backfill, compatibility, rollback, deployment ordering, and verification risk.",
        "overview": "Reviews schema/data changes as operational rollout risks.",
        "use_when": [
            "The user provides a migration file, schema change, rollout plan, or backfill task.",
            "The concern is production safety, locking, rollback, compatibility, or verification.",
            "The output should be migration risk findings and a safer rollout plan.",
        ],
        "not_for": [
            "General service architecture review.",
            "OpenAPI contract documentation review.",
            "External API integration planning.",
        ],
        "preconditions": [
            "Migration SQL, ORM migration, schema diff, or rollout notes are available.",
            "Database type, table size, or deployment constraints are stated or inferable.",
            "The user needs risk assessment before applying the change.",
        ],
        "workflow": [
            "Identify schema changes, data changes, indexes, constraints, and backfills.",
            "Check locking, long-running operations, compatibility with old and new app versions, and rollback path.",
            "Plan deployment ordering and feature-flag or dual-write needs.",
            "Define verification queries and failure recovery steps.",
            "Return a risk-ranked rollout recommendation.",
        ],
        "writing_rules": [
            "Do not assume migrations are safe because they are syntactically valid.",
            "Separate pre-deploy, deploy, backfill, and post-deploy checks.",
            "Call out missing production-size or database-engine context.",
        ],
        "default_shape": [
            "Migration element",
            "Risk",
            "Why it matters",
            "Safer rollout or verification",
        ],
    },
    {
        "family": "api_backend_design",
        "name": "service-dependency-mapper",
        "title": "Service Dependency Mapper",
        "description": "Maps service dependencies, upstream and downstream calls, owners, data contracts, failure modes, and operational handoff points.",
        "overview": "Creates a dependency view of a system rather than evaluating one API or migration.",
        "use_when": [
            "The user wants to understand service dependencies, owners, call paths, or failure propagation.",
            "The task involves multiple services, queues, APIs, databases, or external systems.",
            "The output should be a dependency map with risks and evidence gaps.",
        ],
        "not_for": [
            "Designing one webhook receiver contract.",
            "Reviewing one OpenAPI spec for schema correctness.",
            "Auditing one database migration.",
        ],
        "preconditions": [
            "Service names, architecture notes, traces, logs, or repository evidence are available.",
            "The user wants system relationships rather than a single component fix.",
            "Owners, call directions, or data contracts can be identified or marked unknown.",
        ],
        "workflow": [
            "Identify services, data stores, queues, APIs, and external dependencies.",
            "Map upstream/downstream relationships and ownership.",
            "Record data contracts, critical paths, failure modes, and missing evidence.",
            "Highlight dependency risks and coordination points.",
            "Return a compact map and next evidence to collect.",
        ],
        "writing_rules": [
            "Do not invent dependency edges without evidence.",
            "Mark unknown owners or contracts explicitly.",
            "Keep the map operationally useful for planning or incident response.",
        ],
        "default_shape": [
            "Dependency edge",
            "Owner or contract",
            "Failure mode",
            "Evidence or follow-up",
        ],
    },
]


PROMPTS_BY_FILE = {
    "office_artifact_workflows_confusability.json": [
        {
            "id": "office_p1_pdf_layout_review",
            "family": "office_artifact_workflows",
            "gold_skill": "pdf-layout-reviewer",
            "closest_alternatives": ["pdf-ocr-extractor", "office-to-markdown-converter", "public-office-pdf-extraction", "public-pdf"],
            "prompt": "Please inspect `/workspace/fixtures/office_artifact_workflows/grant_application_packet.pdf` as a rendered PDF. I need page-by-page layout issues: cropped tables, broken headers, missing signature areas, and anything that would make the form hard to read. Do not just extract the fields.",
        },
        {
            "id": "office_p2_scanned_pdf_ocr",
            "family": "office_artifact_workflows",
            "gold_skill": "pdf-ocr-extractor",
            "closest_alternatives": ["pdf-layout-reviewer", "office-to-markdown-converter", "document-field-extractor"],
            "prompt": "Please recover the text from `/workspace/fixtures/office_artifact_workflows/scanned_receipts_packet.pdf`. It looks like image scans, so keep page numbers and mark uncertain OCR text instead of pretending every amount is reliable.",
        },
        {
            "id": "office_p3_docx_redline",
            "family": "office_artifact_workflows",
            "gold_skill": "docx-redline-editor",
            "closest_alternatives": ["office-to-markdown-converter", "document-rewriter", "public-docx", "public-office-docx-manipulation"],
            "prompt": "Please review `/workspace/fixtures/office_artifact_workflows/vendor_agreement_draft.docx` as a Word document and prepare redline-style edits with short reviewer comments. Preserve sections and explain any substantive change.",
        },
        {
            "id": "office_p4_formula_audit",
            "family": "office_artifact_workflows",
            "gold_skill": "spreadsheet-formula-auditor",
            "closest_alternatives": ["office-to-markdown-converter", "data-analysis-with-validation", "public-xlsx", "public-office-xlsx-manipulation"],
            "prompt": "Please check `/workspace/fixtures/office_artifact_workflows/pricing_model.xlsx` for calculation and assumption risks. I care about wrong cell links, mismatched copied ranges, embedded constants, and whether the summary tab traces back correctly.",
        },
        {
            "id": "office_p5_slide_visual_audit",
            "family": "office_artifact_workflows",
            "gold_skill": "slide-deck-visual-auditor",
            "closest_alternatives": ["office-to-markdown-converter", "pdf-layout-reviewer", "public-pptx", "public-office-ppt-visual"],
            "prompt": "Please review `/workspace/fixtures/office_artifact_workflows/thesis_proposal_deck.pptx` for presentation readiness. I need slide-level feedback on visual hierarchy, text overflow, alignment, theme consistency, and speaker-note fit.",
        },
        {
            "id": "office_p6_office_to_markdown",
            "family": "office_artifact_workflows",
            "gold_skill": "office-to-markdown-converter",
            "closest_alternatives": ["pdf-layout-reviewer", "docx-redline-editor", "document-converter"],
            "prompt": "Please convert `/workspace/fixtures/office_artifact_workflows/project_brief.docx` into clean Markdown for a repository. Preserve headings, tables, labels, and source traceability, but do not create tracked changes or a layout audit.",
        },
    ],
    "deployment_browser_qa_confusability.json": [
        {
            "id": "deploy_p1_playwright_flow_debug",
            "family": "deployment_browser_qa",
            "gold_skill": "playwright-flow-debugger",
            "closest_alternatives": ["visual-regression-checker", "accessibility-interaction-auditor", "public-playwright-interactive", "public-openai-playwright"],
            "prompt": "The checkout flow at `http://localhost:4173/checkout` fails after I click Apply coupon. Please reproduce the interaction with browser evidence, capture console or network clues, and identify why the flow breaks.",
        },
        {
            "id": "deploy_p2_visual_regression",
            "family": "deployment_browser_qa",
            "gold_skill": "visual-regression-checker",
            "closest_alternatives": ["playwright-flow-debugger", "accessibility-interaction-auditor", "public-openai-screenshot", "public-anthropic-webapp-testing"],
            "prompt": "Please compare the baseline and current screenshots for `/workspace/fixtures/deployment_browser_qa/pricing_page_desktop.png` and `/workspace/fixtures/deployment_browser_qa/pricing_page_mobile.png`. I need visual regressions like clipping, spacing shifts, text overflow, and contrast changes.",
        },
        {
            "id": "deploy_p3_accessibility_interaction",
            "family": "deployment_browser_qa",
            "gold_skill": "accessibility-interaction-auditor",
            "closest_alternatives": ["visual-regression-checker", "playwright-flow-debugger", "web-ui-tester", "public-anthropic-webapp-testing"],
            "prompt": "Please audit the account-settings modal for keyboard and screen-reader interaction. Focus on tab order, focus trapping, accessible names, ARIA state, and whether form errors are announced.",
        },
        {
            "id": "deploy_p4_build_log_triage",
            "family": "deployment_browser_qa",
            "gold_skill": "deployment-build-triager",
            "closest_alternatives": ["deployment-release-verifier", "playwright-flow-debugger", "web-performance-budget-checker"],
            "prompt": "The Netlify deploy for `/workspace/fixtures/deployment_browser_qa/build_log.txt` failed. Please inspect the build log and identify the likely root cause, missing env/config assumptions, and the smallest rerun sequence.",
        },
        {
            "id": "deploy_p5_release_verification",
            "family": "deployment_browser_qa",
            "gold_skill": "deployment-release-verifier",
            "closest_alternatives": ["deployment-build-triager", "visual-regression-checker", "public-netlify-deploy", "public-openai-vercel-deploy"],
            "prompt": "The production deploy is live at `https://example-release.netlify.app`. Please verify release readiness with URL smoke checks, version evidence, asset loading, critical routes, environment sanity, and rollback notes.",
        },
        {
            "id": "deploy_p6_performance_budget",
            "family": "deployment_browser_qa",
            "gold_skill": "web-performance-budget-checker",
            "closest_alternatives": ["visual-regression-checker", "deployment-release-verifier", "accessibility-interaction-auditor"],
            "prompt": "Please review `/workspace/fixtures/deployment_browser_qa/lighthouse_trace_summary.txt` against a mobile performance budget. I care about LCP, blocking scripts, network weight, image size, and which fixes matter most.",
        },
    ],
    "api_backend_design_confusability.json": [
        {
            "id": "api_p1_openapi_contract_review",
            "family": "api_backend_design",
            "gold_skill": "openapi-contract-reviewer",
            "closest_alternatives": ["external-api-integration-planner", "webhook-contract-planner", "architecture-boundary-reviewer"],
            "prompt": "Please review `/workspace/fixtures/api_backend_design/billing_openapi.yaml` as an API contract. I need endpoint-level issues around schemas, examples, status codes, auth behavior, pagination, and client compatibility.",
        },
        {
            "id": "api_p2_external_api_integration",
            "family": "api_backend_design",
            "gold_skill": "external-api-integration-planner",
            "closest_alternatives": ["openapi-contract-reviewer", "webhook-contract-planner", "service-dependency-mapper"],
            "prompt": "Please plan how our app should connect to the Acme Billing API. Cover authentication, endpoint choices, request/response mapping, provider throttling, recovery behavior, page-through results, secrets, and verification tests.",
        },
        {
            "id": "api_p3_webhook_contract",
            "family": "api_backend_design",
            "gold_skill": "webhook-contract-planner",
            "closest_alternatives": ["external-api-integration-planner", "openapi-contract-reviewer", "public-office-webhook-automation", "public-api-design-principles"],
            "prompt": "A payment provider will send event callbacks into our app. Please design the receiver behavior: which events to accept, how to validate the body, how to check signatures, how to handle duplicate deliveries, retry timing, ordering assumptions, and failed-message storage.",
        },
        {
            "id": "api_p4_architecture_boundary",
            "family": "api_backend_design",
            "gold_skill": "architecture-boundary-reviewer",
            "closest_alternatives": ["service-dependency-mapper", "openapi-contract-reviewer", "database-migration-risk-assessor"],
            "prompt": "Please review `/workspace/fixtures/api_backend_design/service_modules.md` for backend architecture boundaries. I care about module ownership, dependency direction, coupling, misplaced responsibilities, and a safe refactoring sequence.",
        },
        {
            "id": "api_p5_database_migration_risk",
            "family": "api_backend_design",
            "gold_skill": "database-migration-risk-assessor",
            "closest_alternatives": ["architecture-boundary-reviewer", "service-dependency-mapper", "public-office-database-sync", "public-architecture-patterns"],
            "prompt": "Please assess `/workspace/fixtures/api_backend_design/add_subscription_status_migration.sql` before production rollout. I need locking risk, backfill plan, compatibility with old app versions, rollback path, and verification queries.",
        },
        {
            "id": "api_p6_service_dependency_map",
            "family": "api_backend_design",
            "gold_skill": "service-dependency-mapper",
            "closest_alternatives": ["architecture-boundary-reviewer", "external-api-integration-planner", "public-architecture-patterns", "public-api-design-principles"],
            "prompt": "Please trace how the billing, notification, account, and analytics services rely on each other using `/workspace/fixtures/api_backend_design/service_trace_notes.md`. Include call direction, responsible teams, shared data promises, ways failures propagate, and evidence gaps.",
        },
    ],
}


FIXTURES = {
    "office_artifact_workflows/grant_application_packet.pdf": "Pseudo fixture: grant application PDF with tables, signature boxes, and appendix pages for layout review.\n",
    "office_artifact_workflows/scanned_receipts_packet.pdf": "Pseudo fixture: scanned receipt packet requiring OCR with uncertain totals and vendor names.\n",
    "office_artifact_workflows/vendor_agreement_draft.docx": "Pseudo fixture: Word agreement draft with sections, comments, and clauses needing redline review.\n",
    "office_artifact_workflows/pricing_model.xlsx": "Pseudo fixture: workbook with assumptions, summary tab, lookup formulas, and copied ranges.\n",
    "office_artifact_workflows/thesis_proposal_deck.pptx": "Pseudo fixture: proposal deck with dense slides, speaker notes, charts, and inconsistent theme use.\n",
    "office_artifact_workflows/project_brief.docx": "Pseudo fixture: Word project brief with headings, tables, and labeled fields for Markdown conversion.\n",
    "deployment_browser_qa/pricing_page_desktop.png": "Pseudo fixture placeholder for desktop screenshot comparison.\n",
    "deployment_browser_qa/pricing_page_mobile.png": "Pseudo fixture placeholder for mobile screenshot comparison.\n",
    "deployment_browser_qa/build_log.txt": "10:41:21 PM: build command npm run build\n10:41:33 PM: Error: Missing required environment variable VITE_API_BASE_URL\n10:41:34 PM: Build failed during stage 'building site'.\n",
    "deployment_browser_qa/lighthouse_trace_summary.txt": "Mobile LCP 4.8s; total JS 890KB; render-blocking script app.bundle.js; hero image 1.9MB; TBT 460ms.\n",
    "api_backend_design/billing_openapi.yaml": "openapi: 3.0.3\npaths:\n  /invoices:\n    get:\n      responses:\n        '200': {description: invoice list}\n",
    "api_backend_design/service_modules.md": "# Service modules\nBilling imports account models directly. Notifications calls billing and analytics. Analytics reads billing tables nightly.\n",
    "api_backend_design/add_subscription_status_migration.sql": "ALTER TABLE subscriptions ADD COLUMN status TEXT NOT NULL DEFAULT 'active';\nUPDATE subscriptions SET status = 'active' WHERE status IS NULL;\n",
    "api_backend_design/service_trace_notes.md": "billing -> account: customer lookup\nbilling -> notification: invoice email\nnotification -> analytics: event emit\nanalytics -> billing_db: nightly read\n",
}


def render_skill(skill: dict[str, object]) -> str:
    return SKILL_TEMPLATE.format(
        name=skill["name"],
        title=skill["title"],
        description_json=json.dumps(skill["description"]),
        overview=skill["overview"],
        use_when=bullets(skill["use_when"]),  # type: ignore[arg-type]
        not_for=bullets(skill["not_for"]),  # type: ignore[arg-type]
        preconditions=bullets(skill["preconditions"]),  # type: ignore[arg-type]
        workflow=numbered(skill["workflow"]),  # type: ignore[arg-type]
        writing_rules=bullets(skill["writing_rules"]),  # type: ignore[arg-type]
        default_shape=bullets(skill["default_shape"]),  # type: ignore[arg-type]
    )


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    skills_root = repo_root / "skills"
    prompts_root = repo_root / "prompts"
    fixtures_root = repo_root / "fixtures"

    families = sorted({str(skill["family"]) for skill in SKILLS})
    for family in families:
        family_dir = skills_root / family
        if family_dir.exists():
            shutil.rmtree(family_dir)
        family_dir.mkdir(parents=True)

    for skill in SKILLS:
        skill_dir = skills_root / str(skill["family"]) / str(skill["name"])
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(render_skill(skill), encoding="utf-8")

    prompts_root.mkdir(parents=True, exist_ok=True)
    for file_name, prompts in PROMPTS_BY_FILE.items():
        (prompts_root / file_name).write_text(json.dumps(prompts, indent=2) + "\n", encoding="utf-8")

    for relative_path, content in FIXTURES.items():
        path = fixtures_root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    print(f"Generated {len(SKILLS)} core v2 skills across {len(families)} families.")
    print(f"Generated {sum(len(prompts) for prompts in PROMPTS_BY_FILE.values())} prompts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
