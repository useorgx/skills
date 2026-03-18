# Delegation Template

Use this template for every delegation the orchestrator sends to a domain agent. All 7 sections are required. A delegation missing any section is incomplete and must not be sent.

---

## Template

```json
{
  "target_agent": "<agent-name>",
  "context": {
    "background": "<Why this work matters. Link to initiative success metrics and strategic objective. Minimum 50 characters. The receiving agent should understand not just WHAT to do but WHY it matters.>",
    "initiative_id": "<parent initiative ID>",
    "initiative_success_metrics": ["<metric 1>", "<metric 2>"]
  },
  "task": {
    "objective": "<What 'done' looks like in measurable terms. Not 'build the feature' but 'deliver X with Y measurable property by Z date.'>",
    "requirements": [
      "<Requirement 1: specific, testable>",
      "<Requirement 2: specific, testable>"
    ],
    "scope": {
      "in_scope": [
        "<Item 1: work the agent should do>",
        "<Item 2: work the agent should do>"
      ],
      "out_of_scope": [
        "<Item 1: genuinely tempting work the agent should NOT do>",
        "<Item 2: genuinely tempting work the agent should NOT do>"
      ]
    }
  },
  "quality": {
    "acceptance_criteria": [
      "<Criterion 1: testable condition. Could a script verify this?>",
      "<Criterion 2: testable condition. Could a script verify this?>"
    ]
  },
  "timeline": {
    "deadline": "<YYYY-MM-DD>",
    "deadline_rationale": "<Why this date. What downstream work depends on it.>",
    "checkpoints": [
      {
        "date": "<YYYY-MM-DD>",
        "expected_deliverable": "<What should exist at this checkpoint>",
        "purpose": "<Why this checkpoint matters>"
      }
    ]
  },
  "dependencies": {
    "needs_from_others": [
      {
        "agent": "<agent-name>",
        "what": "<specific deliverable needed>",
        "expected_date": "<YYYY-MM-DD>",
        "status": "<delivered | in_progress | not_started>"
      }
    ],
    "others_need": [
      {
        "agent": "<agent-name>",
        "what": "<specific deliverable this agent must produce>",
        "needed_by": "<YYYY-MM-DD>"
      }
    ]
  },
  "escalation": {
    "path": "<When to escalate, how to escalate, what information to include>",
    "contact": "<Who to contact and via what channel>",
    "response_time": "<Expected response time>"
  },
  "handoff": {
    "output_format": "<Specific format of deliverables: RFC, deployed service, document, etc.>",
    "completion_signal": "<How the agent signals completion: entity action, activity emission, etc.>"
  }
}
```

---

## Quality Checklist

Run this checklist before sending any delegation. Every item must be checked.

### Context (Section 1 of 7)
- [ ] Background explains WHY this work matters, not just WHAT the work is
- [ ] Initiative ID links this work to the parent initiative
- [ ] Success metrics are included so the agent can make informed tradeoff decisions
- [ ] Background is at least 50 characters (not a one-liner)

### Objective (Section 2 of 7)
- [ ] Objective is measurable — someone could objectively verify "done"
- [ ] Objective specifies the deliverable, not just the activity ("deliver an RFC" not "research the problem")
- [ ] Objective includes quantitative criteria where applicable (performance targets, coverage thresholds)

### Scope (Section 3 of 7)
- [ ] In-scope items are complete — nothing the agent needs to build is missing
- [ ] Out-of-scope items are genuinely tempting (things the agent might reasonably attempt)
- [ ] Out-of-scope items are NOT strawmen (obviously unrelated work listed for padding)
- [ ] The boundary between in-scope and out-of-scope is clear — no ambiguous items

### Acceptance Criteria (Section 4 of 7)
- [ ] At least 2 acceptance criteria are defined
- [ ] Each criterion is testable (could a script, test suite, or objective reviewer verify it?)
- [ ] Criteria are specific enough that two people would agree on pass/fail
- [ ] Criteria cover both functional requirements and quality requirements (performance, documentation, testing)

### Deadline (Section 5 of 7)
- [ ] Deadline is a specific date (YYYY-MM-DD), not "as soon as possible" or "next sprint"
- [ ] Rationale explains why this date — what downstream work depends on it
- [ ] At least one intermediate checkpoint is defined
- [ ] Checkpoint has an expected deliverable and purpose (not just a date)

### Dependencies (Section 6 of 7)
- [ ] Incoming dependencies list what the agent needs from others
- [ ] Incoming dependencies include expected delivery dates and current status
- [ ] Outgoing dependencies list what others need from this agent
- [ ] Outgoing dependencies include the date by which the output is needed
- [ ] Any dependency currently at risk is flagged with a note

### Escalation Path (Section 7 of 7)
- [ ] Escalation trigger is defined (how long blocked before escalating)
- [ ] Escalation channel is specified (how to reach the orchestrator)
- [ ] Required escalation information is listed (what to include in the escalation)
- [ ] Expected response time is stated
- [ ] Common escalation scenarios are pre-identified where possible

---

## Common Delegation Failures

These are the most frequent ways delegations fail. Check your delegation against each one.

### Failure: Vague Objective
- **Bad**: "Build the analytics backend"
- **Good**: "Deliver REST API endpoints for agent activity, decision history, and outcome metrics with <200ms p95 response time, deployed to staging by April 22"
- **Why it matters**: Vague objectives lead to rework. The agent builds something, but not the right something. Each revision cycle costs days.

### Failure: Missing Out-of-Scope
- **Bad**: Only in-scope items listed
- **Good**: In-scope AND out-of-scope, where out-of-scope items are genuinely tempting
- **Why it matters**: Without explicit boundaries, ambitious agents expand scope. Well-intentioned scope creep is still scope creep. It delays the critical path.

### Failure: Untestable Acceptance Criteria
- **Bad**: "The API should be well-documented"
- **Good**: "API documentation is published as an OpenAPI spec and the marketing-agent confirms it is sufficient for developer content"
- **Why it matters**: If two people can disagree on whether a criterion is met, it is not a criterion — it is an opinion. Untestable criteria create conflict at handoff.

### Failure: Deadline Without Rationale
- **Bad**: "Due April 29"
- **Good**: "Due April 29 because marketing press coverage is scheduled for launch day and sales enablement training requires 1 week with staging, which means staging must be ready by April 22"
- **Why it matters**: Without rationale, the agent treats the deadline as negotiable. With rationale, the agent understands the consequences of delay and can propose alternatives that preserve the constraint.

### Failure: One-Way Dependencies
- **Bad**: Only listing what the agent needs from others
- **Good**: Listing both what the agent needs AND what others need from the agent
- **Why it matters**: An agent that does not know who depends on their output will optimize for their own timeline, not the initiative timeline. Knowing that "sales-agent needs staging by April 22" changes how engineering-agent prioritizes their work.

### Failure: No Escalation Path
- **Bad**: "Reach out if you need anything"
- **Good**: "If blocked for >24 hours on a critical-path item, escalate via activity emission with urgency:high, including: what is blocked, what has been tried, what is needed, timeline impact. Response within 4 hours."
- **Why it matters**: Without a clear escalation path, agents either suffer in silence (delaying the initiative) or escalate everything (overwhelming the orchestrator). A clear path with thresholds prevents both failure modes.
