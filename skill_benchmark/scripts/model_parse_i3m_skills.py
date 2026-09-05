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
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Lock
from typing import Any


SCHEMA_VERSION = "I3_MODEL_EXTRACTION_V1"

I3_FIELDS = [
    "use_conditions",
    "input_preconditions",
    "output_artifacts",
    "workflow_steps",
    "constraints_boundaries",
    "dependencies_resources",
    "success_criteria",
]

FIELD_ID_PREFIX = {
    "use_conditions": "use_",
    "input_preconditions": "input_",
    "output_artifacts": "output_",
    "workflow_steps": "step_",
    "constraints_boundaries": "boundary_",
    "dependencies_resources": "dependency_",
    "success_criteria": "success_",
}

SELECTOR_ITEM_KEYS = {
    "use_conditions": {"id", "text", "evidence", "evidence_status", "confidence"},
    "input_preconditions": {
        "id",
        "text",
        "input_type",
        "necessity",
        "evidence",
        "evidence_status",
        "confidence",
    },
    "output_artifacts": {
        "id",
        "text",
        "artifact_type",
        "format",
        "evidence",
        "evidence_status",
        "confidence",
    },
    "workflow_steps": {
        "id",
        "order",
        "action",
        "object",
        "text",
        "evidence",
        "evidence_status",
        "confidence",
    },
    "constraints_boundaries": {
        "id",
        "polarity",
        "text",
        "evidence",
        "evidence_status",
        "confidence",
    },
    "dependencies_resources": {
        "id",
        "text",
        "dependency_type",
        "necessity",
        "evidence",
        "evidence_status",
        "confidence",
    },
    "success_criteria": {"id", "text", "evidence", "evidence_status", "confidence"},
}

ALLOWED_TOP_KEYS = {
    "schema_version",
    "skill_id",
    "skill_name",
    "source",
    "artifact_language",
    *I3_FIELDS,
}

SYSTEM_PROMPT = """You are a strict evidence-grounded parser for agent skill artifacts.

Your job is to extract selector-relevant information from a single skill artifact into a structured I3 representation.

Return only valid JSON. Do not include Markdown, commentary, or explanations outside JSON.

Do not infer what a skill should contain. Extract only information supported by direct evidence from the provided artifact. You may normalize wording, but every extracted item must include a short exact quote copied from the artifact as evidence.

If a field is absent or not supported by evidence, return an empty array for that field."""

USER_TEMPLATE = """Parse the following skill artifact into the I3 structured selection representation.

Definitions:
- use_conditions: when this skill should be selected; task types, user intents, or activation conditions.
- input_preconditions: required inputs, files, data state, user context, prerequisites, permissions, or prior artifacts.
- output_artifacts: expected deliverables, formats, files, reports, patches, tables, plans, answers, or response shape.
- workflow_steps: concrete procedure steps, methods, checks, transformations, or execution sequence. Extract multiple steps separately and preserve order when order is implied.
- constraints_boundaries: scope limits, not-for cases, style constraints, exclusions, or situations where the skill should not be used.
- dependencies_resources: required tools, APIs, commands, models, platforms, credentials, bundled files, templates, links, scripts, or external services.
- success_criteria: verification checks, acceptance criteria, metrics, quality conditions, or what counts as correct completion.

Extraction rules:
1. Return JSON only.
2. Do not invent missing information.
3. Every extracted item must be grounded in one exact contiguous evidence quote from the artifact.
4. Evidence quotes must be short and copied verbatim as a single substring.
4a. Do not combine a section heading with a bullet unless that exact combined text appears contiguously in the artifact.
4b. If a field is supported by several bullets, create separate extracted items with separate evidence quotes.
4c. Do not join multiple bullets, table rows, or separated phrases into one evidence quote.
5. Use "explicit" when the artifact directly labels or plainly states the field.
6. Use "implicit" when the field is present through different wording but still supported by direct evidence.
7. Use [] for fields with no evidence.
8. Number multiple items within each field using stable ids: use_1, input_1, output_1, step_1, boundary_1, dependency_1, success_1.
9. For workflow_steps, include an integer "order" when order is implied; otherwise use null.
10. For dependencies_resources, mark "necessity" as "required", "optional", or "unknown" based only on the artifact.
11. For constraints_boundaries, mark "polarity" as "positive_constraint" or "negative_boundary".
12. Do not treat general background prose as a trigger unless it helps decide when to use the skill.
13. Do not treat every mentioned tool as a dependency unless the skill appears to require or use it.
14. Do not extract side effects or hierarchy links as separate fields. If they matter for selection, express them only through one of the seven I3 fields above.
15. For a bullet under a heading, quote the bullet text itself, without adding the heading label, unless the heading label is part of the same contiguous text span.
16. If you cannot find one short contiguous quote for an item, do not extract that item.

Return JSON matching this schema:

{
  "schema_version": "I3_MODEL_EXTRACTION_V1",
  "skill_id": "<provided skill id>",
  "skill_name": "<provided skill name>",
  "source": "<provided source or null>",
  "artifact_language": "<detected language or unknown>",
  "use_conditions": [
    {
      "id": "use_1",
      "text": "normalized use condition",
      "evidence": "exact quote",
      "evidence_status": "explicit | implicit",
      "confidence": 0.0
    }
  ],
  "input_preconditions": [
    {
      "id": "input_1",
      "text": "normalized input or precondition",
      "input_type": "file | data | context | permission | prior_state | platform | other | unknown",
      "necessity": "required | optional | unknown",
      "evidence": "exact quote",
      "evidence_status": "explicit | implicit",
      "confidence": 0.0
    }
  ],
  "output_artifacts": [
    {
      "id": "output_1",
      "text": "normalized output artifact",
      "artifact_type": "answer | report | file | patch | plan | table | code | config | visualization | other | unknown",
      "format": "format if stated, otherwise unknown",
      "evidence": "exact quote",
      "evidence_status": "explicit | implicit",
      "confidence": 0.0
    }
  ],
  "workflow_steps": [
    {
      "id": "step_1",
      "order": 1,
      "action": "normalized action",
      "object": "object of the action or unknown",
      "text": "normalized workflow step",
      "evidence": "exact quote",
      "evidence_status": "explicit | implicit",
      "confidence": 0.0
    }
  ],
  "constraints_boundaries": [
    {
      "id": "boundary_1",
      "polarity": "positive_constraint | negative_boundary",
      "text": "normalized constraint or boundary",
      "evidence": "exact quote",
      "evidence_status": "explicit | implicit",
      "confidence": 0.0
    }
  ],
  "dependencies_resources": [
    {
      "id": "dependency_1",
      "text": "normalized dependency or resource",
      "dependency_type": "tool | api | command | model | platform | credential | file | template | script | documentation | service | other | unknown",
      "necessity": "required | optional | unknown",
      "evidence": "exact quote",
      "evidence_status": "explicit | implicit",
      "confidence": 0.0
    }
  ],
  "success_criteria": [
    {
      "id": "success_1",
      "text": "normalized success criterion",
      "evidence": "exact quote",
      "evidence_status": "explicit | implicit",
      "confidence": 0.0
    }
  ]
}

Skill metadata:
- skill_id: {skill_id}
- skill_name: {skill_name}
- source: {source}

Skill artifact:
```markdown
{skill_artifact}
```"""

COMPACT_USER_TEMPLATE = """Parse one agent skill artifact into the I3 structured selection representation.

Return valid JSON only. Use exactly these top-level fields:
- schema_version, skill_id, skill_name, source, artifact_language
- use_conditions
- input_preconditions
- output_artifacts
- workflow_steps
- constraints_boundaries
- dependencies_resources
- success_criteria

Set schema_version exactly to "I3_MODEL_EXTRACTION_V1".

Definitions:
- use_conditions: when this skill should be selected; task types, user intents, or activation conditions.
- input_preconditions: required inputs, files, data state, user context, prerequisites, permissions, or prior artifacts.
- output_artifacts: expected deliverables, formats, files, reports, patches, tables, plans, answers, or response shape.
- workflow_steps: concrete procedure steps, methods, checks, transformations, or execution sequence.
- constraints_boundaries: scope limits, not-for cases, style constraints, exclusions, or situations where the skill should not be used.
- dependencies_resources: required tools, APIs, commands, models, platforms, credentials, bundled files, templates, links, scripts, or external services.
- success_criteria: verification checks, acceptance criteria, metrics, quality conditions, or what counts as correct completion.

Evidence rules:
- Extract only information supported by direct evidence in the artifact.
- Every item must include one short exact contiguous evidence quote copied from the artifact.
- Do not combine headings with bullets unless that exact combined text appears contiguously.
- Do not merge multiple bullets, table rows, or separated phrases into one evidence quote.
- For a bullet under a heading, quote the bullet text itself without adding the heading label.
- If you cannot find one exact contiguous quote for an item, omit that item.
- Use [] for absent fields.

Item rules:
- Every item has id, text, evidence, evidence_status, confidence.
- evidence_status is "explicit" or "implicit".
- confidence is a number from 0.0 to 1.0.
- Use ids: use_1, input_1, output_1, step_1, boundary_1, dependency_1, success_1.
- For workflow_steps, also include order, action, object. Use order null if not implied.
- For input_preconditions, include input_type and necessity.
- For output_artifacts, include artifact_type and format.
- For constraints_boundaries, include polarity: positive_constraint or negative_boundary.
- For dependencies_resources, include dependency_type and necessity.

Do not add hierarchy links, selection summaries, parse warnings, broad relation fields, or side-effect fields outside the seven I3 fields.

Skill metadata:
- skill_id: {skill_id}
- skill_name: {skill_name}
- source: {source}

Skill artifact:
```markdown
{skill_artifact}
```"""

ACTIVE_USER_TEMPLATE = COMPACT_USER_TEMPLATE

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


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


def parse_scalar(raw: str) -> object:
    value = raw.strip()
    if not value:
        return ""
    if value[0] in {"'", '"'}:
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value.strip("'\"")
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    data: dict[str, object] = {}
    current_map: dict[str, object] | None = None
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  ") and current_map is not None:
            key, _, value = line.strip().partition(":")
            if key:
                current_map[key] = parse_scalar(value)
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        if not key:
            continue
        if value.strip():
            data[key] = parse_scalar(value)
            current_map = None
        else:
            nested: dict[str, object] = {}
            data[key] = nested
            current_map = nested
    return data, text[match.end() :]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_json(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def slug(value: str) -> str:
    cleaned = "".join(char if char.isalnum() or char in "-._" else "_" for char in value)
    return cleaned.strip("_") or "default"


def normalize_base_url(base_url: str) -> str:
    return base_url.rstrip("/")


def chat_endpoint(base_url: str) -> str:
    base = normalize_base_url(base_url)
    if base.endswith("/v1"):
        return f"{base}/chat/completions"
    return f"{base}/chat/completions"


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


def extract_json_object(text: str) -> dict[str, Any]:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        raise ValueError("Model response did not contain a JSON object.")
    return json.loads(match.group(0))


def truncate_skill_text(text: str, max_chars: int) -> tuple[str, bool]:
    if len(text) <= max_chars:
        return text, False
    return text[:max_chars] + "\n\n[TRUNCATED FOR I3M INPUT]\n", True


def canonical_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip()).lower()


def evidence_match(evidence: str, artifact: str) -> dict[str, bool]:
    evidence = str(evidence or "").strip()
    if not evidence:
        return {"exact": False, "case_insensitive": False, "whitespace_insensitive": False}
    return {
        "exact": evidence in artifact,
        "case_insensitive": evidence.lower() in artifact.lower(),
        "whitespace_insensitive": canonical_ws(evidence) in canonical_ws(artifact),
    }


def repair_evidence_quote(evidence: str, artifact: str) -> tuple[str, list[str]]:
    """Return a direct source substring when the model supplied a near-quote.

    The repair is intentionally narrow: it only accepts candidates that already
    occur verbatim in the artifact. This fixes common model formatting habits
    such as adding "Not for" to a bullet or unescaping quotes from YAML strings.
    """
    evidence = str(evidence or "").strip()
    notes: list[str] = []
    if not evidence:
        return evidence, notes
    if evidence_match(evidence, artifact)["case_insensitive"]:
        return evidence, notes

    candidates = [
        evidence.replace('"', r"\""),
        evidence.replace("'", r"\'"),
    ]
    prefixes = [
        "Not for: ",
        "Not for ",
        "Use when: ",
        "Use when ",
        "Expected output: ",
        "External Dependencies To Preserve: ",
        "Dependency Profile: ",
    ]
    for prefix in prefixes:
        if evidence.startswith(prefix):
            candidates.append(evidence[len(prefix) :].strip())
    for marker in ["\n- ", ": "]:
        if marker in evidence:
            parts = [part.strip() for part in evidence.split(marker) if part.strip()]
            candidates.extend(parts)
    # Keep enough context to be meaningful, but allow a narrower direct quote.
    words = re.findall(r"[A-Za-z0-9_./`-]+", evidence)
    if len(words) >= 2:
        candidates.append(" ".join(words[: min(8, len(words))]))
        candidates.append(" ".join(words[-min(8, len(words)) :]))

    seen: set[str] = set()
    for candidate in candidates:
        candidate = candidate.strip().strip("`")
        if not candidate or candidate in seen:
            continue
        seen.add(candidate)
        if evidence_match(candidate, artifact)["case_insensitive"]:
            notes.append("evidence_repaired_to_direct_source_substring")
            return candidate, notes
    return evidence, notes


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


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")


def load_r1_map(path: Path) -> dict[tuple[str, str], dict[str, Any]]:
    rows = load_jsonl(path)
    return {(str(row.get("family")), str(row.get("skill"))): row for row in rows}


def collect_skill_records(skills_root: Path, r1_path: Path) -> list[dict[str, Any]]:
    r1_map = load_r1_map(r1_path)
    records: list[dict[str, Any]] = []
    for path in sorted(skills_root.glob("*/*/SKILL.md")):
        artifact = read_text(path)
        frontmatter, _ = parse_frontmatter(artifact)
        family = path.parts[-3]
        name = str(frontmatter.get("name") or path.parent.name)
        r1 = r1_map.get((family, name), {})
        records.append(
            {
                "skill": name,
                "name": name,
                "family": family,
                "path": str(path),
                "source": str(path),
                "description": str(frontmatter.get("description") or r1.get("description") or ""),
                "is_main_evaluated": bool(r1.get("is_main_evaluated", False)),
                "artifact": artifact,
                "artifact_sha256": sha256_text(artifact),
            }
        )
    return records


def collect_external_jsonl_records(
    input_jsonl: Path,
    family_label: str,
    offset: int,
    limit: int | None,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with input_jsonl.open("r", encoding="utf-8") as handle:
        for index, line in enumerate(handle):
            if index < offset or not line.strip():
                continue
            row = json.loads(line)
            skill_id = str(row.get("skill_id") or row.get("skill") or row.get("id") or "")
            if not skill_id:
                continue
            text = str(row.get("text") or row.get("body") or row.get("artifact") or "")
            if not text:
                continue
            name = str(row.get("name") or skill_id)
            description = str(row.get("description") or "")
            records.append(
                {
                    "skill": skill_id,
                    "name": name,
                    "family": family_label,
                    "path": str(input_jsonl),
                    "source": str(row.get("source") or row.get("representation") or input_jsonl),
                    "description": description,
                    "is_main_evaluated": False,
                    "artifact": text,
                    "artifact_sha256": sha256_text(text),
                    "external_row": {
                        "in_easy": row.get("in_easy"),
                        "in_hard": row.get("in_hard"),
                        "is_hard_only": row.get("is_hard_only"),
                        "tokens_approx": row.get("tokens_approx"),
                    },
                }
            )
            if limit is not None and len(records) >= limit:
                break
    return records


def skill_group(record: dict[str, Any]) -> str:
    family = record["family"]
    if family.startswith("skillrouter_eval_core"):
        return "skillrouter_eval_core"
    if family == "public_imported_background":
        return "public_imported_background"
    if family == "background_scale":
        return "background_scale"
    if family in {"public_style_controlled", "implicit_field_stress"}:
        return "public_style_or_implicit_controlled"
    if record.get("is_main_evaluated"):
        return "controlled_core"
    return "other_local"


def select_pilot(records: list[dict[str, Any]], seed: int) -> list[dict[str, Any]]:
    quotas = {
        "controlled_core": 20,
        "public_imported_background": 20,
        "public_style_or_implicit_controlled": 10,
        "background_scale": 10,
    }
    rng = random.Random(seed)
    by_group: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        by_group[skill_group(record)].append(record)
    selected: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for group, quota in quotas.items():
        candidates = sorted(by_group.get(group, []), key=lambda row: (row["family"], row["skill"]))
        rng.shuffle(candidates)
        for record in candidates[:quota]:
            key = (record["family"], record["skill"])
            if key not in seen:
                selected.append(record)
                seen.add(key)
    return selected


def selected_records(args: argparse.Namespace, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if args.mode == "pilot":
        selected = select_pilot(records, args.seed)
    else:
        selected = records
    if args.only:
        wanted: set[tuple[str, str]] = set()
        for item in args.only:
            if "/" not in item:
                raise SystemExit(f"--only must use family/skill format, got: {item}")
            family, skill = item.split("/", 1)
            wanted.add((family, skill))
        selected = [row for row in selected if (row["family"], row["skill"]) in wanted]
    if args.limit is not None:
        selected = selected[: args.limit]
    return selected


class ChatParser:
    def __init__(
        self,
        provider: str,
        base_url: str,
        model: str,
        api_key: str,
        cache_dir: Path,
        timeout: int,
        max_retries: int,
        max_output_tokens: int,
        thinking: str,
    ) -> None:
        self.provider = provider
        self.base_url = base_url
        self.model = model
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.max_output_tokens = max_output_tokens
        self.thinking = thinking
        self.cache_dir = cache_dir / "i3m_parse" / provider / slug(model)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.api_calls = 0
        self.cache_hits = 0

    def cache_path(self, prompt: str, artifact_sha256: str) -> Path:
        key = sha256_json(
            {
                "schema_version": SCHEMA_VERSION,
                "provider": self.provider,
                "base_url": self.base_url,
                "model": self.model,
                "thinking": self.thinking,
                "system_prompt_sha256": sha256_text(SYSTEM_PROMPT),
                "user_prompt_sha256": sha256_text(prompt),
                "artifact_sha256": artifact_sha256,
            }
        )
        return self.cache_dir / f"{key}.json"

    def parse(self, prompt: str, artifact_sha256: str) -> dict[str, Any]:
        path = self.cache_path(prompt, artifact_sha256)
        if path.exists():
            self.cache_hits += 1
            return json.loads(path.read_text(encoding="utf-8"))

        payload: dict[str, Any] = {
            "model": self.model,
            "temperature": 0,
            "max_tokens": self.max_output_tokens,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            "response_format": {"type": "json_object"},
        }
        if self.thinking != "provider_default":
            payload["thinking"] = {"type": self.thinking}
        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                response = post_json(chat_endpoint(self.base_url), self.api_key, payload, self.timeout)
                content = response["choices"][0]["message"]["content"]
                result = extract_json_object(content)
                path.write_text(
                    json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )
                self.api_calls += 1
                return result
            except Exception as exc:  # noqa: BLE001 - provider details are useful after retries.
                last_error = exc
                if attempt < self.max_retries:
                    time.sleep(1.5 * (attempt + 1))
        raise RuntimeError(f"Model parse failed after retries: {last_error}") from last_error


def build_prompt(record: dict[str, Any], artifact: str) -> str:
    return (
        ACTIVE_USER_TEMPLATE.replace("{skill_id}", str(record["skill"]))
        .replace("{skill_name}", str(record["name"]))
        .replace("{source}", str(record["source"]))
        .replace("{skill_artifact}", artifact)
    )


def normalize_confidence(value: Any) -> float:
    try:
        return max(0.0, min(1.0, float(value)))
    except (TypeError, ValueError):
        return 0.0


def normalize_item(
    field: str,
    item: Any,
    artifact: str,
    issues: list[str],
    warnings: list[str],
) -> dict[str, Any] | None:
    if not isinstance(item, dict):
        issues.append(f"{field}: non-object item dropped")
        return None
    allowed_keys = SELECTOR_ITEM_KEYS[field]
    normalized: dict[str, Any] = {}
    dropped_keys = sorted(key for key in item.keys() if key not in allowed_keys)
    if dropped_keys:
        normalized["_dropped_item_keys"] = dropped_keys

    prefix = FIELD_ID_PREFIX[field]
    item_id = str(item.get("id") or "").strip()
    repair_notes: list[str] = []
    if not item_id.startswith(prefix):
        suffix_match = re.search(r"(\d+)$", item_id)
        index = suffix_match.group(1) if suffix_match else "1"
        item_id = f"{prefix}{index}"
        repair_notes.append("id_prefix_repaired")
    normalized["id"] = item_id

    text = str(item.get("text") or item.get("action") or "").strip()
    evidence = str(item.get("evidence") or "").strip()
    if not text:
        issues.append(f"{field}/{item_id}: missing text")
    if not evidence:
        issues.append(f"{field}/{item_id}: missing evidence")
        return None

    evidence, evidence_repair_notes = repair_evidence_quote(evidence, artifact)
    repair_notes.extend(evidence_repair_notes)
    normalized["text"] = text[:1000]
    normalized["evidence"] = evidence[:500]
    status = str(item.get("evidence_status") or "implicit").strip().lower()
    if status not in {"explicit", "implicit"}:
        issues.append(f"{field}/{item_id}: invalid evidence_status '{status}'")
        status = "implicit"
    normalized["evidence_status"] = status
    normalized["confidence"] = normalize_confidence(item.get("confidence", 0.0))

    for key in sorted(allowed_keys - {"id", "text", "evidence", "evidence_status", "confidence"}):
        if key in item:
            normalized[key] = item[key]
    matches = evidence_match(evidence, artifact)
    normalized["_evidence_match"] = matches
    if repair_notes:
        normalized["_repair_notes"] = repair_notes
    if not matches["case_insensitive"]:
        warnings.append(f"{field}/{item_id}: dropped item because evidence not found in artifact")
        return None
    return normalized


def normalize_i3m(raw: dict[str, Any], record: dict[str, Any], artifact: str, truncated: bool) -> dict[str, Any]:
    issues: list[str] = []
    warnings: list[str] = []
    dropped_top_keys = sorted(key for key in raw.keys() if key not in ALLOWED_TOP_KEYS)
    if str(raw.get("schema_version")) != SCHEMA_VERSION:
        issues.append("schema_version missing or mismatched")

    fields: dict[str, list[dict[str, Any]]] = {}
    for field in I3_FIELDS:
        raw_items = raw.get(field, [])
        if raw_items is None:
            raw_items = []
        if not isinstance(raw_items, list):
            issues.append(f"{field}: expected list, got {type(raw_items).__name__}")
            raw_items = []
        normalized_items: list[dict[str, Any]] = []
        for item in raw_items:
            normalized_item = normalize_item(field, item, artifact, issues, warnings)
            if normalized_item is not None:
                normalized_items.append(normalized_item)
        fields[field] = normalized_items

    row = {
        "schema_version": SCHEMA_VERSION,
        "representation": "I3M_model_parsed",
        "skill": record["skill"],
        "name": record["name"],
        "family": record["family"],
        "group": skill_group(record),
        "source": record["source"],
        "description": record["description"],
        "is_main_evaluated": record["is_main_evaluated"],
        "artifact_sha256": record["artifact_sha256"],
        "input_truncated": truncated,
        "artifact_language": str(raw.get("artifact_language") or "unknown"),
        "dropped_top_keys": dropped_top_keys,
        "fields": fields,
        "validation": {
            "issues": issues,
            "warnings": warnings,
            "valid_schema": not issues and not dropped_top_keys,
            "dropped_top_keys": dropped_top_keys,
        },
    }
    row["text"] = selector_text(row)
    return row


def selector_text(row: dict[str, Any]) -> str:
    parts = [
        f"name: {row['name']}",
        f"family: {row['family']}",
        f"description: {row['description']}",
    ]
    fields: dict[str, list[dict[str, Any]]] = row["fields"]
    for field in I3_FIELDS:
        items = fields.get(field, [])
        if items:
            parts.append(f"{field}:")
            for item in items:
                text = str(item.get("text") or "").strip()
                if text:
                    parts.append(f"- {text}")
    return "\n".join(parts).strip()


def row_key(row: dict[str, Any]) -> tuple[str, str]:
    return (str(row.get("family")), str(row.get("skill")))


def completed_keys(path: Path, retry_failed: bool = False) -> set[tuple[str, str]]:
    keys: set[tuple[str, str]] = set()
    for row in load_jsonl(path):
        if retry_failed and row.get("parse_failed"):
            continue
        keys.add(row_key(row))
    return keys


def latest_selected_rows(
    rows: list[dict[str, Any]],
    selected: list[dict[str, Any]],
    retry_failed: bool = False,
) -> list[dict[str, Any]]:
    latest: dict[tuple[str, str], dict[str, Any]] = {}
    for row in rows:
        key = row_key(row)
        if retry_failed and row.get("parse_failed") and key in latest:
            continue
        latest[key] = row
    output: list[dict[str, Any]] = []
    for record in selected:
        key = (record["family"], record["skill"])
        if key in latest:
            output.append(latest[key])
    return output


def parse_record(record: dict[str, Any], args: argparse.Namespace, client: ChatParser) -> dict[str, Any]:
    artifact, truncated = truncate_skill_text(record["artifact"], args.max_chars)
    prompt = build_prompt(record, artifact)
    raw = client.parse(prompt, record["artifact_sha256"])
    row = normalize_i3m(raw, record, artifact, truncated)
    row["provider"] = args.provider
    row["model"] = args.model
    row["system_prompt_sha256"] = sha256_text(SYSTEM_PROMPT)
    row["user_template_sha256"] = sha256_text(ACTIVE_USER_TEMPLATE)
    row["max_chars"] = args.max_chars
    return row


def parse_record_with_fallback(
    record: dict[str, Any],
    args: argparse.Namespace,
    client: ChatParser,
    fallback_client: ChatParser | None,
) -> dict[str, Any]:
    try:
        return parse_record(record, args, client)
    except Exception as primary_exc:  # noqa: BLE001 - optionally recover with a stabler model.
        if fallback_client is None:
            raise
        fallback_args = argparse.Namespace(**vars(args))
        fallback_args.model = fallback_client.model
        row = parse_record(record, fallback_args, fallback_client)
        row["fallback_from_model"] = args.model
        row["primary_parse_error"] = str(primary_exc)[:1000]
        return row


def failed_parse_row(record: dict[str, Any], args: argparse.Namespace, error: Exception) -> dict[str, Any]:
    row = {
        "schema_version": SCHEMA_VERSION,
        "representation": "I3M_model_parsed",
        "skill": record["skill"],
        "name": record["name"],
        "family": record["family"],
        "group": skill_group(record),
        "source": record["source"],
        "description": record["description"],
        "is_main_evaluated": record["is_main_evaluated"],
        "artifact_sha256": record["artifact_sha256"],
        "input_truncated": len(record["artifact"]) > args.max_chars,
        "artifact_language": "unknown",
        "dropped_top_keys": [],
        "fields": {field: [] for field in I3_FIELDS},
        "validation": {
            "issues": [f"model_parse_failed: {str(error)[:500]}"],
            "warnings": [],
            "valid_schema": False,
            "dropped_top_keys": [],
        },
        "parse_failed": True,
        "parse_error": str(error)[:1000],
        "provider": args.provider,
        "model": args.model,
        "system_prompt_sha256": sha256_text(SYSTEM_PROMPT),
        "user_template_sha256": sha256_text(ACTIVE_USER_TEMPLATE),
        "max_chars": args.max_chars,
    }
    row["text"] = selector_text(row)
    return row


def summarize(rows: list[dict[str, Any]], provider: str, model: str) -> dict[str, Any]:
    total_items = 0
    exact_found = 0
    ci_found = 0
    loose_found = 0
    field_counts = Counter()
    nonempty_skills = Counter()
    group_counts = Counter(row.get("group") for row in rows)
    issue_counts = Counter()
    warning_counts = Counter()

    for row in rows:
        for issue in row.get("validation", {}).get("issues", []):
            issue_counts[issue.split(":")[0]] += 1
        for warning in row.get("validation", {}).get("warnings", []):
            warning_counts[warning.split(":")[0]] += 1
        for field, items in row.get("fields", {}).items():
            if items:
                nonempty_skills[field] += 1
            for item in items:
                total_items += 1
                field_counts[field] += 1
                matches = item.get("_evidence_match", {})
                exact_found += int(bool(matches.get("exact")))
                ci_found += int(bool(matches.get("case_insensitive")))
                loose_found += int(bool(matches.get("whitespace_insensitive")))

    valid_rows = sum(1 for row in rows if not row.get("validation", {}).get("issues") and not row.get("dropped_top_keys"))
    return {
        "schema_version": SCHEMA_VERSION,
        "provider": provider,
        "model": model,
        "rows": len(rows),
        "valid_rows": valid_rows,
        "valid_row_rate": valid_rows / len(rows) if rows else 0.0,
        "group_counts": dict(group_counts),
        "field_item_counts": dict(field_counts),
        "field_nonempty_skill_counts": dict(nonempty_skills),
        "total_extracted_items": total_items,
        "evidence_exact_rate": exact_found / total_items if total_items else 0.0,
        "evidence_case_insensitive_rate": ci_found / total_items if total_items else 0.0,
        "evidence_whitespace_insensitive_rate": loose_found / total_items if total_items else 0.0,
        "rows_with_issues": sum(1 for row in rows if row.get("validation", {}).get("issues")),
        "rows_with_warnings": sum(1 for row in rows if row.get("validation", {}).get("warnings")),
        "rows_with_dropped_top_keys": sum(1 for row in rows if row.get("dropped_top_keys")),
        "input_truncated_rows": sum(1 for row in rows if row.get("input_truncated")),
        "parse_failed_rows": sum(1 for row in rows if row.get("parse_failed")),
        "fallback_rows": sum(1 for row in rows if row.get("fallback_from_model")),
        "issue_counts_by_prefix": dict(issue_counts.most_common()),
        "warning_counts_by_prefix": dict(warning_counts.most_common()),
    }


def manual_packet_rows(rows: list[dict[str, Any]], seed: int, limit: int) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    selected: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    issue_rows = [row for row in rows if row.get("validation", {}).get("issues") or row.get("dropped_top_keys")]
    for row in issue_rows[: max(5, limit // 4)]:
        key = (row["family"], row["skill"])
        selected.append(row)
        seen.add(key)
    by_group: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_group[row.get("group", "unknown")].append(row)
    for group_rows in by_group.values():
        rng.shuffle(group_rows)
        for row in group_rows[:2]:
            key = (row["family"], row["skill"])
            if key not in seen:
                selected.append(row)
                seen.add(key)
    remaining = [row for row in rows if (row["family"], row["skill"]) not in seen]
    rng.shuffle(remaining)
    for row in remaining:
        if len(selected) >= limit:
            break
        selected.append(row)
    return selected[:limit]


def write_report(report_path: Path, rows: list[dict[str, Any]], summary: dict[str, Any], seed: int) -> None:
    lines = [
        f"# I3M Model Parse Report ({summary['schema_version']})",
        "",
        f"- Provider/model: `{summary['provider']}` / `{summary['model']}`",
        f"- Parsed rows: {summary['rows']}",
        f"- Valid rows: {summary['valid_rows']} ({summary['valid_row_rate']:.1%})",
        f"- Extracted items: {summary['total_extracted_items']}",
        f"- Evidence exact match rate: {summary['evidence_exact_rate']:.1%}",
        f"- Evidence case-insensitive match rate: {summary['evidence_case_insensitive_rate']:.1%}",
        f"- Evidence whitespace-insensitive match rate: {summary['evidence_whitespace_insensitive_rate']:.1%}",
        f"- Rows with validation issues: {summary['rows_with_issues']}",
        f"- Rows with QA warnings: {summary['rows_with_warnings']}",
        f"- Rows with dropped top-level keys: {summary['rows_with_dropped_top_keys']}",
        f"- Parse-failed rows: {summary['parse_failed_rows']}",
        f"- Fallback-model rows: {summary['fallback_rows']}",
        f"- Input-truncated rows: {summary['input_truncated_rows']}",
        "",
        "## Group Counts",
        "",
    ]
    for group, count in sorted(summary["group_counts"].items()):
        lines.append(f"- `{group}`: {count}")
    lines.extend(["", "## Field Coverage", ""])
    for field in I3_FIELDS:
        item_count = summary["field_item_counts"].get(field, 0)
        skill_count = summary["field_nonempty_skill_counts"].get(field, 0)
        lines.append(f"- `{field}`: {skill_count} skills, {item_count} items")
    lines.extend(["", "## Issue Prefix Counts", ""])
    if summary["issue_counts_by_prefix"]:
        for issue, count in summary["issue_counts_by_prefix"].items():
            lines.append(f"- `{issue}`: {count}")
    else:
        lines.append("- None")
    lines.extend(["", "## Warning Prefix Counts", ""])
    if summary.get("warning_counts_by_prefix"):
        for warning, count in summary["warning_counts_by_prefix"].items():
            lines.append(f"- `{warning}`: {count}")
    else:
        lines.append("- None")
    lines.extend(["", "## Manual Review Packet", ""])
    for row in manual_packet_rows(rows, seed, 24):
        lines.extend(
            [
                f"### {row['family']}/{row['skill']}",
                "",
                f"- Group: `{row.get('group')}`",
                f"- Source: `{row.get('source')}`",
                f"- Description: {row.get('description')}",
                f"- Validation issues: {row.get('validation', {}).get('issues') or []}",
                f"- QA warnings: {row.get('validation', {}).get('warnings') or []}",
                f"- Dropped top-level keys: {row.get('dropped_top_keys') or []}",
                "",
            ]
        )
        for field in I3_FIELDS:
            items = row.get("fields", {}).get(field, [])
            if not items:
                continue
            lines.append(f"**{field}**")
            for item in items[:4]:
                text = str(item.get("text") or "")
                evidence = str(item.get("evidence") or "")
                matches = item.get("_evidence_match", {})
                lines.append(
                    f"- {text} | evidence: `{evidence[:160]}` | exact={matches.get('exact')} ci={matches.get('case_insensitive')}"
                )
            lines.append("")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def representation_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in rows:
        compact = {
            "representation": "I3M_model_parsed",
            "schema_version": row["schema_version"],
            "skill": row["skill"],
            "name": row["name"],
            "family": row["family"],
            "group": row.get("group"),
            "description": row.get("description"),
            "is_main_evaluated": row.get("is_main_evaluated"),
            "source": row.get("source"),
            "fields": {
                field: [
                    {
                        key: value
                        for key, value in item.items()
                        if key in SELECTOR_ITEM_KEYS[field]
                    }
                    for item in row.get("fields", {}).get(field, [])
                ]
                for field in I3_FIELDS
            },
            "text": row.get("text", ""),
            "provider": row.get("provider"),
            "model": row.get("model"),
            "parse_failed": bool(row.get("parse_failed")),
            "fallback_from_model": row.get("fallback_from_model"),
        }
        output.append(compact)
    return output


def default_paths(repo_root: Path, mode: str) -> tuple[Path, Path, Path]:
    if mode == "pilot":
        base = repo_root / "outputs" / "i3m"
        return (
            base / "local_i3m_pilot_model_parse.jsonl",
            base / "local_i3m_pilot_representation.jsonl",
            base / "local_i3m_pilot_model_parse_report.md",
        )
    return (
        repo_root / "outputs" / "i3m" / "local_i3m_full_model_parse.jsonl",
        repo_root / "representations" / "I3M_model_parsed.jsonl",
        repo_root / "outputs" / "i3m" / "local_i3m_full_model_parse_report.md",
    )


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Model-parse local SKILL.md files into the I3M information layer.")
    parser.add_argument("--mode", choices=["pilot", "full"], default="pilot")
    parser.add_argument("--skills-root", default=str(repo_root / "skills"))
    parser.add_argument("--r1-jsonl", default=str(repo_root / "representations" / "R1_flat_metadata.jsonl"))
    parser.add_argument("--input-jsonl", help="Parse external JSONL rows with text/body/artifact fields instead of local skills.")
    parser.add_argument("--family-label", default="skillrouter_eval_core")
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--output-jsonl")
    parser.add_argument("--representation-jsonl")
    parser.add_argument("--report-md")
    parser.add_argument("--dotenv", default=".env")
    parser.add_argument("--provider", default="deepseek")
    parser.add_argument("--base-url", default=os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com"))
    parser.add_argument("--model", default=os.environ.get("DEEPSEEK_MODEL", "deepseek-v4-flash"))
    parser.add_argument("--fallback-model")
    parser.add_argument("--key-env", default="DEEPSEEK_API_KEY")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--only", action="append", default=[], help="Restrict to family/skill. Can be repeated.")
    parser.add_argument("--seed", type=int, default=4990)
    parser.add_argument("--max-chars", type=int, default=22000)
    parser.add_argument("--max-output-tokens", type=int, default=5000)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--max-retries", type=int, default=2)
    parser.add_argument(
        "--thinking",
        choices=["disabled", "enabled", "provider_default"],
        default="disabled",
        help="DeepSeek thinking mode control. Disabled is preferred for deterministic JSON extraction.",
    )
    parser.add_argument("--cache-dir", default=str(repo_root / "runtime" / "provider_cache"))
    parser.add_argument("--concurrency", type=int, default=2)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--retry-failed", action="store_true", help="Treat parse_failed rows as pending and summarize latest row per skill.")
    parser.add_argument("--stop-on-error", action="store_true")
    args = parser.parse_args()

    output_default, representation_default, report_default = default_paths(repo_root, args.mode)
    output_jsonl = Path(args.output_jsonl) if args.output_jsonl else output_default
    representation_jsonl = Path(args.representation_jsonl) if args.representation_jsonl else representation_default
    report_md = Path(args.report_md) if args.report_md else report_default

    load_dotenv(Path(args.dotenv))
    api_key = os.environ.get(args.key_env)
    if not api_key:
        raise SystemExit(
            f"Missing {args.key_env}. Add it to .env, or pass --key-env for another OpenAI-compatible provider."
        )

    if args.force:
        for path in [output_jsonl, representation_jsonl, report_md]:
            if path.exists():
                path.unlink()

    if args.input_jsonl:
        records = collect_external_jsonl_records(
            Path(args.input_jsonl),
            args.family_label,
            max(0, args.offset),
            args.limit,
        )
    else:
        records = collect_skill_records(Path(args.skills_root), Path(args.r1_jsonl))
    selected = selected_records(args, records)
    done = completed_keys(output_jsonl, retry_failed=args.retry_failed)
    pending = [row for row in selected if (row["family"], row["skill"]) not in done]
    client = ChatParser(
        provider=args.provider,
        base_url=args.base_url,
        model=args.model,
        api_key=api_key,
        cache_dir=Path(args.cache_dir),
        timeout=args.timeout,
        max_retries=args.max_retries,
        max_output_tokens=args.max_output_tokens,
        thinking=args.thinking,
    )
    fallback_client = None
    if args.fallback_model:
        fallback_client = ChatParser(
            provider=args.provider,
            base_url=args.base_url,
            model=args.fallback_model,
            api_key=api_key,
            cache_dir=Path(args.cache_dir),
            timeout=args.timeout,
            max_retries=args.max_retries,
            max_output_tokens=args.max_output_tokens,
            thinking=args.thinking,
        )

    print(f"Mode: {args.mode}")
    print(f"Selected skills: {len(selected)}")
    print(f"Pending skills at start: {len(pending)}")
    print(f"Output JSONL: {output_jsonl}")
    print(f"Representation JSONL: {representation_jsonl}")
    print(f"Report MD: {report_md}")

    append_lock = Lock()
    processed = 0
    concurrency = max(1, args.concurrency)
    if concurrency == 1:
        for record in pending:
            try:
                row = parse_record_with_fallback(record, args, client, fallback_client)
            except Exception as exc:  # noqa: BLE001 - keep long batch jobs resumable.
                if args.stop_on_error:
                    raise RuntimeError(f"I3M parse failed for {record['family']}/{record['skill']}: {exc}") from exc
                row = failed_parse_row(record, args, exc)
            append_jsonl(output_jsonl, row)
            processed += 1
            if processed % 10 == 0 or processed == len(pending):
                print(f"Progress: {processed}/{len(pending)} new rows", flush=True)
    else:
        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            futures = {
                executor.submit(parse_record_with_fallback, record, args, client, fallback_client): record
                for record in pending
            }
            for future in as_completed(futures):
                record = futures[future]
                try:
                    row = future.result()
                except Exception as exc:  # noqa: BLE001 - identify failed skill before exiting.
                    if args.stop_on_error:
                        raise RuntimeError(f"I3M parse failed for {record['family']}/{record['skill']}: {exc}") from exc
                    row = failed_parse_row(record, args, exc)
                with append_lock:
                    append_jsonl(output_jsonl, row)
                processed += 1
                if processed % 10 == 0 or processed == len(pending):
                    print(f"Progress: {processed}/{len(pending)} new rows", flush=True)

    all_rows = load_jsonl(output_jsonl)
    selected_rows = latest_selected_rows(all_rows, selected, retry_failed=args.retry_failed)
    rep_rows = representation_rows(selected_rows)
    write_jsonl(representation_jsonl, rep_rows)
    summary = summarize(selected_rows, args.provider, args.model)
    write_report(report_md, selected_rows, summary, args.seed)
    summary_path = report_md.with_suffix(".summary.json")
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"New parsed skills: {processed}")
    print(f"Cache hits: {client.cache_hits}")
    print(f"API calls: {client.api_calls}")
    if fallback_client is not None:
        print(f"Fallback cache hits: {fallback_client.cache_hits}")
        print(f"Fallback API calls: {fallback_client.api_calls}")
    print(f"Valid row rate: {summary['valid_row_rate']:.1%}")
    print(f"Evidence exact rate: {summary['evidence_exact_rate']:.1%}")
    print(f"Evidence case-insensitive rate: {summary['evidence_case_insensitive_rate']:.1%}")
    print(f"Wrote {output_jsonl}")
    print(f"Wrote {representation_jsonl}")
    print(f"Wrote {report_md}")
    print(f"Wrote {summary_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Interrupted.", file=sys.stderr)
        raise SystemExit(130)
