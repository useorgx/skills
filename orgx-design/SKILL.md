---
name: orgx-design
version: '3.3.0'
description: "The canonical OrgX product design system and full-surface audit workflow. Use before building, redesigning, reviewing, cutting, or verifying any OrgX UI: core app pages, public marketing, onboarding, MCP widgets, overlays, public proof, artifact renderers, and responsive states. Triggers on OrgX design, UX, UI polish, design-system work, 'Ive-level', progressive disclosure, responsive audits, interaction quality, product theater, or requests to make a surface feel unmistakably OrgX."
---

# OrgX Design System — v3

Act as OrgX's uncompromising product-design lead. Ship interfaces that are
structurally inevitable, operationally sharp, emotionally composed, and
visually distinct from generic SaaS.

The product promise is not more management UI. It is a visible
**goal → plan → work → decision → artifact → proof → next action** loop.
Every surface must shorten that loop or get out of its way.

## Required Reading

Read each selected file completely before acting.

| File                                                                    | Required when                                                                                             |
| ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| [philosophy.md](references/philosophy.md)                               | Any new or redesigned visual surface. Read first.                                                         |
| [surface-audit.md](references/surface-audit.md)                         | Any page, flow, onboarding, responsive, consolidation, or removal work.                                   |
| [app-shell.md](references/app-shell.md)                                 | Any full-page authenticated app surface.                                                                  |
| [implementation-map.md](references/implementation-map.md)               | Editing OrgX React/CSS or choosing existing primitives.                                                   |
| [verification.md](references/verification.md)                           | Any work described as done, fixed, verified, responsive, or ready to ship.                                |
| [scorecard.md](references/scorecard.md)                                 | Before shipping any visual change.                                                                        |
| [modes-and-patterns.md](references/modes-and-patterns.md)               | Choosing layout, mode, content hierarchy, or microcopy.                                                   |
| [tokens.md](references/tokens.md)                                       | Writing or reviewing visual styling.                                                                      |
| [components.md](references/components.md)                               | Building layouts or reusable components.                                                                  |
| [marketing-product-theater.md](references/marketing-product-theater.md) | Public homepage, pricing, atmospheric imagery, embedded product demonstrations, or marketing UI fidelity. |
| [widget-sdk.md](references/widget-sdk.md)                               | MCP widgets, embedded HTML, protocol actions, or widget navigation.                                       |
| [distribution.md](references/distribution.md)                           | Editing or syncing this skill across tools.                                                               |

## Non-Negotiable Workflow

Do not jump from request to JSX. Record this compact design brief in working
notes, an audit artifact, or the implementation plan.

### 1. Establish truth

1. Inventory **existing / new / missing** product behavior before proposing.
2. Identify the canonical route, data owner, action owner, and replacement
   route for any proposed cut.
3. Separate repo truth, local-render truth, merged truth, deployed truth, and
   outcome truth. Never collapse them into “done.”
4. Trace the surface to the goal-to-value loop. Name the user value advanced.

### 2. Classify

1. Surface family: full-page app / MCP widget / overlay-dialog / public-proof.
2. Surface type: State / Action / Process / Executive Readout.
3. Mode: Command / Escalation / Creation / Readout.
4. Single-glance question: the one question answered in two seconds.
5. Attention state: Needs You / Progressing / Complete-Idle.
6. Primary user: new / returning / operator / reviewer / external viewer.

### 3. Compose

Define:

- the dominant signal and one primary action;
- what collapses when healthy;
- what reshapes when urgent;
- what is visible now versus disclosed later;
- the specific OrgX brand-world element doing real information work;
- the non-generic interaction or composition;
- the smallest proof that tells the user the system actually moved work.

Draft 2–3 materially different layouts mentally or on paper. Reject the
weaker structures by naming why they fail the user question, hierarchy, or
goal-to-value loop. Do not generate cosmetic variants of the same card grid.

### 4. Model the states

Specify every applicable state before implementation:

- loading or cold start;
- empty or first use;
- populated default;
- long content and long labels;
- degraded, disconnected, or error;
- Needs You / urgent;
- resolved, complete, or idle;
- permission-limited or unavailable.

A component that only works with ideal fixture data is not designed.

### 5. Implement from the system

Use existing OrgX primitives and tokens first. Extend the system only when the
new contract will be reused or removes repeated inconsistency.

- One visible H1 and one page-level primary action.
- One data owner and one action owner per user job.
- Flat information architecture; no card nesting or decorative containers.
- Progressive disclosure after three visible choices.
- URL-addressable selection when state should survive reload/share/back.
- 44px minimum touch targets and no horizontal overflow.
- No initial mutation, surprise autosave, duplicated fetches, or action on both
  pointer and click.
- Motion explains change; it never compensates for weak hierarchy.

### 6. Verify the rendered experience

Static inspection is not visual verification. Use the strongest available
browser/computer tool to inspect the real rendered route and use focused tests
for contracts. Required evidence is defined in
[verification.md](references/verification.md).

At minimum, inspect:

- desktop 1440px;
- tablet 768px;
- phone 375px;
- keyboard and visible focus;
- loading, empty, populated, long, degraded, urgent, and resolved states where
  applicable;
- overflow, touch targets, reduced motion, and back/Escape behavior.

Render locally with the offline fixture (`pnpm dev:ui`, profiles in
`docs/LOCAL_FIXTURE.md`). Full-page screenshots miss lazy-loaded imagery and
fixed/sticky chrome, so an "empty panel" in a full-page capture is not a
defect until a scrolled viewport capture confirms it.

### 7. Judge and cut

Run both gates:

1. The design scorecard: at least **85/100**, hierarchy at least 90%, and
   distinctiveness at least 80%.
2. OrgX artifact quality: the four lenses (judged, measured, observed,
   outcome) with **AQ ≥ 0.85** when the work is attached as an artifact.

Then remove anything that:

- duplicates another route, title, metric, action, or explanation;
- has no current core job or evidence of use;
- can be inferred without being shown;
- creates maintenance surface without shortening time-to-value.

Route removal additionally requires reference search, traffic or live-behavior
evidence where available, a canonical replacement, redirect preservation, and
tests. Full-license-to-cut is not license to break deep links.

Search for template-string links (`` `/plans/${id}` ``), MCP widget links,
email templates, and generated registries, not just quoted literals. When a
deletion is refused by tooling or review, record the verified cut list, its
replacements, and its redirects in the audit and leave the decision with the
owner. Never make a route unreachable another way (redirecting it, gating it)
to get the same result.

## Page Grammar

Authenticated core pages follow this information order:

1. Context and one H1.
2. Earned attention signal, only if it needs the user.
3. Dominant read that answers the page question.
4. Metric rail when metrics navigate meaningful detail.
5. Working area with one selected detail.
6. Inline action at the point of consequence.
7. Calm completion or proof.

Do not turn the grammar into seven boxes. Most steps should be typographic,
spatial, or interactive relationships on one continuous surface.

## Coherence Rules

These are the defects the September 2026 core-experience audit found on
nearly every page. Check them on every change; each one is cheap to see and
expensive to leave.

1. **The header is not a card.** `PageHero` is a flat region closed by one
   hairline. The only surface allowed to claim a tinted band is the
   `FocusBanner`, and only when tone is warning/danger. A boxed hero holding a
   boxed banner holding a boxed glyph is three levels of nesting.
2. **One name per destination.** The sidebar label, the page H1, and the
   browser title use the same noun (`Command` → H1 `Command`, `Playbooks` →
   H1 `Playbooks`). Two names for one place reads as two places.
3. **Say it once.** A subline under the H1 is not repeated under the first
   section; a banner headline is not paraphrased in a paragraph below it; a
   control ("Next unread", "Search") exists once per view; a row title is not
   repeated as its own subtitle; an item shown in "Needs you" is not listed
   again in the section beneath it.
4. **Omit empty sections; do not announce them.** Five headers that say
   "none" push the one section with work below the fold. When everything is
   empty, one quiet line replaces the whole group. Filter tabs whose counts
   are all zero are not rendered.
5. **One CTA per empty state.** An empty state carries exactly one action, in
   the page's action color, that completes the job in place (open the dialog)
   rather than sending the user to another page to start over.
6. **Guard computed numbers.** Never render a value whose units disagree with
   its target (`214,500% of 100%`), a percent above what the model allows, or
   a raw internal id as the primary label. Fix the derivation, add a test,
   and only then the formatting.
7. **No codenames or engineering status in product UI.** Internal program
   names (`Red Dot`, `IWMT`) and pipeline state (`backfill`, `write path`,
   `latest schema`) are replaced with what the user can do next.
8. **Healthy status is a line, not a panel.** "Execution truth is current" is
   ambient text beside the heading. Warning and danger earn the full strip.
9. **Label/value rows let the label keep its width.** Use
   `grid-template-columns: auto minmax(0, 1fr)` so the value wraps; a value on
   `auto` takes max-content and collapses the label beneath it.
10. **Every block sits on the page grid.** On marketing pages every section,
    theater, and strip uses the shared measure (`--hv3-max`); a bare child of
    `<main>` runs to the viewport edge. On app pages the hero and the working
    area share one left edge.

## Navigation Budget

The primary sidebar lists at most eleven destinations and must fit a 768px-tall
viewport without the nav scrolling; a destination below the fold is one nobody
finds. Rows are 36px for fine pointers and 44px under `pointer: coarse`.
Before adding a link, remove one or prove the new page is not a view of an
existing one. A page that leaves the nav keeps its route and gains a visible
entry point from the page that owns its job (Today → a "Daily brief" link on
Command; Council → the Agents roster).

## Attention Model

**Needs You** — the action is the component. Put it in first-paint, explain
consequence, and keep supporting context subordinate.

**Progressing** — show motion, owner, next checkpoint, and only the metrics that
change a decision. Detail stays collapsed until requested.

**Complete / Idle** — collapse to proof, timestamp, and next useful action.
Healthy work should not impersonate an alert.

## Kill List

Reject:

1. card-within-card layouts;
2. equal-volume sections;
3. decorative gradients, borders, badges, or motion;
4. dashboard metrics that do not navigate or change a decision;
5. labels announcing labels;
6. more than one primary action;
7. small pills for consequential decisions;
8. status labels that should be actions;
9. contextless progress bars;
10. giant avatars or illustrations with low information value;
11. duplicated page titles, fetches, filters, tabs, or action systems;
12. hover-only disclosure or icon-only controls without names;
13. raw anchors in MCP widgets;
14. versioned duplicate routes without a consolidation plan;
15. “award-winning” polish claims without rendered evidence;
16. a boxed page hero, or a banner nested inside one;
17. empty sections, zero-count filter tabs, or a second CTA in an empty state;
18. internal codenames, raw ids, or pipeline status as user-facing copy;
19. a nav label that differs from the H1 it opens;
20. marketing blocks off the page measure.

## Final Gate

Before shipping, answer:

1. What single question is answered in two seconds?
2. What user value moved closer, and what proof shows it?
3. What becomes quiet when healthy and dominant when urgent?
4. Can the user act at the point of consequence?
5. Is secondary detail progressively disclosed?
6. Does every visible element earn its space?
7. What makes this unmistakably OrgX rather than generic SaaS?
8. Did rendered desktop, tablet, phone, keyboard, and state evidence pass?
9. Is the design score at least 85/100 with the sub-gates met?
10. Are merged, deployed, and observed outcomes reported separately?
