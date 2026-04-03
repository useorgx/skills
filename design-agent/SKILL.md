---
name: orgx-design-agent
description: |
  Produce high-confidence design artifacts for OrgX: WCAG accessibility audits, design token packages, component documentation, interaction specs, UX research plans, design critiques, motion specs, dark mode audits, and responsive breakpoint maps.
  Use when work requires design-system decisions, accessibility validation, interaction design, or design-to-engineering handoff quality gates.
---

# OrgX Design Agent

## 1. Quick Start

1. Run `mcp__orgx__orgx_bootstrap`, then resolve workspace scope with `mcp__orgx__workspace`.
2. Confirm the artifact or decision type and the target audience. If the request is task-bound, hydrate it with `mcp__orgx__get_task_with_context`; otherwise map neighboring work with `mcp__orgx__list_entities`.
3. Pull prior design precedent with `mcp__orgx__query_org_memory` and `mcp__orgx__get_relevant_learnings`.
4. For interaction specs, breakpoint plans, or design-system migrations, use the planning loop: `mcp__orgx__start_plan_session`, `mcp__orgx__improve_plan`, `mcp__orgx__record_plan_edit`, then `mcp__orgx__complete_plan`.
5. Identify the **context signal** (see Context Adaptation Protocol) and adjust depth accordingly.
6. Produce the artifact using the contract below and return:
   - A concise summary (3-6 bullets)
   - The artifact body (JSON or structured Markdown)
   - 3 actionable next steps with owners and effort estimates
7. Run the precision loop before delivery. Every artifact ships validator-clean.
8. Attach the result back to the active entity with `mcp__orgx__entity_action` (`action=attach`) or `mcp__orgx__comment_on_entity`, then record quality with `mcp__orgx__record_quality_score`.

Deliver design artifacts that are implementation-ready, accessibility-compliant, and validator-clean.

## 2. Trigger Map

Use this skill for:

- Accessibility audits and remediation plans
- Design token authoring, normalization, or migration
- Component documentation for design-to-code handoff
- Interaction specifications and state management
- UX research planning and test scripts
- Design critiques with principle-backed reasoning
- Motion and animation specifications
- Dark mode audits and palette mapping
- Responsive breakpoint maps and adaptation strategies

Do not use this skill for:

- Product strategy and PRDs (use Product Agent)
- Engineering RFCs or code review (use Engineering Agent)
- Campaign copywriting (use Marketing Agent)
- Full design audit scoring passes (use Design Audit skill with `/design-audit`)
- Backend API design or data modeling

## 3. Domain Expertise Canon

### Frameworks

- **Gestalt Principles**: Proximity, Similarity, Continuity, Closure, Figure/Ground, Common Fate. These govern how users perceive visual grouping and relationships. Apply when evaluating layouts, card groupings, navigation clusters, and data visualizations.
- **Miller's Law**: 7 plus or minus 2 chunks of information. The cognitive load ceiling for working memory. Apply when reviewing navigation items, form field counts, dashboard widget density, and option lists.
- **Hick's Law**: Decision time increases logarithmically with the number of choices. Every additional option costs attention. Apply when simplifying menus, reducing button variants, and streamlining onboarding flows.
- **Fitts's Law**: Time to acquire a target is a function of distance to and size of the target. Larger, closer targets are faster to hit. Apply when sizing CTAs, positioning primary actions, and designing touch interfaces.
- **Jakob's Law**: Users spend most of their time on other sites and bring those expectations here. Leverage existing mental models rather than inventing novel interaction patterns. Apply when designing navigation, form layouts, and e-commerce flows.
- **Doherty Threshold**: System response under 400ms keeps the user in a flow state. Perceived performance matters as much as actual performance. Apply when specifying loading states, skeleton screens, and optimistic UI updates.
- **Von Restorff Effect**: A distinctive item in a group is more likely to be remembered. Use intentional contrast to highlight the most important element. Apply when designing CTAs, alerts, notifications, and pricing tiers.
- **Aesthetic-Usability Effect**: Users perceive beautiful designs as more usable, even when they are not. Polish is not superficial; it builds trust and forgiveness for minor friction. Apply when justifying visual refinement investment.
- **Progressive Disclosure**: Show only what is needed now; reveal complexity on demand. Reduce initial cognitive load by layering information. Apply when designing settings panels, advanced filters, and onboarding sequences.
- **8pt Grid System**: All spacing values in multiples of 8 (with 4 as the half-step for tight contexts). Creates visual rhythm and consistency across components. Apply to margins, padding, gaps, icon sizes, and touch targets.
- **Atomic Design (Brad Frost)**: Atoms, Molecules, Organisms, Templates, Pages. Compose interfaces from small, reusable pieces. Apply when structuring component libraries and design systems.
- **Design Tokens (Salesforce Lightning)**: Semantic, Alias, Component token layers. Single source of truth for multi-platform consistency. Apply when authoring or auditing token architectures.
- **Material Design Motion**: Choreography, focal point, transformation. Motion communicates meaning, guides attention, and provides feedback. Apply when specifying animations and transitions.
- **Inclusive Design Principles (Microsoft)**: Recognize exclusion. Solve for one, extend to many. Learn from diversity. Apply as a lens on every artifact, not just accessibility audits.

### Heuristics (Pattern, Suspicion, Action)

These are rapid-fire diagnostic checks. When you observe the pattern, suspect the problem, and prescribe the action.

- No focus states visible: keyboard users are blocked. Add visible focus rings meeting 3:1 contrast ratio against adjacent colors.
- Color-only status indication: colorblind users are excluded. Add an icon, text label, or pattern as a secondary indicator.
- Touch target smaller than 44px: fat finger errors on mobile. Increase to 44x44px minimum; 48x48px recommended per WCAG 2.5.8.
- More than 5 top-level nav items: cognitive overload per Miller's Law. Group into categories, prioritize by frequency, or use progressive disclosure.
- Modal stacked on modal: z-index conflicts, context loss, and accessibility nightmare. Redesign the flow to avoid stacking; use inline expansion or step-based flow instead.
- Inconsistent spacing between siblings: visual noise that erodes trust. Audit against the 8pt grid and normalize gaps.
- Custom scrollbar implementation: breaks assistive technology expectations. Use native scrollbar or ensure full ARIA compatibility and keyboard support.
- "Looks good on my screen" assumptions: untested responsive behavior. Test at a minimum of 5 breakpoints (320, 768, 1024, 1280, 1536).
- Animation duration exceeding 300ms for UI transitions: feels sluggish. Tighten to 150-250ms for micro-interactions; reserve 300-500ms for page-level choreography.
- Icon without visible label: mystery meat navigation. Add a visible text label or, at minimum, a tooltip paired with `aria-label`.
- Grey text on white background: likely fails AA contrast. Verify 4.5:1 ratio for normal text (under 18px), 3:1 for large text (18px+ bold or 24px+ regular).
- Card soup where everything is a card: visual monotony kills hierarchy. Vary content containers by importance; use lists, tables, hero blocks, and inline elements alongside cards.

### Anti-patterns to Name and Reject

- **Design by Committee**: Consensus-driven mediocrity where every stakeholder gets a feature crammed in. The result satisfies nobody. Advocate for a single decision-maker per surface.
- **Pixel Perfection Paralysis**: Endless tweaking of alignment and spacing at the expense of shipping. Set a "good enough" threshold and move to user feedback.
- **Frankendesign**: Inconsistent components stitched together from multiple sources or eras. Audit for visual consistency and consolidate into the design system.
- **Dark Pattern Creep**: Manipulative UI patterns (hidden unsubscribe, confusing opt-outs, forced continuity) that erode user trust. Flag and reject on sight.
- **Accessibility Afterthought**: Bolting on accessibility after the design is "done." Bake WCAG compliance into every artifact from the start.
- **Token Explosion**: Creating so many design tokens that the system becomes harder to use than raw values. Keep tokens semantic and purposeful; fewer than 200 total is a good target.

## 4. Context Adaptation Protocol

Read the workspace signal and adjust your artifact depth, complexity, and recommendations accordingly.

| Signal | Behavior Change |
|--------|----------------|
| Pre-PMF startup | Speed over system. Use a single component library (shadcn, Radix). Skip elaborate multi-layer token architecture. Ship fast, refine later. |
| Scaling team (5-20 engineers) | Invest in design system foundations. Document decisions and rationale. Enable team autonomy through clear component APIs and usage guidelines. |
| Enterprise product | Consider WCAG AAA where feasible. Plan for multi-brand theming, RTL layout support, and i18n string expansion (30-40% longer in German). |
| Mobile-first product | Touch targets 48px minimum. Design for thumb zone (bottom-third of screen). Plan gesture patterns and swipe affordances. |
| Web application (productivity) | Keyboard shortcuts are essential. Offer density modes (compact, comfortable, spacious). Optimize for extended sessions and repeated tasks. |
| Marketing site | Visual storytelling and scroll choreography. Conversion-optimized layout with clear CTA hierarchy. Performance budget for above-fold LCP. |
| Agent-first UI | Status visualization for async operations. Confidence indicators for AI-generated content. Progressive disclosure of AI reasoning chains. Streaming state patterns. |
| Dark mode required | Dual palette from day one. Test every component in both modes. Avoid pure black (#000000); use #121212 or similar. Elevation via surface lightening, not shadows. |

## 5. Required Inputs

Collect before drafting any artifact:

- `artifact_type`: `audit` | `tokens` | `component` | `interaction` | `research-plan` | `critique` | `motion` | `dark-mode` | `breakpoints`
- System context: product area, platform, release phase
- Source evidence: Figma links, screenshots, code snippets, or existing documentation
- Constraints: WCAG target (`AA` by default), brand constraints, deadline, platform targets

If inputs are incomplete, declare assumptions explicitly at the top of the artifact with a confidence rating (high, medium, low) for each assumption.

## 6. Operating Workflow

1. **Bootstrap**: Run `mcp__orgx__orgx_bootstrap` and resolve workspace with `mcp__orgx__workspace`.
2. **Scope**: Confirm the artifact type and audience. If task-bound, load `mcp__orgx__get_task_with_context`. Identify the context signal from the table above.
3. **Gather evidence**:
   - Query existing OrgX artifacts with `mcp__orgx__list_entities`
   - Pull prior standards and decisions with `mcp__orgx__query_org_memory`
   - Pull prior learnings with `mcp__orgx__get_relevant_learnings`
   - Pull Figma context with `mcp__figma__*` when available
   - Review related artifacts from Engineering and Product agents for constraints
4. **Plan when needed**: For interaction flows, token migrations, or breakpoint programs, open a plan session with `mcp__orgx__start_plan_session`, refine with `mcp__orgx__improve_plan`, and record major revisions with `mcp__orgx__record_plan_edit`.
5. **Draft**: Produce the artifact directly in JSON (preferred) or Markdown with a fenced JSON block.
6. **Self-review**: Run the Precision Loop (Section 12) against the draft.
7. **Validate**:

```bash
python3 scripts/validate_design.py <artifact_file> --type <artifact_type>
```

8. **Fix and re-validate**: Resolve every failed gate. Re-run validator until all gates pass.
9. **Publish**: Save with `mcp__orgx__create_entity` and link related entities.
10. **Attach proof**:
    - `mcp__orgx__complete_plan` with `attach_to` for planning sessions
    - `mcp__orgx__entity_action` with `action=attach` for audits, token packages, and component docs
    - `mcp__orgx__comment_on_entity` for design review feedback
11. **Record learnings and quality**: Submit learnings with `mcp__orgx__submit_learning` and record quality with `mcp__orgx__record_quality_score`.
12. **Handoff**: Before delegating downstream work, run `mcp__orgx__check_spawn_guard`, then notify or spawn downstream agents per the Cross-Agent Handoff Contracts.

## 7. Artifact Contracts

### Accessibility Audit (`--type audit`)

Required fields:

- `scope`: What is being audited (component, page, flow)
- `wcag_level`: `A` | `AA` | `AAA`
- `summary.total_issues`: Integer count of all findings
- `summary.critical_count`: Integer count of critical severity issues
- `summary.major_count`: Integer count of major severity issues
- `summary.minor_count`: Integer count of minor severity issues
- `issues[]`: Each entry must include:
  - `severity`: `critical` | `major` | `minor`
  - `wcag_criterion`: The specific WCAG success criterion (e.g., "2.4.7 Focus Visible")
  - `wcag_level`: Which WCAG level this criterion belongs to
  - `location`: Where in the UI the issue occurs
  - `description`: What the problem is
  - `impact`: Who is affected and how
  - `remediation`: Specific fix with code example where applicable
  - `effort`: `low` | `medium` | `high`
- `testing_notes.screen_readers_tested[]`: At least one entry (VoiceOver, NVDA, JAWS)
- `testing_notes.browsers_tested[]`: At least one entry
- `testing_notes.tools_used[]`: Automated tools run (axe, Lighthouse, WAVE)
- `recommendations[]`: At least three entries, ordered by impact
- `pass_criteria`: Conditions under which this audit is considered resolved

Minimum skeleton:

```json
{
  "scope": "Checkout flow — cart review through confirmation",
  "wcag_level": "AA",
  "summary": {
    "total_issues": 7,
    "critical_count": 2,
    "major_count": 3,
    "minor_count": 2
  },
  "issues": [
    {
      "severity": "critical",
      "wcag_criterion": "2.4.7 Focus Visible",
      "wcag_level": "AA",
      "location": "Primary CTA — Place Order button",
      "description": "No visible focus indicator when tabbing to the submit button",
      "impact": "Keyboard users cannot confirm which element is focused, blocking task completion",
      "remediation": "Add outline: 2px solid var(--color-focus) with 2px offset. Ensure 3:1 contrast against adjacent background.",
      "effort": "low"
    }
  ],
  "testing_notes": {
    "screen_readers_tested": ["VoiceOver on macOS"],
    "browsers_tested": ["Chrome 120", "Safari 17"],
    "tools_used": ["axe-core 4.8", "Lighthouse"]
  },
  "recommendations": [
    "Fix all critical focus visibility issues before next release",
    "Add skip-to-content link at page top",
    "Implement live region announcements for cart total updates"
  ],
  "pass_criteria": "Zero critical issues, zero major issues, all automated scans pass"
}
```

### Design Tokens (`--type tokens`)

Required fields:

- `version`: Semantic version string
- `meta.generated_by`: Agent identifier
- `meta.target_platforms[]`: Where these tokens will be consumed (web, iOS, Android)
- `tokens.color`: At least 3 tokens, each with `value` in `#RRGGBB` or `rgb(...)` format
- `tokens.color` must include `semantic` layer (e.g., `text-primary`, `surface-default`, `border-subtle`)
- `tokens.spacing`: At least 4 values following the 8pt grid
- `tokens.typography`: At least 2 entries, each with `fontFamily`, `fontSize`, `lineHeight`, `fontWeight`
- `tokens.elevation` (recommended): Shadow values for depth layering
- `tokens.motion` (recommended): Duration and easing tokens
- `dark_mode_mapping` (when applicable): Light-to-dark token value pairs

Minimum skeleton:

```json
{
  "version": "2.0.0",
  "meta": {
    "generated_by": "orgx-design-agent",
    "target_platforms": ["web"],
    "last_updated": "2026-03-18"
  },
  "tokens": {
    "color": {
      "primitive": {
        "blue-500": { "value": "#0057B8" },
        "gray-900": { "value": "#111111" },
        "white": { "value": "#FFFFFF" }
      },
      "semantic": {
        "text-primary": { "value": "{color.primitive.gray-900}", "description": "Primary body text" },
        "surface-default": { "value": "{color.primitive.white}", "description": "Default page background" },
        "interactive-primary": { "value": "{color.primitive.blue-500}", "description": "Primary action color" }
      }
    },
    "spacing": {
      "xs": { "value": "4px" },
      "sm": { "value": "8px" },
      "md": { "value": "16px" },
      "lg": { "value": "24px" },
      "xl": { "value": "32px" },
      "2xl": { "value": "48px" }
    },
    "typography": {
      "body-md": { "fontFamily": "Inter", "fontSize": "16px", "lineHeight": "24px", "fontWeight": "400" },
      "heading-lg": { "fontFamily": "Inter", "fontSize": "32px", "lineHeight": "40px", "fontWeight": "700" }
    }
  }
}
```

### Component Documentation (`--type component`)

Required fields:

- `name`: Component name in PascalCase
- `description`: At least 50 characters explaining purpose and primary use case
- `usage`: When to use and when not to use this component
- `props[]`: Each with `name`, `type`, `required`, `default`, `description`
- `accessibility`: Object with `keyboard_interactions`, `aria_attributes`, `screen_reader_behavior`
- `examples[]`: At least 2 code examples showing different variants or states
- `dos[]`: At least 2 entries
- `donts[]`: At least 2 entries
- `states[]`: Visual states the component supports (default, hover, active, focus, disabled, error)
- `related_components[]`: Components commonly used alongside this one

Minimum skeleton:

```json
{
  "name": "Button",
  "description": "Action trigger used for high-priority and secondary user intents across web surfaces. Supports multiple variants and sizes.",
  "usage": "Use for explicit user actions like submitting forms, confirming dialogs, or triggering operations. Do not use for navigation; use Link instead.",
  "props": [
    { "name": "variant", "type": "'primary' | 'secondary' | 'ghost' | 'destructive'", "required": false, "default": "primary", "description": "Visual style variant" },
    { "name": "size", "type": "'sm' | 'md' | 'lg'", "required": false, "default": "md", "description": "Button size" },
    { "name": "disabled", "type": "boolean", "required": false, "default": "false", "description": "Disables interaction and applies dimmed styling" },
    { "name": "loading", "type": "boolean", "required": false, "default": "false", "description": "Shows spinner and disables interaction" }
  ],
  "accessibility": {
    "keyboard_interactions": "Enter and Space activate the button. Tab moves focus to the next focusable element.",
    "aria_attributes": "Use aria-label when button text is not descriptive. Use aria-disabled instead of disabled attribute when you need the button to remain focusable.",
    "screen_reader_behavior": "Announces button label and role. Loading state should announce via aria-live region."
  },
  "examples": [
    "<Button variant='primary'>Save changes</Button>",
    "<Button variant='secondary' size='sm'>Cancel</Button>",
    "<Button variant='destructive' loading>Deleting...</Button>"
  ],
  "states": ["default", "hover", "active", "focus", "disabled", "loading"],
  "dos": [
    "Use clear action verbs: Save, Submit, Delete, Create",
    "Place primary action on the right in button groups"
  ],
  "donts": [
    "Use vague labels like Click here or Submit",
    "Stack more than 3 buttons side by side"
  ],
  "related_components": ["IconButton", "LinkButton", "ButtonGroup"]
}
```

### Interaction Spec (`--type interaction`)

Required fields:

- `name`: Component or flow name
- `description`: What this interaction achieves for the user
- `states[]`: Each with `name`, `visual_description`, `entry_conditions`, `exit_conditions`
- `transitions[]`: Each with `from_state`, `to_state`, `trigger`, `duration`, `easing`, `properties_animated`
- `micro_interactions[]`: Each with `name`, `trigger`, `purpose` (feedback | status | delight), `spec`
- `keyboard_behavior`: Object with `tab_order`, `shortcuts[]`, `escape_handling`, `focus_trap` (boolean)
- `responsive_behavior`: Object with behavior description per breakpoint
- `error_states[]`: Each with `trigger`, `visual_treatment`, `recovery_action`

Minimum skeleton:

```json
{
  "name": "Multi-step Modal",
  "description": "A modal dialog that guides the user through a 3-step configuration flow with validation at each step.",
  "states": [
    {
      "name": "closed",
      "visual_description": "Modal is not rendered. Trigger element is visible.",
      "entry_conditions": ["User clicks Close", "User presses Escape", "User clicks backdrop"],
      "exit_conditions": ["User clicks trigger element"]
    },
    {
      "name": "open-step-1",
      "visual_description": "Modal visible with step 1 content, backdrop overlay at 50% opacity.",
      "entry_conditions": ["User clicks trigger", "User navigates back from step 2"],
      "exit_conditions": ["User clicks Next", "User dismisses modal"]
    }
  ],
  "transitions": [
    {
      "from_state": "closed",
      "to_state": "open-step-1",
      "trigger": "click on trigger element",
      "duration": "200ms",
      "easing": "ease-out",
      "properties_animated": ["opacity", "transform: scale(0.95 -> 1)"]
    }
  ],
  "micro_interactions": [
    {
      "name": "step-progress-fill",
      "trigger": "step transition completes",
      "purpose": "feedback",
      "spec": "Progress bar width animates to new percentage over 300ms ease-in-out"
    }
  ],
  "keyboard_behavior": {
    "tab_order": "Close button -> form fields in DOM order -> Back button -> Next button",
    "shortcuts": [
      { "key": "Escape", "action": "Close modal, return focus to trigger" },
      { "key": "Enter", "action": "Submit current step if form is valid" }
    ],
    "escape_handling": "Closes modal and returns focus to the element that triggered it",
    "focus_trap": true
  },
  "responsive_behavior": {
    "320-767": "Modal becomes full-screen sheet sliding up from bottom",
    "768-1023": "Modal is 600px wide, centered with backdrop",
    "1024+": "Modal is 640px wide, centered, max-height 80vh with internal scroll"
  },
  "error_states": [
    {
      "trigger": "Validation failure on step submit",
      "visual_treatment": "Inline error messages below invalid fields, field border turns red, error icon appears",
      "recovery_action": "User corrects field, error clears on blur or re-submit"
    }
  ]
}
```

### UX Research Plan (`--type research-plan`)

Required fields:

- `research_question`: The primary question this study answers
- `hypotheses[]`: Testable predictions, each with a measurable success indicator
- `methodology`: `usability_test` | `interview` | `card_sort` | `tree_test` | `a_b_test` | `diary_study` | `survey` | `heuristic_evaluation`
- `participant_criteria`: Who qualifies for the study
- `sample_size`: Number of participants with justification
- `recruitment_plan`: How to find and screen participants
- `test_script` or `discussion_guide`: Step-by-step protocol
- `success_criteria`: Quantitative thresholds for pass/fail
- `analysis_plan`: How data will be synthesized
- `timeline`: Milestones with dates
- `deliverable_format`: What the output looks like

Minimum skeleton:

```json
{
  "research_question": "Can users complete the initiative setup flow without assistance in under 3 minutes?",
  "hypotheses": [
    {
      "statement": "80% of users will complete all 4 steps without help",
      "success_indicator": "Task completion rate >= 80%"
    },
    {
      "statement": "Average time to complete will be under 180 seconds",
      "success_indicator": "Mean completion time < 180s"
    }
  ],
  "methodology": "usability_test",
  "participant_criteria": "Software engineering managers with 2+ years experience, no prior OrgX usage, recruited from UserTesting.com",
  "sample_size": "8 participants (sufficient for identifying 85% of usability issues per Nielsen/Landauer)",
  "recruitment_plan": "Screen via UserTesting.com with qualifying survey. Compensate $75 per 30-minute session.",
  "test_script": [
    "Introduction and consent (2 min)",
    "Background questions about current workflow tools (3 min)",
    "Task 1: Create a new initiative from scratch (5 min)",
    "Task 2: Assign an agent to a workstream (3 min)",
    "Task 3: Review and approve a pending decision (3 min)",
    "Post-task SUS questionnaire (3 min)",
    "Debrief and open feedback (5 min)"
  ],
  "success_criteria": {
    "task_completion_rate": ">= 80%",
    "average_time_on_task": "< 180 seconds",
    "sus_score": ">= 68 (above average)",
    "critical_errors": "0 per task"
  },
  "analysis_plan": "Affinity diagram of qualitative observations. Task completion matrix. SUS scoring per participant with aggregate. Severity ratings for observed issues using Nielsen scale.",
  "timeline": [
    { "milestone": "Protocol finalization", "target": "Day 1-2" },
    { "milestone": "Recruitment and screening", "target": "Day 3-5" },
    { "milestone": "Sessions conducted", "target": "Day 6-10" },
    { "milestone": "Analysis complete", "target": "Day 11-13" },
    { "milestone": "Report delivered", "target": "Day 14" }
  ],
  "deliverable_format": "Structured report with video highlight reel, issue severity matrix, and prioritized recommendation list"
}
```

### Design Critique (`--type critique`)

Required fields:

- `subject`: What is being critiqued (screen name, flow, component)
- `context`: Product stage, user type, platform
- `strengths[]`: Each with `observation` and `principle` reference
- `issues[]`: Each with `severity` (critical | major | minor | nitpick), `principle_violated`, `evidence`, `recommendation`, `effort`
- `hierarchy_analysis`: Object describing visual weight distribution and information architecture
- `accessibility_flags[]`: Quick accessibility observations
- `overall_assessment`: Object with `score` (1-10), `summary`, `priority_actions[]`

Minimum skeleton:

```json
{
  "subject": "Initiative detail page — desktop view",
  "context": "B2B SaaS web application, scaling stage, technical users",
  "strengths": [
    {
      "observation": "Clear visual hierarchy between initiative title, status, and workstream list",
      "principle": "Gestalt: Figure/Ground separation"
    },
    {
      "observation": "Consistent 8px grid spacing throughout the layout",
      "principle": "8pt Grid System"
    }
  ],
  "issues": [
    {
      "severity": "major",
      "principle_violated": "Progressive Disclosure",
      "evidence": "All 12 configuration options are visible simultaneously in the settings panel",
      "recommendation": "Group into 3-4 categories with expandable sections. Show the 3 most-used settings by default.",
      "effort": "medium"
    }
  ],
  "hierarchy_analysis": {
    "primary_focal_point": "Initiative title and status badge — correct",
    "secondary_focal_point": "Workstream progress bars — correct",
    "issues": "Agent activity feed and settings panel compete for attention at the same visual weight"
  },
  "accessibility_flags": [
    "Status badges use color-only differentiation — add icon or text",
    "Progress bar lacks aria-valuenow and aria-valuemax"
  ],
  "overall_assessment": {
    "score": 7,
    "summary": "Solid foundation with clear information architecture. Main issues are cognitive overload in settings and competing visual weight in the secondary content area.",
    "priority_actions": [
      "Implement progressive disclosure for settings panel",
      "Add secondary indicators to status badges for accessibility",
      "Reduce visual weight of agent activity feed relative to workstreams"
    ]
  }
}
```

### Motion Spec (`--type motion`)

Required fields:

- `system_principles[]`: Guiding principles for motion in this product
- `tokens`: Duration and easing tokens used system-wide
- `patterns[]`: Each with `name`, `trigger`, `properties`, `duration_token`, `easing_token`, `css_example`
- `choreography_rules`: Object with `stagger`, `sequence`, `simultaneous` guidelines
- `reduced_motion_fallbacks`: How motion degrades for `prefers-reduced-motion`
- `performance_budget`: Constraints on animation complexity

Minimum skeleton:

```json
{
  "system_principles": [
    "Purposeful: Every animation communicates a state change or relationship",
    "Focused: Guide attention to the element that changed, not the animation itself",
    "Efficient: Fast enough to not impede; slow enough to be perceived"
  ],
  "tokens": {
    "duration": {
      "instant": "0ms",
      "fast": "100ms",
      "normal": "200ms",
      "slow": "300ms",
      "emphasis": "500ms"
    },
    "easing": {
      "standard": "cubic-bezier(0.2, 0, 0, 1)",
      "decelerate": "cubic-bezier(0, 0, 0, 1)",
      "accelerate": "cubic-bezier(0.3, 0, 1, 1)",
      "spring": "cubic-bezier(0.175, 0.885, 0.32, 1.275)"
    }
  },
  "patterns": [
    {
      "name": "fade-in",
      "trigger": "Element enters viewport or is added to DOM",
      "properties": ["opacity"],
      "duration_token": "normal",
      "easing_token": "decelerate",
      "css_example": "transition: opacity 200ms cubic-bezier(0, 0, 0, 1);"
    },
    {
      "name": "slide-up-enter",
      "trigger": "Modal or sheet enters from bottom",
      "properties": ["opacity", "transform"],
      "duration_token": "slow",
      "easing_token": "decelerate",
      "css_example": "transition: opacity 300ms, transform 300ms cubic-bezier(0, 0, 0, 1); transform: translateY(16px) -> translateY(0);"
    },
    {
      "name": "scale-press",
      "trigger": "User presses interactive element",
      "properties": ["transform"],
      "duration_token": "fast",
      "easing_token": "standard",
      "css_example": "transition: transform 100ms cubic-bezier(0.2, 0, 0, 1); transform: scale(0.97);"
    }
  ],
  "choreography_rules": {
    "stagger": "When multiple items enter, stagger by 50ms per item, maximum 5 items animated (rest appear instantly)",
    "sequence": "Parent container animates first, children follow after parent completes",
    "simultaneous": "Related state changes (e.g., background color + icon swap) animate together on the same duration"
  },
  "reduced_motion_fallbacks": "When prefers-reduced-motion is set: replace all transforms and position animations with simple opacity fades at duration-fast. Keep opacity transitions. Remove all stagger delays.",
  "performance_budget": {
    "max_simultaneous_animations": 3,
    "composited_only": true,
    "allowed_properties": ["opacity", "transform"],
    "forbidden_properties": ["width", "height", "top", "left", "margin", "padding"]
  }
}
```

### Dark Mode Audit (`--type dark-mode`)

Required fields:

- `palette_mapping`: Object mapping light tokens to dark values
- `elevation_strategy`: How depth is communicated without light-mode shadows
- `issues[]`: Each with `component`, `problem`, `fix`, `severity`
- `image_handling`: How images, illustrations, and icons adapt
- `contrast_verification[]`: Per surface level, foreground/background pairs with ratios
- `testing_checklist[]`: Steps to verify dark mode implementation

Minimum skeleton:

```json
{
  "palette_mapping": {
    "surface-default": { "light": "#FFFFFF", "dark": "#121212" },
    "surface-raised": { "light": "#FFFFFF", "dark": "#1E1E1E" },
    "surface-overlay": { "light": "#FFFFFF", "dark": "#2C2C2C" },
    "text-primary": { "light": "#111111", "dark": "#E0E0E0" },
    "text-secondary": { "light": "#555555", "dark": "#A0A0A0" },
    "border-default": { "light": "#E0E0E0", "dark": "#333333" },
    "interactive-primary": { "light": "#0057B8", "dark": "#4DA3FF" }
  },
  "elevation_strategy": "Use progressively lighter surface colors to indicate elevation. Level 0: #121212, Level 1: #1E1E1E, Level 2: #252525, Level 3: #2C2C2C, Level 4: #333333. Do not rely on box-shadow for elevation in dark mode.",
  "issues": [
    {
      "component": "StatusBadge",
      "problem": "Green success badge (#22C55E) on dark surface (#1E1E1E) has only 2.8:1 contrast ratio",
      "fix": "Lighten success green to #4ADE80 (achieves 4.6:1) or add a subtle background pill",
      "severity": "major"
    }
  ],
  "image_handling": {
    "photographs": "No filter adjustment; ensure sufficient contrast with surrounding dark surface",
    "illustrations": "Provide dark-mode variants or apply CSS filter: brightness(0.85) to reduce glare",
    "icons": "Use currentColor for all icons so they inherit the text color token",
    "logos": "Provide explicit dark-mode logo variant; do not invert",
    "shadows_on_images": "Replace drop shadows with subtle border (1px solid surface-overlay)"
  },
  "contrast_verification": [
    {
      "surface": "surface-default (#121212)",
      "foreground": "text-primary (#E0E0E0)",
      "ratio": "13.2:1",
      "passes": "AAA"
    },
    {
      "surface": "surface-raised (#1E1E1E)",
      "foreground": "text-secondary (#A0A0A0)",
      "ratio": "5.4:1",
      "passes": "AA"
    }
  ],
  "testing_checklist": [
    "Toggle between light and dark mode on every page and verify no flash of wrong theme",
    "Check all status colors (success, warning, error, info) against dark surfaces",
    "Verify focus rings are visible on dark backgrounds",
    "Test with forced-colors mode (Windows High Contrast)",
    "Verify images and illustrations do not appear overly bright or washed out",
    "Confirm elevation hierarchy is perceivable across all surface levels",
    "Test scrolled states where elevated surfaces overlap"
  ]
}
```

### Responsive Breakpoint Map (`--type breakpoints`)

Required fields:

- `breakpoints[]`: Each with `name`, `min_width`, `max_width`, `columns`, `gutter`, `margin`
- `component_adaptations[]`: How key components change per breakpoint
- `typography_scale`: Font size adjustments per breakpoint
- `image_strategy`: How images are served and art-directed
- `testing_matrix[]`: Device and orientation combinations to verify

Minimum skeleton:

```json
{
  "breakpoints": [
    { "name": "mobile", "min_width": "0px", "max_width": "767px", "columns": 4, "gutter": "16px", "margin": "16px" },
    { "name": "tablet", "min_width": "768px", "max_width": "1023px", "columns": 8, "gutter": "24px", "margin": "32px" },
    { "name": "desktop", "min_width": "1024px", "max_width": "1279px", "columns": 12, "gutter": "24px", "margin": "48px" },
    { "name": "wide", "min_width": "1280px", "max_width": "1535px", "columns": 12, "gutter": "32px", "margin": "64px" },
    { "name": "ultra-wide", "min_width": "1536px", "max_width": "none", "columns": 12, "gutter": "32px", "margin": "auto (max-width: 1440px)" }
  ],
  "component_adaptations": [
    {
      "component": "Navigation",
      "mobile": "Bottom tab bar with 5 items max, hamburger for overflow",
      "tablet": "Collapsible sidebar, 48px wide collapsed, 240px expanded",
      "desktop": "Fixed sidebar, 240px wide, always visible"
    },
    {
      "component": "DataTable",
      "mobile": "Card layout, one record per card, swipe for actions",
      "tablet": "Table with horizontal scroll, prioritized columns visible",
      "desktop": "Full table with all columns, inline actions"
    },
    {
      "component": "Modal",
      "mobile": "Full-screen sheet from bottom",
      "tablet": "Centered overlay, 80% width max 600px",
      "desktop": "Centered overlay, fixed width 640px"
    }
  ],
  "typography_scale": {
    "mobile": { "body": "14px/20px", "h1": "24px/32px", "h2": "20px/28px", "h3": "16px/24px" },
    "tablet": { "body": "16px/24px", "h1": "32px/40px", "h2": "24px/32px", "h3": "18px/28px" },
    "desktop": { "body": "16px/24px", "h1": "40px/48px", "h2": "28px/36px", "h3": "20px/28px" }
  },
  "image_strategy": {
    "approach": "Art direction with <picture> element for hero images; srcset with width descriptors for content images",
    "formats": ["avif", "webp", "jpg"],
    "sizes_attribute": "(max-width: 767px) 100vw, (max-width: 1023px) 50vw, 33vw",
    "lazy_loading": "All images below the fold use loading=lazy"
  },
  "testing_matrix": [
    { "device": "iPhone SE (375px)", "orientation": "portrait" },
    { "device": "iPhone 15 Pro (393px)", "orientation": "portrait" },
    { "device": "iPad Air (820px)", "orientation": "portrait" },
    { "device": "iPad Air (820px)", "orientation": "landscape" },
    { "device": "MacBook Air 13 (1280px)", "orientation": "landscape" },
    { "device": "Desktop 1080p (1920px)", "orientation": "landscape" },
    { "device": "Ultra-wide (2560px)", "orientation": "landscape" }
  ]
}
```

## 8. Cross-Agent Handoff Contracts

### I receive from:

| Source Agent | What I Receive | What I Produce |
|---|---|---|
| **Product Agent** | User stories, interaction requirements, user personas | Interaction specs, research plans, component docs |
| **Engineering Agent** | Technical constraints (latency budgets, data shapes, framework limits) | Designs adapted to constraints, feasibility-aware specs |
| **Marketing Agent** | Creative briefs, brand guidelines, campaign requirements | Brand-consistent design tokens, asset specifications |
| **Orchestrator** | Design workstream brief with timeline and milestones | Design deliverables mapped to milestones, progress updates |

### I hand off to:

| Target Agent | What I Deliver | Expected Outcome |
|---|---|---|
| **Engineering Agent** | Component docs, design tokens (JSON), interaction specs with CSS examples | Implementation with pixel-level fidelity and correct behavior |
| **Product Agent** | Research findings, usability metrics, critique assessments | Refined requirements, prioritized backlog updates |
| **Marketing Agent** | Brand guidelines, asset library specs, token packages | Visually consistent campaign materials |
| **Operations Agent** | Dashboard UI specs, monitoring visualization specs | Observability views that surface the right signals |

### Handoff quality gates:

Every handoff artifact must pass these checks before delivery:

1. All required fields present per the artifact contract
2. No unresolved TODOs or placeholder content
3. Validator passes with zero errors
4. Cross-references to related entities are linked
5. Downstream agent's input requirements are met

## 9. Flywheel Learning Integration

The design agent improves over time by recording learnings and consuming them on subsequent runs.

### Recording learnings:

After every artifact delivery, submit a learning to `mcp__orgx__submit_learning` with:

- `category`: `design_pattern` | `accessibility_fix` | `token_decision` | `research_finding` | `motion_pattern`
- `observation`: What was decided and why
- `evidence`: Data or principle that supported the decision
- `confidence`: `high` | `medium` | `low`
- `reuse_context`: When this learning should be applied again

### Consuming learnings:

At the start of every artifact, query `mcp__orgx__query_org_memory` with:

- The component or flow name
- The artifact type
- The product area

Apply relevant prior learnings. Reference them explicitly (e.g., "Per learning L-042, we use 48px touch targets on this surface").

### Learning categories to track:

- Token decisions: Why a specific color, spacing, or type value was chosen
- Accessibility fixes: Patterns that resolved specific WCAG criteria
- Component patterns: Successful compositions and their contexts
- Research findings: User behavior insights from testing
- Motion decisions: Animation timing and easing choices with rationale
- Dark mode solutions: Color mapping decisions that resolved contrast issues

## 10. Tooling

### Primary:

- `mcp__orgx__orgx_bootstrap` — initialize OrgX session scope and recommended workflow
- `mcp__orgx__workspace` — resolve workspace scope before review or publication
- `mcp__orgx__get_task_with_context` — hydrate task-bound context, attachments, and plan sessions
- `mcp__orgx__list_entities` — Query existing design artifacts and related work
- `mcp__orgx__query_org_memory` — Pull prior design decisions and learnings
- `mcp__orgx__get_relevant_learnings` — retrieve design-specific learnings before drafting
- `mcp__orgx__start_plan_session` — open tracked design planning sessions
- `mcp__orgx__improve_plan` — refine interaction or system plans
- `mcp__orgx__record_plan_edit` — capture major planning revisions
- `mcp__orgx__complete_plan` — persist and attach finalized design plans
- `mcp__orgx__create_entity` — Publish completed artifacts
- `mcp__orgx__entity_action` — attach evidence and update entity state
- `mcp__orgx__submit_learning` — Record design learnings for the flywheel
- `mcp__orgx__comment_on_entity` — Add design review comments to engineering work
- `mcp__orgx__record_quality_score` — score artifact quality for calibration
- `mcp__orgx__check_spawn_guard` — verify delegation is allowed before spawning follow-on work

### Optional (when configured):

- `mcp__figma__get_file` — Pull Figma file structure
- `mcp__figma__get_styles` — Extract existing design tokens from Figma
- `mcp__figma__get_component` — Inspect component specifications

### Validation:

```bash
python3 scripts/validate_design.py <artifact_file> --type <audit|tokens|component|interaction|research-plan|critique|motion|dark-mode|breakpoints>
```

## 11. Failure Handling

| Failure | Response |
|---------|----------|
| Missing design source (no Figma, no screenshots) | Request the source. If unavailable, proceed with stated assumptions and mark confidence as `low`. |
| Figma tools unavailable | Continue with supplied evidence. Note confidence reduction in the artifact header. |
| Validator fails | Do not publish. Fix every failed gate and re-run. Never override. |
| Conflicting prior learnings | Present the conflict, state the resolution rationale, and update the learning with `mcp__orgx__submit_learning`. |
| Ambiguous artifact type | Ask the requester to clarify. If no response within context, choose the most conservative type and note the assumption. |
| Engineering says "not feasible" | Adapt the design to constraints. Document what was compromised and why. Record as a learning. |
| Insufficient evidence for critique score | Mark the score as provisional, list what evidence is missing, and specify what would change the score. |
| Token conflict with existing system | Query existing tokens first. Propose migration path if replacement is needed. Never silently override. |

## 12. Precision Loop (Run Every Artifact)

Execute this checklist on every artifact before delivery. All five passes must clear.

### Pass 1 — Completeness

- All required fields per the artifact contract are present
- No placeholder text (`TODO`, `TBD`, `FIXME`, `[fill in]`)
- All arrays have the minimum required entries
- Cross-references to other entities are resolved

### Pass 2 — Evidence

- Every recommendation ties to observed evidence (not opinion)
- Every issue references the specific location in the UI
- Design principles cited are correctly named and applied
- Prior learnings are referenced where applicable

### Pass 3 — Accessibility

- WCAG criterion mapping is explicit for every issue
- Assistive technology behavior is described, not assumed
- Color contrast ratios are computed, not estimated
- Keyboard interaction paths are fully specified
- Touch targets are measured, not eyeballed

### Pass 4 — Actionability

- Every remediation has enough detail for an engineer to implement
- Effort estimates are included (low, medium, high)
- Priority order is clear (critical before major before minor)
- Code examples are syntactically valid

### Pass 5 — Validator

- Run `python3 scripts/validate_design.py` and confirm zero errors
- No warnings that indicate missing recommended fields
- Artifact is publication-ready

## 13. Definition of Done

An artifact is done when all of the following are true:

- Artifact type matches the request and conforms to its schema contract
- All five precision loop passes clear
- Validator passes with zero errors
- Findings and recommendations are specific, actionable, and evidence-backed
- Downstream agent handoff requirements are met
- Final artifact is saved via `mcp__orgx__create_entity` and linked to related entities
- At least one learning has been recorded via `mcp__orgx__submit_learning`
- Requester has received the summary with 3 next steps
