---
name: motion-slg
description: >-
  Designs or audits a Sales-Led Growth motion for a developer-first product:
  checks SLG readiness, maps the full deal anatomy, runs a sales enablement
  content gap analysis, designs the PLG-to-SLG handoff protocol, and checks
  pipeline health against benchmarks. Use when deciding whether to add SLG on
  top of PLG, building the sales motion from scratch, or diagnosing why the
  sales pipeline is stalling.
triggers:
  - /motion-slg
  - user wants to design or add a sales motion
  - user is deciding whether to hire salespeople or build a sales process
  - user wants to build sales enablement content
  - user wants to design the PLG to SLG handoff
  - user's sales pipeline is underperforming or stalling
  - user needs to build a business case or one-pager for enterprise buyers
role: workflow
version: 1.0.0
sources:
  - "growth-motion-slg (growth-skills v1.0, score 8/10)"
  - "growth-motion-plg (growth-skills v1.0, score 8.5/10)"
  - "b2b-practitioner-voice (growth-skills v1.0)"
feeds:
  - growth/motion-mlg
  - growth/funnel-audit
  - growth/growth-experiment
related:
  - growth/motion-plg
  - growth/motion-mlg
  - growth/funnel-audit
  - pmm/icp-research
  - pmm/positioning
---

# Motion: Sales-Led Growth (SLG)

## Contract

This skill guarantees:
- SLG is not recommended without passing the three-signal readiness check
- Deal anatomy is mapped for the specific product before enablement content is designed
- Enablement gap analysis covers every deal stage — no stage is skipped
- PLG→SLG handoff protocol is explicitly specified before any outreach begins
- Pipeline health is checked against benchmarks with actionable interpretation

---

**Role:** Sales Motion Architect. For developer-first products, SLG is not the starting motion — it is the up-market layer added when deals are large enough to justify a human sales cycle. This skill tells you when to add it, how to design it, and what content to build for it.

---

## Before starting

Confirm:
- **Product context** — what does the product do, what is the current GTM motion (PLG only, PLG+SLG, no motion yet)?
- **ICP card** — read `knowledge/icp-map.md` to identify both the IC champion profile and the economic buyer profile; SLG requires both
- **Experiment history** — read `experiments/experiment-log.md` to understand what outreach or sales tactics have been tried
- **Current pipeline data** — if auditing an existing SLG motion, gather conversion rates for each deal stage before starting

---

## Inputs

**Required before proceeding:**
- Product description and target market
- Whether SLG is being designed from scratch or an existing motion is being audited
- Current ACV range or deal size (even approximate)
- Whether a PLG or community motion already exists alongside SLG

**If ICP card is available:** use Core ICP segment to identify champion profile; use enterprise ICP layers to identify economic buyer profile.

---

## Step 1 — SLG Readiness Check

Three signals determine whether adding SLG is the right move. Evaluate each one.

```
Signal 1 — ACV threshold
  "Does deal size justify the cost and time of a human sales cycle?"
  
  The benchmark range for US/Western-market B2B SaaS is $20–40K ACV.
  
  PASS: Current or projected ACV is in range or above
  BORDERLINE: ACV is below range but deal complexity or buyer process requires sales
  NOT READY: ACV is well below range and buyer can self-serve through procurement
  
  Context: This range does not apply to: Japan or Southeast Asia markets (lower ACV
  norms, relationship-led sales); open-source or developer tools with services-based
  ACV; bundled pricing where ACV understates deal value. If your ACV is below range,
  evaluate sales ROI on pipeline velocity and close rate, not the threshold alone.
  
  Finding: [current or projected ACV] → [PASS / BORDERLINE / NOT READY]
  Rationale: [one sentence]

Signal 2 — Multi-stakeholder buying
  "Does the buying process require procurement, security, legal, or VP approval?"
  
  PASS: Deals require approval beyond the individual user (procurement, InfoSec,
        legal review, VP sign-off on budget)
  BORDERLINE: Some deals require multi-stakeholder approval; others self-close
  NOT READY: Individual contributor can purchase without approval; self-serve closes

  Finding: [description of buyer process] → [PASS / BORDERLINE / NOT READY]

Signal 3 — Enterprise usage signal
  "Are enterprise-domain users already appearing in self-serve or trial accounts?"
  
  PASS: Users from company domains matching enterprise ICP profile are using the
        product self-serve; PLG→SLG handoff signals are firing
  BORDERLINE: Some enterprise-domain signups but usage is shallow or one-off
  NOT READY: No enterprise-domain usage; only SMB or individual users in funnel
  
  Finding: [description of enterprise signal] → [PASS / BORDERLINE / NOT READY]
```

**SLG Readiness verdict:**
```
SLG Readiness: [READY / BORDERLINE — add with caution / NOT READY]

Signal 1 (ACV): [PASS/BORDERLINE/NOT READY] — [finding]
Signal 2 (Multi-stakeholder): [PASS/BORDERLINE/NOT READY] — [finding]
Signal 3 (Enterprise usage): [PASS/BORDERLINE/NOT READY] — [finding]

Recommended action: [proceed to design / add SLG to specific ICP segment only / 
                     delay until X condition is met]
```

---

## Step 2 — Deal Anatomy Mapping

Map the deal anatomy for the specific product before designing enablement content. Generic deal stages do not produce useful enablement gaps.

### Reference deal anatomy

See `growth/DOMAIN.md` for the standard developer-first deal anatomy (Champion → Technical Evaluation → Internal Advocacy → Business Case → Procurement/Security → Negotiation/Close → Onboarding/Expansion). Reference, do not duplicate.

### Product-specific deal anatomy worksheet

For each stage, answer the three questions:

```
Stage: Champion Identified
  How do champions currently enter the funnel?
    [Usage signal from PLG / inbound form / event / referral / outbound — specify]
  Who is the typical champion (role, seniority, team)?
    [e.g. "Senior backend engineer on infrastructure team"]
  What does the champion need to confirm before moving forward?
    [e.g. "That the product solves their specific technical problem better than X"]

Stage: Technical Evaluation
  How long does this stage typically last? [days/weeks]
  What does a successful POC or trial look like for this product?
    [e.g. "Champion runs X migration successfully in a test environment"]
  What are the top 3 technical objections or blockers at this stage?
    [list them]

Stage: Internal Advocacy
  Who does the champion present to? [manager / VP Eng / CTO / committee]
  What format does the champion use to present internally?
    [email forward / slide deck / Slack message / budget request form]
  What is the single most common reason internal advocacy stalls?
    [e.g. "Champion cannot articulate the ROI case" / "Security question comes up early"]

Stage: Business Case
  Who drives the business case — champion, sales rep, or both?
  What cost comparison is required? [vs current solution / vs build-it-yourself / vs alternatives]
  What proof does the economic buyer require?
    [customer references / case studies / ROI calculator / benchmark data]

Stage: Procurement / Security Review
  What security or compliance documents are typically requested?
    [SOC 2 / ISO 27001 / DPA / GDPR compliance / security questionnaire]
  Who conducts the security review on the buyer side?
    [InfoSec team / legal / procurement / all three]
  Average time spent in this stage: [weeks]

Stage: Negotiation and Close
  What typically gets negotiated? [price / contract length / SLA / support tier / custom terms]
  Who has authority to close on the buyer side? [procurement / CFO / VP / legal]
  Average time from proposal to signed contract: [weeks]
```

---

## Step 3 — Sales Enablement Content Gap Analysis

Using the deal anatomy from Step 2, identify what content exists and what is missing.

### Enablement gap matrix

For each stage, assess content status:

```
| Deal stage | Content needed | Exists? | Quality | Owner | Priority |
|---|---|---|---|---|---|
| Technical evaluation | Quickstart guide | [YES/NO/PARTIAL] | [Good/Needs work/--] | [role] | [High/Med/Low] |
| Technical evaluation | Architecture overview | [YES/NO/PARTIAL] | [Good/Needs work/--] | [role] | |
| Technical evaluation | Migration guide (from top alternatives) | [YES/NO/PARTIAL] | [Good/Needs work/--] | [role] | |
| Internal advocacy | One-page summary | [YES/NO/PARTIAL] | [Good/Needs work/--] | [role] | |
| Internal advocacy | Customer references (named) | [YES/NO/PARTIAL] | [Good/Needs work/--] | [role] | |
| Business case | ROI calculator or cost model | [YES/NO/PARTIAL] | [Good/Needs work/--] | [role] | |
| Business case | Comparison vs alternatives | [YES/NO/PARTIAL] | [Good/Needs work/--] | [role] | |
| Business case | Customer case study with named metrics | [YES/NO/PARTIAL] | [Good/Needs work/--] | [role] | |
| Procurement / security | Security overview document | [YES/NO/PARTIAL] | [Good/Needs work/--] | [role] | |
| Procurement / security | Data processing agreement | [YES/NO/PARTIAL] | [Good/Needs work/--] | [role] | |
| Procurement / security | Compliance FAQ (SOC 2, GDPR, etc.) | [YES/NO/PARTIAL] | [Good/Needs work/--] | [role] | |
| Negotiation | Pricing sheet | [YES/NO/PARTIAL] | [Good/Needs work/--] | [role] | |
```

### Priority build order

Build in this order (highest leverage first):
1. **One-page summary** — most under-invested; champions cannot advocate without it
2. **Security overview** — single most common procurement blocker; often kills deals that were otherwise closed
3. **Migration guide** — Technical Evaluation is the longest stage; reducing friction here shortens sales cycles
4. **ROI calculator** — required at Business Case; without it the champion cannot justify cost
5. **Customer case study** — requires a named reference; plan 4–8 weeks to produce

Note which items in your matrix are HIGH priority and missing. These are the immediate gaps to close.

---

## Step 4 — PLG→SLG Handoff Protocol Design

When a PLG signal triggers a sales touch, the handoff quality determines whether the warm account converts or churns.

### Handoff rules

```
Rule 1 — Timely
  Contact within 24–48 hours of signal firing.
  Enterprise evaluation windows are short. After 72 hours, the champion has
  moved on or found a workaround.

Rule 2 — Informed
  Sales rep knows the usage context before the first call.
  What the rep must have before reaching out:
    - Company name and domain
    - List of team members who have signed up
    - Features used and usage volume
    - Which handoff signal(s) fired
    - Time from signup to FVM (if instrumented)

Rule 3 — Low-friction
  First outreach acknowledges existing usage. Never ask them to restart the
  evaluation or schedule a generic demo. Reference what they have already built
  or tested.
```

### Handoff protocol spec

```
Handoff trigger(s) active for this product:
  [List signals from motion-plg Step 5 that are instrumented]

When signal fires, route to:
  [SDR / AE / founder — specify by deal size or company size]

Context package passed to sales:
  [ ] Company name and domain
  [ ] User names and roles (if known)
  [ ] Features used
  [ ] Usage volume vs tier limits
  [ ] Signal(s) that fired
  [ ] FVM achieved (YES/NO) and time to FVM

First outreach:
  Channel: [email / LinkedIn — specify]
  Sent by: [SDR / AE / founder]
  Tone: reference existing usage; acknowledge what they've built; offer specific help
  Template reference: growth/DOMAIN.md SLG section (outreach template)

CRM action on signal:
  [ ] Account created or matched
  [ ] Opportunity created with source = PLG signal
  [ ] Usage context logged on the opportunity
```

---

## Step 5 — Pipeline Health Check

If an SLG motion already exists, compare current conversion rates against benchmarks.

### Benchmark comparison

See `growth/DOMAIN.md` for the full pipeline benchmark table (MQL→SQL, SQL→Demo, Demo→Proposal, Proposal→Close, sales cycle length by segment). Reference, do not duplicate.

### Health check worksheet

```
| Stage | Your current rate | Benchmark range | Status | Interpretation |
|---|---|---|---|---|
| MQL → SQL | [%] | 15–25% | [Above/In/Below] | [one sentence] |
| SQL → Demo completed | [%] | 60–75% | [Above/In/Below] | [one sentence] |
| Demo → Proposal | [%] | 40–60% | [Above/In/Below] | [one sentence] |
| Proposal → Close | [%] | 25–40% | [Above/In/Below] | [one sentence] |
| Sales cycle (your segment) | [weeks] | 2–6 wk / 2–6 mo | [Shorter/In/Longer] | [one sentence] |
```

**Declining ratio interpretation:**
- MQL→SQL below range: ICP is drifting (wrong leads entering top of funnel) or SQL qualification criteria are too loose
- SQL→Demo below range: outreach quality or timing is poor; or wrong ICP at top of funnel
- Demo→Proposal below range: technical evaluation is failing; missing migration guide or architecture docs
- Proposal→Close below range: procurement or security stage is the blocker; missing security overview or ROI case

---

## Output format

Produce all three of the following at the end of the session:

### 1. SLG Readiness Verdict

```
## SLG Readiness Verdict

Product: [name]
Date: [date]

SLG Readiness: [READY / BORDERLINE / NOT READY]
  Signal 1 (ACV threshold): [PASS/BORDERLINE/NOT READY] — [finding]
  Signal 2 (Multi-stakeholder buying): [PASS/BORDERLINE/NOT READY] — [finding]
  Signal 3 (Enterprise usage signal): [PASS/BORDERLINE/NOT READY] — [finding]

Recommended action: [one sentence]
If BORDERLINE: specific condition to meet before full SLG investment — [condition]
```

### 2. Enablement Gap Matrix

Full matrix from Step 3 with priority column populated. Top 3 priority items called out explicitly with owner and target completion date.

### 3. Handoff Protocol Spec

```
## PLG→SLG Handoff Protocol

Triggers active: [list]
Route to: [role by deal size]
Time to first touch: [hours]
Context package: [checklist of what is passed]
First outreach format: [channel, tone, template reference]
CRM actions: [checklist]

Next step: /motion-mlg (if PLG and SLG are both active in same accounts)
```

---

## Brain reads / writes

**If a companion `aether-growth-brain` repo is connected:**

Before starting:
- Read `knowledge/icp-map.md` — identify champion profile (technical ICP) and economic buyer profile (enterprise ICP); both are required for deal anatomy mapping
- Read `experiments/experiment-log.md` — check what outreach or sales tactics have been tried; avoid repeating approaches with prior LOSS verdict

Brain write (when SLG design is finalized):
- Write SLG readiness verdict and handoff protocol to `decisions/motion-slg-design-[date].md`
- Note top 3 enablement gaps and owners in `decisions/enablement-gaps-[date].md`

**Brain not connected:** proceed; recommend saving the readiness verdict and handoff protocol locally as the authoritative record.

---

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Adding SLG because "we should have sales" | SLG has a real cost; below-threshold ACV means sales economics are negative | Run the three-signal readiness check; delay SLG until math works |
| Designing SLG without a champion profile | Sales motion designed for the wrong person; pitching to buyers before champions are ready | Map deal anatomy first; identify who the champion is before building outreach |
| Building a full content library before knowing the biggest gap | High effort, low leverage | Start with the one-page summary and security overview — these unblock more deals than any other content |
| First outreach ignores existing usage | Engineers see a generic sales email and disengage; trust is burned | Require informed handoff; sales must have usage context before first contact |
| Measuring pipeline health with total volume, not conversion rates | Volume hides ICP drift and stage-specific blockages | Track stage-by-stage conversion rates; compare to benchmarks quarterly |
| Running SLG against community without community buy-in | Aggressive sales outreach in developer communities destroys trust | Sequence: community trust first, sales touch only after warm signal |

---

## Validation criteria

- [ ] All three SLG readiness signals assessed with explicit verdict
- [ ] Deal anatomy mapped for the specific product (not just generic stages)
- [ ] Enablement gap matrix completed for all deal stages
- [ ] Top 3 priority content gaps identified with owners
- [ ] PLG→SLG handoff protocol specified with trigger, timing, context package, and outreach format
- [ ] Pipeline health checked against benchmarks (if existing motion)
- [ ] SLG readiness verdict produced
- [ ] Enablement gap matrix produced
- [ ] Handoff protocol spec produced

---

## References & Sources

**Tier 1:**
- growth-motion-slg (growth-skills v1.0, score 8/10): readiness signals, deal anatomy, enablement content priority, handoff rules, pipeline benchmarks
- growth-motion-plg (growth-skills v1.0, score 8.5/10): PLG→SLG handoff signal definitions and outreach template

**Tier 2 (via growth/DOMAIN.md):**
- Full deal anatomy diagram
- Pipeline benchmark table with ACV threshold context
- Outreach template for first sales touch
