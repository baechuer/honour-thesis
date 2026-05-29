---
name: privacy-risk-reviewer
description: Reviews data collection, retention, sharing, consent, logging, PII exposure, and user-data handling for privacy and compliance-style risk.
---

# Privacy Risk Reviewer

Reviews privacy and user-data handling risk.

## Use when

- The user asks about privacy, personal data, PII, consent, retention, logs, user tracking, or data sharing.
- The task focuses on how user data is collected, stored, exposed, retained, or communicated.
- The output should identify privacy risks and practical mitigations.

## Not for

- Code-level vulnerability review unrelated to personal data.
- General security misuse mapping across protected assets, external actors, component boundaries, abuse scenarios, mitigations, and residual risk when the main concern is not personal data handling.
- Protected assets, external actors, component boundaries, abuse scenarios, security assumptions, mitigations, detection ideas, and residual risk as a general security design exercise.
- Dependency or package risk audits.
- Secret scanning only.
- Authentication logic review as the main task.

## Preconditions

- The user provides a feature design, code path, dependency context, diff, auth flow, logs, or data-handling description.
- The user indicates whether the concern is threat modeling, code vulnerability, dependency risk, secrets, auth, or privacy.

## Workflow

1. Identify data types, users, collection points, storage, sharing, retention, and deletion behavior.
2. Separate sensitive data, personal data, and operational metadata.
3. Check whether collection and exposure are necessary, minimized, and explainable.
4. Identify logging, analytics, retention, consent, and third-party sharing risks.
5. Recommend practical privacy mitigations and open questions.

## Output pattern

- Privacy-risk findings.
- Data collection, retention, sharing, or logging concerns.
- Practical mitigations and open questions.

## Writing rules

- Avoid pretending to give legal advice.
- Be concrete about data flows and exposure points.
- Distinguish privacy risk from general security risk.
- Use `references/privacy_review_axes.md` when a checklist is useful.
