#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path


MAIN_ROOT = Path(__file__).resolve().parent.parent / "skills"


FAMILY_DEFAULT_PRECONDITIONS = {
    "browser_web_automation": [
        "The target page, route, or flow is available, described, or can be opened in a browser-like environment.",
        "The user has stated whether the goal is observation, interaction, testing, extraction, debugging, or accessibility review.",
    ],
    "code_github_workflow": [
        "The user provides code, a diff, PR context, CI output, review comments, or a completed-change summary.",
        "The requested artifact is clear: review findings, fixes, debugging notes, changelog text, or release notes.",
    ],
    "data_spreadsheet": [
        "The user provides a spreadsheet, CSV, table, or tabular summary.",
        "The user has an analysis goal such as overview, validation, anomaly detection, diagnosis, reporting, ranking, or forecasting.",
    ],
    "documents_files": [
        "The user provides one or more documents, document excerpts, forms, PDFs, policies, invoices, or practical files.",
        "The desired artifact is clear: summary, structured extraction, rewrite, normalization, conversion, or comparison.",
    ],
    "metrics_observability": [
        "The user provides service metrics, dashboard values, incident notes, or operational observations.",
        "The user indicates whether they need current-state summary, anomaly detection, SLO judgment, forecast, root cause, or incident communication.",
    ],
    "news_monitoring": [
        "The user provides one or more news items, snippets, articles, or source summaries.",
        "The user indicates whether they need recap, briefing, grounded facts, themes, or trend signal.",
    ],
    "planning_meetings": [
        "The user provides notes, obligations, tasks, meeting context, or planning constraints.",
        "The user indicates whether the target is before a meeting, after a meeting, task extraction, or week-level planning.",
    ],
    "reading_research": [
        "The user provides one or more sources, paper excerpts, notes, claims, or research summaries.",
        "The user indicates the intended research use: understanding, citation, method comparison, grounding, or synthesis.",
    ],
    "reply_messaging": [
        "The user provides message context, recipient context, or an existing draft reply.",
        "The user indicates whether the goal is a fresh draft, refinement, academic reply, group coordination, or follow-up commitment.",
    ],
    "security_appsec": [
        "The user provides a feature design, code path, dependency context, diff, auth flow, logs, or data-handling description.",
        "The user indicates whether the concern is threat modeling, code vulnerability, dependency risk, secrets, auth, or privacy.",
    ],
    "skill_lifecycle": [
        "The user provides a skill need, existing skill, public source, installed library, or packaging target.",
        "The user indicates whether the operation is find, install, create, edit, evaluate, or package.",
    ],
}


REFINEMENTS: dict[str, dict[str, list[str]]] = {
    "accessibility-checker": {
        "output": ["Accessibility findings grouped by severity.", "Affected element or interaction.", "Suggested fix or verification step."],
    },
    "frontend-debugger": {
        "output": ["Observed symptom.", "Evidence from UI, console, network, DOM, or code.", "Likely cause.", "Smallest fix and verification."],
    },
    "web-data-extractor": {
        "output": ["Structured table or field list.", "Source/page reference for extracted values.", "Missing or ambiguous fields."],
    },
    "web-form-filler": {
        "output": ["Completed interaction steps.", "Values entered or choices made.", "Blockers or confirmations required before submission."],
    },
    "web-page-snapshotter": {
        "output": ["Page-state report.", "Key visible content or layout evidence.", "Screenshots or blockers when relevant."],
    },
    "web-ui-tester": {
        "output": ["Tested behavior.", "Expected versus actual result.", "Pass/fail/blocked status.", "Reproduction steps and evidence."],
    },
    "changelog-writer": {
        "output": ["Changelog bullets grouped by change type.", "User-facing or developer-facing impact.", "Breaking changes or caveats when supported."],
    },
    "ci-failure-debugger": {
        "output": ["Failing command or job.", "First meaningful error.", "Likely root cause.", "Minimal fix and verification command."],
    },
    "code-reviewer": {
        "output": ["Prioritized review findings.", "Evidence or file/code reference.", "Severity and missing-test risk.", "Residual risk summary."],
    },
    "pr-reviewer": {
        "output": ["PR review findings ordered by severity.", "Affected files or behavior.", "Test/check gaps.", "Merge risk summary."],
    },
    "release-note-writer": {
        "output": ["User-facing release note sections.", "What changed and why it matters.", "Required user action or caveat when relevant."],
    },
    "review-comment-resolver": {
        "output": ["Resolved review comments.", "Code changes or proposed fixes.", "Verification performed or still needed."],
    },
    "data-analysis-overview": {
        "not_for": ["Validating whether the data can be trusted before use.", "Explaining the cause of a specific spike, drop, or regression.", "Producing a manager-ready report, forecast, or ranking recommendation."],
    },
    "data-analysis-with-validation": {
        "not_for": ["Providing only a broad descriptive overview.", "Explaining the likely cause of a confirmed change.", "Writing a polished report or ranking options."],
    },
    "data-analysis-with-anomaly-focus": {
        "not_for": ["Checking general data trustworthiness without a salient abnormal pattern.", "Explaining root cause after the anomaly is already established.", "Forecasting future outcomes or writing stakeholder report text."],
    },
    "data-analysis-for-root-cause-diagnosis": {
        "not_for": ["Only detecting whether something looks unusual.", "Only validating data quality before interpretation.", "Producing broad overview, forecast, or stakeholder report text."],
    },
    "data-analysis-for-reporting": {
        "not_for": ["Exploring the spreadsheet only for internal understanding.", "Ranking options or making a selection decision.", "Forecasting future outcomes or diagnosing a single root cause as the main output."],
    },
    "data-analysis-for-ranking-selection": {
        "not_for": ["Producing only a broad overview of the table.", "Writing a report without choosing among options.", "Forecasting future values without a selection decision."],
    },
    "data-analysis-for-forecasting": {
        "not_for": ["Summarizing the current state only.", "Explaining why a past change happened.", "Ranking candidates or writing a stakeholder report."],
    },
    "document-summariser": {
        "not_for": ["Extracting targeted fields, values, clauses, dates, or entities.", "Rewriting or polishing the document text.", "Converting file format or preserving layout.", "Comparing multiple documents side by side."],
    },
    "document-field-extractor": {
        "not_for": ["Producing a narrative summary.", "Rewriting the document for tone or clarity.", "Converting the document format.", "Preparing multi-document comparison as the main goal."],
    },
    "document-normaliser": {
        "not_for": ["Changing the meaning, tone, or substantive content.", "Extracting only specific fields.", "Summarizing the document.", "Converting format while preserving layout as the main goal."],
    },
    "document-rewriter": {
        "not_for": ["Producing only a summary.", "Extracting structured fields.", "Converting file formats.", "Normalizing OCR noise without substantive rewriting."],
    },
    "document-converter": {
        "not_for": ["Preserving layout fidelity as the central success criterion.", "Rewriting or improving the content.", "Extracting targeted fields.", "Summarizing the document."],
    },
    "layout-preserving-converter": {
        "not_for": ["Simple conversion where layout does not matter.", "Narrative summary or field extraction.", "Rewriting content for tone or clarity.", "Comparing multiple documents."],
    },
    "multi-document-comparison-preparer": {
        "not_for": ["Single-document summary, extraction, rewrite, or conversion.", "Producing a final argumentative synthesis instead of comparison-ready alignment.", "Changing the documents' content."],
    },
    "metrics-overview": {
        "not_for": ["Determining whether a specific SLO or SLA target is breached.", "Explaining the root cause of a known degradation.", "Forecasting future capacity risk or writing incident update text."],
    },
    "latency-anomaly-detector": {
        "not_for": ["Providing only a broad service-health overview.", "Explaining definitive root cause.", "Checking formal SLO compliance.", "Writing incident communication."],
    },
    "slo-breach-checker": {
        "not_for": ["Detecting unusualness without a target or reliability objective.", "Explaining root cause as the main output.", "Forecasting capacity risk or writing incident summary text."],
    },
    "capacity-risk-forecaster": {
        "not_for": ["Summarizing current state only.", "Checking a current SLO breach only.", "Explaining root cause of a past incident.", "Writing incident update text."],
    },
    "metrics-root-cause-diagnoser": {
        "not_for": ["Only detecting an anomaly.", "Only checking SLO compliance.", "Forecasting future capacity risk.", "Writing stakeholder incident text as the main output."],
    },
    "incident-summary-writer": {
        "not_for": ["Root-cause investigation as the main task.", "SLO calculation as the main task.", "Anomaly detection without communication needs.", "Capacity forecasting."],
    },
    "news-summariser": {
        "output": ["Straightforward recap of the source.", "Main announcement or event.", "Important supporting details and caveats."],
    },
    "news-theme-extractor": {
        "output": ["Recurring themes or topics across sources.", "Evidence snippets for each theme.", "Scope limits or weak signals."],
    },
    "source-grounding-extractor": {
        "output": ["Grounded claims or facts.", "Source linkage or supporting wording.", "Named entities, figures, plans, and qualifiers."],
    },
    "meeting-agenda-builder": {
        "output": ["Meeting objective.", "Agenda items in useful order.", "Discussion prompts, decisions needed, and preparation notes."],
    },
    "meeting-followup-extractor": {
        "output": ["Follow-up actions.", "Owners, deadlines, and dependencies.", "Open questions and next check-in points."],
    },
    "meeting-summary-writer": {
        "output": ["Concise meeting recap.", "Discussion points, decisions, unresolved issues.", "Current status or takeaway."],
    },
    "task-extractor": {
        "output": ["Actionable task list.", "Owner or context when available.", "Deadline, priority, or missing detail when relevant."],
    },
    "weekly-planner": {
        "output": ["Week-level plan.", "Sequenced tasks and time windows.", "Constraints, priorities, and risk buffers."],
    },
    "paper-summariser": {
        "not_for": ["Extracting citation-ready notes as the main output.", "Building method-comparison notes.", "Checking whether a claim is grounded by the source.", "Synthesizing multiple sources into related-work prose."],
    },
    "citation-note-extractor": {
        "not_for": ["Producing a broad paper summary.", "Comparing methods across papers.", "Checking a user's already-written claim for support.", "Writing related-work prose directly."],
    },
    "method-note-builder": {
        "not_for": ["Summarizing the whole paper broadly.", "Extracting citation notes for later prose.", "Checking claim grounding.", "Synthesizing multiple sources into narrative related work."],
    },
    "related-work-synthesiser": {
        "not_for": ["Summarizing one source in isolation.", "Extracting fields or citation notes only.", "Producing side-by-side comparison table as the main output.", "Checking a single claim's source support."],
    },
    "citation-grounding-helper": {
        "not_for": ["Summarizing a paper from scratch.", "Extracting general citation notes.", "Comparing multiple sources.", "Writing full related-work synthesis."],
    },
    "multi-source-comparison-builder": {
        "not_for": ["Summarizing one paper.", "Writing polished related-work prose as the main output.", "Extracting citation notes only.", "Checking one claim against one source."],
    },
    "document-extractor": {
        "not_for": ["Producing a narrative summary.", "Writing citation-ready notes.", "Focusing only on method comparison.", "Synthesizing related work prose."],
    },
    "general-source-summariser": {
        "not_for": ["Using a paper-specific research summary structure when the source is not research.", "Extracting targeted fields only.", "Checking claim grounding.", "Writing synthesis across multiple sources."],
    },
    "followup-reply-writer": {
        "output": ["Reply message.", "Explicit next action or commitment.", "Timing, clarification, or owner when relevant."],
    },
    "groupwork-reply": {
        "output": ["Coordination reply.", "Responsibilities, deadlines, and progress details.", "Tone suitable for teammates."],
    },
    "professor-email-reply": {
        "output": ["Respectful academic email reply.", "Clear answer to the professor or supervisor.", "Professional structure and etiquette."],
    },
    "reply-drafter": {
        "output": ["Fresh sendable reply.", "Appropriate tone for the recipient and context.", "No unsupported commitments."],
    },
    "reply-polisher": {
        "output": ["Polished version of the user's existing draft.", "Preserved meaning, facts, dates, and commitments.", "Improved tone, clarity, and flow."],
    },
    "auth-flow-reviewer": {
        "output": ["Auth-flow findings.", "Bypass or privilege-escalation scenarios.", "Tests or mitigations for risky access-control behavior."],
    },
    "dependency-risk-auditor": {
        "output": ["Dependency risk assessment.", "Confirmed versus unverified package concerns.", "Recommended update, removal, pinning, or monitoring actions."],
    },
    "privacy-risk-reviewer": {
        "output": ["Privacy-risk findings.", "Data collection, retention, sharing, or logging concerns.", "Practical mitigations and open questions."],
    },
    "secret-leak-scanner": {
        "output": ["Potential secret exposures with values redacted.", "Likely source and blast radius.", "Rotation, removal, and history-cleanup recommendations."],
    },
    "security-code-reviewer": {
        "output": ["Concrete security findings tied to code behavior.", "Exploit path or impact.", "Focused fix and verification suggestion."],
    },
    "security-threat-modeler": {
        "output": ["Assets, actors, and trust boundaries.", "Abuse cases and threat scenarios.", "Mitigations, detection, residual risk, and open questions."],
    },
    "skill-creator": {
        "output": ["New skill design or skill folder contents.", "Trigger description, workflow, boundaries, and optional resources.", "Validation notes for atomic scope."],
    },
    "skill-editor": {
        "output": ["Edited skill changes.", "Updated metadata, workflow, boundaries, examples, or resources.", "Reason the edit improves selection or execution."],
    },
    "skill-evaluator": {
        "output": ["Evaluation findings.", "Trigger fit, boundary fit, workflow fit, output fit, and failure modes.", "Recommendation on whether editing is needed."],
    },
    "skill-finder": {
        "output": ["Candidate existing skills.", "Fit assessment and confidence.", "Recommendation to use, reject, edit, install, or create."],
    },
    "skill-installer": {
        "output": ["Installation status.", "Source and installed skill path.", "Verification result and activation caveats."],
    },
    "skill-packager": {
        "output": ["Packaging readiness report.", "Required files, metadata, resource links, and clutter checks.", "Remaining blockers before sharing."],
    },
}


def skill_path(skill_name: str) -> Path | None:
    matches = list(MAIN_ROOT.glob(f"*/*/SKILL.md"))
    for path in matches:
        if path.parent.name == skill_name:
            family = path.parts[-3]
            if family in FAMILY_DEFAULT_PRECONDITIONS:
                return path
    return None


def section_exists(text: str, heading: str) -> bool:
    return f"\n## {heading}\n" in text or text.startswith(f"## {heading}\n")


def bullet_section(heading: str, items: list[str]) -> str:
    bullets = "\n".join(f"- {item}" for item in items)
    return f"## {heading}\n\n{bullets}\n\n"


def insert_before(text: str, marker: str, addition: str) -> str:
    index = text.find(marker)
    if index == -1:
        if not text.endswith("\n"):
            text += "\n"
        return text + "\n" + addition.rstrip() + "\n"
    return text[:index] + addition + text[index:]


def refine_file(path: Path, refinements: dict[str, list[str]]) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    family = path.parts[-3]

    if not section_exists(text, "Not for") and refinements.get("not_for"):
        text = insert_before(text, "## Workflow", bullet_section("Not for", refinements["not_for"]))

    if not section_exists(text, "Preconditions"):
        preconditions = refinements.get("preconditions") or FAMILY_DEFAULT_PRECONDITIONS[family]
        text = insert_before(text, "## Workflow", bullet_section("Preconditions", preconditions))

    has_output = (
        section_exists(text, "Output pattern")
        or section_exists(text, "Default shape")
        or section_exists(text, "Expected output")
    )
    if not has_output and refinements.get("output"):
        text = insert_before(text, "## Writing rules", bullet_section("Output pattern", refinements["output"]))

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    changed = 0
    missing: list[str] = []
    main_skill_paths = {
        path.parent.name: path
        for path in MAIN_ROOT.glob("*/*/SKILL.md")
        if path.parts[-3] in FAMILY_DEFAULT_PRECONDITIONS
    }

    for skill_name in sorted(main_skill_paths):
        refinements = REFINEMENTS.get(skill_name, {})
        path = skill_path(skill_name)
        if path is None:
            missing.append(skill_name)
            continue
        if refine_file(path, refinements):
            changed += 1

    if missing:
        print("Missing skill paths:")
        for name in missing:
            print(f"- {name}")
        raise SystemExit(1)

    print(f"Refined {changed} main evaluated skill files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
