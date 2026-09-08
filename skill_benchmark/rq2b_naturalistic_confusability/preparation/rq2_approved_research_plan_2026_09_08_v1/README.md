# Approved RQ2 research plan v1

Researcher decision: finalise the updated plan as the new RQ2 plan; start experiment preparation; list approximately 20,000 additional background skills as future work.

`plan_freeze.json` binds the complete approved document, B36/C6 condition manifests, V7 sources/prompts/exclusions/amendment and master SOP. It fixes P1–P5 and the written statistical/interpretation rules before new selector outcomes. This is a research-plan freeze, not the Phase-8 runtime root or provider authorisation.

Canonical document: `thesis_notes/current/RQ2 Approved Research Plan - 2026-09-08.zh-CN.md`.

Plan SHA-256: `b54d3d8c6816b2bb5f75b2b946448063fcc800c1f9927e27babd767e3468d4d8`.

```sh
python3 -B skill_benchmark/scripts/freeze_rq2_approved_research_plan.py --verify
python3 -B skill_benchmark/scripts/verify_rq2b_nc_v7_acceptable_set_final_library_freeze.py
python3 -B skill_benchmark/scripts/prepare_rq2b_v7_first_matrix.py --verify
```

Current required scope: 3,798 candidates, 1,077 retained queries, 36 end-to-end configurations and six new fixed-candidate diagnostic configurations. RQ1/RQ2a and historical RQ2b results remain separate and unchanged. New full-library retrieval is not limited to the small audit clusters.

Future scope: source-screened nested background expansion, wiki/graph/tree adaptations and the optional self-designed system. The approximate 20k target is additional background, not an already-admitted count; no candidates were added this turn. Future additions are not assumed negative; enlarged-pool label coverage needs its own prospective contract. Current results cannot establish tens-of-thousands-scale scalability or that graph/pure-LLM methods are inherently unscalable.

Local Phase-7 preparation has started in `../v7_phase7_i1_i2_2026_09_08_v1/`. Formal inference remains pending representation QA, dependency/exposure and exact runtime/model/length/cost bindings under the master SOP. The approved scientific plan itself no longer needs to be treated as an unapproved draft.

Scope of this repository update: this plan/seal, versioned local-preparation manifests/scripts, small tests and current documentation pointers. Cache payloads, model downloads, credentials, snapshots and unrelated original-workspace files remain excluded and untouched.
