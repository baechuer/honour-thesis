#!/usr/bin/env python3
"""Offline regression tests for the non-freezing RQ2b preflight audit."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from audit_rq2b_preflight import (
    legacy_drift,
    parse_frontmatter,
    prompt_inventory,
    source_inventory,
)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_frontmatter_blocks() -> None:
    folded = parse_frontmatter(
        "---\nname: folded\ndescription: >-\n  First line\n  second line.\n\n  New paragraph.\n---\nBody\n"
    )
    assert folded == {
        "name": "folded",
        "description": "First line second line.\n\nNew paragraph.",
    }
    literal = parse_frontmatter(
        "---\nname: 'literal'\ndescription: |\n  First line\n  second line.\n---\nBody\n"
    )
    assert literal == {
        "name": "literal",
        "description": "First line\nsecond line.",
    }


def test_source_policy(root: Path) -> None:
    skills = root / "skill_benchmark" / "skills"
    authored = skills / "controlled" / "authored"
    public = skills / "public_imported_background" / "public-one"
    write(
        authored / "SKILL.md",
        "---\nname: authored\ndescription: Authored description.\n---\nAuthored body.\n",
    )
    write(
        public / "SKILL.md",
        "---\nname: public-one\ndescription: Wrapper description.\n---\nWrapper body.\n",
    )
    write(
        public / "source" / "SKILL.original.md",
        "---\nname: source-one\ndescription: >-\n  Original public\n  description.\n---\nOriginal body.\n",
    )
    write(
        public / "source" / "IMPORT.json",
        json.dumps(
            {
                "origin": "test/source",
                "source_url": "https://example.invalid/source",
                "import_status": "downloaded",
            }
        ),
    )
    rows, errors = source_inventory(root, skills)
    assert errors == []
    by_id = {row["skill_id"]: row for row in rows}
    assert by_id["authored"]["source_policy"] == "authored_skill"
    assert by_id["authored"]["source_name"] == "authored"
    assert by_id["public-one"]["source_policy"] == "public_original"
    assert by_id["public-one"]["source_name"] == "source-one"
    assert by_id["public-one"]["source_description"] == "Original public description."
    assert by_id["public-one"]["source_path"].endswith("source/SKILL.original.md")


def test_exact_equivalence_closure(root: Path) -> None:
    prompt_dir = root / "prompts"
    write(
        prompt_dir / "cases.json",
        json.dumps(
            [
                {
                    "id": "p1",
                    "family": "test",
                    "gold_skill": "gold",
                    "closest_alternatives": ["duplicate", "other"],
                    "prompt": "Route this request.",
                }
            ]
        ),
    )
    skills = {
        skill_id: {"skill_id": skill_id}
        for skill_id in ("gold", "duplicate", "other", "other_duplicate")
    }
    rows, errors = prompt_inventory(
        root,
        [("controlled", prompt_dir)],
        {"controlled": {"p1": {"acceptable": ["other"], "borderline": []}}},
        skills,
        {
            "gold": ["gold", "duplicate"],
            "duplicate": ["gold", "duplicate"],
            "other": ["other", "other_duplicate"],
            "other_duplicate": ["other", "other_duplicate"],
        },
    )
    assert errors == []
    assert len(rows) == 1
    assert rows[0]["acceptable_skills"] == ["duplicate", "other", "other_duplicate"]
    assert rows[0]["valid_skills"] == ["duplicate", "gold", "other", "other_duplicate"]
    assert rows[0]["exact_source_equivalents_added"] == ["duplicate", "other_duplicate"]
    assert "prompt" not in rows[0]


def test_legacy_drift(root: Path) -> None:
    stable = root / "stable.txt"
    changed = root / "changed.txt"
    write(stable, "stable\n")
    write(changed, "before\n")
    import hashlib

    manifest = root / "manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "version": "test-v1",
                "file_hashes": {
                    "stable.txt": hashlib.sha256(stable.read_bytes()).hexdigest(),
                    "changed.txt": hashlib.sha256(changed.read_bytes()).hexdigest(),
                },
            }
        ),
        encoding="utf-8",
    )
    write(changed, "after\n")
    report = legacy_drift(root, manifest)
    assert report["matched_count"] == 1
    assert report["drifted"] == ["changed.txt"]


def main() -> None:
    test_frontmatter_blocks()
    with tempfile.TemporaryDirectory(prefix="rq2b-preflight-") as raw:
        root = Path(raw)
        test_source_policy(root)
    with tempfile.TemporaryDirectory(prefix="rq2b-prompts-") as raw:
        test_exact_equivalence_closure(Path(raw))
    with tempfile.TemporaryDirectory(prefix="rq2b-drift-") as raw:
        test_legacy_drift(Path(raw))
    print("RQ2b preflight tests: PASS")


if __name__ == "__main__":
    main()
