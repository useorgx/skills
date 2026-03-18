# RFC Template Reference

## Required Sections

Every RFC MUST include these sections to pass validation.

## RFC Thinking Checklist

Before writing a single word of the RFC, walk through this checklist. It forces you to confront the decisions that matter before you get lost in solution details.

### Problem Validation

- [ ] Can I state the problem in one sentence without mentioning the solution?
- [ ] Do I have quantitative data showing the problem's impact (cost, latency, error rate, lost revenue, time wasted)?
- [ ] Has this problem been attempted before? What happened and why did it fail?
- [ ] What happens if we do nothing for 6 months? Is the problem getting worse, stable, or self-resolving?

### Framework Lenses

Apply each relevant framework as a lens on the proposal. Not all frameworks apply to every RFC — use the ones that illuminate real tradeoffs.

**DORA Metrics Check**: Will this change improve or degrade deployment frequency, lead time, change failure rate, or MTTR? If it degrades any DORA metric, that must be in the risks section with a mitigation plan.

**CAP Theorem Check** (for distributed systems): Which two of Consistency, Availability, and Partition Tolerance does this design choose? Document the sacrifice explicitly. If the RFC claims all three, it is either wrong or describing a system that is not truly distributed.

**STRIDE Check** (for anything touching auth, data, or network boundaries): Walk through Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege for the proposed design. Each applicable category must appear in the security considerations section.

**12-Factor Check** (for new services): Does the proposed service comply with 12-factor methodology? Flag violations of Factor III (config in environment, not code), Factor X (dev/prod parity), and Factor XI (logs as event streams) as they are the most commonly violated and most dangerous.

**Conway's Law Check**: Does the proposed architecture match the team structure that will own it? If Service A and Service B are owned by different teams that rarely communicate, a design requiring tight coordination between those services will fail. Either change the design or change the team topology.

**Amdahl's Law Check** (for performance proposals): If the RFC proposes parallelization or scaling, what fraction of the workload is inherently serial? Calculate the maximum theoretical speedup. If the serial fraction means you can only achieve a 2x improvement but the RFC promises 10x, the math does not work.

**INVEST Check** (for work breakdown): Are the tasks in the migration plan Independent, Negotiable, Valuable, Estimable, Small, and Testable? If a single task takes more than 1 week, it needs decomposition.

**Little's Law Check** (for capacity or queue-based systems): L = lambda * W. If the RFC proposes a queue or processing pipeline, calculate the expected queue depth given the arrival rate and processing time. If the queue depth exceeds what the system can handle, the design needs backpressure or rate limiting.

### Alternative Analysis Quality

- [ ] Do I have at least 2 genuine alternatives (not strawmen)?
- [ ] Would a reasonable, senior engineer advocate for each alternative?
- [ ] Have I honestly listed the cons of my preferred approach?
- [ ] For each rejected alternative, is the "why not" specific to our context (not a generic dismissal)?

### Migration and Rollback

- [ ] Can every phase of the migration be rolled back independently?
- [ ] Is there a specific trigger (metric threshold, error rate, user report) that initiates rollback?
- [ ] Have I estimated how long rollback takes for each phase?
- [ ] Is the rollback plan tested, or at least testable before the migration begins?
- [ ] Are feature flags in place to control the rollout?

### Organizational Readiness

- [ ] Does the team have the skills to build this? If not, what training or hiring is needed?
- [ ] Is there on-call capacity to support this change post-launch?
- [ ] Are downstream teams aware of changes that affect them?
- [ ] Does this require changes to the CI/CD pipeline? Who owns that work?

## Template

````markdown
# RFC: [Title]

## Metadata

- **RFC ID**: RFC-XXXX
- **Author**: [Name]
- **Status**: Draft | Review | Approved | Implemented | Rejected
- **Created**: YYYY-MM-DD
- **Reviewers**: [Names]

## Summary

One paragraph (100+ chars) summarizing what this RFC proposes and why.
This should be understandable to someone who hasn't read the full document.

## Background

Why is this change needed? Include:

- Current state and its problems
- Data showing the impact (numbers required)
- Failed approaches or workarounds already tried
- What triggered this RFC

Example:
"Our API currently handles 10,000 requests/second. Load testing shows
we'll hit 25,000 rps by Q3 based on 40% MoM growth. Current architecture
caps at 15,000 rps before latency exceeds SLA. Three incidents in past
month traced to this bottleneck."

## Proposal

### Overview

Detailed description of the proposed solution.

### API Changes

```typescript
// New or modified endpoints
POST / api / v2 / resource;
{
  field: string;
  newField: number; // Added in this RFC
}
```
````

### Database Changes

```sql
-- Migrations required
ALTER TABLE resources ADD COLUMN new_field INTEGER;
CREATE INDEX idx_resources_new_field ON resources(new_field);
```

### Architecture

```mermaid
graph LR
    A[Client] --> B[API Gateway]
    B --> C[New Service]
    C --> D[Database]
```

### Security Considerations

Map findings to STRIDE categories:

- **Spoofing**: Authentication changes, identity verification impact
- **Tampering**: Data integrity protections, input validation
- **Repudiation**: Audit logging requirements, non-repudiation measures
- **Information Disclosure**: Data exposure risks, PII handling
- **Denial of Service**: Rate limiting, resource exhaustion protections
- **Elevation of Privilege**: Authorization changes, privilege boundary enforcement

## Alternatives Considered

### Alternative 1: [Name]

**Description**: Brief description of this approach.

**Pros**:

- Pro 1
- Pro 2

**Cons**:

- Con 1
- Con 2

**Why not**: Specific reason this wasn't chosen.

### Alternative 2: [Name]

[Same structure]

## Migration Plan

### Phase 1: Preparation

- [ ] Task 1
- [ ] Task 2
- Rollback trigger: [specific condition that initiates rollback]
- Rollback procedure: [specific steps to reverse this phase]
- Rollback duration estimate: [how long rollback takes]

### Phase 2: Rollout

- [ ] Task 1
- [ ] Task 2
- Rollback trigger: [specific condition]
- Rollback procedure: [specific steps]
- Rollback duration estimate: [time]

### Feature Flags

- `new_feature_enabled`: Controls new behavior
- Rollout: 1% -> 10% -> 50% -> 100% over 2 weeks

### Backward Compatibility

- Old API version supported for X months
- Data migration is reversible: Yes/No

## Risks

| Risk             | Probability  | Impact       | Mitigation          | DORA Impact |
| ---------------- | ------------ | ------------ | ------------------- | ----------- |
| Risk description | High/Med/Low | High/Med/Low | Mitigation strategy | Which metric |

## Success Metrics

| Metric      | Current | Target | Measurement | Timeline |
| ----------- | ------- | ------ | ----------- | -------- |
| Latency p99 | 500ms   | 200ms  | Datadog APM | 2 weeks  |
| Error rate  | 0.1%    | 0.05%  | Sentry      | 1 month  |

## Open Questions

- [ ] Question for reviewers?
- [ ] Decision that needs input?

## References

- Link to related RFC
- Link to design doc
- Link to relevant code

```

## Writing Effective Backgrounds

### Must Include
1. **Current state** with specific data
2. **Problem impact** (quantified)
3. **Why now** - what's the trigger

### Bad Examples
- "The system is slow" (no data)
- "Users complain about performance" (not specific)
- "We need to modernize" (no justification)

### Good Examples
- "Query latency increased 300% (from 50ms to 200ms p99) after data grew to 50M rows. This affects 15% of users who experience timeouts."
- "Authentication failures cause 2,500 support tickets/month ($125K support cost) and 8% trial abandonment."

## Alternative Analysis Framework

For each alternative, answer:
1. **What**: Brief description
2. **Pros**: 2-3 genuine advantages
3. **Cons**: 2-3 honest drawbacks
4. **Why not**: Specific reason it's not chosen

Don't include strawman alternatives. Each should be a genuine option someone could reasonably advocate for. A good test: if you cannot imagine a senior engineer on your team championing this alternative, it is a strawman.

## Risk Assessment Matrix

| Probability | Impact | Priority |
|-------------|--------|----------|
| High | High | P0 - Block launch |
| High | Low | P1 - Fix before GA |
| Low | High | P1 - Have mitigation ready |
| Low | Low | P2 - Monitor |

## Common RFC Mistakes

1. **No data in background** - Always include numbers. If you don't have numbers, that's the first problem to solve.
2. **Single alternative** - Need at least 2 genuine options. "Do nothing" counts only if it's genuinely viable.
3. **Vague migration plan** - Be specific about phases and rollback. "We'll migrate gradually" is not a plan.
4. **Missing rollback strategy** - Every change needs an undo plan. "We'll figure it out" means you haven't thought about it.
5. **No success metrics** - Define how you'll know it worked. If you can't measure it, you can't declare victory.
6. **Skipping security review** - Consider auth, authz, data exposure. Use STRIDE as a minimum checklist.
7. **Strawman alternatives** - Including obviously bad alternatives to make the preferred option look good. Each alternative must be defensible.
8. **Missing DORA impact** - Not considering how the change affects deployment frequency, lead time, change failure rate, or MTTR.
9. **Conway's Law violation** - Proposing an architecture that doesn't match the team structure without addressing the organizational change required.
10. **No feature flags** - Proposing an all-or-nothing deployment when a gradual rollout would reduce blast radius.
```
