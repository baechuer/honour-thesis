---
name: create-an-asset
description: Generates customized sales assets including one-pagers, proposals, executive summaries, ROI summaries, and mutual action plans from Dataverse context. Use when user says "create a one-pager", "draft a proposal", "generate executive summary", "build ROI summary", "create mutual action plan", "sales asset for [account]", "proposal outline", or "customer-facing document".
metadata:
  author: Dataverse
  version: 1.0.0
  category: sales-productivity
---

# Create an Asset

Reps waste time reformatting generic templates for each prospect. This skill pulls real Dataverse data — deal context, pain points, products, account details, and relationship history — to generate tailored sales documents that feel specific to the buyer. Assets are saved back to Dataverse as annotations so the full team has access.

## Instructions

### Step 1: Identify Asset Type and Target
Accept input from the user:
- **Asset type:** One-pager, proposal outline, executive summary, ROI summary, mutual action plan (MAP), competitive battlecard, or meeting follow-up summary
- **Target:** Opportunity name, account name, or contact name
- **Audience:** Economic buyer, technical evaluator, end user, executive sponsor

#### Step 2: Retrieve Opportunity Context
```
SELECT opportunityid, name, estimatedvalue, estimatedclosedate, salesstage,
       closeprobability, budgetstatus, need, purchasetimeframe, purchaseprocess,
       decisionmaker, description, currentsituation, customerneed,
       customerpainpoints, msdyn_forecastcategory, ownerid, customerid, accountid
FROM opportunity
WHERE opportunityid = '[opportunityid]'
```

If searching by name:
```
SELECT opportunityid, name, estimatedvalue, estimatedclosedate, salesstage,
       customerid, ownerid
FROM opportunity
WHERE statecode = 0
AND name LIKE '%[search_term]%'
```

#### Step 3: Retrieve Account Details
```
SELECT accountid, name, industrycode, revenue, numberofemployees, description,
       address1_city, address1_stateorprovince, address1_country,
       customertypecode, accountcategorycode, websiteurl
FROM account
WHERE accountid = '[accountid]'
```

#### Step 4: Retrieve Key Contacts and Stakeholders
```
SELECT contactid, fullname, jobtitle, emailaddress1, description
FROM contact
WHERE accountid = '[accountid]'
ORDER BY createdon DESC
```

Identify stakeholder roles from jobtitle field (Economic Buyer, Technical Evaluator, Champion, End User) for use in asset personalization.

#### Step 5: Retrieve Products Under Consideration
```
SELECT opportunityproduct.productid, product.name, product.description,
       opportunityproduct.quantity, opportunityproduct.priceperunit,
       opportunityproduct.tax, opportunityproduct.baseamount
FROM opportunityproduct
JOIN product ON opportunityproduct.productid = product.productid
WHERE opportunityproduct.opportunityid = '[opportunityid]'
```

#### Step 6: Retrieve Activity History for Context
```
SELECT activityid, activitytypecode, subject, actualend, description
FROM activitypointer
WHERE regardingobjectid = '[opportunityid]'
AND statecode = 1
ORDER BY actualend DESC
```
Limit to 5 most recent. Extract key discussion topics from subject and description fields.

#### Step 7: Check for Related Products Already Owned (for ROI/Upsell context)
```
SELECT product.name, opportunityproduct.quantity, opportunity.actualclosedate
FROM opportunityproduct
JOIN opportunity ON opportunityproduct.opportunityid = opportunity.opportunityid
JOIN product ON opportunityproduct.productid = product.productid
WHERE opportunity.customerid = '[accountid]'
AND opportunity.statecode = 1
ORDER BY opportunity.actualclosedate DESC
```

#### Step 8: Generate Asset by Type

---
**ASSET TYPE: One-Pager**

Structure:
```
[ACCOUNT NAME] + [YOUR COMPANY]
[Date]

THE CHALLENGE
[2-3 sentences from opportunity.customerpainpoints and currentsituation]

OUR SOLUTION
[Products being considered with 1-line value prop each, from product.description]

WHY IT MATTERS FOR [ACCOUNT NAME]
[Industry-specific benefit framing based on account.industry]
[Reference estimatedvalue savings or outcomes if quantified in notes]

WHAT WE'VE HEARD FROM YOU
• [Key pain point from customerpainpoints]
• [Need from opportunity.need field context]
• [Timeline urgency from purchasetimeframe]

NEXT STEPS
[3 bullets: immediate action, validation step, decision checkpoint]

[Rep Name] | [Title] | [Contact Info]
```

---
**ASSET TYPE: Proposal Outline**

Structure:
```
PROPOSAL: [Opportunity Name]
Prepared for: [Contact Name], [Title] | [Account Name]
Date: [Today]

1. EXECUTIVE SUMMARY
   [2 sentences: problem + proposed solution]

2. UNDERSTANDING YOUR SITUATION
   Current state: [currentsituation]
   Key challenges: [customerpainpoints]
   Desired outcome: [customerneed]

3. PROPOSED SOLUTION
   [Product 1 — name, description, quantity, price]
   [Product 2 — if applicable]

   Total investment: $[baseamount sum from opportunityproduct]

4. IMPLEMENTATION APPROACH
   [Phased rollout based on complexity and timeline from purchasetimeframe]
   Timeline: [Estimated based on purchasetimeframe field]

5. WHY [YOUR COMPANY]
   [Differentiation narrative — customize based on industry and deal context]

6. INVESTMENT SUMMARY
   [Pricing table from opportunityproduct records]
   [Payment terms if discussed]

7. NEXT STEPS
   [ ] [Action 1 with owner and date]
   [ ] [Action 2 with owner and date]
   [ ] Decision date: [estimatedclosedate]
```

---
**ASSET TYPE: Executive Summary**

For economic buyer audience — concise, outcome-focused:
```
EXECUTIVE SUMMARY
[Account Name] | [Opportunity Name]
[Date]

BUSINESS OBJECTIVE
[1 sentence on what the customer is trying to achieve]

RECOMMENDED APPROACH
[Products/solution in plain business language — no technical jargon]

EXPECTED OUTCOMES
• [Outcome 1 with estimated value/impact if available]
• [Outcome 2]
• [Outcome 3]

INVESTMENT
Total: $[estimatedvalue]
Timeline to value: [Based on purchasetimeframe and implementation estimate]

DECISION TIMELINE
Target close: [estimatedclosedate]
Key milestone: [Next step from most recent activity]

Prepared by: [Rep Name] | [Date]
```

---
**ASSET TYPE: ROI Summary**

```
ROI SUMMARY: [Account Name]
[Opportunity Name] | $[estimatedvalue]

CURRENT SITUATION
[currentsituation from opportunity record]

COST OF INACTION
[If pain points mention productivity, manual work, errors — quantify where possible]
Estimated annual cost without solution: [If data available in notes]

PROJECTED VALUE
[Frame around pain points + products under consideration]
• [Benefit 1 — e.g., hours saved × hourly rate if mentioned]
• [Benefit 2 — e.g., error reduction]
• [Benefit 3 — e.g., revenue opportunity]

Estimated annual value: [Calculate if sufficient data]
Payback period: [estimatedvalue / annual value]

EXISTING RELATIONSHIP
[Reference products already owned, tenure as customer, relationship value]

Prepared by: [Rep Name] | [Date]
```

---
**ASSET TYPE: Mutual Action Plan (MAP)**

```
MUTUAL ACTION PLAN
[Account Name] ↔ [Your Company]
Opportunity: [Opportunity Name] | Target Close: [estimatedclosedate]

SHARED GOAL
[One sentence agreed outcome]

OPEN ITEMS
Item                    | Owner         | Due Date    | Status
───────────────────────────────────────────────────────────────
[From open tasks in Dataverse, listed per regardingobjectid]

UPCOMING MILESTONES
Date        | Milestone               | Owner
[Series of steps leading to estimatedclosedate]

DECISION CRITERIA
[ ] [Criterion 1]
[ ] [Criterion 2 — from customerneed or notes]
[ ] Budget approved (budgetstatus target)
[ ] Stakeholders aligned (decisionmaker = true)

CONTACTS
[Your team]: [Rep Name, title, email]
[Their team]: [Contacts from Dataverse with jobtitle]
```

---
**ASSET TYPE: Meeting Follow-Up Summary**

Pull from most recent completed appointment:
```
MEETING SUMMARY
[Meeting subject] | [Date] | [Attendees]

KEY DISCUSSION POINTS
• [From appointment.description]

DECISIONS MADE
• [From notes if available]

OPEN ITEMS / COMMITMENTS
[From tasks created from appointment regardingobjectid]

AGREED NEXT STEPS
[From open tasks due after meeting date]

RELEVANT DEAL: [Opportunity name, stage, close date]

Follow-up sent by: [Rep Name] | [Date]
```

#### Step 9: Save Asset to Dataverse
After generating the asset, create an annotation record:
```
Use create_record tool with tablename: annotation
- subject: "[Asset Type] — [Account Name] — [Date]"
- notetext: [Full generated asset content]
- objectid: [Opportunity ID or Account ID]
- objecttypecode: "opportunity" or "account"
```

Confirm with the user before saving. The annotation becomes accessible to the full sales team from the opportunity or account record in Dynamics 365.

### Output Format
Provide:
1. **Generated asset** in full (formatted for copy-paste or review)
2. **Data sources used** — which fields populated each section
3. **Gaps identified** — sections where data was missing and how to fill them
4. **Save confirmation** — annotation ID after saving to Dataverse

### Example Interaction

**User Input:**
"Create a one-pager for the Fabrikam Cloud Migration opportunity."

**Skill Output:**
📄 **One-Pager: Fabrikam + [Your Company]**
*Generated from Dataverse — March 3, 2026*

---
**FABRIKAM + CONTOSO CLOUD**
*March 2026*

**THE CHALLENGE**
Fabrikam's current on-premises infrastructure requires manual maintenance and has experienced recurring reliability issues, limiting the team's ability to scale operations efficiently. The IT team is managing integration complexity that is consuming resources better spent on business-critical work.

**OUR SOLUTION**
- **Cloud Migration Suite** — end-to-end migration tooling and managed transition service
- **Dataverse Integration Connector** — resolves the current API timeout issues with a pre-built, certified connector

**WHY IT MATTERS FOR FABRIKAM**
Manufacturing companies like Fabrikam typically reduce infrastructure overhead by 30-40% after cloud migration. Eliminating the integration bottleneck frees the IT team for higher-value projects.

**WHAT WE'VE HEARD FROM YOU**
- Reliability issues with current vendor are creating operational risk
- Timeline: decision needed by end of Q1 to hit implementation target
- Budget allocated at $85,000 for initial implementation

**NEXT STEPS**
- [ ] Emily and James: review updated SOW (due this week)
- [ ] Technical validation: API connector pilot — 1 week
- [ ] Sign-off: March 31

*Sarah Johnson | Account Executive | sarah.johnson@contoso.com*

---
**Data used:** customerpainpoints, products in opportunity, estimatedvalue, estimatedclosedate, open tasks
**Gaps:** ROI quantification unavailable — ask Emily for current infrastructure cost to strengthen the one-pager
**Saved:** Annotation created on Fabrikam Cloud Migration (ID: annotation-xxx)

### Dataverse Tables Used
| Table | Purpose |
|-------|---------|
| `opportunity` | Deal context, pain points, qualification |
| `account` | Account details and industry |
| `contact` | Stakeholder names and titles |
| `opportunityproduct` | Products in scope and pricing |
| `product` | Product descriptions |
| `activitypointer` | Recent activity context |
| `task` | Open commitments for MAP |
| `annotation` | Save generated asset |

### Key Fields Reference
**opportunity:**
- `currentsituation` (MULTILINE TEXT) - Customer's current state
- `customerneed` (MULTILINE TEXT) - What they need
- `customerpainpoints` (MULTILINE TEXT) - Pain points identified
- `description` (MULTILINE TEXT) - General notes

**annotation:**
- `subject` (NVARCHAR 500) - Asset title
- `notetext` (MULTILINE TEXT) - Full asset content
- `objectid` (LOOKUP) - Linked opportunity or account
- `objecttypecode` (NVARCHAR) - "opportunity" or "account"

### Configurable Parameters
- Default asset type (one-pager by default)
- Auto-save to Dataverse (default: prompt before saving)
- Maximum asset length (default: no limit)
- Product description verbosity (brief tagline vs full description)

## Examples

### Example 1: Executive Summary One-Pager

**User says:** "Create a one-pager for the Fabrikam opportunity"

**Actions:**
1. Query Fabrikam opportunity for deal context
2. Retrieve account details and stakeholders
3. Pull products under consideration
4. Extract pain points and customer needs
5. Generate formatted one-pager

**Result:**
```
FABRIKAM + CONTOSO
March 2026

THE CHALLENGE:
Fabrikam's current on-premise infrastructure creates
operational risk and limits their expansion plans.

OUR SOLUTION:
• Cloud Migration Platform ($65,000)
• Managed Support Package ($20,000/yr)

WHAT WE'VE HEARD FROM YOU:
• Reliability issues creating operational risk
• Timeline: decision by end of Q1
• Budget allocated at $85,000

NEXT STEPS:
[ ] Review updated SOW (this week)
[ ] API connector pilot (1 week)
[ ] Sign-off: March 31

---
Saved: Annotation created on Fabrikam opportunity
```

### Example 2: Mutual Action Plan

**User says:** "Build a mutual action plan for Alpine Ski House"

**Actions:**
1. Query opportunity and open tasks
2. Identify stakeholders and decision timeline
3. Calculate milestone dates
4. Generate structured MAP

**Result:**
```
MUTUAL ACTION PLAN
Alpine Ski House + Contoso

GOAL: Go-live by April 15, 2026

MILESTONES:
| Date    | Action                    | Owner      |
|---------|---------------------------|------------|
| Mar 7   | Technical requirements    | Lisa (ASH) |
| Mar 14  | Security review complete  | IT Team    |
| Mar 21  | Contract redlines         | Legal      |
| Mar 28  | Final sign-off            | CFO        |
| Apr 15  | Go-live                   | Joint team |

SUCCESS CRITERIA:
• 95% uptime SLA met
• Training complete for 50 users
• Integration with existing ERP

---
Saved: Annotation created on Alpine Ski House opportunity
```

### Example 3: ROI Summary

**User says:** "Generate an ROI summary for Northwind"

**Actions:**
1. Query opportunity and products
2. Retrieve current situation and pain points
3. Calculate potential savings based on product benefits
4. Generate ROI document

**Result:**
```
ROI SUMMARY: NORTHWIND TRADERS

CURRENT STATE:
• Manual order processing: 2 hours/day
• Error rate: 3.5%
• Customer complaints: 12/month

PROJECTED BENEFITS:
| Metric            | Current | Projected | Savings  |
|-------------------|---------|-----------|----------|
| Processing time   | 2 hr/day| 30 min    | $18K/yr  |
| Error rate        | 3.5%    | 0.5%      | $12K/yr  |
| Customer sat      | 72%     | 90%       | Retention|

INVESTMENT: $45,000
ANNUAL SAVINGS: $30,000
PAYBACK: 18 months

---
Gaps: Need actual infrastructure costs from Emily
Saved: Annotation created on Northwind opportunity
```

## Troubleshooting

### Error: Opportunity not found
**Cause:** Name doesn't match or opportunity is closed
**Solution:**
- Search with partial name
- Include closed opportunities in search
- Present multiple matches for selection

### Error: Insufficient context for asset
**Cause:** Opportunity missing key fields (pain points, products, etc.)
**Solution:**
- Note missing data in output
- Generate with available data, mark gaps
- Suggest fields to populate for better assets

### Error: No products attached to opportunity
**Cause:** opportunityproduct records not created
**Solution:**
- Ask user for product information
- Check if products exist at account level
- Generate asset without pricing details, flag for follow-up
