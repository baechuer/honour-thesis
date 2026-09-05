#!/usr/bin/env python3
"""Apply five literal-cue wording repairs to frozen Round 38 C2 drafts only."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


REPAIRS = {
    (
        "R38-C0A-AGENT_FRAMEWORKS-01-01",
        "r38m1-braintrustdata-braintrust-sdk-agents-skills-instrumentation",
        "direct",
    ): (
        "I am changing observability hooks in a TypeScript SDK. Help me choose among the shared event layer, vendor-specific adapter, automatic hook, and explicit wrapper, then add focused end-to-end tests while preserving async context, stream and promise behavior, error propagation, safe handling of untrusted data, and repeatable setup and teardown."
    ),
    (
        "R38-C0A-AGENT_FRAMEWORKS-01-01",
        "r38m1-pydantic-skills-plugins-logfire-skills-logfire-instrumentation",
        "direct",
    ): (
        "Set up broad observability for my Python FastAPI service. Configure telemetry once before instrumenting the web app, outbound requests, persistence layer, and model calls; replace unsearchable log strings with structured events, add service and environment metadata plus host metrics, and verify the setup with a normal smoke request without exposing a browser credential."
    ),
    (
        "R38-C0A-AGENT_FRAMEWORKS-02-01",
        "r38m1-Arize-ai-phoenix-agents-skills-phoenix-cli",
        "paraphrase",
    ): (
        "Help me investigate why my language-model application is misbehaving from the terminal: review representative execution records, annotate failure causes, and organize the findings into recurring error categories so I can choose follow-up tests."
    ),
    (
        "R38-C0A-AGENT_FRAMEWORKS-02-01",
        "r38m1-pydantic-skills-plugins-logfire-skills-logfire-query",
        "direct",
    ): (
        "I want to analyze application telemetry with queries rather than open a dashboard. Write a bounded SQL investigation for recent errors, slow operations, or service-level metrics, using the available trace, span, log, and metric fields, and return a small result set that can support diagnosis."
    ),
    (
        "R38-C0A-AUTOMATION_INTEGRATION-01",
        "r38m1-browser-use-browser-use-skills-remote-browser",
        "direct",
    ): (
        "Run a headless browser in the isolated environment, open the local development site, complete the contact fields with the supplied sample details, send the request, and capture the resulting confirmation screen."
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repair-log", type=Path, required=True)
    args = parser.parse_args()

    rows = [json.loads(line) for line in args.input.read_text(encoding="utf-8").splitlines() if line.strip()]
    repaired: list[dict[str, str]] = []
    for row in rows:
        key = (str(row.get("proposal_id")), str(row.get("intended_candidate_skill_id")), str(row.get("variant")))
        replacement = REPAIRS.get(key)
        if replacement is None:
            continue
        original = str(row.get("prompt", ""))
        if not original:
            raise SystemExit(f"blank_repair_target:{key}")
        row["prompt"] = replacement
        repaired.append({"proposal_id": key[0], "intended_candidate_skill_id": key[1], "variant": key[2], "old_prompt": original, "new_prompt": replacement})
    if len(repaired) != len(REPAIRS):
        found = {(item["proposal_id"], item["intended_candidate_skill_id"], item["variant"]) for item in repaired}
        raise SystemExit(f"repair_target_count:{len(repaired)}:missing={sorted(set(REPAIRS) - found)}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    args.repair_log.write_text(json.dumps({
        "status": "C3_ROUND38_LITERAL_CUE_WORDING_REPAIRED_PENDING_REAUDIT_NOT_A_LABEL_OR_RESULT",
        "input": str(args.input),
        "input_sha256": sha256(args.input),
        "output": str(args.output),
        "output_sha256": sha256(args.output),
        "repair_count": len(repaired),
        "repairs": repaired,
        "invariant": "Only the five declared prompt strings changed. Candidate membership, intended construction target, variant, status, source evidence, prompt coverage, and all later C3/C4/C5/C6 facts remain uncreated or unchanged.",
    }, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "repair_written", "repair_count": len(repaired)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
