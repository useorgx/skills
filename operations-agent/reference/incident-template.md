# Blameless Postmortem Template

Copy this template for every P1 and P2 incident. P3/P4 incidents may use a shortened version (skip Coaching Questions and Contributing Factors sections).

---

## Incident: [INC-YYYY-NNNN] — [Short descriptive title]

### Metadata

- **Incident ID**: INC-YYYY-NNNN
- **Title**: [One-line description of what happened]
- **Severity**: P1 | P2 | P3 | P4
- **Started At**: [ISO 8601 timestamp]
- **Detected At**: [ISO 8601 timestamp]
- **Resolved At**: [ISO 8601 timestamp]
- **Duration**: [X minutes/hours]
- **Author**: [Name]
- **Reviewers**: [Names of people who reviewed this postmortem]
- **Status**: Draft | In Review | Complete

---

### Impact

**Description**: [What happened from the user's perspective. What could they not do? What errors did they see?]

**Users Affected**: [Number and segment. "All users" or "Enterprise tier users in EU region" etc.]

**Revenue Impact**: [Estimated dollar amount, or "Not estimated — rationale: [reason]"]

**Downstream Effects**: [Other systems, teams, or customers affected. Support ticket volume, SLA implications, etc.]

---

### Detection

- **Method**: automated_alert | customer_report | internal_discovery | synthetic_monitor
- **Alert Name**: [Name of the alert that fired, if applicable]
- **MTTD (Mean Time to Detect)**: [Minutes from incident start to first alert/report]
- **Detection Gap Analysis**: [Why was detection not faster? What would have caught this sooner?]

---

### Response Metrics

- **MTTD**: [Minutes]
- **MTTR**: [Minutes, from detection to resolution]
- **Time to Identify Root Cause**: [Minutes]
- **Time to Remediate**: [Minutes]

---

### Timeline

Document at least 5 events. Include timestamps for every significant moment. Use ISO 8601 format. Events must be in chronological order.

| Timestamp (UTC) | Event |
|-----------------|-------|
| [HH:MM:SS] | [What happened] |
| [HH:MM:SS] | [What happened] |
| [HH:MM:SS] | [What happened] |
| [HH:MM:SS] | [What happened] |
| [HH:MM:SS] | [What happened] |

**Tips for a good timeline:**
- Include the triggering event (deploy, config change, traffic spike, etc.)
- Include the moment the problem became user-visible
- Include the moment of detection (alert, customer report)
- Include key investigation steps and what was learned at each step
- Include the remediation action and when it took effect
- Include the moment the system returned to normal

---

### Root Cause

**Category**: code_defect | configuration | capacity | dependency | process | unknown

**Description**: [Detailed description, minimum 100 characters. Explain the mechanism of failure, not just the symptom. What specifically broke and why.]

**Five Whys Analysis**:

1. **Why did [symptom]?** Because [immediate cause].
2. **Why did [immediate cause]?** Because [deeper cause].
3. **Why did [deeper cause]?** Because [still deeper cause].
4. **Why did [still deeper cause]?** Because [systemic cause].
5. **Why did [systemic cause]?** Because [organizational/process gap].

**Guidance**: Keep asking "why" until you reach a systemic or process-level cause. If your final "why" names a person ("because Sarah did X"), ask one more why ("why did the system allow X to happen without a safety check?").

---

### Contributing Factors (Swiss Cheese Model)

Map the defensive layers that had holes. An incident occurs when holes in multiple layers align.

| Layer | Expected Defense | What Failed (The Hole) |
|-------|-----------------|----------------------|
| Code Review | [What review should have caught] | [Why it was missed] |
| Automated Testing | [What tests should have caught] | [Why the test gap exists] |
| Staging/Pre-production | [What staging should have revealed] | [Why staging did not catch it] |
| Monitoring/Alerting | [What monitoring should have detected] | [Why detection was delayed or absent] |
| Incident Response | [How response should have worked] | [Where response was slower or less effective than expected] |
| Rollback/Recovery | [How recovery should have worked] | [Why recovery took longer than expected] |

**Which layer actually caught the problem?** [Identify which defense finally worked and how.]

**Where did we get lucky?** [What almost made this worse but didn't? What saved us that we should not count on next time?]

---

### Action Items

Every action item must have a named owner (person, not team) and a due date. Prioritize by impact on preventing recurrence.

| ID | Action | Owner | Due Date | Priority | Status |
|----|--------|-------|----------|----------|--------|
| AI-NNNN-1 | [Specific, verifiable action] | [Name] | [YYYY-MM-DD] | P1 | Open |
| AI-NNNN-2 | [Specific, verifiable action] | [Name] | [YYYY-MM-DD] | P1 | Open |
| AI-NNNN-3 | [Specific, verifiable action] | [Name] | [YYYY-MM-DD] | P2 | Open |

**Action item quality checklist:**
- [ ] Action is specific and verifiable (you can confirm it was done)
- [ ] Action addresses a hole in the Swiss Cheese model, not just the root cause
- [ ] Owner is a named person, not a team
- [ ] Due date is realistic and within 30 days for P1, 60 days for P2
- [ ] At least one action item addresses detection (how to catch this faster)
- [ ] At least one action item addresses prevention (how to stop this from happening)
- [ ] At least one action item addresses recovery (how to recover faster if it happens again)

---

### Lessons Learned

Document at least 2 lessons. Focus on systemic insights, not individual actions.

1. **[Lesson title]**: [What we learned and why it matters for future reliability.]
2. **[Lesson title]**: [What we learned and why it matters for future reliability.]

**Guidance for good lessons:**
- A good lesson changes how you think about a class of problems, not just this one incident.
- "We should monitor X" is a weak lesson. "Our monitoring strategy does not account for [category of failure]" is a strong lesson.
- If the lesson is "be more careful," you have not found a real lesson. What system change would make "being careful" unnecessary?

---

### Coaching Questions (For Team Retrospective)

Use these questions to facilitate a team discussion. The goal is to surface systemic improvements, not to review the incident itself.

- How many other systems are vulnerable to this same failure mode? Should we audit them?
- If this happened at 3 AM on a holiday weekend with our most junior on-call, what would the outcome have been? What changes would make the outcome the same regardless of who responds?
- What information did the responder need that was not immediately available? How can we make that information faster to access?
- Was there a moment during the incident where the responder had to make a judgment call? Can we encode that judgment into a runbook or automation?
- What is the earliest point in the development/deployment pipeline where this could have been caught?
- If we had unlimited budget, what would we build to prevent this class of incident? What is the 80/20 version of that?

---

### Appendix (Optional)

Include supporting data that does not fit in the main sections:

- **Dashboard screenshots**: Monitoring data from during the incident
- **Log excerpts**: Key log entries that aided diagnosis (redact sensitive data)
- **Configuration diffs**: Changes that contributed to the incident
- **Related incidents**: Links to prior postmortems for similar issues

---

## Blameless Language Reference

When writing this postmortem, avoid these patterns:

| Blameful Pattern | Blameless Alternative |
|-----------------|----------------------|
| "[Person] forgot to..." | "The process did not include a check for..." |
| "[Person] should have..." | "The system did not surface information about..." |
| "[Person] failed to..." | "The [tool/process] did not prevent..." |
| "If [person] had..." | "If the system had [automated check/alert]..." |
| "Human error" | "The interface/process allowed an unintended action" |
| "[Person] made a mistake" | "The configuration was changed without [safety mechanism]" |
| "Negligence" | "The operating procedure did not account for this scenario" |
| "Carelessness" | "The system lacked guardrails for this operation" |

**The test**: Replace every person's name with "the system" or "the process." If the sentence still makes sense and still suggests a fix, it is blameless.

---

## Review Checklist (Before Marking Complete)

- [ ] All metadata fields filled in
- [ ] Impact quantified (users, revenue, downstream)
- [ ] Timeline has >= 5 events in chronological order
- [ ] Root cause description >= 100 characters
- [ ] Root cause category assigned
- [ ] Five Whys reaches a systemic cause (not a person)
- [ ] Contributing factors map at least 3 Swiss Cheese layers
- [ ] Action items >= 3 with named owners and due dates
- [ ] At least one action item for detection, prevention, and recovery
- [ ] Lessons learned >= 2 with systemic insights
- [ ] No blameful language (run text search for: fault, blame, failed to, should have, mistake, negligence, careless)
- [ ] Reviewed by at least one person who was not involved in the incident
- [ ] Coaching questions prepared for team retrospective
