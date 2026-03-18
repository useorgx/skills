# PRD Template Reference

## Full Template Structure

```json
{
  "feature_name": "string - Clear, descriptive name",
  "version": "string - Document version (e.g., '1.0.0')",
  "author": "string - Author name",
  "last_updated": "string - ISO date",
  "confidence_level": "string - high|medium|low — based on evidence strength",

  "problem_statement": "string - What problem does this solve? (2-3 sentences, minimum 100 chars)",

  "target_users": [
    {
      "persona": "string - User type (specific, not 'users')",
      "segment_size": "string - Estimated number of users in this segment",
      "needs": ["string - Key need"],
      "pain_points": ["string - Current frustration with quantification"],
      "jtbd": "string - When [situation], I want to [motivation], so I can [outcome]"
    }
  ],

  "user_stories": [
    {
      "id": "string - US-001",
      "as_a": "string - Specific user persona",
      "i_want": "string - Desired action/capability",
      "so_that": "string - Expected benefit (measurable when possible)",
      "priority": "string - P0|P1|P2",
      "acceptance_criteria": ["string - Reference to AC-XXX"]
    }
  ],

  "acceptance_criteria": [
    {
      "id": "string - AC-001",
      "user_story": "string - Reference to US-XXX",
      "given": "string - Initial context/state",
      "when": "string - Action taken",
      "then": "string - Expected outcome (specific, testable by machine)"
    }
  ],

  "success_metrics": [
    {
      "metric": "string - Metric name",
      "current_baseline": "string - Current value (or 'TBD — baseline measurement plan below')",
      "target": "string - Target value with number",
      "measurement_method": "string - How to measure (tool + query/filter)",
      "timeline": "string - When to measure",
      "health_check_metric": "string - Paired metric that prevents gaming (e.g., retention pairs with DAU)"
    }
  ],

  "technical_requirements": {
    "dependencies": ["string - System/service dependencies"],
    "api_changes": ["string - API modifications needed"],
    "data_model_changes": ["string - Schema changes"],
    "security_considerations": ["string - Security requirements"],
    "performance_requirements": ["string - Latency, throughput, etc."]
  },

  "out_of_scope": ["string - Explicitly excluded items (must be genuinely tempting, not strawmen)"],

  "risks": [
    {
      "risk": "string - Risk description",
      "category": "string - technical|user-behavior|market|operational",
      "probability": "string - High|Medium|Low",
      "impact": "string - High|Medium|Low",
      "mitigation": "string - Mitigation strategy"
    }
  ],

  "timeline": {
    "design_complete": "string - ISO date",
    "development_start": "string - ISO date",
    "beta_release": "string - ISO date",
    "ga_release": "string - ISO date"
  },

  "open_questions": ["string - Unresolved questions that could change the PRD"],

  "decision_log": [
    {
      "date": "string - ISO date",
      "decision": "string - What was decided",
      "rationale": "string - Why",
      "alternatives_considered": ["string - What else was considered"]
    }
  ]
}
```

## Product Thinking Checklist

Apply this checklist before finalizing any PRD. Every item must pass or have a documented exception.

### Problem Framing

- [ ] **Problem statement describes the user's world, not the product's world.** Bad: "Our system lacks MFA." Good: "Enterprise customers cannot meet SOC2 requirements because..."
- [ ] **Target users are specific segments, not "users."** Every persona has a segment size, specific needs, and quantified pain points.
- [ ] **JTBD is articulated.** At least one user segment has a Jobs-to-Be-Done statement: "When [situation], I want to [motivation], so I can [outcome]."
- [ ] **The problem is validated.** Evidence exists: user interviews, support tickets, usage data, or churn analysis. If not, the evidence gap is flagged and a research plan is attached.

### Solution Quality

- [ ] **User stories map to real segments.** No "as a user" — every story specifies the persona.
- [ ] **Acceptance criteria are machine-testable.** A QA engineer or automated test can verify each criterion without interpretation.
- [ ] **Out-of-scope items are genuinely tempting.** If nobody would ever suggest the out-of-scope items, they are not useful boundaries.
- [ ] **The solution addresses the JTBD.** Trace each user story back to the job it helps the user accomplish.

### Measurement

- [ ] **Every success metric has a baseline.** Or a documented plan to establish one within 2 weeks.
- [ ] **Every success metric has a health-check pair.** DAU pairs with retention. Revenue pairs with LTV/CAC. Signups pair with activation.
- [ ] **Targets are ambitious but achievable.** Check: would the team be proud of hitting the target? Would they be surprised? If yes to both, the target is probably right.
- [ ] **Measurement method is specific.** Not "analytics" but "Amplitude: Event X filtered by property Y, cohorted by Z."

### Risk and Scope

- [ ] **Risks include user-behavior risks, not just technical risks.** "Users may not adopt this because..." is as important as "The database may not scale because..."
- [ ] **The PRD could be understood by someone outside the team.** No unexplained jargon. No assumed context.
- [ ] **Scope is sized for one bet.** If the PRD tests more than one hypothesis, split it.

### Framework Application

- [ ] **Appropriate prioritization framework applied.** RICE for 5+ items, ICE for quick ranking, Kano for feature categorization, WSJF for dependency-heavy environments.
- [ ] **Value Proposition Canvas alignment.** Every pain reliever maps to a documented pain. Every gain creator maps to a documented gain.
- [ ] **MVP type is explicit.** If this is an MVP, which type? Concierge, Wizard of Oz, Single-feature, or MLP?

## Writing Effective Problem Statements

### Bad Examples (Avoid)

- "Users need a better experience" (vague)
- "We should add feature X" (solution, not problem)
- "Competitors have this" (not user-focused)
- "Our system doesn't support Y" (product-centric, not user-centric)

### Good Examples (Use)

- "Users currently spend 15 minutes manually entering data that could be automated, leading to errors in 23% of submissions and frustration that causes 12% churn in the first month."
- "Enterprise customers cannot comply with SOC2 requirements because our audit logs don't include user action timestamps, blocking $2.3M in pipeline."
- "New users abandon onboarding at step 3 (integration setup) at a 67% rate because the current flow requires manual API key configuration that takes 20+ minutes."

### Problem Statement Formula

```
[User segment] currently [painful action/situation] because [root cause],
resulting in [quantified negative outcome].
```

## Writing Effective User Stories

### Format

```
As a [specific persona],
I want [concrete action],
So that [measurable benefit].
```

### Bad Examples (Avoid)

- "As a user, I want things to work better" (vague persona, vague action)
- "As an admin, I want a dashboard" (no benefit stated)
- "As a customer, I want to be able to use the product" (meaningless)

### Good Examples (Use)

- "As a sales manager with 10+ direct reports, I want to see a weekly summary of my team's pipeline changes, so that I can identify coaching opportunities without reviewing each rep's activities individually."
- "As a first-time user completing onboarding, I want to import my existing data from a CSV file, so that I can start using the product with my real data within 5 minutes of signup."

## Writing Testable Acceptance Criteria

### Format (Gherkin)

```
Given [initial state/context],
When [action is performed],
Then [expected outcome with verification].
```

### Bad Examples (Avoid)

- "Then it should work correctly" (not testable)
- "Then the user is happy" (subjective)
- "Then the page loads fast" (not specific)

### Good Examples (Use)

- "Given a user with admin role, When they click 'Export All', Then a CSV file downloads within 5 seconds containing all records with headers matching the table columns."
- "Given an invalid email format is entered, When the user submits the form, Then an inline error message 'Please enter a valid email' appears within 200ms and the submit button remains disabled."

## Writing Measurable Success Metrics

### Metric Formula

```
[Increase/Decrease] [specific metric] by [percentage/number]
from [baseline] to [target] within [timeframe],
measured by [method/tool].
```

### Health-Check Pairing

Every primary metric needs a health-check metric to prevent gaming:

| Primary Metric | Health-Check Metric | Why |
|---------------|-------------------|-----|
| DAU | D7/D30 retention | Prevents acquisition masking churn |
| Revenue | LTV/CAC ratio | Prevents unprofitable growth |
| Signups | Activation rate | Prevents vanity growth |
| NPS | Response rate | Prevents selection bias |
| Feature usage | Task completion rate | Prevents false engagement |
| Time on page | Goal completion rate | Prevents confusion being mistaken for engagement |

### Bad Examples (Avoid)

- "Improve user satisfaction" (not measurable)
- "Reduce errors" (no baseline or target)
- "Increase engagement" (no definition of engagement)

### Good Examples (Use)

- "Increase 7-day retention from 34% to 45% within 90 days of launch, measured by Amplitude cohort analysis. Health check: D1 retention stays above 60%."
- "Reduce average support tickets per user from 2.3/month to 1.5/month within 60 days, measured by Zendesk reporting filtered to feature-related tags. Health check: CSAT stays above 4.2."
