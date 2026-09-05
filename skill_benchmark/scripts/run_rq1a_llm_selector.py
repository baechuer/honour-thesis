#!/usr/bin/env python3
"""Run an LLM selector diagnostic over RQ1a field-discriminability suites.

This is not a retriever benchmark. It asks whether a reasoning selector can use
the same selector-visible representations from the RQ1a clusters to identify the
gold skill, while avoiding option-id/order leakage.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.append(str(SCRIPT_DIR))

from run_provider_selectors import load_dotenv  # noqa: E402
from run_rq1a_field_ablation import (  # noqa: E402
    approximate_tokens,
    doc_for_condition,
    load_suite,
    prompt_query_text,
)


PROMPT_TEMPLATE_VERSION = "rq1a_llm_selector_v1"
LABELS = ["A", "B", "C", "D", "E"]


SYSTEM_PROMPT = """You are a stateless skill-routing evaluator.
Use only the user request and candidate skill representations shown in this message.
Do not use candidate order, label names, outside knowledge, or assumptions not supported by the text.
If the provided candidate representations do not contain enough distinguishing evidence, return decision "ambiguous".
Keep evidence_quote and rationale concise, under 25 words each.
Return only one JSON object."""


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def resolve_dotenv(path_text: str, output_root: Path) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    for candidate in (Path.cwd() / path, output_root / path, output_root.parent / path):
        if candidate.exists():
            return candidate
    return Path.cwd() / path


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def stable_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def stable_candidate_order(prompt_id: str, condition: str, skill_ids: list[str]) -> list[str]:
    return sorted(
        skill_ids,
        key=lambda skill_id: stable_hash(f"{PROMPT_TEMPLATE_VERSION}|{prompt_id}|{condition}|{skill_id}"),
    )


def response_json_from_text(text: str) -> dict[str, Any]:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", stripped, flags=re.DOTALL)
        if not match:
            raise
        return json.loads(match.group(0))


def make_selector_prompt(
    *,
    field: str,
    condition: str,
    query_text: str,
    candidates: list[dict[str, str]],
) -> str:
    candidate_blocks = []
    for candidate in candidates:
        candidate_blocks.append(
            f"Candidate {candidate['label']}:\n{candidate['doc']}"
        )
    return "\n\n".join(
        [
            "User request used for routing:",
            query_text,
            f"Target information field under test: {field}",
            f"Representation condition: {condition}",
            "Candidate skill representations:",
            "\n\n---\n\n".join(candidate_blocks),
            "Task:",
            (
                "Select the single candidate skill that best matches the user request. "
                "If the candidates are indistinguishable from the provided text, return ambiguous."
            ),
            "Keep the JSON compact. Keep evidence_quote and rationale under 25 words each.",
            (
                "Return exactly this JSON shape: "
                '{"decision":"select|ambiguous","selected_label":"A|B|C|null",'
                '"evidence_field":"string","evidence_quote":"string",'
                '"rationale":"string","confidence":0.0}'
            ),
        ]
    )


def build_tasks(suite_dirs: list[Path], conditions: list[str]) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    for suite_dir in suite_dirs:
        prompts, units = load_suite(suite_dir)
        for prompt in prompts:
            unit = units[prompt["cluster_id"]]
            skills_by_id = {skill["skill_id"]: skill for skill in unit["skills"]}
            skill_ids = list(prompt["candidate_skill_ids"])
            query_text = prompt_query_text(prompt)
            for condition in conditions:
                ordered_skill_ids = stable_candidate_order(prompt["prompt_id"], condition, skill_ids)
                candidates = []
                for index, skill_id in enumerate(ordered_skill_ids):
                    label = LABELS[index]
                    doc = doc_for_condition(suite_dir, unit, skills_by_id[skill_id], condition)
                    candidates.append({"label": label, "skill_id": skill_id, "doc": doc})
                prompt_text = make_selector_prompt(
                    field=prompt["field"],
                    condition=condition,
                    query_text=query_text,
                    candidates=candidates,
                )
                doc_hash = stable_hash(
                    json.dumps(
                        {
                            "query_text": query_text,
                            "condition": condition,
                            "candidates": candidates,
                            "template": PROMPT_TEMPLATE_VERSION,
                        },
                        sort_keys=True,
                    )
                )
                tasks.append(
                    {
                        "suite_dir": str(suite_dir),
                        "suite_name": suite_dir.name,
                        "cluster_id": prompt["cluster_id"],
                        "field": prompt["field"],
                        "field_subtype": prompt.get("field_subtype"),
                        "prompt_id": prompt["prompt_id"],
                        "prompt_variant": prompt["prompt_variant"],
                        "condition": condition,
                        "query_text": query_text,
                        "gold_skill_id": prompt["gold_skill_id"],
                        "candidate_map": {
                            candidate["label"]: candidate["skill_id"] for candidate in candidates
                        },
                        "candidate_skill_ids_ordered": [candidate["skill_id"] for candidate in candidates],
                        "selector_prompt": prompt_text,
                        "selector_prompt_hash": stable_hash(prompt_text),
                        "task_hash": doc_hash,
                        "selector_visible_tokens": approximate_tokens(prompt_text),
                        "workflow_contrast_aspects": prompt.get("workflow_contrast_aspects"),
                        "workflow_policy_type": prompt.get("workflow_policy_type"),
                    }
                )
    return tasks


def call_chat_completion(
    *,
    base_url: str,
    api_key: str,
    model: str,
    prompt: str,
    timeout: int,
    temperature: float,
    max_tokens: int,
    retries: int,
    response_format: bool,
) -> dict[str, Any]:
    base = base_url.rstrip("/")
    if not base.endswith("/v1"):
        base = base + "/v1"
    url = base + "/chat/completions"
    payload: dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if response_format:
        payload["response_format"] = {"type": "json_object"}
    data = json.dumps(payload).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    last_error: str | None = None
    for attempt in range(retries + 1):
        request = urllib.request.Request(url, data=data, headers=headers, method="POST")
        try:
            started = time.monotonic()
            with urllib.request.urlopen(request, timeout=timeout) as response:
                body = json.loads(response.read().decode("utf-8"))
            elapsed = time.monotonic() - started
            content = body["choices"][0]["message"].get("content") or ""
            try:
                parsed = response_json_from_text(content)
            except json.JSONDecodeError as exc:
                last_error = f"JSON parse error: {exc}; content={content[:500]!r}"
                if response_format:
                    return call_chat_completion(
                        base_url=base_url,
                        api_key=api_key,
                        model=model,
                        prompt=prompt,
                        timeout=timeout,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        retries=retries,
                        response_format=False,
                    )
                raise
            return {
                "ok": True,
                "raw_response": body,
                "content": content,
                "parsed": parsed,
                "api_elapsed_s": elapsed,
            }
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            last_error = f"HTTP {exc.code}: {detail[:1000]}"
            if exc.code == 400 and response_format:
                return call_chat_completion(
                    base_url=base_url,
                    api_key=api_key,
                    model=model,
                    prompt=prompt,
                    timeout=timeout,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    retries=retries,
                    response_format=False,
                )
        except Exception as exc:  # noqa: BLE001
            last_error = repr(exc)
        if attempt < retries:
            time.sleep(min(2**attempt, 8))
    return {"ok": False, "error": last_error or "unknown error"}


def normalize_selection(parsed: dict[str, Any], candidate_map: dict[str, str]) -> tuple[str, str | None, str | None]:
    decision = str(parsed.get("decision", "")).strip().lower()
    raw_label = parsed.get("selected_label")
    selected_label = None if raw_label is None else str(raw_label).strip().upper()
    if selected_label in {"", "NULL", "NONE", "N/A"}:
        selected_label = None
    if decision not in {"select", "ambiguous"}:
        decision = "select" if selected_label in candidate_map else "ambiguous"
    selected_skill_id = candidate_map.get(selected_label) if selected_label else None
    if decision == "select" and selected_skill_id is None:
        decision = "ambiguous"
    return decision, selected_label, selected_skill_id


def run_one(
    task: dict[str, Any],
    *,
    base_url: str,
    api_key: str,
    model: str,
    timeout: int,
    retries: int,
    temperature: float,
    max_tokens: int,
) -> dict[str, Any]:
    result = call_chat_completion(
        base_url=base_url,
        api_key=api_key,
        model=model,
        prompt=task["selector_prompt"],
        timeout=timeout,
        temperature=temperature,
        max_tokens=max_tokens,
        retries=retries,
        response_format=True,
    )
    row = {key: value for key, value in task.items() if key != "selector_prompt"}
    row.update(
        {
            "model": model,
            "prompt_template_version": PROMPT_TEMPLATE_VERSION,
            "api_ok": result["ok"],
        }
    )
    if not result["ok"]:
        row.update({"error": result.get("error"), "decision": "error", "correct": 0.0})
        return row

    parsed = result["parsed"]
    decision, selected_label, selected_skill_id = normalize_selection(parsed, task["candidate_map"])
    correct = 1.0 if selected_skill_id == task["gold_skill_id"] else 0.0
    row.update(
        {
            "decision": decision,
            "selected_label": selected_label,
            "selected_skill_id": selected_skill_id,
            "correct": correct,
            "evidence_field": parsed.get("evidence_field"),
            "evidence_quote": parsed.get("evidence_quote"),
            "rationale": parsed.get("rationale"),
            "confidence": parsed.get("confidence"),
            "api_elapsed_s": result.get("api_elapsed_s"),
            "usage": result["raw_response"].get("usage", {}),
            "raw_content": result.get("content"),
        }
    )
    return row


def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    buckets: dict[tuple[str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row.get("decision") == "error":
            continue
        buckets[
            (
                row["field"],
                row["condition"],
                row["prompt_variant"],
                row["model"],
            )
        ].append(row)

    summaries: list[dict[str, Any]] = []
    expanded: dict[tuple[str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row.get("decision") == "error":
            continue
        for variant in (row["prompt_variant"], "combined"):
            expanded[(row["field"], row["condition"], variant, row["model"])].append(row)

    for (field, condition, variant, model), items in sorted(expanded.items()):
        n = len(items)
        if not n:
            continue
        summaries.append(
            {
                "field": field,
                "condition": condition,
                "prompt_variant": variant,
                "model": model,
                "n": n,
                "accuracy": sum(row.get("correct", 0.0) for row in items) / n,
                "ambiguous_rate": sum(1 for row in items if row.get("decision") == "ambiguous") / n,
                "selection_rate": sum(1 for row in items if row.get("decision") == "select") / n,
                "mean_selector_visible_tokens": sum(row.get("selector_visible_tokens", 0) for row in items) / n,
            }
        )
    return summaries


def render_markdown(rows: list[dict[str, Any]], summaries: list[dict[str, Any]]) -> str:
    lines = [
        "# RQ1a LLM Selector Diagnostic",
        "",
        f"- Prompt template: `{PROMPT_TEMPLATE_VERSION}`",
        "- Selector sees the same RQ1a user prompt and candidate representations as the field-isolation runner.",
        "- Candidate labels are shuffled per prompt/condition and real `option-a/b/c` skill IDs are hidden from the model.",
        "- The model may return `ambiguous` when the visible candidate representations do not contain distinguishing evidence.",
        "",
        "## Summary",
        "",
        "| Field | Condition | Prompt subset | Model | n | Accuracy | Ambiguous rate | Selection rate | Mean visible tokens |",
        "|---|---|---|---|---:|---:|---:|---:|---:|",
    ]
    for item in summaries:
        lines.append(
            f"| `{item['field']}` | `{item['condition']}` | `{item['prompt_variant']}` | `{item['model']}` | "
            f"{item['n']} | {item['accuracy']:.3f} | {item['ambiguous_rate']:.3f} | "
            f"{item['selection_rate']:.3f} | {item['mean_selector_visible_tokens']:.1f} |"
        )

    by_key = {
        (item["field"], item["model"], item["prompt_variant"], item["condition"]): item
        for item in summaries
    }
    lines.extend(
        [
            "",
            "## Field Lift",
            "",
            "| Field | Model | Prompt subset | Hidden accuracy | +Field accuracy | Accuracy lift | Hidden ambiguity | +Field ambiguity |",
            "|---|---|---|---:|---:|---:|---:|---:|",
        ]
    )
    fields = sorted({item["field"] for item in summaries})
    models = sorted({item["model"] for item in summaries})
    variants = ["direct", "paraphrase", "contextual", "implicit_authority", "combined"]
    for field in fields:
        for model in models:
            for variant in variants:
                hidden = by_key.get((field, model, variant, "shared_context_only"))
                exposed = by_key.get((field, model, variant, "shared_context_plus_field"))
                if not hidden or not exposed:
                    continue
                lines.append(
                    f"| `{field}` | `{model}` | `{variant}` | {hidden['accuracy']:.3f} | "
                    f"{exposed['accuracy']:.3f} | {exposed['accuracy'] - hidden['accuracy']:+.3f} | "
                    f"{hidden['ambiguous_rate']:.3f} | {exposed['ambiguous_rate']:.3f} |"
                )

    failures = [
        row
        for row in rows
        if row.get("condition") == "shared_context_plus_field"
        and row.get("decision") != "error"
        and row.get("correct", 0.0) < 1
    ][:30]
    lines.extend(["", "## First +Field Misses", ""])
    if not failures:
        lines.append("- No +field misses.")
    else:
        lines.extend(
            [
                "| Field | Prompt | Variant | Decision | Selected | Gold | Rationale |",
                "|---|---|---|---|---|---|---|",
            ]
        )
        for row in failures:
            rationale = str(row.get("rationale") or "").replace("|", "\\|")
            lines.append(
                f"| `{row['field']}` | `{row['prompt_id']}` | `{row['prompt_variant']}` | "
                f"`{row.get('decision')}` | `{row.get('selected_skill_id')}` | `{row.get('gold_skill_id')}` | {rationale} |"
            )
    return "\n".join(lines) + "\n"


def discover_suites(root: Path, requested: str) -> list[Path]:
    base = root / "rq1a_field_discriminability"
    if requested == "all":
        return sorted(path for path in base.iterdir() if (path / "prompts.jsonl").exists())
    suite_dirs = []
    for item in requested.split(","):
        item = item.strip()
        if not item:
            continue
        path = Path(item)
        if not path.is_absolute():
            candidate = base / item
            path = candidate if candidate.exists() else root / item
        suite_dirs.append(path.resolve())
    return suite_dirs


def main() -> None:
    parser = argparse.ArgumentParser(description="Run LLM selector diagnostics on RQ1a suites.")
    parser.add_argument("--suites", default="all", help="Comma-separated suite names/paths, or all.")
    parser.add_argument("--conditions", default="shared_context_only,shared_context_plus_field")
    parser.add_argument("--output-prefix", default="rq1a_llm_selector_deepseek")
    parser.add_argument("--dotenv", default=".env")
    parser.add_argument("--base-url-env", default="DEEPSEEK_BASE_URL")
    parser.add_argument("--api-key-env", default="DEEPSEEK_API_KEY")
    parser.add_argument("--model-env", default="DEEPSEEK_MODEL")
    parser.add_argument("--model")
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-tokens", type=int, default=1000)
    parser.add_argument("--concurrency", type=int, default=2)
    parser.add_argument("--max-calls", type=int, help="Optional cap for smoke tests.")
    parser.add_argument("--resume", action="store_true", help="Skip rows already present in the output JSONL.")
    args = parser.parse_args()

    root = repo_root()
    load_dotenv(resolve_dotenv(args.dotenv, root))
    base_url = os.environ.get(args.base_url_env, "").strip()
    api_key = os.environ.get(args.api_key_env, "").strip()
    model = args.model or os.environ.get(args.model_env, "deepseek-chat").strip()
    if not base_url or not api_key:
        raise SystemExit(f"Missing {args.base_url_env} or {args.api_key_env}")

    suite_dirs = discover_suites(root, args.suites)
    for suite_dir in suite_dirs:
        if not (suite_dir / "prompts.jsonl").exists():
            raise SystemExit(f"Suite missing prompts.jsonl: {suite_dir}")
    conditions = [item.strip() for item in args.conditions.split(",") if item.strip()]
    tasks = build_tasks(suite_dirs, conditions)

    output_dir = root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    rows_path = output_dir / f"{args.output_prefix}_rows.jsonl"
    json_path = output_dir / f"{args.output_prefix}.json"
    md_path = output_dir / f"{args.output_prefix}.md"

    existing_rows = read_jsonl(rows_path) if args.resume else []
    done_keys = {
        (row.get("task_hash"), row.get("model"))
        for row in existing_rows
        if row.get("api_ok")
    }
    pending = [task for task in tasks if (task["task_hash"], model) not in done_keys]
    if args.max_calls is not None:
        pending = pending[: args.max_calls]

    print(
        json.dumps(
            {
                "suites": [str(path) for path in suite_dirs],
                "conditions": conditions,
                "model": model,
                "existing_rows": len(existing_rows),
                "pending_calls": len(pending),
                "output_rows": str(rows_path),
            },
            indent=2,
        )
    )

    new_rows: list[dict[str, Any]] = []
    if pending:
        with rows_path.open("a", encoding="utf-8") as handle:
            with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.concurrency)) as executor:
                futures = [
                    executor.submit(
                        run_one,
                        task,
                        base_url=base_url,
                        api_key=api_key,
                        model=model,
                        timeout=args.timeout,
                        retries=args.retries,
                        temperature=args.temperature,
                        max_tokens=args.max_tokens,
                    )
                    for task in pending
                ]
                for index, future in enumerate(concurrent.futures.as_completed(futures), start=1):
                    row = future.result()
                    handle.write(json.dumps(row, ensure_ascii=False) + "\n")
                    handle.flush()
                    new_rows.append(row)
                    if index % 10 == 0 or index == len(futures):
                        print(f"completed {index}/{len(futures)}")

    all_rows = existing_rows + new_rows
    summaries = summarize(all_rows)
    json_path.write_text(
        json.dumps(
            {
                "metadata": {
                    "prompt_template_version": PROMPT_TEMPLATE_VERSION,
                    "model": model,
                    "suites": [str(path) for path in suite_dirs],
                    "conditions": conditions,
                    "row_count": len(all_rows),
                },
                "summaries": summaries,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    md_path.write_text(render_markdown(all_rows, summaries), encoding="utf-8")
    print(f"Wrote {md_path}")
    print(f"Wrote {json_path}")
    print(f"Wrote {rows_path}")


if __name__ == "__main__":
    main()
