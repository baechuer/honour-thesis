# RQ1b Naturalistic Public-Skill Replication Protocol

<!-- RQ1-RECORD-STATUS:START -->
> **RQ1 record status (2026-09-04): `HISTORICAL_OR_SUPERSEDED`.** Retained for provenance and method history. Do not use its dated status, denominator, or result as the current RQ1 claim unless the canonical RQ1 index explicitly carries it forward. Canonical index: `thesis_notes/current/RQ1/README.md`.
<!-- RQ1-RECORD-STATUS:END -->



Date: 2026-08-24  
Status: `WAVE 001 FROZEN / NATURAL_ORIGINAL_ONLY / NOT EXECUTED`

> **2026-08-28 active-method amendment.** This document continues to govern
> the provenance-preserved public-source pool, strict public cluster curation,
> source evidence, prompts, and natural-artifact label boundary. Its proposed
> original-document causal masking branch is superseded: naturally authored
> evidence is too jointly expressed for that to identify a field effect. The
> active intervention is the separately source-grounded, all-candidate
> field-type ablation protocol:
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b Public Field-Type Ablation Protocol - 2026-08-28.md`.
> This amendment creates no retrieval or selector result.

## 1. Purpose And Boundary

The formal RQ1 remains unchanged:

> Which operational information types help distinguish semantically similar but procedurally distinct agent skills?

RQ1a already provides the controlled answer: when sibling skills are deliberately tied outside one field, that field can resolve the ambiguity. RQ1b is an ecological replication, not a replacement for RQ1a and not a claim that any field is universally necessary in naturally authored documentation.

The existing 460-file public-original audit is supporting context only. It measures field prevalence and recoverability, not this replication, and must not be reported as a natural routing result.

RQ1c joint-field interaction is explicitly deferred until RQ1b has been reviewed with the user. No RQ1c data, clusters, or model runs are in scope here.

## 2. Research Question

Among semantically close skills represented by their original public artifacts, does documented evidence for a user-required operational constraint support selection of an independently adjudicated acceptable skill? In the subset where every differential cue for the declared field can be located and neutralised, does masking that field evidence reduce selection?

The two parts have different strength:

- Original-artifact selection is a naturalistic association test.
- Original-versus-masked selection is a causal field-evidence test only in mask-eligible clusters.

## 3. Source Population And Unit Of Analysis

- Source artifacts: preserved `SKILL.original.md` files only, from `skill_benchmark/skills/public_imported_background/<skill>/source/` and the separately staged `skill_benchmark/rq1b_naturalistic_public_replication/staged_sources/emmraan-agent-skills-1124ce40/skills/<skill>/source/` set. Do not use benchmark wrappers, generated RQ1a skills, I1/I2/I3 representations, or I3C extractions.
- Discovery source corpus: 1,099 preserved artifacts: the historical 460-file source set, 168 MIT-licensed Emmraan artifacts pinned to commit `1124ce406f47ba7c5c54e18c5f86f70ebd51c33d`, and 471 MIT-licensed Skill Me artifacts pinned to commit `a28c4ce9366b5a8540577bed8f70b6a60f8fde27`. The source inventory may contain historical exact-byte duplicates; staging a source does not make it an RQ1b cluster.
- Wave 002 source expansion is deliberately outside the Wave 001 source
  population and frozen manifest. It preserves an additional 432 original
  public `SKILL.md` files at pinned revisions across legal, scientific/clinical,
  finance, marketing, and education sources. Local source screening has
  yielded 17 `SOURCE_BACKED_DRAFT` cards and 8 rejections. All 17 now have two
  locally authored prompts and passed P1 literal/semantic prompt QA; no Wave
  002 card has an acceptable-set judgment, representation, or retrieval
  result. The discovery record is
  `skill_benchmark/rq1b_naturalistic_public_replication/manifest/wave_002_discovery_only_plan.md`,
  and the subsequent P0--P4 gate sequence is
  `skill_benchmark/rq1b_naturalistic_public_replication/manifest/wave_002_prompt_review_plan.md`.
- Cluster: two to four semantically close skills within a broad task family, with one declared primary operational field from the seven RQ1a fields.
- Candidate-discovery pool: seek 100 to 140 source-backed candidate clusters before applying the full quality gates.
- Final benchmark: at least 50 valid clusters. Expand toward 100 valid clusters only where the public corpus naturally supports the same source, semantic-neighbour, evidence, prompt, and independent-review standard; never manufacture a quota or rewrite a source artifact to fill one.
- Analysis unit: cluster. Multiple prompts per cluster improve measurement, but must not be treated as independent clusters.
- Final-cluster disjointness: a candidate skill may appear in at most one frozen final cluster. Discovery suggestions may overlap, but such families must be merged or rejected before freezing so cluster-level resampling is not inflated by repeated candidate artifacts.

## 4. Cluster Eligibility Gates

A candidate cluster enters the frozen study only if all gates pass:

1. Each candidate has a preserved original-source path and hash.
2. There are two to four original artifacts with a documented near-neighbour relationship, rather than a broad unrelated library search.
3. The declared target field has exact evidence spans in every candidate, including contrasting or absent evidence where relevant.
4. A task-like prompt can require the operational distinction without naming a skill heading or copying source evidence verbatim.
5. All residual occurrences of the target distinction in title, description, workflow, examples, and resources have been mapped.
6. Candidate construction and prompt writing occur before any retrieval result is viewed.
7. If residual differential evidence cannot be neutralised without changing the shared task, the cluster may be retained for original-artifact descriptive selection only. It is ineligible for the causal masking comparison.

## 5. Prompt, Label, And Review Protocol

Each valid cluster receives two task-like prompts: a direct operational request and an independently written paraphrase. Prompts must state the required object or constraint clearly but must not name the target field heading or reproduce distinctive source spans. A lexical-overlap audit records any unavoidable exact terminology.

Two blinded reviewers independently see the prompt and original candidate artifacts, but not the declared target field, model predictions, primary label, or cluster provenance. For each candidate they assign one of:

- `acceptable`: a skill that is appropriate to load first for the request;
- `plausible_but_insufficient`: related but missing a material required condition;
- `not_acceptable`: materially incompatible with the requested condition.

A third blinded adjudicator resolves disagreements. The primary label is the set of independently adjudicated `acceptable` candidates, not a single intended skill. A single intended label may be retained only as a descriptive secondary annotation.

## 6. Representations And Conditions

`natural_original` preserves each original artifact, aside from deterministic whitespace normalisation.

`target_evidence_masked` replaces only the pre-mapped target-evidence spans with neutral, length-controlled markers. It is permitted only for mask-eligible clusters. The residual-cue audit must pass before this condition is treated as a causal comparison.

RQ1b-1 does not create I1, I2, I3, I3-flat, or I3C representations. Those are RQ2 representation conditions and are out of scope.

## 7. Selectors And Metrics

After the data, prompts, review outcomes, eligibility status, and source hashes are frozen:

- BM25 is the local lexical selector.
- Qwen `text-embedding-v4` is the initial semantic selector. It requires a new explicit user approval before any original skill or prompt text leaves the workspace; document/query embeddings may then be locally cached.
- Direct-reasoner selection can be a diagnostic only, not the primary estimate.

Primary metric: cluster-level acceptable Hit@1. Secondary metrics: acceptable MRR, candidate-level reviewer agreement, original-versus-masked paired delta in mask-eligible clusters, and error taxonomy. Report direct and paraphrase prompts separately as well as combined, but use cluster-level resampling or paired summaries rather than treating prompt rows as independent observations.

## 8. Freeze, Stop, And Interpretation Rules

Freeze the manifest, source hashes, evidence spans, prompts, reviewer decisions, masking eligibility, and scoring configuration before retrieval is run. Keep RQ1a and RQ1b-1 estimates separate; never pool their results.

Minimum viable benchmark interpretation requires at least 50 valid clusters. Field-level comparisons need at least five naturally available clusters in a reported field and must be described as exploratory below ten clusters. Otherwise report a feasibility result rather than a field ranking.

A null, negative, or inconclusive result is still a valid result. If reviewer clarity is inadequate, revise the reviewer codebook and repeat only the review gate before any scoring. If residual target cues cannot be safely masked, retain the natural-original evidence but do not make a causal masking claim.

## 9. Planned Workspace

Working root: `skill_benchmark/rq1b_naturalistic_public_replication/`

- `README.md`: scope and non-execution boundary.
- `clusters/`: source-backed cluster packets after curation begins.
- `manifest/`: frozen identities, hashes, field evidence, and eligibility records.
- `review/`: anonymised review packets and adjudication outputs.
- `outputs/`: local retrieval and analysis outputs after a future execution approval.

## 10. Wave 001 Freeze Checkpoint

Local-only Wave 001 has frozen 62 source-disjoint clusters (129 distinct
original candidate artifacts) from the 113-card source-backed draft funnel.
Its frozen manifest is
`skill_benchmark/rq1b_naturalistic_public_replication/manifest/wave_001_frozen_manifest.jsonl`.
The freeze certificate verifies each preserved-source hash, zero candidate
reuse, 62 two-prompt packets, zero candidate-name matches, and zero copied
three- or four-token source phrases in the prompt audit.

Six internal Codex agents conducted two independent blinded reviews per packet
without source provenance, declared field, authoring primary, retrieval output,
or external tools. They agreed on the same singleton acceptable first skill for
both prompts in all 62 packets; raw local response tables are retained. This
is model-assisted curation evidence, not human annotation or a selector result.

Every cluster is `VALID_CLUSTER_ORIGINAL_ONLY`: the source evidence map finds
the relevant distinction distributed through multiple natural-document
surfaces. Thus this wave satisfies the protocol's minimum of 50 valid
natural-original clusters, but has zero mask-eligible clusters and cannot
answer the causal original-versus-masked part of Section 2. No BM25,
embedding, external transfer, API call, selector, or RQ1b retrieval result has
been run. Field counts are `use_condition` 17, `output_artifact` 20,
`dependency_resource` 6, `input_precondition` 7, `workflow_procedure` 6,
`boundary_not_for` 4, and `success_verification` 2; fields below five remain
exploratory.

## 11. Wave 002 Freeze Checkpoint

On 2026-08-25, a separate source-expansion pass preserved 432 original public
skill artifacts across five pinned repositories: 141 legal (`mike-workflows`),
71 individually MIT-licensed scientific/clinical (`scientific-agent-skills`),
5 finance (`UZI-Skill`), 50 marketing (`marketingskills`), and 165 education
(`education-agent-skills`, CC BY-SA 4.0). The source ledger and exact hashes
are in `skill_benchmark/rq1b_naturalistic_public_replication/staged_sources/`;
the provenance/status ledger is
`skill_benchmark/rq1b_naturalistic_public_replication/manifest/wave_002_public_source_prospects.md`.

The 25 Wave 002 family rows completed local source screening, recorded
in `review/BATCH_037_WAVE002_LEGAL_SOURCE_READING.md` through
`review/BATCH_040_WAVE002_EDUCATION_SOURCE_READING.md`: 17 were promoted to
separate `SOURCE_BACKED_DRAFT` cards and 8 were rejected as non-neighbours,
containment, or sequential composition. A source-backed draft has passed only
provenance, source reading, semantic-neighbour, provisional non-subsumption,
and exact-evidence checks. The 17 survivors then completed P0 authoring, final
P1 literal/semantic QA, blinded P2 acceptable-set review, P3 residual mapping,
and P4 freeze. `manifest/wave_002_frozen_manifest.jsonl` now contains 17
`VALID_CLUSTER_ORIGINAL_ONLY` pairs over 34 new candidate skills: zero
candidate reuse within Wave 002, zero candidate overlap with Wave 001, and 34
final prompts with zero candidate-name, title/short-line, or 3/4-token phrase
hits. The current P2 record is 34/34 model-assisted two-reviewer
agreed-singleton decisions with zero adjudications; C003, C011, and C014 use
the replacement R1 reviews after prompt revision.

Every Wave 002 pair remains `ORIGINAL_ONLY`, because the natural operational
distinction is repeated through several artifact carriers. Wave 002 therefore
extends the frozen natural-original pool to 79 separately versioned clusters,
but does not alter Wave 001 and cannot support a causal field-mask comparison.
No Wave 002 document has been sent to a selector, model, API, or external
service; no representation, score, or retrieval result exists. The local
evidence and execution boundary are fixed by
`manifest/wave_002_freeze_certificate.json` and
`manifest/wave_002_prompt_review_plan.md`.

## 12. Wave 003 Mass Candidate-Pool Discovery

Wave 003 has started as a separate provenance-preserving discovery pass with a
target of at least 500 **net-new source artifacts**, not 500 valid clusters.
It cannot modify the independently frozen Wave 001 or Wave 002 manifests. Its
fixed D0--D4 gates require original-artifact provenance, licence and pinned
revision evidence, exact-byte duplicate screening, domain/source accounting,
and later manual family screening before any P0--P4 curation begins. No Wave
003 prompt, label, representation, selector, model call, or retrieval result
is authorised at this stage. The operational plan is
`skill_benchmark/rq1b_naturalistic_public_replication/manifest/wave_003_mass_candidate_pool_plan.md`.

On 2026-08-25, its D0--D3 gates completed locally: nine direct, licensed,
pinned sources yielded 573 preserved source files. The canonical D3 audit
recomputed every staged SHA-256, found zero overlap with the pre-Wave-003
source corpus, retained but excluded 57 within-Wave exact-byte duplicates, and
therefore established a pool of 516 net-new exact-byte-distinct original
artifacts. ThomasMore's otherwise domain-concentrated legal source was limited
to a deterministic 100-file jurisdiction/practice-stratified selection; it was
not used to create a semantic cluster. The pool meets the source-volume target
only. D4a has now revalidated the 516 canonical staged originals and recorded
only their source-provided front-matter navigation metadata and headings in
`manifest/wave_003_d4a_source_navigation_inventory.jsonl`. This is not a
semantic grouping: D4b's first `UNSCREENED_NOT_A_CLUSTER` reading queue is
separate. Its completed initial D4c source-reading queue promoted nine
`SOURCE_BACKED_DRAFT` cards and rejected five families for containment,
complementarity, interface-only distinction, or non-neighbour relation. The
remaining source pool must still establish same-task envelope, non-subsumption,
and plausible operational distinction before any P0--P4 curation. Thus Wave 003
still has no valid clusters, prompts, acceptable-set labels, selector input,
external transfer, or retrieval result.

The second D4b queue is recorded separately in
`manifest/wave_003_second_source_reading_queue.md`. Its complete eleven-family
full-source decision set added five further `SOURCE_BACKED_DRAFT` cards and six
rejections. The cumulative source-screening count is therefore fourteen drafts
and eleven rejections; this is still discovery evidence only, and none has
entered P0--P4.

The twelve metadata-selected navigation proposals in
`manifest/wave_003_third_source_reading_queue.md` have all completed
full-source D4c. The first four were rejected for duplicate/contained scope or
subsystem/prerequisite relation; the next four added three
`SOURCE_BACKED_DRAFT`s and one resource-management rejection; the final four
added two drafts and rejected a generic-to-specialised containment pair plus a
pointer-only/subsystem-risk pair. These are not semantic families or benchmark
entries. The current Wave 003 source-screen count is nineteen drafts and
eighteen rejections; every promoted draft still requires P0--P4 before it can
become a valid cluster.

The twelve navigation proposals in
`manifest/wave_003_fourth_source_reading_queue.md` have all completed
full-source D4c. Seven became `SOURCE_BACKED_DRAFT`s; five were rejected for
contained/subcomponent scope, an explicit prerequisite relation, a
non-neighbour training-family relation, or sequential composition. The current
Wave 003 source-screen count is twenty-six drafts and twenty-three rejections,
and every promoted draft still requires P0--P4 before it can become a valid
cluster.

The next twelve source-metadata navigation proposals are recorded in
`manifest/wave_003_fifth_source_reading_queue.md`. Its complete D4c screen
added five `SOURCE_BACKED_DRAFT`s and rejected platform specialisation,
general-review subsumption, bidirectional overlap, orthogonal/composable
properties, explicit specialised routing, model-selection followed by a
feasibility check, and prelaunch-versus-active-failure work. The current Wave
003 source-screen count is thirty-one drafts and thirty rejections. D4c may
only read the original artifacts and record individual promote-or-reject
decisions. It does not
authorise prompts, labels, representations, selector inputs, model calls,
external transfer, or results.

`manifest/wave_003_sixth_source_reading_queue.md` is a D4b navigation-only
queue of twelve previously unused source pairs. It has no D4c decisions and
does not change the current source-screen count.

## 13. RQ1b Multi-Neighbour Expansion Amendment

On 2026-08-25, the study added a separately versioned, local-only E1 amendment
to address the limited multi-neighbour coverage of the frozen naturalistic
data. Wave 001 contains 57 pairs and five natural triplets; Wave 002 contains
17 pairs. The amendment first audits the 74 frozen pairs for a third real,
unfrozen public near neighbour, without changing either frozen manifest.

Each passing E1 item is a parallel three-candidate packet. Its existing direct
and paraphrase prompts are first retained unchanged, then re-audited against
all three sources and independently reviewed for an acceptable set. An
expansion fails if the third candidate is a container, prerequisite,
subsequent/composable operation, interface-only variation, or if it makes an
unchanged prompt multi-acceptable or unstable. The old pair remains frozen and
valid when this happens; no prompt may be rewritten merely to reject the third
candidate.

E1 remains a natural-original association/robustness study. It cannot identify
the causal effect of a single operational field because those facts recur
across natural artefact surfaces. The full T0--T5 requirements, scale gate,
and no-retrieval boundary are recorded in
`skill_benchmark/rq1b_naturalistic_public_replication/manifest/rq1b_multi_neighbour_expansion_plan.md`.
After the targeted Wave 001/002 audit, Wave 003 D4 prioritises native triplet
families over new pair-only discovery. No E1 or Wave 003 selector, embedding,
API, text-transfer, scoring, or empirical result has been authorised.
