# OrgX Design Modes, Patterns & Microcopy

## Design Modes

Beyond widget type, every OrgX surface operates in a **mode of expression**. The mode changes rhythm, density, motion, contrast, and focal mechanics — not just accent color.

### Command Mode
**When:** Agent status boards, multi-agent grids, operational dashboards
**Feel:** Dense, composed, quiet, confident. Strong horizontal scanning. Minimal drama.
**Design traits:**
- Tight vertical spacing (8–12px between elements)
- Metric rail as primary navigation
- Status communicated through tone colors, not labels
- Multiple items visible simultaneously (grid layout)
- Hovering reveals detail; default shows compressed state
- Typography weighted toward Label and Value voices; minimal Body

### Escalation Mode
**When:** Blocker banners, critical decisions, stalled agent alerts
**Feel:** Higher contrast, sharper grouping, action-forward, compressed context.
**Design traits:**
- The attention element dominates the card — other content dims or collapses
- Action buttons are large and verb-loaded
- Context is compressed to 1–2 lines maximum
- Color shifts from accent to danger/warning palette
- Spacing opens around the action area (breathing room for the decision)
- No drill-down sections visible — focus is singular

### Creation Mode
**When:** Scaffold visualization, initiative creation, onboarding flows
**Feel:** More atmospheric, deeper depth cues, controlled ambient motion, emotional payoff.
**Design traits:**
- Allowed to use ambient animation (orbs, drift, sparkle)
- Deeper shadows and glow effects (scaffold stage)
- 3D perspective transform on hover/cursor
- More vertical space — let the structure breathe
- Status narration (text describing what's happening in the build)
- This is the ONLY mode where celebration is appropriate

### Executive Readout Mode
**When:** Morning brief, org snapshot, summary views
**Feel:** Summary-oriented, fewer interactions, stronger narrative compression.
**Design traits:**
- Headline + subhead hierarchy (editorial, not operational)
- Minimal interactive elements — mostly read-only
- Data presented as insights, not raw numbers
- Wider line lengths for readability (max-width: 640px on text blocks)
- Sections separated by generous whitespace, not divider lines
- Exception-first ordering: blockers and anomalies surface before routine status

## Paired Rewrites: Great vs Mediocre

These concrete examples show what to aim for and what to reject.

### Example 1: Initiative Health Overview

**Mediocre:**
```
┌─────────────────────────────────┐
│ STATUS OVERVIEW                 │
│ ┌──────┐ ┌──────┐ ┌──────┐    │
│ │ On   │ │ At   │ │ Off  │    │
│ │Track │ │Risk  │ │Track │    │
│ │  3   │ │  1   │ │  1   │    │
│ └──────┘ └──────┘ └──────┘    │
│ [Progress bar: 65%]            │
│ ┌──────┐ ┌──────┐ ┌──────┐    │
│ │Card 1│ │Card 2│ │Card 3│    │
│ └──────┘ └──────┘ └──────┘    │
└─────────────────────────────────┘
```
Why it fails: Equal-volume cards. Status overview eyebrow announces what's already obvious. Progress bar without context. Three status categories given equal weight when only "At Risk" matters.

**Strong:**
```
┌─────────────────────────────────┐
│ [Health ring: 70]               │
│  ⚠ 1 workstream at risk        │  ← blocker dominates
│                                 │
│ ┌─ 5 ─┐ ┌─ 1 ─┐ ┌─ 12 ─┐     │  ← metric rail (tappable)
│  Strms   Blkd    Tasks         │
│                                 │
│ ▓▓▓▓▓▓▓░░ ▓▓▓▓░░░ ▓▓▓▓▓▓▓▓▓  │  ← signal strip (compressed)
│                                 │
│ [Detail panel for selected rail]│
│                                 │
│ Synced 2m ago    Open live →    │
└─────────────────────────────────┘
```
Why it works: Health ring is single-glance answer. Blocker banner appears only when relevant and dominates. Metric rail is scannable and interactive. Signal strip shows parallelism. Detail panel is on-demand, not always-visible.

### Example 2: Agent Card (Running State)

**Mediocre:**
```
┌─────────────────────────────────┐
│ [56px avatar with glow ring]    │
│ AGENT: Pace                     │
│ ROLE: Product                   │
│ STATUS: Running                 │
│ CURRENT TASK: Review PRD v2     │
│ [Progress: ████░░░░ 50%]       │
│ Started: 3m ago                 │
│ Est. complete: ~5m              │
│ [View Details] [Stop Agent]     │
└─────────────────────────────────┘
```
Why it fails: Avatar too large. Labels announce what's already clear from context. Status is passive text, not actionable. Progress bar without context. Small generic buttons.

**Strong:**
```
┌─────────────────────────────────┐
│ Pace · Product        ● running │  ← identity + status dot (pulsing)
│ Review PRD v2             ~5m ↗ │  ← task + remaining time
└─────────────────────────────────┘
```
Why it works: Two lines. Everything a running-state agent needs. The pulsing dot communicates "running" faster than a label. Time estimate is contextual. Whole card tappable for drill-down. In healthy state, this is all you see.

### Example 3: Decision Card

**Mediocre:**
```
┌─────────────────────────────────┐
│ DECISION                        │
│ ┌───────────────────────────┐   │
│ │ Approve pricing structure │   │
│ │ Priority: High            │   │
│ │ Agent: Pace               │   │
│ │ Created: 2h ago           │   │
│ └───────────────────────────┘   │
│ [Approve] [Reject] [View More]  │
└─────────────────────────────────┘
```
Why it fails: Card-within-card. "DECISION" label is redundant (the widget IS decisions). Small buttons for a big action. Metadata given equal weight to the decision itself. "View More" is passive.

**Strong:**
```
┌─ gradient line (amber) ─────────┐
│ Pace · Product           ● High │
│ Approve pricing tier structure  │  ← decision title dominates
│ Three-tier model with 40% bump…│  ← compressed context
│                                 │
│ ┌─────────────┐ ┌─────────────┐│
│ │ ✓ Approve   │ │ ✕ Reject    ││  ← 88px tall action buttons
│ │ Unblock now │ │ Return with ││
│ │             │ │ guidance    ││
│ └─────────────┘ └─────────────┘│
│                                 │
│ 1 of 3 pending    ▓▓░░░        │
└─────────────────────────────────┘
```
Why it works: Gradient line colored by urgency. Decision title is the dominant read. Context is compressed. Action buttons are large with verb + consequence. Pagination shows queue position.

## Microcopy Rules

Words shape the interface as much as layout. OrgX microcopy is action-loaded, compressed, and confident.

### Button Language

**Avoid:** Generic, passive verbs
- ❌ "View Details"
- ❌ "Learn More"
- ❌ "Submit"
- ❌ "OK"
- ❌ "Continue"

**Prefer:** Specific, action-loaded verbs that name the outcome
- ✅ "Review blocker"
- ✅ "Resume rollout"
- ✅ "Approve path"
- ✅ "Reject with guidance"
- ✅ "Unblock execution"
- ✅ "Launch initiative"
- ✅ "Resolve conflict"

### Banner Tone

Attention banners are **direct and operational**, not alarming or euphemistic.

- ❌ "Warning: There are issues that need your attention"
- ❌ "Heads up! Something went wrong"
- ✅ "2 workstreams blocked"
- ✅ "Pricing approval needed"
- ✅ "Agent stalled — missing context"

### Urgency Phrasing

Urgency is stated factually, never with exclamation marks or emotional language.

- ❌ "CRITICAL! Immediate action required!"
- ❌ "This is urgent and needs your attention right away"
- ✅ "Critical · Blocking 3 downstream tasks"
- ✅ "High · 2h since requested"

### Timestamps

Always relative and contextual:

- ✅ "Synced 2m ago"
- ✅ "Running for 14m"
- ✅ "Idle since yesterday"
- ✅ "~3h remaining"
- ❌ "Last updated: 2025-04-16T14:23:00Z"
- ❌ "April 16, 2025 at 2:23 PM"

### Summaries

Summaries compress, they don't narrate:

- ❌ "The initiative currently has 5 workstreams, of which 3 are on track and 1 is blocked"
- ✅ "5 streams · 1 blocked"
- ✅ "70% health · behind on marketing"

### Empty States

Empty states are calm and informative, not apologetic:

- ❌ "Oops! Nothing here yet 😅"
- ❌ "No data available at this time"
- ✅ "Agent on standby"
- ✅ "No pending decisions"
- ✅ "Queue clear — agents executing autonomously"

### Confirmation States

Confirmation is brief and moves to next context:

- ❌ "Your decision has been successfully submitted! The agent will now proceed with the approved action."
- ✅ "Approved — agent unblocked"
- ✅ "Rejected — guidance sent to Pace"

## Refuse These Outputs

If the surface you're building matches any of these descriptions, it's not ready. Revise.

1. **Safe but generic** — Clean, well-organized, could be any B2B product. No OrgX signature moves. No compression/expansion. No urgency-driven hierarchy.

2. **Over-labeled** — Every section has an eyebrow, every metric has a label, every list has a header. The labels take up more visual space than the data.

3. **Over-badged** — Status pills, urgency badges, count badges, type badges — badges everywhere. If you have more than 2 badge-type elements visible at once, consolidate.

4. **Over-animated** — Motion on hover, motion on load, motion on state change, ambient motion. If the surface has more than 2 simultaneous animations, it's a nightclub, not a control surface.

5. **Too many sections visible at once** — If the surface shows more than 3 distinct content sections simultaneously (not counting shell and footer), it's not collapsing enough. Use the metric rail pattern to toggle between sections.

6. **Clean enterprise template** — Rounded corners, card shadows, blue accent, tabbed navigation, sidebar. This is the default output of every UI generator. OrgX is not this. Add matte materiality, gradient line, urgency-driven layout, compression/expansion.

7. **Dashboard grid of equal cards** — Four equal-size cards showing different metrics. This is the #1 most generic SaaS layout. Replace with: single health anchor + metric rail + detail panel on demand.

8. **Celebration for routine work** — Green checkmarks, success banners, confetti, "Great job!" messages for normal operations. OrgX celebrates only in Creation Mode (scaffold). Everything else: silence is the happy path.
