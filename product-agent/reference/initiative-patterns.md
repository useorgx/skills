# Initiative Patterns Reference

## Pattern 1: Feature Launch Initiative

Best for: New feature releases, product launches

```json
{
  "title": "[Feature Name] Launch Initiative",
  "summary": "Launch [feature] to [target users] to solve [problem], expected to [impact metric].",
  "success_metrics": [
    {
      "metric": "Feature adoption rate",
      "target": "30% of active users within 30 days"
    },
    { "metric": "Task completion rate", "target": "85%+ for core workflow" },
    {
      "metric": "Support tickets",
      "target": "<5 tickets/week related to feature"
    }
  ],
  "milestones": [
    {
      "title": "Discovery & Design",
      "due_date": "Week 2",
      "deliverables": ["User research summary", "Design specs", "Technical RFC"]
    },
    {
      "title": "Development Sprint 1",
      "due_date": "Week 4",
      "deliverables": ["Core functionality", "Unit tests", "API endpoints"]
    },
    {
      "title": "Development Sprint 2",
      "due_date": "Week 6",
      "deliverables": [
        "UI implementation",
        "Integration tests",
        "Documentation"
      ]
    },
    {
      "title": "Beta & Iteration",
      "due_date": "Week 8",
      "deliverables": ["Beta release", "Feedback collection", "Bug fixes"]
    },
    {
      "title": "GA Launch",
      "due_date": "Week 10",
      "deliverables": ["Production release", "Launch comms", "Success tracking"]
    }
  ]
}
```

## Pattern 2: Platform Migration Initiative

Best for: Technical migrations, infrastructure changes

```json
{
  "title": "[System] Migration to [Target]",
  "summary": "Migrate [current system] to [target system] to achieve [benefits] while maintaining [SLAs].",
  "success_metrics": [
    {
      "metric": "Migration completion",
      "target": "100% of data migrated with <0.01% loss"
    },
    { "metric": "Downtime", "target": "<4 hours total during migration" },
    {
      "metric": "Performance",
      "target": "P95 latency equal or better post-migration"
    }
  ],
  "milestones": [
    {
      "title": "Assessment & Planning",
      "due_date": "Week 2",
      "deliverables": [
        "Current state audit",
        "Migration plan",
        "Risk assessment",
        "Rollback plan"
      ]
    },
    {
      "title": "Infrastructure Setup",
      "due_date": "Week 4",
      "deliverables": [
        "Target environment",
        "CI/CD pipelines",
        "Monitoring setup"
      ]
    },
    {
      "title": "Data Migration (Non-Prod)",
      "due_date": "Week 6",
      "deliverables": [
        "Staging migration",
        "Data validation",
        "Performance testing"
      ]
    },
    {
      "title": "Production Migration",
      "due_date": "Week 8",
      "deliverables": [
        "Cutover execution",
        "Validation checks",
        "Traffic switch"
      ]
    },
    {
      "title": "Stabilization",
      "due_date": "Week 10",
      "deliverables": [
        "Monitoring review",
        "Cleanup old system",
        "Documentation update"
      ]
    }
  ]
}
```

## Pattern 3: Growth Experiment Initiative

Best for: A/B tests, growth experiments, funnel optimization, activation improvements

This pattern is specifically designed for hypothesis-driven product changes where the goal is learning, not shipping. The initiative succeeds if the hypothesis is validated or invalidated with statistical confidence, regardless of the result direction.

```json
{
  "title": "[Hypothesis] Growth Experiment",
  "summary": "Test hypothesis that [change] will [impact] for [segment], measured by [metric]. Decision criteria: ship if [primary metric] improves by >5% with 95% confidence and [guardrail metrics] do not degrade by >2%.",
  "success_metrics": [
    { "metric": "Statistical significance", "target": "95% confidence level" },
    { "metric": "Sample size", "target": "10,000+ users per variant" },
    {
      "metric": "Primary metric lift",
      "target": ">5% improvement over control"
    },
    {
      "metric": "Guardrail metrics",
      "target": "No degradation >2% in retention, revenue, or error rate"
    }
  ],
  "milestones": [
    {
      "title": "Hypothesis & Design",
      "due_date": "Week 1",
      "deliverables": [
        "Experiment brief with hypothesis, primary metric, guardrails",
        "Power analysis and sample size calculation",
        "Variant designs and success criteria",
        "Decision matrix: what result leads to what action"
      ]
    },
    {
      "title": "Implementation & QA",
      "due_date": "Week 2",
      "deliverables": [
        "Feature flags configured",
        "Variant implementations complete",
        "Tracking events verified in staging",
        "Randomization unit confirmed (user-level, session-level)"
      ]
    },
    {
      "title": "Experiment Running",
      "due_date": "Week 4",
      "deliverables": [
        "Daily guardrail monitoring (automated alerts)",
        "SRM check (sample ratio mismatch) at day 1 and day 3",
        "Interim peek at day 7 (no decisions, just directional)"
      ]
    },
    {
      "title": "Analysis & Decision",
      "due_date": "Week 5",
      "deliverables": [
        "Full statistical analysis with confidence intervals",
        "Segment breakdown (does the effect vary by user segment?)",
        "Guardrail metric review",
        "Recommendation: ship, iterate, or kill",
        "Learning document submitted to flywheel"
      ]
    }
  ]
}
```

### Growth Experiment Guardrails

- Never peek and make decisions before the experiment reaches the calculated sample size
- Always check for Sample Ratio Mismatch (SRM) — if the variant split is not 50/50 (+/- 1%), the experiment is compromised
- Define the decision matrix before the experiment starts, not after seeing results
- If multiple metrics conflict (primary improves, guardrail degrades), default to protecting the guardrail
- Document learnings regardless of outcome — a well-run experiment that invalidates a hypothesis is a success

## Pattern 4: Technical Debt Initiative

Best for: Refactoring, performance improvements, cleanup

```json
{
  "title": "[Area] Technical Debt Reduction",
  "summary": "Reduce technical debt in [area] to improve [developer velocity/reliability/performance].",
  "success_metrics": [
    { "metric": "Code coverage", "target": "Increase from X% to Y%" },
    { "metric": "Build time", "target": "Reduce from X min to Y min" },
    { "metric": "Incident rate", "target": "Reduce related incidents by 50%" }
  ],
  "milestones": [
    {
      "title": "Audit & Prioritization",
      "due_date": "Week 1",
      "deliverables": [
        "Debt inventory",
        "Impact assessment",
        "Priority ranking"
      ]
    },
    {
      "title": "Quick Wins",
      "due_date": "Week 3",
      "deliverables": [
        "High-impact/low-effort items",
        "Linting fixes",
        "Dependency updates"
      ]
    },
    {
      "title": "Major Refactors",
      "due_date": "Week 6",
      "deliverables": ["Core refactoring", "Test coverage", "Documentation"]
    },
    {
      "title": "Validation & Cleanup",
      "due_date": "Week 8",
      "deliverables": [
        "Performance validation",
        "Dead code removal",
        "Final metrics"
      ]
    }
  ]
}
```

## Pattern 5: Pivot Evaluation Initiative

Best for: Evaluating and executing a strategic pivot when current product-market fit signals are weak, growth has stalled, or a fundamental assumption has been invalidated.

This pattern is different from others because its primary output is a decision, not a feature. The initiative succeeds when the team makes a high-confidence decision about whether and how to pivot, then executes that decision.

```json
{
  "title": "[Current Product] Pivot Evaluation: [Pivot Type]",
  "summary": "Evaluate whether to pivot [current product/approach] based on [evidence of need: declining retention, failed PMF threshold, market shift]. Pivot type under consideration: [zoom-in|zoom-out|customer-segment|value-capture|channel|technology]. Decision deadline: [date].",
  "success_metrics": [
    {
      "metric": "Decision confidence",
      "target": "Team alignment score >80% on chosen direction"
    },
    {
      "metric": "Evidence completeness",
      "target": ">=3 data sources per option evaluated"
    },
    {
      "metric": "Transition speed",
      "target": "First pivot milestone delivered within 2 weeks of decision"
    },
    {
      "metric": "Post-pivot leading indicator",
      "target": "Defined and measurable within 30 days of pivot execution"
    }
  ],
  "milestones": [
    {
      "title": "Current State Diagnosis",
      "due_date": "Week 1",
      "deliverables": [
        "Retention curve analysis showing trend",
        "Sean Ellis PMF survey results (if available)",
        "Revenue trajectory and burn rate projection",
        "User interview synthesis (>=5 interviews with churned users)",
        "Honest assessment: what is working and what is not"
      ]
    },
    {
      "title": "Option Development",
      "due_date": "Week 2",
      "deliverables": [
        "Minimum 3 pivot options documented using pivot taxonomy",
        "Each option includes: description, evidence for, evidence against, resource requirement, reversibility assessment",
        "Quick validation for each option (landing page test, concierge MVP, customer interviews)",
        "Competitive landscape for each option's target market"
      ]
    },
    {
      "title": "Decision & Alignment",
      "due_date": "Week 3",
      "deliverables": [
        "Decision matrix with scoring across: evidence strength, resource fit, team capability, market timing, reversibility",
        "Team vote or alignment session documented",
        "Kill criteria defined: what signals in the first 30 days would tell us this pivot is wrong",
        "Communication plan for stakeholders, investors, customers"
      ]
    },
    {
      "title": "Transition Execution",
      "due_date": "Week 6",
      "deliverables": [
        "Pivot execution plan with weekly checkpoints",
        "Leading indicator dashboard live and tracking",
        "First customer/user validation in new direction",
        "30-day checkpoint: review kill criteria, decide continue or course-correct"
      ]
    }
  ]
}
```

### Pivot Taxonomy Reference

| Pivot Type | Description | Example | Key Risk |
|-----------|-------------|---------|----------|
| **Zoom-in** | A single feature of the current product becomes the entire product | Instagram pivoting from Burbn (check-in app) to photo sharing only | Abandoning users who valued the broader product |
| **Zoom-out** | The current product becomes a feature of a larger product | Offering a platform instead of a point solution | Scope explosion, loss of focus |
| **Customer segment** | Same product, different target users | Slack pivoting from gaming company internal tool to enterprise messaging | Product-market assumptions from old segment may not transfer |
| **Value capture** | Same product, different monetization | Moving from ads to subscriptions | Revenue disruption during transition |
| **Channel** | Same product, different distribution | Moving from direct sales to self-serve | Loss of high-touch customer relationships |
| **Technology** | Same user problem, fundamentally different technical approach | Rewriting from on-prem to cloud-native | Engineering risk and timeline uncertainty |

### Pivot Decision Principles

1. A pivot preserves one leg while changing the other. If you change both the product and the customer, that is not a pivot — it is a new company.
2. Pivots should be evidence-based, not panic-based. "Revenue is declining" is not enough evidence. "Revenue is declining because our target segment is shrinking and we have evidence that adjacent segment X has the same job-to-be-done" is evidence.
3. The best pivots feel obvious in retrospect. If the team cannot articulate why the pivot makes sense in one paragraph, the reasoning is not clear enough.
4. Speed matters more than perfection. A pivot executed 80% right in 3 weeks beats a pivot executed 100% right in 3 months, because the learning from execution is the most valuable input.

## Pattern 6: Discovery Sprint Initiative

Best for: Early-stage problem validation, new market exploration, pre-PRD research

```json
{
  "title": "[Problem Space] Discovery Sprint",
  "summary": "Conduct a focused discovery sprint to validate whether [problem hypothesis] is real, significant, and solvable for [target segment]. Output: go/no-go recommendation for building a solution.",
  "success_metrics": [
    {
      "metric": "Interviews completed",
      "target": ">=10 users in target segment"
    },
    {
      "metric": "Problem validation",
      "target": ">=7 of 10 interviewees confirm the problem unprompted"
    },
    {
      "metric": "Willingness to pay",
      "target": ">=5 of 10 would pay for a solution or switch from current approach"
    }
  ],
  "milestones": [
    {
      "title": "Problem Hypothesis & Recruiting",
      "due_date": "Week 1",
      "deliverables": [
        "Problem hypothesis document",
        "Interview guide with JTBD questions",
        "Participant recruiting (target: 12-15 scheduled for 10 completed)"
      ]
    },
    {
      "title": "User Interviews",
      "due_date": "Week 2",
      "deliverables": [
        "10 completed interviews (recorded with consent)",
        "Per-interview summary: key quotes, jobs, pains, current solutions",
        "Running affinity map of themes"
      ]
    },
    {
      "title": "Synthesis & Recommendation",
      "due_date": "Week 3",
      "deliverables": [
        "Affinity-mapped themes with frequency counts",
        "JTBD statements validated by interview data",
        "Go/no-go recommendation with evidence",
        "If go: draft product canvas and next steps",
        "If no-go: learnings document and alternative directions"
      ]
    }
  ]
}
```

## Initiative Naming Conventions

### Do

- Use action-oriented titles: "Launch X", "Migrate to Y", "Improve Z"
- Include the target outcome: "Reduce Churn for Enterprise Segment"
- Be specific: "Q1 2025 Mobile App Redesign"
- Include the initiative type when helpful: "[Feature Launch] Real-Time Collaboration"

### Don't

- Vague titles: "Project Alpha", "Phase 2"
- Implementation details: "Add Redux to Frontend"
- Internal jargon without context
- Titles that do not indicate the desired outcome

## Milestone Best Practices

1. **3-5 milestones per initiative** — More indicates scope creep
2. **2-3 week spacing** — Shorter for urgency, longer for complexity
3. **Clear deliverables** — Each milestone has concrete outputs (not activities)
4. **Dependencies explicit** — Note if milestone depends on another initiative or external event
5. **Owner assigned** — Each milestone has a DRI (Directly Responsible Individual)
6. **Exit criteria defined** — What must be true to consider the milestone complete
7. **First milestone is fast** — The first milestone should complete within 1-2 weeks to build momentum
