# Critique Response and Validity Improvement Plan

Date: 2026-05-29

Purpose: record the strongest criticism of the current thesis design and convert it into concrete improvement steps.

This note should be treated as a guardrail. Before adding new models, skills, or experiments, check whether the next action addresses one of these validity risks.

## Current Strong Position

The project has a defensible core result:

> At 2089-skill scale, description-only and generic semantic retrieval are fragile, while representations that preserve procedural information improve skill selection. Field ablations suggest that use conditions, output artifacts, and workflow/procedure are the most retrieval-critical fields.

The best current framing is not "structure-aware retrieval is always better." The sharper claim is:

> Scalable skill retrieval depends on preserving the right procedural information and using it with field-aware scoring, because some fields help selection while other fields add noise when treated as ordinary positive text.

## Main Criticisms To Address

### 1. Benchmark and Schema Co-Adaptation

Risk:

- The benchmark skills, prompts, structured fields, and schema reranker were refined together.
- This can advantage the structure-aware method because the benchmark may encode exactly the distinctions the reranker expects.

Mitigation:

- Keep the public-skill audit as external grounding.
- Report field ablation honestly, including fields that hurt.
- Add a final blinded/independent gold-label or acceptable-alternative review for confusing cases.
- Avoid further prompt/schema tuning after final method set is frozen.

Pass condition:

- Final thesis explicitly states that the benchmark is controlled and diagnostic, not a fully naturalistic public benchmark.
- Any final benchmark change after this point must be logged with a reason.

### 2. Gold-Label Stability Against Realistic Alternatives

Risk:

- Some background or public skills may be genuinely acceptable or better than the intended gold skill.
- If this happens, retrieval errors may actually be annotation errors.

Mitigation:

- Do a targeted second-pass adjudication over non-core winners and strict top-1 failures.
- Judge whether each non-core winner is:
  - clearly wrong;
  - acceptable but less specific;
  - acceptable equivalent;
  - better than the current gold;
  - ambiguous / prompt should be revised.

Pass condition:

- All high-impact non-core-over-gold cases are classified.
- Acceptable alternatives are updated before final result tables.
- Remaining strict failures can be explained as retrieval failures, not obvious gold-label mistakes.

### 3. Limited Evaluated Prompt Count

Risk:

- 85 evaluated prompts is enough for an honours-scale controlled study, but thin for broad claims about all skill libraries.

Mitigation:

- Frame claims as controlled benchmark findings.
- Use public-skill audit and literature to support ecological relevance.
- Avoid claiming universal generalization.
- If time allows, add a small additional holdout set, but only after final methods are frozen.

Pass condition:

- Final writing uses language like "in this controlled benchmark" and "evidence suggests," not "proves generally."

### 4. Generated Background Skills May Be Artificial

Risk:

- 1800 background skills provide scale pressure, but generated skills may not match real-world messiness, hierarchy, redundancy, or underspecification.

Mitigation:

- Keep the 460 public imported skills in the library.
- Use public-skill audit to show which fields are observed, extractable, or proposed.
- Report that public skills are messier than controlled benchmark skills.
- Treat this as a limitation and motivation for representation-layer normalization.

Pass condition:

- Thesis distinguishes controlled core skills from generated background skills and public background skills.
- Claims about public skill conventions are based on the public audit, not generated skills.

Follow-up:

- Expanding the public-skill set is useful, but only if it is treated as external background pressure and taxonomy validation.
- Do not silently turn broad public skills into evaluated gold tasks unless they are manually atomized, assigned prompts, and checked for acceptable alternatives.

### 5. Semantic Confusability Measurement Is Not Final

Risk:

- Semantic confusability currently relies on MiniLM for validation.
- MiniLM is useful locally but not a strong modern semantic judge.

Mitigation:

- Treat MiniLM confusability as benchmark construction evidence, not final proof.
- Use stronger provider retrieval/reranking results as additional evidence of difficulty.
- In final writing, say semantic confusability is operationalized by controlled near-neighbour design plus embedding-based checks.

Pass condition:

- Do not claim MiniLM is the final semantic authority.
- Report the 75/85 pass with caveat.

### 6. Public-Skill Audit Is Not A Gold Annotation Study

Risk:

- Public-field evidence comes from heuristic extraction, DeepSeek verification, subagent calibration, and pattern-level adjudication.
- This is useful but not the same as a full human-coded corpus study.

Mitigation:

- Use public audit as grounding and plausibility evidence.
- Do not overclaim field prevalence numbers.
- Present the final taxonomy as observed/extractable/proposed.

Pass condition:

- Final thesis says public skills contain recoverable procedural signals, not clean author-provided schema fields.

### 7. Downstream Task Success Is Missing

Risk:

- Current results prove offline retrieval/ranking quality.
- They do not yet prove that better retrieval improves actual agent outputs.

Mitigation:

- Run Step 9 downstream validation on a small sample.
- Include oracle-gold condition to check whether the skill itself supports successful task completion.
- Compare baseline candidates against schema/hybrid candidates.

Pass condition:

- At minimum, run 12 prompts across:
  - oracle gold skill;
  - flat/metadata baseline candidates;
  - embedding candidates;
  - structured or hybrid candidates.
- Report task success, wrong-skill misuse, artifact correctness, and cost/context.

## Recommended Next Experiments

### Experiment A: Targeted Independent Adjudication

Purpose:

- Strengthen gold-label stability and reduce benchmark bias.

Scope:

- Non-core-over-gold cases.
- Strict top-1 failures from strongest methods.
- Any prompt where an alternative seems plausibly equivalent.

Output:

- Updated `acceptable_alternatives.json`.
- A short adjudication report.

Minimum pass:

- Every high-impact disagreement is classified as wrong / acceptable / equivalent / better-than-gold / ambiguous.

### Experiment B: Downstream Validation

Purpose:

- Show that retrieval quality matters for actual agent behavior, not just ranking metrics.

Scope:

- 12 to 20 prompts.
- Include easy, medium, and hard confusion cases.
- Compare 3 or 4 candidate conditions, not every method.

Suggested conditions:

1. Oracle gold skill.
2. Flat baseline top-k.
3. Dense embedding top-k.
4. Hybrid semantic retrieval plus procedural reranking.

Minimum pass:

- Oracle-gold condition succeeds often enough to prove skills are executable/useful.
- Hybrid/structured candidates improve wrong-skill misuse or task success over flat/dense baselines.

### Experiment C: Candidate Budget, Cost, And Latency

Purpose:

- Decide whether top-50 or top-100 is practical.

Scope:

- Qwen full-skill retrieval plus local schema rerank.
- Candidate budgets: top-20, top-50, top-100.

Output:

- Accuracy, top-5, MRR, non-core top-1.
- API cache status.
- Local rerank time.
- Candidate text/context estimate.

Minimum pass:

- Pick a final candidate budget and justify it as an accuracy/cost trade-off.

### Experiment D: Expanded Public-Skill Taxonomy And Background Stress Test

Purpose:

- Check whether the final representation-field taxonomy still holds on a larger and messier set of public skills.
- Increase realistic background pressure so target skills must still be retrievable when many unrelated or weakly related public skills exist.

Scope:

- Add more public `SKILL.md` artifacts as background skills where licensing/tool assumptions are acceptable for research use.
- Keep the evaluated gold set unchanged unless a public skill is manually atomized and annotated.
- Run the public-field audit on the expanded public subset.
- Rerun selector results only after confirming that added public skills do not create obvious better-than-gold alternatives.

What this tests:

- Whether the field taxonomy generalizes beyond the original 460 public skills.
- Whether structured/hybrid retrieval remains robust when many public skills are not semantically similar to the target prompt.
- Whether the retriever can avoid irrelevant public skills that happen to share tools, resources, or broad domain terms.

What this does not test:

- It does not test new semantic-confusion clusters unless the imported public skills are manually converted into atomic evaluated skills with gold prompts.
- It does not replace downstream validation.

Pass condition:

- Expanded public skills are clearly marked as background/public, not controlled gold skills.
- Public-field prevalence is reported as observed/extractable/proposed, not as exact ecosystem truth.
- Target gold skills remain top-k retrievable under the expanded background condition.
- Any public skill that beats gold is manually classified as wrong / acceptable / equivalent / better-than-gold / ambiguous.

## Novelty Position After Critique

The novelty is not:

- inventing BM25;
- inventing embeddings;
- inventing reranking;
- proving that retrieval matters.

The novelty is:

- focusing on agent skill artifacts rather than ordinary documents or atomic tools;
- operationalizing semantic confusion among procedurally different near-neighbour skills;
- showing which skill-representation fields improve retrieval;
- showing that some procedural fields must be used carefully because naive text concatenation can hurt;
- connecting public skill artifact analysis with controlled retrieval experiments.

## Updated Thesis Claim

Use this version in writing:

> This thesis studies scalable retrieval for agent skill libraries by asking what procedural information a skill representation should preserve. In a controlled 2089-skill benchmark, retrieval methods that expose use conditions, expected outputs, and workflow information distinguish semantically similar skills more reliably than flat descriptions or generic semantic retrieval alone. However, boundary, dependency, and resource information must be handled with field-aware logic because simply adding more text can introduce retrieval noise.
