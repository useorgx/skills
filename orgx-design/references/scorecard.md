# OrgX Design Scorecard & Critique Protocol

Read this before shipping any OrgX surface. This is the quality gate.

## Weighted Scorecard (100 points)

Score every surface against this rubric. **Under 85 = do not ship. Revise.**

| Dimension | Weight | What it measures |
|-----------|--------|-----------------|
| **Signal clarity** | 25 | Can the dominant question be answered in under 2 seconds? Is noise eliminated? Does every element carry information? |
| **Hierarchy / glanceability** | 20 | Does the layout survive a squint test? Is there one clear focal point? Does urgency reshape the layout? |
| **Actionability** | 15 | Can the user act without navigating away? Are actions prominent and verb-loaded? Is the path from diagnosis to action immediate? |
| **OrgX brand distinctiveness** | 15 | Could this only be OrgX? Is the gradient line present? Does compression/expansion breathe? Is the materiality matte-instrument, not glossy-SaaS? |
| **Composure in quiet state** | 10 | Does the surface become near-invisible when healthy? Is silence the happy path? No congratulatory noise? |
| **Motion / interaction elegance** | 5 | Is motion purposeful (orientation or ambient presence only)? Is the easing correct? No bounce, no overshoot? |
| **Accessibility / legibility** | 5 | Are contrast ratios sufficient? Is type legible at all sizes? Do interactive elements have adequate touch targets (44px min)? |
| **Implementation discipline** | 5 | Uses ox- token system? No magic numbers? Proper dark/light mode? Uses SDK patterns (callTool, openWidgetLink)? |

### Hard Rules

- **Under 85/100 total** → don't ship, revise
- **Under 90/100 on hierarchy** → redesign the layout from scratch
- **Under 80/100 on distinctiveness** → too generic, add OrgX signature moves
- **Under 80/100 on signal clarity** → the surface doesn't answer its question, rethink what it shows

### How to Score

For each dimension, score 0–100 as a percentage of the weight. Then sum.

Example: Signal clarity at 90% of 25 = 22.5. Hierarchy at 85% of 20 = 17. And so on.

A surface that scores 92 on signal clarity, 88 on hierarchy, 90 on actionability, 75 on distinctiveness, 95 on composure, 85 on motion, 90 on accessibility, 95 on implementation = 23 + 17.6 + 13.5 + 11.25 + 9.5 + 4.25 + 4.5 + 4.75 = **88.35**. Ships, but the distinctiveness score (75) is under 80, so it needs a revision pass to add OrgX-specific identity.

## Screenshot Critique Protocol

After building, evaluate the result as if looking at a static screenshot. Run these tests:

### 2-Second Test
Look at the surface for 2 seconds, then look away. What did you understand?
- **Pass:** The dominant question was answered. You know the state.
- **Fail:** You got a general impression of "data" but couldn't name what matters.

### Blur Test
Mentally blur the surface to low fidelity. Does hierarchy survive?
- **Pass:** You can still identify the primary read, the secondary elements, and the quiet zones.
- **Fail:** Everything becomes an undifferentiated gray mass.

### Squint Test
Is there one clear dominant read?
- **Pass:** One element (health ring, blocker banner, decision title) clearly dominates.
- **Fail:** Multiple elements compete for attention at equal volume.

### Silent-State Test
Set all values to healthy / complete / idle. Does the UI become nearly invisible?
- **Pass:** The surface compresses to identity + status + timestamp. Minimal visual weight.
- **Fail:** The surface still shows charts, progress bars, section headers, and badges even when there's nothing to report.

### Stress-State Test
Set values to maximum urgency (blocker, critical decision, stalled agents). Does the blocker truly dominate?
- **Pass:** The attention banner reshapes the entire card. Actions are immediately visible. Context is compressed but present.
- **Fail:** The blocker is just another section among equals.

### Crop Test
Crop to just the main card. Does it still feel premium?
- **Pass:** The card stands alone as a polished component. Edge lighting, spacing, typography all hold up.
- **Fail:** Without the page background and grid, it looks like a generic div.

### Generic SaaS Test — THE CRITICAL ONE
Look at the surface and ask: what parts could belong to any B2B dashboard?
- **Pass:** The gradient line, the compression/expansion behavior, the metric rail pattern, the urgency-driven hierarchy — these are distinctly OrgX.
- **Fail:** Swap the accent color and logo, and this could be a Stripe dashboard, a Linear board, a Datadog panel.

For every element that fails the generic SaaS test, ask: **what is the OrgX-only move here?** Then apply it.

## Distinctiveness Tests

Before shipping, answer these four questions. If any answer is vague, the design needs more identity.

1. **What would make this look like Linear?** (editorial minimalism, monochrome, lots of whitespace, thin type)
   → If you see these, you've drifted toward Linear's lane. Add OrgX density, metric rail, instrument-panel materiality.

2. **What would make this look like a Stripe dashboard clone?** (clean cards, blue accent, tabs, charts)
   → If you see these, you're in generic premium SaaS territory. Add urgency-driven hierarchy, compression/expansion, surveillance calm.

3. **What is the one OrgX-only move here?** Name a specific design element that only exists in OrgX's visual language.
   → Must be concrete: "the gradient line edge-light," "the metric rail with tone-colored active states," "the attention banner that reshapes the entire card," etc.

4. **Where is the signature compression/expansion behavior?** Point to what collapses in healthy state and what dominates in urgent state.
   → If there's no compression/expansion, the surface isn't breathing with operational state. Fix this.

## Premium Finish Tests

The difference between "good" and "award-winning" lives in the details. Check these before shipping:

### Rhythm Consistency
- Is the spacing cadence consistent? (4px grid, no off-grid gaps)
- Do section gaps follow a clear progression? (8 → 12 → 16 → 20 → 24)
- Is vertical rhythm maintained across the card?

### Edge Alignment
- Do left edges of text, icons, and containers align to a shared margin?
- Are right-aligned elements consistently positioned?
- Do section dividers span the correct width?

### Spacing Cadence
- Is padding consistent within similar elements?
- Do symmetric elements have symmetric spacing?
- Is the card's internal padding (20px horizontal) respected by all children?

### Icon Discipline
- Are all icons the same optical weight?
- Are icon sizes consistent within a context? (18px in rails, 20px in shells, 24px in banners)
- Do icons have consistent stroke width?

### Visual Noise Budget
- Count the number of distinct visual elements (borders, shadows, colors, type styles) in view.
- Is it under the budget? (State widgets: ≤12 distinct elements. Action widgets: ≤10. Process widgets: ≤15 including ambient.)
- Can any be consolidated?

### Motion Restraint
- Is every animation serving orientation or ambient presence?
- Are durations from the token system? (160ms micro, 220ms medium, 600ms entrance)
- Is the easing `cubic-bezier(0.16, 1, 0.3, 1)` consistently applied?

### No Accidental Style Collisions
- Does every element use ox- tokens, not hardcoded values?
- Do dark mode and light mode both work without special-casing?
- Are hover/active/disabled states defined for all interactive elements?
