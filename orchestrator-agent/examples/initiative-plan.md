# Example: Cross-Domain Initiative Plan

## Workspace Analytics Dashboard

This is a worked example of a cross-domain initiative plan produced by the orchestrator agent. It demonstrates proper dependency mapping, critical path identification, RACI assignment, and risk management across 5 domain agents.

---

## Initiative Plan (JSON)

```json
{
  "title": "Launch Workspace Analytics Dashboard",
  "summary": "Deliver a unified analytics dashboard that gives workspace owners visibility into agent activity, decision history, and outcome metrics. Addresses the #1 feature request from enterprise customers (47 requests in Q4) and unblocks the sales team's enterprise expansion pipeline ($2.1M in pipeline blocked on 'visibility' objection).",
  "owner": "orchestrator-agent",
  "target_date": "2026-04-29",
  "success_metrics": [
    {
      "metric": "Dashboard adoption rate",
      "target": "50% of active workspaces access the dashboard within 30 days of launch",
      "baseline": "0% (new feature)",
      "measurement_method": "Track unique workspace_id accessing /analytics endpoint, measured daily via product analytics"
    },
    {
      "metric": "User satisfaction (NPS)",
      "target": "NPS score of 40+ from dashboard users in post-launch survey",
      "baseline": "No baseline (new feature)",
      "measurement_method": "In-app NPS survey triggered 7 days after first dashboard visit, minimum 50 responses"
    },
    {
      "metric": "Page load performance",
      "target": "<2s page load time at p95",
      "baseline": "N/A (new page)",
      "measurement_method": "Real User Monitoring (RUM) via existing performance tracking, measured from navigation start to largest contentful paint"
    }
  ],
  "workstreams": [
    {
      "id": "ws-product",
      "name": "Product Definition and User Research",
      "agent": "product-agent",
      "goal": "Deliver a PRD with validated user requirements, widget prioritization, and acceptance criteria for the analytics dashboard",
      "dependencies": [],
      "milestones": [
        {
          "name": "User research complete",
          "due_date": "2026-03-25",
          "deliverables": ["User interview synthesis (8 enterprise customers)", "Widget prioritization matrix (RICE scored)", "Draft PRD v1"]
        },
        {
          "name": "PRD finalized",
          "due_date": "2026-04-01",
          "deliverables": ["Final PRD with acceptance criteria", "Success metric measurement plan", "Handoff to engineering and design"]
        }
      ]
    },
    {
      "id": "ws-design",
      "name": "UI/UX Design and Prototyping",
      "agent": "design-agent",
      "goal": "Deliver component specifications, interaction design, and a validated prototype for the analytics dashboard",
      "dependencies": ["ws-product"],
      "milestones": [
        {
          "name": "Design exploration complete",
          "due_date": "2026-04-08",
          "deliverables": ["3 design concepts with tradeoff analysis", "Information architecture for dashboard layout", "Data visualization component audit"]
        },
        {
          "name": "Final specs delivered",
          "due_date": "2026-04-15",
          "deliverables": ["Component specifications for all dashboard widgets", "Interaction design for filtering, date ranges, and drill-downs", "Responsive design specs (desktop + tablet)", "Usability test results (5 participants)"]
        }
      ]
    },
    {
      "id": "ws-engineering",
      "name": "Backend API and Data Pipeline",
      "agent": "engineering-agent",
      "goal": "Build REST API endpoints and data aggregation pipeline for agent activity, decision history, and outcome metrics with <200ms p95 response time",
      "dependencies": ["ws-product", "ws-design"],
      "milestones": [
        {
          "name": "API design and RFC approved",
          "due_date": "2026-04-08",
          "deliverables": ["RFC with API contract, data model, and migration plan", "Performance budget for API endpoints", "Test strategy document"]
        },
        {
          "name": "API endpoints live in staging",
          "due_date": "2026-04-22",
          "deliverables": ["All API endpoints deployed to staging", "Data pipeline processing events into dashboard views", "Integration tests passing", "Performance benchmarks meeting <200ms p95 target"]
        },
        {
          "name": "Production deployment complete",
          "due_date": "2026-04-29",
          "deliverables": ["Production deployment with feature flag", "Monitoring and alerting configured", "Runbook for dashboard service incidents", "API documentation for marketing developer content"]
        }
      ]
    },
    {
      "id": "ws-marketing",
      "name": "Launch Communications and Positioning",
      "agent": "marketing-agent",
      "goal": "Create and execute a launch communication plan that drives 50% awareness among active workspace owners within 2 weeks of launch",
      "dependencies": ["ws-product", "ws-design"],
      "milestones": [
        {
          "name": "Launch messaging finalized",
          "due_date": "2026-04-15",
          "deliverables": ["Positioning document", "Blog post draft", "In-app announcement copy", "Email campaign for existing customers"]
        },
        {
          "name": "Launch execution",
          "due_date": "2026-04-29",
          "deliverables": ["Blog post published", "Email campaign sent", "In-app announcement deployed", "Social media posts scheduled", "Developer documentation page live"]
        }
      ]
    },
    {
      "id": "ws-sales",
      "name": "Enterprise Sales Enablement",
      "agent": "sales-agent",
      "goal": "Equip the sales team to demo the analytics dashboard and address the 'visibility' objection in enterprise deals",
      "dependencies": ["ws-product", "ws-engineering"],
      "milestones": [
        {
          "name": "Enablement materials ready",
          "due_date": "2026-04-22",
          "deliverables": ["Demo script with talking points", "Competitive comparison showing analytics advantage", "ROI calculator incorporating dashboard value"]
        },
        {
          "name": "Sales team trained",
          "due_date": "2026-04-29",
          "deliverables": ["Training session delivered to full sales team", "FAQ document for common prospect questions", "Demo environment configured with sample data"]
        }
      ]
    }
  ],
  "dependency_graph": {
    "edges": [
      {"from": "ws-design", "to": "ws-product", "type": "blocks", "description": "Design needs PRD before starting component specs"},
      {"from": "ws-engineering", "to": "ws-product", "type": "blocks", "description": "Engineering needs PRD for API contract design"},
      {"from": "ws-engineering", "to": "ws-design", "type": "blocks", "description": "Frontend implementation needs component specs"},
      {"from": "ws-marketing", "to": "ws-product", "type": "informs", "description": "Marketing uses PRD for positioning"},
      {"from": "ws-marketing", "to": "ws-design", "type": "informs", "description": "Marketing uses design assets for launch content"},
      {"from": "ws-sales", "to": "ws-product", "type": "informs", "description": "Sales uses PRD for value proposition"},
      {"from": "ws-sales", "to": "ws-engineering", "type": "blocks", "description": "Sales demo needs working staging environment"}
    ]
  },
  "critical_path": {
    "path": ["ws-product (PRD finalized)", "ws-design (Final specs delivered)", "ws-engineering (Production deployment)"],
    "total_duration": "5 weeks",
    "slack_per_workstream": {
      "ws-product": "0 days (critical path)",
      "ws-design": "0 days (critical path)",
      "ws-engineering": "0 days (critical path)",
      "ws-marketing": "1 week slack (can start after PRD, parallel with engineering)",
      "ws-sales": "1 week slack (needs staging, not production)"
    }
  },
  "raci": {
    "initiative_level": {
      "accountable": "orchestrator-agent",
      "responsible": ["product-agent", "engineering-agent", "design-agent", "marketing-agent", "sales-agent"],
      "consulted": [],
      "informed": ["workspace owners (beta testers)"]
    },
    "ws-product": {"accountable": "product-agent", "responsible": ["product-agent"], "consulted": ["sales-agent", "design-agent"], "informed": ["engineering-agent", "marketing-agent"]},
    "ws-design": {"accountable": "design-agent", "responsible": ["design-agent"], "consulted": ["product-agent", "engineering-agent"], "informed": ["marketing-agent"]},
    "ws-engineering": {"accountable": "engineering-agent", "responsible": ["engineering-agent"], "consulted": ["design-agent", "operations-agent"], "informed": ["product-agent", "sales-agent"]},
    "ws-marketing": {"accountable": "marketing-agent", "responsible": ["marketing-agent"], "consulted": ["product-agent", "sales-agent"], "informed": ["engineering-agent"]},
    "ws-sales": {"accountable": "sales-agent", "responsible": ["sales-agent"], "consulted": ["product-agent", "marketing-agent"], "informed": ["engineering-agent"]}
  },
  "risks": [
    {
      "description": "Engineering underestimates data pipeline complexity, especially aggregation performance at scale",
      "probability": 3,
      "impact": 4,
      "risk_score": 12,
      "mitigation": "Require performance benchmarks at milestone 2 with production-scale test data. If p95 exceeds 200ms, trigger scope reduction (reduce widget count from 12 to 8 core widgets).",
      "owner": "engineering-agent"
    },
    {
      "description": "Design requires multiple revision cycles after usability testing, compressing engineering timeline",
      "probability": 3,
      "impact": 3,
      "risk_score": 9,
      "mitigation": "Design does guerrilla usability testing on design concepts (milestone 1) before committing to final specs. Engineering starts API work from PRD, not design specs, to parallelize.",
      "owner": "design-agent"
    },
    {
      "description": "Enterprise customers have requirements not captured in initial user research, causing scope creep",
      "probability": 2,
      "impact": 3,
      "risk_score": 6,
      "mitigation": "Product agent includes 3 enterprise customers in research sample. Any new requirements discovered after PRD finalization go to v2 backlog, not v1 scope.",
      "owner": "product-agent"
    },
    {
      "description": "Marketing launch date is coupled to external press schedule that cannot be moved",
      "probability": 2,
      "impact": 4,
      "risk_score": 8,
      "mitigation": "Marketing confirms press flexibility by end of week 1. If press date is immovable, engineering scope is reduced to meet the date (feature-flag non-critical widgets).",
      "owner": "marketing-agent"
    }
  ]
}
```

---

## What Makes This a Good Initiative Plan

1. **Clear decomposition**: Five workstreams, each owned by a single domain agent with a specific goal.
2. **Explicit dependencies**: The dependency graph shows which workstreams block others and which merely inform. This prevents hidden coupling.
3. **Critical path identified**: Product, Design, and Engineering are on the critical path. Marketing and Sales have slack. This tells the orchestrator where to focus attention.
4. **Measurable success metrics**: Each metric has a target, baseline (or acknowledgment that baseline is N/A for new features), and a measurement method.
5. **Risks with mitigation**: Each risk has a probability, impact, owner, and a specific mitigation action — not generic "monitor closely."
6. **RACI at both levels**: Initiative-level RACI names the orchestrator as accountable. Workstream-level RACI ensures each workstream has exactly one accountable agent.
7. **Milestones are concrete**: Each milestone has a date and specific deliverables, not vague descriptions like "design phase complete."
8. **Scope protection built in**: Risks include a scope reduction trigger (reduce widget count) and a scope freeze (new requirements go to v2).
