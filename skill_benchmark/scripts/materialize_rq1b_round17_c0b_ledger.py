#!/usr/bin/env python3
"""Materialise the independently reviewed Round 17 C0B source-screen ledger.

The data below records source-only C0B decisions made against byte-preserved
originals. It is intentionally limited to peer-route structure: it creates no
prompt, label, acceptable set, retrieval input, model score, or result.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "rq1b_cross_source_public_benchmark" / "manifest"
QUEUE = MANIFEST / "c0b_round17_source_screen_queue_2026-08-27.jsonl"
OUTPUT = MANIFEST / "c0b_structural_ledger_round17_2026-08-27.jsonl"


def review(status: str, reviewer: str, envelope: str, risks: list[str], rationale: str, evidence: dict[str, tuple[str, str]]) -> dict[str, object]:
    return {
        "status": status,
        "reviewer": reviewer,
        "envelope": envelope,
        "risks": risks,
        "rationale": rationale,
        "evidence": evidence,
    }


REVIEWS: dict[str, dict[str, object]] = {
    "rq1b-xs-c0a-201": review(
        "C0_SOURCE_BACKED_DRAFT_NOT_A_CLUSTER_OR_RESULT", "01a04203-23bc-7cb1-aeab-730a24484f27",
        "End-to-end contract review through a selected jurisdiction, playbook, risk-analysis, or controlled-delivery route.",
        ["broad contract-review overlap", "possible multi-adequacy"],
        "All four sources provide complete contract-review entry routes at comparable abstraction. Jurisdiction, playbook, risk-analysis, and delivery constraints are peer distinctions; later prompt review must test overlap.",
        {
            "r17m1-NOMOREKKK-contract-review-skill-unknown": ("PRC-jurisdiction contract review with legal risk analysis and revision suggestions.", "系统化审查中国法域合同/协议/法律文书的纯法律视角流程"),
            "r17m1-WenzhuoXu-lawgent-legal-helper-skills-review-contract": ("Playbook-based commercial-contract review with deviations, redlines, and business impact.", "Review a commercial contract against a configurable playbook — flag deviations, generate redlines, and provide business-impact analysis."),
            "r17m1-evan66547-Contract-Reviewer-Agent-Eval-skills-senior-legal-contract-reviewer-v1": ("PRC commercial-contract review with risk quantification and adversarial testing.", "高级法务合同审核智能体 v1.2，专注于商业合同风险管理，深度对齐中国《民法典》及相关司法解释，提供结构扫描、逻辑诊断、风险量化输出。"),
            "r17m1-nwwfewx-contract-review-unknown": ("Intake-gated contract and institutional-document review with checklist routes and delivery gates.", "Contract and institutional-document review with evidence-backed risk findings and revision-ready outputs."),
        },
    ),
    "rq1b-xs-c0a-202": review(
        "C0_STRUCTURAL_REJECT_NOT_A_CLUSTER_OR_RESULT", "01a04203-23bc-7cb1-aeab-730a24484f27",
        "Broad legal analysis.", ["different legal task families", "no bounded common route"],
        "The sources cover authority research, prospective compliance, litigation analysis, and risk scoring. Their shared legal topic is too broad to form symmetric routes.",
        {
            "r17m1-Golden2002-legal-research-skill-legal-research": ("PRC legal-source research and application analysis.", "完整法源检索（法律/行政法规/司法解释/指导性案例/典型案例）"),
            "r17m1-WenzhuoXu-lawgent-legal-helper-skills-compliance-check": ("Prospective regulatory compliance assessment.", "Run a compliance check or standalone legal enquiry on a proposed action, new product/feature, business launch, vendor change, data flow, incident, or regulated activity."),
            "r17m1-WenzhuoXu-lawgent-legal-helper-skills-litigation-analysis": ("Litigation or arbitration analysis with claims, evidence, and limitation review.", "Analyze a litigation or arbitration matter — map every claim and defense to its legal elements with supporting facts and verified authority"),
            "r17m1-WenzhuoXu-lawgent-legal-helper-skills-legal-risk-assessment": ("Severity-by-likelihood legal-risk triage.", "Assess and classify legal risks using a severity-by-likelihood framework with escalation criteria."),
        },
    ),
    "rq1b-xs-c0a-203": review(
        "C0_STRUCTURAL_REJECT_NOT_A_CLUSTER_OR_RESULT", "01a04203-23bc-7cb1-aeab-730a24484f27",
        "Legal-document work.", ["generic utility", "delivery component", "mixed substantive tasks"],
        "The generic DOCX utility and redline-delivery component are not peer legal drafting or response routes; substantive routes also differ in task object.",
        {
            "r17m1-Golden2002-legal-research-skill-docx": ("Generic DOCX manipulation utility.", "Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files)."),
            "r17m1-WenzhuoXu-lawgent-legal-helper-skills-docx-redline": ("Native Word tracked-change delivery component.", "Deliver contract/document edits as native Word tracked changes"),
            "r17m1-WenzhuoXu-lawgent-legal-helper-skills-draft-agreement": ("First-draft agreement or PRC litigation-document production.", "Draft a new agreement or PRC litigation document from deal terms"),
            "r17m1-WenzhuoXu-lawgent-legal-helper-skills-legal-response": ("Response analysis for an inbound authority or counterparty communication.", "Draft a careful response to a regulator, authority, or counterparty communication"),
        },
    ),
    "rq1b-xs-c0a-204": review(
        "C0_SOURCE_BACKED_DRAFT_NOT_A_CLUSTER_OR_RESULT", "01a04203-23bc-7cb1-aeab-730a24484f27",
        "Financial reconciliation or tie-out against a selected accounting object and verification rule.",
        ["vague reconciliation prompt may be multi-adequate"],
        "All four candidates are complete reconciliation or tie-out routes at comparable abstraction, distinguished by accounting object, input form, and verification rule.",
        {
            "r17m1-adoptai-cpa-skills-skills-ar-aging-tie-out": ("AR-aging-to-GL reconciliation.", "Tie the accounts receivable aging to the general ledger control account and test it properly"),
            "r17m1-adoptai-cpa-skills-skills-payroll-tax-reconciliation": ("Four-way payroll reconciliation.", "Reconcile the payroll register to the quarterly Forms 941, the W-2/W-3 totals, and the general ledger"),
            "r17m1-anthropics-financial-services-plugins-agent-plugins-gl-reconciler-skills-gl-recon": ("Investment-operations GL-to-subledger reconciliation.", "Reconcile general ledger to subledger for a trade date or period"),
            "r17m1-anthropics-financial-services-plugins-agent-plugins-statement-auditor-skills-nav-tieout": ("LP-statement-to-NAV-pack tie-out.", "Tie an LP statement to the fund's NAV pack"),
        },
    ),
    "rq1b-xs-c0a-205": review(
        "C0_STRUCTURAL_REJECT_NOT_A_CLUSTER_OR_RESULT", "01a04203-23bc-7cb1-aeab-730a24484f27",
        "Audit work.", ["sampling prerequisite", "mixed testing tasks", "model QA mismatch"],
        "The candidates mix an audit sampling method, substantive population tests, and spreadsheet QA; there is no comparable peer first route.",
        {
            "r17m1-adoptai-cpa-skills-skills-audit-sampling": ("Audit-population sampling method.", "Select an audit sample from a population using monetary unit (PPS), stratified, or random attribute sampling"),
            "r17m1-adoptai-cpa-skills-skills-journal-entry-anomaly-scan": ("Full-population journal-entry anomaly scan.", "Scan a full-population general ledger or journal entry extract"),
            "r17m1-adoptai-cpa-skills-skills-expense-policy-testing": ("Expense-population compliance testing.", "Test an expense, travel, or corporate card population against the client's own written policy"),
            "r17m1-anthropics-financial-services-plugins-agent-plugins-earnings-reviewer-skills-audit-xls": ("Spreadsheet formula and model-integrity audit.", "Audit a spreadsheet for formula accuracy, errors, and common mistakes."),
        },
    ),
    "rq1b-xs-c0a-206": review(
        "C0_SOURCE_BACKED_DRAFT_NOT_A_CLUSTER_OR_RESULT", "01a04203-217f-72e3-b977-dc71e2a69edb",
        "Retrieve or update public market data through a selected asset, venue, or delivery context.",
        ["direct stock lookup and spreadsheet update overlap"],
        "All candidates are complete public-market-data routes. Asset or venue scope and spreadsheet delivery are parallel operational distinctions, subject to later adequacy review.",
        {
            "r17m1-NousResearch-hermes-agent-optional-skills-finance-stocks": ("Yahoo-backed stock and crypto quote/history lookup.", "Read-only market data via Yahoo Finance."),
            "r17m1-NousResearch-hermes-agent-optional-skills-finance-polymarket": ("Prediction-market data retrieval.", "Query prediction market data from Polymarket using their public REST APIs."),
            "r17m1-NousResearch-hermes-agent-optional-skills-blockchain-hyperliquid": ("Hyperliquid market and account data retrieval.", "Query Hyperliquid market and account data through the public `/info` endpoint."),
            "r17m1-insight68-Skills-skills-stock-price-updater": ("Workbook-driven stock-price update and writeback.", "Update Excel files with latest stock market data from multiple sources."),
        },
    ),
    "rq1b-xs-c0a-207": review(
        "C0_SOURCE_BACKED_DRAFT_NOT_A_CLUSTER_OR_RESULT", "01a04203-217f-72e3-b977-dc71e2a69edb",
        "Build a financial valuation or transaction model under a selected methodology.",
        ["valuation-method prompt overlap"],
        "Comparable financial-model construction routes differ by relative valuation, intrinsic valuation, leveraged buyout, and merger analysis. Prompt review must control for overlap.",
        {
            "r17m1-NousResearch-hermes-agent-optional-skills-finance-comps-analysis": ("Comparable-company valuation workbook construction.", "Build comparable-company valuation workbooks in Excel."),
            "r17m1-anthropics-financial-services-plugins-agent-plugins-model-builder-skills-dcf-model": ("DCF equity-valuation model construction.", "Real DCF (Discounted Cash Flow) model creation for equity valuation."),
            "r17m1-anthropics-financial-services-plugins-agent-plugins-model-builder-skills-lbo-model": ("Leveraged-buyout model completion.", "This skill should be used when completing LBO (Leveraged Buyout) model templates in Excel for private equity transactions, deal materials, or investment committee presentations."),
            "r17m1-anthropics-financial-services-plugins-vertical-plugins-investment-banking-skills-merger-model": ("M&A accretion/dilution model construction.", "Build accretion/dilution analysis for M&A transactions."),
        },
    ),
    "rq1b-xs-c0a-208": review(
        "C0_STRUCTURAL_REJECT_NOT_A_CLUSTER_OR_RESULT", "01a04203-217f-72e3-b977-dc71e2a69edb",
        "Month-end close work.", ["generic journal-entry container", "different close-package outputs"],
        "The journal-entry route explicitly contains the accrual use case while the other sources make different close-package artefacts, so the peer gate fails.",
        {
            "r17m1-anthropics-financial-services-plugins-agent-plugins-month-end-closer-skills-accrual-schedule": ("Policy-based accrual schedule and draft entry.", "Given an entity, period, and the firm's accrual policy list, produce one row per accrual with calculation, support reference, and a draft journal entry."),
            "r17m1-anthropics-financial-services-plugins-agent-plugins-month-end-closer-skills-roll-forward": ("Balance-sheet roll-forward.", "Given an account (or account group), entity, and period, produce a roll-forward that ties beginning to ending."),
            "r17m1-anthropics-financial-services-plugins-agent-plugins-month-end-closer-skills-variance-commentary": ("Threshold-based variance commentary.", "Given current-period actuals, prior-period actuals, and budget for the same scope, produce a commentary table."),
            "r17m1-insight68-Skills-skills-journal-entry-prep": ("Generic month-end journal-entry preparation.", "Use when booking accruals, prepaid amortization, fixed asset depreciation, payroll entries, revenue recognition, or any manual journal entry."),
        },
    ),
    "rq1b-xs-c0a-209": review(
        "C0_STRUCTURAL_REJECT_NOT_A_CLUSTER_OR_RESULT", "01a04203-217f-72e3-b977-dc71e2a69edb",
        "Equity research.", ["pre/post-event lifecycle mismatch", "snapshot versus full-research scope"],
        "The candidates mix pre-earnings, post-earnings, company snapshot, and broad full-company research routes, not comparable peers.",
        {
            "r17m1-HHFinAi-earnings-analysis-unknown": ("Post-event earnings analysis.", "post-print analysis"),
            "r17m1-anthropics-financial-services-plugins-partner-built-spglobal-skills-earnings-preview-beta": ("Pre-event earnings preview.", "Generate a concise 4-5 page equity research earnings preview for a single company."),
            "r17m1-anthropics-financial-services-plugins-partner-built-spglobal-skills-tear-sheet": ("Audience-specific company snapshot.", "Generate audience-specific company tear sheets by pulling live data from S&P Capital IQ via the S&P Global MCP tools and formatting the result as a professional Word document."),
            "r17m1-pppop00-Equity-Research-Company-unknown": ("Broad company-research report workflow.", "Full-stack equity research report generator built on the Anamnesis Pattern (cross-session institutional memory + scheduled adversarial review)."),
        },
    ),
    "rq1b-xs-c0a-210": review(
        "C0_SOURCE_BACKED_DRAFT_NOT_A_CLUSTER_OR_RESULT", "01a04203-217f-72e3-b977-dc71e2a69edb",
        "Answer a data or business question with SQL using a selected execution environment.",
        ["warehouse and dbt request overlap"],
        "All candidates provide complete SQL-based analytical routes at comparable abstraction with different execution or data interfaces. Later prompts must establish singleton adequacy.",
        {
            "r16m1-astronomer-agents-skills-analyzing-data": ("Warehouse SQL analysis.", "Queries the data warehouse with SQL and answers business questions about data."),
            "r17m1-dbt-labs-dbt-agent-skills-skills-dbt-skills-answering-natural-language-questions-with-dbt": ("dbt semantic-layer or project SQL analysis.", "Writes and executes SQL queries against the data warehouse using dbt's Semantic Layer or ad-hoc SQL to answer business questions."),
            "r17m1-ClickHouse-agent-skills-skills-chdb-sql": ("Embedded ClickHouse SQL over local, cloud, or remote inputs.", "Run ClickHouse SQL directly in Python — no server needed."),
            "r17m1-aws-agent-toolkit-for-aws-plugins-aws-data-analytics-skills-querying-data-lake": ("Athena data-lake SQL execution.", "Execute SQL queries on Amazon Athena across default and federated catalogs (Glue, S3 Tables, Redshift) with workgroup selection, statement classification, and error recovery."),
        },
    ),
    "rq1b-xs-c0a-211": review(
        "C0_STRUCTURAL_REJECT_NOT_A_CLUSTER_OR_RESULT", "01a04203-2516-79e3-8f3b-ddec5167dc71",
        "Database optimisation.", ["generic-versus-specialist asymmetry", "query-text-only mismatch"],
        "Three candidates are broad database guidance or operations routes while the Snowflake candidate is a narrow SQL-text transformation specialist.",
        {
            "r17m1-neondatabase-postgres-skills-skills-postgres-best-practices": ("Broad PostgreSQL schema, indexing, and query guidance.", "Guidelines and best practices for working with Postgres, covering schema design, indexing, query optimization, and common pitfalls."),
            "r17m1-ClickHouse-agent-skills-skills-clickhouse-best-practices": ("Broad ClickHouse schema, query, ingestion, and connectivity guidance.", "Comprehensive guidance for ClickHouse covering schema design, query optimization, data ingestion, and AI agent connectivity."),
            "r17m1-AltimateAI-data-engineering-skills-skills-snowflake-optimizing-query-text": ("Supplied Snowflake query-text optimisation.", "Optimizes Snowflake SQL query performance from provided query text."),
            "r17m1-aws-agent-toolkit-for-aws-skills-specialized-skills-analytics-skills-redshift-guide": ("Broad Redshift SQL and operations guidance.", "Amazon Redshift is NOT PostgreSQL — corrects PostgreSQL-derived LLM mistakes; covers Redshift-specific SQL, DDL, COPY/UNLOAD, system views, metadata discovery, and operational patterns."),
        },
    ),
    "rq1b-xs-c0a-212": review(
        "C0_SOURCE_BACKED_DRAFT_NOT_A_CLUSTER_OR_RESULT", "01a04203-2516-79e3-8f3b-ddec5167dc71",
        "Provision or operate PostgreSQL under a selected local or managed-service environment.",
        ["broader RDS engine coverage", "possible multi-adequacy"],
        "Each candidate is a complete first route for local/ClickHouse Cloud Postgres, Aurora PostgreSQL, or standalone RDS. Their platform boundaries are explicit and source-supported.",
        {
            "r17m1-ClickHouse-agent-skills-skills-infra-postgres": ("clickhousectl local or cloud Postgres operation.", "Sets up and manages Postgres using the clickhousectl CLI"),
            "r17m1-aws-agent-toolkit-for-aws-skills-specialized-skills-database-skills-amazon-aurora-postgresql": ("Aurora PostgreSQL creation and operation.", "A modular toolkit for **Aurora PostgreSQL** organized as a registry of sub-skills."),
            "r17m1-aws-agent-toolkit-for-aws-skills-specialized-skills-database-skills-rds-oss": ("Standalone RDS open-source database operation.", "Scoped to RDS open-source engines. For Aurora, use `amazon-aurora`."),
        },
    ),
    "rq1b-xs-c0a-213": review(
        "C0_STRUCTURAL_REJECT_NOT_A_CLUSTER_OR_RESULT", "01a04203-2516-79e3-8f3b-ddec5167dc71",
        "dbt migration.", ["lifecycle-stage mismatch", "triage versus migration", "different migration objects"],
        "The sources mix SQL adoption, Core-to-Fusion issue triage, data-platform migration, and dbt-core upgrade routes.",
        {
            "r17m1-AltimateAI-data-engineering-skills-skills-dbt-migrating-sql-to-dbt": ("Legacy SQL-to-dbt conversion.", "Converts legacy SQL to modular dbt models."),
            "r17m1-dbt-labs-dbt-agent-skills-skills-dbt-migration-skills-migrating-dbt-core-to-fusion": ("Core-to-Fusion error triage.", "Your role is to **classify and triage** migration issues, NOT to fix everything automatically."),
            "r17m1-dbt-labs-dbt-agent-skills-skills-dbt-migration-skills-migrating-dbt-project-across-platforms": ("dbt data-platform migration.", "This skill guides migration of a dbt project from one data platform (source) to another (target) — for example, Snowflake to Databricks, or Databricks to Snowflake."),
            "r17m1-dbt-labs-dbt-agent-skills-skills-dbt-migration-skills-upgrading-dbt-core": ("dbt-core version upgrade.", "You upgrade a dbt-core **v1** project all the way to **1.12** — not one minor"),
        },
    ),
    "rq1b-xs-c0a-214": review(
        "C0_STRUCTURAL_REJECT_NOT_A_CLUSTER_OR_RESULT", "01a04203-2516-79e3-8f3b-ddec5167dc71",
        "Data lineage work.", ["output-format component", "broad governance route", "directional peers incomplete"],
        "Upstream and downstream tracing are peers, but Mermaid materialisation is an output specialist and dbt Mesh is broader governance/implementation.",
        {
            "r16m1-astronomer-agents-skills-tracing-upstream-lineage": ("Upstream origin investigation.", "Trace the origins of data - answer \"Where does this data come from?\""),
            "r16m1-astronomer-agents-skills-tracing-downstream-lineage": ("Downstream impact tracing.", "Answer the critical question: \"What breaks if I change this?\""),
            "r17m1-dbt-labs-dbt-agent-skills-skills-dbt-extras-skills-creating-mermaid-dbt-dag": ("Mermaid lineage visualisation.", "Generates a Mermaid flowchart diagram of dbt model lineage using MCP tools, manifest.json, or direct code parsing as fallbacks."),
            "r17m1-dbt-labs-dbt-agent-skills-skills-dbt-skills-working-with-dbt-mesh": ("dbt Mesh governance and implementation.", "dbt Mesh includes four governance features."),
        },
    ),
    "rq1b-xs-c0a-215": review(
        "C0_SOURCE_BACKED_DRAFT_NOT_A_CLUSTER_OR_RESULT", "01a04203-2516-79e3-8f3b-ddec5167dc71",
        "Deliver database data to an analytics-ready lake using a selected continuous, ingestion, or snapshot route.",
        ["broad AWS ingestion coverage", "possible multi-adequacy"],
        "All candidates are complete data-to-lake first routes differentiated by continuous CDC, source-driven AWS ingestion, or RDS snapshot export.",
        {
            "r17m1-confluentinc-agent-skills-skills-confluent-cloud-cdc-tableflow": ("Continuous Confluent CDC to Iceberg or Delta.", "This skill handles the complete workflow from database to Iceberg/Delta tables."),
            "r17m1-aws-agent-toolkit-for-aws-plugins-aws-data-analytics-skills-ingesting-into-data-lake": ("AWS data-lake ingestion.", "Move data from a source into a queryable table in the data lake."),
            "r17m1-aws-agent-toolkit-for-aws-skills-specialized-skills-database-skills-exporting-rds-to-s3": ("RDS or Aurora snapshot export to S3 Parquet.", "Domain expertise for exporting Amazon RDS and Aurora database snapshots to Amazon S3"),
        },
    ),
    "rq1b-xs-c0a-216": review(
        "C0_STRUCTURAL_REJECT_NOT_A_CLUSTER_OR_RESULT", "01a04203-230f-7621-89b2-5f19025122f3",
        "Data-platform troubleshooting.", ["different problem objects", "different execution environments", "over-broad envelope"],
        "Managed-Postgres performance RCA, local dbt debugging, dbt platform-job investigation, and Airflow failure diagnosis do not form one parallel peer class.",
        {
            "r17m1-ClickHouse-agent-skills-skills-clickhouse-managed-postgres-rca": ("Managed-Postgres performance RCA.", "Trigger whenever a user reports slowness, high CPU, low"),
            "r17m1-AltimateAI-data-engineering-skills-skills-dbt-debugging-dbt-errors": ("Local dbt error debugging.", "Debugs and fixes dbt errors systematically."),
            "r17m1-dbt-labs-dbt-agent-skills-skills-dbt-skills-troubleshooting-dbt-job-errors": ("dbt platform-job failure investigation.", "Diagnoses dbt Cloud/platform job failures by analyzing run logs, querying the Admin API, reviewing git history, and investigating data issues."),
            "r16m1-astronomer-agents-skills-debugging-dags": ("Airflow DAG failure diagnosis.", "You are a data engineer debugging a failed Airflow DAG."),
        },
    ),
    "rq1b-xs-c0a-217": review(
        "C0_SOURCE_BACKED_DRAFT_NOT_A_CLUSTER_OR_RESULT", "01a04203-230f-7621-89b2-5f19025122f3",
        "Run static application-security analysis with a selected scanner.",
        ["broad multi-language SAST requests may be multi-adequate"],
        "Semgrep, Horusec, and Fortify are complete scanner-specific SAST routes at comparable abstraction. Their analysis architecture and workflow are source-backed distinctions.",
        {
            "r17m1-AgentSecOps-SecOpsAgentKit-skills-appsec-sast-semgrep": ("Semgrep static-analysis route.", "Perform comprehensive static application security testing using Semgrep, a fast, open-source"),
            "r17m1-AgentSecOps-SecOpsAgentKit-skills-secsdlc-sast-horusec": ("Horusec multi-tool static-analysis route.", "Horusec is an open-source security analysis tool that performs static code analysis across 18+ programming languages using 20+ integrated security tools."),
            "r17m1-selvarajmurugesan90-ops-engineering-skills-plugins-security-scanning-tooling-skills-fortify-static-analysis": ("Fortify SCA route.", "Fortify Static Code Analyzer (SCA) is an enterprise, historically"),
        },
    ),
    "rq1b-xs-c0a-218": review(
        "C0_STRUCTURAL_REJECT_NOT_A_CLUSTER_OR_RESULT", "01a04203-230f-7621-89b2-5f19025122f3",
        "API security.", ["design-time versus runtime lifecycle", "interactive proxy versus automated scan"],
        "Specification linting, runtime interception, and deployed-target DAST use incompatible lifecycle stages and input forms.",
        {
            "r17m1-AgentSecOps-SecOpsAgentKit-skills-appsec-api-spectral": ("Design-time API specification linting.", "Spectral is a flexible JSON/YAML linter from Stoplight that validates API specifications against"),
            "r17m1-AgentSecOps-SecOpsAgentKit-skills-appsec-api-mitmproxy": ("Interactive runtime traffic interception and replay.", "mitmproxy is an interactive, TLS-capable intercepting HTTP proxy for penetration testers and developers."),
            "r17m1-selvarajmurugesan90-ops-engineering-skills-plugins-security-scanning-tooling-skills-owasp-zap-dast-configuration": ("Automated dynamic application-security scanning.", "Guides deep, tool-specific configuration of OWASP ZAP (Zed Attack"),
        },
    ),
    "rq1b-xs-c0a-219": review(
        "C0_SOURCE_BACKED_DRAFT_NOT_A_CLUSTER_OR_RESULT", "01a04203-230f-7621-89b2-5f19025122f3",
        "Author and enforce Kubernetes admission policy using a selected engine.",
        ["OPA has additional non-Kubernetes domains", "unconstrained prompt may be multi-adequate"],
        "Rego/Gatekeeper, YAML-native Kyverno, and WASM Kubewarden are complete Kubernetes admission-policy first routes with parallel implementation contexts.",
        {
            "r17m1-AgentSecOps-SecOpsAgentKit-skills-compliance-policy-opa": ("Rego/Gatekeeper Kubernetes admission policy.", "Validating Kubernetes admission control policies"),
            "r17m1-selvarajmurugesan90-ops-engineering-skills-plugins-policy-and-governance-tooling-skills-kyverno-policy-management": ("YAML-native Kyverno admission policy.", "Kyverno is a Kubernetes-native policy engine that expresses admission"),
            "r17m1-selvarajmurugesan90-ops-engineering-skills-plugins-security-scanning-tooling-skills-kubewarden-admission-policy-configuration": ("WASM-based Kubewarden admission policy.", "Kubewarden is a Kubernetes admission policy engine, like OPA/Gatekeeper"),
        },
    ),
    "rq1b-xs-c0a-220": review(
        "C0_STRUCTURAL_REJECT_NOT_A_CLUSTER_OR_RESULT", "01a04203-230f-7621-89b2-5f19025122f3",
        "Telemetry expressions.", ["pipeline versus datastore-query lifecycle", "cross-signal mismatch"],
        "OTTL configures collector transformation, while PromQL and LogQL query stored metrics or logs. The proposed three-way peer class is not comparable.",
        {
            "r17m1-ollygarden-opentelemetry-agent-skills-skills-otel-ottl": ("Collector telemetry transformation and routing.", "OTTL transforms or selects telemetry inside Collector components."),
            "r17m1-selvarajmurugesan90-ops-engineering-skills-plugins-observability-and-platform-extras-skills-promql-query-authoring": ("Prometheus metric-query authoring.", "Writing a new PromQL query for a dashboard panel, recording rule, or"),
            "r17m1-selvarajmurugesan90-ops-engineering-skills-plugins-observability-and-platform-extras-skills-logql-query-authoring": ("Loki log-query authoring.", "Writing a new LogQL query to find, filter, or count log lines matching"),
        },
    ),
    "rq1b-xs-c0a-221": review(
        "C0_STRUCTURAL_REJECT_NOT_A_CLUSTER_OR_RESULT", "01a04203-246e-7291-a8b8-55be794f4e3c",
        "Pre-production assessment.", ["readiness container", "security audit component", "well-architected overlap"],
        "Production readiness explicitly contains security review while Well-Architected overlaps its broad assessment dimensions; the candidates are structurally asymmetric.",
        {
            "r16m1-cloudflare-security-audit-skill-skills-security-audit": ("Codebase vulnerability audit.", "Security audit of a codebase — web apps, APIs, services, CLI tools, libraries, daemons, and more."),
            "r17m1-nik-kale-sre-skills-skills-production-readiness": ("Pre-launch service readiness checklist.", "Systematic checklist to ensure services are ready for production deployment."),
            "r17m1-selvarajmurugesan90-ops-engineering-skills-plugins-standards-and-compliance-frameworks-skills-cloud-well-architected-framework-review": ("Cloud Well-Architected workload review.", "systematically walk a real, existing workload through each"),
        },
    ),
    "rq1b-xs-c0a-222": review(
        "C0_SOURCE_BACKED_DRAFT_NOT_A_CLUSTER_OR_RESULT", "01a04203-246e-7291-a8b8-55be794f4e3c",
        "Investigate an active incident through the evidence interface available to the operator.",
        ["multi-evidence incidents may be multi-adequate"],
        "Network-packet analysis, endpoint forensics, and service observability are complete, symmetric evidence-specific investigation routes at comparable abstraction.",
        {
            "r17m1-AgentSecOps-SecOpsAgentKit-skills-offsec-analysis-tshark": ("Packet-capture and network-protocol incident forensics.", "TShark is the command-line network protocol analyzer from the Wireshark project."),
            "r17m1-AgentSecOps-SecOpsAgentKit-skills-incident-response-forensics-osquery": ("Endpoint-state and threat-hunting forensics.", "osquery transforms operating systems into queryable relational databases, enabling security analysts to investigate compromises using SQL rather than traditional CLI tools."),
            "r17m1-selvarajmurugesan90-ops-engineering-skills-plugins-observability-and-platform-extras-skills-incident-investigation-using-metrics-logs-traces": ("Production incident localisation across metrics, logs, and traces.", "Metrics, logs, and traces each answer a different question well"),
        },
    ),
    "rq1b-xs-c0a-223": review(
        "C0_STRUCTURAL_REJECT_NOT_A_CLUSTER_OR_RESULT", "01a04203-246e-7291-a8b8-55be794f4e3c",
        "Frontend design.", ["near-duplicate general routes", "mode-dependent route", "orchestration dependency"],
        "The sources claim the same broad frontend creation/re-design need; their differences are aesthetic doctrine or ticket-engine orchestration, not separate user contexts.",
        {
            "r17m1-Ilm-Alan-frontend-design-unknown": ("Visual-anchor frontend build or restyling.", "Build a frontend with a deliberate visual direction held through palette, typography, structure, and texture"),
            "r17m1-PaulRBerg-agent-skills-skills-frontend-design": ("Frontend creation and redesign with rendered validation.", "Create a working frontend with a clear, subject-specific point of view, then prove it in the rendered UI."),
            "r17m1-event4u-app-agent-config-dist-agent-src-skills-fe-design": ("Mode-dependent UI change execution.", "Use when building or changing any UI, not only when planning one."),
        },
    ),
    "rq1b-xs-c0a-224": review(
        "C0_STRUCTURAL_REJECT_NOT_A_CLUSTER_OR_RESULT", "01a04203-246e-7291-a8b8-55be794f4e3c",
        "Technical diagrams.", ["generic-versus-specialist", "near duplicate", "analysis versus diagram mismatch"],
        "Two sources are overlapping broad Mermaid diagram routes, while the data-flow mapper is a bounded static-analysis trace rather than a diagramming peer.",
        {
            "r17m1-ArvindChander-skill-lab-diagramming": ("General editable Mermaid diagram construction.", "Turn a concept, process, algorithm, code path, system architecture, data model, lifecycle, hierarchy, or timeline into a clear editable diagram."),
            "r17m1-SpillwaveSolutions-design-doc-mermaid-unknown": ("Mermaid diagram and documentation generation.", "Create Mermaid diagrams (flowchart, sequence, class, ER, state, C4, architecture) from text or source code."),
            "r17m1-event4u-app-agent-config-dist-agent-src-skills-data-flow-mapper": ("Static code data-flow tracing.", "Your only job is to trace how a specific piece of data moves through the"),
        },
    ),
    "rq1b-xs-c0a-225": review(
        "C0_STRUCTURAL_REJECT_NOT_A_CLUSTER_OR_RESULT", "01a04203-246e-7291-a8b8-55be794f4e3c",
        "Academic writing.", ["near-duplicate broad writing routes", "style/method distinctions only"],
        "All candidates broadly cover drafting, manuscript structure, revision, figures, citations, and review; their differences do not give distinct operational routing contexts.",
        {
            "r17m1-YuanZHAO321-Academic-Writing-unknown": ("Academic and scientific writing coaching.", "Academic and scientific writing coach"),
            "r17m1-Brandon030722-academic-writing-skill-academic-writing": ("Evidence-grounded academic drafting and revision.", "Draft, translate, restructure, revise, shorten, expand, humanize, analyze, and reviewer-audit academic papers"),
            "r16m1-jkitchin-skillz-skills-communication-scientific-writing": ("Scientific writing and communication guidance.", "Comprehensive scientific writing guidance for research papers, grants, and technical documentation."),
        },
    ),
    "rq1b-xs-c0a-226": review(
        "C0_STRUCTURAL_REJECT_NOT_A_CLUSTER_OR_RESULT", "01a04203-2209-7f02-897a-f596a44a8f68",
        "Experimental work.", ["planning versus design selection", "execution-loop lifecycle mismatch"],
        "Research experiment planning, statistical DOE selection, and verifier-driven optimisation occupy different stages and abstractions.",
        {
            "r17m1-yananlong-codex-skills-research-research-experiment-plan": ("Tracked, decisive research experiment planning.", "Convert a concrete research claim into a tracked, decisive experiment plan that works either as a standalone planning artifact or as the experiment stage inside a coordinated research workflow."),
            "r16m1-jkitchin-skillz-skills-scientific-design-of-experiments": ("Statistical design-of-experiments selection and implementation.", "This skill covers classical DOE, Bayesian optimization, model-driven designs, and active learning—helping you choose between batch and sequential strategies, screening and optimization, and exploration and exploitation."),
            "r17m1-event4u-app-agent-config-dist-agent-src-skills-experiment-loop": ("Verifier-driven scalar optimisation loop.", "A bounded **change → commit → evaluate → keep-or-revert** cycle against a"),
        },
    ),
    "rq1b-xs-c0a-227": review(
        "C0_STRUCTURAL_REJECT_NOT_A_CLUSTER_OR_RESULT", "01a04203-2209-7f02-897a-f596a44a8f68",
        "Critical review.", ["near-duplicate scientific reviewers", "generic finished-artifact stress test"],
        "The two paper-review routes substantially overlap and the adversarial-review route is a generic finished-work stress test, not a parallel scientific-review route.",
        {
            "r17m1-yananlong-codex-skills-research-research-paper-review": ("Academic-paper review with OCR and multi-pass critique.", "Run academic paper review with OCR extraction, ChatGPT-native multi-agent critique, local visualization, and section-level review workflows integrated into the research skill suite."),
            "r16m1-jkitchin-skillz-skills-research-scientific-reviewer": ("Comprehensive scientific-document peer review.", "This skill transforms Claude into a rigorous scientific peer reviewer, systematically evaluating research documents across multiple dimensions of scientific quality and integrity."),
            "r17m1-event4u-app-agent-config-dist-agent-src-skills-adversarial-review": ("Generic finished-work adversarial critique.", "Adversarial critique — devil's advocate, stress-test, honest teardown ('poke holes', 'be brutal', 'was hältst du davon'); explicit request only."),
        },
    ),
    "rq1b-xs-c0a-228": review(
        "C0_STRUCTURAL_REJECT_NOT_A_CLUSTER_OR_RESULT", "01a04203-2209-7f02-897a-f596a44a8f68",
        "Product prioritisation.", ["RICE contained by multi-framework route", "stakeholder analysis does not lock choice"],
        "The broad prioritisation framework explicitly contains RICE while stakeholder-tradeoff is a distinct decision-support stage that hands off the final choice.",
        {
            "r16m1-product-on-purpose-pm-skills-skills-define-prioritization-framework": ("Multi-framework product prioritisation.", "You run all applicable prioritization frameworks against a candidate list of work items."),
            "r17m1-event4u-app-agent-config-dist-agent-src-skills-rice-prioritization": ("RICE-only prioritisation.", "RICE = `(Reach × Impact × Confidence) / Effort`."),
            "r17m1-event4u-app-agent-config-dist-agent-src-skills-stakeholder-tradeoff": ("Stakeholder cost-benefit trade-off analysis.", "Do NOT lock the choice in this skill; hand off to"),
        },
    ),
    "rq1b-xs-c0a-229": review(
        "C0_STRUCTURAL_REJECT_NOT_A_CLUSTER_OR_RESULT", "01a04203-2209-7f02-897a-f596a44a8f68",
        "Pre-commit product risk work.", ["explicit container/component relationship", "product-demand versus risk gate"],
        "Premortem explicitly invokes risk-officer for scoring, while build-risk review is a different product-demand triage hub. The candidates are not independent peers.",
        {
            "r16m1-product-on-purpose-pm-skills-skills-foundation-build-risk-review": ("Product build-risk triage and verdict.", "It is a foundation hub: its job is to triage and dispatch, not to duplicate the deeper skills."),
            "r17m1-event4u-app-agent-config-dist-agent-src-skills-premortem": ("Prospective failure analysis container.", "Invoke [`risk-officer`](../risk-officer/SKILL.md) to assign L × I (likelihood"),
            "r17m1-event4u-app-agent-config-dist-agent-src-skills-risk-officer": ("Pre-commit risk identification and scoring.", "Surface risks the implementer or PO is likely to underweight, score"),
        },
    ),
}


def load_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    queue = load_jsonl(QUEUE)
    if set(REVIEWS) != {str(row["proposal_id"]) for row in queue}:
        raise SystemExit("review_queue_identity_mismatch")
    output_rows: list[dict[str, object]] = []
    for queued in queue:
        proposal_id = str(queued["proposal_id"])
        source_review = REVIEWS[proposal_id]
        candidates = [str(item["skill_id"]) for item in queued["candidates"]]
        evidence = source_review["evidence"]
        if set(evidence) != set(candidates):
            raise SystemExit(f"candidate_evidence_identity_mismatch:{proposal_id}")
        output_rows.append({
            "proposal_id": proposal_id,
            "c0b_status": source_review["status"],
            "c0b_reviewer_id": source_review["reviewer"],
            "c0b_review_method": "independent_model_assisted_full_source_review",
            "candidate_skill_ids": candidates,
            "common_envelope_from_sources": source_review["envelope"],
            "candidate_evidence": [
                {"skill_id": skill_id, "first_route": evidence[skill_id][0], "evidence_substrings": [evidence[skill_id][1]]}
                for skill_id in candidates
            ],
            "structural_risks": source_review["risks"],
            "rationale": source_review["rationale"],
            "exclusions": ["no prompt", "no label", "no acceptable set", "no retrieval input", "no model result", "no benchmark-cluster claim"],
        })
    OUTPUT.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in output_rows), encoding="utf-8")
    print(f"wrote:{OUTPUT}:{len(output_rows)}")


if __name__ == "__main__":
    main()
