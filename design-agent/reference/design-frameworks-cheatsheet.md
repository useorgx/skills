# Design Frameworks Cheatsheet

Quick reference for the design principles, laws, and frameworks used by the OrgX Design Agent. Each entry includes the principle, when to apply it, and a concrete example.

## Perceptual and Cognitive Laws

### Gestalt Principles

The human visual system organizes elements into groups and patterns. Use these principles to structure layouts so users perceive the intended relationships without conscious effort.

**Proximity**: Elements near each other are perceived as related. Place form labels close to their fields. Separate unrelated groups with whitespace.
- Apply when: Grouping related controls, organizing card layouts, structuring settings panels.
- Example: A 16px gap between a label and its input, versus 32px between field groups, creates clear visual association.

**Similarity**: Elements that look alike are perceived as related. Use consistent styling for items of the same type.
- Apply when: Designing lists, tag systems, navigation items, status indicators.
- Example: All workstream cards share the same border radius, padding, and shadow. Agent status cards use a distinct style.

**Continuity**: The eye follows smooth paths. Align elements along clear axes.
- Apply when: Laying out dashboards, designing progress flows, arranging timeline views.
- Example: A step indicator with connected dots along a horizontal line reads as a sequence, even without numbering.

**Closure**: The mind completes incomplete shapes. You can suggest structure without drawing every line.
- Apply when: Designing icons, creating card grids with implied boundaries, progress indicators.
- Example: A circular progress ring at 75% completion is perceived as "almost done" because the mind closes the circle.

**Figure/Ground**: Users distinguish foreground elements from background. Use contrast and elevation to establish layers.
- Apply when: Designing modals over content, floating action buttons, overlay panels.
- Example: A modal with backdrop overlay (background dimmed to 50% opacity) clearly separates the dialog from page content.

**Common Fate**: Elements moving in the same direction are perceived as grouped.
- Apply when: Animating list items, collapsing/expanding sections, stagger animations.
- Example: When filtering a list, remaining items slide up together while removed items fade out, reinforcing the group distinction.

### Miller's Law (7 plus or minus 2)

Working memory holds approximately 7 items. Beyond that, users must chunk or offload information.

- Apply when: Designing navigation menus, form sections, dashboard widget counts, dropdown options.
- Red flag: A settings panel with 15 ungrouped toggles. Solution: group into 3-4 categories of 4-5 items each.
- Example: Top navigation with 5 items (Dashboard, Initiatives, Agents, Settings, Help) versus 9 items (too many to scan quickly).

### Hick's Law

Decision time = a + b * log2(n), where n is the number of choices. More options means slower decisions.

- Apply when: Designing action menus, onboarding choices, pricing tiers, filter panels.
- Red flag: A context menu with 12 items. Solution: group into submenus or prioritize the top 5 actions.
- Example: Presenting 3 pricing tiers converts better than 5 tiers because the decision is simpler.

### Fitts's Law

Time = a + b * log2(1 + D/W), where D is distance and W is target width. Larger, closer targets are faster.

- Apply when: Sizing buttons, positioning CTAs, designing touch interfaces, placing destructive actions.
- Red flag: A 24px delete button in the top corner of a full-screen modal. Solution: make it 44px minimum and position it where the user's cursor already is.
- Example: Place the primary action button at the bottom-right of a form (where the user's attention naturally ends after filling fields), sized at 48px height minimum.

### Jakob's Law

Users prefer interfaces that work like the ones they already know.

- Apply when: Choosing interaction patterns, designing navigation, building e-commerce flows.
- Red flag: A custom date picker that uses non-standard gestures. Solution: use the platform-native date picker or a well-established library.
- Example: Place the shopping cart icon in the top-right corner because that is where every other e-commerce site puts it.

### Doherty Threshold (400ms)

If the system responds in under 400ms, users stay in flow. Above 400ms, they disengage.

- Apply when: Specifying loading states, designing skeleton screens, choosing optimistic updates.
- Red flag: A "Loading..." text that appears for 2 seconds before content renders. Solution: show a skeleton screen immediately that matches the content layout.
- Example: When a user clicks "Save", immediately show a success state (optimistic update) and reconcile with the server response. If the save fails, show the error and revert.

### Von Restorff Effect (Isolation Effect)

A distinctive item among similar items stands out and is remembered.

- Apply when: Highlighting CTAs, designing notification badges, emphasizing the recommended pricing tier.
- Red flag: All buttons on a page are the same style. Solution: make the primary action visually distinct (color, size, or weight).
- Example: On a pricing page, the recommended plan has a highlighted border, a "Most Popular" badge, and slightly larger card size.

### Aesthetic-Usability Effect

Users perceive aesthetically pleasing designs as more usable and are more tolerant of minor usability issues.

- Apply when: Justifying investment in visual polish, choosing between quick-and-functional versus refined-and-beautiful.
- Key insight: This does not mean pretty overrides usable. It means that when two designs are equally functional, the more polished one will be perceived as easier to use.
- Example: Two forms with identical functionality. One has consistent spacing, aligned labels, and subtle shadows. The other has misaligned fields and inconsistent colors. Users rate the polished form as "easier" even though the task completion time is the same.

## Design System Frameworks

### 8pt Grid System

All spatial values (margins, padding, gaps, sizes) use multiples of 8px. Use 4px as a half-step for tight situations only.

Scale: 4, 8, 12, 16, 20, 24, 32, 40, 48, 56, 64, 80, 96, 120, 160

- Apply when: Setting any spacing value, sizing components, defining layout grids.
- Red flag: A component with 13px padding. Solution: round to 12px or 16px.
- Example: Card padding is 16px (2 units). Gap between cards is 24px (3 units). Section margin is 48px (6 units).

### Atomic Design (Brad Frost)

Build interfaces from small to large, ensuring reusability at every level.

| Level | Definition | Examples |
|-------|-----------|----------|
| Atoms | Smallest indivisible elements | Button, Input, Label, Icon, Badge |
| Molecules | Groups of atoms functioning together | Search bar (input + button), Form field (label + input + error) |
| Organisms | Complex components with distinct sections | Navigation header, Card with title + body + actions, Data table |
| Templates | Page-level layouts defining content areas | Dashboard layout, Settings page layout, Two-column detail view |
| Pages | Templates filled with real content | The actual Initiative Detail page with real data |

- Apply when: Structuring a component library, deciding what to build as a shared component versus a one-off.
- Red flag: Every page builds its own card component from scratch. Solution: extract the atom (Card container) and molecule (CardHeader, CardBody, CardFooter) to a shared library.

### Design Token Architecture (Three Layers)

Tokens are the single source of truth for visual values. Three layers keep them maintainable.

| Layer | Purpose | Naming Convention | Example |
|-------|---------|------------------|---------|
| Primitive | Raw values, no semantic meaning | color name + shade | `blue-500: #0057B8` |
| Semantic | Purpose-based aliases to primitives | purpose + modifier | `text-primary: {blue-900}` |
| Component | Component-specific overrides | component + property + state | `button-bg-hover: {blue-600}` |

- Apply when: Creating or auditing a token system. Always start with semantic tokens for a new project. Add primitive and component layers as the system grows.
- Red flag: A codebase using raw hex values in 200+ places. Solution: extract into semantic tokens and replace references.
- Red flag: A token file with 500+ entries. Solution: audit for unused tokens and consolidate overlapping values.

## Motion Design Principles

### Material Design Motion Guidelines

Motion should be purposeful, not decorative. Every animation communicates something.

**Duration guidelines:**
- Micro-interactions (button press, toggle): 100-150ms
- Simple transitions (fade, color change): 150-200ms
- Medium transitions (slide, scale): 200-300ms
- Complex transitions (page change, modal): 300-500ms
- Emphasis animations (celebration, onboarding): 500-800ms

**Easing guidelines:**
- Standard (enter and exit): `cubic-bezier(0.2, 0, 0, 1)` — used for most transitions
- Decelerate (enter only): `cubic-bezier(0, 0, 0, 1)` — elements arriving on screen
- Accelerate (exit only): `cubic-bezier(0.3, 0, 1, 1)` — elements leaving screen
- Spring (playful emphasis): `cubic-bezier(0.175, 0.885, 0.32, 1.275)` — slight overshoot

**Choreography rules:**
- Parent animates before children
- Related elements animate together (same duration)
- Stagger delay between list items: 30-50ms, cap at 5 items (rest appear instantly)
- Elements enter from the direction they will exit

**Reduced motion:**
- Respect `prefers-reduced-motion: reduce`
- Replace transforms with opacity fades
- Remove stagger delays
- Reduce durations to 100ms or instant
- Keep functional animations (loading spinners), remove decorative ones

## Accessibility Quick Checks

### The 5-Second Accessibility Scan

Rapid checks you can do on any screen in under 5 seconds:

1. **Squint test**: Squint at the screen. Can you still tell what the hierarchy is? If not, contrast and sizing need work.
2. **Tab test**: Press Tab 5 times. Can you see where focus is? Can you tell what is focused?
3. **Zoom test**: Set the browser to 200% zoom. Does the layout still work? Is any content hidden or overlapping?
4. **Color removal test**: View the screen in grayscale. Can you still understand all information? Any color-only indicators become invisible.
5. **Heading test**: Open the screen reader heading list (VoiceOver: Ctrl+Cmd+U). Is there a logical hierarchy? Are there gaps?

### POUR Principles (WCAG Foundation)

All WCAG criteria map to one of these four principles:

- **Perceivable**: Can users perceive the content? (text alternatives, captions, contrast, adaptable content)
- **Operable**: Can users operate the interface? (keyboard, timing, seizure safety, navigation)
- **Understandable**: Can users understand the content? (readable, predictable, input assistance)
- **Robust**: Does it work with assistive technology? (parsing, name/role/value, status messages)

## Agent-First UI Patterns

Design patterns specific to interfaces where AI agents are primary actors or where AI-generated content is displayed.

### Confidence Indicators

Show how confident the AI is in its output. Prevents users from treating uncertain output as certain.

- Use a visual scale (low/medium/high) or percentage
- Never hide uncertainty from the user
- Position near the AI-generated content, not in a distant tooltip

### Streaming State Patterns

Display content as it generates, not after it completes.

- Show a typing indicator or cursor for text generation
- Use skeleton screens that progressively fill with real content
- Provide a cancel button that is visible during generation
- Indicate when generation is complete (visual shift or notification)

### Decision Points

When the AI needs human approval before proceeding.

- Make the decision request visually prominent (not buried in a feed)
- Show what happens if the user approves and what happens if they reject
- Provide a "not now" option that defers without blocking
- Group batch decisions when multiple are pending

### Reasoning Transparency

Let users see why the AI made a choice, on demand.

- Default: show the result only
- On demand: expand to show the reasoning chain
- Never force users to read the reasoning before acting
- Use progressive disclosure: result, then summary, then full chain
