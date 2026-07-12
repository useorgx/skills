# App-Shell Contract — the page layer above the widget

> The widgets follow this design system. The **pages** are where it breaks.
> Every full-page app surface (`/command`, `/initiatives`, `/decisions`,
> `/people`, `/businesses`, `/goals`, `/learn`, `/settings`) tends to drift
> back into the one thing the philosophy puts on the refuse list: a **dashboard
> grid of equal-volume cards**. This file is the enforcement layer. Read it
> before touching any page-level surface, not just MCP widgets.

## The one diagnosis

Almost every app page is fundamentally a **big list** (487 businesses, 446
people, 164 playbooks, 139 initiatives, 22 decisions) rendered **flat and
equal-volume** — nothing tells you which few to care about. That violates
Law #1 (hierarchy is earned by urgency, not category) on every page at once.
The fix is mostly **enforcement, not invention** — the primitives already
exist (`MetricRail`, `ListRow`, `PageHero`, `AppPageShell`).

## The one grammar (every page obeys this)

```
dominant signal → metric rail → selected detail → inline action → collapse to calm
```

A page is quiet unless the org needs judgment. When it does, **the blocker
becomes the interface** and everything else compresses.

## The six cross-cutting rules

### 1. Urgency-first ordering on every list
Lead with the subset that needs the operator, extracted and dominant; the
healthy long-tail compresses below or collapses. Initiatives leads with the
*at-risk*, not alphabetical. People leads with *stalled / recovery*, not the
first name. Businesses leads with *engaged / needs-next-action*, not 487
identical prospect cards. The most important signal must never render at the
same volume as noise.

### 2. The metric strip IS the navigation
`MetricRail` already supports `href` / `onClick` / `isActive` / `tone`. A
read-only stat header is a missed primitive. Wire each tile to filter the list
below (shareable `href` preferred — mirrors the `/initiatives` pattern).
Re-clicking an active narrowing tile clears it. This converts dead headers
into the interactive spine and kills most of the "where do I start" problem.

### 3. Color semantics — never teal-everywhere
`lime = execution · teal = health · amber = attention · iris = creation.`
Teal is **not** the universal button color. Consequences:
- Attention surfaces (decisions, approvals) use the **amber `attention`**
  button variant, and re-key the surface with
  `style={{ '--ox-primary-rgb': '249, 199, 112' }}` on `AppPageShell` so focus
  rings / selection / rail underlines read amber.
- A disabled / dead-end control (e.g. "Requires live runtime") must be muted
  (`ghost`/`outline` + reduced opacity) — never a saturated filled button.
- Accent is signal, not decoration. Don't give index icons three different
  accents for no semantic reason — one neutral treatment.

### 4. One banner, never two. Collapse empty states.
Say it once. A subhead + an "ATTENTION REQUIRED" section announcing the same
thing is a label announcing a label. And **omit, don't show** empty states:
"No stalled relationships", "No impact metric yet", "Set target" are rendered
silence taking space. Silence is the happy path — render nothing there.

### 5. One list-row primitive
Use `components/ui/list-row.tsx` (`ListRow`) for decisions / initiatives /
businesses / people / playbooks. Build once, skin per domain. Card grids of
one-card-per-entity at full volume are the worst offender — collapse the
long-tail into a count + dense rows.

### 6. Button hierarchy + verb-loaded microcopy
**One primary per view**, reserved for the thing that matters — not a filled
button on every row (that's equal-volume again). Copy is operational, not
passive: "Decide" → "Approve & unblock"; "Plan outreach" → "Plan next touch";
"Open guided builder" → "Scope initiative". Merge double pills (Status +
Priority) into a single urgency token: `Urgent · 5d`.

## Cut the decoration-as-information
Radar/sonar glyphs that inform nothing, unlabeled segment strips, progress
bars without a deadline. Law #3: if removing it loses no information, remove it.

## The page anatomy (target)

```
CONTEXT STRIP   workspace · live state · last sync · mode
ATTENTION STRIP only when something needs judgment (FocusBanner warning/danger)
DOMINANT READ   one answer in < 2s
METRIC RAIL     3–5 tappable tiles that filter the working area
WORKING AREA    list / board / graph (urgency-first)
RIGHT INSPECTOR appears only when an entity is selected
COMMAND         persistent, contextual composer
```

Healthy state collapses to identity + status + timestamp. Escalated state lets
the attention element dominate and makes the action large and verb-loaded.

## Reference implementation
`/decisions` (`app/decisions/page.client.tsx`) is the worked example of this
contract: amber attention surface, interactive `MetricRail`
(Pending / Urgent / All → filters), single urgency token replacing the
status+priority+updated triple, one amber primary ("Approve & unblock"),
urgency-first ordering, and the two teaching cards collapsed to one quiet line.
Copy its shape when rebuilding the other pages.

## The gate
For every page: (1) Can the dominant question be answered in < 2s? (2) Does
urgency reshape the layout? (3) Is the metric rail wired to the list? (4) Does
the healthy state go near-silent? (5) Would any block read as generic SaaS?
If any answer is unsatisfying, it is not ready.
