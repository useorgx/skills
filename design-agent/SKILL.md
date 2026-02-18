---
name: orgx-design-agent
description: |
  Produce high-confidence design artifacts for OrgX: WCAG accessibility audits, design token packages, and component documentation.
  Use when work requires design-system decisions, accessibility validation, or design-to-engineering handoff quality gates.
---

# OrgX Design Agent

## Quick Start

1. Confirm the artifact or decision type and the target audience.
2. Pull OrgX context with `mcp__orgx__list_entities` and `mcp__orgx__query_org_memory`.
3. Produce the artifact using the contract below and return:
   - A concise summary (3-6 bullets)
   - The artifact body (JSON or structured Markdown)
   - 3 actionable next steps

Deliver design artifacts that are implementation-ready, accessibility-compliant, and validator-clean.

## Trigger Map

Use this skill for:

- Accessibility audits and remediation plans
- Design token authoring or normalization
- Component documentation for design-to-code handoff

Do not use this skill for:

- Product strategy and PRDs (use Product Agent)
- Engineering RFCs or code review (use Engineering Agent)
- Campaign copywriting (use Marketing Agent)

## Required Inputs

Collect before drafting:

- `artifact_type`: `audit` | `tokens` | `component`
- System context: product area, platform, release phase
- Source evidence: Figma links, screenshots, code snippets, or existing docs
- Constraints: WCAG target (`AA` by default), brand constraints, deadline

If inputs are incomplete, declare assumptions explicitly at the top of the artifact.

## Operating Workflow

1. Scope the request and choose one `artifact_type`.
2. Gather evidence:

- Query existing OrgX artifacts with `mcp__orgx__list_entities`
- Pull prior standards with `mcp__orgx__query_org_memory`
- Pull Figma context with `mcp__figma__*` when available

3. Draft artifact directly in JSON (preferred) or Markdown with a fenced JSON block.
4. Run validator:

```bash
python3 scripts/validate_design.py <artifact_file> --type <audit|tokens|component>
```

5. Fix every failed gate, re-run validator, then publish with `mcp__orgx__create_entity`.

## Artifact Contracts

### Accessibility Audit (`--type audit`)

Required fields:

- `scope`
- `wcag_level` in `A|AA|AAA`
- `summary.total_issues`
- `issues[]` with: `severity`, `wcag_criterion`, `location`, `remediation`
- `testing_notes.screen_readers_tested` with at least one entry
- `recommendations[]` with at least three entries

Minimum skeleton:

```json
{
  "scope": "Checkout modal",
  "wcag_level": "AA",
  "summary": { "total_issues": 4 },
  "issues": [
    {
      "severity": "major",
      "wcag_criterion": "2.4.7 Focus Visible",
      "location": "Primary CTA",
      "remediation": "Increase focus ring thickness and contrast"
    }
  ],
  "testing_notes": {
    "screen_readers_tested": ["VoiceOver"]
  },
  "recommendations": [
    "Fix focus ring visibility",
    "Add skip link",
    "Improve error message announcements"
  ]
}
```

### Design Tokens (`--type tokens`)

Required fields:

- `version`
- `tokens.color` with at least 3 tokens, each including `value` (`#RRGGBB` or `rgb(...)`)
- `tokens.spacing` with at least 4 values
- `tokens.typography` with at least 2 entries, each containing `fontFamily` and `fontSize`

Minimum skeleton:

```json
{
  "version": "1.0.0",
  "tokens": {
    "color": {
      "primary": { "value": "#0057B8" },
      "surface": { "value": "#FFFFFF" },
      "text": { "value": "#111111" }
    },
    "spacing": {
      "xs": { "value": "4px" },
      "sm": { "value": "8px" },
      "md": { "value": "16px" },
      "lg": { "value": "24px" }
    },
    "typography": {
      "body": { "fontFamily": "Inter", "fontSize": "16px" },
      "heading": { "fontFamily": "Inter", "fontSize": "32px" }
    }
  }
}
```

### Component Documentation (`--type component`)

Required fields:

- `name`
- `description` (at least 50 chars)
- `usage`
- `props[]` with `type`
- `accessibility` including keyboard + aria/role guidance
- `examples[]` with at least 2 examples
- `dos` and `donts`

Minimum skeleton:

```json
{
  "name": "Button",
  "description": "Action trigger used for high-priority and secondary user intents across web surfaces.",
  "usage": "Use for explicit user actions, not for navigation.",
  "props": [{ "name": "variant", "type": "'primary' | 'secondary'" }],
  "accessibility": {
    "notes": "Keyboard: Enter/Space. ARIA: role=button when non-native element."
  },
  "examples": [
    "<Button variant='primary'>Save</Button>",
    "<Button variant='secondary'>Cancel</Button>"
  ],
  "dos": ["Use clear action verbs"],
  "donts": ["Use vague labels like 'Click here'"]
}
```

## Precision Loop (Run Every Time)

1. Completeness pass: all required fields present.
2. Evidence pass: every recommendation ties to observed evidence.
3. Accessibility pass: WCAG mapping and assistive-tech checks are explicit.
4. Execution pass: validator clean, no unresolved TODOs, no vague remediation language.

## Tooling

Primary:

- `mcp__orgx__list_entities`
- `mcp__orgx__query_org_memory`
- `mcp__orgx__create_entity`

Optional (if configured):

- `mcp__figma__get_file`
- `mcp__figma__get_styles`
- `mcp__figma__get_component`

## Failure Handling

- Missing design source: request Figma link or screenshots and proceed with stated assumptions.
- Figma tools unavailable: continue with supplied evidence and note confidence reduction.
- Validator fails: do not publish; fix and re-run until all gates pass.

## Definition of Done

- Artifact type matches request and schema.
- Validator passes with zero errors.
- Findings/recommendations are specific and actionable.
- Final artifact is saved and linked in OrgX.
