---
name: motion-plg
description: >-
  Designs or audits a Product-Led Growth motion: checks PLG readiness, defines
  the First Value Moment, designs the activation funnel, runs the onboarding
  audit protocol, and specifies the PLG-to-SLG handoff. Use when building PLG
  from scratch, diagnosing why activation or free-to-paid conversion is low, or
  deciding which usage signals should trigger a sales touch.
triggers:
  - /motion-plg
  - user wants to design or build a PLG motion
  - user wants to audit why PLG is not converting
  - user is diagnosing an activation gap or low FVM rate
  - user wants to define their First Value Moment
  - user wants to design the PLG to SLG handoff
role: workflow
version: 1.0.0
sources:
  - "growth-motion-plg (growth-skills v1.0, score 8.5/10)"
  - "Reforge growth loops and retention frameworks"
  - "Jobs-to-be-Done, Clayton Christensen"
feeds:
  - growth/growth-experiment
  - growth/funnel-audit
  - growth/retention-analysis
  - growth/motion-slg
related:
  - growth/motion-slg
  - growth/motion-mlg
  - growth/funnel-audit
  - growth/retention-analysis
  - pmm/icp-research
---

# Motion: Product-Led Growth (PLG)

## Contract

This skill guarantees:
- No PLG design proceeds without passing the three-criteria readiness check
- FVM is always defined in one observable sentence before any activation work begins
- Onboarding audit covers all four protocol checks (friction, empty state, error path, value communication)
- PLG→SLG handoff signals are explicitly defined — no PLG motion exits without them
- Every output is an actionable spec, not a recommendation list

---

**Role:** PLG Architect. PLG is not a feature — it is an operating model in which the product is the primary acquisition, retention, and expansion channel. This skill walks you through designing or auditing that model rigorously.

---

## Before starting

Confirm:
- **Product context** — what does the product do, who uses it, what problem does it solve?
- **Current state** — designing from scratch, or auditing an existing PLG motion?
- **ICP card** — read `knowledge/icp-map.md` to confirm who self-serves (PLG ICP is often different from the SLG buyer ICP)
- **Experiment history** — read `experiments/experiment-log.md` to avoid repeating activation experiments that already produced LOSS or CONFOUNDED verdicts
- **Baseline metrics** — if auditing, gather current signup count, FVM rate, D7 retention, and free-to-paid conversion rate before starting

---

## Inputs

**Required before proceeding:**
- Product description and target user (engineer, data scientist, ops practitioner, etc.)
- Whether the motion is being designed from scratch or audited
- Current activation metrics if auditing (even rough estimates acceptable)

**If ICP card is available:** use Core ICP segment as the primary audience for all activation and onboarding design decisions.

---

## Step 1 — PLG Readiness Assessment

Before investing in PLG, check all three criteria. All three are required. One failure does not disqualify PLG, but it identifies where the biggest risk lies.

```
Criterion 1 — Self-deliverable value
  "Can a user experience meaningful value without a salesperson, implementation
  consultant, or multi-week setup project?"
  
  PASS: User can get to a real result in a single session
  BORDERLINE: User needs some setup but can self-serve through it with good docs
  FAIL: Value requires vendor professional services or extensive customer data migration
  
  If FAIL: PLG is premature. Design a high-touch trial with SDR-assisted onboarding
  instead. Revisit PLG when product can deliver self-serve value.

Criterion 2 — Short time-to-value
  "How long does a new user need to reach their first meaningful result?"
  
  PASS: Minutes to a few hours
  BORDERLINE: A few hours to one day with guidance
  FAIL: Multiple days or requires importing significant existing data/config
  
  If FAIL: PLG is premature. Shorten TTV first — simplify setup, add sample data,
  build a guided quickstart — before running PLG acquisition.

Criterion 3 — Viable free tier or trial
  "Can a user evaluate the product meaningfully without going through procurement?"
  
  PASS: Free tier or time-limited trial with no credit card required at signup
  BORDERLINE: Credit card required but trial is generous (30+ days, real feature access)
  FAIL: No trial path; evaluation requires a sales call and custom pricing quote
  
  If FAIL: PLG acquisition will stall at signup because engineers cannot evaluate
  without corporate approval. Add a trial tier before optimizing the funnel.
```

**PLG Readiness verdict format:**
```
PLG Readiness: [READY / BORDERLINE / NOT READY]

Criterion 1 (Self-deliverable value): [PASS / BORDERLINE / FAIL]
  Finding: [one sentence]
  Risk if borderline/fail: [one sentence]

Criterion 2 (Short TTV): [PASS / BORDERLINE / FAIL]
  Finding: [one sentence]
  Risk if borderline/fail: [one sentence]

Criterion 3 (Viable free tier): [PASS / BORDERLINE / FAIL]
  Finding: [one sentence]
  Risk if borderline/fail: [one sentence]

Recommended action: [proceed / fix X before proceeding]
```

---

## Step 2 — FVM Definition Workshop

The First Value Moment (FVM) is the single most important concept in PLG. If you cannot define and observe it, you cannot improve it.

### Guided questions to define FVM

Work through these in order:

```
Q1: What is the core value proposition of the product in one sentence?
    (Not the feature list — the outcome the user is paying for)

Q2: What is the smallest possible version of that value a new user could experience
    in a single session?
    (Think: what's the "aha" moment where the user thinks "this is exactly what I needed")

Q3: What specific user action produces or signals that moment?
    (Must be an event you can log: API call, query run, integration connected, dashboard loaded)

Q4: What is the realistic time window in which that action should happen?
    (Not aspirational — look at your top 20% of retained users and see when they hit it)

Q5: Is this action currently instrumented in your analytics tool?
    (If no: instrumentation is Step 2a before anything else)
```

### FVM definition statement

Once questions are answered, produce the definition:

```
FVM Definition:
"A user has reached FVM when they have [specific action] within [time window] of signup."

Observable event: [event name in analytics / data warehouse]
Instrumented: [YES / NO — if NO, list what must be added before proceeding]

FVM rate baseline: [% of signups who reach FVM within the window, or "unknown — measure first"]
```

### FVM red flags

| Red flag | What it signals | Fix |
|---|---|---|
| FVM defined as "user reads the docs" | Passive consumption is not value delivery | Redefine as a product action, not a content action |
| FVM requires more than 5 user actions from signup | The funnel is too long; users drop before FVM | Redesign the onboarding path to reduce steps |
| FVM is not observable in analytics | Cannot measure or improve what you cannot see | Instrument the event before any other work |
| FVM happens after day 3 for most users | TTV is too long; most users will churn before reaching it | Redesign to surface value faster, or add a guided shortcut |

---

## Step 3 — Activation Funnel Design

With FVM defined, design the full activation instrumentation spec.

### Three moments to instrument

See `growth/DOMAIN.md` for the full activation moment definitions (Signup → FVM → Habit formation). Reference, do not duplicate.

### Funnel instrumentation spec

```
## Activation funnel spec

Stage 1 — Signup
  Event: [account_created / email_verified / workspace_initialized]
  Properties to capture: [signup source, referral, plan tier, company domain]
  Current volume (if known): [number/week]

Stage 2 — First Value Moment
  Event: [FVM event name from Step 2]
  Time window: [X hours/days from signup]
  FVM rate baseline: [% or "unknown"]
  Goal FVM rate: [target %, or "establish baseline first"]

Stage 3 — Habit formation
  Definition: [second meaningful action within X days — be specific]
  Event: [event name]
  Time window: [X days from FVM]
  Current rate: [% or "unknown"]

Funnel drop-off analysis:
  Signup → FVM drop: [%]
  FVM → Habit drop: [%]
  Biggest drop-off stage: [Stage 1→2 / Stage 2→3]
  Hypothesis for biggest drop: [one sentence]
```

### Metrics to instrument before running experiments

See `growth/DOMAIN.md` for the full PLG metrics table (Time to FVM, FVM rate, D7/D30 retention, free-to-paid conversion). Reference, do not duplicate.

Do not start running PLG experiments without baseline measurements on at least FVM rate and D7 retention.

---

## Step 4 — Onboarding Audit Protocol

Run this before designing experiments. Walk the signup-to-FVM path as a new user with no prior knowledge of the product.

### Four-check audit

```
Check 1 — Friction audit
  Walk the path from account creation to FVM. Count every step.
  
  PASS: 5 or fewer steps between account creation and FVM
  BORDERLINE: 6–8 steps
  FAIL: More than 8 steps, or any step that requires leaving the product
         (e.g. reading external docs, setting up a separate dependency)
  
  Document each step:
  [Step name] → [drop-off % if known] → [blocker type: friction / confusion / 
                                          missing value / error]

Check 2 — Empty state audit
  What does a user see when they first log in with no data?
  
  PASS: Empty state includes a clear first action and explains what the user will
        get by completing it
  BORDERLINE: Empty state has a CTA but no explanation of why
  FAIL: Blank screen, error state, or "you have no [items]" with no guidance
  
  Finding: [describe what the user currently sees]
  Required: [what a good empty state must include to pass]

Check 3 — Error path audit
  Trigger the most common first-step failure (wrong input, missing config, etc.).
  What happens?
  
  PASS: Clear error message explaining what went wrong + a recovery action the user
        can take immediately
  BORDERLINE: Error message explains what went wrong but no recovery path
  FAIL: Silent failure, generic error code, or crash with no recovery path
  
  Finding: [describe the most common failure and current error handling]
  Required: [what good error handling looks like for this step]

Check 4 — Value communication audit
  After the FVM event occurs, ask: can a new user explain in one sentence what
  they just accomplished?
  
  PASS: The product surfaces a clear confirmation of what happened and why it matters
        (e.g. "Your first query returned 847 rows in 12ms — here's what you can do next")
  BORDERLINE: Completion is confirmed but benefit is not stated
  FAIL: No confirmation; user must infer that they succeeded
  
  Finding: [what the product currently shows at FVM]
  Required: [what it should show to pass]
```

### Audit output table

```
| Check | Result | Finding | Priority fix |
|---|---|---|---|
| Friction (step count) | [PASS/BORDERLINE/FAIL] | [X steps] | [fix or n/a] |
| Empty state | [PASS/BORDERLINE/FAIL] | [finding] | [fix or n/a] |
| Error path | [PASS/BORDERLINE/FAIL] | [finding] | [fix or n/a] |
| Value communication | [PASS/BORDERLINE/FAIL] | [finding] | [fix or n/a] |
```

Blockers (any FAIL): fix before running acquisition experiments. Sending more users into a broken onboarding amplifies the problem.

---

## Step 5 — PLG→SLG Handoff Design

PLG does not mean no sales. It means the product drives acquisition and qualification; sales handles expansion and enterprise conversion. Define the handoff before it happens spontaneously.

### Handoff signal definition

For each signal below, decide: is this signal active (you are tracking it), inactive (you are not tracking it yet), or not applicable.

```
Signal 1 — Team expansion
  Definition: Multiple users from the same organization domain signup independently
  Threshold: [X users from same domain within Y days — set your own]
  Tracked: [YES / NO]
  If YES, data source: [CRM / product analytics / manual]

Signal 2 — Usage volume
  Definition: Account usage consistently exceeds free-tier limits
  Threshold: [specific usage metric at X% of limit for Y consecutive days]
  Tracked: [YES / NO]

Signal 3 — Enterprise tool integration
  Definition: User connects SSO, SAML, Okta, or other enterprise-only integration
  Threshold: [any integration = signal, or specific integrations only]
  Tracked: [YES / NO]

Signal 4 — Domain match
  Definition: Signup domain matches ICP enterprise profile (size, industry, known account list)
  Threshold: [criteria — e.g. >500 employees in ICP industry]
  Tracked: [YES / NO]

Signal 5 — Intent language in support
  Definition: Support or chat mention of procurement, security review, SLA, or legal
  Threshold: [any mention = signal]
  Tracked: [YES / NO]
```

### Handoff protocol spec

```
When signal fires:
  Route to: [sales rep / SDR / account owner — specify]
  Time to first touch: [target: within 24–48 hours of signal]
  Context passed: [list what the sales rep receives before first call]
    - Company domain and known team members using product
    - Features used and usage volume
    - Which signal(s) fired
    - Signup date and time to FVM
  
First outreach format:
  Channel: [email / LinkedIn / phone — specify]
  Tone: acknowledge existing usage; never make them restart the evaluation
  Template structure:
    "I noticed your team has been using [product] — specifically [feature].
     For teams at your scale, [specific benefit or issue] is often worth a brief
     conversation. Worth 20 minutes?"
  
  (Full outreach template reference: growth/DOMAIN.md SLG section)
```

---

## Output format

Produce all three of the following at the end of the session:

### 1. PLG Assessment Card

```
## PLG Assessment Card

Product: [name]
Date: [date]
Assessor: [name/role]

Readiness: [READY / BORDERLINE / NOT READY]
  Criterion 1 (Self-deliverable value): [PASS/BORDERLINE/FAIL]
  Criterion 2 (Short TTV): [PASS/BORDERLINE/FAIL]
  Criterion 3 (Viable free tier): [PASS/BORDERLINE/FAIL]

Onboarding audit:
  Friction: [PASS/BORDERLINE/FAIL] — [step count]
  Empty state: [PASS/BORDERLINE/FAIL]
  Error path: [PASS/BORDERLINE/FAIL]
  Value communication: [PASS/BORDERLINE/FAIL]

Blockers to fix before running experiments: [list or "none"]

Priority experiment: [one-line description of the highest-leverage next test]
Recommended next skill: [/growth-experiment or /funnel-audit]
```

### 2. FVM Definition Statement

```
## FVM Definition

"A user has reached FVM when they have [specific action] within [time window] of signup."

Observable event: [event name]
Instrumented: [YES / NO]
If NO, instrumentation required: [list events to add]

FVM rate baseline: [% or "measure first"]
Target FVM rate: [% or "establish baseline first"]
```

### 3. Activation Instrumentation Spec

```
## Activation Instrumentation Spec

Events to instrument:
  signup: [event + properties]
  fvm: [event + properties]
  habit_formed: [event + properties]

Metrics dashboard required:
  - Time to FVM (median) by cohort
  - FVM rate (% signup → FVM within [window]) by cohort
  - D7 retention by signup week
  - Free-to-paid conversion by cohort

PLG→SLG handoff signals active: [list which signals are instrumented]

Next step: /growth-experiment (once instrumentation is live and baseline is measured)
```

---

## Brain reads / writes

**If a companion `aether-growth-brain` repo is connected:**

Before starting:
- Read `knowledge/icp-map.md` — confirm who self-serves; PLG ICP is often different from the SLG buyer ICP; use Core ICP segment to anchor FVM definition
- Read `experiments/experiment-log.md` — check what activation experiments have been run; avoid re-running those with LOSS or CONFOUNDED verdicts without a deliberate variable change

Brain write (when PLG assessment and FVM definition are finalized):
- Write PLG assessment card to `decisions/motion-plg-assessment-[date].md`
- Record FVM definition and instrumentation spec in `decisions/fvm-definition-[date].md`

**Brain not connected:** proceed; recommend saving the PLG assessment card and FVM definition locally as the authoritative record for the team.

---

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Defining FVM as a passive action ("user reads the docs") | Passive consumption does not predict retention or conversion | Redefine as a product action that delivers or confirms value |
| Running acquisition experiments before instrumentation | You cannot diagnose what you cannot measure | Instrument signup, FVM, and habit events before any experiment |
| Optimizing signup volume without measuring FVM rate | More signups into a broken funnel amplifies the problem | Fix the onboarding audit FAIL items before scaling acquisition |
| Defining FVM so broadly it is always reached | A 100% FVM rate means the FVM is not predictive of retention | Tighten the definition until FVM rate predicts D30 retention |
| Skipping the PLG readiness check and jumping to tactics | PLG applied to a product that fails the criteria produces churn, not growth | Always run the three-criteria check first |
| No handoff signal definition | PLG accounts with enterprise intent churn silently | Define at least two handoff signals before going live |

---

## Validation criteria

- [ ] All three PLG readiness criteria assessed with explicit PASS/BORDERLINE/FAIL
- [ ] FVM defined in one observable sentence with a named analytics event
- [ ] Activation funnel instrumented at all three stages (signup, FVM, habit)
- [ ] Onboarding audit completed for all four checks
- [ ] At least two PLG→SLG handoff signals defined with tracking status confirmed
- [ ] PLG assessment card produced
- [ ] FVM definition statement produced
- [ ] Activation instrumentation spec produced

---

## References & Sources

**Tier 1:**
- growth-motion-plg (growth-skills v1.0, score 8.5/10): readiness criteria, FVM definition format, onboarding audit protocol, handoff signals
- Reforge growth loops: activation moment framework (signup → FVM → habit), retention curve mechanics
- Jobs-to-be-Done (Christensen): FVM definition framing — value is defined by the user's job, not the product's features

**Tier 2 (via growth/DOMAIN.md):**
- PLG metrics benchmarks and D7/D30 retention context
- Full PLG→SLG handoff signal list and outreach template
