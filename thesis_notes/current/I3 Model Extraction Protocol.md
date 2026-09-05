# I3 Model Extraction Protocol

Last updated: 2026-08-18

RQ2 scope note: local full-library I3C is **not required for current RQ2a**, which uses reviewed oracle facts from RQ1a. It becomes relevant only if the draft RQ2b full-library study is later reviewed and approved. Do not launch local I3C extraction merely to satisfy the current RQ2a implementation queue.

Canonical RQ2 status and implementation authority: `thesis_notes/current/RQ2 Current Status and Implementation Tracker - 2026-07-26.md`.

Current RQ2b V3 exception: the first V3 manual-QA attempt is quarantined and
unscored because its rubric was under-specified. The user explicitly waived a
replacement blinded review. For this one frozen V3 corpus, pre-retrieval
eligibility rests on the automatic-integrity freeze (source hashes, exact
evidence, identity, serialisation, root coverage, duplicate observation, and
scaffold exclusion), not on independent human/semantic extraction QA. Any RQ2b
write-up must state that limitation.

Status: local full-library I3M extraction completed for `benchmark-v0.4-2026-06-16` on 2026-06-18 as a paid DeepSeek/API feasibility attempt. External SkillRouter-Eval-Core I3M extraction is complete for rows `0-2999` as an extraction-quality pilot. ChatGPT/Codex-subagent I3C extraction is complete for rows `3000-5999`, the 3284-row top-20 task-relevant pool, and the full 79,141-row Hard-tier `all_I2` library under the V2 prompt. Full-tier external I3C FTS/BM25 retrieval has been run. Local frozen-v0.4 I3C has not yet been produced.

## Why This Exists

The current frozen-v0.4 `I3`/`R2` representation was not uniformly produced by a model parser.

Current state:

- Controlled benchmark skills are mostly authored with explicit skill sections such as `use_when`, `preconditions`, `workflow`, `output`, and `not_for`. The exporter reads those fields deterministically.
- Public imported skills were audited heuristically and then verified with DeepSeek-assisted field-presence checks, but those model checks were not used as the canonical retrieval representation.
- SkillRouter-Eval-Core external `I3` was produced with the same deterministic/heuristic extractor. No DeepSeek/Qwen/LLM API was used for that first external parse.

Therefore, any strong claim about the full potential of extracted selection information should distinguish:

1. **Heuristic I3**: deterministic heading/sentence extraction.
2. **Model-verified field audit**: model checks whether fields are present, with evidence spans.
3. **Model-parsed I3**: model produces the actual structured selection representation used by retrievers/rerankers.
4. **ChatGPT/Codex-parsed I3**: Codex subagents produce the same seven-field representation without a paid provider extraction API; this is labelled `I3C` and must pass evidence/provenance gates before headline use. Manual QA is normally an additional gate; the RQ2b V3 automatic-integrity exception above is explicit, bounded, and does not license an independent semantic-completeness claim. The current subagent prompt is `skill_benchmark/extraction_prompts/I3C_SUBAGENT_EXTRACTION_V2.md`.

The first local full-library **model-parsed I3** run is complete, but it is the paid-model `I3M` attempt. External SkillRouter-Eval-Core I3C extraction coverage is now sufficient for fixed-candidate and full-tier retrieval evaluation, and the full-tier FTS/BM25 I3C condition has been run.

## Intended Thesis Role

Model-parsed I3 should test the upper bound of explicit information extraction:

> If the necessary selection information is recoverable from a skill artifact, does exposing it in a structured field layer improve retrieval or reranking compared with flat metadata and full raw skill text?

This does not claim all skills must be authored in this schema. It tests whether these information types are useful when recovered and made selector-visible.

## Field Taxonomy

Each extracted item must be grounded in the skill text. Multiple inputs, outputs, workflow steps, constraints, dependencies, or resources must be preserved as numbered entries within the same skill-level I3 instance.

| Field | What to extract | Why it matters for retrieval |
|---|---|---|
| `use_conditions` | Conditions, tasks, or user intents that indicate when the skill should be selected. | Distinguishes broad topical relevance from actual fit. |
| `input_preconditions` | Required inputs, files, data state, user context, prerequisites, permissions, or prior artifacts. | Many confusable skills differ mainly by what they require. |
| `output_artifacts` | Expected deliverables, formats, files, reports, patches, tables, plans, answers, or response shape. | Selection often depends on the requested artifact, not only topic. |
| `workflow_steps` | Ordered or unordered procedure steps the skill performs. | Captures procedural difference among semantically similar skills. |
| `constraints_boundaries` | Scope limits, not-for cases, style rules, exclusions, or conditions where use is inappropriate. | Prevents plausible-but-wrong skills from being selected. |
| `dependencies_resources` | Tools, APIs, commands, models, platforms, credentials, bundled files, links, templates, scripts, or external services. | Helps when the correct skill depends on particular capabilities or resources. |
| `success_criteria` | What counts as correct completion, verification checks, acceptance criteria, metrics, or quality conditions. | Separates skills that produce superficially similar artifacts but optimize different outcomes. |

Excluded from I3M:

- `hierarchy_links`: belongs to planned I4/I5 relation/hierarchy layers, not core I3.
- `side_effects`: only extract them if they are stated as constraints, boundaries, dependencies, or success criteria.
- `selection_summary`: may be generated later as a serialization convenience, but it is not an independent I3 information field.
- `parse_warnings` / `qa_warnings`: may be stored in QA metadata, but it is not selector-visible I3 information.

## Output Requirements

- Return valid JSON only.
- Do not infer what a good skill should contain.
- Extract only information supported by the provided skill artifact.
- Use `[]` for missing fields.
- Every extracted item must include:
  - a stable local `id`, such as `input_1` or `step_3`;
  - a concise normalized `text`;
  - `evidence`: one short exact quote from the skill artifact;
  - `evidence_status`: `explicit` or `implicit`;
  - `confidence`: number from 0.0 to 1.0.
- Evidence quotes must be copied verbatim from the provided artifact.
- If an evidence quote cannot be found in the artifact, the item should not be extracted.
- Keep code snippets, YAML, long tables, and long examples out of evidence unless no shorter evidence exists.
- Preserve multiple workflow steps as separate numbered objects.
- Preserve multiple inputs and outputs as separate numbered objects.
- Do not collapse a broad skill into multiple skills. This parser extracts one I3 instance per skill artifact.
- Do not extract hierarchy, relation, broad/subskill links, parse warnings, or selection summaries into I3M.
- For I3C, missing or weak fields should be recorded as non-selector-visible `absent_fields`, `field_warnings`, or `qa_warnings`; do not force vague or generic artifact text into the seven selector-visible fields.

## Frozen Prompt Candidate: `I3_MODEL_EXTRACTION_V1`

### System Message

```text
You are a strict evidence-grounded parser for agent skill artifacts.

Your job is to extract selector-relevant information from a single skill artifact into a structured I3 representation.

Return only valid JSON. Do not include Markdown, commentary, or explanations outside JSON.

Do not infer what a skill should contain. Extract only information supported by direct evidence from the provided artifact. You may normalize wording, but every extracted item must include a short exact quote copied from the artifact as evidence.

If a field is absent or not supported by evidence, return an empty array for that field.
```

### User Message Template

```text
Parse the following skill artifact into the I3 structured selection representation.

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
3. Every extracted item must be grounded in an exact evidence quote from the artifact.
4. Evidence quotes must be short and copied verbatim.
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
- skill_id: {{skill_id}}
- skill_name: {{skill_name}}
- source: {{source}}

Skill artifact:
```markdown
{{skill_artifact}}
```
```

## Executed Local Model Settings

Final local full-library run:

- Script: `skill_benchmark/scripts/model_parse_i3m_skills.py`
- Primary provider/model: `deepseek` / `deepseek-v4-flash`
- Fallback model: `deepseek-chat`
- Temperature: `0`
- JSON mode: enabled through `response_format = {"type": "json_object"}`
- Max output tokens: `5000`
- Input truncation cap: `22000` characters; final full run had `0` truncated rows
- Resume key: `family/skill` rows appended to JSONL and skipped on resume
- Output: `skill_benchmark/representations/I3M_model_parsed.jsonl`
- Checkpoint: `thesis_notes/checkpoints/methods/I3M Local Full-Library Parse Checkpoint - 2026-06-18.md`

## External SkillRouter-Eval-Core I3M / I3C Status

First external checkpoint:

- Checkpoint: `thesis_notes/checkpoints/skillrouter/External SkillRouter I3M Partial Extraction Checkpoint - 2026-06-19.md`
- Input artifact: `skill_benchmark/external/skillrouter_eval_core/derived/representations/all_I2.jsonl`
- Target subset started: first `3000` SkillRouter rows.
- Output chunk folder: `skill_benchmark/external/skillrouter_eval_core/outputs/i3m_model_parse/chunks`
- Representation chunk folder: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3m_chunks`

I3M status:

- External JSONL parsing support is implemented through `--input-jsonl`, `--offset`, and `--family-label`.
- Unsupported evidence items are dropped from selector-visible fields and recorded as QA warnings.
- `--retry-failed` is implemented so failed rows can be repaired without discarding successful rows.
- Rows `0-2999` now have `3000` deduplicated latest rows and `0` latest parse-failed rows.
- The strict selector-valid count is `2997/3000`, with 3 documented QA residues in the SkillRouter I3M checkpoint.

I3C status:

- Rows `3000-5999` were parsed by ChatGPT/Codex subagents using the same seven I3 fields and no external provider extraction API.
- Canonical output: `skill_benchmark/external/skillrouter_eval_core/derived/representations/I3C_codex_subagent_rows_03000_05999.jsonl`.
- Validation after merge repair: `3000` rows, `0` parse-failed rows, `0` missing skill ids, `46,129` extracted evidence items, `45,507` exact evidence matches, and `620` missing exact evidence strings (`1.34%`).
- Manual sample inspection found generally usable structured fields but also heterogeneous extraction style and occasional broad/background extraction. Treat I3C as a candidate practical extraction method with QA gates, not as unchecked ground truth.
- Prompt update: future I3C runs should use `I3C_SUBAGENT_EXTRACTION_V2` in `skill_benchmark/extraction_prompts/I3C_SUBAGENT_EXTRACTION_V2.md`. V2 requires selector-usefulness checks and stores absent/weak fields in `absent_fields`, `field_warnings`, and `qa_warnings` rather than forcing weak text into selector-visible fields.

I3C V2 task-relevant SkillRouter top-20 pool:

- Source pool: `skill_benchmark/external/skillrouter_eval_core/derived/representations/skillrouter_task_relevant_pool_top20_I2.jsonl`.
- Raw merge: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_top20_pool/I3C_V2_top20_pool_merged.jsonl`.
- Canonical cleaned file for external retrieval experiments: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_top20_pool/I3C_V2_top20_pool_cleaned.jsonl`.
- Rows: `3284`.
- Parse-failed rows: `0`.
- Missing skill ids: `0`.
- Duplicate skill ids: `0`.
- Evidence validation after cleaning: `25544/25544` exact source matches, `0` evidence mismatches, `0` heading-only evidence items.
- Sparse-artifact behavior: `7` rows have no selector-visible fields and are retained with QA metadata rather than overfilled.
- Checkpoint: `thesis_notes/checkpoints/skillrouter/External SkillRouter I3C V2 Top20 Pool Extraction Checkpoint - 2026-06-19.md`.

Full SkillRouter I3C V2 extraction status:

- Completed target: all rows in `skill_benchmark/external/skillrouter_eval_core/derived/representations/all_I2.jsonl` are parsed into I3C V2.
- Canonical cleaned file for external full-tier experiments: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_full_all/I3C_V2_full_all_cleaned.jsonl`.
- Clean QA: `79141/79141` rows, `0` parse failures, `0` missing skill ids, `0` duplicate skill ids, `498836/498836` exact evidence matches, and `0` heading-only evidence after cleaning.
- Seed: reused `I3C_V2_top20_pool_cleaned.jsonl` because it had already passed V2 QA.
- Do not mix this artifact with older DeepSeek `I3M` or older V1-style I3C slices in retrieval tables, because those use different extraction protocols.
- Preparation script: `skill_benchmark/scripts/prepare_skillrouter_i3c_full_extraction.py`.

External retrieval warning:

- The first I3M and V1-style I3C subsets are not sufficient for SkillRouter-Eval-Core retrieval evaluation. The 75 scored tasks use 186 unique gold skills at rows `27018-27213`, while the older completed slices cover rows `0-5999`.
- The I3C V2 top-20 task-relevant pool is sufficient for a fixed-candidate external reranking/information-layer ablation, while the full-all I3C V2 artifact is sufficient for a full-tier I3C condition. Full-tier FTS/BM25 retrieval has been run; fixed-candidate top-20/top-50 reranking remains separate future work.
- I3C V2 is still an `I3` structured field representation. It does not create `I4` relation edges or `I5` hierarchy/tree structure.
- External full-tier I3C result report: `skill_benchmark/external/skillrouter_eval_core/outputs/skillrouter_eval_core_fts_information_layers_i3c_v2.md`.
- Before reporting any additional external I3C result, declare the candidate universe and report Hit@1, MRR@10, Recall@k, FullCoverage@k, nDCG@10, and representation/token cost.

Pilot gate:

- Rows: `60`
- Valid rows: `57` (`95.0%`)
- Parse-failed rows: `0`
- Evidence exact match rate: `99.3%`
- Evidence case-insensitive/whitespace-insensitive match rate: `99.6%`

Full local parse:

- Rows: `2433`
- Valid rows: `2333` (`95.9%`)
- Parse-failed rows: `0`
- Fallback rows: `1398`
- Extracted items: `54,989`
- Evidence exact match rate: `98.7%`
- Evidence case-insensitive/whitespace-insensitive match rate: `99.7%`

## Model Settings To Freeze For Future Runs

Recommended settings for future paid-provider I3M reruns, if budget returns:

- Provider/model: DeepSeek cheap JSON-capable model or Qwen long-context JSON-capable model; exact model must be recorded before running.
- Temperature: `0`.
- JSON mode: enabled if provider supports it.
- Max output tokens: at least `4000`; increase if truncation is common.
- Input truncation: record `max_chars` and whether truncation occurred.
- Cache key: include schema version, model, provider, prompt hash, skill id, and artifact hash.
- Resume behavior: append JSONL rows and skip completed skill ids unless `--force` is set.

## Required Validation Before Using Model-Parsed I3 In Thesis Results

Before rerunning retrieval on model-parsed I3 in a new benchmark or external dataset:

1. Parse a pilot sample:
   - 20 local benchmark skills.
   - 20 imported public skills.
   - 20 SkillRouter-Eval-Core skills, including gold and hard-only distractors where possible.
2. Validate JSON schema strictly.
3. Check evidence quotes are found in the source artifact.
4. Manually inspect at least 20 pilot outputs.
5. Compare token size and field coverage against heuristic I3.
6. Only then run full model-parsed I3 extraction.

Local frozen-v0.4 status: paid-model I3M pilot gate and full local extraction are complete. Local I3C is not yet produced; do not relabel `skill_benchmark/representations/I3M_model_parsed.jsonl` as I3C. Next validation, if local I3C is needed, is extraction-side first: create the local Codex/ChatGPT-style I3C artifact, then compare it against I1/I3H/I2 under fixed retrieval methods.

External SkillRouter-Eval-Core status: I3C V2 top-20 task-relevant pool extraction and full-all Hard-tier extraction are complete and cleaned. Full-tier FTS/BM25 has compared I1, I2, I3H, and I3C on Easy/Hard. Remaining optional external work is fixed-candidate top-20/top-50 reranking; the top-50 I3C condition can be materialized by filtering the full-all cleaned artifact. Graph/relation conversion remains separate `I4/I5` work.

## Naming

Use these names to avoid confusion:

- `I3H`: heuristic I3, current deterministic/section-based extraction.
- `I3V`: model-verified field audit, not necessarily used as retrieval representation.
- `I3M`: paid-provider model-parsed I3 using the frozen provider/API extraction protocol.
- `I3C`: ChatGPT/Codex-subagent parsed I3 using the same seven fields, proposed as a practical extraction route only after QA gates.

Do not compare old `I3H` results against future `I3M` or `I3C` results without naming the extraction condition.
