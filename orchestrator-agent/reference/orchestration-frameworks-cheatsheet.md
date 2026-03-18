# Orchestration Frameworks Cheatsheet

Quick reference for the orchestrator agent's coordination frameworks. Use this during planning and execution to select the right framework for the situation.

---

## Framework Selection Guide

| Situation | Primary Framework | Supporting Framework |
|-----------|------------------|---------------------|
| Identifying the initiative bottleneck | Theory of Constraints | Critical Path Method |
| Estimating minimum timeline | Critical Path Method | Dependency Mapping (DAG) |
| Clarifying who does what | RACI Matrix | Two-Pizza Rule |
| Sequencing work across agents | Dependency Mapping (DAG) | Work Breakdown Structure |
| Aligning multiple teams on shared goals | Program Increment Planning | Work Breakdown Structure |
| Decomposing an initiative into tasks | Work Breakdown Structure | Eisenhower Matrix |
| Deciding where to focus orchestrator time | Eisenhower Matrix | Theory of Constraints |
| Responding to a coordination crisis | Boyd's OODA Loop | Tuckman's Team Stages |
| Adapting to a new or immature team | Tuckman's Team Stages | Two-Pizza Rule |
| Evaluating whether to add agents | Brooks's Law | Metcalfe's Law of Meetings |
| Determining maximum workstream size | Two-Pizza Rule | Brooks's Law |
| Minimizing coordination overhead | Metcalfe's Law of Meetings | Two-Pizza Rule |

---

## Framework Summaries

### Theory of Constraints (Goldratt)

**Core idea**: Every system has exactly one bottleneck that limits total throughput.

**Five focusing steps**:
1. **Identify** the constraint (the agent, workstream, or resource that limits initiative throughput)
2. **Exploit** the constraint (ensure the bottleneck is never idle — feed it work constantly)
3. **Subordinate** everything else (other workstreams pace to the bottleneck, not the other way around)
4. **Elevate** the constraint (invest in increasing bottleneck capacity — more resources, better tools, scope reduction)
5. **Repeat** (once this bottleneck is resolved, the next bottleneck emerges — find it)

**Orchestrator application**: At any point during an initiative, you should be able to answer: "What is the current bottleneck?" If you cannot, you are not coordinating — you are administering.

---

### Critical Path Method (CPM)

**Core idea**: The longest chain of dependent tasks determines the minimum possible timeline.

**Steps**:
1. List all tasks with durations and dependencies
2. Build the dependency graph (DAG)
3. Forward pass: calculate earliest start and finish for each task
4. Backward pass: calculate latest start and finish for each task
5. Slack = Latest Start - Earliest Start (tasks with zero slack are on the critical path)

**Key formulas**:
- Earliest Start (ES) = max(Earliest Finish of all predecessors)
- Earliest Finish (EF) = ES + Duration
- Latest Finish (LF) = min(Latest Start of all successors)
- Latest Start (LS) = LF - Duration
- Slack = LS - ES

**Orchestrator application**: Focus on critical-path tasks. Non-critical tasks can slip by their slack amount without affecting the deadline. When the critical path changes (which it does when tasks finish early or late), recalculate.

---

### RACI Matrix

**Core idea**: Eliminate ambiguity in who does what.

**Roles**:
- **R** - Responsible: Does the work. Can be multiple agents.
- **A** - Accountable: Owns the outcome. Exactly ONE per task. Has final decision authority.
- **C** - Consulted: Provides input BEFORE the work or decision. Two-way communication.
- **I** - Informed: Notified AFTER the work or decision. One-way communication.

**Rules**:
- Every row (task/decision) must have exactly one A
- Every row must have at least one R
- The A can also be the R (common for domain-specific work)
- Minimize C entries — each Consulted relationship adds communication overhead
- If everyone is C, nobody is — reduce to the 2-3 agents whose input actually changes the outcome

See `reference/raci-template.md` for the standard template.

---

### Dependency Mapping (DAG)

**Core idea**: Model all work dependencies as a Directed Acyclic Graph.

**Dependency types**:
- **Blocks**: Target cannot start until source completes. Hard constraint.
- **Informs**: Target benefits from source output but can start without it. Soft constraint.
- **Shares_resource**: Both tasks need the same agent or resource. Scheduling constraint.

**Validation rules**:
- No cycles (use DFS cycle detection)
- Every node must be reachable from at least one start node
- Every node must have a path to at least one end node
- Cross-domain edges (dependencies between different agents) require explicit handoff contracts

**Orchestrator application**: Maintain a living DAG throughout the initiative. Update it when tasks complete, dependencies change, or new work is discovered. Share the DAG with all agents so everyone understands the sequencing.

---

### Program Increment Planning (SAFe)

**Core idea**: Align multiple teams on shared objectives with explicit dependencies.

**Components**:
- **Objectives**: What each team commits to delivering this increment
- **Dependencies**: Cross-team commitments with delivery dates
- **Risks**: What could prevent teams from meeting commitments
- **Confidence vote**: Each team rates their confidence in meeting their objectives (1-5)

**Orchestrator application**: Use for strategic initiatives spanning 4+ weeks with 5+ agents. Facilitate a planning session where each agent commits to objectives, declares dependencies, and identifies risks. Low confidence votes (1-3) require immediate attention — either scope reduction or additional support.

---

### Work Breakdown Structure (WBS)

**Core idea**: Hierarchical decomposition of work.

**Levels**:
1. **Initiative** (the top-level goal)
2. **Workstreams** (major work areas, typically one per domain agent)
3. **Milestones** (significant checkpoints with deliverables)
4. **Tasks** (individual work items assignable to a single agent)

**Rules**:
- Every leaf node must be assignable to a single agent
- Every leaf node must be completable within one sprint (1-2 weeks)
- Parent nodes are NOT tasks — they are containers for grouping
- 100% Rule: child nodes must account for 100% of the parent's work
- No overlap: a task appears in exactly one branch of the WBS

**Orchestrator application**: The WBS is the first artifact the orchestrator creates for any initiative. It drives all other artifacts: the DAG comes from WBS dependencies, the RACI comes from WBS assignments, milestones come from WBS intermediate nodes.

---

### Eisenhower Matrix

**Core idea**: Prioritize by urgency and importance.

| | Urgent | Not Urgent |
|---|--------|-----------|
| **Important** | Q1: Do immediately (blocked critical-path items, escalations) | Q2: Schedule (dependency audits, risk reviews, stakeholder relationships) |
| **Not Important** | Q3: Delegate or batch (status requests, low-priority questions) | Q4: Eliminate (unnecessary meetings, administrative overhead) |

**Orchestrator application**: The orchestrator's trap is spending all time in Q1 (firefighting) and Q3 (responding to requests). Effective orchestration lives in Q2 — preventing Q1 emergencies through proactive dependency management, risk monitoring, and stakeholder communication.

---

### Boyd's OODA Loop

**Core idea**: Rapid decision cycle for coordination.

**Phases**:
1. **Observe**: Gather signals from agents (activity feed, status updates, blockers, metrics)
2. **Orient**: Interpret signals against the initiative plan (is this a problem? how does it affect the critical path?)
3. **Decide**: Choose a coordination action (escalate, reassign, descope, wait)
4. **Act**: Execute the action (emit activity, update plan, delegate)

**Cycle speed by context**:
- **Crisis/incident**: Minutes (compressed OODA)
- **Time-critical (<1 week)**: Hours
- **Normal execution**: Daily
- **Strategic planning**: Weekly

**Orchestrator application**: The Orient phase is where orchestration expertise lives. Raw observations (agent says "blocked") must be interpreted (is this on the critical path? what is the downstream impact? what precedent exists for this type of blocker?). Speed through the Orient phase comes from experience — which is why the flywheel learning integration matters.

---

### Tuckman's Team Stages

**Core idea**: Teams evolve through predictable stages.

| Stage | Characteristics | Orchestrator Response |
|-------|----------------|----------------------|
| **Forming** | New team, uncertain roles, polite conflict avoidance | Prescriptive delegation, explicit norms, tight checkpoints, build trust through small wins |
| **Storming** | Conflict emerges, roles contested, some resistance to coordination | Facilitate conflict resolution, clarify RACI, maintain structure but allow healthy disagreement |
| **Norming** | Patterns settle, trust builds, agents self-organize for routine decisions | Loosen checkpoints, shift to outcome-based delegation, let agents negotiate directly |
| **Performing** | Self-organizing, high output, agents proactively coordinate | Light touch, focus on cross-initiative coordination, intervene only for strategic decisions |

---

### Brooks's Law

**Core idea**: Adding people to a late project makes it later.

**Why**: New agents need onboarding (time from existing agents), communication paths increase quadratically, work must be repartitioned (coordination overhead), and the new agent's initial productivity is negative (they consume more help than they produce).

**Formula**: Communication paths = n(n-1)/2

| Agents | Communication Paths |
|--------|-------------------|
| 3 | 3 |
| 5 | 10 |
| 8 | 28 |
| 10 | 45 |
| 15 | 105 |

**Orchestrator application**: When an initiative is behind schedule, resist the urge to add agents. First try: scope reduction. Second: deadline extension. Third: process improvement. Adding agents is the last resort and only for workstreams where the new agent can work independently on a cleanly separated task.

---

### Two-Pizza Rule

**Core idea**: If a workstream needs more than 8 people, split it.

**Why**: Communication overhead grows quadratically (Metcalfe's Law). Beyond 8 agents, the time spent coordinating exceeds the time spent working. Two teams of 4 outperform one team of 8, even accounting for inter-team coordination.

**Orchestrator application**: When decomposing an initiative, ensure no workstream has more than 8 agents assigned. If a workstream requires more, it is too large and should be split into two workstreams with an explicit interface between them.

---

### Metcalfe's Law of Meetings

**Core idea**: Communication paths = n(n-1)/2 — minimize sync points.

**Application to orchestration**:
- Prefer async updates (activity feeds, status artifacts) over synchronous checkpoints
- When a sync is necessary, invite the minimum viable set of agents
- A daily standup with 10 agents has 45 communication paths — most of the information is irrelevant to most participants
- Split large syncs into focused, small-group syncs organized by dependency clusters

**Rule of thumb**: If a sync involves agents who share no dependencies, the sync is too broad. Split it.
