# Example: Gold-Standard Delegation Message

## Delegation to Engineering Agent

This is a worked example of a delegation message from the orchestrator to the engineering-agent. It demonstrates all 7 elements of the Delegation Quality Standard: context, objective, scope, acceptance criteria, deadline, dependencies, and escalation path.

---

## Delegation Message (JSON)

```json
{
  "target_agent": "engineering-agent",
  "context": {
    "background": "The Workspace Analytics Dashboard is our top strategic initiative for Q2. It addresses the #1 enterprise feature request (47 requests in Q4) and unblocks $2.1M in pipeline where 'visibility into agent activity' is the primary objection. The product-agent has delivered a PRD (artifact ref: prd-analytics-dash-v2) defining 12 dashboard widgets with real-time data updates. The design-agent will deliver component specifications by April 15. Your workstream is on the critical path — any delay directly delays the initiative launch date.",
    "initiative_id": "init-analytics-dash-001",
    "initiative_success_metrics": [
      "50% adoption within 30 days",
      "NPS 40+ from dashboard users",
      "<2s page load at p95"
    ]
  },
  "task": {
    "objective": "Deliver production-ready REST API endpoints and a data aggregation pipeline for the analytics dashboard. Endpoints must serve agent activity, decision history, and outcome metrics with <200ms p95 API response time. The data pipeline must process raw events into pre-aggregated views suitable for dashboard rendering.",
    "requirements": [
      "REST API endpoints for: agent activity feed (paginated, filterable by agent and date range), decision history (with approval status and outcome), outcome metrics (aggregated by initiative, workstream, and time period)",
      "Data aggregation pipeline that processes raw agent events into dashboard-ready materialized views, running on a schedule no slower than every 5 minutes",
      "API response time <200ms at p95 under expected load (100 concurrent dashboard sessions, each polling every 30 seconds)",
      "Feature flag controlling dashboard API access, defaulting to off in production until launch",
      "API documentation sufficient for the marketing-agent to create developer-facing content"
    ],
    "scope": {
      "in_scope": [
        "Backend API design, implementation, and deployment",
        "Data aggregation pipeline for raw events to dashboard views",
        "Database schema design and migration for materialized views",
        "Performance optimization to meet <200ms p95 target",
        "Integration tests covering all API endpoints",
        "API documentation (OpenAPI spec)",
        "Monitoring and alerting for API endpoints and pipeline",
        "Runbook for common failure modes"
      ],
      "out_of_scope": [
        "Frontend implementation (design-agent owns component specs, frontend work is a separate delegation)",
        "Real-time WebSocket connections (deferred to v2 based on synthesis decision; v1 uses polling with 30-second intervals)",
        "Custom widget builder backend (deferred to v2 per initiative scope decision)",
        "Historical data backfill beyond 90 days (v1 covers last 90 days only)",
        "Mobile-specific API optimizations (v1 targets desktop and tablet only)"
      ]
    }
  },
  "quality": {
    "acceptance_criteria": [
      "All API endpoints return valid JSON conforming to the OpenAPI spec with appropriate HTTP status codes for success, validation errors, and server errors",
      "API p95 response time is <200ms measured under load test simulating 100 concurrent sessions polling every 30 seconds",
      "Data pipeline processes 10,000 raw events into materialized views within 5 minutes, verified by pipeline monitoring metrics",
      "Integration test suite covers all endpoints with >=90% line coverage on API route handlers",
      "Feature flag correctly gates API access: disabled = 404 response, enabled = normal operation",
      "Runbook covers at least: pipeline failure/restart, API latency spike diagnosis, database migration rollback, feature flag emergency disable",
      "API documentation is published and the marketing-agent confirms it is sufficient for developer content (explicit confirmation required)"
    ]
  },
  "timeline": {
    "deadline": "2026-04-29",
    "deadline_rationale": "Launch date is April 29, coordinated with marketing press coverage and sales enablement training. Engineering must be production-deployed by this date for marketing launch to proceed. Any delay past this date delays the full initiative including $2.1M in enterprise pipeline.",
    "checkpoints": [
      {
        "date": "2026-04-08",
        "expected_deliverable": "RFC with API contract, data model, and migration plan approved. Performance budget documented. Test strategy finalized.",
        "purpose": "Validate technical approach before implementation begins. Catch architectural issues early. Confirm that the data model supports all dashboard requirements."
      },
      {
        "date": "2026-04-22",
        "expected_deliverable": "All API endpoints deployed to staging. Data pipeline running. Integration tests passing. Performance benchmarks meeting <200ms p95.",
        "purpose": "Verify implementation against acceptance criteria before production deployment. Allow sales-agent to configure demo environment. Catch performance issues with time to fix."
      }
    ]
  },
  "dependencies": {
    "needs_from_others": [
      {
        "agent": "product-agent",
        "what": "Finalized PRD with widget specifications and data requirements",
        "status": "delivered",
        "artifact_ref": "prd-analytics-dash-v2"
      },
      {
        "agent": "design-agent",
        "what": "Component specifications defining data display requirements, field names, and interaction patterns",
        "expected_date": "2026-04-15",
        "status": "in_progress",
        "note": "Engineering can start API design from PRD; component specs needed before frontend integration but not for backend API work"
      }
    ],
    "others_need": [
      {
        "agent": "sales-agent",
        "what": "Working staging environment with sample data for demo configuration",
        "needed_by": "2026-04-22",
        "note": "Sales team needs 1 week with staging to prepare demo scripts"
      },
      {
        "agent": "marketing-agent",
        "what": "API documentation (OpenAPI spec) for developer-facing launch content",
        "needed_by": "2026-04-22",
        "note": "Marketing needs 1 week to finalize developer documentation page"
      },
      {
        "agent": "operations-agent",
        "what": "Runbook and monitoring configuration for on-call team",
        "needed_by": "2026-04-29",
        "note": "Operations team needs runbook before production launch for on-call readiness"
      }
    ]
  },
  "escalation": {
    "path": "If blocked for more than 24 hours on any critical-path item, escalate to orchestrator-agent with: (1) what is blocked, (2) what has been tried, (3) what is needed to unblock, (4) impact on timeline if not resolved within 48 hours.",
    "contact": "orchestrator-agent via mcp__orgx__orgx_emit_activity with urgency: high",
    "response_time": "Orchestrator will respond within 4 hours during business hours, 12 hours outside business hours",
    "common_escalation_scenarios": [
      "Design specs are delayed past April 15 — orchestrator will negotiate timeline adjustment or scope reduction",
      "Performance target cannot be met with current architecture — orchestrator will convene design + product to evaluate scope reduction",
      "Database migration requires operations-agent support — orchestrator will delegate to operations-agent with appropriate priority"
    ]
  },
  "handoff": {
    "output_format": "RFC (for API design review at checkpoint 1) + deployed staging environment (at checkpoint 2) + production deployment with monitoring (at deadline). All artifacts published via mcp__orgx__create_entity linked to init-analytics-dash-001.",
    "completion_signal": "Call mcp__orgx__entity_action to mark workstream ws-engineering as complete. Include artifact references for RFC, staging URL, production deployment confirmation, and monitoring dashboard URL."
  }
}
```

---

## What Makes This a Good Delegation

### 1. Context (Why This Matters)
The delegation does not just say "build an API." It explains why: enterprise customer demand, $2.1M in pipeline, strategic initiative priority. The engineering-agent understands the stakes and can make informed tradeoff decisions.

### 2. Objective (Measurable Done)
"Done" is specific: REST API endpoints + data pipeline + <200ms p95. Not "build the backend" but a measurable definition that can be objectively verified.

### 3. Scope (In and Out)
Out-of-scope items are genuinely tempting: WebSocket real-time, custom widget builder backend, mobile optimizations. These are things the engineering-agent might reasonably attempt if not explicitly excluded. The scope boundary prevents drift.

### 4. Acceptance Criteria (Testable)
Every criterion is verifiable by a machine or process. "API p95 response time is <200ms measured under load test" is testable. "API should be fast" is not.

### 5. Deadline (Date + Rationale)
The date is April 29 with a clear rationale: marketing press coverage and sales training depend on it. The engineering-agent understands that this is not an arbitrary date — it is a coordination constraint.

### 6. Dependencies (Bidirectional)
The delegation specifies both what the engineering-agent needs from others (PRD, design specs) and what others need from the engineering-agent (staging for sales, docs for marketing, runbook for ops). This prevents the engineering-agent from producing outputs that do not serve downstream needs.

### 7. Escalation Path (Clear and Actionable)
The escalation path specifies when to escalate (24 hours blocked), how to escalate (activity emission with urgency: high), what to include (4 specific items), and expected response time (4-12 hours). Common scenarios are pre-identified so the engineering-agent does not hesitate to escalate.

## Delegation Quality Checklist

Use this checklist for every delegation:

- [ ] Context explains why this work matters, with link to initiative and success metrics
- [ ] Objective is measurable and can be verified objectively
- [ ] In-scope items are complete — nothing the agent needs to build is missing
- [ ] Out-of-scope items are genuinely tempting scope, not strawmen
- [ ] Every acceptance criterion is testable (could a script verify it?)
- [ ] Deadline has a specific date and a rationale tied to a downstream dependency
- [ ] At least one intermediate checkpoint is defined with expected deliverable
- [ ] Incoming dependencies list what the agent needs and when it will arrive
- [ ] Outgoing dependencies list what others need from this agent and when
- [ ] Escalation path specifies when, how, what to include, and response time
- [ ] Output format is specific enough that the agent knows what to produce
