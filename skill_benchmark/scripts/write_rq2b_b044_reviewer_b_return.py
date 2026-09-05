#!/usr/bin/env python3
"""Write Reviewer B's independent, source-native B044 decisions."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2] / "skill_benchmark/rq2b_naturalistic_confusability/review/source_native_data_ml_ai_evaluation_data_engineering_databases_security_privacy_observability_b044_2026-09-04/batch_044_full_source_review_packets"
PACKET = ROOT / "reviewer_b_packet.jsonl"
OUTPUT = ROOT / "reviewer_b_return.jsonl"
VALID_DECISIONS = {
    "PASS_TO_PROMPT_AUTHORING", "REJECT_TOPIC_ONLY", "REJECT_COMPONENT_OR_COMPOSITION",
    "REJECT_GENERIC_SPECIALIST", "REJECT_NEAR_DUPLICATE_OR_FORK",
    "REJECT_NO_BOUNDED_ENVELOPE", "REJECT_NO_MEMBER_LEVEL_PROMPTABILITY",
    "DEFER_PROVENANCE_OR_LICENSE", "DEFER_INSUFFICIENT_SOURCE_EVIDENCE",
}


def row(token, decision, common, s1, s2, s3, rationale):
    return {
        "record_type": "source_native_full_source_family_review_return",
        "family_token": token,
        "decision": decision,
        "common_envelope_evidence": common,
        "member_contrast_evidence": {"S-1": s1, "S-2": s2, "S-3": s3},
        "rationale": rationale,
    }


RETURNS = [
    row("F-31bd4f7f28d08de4", "PASS_TO_PROMPT_AUTHORING",
        ["All three sources address Grafana Cloud metric-volume cost investigation: Adaptive Metrics says it reduces active-series billing, Cost Management says it reduces telemetry spend, and dpm-finder ranks metrics driving the bill."],
        ["S-1 applies aggregation rules and measures `grafanacloud_instance_active_series` before/after."],
        ["S-2 adds cost-attribution labels and addresses metrics, logs, traces, and quota alerts."],
        ["S-3 performs a DPM scan and ranks metrics with per-label-set breakdown."],
        "A bounded Grafana Cloud telemetry-cost objective is shared, while the sources support distinct remediation, cross-signal cost-management, and diagnostic-analysis routes."),
    row("F-ab89b92bcb336fb9", "REJECT_NEAR_DUPLICATE_OR_FORK",
        ["Each source returns a " + '"Monitoring plan with signals, thresholds, cadence, owners, and escalation rules."'],
        ["S-1 procedure begins " + '"Define the signals that indicate healthy, degraded, or unsafe operation."'],
        ["S-2 uses the same first procedure step: " + '"Define the signals that indicate healthy, degraded, or unsafe operation."'],
        ["S-3 repeats the same procedure and output, changing only the operational domain and listed materials."],
        "The three sources have the same procedure and deliverable; their domain nouns and input examples do not establish independent operational routes."),
    row("F-4673960f7254d6f3", "PASS_TO_PROMPT_AUTHORING",
        ["The three titles and introductions concern Node/TypeScript relational-SQL data access with queries, migrations, and database support."],
        ["S-1 defines entities with decorators and uses TypeORM `QueryBuilder`."],
        ["S-2 provides a chainable query-builder API with direct SQL control rather than a full ORM."],
        ["S-3 defines Sequelize models and associations in a promise-based ORM."],
        "The sources share a bounded application data-layer task and substantively distinguish decorator ORM, SQL builder, and model/association ORM operations."),
    row("F-c33da344a6c45a5a", "PASS_TO_PROMPT_AUTHORING",
        ["Each source is a " + '"Full Sentry SDK setup"' + " for a client application and covers error monitoring, tracing, profiling, session replay, and logging."],
        ["S-1 explicitly supports Kotlin and Java Android codebases and checks Gradle/AGP configuration."],
        ["S-2 explicitly supports Flutter and Dart and checks `pubspec.yaml` packages and Flutter integrations."],
        ["S-3 explicitly supports Apple platforms and checks SwiftUI/UIKit plus Cocoa dependency mechanisms."],
        "The common SDK-integration objective is bounded, and platform/toolchain-specific setup procedures make the three routes operationally distinct."),
    row("F-df5a32a79b4c2115", "REJECT_TOPIC_ONLY",
        ["The sources sit in the broad ML-operations area but name different artifacts: " + '"Model Evaluation Report," "Data Drift Monitor," and "Experiment Tracking."'],
        ["S-1 fixes a primary metric, establishes baselines, quantifies uncertainty, and writes a report."],
        ["S-2 classifies drift, selects statistical tests, and sets alert/retraining gates."],
        ["S-3 defines run-logging schema, naming, reproducibility, comparison, and promotion workflow."],
        "The material establishes related subject matter, not one bounded objective with three first-route alternatives."),
    row("F-8ab7529911152452", "REJECT_GENERIC_SPECIALIST",
        ["All mention semantic-data queries, but the scopes are materially asymmetric."],
        ["S-1 routes general SQL, SPARQL, SPASQL, SPARQL-FED, and GraphQL requests against live data spaces."],
        ["S-2 is specifically a URIBurner MCP Server toolkit with native MCP query tools."],
        ["S-3 is Virtuoso technical support and database management, including RDF Views generation and instance selection."],
        "The general query router is not a peer first-route alternative to the product-specific MCP toolkit and Virtuoso support/administration source."),
    row("F-32bacee5332ad6a8", "PASS_TO_PROMPT_AUTHORING",
        ["All three sources explicitly maintain persistent context across agent sessions through retained decisions, task history, or retrieved memory."],
        ["S-1 mandates the Gemini bot `lessons-learned.md` Task Ledger and Decision Log."],
        ["S-2 installs claude-mem hooks that capture, compress, store, and retrieve Claude Code session memory."],
        ["S-3 specifies version-controlled `DECISIONS.md`, `ARCHITECTURE.md`, and session-scoped working memory."],
        "The shared persistence objective is bounded and the sources specify distinct platform-bound storage and retrieval mechanisms."),
    row("F-c8af3b6173324a3d", "REJECT_TOPIC_ONLY",
        ["The titles concern offensive-security work but designate different activities: Metasploit penetration testing, Kubernetes red teaming, and Hashcat password recovery."],
        ["S-1's core workflow includes exploit selection and payload configuration."],
        ["S-2 centers Kubernetes attack surfaces and reconnaissance from a compromised pod."],
        ["S-3 centers hash identification and password-cracking workflow."],
        "A broad security-testing topic does not provide one bounded task envelope across exploitation, cluster assessment, and password recovery."),
    row("F-4b735153b1fc0ce1", "PASS_TO_PROMPT_AUTHORING",
        ["All sources provide LLM observability with tracing and evaluation of AI applications."],
        ["S-1 LangSmith covers tracing, datasets/examples, and trace-derived datasets."],
        ["S-2 Langtrace provides OpenTelemetry auto-instrumentation and a self-hostable dashboard."],
        ["S-3 Langfuse covers tracing, prompt management, and evaluation datasets."],
        "The sources share an LLM observability objective and present distinct, source-supported platform workflows."),
    row("F-6d6dc47c3c7f53d0", "PASS_TO_PROMPT_AUTHORING",
        ["The sources each provision and operate a managed cloud SQL database, including creation, network configuration, recovery, or production settings."],
        ["S-1 creates GCP Cloud SQL PostgreSQL/MySQL instances and configures Private IP/read replicas."],
        ["S-2 creates AWS RDS subnet groups and production Multi-AZ databases with Secrets Manager credentials."],
        ["S-3 creates Azure SQL servers/databases and configures Azure AD-only authentication."],
        "A managed-cloud relational database setup is a bounded common objective; provider-specific resource and identity workflows supply the contrast."),
    row("F-573ac2cb98d32406", "PASS_TO_PROMPT_AUTHORING",
        ["Each source describes a backend-as-a-service workflow with authentication, database operations, file storage, and server-side functionality."],
        ["S-1 Nhost uses a Docker local project and auto-generated GraphQL from PostgreSQL."],
        ["S-2 Firebase uses CLI initialization with Firestore, Functions, Hosting, Storage, and Emulators."],
        ["S-3 Appwrite uses self-hosted Docker deployment plus database, functions, and realtime subscriptions."],
        "The common backend-service objective is bounded, while deployment and data/API models provide three distinct operational routes."),
    row("F-ded070c267b483ec", "PASS_TO_PROMPT_AUTHORING",
        ["All three sources create or execute analytics over tabular data using a named analytical data system or language."],
        ["S-1 MotherDuck combines local and cloud DuckDB execution and persists/share cloud databases."],
        ["S-2 Ibis supplies a pandas-like Python API that generates SQL across multiple backends."],
        ["S-3 Malloy defines reusable semantic data models and composable analytics queries."],
        "The sources share a bounded analytics-query/modeling envelope and distinguish hybrid DuckDB, portable Python, and semantic-language workflows."),
    row("F-c120116a7d5cfa27", "REJECT_COMPONENT_OR_COMPOSITION",
        ["The malware-analysis sources include YARA as one capability, while the third source is dedicated to writing YARA rules."],
        ["S-1 lists " + '"YARA Rule Generation"' + " alongside static, dynamic, and family analysis."],
        ["S-2 performs static triage and dynamic analysis before a capability model."],
        ["S-3 is titled " + '"Writing YARA Rules"' + " and focuses on rule anatomy, conditions, testing, and false positives."],
        "Rule authoring is a possible downstream component of malware analysis rather than a peer alternative to the full analysis workflows."),
    row("F-30531f7a391a1d33", "REJECT_NEAR_DUPLICATE_OR_FORK",
        ["S-1 and S-3 both explicitly identify Phoenix as the open-source AI-observability implementation."],
        ["S-1 is titled " + '"Phoenix - AI Observability Platform"' + " and calls it open-source observability and evaluation."],
        ["S-2 is LangSmith, with its own tracing/evaluation/monitoring platform."],
        ["S-3 is titled " + '"Arize (Phoenix) — AI Observability Platform"' + " and instructs use of Phoenix for local development."],
        "Two members materially duplicate the Phoenix route, so the triad does not supply three independent routes."),
    row("F-9ece164b89f53aa0", "REJECT_NEAR_DUPLICATE_OR_FORK",
        ["All sources use NIST CSF 2.0, but two are overlapping control-mapping instructions rather than separate routes."],
        ["S-1 performs a CSF 2.0 gap assessment with Current/Target Profiles and Implementation Tiers."],
        ["S-2 says " + '"Map security implementations to NIST CSF 2.0 framework functions and categories."'],
        ["S-3 likewise says " + '"Map security implementations"' + " across Hack23 projects to NIST CSF 2.0 functions and categories."],
        "The two mapping sources duplicate the same operational route; the assessment source does not restore three independent alternatives."),
    row("F-152b21e26968c0a2", "REJECT_GENERIC_SPECIALIST",
        ["The family ranges from an end-to-end analytics workflow to EDA and a narrow agent wrapper."],
        ["S-1 covers raw ingestion and cleaning through statistical testing, visualization, and executive reporting."],
        ["S-2 is explicitly " + '"Q-EDA"' + " with a checklist and pipeline."],
        ["S-3 is a " + '"Data Analysis Agent"' + " with fixed inputs and a `.run(...)` invocation."],
        "The broad analytics source subsumes a specialist EDA stage and an implementation-specific agent wrapper rather than forming peer routes."),
    row("F-3e33a80ca51ed4b3", "REJECT_TOPIC_ONLY",
        ["The sources expose different life-science repositories: PRIDE, EMDB, and PDB."],
        ["S-1 searches proteomics projects and lists project files."],
        ["S-2 searches electron-microscopy entries, map headers, downloads, and fitted models."],
        ["S-3 searches atomic protein structures and sequence similarity."],
        "These are related scientific databases, but their source-defined data objects and retrieval tasks do not form one bounded operational envelope."),
    row("F-1a4a1d868fda0728", "REJECT_GENERIC_SPECIALIST",
        ["All concern `llms.txt`, but the CLI generator subsumes the create/update directives."],
        ["S-1 is specifically " + '"Create LLMs.txt File from Repository Structure."'],
        ["S-2 is specifically " + '"Update LLMs.txt File"' + " with change detection."],
        ["S-3 exposes `/llms-txt generate`, `/llms-txt audit`, and `/llms-txt update`."],
        "The third source is a broad generator covering the first two action categories, not an independent peer route."),
    row("F-0458a1bf065bda98", "REJECT_COMPONENT_OR_COMPOSITION",
        ["The RDF sources describe generation followed by a separate Virtuoso bulk-load step."],
        ["S-1 produces RDF DET variants."],
        ["S-2 produces RDF DET from CSV."],
        ["S-3 is a " + '"Virtuoso RDF Bulk Loader"' + " that generates `isql` load SQL from a source folder."],
        "Bulk-loading the generated RDF is a subsequent pipeline component, not a peer alternative to the two generation sources."),
    row("F-b5c3a0d707d0e585", "PASS_TO_PROMPT_AUTHORING",
        ["All three sources produce a threat-model assessment from application/security architecture information using an explicit framework."],
        ["S-1 decomposes the application and identifies/classifies threats with STRIDE."],
        ["S-2 runs PASTA's seven stages from objectives and technical scope through residual risk."],
        ["S-3 scores and prioritizes threats with DREAD and returns a Markdown threat model."],
        "Threat modelling is a bounded common objective, and the framework-specific analysis and output procedures are operationally distinct."),
    row("F-13a643ac44ca8610", "REJECT_NEAR_DUPLICATE_OR_FORK",
        ["S-2 and S-3 are both DuckDB sources describing the same embedded analytical-SQL/file-query route."],
        ["S-1 uses embedded ClickHouse `chdb.query()`, Session, or DB-API APIs."],
        ["S-2 is titled " + '"DuckDB"' + " and calls it an embeddable SQL OLAP database querying CSV, Parquet, and JSON directly."],
        ["S-3 is titled " + '"DuckDB - The SQL Engine for Scientific Data"' + " and likewise describes in-process analytical SQL over Pandas/Polars and CSV/Parquet."],
        "The two DuckDB members duplicate one product route; a distinct chDB member does not create a three-route family."),
    row("F-e25f232927799ed3", "REJECT_COMPONENT_OR_COMPOSITION",
        ["The sources place an analytics workflow within notebook tooling/guidance rather than offering three peer implementations."],
        ["S-1 is titled " + '"Python Analytics"' + " and contains only references."],
        ["S-2's example is " + '"Build an exploratory data analysis notebook"' + " and covers Jupyter usage."],
        ["S-3 provides " + '"Notebook Guidance"' + " including kernel/environment management and data-analysis rules."],
        "Notebook guidance and the Jupyter environment support the analytics activity; the sources do not establish three independent first-route skills."),
    row("F-3db96e598aaada78", "REJECT_NEAR_DUPLICATE_OR_FORK",
        ["Two members have the identical title " + '"Investigating AWS Incidents."'],
        ["S-1 is the Azure incident-investigation source, with Azure Activity Log and Defender for Cloud triage."],
        ["S-2 is " + '"Investigating AWS Incidents"' + " and focuses on preserving evidence and reconstructing the control plane."],
        ["S-3 is also " + '"Investigating AWS Incidents"' + " and adds AWS first-hour triage and CloudTrail deep-dive."],
        "The two AWS incident-investigation members overlap the same product/task route, so the family lacks three independent alternatives."),
    row("F-7c74d9be6cfc680f", "REJECT_COMPONENT_OR_COMPOSITION",
        ["The sources name sequential OpenTelemetry work: instrumentation/configuration, validation, and a Sentry exporter setup."],
        ["S-1 is " + '"OpenTelemetry Instrumentation and Collector Configuration."'],
        ["S-2 is " + '"OpenTelemetry Configuration Validation."'],
        ["S-3 is " + '"Sentry OTel Exporter Setup"' + " and directs writing Collector configuration."],
        "Validation and destination-exporter setup are components of configuring telemetry rather than three substitute first routes."),
    row("F-79583d5b299c5d01", "REJECT_COMPONENT_OR_COMPOSITION",
        ["The sources form a risk-management sequence: score risk/CVSS, then plan remediation."],
        ["S-1 is a " + '"Remediation Planner"' + " with effort scale and plan output."],
        ["S-2 is a " + '"Risk Assessor"' + " that scores likelihood and impact and correlates CVSS."],
        ["S-3 is a " + '"CVSS Scorer"' + " with metric inference and scoring behavior."],
        "Risk and CVSS scoring are inputs to remediation planning, so these are composable stages rather than peer alternatives."),
]


def main() -> int:
    if OUTPUT.exists():
        raise SystemExit(f"refusing to overwrite existing Reviewer B return: {OUTPUT}")
    packet_tokens = [json.loads(line)["family_token"] for line in PACKET.read_text(encoding="utf-8").splitlines() if line]
    return_tokens = [entry["family_token"] for entry in RETURNS]
    if len(packet_tokens) != 25 or len(set(packet_tokens)) != 25 or return_tokens != packet_tokens:
        raise SystemExit("return coverage/order does not exactly match the Reviewer B packet")
    for entry in RETURNS:
        if entry["decision"] not in VALID_DECISIONS:
            raise SystemExit(f"invalid decision: {entry['decision']}")
        if not entry["common_envelope_evidence"] or any(not entry["member_contrast_evidence"][key] for key in ("S-1", "S-2", "S-3")):
            raise SystemExit(f"missing source evidence: {entry['family_token']}")
    OUTPUT.write_text("".join(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n" for entry in RETURNS), encoding="utf-8", newline="\n")
    decisions = {}
    for entry in RETURNS:
        decisions[entry["decision"]] = decisions.get(entry["decision"], 0) + 1
    print(json.dumps({"families": len(RETURNS), "decision_totals": decisions, "reviewer_b_return_sha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest()}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
