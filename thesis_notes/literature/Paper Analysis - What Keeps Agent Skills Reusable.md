# Paper Analysis: What Keeps Agent Skills from Being Reusable?

Date: 2026-05-28

Paper:

Chi Zhang, Ping Ji, Xinze Chen, and Yimin Liu. "What Keeps Agent Skills from Being Reusable? Evidence from 138K SKILL.md Files." Agent Skills '26, ACM CAIS workshop, 2026.

Links:

- OpenReview: https://openreview.net/forum?id=n0AIlfxDU0
- PDF: https://openreview.net/pdf?id=n0AIlfxDU0

## Credibility

This is not just a blog post. It is listed as an Agent Skills '26 poster at the ACM CAIS workshop. Treat it as workshop-reviewed / conference-adjacent evidence, but do not call it a full archival conference paper unless proceedings status is confirmed.

The paper is very useful because it studies public skill artifacts directly, at ecosystem scale. It is currently one of the strongest external supports for the claim that real skills contain reusable structure beyond name and description.

## Core Problem

The paper asks why public `SKILL.md` files often fail to become reusable agent capabilities.

Its central argument is:

- A reusable skill is not just a saved prompt.
- A reusable skill must be routable, loadable, actionable, resource-organized, safe, portable, and scoped.
- Many public skills fail because they are serialized from one task, repository, or conversation rather than designed as reusable components.

This maps strongly onto our thesis because we study skill retrieval before full skill loading. Their work asks whether skill files are reusable. Our work asks which parts of those skill files should be preserved in the selection representation.

## Research Questions In The Paper

The paper studies:

1. What reusability defects are prevalent in public skills?
2. How do these defects limit skill reuse?
3. Which platform and provenance signals are associated with reusable skill quality?
4. What traits characterize reusable, high-quality Agent Skills?

This is broader than our thesis. It covers ecosystem quality, safety, portability, and generation workflows. Our scope is narrower: retrieval and representation for semantically similar skills.

## Dataset

The paper analyzes:

- 138,133 public `SKILL.md` files.
- 20,556 repositories.
- Sources include public GitHub and the `agentskills.in` registry.

This is far larger than our current benchmark. We should not compete with this scale. Instead, we should use it as justification that ecosystem-scale skill quality is a real problem and then position our benchmark as a controlled retrieval study.

## Taxonomy

The paper proposes a two-tier taxonomy:

- 7 high-level categories.
- 31 checks.

The main categories are:

1. Routing metadata.
2. Body design.
3. Resource organization.
4. Prohibited content.
5. Behavioral safety.
6. Portability.
7. Persona and scope.

This taxonomy is not identical to ours, but it strongly supports several of our representation fields:

| Their category | Our corresponding representation concern |
|---|---|
| Routing metadata | name, description, use case, trigger conditions |
| Body design | workflow/procedure, actionable steps, body length/context cost |
| Resource organization | scripts, references, assets, external resources |
| Prohibited content | irrelevant content, changelogs, install notes, context waste |
| Behavioral safety | constraints, side effects, unsafe actions |
| Portability | dependencies, environment assumptions, tool/platform requirements |
| Persona and scope | skill boundaries, not-for conditions, role/scope mismatch |

This is important: our schema fields are not arbitrary. They are grounded in external evidence about what makes skills reusable.

## Main Findings

The headline finding is severe:

- 91.8% of public skills contain at least one detected defect under the authors' baseline detector.
- The estimate remains stable under lenient and strict thresholds.
- The dominant problems are ordinary packaging/reuse defects, not only exotic security issues.

The most thesis-relevant defects are:

- weak routing metadata
- bloated or non-actionable bodies
- poor resource organization
- portability issues
- safety/scope conflicts

The paper also runs a deterministic routing stress test over 20,000 sampled skills. Skills with clean routing metadata are retrieved more reliably from startup descriptions than skills with routing defects.

This directly supports our progressive-disclosure critique: if the startup-visible description is weak, the agent may never load the full skill body.

## High-Quality Skill Traits

The paper identifies high-quality examples with two styles:

- minimal and precise
- structured workflow

Shared traits include:

- trigger-complete descriptions, often containing a "Use when" style activation condition
- imperative/actionable body text
- project-specific procedural knowledge rather than generic tutorial content
- little context waste
- no prohibited or irrelevant content

For our thesis, the most important trait is project-specific procedural knowledge. This suggests that useful retrieval representations must preserve more than topical keywords. They need to preserve the concrete procedure, boundary, resource, or environment assumption that makes a skill suitable.

## Authoring Guidelines

The paper derives 12 guidelines. The visible high-level implications are:

- descriptions should be routable and front-load the use case
- routing information should appear in the description, not only deep in the body
- body text should be actionable rather than explanatory filler
- resource organization matters for progressive disclosure
- safety and portability gates are needed before reuse

This gives us a strong bridge from "skill quality" to "retrieval representation":

- If routing metadata is weak, flat metadata retrieval fails.
- If useful information is only in the body/resources, full-body or structure-aware retrieval may help.
- If skills contain bloat/noise, full-body embeddings may also be distracted.
- If dependencies/resources matter, dependency-aware representations should help in some clusters.

## Limitations

The paper is careful about limitations:

- Some detected defects may be intentional design choices.
- Dataset is limited to public GitHub and `agentskills.in`; enterprise/private skills may differ.
- Top repositories contribute a large share of the corpus.
- Platform attribution is approximate.
- Detection rules depend on the current version of the evolving skill specification.
- Some safety-critical detector precision still needs manual audit.

These limitations actually help our thesis framing. They show why we should not simply import their taxonomy as ground truth. We can use it as a literature-grounded starting point, then test representation choices in a controlled benchmark.

## How This Helps Our Thesis

This paper answers a different question from ours:

- Their question: what makes public skills reusable or defective?
- Our question: what information should retrieval representations preserve to select the correct skill among semantically similar skills?

So our thesis novelty remains intact.

We can use their paper to justify:

1. Real skills have quality-relevant structure beyond names and descriptions.
2. Routing metadata is functionally important.
3. Skill bodies/resources can contain important procedural information.
4. Resource organization, portability, and scope boundaries matter for reuse.
5. Public skills are noisy, so retrieval must handle both semantic overlap and artifact-quality variation.

## How To Cite In Our Literature Review

Suggested wording:

> Recent ecosystem-scale work on public `SKILL.md` artifacts shows that reusable agent skills depend on more than valid frontmatter. Zhang et al. analyze 138,133 public skills and identify defects across routing metadata, body design, resource organization, safety, portability, and scope. Their routing stress test further suggests that clean activation metadata improves discoverability. This supports the need to treat skill representation as a retrieval-critical design problem, rather than assuming that name and description fields are sufficient.

Then connect to gap:

> However, their study diagnoses public skill quality, whereas this thesis evaluates how different representation choices affect retrieval among semantically similar but procedurally different skills.

## Impact On Our Design

The paper suggests our current representation classes are sensible:

- R1 flat metadata maps to routing metadata.
- R2 structured procedural representation maps to body design, actionability, scope, and procedure.
- R3 dependency/resource-aware representation maps to resource organization, portability, and external assumptions.
- R4 graph representation can model resource/dependency/scope relations.

It also warns us:

- Full-body retrieval can help, but only if the body is not bloated or noisy.
- Metadata-only retrieval is vulnerable when routing descriptions are weak.
- `not_for` and persona/scope fields are important but difficult because they can introduce negation and object-confusion.
- Resource/dependency signals should not be assumed useful everywhere; they matter most when task feasibility depends on tools, files, platform, or external systems.

## Thesis Takeaway

This paper should become one of the backbone citations for the representation design section.

The clean thesis positioning is:

> Prior ecosystem studies identify what makes skills reusable. This thesis operationalizes those insights as retrieval representations and tests whether preserving such information improves selection under semantic confusion and scale.

