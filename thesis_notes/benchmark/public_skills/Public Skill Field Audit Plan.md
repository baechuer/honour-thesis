# Public Skill Field Audit Plan

Status: started.

This note defines how to analyse public, real-world `SKILL.md` artifacts without drifting away from the thesis. The purpose is not to prove that every public skill is high quality. The purpose is to test whether the information fields used by our structured representation are actually observed or at least extractable from real skill artifacts.

## Research Claim Being Checked

Current thesis claim:

> Skill retrieval at scale depends on what procedural information is preserved in the representation, not only on semantic similarity between the user request and the skill description.

The public-skill audit checks the grounding of the representation fields:

- `observed`: the public skill explicitly exposes the field in frontmatter or headings.
- `extractable`: the public skill contains the field implicitly in the body, but a representation layer must parse or normalize it.
- `proposed`: the public skill usually lacks the field, but the thesis argues it should be added or inferred because it improves retrieval.

This distinction is important. If a field is not commonly explicit in public skills, we should not claim that current public skills already provide it. We can still claim that the representation layer should extract or normalize it if retrieval experiments show that it helps.

## Public Sources To Use

Local public imports already available:

- Anthropic public skills.
- OpenAI public skills.
- Claude office skills.
- SkillRet-preview public skills.
- Hugging Face / scientific-agent public skills.

Online sources to inspect or expand from later:

- Anthropic `skills` GitHub repository.
- Claude custom skills documentation and examples.
- OpenAI `skills` repository.
- SkillRet / related public skill retrieval datasets.
- SkillsBench / public GitHub skill corpus.
- Public skill-quality papers that analyse large `SKILL.md` ecosystems.

Do not mix raw public skills into the controlled core unless they have clear gold labels and atomic routing boundaries. Public skills are mainly for scale realism, distractors, and field-grounding evidence.

## Field Taxonomy

The current audit checks:

| Field | Why It Matters For Retrieval |
|---|---|
| `routing_trigger` | Tells the retriever when the skill should be considered. |
| `input_precondition` | Distinguishes skills that require different artifacts, data, or prior state. |
| `output_artifact` | Distinguishes summary, report, patch, table, plan, conversion, extraction, etc. |
| `workflow_procedure` | Captures procedural behavior beyond topic similarity. |
| `constraints_boundaries` | Captures "do not use when" and scope limitations. |
| `dependencies_tools` | Captures required APIs, tools, binaries, files, credentials, or platforms. |
| `resources_references` | Captures supporting docs, templates, scripts, assets, and linked files. |
| `examples_tests` | Captures examples and verification signals. |
| `safety_side_effects` | Captures permission, privacy, mutation, and risky-action boundaries. |
| `portability_environment` | Captures platform, language, version, and environment assumptions. |
| `hierarchy_links` | Captures references to other skills, subskills, or follow-up resources. |

## Resumable Audit Commands

Smoke test from scratch:

```bash
python3 skill_benchmark/scripts/audit_public_skill_fields.py --limit 20 --force
```

Continue incrementally:

```bash
python3 skill_benchmark/scripts/audit_public_skill_fields.py --limit 30
```

Run the full local public-skill audit:

```bash
python3 skill_benchmark/scripts/audit_public_skill_fields.py
```

Force a full rerun after changing the detector:

```bash
python3 skill_benchmark/scripts/audit_public_skill_fields.py --force
```

Build a human review packet:

```bash
python3 skill_benchmark/scripts/build_public_skill_manual_review_packet.py --sample-size 15
```

Model-assisted semantic extraction:

```bash
python3 skill_benchmark/scripts/model_verify_public_skill_fields.py --limit 460 --concurrency 4
```

Model/heuristic agreement report:

```bash
python3 skill_benchmark/scripts/compare_public_skill_field_audits.py
```

Current output files:

- `skill_benchmark/outputs/public_skill_field_audit.jsonl`
- `skill_benchmark/outputs/public_skill_field_audit_summary.json`
- `skill_benchmark/outputs/public_skill_field_audit.md`
- `skill_benchmark/outputs/public_skill_field_manual_review_packet.md`
- model checkpoint output: `skill_benchmark/outputs/public_skill_field_model_audit.jsonl`
- model/heuristic comparison output: `skill_benchmark/outputs/public_skill_field_agreement_report.md`
- model pilot checkpoint note: `thesis_notes/checkpoints/public_skill_audit/Public Skill Model Verification Checkpoint - 20 Skills.md`
- model full checkpoint note: `thesis_notes/checkpoints/public_skill_audit/Public Skill Model Verification Checkpoint - 460 Skills.md`
- subagent review protocol: `thesis_notes/benchmark/public_skills/Public Skill Subagent Review Protocol.md`
- subagent pilot folder: `skill_benchmark/outputs/subagent_reviews/`
- subagent pilot summary: `skill_benchmark/outputs/subagent_reviews/public_skill_subagent_pilot_summary.md`

## Current Checkpoint

Checkpoint date: 2026-05-29.

Current audit size: 460 public skills.

Subagent calibration:

- Two pilot batches completed.
- 10 public skills reviewed with evidence-grounded labels.
- Summary: `skill_benchmark/outputs/subagent_reviews/public_skill_subagent_pilot_summary.md`.

Model-assisted verification:

- DeepSeek checkpoint completed for all 460 imported public skills.
- Agreement report: `skill_benchmark/outputs/public_skill_field_agreement_report.md`.
- Pilot checkpoint note: `thesis_notes/checkpoints/public_skill_audit/Public Skill Model Verification Checkpoint - 20 Skills.md`.
- Full checkpoint note: `thesis_notes/checkpoints/public_skill_audit/Public Skill Model Verification Checkpoint - 460 Skills.md`.

Initial pattern:

- Strongly present or extractable: routing trigger, input/precondition, output artifact, workflow/procedure, dependencies/tools, resources/references, examples/tests, portability/environment.
- Moderately present: constraints/boundaries and hierarchy links.
- Weakest field so far: safety/side effects.

Full 460-skill heuristic checkpoint:

| Field | Explicit | Explicit or Extractable | Provisional Read |
|---|---:|---:|---|
| `routing_trigger` | 100.0% | 100.0% | observed |
| `input_precondition` | 25.2% | 81.5% | often extractable |
| `output_artifact` | 45.2% | 85.2% | observed/extractable |
| `workflow_procedure` | 71.7% | 84.4% | observed |
| `constraints_boundaries` | 41.3% | 77.6% | partially observed/extractable |
| `dependencies_tools` | 72.8% | 85.0% | observed |
| `resources_references` | 66.7% | 82.0% | observed/extractable |
| `examples_tests` | 63.5% | 93.9% | observed/extractable |
| `safety_side_effects` | 11.3% | 37.0% | proposed or weakly observed |
| `portability_environment` | 72.0% | 85.5% | observed/extractable |
| `hierarchy_links` | 41.0% | 46.5% | partially observed |

Important caveat:

- The audit is heuristic and may overcount fields when keywords appear without a clean procedural role. The manual review packet must be checked before treating prevalence numbers as evidence.
- The current import stores original public `SKILL.md` files, but not necessarily every supporting file from the public repositories. Therefore folder inventory for scripts/references/assets is incomplete until we import full folders for selected repositories.

## Model-Assisted Verification Layer

The heuristic audit is transparent and reproducible, but shallow. It can miss semantic equivalents and can overcount keywords. To deepen the extraction process, add a model-assisted verification layer after the deterministic audit.

Implemented scripts:

- `skill_benchmark/scripts/model_verify_public_skill_fields.py`
- `skill_benchmark/scripts/compare_public_skill_field_audits.py`

Recommended model:

- Default: DeepSeek `deepseek-v4-flash`.
- Rationale: the task is structured extraction with evidence spans, so we want low cost, long-context tolerance, and JSON output more than frontier-level reasoning.
- Use `deepseek-v4-pro` only if the flash model produces unstable JSON or weak evidence-span behavior.

Required `.env` entries:

```bash
DEEPSEEK_API_KEY=...
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-v4-flash
```

Purpose:

- detect semantically equivalent field evidence, such as "prerequisites", "before running", "requires authentication", or "produces a report"
- reduce keyword false positives by asking whether the evidence really supports the field
- produce disagreement cases for targeted human review

Required model output:

```json
{
  "skill": "skill-name",
  "fields": {
    "input_precondition": {
      "status": "explicit | implicit | missing",
      "confidence": 0.0,
      "evidence": ["short quote from SKILL.md"],
      "reason": "one sentence"
    }
  }
}
```

Rules:

- If the model cannot quote evidence from the skill text, it must mark the field as `missing`.
- The model may label a field `implicit` only when the skill text clearly contains the concept under different wording.
- The model must not infer what a good skill should contain.
- The model-assisted audit is a verifier and extractor, not the benchmark judge.

Agreement analysis:

| Case | Interpretation | Action |
|---|---|---|
| heuristic present, model present | stronger evidence |
| heuristic present, model missing | likely keyword false positive; manually inspect |
| heuristic missing, model present | likely semantic false negative; update extractor or classify as implicit |
| both missing | likely proposed/missing field |

Pass:

- Run model verification on at least 20 public skills before finalizing the field taxonomy.
- Prefer disagreement cases for human review.
- Summarize agreement rate by field.
- For final thesis claims, classify each field as observed, extractable, or proposed using heuristic + model + manual evidence.

Fail:

- Model labels fields without evidence spans.
- Model disagreement is high and is ignored.
- The final thesis uses heuristic percentages alone as if they were validated human annotations.

## Online Expansion Candidates

The first full pass is enough for a thesis-side field audit, but online expansion can strengthen external validity if time permits.

| Source | Why It Matters | Use In Thesis |
|---|---|---|
| Anthropic public skills | Official public `SKILL.md` examples and authoring conventions. | Already partly imported; useful for field examples and hierarchy/progressive-disclosure discussion. |
| OpenAI public skills | Public skills with concrete tool/deployment/browser workflows. | Already partly imported; useful for dependency/tool and environment fields. |
| Claude/Agent Skills documentation | Defines skills as `SKILL.md` plus optional scripts, references, and assets. | Use as conceptual grounding for skill artifact vs representation. |
| SkillRet | Large-scale skill retrieval benchmark over public agent skills. | Use as evidence that scale/retrieval is now a recognized problem. |
| SkillsBench | Skill-usage benchmark and large public-skill collection. | Use as external validation that public skills are broad/diverse. |
| Public skill-quality papers | Analyse thousands of public `SKILL.md` files and reuse issues. | Use to motivate quality, safety, redundancy, and missing-field concerns. |

Expansion rule:

- Only import more public skills if they add coverage for underrepresented field types, such as safety/side effects, hierarchy, dependencies, or resource folders.
- Do not import thousands of public skills just for scale if they are not auditable. Scale is already provided by the 2089-skill benchmark; public imports are mainly for realism and field validity.

## Manual Verification Rubric

For a stratified sample of at least 15 public skills:

- Mark each automatic field label as `correct`, `overcount`, `undercount`, or `ambiguous`.
- Record whether the skill is atomic, broad, hierarchical, or underspecified.
- Record whether the skill's procedural distinctions are recoverable from the `SKILL.md` alone.
- Include heuristic/model disagreement cases once model verification exists.

Subagent review:

- Use the fixed protocol in `thesis_notes/benchmark/public_skills/Public Skill Subagent Review Protocol.md`.
- Review public skills in batches of 5 to 10.
- Require exact evidence quotes for every explicit or implicit label.
- Use subagent review mainly for disagreement cases, low-coverage skills, high-coverage skills that may reflect keyword overcounting, and broad/hierarchical public skills.

Pass:

- At least 80% of manually reviewed field labels are `correct`, or systematic errors are fixed and the audit is rerun.
- Each field is classified as observed, extractable, or proposed.
- The thesis can explain whether each field is an empirical public-skill pattern or a representation-layer design recommendation.

Warning:

- If safety, side effects, dependencies, or hierarchy are frequently missing, describe them as proposed or partially extractable fields rather than existing authoring conventions.
- If public skills are broad and hierarchical, keep them out of gold-label core tests unless they are atomized or labelled as acceptable alternatives.

Fail:

- The detector cannot distinguish real procedural evidence from keyword noise.
- The fields appear only in generated benchmark skills.
- The thesis cannot explain whether field extraction is done by the author, a preprocessing parser, a retriever, or a reranker.

## How This Verifies The Thesis Claim

The audit supports the thesis only if it can answer two separate questions:

1. Do real public skills contain the kinds of information our structured representation uses?
2. When the information is implicit or missing, can we justify a representation layer that extracts or normalizes it?

The next experiment after this audit is field ablation:

- description only
- description + use/routing conditions
- + inputs/preconditions
- + outputs
- + workflow/procedure
- + constraints/not-for
- + dependencies/resources/environment

The strongest claim would be:

> Public skill artifacts commonly contain procedural signals, but not always in normalized fields. Retrieval improves when those signals are represented explicitly, especially under scale and semantic confusability.

The weaker but still useful claim would be:

> Current public skill artifacts are inconsistent. This motivates a normalized representation layer because retrieval-critical procedural information is often implicit or missing.

## Next Actions

1. Add `DEEPSEEK_API_KEY` to `.env`.
2. Run model verification on a 20-skill checkpoint.
3. Compare heuristic and model labels by field.
4. Manually review disagreement cases and the existing 20-skill packet.
5. Fix detector/model prompt rules if there are systematic false positives.
6. Rerun the full 460-skill local audit and model audit only if the schema, detector, or verifier prompt changes materially.
7. Summarize observed/extractable/proposed fields in the thesis notes.
8. Run field ablations to test whether the fields that appear useful actually improve retrieval.
9. Optionally import full folders for a small number of public repositories if the thesis needs stronger evidence about scripts, references, assets, and hierarchy.
