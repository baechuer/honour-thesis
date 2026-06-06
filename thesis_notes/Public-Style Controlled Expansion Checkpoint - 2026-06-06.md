# Public-Style Controlled Expansion Checkpoint

Date: 2026-06-06

Purpose: expand the benchmark after the Step 4b cluster audit, while directly addressing the co-adaptation risk that earlier controlled skills were too neatly aligned with the proposed representation fields.

## What Was Added

New evaluated family:

- `public_style_controlled`

New generated artifacts:

- Generator: `skill_benchmark/scripts/generate_public_style_controlled_expansion.py`
- Skills: `skill_benchmark/skills/public_style_controlled/`
- Prompts: `skill_benchmark/prompts/public_style_controlled_confusability.json`
- Placeholder fixtures/resources: `skill_benchmark/fixtures/public_style_controlled/`

Scale after expansion:

- Skills: 2433 total.
- Controlled/evaluated skills: 169.
- Controlled prompts: 201.
- Public-gold prompts remain separate: 82.
- Combined evaluated prompt pool, if controlled and public-gold are reported together: 283.

The new family contains:

- 8 public-style controlled clusters.
- 32 public-style controlled skills.
- 64 prompts.
- 32 `L2_natural` prompts.
- 32 `L3_high_information` prompts.
- 55 provider-implicit prompts.
- 9 provider-explicit prompts.

## New Clusters

| Cluster | Prompts | Purpose |
|---|---:|---|
| `psc_pdf_document_work` | 8 | PDF extraction, OCR, evidence QA, and redaction under shared PDF vocabulary. |
| `psc_browser_quality` | 8 | DevTools diagnosis, Playwright regression, screenshot review, and accessibility audit. |
| `psc_huggingface_workflow` | 8 | Dataset inspection, local model fit, embedding training, and Spaces deployment. |
| `psc_github_maintenance` | 8 | CI diagnosis, PR thread resolution, repository guardrails, and release communication. |
| `psc_security_appsec` | 8 | Threat modeling, code vulnerability review, dependency risk, and privacy telemetry review. |
| `psc_research_reading` | 8 | Method mapping, citation support audit, related-work synthesis, and source-field extraction. |
| `psc_skill_representation` | 8 | Messy skill field extraction, public skill atomization, routing policy, and retrieval adjudication. |
| `psc_data_analysis_intent` | 8 | Data trust audit, anomaly watchlist, decision ranking, and executive metric narrative. |

## Why This Expansion Matters

This expansion is not just more cases. It adds a new stratum:

> public-style controlled skills: gold labels are controlled and defensible, but the raw skill artifacts are written more like public prose skills than neat schema-authored benchmark skills.

This helps test whether structured representations can recover useful information from messier skill artifacts instead of only succeeding on skills that were directly authored around the proposed field taxonomy.

## Validation Results

Validation after regeneration and representation export:

| Gate | Result |
|---|---|
| Step 1 integrity | PASS: 201 prompts and 2433 skills resolve; 0 duplicate prompt IDs; 0 missing references; 0 malformed frontmatter entries. |
| Representation coverage | Public-style controlled coverage is 32/32 for use-when, not-for, workflow, and output fields after extraction. |
| Step 2 procedural distinctness | PASS: 201/201 prompts; 641/641 gold/alternative pairs pass procedural distinctness. |
| Step 2 prompt-specific alignment | PASS with audit targets: 182/201 prompts pass; 618/641 gold/alternative pairs pass; gold ranks first among listed candidates for 183/201 prompts. Public-style controlled passes 60/64. |
| Step 3 semantic confusability | PASS overall: 180/201 prompts, or 89.6%, have at least two plausible alternatives under MiniLM. |
| Step 4 leakage | PASS: 0 critical exact-name leaks and 0 high-risk leaks. |

Public-style controlled Step 3:

- 64/64 prompts pass semantic confusability.
- All 8 public-style clusters pass 8/8.
- L2 natural prompts: 32/32 pass.
- L3 high-information prompts: 32/32 pass.

Remaining Step 3 weakness is now mostly in older clusters, especially `metrics_observability` and `observability_reliability`, not in the new expansion.

Public-style controlled Step 2 alignment:

- 60/64 prompts pass prompt-specific requirement alignment.
- The four weak public-style alignment prompts are useful audit targets rather than automatic failures:
  - `psc_pdf_document_work_p03_1_psc_pdf_evidence_qa`
  - `psc_browser_quality_p02_1_psc_playwright_regression_suite`
  - `psc_security_appsec_p01_1_psc_feature_threat_modeler`
  - `psc_skill_representation_p03_2_psc_skill_routing_budget_planner`

## Important Caveat

The first public-style attempt failed integrity because generated frontmatter had leading spaces, and Step 3 initially dropped because the public-style descriptions were too orthogonal. The final generator fixes both:

- YAML frontmatter now starts at column 0.
- Each public-style cluster includes a natural shared domain context in the description. This mirrors real public libraries where related skills often share collection/domain vocabulary.

This shared context should be described carefully. It is a valid way to create semantic neighbour pressure, but it should not be overused as proof that all public skills are naturally confusable.

## Next Methodology Implications

The expanded benchmark should now be reported in at least three strata:

- original controlled structured skills;
- public-style controlled skills;
- public-gold external-validity prompts.

This lets the thesis test:

- whether fields help when skills are clean and schema-like;
- whether extracted fields help when skills are public-style but controlled;
- whether the same methods survive messy real public skills.

Recommended next steps:

1. Run Qwen/SkillRouter on the new controlled benchmark only after local sanity checks.
2. Report public-style controlled results separately before combining them with the older controlled prompts.
3. Do a focused repair or caveat note for older weak Step 3 families: `metrics_observability`, `observability_reliability`, `browser_web_automation`, and `deployment_browser_qa`.
4. Manually audit the 19 weak Step 2 requirement-alignment prompts before final headline result tables.

## First Local Selector Results On The Expanded Benchmark

Local sanity checks were rerun on the active 201-prompt / 2433-skill benchmark.

| Method | Top-1 | Top-5 | MRR | Non-main top-1 |
|---|---:|---:|---:|---:|
| M1 BM25 flat | 61.7% | 88.1% | 0.727 | 9.0% |
| M1 TF-IDF flat | 55.2% | 86.1% | 0.689 | 15.4% |
| M3 TF-IDF schema | 65.2% | 94.0% | 0.778 | 8.0% |
| M6 BM25 schema rerank | 65.7% | 93.5% | 0.781 | 3.0% |
| M6 TF-IDF schema rerank | 65.7% | 91.5% | 0.773 | 3.5% |

M6-v1 local field-aware reranker, top-100 candidate budget:

| First stage | Best field set | Top-1 | Top-5 | MRR | Candidate R@100 |
|---|---|---:|---:|---:|---:|
| TF-IDF flat | core / core+boundary | 72.6% | 94.0-94.5% | 0.822-0.824 | 96.0% |
| BM25 flat | core+boundary | 72.1% | 95.0% | 0.825 | 97.0% |

Interpretation: the expansion made the benchmark harder, but not broken. Flat metadata is now clearly weaker, schema/rerank methods improve the ordering, and the best local field-aware settings show that output/workflow/core procedural fields help more than simply concatenating every available field.
