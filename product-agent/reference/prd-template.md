# PRD Template Reference

## Full Template Structure

```json
{
  "feature_name": "string - Clear, descriptive name",
  "version": "string - Document version (e.g., '1.0.0')",
  "author": "string - Author name",
  "last_updated": "string - ISO date",

  "problem_statement": "string - What problem does this solve? (2-3 sentences)",

  "target_users": [
    {
      "persona": "string - User type",
      "needs": ["string - Key need"],
      "pain_points": ["string - Current frustration"]
    }
  ],

  "user_stories": [
    {
      "id": "string - US-001",
      "as_a": "string - User persona",
      "i_want": "string - Desired action/capability",
      "so_that": "string - Expected benefit",
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
      "then": "string - Expected outcome"
    }
  ],

  "success_metrics": [
    {
      "metric": "string - Metric name",
      "current_baseline": "string - Current value",
      "target": "string - Target value with number",
      "measurement_method": "string - How to measure",
      "timeline": "string - When to measure"
    }
  ],

  "technical_requirements": {
    "dependencies": ["string - System/service dependencies"],
    "api_changes": ["string - API modifications needed"],
    "data_model_changes": ["string - Schema changes"],
    "security_considerations": ["string - Security requirements"]
  },

  "out_of_scope": ["string - Explicitly excluded items"],

  "risks": [
    {
      "risk": "string - Risk description",
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
  }
}
```

## Writing Effective Problem Statements

### Bad Examples (Avoid)

- "Users need a better experience" (vague)
- "We should add feature X" (solution, not problem)
- "Competitors have this" (not user-focused)

### Good Examples (Use)

- "Users currently spend 15 minutes manually entering data that could be automated, leading to errors in 23% of submissions and frustration that causes 12% churn in the first month."
- "Enterprise customers cannot comply with SOC2 requirements because our audit logs don't include user action timestamps, blocking $2.3M in pipeline."

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

### Bad Examples (Avoid)

- "Improve user satisfaction" (not measurable)
- "Reduce errors" (no baseline or target)

### Good Examples (Use)

- "Increase 7-day retention from 34% to 45% within 90 days of launch, measured by Amplitude cohort analysis."
- "Reduce average support tickets per user from 2.3/month to 1.5/month within 60 days, measured by Zendesk reporting filtered to feature-related tags."
