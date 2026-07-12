# OrgX Component Patterns

Reusable patterns from the live widget system. Each pattern includes the semantic structure, CSS approach, and interaction model.

## Shared Foundation

All widgets load `shared/widget-foundation.css` for base tokens and `shared/interaction-kit.css` + `shared/interaction-kit.js` for interactive components (buttons, links, tooltips). Widget-specific styles go in inline `<style>` blocks.

## Pattern: Widget Shell

The hero card that introduces every widget. Standard across all widget types.

```html
<div class="widget-shell-card animate-in">
  <div class="ox-card">
    <div class="ox-card-inner">
      <div class="widget-hero">
        <div class="widget-hero-copy">
          <div class="widget-kicker">Operator Queue</div>
          <div class="widget-title-lg">Action required</div>
          <div class="widget-subtitle">Approve to unblock execution...</div>
        </div>
        <div class="widget-icon-frame"><!-- 20px SVG icon --></div>
      </div>
    </div>
  </div>
</div>
```

- `widget-kicker`: Label voice (mono, 0.64rem, uppercase, 0.14em tracking)
- `widget-title-lg`: Value voice (clamp(1.4rem, 3.2vw, 1.92rem), weight 700, -0.05em tracking)
- `widget-subtitle`: Body voice (0.86–0.92rem, `--ox-text-muted`)
- `widget-icon-frame`: right-aligned icon container

## Pattern: Attention Banner

Appears when the component needs human action. Two variants exist:

### Inline Banner (agent-status style)
```html
<div class="attention-banner">
  <div class="attention-left">
    <svg class="attention-icon"><!-- 18px --></svg>
    <span class="attention-text">Blocked: Waiting on pricing approval</span>
  </div>
  <button class="attention-action">Resolve</button>
</div>
```

### Expandable Banner (initiative-pulse style)
```html
<button class="pulse-attention">
  <div class="pulse-attention__icon"><!-- 30px icon container --></div>
  <div class="pulse-attention__body">
    <div class="pulse-attention__eyebrow">Needs attention</div>
    <div class="pulse-attention__headline">2 workstreams blocked</div>
  </div>
  <svg class="pulse-attention__chevron"><!-- chevron-down --></svg>
</button>
```

The expandable variant is clickable — chevron rotates on `.is-open`, revealing a detail panel below.

## Pattern: Health Ring (initiative-pulse)

SVG donut chart — the single-glance answer for initiative health.

```html
<div class="pulse-health tone-warning">
  <svg viewBox="0 0 42 42">
    <circle class="pulse-health__track" cx="21" cy="21" r="17.5" />
    <circle class="pulse-health__bar" cx="21" cy="21" r="17.5"
            stroke-dasharray="110" stroke-dashoffset="33" />
  </svg>
  <div class="pulse-health__value">
    <span class="pulse-health__number">70</span>
    <span class="pulse-health__label">Health</span>
  </div>
</div>
```

- Width: 116px. Track: `stroke-width: 5`, gray. Bar: `stroke-width: 5`, primary color.
- Tone changes bar color: `.tone-warning` → amber, `.tone-danger` → red.
- Circumference = 2π × 17.5 ≈ 110. `stroke-dashoffset = 110 × (1 - progress/100)`.
- SVG rotated -90deg so bar starts at 12 o'clock.
- Inner glow via `::before` pseudo with radial gradient.

### Mini Ring (inline in lists)
34px version for list trailing elements:
```html
<div class="pulse-mini-ring tone-good">
  <svg viewBox="0 0 42 42">
    <circle class="pulse-mini-ring__track" cx="21" cy="21" r="17.5" />
    <circle class="pulse-mini-ring__bar" cx="21" cy="21" r="17.5"
            stroke-dasharray="110" stroke-dashoffset="44" />
  </svg>
  <span class="pulse-mini-ring__value">60%</span>
</div>
```

## Pattern: Metric Rail (pulse-rail)

Tab-bar style metric row. Clicking selects and shows the corresponding detail panel.

```html
<div class="pulse-rail">
  <button class="pulse-rail-button is-active">
    <span class="pulse-rail-icon"><!-- 18px SVG --></span>
    <span class="pulse-rail-value">5</span>
    <span class="pulse-rail-label">Streams</span>
  </button>
  <button class="pulse-rail-button is-alert">
    <span class="pulse-rail-icon"><!-- 18px SVG --></span>
    <span class="pulse-rail-value">3</span>
    <span class="pulse-rail-label">Blocked</span>
  </button>
  <!-- ... -->
</div>
```

- `grid-template-columns: repeat(4, minmax(0, 1fr))`
- Active state: `is-active` → colored underline bar via `::after`, icon takes `--ox-primary`
- Alert state: `is-alert` → danger coloring on value + icon, red underline
- The `::after` underline: 3px, `border-radius: 999px`, `scaleX(0.62)` default → `scaleX(1)` on hover/active
- Each button toggles a detail panel below via JS

## Pattern: Signal Strip

Compact parallel progress bars for workstreams.

```html
<div class="pulse-signal-strip">
  <button class="pulse-signal" title="Workstream A: 80%">
    <span class="pulse-signal__fill" style="width: 80%"></span>
  </button>
  <button class="pulse-signal" title="Workstream B: 45%">
    <span class="pulse-signal__fill tone-warning" style="width: 45%"></span>
  </button>
</div>
```

- Each signal: `flex: 1 1 0`, height `7px`, rounded
- Fill uses tone classes for coloring
- Clickable — selects that workstream in the detail panel

## Pattern: Decision Card (action widget)

```html
<div class="decision-card urgency-high animate-in">
  <div class="ox-card">
    <div class="ox-card-inner">
      <div class="decision-header">
        <div class="decision-header-copy">
          <div class="agent-tag">
            <div class="agent-avatar"><!-- 24px --></div>
            <span>Pace · Product</span>
          </div>
          <h3 class="ox-title">Approve pricing tier structure</h3>
          <p class="ox-text">Context about the decision...</p>
        </div>
        <div class="decision-header-meta">
          <div class="ox-badge">High</div>
          <a class="decision-open-link">View details →</a>
        </div>
      </div>
      <div class="actions-grid">
        <button class="ox-btn ox-btn-primary is-card-tone decision-action-btn">
          <div class="decision-action-copy">
            <div class="decision-action-icon"><!-- check icon --></div>
            <div class="decision-action-text">
              <span class="decision-action-title">Approve</span>
              <span class="decision-action-detail">Unblock and continue</span>
            </div>
          </div>
        </button>
        <button class="ox-btn ox-btn-ghost decision-action-btn">
          <div class="decision-action-copy">
            <div class="decision-action-icon"><!-- x icon --></div>
            <div class="decision-action-text">
              <span class="decision-action-title">Reject</span>
              <span class="decision-action-detail">Return with guidance</span>
            </div>
          </div>
        </button>
      </div>
    </div>
  </div>
</div>
```

**Key rules:**
- `--ox-card-color-rgb` set per urgency — colors gradient line, badges, links
- Agent avatar: **24px** (not 56px), rounded 6px
- Action buttons: `min-height: 88px`, grid layout (icon + title + detail)
- `actions-grid`: `grid-template-columns: repeat(2, 1fr)`, gap 12px
- Approve button: `ox-btn-primary is-card-tone` — filled with accent color
- Reject button: `ox-btn-ghost` — transparent with border
- On reject click: expand `reject-composer` with textarea + submit

### Reject Composer
```html
<div class="reject-composer">
  <div class="reject-heading">
    <h4>Rejection guidance</h4>
    <span class="reject-meta">Required</span>
  </div>
  <textarea class="reject-textarea" placeholder="What should the agent do differently?"></textarea>
  <div class="reject-toolbar">
    <div class="reject-toolbar-copy">Be specific — <strong>clear guidance</strong> helps the next attempt.</div>
    <button class="ox-btn ox-btn-primary reject-submit">Send rejection</button>
  </div>
</div>
```
Animates in via `rejectComposerIn` (220ms, translateY + scale + opacity).

## Pattern: List Row (initiative-pulse)

General-purpose list item with leading icon, copy, and trailing element.

```html
<a class="pulse-list-row" href="#">
  <div class="pulse-list-leading"><!-- 28px icon/avatar --></div>
  <div class="pulse-list-copy">
    <div class="pulse-list-title">Workstream name</div>
    <div class="pulse-list-meta">
      3 tasks <span class="pulse-meta-separator">·</span> 1 blocked
    </div>
  </div>
  <div class="pulse-list-trailing">
    <div class="pulse-mini-ring"><!-- 34px ring --></div>
  </div>
</a>
```

- Rows separated by `border-bottom: 1px solid var(--ox-border)` (last child: none)
- Hover: title color transitions to `--ox-primary`
- Leading: 28px icon container or avatar
- Trailing: mini-ring, status pill, or chevron

## Pattern: Scaffold Stage (process widget)

3D perspective container showing the initiative tree.

```html
<div class="scaffold-state">
  <div class="scaffold-state__chrome">
    <span class="scaffold-state__eyebrow">Scaffold Composer</span>
    <span class="scaffold-state__status">
      <span class="scaffold-state__status-dot"></span>
      Assembling hierarchy
    </span>
  </div>
  <div class="scaffold-stage">
    <!-- ambient orbs -->
    <div class="scaffold-stage__ambient scaffold-stage__ambient--one"></div>
    <div class="scaffold-stage__ambient scaffold-stage__ambient--two"></div>
    <div class="scaffold-stage__core">
      <!-- tree: initiative → trunk → columns → branches → nodes -->
    </div>
  </div>
</div>
```

**Key rules:**
- Container: `--scaffold-tilt-x` and `--scaffold-tilt-y` set via mousemove for 3D perspective
- Stage: grid background via `::before`, cursor spotlight via `::after`
- Ambient orbs: blurred circles with `ambientFloat` animation (7–9s)
- Nodes: `scaffold-node` with entity-type colors (initiative=primary, workstream=teal, milestone=warning, task=default)
- Tree connections: `scaffold-stage__trunk` (vertical line) + `scaffold-stage__columns::before` (horizontal line)
- Node drift: `nodeDrift` animation — subtle vertical float (6s)

## Pattern: Empty State

When there's no data to show.

```html
<div class="empty-state animate-in">
  <div class="empty-icon"><!-- 24px SVG --></div>
  <div class="empty-title">Agent on standby</div>
  <div class="empty-desc">No agent telemetry is available yet.</div>
</div>
```

- Centered, `padding: 64px 24px`
- Dashed border: `border: 1px dashed var(--ox-border-strong)`
- Icon: 48px circle with `--ox-primary` glow
- Title: 1.1rem, weight 600. Desc: 0.9rem, muted, max-width 280px.

## Pattern: Skeleton Loading

Shimmer placeholders shown before data arrives.

```html
<div class="skeleton-wrapper">
  <div style="display:flex; align-items:center; gap:16px;">
    <div class="skeleton-line" style="width:48px; height:48px; border-radius:50%;"></div>
    <div style="flex:1;">
      <div class="skeleton-line" style="width:40%; height:18px; margin-bottom:8px;"></div>
      <div class="skeleton-line" style="width:60%; height:14px;"></div>
    </div>
  </div>
</div>
```

- `skeleton-line`: gradient shimmer animation (2s infinite linear)
- `skeleton-wrapper`: `transition: opacity 0.3s ease` — fades out when data arrives
- Match the shape of the real content (avatar circle + text lines for agent cards, rectangles for decision cards)

## Pattern: Pagination (decisions)

```html
<div class="pagination">
  <div class="page-info">
    <div class="page-kicker">
      <span class="page-label">Queue Position</span>
      <span class="page-count">3 pending</span>
    </div>
    <div class="page-progress">
      <div class="page-progress-bar" style="width: 33%"></div>
    </div>
  </div>
  <div class="page-controls">
    <button class="page-btn page-btn--prev">Prev</button>
    <button class="page-btn page-btn--next">Next</button>
  </div>
</div>
```

- Grid: `grid-template-columns: minmax(0, 1fr) auto`
- Progress bar: 4px, gradient fill with glow
- Nav arrows added via `::before` / `::after` content
- Decision cards slide in/out via `decisionSlideForward` / `decisionSlideBackward` animations

## Pattern: Footer

```html
<div class="widget-footer">
  <span class="sync-label">Synced</span>
  <a class="deep-link" href="#" onclick="return openWidgetLink(url, event)">
    Open live view
    <svg><!-- arrow icon --></svg>
  </a>
</div>
```

- `deep-link`: 48px min-height, 14px radius, primary-tinted border + background
- Hover: translateY(-1px), stronger border
- **Must use `openWidgetLink()`** for MCP protocol compatibility — not raw `<a href>` navigation
- `callTool()` for inline actions (approve, reject) — see widget-sdk reference

## Composition: Multi-Agent Grid

```html
<div class="agent-board">
  <div class="agent-item" style="--agent-accent-rgb: 22, 163, 74;">
    <!-- full agent card -->
  </div>
</div>
```

- `grid-template-columns: repeat(auto-fit, minmax(280px, 1fr))`
- Each card sets `--agent-accent-rgb` for per-agent coloring
- Running/blocked agents: full detail. Idle: collapsed.
- Sort: blocked first, running second, idle last.

## Button System (ox-btn)

```css
.ox-btn { /* base: 44px min-height, 12px radius, border, transitions */ }
.ox-btn-primary { /* filled with primary color */ }
.ox-btn-primary.is-card-tone { /* filled with --ox-card-color (urgency-specific) */ }
.ox-btn-ghost { /* transparent + subtle border, for secondary actions */ }
.ox-btn:disabled { /* 0.56 opacity, no transform, no shadow */ }
```

Hover: `translateY(-1px)` + stronger border. Active: no transform. Disabled: no interaction.
