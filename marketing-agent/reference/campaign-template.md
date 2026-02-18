# Campaign Brief Template

## Required Fields

Every campaign brief MUST include these sections to pass validation.

## Template Structure

```json
{
  "campaign_name": "[Descriptive Name] - [Quarter/Date]",
  "objective": "Increase [metric] by [X%] from [baseline] to [target] by [date] through [strategy]",
  "target_audience": {
    "primary_icp": "[Job Title] at [Company Type] with [Characteristics]",
    "company_size": "[Range]",
    "industry": "[Vertical(s)]",
    "pain_points": [
      "Pain point 1 with specific impact",
      "Pain point 2 with quantified cost"
    ],
    "triggers": ["Buying signal 1", "Buying signal 2"]
  },
  "messaging_pillars": [
    {
      "pillar": "Core Value Proposition",
      "key_message": "Clear, benefit-focused statement",
      "proof_points": ["Stat or customer quote", "Feature benefit"]
    },
    {
      "pillar": "Differentiation",
      "key_message": "Why us vs alternatives",
      "proof_points": ["Unique capability", "Comparison point"]
    },
    {
      "pillar": "Trust/Credibility",
      "key_message": "Why they can trust us",
      "proof_points": ["Customer logo", "Third-party validation"]
    }
  ],
  "channels": [
    {
      "channel": "LinkedIn",
      "role": "Primary awareness",
      "content_types": ["Posts", "Ads"]
    },
    {
      "channel": "Email",
      "role": "Nurture",
      "content_types": ["Drip sequence"]
    },
    {
      "channel": "Blog",
      "role": "SEO/Education",
      "content_types": ["Long-form articles"]
    }
  ],
  "success_metrics": [
    {
      "metric": "MQLs Generated",
      "baseline": "X/month",
      "target": "Y/month",
      "measurement": "HubSpot"
    },
    {
      "metric": "Engagement Rate",
      "baseline": "X%",
      "target": "Y%",
      "measurement": "LinkedIn Analytics"
    },
    {
      "metric": "Pipeline Influence",
      "baseline": "$X",
      "target": "$Y",
      "measurement": "Salesforce"
    }
  ],
  "timeline": [
    { "milestone": "Creative Brief Approved", "date": "Week 1" },
    { "milestone": "Assets Produced", "date": "Week 2" },
    { "milestone": "Campaign Launch", "date": "Week 3" },
    { "milestone": "Mid-Campaign Review", "date": "Week 5" },
    { "milestone": "Campaign End + Analysis", "date": "Week 8" }
  ],
  "hypotheses": [
    {
      "hypothesis": "If we [action], then [outcome] because [reasoning]",
      "test_method": "A/B test with [X] sample size",
      "success_criteria": "[Metric] improves by [X%]"
    }
  ],
  "budget": {
    "total": 50000,
    "breakdown": {
      "paid_media": 30000,
      "content_production": 15000,
      "tools": 5000
    }
  }
}
```

## Writing Effective Objectives

### SMART Framework

- **S**pecific: Exactly what will be achieved
- **M**easurable: Quantified target
- **A**chievable: Realistic given resources
- **R**elevant: Aligned with business goals
- **T**ime-bound: Clear deadline

### Bad Examples

- "Increase brand awareness" (not measurable)
- "Get more leads" (not specific or time-bound)
- "Improve marketing ROI" (vague)

### Good Examples

- "Generate 500 MQLs from Series B+ fintech companies by Q2 end, measured by HubSpot lead scoring"
- "Increase LinkedIn engagement rate from 2.1% to 4% within 6 weeks through thought leadership content"
- "Drive $2M in pipeline influence from existing customers through upsell campaign by month end"

## Defining Target Audience

### ICP Formula

```
[Job Title] at [Company Type] who [Key Behavior/Challenge]
```

### Bad Examples

- "Marketing professionals" (too broad)
- "B2B companies" (no specificity)

### Good Examples

- "VP of Engineering at Series B-D SaaS companies (100-500 employees) who are scaling their platform team and struggling with developer productivity"
- "Head of Product at enterprise fintech companies facing compliance requirements for SOC2 and dealing with slow feature velocity"

## Crafting Messaging Pillars

### Pillar Categories

1. **Value Proposition**: The core benefit you deliver
2. **Differentiation**: Why you vs. competitors
3. **Credibility**: Why they should trust you
4. **Urgency**: Why now vs. later

### Proof Point Types

- Customer quotes/testimonials
- Quantified results (X% improvement)
- Third-party validation (analyst quotes, awards)
- Product capabilities (unique features)
- Social proof (logos, user counts)

## Channel Selection Guide

| Channel  | Best For                            | Content Types        | Frequency  |
| -------- | ----------------------------------- | -------------------- | ---------- |
| LinkedIn | B2B awareness, thought leadership   | Posts, articles, ads | 3-5x/week  |
| Twitter  | Real-time engagement, announcements | Threads, updates     | 5-10x/week |
| Email    | Nurture, direct communication       | Drips, newsletters   | 1-2x/week  |
| Blog     | SEO, education, long-form           | Articles, guides     | 2-4x/month |
| Webinar  | Lead gen, deep education            | Live/recorded        | 1-2x/month |
