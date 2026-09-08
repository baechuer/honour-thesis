#!/usr/bin/env python3
"""Build/replay local I1/I2 views without selectors, model calls or label reads.

Tracked outputs are compact manifests and a mechanical report. Full derived
views live in ignored cache and can be restored exactly from tracked sources.
I1 native-identity semantic QA and I3C/I3-flat remain separate Phase-7 work.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from audit_rq2b_preflight import parse_frontmatter
from rq2b_common import serialize_i1
from prepare_rq2b_v7_first_matrix import safe_path

ROOT = Path(__file__).resolve().parents[2]
PREP = Path("skill_benchmark/rq2b_naturalistic_confusability/preparation")
INPUT = PREP / "v7_first_matrix_2026_09_08_v1"
OUTPUT = PREP / "v7_phase7_i1_i2_2026_09_08_v1"
CACHE = Path("skill_benchmark/cache/rq2b_v7_phase7_i1_i2_2026_09_08_v1")
SOURCE_UNION_SHA = "5a49931ee1ff7fc3035a334d6df973393f8169f880b0209f368bd3d05d5fa08b"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encode_json(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def encode_rows(rows: list[dict]) -> bytes:
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows).encode()


def view(source_sha: str, kind: str, text: str) -> dict:
    # Only selector_text may be sent as the candidate view. No family, role,
    # target, review or query-derived metadata is inserted into that text.
    return {"schema_version": "rq2b-v7-local-view-v1", "source_sha256": source_sha,
            "representation": kind, "selector_text": text,
            "selector_text_sha256": sha(text.encode())}


def build() -> tuple[dict[str, bytes], dict[str, bytes]]:
    first = json.loads((ROOT / INPUT / "readiness_report.json").read_bytes())
    manifest_bytes = (ROOT / INPUT / "source_manifest.jsonl").read_bytes()
    if first["bindings"]["source_union_sha256"] != SOURCE_UNION_SHA:
        raise ValueError("V7 source-union binding mismatch")
    if first["output_sha256"]["source_manifest.jsonl"] != sha(manifest_bytes):
        raise ValueError("source manifest drift")
    sources = [json.loads(line) for line in manifest_bytes.splitlines()]
    if len(sources) != 3798 or len({s["sha256"] for s in sources}) != 3798:
        raise ValueError("V7 source identity coverage mismatch")
    i1, i2, inventory = [], [], []
    for source in sorted(sources, key=lambda row: row["sha256"]):
        raw = safe_path(ROOT, source["path"]).read_bytes()
        if sha(raw) != source["sha256"] or len(raw) != source["bytes"]:
            raise ValueError(f"source byte drift: {source['path']}")
        text = raw.decode("utf-8")
        if text.encode("utf-8") != raw:
            raise ValueError("non-roundtrip UTF-8")
        native = parse_frontmatter(text)
        name, description = native.get("name", "").strip(), native.get("description", "").strip()
        text1 = serialize_i1(name, description)  # Fails on absent native fields.
        row1, row2 = view(source["sha256"], "I1-discovery", text1), view(source["sha256"], "I2-original", text)
        if row2["selector_text_sha256"] != source["sha256"]:
            raise ValueError("I2 is not byte-exact")
        i1.append(row1)
        i2.append(row2)
        inventory.append({"source_sha256": source["sha256"], "source_path": source["path"],
                          "i1_selector_text_sha256": row1["selector_text_sha256"],
                          "i2_selector_text_sha256": row2["selector_text_sha256"],
                          "i1_utf8_bytes": len(text1.encode()), "i2_utf8_bytes": len(raw),
                          "i1_chars": len(text1), "i2_chars": len(text),
                          "identity_status": "NATIVE_FIELDS_PARSED_PENDING_SEMANTIC_QA"})
    payloads = {"i1-discovery.jsonl": encode_rows(i1), "i2-original.jsonl": encode_rows(i2)}
    artifacts = {name: {"path": str(CACHE / name), "sha256": sha(data), "rows": len(sources), "bytes": len(data)}
                 for name, data in payloads.items()}
    files = {"source_view_inventory.jsonl": encode_rows(inventory)}
    report = {
        "schema_version": "rq2b-v7-phase7-mechanical-preparation-v1",
        "status": "PASS_I1_I2_MECHANICAL_MATERIALISATION_PENDING_PHASE7_QA_AND_I3",
        "formal_execution_ready": False, "network_calls": 0, "selector_runs": 0,
        "bindings": {"source_manifest_sha256": sha(manifest_bytes), "source_union_sha256": SOURCE_UNION_SHA,
                     "first_preparation_report_sha256": sha((ROOT / INPUT / "readiness_report.json").read_bytes()),
                     "script_sha256": sha(Path(__file__).read_bytes()),
                     "identity_parser_module_sha256": sha(Path(__file__).with_name("audit_rq2b_preflight.py").read_bytes()),
                     "serializer_module_sha256": sha(Path(__file__).with_name("rq2b_common.py").read_bytes()),
                     "path_guard_module_sha256": sha(Path(__file__).with_name("prepare_rq2b_v7_first_matrix.py").read_bytes())},
        "counts": {"source_rows": len(sources), "i1_rows": len(i1), "i2_exact_byte_rows": len(i2),
                   "i1_selector_utf8_bytes": sum(r["i1_utf8_bytes"] for r in inventory),
                   "i2_selector_utf8_bytes": sum(r["i2_utf8_bytes"] for r in inventory),
                   "i1_selector_chars": sum(r["i1_chars"] for r in inventory),
                   "i2_selector_chars": sum(r["i2_chars"] for r in inventory)},
        "local_derived_artifacts": artifacts,
        "tracked_output_sha256": {name: sha(data) for name, data in files.items()},
        "identity_policy": "Reuse the existing native frontmatter parser and I1 serializer; nonempty fields are not semantic/source-identity QA approval.",
        "token_boundary": "Characters and UTF-8 bytes are storage/context-burden inventory, not model token counts, context feasibility, cost or latency results.",
        "remaining": ["I1 parsing/identity semantic QA", "V7-complete I3C/I3-flat extraction, reuse provenance and matched-evidence QA",
                      "master-SOP stratified blinded representation QA", "dependency/exposure and exact tokenizer/window preflight",
                      "final runtime root and payload-specific compute/transfer seal"],
    }
    files["mechanical_report.json"] = encode_json(report)
    return files, payloads


def require_equal(path: Path, expected: bytes) -> None:
    if path.read_bytes() != expected:
        raise ValueError(f"artifact drift: {path}")


def write_missing(path: Path, data: bytes) -> None:
    if path.exists():
        require_equal(path, data)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(data)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--verify", action="store_true", help="read-only replay; requires local payloads")
    mode.add_argument("--restore-payloads", action="store_true", help="validate tracked report then reconstruct only absent cache payloads")
    args = parser.parse_args()
    files, payloads = build()
    if args.verify or args.restore_payloads:
        for name, data in files.items():
            require_equal(ROOT / OUTPUT / name, data)
    else:
        if (ROOT / OUTPUT).exists():
            raise FileExistsError("refusing to overwrite versioned Phase-7 package")
        # Check any existing payload before writing the tracked outputs.
        for name, data in payloads.items():
            path = ROOT / CACHE / name
            if path.exists():
                require_equal(path, data)
        (ROOT / OUTPUT).mkdir(parents=True)
        for name, data in files.items():
            write_missing(ROOT / OUTPUT / name, data)
    for name, data in payloads.items():
        path = ROOT / CACHE / name
        if args.verify:
            require_equal(path, data)
        else:
            write_missing(path, data)
    print(json.dumps({"status": "PASS_PHASE7_I1_I2_REPLAY" if args.verify else "PASS_PHASE7_I1_I2_LOCAL_PREPARATION",
                      "source_count": 3798, "i1_rows": 3798, "i2_rows": 3798,
                      "formal_execution_ready": False, "selector_runs": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
