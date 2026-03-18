# SLO Proposal: Core API Service

## Metadata

- **Service**: core-api
- **Author**: Operations Agent
- **Created**: 2026-03-18
- **Status**: Proposed
- **Review Date**: 2026-04-15

---

## Service Description

The Core API handles user authentication, CRUD operations for all primary product entities (initiatives, workstreams, tasks, milestones), and webhook delivery to customer integrations. It is the single point of entry for all client applications (web dashboard, CLI, MCP integrations) and all third-party API consumers.

## Stakeholders

- **Engineering**: Platform Team (owns infrastructure), Backend Team (owns application logic)
- **Product**: Product Manager for API platform
- **Customer Success**: Handles enterprise SLA escalations
- **Enterprise Customers**: Acme Corp, Globex, Initech (contractual SLA requirements)

---

## Current Performance (Trailing 90 Days)

| Metric | Value | Source |
|--------|-------|--------|
| Availability | 99.95% (21.6 minutes downtime) | Datadog Synthetics |
| p50 Latency | 45ms | Datadog APM |
| p95 Latency | 180ms | Datadog APM |
| p99 Latency | 280ms | Datadog APM |
| Error Rate | 0.08% | Datadog APM (5xx responses / total responses) |
| Webhook Delivery Rate | 99.7% | Custom Prometheus metric |
| Webhook Delivery p95 Latency | 2.3s | Custom Prometheus metric |

---

## Service Level Indicators (SLIs)

### SLI-1: Availability

- **Metric**: Proportion of successful HTTP responses (status < 500) out of total valid requests
- **Measurement Method**: Datadog APM `trace.http.request` filtered to `service:core-api`, excluding health check endpoints (`/api/health`, `/api/ready`)
- **Good Threshold**: Response status code < 500
- **Unit**: Percentage of successful requests
- **Exclusions**: Requests with client errors (4xx) are counted as "successful" from an availability perspective since the server processed them correctly. Requests to deprecated endpoints returning 410 Gone are excluded.

### SLI-2: Read Latency

- **Metric**: Server-side latency of HTTP GET requests to the Core API
- **Measurement Method**: Datadog APM `trace.http.request` where `http.method:GET` and `service:core-api`, measured at p99
- **Good Threshold**: p99 latency < 300ms
- **Unit**: Milliseconds
- **Rationale for Separating Read/Write**: Read operations are the majority of traffic (85%) and have different latency profiles than writes. Users perceive read latency more acutely because it directly affects page load time.

### SLI-3: Write Latency

- **Metric**: Server-side latency of HTTP POST/PUT/PATCH/DELETE requests to the Core API
- **Measurement Method**: Datadog APM `trace.http.request` where `http.method:POST|PUT|PATCH|DELETE` and `service:core-api`, measured at p99
- **Good Threshold**: p99 latency < 500ms
- **Unit**: Milliseconds
- **Rationale**: Write operations involve database transactions, validation, and event emission. A higher latency threshold reflects the inherent complexity of writes.

### SLI-4: Error Rate

- **Metric**: Proportion of HTTP 5xx responses out of total requests
- **Measurement Method**: Datadog APM `trace.http.request` where `http.status_code:5xx` / total requests for `service:core-api`
- **Good Threshold**: Error rate < 0.1%
- **Unit**: Percentage

### SLI-5: Webhook Delivery Rate

- **Metric**: Proportion of webhooks successfully delivered (HTTP 2xx response from customer endpoint) out of total webhook attempts, including retries
- **Measurement Method**: Custom Prometheus metric `webhooks_delivered_total` / `webhooks_attempted_total`
- **Good Threshold**: Delivery rate > 99.5%
- **Unit**: Percentage
- **Note**: "Delivered" means a 2xx response was received from the customer's endpoint. Customer endpoint failures after 3 retries with exponential backoff are counted as delivery failures.

---

## Service Level Objectives (SLOs)

### SLO-1: Availability

- **SLI Reference**: SLI-1 (Availability)
- **Target**: 99.9%
- **Window**: Rolling 28 days
- **Rationale**: Current trailing 90-day availability is 99.95%. Setting the SLO at 99.9% provides a meaningful target that is achievable with current architecture while giving the team a realistic error budget for deployments and maintenance. 99.99% would require architectural changes (multi-region active-active) that are not justified by current customer requirements.
- **Error Budget**: 0.1% = 40.3 minutes of downtime per 28-day window, or approximately 2,016 failed requests per million.

### SLO-2: Read Latency

- **SLI Reference**: SLI-2 (Read Latency)
- **Target**: 99.5% of GET requests complete in < 300ms (p99)
- **Window**: Rolling 28 days
- **Rationale**: Current p99 read latency is 280ms, which is close to the 300ms threshold. This SLO provides a small buffer while signaling that latency regressions need attention. The 0.5% budget allows for occasional slow queries during peak load or cache misses.

### SLO-3: Write Latency

- **SLI Reference**: SLI-3 (Write Latency)
- **Target**: 99.5% of write requests complete in < 500ms (p99)
- **Window**: Rolling 28 days
- **Rationale**: Write operations are inherently slower due to database transactions and event processing. 500ms is the threshold at which users perceive delays in form submissions and action confirmations. Current p99 write latency is approximately 350ms, giving comfortable headroom.

### SLO-4: Error Rate

- **SLI Reference**: SLI-4 (Error Rate)
- **Target**: 99.9% of requests are non-5xx
- **Window**: Rolling 28 days
- **Rationale**: Equivalent to an error rate ceiling of 0.1%. Current error rate is 0.08%, so this provides a small budget for transient errors during deployments and infrastructure maintenance.

### SLO-5: Webhook Delivery

- **SLI Reference**: SLI-5 (Webhook Delivery Rate)
- **Target**: 99.5% delivery rate
- **Window**: Rolling 28 days
- **Rationale**: Current delivery rate is 99.7%. Webhook delivery depends on customer endpoint availability, which we do not control. Setting the SLO at 99.5% accounts for customer-side failures that are outside our control while still flagging systematic delivery problems on our side.

---

## Error Budget Policy

### Budget Calculation

| SLO | Target | Budget (per 28 days) | Concrete Budget |
|-----|--------|---------------------|-----------------|
| Availability | 99.9% | 0.1% | 40.3 minutes downtime OR ~2,016 failed requests per million |
| Read Latency | 99.5% | 0.5% | 5,000 slow reads per million GET requests |
| Write Latency | 99.5% | 0.5% | 5,000 slow writes per million write requests |
| Error Rate | 99.9% | 0.1% | 1,000 5xx errors per million requests |
| Webhook Delivery | 99.5% | 0.5% | 5,000 failed deliveries per million webhooks |

### Threshold Actions

| Condition | Burn Rate | Action | Authority |
|-----------|-----------|--------|-----------|
| Budget > 75% remaining | Normal (< 1x) | Normal operations. Deploy freely. | Engineering team |
| Budget 50-75% remaining | Elevated (1-2x) | Heightened awareness. Review deploys for risk. No optional infrastructure changes. | Engineering lead |
| Budget 25-50% remaining | High (2-5x) | Reduce deploy frequency. Prioritize reliability work. Cancel non-critical maintenance windows. | Engineering lead + Product manager |
| Budget < 25% remaining | Critical (> 5x) | Deploy freeze for non-reliability changes. All engineering effort directed at reliability. Incident review for recent error budget consumption. | VP Engineering (can override) |
| Budget exhausted (0%) | Exhausted | Full deploy freeze. Emergency reliability sprint. Daily standup on SLO recovery. Resume normal operations only when budget recovers to > 25%. | VP Engineering |

### Authority

- **Deploy freeze authority**: Engineering Lead can initiate. VP Engineering can override with documented justification.
- **Resume authority**: Deploy freeze lifts automatically when error budget recovers above 25% of the 28-day window. Manual override requires VP Engineering approval.

---

## Alerting Rules

### Fast Burn (Page Immediately)

- **Condition**: Error budget burn rate > 14.4x over 1 hour (consuming 2% of monthly budget in 1 hour)
- **Lookback**: 5-minute sliding window
- **Routing**: PagerDuty -> Platform Team L1 on-call
- **Example**: If availability drops below 97% for 5 minutes, this fires. This represents a severe active incident.

### Slow Burn (Create Ticket)

- **Condition**: Error budget burn rate > 3x over 24 hours (consuming 10% of monthly budget in 1 day)
- **Lookback**: 6-hour sliding window
- **Routing**: Jira ticket assigned to Platform Team, Slack notification to #reliability
- **Example**: Sustained p99 latency of 350ms (above 300ms threshold) affecting 1.5% of reads over 6 hours. Not an active incident but a degradation trend.

### Budget Threshold Alerts

- **75% remaining**: Informational Slack notification to #reliability
- **50% remaining**: Slack notification + email to Engineering Lead
- **25% remaining**: PagerDuty notification to Engineering Lead + VP Engineering
- **Exhausted**: PagerDuty notification to VP Engineering + all-hands Slack

---

## Review Cadence

- **Monthly SLO Review** (first Tuesday of each month):
  - Review error budget consumption for the past 28 days
  - Identify top contributors to budget spend
  - Decide whether SLO targets need adjustment
  - Review whether alerting thresholds are appropriately tuned (too noisy? too quiet?)
  - Attendees: Platform Team lead, Backend Team lead, Product Manager

- **Quarterly SLO Calibration**:
  - Review whether SLO targets still align with customer expectations
  - Adjust targets based on architecture changes or new customer requirements
  - Review whether new SLIs are needed (new critical paths, new integrations)
  - Attendees: above + VP Engineering, Customer Success lead

---

## Escalation Path

| Condition | Escalation |
|-----------|------------|
| SLO missed for 1 month | Engineering Lead reviews action items from monthly SLO review. Allocate 20% of next sprint to reliability. |
| SLO missed for 2 consecutive months | VP Engineering sponsors a reliability initiative. Dedicated workstream with named DRI. |
| SLO missed for 3 consecutive months | Executive review. Evaluate whether architectural investment is needed (multi-region, database upgrade, etc.). Customer Success proactively communicates with enterprise customers. |

---

## Implementation Requirements

The following instrumentation is needed before these SLOs can be activated:

1. **Datadog SLO monitors**: Create monitors for each SLO using Datadog's SLO tracking feature. Estimated effort: 2 hours.
2. **Webhook delivery metrics**: Verify that `webhooks_delivered_total` and `webhooks_attempted_total` Prometheus metrics are accurate. Current gap: retries after initial failure may not be counted correctly. Estimated effort: 4 hours.
3. **Read/write latency split**: Datadog APM already captures HTTP method. Verify that the SLI queries correctly filter GET vs. non-GET. Estimated effort: 1 hour.
4. **Error budget dashboard**: Create Datadog dashboard showing real-time error budget for all 5 SLOs with burn rate visualization. Estimated effort: 4 hours.
5. **Alerting rules**: Configure Datadog monitors for fast-burn and slow-burn conditions. Route to PagerDuty and Jira as specified. Estimated effort: 3 hours.

**Total implementation effort**: Approximately 14 engineering hours (2 days).

---

## JSON Artifact

```json
{
  "service": "core-api",
  "stakeholders": ["Platform Team", "Backend Team", "Product Manager", "Customer Success", "Enterprise Customers"],
  "slis": [
    {
      "name": "Availability",
      "metric": "Proportion of successful HTTP responses (status < 500) out of total valid requests",
      "measurement_method": "Datadog APM trace.http.request filtered to service:core-api, excluding health checks",
      "good_threshold": "Response status code < 500",
      "unit": "percentage"
    },
    {
      "name": "Read Latency",
      "metric": "Server-side latency of HTTP GET requests at p99",
      "measurement_method": "Datadog APM trace.http.request where http.method:GET and service:core-api",
      "good_threshold": "p99 < 300ms",
      "unit": "milliseconds"
    },
    {
      "name": "Write Latency",
      "metric": "Server-side latency of HTTP POST/PUT/PATCH/DELETE requests at p99",
      "measurement_method": "Datadog APM trace.http.request where http.method:POST|PUT|PATCH|DELETE and service:core-api",
      "good_threshold": "p99 < 500ms",
      "unit": "milliseconds"
    },
    {
      "name": "Error Rate",
      "metric": "Proportion of HTTP 5xx responses out of total requests",
      "measurement_method": "Datadog APM trace.http.request where http.status_code:5xx / total for service:core-api",
      "good_threshold": "Error rate < 0.1%",
      "unit": "percentage"
    },
    {
      "name": "Webhook Delivery Rate",
      "metric": "Proportion of webhooks successfully delivered out of total attempts",
      "measurement_method": "Prometheus webhooks_delivered_total / webhooks_attempted_total",
      "good_threshold": "Delivery rate > 99.5%",
      "unit": "percentage"
    }
  ],
  "slos": [
    {
      "sli_ref": "Availability",
      "target": "99.9%",
      "window": "rolling_28d",
      "rationale": "Achievable with current architecture. 99.99% would require multi-region active-active not justified by customer requirements.",
      "error_budget": "40.3 minutes downtime per 28 days"
    },
    {
      "sli_ref": "Read Latency",
      "target": "99.5% of GET requests < 300ms",
      "window": "rolling_28d",
      "rationale": "Current p99 is 280ms. Small buffer while signaling latency regressions need attention."
    },
    {
      "sli_ref": "Write Latency",
      "target": "99.5% of write requests < 500ms",
      "window": "rolling_28d",
      "rationale": "500ms is user-perceivable delay threshold for form submissions. Current p99 write is 350ms."
    },
    {
      "sli_ref": "Error Rate",
      "target": "99.9% non-5xx",
      "window": "rolling_28d",
      "rationale": "Equivalent to 0.1% error ceiling. Current rate is 0.08%."
    },
    {
      "sli_ref": "Webhook Delivery Rate",
      "target": "99.5%",
      "window": "rolling_28d",
      "rationale": "Accounts for customer endpoint failures outside our control while flagging systematic issues."
    }
  ],
  "error_budget_policy": {
    "thresholds": [
      {"budget_remaining": ">75%", "burn_rate": "<1x", "action": "Normal operations"},
      {"budget_remaining": "50-75%", "burn_rate": "1-2x", "action": "Review deploys for risk"},
      {"budget_remaining": "25-50%", "burn_rate": "2-5x", "action": "Reduce deploy frequency, prioritize reliability"},
      {"budget_remaining": "<25%", "burn_rate": ">5x", "action": "Deploy freeze for non-reliability changes"},
      {"budget_remaining": "0%", "burn_rate": "exhausted", "action": "Full deploy freeze, emergency reliability sprint"}
    ],
    "authority": "Engineering Lead initiates freeze. VP Engineering can override.",
    "resumption_criteria": "Budget recovers above 25% of 28-day window"
  },
  "alerting_rules": {
    "fast_burn": {
      "condition": "Error budget burn rate > 14.4x over 1 hour",
      "lookback": "5-minute sliding window",
      "routing": "PagerDuty -> Platform Team L1"
    },
    "slow_burn": {
      "condition": "Error budget burn rate > 3x over 24 hours",
      "lookback": "6-hour sliding window",
      "routing": "Jira ticket + Slack #reliability"
    },
    "budget_exhaustion": {
      "thresholds": ["75% -> Slack info", "50% -> Slack + email", "25% -> PagerDuty", "0% -> PagerDuty + all-hands"]
    }
  },
  "review_cadence": "Monthly SLO review (first Tuesday). Quarterly calibration.",
  "escalation_path": "1 month miss -> 20% sprint to reliability. 2 months -> dedicated workstream. 3 months -> executive review."
}
```
