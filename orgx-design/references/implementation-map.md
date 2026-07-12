# OrgX Implementation Map

This map prevents parallel design systems. Read the actual source before use;
component APIs can change.

## Full-page app primitives

| Need | Canonical primitive | Contract |
| --- | --- | --- |
| Page frame | `components/layout/AppPageShell.tsx` | Shared max widths, responsive page padding, atmosphere, and optional viewport-owned workbench mode. |
| Page identity / H1 | `components/command-primitives/PageHero.tsx` | One visible page heading with restrained context and actions. |
| Context / identity | `components/command-primitives/IdentityRow.tsx` | Workspace or entity identity, truthful connection state, and quiet metadata. |
| Earned attention | `components/command-primitives/FocusBanner.tsx` | Calm collapses; warning/danger may claim first-paint. Never nest it in another card. |
| Navigable metrics | `components/command-primitives/MetricRail.tsx` | Metrics select meaningful detail; they are not decorative KPI tiles. |
| Action hierarchy | `components/command-primitives/ActionBar.tsx` | One primary, few secondary, rare actions behind one disclosure. |
| Repeated rows | `components/ui/list-row.tsx` | One row grammar for state, metadata, and inline consequence. |

Compatibility wrappers such as `components/ox/OxMetricRail.tsx` and
`components/ox/OxListRow.tsx` may exist. Reuse them only when their contract
matches the canonical primitive; do not fork styling to make a near-duplicate.

## Data and action ownership

- A page may compose multiple reads, but one hook/service boundary owns each
  entity's canonical state.
- A user job has one mutation path. Do not wire the same action through a row,
  banner, and floating button with different loading/error behavior.
- Prefer server-derived initial state plus focused client refresh over duplicate
  mount fetches.
- Do not mutate on mount. Draft creation, autosave, and launch require visible
  user intent unless the product explicitly promises otherwise.
- Consequential selection should survive reload/back/share through route or
  query state when practical.

## Styling

- Use the live design-token module and CSS variables already in the app. Read
  `lib/design-tokens.ts` and the active global theme before adding values.
- Default surfaces are matte and low-chroma. A single accent expresses product
  state; it does not decorate container edges.
- Use spacing and type to create hierarchy before borders and backgrounds.
- Extend a token only when at least two surfaces share the semantic need.
- Avoid arbitrary values when a current token or primitive expresses the same
  relationship.

## Responsive implementation

- Design from 375px, then validate 768px and 1440px.
- Prefer reflow to shrinking. Stack actions, convert secondary regions to
  disclosure, and let rows wrap deliberately.
- Use `min-width: 0` for flex/grid children with variable content.
- Never hide the only label or primary action at a breakpoint.
- Keep touch targets at least 44 by 44 CSS pixels.
- Test 200% zoom, long names, long localized labels, and browser UI/keyboard
  intrusion where applicable.

## Accessibility and interaction

- One H1; named landmarks; logical heading order.
- Native elements first. Tabs, disclosure, menus, dialogs, and listboxes must
  expose their semantics and keyboard model.
- Focus is visible against the real background, not only in isolation.
- Escape closes the top transient layer and returns focus to its trigger.
- Back returns to the prior meaningful state.
- Status is not conveyed by color alone.
- Respect reduced motion; essential state changes remain understandable with
  animation disabled.

## MCP widgets

Full-page React primitives are not automatically widget primitives. For MCP
widgets, follow `widget-sdk.md`: protocol detection, `callTool()` for inline
actions, `openWidgetLink()` for navigation, size/theme synchronization, and
normalization of tool data. Do not use raw `<a href>` as the primary widget
navigation contract.
