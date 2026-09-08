#!/usr/bin/env python3
"""Build/replay V7 I1 with the frozen 39-row identity overlay; preserve I2 bytes."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from audit_rq2b_preflight import parse_frontmatter
from prepare_rq2b_v7_first_matrix import safe_path
from rq2b_common import serialize_i1


ROOT = Path(__file__).resolve().parents[2]
PREP = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation")
SOURCE_PACKAGE = PREP / "v7_first_matrix_2026_09_08_v1"
OLD_PACKAGE = PREP / "v7_phase7_i1_i2_2026_09_08_v1"
OLD_CACHE = Path("skill_benchmark/cache/rq2b_v7_phase7_i1_i2_2026_09_08_v1")
OVERLAY_PACKAGE = PREP / "v7_phase7_i1_identity_overlay_final_2026_09_09_v1"
OUTPUT = PREP / "v7_phase7_i1_i2_2026_09_09_v2"
CACHE = Path("skill_benchmark/cache/rq2b_v7_phase7_i1_i2_2026_09_09_v2")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def rows_bytes(value: list[dict]) -> bytes:
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in value).encode()


def rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_bytes().splitlines()]


def view(source_sha: str, kind: str, text: str) -> dict:
    return {
        "schema_version": "rq2b-v7-local-view-v1",
        "source_sha256": source_sha,
        "representation": kind,
        "selector_text": text,
        "selector_text_sha256": sha(text.encode()),
    }


def build() -> tuple[dict[str, bytes], dict[str, bytes]]:
    sources = rows(ROOT / SOURCE_PACKAGE / "source_manifest.jsonl")
    overlays = rows(ROOT / OVERLAY_PACKAGE / "identity_overlay.jsonl")
    overlay_by_sha = {row["source_sha256"]: row for row in overlays}
    if len(sources) != 3798 or len(overlays) != len(overlay_by_sha) != 39:
        raise ValueError("source/overlay coverage mismatch")
    old_i1_rows = rows(ROOT / OLD_CACHE / "i1-discovery.jsonl")
    old_i2_data = (ROOT / OLD_CACHE / "i2-original.jsonl").read_bytes()
    old_i2_rows = [json.loads(line) for line in old_i2_data.splitlines()]
    old_i1_by_sha = {row["source_sha256"]: row for row in old_i1_rows}
    old_i2_by_sha = {row["source_sha256"]: row for row in old_i2_rows}
    if len(old_i1_by_sha) != len(old_i2_by_sha) != 3798:
        raise ValueError("old I1/I2 coverage mismatch")

    i1, i2, inventory = [], [], []
    changed = 0
    for source in sorted(sources, key=lambda row: row["sha256"]):
        raw = safe_path(ROOT, source["path"]).read_bytes()
        if sha(raw) != source["sha256"] or len(raw) != source["bytes"]:
            raise ValueError(f"source drift: {source['path']}")
        text = raw.decode("utf-8")
        native = parse_frontmatter(text)
        name = native.get("name", "").strip()
        overlay = overlay_by_sha.get(source["sha256"])
        if overlay:
            description = overlay["selected_description"].strip()
            identity_status = "SOURCE_GROUNDED_IDENTITY_OVERLAY"
        else:
            description = native.get("description", "").strip()
            identity_status = "NATIVE_FRONTMATTER_IDENTITY_UNCHANGED"
        if not name or not description or description.lower() in {">", "|", "use this skill when >", "use this skill when |"}:
            raise ValueError(f"unusable final identity: {source['path']}")
        text1 = serialize_i1(name, description)
        row1 = view(source["sha256"], "I1-discovery", text1)
        row2 = view(source["sha256"], "I2-original", text)
        if row2 != old_i2_by_sha[source["sha256"]]:
            raise ValueError("I2 byte/view drift")
        if overlay:
            if row1 == old_i1_by_sha[source["sha256"]]:
                raise ValueError("overlay did not change malformed I1")
            changed += 1
        elif row1 != old_i1_by_sha[source["sha256"]]:
            raise ValueError("non-overlay I1 drift")
        i1.append(row1)
        i2.append(row2)
        inventory.append({
            "source_sha256": source["sha256"],
            "source_path": source["path"],
            "i1_selector_text_sha256": row1["selector_text_sha256"],
            "i2_selector_text_sha256": row2["selector_text_sha256"],
            "i1_utf8_bytes": len(text1.encode()),
            "i2_utf8_bytes": len(raw),
            "i1_chars": len(text1),
            "i2_chars": len(text),
            "identity_status": identity_status,
        })
    if changed != 39:
        raise ValueError("identity overlay application count mismatch")
    payloads = {"i1-discovery.jsonl": rows_bytes(i1), "i2-original.jsonl": rows_bytes(i2)}
    if payloads["i2-original.jsonl"] != old_i2_data:
        raise ValueError("I2 serialized bytes changed")
    files = {"source_view_inventory.jsonl": rows_bytes(inventory)}
    report = {
        "schema_version": "rq2b-v7-phase7-i1-i2-materialisation-v2",
        "status": "PASS_I1_IDENTITY_OVERLAY_AND_I2_BYTE_PRESERVATION_PENDING_I3_V4_AND_FRESH_QA",
        "formal_execution_ready": False,
        "network_calls": 0,
        "selector_runs": 0,
        "counts": {"source_rows": 3798, "i1_rows": 3798, "i1_overlay_rows": 39, "i1_unchanged_rows": 3759, "i2_exact_byte_rows": 3798},
        "bindings": {
            "source_manifest_sha256": sha((ROOT / SOURCE_PACKAGE / "source_manifest.jsonl").read_bytes()),
            "old_i1_i2_report_sha256": sha((ROOT / OLD_PACKAGE / "mechanical_report.json").read_bytes()),
            "old_i2_payload_sha256": sha(old_i2_data),
            "identity_overlay_report_sha256": sha((ROOT / OVERLAY_PACKAGE / "integrity_report.json").read_bytes()),
            "identity_overlay_sha256": sha((ROOT / OVERLAY_PACKAGE / "identity_overlay.jsonl").read_bytes()),
            "script_sha256": sha(Path(__file__).read_bytes()),
        },
        "local_derived_artifacts": {name: {"path": str(CACHE / name), "sha256": sha(data), "rows": len(data.splitlines()), "bytes": len(data)} for name, data in payloads.items()},
        "tracked_artifacts": {"source_view_inventory.jsonl": {"sha256": sha(files["source_view_inventory.jsonl"]), "rows": 3798}},
        "method_boundary": "Only 39 unusable native descriptions are replaced by independently reviewed source-grounded overlays. The other 3,759 I1 rows and all I2 bytes are identical to v1.",
    }
    files["mechanical_report.json"] = json_bytes(report)
    files["README.md"] = (
        "# V7 Phase-7 I1/I2 materialisation v2\n\n"
        "State: `PASS_I1_IDENTITY_OVERLAY_AND_I2_BYTE_PRESERVATION_PENDING_I3_V4_AND_FRESH_QA`. Exactly 39 malformed native descriptions use the frozen source-grounded overlay. The other 3,759 I1 views and all 3,798 I2 views remain byte-identical to v1.\n\n"
        "This package does not authorise selector execution. Replay: `python3 -B skill_benchmark/scripts/materialize_rq2b_v7_i1_i2_with_identity_overlay.py --verify`.\n"
    ).encode()
    return files, payloads


def require_equal(path: Path, data: bytes) -> None:
    if path.read_bytes() != data:
        raise ValueError(f"artifact drift: {path}")


def write_new(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(data)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    files, payloads = build()
    if args.verify:
        for name, data in files.items():
            require_equal(ROOT / OUTPUT / name, data)
        for name, data in payloads.items():
            require_equal(ROOT / CACHE / name, data)
        status = "PASS_V7_I1_I2_V2_REPLAY"
    else:
        if (ROOT / OUTPUT).exists() or (ROOT / CACHE).exists():
            raise FileExistsError("refusing to overwrite versioned I1/I2 v2 package")
        for name, data in files.items():
            write_new(ROOT / OUTPUT / name, data)
        for name, data in payloads.items():
            write_new(ROOT / CACHE / name, data)
        status = "PASS_V7_I1_I2_V2_CREATED"
    print(json.dumps({"status": status, "sources": 3798, "identity_overlays": 39}, sort_keys=True))


if __name__ == "__main__":
    main()
