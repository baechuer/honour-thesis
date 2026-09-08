---
name: motion-mlg
description: >-
  Coordinates a Mixed/Multi-Led Growth motion when PLG and SLG are both active
  in the same accounts: detects MLG territory, maps the account duality between
  IC champions and economic buyers, designs a "one story, two frames" content
  strategy, defines handoff signals, and resolves the organizational tension
  between product-led and sales-led teams. Use when PQL-to-close rate is below
  40%, when IC usage and enterprise deal motion are creating friction, or when
  self-serve and enterprise motions need to compound rather than conflict.
triggers:
  - /motion-mlg
  - user has both PLG and SLG active and they are in conflict
  - PQL to close rate is below 40%
  - sales is contacting self-serve users too early or too late
  - IC usage exists in accounts where sales is also working a deal
  - user needs to design content for both engineers and buyers simultaneously
  - product and sales teams are creating friction over the same accounts
role: workflow
version: 1.0.0
sources:
  - "growth-motion-mlg (growth-skills v1.0, score 7.5/10)"
  - "growth-motion-plg (growth-skills v1.0, score 8.5/10)"
  - "growth-motion-slg (growth-skills v1.0, score 8/10)"
feeds:
  - growth/growth-experiment
  - growth/funnel-audit
  - growth/retention-analysis
related:
  - growth/motion-plg
  - growth/motion-slg
  - growth/funnel-audit
  - pmm/icp-research
  - pmm/positioning
---

# Motion: Mixed / Multi-Led Growth (MLG)

## Contract

This skill guarantees:
- MLG is only entered after confirming at least two of the three MLG detection signals
- Account duality is mapped before any content strategy is designed
- "Write one story; adjust the frame" is applied — no separate content tracks are created
- Handoff signals are explicitly defined with contact timing specified
- Organizational tension is addressed with a concrete resolution playbook, not just a diagnosis

---

**Role:** Motion Coordinator. MLG is not a motion you choose — it is the reality you manage when PLG and SLG are both active. The goal of this skill is to design the two motions to compound, not compete.

---

## Before starting

Confirm:
- **Current motion state** — is PLG already running? Is SLG already running? Are both active?
- **ICP card** — read `knowledge/icp-map.md` to identify both the IC champion profile and the economic buyer profile; MLG requires mapping both in the same account
- **Experiment history** — read `experiments/experiment-log.md` to check what has been tried at the PLG→SLG handoff and what handoff timing experiments have been run
- **PQL→close rate** — if known, gather this metric before starting; it is the primary MLG health indicator

---

## Inputs

**Required before proceeding:**
- Confirmation that both PLG and SLG motions are active (or being designed simultaneously)
- Description of the typical account: who uses the product bottom-up, and who evaluates it top-down
- Current PQL→close rate (or "unknown — will measure")
- Any known friction points between product/growth and sales teams

**If ICP card is available:** use both the IC/engineer profile and the economic buyer profile from the ICP card to anchor the account duality map.

---

## Step 1 — MLG Detection

Confirm you are in MLG territory before designing for it. Check all three signals.

```
Signal 1 — Bottom-up and top-down in the same account
  "Are individual contributors using the product self-serve while their management
  layer evaluates a company-wide deal separately?"
  
  Evidence of this signal:
    - Multiple ICs from the same company domain in self-serve accounts
    - Sales pipeline shows an opportunity at the same company
    - User feedback: "I love this; I just need to convince my VP to buy it for the team"
  
  Present: [YES / NO / UNCERTAIN]
  Evidence: [one sentence description or "none observed yet"]

Signal 2 — PQL and MQL in the same pipeline
  "Do you have both product-qualified leads (from PLG usage) and marketing-qualified
  leads (from demand gen) on the same accounts?"
  
  Evidence of this signal:
    - PQL signal fires on an account that is already in the CRM from a demo request
    - Marketing nurtures a contact who is also an active product user
    - Sales sees usage data on accounts they sourced through outbound
  
  Present: [YES / NO / UNCERTAIN]
  Evidence: [one sentence description or "none observed yet"]

Signal 3 — Organizational friction at the handoff
  "Is there active tension between the product/growth team (who own PLG) and
  sales (who own SLG) over the same accounts?"
  
  Evidence of this signal:
    - Sales contacts PLG users before the handoff signal fires
    - Product team complains that sales is "burning" self-serve users
    - PQL-sourced deals close at the same rate as cold outbound (no PLG advantage)
  
  Present: [YES / NO / UNCERTAIN]
  Evidence: [one sentence description or "none observed yet"]
```

**MLG verdict:**
```
MLG territory confirmed: [YES — 2+ signals present / LIKELY — 1 signal present, 
                          others probable / NOT YET — PLG+SLG but no overlap yet]

If NOT YET: proceed with motion-plg and motion-slg separately.
           Return to this skill when overlap appears.

If LIKELY or YES: proceed with MLG design.
```

---

## Step 2 — Account Duality Mapping

Every MLG account has two audiences with different jobs-to-be-done. Map them before designing content or the handoff.

### Account duality map template

See `growth/DOMAIN.md` for the reference account duality table (IC/Champion vs Economic Buyer). Reference, do not duplicate the table — use it to anchor the product-specific mapping below.

```
For this specific product:

IC / Champion
  Typical role: [e.g. "Senior backend engineer, infrastructure or platform team"]
  Job-to-be-done: [specific technical problem they are trying to solve]
  Success looks like: [e.g. "Running a migration in staging without incidents"]
  Blockers to internal advocacy: [e.g. "Cannot show performance numbers to manager"]
  Content they need at this stage: [list 2–3 specific content types]
  Where they spend time: [GitHub / HN / Reddit / Discord / internal Slack / etc.]

Economic Buyer
  Typical role: [e.g. "VP Engineering or CTO, or Procurement lead for IT tools"]
  Job-to-be-done: [specific business or risk problem they are solving]
  Success looks like: [e.g. "Reduced infra cost, no security incident, no migration failure"]
  Key questions they will ask: [e.g. "What's the SLA? Who else uses this? What's the migration risk?"]
  Content they need: [one-pager, ROI case, security overview, reference customer]
  Where they can be reached: [LinkedIn / email / sales call / internal presentation from champion]

The champion advocates up. The buyer decides.
The critical design question: what makes the champion's job of internal advocacy easier?

Champion advocacy enablers (build these):
  [ ] One-page summary they can forward without editing
  [ ] Usage data they can show their VP (usage volume, team adoption)
  [ ] A named reference customer from a similar company
  [ ] A clear answer to the InfoSec security question they know is coming
```

---

## Step 3 — "One Story, Two Frames" Content Strategy

MLG requires content that serves both audiences — not separate content tracks.

### The core principle

Write one story. Adjust the frame. The same factual narrative (a customer migration, a benchmark, an architectural decision) has both a technical frame and a business frame. Never write them as separate stories.

```
Example transformation:

Technical frame (IC/HN/community):
  "We migrated from [X] to [product]. The migration took 3 weeks, we ran both 
  systems in parallel for 30 days, and P99 latency dropped from 340ms to 52ms.
  Here's how we designed the migration plan and what we'd do differently."

Business frame (buyer/LinkedIn/case study):
  "[Company] reduced database latency by 85% while cutting infrastructure overhead
  and eliminating a 40-hour/week operational burden. Migration completed in 5 weeks
  with zero production incidents."

Same story. Same facts. Different frame.
```

### Content strategy per audience

```
Technical track (IC / Champion)
  Purpose: earn technical trust; help the champion solve their problem and look good
  Content types: migration stories, benchmarks with methodology, architecture decision records,
                 how-to guides, community Q&A
  Voice: practitioner (see pmm content review for voice standards)
  Channels: HN, Reddit, GitHub Discussions, dev community Discord/Slack, technical blog
  Production: community author or DevRel with editorial pass
  Cadence: quality over volume; one credible technical piece per week beats five thin ones

Business track (Economic Buyer)
  Purpose: reduce perceived risk; provide the business case the buyer needs to say yes
  Content types: one-page summary, ROI case, security overview, named customer case study,
                 executive reference call
  Voice: ROI-grounded, risk-aware, non-technical but specific (numbers required)
  Channels: LinkedIn, email (sales sequence), sales deck, internal sharing (champion forwards)
  Production: PMM or sales with ICP-grounded framing
  Cadence: updated when deal stages require it; not volume-driven

Content pairing (write in pairs where possible):
  Technical migration story → Business case study
  Architecture deep dive → Executive one-pager summary
  Benchmark results post → ROI calculator or cost comparison
```

### Content gap check

```
For each content pair, assess:
  [ ] Technical version exists and is current
  [ ] Business version exists and is current
  [ ] Both reference the same facts and numbers (consistency check)

Most common gap: the business version of technical content does not exist.
If champion has the technical piece but no business frame: the internal advocacy
stalls because the buyer sees engineer enthusiasm but no business case.
```

---

## Step 4 — Handoff Signal Definition

The PLG→SLG handoff is the highest-leverage design decision in MLG. Define it explicitly.

### Timing problem

```
Too early: Sales contacts self-serve users before they've had a positive experience.
  Effect: Trust is burned. Engineers complain internally. The champion becomes
  an anti-advocate, not a champion.
  Signal: PQL→close rate is low; self-serve users disengage after sales contact.

Too late: Sales misses the evaluation window.
  Effect: The champion evaluates alternatives while waiting. Or they do not escalate
  because no one helped them build the internal case.
  Signal: Warm PLG accounts close to competitors or stay on free tier indefinitely.

Right time: Sales contacts after the champion has had a positive FVM experience
  and there is a signal of enterprise intent.
```

### Handoff signal spec

```
Signals that are active for this product (from motion-plg handoff design):
  [ ] Team expansion signal: [X users from same domain in Y days]
  [ ] Usage volume signal: [% of tier limit for Z consecutive days]
  [ ] Enterprise tool integration: [SSO / SAML / Okta connection]
  [ ] Domain match: [company domain on ICP enterprise list]
  [ ] Intent language: [procurement / security / SLA mention in support]

For each active signal:
  Contact timing: [within X hours of signal firing]
  Assigned to: [SDR / AE / founder — by deal size or company size]
  Context required before first contact: [list from motion-slg handoff protocol]

Minimum contact rule: never reach out before [condition — e.g. "FVM reached AND
  at least one team-expansion signal has fired"]
```

---

## Step 5 — Org Tension Resolution Playbook

MLG creates structural friction between product/growth and sales. Address it directly.

### Three failure modes and resolutions

```
Failure mode 1: Sales contacts PLG users too early
  Symptom: Self-serve NPS drops after sales touch; engineers complain about unwanted outreach
  Resolution:
    - Define and enforce the minimum contact rule (Step 4 above)
    - Sales reps are blocked from reaching out unless the signal has fired in CRM
    - Track "contacted before signal" as a process metric; flag violations

Failure mode 2: Sales ignores PLG signals
  Symptom: Warm accounts with enterprise intent do not enter pipeline; high-intent free accounts
  stay on free tier until they churn to a competitor
  Resolution:
    - PQL signal routes automatically to CRM as a task with 24-hour SLA
    - Track "PQL signal → first contact within 24h" as a sales process metric
    - Attach usage context to the CRM task so the rep has no excuse for ignoring it

Failure mode 3: Product optimizes for self-serve, makes enterprise harder
  Symptom: Onboarding is frictionless for individuals but lacks enterprise SSO, audit logs,
  or team management features that enterprise evaluators require
  Resolution:
    - Map enterprise-specific requirements at the Technical Evaluation stage
    - Add enterprise readiness criteria to the product roadmap alongside self-serve activation
    - Do not optimize purely for free-to-paid self-serve conversion if it degrades enterprise
    evaluation experience
```

### PQL tracking requirement

```
Track PQL-sourced deals separately from cold outbound in CRM.

Required CRM tags or fields:
  - Lead source: PLG signal (vs outbound / inbound / event / referral)
  - Signal type: [which PLG signal fired]
  - Time from signal to first contact: [hours]
  - Usage context attached: [YES / NO]

Why: PQL-sourced deals should close faster and at higher rates than cold outbound.
  If they do not, either:
    (a) The PQL signal definition is wrong (too broad; not predictive)
    (b) The handoff is broken (too early, uninformed, or missing usage context)
  Track separately so you can diagnose which.
```

---

## Output format

Produce all three of the following at the end of the session:

### 1. MLG Account Duality Map

```
## MLG Account Duality Map

Product: [name]
Date: [date]

MLG confirmed: [YES / LIKELY / NOT YET] — [signals present]

IC / Champion
  Role: [role]
  JTBD: [one sentence]
  Advocacy blocker: [one sentence]
  Content needed: [2–3 types]

Economic Buyer
  Role: [role]
  JTBD: [one sentence]
  Key decision question: [one sentence]
  Content needed: [one-pager / ROI case / security overview / reference]

Champion advocacy enablers:
  [ ] One-page summary: [EXISTS / NEEDED]
  [ ] Usage data dashboard or export: [EXISTS / NEEDED]
  [ ] Named reference customer: [EXISTS / NEEDED]
  [ ] Security FAQ: [EXISTS / NEEDED]
```

### 2. Content Strategy Per Audience

```
## Content Strategy

Technical track:
  Priority content types: [list 2–3]
  Channels: [list]
  Owner: [role]
  Cadence: [weekly / bi-weekly]

Business track:
  Priority content types: [list 2–3]
  Channels: [list]
  Owner: [role]
  Cadence: [as needed for deal stages]

Content pairs needed (technical → business):
  [ ] [Technical piece name] → [Business version name]
  [ ] [Technical piece name] → [Business version name]

Biggest gap: [one sentence — what's missing that unblocks the most deals]
```

### 3. Handoff Protocol and Org Resolution

```
## Handoff Protocol

Active signals: [list]
Minimum contact rule: [condition]
Contact timing: [within X hours]
Context package: [list what is passed to sales]
CRM tracking: [fields / tags required]

Org resolutions implemented:
  [ ] Minimum contact rule enforced in CRM
  [ ] PQL signal routes automatically as CRM task with 24h SLA
  [ ] PQL-sourced pipeline tracked separately from cold outbound
  [ ] Enterprise product requirements added to roadmap

PQL→close rate baseline: [% or "measure from CRM next quarter"]
Target PQL→close rate: [>40%]

Next step: /growth-experiment (if PQL→close rate is below 40% and handoff is redesigned)
```

---

## Brain reads / writes

**If a companion `aether-growth-brain` repo is connected:**

Before starting:
- Read `knowledge/icp-map.md` — both the IC champion profile and the economic buyer profile are required; do not proceed with account duality mapping without both
- Read `experiments/experiment-log.md` — check what handoff timing or contact sequence experiments have been tried; MLG handoff optimization is iterative

Brain write (when MLG design is finalized):
- Write account duality map and handoff protocol to `decisions/motion-mlg-design-[date].md`
- Note content pairs needed and biggest gap in `decisions/content-strategy-mlg-[date].md`

**Brain not connected:** proceed; recommend saving the duality map and handoff protocol locally and reviewing PQL→close rate quarterly.

---

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Writing separate content for ICs and buyers from scratch | Double the effort; the stories are inconsistent; the champion cannot connect the technical piece to the business case the buyer needs | Write once, frame twice: technical piece first, then add a business-framing layer |
| No minimum contact rule for PLG accounts | Sales contacts users at the wrong time; trust is burned; the champion does not advocate | Define and enforce the minimum contact rule before sales has access to PLG user data |
| PQL-sourced deals lumped with cold outbound | Cannot diagnose whether PLG is creating real sales advantage or not | Tag PQL source in CRM; track separately |
| Optimizing for one audience at the expense of the other | IC content that ignores buyer needs leaves champions without advocacy tools; buyer content that ignores IC needs never reaches the champion | Design content in pairs; check both tracks quarterly |
| Declaring MLG complete when the handoff is defined | Handoff definition is the beginning, not the end; MLG requires ongoing PQL signal tuning and org alignment maintenance | Review PQL→close rate quarterly; revisit signal definitions when rate drops |

---

## Validation criteria

- [ ] MLG detection: at least two of three signals confirmed before proceeding
- [ ] Account duality map completed with specific champion and buyer profiles
- [ ] Content strategy designed in pairs (technical track + business track)
- [ ] Handoff signals explicitly defined with timing and minimum contact rule
- [ ] All three org failure modes addressed in the resolution playbook
- [ ] PQL-sourced deals tracked separately from cold outbound (CRM requirement noted)
- [ ] MLG account duality map produced
- [ ] Content strategy per audience produced
- [ ] Handoff protocol spec produced

---

## References & Sources

**Tier 1:**
- growth-motion-mlg (growth-skills v1.0, score 7.5/10): MLG signals, account duality framework, "write one story, adjust the frame", PQL→close rate as health metric, org tension failure modes
- growth-motion-plg (growth-skills v1.0, score 8.5/10): PLG→SLG handoff signal definitions
- growth-motion-slg (growth-skills v1.0, score 8/10): deal anatomy and champion advocacy enabler content

**Tier 2 (via growth/DOMAIN.md):**
- Account duality reference table
- MLG health metric definition (PQL→close rate > 40%)
- Org tension resolution framework
