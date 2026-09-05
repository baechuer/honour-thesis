# Draft grounded skill clusters and confusable test cases

This note turns the current thesis idea into a more concrete benchmark draft.

The main rule is:

- skills should look similar at the metadata level
- but differ procedurally in at least one meaningful way
- wrong selection should still produce a plausible response, but the wrong artifact, workflow, or success condition

## Procedural difference axes

Use these axes to justify why two skills are not interchangeable:

| Axis | What differs | Example |
|---|---|---|
| Input | What the skill expects as starting material | raw paper vs multiple paper notes |
| Output | What artifact the skill should produce | summary vs structured bibliography entry |
| Workflow | What steps the skill should perform | summarize vs compare vs synthesize |
| Preconditions | What must already be true | meeting not yet happened vs meeting already happened |
| Success criterion | What counts as a good result | concise summary vs actionable task list |
| Side effects | What the skill changes or triggers | classify email vs draft a reply |

## Category and skill table

These are candidate benchmark skills after filtering for a stricter requirement:

- the skills should still look plausibly similar from the `name + description` layer
- they should differ in a way that changes the correct procedure
- the prompt should be able to make one of them the gold skill without naming the skill directly

Some earlier ideas, especially a few writing/editing cases, were too easy or too fuzzy. The table below keeps the stronger candidates.

| Category | Skill | Candidate description-style surface | Main procedural differentiator | Likely confusable with | Why wrong selection matters | Similar public skill to inspect |
|---|---|---|---|---|---|---|
| Reading / research | paper-summariser | Process a research paper into concise notes for later reference. | Output | citation-note-extractor, method-note-builder, related-work-synthesiser | user gets general notes instead of citation-ready, method-focused, or synthesis-ready output | `summarize` ([SkillsAuth](https://skillsauth.com/skills/steipete/summarize)) |
| Reading / research | citation-note-extractor | Process a research paper into reusable citation notes for later writing. | Output / success criterion | paper-summariser, method-note-builder | user needs structured citation-oriented notes, not a broad summary | `citations-retrieval` ([SkillsAuth](https://skillsauth.com/skills/markus41/citations-retrieval)) |
| Reading / research | method-note-builder | Process a research paper into notes that support later method comparison. | Output / workflow | paper-summariser, citation-note-extractor, related-work-synthesiser | method details and comparable dimensions get lost if the wrong note type is produced | `lit-review` ([SkillsAuth](https://skillsauth.com/skills/tesseract-ripple/lit-review)) |
| Reading / research | related-work-synthesiser | Turn paper notes into reusable related-work prose or synthesis points. | Input / output | paper-summariser, citation-note-extractor, method-note-builder | user needs draftable synthesis, not isolated notes on one paper | `literature-review` ([Skills Directory](https://www.skillsdirectory.com/skills/hxk622-literature-review)) |
| Reading / research | general-source-summariser | Process an article, URL, report, or local document into concise reusable notes. | Input target / output | paper-summariser, citation-note-extractor, document-field-extractor | broader source wording may wrongly win over a paper-specific skill | `summarize` ([SkillsAuth](https://skillsauth.com/skills/steipete/summarize)) |
| Reading / research | document-extractor | Process a document or source into structured extracted content for later use. | Output / workflow | citation-note-extractor, general-source-summariser, document-field-extractor | user may need citation-oriented paper notes, not generic extracted structure | `ocr-and-documents` ([SkillsAuth](https://skillsauth.com/skills/nousresearch/ocr-and-documents)), `mineru-extract` ([SkillsAuth](https://skillsauth.com/skills/aaaaqwq-agi-super-team-skills-mineru-extract)) |
| Reading / research | citation-grounding-helper | Extract source-attributable facts, references, or grounded support from a document or source. | Success criterion | citation-note-extractor, general-source-summariser, related-work-synthesiser | grounded citation support may be confused with general summarisation or note extraction | `citations-retrieval` ([SkillsAuth](https://skillsauth.com/skills/markus41/citations-retrieval)) |
| Reading / research | multi-source-comparison-builder | Turn multiple papers, articles, or source notes into structured comparison points. | Input / workflow | method-note-builder, related-work-synthesiser, general-source-summariser | user may need cross-source comparison, not a one-source summary or prose synthesis | `tabular-review-lawvable` ([SkillsAuth](https://skillsauth.com/skills/lawvable-awesome-legal-skills-skills-tabular-review-lawvable)), `lit-review` ([SkillsAuth](https://skillsauth.com/skills/tesseract-ripple/lit-review)) |
| Reply / messaging | reply-drafter | Turn message or email context into a sendable reply draft. | Output | reply-polisher, professor-email-reply, groupwork-reply, followup-reply-writer | user needs a fresh reply, not a polished existing draft or specialized coordination/follow-up response | `himalaya` ([SkillsAuth](https://skillsauth.com/skills/nousresearch/himalaya)), `agentmail` ([SkillsAuth](https://skillsauth.com/skills/nousresearch/agentmail)) |
| Reply / messaging | reply-polisher | Turn an existing reply draft into a clearer, more professional, or more appropriate message. | Input / workflow | reply-drafter, professor-email-reply | wrong selection may rewrite from scratch instead of refining the draft | `himalaya` ([SkillsAuth](https://skillsauth.com/skills/aaaaqwq/himalaya)) |
| Reply / messaging | professor-email-reply | Turn academic email context into a respectful, well-structured reply suitable for a lecturer, supervisor, or professor. | Recipient / success criterion | reply-drafter, reply-polisher, followup-reply-writer | user needs academic etiquette and structure, not only a generic professional reply | `himalaya` ([SkillsAuth](https://skillsauth.com/skills/nousresearch/himalaya)) |
| Reply / messaging | groupwork-reply | Turn group-project chat or email context into a reply about coordination, deadlines, ownership, or progress. | Recipient / workflow | reply-drafter, followup-reply-writer, task-extractor | user needs coordination-focused communication, not a generic reply | `imsg` ([SkillsAuth](https://skillsauth.com/skills/openclaw/imsg)), `Email Classifier` ([SkillsAuth](https://skillsauth.com/skills/305s-magicallesson-qoder-skills-email-classifier)) |
| Reply / messaging | followup-reply-writer | Turn message or meeting context into a reply that clearly states next actions, commitments, or clarifications. | Success criterion | reply-drafter, groupwork-reply, professor-email-reply | user needs a commitment/action-oriented response, not only a polite reply | `Email Classifier` ([SkillsAuth](https://skillsauth.com/skills/305s-magicallesson-qoder-skills-email-classifier)) |
| Email / communication | email-drafter | Turn email context into a sendable reply or fresh draft. | Output | email-polisher, email-thread-summariser, email-action-extractor | user needs a sendable email, not notes or action items | `himalaya` ([SkillsAuth](https://skillsauth.com/skills/nousresearch/himalaya)) |
| Email / communication | email-polisher | Turn an existing email draft into a clearer or more professional message. | Input / workflow | email-drafter, email-thread-summariser | wrong selection may rewrite from scratch or summarize rather than refine the draft | `himalaya` ([SkillsAuth](https://skillsauth.com/skills/aaaaqwq/himalaya)) |
| Email / communication | email-thread-summariser | Turn an email thread into a concise summary of issues, decisions, and context. | Output | email-action-extractor, email-drafter | user needs compact thread understanding, not a reply or task list | `Email Classifier` ([SkillsAuth](https://skillsauth.com/skills/305s-magicallesson-qoder-skills-email-classifier)) |
| Email / communication | email-action-extractor | Turn an email thread into tasks, owners, and deadlines. | Output / success criterion | email-thread-summariser, email-drafter | user needs obligations and next steps, not prose summary or reply text | `Email Classifier` ([SkillsAuth](https://skillsauth.com/skills/305s-magicallesson-qoder-skills-email-classifier)) |
| Planning / meetings | task-extractor | Turn notes, email, or rough text into a concrete task list. | Input / output | weekly-planner, meeting-followup-extractor | user needs extraction before prioritization or scheduling can happen | `add-task` ([SkillsAuth](https://skillsauth.com/skills/ahmadelswify/add-task)) |
| Planning / meetings | weekly-planner | Turn tasks and deadlines into a workable plan for the week. | Input / output | task-extractor, meeting-followup-extractor | user needs calendarized execution, not a raw list of tasks | `taskflow` ([SkillsAuth](https://skillsauth.com/skills/steipete-taskflow)) |
| Planning / meetings | meeting-agenda-builder | Turn meeting context into a structured agenda for discussion. | Preconditions / output | meeting-summary-writer, meeting-followup-extractor | wrong skill assumes the meeting already happened | no strong public match found yet |
| Planning / meetings | meeting-summary-writer | Turn meeting notes into a concise record of discussion and decisions. | Preconditions / output | meeting-followup-extractor, meeting-agenda-builder | user needs minutes/record, not agenda or action-only output | `meeting-minutes` ([SkillsAuth](https://skillsauth.com/skills/github-awesome-copilot-skills-meeting-minutes)) |
| Planning / meetings | meeting-followup-extractor | Turn meeting notes into decisions, action items, and next steps. | Preconditions / success criterion | meeting-summary-writer, task-extractor | user needs next actions, not just narrative minutes | `meeting-minutes` ([SkillsAuth](https://skillsauth.com/skills/github-awesome-copilot-skills-meeting-minutes)) |
| Documents / files | document-summariser | Process a document into concise notes for later reference. | Output | document-field-extractor, document-rewriter, document-converter | user gets notes instead of structured fields, rewritten output, or a converted artifact | `pdf` ([Anthropic official](https://github.com/anthropics/skills/blob/main/skills/pdf/SKILL.md)), `docx` ([Anthropic official](https://github.com/anthropics/skills/blob/main/skills/docx/SKILL.md)) |
| Documents / files | document-field-extractor | Process a document into structured fields or reusable extracted information. | Output / success criterion | document-summariser, document-rewriter | key structure is lost if the skill returns only free-form notes | `pdf` ([Anthropic official](https://github.com/anthropics/skills/blob/main/skills/pdf/SKILL.md)) |
| Documents / files | document-rewriter | Turn an existing document into a cleaner or more polished version. | Workflow / output | document-summariser, document-converter | user needs revised content, not notes or a format-only transformation | `docx` ([Anthropic official](https://github.com/anthropics/skills/blob/main/skills/docx/SKILL.md)) |
| Documents / files | document-converter | Turn a document into another output format while preserving useful structure. | Output artifact | document-rewriter, document-field-extractor | user needs a converted artifact, not extracted notes or rewritten prose | `pdf` ([Anthropic official](https://github.com/anthropics/skills/blob/main/skills/pdf/SKILL.md)), `pptx` ([Anthropic official](https://github.com/anthropics/skills/blob/main/skills/pptx/SKILL.md)), `xlsx` ([Anthropic official](https://github.com/anthropics/skills/blob/main/skills/xlsx/SKILL.md)) |
| Documents / files | layout-preserving-converter | Turn a document into another usable format while keeping important layout and structure intact. | Output artifact / success criterion | document-converter, document-rewriter, document-field-extractor | wrong selection may preserve content but lose layout or editability | `pdf` ([Anthropic official](https://github.com/anthropics/skills/blob/main/skills/pdf/SKILL.md)), `docx` ([Anthropic official](https://github.com/anthropics/skills/blob/main/skills/docx/SKILL.md)) |
| Documents / files | document-normaliser | Turn a messy or inconsistent document into a cleaner standardized working version. | Workflow / success criterion | document-rewriter, document-converter, document-field-extractor | user may need normalization rather than extraction or format conversion | `ocr-and-documents` ([SkillsAuth](https://skillsauth.com/skills/nousresearch/ocr-and-documents)), `mineru-extract` ([SkillsAuth](https://skillsauth.com/skills/aaaaqwq-agi-super-team-skills-mineru-extract)) |
| Documents / files | multi-document-comparison-preparer | Turn multiple documents into aligned structured outputs for side-by-side comparison. | Input / workflow | document-field-extractor, document-summariser, document-normaliser | user may need cross-document preparation, not one-document extraction or summary | `tabular-review-lawvable` ([SkillsAuth](https://skillsauth.com/skills/lawvable-awesome-legal-skills-skills-tabular-review-lawvable)) |
| Data / spreadsheet | data-analysis-overview | Analyse a spreadsheet and return a concise overview of what it contains. | Output | data-analysis-with-validation, data-analysis-with-anomaly-focus, data-analysis-for-reporting, data-analysis-for-forecasting | user gets descriptive overview instead of validation, diagnosis, report text, or forward-looking output | `xlsx` ([Anthropic official](https://github.com/anthropics/skills/blob/main/skills/xlsx/SKILL.md)) |
| Data / spreadsheet | data-analysis-with-validation | Analyse a spreadsheet, but first verify whether it is reliable enough to use. | Workflow / preconditions | data-analysis-overview, data-analysis-with-anomaly-focus | wrong selection may trust dirty data or skip a validation step before interpretation | `xlsx` ([Anthropic official](https://github.com/anthropics/skills/blob/main/skills/xlsx/SKILL.md)) |
| Data / spreadsheet | data-analysis-with-anomaly-focus | Analyse a spreadsheet and identify what looks unusual or worth attention. | Workflow / success criterion | data-analysis-overview, data-analysis-with-validation, data-analysis-for-reporting | user needs abnormal-pattern diagnosis, not a generic overview or polished report | `xlsx` ([Anthropic official](https://github.com/anthropics/skills/blob/main/skills/xlsx/SKILL.md)) |
| Data / spreadsheet | data-analysis-for-root-cause-diagnosis | Analyse a spreadsheet and explain the likely drivers of a sharp change, drop, spike, or surprising result. | Workflow / success criterion | data-analysis-overview, data-analysis-with-anomaly-focus, data-analysis-for-reporting | user needs explanation of why something happened, not just detection or description | `xlsx` ([Anthropic official](https://github.com/anthropics/skills/blob/main/skills/xlsx/SKILL.md)) |
| Data / spreadsheet | data-analysis-for-reporting | Analyse a spreadsheet and turn the findings into a concise report for someone else to read. | Input / output | data-analysis-overview, data-analysis-with-anomaly-focus, data-analysis-for-forecasting | user needs communicable report text, not only internal analysis notes | `xlsx` ([Anthropic official](https://github.com/anthropics/skills/blob/main/skills/xlsx/SKILL.md)) |
| Data / spreadsheet | data-analysis-for-ranking-selection | Analyse a spreadsheet and identify which options, rows, or candidates are strongest according to the task criteria. | Output / success criterion | data-analysis-overview, data-analysis-for-reporting, data-analysis-with-anomaly-focus | user needs a decision-oriented ranking, not a general report or descriptive overview | `xlsx` ([Anthropic official](https://github.com/anthropics/skills/blob/main/skills/xlsx/SKILL.md)) |
| Data / spreadsheet | data-analysis-for-forecasting | Analyse a spreadsheet and estimate likely future direction or outcomes. | Output / preconditions | data-analysis-overview, data-analysis-with-anomaly-focus, data-analysis-for-reporting | user needs forward-looking output, not description of current state | `xlsx` ([Anthropic official](https://github.com/anthropics/skills/blob/main/skills/xlsx/SKILL.md)) |
| Metrics / observability | metrics-overview | Analyse service, website, or backend metrics and summarize what the key indicators are showing. | Output | latency-anomaly-detector, metrics-root-cause-diagnoser, slo-breach-checker, incident-summary-writer | user gets a general overview instead of diagnosis, compliance-style checking, or incident-ready output | no strong public match found yet |
| Metrics / observability | latency-anomaly-detector | Analyse service metrics and identify unusual spikes, drops, or instability in indicators such as latency, error rate, throughput, or p95/p99. | Workflow / success criterion | metrics-overview, metrics-root-cause-diagnoser, slo-breach-checker | user needs unusual-pattern detection, not just summary or cause explanation | no strong public match found yet |
| Metrics / observability | metrics-root-cause-diagnoser | Analyse service metrics and explain likely drivers of a spike, slowdown, degradation, or surprising backend behavior. | Workflow / success criterion | latency-anomaly-detector, metrics-overview, incident-summary-writer | user needs explanation of why something happened, not only anomaly detection | no strong public match found yet |
| Metrics / observability | slo-breach-checker | Analyse service metrics and determine whether latency, error rate, uptime, or other indicators breach expected thresholds or SLO/SLA targets. | Success criterion / preconditions | latency-anomaly-detector, metrics-overview, capacity-risk-forecaster | user needs rule/threshold evaluation, not just unusualness or trend description | no strong public match found yet |
| Metrics / observability | capacity-risk-forecaster | Analyse service metrics and estimate whether the system is heading toward saturation, overload, or reliability risk. | Output / preconditions | metrics-overview, slo-breach-checker, metrics-root-cause-diagnoser | user needs forward-looking operational risk, not current-state summary only | no strong public match found yet |
| Metrics / observability | incident-summary-writer | Turn service-metric findings into a concise incident update or operational summary for other people to read. | Input / output | metrics-overview, metrics-root-cause-diagnoser, slo-breach-checker | user needs communicable incident text, not raw technical analysis only | no strong public match found yet |
| Meta-skills | skill-finder | Search for an existing skill that already fits a need. | Workflow | skill-manager, skill-creator | user needs discovery, not editing or authoring | Anthropic skills docs ([Claude docs](https://docs.claude.com/en/docs/claude-code/skills)) |
| Meta-skills | skill-manager | Review, update, or clean up installed skills. | Workflow / side effects | skill-finder, skill-creator | user needs maintenance on installed skills, not search or creation | Anthropic skills help article ([Support](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)) |
| Meta-skills | skill-creator | Create a new skill from a repeated workflow or missing capability. | Output / side effects | skill-finder, skill-manager | user needs a new skill artifact, not discovery or maintenance | `skill-creator` ([Anthropic official](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)) |

## Revised confusable prompt set

These prompts are meant to be direct and informative, not vague. The difficulty should come from overlap between plausible skill descriptions, not from hiding the user's goal completely.

### Reading / research prompts

| Prompt | Candidate skills | Gold skill | Main differentiating cue | Why this is still confusable |
|---|---|---|---|---|
| "Summarise this scientific paper into reusable notes for later citation and writing." | paper-summariser, citation-note-extractor, general-source-summariser, citation-grounding-helper | citation-note-extractor | output is citation-ready reusable notes | broad source/document skills still overlap strongly on summarize/extract/reuse wording |
| "Summarise this scientific paper into notes I can reuse when comparing methods later." | paper-summariser, method-note-builder, citation-note-extractor, general-source-summariser | method-note-builder | intended later use is method comparison | one-source summary and broader source-note skills still sound plausible |
| "Turn these paper notes into a paragraph I can adapt for related work." | paper-summariser, citation-note-extractor, related-work-synthesiser, citation-grounding-helper | related-work-synthesiser | input is already notes, output is prose for related work | multiple research-support skills overlap on writing and citation support |
| "Extract the parts of this scientific paper that I may want to cite later." | citation-note-extractor, citation-grounding-helper, general-source-summariser | citation-note-extractor | target is reusable citation material, not generic extraction only | citation-grounding and general source extraction still sound close from metadata |
| "Turn these paper notes into structured comparison points against other sources." | method-note-builder, multi-source-comparison-builder, related-work-synthesiser | multi-source-comparison-builder | output is cross-source comparison structure | all candidates mention notes, sources, and later comparison/synthesis |

### Reply / messaging prompts

| Prompt | Candidate skills | Gold skill | Main differentiating cue | Why this is still confusable |
|---|---|---|---|---|
| "Draft a reply to this message from my professor." | reply-drafter, professor-email-reply, reply-polisher | professor-email-reply | recipient is academic and likely needs formal structure | generic reply drafting and polishing still sound plausible from description alone |
| "Make this reply to my supervisor more professional before I send it." | reply-polisher, professor-email-reply, reply-drafter | reply-polisher | input already is a draft and user wants refinement | supervisor/professor cue still pulls toward the academic-specialized skill |
| "Draft a reply to this group message about deadlines and who is doing what." | groupwork-reply, reply-drafter, followup-reply-writer | groupwork-reply | context is team coordination and responsibility assignment | all three skills involve responding and clarifying next actions |
| "Reply to this message with what I will do next and when." | followup-reply-writer, reply-drafter, groupwork-reply | followup-reply-writer | success criterion is commitments and next actions | generic reply and group coordination skills still sound applicable |

### Email / communication prompts

| Prompt | Candidate skills | Gold skill | Main differentiating cue | Why this is still confusable |
|---|---|---|---|---|
| "Turn this email thread into the actions and deadlines I need to handle." | email-thread-summariser, email-action-extractor, email-drafter | email-action-extractor | success criterion is tasks and deadlines | a summarizer could still look plausible from the description layer |
| "Turn this email thread into a short summary of the key issues and decisions." | email-thread-summariser, email-action-extractor | email-thread-summariser | output is concise context summary | both skills act on a thread and produce condensed information |
| "Turn this email context into a professional reply I can send." | email-drafter, email-polisher, email-thread-summariser | email-drafter | output is a sendable reply built from context | if a draft already exists, email-polisher would also look plausible |
| "Polish this email draft so it is professional but still sounds like me." | email-polisher, email-drafter | email-polisher | input explicitly says draft | both skills mention helping with emails and making them sendable |

### Planning / meetings prompts

| Prompt | Candidate skills | Gold skill | Main differentiating cue | Why this is still confusable |
|---|---|---|---|---|
| "Turn these rough notes into a task list I can work from." | task-extractor, weekly-planner, meeting-followup-extractor | task-extractor | input is rough notes, not already-structured tasks | planners and follow-up skills also promise actionable output |
| "Turn these tasks and deadlines into a realistic plan for this week." | weekly-planner, task-extractor | weekly-planner | tasks already exist and need scheduling | both skills are about organizing work into something usable |
| "Turn this meeting brief into an agenda I can use tomorrow." | meeting-agenda-builder, meeting-summary-writer | meeting-agenda-builder | meeting has not happened yet | both skills can mention meetings and structured output |
| "Turn these meeting notes into a concise record of what was decided." | meeting-summary-writer, meeting-followup-extractor | meeting-summary-writer | output is minutes/record, not next actions only | both skills consume meeting notes and produce structured post-meeting outputs |
| "Turn these meeting notes into the actions I need to take next." | meeting-followup-extractor, meeting-summary-writer, task-extractor | meeting-followup-extractor | success criterion is next actions | summary and generic task extraction are still plausible competitors |

### Documents / files prompts

| Prompt | Candidate skills | Gold skill | Main differentiating cue | Why this is still confusable |
|---|---|---|---|---|
| "Turn this document into structured fields I can reuse later." | document-field-extractor, document-summariser, document-converter | document-field-extractor | output must preserve structure, not just notes | summary and conversion skills also promise document processing |
| "Turn this document into a cleaner version I can send out." | document-rewriter, document-converter, document-summariser | document-rewriter | user wants improved content, not format-only change | multiple document skills sound applicable from metadata |
| "Turn this file into a format I can work with in another tool." | document-converter, document-field-extractor, document-rewriter | document-converter | target outcome is different artifact format | field extraction and rewriting still sound like useful transformations |
| "Turn this PDF into something editable without losing the important structure." | layout-preserving-converter, document-converter, document-rewriter | layout-preserving-converter | editability plus structure preservation | several document-processing skills sound relevant, but layout preservation is key |
| "Turn this document into a cleaner standardized version I can work from." | document-normaliser, document-rewriter, document-converter | document-normaliser | goal is standardization, not just polishing or conversion | normalization overlaps with rewriting and conversion language |
| "Turn these documents into something I can compare side by side." | multi-document-comparison-preparer, document-field-extractor, document-summariser | multi-document-comparison-preparer | input is multiple documents and output is aligned comparison-ready structure | extraction and summary also sound plausible from description layer |

### Documents / files borderline hard cases

These are useful later as stress-test items once the stable cases above are working.

| Prompt | Candidate skills | Likely gold skill | Why it is hard |
|---|---|---|---|
| "Turn this document into a cleaner version with clearer fields." | document-rewriter, document-field-extractor, document-normaliser | document-rewriter or document-field-extractor depending annotation policy | mixes presentation cues with structure cues |
| "Turn this PDF into something cleaner and easier to work with in Word." | document-converter, layout-preserving-converter, document-normaliser | document-converter or layout-preserving-converter depending whether layout preservation is required | combines format conversion with quality/normalization language |

### Data / spreadsheet prompts

| Prompt | Candidate skills | Gold skill | Main differentiating cue | Why this is still confusable |
|---|---|---|---|---|
| "Analyse this spreadsheet and tell me what looks unusual." | data-analysis-with-anomaly-focus, data-analysis-overview, data-analysis-with-validation | data-analysis-with-anomaly-focus | task asks for salient abnormalities | overview or validation still look reasonable from the description layer |
| "Analyse this spreadsheet and tell me if it is reliable enough to use." | data-analysis-with-validation, data-analysis-overview, data-analysis-with-anomaly-focus | data-analysis-with-validation | precondition is validation before use | all three involve inspecting data before action |
| "Analyse this spreadsheet and give me a concise overview of what it shows." | data-analysis-overview, data-analysis-for-reporting, data-analysis-with-anomaly-focus | data-analysis-overview | output is overview rather than report or diagnosis | "concise overview" still overlaps with report-style skills |
| "Analyse this spreadsheet and explain why this metric changed so sharply." | data-analysis-for-root-cause-diagnosis, data-analysis-with-anomaly-focus, data-analysis-overview | data-analysis-for-root-cause-diagnosis | user wants explanation of cause, not only detection | anomaly and overview skills still look plausible because they also inspect unusual changes |
| "Analyse this spreadsheet and turn the findings into something I can send to my manager." | data-analysis-for-reporting, data-analysis-overview, data-analysis-with-anomaly-focus | data-analysis-for-reporting | output is communicable report text | overview skill still looks tempting because it also produces condensed findings |
| "Analyse this spreadsheet and tell me which options are strongest." | data-analysis-for-ranking-selection, data-analysis-overview, data-analysis-for-reporting | data-analysis-for-ranking-selection | task is decision-oriented ranking, not general description | report and overview skills still sound plausible from broad analysis wording |
| "Analyse this spreadsheet and tell me what it suggests is likely to happen next." | data-analysis-for-forecasting, data-analysis-overview, data-analysis-with-anomaly-focus | data-analysis-for-forecasting | output is forward-looking | general analysis skills still seem plausible from broad descriptions |

### Metrics / observability prompts

| Prompt | Candidate skills | Gold skill | Main differentiating cue | Why this is still confusable |
|---|---|---|---|---|
| "Analyse these backend metrics and tell me what looks unusual." | latency-anomaly-detector, metrics-overview, slo-breach-checker | latency-anomaly-detector | task asks for salient abnormalities in service behavior | overview and threshold-checking skills still sound applicable from description alone |
| "Analyse these backend metrics and explain why p99 jumped so sharply." | metrics-root-cause-diagnoser, latency-anomaly-detector, metrics-overview | metrics-root-cause-diagnoser | user wants explanation of the spike, not just detection | anomaly and overview skills still plausibly inspect the same metrics |
| "Analyse these backend metrics and tell me if we are breaching what we promised." | slo-breach-checker, latency-anomaly-detector, metrics-overview | slo-breach-checker | success criterion is breach against target/SLO, not unusualness only | all three involve looking at service metrics and judging system state |
| "Analyse these backend metrics and tell me if we are heading toward trouble next." | capacity-risk-forecaster, metrics-overview, slo-breach-checker | capacity-risk-forecaster | output is forward-looking operational risk | overview and SLO checking still sound close from broad metrics-analysis wording |
| "Analyse these backend metrics and turn the findings into an incident update." | incident-summary-writer, metrics-overview, metrics-root-cause-diagnoser | incident-summary-writer | output is communicable incident text | overview and diagnosis skills still sound useful from the description layer |

### Meta-skills prompts

| Prompt | Candidate skills | Gold skill | Main differentiating cue | Why this is still confusable |
|---|---|---|---|---|
| "Find whether there is already a skill for this before I try to make one." | skill-finder, skill-creator, skill-manager | skill-finder | workflow is discovery-before-creation | all three skills mention working with skills and improving capability |

## Notes on scope tightening

The strongest benchmark families right now are:

- Reading / research
- Reply / messaging
- Email / communication
- Planning / meetings
- Documents / files
- Data / spreadsheet
- Metrics / observability

The weaker family is general writing/editing. It can still be used later, but it is easier for those skills to become either too obvious or too fuzzy from the description layer. For now, it is better to prioritize the stronger families above.
The metrics / observability family is a useful domain-specific extension because many skills can share the same broad "analyse backend/service metrics" wording while differing only in what they are trying to detect, explain, predict, or communicate.
The reply / messaging family is also useful because many skills can share the same broad "help me reply" wording while differing in recipient type, input state, and communication goal.

## Coverage check

The current candidate set is enough for a strong **confusable core**, but not yet enough for a final large-scale library.

Use it in two layers:

1. **Confusable core**
   - around 20--25 carefully designed skills like the ones above
   - high annotation quality
   - clear procedural differences

2. **Background library**
   - larger set of additional everyday personal-agent skills
   - used to create retrieval pressure and context growth
   - does not need every skill to be equally confusable

The data-analysis family was expanded because it is a particularly good place to create "mostly same workflow, one important step differs" cases. That pattern is likely to produce stronger benchmark examples than only using very broad task differences.

For the reading / research family, the benchmark now includes both:

- paper-specific skills, where the target is clearly a scientific paper
- broader neighboring skills, where the operation vocabulary overlaps but the target is described more generally as a source, article, report, URL, or document

This should create stronger semantic-confusion pressure at the description layer than only comparing paper-specific skills against each other.

## Public skills already worth verifying first-hand

These are the best starting points for hands-on inspection before building custom benchmark skills.

### Official Anthropic examples

- `pdf`: <https://github.com/anthropics/skills/blob/main/skills/pdf/SKILL.md>
- `docx`: <https://github.com/anthropics/skills/blob/main/skills/docx/SKILL.md>
- `pptx`: <https://github.com/anthropics/skills/blob/main/skills/pptx/SKILL.md>
- `xlsx`: <https://github.com/anthropics/skills/blob/main/skills/xlsx/SKILL.md>
- `skill-creator`: <https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md>
- Claude skills docs: <https://docs.claude.com/en/docs/claude-code/skills>
- Custom skill guidance: <https://support.claude.com/en/articles/12512198-how-to-create-custom-skills>

### Community examples that are close enough to inspect

- `literature-review`: <https://www.skillsdirectory.com/skills/hxk622-literature-review>
- `lit-review`: <https://skillsauth.com/skills/tesseract-ripple/lit-review>
- `summarize`: <https://skillsauth.com/skills/steipete/summarize>
- `agentmail`: <https://skillsauth.com/skills/nousresearch/agentmail>
- `himalaya` (nousresearch): <https://skillsauth.com/skills/nousresearch/himalaya>
- `himalaya` (aaaaqwq): <https://skillsauth.com/skills/aaaaqwq/himalaya>
- `imsg`: <https://skillsauth.com/skills/openclaw/imsg>
- `ocr-and-documents`: <https://skillsauth.com/skills/nousresearch/ocr-and-documents>
- `mineru-extract`: <https://skillsauth.com/skills/aaaaqwq-agi-super-team-skills-mineru-extract>
- `citations-retrieval`: <https://skillsauth.com/skills/markus41/citations-retrieval>
- `tabular-review-lawvable`: <https://skillsauth.com/skills/lawvable-awesome-legal-skills-skills-tabular-review-lawvable>
- `add-task`: <https://skillsauth.com/skills/ahmadelswify/add-task>
- `meeting-minutes`: <https://skillsauth.com/skills/github-awesome-copilot-skills-meeting-minutes>
- `Email Classifier`: <https://skillsauth.com/skills/305s-magicallesson-qoder-skills-email-classifier>
- `proofread`: <https://skillsauth.com/skills/tesseract-ripple/proofread>

## Immediate next step

The next refinement pass should do four things:

1. mark which of the candidate skills are truly grounded in your own daily workflow
2. write draft `name + description` metadata for the strongest clusters
3. check whether each prompt is still confusable from those descriptions alone
4. drop or rewrite any case where the gold label is still unstable
