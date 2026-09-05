#!/usr/bin/env python3
"""Build a source-only, lexical T0 roster from Wave 039 public originals.

This is deliberately a review-ordering operation. It uses only each admitted
original's local header metadata to nominate possible common envelopes. It does
not read prompts, labels, field cards, selector outputs, metrics or prior T2+
decisions, and it cannot admit or reject a scientific cluster.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


STOPWORDS = {
    "about", "agent", "agents", "and", "assistant", "best", "build", "built",
    "code", "create", "for", "from", "guide", "help", "how", "into", "its",
    "markdown", "more", "new", "only", "plugin", "plugins", "skill", "skills",
    "after", "against", "before", "every", "need", "needs", "says", "single",
    "then", "that", "the", "this", "tool", "tools", "user", "use", "using",
    "want", "wants", "what", "when", "with", "write", "your",
}
CONTAINER_TERMS = {
    "base", "collection", "connector", "container", "framework", "general",
    "integration", "manager", "overview", "reference", "setup", "starter",
    "template", "tutorial", "utility", "utils", "workflow", "wrapper",
}
TOKEN_RE = re.compile(r"[a-z][a-z0-9_+-]{2,}", re.IGNORECASE)
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
FIELD_RE = re.compile(r"^(name|title|description)\s*:\s*(.+?)\s*$", re.IGNORECASE | re.MULTILINE)
HEADING_RE = re.compile(r"^#{1,2}\s+(.+?)\s*$", re.MULTILINE)

BOUNDARY = (
    "Wave 039 T0 is a source-only lexical review-ordering operation over newly "
    "frozen public originals. It creates no valid cluster, prompt, gold label, "
    "selector input, metric, retrieval result, information-field effect or thesis claim."
)


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def header_metadata(path: Path) -> tuple[str, set[str]]:
    """Return title signals only; descriptions are not lexical envelope evidence."""
    text = path.read_text(encoding="utf-8", errors="replace")[:8192]
    title_fields = []
    match = FRONTMATTER_RE.search(text)
    if match:
        for key, value in FIELD_RE.findall(match.group(1)):
            if key.lower() in {"name", "title"}:
                title_fields.append(value.strip(" '\""))
    heading = HEADING_RE.search(text)
    if heading:
        title_fields.append(heading.group(1).strip())
    title = title_fields[0] if title_fields else path.parent.name.replace("-", " ")
    tokens = {token.lower() for field in title_fields for token in TOKEN_RE.findall(field)}
    return title, {token for token in tokens if token not in STOPWORDS and len(token) >= 4}


def risk_terms(title: str) -> list[str]:
    return sorted(set(token.lower() for token in TOKEN_RE.findall(title)) & CONTAINER_TERMS)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--amendment", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--triad-count", type=int, default=18)
    args = parser.parse_args()
    if args.triad_count <= 0:
        raise SystemExit("triad_count_must_be_positive")
    if args.output_dir.exists():
        raise SystemExit("refusing_to_overwrite_existing_output_dir")

    sources = []
    invalid = []
    for row in read_jsonl(args.amendment):
        canonical = row.get("canonical", {})
        local_path = Path(str(canonical.get("local_raw_path", "")))
        expected = str(canonical.get("source_sha256", ""))
        if not local_path.is_file() or sha256_file(local_path) != expected:
            invalid.append(row.get("amendment_source_id", "UNKNOWN"))
            continue
        title, tokens = header_metadata(local_path)
        sources.append({
            "source_id": row["amendment_source_id"],
            "source_sha256": expected,
            "origin_url": row["origin_url"],
            "repository_ref": canonical["repository_ref"],
            "artifact_path": canonical["artifact_path"],
            "local_raw_path": canonical["local_raw_path"],
            "raw_artifact_url": canonical["raw_artifact_url"],
            "intake_lane": row["intake_lane"],
            "header_title": title,
            "header_tokens": sorted(tokens),
            "title_risk_terms": risk_terms(title),
        })
    if invalid:
        raise SystemExit(f"source_binding_failure:{','.join(invalid[:5])}")

    by_token: dict[str, list[dict]] = defaultdict(list)
    for source in sources:
        for token in source["header_tokens"]:
            by_token[token].append(source)

    token_origin_counts = {token: len({item["origin_url"] for item in members}) for token, members in by_token.items()}
    candidates: dict[tuple[str, str, str], dict] = {}
    for token, members in sorted(by_token.items()):
        # A term appearing in fewer than three origins cannot seed a triad.
        if token_origin_counts[token] < 3 or token_origin_counts[token] > 8:
            continue
        # Limit only the lexical candidate explosion; candidates remain sorted
        # deterministically and no body-level similarity has been used.
        limited = sorted(members, key=lambda item: (len(item["title_risk_terms"]), item["source_id"]))[:18]
        for trio in itertools.combinations(limited, 3):
            if len({item["origin_url"] for item in trio}) != 3:
                continue
            key = tuple(sorted(item["source_id"] for item in trio))
            common = {
                value for value in (set(trio[0]["header_tokens"]) & set(trio[1]["header_tokens"]) & set(trio[2]["header_tokens"]))
                if 3 <= token_origin_counts[value] <= 8
            }
            if not common:
                continue
            pair_overlap = sum(
                len(set(left["header_tokens"]) & set(right["header_tokens"]))
                for left, right in itertools.combinations(trio, 2)
            )
            risk = sum(len(item["title_risk_terms"]) for item in trio)
            specificity = sum(9 - token_origin_counts[value] for value in common)
            score = 10 * specificity + pair_overlap - 3 * risk
            candidate = {
                "candidate_source_ids": list(key),
                "candidate_count": 3,
                "shared_header_terms": sorted(common),
                "seed_token": token,
                "lexical_priority_proxy": score,
                "members": sorted(trio, key=lambda item: item["source_id"]),
                "claim_boundary": BOUNDARY,
            }
            prior = candidates.get(key)
            if prior is None or (score, candidate["seed_token"]) > (prior["lexical_priority_proxy"], prior["seed_token"]):
                candidates[key] = candidate

    ranked = sorted(
        candidates.values(),
        key=lambda item: (-item["lexical_priority_proxy"], item["seed_token"], item["candidate_source_ids"]),
    )
    selected, used_sources, used_envelopes = [], set(), set()
    for prefer_unique_envelope in (True, False):
        for candidate in ranked:
            if len(selected) >= args.triad_count:
                break
            ids = set(candidate["candidate_source_ids"])
            envelope = "|".join(candidate["shared_header_terms"])
            if ids & used_sources:
                continue
            if prefer_unique_envelope and envelope in used_envelopes:
                continue
            selected.append(candidate)
            used_sources.update(ids)
            used_envelopes.add(envelope)
        if len(selected) >= args.triad_count:
            break

    args.output_dir.mkdir(parents=True)
    all_drafts = args.output_dir / "t0_lexical_drafts.jsonl"
    all_drafts.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in ranked), encoding="utf-8")
    roster = []
    for index, candidate in enumerate(selected, start=1):
        roster.append({
            "t0_review_id": f"RQ1B-V3-W39-T0-{index:03d}",
            "candidate_count": 3,
            "members": candidate["members"],
            "shared_header_terms": candidate["shared_header_terms"],
            "seed_token": candidate["seed_token"],
            "lexical_priority_proxy": candidate["lexical_priority_proxy"],
            "allowed_outcomes": ["READY_FOR_C1", "LIKELY_NONPARALLEL", "NO_PLAUSIBLE_TRIAD", "NEEDS_PARENT_REVIEW"],
            "claim_boundary": BOUNDARY,
        })
    roster_path = args.output_dir / "t0_review_roster.jsonl"
    roster_path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in roster), encoding="utf-8")
    audit = {
        "status": "RQ1B_V3_W39_T0_ROSTER_PASS_NOT_A_CLUSTER",
        "amendment_source_count": len(sources),
        "lexical_draft_count": len(ranked),
        "selected_triad_count": len(roster),
        "selected_source_count": len(used_sources),
        "required_source_count": args.triad_count * 3,
        "source_disjoint": len(used_sources) == len(roster) * 3,
        "selected_distinct_origin_count": len({member["origin_url"] for triad in roster for member in triad["members"]}),
        "header_metadata_only": True,
        "network_calls": 0,
        "texts_transmitted": 0,
        "roster_sha256": sha256_file(roster_path),
        "claim_boundary": BOUNDARY,
    }
    (args.output_dir / "T0_ROSTER_AUDIT.json").write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(audit, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
