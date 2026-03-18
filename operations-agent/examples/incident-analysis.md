# Incident Analysis: INC-2026-0342 — Core API Database Connection Pool Exhaustion

## Metadata

- **Incident ID**: INC-2026-0342
- **Title**: Complete service unavailability due to database connection pool exhaustion
- **Severity**: P1
- **Started At**: 2026-03-15T02:47:00Z
- **Detected At**: 2026-03-15T02:52:00Z
- **Resolved At**: 2026-03-15T03:34:00Z
- **Duration**: 47 minutes
- **Author**: Operations Agent
- **Status**: Complete

---

## Impact

**Description**: All API endpoints returned 503 errors for 47 minutes during the overnight window. The primary PostgreSQL connection pool (PgBouncer) was fully exhausted, causing all new database queries to fail. No API requests could be served successfully during this period.

**Users Affected**: 12,400 users were active at the time of the incident (global user base, overnight UTC corresponds to business hours in APAC).

**Revenue Impact**: Estimated $8,200 in failed transactions. 342 webhook deliveries were queued and delayed. 15 enterprise API integrations experienced errors and triggered their own alerting.

**Downstream Effects**: Three enterprise customers (Acme Corp, Globex, Initech) opened support tickets within 20 minutes. Webhook delivery backlog cleared within 12 minutes of resolution.

---

## Detection

- **Method**: Automated alert (Datadog monitor: "PgBouncer Active Connections > 90%")
- **MTTD (Mean Time to Detect)**: 5 minutes (incident started 02:47, alert fired 02:52)
- **Detection Gap Analysis**: The 5-minute detection delay occurred because the Datadog monitor uses a 5-minute rolling average. A 1-minute threshold would have fired at 02:48. This is an action item.

---

## Response Metrics

- **MTTD**: 5 minutes
- **MTTR**: 42 minutes (from detection to resolution)
- **Time to Identify Root Cause**: 13 minutes (02:52 to 03:05)
- **Time to Remediate**: 29 minutes (03:05 to 03:34)

---

## Timeline

| Timestamp (UTC) | Event |
|-----------------|-------|
| 02:30:00 | Nightly analytics export batch job (`nightly-analytics-export`) begins execution. Job connects to PostgreSQL via PgBouncer. |
| 02:35:00 | Batch job begins processing large dataset (2.3M rows). Connection count begins climbing steadily. Connections are not being released between queries due to a bug in the connection handling code introduced in deploy v2.14.7 (March 12). |
| 02:47:00 | PgBouncer connection pool reaches maximum (200/200 connections). All new connection requests begin failing. API error rate jumps from 0.08% to 100%. |
| 02:48:00 | Datadog error rate monitor fires (threshold: > 5% for 1 minute). However, this alert routes to a Slack channel, not PagerDuty. |
| 02:52:00 | Datadog PgBouncer connection saturation monitor fires (threshold: > 90% for 5-minute average). This alert routes to PagerDuty. On-call engineer (Platform Team L1) receives page. |
| 02:55:00 | On-call engineer acknowledges page. Opens Datadog dashboard "Database Health Overview." Observes 200/200 active connections and 100% API error rate. |
| 03:00:00 | On-call engineer checks recent deployments. No deploys in the past 6 hours. Checks batch job schedule and identifies `nightly-analytics-export` as the only active workload. |
| 03:05:00 | Root cause identified: `nightly-analytics-export` is holding 187 of 200 connections. Normal behavior for this job is 5-8 connections. Engineer identifies connection leak in batch job. |
| 03:10:00 | On-call engineer kills the batch job process. Connections begin releasing slowly (PgBouncer server_idle_timeout is 600 seconds). |
| 03:15:00 | Engineer restarts PgBouncer to force-close idle connections. Connections drop to 13/200. API begins serving requests. |
| 03:20:00 | Error rate drops to 2% (connection pool refilling, some clients retrying). Webhook delivery backlog begins processing. |
| 03:34:00 | Error rate returns to baseline (0.08%). All systems nominal. Incident resolved. |
| 03:45:00 | On-call engineer posts incident summary in #incidents Slack channel. Begins drafting timeline notes. |

---

## Root Cause

**Category**: code_defect

**Description**: A connection leak was introduced in the `nightly-analytics-export` batch job in deploy v2.14.7 (merged March 12, 2026). The batch job's query executor was refactored to use async/await patterns, but the connection release logic in the `finally` block was inadvertently removed during the refactor. Each query iteration opened a new connection without releasing the previous one. Under normal data volumes (< 500K rows), the job completed before exhausting the pool. On March 15, the dataset had grown to 2.3M rows, causing the job to consume 187 connections over 17 minutes before the pool was exhausted.

**Five Whys Analysis**:

1. **Why did the API go down?** Because all database connections were exhausted.
2. **Why were all connections exhausted?** Because the batch job was holding 187 connections simultaneously instead of its normal 5-8.
3. **Why was the batch job holding so many connections?** Because a connection leak in the refactored query executor was not releasing connections after each query.
4. **Why was the connection leak not caught before production?** Because the batch job's integration tests use a mock database client that does not enforce connection pooling limits, and the staging dataset (50K rows) is small enough that the job completes before the pool is exhausted.
5. **Why does the staging dataset not reflect production scale?** Because there is no process for scaling test data proportionally to production growth. The staging dataset was seeded 8 months ago and has not been refreshed.

---

## Contributing Factors (Swiss Cheese Model)

Each contributing factor represents a defensive layer that had a hole. The incident occurred because holes aligned across all layers simultaneously.

1. **Code Review Layer**: The connection release removal in the refactor was not caught during code review. The diff was part of a 400-line PR, and the `finally` block deletion was not highlighted by the reviewer. (Hole: large PRs reduce review thoroughness.)

2. **Testing Layer**: Integration tests used mock database clients that do not enforce connection limits. The connection leak was invisible in tests. (Hole: test infrastructure does not simulate production resource constraints.)

3. **Staging Validation Layer**: Staging dataset was 50K rows vs. production's 2.3M rows. The leak only manifests at scale. (Hole: staging data does not reflect production scale.)

4. **Monitoring Layer**: The PgBouncer saturation alert used a 5-minute rolling average, adding 5 minutes of detection delay. The API error rate alert routed to Slack instead of PagerDuty. (Hole: alert routing misconfiguration and averaging window too wide.)

5. **Connection Pool Layer**: PgBouncer's `server_idle_timeout` was set to 600 seconds (10 minutes), meaning leaked connections took 10 minutes to be reclaimed. A shorter timeout would have limited the blast radius. (Hole: pool configuration not tuned for leak resilience.)

---

## Action Items

| ID | Action | Owner | Due Date | Priority | Status |
|----|--------|-------|----------|----------|--------|
| AI-0342-1 | Fix connection leak in `nightly-analytics-export` query executor. Restore `finally` block with explicit connection release. | Jamie Chen (Backend) | 2026-03-17 | P1 | In Progress |
| AI-0342-2 | Add integration test that enforces connection pool limits. Test should fail if any job holds more than 10 connections simultaneously. | Jamie Chen (Backend) | 2026-03-21 | P1 | Open |
| AI-0342-3 | Reduce PgBouncer saturation alert from 5-minute to 1-minute rolling average. Re-route API error rate alert from Slack to PagerDuty. | Morgan Park (Platform) | 2026-03-18 | P1 | Open |
| AI-0342-4 | Reduce PgBouncer `server_idle_timeout` from 600s to 120s to limit connection leak blast radius. | Morgan Park (Platform) | 2026-03-19 | P2 | Open |
| AI-0342-5 | Create process for quarterly staging data refresh. Staging dataset should be at least 20% of production volume. | Alex Rivera (Platform Lead) | 2026-04-01 | P2 | Open |
| AI-0342-6 | Implement PR size guardrail: PRs > 300 lines require two reviewers. | Alex Rivera (Platform Lead) | 2026-04-15 | P3 | Open |

---

## Lessons Learned

1. **Connection pool exhaustion is a single-point-of-failure for all API traffic.** A single misbehaving batch job can take down the entire API because they share a connection pool. We should evaluate separating batch job connections from API connections (dedicated pool or separate PgBouncer instance).

2. **Test infrastructure must simulate production resource constraints.** Mock database clients that ignore connection limits create a false sense of safety. Integration tests should use a real connection pool with enforced limits, even if the database itself is mocked.

3. **Alert routing is as important as alert thresholds.** The API error rate alert fired 4 minutes before the PagerDuty page, but it went to Slack where nobody was watching at 2:48 AM. Critical alerts must route to PagerDuty, not informational channels.

4. **Staging data freshness is a reliability concern, not just a testing convenience.** The connection leak existed for 3 days in production without manifesting because the dataset was below the threshold. If staging data reflected production scale, this would have been caught during pre-production validation.

---

## Coaching Questions (for team retrospective)

- The error rate alert fired at 02:48 but went to Slack. How many other critical alerts route to non-paging channels? Should we audit all alert routing?
- The connection leak existed for 3 days (since v2.14.7). What monitoring would have caught this earlier as a slow leak rather than a sudden failure?
- The on-call engineer had to manually check the batch job schedule. Should PgBouncer connections be tagged with the originating service/job so that "top connections by source" is immediately visible?
- If the batch job had been running on a weekend when the on-call response was slower, what would the impact have been? Do we need automated circuit-breaking for connection pool exhaustion?

---

## JSON Artifact

```json
{
  "incident_id": "INC-2026-0342",
  "title": "Complete service unavailability due to database connection pool exhaustion",
  "severity": "P1",
  "started_at": "2026-03-15T02:47:00Z",
  "detected_at": "2026-03-15T02:52:00Z",
  "resolved_at": "2026-03-15T03:34:00Z",
  "duration_minutes": 47,
  "impact": {
    "description": "All API endpoints returned 503 errors for 47 minutes. Primary PostgreSQL connection pool fully exhausted.",
    "users_affected": 12400,
    "revenue_impact": "$8,200 in failed transactions",
    "downstream_effects": "342 webhook deliveries delayed, 3 enterprise customers opened support tickets"
  },
  "detection": {
    "method": "automated_alert",
    "alert_name": "PgBouncer Active Connections > 90%",
    "mttd_minutes": 5,
    "gap_analysis": "5-minute rolling average delayed detection. 1-minute window would have fired at 02:48."
  },
  "response_metrics": {
    "mttd_minutes": 5,
    "mttr_minutes": 42,
    "time_to_identify_minutes": 13,
    "time_to_remediate_minutes": 29
  },
  "timeline": [
    {"timestamp": "2026-03-15T02:30:00Z", "event": "Nightly analytics export batch job begins execution"},
    {"timestamp": "2026-03-15T02:35:00Z", "event": "Batch job processing 2.3M rows; connection count climbing due to leak"},
    {"timestamp": "2026-03-15T02:47:00Z", "event": "Connection pool exhausted (200/200). All API requests failing."},
    {"timestamp": "2026-03-15T02:48:00Z", "event": "Error rate alert fires, routes to Slack (not PagerDuty)"},
    {"timestamp": "2026-03-15T02:52:00Z", "event": "PgBouncer saturation alert fires, pages on-call engineer via PagerDuty"},
    {"timestamp": "2026-03-15T02:55:00Z", "event": "On-call engineer acknowledges page, opens monitoring dashboard"},
    {"timestamp": "2026-03-15T03:05:00Z", "event": "Root cause identified: batch job holding 187 connections due to leak"},
    {"timestamp": "2026-03-15T03:10:00Z", "event": "Batch job process killed"},
    {"timestamp": "2026-03-15T03:15:00Z", "event": "PgBouncer restarted to force-close idle connections"},
    {"timestamp": "2026-03-15T03:34:00Z", "event": "Error rate returns to baseline. Incident resolved."}
  ],
  "root_cause": {
    "description": "A connection leak was introduced in the nightly-analytics-export batch job in deploy v2.14.7 (March 12). The refactored query executor removed the finally block that released connections. Each query opened a new connection without releasing the previous one. At 2.3M rows, the job consumed 187 connections over 17 minutes before exhausting the pool.",
    "category": "code_defect"
  },
  "contributing_factors": [
    "Code review did not catch finally block removal in a 400-line PR",
    "Integration tests use mock DB clients that do not enforce connection pool limits",
    "Staging dataset (50K rows) does not reflect production scale (2.3M rows)",
    "PgBouncer saturation alert uses 5-minute average, adding detection delay",
    "API error rate alert routes to Slack instead of PagerDuty",
    "PgBouncer server_idle_timeout set to 600s, allowing leaked connections to persist"
  ],
  "action_items": [
    {
      "id": "AI-0342-1",
      "action": "Fix connection leak in batch job query executor",
      "owner": "Jamie Chen",
      "due_date": "2026-03-17",
      "priority": "P1",
      "status": "in_progress"
    },
    {
      "id": "AI-0342-2",
      "action": "Add integration test enforcing connection pool limits",
      "owner": "Jamie Chen",
      "due_date": "2026-03-21",
      "priority": "P1",
      "status": "open"
    },
    {
      "id": "AI-0342-3",
      "action": "Fix alert routing and reduce saturation alert averaging window",
      "owner": "Morgan Park",
      "due_date": "2026-03-18",
      "priority": "P1",
      "status": "open"
    },
    {
      "id": "AI-0342-4",
      "action": "Reduce PgBouncer server_idle_timeout from 600s to 120s",
      "owner": "Morgan Park",
      "due_date": "2026-03-19",
      "priority": "P2",
      "status": "open"
    },
    {
      "id": "AI-0342-5",
      "action": "Create quarterly staging data refresh process",
      "owner": "Alex Rivera",
      "due_date": "2026-04-01",
      "priority": "P2",
      "status": "open"
    },
    {
      "id": "AI-0342-6",
      "action": "Implement PR size guardrail requiring two reviewers for PRs > 300 lines",
      "owner": "Alex Rivera",
      "due_date": "2026-04-15",
      "priority": "P3",
      "status": "open"
    }
  ],
  "lessons_learned": [
    "Connection pool exhaustion is a single-point-of-failure. Batch jobs and API traffic should use separate connection pools.",
    "Test infrastructure must simulate production resource constraints. Mock clients that ignore pool limits create false safety.",
    "Alert routing is as important as alert thresholds. Critical alerts must page, not post to Slack.",
    "Staging data freshness is a reliability concern. Stale test data hides scale-dependent bugs."
  ]
}
```
