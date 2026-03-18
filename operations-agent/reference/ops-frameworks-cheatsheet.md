# Operations Frameworks Cheatsheet

Quick reference for the operational frameworks used by the OrgX Operations Agent. Use this to select the right framework for the situation at hand.

---

## Framework Selection Guide

| Situation | Primary Framework | Supporting Frameworks |
|-----------|------------------|----------------------|
| Active incident (right now) | OODA Loop | Cynefin (classify the problem), Playbook |
| Post-incident analysis | Swiss Cheese + Five Whys | Blameless Postmortem Culture |
| Defining reliability targets | SLI/SLO/SLA Triangle | Error Budget Policy |
| Planning for growth | SRE Pyramid (assess maturity) | FinOps (cost), Capacity Planning |
| Reducing manual work | Toil Taxonomy | SRE Pyramid (automation level) |
| Testing system resilience | Chaos Engineering Principles | SLI/SLO (define steady state) |
| Managing cloud costs | FinOps Framework | Toil Taxonomy (cost of manual work) |
| Enterprise process alignment | ITIL v4 | Change Management, CMDB |
| Classifying problem complexity | Cynefin | Five Whys (for Complicated), Probe-Sense-Respond (for Complex) |

---

## SRE Pyramid (Google)

Maturity ladder from bottom to top. You cannot skip levels.

```
        +-----------+
        | Product   |    <- SRE informs product decisions
       +-------------+
       | Development |   <- Reliability built into code
      +---------------+
      | Capacity Plan |  <- Know limits before hitting them
     +-----------------+
     | Testing/Chaos   | <- Prove resilience before incidents prove fragility
    +-------------------+
    | Postmortem        | <- Learn from every failure systematically
   +---------------------+
   | Incident Response   | <- Respond fast when things break
  +-----------------------+
  | Monitoring            | <- See what is happening in the system
  +-----------------------+
```

**Assessment questions for each level:**

1. **Monitoring**: Can you answer "is the system healthy?" in under 30 seconds?
2. **Incident Response**: Is there an on-call rotation? Do runbooks exist for common alerts?
3. **Postmortem**: Are postmortems written for every P1/P2? Are action items tracked to completion?
4. **Testing**: Do you run load tests before launches? Any chaos experiments?
5. **Capacity Planning**: Do you forecast resource needs quarterly? Is there headroom tracking?
6. **Development**: Do SRE concerns influence code review? Are reliability features in the backlog?
7. **Product**: Does reliability data influence product prioritization?

---

## Cynefin Framework

```
  +-----------------------+-----------------------+
  |       Complex         |     Complicated       |
  |                       |                       |
  |  Probe-Sense-Respond  |  Sense-Analyze-Respond|
  |  (emergent practice)  |  (good practice)      |
  |                       |                       |
  |  Example: cascading   |  Example: intermittent|
  |  failure in distrib.  |  latency spike from   |
  |  system               |  query optimization   |
  +-----------------------+-----------------------+
  |       Chaotic         |       Clear           |
  |                       |                       |
  |  Act-Sense-Respond    |  Sense-Categorize-    |
  |  (novel practice)     |  Respond              |
  |                       |  (best practice)      |
  |  Example: active      |                       |
  |  security breach,     |  Example: restart a   |
  |  unknown scope        |  crashed service      |
  +-----------------------+-----------------------+
                    Confused
              (break the problem down)
```

**Key insight**: The danger zone is treating a Complex problem as if it were Clear. This produces a confident-sounding root cause that is actually wrong. If the system has emergent behavior (distributed systems, human processes, market dynamics), you are in Complex territory. Do not jump to a root cause. Probe first.

---

## Swiss Cheese Model

```
  Threat → | O |  | O |  |   |  | O |  | O | → Incident
           |   |  |   |  | O |  |   |  |   |
           |   |  |   |  |   |  |   |  |   |
  Layer 1  Layer 2  Layer 3  Layer 4  Layer 5
  (Code    (Test   (Monitor (On-call (Rollback
  Review)  Suite)  /Alert)  Response) Procedure)
```

Each layer is a defense. Each layer has holes (weaknesses). An incident occurs when holes in multiple layers align, allowing the threat to pass through all defenses.

**When analyzing an incident, map every layer:**

1. What layers were supposed to prevent this?
2. What was the hole in each layer?
3. Which layer actually caught the problem (if any)?
4. What would have happened if one more layer had held?

**Action items should address holes in multiple layers**, not just the "root cause" layer. Fixing only the root cause leaves you one layer failure away from the next incident.

---

## Five Whys

**Rules:**
1. Each "why" must reference the previous answer, not jump topics.
2. Stop when you reach a systemic or organizational cause.
3. If the final "why" ends at a person, you stopped too early.
4. Multiple branches are allowed (there can be more than one causal chain).
5. Validate each "why" with evidence, not assumption.

**Example:**

- **Why did the API return 500 errors?** Because the database connection pool was exhausted.
- **Why was the connection pool exhausted?** Because the batch job was holding 187 connections instead of the normal 5-8.
- **Why was the batch job holding so many connections?** Because a connection leak was introduced in a code refactor that removed the connection release logic.
- **Why was the connection leak not caught in testing?** Because integration tests use mock database clients that do not enforce connection pool limits.
- **Why do integration tests not enforce resource limits?** Because there is no standard for test infrastructure to mirror production resource constraints.

**Root cause**: Test infrastructure design does not simulate production resource constraints. This is a systemic gap, not an individual error.

---

## SLI / SLO / SLA Triangle

```
         +-------+
         | SLA   |  Contract with consequences
         |       |  (e.g., credits if availability < 99.9%)
        +--------+
        | SLO    |  Internal target for the SLI
        |        |  (e.g., 99.9% availability over 28 days)
       +---------+
       | SLI     |  Measurement of service behavior
       |         |  (e.g., % of requests with status < 500)
       +---------+
```

**Key relationships:**
- SLIs must be measurable with existing tooling (or the proposal must include instrumentation work).
- SLOs must be stricter than SLAs (you want to catch problems before they breach the contract).
- SLAs should only promise what you can consistently deliver with margin.

**Common SLI categories:**

| Category | Example SLI | Measurement |
|----------|-------------|-------------|
| Availability | Successful requests / total requests | Load balancer access logs |
| Latency | p99 response time < threshold | APM traces |
| Throughput | Requests served per second | Load balancer metrics |
| Error Rate | 5xx responses / total responses | Application logs |
| Freshness | Time since last successful data sync | Custom metric |
| Correctness | Responses matching expected output / total | Prober / synthetic checks |
| Durability | Data items retrievable / data items stored | Storage system metrics |

---

## Error Budget Policy Quick Reference

**Formula**: Error Budget = 1 - SLO Target

| SLO Target | Error Budget | Monthly Budget (availability) | Monthly Budget (at 1M req/month) |
|------------|-------------|-------------------------------|----------------------------------|
| 99% | 1% | 7.2 hours | 10,000 failed requests |
| 99.5% | 0.5% | 3.6 hours | 5,000 failed requests |
| 99.9% | 0.1% | 43.2 minutes | 1,000 failed requests |
| 99.95% | 0.05% | 21.6 minutes | 500 failed requests |
| 99.99% | 0.01% | 4.3 minutes | 100 failed requests |

**Key insight**: The jump from 99.9% to 99.99% reduces your budget from 43 minutes to 4 minutes per month. That single "9" often requires multi-region architecture, automated failover, and zero-downtime deployments. Do not commit to 99.99% unless you have (or will invest in) the infrastructure to support it.

---

## OODA Loop (Incident Response)

```
  Observe → Orient → Decide → Act
     ↑                         |
     +-------------------------+
        (iterate until resolved)
```

**During an active incident:**

- **Observe**: What are the symptoms? Check dashboards, alerts, error logs. Do not theorize yet.
- **Orient**: What could cause these symptoms? Check recent changes, known issues, dependency status. This is where runbooks accelerate response.
- **Decide**: What is the most likely hypothesis? What is the fastest action to test it?
- **Act**: Execute the action. If it does not resolve the issue, return to Observe with new information.

**Speed tips:**
- Pre-built dashboards reduce Observe time from minutes to seconds.
- Runbooks reduce Orient time by providing known-good investigation paths.
- Rollback capability reduces Act time by providing a reliable "undo."
- Clear escalation paths reduce Decide time by removing ambiguity about authority.

---

## Toil Taxonomy

A task is toil if it meets 3 or more of these criteria:

| Criterion | Test | Example |
|-----------|------|---------|
| Manual | A human must perform it | SSH into server to restart service |
| Repetitive | It recurs (weekly, per deploy, per customer) | Rotate API keys for each new customer |
| Automatable | A machine could do it with current technology | Run database migrations manually |
| Tactical | Interrupt-driven, not strategic | Respond to disk space alert by clearing logs |
| No enduring value | Does not improve the system permanently | Manually approve each deploy |
| Scales linearly | Effort grows with service/customer count | Onboard each customer's webhook endpoint by hand |

**Toil budget**: Google SRE recommends that toil should not exceed 50% of an SRE team's time. If it does, the team is not doing engineering — it is doing operations.

**Toil reduction priority**: Automate the task with the highest (frequency x time_per_occurrence x risk_of_human_error).

---

## FinOps Framework

```
  Inform → Optimize → Operate
     ↑                    |
     +--------------------+
       (continuous cycle)
```

**Inform (visibility)**:
- Tag every resource with team, service, and environment.
- Attribute cost to business units, not just AWS accounts.
- Make cost dashboards accessible to engineers, not just finance.

**Optimize (action)**:
- Right-size instances (most are over-provisioned by 30-50%).
- Use reserved instances or savings plans for steady-state workloads.
- Use spot instances for fault-tolerant batch workloads.
- Delete unused resources (unattached EBS volumes, idle load balancers).
- Review data transfer costs (often the hidden budget killer).

**Operate (governance)**:
- Set budgets per team with alerts at 80% and 100%.
- Anomaly detection for sudden cost spikes.
- Monthly cost review meeting with engineering leads.
- Cost as a non-functional requirement in architecture reviews.

---

## Chaos Engineering Principles

**Before you start:**
1. Define steady state in terms of measurable business output (not internal metrics).
2. Get explicit approval from stakeholders.
3. Ensure kill switch is tested and ready.
4. Start in non-production. Graduate to production only with safety controls.

**Experiment checklist:**
- [ ] Steady state defined and currently met
- [ ] Hypothesis written in testable form
- [ ] Blast radius defined and acceptable
- [ ] Abort criteria defined
- [ ] Kill switch tested
- [ ] Rollback procedure documented
- [ ] Communication plan in place
- [ ] Monitoring in place to observe experiment effects
- [ ] Schedule agreed (avoid peak hours for early experiments)

**Common experiment types:**

| Type | What It Tests | Tools |
|------|---------------|-------|
| Instance failure | Auto-scaling, load balancing | Chaos Monkey, AWS FIS |
| Network partition | Service mesh resilience, timeout handling | Toxiproxy, tc netem |
| Dependency latency | Circuit breakers, timeout configuration | Toxiproxy, Gremlin |
| Dependency failure | Graceful degradation, fallback paths | Chaos Monkey, Gremlin |
| Load spike | Auto-scaling speed, queue depth handling | Locust, k6, Gatling |
| Disk fill | Log rotation, monitoring, alerting | stress-ng, dd |
| Clock skew | Certificate validation, cron jobs, TTLs | chrony manipulation |
| DNS failure | DNS caching, fallback resolution | iptables, DNS override |

---

## Blameless Postmortem Culture

**Language guide:**

| Instead of (blameful) | Say (blameless) |
|----------------------|-----------------|
| "Bob forgot to check the dashboard" | "The system did not alert when the threshold was breached" |
| "The deploy should have been tested" | "The test suite did not cover this scenario" |
| "If they had followed the runbook" | "The runbook did not include this failure mode" |
| "The on-call engineer failed to respond" | "The alerting configuration did not escalate after the initial timeout" |
| "This was a careless mistake" | "The interface did not prevent this misconfiguration" |
| "The team should have known better" | "The training materials did not cover this operational risk" |

**Test for blamelessness**: Replace every person's name with "the system" or "the process." If the sentence still makes sense and suggests a fix, it is blameless. If it becomes absurd ("the system was negligent"), the original was blameful.
