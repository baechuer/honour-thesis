#!/usr/bin/env python3
"""Generate one deterministic, contamination-free v1.2 background-skill batch.

This writes only the new versioned source overlay. It never mutates the frozen
v1.1 corpus, assigns text to subagents, or runs retrieval/model providers.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from generate_background_scale_skills import (
    ADDITIONAL_DOMAIN_CLUSTERS,
    BACKGROUND_SKILLS,
    DOMAIN_CLUSTERS,
    PROCEDURE_TEMPLATES,
    bullet_lines,
    titleize,
)


VERSION_ID = "rq2b-full-library-v1.2-2026-08-16"
RELATIVE_ROOT = f"skill_benchmark/rq2b_full_library/{VERSION_ID}"
DEFAULT_OUTPUT = f"{RELATIVE_ROOT}/source_overlay/background_scale"
DEFAULT_BATCH_ROOT = f"{RELATIVE_ROOT}/source_overlay_generation_batches"
BATCH_SIZE = 100
BANNED_PATTERNS = {
    "benchmark_scale_explanation": r"background scale skill|retrieval pressure",
    "benchmark_gold_label": r"gold-label core benchmark skill|core benchmark skill",
    "benchmark_confusability": r"neighboring confusable skill|neighboring skill",
    "benchmark_artifact_reference": r"expected artifact below",
    "benchmark_switch_rule": r"do not silently switch to a more specific benchmark core skill",
}

WORKFLOW_BY_SUFFIX = {
    "intake-classifier": [
        "Separate the request into its material type, stated objective, urgency, and owner cues.",
        "Apply the available category and routing criteria.",
        "Record missing context that prevents a confident route.",
        "Return the classification and the immediate next action.",
    ],
    "field-extractor": [
        "Locate the requested fields and their supporting evidence in the source material.",
        "Capture values with their source locations and identify ambiguous values.",
        "Normalise values only against the stated target schema.",
        "Return the structured table with evidence and uncertainty notes.",
    ],
    "evidence-grounder": [
        "List the claims that require evidence.",
        "Match each claim to the most relevant source passage or record.",
        "Classify support as direct, partial, unsupported, or uncertain.",
        "Return the claim-evidence map with limitations.",
    ],
    "risk-reviewer": [
        "Identify concrete risks in the supplied material.",
        "Estimate impact and likelihood using the available evidence.",
        "Connect each material risk to a mitigation or an owner question.",
        "Return a prioritised risk register.",
    ],
    "summary-writer": [
        "Read the supplied material for decisions, facts, open questions, and caveats.",
        "Group the most consequential points for the named audience.",
        "Separate confirmed information from assumptions and gaps.",
        "Write a concise summary with action-relevant detail.",
    ],
    "rewrite-editor": [
        "Identify the intended audience, tone, and non-negotiable constraints in the draft.",
        "Revise wording and structure while preserving the source meaning.",
        "Check that factual claims and constraints remain intact.",
        "Return the revised text and material preservation notes.",
    ],
    "comparison-builder": [
        "Identify the items and criteria that make the comparison meaningful.",
        "Extract comparable evidence for each criterion.",
        "Surface material differences, trade-offs, and missing evidence.",
        "Return the comparison table with bounded recommendation notes.",
    ],
    "compliance-checker": [
        "Map the supplied material to the stated policy, rule set, or acceptance criteria.",
        "Mark each requirement as met, unmet, unclear, or unsupported.",
        "Attach evidence and remediation detail to each failure.",
        "Return compliance status and the correction list.",
    ],
    "timeline-builder": [
        "Extract dated events, ordering cues, dependencies, and unresolved timing gaps.",
        "Place events in chronological order without inventing missing dates.",
        "Flag conflicts, dependencies, and uncertain sequence points.",
        "Return the dated timeline and gap list.",
    ],
    "priority-ranker": [
        "List the candidate items and the applicable ranking criteria.",
        "Assess each item against urgency, impact, effort, dependency, and available evidence.",
        "Make sensitivity to uncertain criteria explicit.",
        "Return the ranked list with rationale.",
    ],
    "quality-auditor": [
        "Compare the artifact against its expected structure and quality criteria.",
        "Identify missing, inconsistent, malformed, or unsupported elements.",
        "Distinguish blocking defects from minor improvements.",
        "Return findings with a correction checklist.",
    ],
    "handoff-brief-writer": [
        "Collect the current state, completed work, decisions, constraints, and open issues.",
        "Identify the next owner and the work needed for a safe continuation.",
        "Structure the brief so unresolved assumptions are visible.",
        "Return the handoff brief with acceptance criteria.",
    ],
    "normalizer": [
        "Identify the target naming, schema, format, or taxonomy.",
        "Map source values to canonical values and retain unmapped exceptions.",
        "Check the transformed artifact for consistency.",
        "Return the normalised artifact and mapping notes.",
    ],
    "dependency-mapper": [
        "Identify prerequisites, dependent items, resources, owners, and downstream effects.",
        "Connect each dependency to the evidence that establishes it.",
        "Flag cycles, missing owners, and high-risk dependencies.",
        "Return the dependency map with risk notes.",
    ],
    "scenario-planner": [
        "State the decision, assumptions, and uncertainty drivers.",
        "Develop bounded alternative scenarios from the available constraints.",
        "Identify outcomes, risks, and triggers for each scenario.",
        "Return the scenario table and decision triggers.",
    ],
    "monitoring-plan-builder": [
        "Define the signals that indicate healthy, degraded, or unsafe operation.",
        "Set measurable thresholds, review cadence, and escalation ownership.",
        "Connect each alert to a practical response action.",
        "Return the monitoring plan and escalation rules.",
    ],
    "artifact-packager": [
        "Identify the audience, required format, and materials that belong in the delivery.",
        "Organise files and sections into a usable delivery order.",
        "Check naming, dependencies, and missing deliverables.",
        "Return the package outline and delivery checklist.",
    ],
    "resource-linker": [
        "Identify resources, references, files, systems, and evidence relevant to the task.",
        "Explain the purpose and limits of each selected resource.",
        "Associate an owner or usage note where available.",
        "Return the resource map.",
    ],
    "failure-diagnoser": [
        "Collect the failed output, expected outcome, and available evidence.",
        "Classify the observed mismatch and trace plausible contributing causes.",
        "Separate established causes from hypotheses needing verification.",
        "Return corrective actions with evidence links.",
    ],
    "acceptance-test-builder": [
        "Translate stated behaviour and constraints into observable acceptance conditions.",
        "Define representative, edge-case, and failure inputs.",
        "State expected outcomes and verification evidence for each case.",
        "Return the acceptance-test set.",
    ],
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def generated_skills() -> list[dict[str, Any]]:
    generated: list[dict[str, Any]] = []
    for domain in [*DOMAIN_CLUSTERS, *ADDITIONAL_DOMAIN_CLUSTERS]:
        for procedure in PROCEDURE_TEMPLATES:
            suffix = procedure["suffix"]
            generated.append({
                "name": f"{domain['prefix']}-ops-{suffix}",
                "description": procedure["description"].format(**domain),
                "use": procedure["use"].format(**domain),
                "precondition": procedure["precondition"].format(**domain),
                "input": domain["input"],
                "dependencies": [*domain["dependencies"], "task-specific constraints"],
                "workflow": WORKFLOW_BY_SUFFIX[suffix],
                "output": procedure["output"].format(**domain),
            })
    return generated


def all_skills() -> list[dict[str, Any]]:
    baseline = [dict(skill) for skill in BACKGROUND_SKILLS]
    result = [*baseline, *generated_skills()]
    names = [skill["name"] for skill in result]
    if len(result) != 1800 or len(names) != len(set(names)):
        raise ValueError("v1.2 background inventory must contain 1800 unique skills")
    return result


def render(skill: dict[str, Any]) -> str:
    sections = [
        "---",
        f"name: {skill['name']}",
        f"description: {skill['description']}",
        "---",
        "",
        f"# {titleize(skill['name'])}",
        "",
        "## Use when",
        "",
        f"- {skill['use']}",
        "",
        "## Input and preconditions",
        "",
        f"- {skill.get('precondition', 'The required task material and expected output are available.')}",
    ]
    if skill.get("input"):
        sections.append(f"- Relevant material: {skill['input']}.")
    if skill.get("dependencies"):
        sections.extend(["", "## Dependencies and resources", "", bullet_lines(skill["dependencies"])])
    if skill.get("workflow"):
        sections.extend(["", "## Procedure", ""])
        sections.extend(f"{index}. {step}" for index, step in enumerate(skill["workflow"], start=1))
    sections.extend(["", "## Output", "", skill["output"], ""])
    return "\n".join(sections)


def lint(text: str) -> list[str]:
    return [name for name, pattern in BANNED_PATTERNS.items() if re.search(pattern, text, flags=re.IGNORECASE)]


def generate(root: Path, output_dir: Path, batch_root: Path, batch_index: int, batch_size: int) -> dict[str, Any]:
    skills = all_skills()
    start = batch_index * batch_size
    selected = skills[start : start + batch_size]
    if not selected:
        raise ValueError("Requested v1.2 batch is outside the 1800-skill inventory")
    output_dir.mkdir(parents=True, exist_ok=True)
    batch_root.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    recovered_existing = 0
    for inventory_index, skill in enumerate(selected, start=start):
        path = output_dir / skill["name"] / "SKILL.md"
        text = render(skill)
        failures = lint(text)
        if failures:
            raise ValueError(f"v1.2 scaffold lint failed for {skill['name']}: {failures}")
        if path.exists():
            if path.read_text(encoding="utf-8") != text:
                raise ValueError(f"Refusing to recover non-deterministic existing v1.2 source: {path}")
            recovered_existing += 1
        else:
            path.parent.mkdir(parents=True, exist_ok=False)
            path.write_text(text, encoding="utf-8")
        rows.append({
            "inventory_index": inventory_index,
            "skill_id": skill["name"],
            "path": path.relative_to(root).as_posix(),
            "sha256": sha256_file(path),
            "utf8_bytes": len(text.encode("utf-8")),
            "scaffold_lint_failures": failures,
        })
    manifest_path = batch_root / f"batch_{batch_index:03d}.json"
    if manifest_path.exists():
        raise FileExistsError(f"Refusing to overwrite frozen batch manifest: {manifest_path}")
    manifest = {
        "schema_version": "rq2b-v12-background-source-batch-v1",
        "version_id": VERSION_ID,
        "batch_index": batch_index,
        "batch_size": batch_size,
        "inventory_index_start": start,
        "inventory_index_end": start + len(selected) - 1,
        "rows": rows,
        "network_calls": 0,
        "external_api_calls": 0,
        "recovered_existing_sources": recovered_existing,
        "subagent_source_assignment": False,
        "scientific_retrieval_or_reranking": False,
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"batch_manifest": manifest_path.relative_to(root).as_posix(), "rows": len(rows), "first_skill": rows[0]["skill_id"], "last_skill": rows[-1]["skill_id"], "recovered_existing_sources": recovered_existing, "network_calls": 0, "external_api_calls": 0}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--batch-index", type=int, required=True)
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--batch-root", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    output_dir = args.output_dir or root / DEFAULT_OUTPUT
    batch_root = args.batch_root or root / DEFAULT_BATCH_ROOT
    result = generate(root, output_dir, batch_root, args.batch_index, args.batch_size)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
