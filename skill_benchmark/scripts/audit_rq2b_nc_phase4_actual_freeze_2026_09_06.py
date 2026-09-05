#!/usr/bin/env python3
"""Independent mechanical audit of the current Phase-4 K=6 audit input.

This is deliberately outcome-blind: it inspects only frozen packet structure,
allocation metadata, and manifest hashes.  It does not resolve joins or score
anything, and it never reads historical V6 result files as evidence.
"""
from __future__ import annotations

import hashlib, json, re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
M = ROOT / "rq2b_naturalistic_confusability/manifests/RQ2b-NC-master-phase4-audit-input-2026-09-06_v2"
OUT = ROOT / "rq2b_naturalistic_confusability/manifests/rq2b_nc_master_phase4_actual_freeze_audit_2026-09-06_v2"
FORBIDDEN_KEYS = {"target", "label", "local_label", "acceptable_set", "historical_gold", "retrieval", "reranking", "provider_output", "metric"}

def read(fn): return [json.loads(x) for x in (M / fn).read_text().splitlines() if x.strip()]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def keys_deep(x):
    out=[]
    if isinstance(x, dict):
        out.extend(x.keys())
        for v in x.values(): out.extend(keys_deep(v))
    elif isinstance(x, list):
        for v in x: out.extend(keys_deep(v))
    return out

summary = json.loads((M / "summary.json").read_text())
main, tails, ledger, join, visible = (read(x) for x in ["main_blind_review_packets.jsonl", "tail_blind_review_packets.jsonl", "prompt_k6_allocation_ledger.jsonl", "opaque_token_join.jsonl", "source_visible_review_pairs.jsonl"])
checks = {}
checks["summary_status"] = summary.get("status") == "PASS_PHASE4_K6_OUTCOME_BLIND_AUDIT_INPUT_MATERIALISED_PENDING_BLIND_REVIEWS"
checks["main_528"] = len(main) == 528 and len(ledger) == 528
checks["main_each_k6"] = all(len(x.get("candidates", [])) == 6 and x.get("packet_kind") == "K6_MAIN" for x in main)
checks["main_pairs_3168"] = sum(len(x.get("candidates", [])) for x in main) == 3168
checks["tails_1056"] = len(tails) == 1056 and all(len(x.get("candidates", [])) == 1 and x.get("packet_kind") == "TAIL_CHALLENGE" for x in tails)
by_prompt = defaultdict(list)
for x in tails: by_prompt[x.get("prompt_sha256")].append(x)
checks["tail_max_two_per_group"] = bool(by_prompt) and max(map(len, by_prompt.values())) <= 2 and min(map(len, by_prompt.values())) == 2
checks["ledger_k6_and_two_tails"] = all(x.get("main_pool_exact_k") == 6 and len(x.get("main_allocation", [])) == 6 and len(x.get("tail_allocation", [])) <= 2 for x in ledger)
checks["ledger_main_formula"] = sum(len(x.get("main_allocation", [])) for x in ledger) == 3168
checks["join_4224"] = len(join) == 4224 and len(visible) == 4224
checks["join_packet_unique"] = len({(x.get("packet_id"), x.get("packet_kind"), x.get("candidate_token")) for x in join}) == len(join)
checks["opaque_tokens"] = all(re.fullmatch(r"C-[0-9A-F]{16}", x.get("candidate_token", "")) for x in join)
checks["blind_packets_no_forbidden_keys"] = not (set(keys_deep(main)) | set(keys_deep(tails))) & FORBIDDEN_KEYS
checks["blind_packets_no_v6_or_result_tokens"] = not any(re.search(r"(?i)(v6[_ -]?(result|token)|acceptable.?set[_ -]?(result|label)|result[_ -]?token)", json.dumps({k:v for k,v in x.items() if k != "review_instruction"})) for x in main + tails)
checks["visible_not_blind"] = len(visible) == 4224 and all("canonical_source_sha256" in x and "target" not in x and "label" not in x for x in visible)
checks["candidate_source_sha_not_in_blind"] = all("canonical_source_sha256" not in keys_deep(x) for x in main + tails)

# Every file named by the summary must exist and hash exactly as recorded.
hash_ok = True; missing=[]; mismatched=[]
for section in (summary.get("bound_inputs", {}), summary.get("outputs", {})):
    for name, expected in section.items():
        p = (ROOT.parent / name) if name.startswith("skill_benchmark/") else (M / name)
        if not p.exists(): missing.append(name); hash_ok=False
        elif sha(p) != expected: mismatched.append(name); hash_ok=False
checks["summary_hash_manifest_complete"] = hash_ok

result = {"status": "PASS" if all(checks.values()) else "BLOCKED", "audit_scope": "actual Phase-4 K=6 frozen audit input v2; mechanical only; no Phase-5", "input": str(M), "checks": checks, "counts": {"main_packets":len(main), "main_pairs":sum(map(lambda x: len(x.get("candidates",[])), main)), "tail_packets":len(tails), "tail_groups":len(by_prompt), "join_rows":len(join), "visible_rows":len(visible)}, "hash_manifest": {"missing":missing,"mismatched":mismatched}, "limitations": ["This does not perform blind semantic review, acceptable-set adjudication, or any retrieval experiment.", "The allocation ledger is source-visible by design; only blind packet leakage was tested."]}
OUT.mkdir(parents=True, exist_ok=False)
(OUT / "report.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
(OUT / "report.md").write_text("# Independent Phase-4 actual-freeze mechanical audit\n\n" + json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if result["status"] == "PASS" else 1)
