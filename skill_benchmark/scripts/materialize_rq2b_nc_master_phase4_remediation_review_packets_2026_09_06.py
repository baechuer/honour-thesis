#!/usr/bin/env python3
"""Stage fresh target-blind adequacy/cue review for the five Phase-4 drafts.

This controller only materialises packets. It never adjudicates prompts or joins
review decisions to the hidden target.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "skill_benchmark/rq2b_naturalistic_confusability"
AUTHOR = BASE / "manifests/rq2b_nc_master_phase4_bounded_prompt_author_return_2026-09-06_v1"
PACKET = BASE / "manifests/rq2b_nc_master_phase4_missing_nc_prompt_authoring_packets_2026-09-06_v1"
OUT = BASE / "manifests/rq2b_nc_master_phase4_remediation_review_packets_2026-09-06_v1"
SOP = BASE / "review/RQ2B_NC_MASTER_PRE_EXPERIMENT_SOP_2026-09-05.md"

def digest(p: Path) -> str: return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p: Path) -> list[dict[str, Any]]:
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
def dump(p: Path, xs: list[dict[str, Any]]) -> None:
    p.write_text("".join(json.dumps(x, ensure_ascii=False, sort_keys=True) + "\n" for x in xs), encoding="utf-8")

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-dir", type=Path, default=OUT)
    ap.add_argument("--validate-only", action="store_true")
    a = ap.parse_args(); out = a.output_dir.resolve()
    required = [SOP, PACKET / "author_packet.jsonl", AUTHOR / "author_return.jsonl", AUTHOR / "manifest.json"]
    missing = [str(p) for p in required if not p.is_file()]
    if missing:
        print(json.dumps({"status":"BLOCKED_MISSING_AUTHOR_RETURN_OR_BINDING", "missing":missing}, indent=2)); return 2
    if out.exists() and not a.validate_only: raise SystemExit(f"Refusing to overwrite: {out}")
    authored = rows(AUTHOR / "author_return.jsonl")
    packets = rows(PACKET / "author_packet.jsonl")
    expected = {str(x["author_packet_id"]) for x in packets}
    actual = {str(x.get("packet_id")) for x in authored}
    if len(packets) != 5 or len(authored) != 5 or actual != expected:
        print(json.dumps({"status":"BLOCKED_AUTHOR_RETURN_ID_SET_OR_COUNT_DRIFT", "expected":sorted(expected), "actual":sorted(actual)}, indent=2)); return 2
    by_id = {str(x["author_packet_id"]): x for x in packets}
    manifest = json.loads((AUTHOR / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("author_return_jsonl_sha256") != digest(AUTHOR / "author_return.jsonl"):
        print(json.dumps({"status":"BLOCKED_AUTHOR_RETURN_FILE_HASH_DRIFT"}, indent=2)); return 2
    if digest(PACKET / "author_packet.jsonl") != manifest.get("authoring_packet_jsonl_sha256"):
        print(json.dumps({"status":"BLOCKED_AUTHOR_PACKET_FILE_HASH_DRIFT"}, indent=2)); return 2
    if any(len(str(x.get("author_packet_sha256", ""))) != 64 for x in authored):
        print(json.dumps({"status":"BLOCKED_AUTHOR_RETURN_HASH_MISSING"}, indent=2)); return 2
    # The author packet is the sole source of originals; keep target and mapping out.
    a_packets=[]; b_packets=[]; cue=[]; joins=[]
    for i, draft in enumerate(sorted(authored, key=lambda x: str(x["packet_id"])), 1):
        pid=str(draft["packet_id"]); src=by_id[pid]; members=src.get("members", [])
        if len(members) != 3 or any("complete_original_skill" not in m for m in members):
            print(json.dumps({"status":"BLOCKED_AUTHOR_PACKET_MEMBER_DRIFT", "packet_id":pid}, indent=2)); return 2
        opaque=[]
        for n,m in enumerate(members,1):
            opaque.append({"candidate_token":f"C-{i:02d}-{n}", "complete_original_skill":m["complete_original_skill"]})
        for reviewer, ordered in (("A", opaque), ("B", list(reversed(opaque)))):
            packet={"packet_id":pid,"reviewer":reviewer,
              "review_boundary":"Assess prompt-to-source adequacy and identity cues only. Do not infer intended target, author mapping, source path/hash, rank, prior disposition, retrieval, outcomes, or acceptable-set membership.",
              "prompt":draft["prompt"],"candidates":ordered,
              "return_schema":{"packet_id":pid,"candidate_assessments":[{"candidate_token":"C-*","adequacy":"FULLY_ACCEPTABLE | PARTIALLY_ADEQUATE | INADEQUATE | UNCLEAR","rationale":"","source_anchors":[]}],"cue_decision":"AVOIDABLE_IDENTITY_CUE | DECLARED_NECESSARY_CUE_STRATUM | NOT_A_CUE | UNCLEAR","cue_anchors":[]}}
            (a_packets if reviewer=="A" else b_packets).append(packet)
        # Mechanical cue inventory; this is a flag, never a semantic decision.
        text=draft["prompt"].lower(); signals=[]
        for m in members:
            raw=(m.get("complete_original_skill") or "")
            head=raw.split("\n\n",1)[0].lower()
            for line in head.splitlines():
                if line.startswith("name:") and line[5:].strip() in text: signals.append(line[5:].strip())
        cue.append({"packet_id":pid,"mechanical_identity_cue_signals":sorted(set(signals)),"review_required":True})
        joins.append({"packet_id":pid,"target_join":"WITHHELD_UNTIL_FINALIZER","target_member_token":src.get("target_member_token"),"target_source_sha256":src.get("target_source_sha256")})
    summary={"status":"PENDING_TWO_INDEPENDENT_TARGET_BLIND_REVIEW","counts":{"author_returns":5,"reviewer_a_packets":5,"reviewer_b_packets":5},"claim_boundary":"Packet staging only; no adequacy, cue, target, admission, selector, retrieval, or result decision.","bound_inputs":{str(p.relative_to(ROOT)):digest(p) for p in required}}
    if a.validate_only: print(json.dumps(summary, indent=2, sort_keys=True)); return 0
    out.mkdir(parents=True)
    for name,data in (("reviewer_a_packet.jsonl",a_packets),("reviewer_b_packet.jsonl",b_packets),("cue_mechanical_screen.jsonl",cue),("internal_target_join.jsonl",joins)):
        dump(out/name,data); summary.setdefault("outputs",{})[name]=digest(out/name)
    (out/"summary.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"output_dir":str(out),**summary}, indent=2, sort_keys=True)); return 0
if __name__ == "__main__": raise SystemExit(main())
