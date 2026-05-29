#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
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

FIELD_DESCRIPTIONS = {
    "routing_trigger": "When the skill should be selected or invoked.",
    "input_precondition": "Required input artifacts, user-provided data, prerequisites, or prior state.",
    "output_artifact": "Expected result, deliverable, file, report, plan, patch, table, or response format.",
    "workflow_procedure": "Concrete process, ordered steps, method, or execution procedure.",
    "constraints_boundaries": "Scope limits, not-for conditions, do-not-use cases, guardrails, or constraints.",
    "dependencies_tools": "Required tools, APIs, binaries, credentials, platforms, commands, or external services.",
    "resources_references": "Referenced files, scripts, templates, assets, documentation, or supporting resources.",
    "examples_tests": "Examples, sample prompts, expected outputs, tests, verification checks, or evals.",
    "safety_side_effects": "Permissions, privacy, security, mutation risk, destructive actions, or side effects.",
    "portability_environment": "OS, language, model, version, runtime, compatibility, or environment assumptions.",
    "hierarchy_links": "Links to related skills, subskills, delegated workflows, or follow-up skill documents.",
}


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def sha256_json(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")


def completed_skills(path: Path) -> set[str]:
    return {row.get("skill", "") for row in load_jsonl(path)}


def select_rows(rows: list[dict[str, Any]], limit: int | None, seed: int) -> list[dict[str, Any]]:
    if limit is None or limit >= len(rows):
        return rows
    rng = random.Random(seed)
    selected: list[dict[str, Any]] = []
    seen: set[str] = set()

    by_origin: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_origin[row.get("origin") or "unknown"].append(row)
    for origin_rows in by_origin.values():
        choice = rng.choice(origin_rows)
        selected.append(choice)
        seen.add(choice["skill"])

    by_coverage = sorted(rows, key=lambda row: (row["explicit_or_extractable_fields"], row["skill"]))
    bands = [
        by_coverage[: max(3, limit // 4)],
        by_coverage[len(by_coverage) // 2 : len(by_coverage) // 2 + max(3, limit // 4)],
        by_coverage[-max(3, limit // 4) :],
    ]
    candidates = [item for band in bands for item in band]
    rng.shuffle(candidates)
    for row in candidates:
        if len(selected) >= limit:
            break
        if row["skill"] not in seen:
            selected.append(row)
            seen.add(row["skill"])

    remaining = [row for row in rows if row["skill"] not in seen]
    rng.shuffle(remaining)
    for row in remaining:
        if len(selected) >= limit:
            break
        selected.append(row)
        seen.add(row["skill"])
    return selected[:limit]


def normalize_base_url(base_url: str) -> str:
    return base_url.rstrip("/")


def chat_endpoint(base_url: str) -> str:
    base = normalize_base_url(base_url)
    if base.endswith("/v1"):
        return f"{base}/chat/completions"
    return f"{base}/chat/completions"


def extract_json_object(text: str) -> dict[str, Any]:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        print(f"FAILED TO PARSE JSON. RAW TEXT: {text}", file=sys.stderr)
        raise ValueError("Model response did not contain a JSON object.")
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        print(f"FAILED TO PARSE MATCHED JSON. RAW TEXT: {text}", file=sys.stderr)
        raise ValueError("Model response did not contain a valid JSON object.")


class ChatVerifier:
    def __init__(
        self,
        provider: str,
        base_url: str,
        model: str,
        api_key: str,
        cache_dir: Path,
        timeout: int,
        max_retries: int,
    ) -> None:
        self.provider = provider
        self.base_url = base_url
        self.model = model
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.cache_dir = cache_dir / "field_verification" / provider / slug(model)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.api_calls = 0
        self.cache_hits = 0

    def cache_path(self, prompt: str) -> Path:
        key = sha256_json(
            {
                "provider": self.provider,
                "base_url": self.base_url,
                "model": self.model,
                "prompt": prompt,
            }
        )
        return self.cache_dir / f"{key}.json"

    def verify(self, prompt: str) -> dict[str, Any]:
        path = self.cache_path(prompt)
        if path.exists():
            self.cache_hits += 1
            return json.loads(path.read_text(encoding="utf-8"))

        payload: dict[str, Any] = {
            "model": self.model,
            "temperature": 0,
            "max_tokens": 4000,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a strict evidence-based annotator for agent skill artifacts. "
                        "Return only valid JSON. Do not infer what a good skill should contain. "
                        "If a field is not supported by direct evidence from the provided SKILL.md, mark it missing."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "response_format": {"type": "json_object"},
        }
        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                response = post_json(chat_endpoint(self.base_url), self.api_key, payload, self.timeout)
                content = response["choices"][0]["message"]["content"]
                result = extract_json_object(content)
                path.write_text(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
                self.api_calls += 1
                return result
            except Exception as exc:  # noqa: BLE001 - surface provider/API details after retries.
                last_error = exc
                if attempt < self.max_retries:
                    time.sleep(1.5 * (attempt + 1))
        raise RuntimeError(f"Model verification failed after retries: {last_error}") from last_error


def slug(value: str) -> str:
    cleaned = "".join(char if char.isalnum() or char in "-._" else "_" for char in value)
    return cleaned.strip("_") or "default"


def post_json(url: str, api_key: str, payload: dict[str, Any], timeout: int) -> dict[str, Any]:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{url} returned HTTP {exc.code}: {detail[:1200]}") from exc


def truncate_skill_text(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n\n[TRUNCATED FOR AUDIT INPUT]\n"


def build_prompt(skill: str, skill_text: str) -> str:
    field_lines = "\n".join(f"- {field}: {FIELD_DESCRIPTIONS[field]}" for field in FIELDS)
    schema = {
        "skill": skill,
        "fields": {
            field: {
                "status": "explicit | implicit | missing",
                "confidence": 0.0,
                "evidence": ["exact verbatim quote from the provided SKILL.md without any paraphrasing"],
                "reason": "one concise sentence",
            }
            for field in FIELDS
        },
    }
    return (
        "Audit the provided public SKILL.md for representation-field evidence.\n\n"
        "Statuses:\n"
        "- explicit: the field is clearly named in frontmatter, a heading, or a directly labelled section.\n"
        "- implicit: the field is present in the body under different wording.\n"
        "- missing: the field is not supported by direct evidence.\n\n"
        "Strict rules:\n"
        "- Every non-missing field must include 1-3 EXACT quotes copied verbatim from the SKILL.md text.\n"
        "- DO NOT paraphrase, summarize, or shorten the evidence. The quote must be a character-for-character match to a span in the text.\n"
        "- If you cannot find an exact verbatim quote, mark the field missing.\n"
        "- Do not infer what the skill should contain. Only annotate what the text actually contains.\n"
        "- Keep reasons short.\n\n"
        f"Fields:\n{field_lines}\n\n"
        "Return JSON exactly matching this shape:\n"
        f"{json.dumps(schema, indent=2)}\n\n"
        f"SKILL NAME: {skill}\n\n"
        "SKILL.md:\n"
        "```markdown\n"
        f"{skill_text}\n"
        "```"
    )


def normalize_model_result(raw: dict[str, Any], row: dict[str, Any], skill_text: str) -> dict[str, Any]:
    fields: dict[str, Any] = {}
    for field in FIELDS:
        data = (raw.get("fields") or {}).get(field) or {}
        status = str(data.get("status") or "missing").strip().lower()
        if status not in {"explicit", "implicit", "missing"}:
            status = "missing"
        confidence_raw = data.get("confidence", 0.0)
        try:
            confidence = max(0.0, min(1.0, float(confidence_raw)))
        except (TypeError, ValueError):
            confidence = 0.0
        evidence = data.get("evidence") or []
        if isinstance(evidence, str):
            evidence = [evidence]
        evidence = [str(item).strip()[:280] for item in evidence if str(item).strip()][:3]
        evidence_found = [
            bool(item and item.lower() in skill_text.lower())
            for item in evidence
        ]
        if status != "missing" and not evidence:
            status = "missing"
            confidence = min(confidence, 0.2)
        fields[field] = {
            "status": status,
            "confidence": confidence,
            "evidence": evidence,
            "evidence_found": evidence_found,
            "reason": str(data.get("reason") or "")[:300],
        }
    return {
        "skill": row["skill"],
        "origin": row.get("origin"),
        "source_name": row.get("source_name"),
        "source_url": row.get("source_url"),
        "audit_file": row["audit_file"],
        "model_fields": fields,
    }


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Model-assisted verification of public skill representation fields.")
    parser.add_argument("--input-jsonl", default=str(repo_root / "outputs" / "public_skill_field_audit.jsonl"))
    parser.add_argument("--output-jsonl", default=str(repo_root / "outputs" / "public_skill_field_model_audit.jsonl"))
    parser.add_argument("--dotenv", default=".env")
    parser.add_argument("--provider", default="deepseek")
    parser.add_argument("--base-url", default=os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com"))
    parser.add_argument("--model", default=os.environ.get("DEEPSEEK_MODEL", "deepseek-v4-flash"))
    parser.add_argument("--key-env", default="DEEPSEEK_API_KEY")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--seed", type=int, default=4990)
    parser.add_argument("--max-chars", type=int, default=18000)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--max-retries", type=int, default=2)
    parser.add_argument("--cache-dir", default=str(repo_root / "runtime" / "provider_cache"))
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    load_dotenv(Path(args.dotenv))
    api_key = os.environ.get(args.key_env)
    if not api_key:
        raise SystemExit(
            f"Missing {args.key_env}. Add it to .env, or pass --key-env for another OpenAI-compatible provider."
        )

    input_jsonl = Path(args.input_jsonl)
    output_jsonl = Path(args.output_jsonl)
    if args.force and output_jsonl.exists():
        output_jsonl.unlink()

    heuristic_rows = load_jsonl(input_jsonl)
    if not heuristic_rows:
        raise SystemExit(f"No heuristic audit rows found at {input_jsonl}. Run audit_public_skill_fields.py first.")
    selected = select_rows(heuristic_rows, args.limit, args.seed)
    done = completed_skills(output_jsonl)
    client = ChatVerifier(
        provider=args.provider,
        base_url=args.base_url,
        model=args.model,
        api_key=api_key,
        cache_dir=Path(args.cache_dir),
        timeout=args.timeout,
        max_retries=args.max_retries,
    )

    processed = 0
    for row in selected:
        if row["skill"] in done:
            continue
        skill_text = read_text(Path(row["audit_file"]))
        prompt = build_prompt(row["skill"], truncate_skill_text(skill_text, args.max_chars))
        raw = client.verify(prompt)
        append_jsonl(output_jsonl, normalize_model_result(raw, row, skill_text))
        processed += 1

    print(f"Selected skills: {len(selected)}")
    print(f"New model-audited skills: {processed}")
    print(f"Cache hits: {client.cache_hits}")
    print(f"API calls: {client.api_calls}")
    print(f"Wrote {output_jsonl}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
