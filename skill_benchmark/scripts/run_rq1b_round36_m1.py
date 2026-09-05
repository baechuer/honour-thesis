#!/usr/bin/env python3
"""Run auditable Round 36 RQ1b source intake through M1 only.

The command has four deliberately narrow modes: ``probe`` pins one public
repository HEAD per fresh M0 root; ``census`` reads the pinned tree without
materialising blobs; ``select`` applies the predeclared tree-path bound; and
``stage`` locally preserves selected original ``SKILL.md`` files and rehashes
them.  No mode executes an acquired file or creates a composition, prompt,
label, selector input, model call, metric, or result.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


ROUND = "36"
DATE = "2026-08-28"
ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "rq1b_cross_source_public_benchmark" / "manifest"
STAGED_ROOT = ROOT / "rq1b_cross_source_public_benchmark" / "staged_sources"
TEMP_ROOT = Path(f"/private/tmp/rq1b-round{ROUND}-m1-{DATE}")
STAGER = ROOT / "scripts" / "stage_rq1b_public_source_set.py"
ORIGINAL_FILE = "SKILL.original.md"
LICENCE_NAMES = ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING", "COPYING.md")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run(command: list[str], *, capture: bool = False) -> str:
    completed = subprocess.run(command, text=True, capture_output=capture, check=True)
    return completed.stdout.strip() if capture else ""


def origin(url: str) -> str:
    parsed = urlsplit(url)
    parts = [part for part in parsed.path.split("/") if part]
    if parsed.scheme != "https" or parsed.netloc != "github.com" or len(parts) != 2:
        raise ValueError(f"not_canonical_github_root:{url}")
    return f"{parts[0]}/{parts[1]}"


def temp_path(item_origin: str) -> Path:
    return TEMP_ROOT / item_origin.replace("/", "--")


def get_tree(item_origin: str, repository_url: str, commit: str) -> Path:
    target = temp_path(item_origin)
    if target.exists():
        actual = run(["git", "-C", str(target), "rev-parse", "FETCH_HEAD"], capture=True)
        if actual != commit:
            raise RuntimeError(f"existing_fetch_head_mismatch:{item_origin}:{actual}:{commit}")
        return target
    target.parent.mkdir(parents=True, exist_ok=True)
    run(["git", "init", "--quiet", str(target)])
    run(["git", "-C", str(target), "remote", "add", "origin", repository_url])
    run(["git", "-C", str(target), "-c", "protocol.version=2", "fetch", "--depth=1", "--filter=blob:none", "origin", commit], capture=True)
    actual = run(["git", "-C", str(target), "rev-parse", "FETCH_HEAD"], capture=True)
    if actual != commit:
        raise RuntimeError(f"pinned_commit_mismatch:{item_origin}:{actual}:{commit}")
    return target


def skill_paths(source_root: Path, commit: str) -> list[str]:
    tree = run(["git", "-C", str(source_root), "ls-tree", "-r", "--name-only", commit], capture=True)
    return [item for item in tree.splitlines() if item == "SKILL.md" or item.endswith("/SKILL.md")]


def root_licence(source_root: Path, commit: str) -> str | None:
    names = set(run(["git", "-C", str(source_root), "ls-tree", "--name-only", commit], capture=True).splitlines())
    return next((name for name in LICENCE_NAMES if name in names), None)


def materialise(source_root: Path, commit: str, paths: list[str]) -> None:
    for start in range(0, len(paths), 80):
        run(["git", "-C", str(source_root), "checkout", commit, "--", *paths[start:start + 80]], capture=True)


def probe(args: argparse.Namespace) -> int:
    m0_rows = read_jsonl(args.m0)
    expected = {str(row["round36_source_candidate_id"]) for row in m0_rows}
    existing = read_jsonl(args.probe_output) if args.probe_output.exists() else []
    prior = {str(row.get("round36_source_candidate_id")): row for row in existing}
    if len(prior) != len(existing) or not set(prior).issubset(expected):
        raise SystemExit("invalid_existing_round36_probe_checkpoint")
    if args.replace_dns_failures:
        # The initial sandbox invocation can fail before any hostname lookup
        # reaches GitHub.  Treat only this uniform environment failure as an
        # unattempted transport error, preserve it in the replacement audit,
        # then permit the same single M1 HEAD probe outside that sandbox.
        dns_failures = [
            row for row in prior.values()
            if row.get("probe_status") == "UNREACHABLE"
            and "Could not resolve host: github.com" in str(row.get("error", ""))
        ]
        if len(dns_failures) != len(prior):
            raise SystemExit("replace_dns_failures_requires_uniform_dns_only_checkpoint")
        args.transport_failure_audit.parent.mkdir(parents=True, exist_ok=True)
        write_json(args.transport_failure_audit, {
            "status": "M1_ROUND36_SANDBOX_DNS_TRANSPORT_FAILURE_SUPERSEDED_BEFORE_NETWORK_PROBE",
            "failure_count": len(dns_failures),
            "reason": "all initial probes failed before hostname resolution; this is not a repository reachability finding",
            "prior_probe_output": str(args.probe_output),
            "excluded_claims": ["No repository-specific non-admission is inferred from this uniform sandbox DNS failure."],
        })
        prior = {}
        args.probe_output.unlink()
    records: list[dict[str, Any]] = []
    sources: list[dict[str, Any]] = []
    new_count = 0
    for position, row in enumerate(m0_rows, start=1):
        identifier = str(row["round36_source_candidate_id"])
        url = str(row["canonical_public_source_url"])
        record = prior.get(identifier)
        if record is None:
            completed = subprocess.run(["git", "ls-remote", url, "HEAD"], text=True, capture_output=True, check=False)
            parts = completed.stdout.strip().split()
            reachable = completed.returncode == 0 and len(parts) == 2 and parts[1] == "HEAD" and len(parts[0]) == 40
            record = {
                "round36_source_candidate_id": identifier,
                "public_url": url,
                "probe_status": "REACHABLE" if reachable else "UNREACHABLE",
                "pinned_commit": parts[0] if reachable else None,
                "error": None if reachable else (completed.stderr.strip() or f"missing_or_invalid_HEAD_or_exit_{completed.returncode}")[:500],
                "m1_probe_status": "M1_HEAD_PINNED_PENDING_TREE_CENSUS_NOT_A_CLUSTER_OR_RESULT" if reachable else "M1_HEAD_PROBE_FAILED_NOT_ADMITTED_NOT_A_CLUSTER_OR_RESULT",
            }
            new_count += 1
        records.append(record)
        write_jsonl(args.probe_output, records)
        if record["probe_status"] == "REACHABLE":
            sources.append({
                "plan_position": position,
                "round36_source_candidate_id": identifier,
                "origin": origin(url),
                "repository_url": url,
                "pinned_commit": record["pinned_commit"],
                "domains": row["domains"],
                "originating_discovery_ids": row["originating_discovery_ids"],
                "navigation_hints": row["navigation_hints"],
                "licence_status_observations": row["licence_status_observations"],
                "caveats": row["caveats"],
                "m1_intake_status": "M1_PINNED_PUBLIC_SOURCE_PENDING_TREE_CENSUS_NOT_A_CLUSTER_OR_RESULT",
            })
        if not args.quiet and identifier not in prior and (new_count % 5 == 0 or position == len(m0_rows)):
            print(json.dumps({"M1_HEAD_PROBE_PROGRESS": f"{position}/{len(m0_rows)}", "newly_probed_this_invocation": new_count, "probe_status": record["probe_status"]}, sort_keys=True), flush=True)
    plan = {
        "status": "M1_ROUND36_BATCH_PLAN_PINNED_PENDING_TREE_CENSUS_NOT_A_CLUSTER_OR_RESULT",
        "round": "RQ1b cross-source Round 36",
        "m0_input": str(args.m0),
        "head_probe": str(args.probe_output),
        "source_count": len(sources),
        "sources": sources,
        "explicit_exclusions": [
            "No repository body was cloned or acquired by the HEAD probe.",
            "No source content was executed, and no composition, prompt, label, retrieval input, model result, metric, or empirical conclusion was created.",
            "A failed HEAD probe is a recorded non-admission and receives no automatic retry.",
        ],
    }
    write_json(args.plan_output, plan)
    summary = {
        "status": "M1_ROUND36_HEAD_PROBE_COMPLETE_NOT_A_SOURCE_BODY_ADMISSION_OR_RESULT",
        "m0_input_count": len(m0_rows), "reachable_pinned_count": len(sources), "unreachable_count": len(m0_rows) - len(sources),
        "probe_output": str(args.probe_output), "plan_output": str(args.plan_output),
        "failures": [row for row in records if row["probe_status"] != "REACHABLE"], "exclusions": plan["explicit_exclusions"],
    }
    write_json(args.summary, summary)
    print(json.dumps({key: summary[key] for key in ("status", "m0_input_count", "reachable_pinned_count", "unreachable_count")}, sort_keys=True))
    return 0


def census(args: argparse.Namespace) -> int:
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    if plan.get("status") != "M1_ROUND36_BATCH_PLAN_PINNED_PENDING_TREE_CENSUS_NOT_A_CLUSTER_OR_RESULT":
        raise SystemExit("unexpected_round36_m1_plan")
    sources = plan["sources"]
    prior = {int(row["plan_position"]): row for row in (read_jsonl(args.output) if args.output.exists() else [])}
    if not set(prior).issubset(set(range(1, len(sources) + 1))):
        raise SystemExit("invalid_existing_round36_census_checkpoint")
    rows: list[dict[str, Any]] = []
    newly = 0
    for number, source in enumerate(sources, start=1):
        record = prior.get(number)
        if record is None:
            newly += 1
            try:
                source_root = get_tree(str(source["origin"]), str(source["repository_url"]), str(source["pinned_commit"]))
                paths = skill_paths(source_root, str(source["pinned_commit"]))
                record = {"plan_position": number, "origin": source["origin"], "repository_url": source["repository_url"], "pinned_commit": source["pinned_commit"], "skill_md_path_count": len(paths), "tree_census_status": "M1_TREE_CENSUS_COMPLETE_NO_BLOBS_STAGED_NOT_A_CLUSTER_OR_RESULT"}
            except Exception as error:
                record = {"plan_position": number, "origin": source["origin"], "repository_url": source["repository_url"], "pinned_commit": source["pinned_commit"], "skill_md_path_count": None, "tree_census_status": "M1_TREE_CENSUS_FAILED_NOT_ADMITTED_NOT_A_RESULT", "error": f"{type(error).__name__}:{error}"}
        rows.append(record)
        write_jsonl(args.output, rows)
        if not args.quiet and number not in prior and (newly % 5 == 0 or number == len(sources)):
            print(json.dumps({"M1_TREE_CENSUS_PROGRESS": f"{number}/{len(sources)}", "newly_censused_this_invocation": newly, "status": record["tree_census_status"]}, sort_keys=True), flush=True)
    summary = {"status": "M1_ROUND36_TREE_CENSUS_COMPLETE_NOT_A_SOURCE_BODY_ADMISSION_OR_RESULT", "plan": str(args.plan), "source_count": len(rows), "complete_count": sum(row["tree_census_status"].startswith("M1_TREE_CENSUS_COMPLETE") for row in rows), "failed_count": sum(row["tree_census_status"].startswith("M1_TREE_CENSUS_FAILED") for row in rows), "skill_md_path_count": sum(int(row["skill_md_path_count"] or 0) for row in rows), "exclusions": ["Only pinned Git trees were fetched; no SKILL.md body was materialised or executed.", "No candidate composition, prompt, label, retrieval input, model result, metric, or empirical conclusion was created."]}
    write_json(args.summary, summary)
    print(json.dumps({key: summary[key] for key in ("status", "source_count", "complete_count", "failed_count", "skill_md_path_count")}, sort_keys=True))
    return 0


def select(args: argparse.Namespace) -> int:
    rows = read_jsonl(args.census)
    selected = [row for row in rows if row.get("tree_census_status") == "M1_TREE_CENSUS_COMPLETE_NO_BLOBS_STAGED_NOT_A_CLUSTER_OR_RESULT" and args.minimum_paths <= int(row.get("skill_md_path_count") or 0) <= args.maximum_paths]
    selected.sort(key=lambda row: int(row["plan_position"]))
    source_positions = [int(row["plan_position"]) for row in selected]
    sources = [{"plan_position": int(row["plan_position"]), "origin": row["origin"], "repository_url": row["repository_url"], "pinned_commit": row["pinned_commit"], "skill_md_path_count": int(row["skill_md_path_count"]), "selection_rationale": f"completed_blobless_tree_census_and_bounded_{args.minimum_paths}_to_{args.maximum_paths}_skill_paths", "selection_status": "M1_SELECTED_FOR_LOCAL_BYTE_STAGING_NOT_A_CLUSTER_OR_RESULT"} for row in selected]
    payload = {"status": "M1_ROUND36_BOUNDED_DIVERSE_STAGING_SELECTION_NOT_A_CLUSTER_OR_RESULT", "round": "RQ1b cross-source Round 36", "census_input": str(args.census), "selection_rule": {"required_tree_census_status": "M1_TREE_CENSUS_COMPLETE_NO_BLOBS_STAGED_NOT_A_CLUSTER_OR_RESULT", "minimum_skill_md_path_count": args.minimum_paths, "maximum_skill_md_path_count": args.maximum_paths, "rule_basis": "tree metadata only; no source body was read for selection"}, "source_count": len(sources), "skill_md_path_count": sum(source["skill_md_path_count"] for source in sources), "sources": sources, "explicit_exclusions": ["Failed/incomplete census records are non-admissions and not automatically retried.", "Completed origins outside the predeclared path bound stay out of this bounded cohort without a source-quality verdict.", "No artifact body, candidate composition, prompt, gold label, acceptable set, retrieval input, embedding, model result, metric, or empirical conclusion was created."]}
    write_json(args.output, payload)
    summary = {"status": "M1_ROUND36_SELECTION_COMPLETE_NOT_A_CLUSTER_OR_RESULT", "census_record_count": len(rows), "selected_source_count": len(sources), "selected_skill_md_path_count": payload["skill_md_path_count"], "source_positions": source_positions, "selection_output": str(args.output), "exclusions": payload["explicit_exclusions"]}
    write_json(args.summary, summary)
    print(json.dumps({key: summary[key] for key in ("status", "selected_source_count", "selected_skill_md_path_count")}, sort_keys=True))
    return 0


def stage(args: argparse.Namespace) -> int:
    selection = json.loads(args.selection.read_text(encoding="utf-8"))
    if selection.get("status") != "M1_ROUND36_BOUNDED_DIVERSE_STAGING_SELECTION_NOT_A_CLUSTER_OR_RESULT":
        raise SystemExit("unexpected_round36_selection")
    prior_payload = json.loads(args.output.read_text(encoding="utf-8")) if args.output.exists() else None
    if prior_payload and prior_payload.get("selection") != str(args.selection):
        raise SystemExit("invalid_existing_round36_stage_checkpoint")
    prior = {int(row["source_position"]): row for row in (prior_payload or {}).get("results", [])}
    results: list[dict[str, Any]] = []
    for ordinal, source in enumerate(selection["sources"], start=1):
        position = int(source["plan_position"])
        record = prior.get(position)
        if record is None:
            print(json.dumps({"M1_STAGE_PROGRESS": f"{ordinal}/{len(selection['sources'])}", "source_position": position, "origin": source["origin"], "event": "begin"}, sort_keys=True), flush=True)
            try:
                source_root = get_tree(str(source["origin"]), str(source["repository_url"]), str(source["pinned_commit"]))
                paths = skill_paths(source_root, str(source["pinned_commit"]))
                if len(paths) != int(source["skill_md_path_count"]):
                    raise RuntimeError(f"tree_census_count_mismatch:{len(paths)}:{source['skill_md_path_count']}")
                licence_path = root_licence(source_root, str(source["pinned_commit"]))
                materialise(source_root, str(source["pinned_commit"]), paths + ([licence_path] if licence_path else []))
                destination = STAGED_ROOT / f"round36-m1-{str(source['origin']).replace('/', '--').lower()}-{str(source['pinned_commit'])[:8]}"
                summary_path = destination / "source_expansion_summary.json"
                if destination.exists() and any(destination.iterdir()):
                    staged_summary = json.loads(summary_path.read_text(encoding="utf-8"))
                    stage_status = "M1_RECOVERED_COMPLETE_LOCAL_STAGE_NOT_A_CLUSTER_OR_RESULT"
                else:
                    command = [sys.executable, str(STAGER), "--source-root", str(source_root), "--source-search-root", ".", "--destination", str(destination), "--origin", str(source["origin"]), "--repository-url", str(source["repository_url"]), "--pinned-commit", str(source["pinned_commit"]), "--skill-prefix", f"r36m1-{str(source['origin']).replace('/', '-')}", "--existing-source-roots", str(ROOT / "skills" / "public_imported_background"), str(ROOT / "rq1b_naturalistic_public_replication" / "staged_sources"), str(STAGED_ROOT)]
                    if licence_path:
                        command.extend(["--license-id", "DECLARED_REPOSITORY_LICENSE_UNCLASSIFIED", "--license-path", licence_path])
                    else:
                        command.extend(["--license-id", "NO_DECLARED_REPOSITORY_LICENSE", "--allow-no-license"])
                    staged_summary = json.loads(run(command, capture=True))
                    stage_status = "M1_LOCAL_BYTE_STAGED_NOT_A_CLUSTER_OR_RESULT"
                record = {"source_position": position, "origin": source["origin"], "repository_url": source["repository_url"], "pinned_commit": source["pinned_commit"], "m1_stage_status": stage_status, "discovered_skill_path_count": len(paths), "staging_destination": str(destination), "staging_summary": staged_summary, "staging_summary_sha256": sha256(summary_path)}
            except Exception as error:
                record = {"source_position": position, "origin": source["origin"], "repository_url": source["repository_url"], "pinned_commit": source["pinned_commit"], "m1_stage_status": "M1_SOURCE_STAGE_FAILED_NOT_ADMITTED_NOT_A_RESULT", "error": f"{type(error).__name__}:{error}"}
        results.append(record)
        payload = {"status": "M1_ROUND36_STAGING_IN_PROGRESS_OR_COMPLETE_NOT_A_CLUSTER_OR_RESULT", "selection": str(args.selection), "results": results}
        write_json(args.output, payload)
        print(json.dumps({"M1_STAGE_PROGRESS": f"{ordinal}/{len(selection['sources'])}", "source_position": position, "origin": source["origin"], "event": "complete_or_recovered", "status": record["m1_stage_status"], "discovered_skill_path_count": record.get("discovered_skill_path_count")}, sort_keys=True), flush=True)
    staged: list[dict[str, Any]] = []
    non_admissions: list[dict[str, Any]] = []
    integrity_failures: list[str] = []
    all_records = 0
    for result in results:
        if result["m1_stage_status"] not in {"M1_LOCAL_BYTE_STAGED_NOT_A_CLUSTER_OR_RESULT", "M1_RECOVERED_COMPLETE_LOCAL_STAGE_NOT_A_CLUSTER_OR_RESULT"}:
            non_admissions.append({"origin": result["origin"], "m1_stage_status": result["m1_stage_status"], "error": result.get("error")})
            continue
        destination = Path(str(result["staging_destination"])).resolve()
        source_manifest = destination / "source_expansion_manifest.jsonl"
        source_summary = destination / "source_expansion_summary.json"
        if not source_manifest.is_file() or not source_summary.is_file() or sha256(source_summary) != result["staging_summary_sha256"]:
            integrity_failures.append(f"stage_summary_missing_or_drift:{result['origin']}")
            continue
        local_summary = json.loads(source_summary.read_text(encoding="utf-8"))
        if local_summary != result["staging_summary"]:
            integrity_failures.append(f"stage_summary_payload_drift:{result['origin']}")
            continue
        source_rows = read_jsonl(source_manifest)
        all_records += len(source_rows)
        for source_row in source_rows:
            if source_row.get("source_status") != "STAGED_SOURCE_ONLY_NOT_A_CLUSTER":
                continue
            skill_id = str(source_row["skill_id"])
            original = destination / "skills" / skill_id / "source" / ORIGINAL_FILE
            if not original.is_file() or sha256(original) != source_row.get("source_sha256"):
                integrity_failures.append(f"source_hash_or_presence_failure:{result['origin']}:{skill_id}")
                continue
            staged.append({"source_admission_status": "M1_PINNED_SOURCE_STAGED_NOT_A_CLUSTER", "skill_id": skill_id, "origin": source_row["origin"], "repository_url": source_row["repository_url"], "pinned_commit": source_row["pinned_commit"], "source_repository_path": source_row["source_repository_path"], "source_url": source_row["source_url"], "source_sha256": source_row["source_sha256"], "source_bytes": original.stat().st_size, "license": source_row["license"], "license_status": source_row["license_status"], "frontmatter_name": source_row.get("frontmatter_name"), "frontmatter_description": source_row.get("frontmatter_description"), "stage_directory": destination.name, "local_original_path": str(original.relative_to(Path.cwd())), "m1_source_position": result["source_position"]})
    by_hash: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in staged:
        by_hash[str(row["source_sha256"])].append(row)
    canonical = [sorted(rows, key=lambda row: (str(row["origin"]), str(row["source_repository_path"]), str(row["skill_id"])))[0] for _, rows in sorted(by_hash.items())]
    canonical.sort(key=lambda row: (str(row["origin"]), str(row["source_repository_path"]), str(row["skill_id"])))
    write_jsonl(args.out_manifest, canonical)
    summary = {"status": "M1_PASS_ROUND36_PINNED_BYTE_VERIFIED_NOT_A_CLUSTER_OR_RESULT" if not integrity_failures else "M1_FAIL_OR_INCOMPLETE_NOT_A_CLUSTER_OR_RESULT", "selection": str(args.selection), "staged_origin_count": len({str(row["origin"]) for row in staged}), "all_source_stage_rows": all_records, "pre_canonical_source_count": len(staged), "m1_staged_source_count": len(canonical), "origin_count": len({str(row["origin"]) for row in canonical}), "by_origin": dict(sorted(Counter(str(row["origin"]) for row in canonical).items())), "exact_duplicate_source_count_excluded_from_navigation": len(staged) - len(canonical), "non_admitted_source_count": len(non_admissions), "non_admitted_sources": non_admissions, "integrity_failures": integrity_failures, "exclusions": ["No source content was executed.", "No semantic grouping, cluster, prompt, gold label, acceptable set, embedding, selector call, retrieval score, metric, or result was created.", "The manifest records byte-verified original-source candidates only; later source-only review remains required for any cluster draft."]}
    write_json(args.summary, summary)
    payload = {"status": "M1_ROUND36_STAGING_COMPLETE_NOT_A_CLUSTER_OR_RESULT", "selection": str(args.selection), "results": results}
    write_json(args.output, payload)
    print(json.dumps({key: summary[key] for key in ("status", "m1_staged_source_count", "origin_count", "non_admitted_source_count", "integrity_failures")}, sort_keys=True))
    return 0 if not integrity_failures else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="mode", required=True)
    probe_parser = sub.add_parser("probe")
    probe_parser.add_argument("--m0", type=Path, required=True); probe_parser.add_argument("--probe-output", type=Path, required=True); probe_parser.add_argument("--plan-output", type=Path, required=True); probe_parser.add_argument("--summary", type=Path, required=True); probe_parser.add_argument("--quiet", action="store_true"); probe_parser.add_argument("--replace-dns-failures", action="store_true"); probe_parser.add_argument("--transport-failure-audit", type=Path, default=MANIFEST / "m1_round36_sandbox_dns_transport_failure_2026-08-28.json")
    census_parser = sub.add_parser("census")
    census_parser.add_argument("--plan", type=Path, required=True); census_parser.add_argument("--output", type=Path, required=True); census_parser.add_argument("--summary", type=Path, required=True); census_parser.add_argument("--quiet", action="store_true")
    selection_parser = sub.add_parser("select")
    selection_parser.add_argument("--census", type=Path, required=True); selection_parser.add_argument("--minimum-paths", type=int, default=3); selection_parser.add_argument("--maximum-paths", type=int, default=64); selection_parser.add_argument("--output", type=Path, required=True); selection_parser.add_argument("--summary", type=Path, required=True)
    stage_parser = sub.add_parser("stage")
    stage_parser.add_argument("--selection", type=Path, required=True); stage_parser.add_argument("--output", type=Path, required=True); stage_parser.add_argument("--out-manifest", type=Path, required=True); stage_parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    return {"probe": probe, "census": census, "select": select, "stage": stage}[args.mode](args)


if __name__ == "__main__":
    raise SystemExit(main())
