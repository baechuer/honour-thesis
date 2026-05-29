# Benchmark Methodology Rubric

This note is the working rubric for deciding whether the benchmark and representation layers are good enough for the thesis.

The thesis studies skill selection as a candidate-subsetting layer before the main agent loads full skill artifacts. The benchmark should therefore test whether different skill representations help a selector surface the right procedural skill under semantic confusion and scale.

For experiment sequencing, use `thesis_notes/Thesis Experiment Roadmap.md`. This rubric answers "is the benchmark valid enough?" The roadmap answers "what experiment should happen next?"

## Core Claim To Test

A benchmark item is useful when several skills look semantically plausible from compressed metadata, but only one skill is procedurally correct once input, output, workflow, preconditions, dependencies, resources, or success criterion are considered.

Good benchmark pressure means:

- high surface similarity between gold and alternatives
- clear procedural divergence between gold and alternatives
- stable gold labels
- non-trivial retrieval difficulty
- measurable degradation under scale
- visible differences between representation methods

## Nine-Step Benchmark Loop

Use this staged loop for benchmark validation. Do not treat the selector-evaluation step as an invitation to test unlimited methods; final method selection is governed by the experiment roadmap.

1. Validate skill and prompt integrity.
2. Validate representation coverage and procedural requirement alignment.
3. Validate semantic confusability.
4. Validate gold-label stability and prompt-leakage risk.
5. Build or refresh scale regimes.
6. Audit public/real-world skill artifacts for representation-field validity.
7. Run offline selectors, rerankers, field ablations, and scale-sensitivity checks.
8. Run the M0 progressive-disclosure main-agent baseline.
9. Run candidate-subsetting plus main-agent downstream checks on a smaller sample.

Loop rule:

- If Step 1 fails, fix references/frontmatter before any retrieval claims.
- If Step 2 fails, rewrite skills or prompts so the gold label is procedurally justified.
- If Step 3 fails, add or revise alternatives so errors are plausible semantic confusions.
- If Step 4 fails, rewrite ambiguous or leaked prompts.
- If Step 5 fails, add realistic background/public skills before claiming scale behavior.
- If Step 6 shows our proposed fields are mostly absent or non-extractable in public skills, reframe the schema as a proposed normalization layer and report that adoption gap explicitly.
- If Step 7 is near-perfect for all methods, harden the benchmark before claiming representation value.
- If Step 8 or Step 9 disagrees with offline selectors, inspect whether the main-agent prompt policy or downstream artifact task is masking retrieval errors.

## Current Validation Snapshot

Last refreshed on 2026-05-28 against the expanded 2089-skill library.

- Step 1 integrity: PASS. 85 prompts and 2349 skills resolve.
- Current composition: 85 controlled/evaluated skills, 1800 generated background-scale skills, 460 public imported background skills, and 4 support email skills.
- Public imports: PASS. 460 public-source wrappers were created from OpenAI, Anthropic, `claude-office-skills`, Hugging Face, `akillness/oh-my-skills`, Addy Osmani skills, Matt Pocock skills, SWE-Skills-Bench, and other smaller public sources; 460/460 original `SKILL.md` files downloaded successfully.
- Step 2 procedural distinctness: PASS. 85/85 prompts pass; 251/251 gold/alternative pairs differ on at least two primary axes.
- Step 2 prompt-specific alignment: PASS. 85/85 prompts pass the stricter automated alignment check after prompt refinements and a negation-aware scoring fix.
- Step 3 semantic confusability: PASS with caveat. The previous MiniLM checkpoint had 75/85 prompts with at least two plausible listed alternatives. The current 2349 rerun used TF-IDF fallback because `sentence_transformers` is unavailable in this shell, producing 27/85, so it is not directly comparable.
- Step 4 prompt leakage: PASS. 0 critical exact-name leaks and 0 high-risk leaks.
- Step 5 scale regime: PASS. The 2349-skill condition is now a near-context-limit scale condition for compact metadata/progressive-disclosure style systems. R1 flat metadata is about 120k selector-visible tokens.
- Step 6 public/real-world skill field audit: MOSTLY DONE. Current heuristic checkpoint audits 460/460 imported public `SKILL.md` files; the earlier 200-skill subset also has DeepSeek model-assisted verification, a 10-skill subagent/manual calibration pilot, and pattern-level disagreement adjudication.
- Step 7 non-core semantic competition: PASS useful pressure under TF-IDF fallback. A non-core skill is top-1 for 26/85 prompts, and the best non-core skill beats gold for 30/85 prompts.
- Step 7 all-non-core procedural competition: PASS with risks under TF-IDF fallback. 14/85 prompts have at least one non-core skill above gold. These cases require manual adjudication before final claims.
- Step 7 local selector baselines: PASS useful pressure. On the 2349-skill full library, the rerun lexical/schema subset ranges from 58.8% to 78.8% top-1. MiniLM methods remain 2089-scale/historical unless the semantic backend is restored.
- Step 7 Qwen provider update: PASS useful pressure for the full-skill condition. Qwen full-skill embedding reaches 50.6% top-1; Qwen full-skill plus Qwen rerank reaches 63.5%; Qwen full-skill plus local schema rerank reaches 84.7% at top-100.
- Historical 1006-skill results remain useful as a v1 comparison for Qwen R1/R2 variants.
- Low-information stress test: DONE separately, not merged into the main benchmark.
- Step 8 M0 progressive disclosure: previous core-only M0 trace remains the only completed M0 run. The full 2349-skill M0 condition is now mainly a context/cost stress test and has not been run.

Interpretation: the expanded benchmark is valid enough for local scale-sensitivity analysis. The main current risk is no longer lack of scale; it is gold-label stability under realistic public/generated competitors. Before final thesis claims, the non-core winners above gold should be manually adjudicated as better, acceptable, borderline, or merely plausible distractors.

## Benchmark Validation Rubric

### 1. Skill And Prompt Integrity

Checks:

- every prompt has a unique `id`
- every `gold_skill` exists as a `SKILL.md`
- every `closest_alternatives` entry exists
- every skill has frontmatter `name` and `description`
- public imports are separated from the controlled core

Pass:

- 100% prompt references resolve
- no duplicate prompt IDs
- no malformed skill frontmatter in evaluated families

Fail:

- missing gold skill
- duplicate prompt ID
- malformed metadata in a main evaluated skill

### 2. Procedural Requirement Alignment

This step has two layers. The first layer is a field audit: do the gold skill and alternatives expose different procedural fields? The second and stricter layer is prompt-specific requirement alignment: what concrete requirement in the prompt makes the gold skill correct and each alternative wrong?

For each gold/alternative pair, annotate which requirement axis differs:

- input type or input state
- output artifact
- workflow steps
- preconditions
- required tools or external dependencies
- optional resources
- success criterion
- side effects

Pass:

- every gold prompt has at least one concrete requirement that explains the gold label
- each listed alternative can be rejected because it misses a prompt requirement, produces the wrong artifact, follows the wrong workflow, assumes the wrong precondition, lacks a required dependency/resource, or optimizes for the wrong success criterion
- most high-value cases differ on two or more axes
- the differentiator is visible in a structured representation and does not depend only on `not_for` negation

Fail:

- gold and alternative are effectively interchangeable
- distinction depends only on wording preference
- gold label cannot be explained procedurally
- workflow fields are merely paraphrases and no prompt-specific requirement separates the skills

### 3. Semantic Confusability

Checks:

- compare prompt text with gold and alternative skill descriptions
- compare gold skill description with closest alternatives
- inspect lexical overlap, shared trigger words, TF-IDF/cosine similarity, and embedding similarity when an embedding backend is available

Pass:

- each main prompt has at least two plausible neighboring skills
- gold and closest alternatives share meaningful task vocabulary
- failures are plausible confusions, not random unrelated selections

Fail:

- gold skill is uniquely obvious from exact wording
- alternatives are semantically unrelated
- background distractors never appear in top-k under cheap selectors

### 4. Gold Label Stability

Checks:

- manual review of prompt and candidate skills
- optional independent annotation by another person or model
- agreement on gold skill and acceptable alternatives

Pass:

- annotators agree on gold for most prompts
- ambiguous prompts are rewritten or removed
- acceptable-but-not-ideal alternatives are documented

Fail:

- multiple skills are equally correct
- prompt requires hidden assumptions
- gold label changes depending on stylistic preference

### 4b. Prompt Leakage

Checks:

- exact gold skill ID or skill name appears in the prompt
- prompt uses distinctive gold title words much more than alternative title words
- prompt copies long phrases from the gold skill card
- selectors could win through label matching rather than procedural fit

Pass:

- zero exact gold skill-name leaks
- zero or very few high-risk title/phrase leaks
- any remaining medium-risk wording is documented and judged to be natural task vocabulary
- Step 2 procedural alignment remains passing after leakage reduction

Fail:

- prompt directly names the gold skill
- prompt contains copied gold-card phrasing that makes the answer obvious
- removing leaked wording makes the gold label procedurally unstable

### 5. Difficulty Calibration

Checks:

- run progressive-disclosure baseline on core library
- run cheap selectors on flat metadata
- inspect per-cluster confusion

Pass:

- not all methods score near-perfect
- not all methods fail randomly
- at least some clusters produce repeatable near-neighbor confusions

Warning:

- top-1 accuracy above 90% for all methods may mean the benchmark is too easy
- top-1 accuracy below 30% for humans or strong main-agent selection may mean the benchmark is ambiguous

### 6. Public/Real-World Skill Field Audit

Purpose:

Check whether the proposed representation fields are grounded in real skill artifacts rather than only in our generated controlled benchmark.

This step separates three claims:

- `observed field`: public skills already expose this information explicitly
- `extractable field`: public skills contain this information implicitly, but the representation layer must parse or normalize it
- `proposed field`: public skills often lack this information, but the thesis argues it should be preserved for reliable retrieval

Checks:

- audit imported public skills for explicit headings and implicit evidence
- count fields such as routing trigger, inputs/preconditions, outputs, workflow/procedure, constraints/not-for, dependencies/tools, scripts/resources/references, examples, and tests
- run a model-assisted semantic extraction pass on a subset or the full public-skill sample, using a strict JSON schema with evidence spans
- compare heuristic and model labels to identify likely false positives and false negatives
- manually sample a small subset to check whether automated field tags are reasonable
- prioritize manual review of heuristic/model disagreement cases
- compare public-skill field prevalence with the controlled benchmark schema
- document public skills that are broad, hierarchical, underspecified, or difficult to atomize

Pass:

- the audit covers at least the current 200 imported public skills or a clearly defined public subset
- model-assisted extraction has been run on at least a checkpoint sample, or the thesis explicitly states why only deterministic extraction is used
- model outputs include quoted evidence spans or mark the field as missing
- heuristic/model disagreements are summarized by field
- each proposed representation field is classified as observed, extractable, or proposed
- the thesis can explain whether the field is an empirical artifact pattern or a retrieval-oriented normalization design
- public skills provide enough evidence that the schema is not only tailored to our generated skills

Fail:

- proposed fields appear only in our generated skills and not in public artifacts
- the model verifier asserts fields without evidence spans
- heuristic/model disagreement is high and no manual calibration is performed
- public skills are so broad or messy that field extraction cannot be meaningfully evaluated
- the thesis cannot explain whether structured fields are authoring requirements or representation-layer extraction targets

### 7. Offline Selectors, Field Ablations, And Scale Sensitivity

Checks:

- evaluate on at least two library sizes:
  - core only
  - core plus background/public skills
- compare accuracy, top-k recall, MRR, context cost, and background false positives
- inspect non-core skills that outrank gold skills to decide whether they are true procedural alternatives or only semantic distractors
- run field ablations to test which information improves selection:
  - description only
  - description + use conditions
  - + input/precondition fields
  - + output artifact fields
  - + workflow/procedure fields
  - + constraints/not-for fields
  - + dependencies/resources

Pass:

- larger library increases context cost or retrieval difficulty
- at least some background/public skills appear as plausible false positives
- representation-aware methods degrade less than weaker representations
- non-core winners are mostly procedurally wrong or documented as acceptable-but-not-gold borderline cases
- field ablation shows which information contributes to retrieval, or honestly shows that some fields add little

Fail:

- adding background skills changes nothing
- background skills are all unrelated noise
- scale condition cannot be distinguished from core condition
- many background skills are equally or more procedurally correct than the gold labels without being documented as acceptable alternatives
- structured reranking wins only because our controlled skills expose hand-authored fields that public skills lack, with no audit or extraction argument

### 8. M0 Progressive Disclosure Baseline

Checks:

- expose all skill names/descriptions/compact metadata to the main agent
- record selected skills and full `SKILL.md` documents loaded
- record selector-visible token cost and final context cost
- compare core-only runs with the largest feasible library stress test

Pass:

- current prompt and skill versions are used
- every trace records selected skill, gold skill, loaded docs, and failure mode
- core runs are feasible and comparable with offline selector metrics
- token/context cost is recorded, approximated, or explicitly marked unavailable
- large-library runs either complete or are documented as context/cost infeasible

Fail:

- traces are stale relative to current prompts or skills
- selected skill cannot be recovered from logs
- M0 is reported as cost evidence without token/context cost

### 9. Downstream Candidate-Subset Validation

Checks:

- take a smaller sample of prompts after offline retrieval behavior is understood
- pass retrieved candidates to the main agent under a fixed prompt policy
- load only the selected full skill artifacts
- evaluate the final task artifact, not only the selected skill ID

Pass:

- retrieval success is separated from downstream artifact success
- task artifact is checked for required fields, workflow, dependency/resource use, and unsupported invention
- downstream failures can be traced back to retrieval, skill execution, or task ambiguity
- at least 12 representative prompts are used, including both easy-success and known-confusion cases
- each compared selector uses the same candidate budget, preferably top-5 for first validation
- gold-or-acceptable candidate recall is at least 85% for methods being taken into downstream execution, otherwise the downstream failure is labelled as retrieval failure
- artifact success is at least 80% for oracle-gold runs; if oracle-gold fails below this, the task prompt or skill itself is not stable enough for downstream evaluation

Fail:

- a good-looking final answer hides wrong-skill selection
- the main agent sees extra skill information that the method was not supposed to expose
- downstream task success is judged without checking whether the selected skill was procedurally appropriate

## Method Families

These are broad experimental families, not single algorithms. A method is a combination of candidate representation, first-stage selector, optional reranker, candidate budget, and final main-agent skill-loading policy.

The thesis should report methods in this form. Embedding retrieval is one scalable selector family, not the baseline. The baseline is normal progressive disclosure.

## Embedding Model Policy

Use embedding models at two different levels.

### Construction / Validation Model

`sentence-transformers/all-MiniLM-L6-v2` is the current local validation model.

Purpose:

- cheap benchmark construction signal
- semantic-confusability sanity check
- prompt/skill similarity audit
- repeatable local validation on an 8 GB laptop

Do not treat MiniLM as the strongest embedding baseline. It is a benchmark-building instrument, not the main evidence against modern retrieval systems.

### Experimental Embedding Baselines

The final retrieval comparison should include stronger embedding/reranking systems where feasible.

Priority candidates:

- Qwen3 embedding model over description cards
- Qwen3 embedding model over full `SKILL.md` artifacts
- Qwen3 reranker over embedding shortlists
- SkillRouter-style embedding model, if the public fine-tuned model is accessible
- SkillRouter-style reranker, if the public fine-tuned model is accessible

Rationale:

- modern embedding models may already encode more procedural information than older sentence encoders
- full-skill embedding may reduce the weakness of description-only retrieval
- reranking is common in realistic retrieval pipelines and should not be ignored
- the thesis claim is stronger if schema/tree/graph-aware methods are compared against modern embedding and reranking baselines, not only against MiniLM

If stronger embedding/reranker baselines perform near-perfectly, revisit the benchmark before making a contribution claim. That may mean the current prompts leak too much information, the clusters are too easy, or the structure-aware representations have been given an unfair information advantage.

### M0: Progressive Disclosure Baseline

Selector-visible representation:

- all skill names and descriptions, possibly basic metadata, in the main agent context
- full `SKILL.md` loaded only after the main agent selects a skill

Purpose:

- realistic small/medium-library baseline
- shows context cost and scalability limit

Pass:

- can run on the core library
- reports selector-visible token/context cost
- produces selected-skill traces
- makes clear when the large-library version is infeasible or only a stress test

### M1: Flat Metadata Candidate Selection

Selector-visible representation:

- name
- description
- optional family/category only when explicitly testing category labels

Selectors may include:

- lexical/BM25
- LLM router over compact metadata

Purpose:

- scalable compressed baseline using the same broad information exposed by progressive disclosure
- tests what happens when candidate subsetting is separated from the main agent but procedural details remain hidden

Pass:

- exports one record per skill
- does not expose full skill bodies, workflow, resources, or schema fields
- reports top-k recall and top-1 accuracy over the same skill library as other scalable methods

### M2: Embedding-Based Skill Retrieval

Embedding retrieval is a method family with variants.

Variants:

- `M2a description-card embedding`: embed only name plus description, optionally family.
- `M2b full-skill embedding`: embed the complete `SKILL.md` text.
- `M2c chunked full-skill embedding`: embed sections/chunks of full skill artifacts, then aggregate or rerank candidate skills.
- `M2d schema-card embedding`: embed structured cards after M3 fields exist.
- `M2e skill-router embedding`: use a skill-routing-tuned embedding model if an accessible public model is available.

Reranking options:

- no reranker
- cross-encoder reranker
- LLM listwise reranker
- Qwen3 reranker
- SkillRouter-style reranker if accessible
- procedural/schema reranker after embedding shortlist

Model tiers:

- MiniLM: construction validator and weak local reference point only
- Qwen3-class embedding: main modern open embedding baseline
- SkillRouter-style embedding: prior-work-aligned skill retrieval baseline if accessible
- API-hosted embedding/reranker: acceptable for stronger comparison if local 8 GB memory is insufficient

Purpose:

- tests dense semantic retrieval under near-neighbor skill descriptions
- tests the claim from skill-routing literature that description-only embeddings can miss procedural distinctions
- tests whether structure-aware representations still help against modern full-skill embeddings and rerankers

Pass:

- reports first-stage top-k recall separately from reranked top-1 accuracy
- compares description-card and full-skill variants
- includes at least one modern stronger embedding baseline beyond MiniLM where feasible
- separates embedding model effects from representation effects
- reports context/storage cost of full-skill or chunked embeddings

### M3: Schema-Enriched Skill Cards

Selector-visible representation:

- name
- description
- input type or input state
- output artifact
- preconditions
- workflow summary
- success criterion
- avoid / not-for boundaries
- optional dependency/resource fields as an ablation

Selectors may include:

- lexical or embedding over serialized fields
- field-weighted scoring
- LLM router over structured cards
- reranker that compares prompt requirements against procedural fields

Purpose:

- tests whether preserving procedural information reduces semantic confusion
- tests a proposed representation format rather than relying only on existing flat descriptions

Pass:

- each main evaluated skill has extractable procedural fields
- fields explain the gold/alternative distinction
- context cost is measured separately from accuracy
- dependency/resource fields are evaluated as ablations, not as an unfair advantage for tool-heavy skills

### M4: Tree / Hierarchical Routing

Selector-visible representation:

- family/category tree
- optional subcategory nodes
- skill leaves
- category summaries

Selectors may include:

- LLM route-to-family then route-to-skill
- lexical or embedding selection at each tree level
- top-n branch routing to reduce early-decision brittleness

Purpose:

- tests an efficient and interpretable scale strategy
- exposes a known weakness: early branch errors can exclude the correct skill

Pass:

- reports branch accuracy separately from final skill accuracy
- reports cases where the gold skill was excluded by an early routing decision
- compares single-branch routing against multi-branch routing

### M5: Graph-Based Skill Retrieval

Selector-visible representation:

- nodes:
  - skill
  - family
  - input type
  - output artifact
  - workflow step
  - tool/dependency
  - resource
  - success criterion
  - avoid condition
- edges:
  - `belongs_to_family`
  - `expects_input`
  - `produces_output`
  - `requires_tool`
  - `uses_resource`
  - `has_precondition`
  - `has_workflow_step`
  - `optimized_for`
  - `avoid_when`
  - `confusable_with`
  - `derived_from_public_skill`

Selectors may include:

- graph filtering by matched input/output/tool nodes
- graph expansion from prompt-derived requirements
- graph-aware reranking over candidate skills
- hybrid retrieval: flat or embedding shortlist followed by graph-based reranking

Purpose:

- tests whether explicit relational structure improves selection beyond serialized text

Pass:

- edges are meaningful and not arbitrary
- graph fields can be ablated
- graph representation improves at least one of top-1, MRR, background false-positive rate, or branch-exclusion recovery without unreasonable context cost

### M6: Hybrid Retrieval And Reranking

Hybrid methods combine a cheap first-stage selector with a richer precision layer.

Examples:

- flat metadata/BM25 shortlist, schema reranker
- description embedding shortlist, full-skill reranker
- full-skill embedding shortlist, schema reranker
- tree route to branches, graph reranker inside branches
- graph filter, LLM listwise reranker

Purpose:

- tests realistic retrieval architecture where a fast candidate generator is followed by a more expensive reranker

Pass:

- reports candidate recall before reranking
- reports reranker rescue rate
- reports cost/latency added by reranking
- improves rank placement without hiding full-library context in the final agent prompt

### M7/M8: Provider Neural Retrieval And Reranking

M7 uses a modern API embedding model as the candidate-subsetting layer. M8 adds a neural reranker over the top-k candidate set.

Implemented examples:

- Qwen `text-embedding-v4` over full `SKILL.md` files
- Qwen `text-embedding-v4` over R1/R2 representation cards
- Qwen `text-embedding-v4` first stage plus `qwen3-rerank` over top-20 candidates
- OpenAI `text-embedding-3-small` or `text-embedding-3-large` as embedding-only baselines

Purpose:

- tests whether the benchmark remains difficult under stronger modern neural retrieval models
- separates representation questions from weak-local-model artifacts
- gives a realistic comparison against current retrieve-then-rerank systems such as SkillRouter-style pipelines

Pass:

- reports provider, model, representation, candidate budget, cache state, and approximate input tokens
- runs a smoke test on a small prompt subset before full-library evaluation
- compares M7/M8 against local M1-M6 on the same prompt set and library scale
- treats API cost, latency, and provider model choice as implementation details, not as the thesis contribution

## Representation Components

The current implementation exports representation components, not final methods.

### Exported Components

- `R1_flat_metadata.jsonl`: name, family, description. Used by M1 and M2a.
- `R2_structured_procedural.jsonl`: parsed use cases, avoid conditions, preconditions, workflows, outputs, and writing rules. Used by M3 and M6.
- `R3_dependency_resource_aware.jsonl`: R2 plus dependency profiles, external dependencies, resource signals, public-source metadata, and resource files. Used as an M3/M5 ablation.
- `R4_graph_edges.jsonl`: graph edge view derived from R2/R3 fields. Used by M5.

What can change:

- embedding model
- description-only versus full-document embedding
- chunking strategy
- schema field weights
- graph edge types and traversal strategy
- reranker type and candidate budget
- whether family/category labels are exposed
- API provider and model, when testing M7/M8

What should not change during a controlled comparison:

- prompt text
- gold labels
- skill library for the scale condition
- whether full skill artifacts are visible before candidate selection, unless that is the method being tested
- final main-agent downstream prompt policy for post-selection runs

## Reranker Families

Reranking should be included because real retrieval systems rarely stop at first-stage retrieval.

Possible variants:

- no reranker
- cross-encoder reranker
- LLM listwise reranker
- pairwise tournament reranker
- structured procedural reranker
- dependency/resource-aware reranker
- graph-aware reranker

When reporting results, separate:

- first-stage recall: did the gold skill enter the candidate set?
- reranking quality: did the reranker move the gold skill toward rank 1?

## Evaluation Metrics

### Retrieval Metrics

- top-1 accuracy
- top-k recall, especially top-3 and top-5
- mean reciprocal rank
- NDCG if alternatives are graded as partially relevant
- confusion matrix by cluster
- background false-positive rate
- public-import false-positive rate

### Efficiency Metrics

- selector-visible token count
- main-agent context tokens after candidate selection
- number of full skill docs loaded
- latency
- approximate cost

### Benchmark Pressure Metrics

- semantic similarity between gold and alternatives
- procedural divergence score
- ambiguity rate
- prompt leakage score
- scale degradation from core to large library
- reranker rescue rate

### Downstream Metrics

Run downstream checks on a smaller sample after retrieval behavior is understood.

- correct artifact type
- required fields included
- unsupported fields not invented
- workflow followed
- dependency/resource used when required
- human judgment of task success

## Expected Results

The benchmark is doing its job if:

- progressive disclosure works reasonably on the core but becomes costly or unstable at larger scale
- flat metadata scalable selectors confuse semantically similar skills
- description-card embeddings underperform full-skill or schema-card variants on procedural near-neighbors
- stronger Qwen3/SkillRouter-style embedding baselines improve over MiniLM but still leave some procedural near-neighbor errors
- first-stage retrieval often has higher top-k recall than top-1 accuracy
- rerankers improve rank placement when the gold skill is in the candidate set
- schema-enriched cards reduce near-neighbor confusions
- dependency/resource fields help only when tool, file, public-source, or external-service requirements matter
- tree routing is efficient but shows branch-exclusion errors
- graph-based methods help only when edges capture real procedural distinctions

The benchmark is weak if:

- every method performs near-perfectly
- every method fails randomly
- background skills never compete with gold skills
- public imported skills add only noise and no dependency/resource pressure
- structured fields do not explain or improve any difficult cases
- annotators cannot agree on gold labels
- modern full-skill embedding plus reranking solves almost every prompt without needing procedural structure

## Immediate Refinement Steps

1. Run the public-skill field audit over imported public `SKILL.md` files.
2. Run representation field ablations to test which fields actually improve retrieval.
3. Consolidate stronger embedding baselines already run through `scripts/run_provider_selectors.py`; rerun Qwen/MiniLM conditions on 2349 only if needed for a final same-scale representation comparison.
4. Decide whether SkillRouter, M4 tree routing, or M5 graph retrieval adds a genuinely new representation claim; otherwise defer them.
5. Rerun M0 progressive-disclosure baseline with exact context-token/cost instrumentation; use the 2349-skill library only as a cost/context stress test if feasible.
6. Run downstream candidate-subset validation on a smaller sample after offline retrieval behavior is stable.
7. If all stronger embedding/reranking methods perform near-perfectly, revisit cluster difficulty and prompt leakage before claiming structure-aware improvement.

## Current Implementation Status

- `scripts/export_skill_representations.py` exports R1-R4 representation components.
- `representations/R1_flat_metadata.jsonl` stores name, family, and description.
- `representations/R2_structured_procedural.jsonl` stores parsed `Use when`, `Not for`, workflow, output, preconditions, and writing rules.
- `representations/R3_dependency_resource_aware.jsonl` adds dependency profiles, external dependencies, resource signals, public-source metadata, and bundled resource files.
- `representations/R4_graph_edges.jsonl` stores graph edges derived from procedural and dependency/resource fields.
- The exported components support method families M1-M8, but do not by themselves implement retrieval, tree routing, graph traversal, reranking, provider API calls, or progressive disclosure evaluation.
- `scripts/analyze_procedural_distinctness.py` implements the first-pass Step 2 field-difference audit over gold/alternative prompt pairs.
- `scripts/analyze_requirement_alignment.py` implements the stricter Step 2 prompt-requirement alignment check.
- `scripts/analyze_semantic_confusability.py` implements Step 3 semantic-confusability reporting with `sentence-transformers/all-MiniLM-L6-v2` when the validation environment is installed, otherwise a local TF-IDF fallback.
- `scripts/analyze_prompt_leakage.py` implements the prompt-leakage check for exact gold-name leakage, dominant gold title-word overlap, and copied gold-card phrases.
- `scripts/validate_benchmark_integrity.py` implements Step 1 as a reproducible report.
- `scripts/audit_public_skill_fields.py` implements the resumable Step 6 public-skill field audit over imported public `SKILL.md` artifacts.
- `scripts/build_public_skill_manual_review_packet.py` builds a stratified manual review packet from the public-skill field audit output.
- `scripts/model_verify_public_skill_fields.py` implements the model-assisted Step 6 semantic verification pass with strict JSON output and required evidence spans.
- `scripts/compare_public_skill_field_audits.py` compares heuristic labels against model labels and produces the Step 6 disagreement report.
- `scripts/build_public_skill_disagreement_review_packet.py` builds a prioritized Step 6 disagreement packet for targeted manual adjudication.
- `scripts/run_field_ablation_selectors.py` implements Step 7 local representation field ablations over cumulative and single-field views.
- `scripts/generate_background_scale_skills.py` now generates 1800 background-scale skills: 80 hand-written broad background skills plus 1720 deterministic domain/procedure skills with dependency and resource signals.
- `scripts/import_public_background_skills.py` now discovers public `SKILL.md` files from selected OpenAI, Anthropic, Hugging Face, `claude-office-skills`, `akillness/oh-my-skills`, Addy Osmani, Matt Pocock, SWE-Skills-Bench, and smaller repositories, while preserving curated metadata overrides for key public skills.
- `scripts/generate_core_v2_clusters.py` generates the current controlled-core v2 expansion: office artifact workflows, deployment/browser QA, and API/backend design.
- `scripts/analyze_non_core_competition.py` checks whether background/public/support skills semantically outrank the gold core skill under description-card similarity.
- `scripts/run_offline_selectors.py` implements the shared offline selector/evaluator harness for M1, M2, M3, and M6 local baselines, with M0 trace-summary support.
- Current M6 rerankers use top-20 first-stage candidates followed by deterministic schema-aware reranking. The reranker combines 40% normalized first-stage score with 60% normalized schema score over description, use_when, output shape, preconditions, workflow, dependency/resource fields, and a mild `not_for` penalty.
- `scripts/run_provider_selectors.py` implements optional M7/M8 provider-backed baselines: OpenAI-compatible embedding retrieval and Qwen `qwen3-rerank` over a first-stage top-k candidate set. It requires API keys and caches calls under `runtime/provider_cache`.
- `notes/provider_api_baselines.md` records current provider choices, API key setup, expected cost controls, and recommended run order.
- `scripts/analyze_m0_manifest.py` implements the dedicated Step 8 M0 progressive-disclosure report with strict top-1, acceptable top-1, any-hit, no-skill, multi-skill, family-level, and prompt-level breakdowns.
- `outputs/step8_downstream_validation_plan.md` records the planned Step 9 downstream sample, conditions, artifact grading rubric, and pass thresholds. The filename still says `step8` from the earlier numbering.
- `scripts/prepare_step8_candidate_report.py` and `outputs/step8_candidate_readiness_report.md` implement the pre-downstream top-5 candidate recall check for the planned Step 9 sample. The filenames still say `step8` from the earlier numbering.
- MiniLM is currently used as a local construction/validation model only. It should not be treated as the main modern embedding baseline in final experiments.
- Stronger embedding/reranking baselines to execute next: Qwen `text-embedding-v4` full-skill retrieval, Qwen `text-embedding-v4` plus `qwen3-rerank`, and SkillRouter-style fine-tuned embedding/reranking if local or hosted execution is feasible. The current M6 reranker is deterministic and local, not a neural cross-encoder.
- Current Step 1 integrity result: PASS. 14 prompt files, 85 prompts, 2349 skills, 85 main evaluated skills, 2264 background/public/support skills, 0 duplicate prompt IDs, 0 duplicate skill names, 0 missing prompt references, and 0 malformed skill frontmatter entries.
- Current representation coverage result: PASS. 85/85 main evaluated skills have `use_when`, `not_for`, `preconditions`, `workflow`, `output_shape`, and `writing_rules`; graph export covers 2349 skills and 52,205 edges.
- Current Step 2 field-audit result: 85/85 prompts pass, and 251/251 gold/alternative pairs have two or more primary procedural differentiators in the structured representation. Treat this as schema coverage only.
- Current stricter Step 2 requirement-alignment result with local TF-IDF scoring: PASS. 85/85 prompts pass and gold ranks first among listed candidates for 85/85 prompts after prompt refinements and negation-aware positive-evidence scoring.
- Current Step 3 semantic-confusability result: PASS with caveat. The previous `sentence-transformers/all-MiniLM-L6-v2` checkpoint had 75/85 prompts with at least two plausible listed alternatives. The 2349 rerun used TF-IDF fallback and produced 27/85, so it is a non-comparable sanity check rather than a replacement result.
- Current Step 4 gold-label stability result: PASS after manual review of `web_p5_frontend_debugging`, `doc_p2_document_rewriter`, `obs_p5_root_cause`, `reply_p2_polish_supervisor`, `sec_p2_security_code_review`, and post-leakage weak cases `sec_p1_threat_model` and `skill_p2_install_existing`. No reviewed case was removed as ambiguous.
- Current prompt-leakage result: PASS. 0 critical exact-name leaks, 0 high-risk title/phrase leaks, 6 medium-risk prompts, and 79 low-risk prompts.
- Current Step 5 scale result: PASS. The large condition is now 2349 skills: 85 controlled core, 1800 generated background-scale skills, 460 public imported background skills, and 4 support email skills. 460/460 public imports have downloaded original `SKILL.md` files.
- Current Step 6 public-skill field audit result: MOSTLY DONE. A 460/460 public-skill heuristic checkpoint has been generated, plus a 15-skill manual review packet. The DeepSeek `deepseek-v4-flash` model-assisted checkpoint has been run on the earlier 200-skill subset, producing `public_skill_field_model_audit.jsonl` and `public_skill_field_agreement_report.md`; a prioritized 50-case disagreement packet and pattern-level adjudication note are complete.
- Current Step 7 non-core semantic competition result: PASS useful pressure under TF-IDF fallback. A non-core skill is top-1 for `26/85` prompts and the best non-core skill scores above gold for `30/85` prompts. Previous MiniLM/embedding results remain historical/comparison evidence.
- Current Step 7 non-core procedural review result: PASS with caveat under TF-IDF fallback. `14/85` prompts have at least one non-core skill above gold. These cases need manual adjudication before final claims.
- Current Step 7 offline selector result: PASS useful pressure. On the 2349-skill condition, the rerun lexical/schema subset has strict top-1 accuracy of `68.2%` for M1 BM25 flat, `58.8%` for M1 TF-IDF flat, `76.5%` for M3 TF-IDF schema, `78.8%` for M6 BM25 -> schema rerank, and `74.1%` for M6 TF-IDF -> schema rerank. MiniLM methods remain 2089-scale/historical unless rerun.
- Current Step 7 field ablation result: DONE. On the 2349-skill condition, cumulative TF-IDF improves from 60.0% top-1 with description only to 84.7% with description + use conditions + preconditions + outputs + workflow; BM25 improves from 69.4% to 89.4% when workflow is included. Naive `not_for` and dependency/resource concatenation can hurt top-1, so these fields should be treated with field-aware scoring/reranking rather than appended as plain text.
- Historical 1006-scale Qwen provider result: PASS useful pressure. On the 1006-skill condition, Qwen `text-embedding-v4` reaches `35.8%` top-1 on R1 flat cards, `46.3%` on full `SKILL.md`, and `47.8%` on R2 structured cards. Qwen `qwen3-rerank` over top-20 improves these to `64.2%`, `61.2%`, and `65.7%` respectively. Qwen full-skill embeddings combined with the local schema reranker reach `68.7%` top-1 at top-20, `80.6%` at top-50, and `85.1%` at top-100. Use this only as historical comparison.
- Current 2089-scale Qwen update: Qwen full-skill embedding-only reaches `50.6%` top-1 and `69.4%` top-5; Qwen full-skill plus Qwen `qwen3-rerank` over top-20 reaches `63.5%` top-1 and `69.4%` top-5; Qwen full-skill plus local schema rerank reaches `80.0%` top-1 at top-50 and `84.7%` top-1 at top-100. R1/R2 Qwen variants remain historical 1006-scale unless rerun.
- Current low-information stress-test result: DONE separately. On 12 less-informative prompts, the best strict top-1 is `41.7%` for MiniLM full-skill embedding; Qwen full + local schema top-100 reaches `25.0%` top-1 and `66.7%` top-5. This should be reported as a robustness/limitation check, not folded into the main benchmark.
- Current strongest-method failure analysis: DONE. Qwen full-skill embedding plus local schema reranking over top-100 candidates has 10 strict top-1 failures: 4 first-stage exclusions and 6 reranker/boundary/annotation failures. The report is `thesis_notes/Failure Mode Analysis - Qwen Full Local Schema Top100.md`.
- Current scale-sensitivity read: PASS. Relative to core, M2a description-card MiniLM drops `-17.6` top-1 points and `-12.9` top-5 points; M1 TF-IDF flat drops `-16.5` top-1 points; M3 TF-IDF schema drops `-5.9` top-1 points; M6 MiniLM full -> schema rerank drops `-8.2` top-1 points but remains strongest at `82.3%` full-library top-1.
- Current Step 8 M0 result: historical core selection trace with cost caveat. The completed progressive-disclosure run covers the older 67-prompt/67-skill controlled core. M0 strict top-1 is `61.2%`, strict any-hit is `64.2%`, no explicit skill is loaded for `31.3%` of prompts, and the mean number of full skill docs loaded is `0.78`. The expanded 85-prompt core has not yet been run through M0.
- Current full-library M0 result: not run. Full progressive disclosure over 2349 skills should be treated as a context/cost stress test rather than a necessary first retrieval result.
- Current Step 9 downstream result: planned, not executed. The downstream sample, conditions, artifact rubric, and pass thresholds are recorded in `outputs/step8_downstream_validation_plan.md` under the old filename. The top-5 readiness check on the 12-prompt sample gives `91.7%` for M1 BM25 flat, `100.0%` for M1 TF-IDF flat, `83.3%` for M2b MiniLM full-skill, `91.7%` for M3 TF-IDF schema, `91.7%` for M6 BM25 -> schema rerank, `91.7%` for M6 TF-IDF -> schema rerank, and `91.7%` for M6 MiniLM full -> schema rerank. Execution should start with a small local dry run, then be repeated after stronger embedding/reranking methods are added.
- Remaining Step 3 weak confusability cases are mostly highly specific extraction/debugging/observability prompts where the gold skill is intentionally clearer than the alternatives.

Next refinement target:

- freeze the final representation-field taxonomy and final method set, then measure top-20/top-50/top-100 latency and cost before Step 9 downstream validation
