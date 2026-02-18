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

Best for: A/B tests, growth experiments, optimization

```json
{
  "title": "[Hypothesis] Growth Experiment",
  "summary": "Test hypothesis that [change] will [impact] for [segment], measured by [metric].",
  "success_metrics": [
    { "metric": "Statistical significance", "target": "95% confidence level" },
    { "metric": "Sample size", "target": "10,000+ users per variant" },
    {
      "metric": "Primary metric lift",
      "target": ">5% improvement over control"
    }
  ],
  "milestones": [
    {
      "title": "Hypothesis & Design",
      "due_date": "Week 1",
      "deliverables": [
        "Experiment brief",
        "Success criteria",
        "Sample size calculation"
      ]
    },
    {
      "title": "Implementation",
      "due_date": "Week 2",
      "deliverables": [
        "Feature flags",
        "Variant implementations",
        "Tracking events"
      ]
    },
    {
      "title": "Experiment Running",
      "due_date": "Week 4",
      "deliverables": [
        "Daily monitoring",
        "Guardrail checks",
        "Interim analysis"
      ]
    },
    {
      "title": "Analysis & Decision",
      "due_date": "Week 5",
      "deliverables": [
        "Statistical analysis",
        "Segment breakdown",
        "Recommendation"
      ]
    }
  ]
}
```

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

## Initiative Naming Conventions

### Do

- Use action-oriented titles: "Launch X", "Migrate to Y", "Improve Z"
- Include the target outcome: "Reduce Churn for Enterprise Segment"
- Be specific: "Q1 2025 Mobile App Redesign"

### Don't

- Vague titles: "Project Alpha", "Phase 2"
- Implementation details: "Add Redux to Frontend"
- Internal jargon without context

## Milestone Best Practices

1. **3-5 milestones per initiative** - More indicates scope creep
2. **2-3 week spacing** - Shorter for urgency, longer for complexity
3. **Clear deliverables** - Each milestone has concrete outputs
4. **Dependencies explicit** - Note if milestone depends on another
5. **Owner assigned** - Each milestone has a DRI
