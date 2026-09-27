# Agent Work Receipt: the record shape for agent work

`@useorgx/agent-work-receipt` (`agent-work-receipt/v0.1`, Apache-2.0) is the
published contract for recording what an agent was asked to do, what authority
it had, what it did, what changed, how the result was checked, and what it cost.
It is account-free: no OrgX workspace, UUID, or database row is required, and
every cross-system identifier is an opaque `{ system, type, id }` reference owned
by its producer. Git commits, GitHub pull requests, MCP calls, A2A tasks,
deployments, and OpenTelemetry traces all fit without translation.

Use its vocabulary when you describe your own work, whichever runtime you are
in. A receipt the producer can validate against a schema beats prose, and beats
a shape that only one system understands.

## The records

Required: `intent`, `actor`, `authority`, `actions`, `artifacts`, `evidence`,
`outcome`, `verification`, `cost`, `lineage`, `human_interventions`,
`timestamps`. Hashes and signatures are optional under `integrity`.

Four of them carry the weight, and three of those four are what hand-rolled
records usually miss.

| Record | Required fields | What it is for |
| --- | --- | --- |
| `intent` | — | What you were asked to do, in your own words |
| `authority` | `mode`, `status`, `scope` | What you were allowed to do, and by whom |
| `verification` | `status`, `method`, `checks`, `evidence_ids` | How the result was checked, by something other than your own say-so |
| `outcome` | `status`, `summary` | What actually changed, plus `acceptance` when a human accepted it |

## How OrgX's own mechanisms fill them

- **`authority.mode`** is the workspace's autonomy mode: `manual`, `gated`, or
  `autopilot`. **`authority.scope`** is what that mode permits.
  **`authority.approvals`** holds the approvals you were granted, and
  `authority.constraints` the budget or time limits you ran under.
- **`verification.checks`** is the evidence a skeptic can re-run: a command with
  its exit code, an HTTPS probe with its status, or an independent judge. Declare
  the checks **before** you build, not after — a check written to match what you
  already produced verifies nothing. Where the OrgX hook shim is installed,
  `orgx-agent criteria set` records them, and the Stop hook runs the command
  checks in your working copy before the session is allowed to end.
- **`human_interventions`** is every point a human had to act. The autonomy floor
  stops eight classes of action at the point of action — `merge`, `force_push`,
  `deploy`, `publish`, `destructive`, `send`, `spend`, `prod_data` — and files an
  OrgX decision (`decision_type: agent_action`) in the owner's decision inbox.
  Only a signed-in human can resolve it; no API key can, including yours.
  Approval covers exactly that one command, once. A denial is not a failure to
  hide: record it as an intervention, carry on with other work, and never retry
  or work around it.
- **`outcome.status`** is how far the work actually got, not how far you intended
  it to get. "Wrote files into a scratch directory" is not `drafted`; a branch
  with commits is. A PR is not merged. Merged is not deployed. Deployed is not
  proven in production. **`outcome.acceptance`** is a human accepting the result,
  which is a separate fact from your verification passing.
- **`cost`** and **`lineage`** are what make a receipt comparable to other
  receipts: what it cost, and which run, initiative, or parent work it belongs
  to.

## What makes a check a check

Measured on 2026-09-27, across seven agents that were each forced to declare
criteria before their session could end: every one of them wrote the criteria
*after* finishing, and every machine check asserted the existence of a file the
agent had just written. All seven passed. None had verified anything. These are
the shapes to refuse, in your own work and in review.

**A check that cannot fail.** One agent declared:

```
test $(tail -n +2 prospects.csv | wc -l) -ge 100 || echo "FAIL: <100 prospects"
```

It printed `FAIL: <100 prospects`, exited `0`, and was recorded as a pass,
because `|| echo` swallows the exit status. Anything ending `|| echo`,
`|| true`, `; true`, or piped into `head`/`tail`/`cat` reports the last
command's status, not the check's. Write the check so a shell can only exit
non-zero when the work is missing.

**A check that was already green when you wrote it.** `test -f the-doc-I-just-wrote.md`
passes the moment it is declared, so it cannot distinguish done from not-done.
A criterion earns trust only by being seen to fail while the work is absent and
pass once it is present. Declare it first, watch it fail, then make it pass.
That is also the cheapest way to discover that your check tests the wrong
thing.

**Prose in place of a check.** One agent declared eight criteria and wrote seven
of them as rubrics for a future judge, leaving one file-existence check to carry
the whole claim. Prose records intent; it verifies nothing. Keep it if it helps a
reader, but never let it stand in for `verification.checks`.

**Weakening the check instead of the claim.** One agent replaced "the landing
page responds at its URL" with "the spec file mentions Calendly" and reported
success. If a criterion turns out to belong to someone else's scope, narrow the
*claim* — say what you did and did not do — and leave the criterion honest. Never
edit the test until it passes.

**A shell error is not a pass.** `test: $count: integer expression expected` with
exit `0` means the shell could not run what you wrote, so its exit status says
nothing. Read the output, not just the code.

## Relationship to `metadata.artifact_contract`

The OrgX MCP artifact contract is the projection of these records onto an
attached artifact. Keep sending it — it is what `orgx_attach` and the four-lens
verification read — and treat AWR as the fuller shape it maps onto:

| `metadata.artifact_contract` | Agent Work Receipt |
| --- | --- |
| `agent_type` | `actor` |
| `company_stage` | context on `intent` |
| `business_outcome` | `intent`, and `outcome.summary` once it is real |
| `owner` | `actor`, or `authority.delegated_by` when delegated |
| `review_date` | `timestamps`, `verification.verified_at` |
| `verification` | `verification.{status,method,checks,evidence_ids,verifier}` |
| — | `authority`, `human_interventions`, `cost`, `lineage` |

The last row is the upgrade. A record with no `authority` cannot say whether the
work was allowed; with no `human_interventions` it cannot say where a human was
needed; with no `cost` or `lineage` it cannot be compared with anything else.

## Using the package

```bash
npm install @useorgx/agent-work-receipt
```

It ships the JSON Schema (Draft 2020-12), TypeScript types, and a validator, and
makes no network calls. Validate before you claim a receipt is well formed.
