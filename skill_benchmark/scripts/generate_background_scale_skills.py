#!/usr/bin/env python3

from __future__ import annotations

import shutil
from pathlib import Path


BACKGROUND_SKILLS = [
    {
        "name": "code-documentation-writer",
        "description": "Writes developer documentation for code modules, APIs, configuration, or workflows so future maintainers can understand usage and constraints.",
        "use": "The user wants documentation for existing code rather than a code review or implementation change.",
        "output": "Developer-facing documentation with examples, assumptions, and maintenance notes.",
    },
    {
        "name": "debugging-root-cause-helper",
        "description": "Investigates a reported software bug by tracing symptoms, reproduction evidence, recent changes, and likely root causes before proposing fixes.",
        "use": "The user has a bug symptom and wants cause analysis rather than a review of possible risks.",
        "output": "Root-cause hypothesis, evidence, reproduction notes, and targeted fix direction.",
    },
    {
        "name": "refactor-planner",
        "description": "Plans a code refactor by identifying boundaries, dependencies, migration steps, risks, and verification needed before editing.",
        "use": "The user wants a refactoring plan rather than an immediate code review or bug fix.",
        "output": "Refactor plan with sequence, risk controls, and test strategy.",
    },
    {
        "name": "test-case-generator",
        "description": "Creates unit, integration, or end-to-end test cases for specified behavior, edge cases, regressions, or acceptance criteria.",
        "use": "The user needs tests designed or expanded for known behavior.",
        "output": "Test cases, scenarios, fixtures, and expected assertions.",
    },
    {
        "name": "version-control-helper",
        "description": "Helps with Git workflow decisions such as branching, merging, rebasing, conflict interpretation, and safe change organization.",
        "use": "The user asks about managing repository history or branches rather than reviewing code content.",
        "output": "Git workflow guidance and safe command sequence.",
    },
    {
        "name": "git-commit-writer",
        "description": "Writes concise commit messages from staged changes, diffs, or implementation summaries, including type, scope, and breaking-change notes when relevant.",
        "use": "The user wants a commit message for completed changes.",
        "output": "Commit subject and optional body.",
    },
    {
        "name": "pr-description-writer",
        "description": "Writes pull request descriptions from branch changes, covering what changed, why, how it was tested, and reviewer notes.",
        "use": "The user wants PR description text, not PR review findings.",
        "output": "Pull request description with summary, details, tests, and risks.",
    },
    {
        "name": "api-design-reviewer",
        "description": "Reviews REST, GraphQL, or event API designs for resource shape, naming, error behavior, versioning, and client usability.",
        "use": "The user wants API design feedback rather than implementation debugging.",
        "output": "API design findings and recommended design adjustments.",
    },
    {
        "name": "api-integration-planner",
        "description": "Plans how to integrate a third-party API by mapping auth, endpoints, rate limits, data mapping, retries, and failure handling.",
        "use": "The user wants an integration plan for an external API.",
        "output": "Integration plan with calls, data flow, edge cases, and verification.",
    },
    {
        "name": "openapi-contract-tester",
        "description": "Designs API contract tests from OpenAPI or endpoint specifications, covering status codes, schema validation, and edge cases.",
        "use": "The user wants tests against an API contract.",
        "output": "Contract test scenarios and expected assertions.",
    },
    {
        "name": "graphql-schema-designer",
        "description": "Designs or reviews GraphQL schemas, queries, mutations, field naming, resolver boundaries, and pagination shapes.",
        "use": "The user asks for GraphQL-specific schema design support.",
        "output": "GraphQL schema recommendations and operation shapes.",
    },
    {
        "name": "webhook-setup-planner",
        "description": "Plans webhook integrations including event selection, signature verification, retry behavior, idempotency, and failure handling.",
        "use": "The user wants to configure or design webhook handling.",
        "output": "Webhook setup plan and validation checklist.",
    },
    {
        "name": "database-schema-designer",
        "description": "Designs normalized database schemas, tables, relationships, constraints, and indexes for a specified application model.",
        "use": "The user wants database structure design rather than data analysis.",
        "output": "Schema proposal with tables, fields, constraints, and rationale.",
    },
    {
        "name": "migration-risk-auditor",
        "description": "Reviews database migrations for locking hazards, data loss, missing rollbacks, backfill risk, and deployment ordering problems.",
        "use": "The user wants to assess a schema migration before production.",
        "output": "Migration risk findings and safer rollout plan.",
    },
    {
        "name": "query-optimizer",
        "description": "Improves slow SQL or database queries by inspecting joins, filters, indexes, query plans, and data-shape assumptions.",
        "use": "The user has a slow or expensive query and wants optimization guidance.",
        "output": "Optimized query direction and indexing or plan notes.",
    },
    {
        "name": "database-backup-planner",
        "description": "Plans database backup, restore, retention, verification, and recovery procedures for operational resilience.",
        "use": "The user wants backup or recovery planning.",
        "output": "Backup and restore plan with verification checks.",
    },
    {
        "name": "seed-data-generator",
        "description": "Creates realistic seed data or test fixtures for development, demos, migrations, or QA environments.",
        "use": "The user wants generated data for testing or demos.",
        "output": "Seed-data plan or generated fixture content.",
    },
    {
        "name": "ci-cd-pipeline-builder",
        "description": "Designs CI/CD pipelines for build, test, lint, artifact creation, deployment gates, and environment promotion.",
        "use": "The user wants pipeline setup rather than debugging a specific failing run.",
        "output": "Pipeline design and workflow steps.",
    },
    {
        "name": "docker-compose-configurator",
        "description": "Creates or reviews Docker Compose configurations for local multi-service applications, dependencies, volumes, and networks.",
        "use": "The user asks for Docker Compose setup or configuration review.",
        "output": "Compose configuration guidance and service wiring.",
    },
    {
        "name": "cloud-monitoring-configurer",
        "description": "Configures cloud or service monitoring, alerts, dashboards, thresholds, and ownership routing for operational visibility.",
        "use": "The user wants monitoring setup rather than interpreting an existing metric snapshot.",
        "output": "Monitoring configuration plan and alert rules.",
    },
    {
        "name": "infrastructure-as-code-planner",
        "description": "Plans Terraform, Pulumi, or CloudFormation infrastructure changes with resources, dependencies, state risks, and rollout order.",
        "use": "The user wants infrastructure-as-code planning.",
        "output": "IaC plan with resources, risks, and deployment checks.",
    },
    {
        "name": "kubernetes-deployment-helper",
        "description": "Helps deploy or adjust Kubernetes workloads, services, ingress, config maps, secrets, probes, and rollout settings.",
        "use": "The user asks for Kubernetes deployment support.",
        "output": "Kubernetes deployment plan or manifest guidance.",
    },
    {
        "name": "deployment-rollback-planner",
        "description": "Plans safe rollback or recovery steps for a failed deployment, including data compatibility, feature flags, and verification.",
        "use": "The user wants rollback planning rather than release-note writing.",
        "output": "Rollback plan with triggers, steps, and checks.",
    },
    {
        "name": "environment-config-auditor",
        "description": "Reviews environment variables, config files, secrets references, feature flags, and deployment settings for consistency and risk.",
        "use": "The user wants configuration audit rather than secret scanning only.",
        "output": "Configuration findings and cleanup recommendations.",
    },
    {
        "name": "calendar-conflict-checker",
        "description": "Checks a schedule or calendar plan for conflicts, impossible timing, missing travel buffers, and priority clashes.",
        "use": "The user wants conflict detection in a schedule.",
        "output": "Conflict list and adjustment suggestions.",
    },
    {
        "name": "meeting-scheduler",
        "description": "Finds or proposes meeting times across participants, constraints, time zones, and availability windows.",
        "use": "The user wants to schedule a meeting rather than write an agenda or summary.",
        "output": "Candidate meeting times and scheduling message.",
    },
    {
        "name": "deadline-reminder-planner",
        "description": "Turns upcoming due dates into reminders, checkpoints, and escalation points so work is not missed.",
        "use": "The user wants reminder structure around deadlines.",
        "output": "Reminder plan with timing and priority.",
    },
    {
        "name": "file-organiser",
        "description": "Organizes files or folders into a cleaner structure based on project, date, topic, type, or workflow purpose.",
        "use": "The user wants file organization rather than document content analysis.",
        "output": "Folder structure and move/rename plan.",
    },
    {
        "name": "file-renamer",
        "description": "Creates consistent file names from messy file lists using date, source, project, version, or content cues.",
        "use": "The user wants naming cleanup rather than moving or archiving files.",
        "output": "Rename mapping and naming convention.",
    },
    {
        "name": "duplicate-file-finder",
        "description": "Identifies likely duplicate or redundant files using filenames, metadata, checksums, or content similarity cues.",
        "use": "The user wants duplicate detection.",
        "output": "Duplicate groups and safe cleanup advice.",
    },
    {
        "name": "archive-preparer",
        "description": "Prepares completed files, notes, or project materials for archive with retention, naming, and retrieval considerations.",
        "use": "The user wants archival organization.",
        "output": "Archive plan and final checklist.",
    },
    {
        "name": "note-tagger",
        "description": "Assigns tags, labels, or categories to notes so they can be searched, grouped, or reviewed later.",
        "use": "The user wants note classification rather than summarization.",
        "output": "Tags and classification rationale.",
    },
    {
        "name": "note-linker",
        "description": "Connects related notes, concepts, source claims, and project ideas into links or cross-reference suggestions.",
        "use": "The user wants relationships between notes.",
        "output": "Suggested note links and connection rationale.",
    },
    {
        "name": "flashcard-generator",
        "description": "Turns learning material into question-answer flashcards for spaced repetition or exam preparation.",
        "use": "The user wants study cards rather than a summary or citation notes.",
        "output": "Flashcards with prompts and answers.",
    },
    {
        "name": "decision-matrix-builder",
        "description": "Builds a weighted decision matrix to compare options against criteria, tradeoffs, and uncertainty.",
        "use": "The user wants structured decision support.",
        "output": "Decision matrix and recommendation caveats.",
    },
    {
        "name": "priority-sorter",
        "description": "Sorts tasks, ideas, or options by urgency, impact, effort, dependency, or risk.",
        "use": "The user wants prioritization rather than scheduling.",
        "output": "Prioritized list with reasoning.",
    },
    {
        "name": "budget-planner",
        "description": "Creates a budget plan with income, costs, categories, constraints, and variance-monitoring points.",
        "use": "The user wants budgeting rather than expense categorization.",
        "output": "Budget structure and tracking plan.",
    },
    {
        "name": "expense-categoriser",
        "description": "Classifies expenses by category, project, department, or tax treatment using transaction descriptions and rules.",
        "use": "The user wants expense classification.",
        "output": "Categorized expenses and uncertain items.",
    },
    {
        "name": "receipt-extractor",
        "description": "Extracts merchant, date, totals, taxes, line items, and payment details from receipts into reusable records.",
        "use": "The user wants receipt fields rather than invoice processing or document summary.",
        "output": "Structured receipt fields.",
    },
    {
        "name": "invoice-payment-checker",
        "description": "Checks invoices for due dates, totals, payment terms, missing fields, duplicate billing, and action required.",
        "use": "The user wants invoice payment readiness or follow-up.",
        "output": "Invoice payment status and next actions.",
    },
    {
        "name": "financial-model-builder",
        "description": "Builds financial projections, assumptions, scenarios, revenue drivers, costs, and sensitivity analysis.",
        "use": "The user wants a financial model rather than a general spreadsheet report.",
        "output": "Model structure, assumptions, and scenario outputs.",
    },
    {
        "name": "financial-report-writer",
        "description": "Turns financial data into balance, cash-flow, performance, or variance reports for stakeholders.",
        "use": "The user wants finance-specific reporting.",
        "output": "Financial report with key figures and caveats.",
    },
    {
        "name": "variance-analysis-helper",
        "description": "Compares planned versus actual figures and explains major variances, drivers, and follow-up questions.",
        "use": "The user wants variance interpretation.",
        "output": "Variance analysis with likely drivers.",
    },
    {
        "name": "market-opportunity-assessor",
        "description": "Assesses a market opportunity using customer segment, problem severity, competition, timing, and measurable next steps.",
        "use": "The user wants market evaluation rather than a business execution plan.",
        "output": "Opportunity assessment and assumptions.",
    },
    {
        "name": "business-plan-builder",
        "description": "Turns a business idea into an execution plan with assumptions, target users, milestones, risks, and KPIs.",
        "use": "The user wants a business plan.",
        "output": "Business plan outline with assumptions and metrics.",
    },
    {
        "name": "competitive-battlecard-builder",
        "description": "Builds competitive positioning notes with strengths, weaknesses, objections, differentiators, and sales talk tracks.",
        "use": "The user wants competitive battlecard material.",
        "output": "Battlecard with positioning and objection handling.",
    },
    {
        "name": "contract-risk-reviewer",
        "description": "Reviews contracts for risky clauses, obligations, ambiguous terms, renewal traps, liability, and negotiation points.",
        "use": "The user wants contract risk analysis.",
        "output": "Contract risk findings and questions.",
    },
    {
        "name": "clause-obligation-extractor",
        "description": "Extracts obligations, deadlines, notice requirements, restrictions, parties, and conditions from legal or policy text.",
        "use": "The user wants structured obligations rather than contract risk advice.",
        "output": "Obligation table with parties and deadlines.",
    },
    {
        "name": "license-compatibility-checker",
        "description": "Reviews open-source license compatibility, attribution requirements, redistribution constraints, and policy obligations.",
        "use": "The user wants license-risk assessment.",
        "output": "License compatibility notes and required actions.",
    },
    {
        "name": "compliance-checklist-builder",
        "description": "Creates practical compliance checklists for standards, policies, regulations, audits, or internal governance requirements.",
        "use": "The user wants a checklist for compliance work.",
        "output": "Checklist organized by requirement area.",
    },
    {
        "name": "privacy-policy-drafter",
        "description": "Drafts privacy-policy text based on data collection, retention, sharing, user rights, and service behavior.",
        "use": "The user wants policy text rather than privacy-risk review.",
        "output": "Draft privacy policy section or full policy outline.",
    },
    {
        "name": "terms-of-service-drafter",
        "description": "Drafts terms-of-service text covering acceptable use, account terms, liability, termination, and user obligations.",
        "use": "The user wants terms text, not a legal risk review.",
        "output": "Draft ToS section or full outline.",
    },
    {
        "name": "policy-compliance-checker",
        "description": "Checks whether a workflow, document, or proposed action appears to comply with a given internal policy or rule set.",
        "use": "The user wants compliance checking against a policy.",
        "output": "Compliance status, gaps, and evidence.",
    },
    {
        "name": "procurement-risk-summariser",
        "description": "Summarises procurement or vendor risk from proposals, contracts, security notes, pricing, and operational dependencies.",
        "use": "The user wants vendor or procurement risk summarized.",
        "output": "Procurement risk summary and follow-up questions.",
    },
    {
        "name": "keyword-researcher",
        "description": "Finds and groups SEO or advertising keywords by intent, topic, competition, and content opportunity.",
        "use": "The user wants keyword research.",
        "output": "Keyword clusters and recommended targets.",
    },
    {
        "name": "seo-metadata-checker",
        "description": "Reviews page titles, meta descriptions, headings, URLs, and structured snippets for search visibility and clarity.",
        "use": "The user wants SEO metadata checking rather than general page testing.",
        "output": "SEO metadata findings and suggested revisions.",
    },
    {
        "name": "landing-page-copy-reviewer",
        "description": "Reviews landing-page copy for clarity, audience fit, conversion friction, proof, positioning, and call-to-action quality.",
        "use": "The user wants marketing copy review.",
        "output": "Copy findings and suggested improvements.",
    },
    {
        "name": "content-strategy-builder",
        "description": "Builds content strategy around audience, topics, channels, cadence, positioning, and measurable goals.",
        "use": "The user wants a strategy, not one piece of content.",
        "output": "Content plan with themes and cadence.",
    },
    {
        "name": "social-post-planner",
        "description": "Plans social media posts, hooks, captions, schedule, platform fit, and reuse from source material.",
        "use": "The user wants social content planning.",
        "output": "Post plan with captions and timing.",
    },
    {
        "name": "customer-feedback-analyser",
        "description": "Analyzes customer comments, support notes, reviews, surveys, or NPS feedback for themes, severity, and product signals.",
        "use": "The user wants qualitative customer feedback analysis.",
        "output": "Theme summary, evidence, and recommended follow-up.",
    },
    {
        "name": "churn-risk-analyser",
        "description": "Identifies accounts or users at risk of churn using usage signals, feedback, support history, and renewal context.",
        "use": "The user wants churn-risk assessment.",
        "output": "Churn risk levels and retention actions.",
    },
    {
        "name": "support-ticket-triager",
        "description": "Classifies and prioritizes support tickets by issue type, urgency, affected user, severity, and routing owner.",
        "use": "The user wants ticket triage rather than drafting a support reply.",
        "output": "Ticket labels, priorities, and routing notes.",
    },
    {
        "name": "knowledge-base-article-writer",
        "description": "Writes help-center or FAQ articles from product behavior, support patterns, troubleshooting steps, or policy details.",
        "use": "The user wants self-serve support documentation.",
        "output": "Knowledge-base article with steps and caveats.",
    },
    {
        "name": "sales-email-sequence-writer",
        "description": "Designs multi-touch sales email sequences with targeting, value proposition, follow-up logic, and objection handling.",
        "use": "The user wants outbound sales email sequence planning.",
        "output": "Email sequence with timing and variants.",
    },
    {
        "name": "crm-data-enricher",
        "description": "Enriches CRM records with firmographic, contact, industry, lifecycle, and account-fit information from provided sources.",
        "use": "The user wants CRM data enhancement.",
        "output": "Enriched fields with source notes and uncertainty.",
    },
    {
        "name": "proposal-drafter",
        "description": "Drafts tailored proposals, RFP responses, or project pitches using requirements, constraints, differentiators, and pricing context.",
        "use": "The user wants proposal text.",
        "output": "Proposal draft or response outline.",
    },
    {
        "name": "context-compressor",
        "description": "Compresses long conversation, document, or project context into a smaller working brief while preserving decisions and constraints.",
        "use": "The user wants context reduced for later use.",
        "output": "Compact context brief with preserved constraints.",
    },
    {
        "name": "context-ranker",
        "description": "Ranks candidate context items by relevance, recency, reliability, and usefulness for a specific downstream task.",
        "use": "The user wants context prioritization rather than retrieval or summarization.",
        "output": "Ranked context list with reasons.",
    },
    {
        "name": "context-retriever",
        "description": "Retrieves relevant notes, documents, memories, or knowledge snippets for a given question or task.",
        "use": "The user wants candidate context fetched from a collection.",
        "output": "Retrieved context snippets with relevance notes.",
    },
    {
        "name": "rag-failure-diagnoser",
        "description": "Diagnoses retrieval-augmented generation failures such as missing evidence, wrong chunking, stale context, or structural query mismatch.",
        "use": "The user wants to understand why a RAG answer failed.",
        "output": "Failure classification and architecture fix direction.",
    },
    {
        "name": "knowledge-graph-builder",
        "description": "Builds entities, relationships, and typed links from unstructured notes, documents, or domain material.",
        "use": "The user wants graph-like knowledge organization.",
        "output": "Entity-relation map and schema notes.",
    },
    {
        "name": "prompt-refiner",
        "description": "Improves prompts by clarifying goal, context, constraints, output shape, examples, and evaluation criteria.",
        "use": "The user wants a better prompt rather than a task answer.",
        "output": "Refined prompt and rationale.",
    },
    {
        "name": "agent-handoff-orchestrator",
        "description": "Plans handoff between agents or people by defining task boundaries, inputs, outputs, responsibilities, and completion criteria.",
        "use": "The user wants multi-agent or multi-person task handoff.",
        "output": "Handoff plan and responsibility map.",
    },
    {
        "name": "subagent-task-planner",
        "description": "Breaks a complex task into subagent-sized work packages with instructions, inputs, dependencies, and expected outputs.",
        "use": "The user wants to delegate pieces of work to subagents.",
        "output": "Subagent task plan.",
    },
    {
        "name": "agent-eval-coverage-auditor",
        "description": "Reviews whether an agent evaluation suite covers realistic tasks, edge cases, failure modes, and success metrics.",
        "use": "The user wants to audit agent evaluation coverage.",
        "output": "Coverage gaps and evaluation improvements.",
    },
    {
        "name": "tool-use-coach",
        "description": "Improves an agent's tool-use strategy by identifying when tools should be called, avoided, sequenced, or verified.",
        "use": "The user wants guidance on tool-use behavior.",
        "output": "Tool-use strategy recommendations.",
    },
    {
        "name": "slide-outline-builder",
        "description": "Turns a topic, report, or research plan into a slide-by-slide outline with purpose, flow, and key visual ideas.",
        "use": "The user wants a deck outline rather than a full presentation artifact.",
        "output": "Slide outline with titles, purpose, and visual cue.",
    },
    {
        "name": "speaker-notes-writer",
        "description": "Writes speaker notes or oral delivery script for slides, focusing on verbal flow, timing, and explanation.",
        "use": "The user wants notes for presenting slides.",
        "output": "Speaker notes organized by slide.",
    },
    {
        "name": "deck-template-applier",
        "description": "Applies a visual deck template, brand style, or layout system to existing slide content while preserving message order.",
        "use": "The user wants style/template application rather than content planning.",
        "output": "Template application plan or revised slide structure.",
    },
    {
        "name": "chart-caption-writer",
        "description": "Writes clear captions, takeaway statements, and annotations for charts, figures, dashboards, or tables.",
        "use": "The user wants explanatory text for visual data.",
        "output": "Chart captions and takeaway annotations.",
    },
]


TEMPLATE = """---
name: {name}
description: {description}
---

# {title}

Background scale skill used to create realistic retrieval pressure in the benchmark.

## Dependency Profile

{dependency_profile}

## External Dependencies To Preserve

{external_dependencies}

## Resource And Structure Signals

{resource_signals}

## Use when

- {use}
- {precondition}
- The task needs this specific procedure rather than a neighboring confusable skill.
- The output should match the expected artifact below.

## Not for

- Replacing a gold-label core benchmark skill when that core skill is procedurally more specific.
- Broad internal routing across unrelated domains.
- Acting on missing context without asking for or identifying the needed input.

## Workflow

1. Identify the user's intended input and desired artifact.
2. Confirm this skill's procedure is the best fit rather than a neighboring skill.
3. Extract the relevant constraints, evidence, or requirements.
4. Produce the expected output in a compact and reusable form.
5. State uncertainty or required follow-up when the input is incomplete.

## Expected output

{output}

## Writing rules

- Keep the result focused on this skill's procedural role.
- Do not silently switch to a more specific benchmark core skill.
- Preserve important caveats and source limits.
"""


def titleize(name: str) -> str:
    return " ".join(part.capitalize() for part in name.split("-"))


DOMAIN_CLUSTERS = [
    {
        "prefix": "contract",
        "domain": "contract operations",
        "input": "contract text, amendment notes, renewal terms, obligation logs",
        "dependencies": ["contract document", "party names", "clause references", "effective dates"],
        "signals": ["clauses", "obligations", "deadlines", "legal risk", "redlines"],
    },
    {
        "prefix": "vendor",
        "domain": "vendor and procurement review",
        "input": "vendor proposal, security questionnaire, pricing sheet, contract summary",
        "dependencies": ["vendor profile", "pricing document", "security answers", "procurement criteria"],
        "signals": ["vendor risk", "pricing", "security controls", "service levels", "procurement stage"],
    },
    {
        "prefix": "crm",
        "domain": "CRM and sales operations",
        "input": "CRM records, account notes, opportunity fields, email history",
        "dependencies": ["CRM export", "account stage", "contact fields", "activity history"],
        "signals": ["accounts", "opportunities", "pipeline", "lead scoring", "contacts"],
    },
    {
        "prefix": "support",
        "domain": "customer support operations",
        "input": "support tickets, chat transcripts, issue labels, customer history",
        "dependencies": ["ticket queue", "customer context", "product area", "severity policy"],
        "signals": ["tickets", "severity", "routing", "resolution", "customer impact"],
    },
    {
        "prefix": "research",
        "domain": "research and source review",
        "input": "papers, reports, source notes, citation metadata",
        "dependencies": ["source text", "citation metadata", "method section", "evidence snippets"],
        "signals": ["claims", "methods", "citations", "related work", "evidence"],
    },
    {
        "prefix": "dataset",
        "domain": "dataset and analytics preparation",
        "input": "CSV files, data dictionary, metric definitions, quality notes",
        "dependencies": ["dataset file", "schema", "metric definitions", "sampling notes"],
        "signals": ["columns", "rows", "quality checks", "metrics", "analysis"],
    },
    {
        "prefix": "dashboard",
        "domain": "dashboard and metric reporting",
        "input": "dashboard screenshots, metric tables, alert notes, KPI definitions",
        "dependencies": ["dashboard export", "metric glossary", "time window", "owner notes"],
        "signals": ["charts", "KPIs", "alerts", "thresholds", "trend lines"],
    },
    {
        "prefix": "incident",
        "domain": "incident and reliability operations",
        "input": "incident timeline, logs, alerts, postmortem notes",
        "dependencies": ["timeline", "service logs", "alert history", "owner map"],
        "signals": ["outage", "timeline", "root cause", "mitigation", "follow-up actions"],
    },
    {
        "prefix": "security",
        "domain": "application security operations",
        "input": "repository files, threat notes, scan findings, architecture description",
        "dependencies": ["codebase", "architecture context", "security findings", "asset list"],
        "signals": ["threats", "vulnerabilities", "controls", "assets", "trust boundaries"],
    },
    {
        "prefix": "web",
        "domain": "web automation and QA",
        "input": "web page, browser state, test flow, screenshot evidence",
        "dependencies": ["web target", "browser runtime", "test data", "screenshot evidence"],
        "signals": ["DOM", "forms", "screenshots", "interactions", "accessibility"],
    },
    {
        "prefix": "repo",
        "domain": "repository and engineering workflow",
        "input": "pull request, diff, CI logs, issue description",
        "dependencies": ["repository diff", "test output", "issue context", "review policy"],
        "signals": ["diffs", "tests", "CI", "reviews", "release notes"],
    },
    {
        "prefix": "docs",
        "domain": "document operations",
        "input": "PDF, DOCX, Markdown file, policy draft, extracted text",
        "dependencies": ["document file", "layout evidence", "source text", "format target"],
        "signals": ["pages", "sections", "formatting", "fields", "summaries"],
    },
    {
        "prefix": "meeting",
        "domain": "meeting and planning operations",
        "input": "meeting transcript, agenda notes, calendar constraints, action list",
        "dependencies": ["meeting notes", "participant list", "calendar window", "action owners"],
        "signals": ["agenda", "decisions", "actions", "owners", "timelines"],
    },
    {
        "prefix": "email",
        "domain": "email and messaging operations",
        "input": "draft email, message thread, recipient context, tone constraints",
        "dependencies": ["message thread", "recipient relationship", "tone target", "requested action"],
        "signals": ["reply", "tone", "commitment", "recipient", "follow-up"],
    },
    {
        "prefix": "agent",
        "domain": "agent and skill operations",
        "input": "agent traces, tool specs, skill cards, evaluation notes",
        "dependencies": ["agent trace", "skill library", "tool definitions", "evaluation criteria"],
        "signals": ["skills", "tools", "routing", "traces", "evaluation"],
    },
]


ADDITIONAL_DOMAIN_CLUSTERS = [
    {
        "prefix": "finance",
        "domain": "finance and accounting operations",
        "input": "financial report, budget sheet, invoice set, forecast model",
        "dependencies": ["financial data", "accounting period", "chart of accounts", "assumption notes"],
        "signals": ["budget", "variance", "forecast", "invoice", "cash flow"],
    },
    {
        "prefix": "legal",
        "domain": "legal and policy operations",
        "input": "policy text, legal memo, contract clause, compliance question",
        "dependencies": ["legal text", "jurisdiction note", "policy version", "review purpose"],
        "signals": ["clauses", "policy", "obligations", "compliance", "review notes"],
    },
    {
        "prefix": "hr",
        "domain": "human resources operations",
        "input": "candidate notes, performance feedback, role description, HR policy",
        "dependencies": ["role profile", "employee context", "policy document", "feedback records"],
        "signals": ["candidates", "feedback", "roles", "policy", "performance"],
    },
    {
        "prefix": "recruiting",
        "domain": "recruiting pipeline operations",
        "input": "resume, interview notes, job criteria, candidate comparison table",
        "dependencies": ["resume file", "job criteria", "interview notes", "candidate stage"],
        "signals": ["screening", "interviews", "candidates", "criteria", "shortlist"],
    },
    {
        "prefix": "course",
        "domain": "course and learning operations",
        "input": "lecture notes, assignment brief, rubric, study material",
        "dependencies": ["course material", "rubric", "deadline", "learning objective"],
        "signals": ["assignment", "rubric", "study", "lecture", "feedback"],
    },
    {
        "prefix": "thesis",
        "domain": "thesis research operations",
        "input": "thesis notes, supervisor feedback, proposal draft, experiment log",
        "dependencies": ["research question", "supervisor note", "method plan", "literature notes"],
        "signals": ["research question", "methodology", "proposal", "evaluation", "timeline"],
    },
    {
        "prefix": "lab",
        "domain": "laboratory and experiment operations",
        "input": "experiment protocol, measurement table, lab notes, result log",
        "dependencies": ["protocol", "measurement data", "instrument notes", "safety constraints"],
        "signals": ["protocol", "measurements", "samples", "results", "controls"],
    },
    {
        "prefix": "medical-admin",
        "domain": "medical administration operations",
        "input": "appointment note, referral text, intake form, clinic instruction",
        "dependencies": ["patient-provided note", "appointment details", "clinic policy", "form fields"],
        "signals": ["appointments", "referrals", "intake", "forms", "follow-up"],
    },
    {
        "prefix": "travel",
        "domain": "travel planning operations",
        "input": "itinerary, booking email, visa note, travel constraint list",
        "dependencies": ["destination", "dates", "booking details", "traveler constraints"],
        "signals": ["itinerary", "booking", "visa", "schedule", "travel risk"],
    },
    {
        "prefix": "events",
        "domain": "event planning operations",
        "input": "event brief, attendee list, venue note, run sheet",
        "dependencies": ["event brief", "attendee list", "venue constraints", "run sheet"],
        "signals": ["attendees", "venue", "agenda", "logistics", "run sheet"],
    },
    {
        "prefix": "product",
        "domain": "product management operations",
        "input": "feature brief, roadmap item, user feedback, acceptance criteria",
        "dependencies": ["feature brief", "user feedback", "roadmap context", "acceptance criteria"],
        "signals": ["features", "roadmap", "users", "acceptance criteria", "priorities"],
    },
    {
        "prefix": "ux",
        "domain": "UX research and design operations",
        "input": "user interview notes, usability findings, design brief, prototype feedback",
        "dependencies": ["research notes", "participant context", "prototype", "design goals"],
        "signals": ["users", "usability", "prototype", "findings", "design constraints"],
    },
    {
        "prefix": "analytics",
        "domain": "analytics and experimentation operations",
        "input": "experiment result, metric table, cohort data, analytics request",
        "dependencies": ["metric definitions", "experiment design", "cohort data", "analysis window"],
        "signals": ["experiments", "cohorts", "metrics", "significance", "segments"],
    },
    {
        "prefix": "ml",
        "domain": "machine learning operations",
        "input": "model card, training log, evaluation table, dataset note",
        "dependencies": ["model artifact", "dataset split", "training config", "evaluation metric"],
        "signals": ["model", "dataset", "training", "evaluation", "drift"],
    },
    {
        "prefix": "cloud",
        "domain": "cloud infrastructure operations",
        "input": "cloud config, resource inventory, deployment note, cost report",
        "dependencies": ["cloud account", "resource inventory", "deployment config", "cost data"],
        "signals": ["resources", "regions", "cost", "deployment", "permissions"],
    },
    {
        "prefix": "k8s",
        "domain": "Kubernetes platform operations",
        "input": "manifest, pod log, deployment event, cluster configuration",
        "dependencies": ["cluster context", "manifest", "pod logs", "namespace"],
        "signals": ["pods", "services", "ingress", "rollouts", "resources"],
    },
    {
        "prefix": "devops",
        "domain": "DevOps pipeline operations",
        "input": "pipeline log, build script, deploy config, release checklist",
        "dependencies": ["CI logs", "build config", "environment variables", "release target"],
        "signals": ["build", "deploy", "pipeline", "release", "rollback"],
    },
    {
        "prefix": "api",
        "domain": "API integration operations",
        "input": "API spec, endpoint docs, integration error, webhook payload",
        "dependencies": ["API documentation", "auth method", "payload example", "rate limits"],
        "signals": ["endpoints", "payloads", "auth", "webhooks", "rate limits"],
    },
    {
        "prefix": "database",
        "domain": "database operations",
        "input": "schema, migration file, query plan, data quality note",
        "dependencies": ["database schema", "migration file", "query plan", "data sample"],
        "signals": ["tables", "indexes", "migrations", "queries", "data quality"],
    },
    {
        "prefix": "search",
        "domain": "search and retrieval operations",
        "input": "search query log, retrieval results, index schema, relevance judgment",
        "dependencies": ["query logs", "index schema", "relevance labels", "retrieval config"],
        "signals": ["queries", "ranking", "index", "relevance", "recall"],
    },
    {
        "prefix": "knowledge",
        "domain": "knowledge management operations",
        "input": "notes, wiki pages, knowledge base articles, taxonomy",
        "dependencies": ["note corpus", "taxonomy", "source links", "owner context"],
        "signals": ["notes", "taxonomy", "links", "knowledge base", "sources"],
    },
    {
        "prefix": "media",
        "domain": "media production operations",
        "input": "script, transcript, image brief, video shot list",
        "dependencies": ["media brief", "asset list", "audience", "format constraints"],
        "signals": ["scripts", "transcripts", "assets", "captions", "storyboard"],
    },
    {
        "prefix": "localization",
        "domain": "localization and translation operations",
        "input": "source copy, translation memory, locale guide, glossary",
        "dependencies": ["source text", "target locale", "glossary", "style guide"],
        "signals": ["locale", "translation", "glossary", "tone", "terminology"],
    },
    {
        "prefix": "community",
        "domain": "community management operations",
        "input": "forum post, moderation queue, announcement draft, user feedback thread",
        "dependencies": ["community guidelines", "thread context", "user history", "announcement goal"],
        "signals": ["posts", "moderation", "announcements", "feedback", "guidelines"],
    },
    {
        "prefix": "operations",
        "domain": "general business operations",
        "input": "SOP, process note, operations checklist, team request",
        "dependencies": ["process document", "owner map", "deadline", "operational constraint"],
        "signals": ["SOP", "process", "owners", "checklists", "handoff"],
    },
    {
        "prefix": "personal",
        "domain": "personal productivity operations",
        "input": "task list, personal note, habit log, calendar item",
        "dependencies": ["task list", "calendar", "priority context", "personal constraints"],
        "signals": ["tasks", "habits", "calendar", "priorities", "reminders"],
    },
    {
        "prefix": "writing",
        "domain": "writing and editing operations",
        "input": "draft text, outline, editorial brief, reader feedback",
        "dependencies": ["draft", "audience", "style guide", "feedback notes"],
        "signals": ["draft", "outline", "voice", "reader", "revision"],
    },
    {
        "prefix": "insurance",
        "domain": "insurance claims operations",
        "input": "claim form, policy wording, incident evidence, assessor notes",
        "dependencies": ["claim file", "policy document", "incident evidence", "coverage criteria"],
        "signals": ["claims", "coverage", "policy", "evidence", "settlement"],
    },
    {
        "prefix": "property",
        "domain": "property management operations",
        "input": "lease, maintenance ticket, inspection report, tenant message",
        "dependencies": ["property record", "lease terms", "maintenance history", "tenant context"],
        "signals": ["lease", "inspection", "maintenance", "tenant", "property"],
    },
    {
        "prefix": "real-estate",
        "domain": "real estate transaction operations",
        "input": "listing brief, offer terms, inspection note, settlement timeline",
        "dependencies": ["listing details", "buyer criteria", "offer terms", "inspection evidence"],
        "signals": ["listing", "offer", "settlement", "inspection", "valuation"],
    },
    {
        "prefix": "logistics",
        "domain": "logistics and shipment operations",
        "input": "shipment manifest, tracking update, carrier note, customs form",
        "dependencies": ["shipment manifest", "carrier data", "delivery window", "customs details"],
        "signals": ["shipment", "tracking", "carrier", "customs", "delivery"],
    },
    {
        "prefix": "warehouse",
        "domain": "warehouse inventory operations",
        "input": "stock count, pick list, receiving note, inventory adjustment",
        "dependencies": ["inventory export", "SKU catalog", "location map", "receiving record"],
        "signals": ["SKU", "stock", "warehouse", "receiving", "fulfillment"],
    },
    {
        "prefix": "manufacturing",
        "domain": "manufacturing operations",
        "input": "work order, defect log, production schedule, quality report",
        "dependencies": ["work order", "production line", "quality criteria", "operator notes"],
        "signals": ["production", "defects", "schedule", "quality", "work order"],
    },
    {
        "prefix": "supply-chain",
        "domain": "supply chain operations",
        "input": "supplier update, demand forecast, inventory plan, risk note",
        "dependencies": ["supplier list", "forecast data", "inventory position", "risk register"],
        "signals": ["suppliers", "forecast", "inventory", "lead time", "risk"],
    },
    {
        "prefix": "retail",
        "domain": "retail operations",
        "input": "sales report, product catalog, store note, promotion plan",
        "dependencies": ["sales data", "store profile", "product catalog", "promotion calendar"],
        "signals": ["sales", "store", "promotion", "catalog", "stock"],
    },
    {
        "prefix": "ecommerce",
        "domain": "ecommerce operations",
        "input": "order export, product listing, refund note, marketplace report",
        "dependencies": ["order data", "product catalog", "marketplace rules", "customer message"],
        "signals": ["orders", "products", "refunds", "marketplace", "listings"],
    },
    {
        "prefix": "marketing",
        "domain": "marketing campaign operations",
        "input": "campaign brief, ad copy, audience segment, performance report",
        "dependencies": ["campaign goal", "audience data", "creative assets", "performance metrics"],
        "signals": ["campaign", "audience", "copy", "conversion", "creative"],
    },
    {
        "prefix": "seo",
        "domain": "search engine optimization operations",
        "input": "keyword list, page audit, ranking report, content brief",
        "dependencies": ["target page", "keyword data", "search intent", "ranking baseline"],
        "signals": ["keywords", "rankings", "content", "search intent", "metadata"],
    },
    {
        "prefix": "content",
        "domain": "content production operations",
        "input": "content calendar, draft article, brief, editorial feedback",
        "dependencies": ["content brief", "brand voice", "publication channel", "editorial criteria"],
        "signals": ["article", "calendar", "editorial", "brand voice", "draft"],
    },
    {
        "prefix": "social",
        "domain": "social media operations",
        "input": "post draft, publishing calendar, engagement report, campaign note",
        "dependencies": ["platform rules", "posting schedule", "brand guidelines", "engagement data"],
        "signals": ["posts", "engagement", "platform", "schedule", "campaign"],
    },
    {
        "prefix": "ads",
        "domain": "paid advertising operations",
        "input": "ad account report, campaign settings, creative brief, budget note",
        "dependencies": ["ad platform", "budget", "targeting settings", "conversion data"],
        "signals": ["ads", "budget", "targeting", "creative", "ROAS"],
    },
    {
        "prefix": "sales",
        "domain": "sales enablement operations",
        "input": "deal note, pitch deck, objection log, account plan",
        "dependencies": ["account profile", "deal stage", "buyer role", "sales collateral"],
        "signals": ["deal", "pipeline", "pitch", "objections", "accounts"],
    },
    {
        "prefix": "partnerships",
        "domain": "partnership operations",
        "input": "partner proposal, MOU draft, co-marketing plan, partner report",
        "dependencies": ["partner profile", "proposal terms", "shared goals", "approval process"],
        "signals": ["partners", "MOU", "proposal", "co-marketing", "alignment"],
    },
    {
        "prefix": "fundraising",
        "domain": "fundraising operations",
        "input": "pitch materials, donor list, grant brief, investor update",
        "dependencies": ["target audience", "funding goal", "impact evidence", "deadline"],
        "signals": ["donors", "investors", "grant", "pitch", "funding"],
    },
    {
        "prefix": "grant",
        "domain": "grant application operations",
        "input": "grant instructions, proposal draft, budget table, eligibility note",
        "dependencies": ["grant guidelines", "eligibility criteria", "budget", "submission deadline"],
        "signals": ["grant", "eligibility", "budget", "proposal", "deadline"],
    },
    {
        "prefix": "academic-admin",
        "domain": "academic administration operations",
        "input": "course policy, enrollment note, assessment record, student request",
        "dependencies": ["institution policy", "student record", "assessment criteria", "deadline"],
        "signals": ["course", "student", "assessment", "policy", "enrollment"],
    },
    {
        "prefix": "library",
        "domain": "library and archive operations",
        "input": "catalog record, archive note, metadata sheet, digitization plan",
        "dependencies": ["catalog schema", "collection metadata", "rights note", "preservation policy"],
        "signals": ["catalog", "archive", "metadata", "rights", "digitization"],
    },
    {
        "prefix": "publishing",
        "domain": "publishing operations",
        "input": "manuscript, production checklist, author query, proof note",
        "dependencies": ["manuscript", "style sheet", "publication schedule", "rights context"],
        "signals": ["manuscript", "proof", "author", "publication", "style"],
    },
    {
        "prefix": "journalism",
        "domain": "journalism operations",
        "input": "source notes, interview transcript, news brief, fact-check log",
        "dependencies": ["source material", "editorial policy", "fact-check criteria", "deadline"],
        "signals": ["sources", "interviews", "facts", "story", "editorial"],
    },
    {
        "prefix": "legal-discovery",
        "domain": "legal discovery operations",
        "input": "document production, privilege log, deposition note, evidence request",
        "dependencies": ["case context", "document set", "privilege criteria", "request scope"],
        "signals": ["discovery", "privilege", "evidence", "deposition", "production"],
    },
    {
        "prefix": "compliance",
        "domain": "compliance operations",
        "input": "control checklist, audit finding, policy exception, evidence packet",
        "dependencies": ["control framework", "evidence files", "audit scope", "owner map"],
        "signals": ["controls", "audit", "evidence", "policy", "exceptions"],
    },
    {
        "prefix": "privacy",
        "domain": "privacy operations",
        "input": "data inventory, DSR request, privacy notice, processing activity",
        "dependencies": ["data map", "privacy policy", "jurisdiction note", "request details"],
        "signals": ["privacy", "data subject", "processing", "retention", "consent"],
    },
    {
        "prefix": "risk",
        "domain": "risk management operations",
        "input": "risk register, control report, incident note, mitigation plan",
        "dependencies": ["risk taxonomy", "control evidence", "owner map", "impact scale"],
        "signals": ["risk", "controls", "mitigation", "impact", "likelihood"],
    },
    {
        "prefix": "procurement",
        "domain": "procurement operations",
        "input": "purchase request, vendor quote, RFP response, approval note",
        "dependencies": ["purchase request", "vendor quote", "budget code", "approval policy"],
        "signals": ["purchase", "vendor", "RFP", "approval", "quote"],
    },
    {
        "prefix": "facilities",
        "domain": "facilities operations",
        "input": "maintenance request, space plan, safety report, vendor schedule",
        "dependencies": ["facility map", "maintenance log", "safety policy", "vendor contact"],
        "signals": ["maintenance", "facility", "space", "safety", "vendor"],
    },
    {
        "prefix": "energy",
        "domain": "energy operations",
        "input": "usage report, meter reading, sustainability plan, tariff note",
        "dependencies": ["meter data", "tariff schedule", "facility profile", "sustainability target"],
        "signals": ["energy", "meter", "tariff", "usage", "sustainability"],
    },
    {
        "prefix": "environmental",
        "domain": "environmental compliance operations",
        "input": "emissions report, permit condition, monitoring data, incident note",
        "dependencies": ["permit", "monitoring data", "emissions factor", "reporting period"],
        "signals": ["emissions", "permit", "monitoring", "environmental", "compliance"],
    },
    {
        "prefix": "construction",
        "domain": "construction project operations",
        "input": "site report, change order, drawing register, safety observation",
        "dependencies": ["site records", "drawing set", "contract scope", "safety plan"],
        "signals": ["site", "drawings", "change order", "safety", "schedule"],
    },
    {
        "prefix": "engineering-design",
        "domain": "engineering design operations",
        "input": "design specification, calculation note, review comment, requirement list",
        "dependencies": ["specification", "requirement set", "calculation record", "review standard"],
        "signals": ["requirements", "calculations", "design", "review", "specification"],
    },
    {
        "prefix": "qa",
        "domain": "quality assurance operations",
        "input": "test plan, defect report, acceptance criteria, release evidence",
        "dependencies": ["test plan", "defect log", "acceptance criteria", "release scope"],
        "signals": ["tests", "defects", "QA", "acceptance", "release"],
    },
    {
        "prefix": "customer-success",
        "domain": "customer success operations",
        "input": "account health note, renewal plan, usage report, success plan",
        "dependencies": ["account profile", "usage data", "renewal date", "success criteria"],
        "signals": ["account health", "renewal", "usage", "success plan", "customer"],
    },
    {
        "prefix": "training",
        "domain": "training and enablement operations",
        "input": "training brief, learner feedback, curriculum outline, assessment result",
        "dependencies": ["learning objective", "audience profile", "training materials", "assessment rubric"],
        "signals": ["training", "curriculum", "learners", "assessment", "feedback"],
    },
    {
        "prefix": "support-ops",
        "domain": "support process operations",
        "input": "support macro, escalation rule, queue report, knowledge base article",
        "dependencies": ["support policy", "queue data", "macro library", "escalation owner"],
        "signals": ["support", "macros", "queue", "escalation", "knowledge base"],
    },
    {
        "prefix": "identity",
        "domain": "identity and access operations",
        "input": "access request, role matrix, audit log, permission review",
        "dependencies": ["identity provider", "role matrix", "access logs", "approval policy"],
        "signals": ["access", "roles", "permissions", "audit", "identity"],
    },
    {
        "prefix": "sre",
        "domain": "site reliability engineering operations",
        "input": "SLO report, runbook, alert history, reliability review",
        "dependencies": ["service map", "SLO definitions", "alert data", "runbook"],
        "signals": ["SLO", "runbook", "alerts", "reliability", "service"],
    },
    {
        "prefix": "platform",
        "domain": "platform engineering operations",
        "input": "developer platform request, service catalog, template repo, platform metric",
        "dependencies": ["platform service", "template repository", "developer workflow", "service owner"],
        "signals": ["platform", "templates", "developer workflow", "service catalog", "self-service"],
    },
    {
        "prefix": "mobile",
        "domain": "mobile application operations",
        "input": "app crash log, release note, store review, mobile test report",
        "dependencies": ["mobile app build", "device context", "crash log", "release channel"],
        "signals": ["mobile", "crash", "release", "app store", "device"],
    },
    {
        "prefix": "iot",
        "domain": "IoT operations",
        "input": "device telemetry, firmware note, sensor log, provisioning record",
        "dependencies": ["device registry", "telemetry data", "firmware version", "network context"],
        "signals": ["devices", "telemetry", "firmware", "sensors", "provisioning"],
    },
    {
        "prefix": "robotics",
        "domain": "robotics operations",
        "input": "robot log, mission plan, sensor trace, calibration note",
        "dependencies": ["robot platform", "sensor data", "mission objective", "calibration file"],
        "signals": ["robot", "sensors", "mission", "calibration", "navigation"],
    },
    {
        "prefix": "bioinformatics",
        "domain": "bioinformatics operations",
        "input": "sequence file, variant table, pipeline log, sample metadata",
        "dependencies": ["sequence data", "sample metadata", "pipeline config", "reference genome"],
        "signals": ["sequence", "variants", "samples", "pipeline", "genome"],
    },
    {
        "prefix": "geospatial",
        "domain": "geospatial analysis operations",
        "input": "map layer, coordinate table, spatial query, GIS project note",
        "dependencies": ["spatial data", "coordinate reference system", "map layers", "analysis boundary"],
        "signals": ["map", "coordinates", "layers", "GIS", "spatial"],
    },
]


PROCEDURE_TEMPLATES = [
    {
        "suffix": "intake-classifier",
        "description": "Classifies {domain} requests by input type, expected artifact, routing owner, urgency, and missing context.",
        "use": "The user needs classification or routing for {domain} material before deeper work begins.",
        "precondition": "There is enough task context to decide category, owner, urgency, and next action.",
        "output": "Classification labels, routing decision, missing-context list, and next-step recommendation.",
    },
    {
        "suffix": "field-extractor",
        "description": "Extracts structured fields from {domain} material while preserving source location, uncertainty, and required normalization.",
        "use": "The user wants structured fields from {input} rather than a narrative summary.",
        "precondition": "The source includes identifiable fields or evidence spans that can be mapped into a table.",
        "output": "Structured field table with source evidence, confidence, and normalization notes.",
    },
    {
        "suffix": "evidence-grounder",
        "description": "Grounds {domain} claims in specific evidence snippets, source locations, and confidence notes.",
        "use": "The user wants claims checked against {input} rather than rewritten or summarized.",
        "precondition": "Source material is available and claims can be linked to evidence spans.",
        "output": "Claim-evidence map with supported, unsupported, and uncertain claims.",
    },
    {
        "suffix": "risk-reviewer",
        "description": "Reviews {domain} material for operational, compliance, security, quality, or delivery risk.",
        "use": "The user wants risk findings from {input} rather than extraction or formatting.",
        "precondition": "The task includes enough context to identify impact, likelihood, and mitigation.",
        "output": "Risk register with severity, evidence, mitigation, and owner questions.",
    },
    {
        "suffix": "summary-writer",
        "description": "Summarizes {domain} material into concise takeaways, decisions, open questions, and evidence limits.",
        "use": "The user wants a readable summary of {input} rather than structured extraction.",
        "precondition": "The source is long enough that condensation is useful and the audience is known.",
        "output": "Concise summary with key points, caveats, and action-relevant details.",
    },
    {
        "suffix": "rewrite-editor",
        "description": "Rewrites {domain} text for clarity, audience fit, tone, structure, and constraint preservation.",
        "use": "The user wants improved wording for existing {domain} text rather than analysis.",
        "precondition": "A draft or source text exists and the desired audience or tone is stated.",
        "output": "Rewritten text plus a compact list of changed assumptions or preserved constraints.",
    },
    {
        "suffix": "comparison-builder",
        "description": "Compares multiple {domain} items by criteria, differences, conflicts, tradeoffs, and decision relevance.",
        "use": "The user wants comparison across two or more {domain} sources or options.",
        "precondition": "At least two comparable items and evaluation criteria are available.",
        "output": "Comparison table with criteria, differences, tradeoffs, and recommendation caveats.",
    },
    {
        "suffix": "compliance-checker",
        "description": "Checks {domain} material against policy, requirements, acceptance criteria, or required procedure.",
        "use": "The user wants compliance or requirement fit checked rather than a general review.",
        "precondition": "The relevant policy, checklist, acceptance criteria, or rule set is available.",
        "output": "Compliance status, failed requirements, evidence, and remediation steps.",
    },
    {
        "suffix": "timeline-builder",
        "description": "Builds a timeline for {domain} events, deadlines, dependencies, decisions, and follow-up checkpoints.",
        "use": "The user wants sequence reconstruction or schedule structure from {input}.",
        "precondition": "The source contains dates, order cues, event descriptions, or dependency markers.",
        "output": "Timeline with dates, event descriptions, dependencies, and unresolved gaps.",
    },
    {
        "suffix": "priority-ranker",
        "description": "Ranks {domain} items by urgency, impact, effort, dependency, evidence strength, or stakeholder importance.",
        "use": "The user wants prioritization among candidate {domain} items rather than a summary.",
        "precondition": "Items and ranking criteria are explicit or inferable from the task context.",
        "output": "Ranked list with scoring criteria, rationale, and sensitivity notes.",
    },
    {
        "suffix": "quality-auditor",
        "description": "Audits {domain} artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.",
        "use": "The user wants quality assurance over {input} before the artifact is used downstream.",
        "precondition": "Expected quality criteria or artifact shape is available.",
        "output": "Quality findings, missing elements, inconsistent details, and correction checklist.",
    },
    {
        "suffix": "handoff-brief-writer",
        "description": "Writes a handoff brief for {domain} work with context, decisions, constraints, owners, and next actions.",
        "use": "The user wants another person or agent to continue {domain} work without losing context.",
        "precondition": "Current state, unresolved questions, and expected next owner can be identified.",
        "output": "Handoff brief with context, completed work, open issues, owner, and acceptance criteria.",
    },
    {
        "suffix": "normalizer",
        "description": "Normalizes {domain} material into a consistent naming, schema, format, or taxonomy.",
        "use": "The user wants consistency and canonicalization for {input}.",
        "precondition": "There is a target schema, naming convention, taxonomy, or example format.",
        "output": "Normalized artifact with mapping from original values to canonical values.",
    },
    {
        "suffix": "dependency-mapper",
        "description": "Maps dependencies, prerequisites, resources, owners, and downstream effects in {domain} work.",
        "use": "The user wants dependency structure rather than content summarization.",
        "precondition": "Inputs mention resources, owners, tools, dates, systems, or prerequisite actions.",
        "output": "Dependency map with prerequisite, dependent item, owner, and risk notes.",
    },
    {
        "suffix": "scenario-planner",
        "description": "Plans alternative scenarios for {domain} decisions under changing assumptions, constraints, or risks.",
        "use": "The user wants scenario planning for {domain} rather than a single recommendation.",
        "precondition": "Key assumptions, decision options, or uncertainty drivers are available.",
        "output": "Scenario table with assumptions, expected outcomes, risks, and decision triggers.",
    },
    {
        "suffix": "monitoring-plan-builder",
        "description": "Builds a monitoring plan for {domain} with signals, thresholds, review cadence, and escalation owners.",
        "use": "The user wants ongoing monitoring or follow-up design for {domain}.",
        "precondition": "Relevant signals, owners, and decision thresholds can be defined.",
        "output": "Monitoring plan with signals, thresholds, cadence, owners, and escalation rules.",
    },
    {
        "suffix": "artifact-packager",
        "description": "Packages {domain} outputs into a reusable artifact with sections, file naming, dependencies, and delivery notes.",
        "use": "The user wants a finished deliverable package rather than raw analysis.",
        "precondition": "The required output audience, format, and included materials are known.",
        "output": "Packaged artifact outline with included files, section order, and delivery checklist.",
    },
    {
        "suffix": "resource-linker",
        "description": "Links {domain} work to relevant resources, references, files, systems, or supporting evidence.",
        "use": "The user wants resource mapping for {domain} rather than completing the task itself.",
        "precondition": "Candidate resources, references, or system links are available or named.",
        "output": "Resource map with purpose, relevance, owner, and usage notes.",
    },
    {
        "suffix": "failure-diagnoser",
        "description": "Diagnoses why a {domain} workflow, artifact, or previous answer failed to meet expectations.",
        "use": "The user wants failure analysis for {domain} rather than a fresh artifact.",
        "precondition": "There is a failed output, error report, mismatch, or user complaint to analyze.",
        "output": "Failure classification, evidence, root-cause hypothesis, and corrective action.",
    },
    {
        "suffix": "acceptance-test-builder",
        "description": "Builds acceptance tests or review checks for {domain} outputs against expected behavior and constraints.",
        "use": "The user wants testable checks for {domain} deliverables or workflows.",
        "precondition": "Success criteria, expected artifact shape, or user acceptance conditions are available.",
        "output": "Acceptance tests with inputs, expected results, edge cases, and verification notes.",
    },
]


def bullet_lines(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def generated_background_skills() -> list[dict[str, str]]:
    generated: list[dict[str, str]] = []
    for domain in [*DOMAIN_CLUSTERS, *ADDITIONAL_DOMAIN_CLUSTERS]:
        for procedure in PROCEDURE_TEMPLATES:
            name = f"{domain['prefix']}-ops-{procedure['suffix']}"
            dependencies = [*domain["dependencies"], "task-specific constraints"]
            signals = [*domain["signals"], procedure["suffix"].replace("-", " ")]
            generated.append(
                {
                    "name": name,
                    "description": procedure["description"].format(**domain),
                    "use": procedure["use"].format(**domain),
                    "precondition": procedure["precondition"].format(**domain),
                    "output": procedure["output"].format(**domain),
                    "dependency_profile": f"{domain['domain']} procedure over {domain['input']}; requires preserving the procedure-specific input state and output artifact.",
                    "external_dependencies": bullet_lines(dependencies),
                    "resource_signals": bullet_lines(signals),
                }
            )
    return generated


def merged_background_skills() -> list[dict[str, str]]:
    merged: list[dict[str, str]] = []
    seen: set[str] = set()
    for skill in [*BACKGROUND_SKILLS, *generated_background_skills()]:
        name = skill["name"]
        if name in seen:
            raise ValueError(f"Duplicate background skill name: {name}")
        seen.add(name)
        merged.append(skill)
    return merged


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    family_dir = repo_root / "skills" / "background_scale"
    if family_dir.exists():
        shutil.rmtree(family_dir)
    family_dir.mkdir(parents=True)

    skills = merged_background_skills()
    for skill in skills:
        skill_dir = family_dir / skill["name"]
        skill_dir.mkdir(parents=True)
        text = TEMPLATE.format(
            name=skill["name"],
            title=titleize(skill["name"]),
            description=skill["description"],
            use=skill["use"],
            precondition=skill.get("precondition", "The user provides enough context to identify the intended input and output artifact."),
            output=skill["output"],
            dependency_profile=skill.get(
                "dependency_profile",
                "General background procedure; depends on user-provided task context and the source material named in the request.",
            ),
            external_dependencies=skill.get("external_dependencies", "- user-provided task context\n- source material named in the request"),
            resource_signals=skill.get("resource_signals", "- requested artifact\n- input type\n- domain-specific constraints"),
        )
        (skill_dir / "SKILL.md").write_text(text, encoding="utf-8")

    print(f"Generated {len(skills)} background skills in {family_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
