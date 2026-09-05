# RQ2b Naturalistic Semantic-Confusability Extension Protocol

Date: 2026-08-31  
Status: **DISCOVERY AUTHORISED / NO NEW RQ2 RESULT / FINAL-FREEZE PATH ONLY**

## Decision and claim boundary

This protocol starts a new, source-grounded extension, `RQ2b-NC`, to make the eventual RQ2 library contain more genuinely confusable public-skill routing problems. It does **not** revise, pool with, or invalidate the completed V3 result. V3 remains the 2,433-candidate, 381-prompt strict-label corpus bound by `skill_benchmark/rq2b_full_library/rq2b-i3c-v3-2026-08-18/`.

The desired deliverable is one subsequently immutable **RQ2b-NC final library**, formed from the exact V3 base plus only the new public-original candidates and prompts that pass every gate below. “One final library” means a new named freeze with explicit parent hashes; it never means changing V3 rows or silently treating an RQ1 asset as a valid RQ2 label.

The final library has two explicitly tagged intake arms. `NC-P` adds newly
reviewed confusability prompts over candidates already in V3; it increases the
challenge-prompt set but never duplicates a V3 source row. `NC-S` imports a
new public-original candidate only after provenance, licence, cluster and
representation gates, then adds its newly reviewed prompts. Both arms use the
same final manifests and are reported separately as well as jointly where the
estimand permits.

The extension can strengthen the ecological relevance and difficulty of the retrieval test. It cannot by itself establish population representativeness, human task success, unique real-world routing correctness, or semantic completeness of automatic I3C extraction.

## Why RQ1 material is input, not direct RQ2 evidence

RQ1b was designed to test information-field recoverability and contains a large public-source frame plus curated candidate combinations. RQ2 tests retrieval/reranking against a frozen candidate library. Therefore an RQ1b source, cluster card, field card, prompt, or strict case may enter only as:

1. a *candidate-discovery lead*;
2. a byte-bound public-original source candidate; or
3. a proposed semantic-confusability cluster to be re-reviewed under this protocol.

It is not automatically an RQ2 gold label, an RQ2 prompt, an acceptable set, or a scored case. In particular, the 82-composition RQ1b final provenance registry includes historical and partial curation records; it is not 82 independent, complete RQ2 routing tasks.

An exact RQ1-to-V3 source reuse is eligible for `NC-P` cluster/prompt review
because the candidate is already in the base library. It is ineligible to add
another source row. A source absent from V3 is eligible only for `NC-S`
candidate-intake review.

## Inputs and provenance boundary

Discovery is initially local-only and may use these existing artefacts:

- `skill_benchmark/rq1b_final_public_corpus_v1/` — 82-composition provenance registry, used for leads only;
- `skill_benchmark/rq1b_naturalistic_public_replication/manifest/source_inventory.jsonl` — existing public-source inventory, used after identity and origin checks;
- `skill_benchmark/rq1b_cross_source_public_benchmark/` — pinned public originals and candidate packets, used only where its provenance gates pass;
- `skill_benchmark/rq1b_v3_public_source_frame/` — large source frame for later diversified discovery, not a random population sample; and
- V3's final merge, prompt preflight, and automatic-integrity artefacts under `skill_benchmark/rq2b_full_library/rq2b-i3c-v3-2026-08-18/`.

For every selected new candidate, the NC manifest must record: canonical source SHA-256; preserved local path; source bytes; source title and native description as observed; origin/repository; immutable commit or release reference where available; retrieval date where available; licence evidence or an explicit `unknown`; parent RQ1 record(s); and its relation to a V3 source hash (`new`, `exact_reuse`, or `same-origin-nonidentical`). A `main` URL alone is insufficient for an NC final candidate. Missing immutable provenance or a licence disposition blocks final inclusion rather than being silently filled.

The 1,800 deterministic `background_scale` V3 sources remain valid scale controls, but are not treated as public-natural cluster targets. New NC clusters are built from preserved public originals. Exact duplicates are retained only once in the final candidate library and may not form a cluster.

The first hash-canonical **planned final-library candidate-union preflight**
contained 3,070 unique source documents: 2,431 unique V3 source hashes plus
639 RQ1-only public source hashes. It was never the public-source discovery
universe. All 639 new records passed the local
original-byte, pinned-reference and captured-licence-file-hash check. This is
not an NC source admission or representation freeze: each still needs the
cluster/prompt-label and V3-equivalent representation gates. The V3 parent
duplicate aliases remain preserved in its historical manifest but are not
repeated as final candidates. Reviewed Wave 001 subsequently admitted six
additional exact-commit public originals supporting accepted prior-art and
pathway clusters; the current pre-freeze union is 3,076 unique source hashes.
RQ1-derived batch 001 subsequently admitted six missing pinned
Open-Legal-Products originals after source, import-metadata and licence hash
replay, extending the current pre-freeze union to 3,082 unique source hashes.
Two other pinned NC-S sources in that batch were already present and were not
duplicated. Batch 004 then added two fully pinned SEO originals, producing
3,084 sources. Batch 003 subsequently admitted ten fully pinned legal/tabular
originals after source, import-metadata and licence-hash replay, producing the
current 3,094-source union. Batch 002 and the RQ2-native business and technical
waves use sources already present in that union and add no duplicate rows.

The public-source discovery frame is separately reconciled. The frozen base
contains 29,292 source hashes; 25 standard amendments add 2,086 hash-unique
sources, producing a latest-chain `ACTIVE` frame of 31,378. Wave 24's 87
cleanly captured sources are retained as `QUARANTINE` because later cumulative
reports omit them; they are neither silently admitted nor discarded. After
excluding all 163 frozen-RQ1 member hashes and 18 additional prior NC lead or
review hashes, the current RQ2-native navigation universe is 31,197. The
earlier 29,120-row navigation is preserved only as a superseded base-frame
audit. Navigation is a reading frame, not a cluster, label, selector result or
population sample.

## Five gates

### 1. Discover candidates without choosing on a selector result

Two discovery lines are kept separate. In the `RQ1-transfer review` line, the
79 frozen RQ1 source memberships may be used as proposed leads, but every
source is reread and no RQ1 prompt, gold/acceptable label, field card, selector
output or result is transferred. In the `RQ2-native discovery` line, mining is
restricted to the reconciled active public-source frame after exact-hash
exclusion of every frozen-RQ1 member and prior NC lead/review source; RQ1
cluster cards and labels are not discovery inputs. The former 1,099-source
inventory remains a useful pinned subset, not the whole frame. A deterministic
lexical or embedding-neighbour queue is allowed only to prioritise reading; it
is not a semantic similarity score, gold-label generator, or retrieval result.
Both lines must retain rejected leads and their rejection category so that only
apparent successes are not preserved.

### 2. Confirm a bounded common envelope and genuine operational contrast

Each proposed cluster must contain independent first-route skills that address the same bounded user need. For every candidate pair, the card must state an operational distinction which would make that candidate inadequate for at least one neighbouring route. Reject a group containing a broad container and component, a prerequisite and downstream step, near-duplicate/fork, generic fallback and specialist, incompatible lifecycle stages, or merely a shared keyword/title. The target cluster size is three or four candidates; a pair is only a discovery lead.

### 3. Construct cue-safe prompts and labels independently

Prompts are written from a task vignette, not by copying a candidate title, repository, tool/vendor name, unique file path, or a label-bearing phrase. The prompt author may see the source card but must record a cue audit. A separate reviewer, blinded to the intended primary candidate where feasible, classifies every candidate as `fully_adequate`, `partially_adequate`, `inadequate`, or `unclear` for the prompt.

The primary strict stratum requires exactly one fully adequate candidate. If two or more candidates are fully adequate, the prompt may enter a separately frozen acceptable-set stratum with all such IDs recorded; it must never be forced into strict top-1 scoring. If no candidate is fully adequate, reject the prompt. No prompt is allowed to inherit V3's historical strict label or an RQ1 label without this review.

Singleton adequacy inside an authored cluster is only a local curation gate. It
does not prove that no source elsewhere in the 3,094-candidate union is also
fully adequate. Before final strict-gold freezing, every admitted prompt must
therefore pass an outcome-blind, retrieval-result-free alternative-candidate
discovery and acceptable-set adjudication step over the whole frozen library.
Any newly found fully adequate alternative moves the case to the acceptable-set
stratum or blocks it; it may not be ignored to preserve strict top-1 scoring.

### 4. Validate before freezing

| Gate | Required evidence | Failing disposition |
| --- | --- | --- |
| Provenance | byte hash, local original, pinned reference, origin and licence disposition | exclude from final library |
| Deduplication | source-hash and normalized-name checks against V3 and NC intake | retain one candidate or reject cluster |
| Cluster validity | source quotations supporting envelope and pairwise contrast | reject as nonparallel/overlapping |
| Prompt cue audit | literal overlap check plus reviewer statement | rewrite once, then reject if unresolved |
| Label coverage | candidate-by-candidate adequacy matrix and adjudication | strict/acceptable/reject as above |
| Split integrity | no same prompt, duplicate source, or transformed near-copy appears in more than one final split | remove/reassign before freeze |
| Representation integrity | V3-equivalent I1/I2/I3 extraction and automatic source/evidence/coverage checks for every new row | block freeze |

Independent review here is a curation-validity measure. Unless a subsequent approved human-annotation protocol is completed, it is not claimed to be a human-study result or inter-rater-reliability estimate.

### 5. Assemble, verify, then run once

Only after the four previous gates are complete may the builder materialise `RQ2b-NC-final-YYYY-MM-DD/`. It must contain:

- a parent-V3 identity and hash manifest;
- a source union manifest with the final candidate count and exact-reuse mapping;
- strict and acceptable-set prompt manifests, disjoint by construction;
- cluster cards, review/adjudication ledgers, source and licence evidence;
- I1, I2, I3-flat and I3C representations plus automatic integrity report; and
- frozen selectors/rerankers, predeclared analysis plan, and cost ledger.

The finaliser must fail closed on a missing source, hash mismatch, duplicate, unreviewed candidate, uncertain label, field-extraction failure, or prompt split leak. It must emit a single final manifest SHA-256 and a reproducibility command before any new retrieval/reranking execution is authorised. Existing V3 results remain separately reportable as the prior frozen benchmark; the NC run is a new final evaluation, not a retroactive edit.

## Current execution state

| Work item | State on 2026-08-31 |
| --- | --- |
| RQ1 lead inventory and V3 overlap audit | completed for all 79 frozen RQ1 clusters: 51 are existing-V3 prompt-only leads and 28 are new-source intake leads. Full-source rereview yields 45 prompt-authoring promotions, 10 defers and 24 rejects. After prompt authoring, rewrite and target-blinded review, batches 001–004 admit 38 clusters and 76 prompts in total; this is model-assisted curation evidence, not transferred RQ1 labels or final gold |
| RQ2-native discovery-frame reconciliation | latest-chain `ACTIVE` is 31,378 sources; Wave 24's 87 sources are quarantined; exact exclusion of 181 frozen-RQ1/prior-NC hashes leaves 31,197 navigation sources. All 31,465 active-plus-quarantine local files replay their recorded bytes and SHA-256 |
| Source-provenance and licence eligibility screening | 639/639 RQ1-only source candidates pass local byte/pin/licence-file preflight; strongest-binding audit finds 60/163 frozen-RQ1 sources with captured pin plus locally hash-verified licence and 6 with pinned declared-but-unverified licence; 97 legacy all-V3 sources still need an immutable-upstream provenance upgrade |
| Semantic cluster confirmation | Wave 001 admits pathway, prior-art, and peer-framework UI; legal and API are deferred and domain UI awaits licence evidence. RQ2-native business admits six complete clusters while competitive-intelligence/moat is deferred for unresolved source-example echo. RQ2-native technical admits nine clusters after full-source, prompt, singleton-adequacy, cue and optional-composition review |
| Cue-safe prompt construction and target-blinded adequacy review | the consolidated admission view contains 56 clusters and 129 prompts: Wave 001 3/9, native business 6/17, native technical 9/27, and RQ1-derived batches 001–004 at 10/20, 10/20, 5/10 and 13/26. A later full-source local acceptable-set audit supersedes the blanket singleton assumption: 125 remain `STRICT_LOCAL`, one becomes `ACCEPTABLE_SET_LOCAL`, and three are `BLOCK_NO_FULL`, leaving 126 locally admissible NC prompts. Two malformed placeholder descriptions enter remediation. These are still cluster-local, model-assisted decisions—not human annotation or evidence of unique adequacy across all 3,094 candidates |
| NC union build, I3 extraction, and automatic integrity freeze | the hash-unique planned candidate-library union progresses 3,070 → 3,076 → 3,082 → 3,084 → 3,094 after only fully pinned, admission-supporting source additions. The 31,197-row discovery navigation is deliberately not bulk-added. The single working ledger is `skill_benchmark/rq2b_naturalistic_confusability/manifests/current_pre_freeze_consolidated_2026-08-31/`; materialisation and new-row representation extraction are not started |
| Retrieval/reranking execution | not authorised by this protocol |

At the time of this protocol's creation, no NC source row, cluster, prompt, label, extraction, selector score, metric, or thesis claim existed. The later candidate-preflight and authoring-draft artefacts above remain non-final and do not alter that boundary.

## Reporting rule

The thesis will report V3 and NC as distinct frozen benchmarks unless an explicit final amendment establishes a valid pooled estimand and reports both strata. “More data” will be described as an enlarged, curated public-skill library, never as proof that all public skill libraries have the same distribution.
