#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


FIELDS = [
    "routing_trigger",
    "input_precondition",
    "output_artifact",
    "workflow_procedure",
    "constraints_boundaries",
    "dependencies_tools",
    "resources_references",
    "examples_tests",
    "safety_side_effects",
    "portability_environment",
    "hierarchy_links",
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def is_heuristic_present(status: str) -> bool:
    return status in {"explicit", "extractable"}


def is_model_present(status: str) -> bool:
    return status in {"explicit", "implicit"}


def relation_label(heuristic_status: str, model_status: str) -> str:
    heuristic_present = is_heuristic_present(heuristic_status)
    model_present = is_model_present(model_status)
    if heuristic_present and model_present:
        return "both_present"
    if heuristic_present and not model_present:
        return "heuristic_only"
    if not heuristic_present and model_present:
        return "model_only"
    return "both_missing"


def summarize(heuristic_rows: list[dict[str, Any]], model_rows: list[dict[str, Any]]) -> dict[str, Any]:
    heuristic_by_skill = {row["skill"]: row for row in heuristic_rows}
    model_by_skill = {row["skill"]: row for row in model_rows}
    common_skills = sorted(set(heuristic_by_skill) & set(model_by_skill))
    field_counts: dict[str, Counter[str]] = {field: Counter() for field in FIELDS}
    status_pairs: dict[str, Counter[str]] = {field: Counter() for field in FIELDS}
    evidence_counts: dict[str, Counter[str]] = {field: Counter() for field in FIELDS}
    confidence_sums: dict[str, float] = defaultdict(float)
    confidence_counts: dict[str, int] = defaultdict(int)
    disagreements: list[dict[str, Any]] = []

    for skill in common_skills:
        hrow = heuristic_by_skill[skill]
        mrow = model_by_skill[skill]
        for field in FIELDS:
            hstatus = hrow["fields"][field]["status"]
            mfield = mrow["model_fields"][field]
            mstatus = mfield["status"]
            relation = relation_label(hstatus, mstatus)
            field_counts[field][relation] += 1
            status_pairs[field][f"{hstatus} -> {mstatus}"] += 1
            if is_model_present(mstatus):
                evidence_found = mfield.get("evidence_found") or []
                if evidence_found and all(evidence_found):
                    evidence_counts[field]["all_evidence_found"] += 1
                elif evidence_found and any(evidence_found):
                    evidence_counts[field]["some_evidence_found"] += 1
                else:
                    evidence_counts[field]["no_evidence_found"] += 1
                confidence_sums[field] += float(mfield.get("confidence") or 0.0)
                confidence_counts[field] += 1
            if relation in {"heuristic_only", "model_only"}:
                disagreements.append(
                    {
                        "skill": skill,
                        "origin": hrow.get("origin") or mrow.get("origin"),
                        "field": field,
                        "relation": relation,
                        "heuristic_status": hstatus,
                        "model_status": mstatus,
                        "model_confidence": mfield.get("confidence"),
                        "heuristic_evidence": hrow["fields"][field].get("evidence") or [],
                        "model_evidence": mfield.get("evidence") or [],
                        "model_reason": mfield.get("reason") or "",
                    }
                )

    field_summary: dict[str, Any] = {}
    for field in FIELDS:
        total = sum(field_counts[field].values())
        both_present = field_counts[field]["both_present"]
        both_missing = field_counts[field]["both_missing"]
        heuristic_only = field_counts[field]["heuristic_only"]
        model_only = field_counts[field]["model_only"]
        field_summary[field] = {
            "total": total,
            "both_present": both_present,
            "both_missing": both_missing,
            "heuristic_only": heuristic_only,
            "model_only": model_only,
            "agreement": both_present + both_missing,
            "agreement_pct": round((both_present + both_missing) / total, 4) if total else 0,
            "heuristic_only_pct": round(heuristic_only / total, 4) if total else 0,
            "model_only_pct": round(model_only / total, 4) if total else 0,
            "avg_present_confidence": round(confidence_sums[field] / confidence_counts[field], 3)
            if confidence_counts[field]
            else None,
            "evidence_counts": dict(evidence_counts[field]),
            "status_pairs": dict(status_pairs[field].most_common()),
        }
    return {
        "skills_compared": len(common_skills),
        "field_summary": field_summary,
        "disagreements": disagreements,
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Public Skill Field Audit Agreement Report",
        "",
        "This report compares the deterministic heuristic field audit with model-assisted semantic extraction.",
        "",
        f"- Skills compared: {summary['skills_compared']}",
        "",
        "Interpretation:",
        "",
        "- `both_present`: stronger evidence that the field exists in the public skill.",
        "- `heuristic_only`: likely keyword/heading false positive, or model false negative.",
        "- `model_only`: likely semantic false negative in the heuristic audit.",
        "- `both_missing`: likely missing/proposed field.",
        "",
        "## Field Agreement",
        "",
        "| Field | Agreement | Both Present | Both Missing | Heuristic Only | Model Only | Avg Model Confidence |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for field, data in summary["field_summary"].items():
        confidence = data["avg_present_confidence"]
        confidence_text = "" if confidence is None else f"{confidence:.3f}"
        lines.append(
            f"| `{field}` | {data['agreement_pct']:.1%} | {data['both_present']} | "
            f"{data['both_missing']} | {data['heuristic_only']} | {data['model_only']} | {confidence_text} |"
        )

    lines.extend(["", "## Model Evidence Check", ""])
    lines.append("| Field | Evidence Found For Model-Present Labels |")
    lines.append("|---|---|")
    for field, data in summary["field_summary"].items():
        evidence_counts = data["evidence_counts"]
        if not evidence_counts:
            text = "no model-present labels"
        else:
            text = ", ".join(f"{key}: {value}" for key, value in evidence_counts.items())
        lines.append(f"| `{field}` | {text} |")

    disagreements = summary["disagreements"]
    lines.extend(["", "## Disagreement Cases For Manual Review", ""])
    if not disagreements:
        lines.append("No heuristic/model disagreements in the compared set.")
    else:
        lines.append("| Skill | Field | Type | Heuristic | Model | Model Evidence | Model Reason |")
        lines.append("|---|---|---|---|---|---|---|")
        for item in disagreements[:80]:
            evidence = " / ".join(item["model_evidence"]).replace("|", "\\|")[:220]
            reason = item["model_reason"].replace("|", "\\|")[:180]
            lines.append(
                f"| `{item['skill']}` | `{item['field']}` | `{item['relation']}` | "
                f"`{item['heuristic_status']}` | `{item['model_status']}` | {evidence} | {reason} |"
            )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Compare heuristic and model-assisted public skill field audits.")
    parser.add_argument("--heuristic-jsonl", default=str(repo_root / "outputs" / "public_skill_field_audit.jsonl"))
    parser.add_argument("--model-jsonl", default=str(repo_root / "outputs" / "public_skill_field_model_audit.jsonl"))
    parser.add_argument("--output-json", default=str(repo_root / "outputs" / "public_skill_field_agreement_report.json"))
    parser.add_argument("--output-md", default=str(repo_root / "outputs" / "public_skill_field_agreement_report.md"))
    args = parser.parse_args()

    heuristic_rows = load_jsonl(Path(args.heuristic_jsonl))
    model_rows = load_jsonl(Path(args.model_jsonl))
    if not heuristic_rows:
        raise SystemExit(f"No heuristic rows found at {args.heuristic_jsonl}")
    if not model_rows:
        raise SystemExit(f"No model rows found at {args.model_jsonl}")

    summary = summarize(heuristic_rows, model_rows)
    output_json = Path(args.output_json)
    output_md = Path(args.output_md)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    output_md.write_text(render_markdown(summary), encoding="utf-8")
    print(f"Compared skills: {summary['skills_compared']}")
    print(f"Wrote {output_json}")
    print(f"Wrote {output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
