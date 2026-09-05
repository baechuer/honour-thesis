#!/usr/bin/env python3
"""Rank local source-text neighbours for RQ1b V3 source-only triage.

This is a deterministic lexical reading aid. It cannot establish shared task
envelopes, parallel alternatives, C1 eligibility, or a valid cluster.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path


TOKEN = re.compile(r"[a-z][a-z0-9_-]{2,}")
STOPWORDS = {
    "about", "after", "also", "and", "are", "because", "before", "but", "can", "does", "each",
    "for", "from", "has", "have", "into", "its", "may", "not", "only", "or", "our", "out",
    "that", "the", "their", "then", "this", "through", "use", "used", "using", "when", "with",
    "will", "your", "you", "skill", "skills", "workflow", "output", "input", "step", "steps",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--amendment", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--top-neighbours", type=int, default=8)
    parser.add_argument("--status-prefix", default="RQ1B_V3_D1_W25")
    return parser.parse_args()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def terms(text: str) -> Counter[str]:
    return Counter(token for token in TOKEN.findall(text.lower()) if token not in STOPWORDS)


def heading_lines(text: str) -> list[str]:
    return [line[1:].strip() for line in text.splitlines() if re.match(r"^#{1,3}\s+\S", line)][:12]


def cosine(left: dict[str, float], right: dict[str, float]) -> float:
    numerator = sum(value * right.get(term, 0.0) for term, value in left.items())
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    return numerator / (left_norm * right_norm) if left_norm and right_norm else 0.0


def main() -> int:
    args = parse_args()
    sources = read_jsonl(args.amendment)
    documents: list[dict] = []
    df: Counter[str] = Counter()
    for source in sources:
        canonical = source["canonical"]
        path = Path(canonical["local_raw_path"])
        text = path.read_text(encoding="utf-8", errors="replace")
        raw_terms = terms(text)
        df.update(raw_terms)
        documents.append({
            "source": source,
            "raw_terms": raw_terms,
            "headings": heading_lines(text),
        })

    total_documents = len(documents)
    for document in documents:
        weighted = {
            term: (1.0 + math.log(count)) * math.log((1 + total_documents) / (1 + df[term]))
            for term, count in document["raw_terms"].items()
        }
        document["weighted_terms"] = weighted
        document["top_terms"] = [term for term, _ in sorted(weighted.items(), key=lambda item: (-item[1], item[0]))[:16]]

    rows: list[dict] = []
    for index, document in enumerate(documents):
        source = document["source"]
        candidates: list[tuple[float, dict]] = []
        for other_index, other in enumerate(documents):
            if index == other_index:
                continue
            score = cosine(document["weighted_terms"], other["weighted_terms"])
            shared_terms = sorted(set(document["top_terms"]) & set(other["top_terms"]))
            if not shared_terms:
                continue
            candidates.append((score, {"document": other, "shared_terms": shared_terms}))
        candidates.sort(
            key=lambda item: (
                -item[0],
                item[1]["document"]["source"]["amendment_source_id"],
            )
        )
        neighbours = []
        for score, item in candidates[: args.top_neighbours]:
            other_source = item["document"]["source"]
            neighbours.append({
                "source_id": other_source["amendment_source_id"],
                "repository_ref": other_source["canonical"]["repository_ref"],
                "artifact_path": other_source["canonical"]["artifact_path"],
                "lexical_cosine": round(score, 6),
                "cross_repository": other_source["canonical"]["repository_ref"] != source["canonical"]["repository_ref"],
                "shared_high_weight_terms": item["shared_terms"],
                "literal_headings": item["document"]["headings"],
            })
        rows.append({
            "status": f"{args.status_prefix}_LOCAL_LEXICAL_PRETRIAGE_NOT_A_CLUSTER",
            "source_id": source["amendment_source_id"],
            "repository_ref": source["canonical"]["repository_ref"],
            "artifact_path": source["canonical"]["artifact_path"],
            "local_raw_path": source["canonical"]["local_raw_path"],
            "source_sha256": source["canonical"]["source_sha256"],
            "literal_headings": document["headings"],
            "top_local_terms": document["top_terms"],
            "ranked_neighbours": neighbours,
            "claim_boundary": "Deterministic lexical source-text proximity is only a reading-order aid. It does not establish a shared envelope, operational contrast, parallel alternatives, C1 eligibility, prompt, label, selector input, field effect, or scientific result.",
        })

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    print(json.dumps({
        "status": f"{args.status_prefix}_LOCAL_LEXICAL_PRETRIAGE_PASS_NOT_A_CLUSTER",
        "source_count": total_documents,
        "top_neighbours": args.top_neighbours,
        "network_calls": 0,
        "texts_transmitted": 0,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
