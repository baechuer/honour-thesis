#!/usr/bin/env python3
"""Create source-visible, identity-blinded, double-review packets for V2 tails.

This materialises reviewer inputs only.  It does not create a reviewer answer,
adequacy label, acceptable-set decision, selector output, or metric.  The
coordinator-only map is deliberately separated from the reviewer exports.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import re
import secrets
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
BENCHMARK = WORKSPACE / "skill_benchmark"
NC_ROOT = BENCHMARK / "rq2b_naturalistic_confusability"
QUEUE_DIR = NC_ROOT / "manifests/whole_library_pooled_discovery_queue_v2_2026-08-31"
QUEUE_PAIRS = QUEUE_DIR / "source_visible_review_pairs.jsonl"
PROMPT_QUEUES = QUEUE_DIR / "prompt_discovery_queues.jsonl"
PROFILES = NC_ROOT / "manifests/whole_library_navigation_profiles_prefreeze_2026-08-31/navigation_profiles.jsonl"
UNION = NC_ROOT / "manifests/current_pre_freeze_consolidated_2026-08-31/canonical_candidate_union_current_pre_freeze.jsonl"
OUT = NC_ROOT / "review/whole_library_pooled_tail_packets_v1_2026-08-31"
SEALED = OUT / "coordinator_sealed"
KEY_FILE = SEALED / "blinding_key.json"
MAP_OUT = SEALED / "blinding_map.jsonl"
ALLOCATION_OUT = SEALED / "allocation_ledger.jsonl"
SUMMARY_OUT = OUT / "summary.json"
TAIL_PACKET_QUEUE_VERSION = "V2"
PACKET_ID_PREFIX = "RQ2B-TAIL-V2"

IDENTITY_SECTION_TITLES = {
    "related skills", "related skill", "see also", "references", "links",
    "further reading", "provenance", "licence", "license", "credits",
    "acknowledgements", "acknowledgments",
}
PROVIDER_TOKENS = ("anthropic", "chatgpt", "claude", "codex", "gemini", "openai", "github")
REVIEW_STREAMS = ("A", "B")
DOUBLETS_PER_PACKET = 11


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def hmac_token(key: bytes, purpose: str, *parts: str) -> str:
    material = "\x1f".join((purpose, *parts)).encode("utf-8")
    return hmac.new(key, material, hashlib.sha256).hexdigest()[:20]


def load_or_create_key() -> bytes:
    SEALED.mkdir(parents=True, exist_ok=True)
    if KEY_FILE.exists():
        row = json.loads(KEY_FILE.read_text(encoding="utf-8"))
        if row.get("schema") != "rq2b-tail-packet-sealed-key-v1":
            raise ValueError("unexpected_sealed_key_schema")
        return bytes.fromhex(str(row["key_hex"]))
    key = secrets.token_bytes(32)
    KEY_FILE.write_text(
        json.dumps(
            {
                "schema": "rq2b-tail-packet-sealed-key-v1",
                "key_hex": key.hex(),
                "scope": "coordinator-only; never copy into reviewer exports",
            },
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )
    KEY_FILE.chmod(0o600)
    return key


def remove_frontmatter(lines: list[str]) -> tuple[list[tuple[int, str]], list[dict[str, Any]]]:
    if not lines or lines[0].strip() != "---":
        return list(enumerate(lines, start=1)), []
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return list(enumerate(lines[index + 1:], start=index + 2)), [
                {"kind": "frontmatter", "source_lines": [1, index + 1]}
            ]
    raise ValueError("unclosed_frontmatter")


def redact_source(text: str, profile: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
    """Preserve source capability text and line anchors while removing identity cues."""
    source_name = str(profile["source_name"])
    aliases = [str(value) for value in profile["candidate_alias_ids"]]
    source_paths = [str(value) for value in profile["source_paths"]]
    rows, redactions = remove_frontmatter(text.splitlines())
    retained: list[tuple[int, str]] = []
    skip_section = False
    for original_line, line in rows:
        heading = re.match(r"^\s*#{1,6}\s+(.+?)\s*#*\s*$", line)
        if heading:
            heading_text = heading.group(1).strip().casefold()
            skip_section = heading_text in IDENTITY_SECTION_TITLES
            if skip_section:
                redactions.append({"kind": "identity_section", "source_lines": [original_line, original_line]})
                continue
        if skip_section:
            continue
        rendered = re.sub(r"<!--.*?-->", "", line)
        rendered = rendered.replace("<!--", "[REDACTED_COMMENT_MARKER]").replace("-->", "")
        rendered = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", rendered)
        rendered = re.sub(r"https?://\S+", "[REDACTED_URL]", rendered, flags=re.IGNORECASE)
        rendered = re.sub(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", "[REDACTED_EMAIL]", rendered)
        for marker in [source_name, *aliases, *source_paths]:
            if marker and marker.casefold() in rendered.casefold():
                rendered = re.sub(re.escape(marker), "[REDACTED_SOURCE_ID]", rendered, flags=re.IGNORECASE)
        for number, marker in enumerate(PROVIDER_TOKENS, start=1):
            if marker.casefold() in rendered.casefold():
                rendered = re.sub(re.escape(marker), f"[ENTITY_{number}]", rendered, flags=re.IGNORECASE)
        rendered = re.sub(r"(?<!\w)/(?:[\w.-]+/){2,}[\w.-]+", "[REDACTED_PATH]", rendered)
        if rendered.strip():
            retained.append((original_line, rendered))
    rendered_lines = [f"[S{index:04d}|L{source_line:04d}] {line}" for index, (source_line, line) in enumerate(retained, start=1)]
    if not rendered_lines:
        raise ValueError("empty_after_redaction")
    rendered_text = "\n".join(rendered_lines) + "\n"
    prohibited = [source_name, *aliases, *source_paths, *PROVIDER_TOKENS]
    for marker in prohibited:
        if marker and marker.casefold() in rendered_text.casefold():
            raise ValueError(f"unredacted_marker:{marker}")
    if re.search(r"https?://|github\\.com|<!--", rendered_text, flags=re.IGNORECASE):
        raise ValueError("unredacted_url_or_comment")
    redactions.append({"kind": "retained_line_map", "source_to_card_lines": [[raw, index + 1] for index, (raw, _) in enumerate(retained)]})
    return rendered_text, redactions


def allocate_doublets(doublets: list[dict[str, Any]], key: bytes) -> list[list[dict[str, Any]]]:
    """Deterministically spread repeated sources while retaining 11 prompt groups/packet."""
    packet_count = len(doublets) // DOUBLETS_PER_PACKET
    assert packet_count * DOUBLETS_PER_PACKET == len(doublets) == 506
    source_frequency = Counter(
        pair["canonical_source_sha256"] for doublet in doublets for pair in doublet["pairs"]
    )
    ordered = sorted(
        doublets,
        key=lambda row: (
            -sum(source_frequency[pair["canonical_source_sha256"]] for pair in row["pairs"]),
            hmac_token(key, "allocation", row["lane_id"], row["prompt_id"]),
        ),
    )
    packets: list[list[dict[str, Any]]] = [[] for _ in range(packet_count)]
    packet_sources: list[Counter[str]] = [Counter() for _ in range(packet_count)]
    packet_lanes: list[Counter[str]] = [Counter() for _ in range(packet_count)]
    for doublet in ordered:
        sources = [pair["canonical_source_sha256"] for pair in doublet["pairs"]]
        eligible = [index for index, packet in enumerate(packets) if len(packet) < DOUBLETS_PER_PACKET]
        packet_index = min(
            eligible,
            key=lambda index: (
                sum(packet_sources[index][source] for source in sources),
                packet_lanes[index][doublet["lane_id"]],
                len(packets[index]),
                hmac_token(key, "packet-tiebreak", str(index), doublet["prompt_id"]),
            ),
        )
        packets[packet_index].append(doublet)
        packet_sources[packet_index].update(sources)
        packet_lanes[packet_index][doublet["lane_id"]] += 1
    assert all(len(packet) == DOUBLETS_PER_PACKET for packet in packets)
    return packets


def main() -> None:
    queue_pairs = read_jsonl(QUEUE_PAIRS)
    prompt_queues = read_jsonl(PROMPT_QUEUES)
    profiles = read_jsonl(PROFILES)
    union_rows = read_jsonl(UNION)
    key = load_or_create_key()
    queue_sha = file_sha256(QUEUE_PAIRS)
    prompt_queue_sha = file_sha256(PROMPT_QUEUES)
    profile_sha = file_sha256(PROFILES)
    union_sha = file_sha256(UNION)

    profiles_by_hash = {row["canonical_source_sha256"]: row for row in profiles}
    assert len(profiles_by_hash) == 3094
    assert len({row["canonical_source_sha256"] for row in union_rows}) == 3094
    prompt_by_key = {(row["lane_id"], row["prompt_id"]): row for row in prompt_queues}
    tails = [row for row in queue_pairs if row["tail"]]
    assert len(tails) in {1011, 1012}
    assert len({(row["lane_id"], row["prompt_id"], row["canonical_source_sha256"]) for row in tails}) == len(tails)
    unique_tail_source_count = len({row["canonical_source_sha256"] for row in tails})

    doublet_pairs: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for pair in tails:
        doublet_pairs[(pair["lane_id"], pair["prompt_id"])].append(pair)
    assert len(doublet_pairs) == 506
    doublets: list[dict[str, Any]] = []
    raw_source_cache: dict[str, tuple[str, list[dict[str, Any]], str, str]] = {}
    source_replay_count = 0
    for (lane_id, prompt_id), pairs in sorted(doublet_pairs.items()):
        if len(pairs) not in {1, 2}:
            raise ValueError(f"tail_prompt_group_size:{lane_id}:{prompt_id}:{len(pairs)}")
        tail_reasons = {tuple(pair["discovery_reasons"]) for pair in pairs}
        if len(pairs) == 2:
            assert tail_reasons == {("TAIL_PHRASE",), ("TAIL_RESIDUAL",)}
        else:
            assert tail_reasons == {("TAIL_RESIDUAL",)}
        prompt_row = prompt_by_key[(lane_id, prompt_id)]
        assert all(pair["prompt_sha256"] == prompt_row["prompt_sha256"] for pair in pairs)
        rendered_pairs: list[dict[str, Any]] = []
        for pair in sorted(pairs, key=lambda row: row["canonical_source_sha256"]):
            source_hash = pair["canonical_source_sha256"]
            profile = profiles_by_hash[source_hash]
            if source_hash not in raw_source_cache:
                matching_paths = []
                for relative in profile["source_paths"]:
                    path = WORKSPACE / relative
                    if path.is_file() and file_sha256(path) == source_hash:
                        matching_paths.append(path)
                if len(matching_paths) != 1:
                    raise ValueError(f"source_replay_resolution:{source_hash}:{len(matching_paths)}")
                raw_text = matching_paths[0].read_text(encoding="utf-8")
                redacted_text, redaction_map = redact_source(raw_text, profile)
                raw_source_cache[source_hash] = (
                    str(matching_paths[0].relative_to(WORKSPACE)), redaction_map, raw_text, redacted_text
                )
                source_replay_count += 1
            source_path, redaction_map, _raw_text, redacted_text = raw_source_cache[source_hash]
            rendered_pairs.append({
                "canonical_source_sha256": source_hash,
                "source_path": source_path,
                "tail_class": pair["discovery_reasons"][0],
                "redacted_source_text": redacted_text,
                "redaction_map": redaction_map,
            })
        doublets.append({
            "lane_id": lane_id,
            "prompt_id": prompt_id,
            "prompt": prompt_row["prompt"],
            "prompt_sha256": prompt_row["prompt_sha256"],
            "pairs": rendered_pairs,
        })
    assert source_replay_count == unique_tail_source_count

    allocations = allocate_doublets(doublets, key)
    coordinator_rows: list[dict[str, Any]] = []
    allocation_rows: list[dict[str, Any]] = []
    reviewer_manifests: dict[str, list[dict[str, Any]]] = {stream: [] for stream in REVIEW_STREAMS}
    stream_card_counts: Counter[str] = Counter()

    for packet_number, doublets_in_packet in enumerate(allocations, start=1):
        packet_id = f"{PACKET_ID_PREFIX}-{packet_number:02d}"
        for stream in REVIEW_STREAMS:
            cards: list[dict[str, Any]] = []
            for slot, doublet in enumerate(doublets_in_packet, start=1):
                for source_slot, pair in enumerate(doublet["pairs"], start=1):
                    case_token = hmac_token(
                        key, "case", queue_sha, doublet["prompt_sha256"], pair["canonical_source_sha256"], stream, packet_id, str(slot), str(source_slot)
                    )
                    source_token = hmac_token(key, "source", pair["canonical_source_sha256"], stream, packet_id, str(slot), str(source_slot))
                    prompt_token = hmac_token(key, "prompt", doublet["prompt_sha256"], stream, packet_id, str(slot))
                    card = {
                        "status": "BLINDED_SOURCE_VISIBLE_TAIL_REVIEW_INPUT_NOT_A_LABEL_RESULT_OR_METRIC",
                        "packet_id": packet_id,
                        "opaque_case_token": f"TC-{case_token}",
                        "opaque_prompt_token": f"TP-{prompt_token}",
                        "opaque_source_token": f"TS-{source_token}",
                        "prompt_text": doublet["prompt"],
                        "prompt_sha256": doublet["prompt_sha256"],
                        "redacted_source_text": pair["redacted_source_text"],
                        "review_response_form": {
                            "outcome_placeholder": "UNFILLED",
                            "allowed_outcomes": ["FULLY_ACCEPTABLE", "PARTIALLY_ADEQUATE", "NOT_ADEQUATE", "UNCLEAR"],
                            "required": [
                                "supporting_anchor_positions",
                                "limitation_anchor_positions",
                                "prompt_requirement_map",
                                "short_rationale",
                            ],
                        },
                        "reviewer_instruction": "Assess this one source against the exact prompt. Cite [S....|L....] anchors for support and limitations. Do not infer any hidden target, discovery route, provenance, prior result, or metric. Leave the outcome field unfilled until independently reviewing the card.",
                    }
                    card["rendered_card_sha256"] = canonical_sha(card)
                    cards.append(card)
                    coordinator_rows.append({
                        "opaque_case_token": card["opaque_case_token"],
                        "packet_id": packet_id,
                        "reviewer_stream": stream,
                        "prompt_id": doublet["prompt_id"],
                        "prompt_sha256": doublet["prompt_sha256"],
                        "canonical_source_sha256": pair["canonical_source_sha256"],
                        "resolved_source_path": pair["source_path"],
                        "tail_class": pair["tail_class"],
                        "lane_id": doublet["lane_id"],
                        "redaction_map_sha256": canonical_sha(pair["redaction_map"]),
                        "rendered_card_sha256": card["rendered_card_sha256"],
                        "status": "COORDINATOR_ONLY_NO_LABEL_OR_RESULT",
                    })

            cards.sort(key=lambda card: hmac_token(key, "card-order", stream, packet_id, card["opaque_case_token"]))
            stream_dir = OUT / f"reviewer_stream_{stream}"
            packet_path = stream_dir / f"{packet_id}.jsonl"
            write_jsonl(packet_path, cards)
            reviewer_manifests[stream].append({
                "packet_id": packet_id,
                "card_count": len(cards),
                "rendered_card_sha256s": [card["rendered_card_sha256"] for card in cards],
                "status": "BLINDED_SOURCE_VISIBLE_TAIL_REVIEW_INPUT_NOT_A_LABEL_RESULT_OR_METRIC",
            })
            stream_card_counts[stream] += len(cards)
        allocation_rows.append({
            "packet_id": packet_id,
            "doublet_count": len(doublets_in_packet),
            "sealed_doublets": [
                {
                    "lane_id": doublet["lane_id"],
                    "prompt_id": doublet["prompt_id"],
                    "source_sha256s": [pair["canonical_source_sha256"] for pair in doublet["pairs"]],
                }
                for doublet in doublets_in_packet
            ],
            "status": "COORDINATOR_ONLY_ALLOCATION_NOT_A_LABEL_OR_RESULT",
        })

    assert stream_card_counts == Counter({"A": len(tails), "B": len(tails)})
    assert len(coordinator_rows) == 2 * len(tails)
    write_jsonl(MAP_OUT, sorted(coordinator_rows, key=lambda row: (row["reviewer_stream"], row["opaque_case_token"])))
    write_jsonl(ALLOCATION_OUT, allocation_rows)
    for stream in REVIEW_STREAMS:
        manifest_path = OUT / f"reviewer_stream_{stream}" / "manifest.jsonl"
        write_jsonl(manifest_path, reviewer_manifests[stream])

    summary = {
        "status": f"PASS_{TAIL_PACKET_QUEUE_VERSION}_TAIL_DOUBLE_BLIND_PACKETISATION_NOT_A_LABEL_RESULT_OR_METRIC",
        "bound_inputs": {
            str(QUEUE_PAIRS.relative_to(BENCHMARK)): queue_sha,
            str(PROMPT_QUEUES.relative_to(BENCHMARK)): prompt_queue_sha,
            str(PROFILES.relative_to(BENCHMARK)): profile_sha,
            str(UNION.relative_to(BENCHMARK)): union_sha,
        },
        "counts": {
            "tail_pairs": len(tails),
            "prompt_doublets": len(doublets),
            "residual_only_prompt_groups": sum(len(doublet["pairs"]) == 1 for doublet in doublets),
            "unique_tail_sources_sha_replayed": source_replay_count,
            "packets_per_reviewer_stream": len(allocations),
            "cards_per_reviewer_stream": dict(sorted(stream_card_counts.items())),
            "coordinator_blinding_map_rows": len(coordinator_rows),
        },
        "sealed_key_commitment": hashlib.sha256(key).hexdigest(),
        "outputs": {
            "coordinator_sealed/blinding_map.jsonl": file_sha256(MAP_OUT),
            "coordinator_sealed/allocation_ledger.jsonl": file_sha256(ALLOCATION_OUT),
            "reviewer_stream_A/manifest.jsonl": file_sha256(OUT / "reviewer_stream_A/manifest.jsonl"),
            "reviewer_stream_B/manifest.jsonl": file_sha256(OUT / "reviewer_stream_B/manifest.jsonl"),
        },
        "reviewer_export_prohibitions": [
            "canonical_source_sha256", "candidate_alias_ids", "source_name", "source_path", "origin", "provider", "repository", "lane_id", "tail_class", "discovery_reasons", "channel_scores", "gold", "local_roster", "prior_review", "selector_output", "metric"
        ],
        "claim_boundary": [
            "Packets support source-visible, outcome-blind review of frozen pooled discovery tails only.",
            "The materialiser creates blank review forms, not adequacy labels or acceptable sets.",
            "Unqueued sources receive no negative label; this is not exhaustive whole-library relevance annotation.",
        ],
    }
    SUMMARY_OUT.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
