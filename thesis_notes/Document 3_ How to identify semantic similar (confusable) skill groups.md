Yes. The right move now is to start identifying **confusable skill groups**.

But use public skills only as **seeds**. For a strong benchmark, you will probably need to **author or normalize your own final groups**, because public skill repositories are useful for realism but rarely give perfectly controlled “same meaning on the surface, different procedure underneath” pairs. Anthropic’s public repo shows that skills are packaged as folders with `SKILL.md` plus resources, and examples span document processing, web testing, MCP generation, branding, and other workflows. Public skill ecosystems also explicitly surface domains like PR review, changelog creation, React performance, document work, and meta-skills for finding/managing skills.

## **What should count as “semantically similar but different”?**

Use this definition:

Two skills are **semantically similar** if, from the perspective of the selector, their **name, description, trigger phrases, or opening SKILL.md content overlap strongly enough that a flat text retriever or LLM could plausibly confuse them**.

They are **procedurally different** if the correct execution differs in one or more of these ways:

* required preconditions,  
* tools or commands used,  
* input artifact type,  
* output artifact type,  
* action sequence,  
* side effects,  
* scope,  
* verification criteria.

That is the characterization you want.

So not every difference counts.  
 For your thesis, the difference should be one that can **change agent behavior or outcome** if the wrong skill is chosen.

## **A practical characterization rule**

A pair belongs in your benchmark if all three are true:

1. **Surface overlap is high**  
    Their metadata or introductory text looks similar.  
2. **Correct procedure is meaningfully different**  
    The agent should do something different, not just say the same thing in a different style.  
3. **Wrong selection is costly**  
    Choosing the wrong skill would produce a different artifact, use the wrong toolchain, miss required checks, or otherwise harm task success.

That third criterion is important. It keeps the benchmark from becoming superficial.

---

# **Candidate public-seed skill groups**

Below are good **starting groups**, grounded in public skill ecosystems, but you should treat them as **seed templates** and likely rewrite them into controlled benchmark skills.

## **Group 1: Code review vs PR review vs review-comment resolution**

Public ecosystems clearly include PR review skills and code review skills.

Why they are semantically similar:

* descriptions often include “review,” “feedback,” “pull request,” “code quality”  
* a user query like “review this PR” or “check my changes” can plausibly activate multiple skills

Why they are procedurally different:

* **code review**: inspect correctness, security, readability, conventions  
* **PR review**: incorporate diff context, commit history, merge risk, reviewer expectations  
* **review-comment resolution**: address existing comments one by one, possibly iteratively and resumably

Why wrong selection matters:

* a generic code review skill may not resolve review threads  
* a comment-resolution workflow may be wrong when no review comments exist  
* a PR-focused workflow may over-assume GitHub/PR context

This is an excellent benchmark family because surface language overlaps heavily, but procedure and context differ.

## **Group 2: Changelog drafting vs release workflow vs patch-release procedure**

Public skills explicitly use “changelog” as a search example, and there are real release-procedure skills that include drafting changelog entries plus tagging and PR steps.

Why they are semantically similar:

* all mention “release,” “changelog,” “notes,” “version,” “update”

Why they are procedurally different:

* **changelog drafting**: summarize user-facing changes  
* **release workflow**: version bump, tagging, packaging, publishing  
* **patch-release procedure**: branch-specific release steps, tagging, follow-up PRs, controller-specific release process

Why wrong selection matters:

* drafting text is not enough for an actual release  
* release procedure may be too destructive/heavy when user only wants notes  
* wrong branching or tagging procedure can be operationally harmful

This family is strong because the metadata overlap is high but the operational consequences differ sharply.

## **Group 3: PDF processing vs general document processing vs presentation processing**

Anthropic’s public skills include dedicated PDF and PPTX skills, and public repos also expose broader “working with documents” skills.

Why they are semantically similar:

* all mention “document,” “extract,” “convert,” “create,” “edit,” “format”

Why they are procedurally different:

* **PDF processing**: OCR, form filling, merging/splitting, watermarks, encryption, image extraction  
* **presentation/PPTX**: slide creation/editing rather than page-oriented PDF operations  
* **general document workflow**: format conversion, broader office-document handling

Why wrong selection matters:

* choosing PPTX when the task is PDF form extraction is wrong  
* choosing general document conversion when the task is OCR or PDF forms is too weak  
* output artifact type changes

This is a very natural artifact-type confusion family.

## **Group 4: Find-skills vs skill-management vs skill-creation/meta-skill**

Public ecosystems include find-skills, skill managers, and skill creators/meta-skill creators.

Why they are semantically similar:

* all mention “skills,” “create/manage/find/install/update”

Why they are procedurally different:

* **find-skills**: search ecosystem and recommend installable skills  
* **skill-management**: audit/validate/update installed skills  
* **skill-creator/meta-skill-creator**: author a new skill from requirements

Why wrong selection matters:

* recommending an existing skill is different from creating a new one  
* updating installed skills is different from finding external skills  
* these can look very similar in descriptions because they all concern “skills”

This is useful because it isolates conceptual confusion rather than file-type confusion.

## **Group 5: React performance vs frontend optimization vs web app testing**

Public skill search examples explicitly mention “react performance,” and Anthropic’s repo mentions testing web apps as a skill domain.

Why they are semantically similar:

* all may mention “app,” “performance,” “frontend,” “quality,” “improve”

Why they are procedurally different:

* **React performance**: rendering, memoization, bundle, state updates  
* **frontend optimization**: possibly broader design/runtime/web delivery concerns  
* **web app testing**: verification and bug detection, not optimization

Why wrong selection matters:

* testing does not optimize performance  
* performance tuning may skip validation workflow  
* broader frontend skill may be too diffuse

This family is useful, though you may need to author the final controlled variants yourself.

---

# **My recommendation: use “controlled confusable clusters”**

Do **not** rely purely on raw public skills.

Instead, create **controlled clusters** like this:

### **Cluster template**

* one shared user-facing intent theme  
* 3–4 skills with highly overlapping metadata  
* each differs on one major procedural axis

Example:

**Shared theme:** “review code changes”

* `code-review` — review correctness/security/readability  
* `pr-review` — review PR in repository/merge context  
* `review-comment-resolution` — address existing PR review comments  
* `release-readiness-review` — verify release blockers/checklist before merge

These will be much better benchmark units than uncurated public skills.

---

# **How to test whether your skills are actually semantically similar**

Use a two-part test: **surface similarity** and **procedural divergence**.

## **Part A: Surface similarity test**

Measure similarity on the representations the selector would actually see.

Do this separately for:

* **metadata only**: `name + description`  
* **header-only SKILL.md**: first section / when-to-use  
* **full SKILL.md** if that is a representation variant in your thesis

Ways to test:

* cosine similarity over embeddings  
* lexical overlap/Jaccard on key phrases  
* LLM judgment: “Would these two skill descriptions appear to solve the same kind of user request?”

A benchmark pair/group should score **high** on at least one of those surface-similarity measures.

## **Part B: Procedural divergence test**

Then annotate whether they differ on these axes:

* preconditions  
* required tools  
* input artifact/environment  
* output artifact  
* workflow steps  
* side effects  
* verification/success criteria

For each skill pair, mark how many axes differ.

A good benchmark pair should have:

* **high surface similarity**  
* **high procedural divergence**

That is the core combination you want.

---

# **How to test whether the difference actually impacts the agent**

This is the most important part.

A pair is useful only if wrong selection changes behavior in a meaningful way.

Use three levels of impact testing.

## **Level 1: Retrieval confusion test**

Given a query, does the method rank the wrong skill above the correct one?

Metrics:

* top-1 accuracy  
* top-k recall  
* MRR / NDCG if you want ranking detail

## **Level 2: Workflow divergence test**

After retrieval, inspect whether the selected skill causes a different workflow.

For example:

* wrong commands  
* wrong file format  
* wrong environment assumptions  
* missing safety checks  
* wrong artifact produced

You can score this manually or with rubric-based annotation.

## **Level 3: Downstream task impact test**

Actually run or simulate the task.

Examples:

* wrong review skill produces generic comments instead of resolving review threads  
* wrong changelog/release skill drafts notes but does not perform release steps  
* wrong document skill produces PPTX logic for a PDF form task

Metrics:

* task success / failure  
* completeness  
* correctness of produced artifact  
* human or rubric-based quality score  
* token/context cost  
* latency

This is how you show the difference matters to agents, not just to retrieval metrics.

---

# **A concrete acceptance rule for benchmark groups**

I would use this rule for each cluster you include:

A cluster is accepted if:

* metadata similarity is high,  
* at least one pair in the cluster is topically confusable for a flat retriever,  
* procedural divergence exists on at least 2–3 important axes,  
* wrong skill choice produces observable downstream degradation.

That gives you a principled benchmark filter.

---

# **Suggested annotation sheet for each skill**

For every skill in your pilot library, record:

* skill name  
* short description  
* typical user query triggers  
* visible representation variant(s): metadata / header / full skill  
* required tools  
* preconditions  
* inputs  
* outputs  
* side effects  
* core workflow steps  
* success criteria  
* nearest confusable neighbors  
* why they are confusable  
* why they differ procedurally  
* expected consequence of wrong selection

This will make your later evaluation much cleaner.

---

# **Best immediate next step**

Build **5–10 confusable clusters**, each with **3–4 skills**.

Start with these families:

* code review / PR review / review-comment resolution  
* changelog / release / patch-release workflow  
* PDF / document / presentation processing  
* find-skill / manage-skill / create-skill  
* React performance / frontend optimization / web testing

Use public skills as inspiration, but normalize them into controlled benchmark skills.

That gives you enough material to:

* sharpen the literature review,  
* define “semantic similarity” operationally,  
* and later scale the library by adding paraphrases, variants, and distractors.

If you want, next I can turn this into a **pasteable benchmark design template** with a table format for clusters, annotations, and scoring.

