# RACI Matrix Template

Use this template for any initiative involving 3 or more agents. The RACI matrix eliminates ambiguity in who does what by assigning exactly one of four roles to each agent for each task or decision.

---

## Roles

| Role | Symbol | Definition | Rules |
|------|--------|-----------|-------|
| **Responsible** | R | Does the work. Produces the deliverable. | Can be multiple agents per task. At least one R per task. |
| **Accountable** | A | Owns the outcome. Has final decision authority. Signs off on completion. | Exactly ONE per task. Cannot be delegated. The A can also be R. |
| **Consulted** | C | Provides input BEFORE the work or decision. Two-way communication. | Minimize C entries. Each C adds communication overhead. Only include agents whose input actually changes the outcome. |
| **Informed** | I | Notified AFTER the work or decision. One-way communication. | Use for agents who need awareness but not influence. Async notification is sufficient. |

---

## Initiative-Level RACI Template

Fill in one row per workstream or major decision. Fill in one column per participating agent.

### Example: Workspace Analytics Dashboard Initiative

| Task / Decision | Orchestrator | Product | Engineering | Design | Marketing | Sales |
|----------------|:---:|:---:|:---:|:---:|:---:|:---:|
| Initiative planning and coordination | A/R | C | C | I | I | I |
| PRD and user requirements | I | A/R | C | C | I | C |
| UI/UX design and prototyping | I | C | C | A/R | I | I |
| Backend API and data pipeline | I | I | A/R | C | I | I |
| Launch communications | I | C | I | C | A/R | C |
| Sales enablement materials | I | C | I | I | C | A/R |
| Cross-domain synthesis | A/R | C | C | C | C | I |
| Risk register maintenance | A/R | I | C | I | I | I |
| Stakeholder updates | A/R | C | I | I | I | I |
| Go/no-go launch decision | A | C | C | C | C | C |
| Post-launch retrospective | A/R | R | R | R | R | R |

---

## Blank Template

Copy this template for your initiative. Replace column headers with participating agents. Add rows for each workstream, milestone, or major decision.

| Task / Decision | Agent 1 | Agent 2 | Agent 3 | Agent 4 | Agent 5 | Agent 6 |
|----------------|:---:|:---:|:---:|:---:|:---:|:---:|
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |

---

## Validation Rules

After completing the RACI matrix, verify these rules. Violations are hard blockers — fix before proceeding.

### Rule 1: Exactly One Accountable Per Row
Every task or decision must have exactly one A. If a row has zero A entries, nobody owns the outcome and it will fall through the cracks. If a row has two A entries, accountability is diffused and neither person truly owns it.

**Common mistake**: Marking both the orchestrator and a domain agent as A for the same workstream. The domain agent should be A for their workstream. The orchestrator is A for the initiative, not individual workstreams.

### Rule 2: At Least One Responsible Per Row
Every task must have at least one R. If nobody is doing the work, the task will not get done.

**Common mistake**: Having an A without an R. Accountability without execution is delegation without assignment.

### Rule 3: Minimize Consulted Entries
Each C entry adds a communication dependency. Before the work can proceed, the Responsible agent must consult the C agent and incorporate their input. Too many C entries slow everything down.

**Test**: For each C entry, ask: "Would the outcome be meaningfully different without this agent's input?" If no, change C to I.

### Rule 4: No Empty Rows
Every row must have at least one entry. A task with no assignments is not a task — it is a wish.

### Rule 5: No Empty Columns
Every agent column must have at least one entry. An agent with no assignments should not be participating in the initiative. Remove them to reduce coordination overhead.

---

## Decision RACI vs. Task RACI

The RACI matrix can be used for both tasks (work to be done) and decisions (choices to be made). The distinction matters:

### Task RACI
- R = does the work
- A = approves the deliverable
- C = provides input that shapes the work
- I = receives the deliverable when complete

### Decision RACI
- R = gathers information and prepares the decision
- A = makes the final call
- C = provides input that influences the decision (consulted BEFORE)
- I = is informed of the decision (notified AFTER)

**Example**: "Choose between WebSocket and SSE for real-time updates"
- R: engineering-agent (prepares technical comparison)
- A: orchestrator-agent (makes the call based on initiative constraints)
- C: design-agent (their requirements affect the choice), product-agent (latency requirements)
- I: marketing-agent, sales-agent (need to know but do not influence the technical decision)

---

## Escalation Matrix

Pair the RACI with an escalation matrix for when things go wrong.

| Situation | First Escalation | Second Escalation | Decision Deadline |
|-----------|-----------------|-------------------|-------------------|
| Agent misses checkpoint | Orchestrator contacts agent directly | Orchestrator flags in stakeholder update | 24 hours |
| Two agents disagree on approach | Orchestrator facilitates tradeoff discussion | Escalate to initiative owner | 48 hours |
| Resource conflict between initiatives | Orchestrator negotiates with other initiative's orchestrator | Escalate to program-level owner | 72 hours |
| Scope change requested | Orchestrator evaluates against success metrics | Escalate to initiative owner if metrics are affected | 48 hours |
| External dependency delayed | Orchestrator adjusts plan and communicates impact | Escalate to stakeholder if deadline is affected | 24 hours |

---

## Tips for Effective RACI

1. **Build it early**: Create the RACI during initiative planning, not after work has started. Discovering role confusion mid-initiative is expensive.

2. **Review it with all agents**: Share the RACI with every participating agent and ask them to confirm their assignments. Assumptions about roles are the #1 source of coordination failure.

3. **Update it when scope changes**: When work is added, removed, or reassigned, update the RACI. A stale RACI is worse than no RACI because it creates false confidence.

4. **Keep it visible**: The RACI should be linked from the initiative entity in OrgX. Any agent should be able to answer "who is accountable for X?" in under 30 seconds.

5. **Use it for conflict resolution**: When two agents disagree, check the RACI. The Accountable agent has final decision authority. If the disagreement is between two R agents, the A agent breaks the tie.
