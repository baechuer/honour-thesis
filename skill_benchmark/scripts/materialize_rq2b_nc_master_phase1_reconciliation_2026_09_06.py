#!/usr/bin/env python3
"""Materialise the RQ2b-NC Phase-1 reconciliation (append-only).

This controller is deliberately a ledger builder: it consumes canonical JSON/JSONL
artifacts, performs no retrieval or embedding, and refuses to replace an existing
output directory.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NC = ROOT / "skill_benchmark/rq2b_naturalistic_confusability"
M = NC / "manifests"
DEFAULTS = {
 "sop": NC/"review/RQ2B_NC_MASTER_PRE_EXPERIMENT_SOP_2026-09-05.md",
 "phase0": M/"rq2b_nc_master_phase0_reconciliation_2026-09-06_v1",
 "phase1": M/"rq2b_nc_master_phase1_v4_b071_replay_2026-09-06_v1",
 "temporal": M/"rq2b_nc_master_phase1_temporal_handoff_validation_2026-09-06_v1/report.json",
 "b052": M/"rq2b_nc_master_phase1_b052_coordinator_staging_2026-09-06_v1",
 "b052_validation": M/"rq2b_nc_master_phase1_b052_staging_validation_2026-09-06_v2/report.json",
}
B071_SPEC = NC / "review/source_native_local_bge_continuation_b071_2026-09-05/batch_071_full_source_review_packets/reconciliation/prompt_authoring/cue_remediation/partial_remediation_composite_closure/B071_PHASE1_V4_TERMINAL_SPEC.json"

def sha(p: Path) -> str:
    h=hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()
def jsonish(p: Path):
    try: return json.loads(p.read_text())
    except (ValueError, UnicodeDecodeError): return None
def files_under(x: Path):
    if x.is_file(): return [x]
    return sorted(p for p in x.rglob("*") if p.is_file() and p.suffix in {".json",".jsonl",".md"})
def write(path, obj): path.write_text(json.dumps(obj, indent=2, sort_keys=True)+"\n")
def read_jsonl(path): return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
def write_jsonl(path, rows): path.write_text("".join(json.dumps(row, sort_keys=True)+"\n" for row in rows))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output-dir", required=True, type=Path)
    ap.add_argument("--b071-terminal-spec", type=Path, default=B071_SPEC)
    a=ap.parse_args()
    out=a.output_dir.resolve()
    if out.exists() and any(out.iterdir()): raise SystemExit(f"refusing to overwrite non-empty output: {out}")
    out.mkdir(parents=True, exist_ok=False)
    inputs=[]
    for name,p in DEFAULTS.items():
        fs=files_under(p)
        if not fs: raise SystemExit(f"missing canonical input {name}: {p}")
        inputs += [(name,str(f.relative_to(ROOT)),sha(f)) for f in fs]
    b071_spec = a.b071_terminal_spec.resolve()
    fs=files_under(b071_spec)
    if not fs: raise SystemExit("B071 terminal spec is missing or empty")
    inputs += [("b071",str(f.relative_to(ROOT)),sha(f)) for f in fs]
    # Bind B013/B014/B015 as validated terminal historical records.
    temporal=jsonish(DEFAULTS["temporal"])
    batches=(temporal or {}).get("batches",{})
    if any(batches.get(f"B{i:03d}",{}).get("status") != "PASS" for i in (13,14,15)):
        raise SystemExit("temporal handoff validation did not PASS for B013/B014/B015")
    terminal={f"B{i:03d}": {"status":"PASS", "terminal_record":"validated_terminal_historical_record",
                         "validation": batches[f"B{i:03d}"]} for i in (13,14,15)}
    phase0=jsonish(DEFAULTS["phase0"] / "summary.json") or {}
    phase1=jsonish(DEFAULTS["phase1"] / "summary.json") or {}
    b052_summary=jsonish(DEFAULTS["b052"] / "adapter/reconciliation/final_prompt_dispositions/summary.json")
    if not b052_summary or b052_summary.get("status","") != "PASS_SOURCE_NATIVE_B052_MASTER_FRESH_COORDINATOR_TARGET_BLIND_ADEQUACY_FINALISED_NO_FINAL_LIBRARY_ADMISSION":
        raise SystemExit("B052 fresh staging closure is not the required PASS status")
    b052_counts=b052_summary.get("counts",{}).get("family_dispositions",{})
    if b052_counts.get("ELIGIBLE_FOR_WHOLE_LIBRARY_ACCEPTABLE_SET_AUDIT") != 3 or b052_counts.get("RETAIN_AS_UNADMITTED_REVIEW_RECORD") != 2:
        raise SystemExit("B052 fresh closure must be exactly 3 eligible and 2 retained")
    b052_validation=jsonish(DEFAULTS["b052_validation"])
    if not b052_validation or b052_validation.get("status") != "PASS":
        raise SystemExit("B052 staging re-audit is not PASS")
    # The structural equation is fixed by the Master SOP; B052's fresh closure supersedes 301.
    d=jsonish(b071_spec) or {}
    if d.get("batch") != "B071" or d.get("terminal_kind") != "partial_remediation_composite_closure": raise SystemExit("invalid B071 terminal spec")
    if int(d.get("expected_terminal_families",0)) != 6 or int(d.get("expected_passed_prompts_in_eligible_families",0)) != 9: raise SystemExit("B071 terminal spec count gate failed")
    b071_count=int(d["expected_eligible_families"])
    parts={"frozen":54,"phase0":167,"historical_phase1_v3_terminal":61,
           "b052_fresh_eligible_delta":-2,"b066_b070":19,"b071_eligible_families":b071_count}
    total=sum(parts.values())
    structural={"equation": "54 + 167 + (61 - 2) + 19 + B071", "parts":parts,
                "structural_count":total, "reject_final_library_count":301,
                "b052_fresh_closure_supersedes_historical_count":True}
    if phase1.get("counts", {}).get("structural_progress_count") != 304 or total != 302:
        raise SystemExit("Phase-1 inheritance or B052/B071 correction count drift")
    # Exact source-union audit: retain hashes from both phase0 ledgers and compare when present.
    unions=[]
    current = DEFAULTS["phase0"] / "phase0_source_native_inspection_union.jsonl"
    old = NC / "review/rq2b_nc_phase0_state_reconciliation_2026-09-05_v2/phase0_source_native_inspection_union.jsonl"
    for f in (old, current):
        if f.exists(): unions.append({"path":str(f.relative_to(ROOT)),"sha256":sha(f),"bytes":f.stat().st_size})
    union_ok = len(unions)==2 and unions[0]["sha256"] == unions[1]["sha256"]
    replay_state=DEFAULTS["phase1"] / "post_phase1_terminal_local_state.jsonl"
    if not replay_state.exists(): raise SystemExit("missing B066-B071 replay terminal state")
    family_rows=[]
    for batch, rec in terminal.items():
        family_gate = NC / f"review/source_native_dense_lexical_union_b{batch[1:]}_2026-09-04/batch_{batch[1:]}_full_source_review_packets/reconciliation/prompt_authoring/target_blind_adequacy_packets/reconciliation/final_prompt_dispositions/family_gate_dispositions.jsonl"
        for row in read_jsonl(family_gate):
            family_rows.append({"batch":batch,"family_token":row["family_token"],"local_family_disposition":row["family_disposition"],"origin":"validated_temporal_handoff"})
    b052_gate=DEFAULTS["b052"] / "adapter/reconciliation/final_prompt_dispositions/family_gate_dispositions.jsonl"
    for row in read_jsonl(b052_gate):
        family_rows.append({"batch":"B052","family_token":row["family_token"],"local_family_disposition":row["family_disposition"],"origin":"fresh_B052_target_blind_closure"})
    replay_rows=read_jsonl(replay_state)
    for row in replay_rows:
        family_rows.append({"batch":row["batch"],"family_token":row["family_token"],"local_family_disposition":row["terminal_local_family_disposition"],"origin":"Phase1_v4_B071_binding_replay"})
    write_jsonl(out/"family_state_ledger.jsonl", family_rows)

    source_rows=[]
    for row in replay_rows:
        if row.get("locally_eligible_all_three"):
            hs=row.get("joined_canonical_source_sha256")
            if not isinstance(hs,list) or len(set(hs)) != 3: raise SystemExit("eligible replay family lacks exactly three unique source hashes")
            for h in hs: source_rows.append({"batch":row["batch"],"family_token":row["family_token"],"canonical_source_sha256":h,"origin":"post_phase1_terminal_local_state"})
    # Historical terminal families: provenance preflight rows are the canonical source union.
    b052_eligible={row["family_token"] for row in read_jsonl(b052_gate) if row.get("family_disposition")=="ELIGIBLE_FOR_WHOLE_LIBRARY_ACCEPTABLE_SET_AUDIT"}
    for batch in ("B013","B014","B015","B052"):
        parent = (NC / f"review/source_native_dense_lexical_union_b{batch[1:]}_2026-09-04/batch_{batch[1:]}_full_source_review_packets" if batch != "B052" else NC / "review/source_native_marketing_advertising_seo_social_community_web_analytics_journalism_publishing_localisation_communications_b052_2026-09-05/batch_052_full_source_review_packets")
        provenance = parent / "reconciliation/pass_provenance_preflight/pass_family_source_provenance_preflight.jsonl"
        if not provenance.is_file(): raise SystemExit(f"missing provenance ledger: {provenance}")
        for row in read_jsonl(provenance):
            include = row.get("provenance_preflight_status", "").startswith("PASS")
            if batch == "B052": include = include and row.get("family_token") in b052_eligible
            if include:
                source_rows.append({"batch":batch,"family_token":row["family_token"],"canonical_source_sha256":row["canonical_source_sha256"],"origin":str(provenance.relative_to(ROOT))})
    seen={};
    for r in source_rows: seen.setdefault((r["batch"],r["family_token"]),set()).add(r["canonical_source_sha256"])
    if any(len(v)!=3 for v in seen.values()) or len({r["canonical_source_sha256"] for r in source_rows}) != len(source_rows): raise SystemExit("source union overlap or non-triad detected")
    if len(seen) != 49 or len(source_rows) != 147: raise SystemExit("unexpected terminal source-union cardinality")
    write_jsonl(out/"source_union.jsonl", source_rows)
    write(out/"source_union_summary.json", {"phase0_old_new_union_bytes_equal":union_ok,"terminal_eligible_families":len(seen),"source_rows":len(source_rows),"source_hashes_unique":len({r["canonical_source_sha256"] for r in source_rows})})
    write(out/"discrepancy_ledger.json", {"corrections":[{"from":301,"to":299,"reason":"fresh B052 closure -2","applies_unless_b071":True}],"b071_supplied":bool(a.b071_terminal_spec)})
    write(out/"input_hashes.json", {"inputs":[{"role":n,"path":p,"sha256":s} for n,p,s in inputs]})
    write(out/"reconciliation.json", {"status":"materialized","structural":structural,"phase0_summary":phase0,"phase1_summary":phase1})
    write(out/"summary.json", {"status":"PASS_RQ2B_NC_MASTER_PHASE1_RECONCILIATION_NO_EXPERIMENT","structural_count":total,"b071_included":True,"gates":{"phase0_old_new_union_bytes_equal":union_ok,"B013_B014_B015_validated_terminal":True,"B052_fresh_closure_reaudited":True,"terminal_source_union_49_by_3":True,"no_retrieval_or_embedding":True}})

if __name__ == "__main__": main()
