---
name: newsletter-growth
description: >-
  Designs and runs a newsletter as a compounding growth loop — not a broadcast
  and not SEO. Covers the subscribe→open→value→share loop, single-issue
  architecture (one idea, a lead that earns the open, a takeaway worth
  forwarding), subject/preview lines, where the subscribe and referral asks
  live, cadence and retention (open/reply/unsubscribe as signal), and the
  resource-entry → opinion content-mix sequence that builds a list then spends
  its attention. Use whenever someone wants to start or grow a newsletter,
  treat email as a growth channel, plan an issue or a launch sequence, lift open
  or subscribe rates, or design a newsletter subscribe/referral loop — including
  from a cold start with no list. Reads a VOICE-PRINT.md when present. For search
  as a channel use seo-content-strategy; for drafting craft use content-craft;
  this skill owns the newsletter as a growth system.
triggers:
  - /newsletter-growth
  - user wants to start, grow, or fix a newsletter
  - user treats email/newsletter as a growth channel
  - planning a newsletter issue, launch sequence, or subscribe/referral loop
  - open rate / subscribe rate / list growth is the problem
role: workflow
layer: growth
version: 1.0.0
sources:
  - "Reforge growth loops framework — loop (not funnel) design"
  - "Jobs-to-be-Done (Christensen) — why a reader subscribes and returns"
  - "growth-lifecycle-design (growth-skills v1.0, score 8/10) — behavior-triggered lifecycle"
borrowed_from: null
feeds:
  - pmm/content-review/SKILL.md
related:
  - pmm/voice-print/SKILL.md
  - pmm/ai-slop-audit/SKILL.md
  - pmm/seo-content-strategy/SKILL.md
  - foundations/shared-skills/content-craft/SKILL.md
  - growth/cold-start-motion/SKILL.md
  - growth/DOMAIN.md
---

# Newsletter Growth — Email as a Compounding Loop

## Purpose

Most "newsletter advice" is really drafting advice (how to write the issue) or SEO advice (how to get found). This skill is neither. It treats the newsletter as a **growth loop**: a system where each issue both delivers value *and* produces the next subscriber. The unit of work is the loop, not the post.

It exists because the default mental model — "write issues, email them out, hope the list grows" — is a broadcast, not a loop. A broadcast plateaus. A loop compounds, because every issue creates a reason and a mechanism for a reader to bring the next reader.

This skill owns the newsletter **as a growth system**. For the craft of drafting a long piece, use [content-craft](../../foundations/shared-skills/content-craft/SKILL.md); for search as an acquisition channel, use [seo-content-strategy](../../pmm/seo-content-strategy/SKILL.md); to make the writing sound like the author, use [voice-print](../../pmm/voice-print/SKILL.md) + [ai-slop-audit](../../pmm/ai-slop-audit/SKILL.md). They compose; this one decides the loop.

---

## Inputs

| Input | Required? | Description |
|-------|-----------|-------------|
| **Who it's for** | Required | The ICP / reader. "Anyone interested in X" is not enough — name the reader whose forward is worth more than a stranger's signup. |
| **The thesis / product it serves** | Required | What the newsletter is *for* — the worldview it advances or the product it feeds. A newsletter with no point can't earn a forward. |
| **Stage** | Required | List size + cadence today (zero / cold-start / growing / established). Decides whether this is a cold-start problem or a loop-optimization problem. |
| **Cadence capacity** | Required | Realistic issues per month the author can sustain. Over-promising cadence is the most common newsletter death. |
| **VOICE-PRINT.md** | Recommended | From [voice-print](../../pmm/voice-print/SKILL.md). Issues that don't sound like a person don't get forwarded. |
| **Brain context** | Optional | If `aether-growth-brain` is connected, read `knowledge/icp-map.md` for reader context and `channels/channel-history.md` for what's worked. |

### BLOCK rule

```
IF the reader (ICP) or the thesis is undefined:
  BLOCK. Return: "A newsletter loop needs a specific reader and a point. Tell me
  (1) who this is for — the person whose forward matters, and (2) what the
  newsletter is for — the worldview or product it advances. Without these,
  'grow the newsletter' is just 'send more email.'"
```

---

## Decision Logic

### Step 1 — Diagnose stage: cold-start vs. loop-optimization

```
IF list ≈ 0 / no repeatable subscriber source:
  This is a COLD-START problem first. The first ~100 subscribers are won by hand,
  not by a loop (see growth/cold-start-motion). The loop is what you graduate INTO.
  Do not design referral mechanics before you have readers who'd refer.

IF list is growing but flat or churny:
  This is a LOOP-OPTIMIZATION problem. Find which loop stage leaks
  (subscribe / open / value / share) and fix that stage — not "write better."
```

### Step 2 — Map the loop, find the leak

The newsletter growth loop has four stages; growth comes from closing it, and the leak is almost never where people look (they fix "writing" when the leak is "share"). Detail + diagnostics in [references/loop-and-issue.md](references/loop-and-issue.md).

```
SUBSCRIBE ── a reader joins (from an issue shared, a companion asset, a CTA)
    │
   OPEN ──── subject + preview earn the open (the only job of the subject line)
    │
  VALUE ──── the issue delivers one idea worth the reader's time
    │
  SHARE ──── the reader forwards / quotes / refers → produces the next SUBSCRIBE
    └────────────────────────────────────────────────────────────┘
```

Score each stage against benchmarks (Benchmarks section). Concentrate on the leaking stage. A 60% open rate with a 0% share rate is a broadcast with good subject lines — the loop is open.

### Step 3 — Issue architecture (one issue's job)

A single issue must do three things, in this order of priority: **earn the open**, **deliver one idea**, **be worth forwarding**. Full template in [references/loop-and-issue.md](references/loop-and-issue.md). Summary:

- **One idea per issue.** Not a digest of five. A reader can forward "the piece about X"; they can't forward "this week's roundup."
- **A lead that earns the open** within the first ~100 words — a specific scene, number, or claim, not a warm-up. (Cross-ref [content-review](../../pmm/content-review/SKILL.md) newsletter platform checks: lead with insight, no 3-paragraph warm-up, each section a standalone takeaway.)
- **A takeaway worth forwarding** — the reader should be able to say in one sentence why a peer needs this. That sentence is the share mechanism; if you can't write it, the issue won't spread.

### Step 4 — The content-mix sequence (build the list, then spend its attention)

Not every issue does the same job. Three archetypes, sequenced deliberately:

| Archetype | Job | When to lead with it |
|---|---|---|
| **Resource-entry** (a useful asset, guide, or tool the reader keeps) | Grows the list — high forward/save rate, low ask | Early / cold-start: build the list first |
| **Tutorial / how-to** | Builds trust and habit — demonstrates competence | Middle: convert attention into trust |
| **Opinion / thesis** | Spends attention — advances the worldview, the highest-value but highest-cost issue | After a list exists: spend the attention you built |

The sequencing rule: **lead with resource-entry to build the list, then spend that attention on opinion pieces.** A pure-manifesto cold start (opinion with no resource value, no audience yet) underperforms — open it with a hard asset, earn the right to the thesis later. (See Anti-patterns.)

### Step 5 — The subscribe + referral loop (close it deliberately)

- **Subscribe ask placement:** every issue is also an acquisition surface for non-subscribers who see it shared. The subscribe ask must be present and frictionless on the shared/public version — but never interrupt the value.
- **Companion / lead magnet:** a resource-entry asset (a guide, a pack, a checklist) is the highest-converting subscribe driver; tie it to the issue. (In the Aether family, a Fieldwork Recipe can be the companion — see `essay_links`/`companion` in the Recipe model.)
- **Referral:** only design referral mechanics once readers already share organically — instrument the organic share first, then lower its friction. Cash incentives attract the wrong reader; recognition and access work better for a quality list.

### Step 6 — Cadence & retention (read the real signals)

- **Cadence:** pick a cadence the author can sustain through a bad week. Consistency beats frequency. Missing sends trains the list to forget you.
- **Retention signals:** open rate (subject health), **reply rate** (the truest engagement signal — a reader who replies is a reader who shares), unsubscribe rate (a *content-fit* signal, not just loss — a spike after an issue is data about the issue).
- **Wrong-ICP guard:** a high open rate from the wrong reader is a vanity metric. Optimize for opens *from the ICP*, and treat replies/forwards from the ICP as the real north star.

---

## Outputs

```
## Newsletter Growth Plan — [name]

**Reader (ICP):** [the person whose forward matters]   **Thesis/serves:** [...]
**Stage:** [cold-start / growing / established]   **Cadence:** [sustainable rate]

### Loop diagnosis
[The 4-stage loop with each stage's current health + the identified leak.]

### Issue architecture
[One-idea template; lead pattern; the "worth-forwarding" one-sentence test.]

### Content-mix sequence
[Resource-entry / tutorial / opinion plan for the next N issues, sequenced.]

### Subscribe + referral loop
[Where the subscribe ask lives; the companion asset; referral plan or "not yet — instrument organic share first".]

### Cadence & success metrics
[Cadence; the ICP-weighted metrics to watch with targets; the wrong-ICP guard.]
```

Per-issue, the skill also produces a **pre-send checklist** (earns the open? one idea? forward-sentence exists? subscribe ask on the public version? sounds like the voice print?).

**Cross-review:** issue copy goes through [content-review](../../pmm/content-review/SKILL.md) (email/newsletter platform checks + brand voice) and, if AI-assisted, [ai-slop-audit](../../pmm/ai-slop-audit/SKILL.md) before send.

**Brain write (if connected):** append issue performance to `experiments/experiment-log.md`; skip silently if no brain.

---

## Cross-Review Triggers

**Before any issue ships (customer-facing copy):**
- [ ] [content-review](../../pmm/content-review/SKILL.md) — newsletter platform checks, banned-hype, brand voice
- [ ] [ai-slop-audit](../../pmm/ai-slop-audit/SKILL.md) — when the draft is AI-assisted

The growth *plan* itself is a strategy artifact (no blocking gate); the *issues* it produces are gated copy.

---

## Example Usage

### Example 1 — Cold-start newsletter, no list
**Input:** Solo founder, 0 subscribers, technical audience, can write biweekly.
**Output:** Diagnoses cold-start (not loop) → first ~100 by hand (points to cold-start-motion) → lead with resource-entry issues + a companion asset as the subscribe driver → defer referral mechanics. Cadence set to biweekly (sustainable). Metrics: ICP-weighted subscribes, reply rate.

### Example 2 — Flat list, good writing
**Input:** 2,000 subscribers, 55% open, list not growing.
**Output:** Loop diagnosis = SHARE stage leaks (good open, no forward mechanism). Fix: one idea per issue + an explicit forward-sentence per issue + subscribe ask on the public version. Not "write better" — the writing is fine; the loop is open.

### Example 3 — Manifesto-first cold start
**Input:** Founder wants issue #1 to be the big thesis, no list yet.
**Output:** Reframes: lead with a resource-entry hard asset to build the list; schedule the thesis for after a list exists. Names the trap (manifesto-with-no-audience underperforms) and why.

---

## Validation Criteria

**Output passes if:**
- [ ] Stage is diagnosed (cold-start vs loop-optimization) and the advice matches it
- [ ] The four-stage loop is mapped and the *specific leaking stage* is named (not "grow more")
- [ ] Issue architecture enforces one-idea + earns-the-open + a forward-sentence
- [ ] Content mix is sequenced (resource-entry → opinion), not uniform
- [ ] Subscribe loop placement is specified; referral is gated on organic-share evidence
- [ ] Cadence is sustainable; metrics are ICP-weighted (not raw opens)

**Output fails if:**
- [ ] It optimizes "writing quality" when the leak is the share/subscribe stage
- [ ] It designs referral mechanics for a list with no organic sharing yet
- [ ] It treats raw open rate as success regardless of who opens
- [ ] It recommends a cadence the author can't sustain

---

## Benchmarks

| Metric | Benchmark | Source |
|---|---|---|
| Newsletter open rate (engaged niche list) | 30–50% | growth/DOMAIN distribution norms (2025–2026) |
| Reply rate as engagement signal | any consistent reply flow = strong | Reforge loop framing |
| Subscribe→active retention (read 3 of first 5) | the real activation signal | growth-lifecycle-design |
| Median time for content/email loops to compound | months, not weeks | seo-content-strategy timeline lineage |


---

## References & Sources

**Tier-1 frameworks:**
- Reforge growth loops — loop-over-funnel; the subscribe→share closure
- Jobs-to-be-Done (Christensen) — why a reader subscribes and returns
- growth-lifecycle-design (growth-skills v1.0) — behavior-triggered retention

**Cross-references (this repo):**
- [references/loop-and-issue.md](references/loop-and-issue.md) — loop-stage diagnostics + issue template + content-mix detail
- [growth/cold-start-motion](../cold-start-motion/SKILL.md) — the first ~100 subscribers (cold-start graduates into this loop)
- [pmm/seo-content-strategy](../../pmm/seo-content-strategy/SKILL.md) — search channel (distinct); [content-craft](../../foundations/shared-skills/content-craft/SKILL.md) — drafting craft (distinct)
- [pmm/content-review](../../pmm/content-review/SKILL.md) + [pmm/ai-slop-audit](../../pmm/ai-slop-audit/SKILL.md) — issue gates

*Output metadata:*
```
---
Skill: newsletter-growth v1.0.0
Stage: [cold-start/growing/established]
Generated: [date]
---
```
