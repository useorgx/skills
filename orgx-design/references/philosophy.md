# OrgX Design Philosophy & Visual Language

This file defines what makes OrgX look, feel, and behave like OrgX — and nothing else. Read this before designing any new surface.

## The Three Laws

In priority order:

1. **Hierarchy is earned by urgency, not by category.** A blocker reshapes the entire card. An agent running clean barely whispers.
2. **Every border is a failure of spacing.** One container maximum. Inner grouping comes from whitespace and weight. Wells are reserved for inset interactive areas only (reject composer, scaffold stage).
3. **Decoration that doesn't inform is noise.** Progress bars without deadlines, glow effects without status — cut them.

## Brand World

OrgX is a **cognitive operating system for organizations**. The interface should feel like a mission-critical control surface — not a project management tool, not a dashboard builder, not enterprise SaaS.

The emotional register: **composed authority**. The person using OrgX is a decision-maker who delegates to autonomous agents. The UI exists to give them calm confidence that their organization is executing — and immediate, decisive control when it isn't.

### What OrgX is not

- Not playful (Notion)
- Not editorial-minimalist (Linear)
- Not dense-enterprise (Salesforce)
- Not developer-terminal (Warp)
- Not marketing-bright (Monday.com)

OrgX sits in its own lane: **instrument-grade control for autonomous operations**.

## Visual Language

### Materiality

**Matte instrument panel.** Smoked glass restraint. Precise edge lighting via the gradient line. Not glossy SaaS gradients. The surface should feel like a well-machined control panel — dark aluminum, recessed readouts, precision-cut bezels.

In practice:
- Backgrounds are flat and matte, never gradient-washed
- The single gradient line at card top is the *only* decorative gradient — it serves as an edge-light, like the seam where two panels meet
- Glass effects (backdrop-blur) are used sparingly and only for overlays, never as surface treatment
- No glossy buttons, no gradient fills on interactive elements

### Depth Model

**Shallow, deliberate depth.** No random elevation soup. The hierarchy is:

1. **Page background** — the deepest layer, with subtle grid texture
2. **Card** — one elevation step up, single shadow, the primary container
3. **Well** — recessed into the card for interactive insets (reject composer, scaffold stage)
4. **Overlay** — the only element that floats above the card (tooltips, modals)

Nothing else gets elevation. No stacked card layers. No floating badges. No shadow on inner sections.

### Line Behavior

Signal lines are **purposeful and sparse**. Every line communicates structure.

- The gradient line at card top = identity / accent
- Section dividers via `border-top` = content grouping
- Progress bar tracks = measurement
- Grid background = spatial context

No decorative lines, no double borders, no rule-as-ornament.

### Texture

Subtle system texture only when it improves the sense of control:

- Grid background on standalone pages = spatial grounding
- Gradient line on cards = edge definition
- Shimmer on skeletons = loading state

No noise textures, no patterns, no hatching, no grain.

### Color Role

**Accent color is signal, not decoration.**

- Per-widget primary identifies the tool's domain (lime = execution, teal = health, amber = attention, iris = creation)
- Tone colors carry semantic weight (good/warning/danger/muted)
- Accent never appears decoratively — no colored headers, no tinted backgrounds for aesthetics, no accent-colored section labels

The only places accent color appears:
- Gradient line (identity)
- Active states (selected rail item, focused button)
- Tone indicators (status pills, health rings, progress fills)
- Primary action buttons

### Motion Philosophy

**No playful motion.** Motion in OrgX serves exactly two purposes:

1. **Orientation** — helping the user understand state transitions (banner appearing, section collapsing, card resolving)
2. **Ambient presence** — only in Process widgets, where controlled emergence is the emotional intent (scaffold orbs, node drift)

Motion is never celebratory outside Process widgets. No bounce. No overshoot. No confetti. No spring physics on buttons. The easing is `cubic-bezier(0.16, 1, 0.3, 1)` — fast attack, smooth settle. Clinical.

### Density Ethic

**Compact but breathable.** Never airy just to look premium. Never dense just to look powerful.

The test: can you remove whitespace without losing hierarchy? If yes, it's too airy. Can you add whitespace without losing information density? If no, it's too dense.

OrgX density should feel like a well-organized flight deck — everything reachable, nothing wasted, breathing room only where it serves scanability.

## The OrgX Signature Moves

These are the design patterns that, taken together, make something feel unmistakably OrgX:

1. **The gradient line** — a single 1px edge-light across the card top, colored by widget primary. Present on every card. The signature OrgX detail.

2. **Urgency-driven hierarchy** — the entire layout reshapes based on what needs attention. Not tabs, not equal sections — the blocker *becomes* the interface.

3. **Compression/expansion** — healthy state compresses to near-nothing. Urgent state expands to dominate. The surface breathes based on operational state, not user preference.

4. **The metric rail** — a tab-bar of tappable metrics that selects detail panels below. Compact, scannable, interactive. OrgX's answer to the dashboard grid.

5. **Surveillance calm** — when everything is fine, OrgX barely speaks. No congratulatory banners, no green-means-good celebrations. Silence is the healthy state.

6. **Card-height action buttons** — decisions are not afterthought pills. They are 88px tall with icon + title + subtitle. The action is the interface.

## Surface Emotional Registers

Different surfaces carry different emotional weight. Match the register:

| Surface | Emotional register | Design implication |
|---------|-------------------|-------------------|
| Agent status (healthy) | Quiet confidence | Near-invisible. Identity + timestamp. |
| Agent status (blocked) | Controlled urgency | Banner dominates. Context compressed. Action prominent. |
| Initiative pulse | Analytical calm | Health ring anchors. Metrics scannable. Signal strip shows parallelism. |
| Decision queue | Weighted deliberation | Context rich but compressed. Actions large and clear. Urgency colors the frame. |
| Scaffold complete | Earned satisfaction | Emergence animation. Structure visible. Ambient atmosphere. This is the *only* place OrgX celebrates. |
| Morning brief | Executive composure | Narrative summary. Minimal interaction. Strong editorial hierarchy. |
