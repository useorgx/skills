# OrgX Design Tokens

Single source of truth for every visual value. If it's not here, it shouldn't be in the CSS.

All shared classes use the `ox-` prefix: `ox-card`, `ox-well`, `ox-eyebrow`, `ox-title`, `ox-btn`, `ox-badge`. Widget-specific classes are unprefixed and scoped to that widget's `<style>` block.

## Colors

### Backgrounds
```css
/* Light (default + [data-theme="light"]) */
--ox-bg:           #f8fafc;
--ox-panel:        #ffffff;
--ox-well-bg:      #f1f5f9;
--ox-well-shadow:  inset 0 2px 4px rgba(0,0,0,0.02);

/* Dark (prefers-color-scheme: dark + [data-theme="dark"]) */
--ox-bg:           #02040a;
--ox-panel:        rgba(10, 15, 22, 0.95);
--ox-well-bg:      rgba(0,0,0,0.3);
--ox-well-shadow:  inset 0 2px 10px rgba(0,0,0,0.4);
```

### Borders
```css
/* Light */
--ox-border:        rgba(0, 0, 0, 0.08);
--ox-border-strong: rgba(0, 0, 0, 0.15);

/* Dark */
--ox-border:        rgba(255, 255, 255, 0.08);
--ox-border-strong: rgba(255, 255, 255, 0.15);
```

### Text
```css
/* Light */
--ox-text:       #0f172a;
--ox-text-muted: #64748b;

/* Dark */
--ox-text:       #f8fafc;
--ox-text-muted: rgba(255, 255, 255, 0.5);
```

### Status Colors
Each color has light and dark mode variants:

```css
/* Light mode */
--ox-lime:    #a3e635;
--ox-teal:    #0d9488;
--ox-danger:  #e11d48;
--ox-warning: #d97706;
--ox-iris:    #4f46e5;

/* Dark mode */
--ox-lime:    #D4ED31;
--ox-teal:    #00C9A7;
--ox-danger:  #F43F5E;
--ox-warning: #FBBF24;
--ox-iris:    #6366f1;
```

### The Per-Widget Primary
Every widget sets `--ox-primary-rgb` on `:root` — a single RGB triplet that cascades through the gradient line, badges, glow effects, and button accents:

```css
/* agent-status */    :root { --ox-primary-rgb: 191, 255, 0; }
/* initiative-pulse */ :root { --ox-primary-rgb: 0, 201, 167; }
/* decisions */        :root { --ox-primary-rgb: 251, 191, 36; }
/* scaffolded-init */  :root { --ox-primary-rgb: 99, 102, 241; }
```

Use `rgba(var(--ox-primary-rgb), 0.1)` for backgrounds, `rgba(var(--ox-primary-rgb), 0.2)` for borders, `var(--ox-primary)` for text/icons.

### Per-Decision Urgency Colors
Decision cards set their own `--ox-card-color-rgb` per urgency level:
```css
.urgency-critical { --ox-card-color-rgb: 225, 29, 72; }   /* danger */
.urgency-high     { --ox-card-color-rgb: 217, 119, 6; }   /* warning */
.urgency-medium   { --ox-card-color-rgb: 132, 204, 22; }  /* lime */
.urgency-low      { --ox-card-color-rgb: 100, 116, 139; } /* muted */
```

### Agent Directory
Per-agent accent colors set via `--agent-accent-rgb` on each card:

| Agent | Role | RGB | Hex |
|-------|------|-----|-----|
| Pace | Product | `22, 163, 74` | Green |
| Eli | Engineering | `6, 182, 212` | Cyan |
| Mark | Marketing | `249, 115, 22` | Orange |
| Sage | Sales | `168, 85, 247` | Purple |
| Orion | Operations | `245, 158, 11` | Amber |
| Dana | Design | `236, 72, 153` | Pink |
| Xandy | Orchestrator | `20, 184, 166` | Teal |

Agent avatars are served from `https://mcp.useorgx.com/widgets/shared/{filename}.png` with letter-fallback on error.

### Tone Classes
The `.tone-*` system provides semantic coloring across all components:
```css
.tone-good    { color: var(--ox-primary); }
.tone-warning { color: var(--ox-warning); }
.tone-danger  { color: var(--ox-danger); }
.tone-muted   { color: var(--ox-text-muted); }
```

Each tone also has background/border patterns:
```css
.tone-good    { background: rgba(var(--ox-primary-rgb), 0.08); border-color: rgba(var(--ox-primary-rgb), 0.18); }
.tone-warning { background: rgba(251, 191, 36, 0.08); border-color: rgba(251, 191, 36, 0.18); }
.tone-danger  { background: rgba(244, 63, 94, 0.08); border-color: rgba(244, 63, 94, 0.2); }
.tone-muted   { background: rgba(148, 163, 184, 0.1); border-color: rgba(148, 163, 184, 0.18); }
```

## Typography

### The Three Voices
| Voice | Role | Size | Weight | Color | Tracking | Transform |
|-------|------|------|--------|-------|----------|-----------|
| **Label** | Section names, kickers, timestamps | 0.55–0.65rem | 600–700 | `--ox-text-muted` | 0.08–0.14em | uppercase |
| **Value** | Numbers, names, key data | 0.88–2rem | 600–700 | `--ox-text` | -0.02 to -0.06em | none |
| **Body** | Descriptions, task names, copy | 0.74–0.92rem | 400–600 | `--ox-text` or `--ox-text-muted` | normal | none |

### Font Stacks
```css
--ox-font: -apple-system, BlinkMacSystemFont, 'Inter', system-ui, sans-serif;
--ox-mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, monospace;
```

Labels use `--ox-mono`. Values use `--ox-mono` for numbers, `--ox-font` for names. Body uses `--ox-font`.

### Type Scale (rem)
```
0.50   — Mini ring value
0.55–0.58 — Micro labels (pulse-rail-label, pulse-health__label, signal labels)
0.62–0.66 — Small labels (kicker, page-label, param-chip, mono metadata)
0.68–0.72 — Data (pulse-rail-value small, page-count)
0.74–0.78 — Body small (task names, reject-toolbar-copy)
0.80–0.86 — Body (focus task, descriptions, pulse-message)
0.88–0.95 — Titles (agent-name, resolution-banner-title, pulse-list-title)
1.0–1.15  — Metric values (pulse-rail-value, workload-stat-value)
1.4–1.92  — Hero (pulse-title via clamp(), widget-title-lg)
2.0       — Health number (pulse-health__number)
```

## Spacing (4px grid)
```
4px    — Minimum gap
8px    — Tight inline gaps
10px   — Standard inner padding (badges, pills, signal strip gaps)
12px   — Section gaps, list item padding
14px   — Comfortable padding (section trigger, reject composer)
16px   — Standard horizontal padding, body padding
18px   — Section group spacing
20px   — Primary card horizontal padding
22px   — Scaffold stage padding
24px   — Page-level body padding, major section separators
```

## Radii
```
4px    — Param chips, skeleton lines
6px    — Small badges (agent-avatar)
10px   — Banners, panel-icons, mini-rings, panel headers
12px   — Buttons (ox-btn), workload-stat, section triggers
14px   — Inner panels (reject-composer, blockers, output-panel)
16px   — Cards (ox-card), empty-state
18px   — Pagination container
22px   — Scaffold stage (outer process container)
999px  — Pills, dots, progress bars (circular)
```

## Shadows
```css
/* Card shadow — light */
--ox-shadow: 0 12px 32px -12px rgba(0,0,0,0.1), 0 2px 6px rgba(0,0,0,0.04);

/* Card shadow — dark */
--ox-shadow: 0 16px 40px -10px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.05);

/* Buttons */
box-shadow: 0 14px 30px -24px rgba(0,0,0,0.7), inset 0 1px 0 rgba(255,255,255,0.06);

/* Scaffold stage */
box-shadow: 0 26px 50px -30px rgba(0,0,0,0.65), inset 0 1px 0 rgba(255,255,255,0.04);
```

Wells get `--ox-well-shadow`. The outer card gets `--ox-shadow`. Buttons get their own shadow. Nothing else gets a shadow.

## The Gradient Line
Every `ox-card` has a `::after` pseudo-element gradient line at top:
```css
.ox-card::after {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(var(--ox-primary-rgb), 0.5), transparent);
  opacity: 0.8;
}
```
Decision cards override this with `--ox-card-color-rgb` for urgency-specific coloring. This is a STANDARD PATTERN — present on every card.

## Motion

### Easing
```css
cubic-bezier(0.16, 1, 0.3, 1)  /* All UI transitions */
```

### Durations
```
160ms  — Micro (hover, color, transform, border)
180ms  — Standard (stroke, filter transitions)
220ms  — Medium (card resolve, reject composer entry)
300ms  — Skeleton fade-out
360ms  — Health ring stroke animation
600ms  — Entrance animations (fadeSlideUp)
1.8–2.4s — Ambient pulse/breathe
3.8–9.4s — Scaffold ambient float/sparkle/sweep
```

### Standard Animations
```css
/* Entry — all widgets */
@keyframes fadeSlideUp {
  from { opacity: 0; transform: translateY(16px) scale(0.98); filter: blur(4px); }
  to   { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }
}
.animate-in { opacity: 0; animation: fadeSlideUp 0.6s cubic-bezier(0.16,1,0.3,1) forwards; }

/* Skeleton shimmer */
@keyframes shimmer { 0% { background-position: -200% 0; } 100% { background-position: 200% 0; } }

/* Status dot pulse */
@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.4; } }

/* Decision card resolve-out */
.is-resolving { opacity: 0; transform: translateY(-8px) scale(0.985); filter: blur(6px); }
```

### Grid Background
```css
body::before {
  background: radial-gradient(circle at 50% 0%, rgba(var(--ox-primary-rgb), 0.08), transparent 60%),
              linear-gradient(var(--ox-grid) 1px, transparent 1px),
              linear-gradient(90deg, var(--ox-grid) 1px, transparent 1px);
  background-size: 100% 100%, 20px 20px, 20px 20px;
}
```
Present on all standalone widget pages. The radial gradient uses the per-widget primary.
