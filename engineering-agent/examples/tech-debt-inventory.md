# Tech Debt Inventory: Payment Processing Service

## Metadata

- **Inventory Date**: 2026-03-15
- **Scope**: `payment-service` repository (Node.js/Express)
- **Author**: Engineering Agent
- **Last Updated**: 2026-03-15
- **Review Cadence**: Monthly

## Executive Summary

The payment-service carries 11 identified tech debt items totaling an estimated 22-28 person-weeks of remediation effort. Three items are rated critical: the Node.js 16 runtime (EOL since September 2023), the hand-rolled retry mechanism responsible for two P2 incidents last quarter, and the outdated Stripe SDK with 3 unpatched CVEs. The service processes $2M/month in transactions, making reliability debt particularly high-impact.

Recommended allocation: 20% of sprint capacity (approximately 1.6 person-days/week across the 3-person team) dedicated to debt reduction, prioritized by the backlog below.

## Inventory

### TD-001: Node.js 16 Runtime (End of Life)

- **Category**: infrastructure
- **Severity**: critical
- **Effort Estimate**: M (5-8 person-days)
- **Blast Radius**: Entire service. No security patches since September 2023. Any newly discovered V8 or OpenSSL vulnerability is unpatched in production. Compliance audit risk for SOC2 and PCI-DSS.
- **Interest Rate**: accelerating — CVE exposure grows with every month on an unsupported runtime, and the upgrade difficulty increases as transitive dependencies drift further from Node.js 16 compatibility.
- **Evidence**: `package.json` specifies `"engines": { "node": "16.x" }`. Node.js 16 EOL announced April 2023, entered EOL September 2023. CI runs on `node:16-alpine`. Three CVEs published for Node.js 16 since EOL: CVE-2023-44487 (HTTP/2 rapid reset, severity HIGH), CVE-2024-22019 (HTTP request smuggling, severity HIGH), CVE-2024-21896 (path traversal, severity MEDIUM).
- **Proposed Fix**: Upgrade to Node.js 20 LTS (supported until April 2026) or Node.js 22 LTS (supported until April 2027). Steps: (1) run `npx ncu` to identify dependency conflicts, (2) update test matrix to run on both 16 and 20, (3) fix breaking changes (likely in `crypto` and `fs` modules), (4) update Dockerfile base image, (5) canary deploy to 10% traffic for 48 hours, (6) full rollout. Rollback: revert Dockerfile to `node:16-alpine`.

### TD-002: Hand-Rolled Retry Mechanism

- **Category**: architecture
- **Severity**: critical
- **Effort Estimate**: M (5-8 person-days)
- **Blast Radius**: All outbound API calls (Stripe, email provider, webhook delivery). Current implementation retries with fixed 1-second delay, no jitter, no exponential backoff, no circuit breaker. Under provider degradation, this creates retry storms that amplify the outage. Directly caused P2-2026-007 and P2-2026-011.
- **Interest Rate**: accelerating — every new outbound integration added to the service inherits this broken retry behavior, increasing blast radius. Transaction volume is growing 15% MoM, meaning retry storms get proportionally worse.
- **Evidence**: `src/lib/retry.ts` lines 12-34: `setTimeout(fn, 1000)` in a loop with `maxRetries: 5`. No backoff multiplier. No jitter. No circuit breaker state. Incident P2-2026-007 timeline shows 5x amplification of Stripe API calls during a 30-minute Stripe degradation. Incident P2-2026-011 shows identical pattern with email provider.
- **Proposed Fix**: Replace with a battle-tested retry library (`p-retry` or `cockatiel`) configured with: exponential backoff (base 1s, multiplier 2x, max 30s), full jitter, circuit breaker (open after 5 failures in 60s, half-open after 30s). Add per-provider retry configuration. Add retry metrics (attempts, successes, circuit breaker state) to the dashboard. Steps: (1) add library and write adapter matching current interface, (2) write unit tests covering backoff timing, jitter distribution, and circuit breaker transitions, (3) deploy with feature flag, (4) enable for email provider first (lower risk), (5) enable for Stripe after 1 week, (6) remove old code. Rollback: disable feature flag.

### TD-003: Outdated Stripe SDK

- **Category**: dependency
- **Severity**: critical
- **Effort Estimate**: S (3-4 person-days)
- **Blast Radius**: All payment processing. Current version (stripe@10.x) is 2 major versions behind (current: stripe@12.x). Three unpatched CVEs in our version. Missing access to Stripe's latest payment method types, which blocks the product roadmap item for Apple Pay support.
- **Interest Rate**: accelerating — Stripe deprecates older API versions on a rolling 2-year window. We are 18 months into the deprecation window for the API version our SDK targets. In 6 months, Stripe may begin returning errors for our API version.
- **Evidence**: `package.json`: `"stripe": "^10.17.0"`. Stripe changelog shows breaking changes in v11 (webhook signature verification API change) and v12 (PaymentIntent flow refactor, TypeScript strict mode). CVE-2025-0001 (webhook signature bypass, severity HIGH), CVE-2025-0034 (insufficient input validation, severity MEDIUM), CVE-2025-0089 (timing attack on API key comparison, severity MEDIUM).
- **Proposed Fix**: Upgrade to stripe@12.x. Steps: (1) audit all Stripe API calls in codebase (grep for `stripe.` — 47 call sites identified), (2) create branch and upgrade, (3) fix webhook signature verification (breaking change in v11), (4) update PaymentIntent flow to new API (breaking change in v12), (5) run full test suite (payment integration tests are comprehensive here), (6) test against Stripe's test mode, (7) canary deploy processing $0 test transactions for 24 hours, (8) gradual rollout. Rollback: revert to stripe@10.x (full backward compatibility with current Stripe API version for another 6 months).

### TD-004: Slow Test Suite (25 Minutes)

- **Category**: testing
- **Severity**: high
- **Effort Estimate**: M (5-8 person-days)
- **Blast Radius**: Developer productivity across entire team. 25-minute test suite means developers run tests infrequently, batch changes into larger PRs, and skip local testing in favor of CI. This degrades DORA lead time metric and increases change failure rate because bugs are caught later.
- **Interest Rate**: linear — test count grows by approximately 15 tests/month. At current trajectory, suite will exceed 30 minutes within 4 months.
- **Evidence**: CI metrics show average suite duration of 25m12s (p50) and 31m45s (p95). Test count: 847 tests. Test pyramid analysis: 112 unit tests (13%), 623 integration tests (74%), 112 end-to-end tests (13%). Healthy pyramid would be approximately 60/30/10. Integration test overhead accounts for ~18 minutes (each test starts a database transaction and seeds test data).
- **Proposed Fix**: (1) Identify the 50 slowest tests and optimize or reclassify them. (2) Convert integration tests that don't actually need a database into unit tests with mocked dependencies (target: move 200 tests from integration to unit tier). (3) Parallelize remaining integration tests across 4 workers (current: single-threaded). (4) Implement shared test fixtures to reduce per-test database setup. Target: under 8 minutes wall clock. Steps: (1) add timing instrumentation to identify slowest tests (1 day), (2) reclassify and convert tests (3-4 days), (3) add parallel runner configuration (1 day), (4) optimize fixtures (1-2 days).

### TD-005: Flaky Tests (6 Known)

- **Category**: testing
- **Severity**: high
- **Effort Estimate**: S (2-3 person-days)
- **Blast Radius**: CI reliability and team trust in the test suite. 6 flaky tests cause approximately 15% of CI runs to fail spuriously. Team has developed a habit of re-running failed CI without investigating, which means real failures are occasionally ignored.
- **Interest Rate**: linear — flaky tests erode trust gradually. Each new flaky test makes the problem incrementally worse and makes the team more likely to ignore CI failures.
- **Evidence**: CI failure analysis (last 30 days): 47 pipeline failures, 31 (66%) were flaky test failures. Flaky tests identified: `test/payment/webhook-race.spec.ts` (timing-dependent), `test/payment/concurrent-charge.spec.ts` (database ordering assumption), `test/notification/email-send.spec.ts` (external API mock instability), `test/payment/refund-idempotency.spec.ts` (shared test state), `test/health/readiness.spec.ts` (port binding race), `test/payment/stripe-retry.spec.ts` (setTimeout sensitivity).
- **Proposed Fix**: Fix each flaky test individually. Common patterns: (1) replace `setTimeout` timing assertions with event-based waits, (2) isolate database state per test (no shared mutation), (3) use deterministic mocks for external APIs, (4) add retry with `jest.retryTimes(2)` as a temporary measure while root-causing. Add a flaky test detector to CI that quarantines newly flaky tests automatically.

### TD-006: Inconsistent Error Handling

- **Category**: code-quality
- **Severity**: high
- **Effort Estimate**: L (8-12 person-days)
- **Blast Radius**: Error observability and incident response time. Mix of `try/catch`, `.catch()`, and unhandled promise rejections makes it impossible to implement consistent error monitoring. Some errors are logged, some are swallowed, some crash the process. Increases MTTR because errors are hard to trace.
- **Interest Rate**: linear — every new feature added using inconsistent patterns makes the eventual cleanup harder, but the core risk (unhandled rejections crashing the process) does not compound.
- **Evidence**: Grep analysis: 89 `try/catch` blocks, 43 `.catch()` chains, 12 locations with no error handling on async operations. `process.on('unhandledRejection')` handler logs but does not prevent process exit in Node.js 16+ default behavior. Sentry shows 23 unique unhandled rejection events in the past 30 days, 8 of which resulted in container restarts.
- **Proposed Fix**: (1) Establish an error handling standard: all async operations use `try/catch` with a shared `handleError(error, context)` utility that classifies, logs, and reports errors. (2) Add ESLint rule `no-floating-promises` to prevent new unhandled promises. (3) Remediate existing code in priority order: payment processing paths first, then notification paths, then administrative paths. (4) Add global unhandled rejection handler that gracefully drains connections before exiting.

### TD-007: No Structured Logging

- **Category**: infrastructure
- **Severity**: medium
- **Effort Estimate**: S (3-4 person-days)
- **Blast Radius**: Incident investigation speed. Current logging uses `console.log` with string interpolation. No structured fields, no request correlation IDs, no log levels. Finding relevant logs during an incident requires searching for exact string matches.
- **Interest Rate**: stable — the problem doesn't get worse over time, but it consistently adds 15-30 minutes to every incident investigation.
- **Evidence**: Grep for `console.log`: 156 occurrences. Grep for structured logger (winston, pino, bunyan): 0 occurrences. Incident P2-2026-007 retro noted "took 20 minutes to correlate retry logs with the originating request" as a contributing factor to resolution time.
- **Proposed Fix**: (1) Add `pino` as the logging library (chosen for performance in hot paths — payment processing). (2) Configure with JSON output, request correlation ID injection via middleware, and standard fields (service, environment, version). (3) Replace `console.log` calls incrementally, starting with payment processing paths. (4) Add log level configuration via environment variable.

### TD-008: Missing Database Indexes

- **Category**: infrastructure
- **Severity**: medium
- **Effort Estimate**: XS (1 person-day)
- **Blast Radius**: Query performance on `notification_logs` table (currently 45M rows). Two queries in the notification path do full table scans: `SELECT * FROM notification_logs WHERE user_id = ? AND created_at > ?` and `SELECT COUNT(*) FROM notification_logs WHERE status = 'pending'`.
- **Interest Rate**: accelerating — table grows by approximately 2.3M rows/month. Query performance degrades linearly with table size. Currently at 200ms for the user query; will exceed 500ms within 3 months at current growth rate.
- **Evidence**: `EXPLAIN ANALYZE` output for both queries shows sequential scan. Query timing from APM: user_id query averages 200ms (p50), 450ms (p95). Pending count query averages 800ms (p50), 1.2s (p95). No index on `(user_id, created_at)` or `(status)` for the notification_logs table. Index on `(user_id)` alone exists but doesn't cover the compound query.
- **Proposed Fix**: Add two indexes: `CREATE INDEX CONCURRENTLY idx_notification_logs_user_date ON notification_logs(user_id, created_at DESC)` and `CREATE INDEX CONCURRENTLY idx_notification_logs_status ON notification_logs(status) WHERE status = 'pending'` (partial index). Use `CONCURRENTLY` to avoid locking the table during creation. Estimated index creation time: 10-15 minutes for 45M rows. Verify with `EXPLAIN ANALYZE` post-creation.

### TD-009: Hardcoded Configuration Values

- **Category**: code-quality
- **Severity**: medium
- **Effort Estimate**: S (2-3 person-days)
- **Blast Radius**: Deployment flexibility and 12-Factor compliance. Rate limits, retry counts, timeout values, and feature thresholds are hardcoded in source files. Changing any operational parameter requires a code deploy.
- **Interest Rate**: stable — doesn't compound but consistently blocks fast operational response. During incident P2-2026-011, the team wanted to increase the Stripe timeout from 10s to 30s but had to wait for a deploy pipeline.
- **Proposed Fix**: (1) Create a `config.ts` module that reads all operational parameters from environment variables with sensible defaults. (2) Extract all hardcoded values to this module. (3) Document each configuration parameter. (4) Consider adding a runtime config reload mechanism for critical operational parameters.

### TD-010: No Health Check Endpoint Granularity

- **Category**: infrastructure
- **Severity**: medium
- **Effort Estimate**: XS (0.5 person-days)
- **Blast Radius**: False-positive healthy status during partial outages. Current health check (`/health`) returns 200 if the Express process is running, regardless of database connectivity, Stripe API reachability, or email provider status. Kubernetes continues routing traffic to pods that cannot process payments.
- **Interest Rate**: stable — the risk is constant but the consequence is severe when it occurs (during incident P2-2026-007, healthy pods were serving 500 errors for 12 minutes before manual intervention).
- **Evidence**: `src/routes/health.ts`: returns `{ status: 'ok' }` unconditionally. No dependency checks. Kubernetes liveness probe hits this endpoint. Incident P2-2026-007 timeline: database connection pool exhausted at 14:02, health check still returning 200, traffic continued routing to degraded pods until manual intervention at 14:14.
- **Proposed Fix**: (1) Split into `/health/live` (process is running) and `/health/ready` (all dependencies reachable). (2) Readiness check verifies: database connection (run `SELECT 1`), Stripe API key validity (cached check, refresh every 60s), email provider reachability (cached check). (3) Configure Kubernetes readiness probe to use `/health/ready`. (4) Add `/health/startup` for slow-starting pods.

### TD-011: Missing API Rate Limiting

- **Category**: architecture
- **Severity**: medium
- **Effort Estimate**: S (2-3 person-days)
- **Blast Radius**: Service availability during traffic spikes or abuse. No rate limiting on any endpoint. A misbehaving client or attacker can exhaust the service's capacity. The 10x traffic spike that triggered incident P2-2026-007 could have been mitigated with rate limiting.
- **Interest Rate**: linear — risk grows with the service's public exposure and client count.
- **Evidence**: No rate limiting middleware in `src/middleware/` directory. Express app mounts no throttling layer. Load test shows the service accepts connections until process memory is exhausted.
- **Proposed Fix**: (1) Add `express-rate-limit` with Redis-backed store (for multi-pod consistency). (2) Configure per-endpoint limits: payment endpoints at 100 req/min per API key, webhook endpoints at 1000 req/min per source IP, health endpoints unlimited. (3) Return `429 Too Many Requests` with `Retry-After` header. (4) Add rate limit metrics to dashboard.

## Prioritized Backlog (Top 5)

Ranked by impact-to-effort ratio, weighted for the financial service context where reliability debt carries outsized risk.

| Rank | Item | Rationale |
|------|------|-----------|
| 1 | **TD-002: Hand-Rolled Retry** | Highest impact: directly caused 2 P2 incidents last quarter, affects all outbound calls, and risk compounds with traffic growth. Medium effort. Fix eliminates the single largest known reliability risk. |
| 2 | **TD-003: Outdated Stripe SDK** | Critical security exposure (3 CVEs) on the payment processing path. Relatively small effort (S). Stripe API version deprecation creates a hard deadline. Blocks Apple Pay product roadmap item. |
| 3 | **TD-001: Node.js 16 EOL** | Foundational infrastructure debt. Every day on an unsupported runtime is a compliance and security risk. Medium effort but well-understood upgrade path. Must be done before any other major dependency upgrades. |
| 4 | **TD-010: Health Check Granularity** | Tiny effort (XS, half a day) with disproportionate impact on incident response. Prevents the specific failure mode from P2-2026-007 where degraded pods continued receiving traffic. |
| 5 | **TD-008: Missing Database Indexes** | Tiny effort (XS, 1 day) with immediate measurable performance improvement. The accelerating interest rate (table grows 2.3M rows/month) means delaying this makes the queries progressively worse. |

## Cost Summary

- **Total Estimated Cost**: 24 person-weeks (range: 20-30 person-weeks depending on complexity discovered during remediation)
- **Critical Items Only**: 8 person-weeks (TD-001, TD-002, TD-003)
- **Quick Wins (XS/S effort)**: 6 person-weeks (TD-003, TD-005, TD-007, TD-008, TD-009, TD-010)
- **Recommended Budget**: 20% of sprint capacity allocated to debt reduction
  - Team capacity: 3 engineers * 5 days/week = 15 person-days/week
  - 20% allocation: 3 person-days/week = 0.6 person-weeks/week
  - Time to clear critical items at this rate: approximately 13 weeks
  - Time to clear all items at this rate: approximately 40 weeks

## Tracking

Review this inventory monthly. For each item, track:
- Status: `open` | `in-progress` | `resolved` | `accepted` (deliberately not fixing)
- If `accepted`, document the rationale and conditions that would change the decision
- If `resolved`, link to the PR(s) that fixed it and verify the fix with the evidence criteria

## Risk Note

This service processes $2M/month in transactions. The three critical items (TD-001, TD-002, TD-003) collectively represent: unpatched security vulnerabilities on a financial service, a retry mechanism that amplifies outages, and a runtime that receives no security updates. The recommended prioritization treats these as a single "reliability sprint" to be completed before any new feature work on this service.
