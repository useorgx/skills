# Engineering Frameworks Cheatsheet

Quick-reference card for the engineering agent's domain expertise frameworks. Use this to select the right lens for the problem at hand.

## When to Use Each Framework

| Framework | Use When | Key Question It Answers |
|-----------|----------|------------------------|
| DORA Metrics | Assessing team health, proposing process changes, writing postmortems | "Is this team delivering software effectively?" |
| C4 Model | Documenting architecture at the right level of detail | "What level of detail does this audience need?" |
| STRIDE | Any RFC touching auth, data storage, network boundaries, or user input | "What are the security threats to this design?" |
| INVEST | Evaluating task/story quality in work breakdowns | "Is this task well-defined enough to execute?" |
| 12-Factor App | Evaluating new service architecture or service redesigns | "Does this service follow modern deployment practices?" |
| CAP Theorem | Distributed system design, database selection, replication strategy | "Which consistency tradeoff is this system making?" |
| Amdahl's Law | Performance optimization proposals, parallelization efforts | "What is the maximum theoretical speedup?" |
| Conway's Law | Team topology changes, service boundary decisions, org restructuring | "Does this architecture match our team structure?" |
| Little's Law | Queue-based systems, capacity planning, WIP limit decisions | "How deep will this queue get under load?" |
| FMEA | Critical system design where simple risk tables are insufficient | "What are all the ways this component can fail?" |

## Framework Details

### DORA Metrics

**What it measures**: Four key metrics that predict software delivery performance.

| Metric | Elite | High | Medium | Low |
|--------|-------|------|--------|-----|
| Deployment Frequency | On-demand (multiple per day) | Weekly to monthly | Monthly to biannually | Fewer than once per 6 months |
| Lead Time for Changes | Less than 1 hour | 1 day to 1 week | 1 week to 1 month | More than 1 month |
| Change Failure Rate | 0-15% | 16-30% | 16-30% | 46-60% |
| Mean Time to Recovery | Less than 1 hour | Less than 1 day | 1 day to 1 week | More than 1 week |

**How to use in artifacts**:
- In RFCs: quantify expected impact on each metric. "This change adds a CI gate that increases lead time by 5 minutes but is expected to reduce change failure rate from 18% to under 10%."
- In postmortems: identify which metrics this incident degraded and by how much. Track trends across incidents.
- In capacity plans: use deployment frequency and lead time as inputs to throughput calculations.

### C4 Model

**Four levels of abstraction**:

| Level | Shows | Audience | When to Use |
|-------|-------|----------|-------------|
| **Context** | System and its external actors (users, other systems) | Non-technical stakeholders, new team members | Executive summaries, onboarding docs |
| **Container** | Applications, databases, message queues within the system | Technical decision makers, architects | RFCs, architecture overviews |
| **Component** | Internal modules/services within a container | Development team implementing the change | Detailed design docs, implementation plans |
| **Code** | Classes, interfaces, functions | Individual developers | Only when interface contracts are ambiguous |

**Rule of thumb**: Start at the highest level that answers the reader's question. Go deeper only when ambiguity remains.

### STRIDE

**Threat categories for security analysis**:

| Category | Threat | Typical Mitigation |
|----------|--------|-------------------|
| **S**poofing | Attacker pretends to be another user or system | Authentication (MFA, API keys, mTLS), session management |
| **T**ampering | Attacker modifies data in transit or at rest | Input validation, checksums, signed payloads, database constraints |
| **R**epudiation | User denies performing an action | Audit logs, digital signatures, tamper-evident logging |
| **I**nformation Disclosure | Sensitive data exposed to unauthorized parties | Encryption at rest and in transit, access controls, data classification |
| **D**enial of Service | System made unavailable to legitimate users | Rate limiting, autoscaling, circuit breakers, CDN, redundancy |
| **E**levation of Privilege | Attacker gains higher access than authorized | Principle of least privilege, RBAC, input validation, sandboxing |

**How to use**: For each component in the RFC that handles user input, stores data, or crosses a network boundary, walk through all six categories. Document findings in the security considerations section. Not every category applies to every component, but you must explicitly confirm you checked.

### INVEST

**Criteria for well-formed user stories and tasks**:

| Criterion | Question | Failure Symptom |
|-----------|----------|----------------|
| **I**ndependent | Can this be delivered without waiting on other stories? | "Blocked by..." in every standup |
| **N**egotiable | Is the implementation approach flexible? | Prescriptive implementation details in the story |
| **V**aluable | Does completing this deliver value to a user or the business? | Technical tasks with no user-visible outcome |
| **E**stimable | Can the team estimate the effort? | "We don't know enough to estimate" — needs a spike first |
| **S**mall | Can it be completed in one sprint? | Stories that span multiple sprints |
| **T**estable | Can you write a test that proves it's done? | "We'll know it when we see it" acceptance criteria |

### 12-Factor App

**Checklist for service architecture**:

| Factor | Requirement | Common Violation |
|--------|-------------|-----------------|
| I. Codebase | One codebase tracked in version control, many deploys | Multiple repos for one service, or one repo for unrelated services |
| II. Dependencies | Explicitly declare and isolate dependencies | System-level dependencies assumed to exist (e.g., ImageMagick) |
| III. Config | Store config in the environment | Config files committed to the repo, feature flags in code |
| IV. Backing Services | Treat backing services as attached resources | Hardcoded database connection strings, in-process queues |
| V. Build/Release/Run | Strictly separate build and run stages | Building on production servers, manual deploy steps |
| VI. Processes | Execute the app as stateless processes | Local file storage, in-memory session state |
| VII. Port Binding | Export services via port binding | Relying on runtime injection into an app server |
| VIII. Concurrency | Scale out via the process model | Vertical scaling only, single-threaded bottlenecks |
| IX. Disposability | Maximize robustness with fast startup and graceful shutdown | 60-second startup times, no graceful shutdown handler |
| X. Dev/Prod Parity | Keep development, staging, and production as similar as possible | SQLite in dev, PostgreSQL in prod; mocked services in dev |
| XI. Logs | Treat logs as event streams | Writing to local files, custom log aggregation |
| XII. Admin Processes | Run admin/management tasks as one-off processes | SSH-ing into production to run scripts, manual database migrations |

### CAP Theorem

**Decision framework for distributed systems**:

```
Pick two. You cannot have all three in the presence of network partitions.

Consistency + Availability  = Only works if partitions never happen (single datacenter)
Consistency + Partition Tol. = System rejects requests during partitions (CP: HBase, MongoDB)
Availability + Partition Tol. = System serves stale data during partitions (AP: Cassandra, DynamoDB)
```

**In practice**: Network partitions will happen in any distributed system. The real choice is between consistency (CP) and availability (AP) during a partition. Most applications need different guarantees for different data: financial transactions need CP, user preferences can tolerate AP.

### Amdahl's Law

**Formula**: S(n) = 1 / ((1 - p) + p/n)

Where:
- S(n) = speedup with n processors/workers
- p = fraction of the workload that can be parallelized
- n = number of processors/workers

**Quick reference**:

| Serial Fraction | Max Speedup (infinite workers) | Speedup with 8 workers | Speedup with 16 workers |
|----------------|-------------------------------|----------------------|------------------------|
| 5% | 20x | 5.9x | 7.0x |
| 10% | 10x | 4.7x | 5.3x |
| 25% | 4x | 2.9x | 3.1x |
| 50% | 2x | 1.8x | 1.9x |

**Key insight**: If 50% of your workload is serial, no amount of parallelization will get you past 2x speedup. Identify and reduce the serial portion before investing in parallelism.

### Conway's Law

**The law**: "Any organization that designs a system will produce a design whose structure is a copy of the organization's communication structure." — Melvin Conway, 1967

**Inverse Conway Maneuver**: Deliberately structure teams to match the desired architecture. If you want independent microservices, you need independent teams.

**Warning signs of Conway's Law violations**:
- Service A and Service B are tightly coupled but owned by teams that rarely talk
- A "platform" team owns services that require deep business domain knowledge
- Cross-team PRs are common and slow, indicating wrong service boundaries
- Architecture meetings require more than 2 teams to attend regularly

### Little's Law

**Formula**: L = lambda * W

Where:
- L = average number of items in the system (queue depth, WIP)
- lambda = average arrival rate (items per unit time)
- W = average time an item spends in the system

**Practical applications**:
- **Queue sizing**: If 100 requests/second arrive and each takes 200ms to process, the average queue depth is 100 * 0.2 = 20 items. Size your queue accordingly.
- **WIP limits**: If a team can handle 5 items per week (lambda = 5/week) and you want average cycle time of 1 week (W = 1 week), WIP limit should be L = 5 * 1 = 5 items.
- **Capacity planning**: If you need queue depth under 50 and arrival rate is 200/second, each item must be processed in under 250ms (W = L/lambda = 50/200 = 0.25 seconds).

### FMEA (Failure Mode and Effects Analysis)

**Process**: For each component, fill in this table:

| Component | Failure Mode | Cause | Effect | Severity (1-10) | Occurrence (1-10) | Detection (1-10) | RPN | Recommended Action |
|-----------|-------------|-------|--------|-----------------|-------------------|-------------------|-----|-------------------|
| [Name] | How it fails | Why it fails | What happens to users | Impact | How likely | How easy to detect | S*O*D | What to do |

**Risk Priority Number (RPN)** = Severity * Occurrence * Detection. Higher is worse. Prioritize actions by RPN.

**When to use over simple risk tables**: Use FMEA when the system has many components that can fail independently, when failures have cascading effects, or when the system has safety or financial implications that require rigorous analysis.
