# Step 2, Step 3, And Non-Core Caveat Review

Date: 2026-05-28

This note records the latest benchmark-health check after expanding to 2089 skills.

## Short Answer

Step 2 is no longer failing.

- Procedural distinctness: PASS, 85/85 prompts.
- Gold/alternative procedural pair audit: PASS, 251/251 pairs differ on at least two primary axes.
- Prompt-specific requirement alignment: PASS, 85/85 prompts.

Step 3 is passing, but not perfect.

- Semantic confusability: PASS, 75/85 prompts.
- The remaining 10 weak cases are mostly tasks where the prompt is so procedurally explicit that the gold skill becomes semantically obvious.
- This is a calibration caveat, not currently a blocking failure.

The non-core caveat is real and should be reported carefully.

- Non-core semantic top-1: 24/85 prompts.
- Best non-core semantic score beats gold: 33/85 prompts.
- Non-core procedural competitor above gold: 16/85 prompts.
- These cases show useful scale pressure, but they require human adjudication before final claims.

## What Was Fixed

The stricter Step 2 alignment checker was previously too naive about negation. For example, phrases such as "not a calendar plan" or "no existing draft to polish" could still boost the very skill being rejected. This made some prompts look procedurally weak even when the natural-language requirement was clear.

I updated `skill_benchmark/scripts/analyze_requirement_alignment.py` so positive prompt-fit scoring strips local negated spans before scoring. Boundary and `not_for` evidence still use the full prompt text. After this change, Step 2 prompt alignment rose to 85/85.

I also tightened several older prompts so the gold skill is justified by a positive procedural requirement rather than only by rejecting alternatives.

## Current Results

| Check | Result | Interpretation |
|---|---:|---|
| Step 1 integrity | PASS, 85 prompts / 2089 skills | References and frontmatter resolve. |
| Step 2 procedural distinctness | PASS, 85/85 prompts | Gold and listed alternatives are procedurally separable. |
| Step 2 pair audit | PASS, 251/251 pairs | Every gold/alternative pair differs on at least two primary axes. |
| Step 2 prompt alignment | PASS, 85/85 prompts | Each prompt now gives enough positive evidence for the gold label. |
| Step 3 semantic confusability | PASS, 75/85 prompts | Most prompts have plausible semantic neighbours. |
| Step 4 leakage | PASS, 0 critical / 0 high risk | Prompts do not reveal labels directly. |
| Non-core semantic competition | 24/85 top-1 non-core | Scale creates realistic semantic collisions. |
| Non-core procedural competition | 16/85 prompts above gold | Needs adjudication, not automatic invalidation. |

## Remaining Step 3 Weak Cases

The 10 weak semantic-confusability prompts are:

- `api_p5_database_migration_risk`
- `web_p4_data_extraction`
- `web_p5_frontend_debugging`
- `deploy_p2_visual_regression`
- `deploy_p3_accessibility_interaction`
- `obs_p2_latency_anomaly`
- `obs_p4_capacity_risk`
- `obs_p5_root_cause`
- `obs_p6_incident_summary`
- `office_p1_pdf_layout_review`

These are not all bad prompts. Several are high-precision procedural tasks where the gold is naturally clearer than the alternatives. Forcing every one of them to become more semantically ambiguous would risk making gold labels less stable.

Current decision: keep Step 3 as PASS at 75/85, but document that the benchmark contains a mix of high-confusion and high-precision cases.

## Non-Core Caveat Interpretation

A background/public skill beating gold under compressed semantic similarity does not automatically mean the gold is wrong. It can mean one of four things:

- `gold_clear`: the non-core skill shares words but misses the requested procedure.
- `object_confusion`: the non-core skill is the object being searched, edited, installed, evaluated, or packaged, not the meta-operation requested.
- `acceptable_alternative`: the non-core skill is genuinely close enough that strict gold-only scoring is unfair.
- `gold_threat`: the prompt or background library should be revised because the non-core skill is arguably better.

The strongest current caveat is in document and skill-lifecycle prompts. For example, `travel-ops-rewrite-editor` is close to `document-rewriter` when the source is a travel request note, and `public-markitdown` is close to `document-converter` for Markdown conversion. These should be handled through acceptable-alternative labels, not hidden.

## What This Means For The Thesis

The benchmark is valid enough to continue because it now satisfies the core design goal:

- gold labels are procedurally justified
- alternatives are mostly semantically plausible
- scale introduces non-core collisions
- representation-aware methods behave differently from flat and dense baselines

The thesis claim should not be "structured methods always retrieve the uniquely correct skill." A better claim is:

> As skill libraries scale, compressed semantic representations create both near-neighbour confusion and background-skill collisions. Procedural representations and reranking reduce these failures, but final evaluation must account for acceptable alternatives and object-confusion cases.

## Next Actions

1. Update the human adjudication file for the current 33 semantic non-core-over-gold cases.
2. Add any true near-equivalent cases to `skill_benchmark/annotations/acceptable_alternatives.json`.
3. Keep Step 3 weak cases documented unless they become selector failure hotspots.
4. Use strict and acceptable-alternative metrics side by side in final result tables.
