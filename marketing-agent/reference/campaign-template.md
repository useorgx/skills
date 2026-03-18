# Campaign Brief Template

## Required Fields

Every campaign brief MUST include these sections to pass validation.

## Marketing Thinking Checklist

Before drafting, verify these strategic foundations. If any answer is "I don't know," stop and resolve before writing copy.

- [ ] **Who exactly is this for?** ICP specific enough to find 10 people on LinkedIn in 5 minutes. (Framework: April Dunford -- Best-fit customers)
- [ ] **What job are they hiring us for?** Framed as: "When I [situation], I want to [motivation], so I can [outcome]." (Framework: Jobs-to-Be-Done)
- [ ] **Why now?** Triggering event or market moment creating urgency. If there is no "why now," reconsider the campaign timing.
- [ ] **Why us vs. alternatives?** Name the top 3 alternatives and state what you do that they cannot. (Framework: April Dunford -- Competitive alternatives -> Unique attributes)
- [ ] **What is the one thing?** If the audience forgets everything else, what single message sticks? This becomes the campaign's core message. (Framework: StoryBrand -- the plan)
- [ ] **What does the funnel look like?** Which AARRR stage is this campaign targeting? Do not build awareness campaigns when activation is the bottleneck. (Framework: Pirate Metrics)
- [ ] **How will we know it worked?** At least one metric with numeric target, measurement method, and timeline. (Framework: SMART objectives)
- [ ] **What are we testing?** State at least one hypothesis: "We believe [X] will happen because [Y]." (Framework: Message-Market Fit Testing)
- [ ] **What copy structure will we use?** Choose AIDA or PAS based on audience awareness level. AIDA for aware audiences. PAS for unaware audiences. (Framework: AIDA / PAS)
- [ ] **What will we do if it fails?** Contingency plan or iteration trigger. Define the threshold at which you pivot.

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
      "proof_points": ["Stat or customer quote", "Feature benefit"],
      "framework_reference": "Which framework informs this pillar (e.g., JTBD, Category Design)"
    },
    {
      "pillar": "Differentiation",
      "key_message": "Why us vs alternatives",
      "proof_points": ["Unique capability", "Comparison point"],
      "framework_reference": "April Dunford -- unique attributes mapped to value"
    },
    {
      "pillar": "Trust/Credibility",
      "key_message": "Why they can trust us",
      "proof_points": ["Customer logo", "Third-party validation"],
      "framework_reference": "Proof point types: customer, data, analyst, award"
    }
  ],
  "channels": [
    {
      "channel": "LinkedIn",
      "role": "Primary awareness",
      "content_types": ["Posts", "Ads"],
      "copy_structure": "AIDA for ads, PAS for organic posts"
    },
    {
      "channel": "Email",
      "role": "Nurture",
      "content_types": ["Drip sequence"],
      "copy_structure": "Hook Model stages mapped to email sequence"
    },
    {
      "channel": "Blog",
      "role": "SEO/Education",
      "content_types": ["Long-form articles"],
      "copy_structure": "Content-Market Fit validated topic clusters"
    }
  ],
  "success_metrics": [
    {
      "metric": "MQLs Generated",
      "baseline": "X/month",
      "target": "Y/month",
      "measurement": "HubSpot",
      "attribution_model": "Multi-touch, 30-day window"
    },
    {
      "metric": "Engagement Rate",
      "baseline": "X%",
      "target": "Y%",
      "measurement": "LinkedIn Analytics",
      "attribution_model": "Direct"
    },
    {
      "metric": "Pipeline Influence",
      "baseline": "$X",
      "target": "$Y",
      "measurement": "Salesforce",
      "attribution_model": "Multi-touch, 90-day window"
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
      "success_criteria": "[Metric] improves by [X%]",
      "decision_on_failure": "What we do if this hypothesis is wrong"
    }
  ],
  "budget": {
    "total": 50000,
    "breakdown": {
      "paid_media": 30000,
      "content_production": 15000,
      "tools": 5000
    }
  },
  "context_adaptation": {
    "company_stage": "Pre-PMF | Growth | Enterprise GTM",
    "gtm_motion": "PLG | Sales-led | Community-led | Content-led",
    "audience_type": "Developer | Executive | Practitioner | Mixed",
    "adaptations_applied": "List specific behavior changes from context adaptation protocol"
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

### ICP Depth Test

Your ICP is specific enough when you can answer all of these:

1. What is their job title? (not department -- title)
2. What company stage/size are they at? (specific range)
3. What is their triggering event? (why are they looking now?)
4. What are they doing today without your product? (current workaround)
5. What would they Google when they have this problem? (search intent)
6. Where do they spend time online? (channel selection)
7. Who do they report to? (stakeholder messaging)
8. What metrics are they measured on? (outcome alignment)

## Crafting Messaging Pillars

### Pillar Categories

1. **Value Proposition**: The core benefit you deliver (Framework: JTBD -- what job does it do?)
2. **Differentiation**: Why you vs. competitors (Framework: April Dunford -- unique attributes -> value)
3. **Credibility**: Why they should trust you (proof point types below)
4. **Urgency**: Why now vs. later (triggering events, market timing, cost of inaction)

### Proof Point Types (Ranked by Persuasion Strength)

1. **Named customer results** -- "Sarah Chen, VP Product at Acme, reduced review time by 60%"
2. **Quantified aggregate data** -- "Design partners saw 60% average reduction in first 30 days"
3. **Third-party validation** -- "Named a Gartner Cool Vendor 2025" or "4.8/5 on G2 from 200+ reviews"
4. **Product capability with demo** -- "Watch a 2-minute demo of architectural drift detection"
5. **Social proof at scale** -- "Used by 500+ engineering teams" or "50,000+ PRs reviewed daily"
6. **Awards and recognition** -- "Winner, TechCrunch Disrupt 2025"

Rule: every messaging pillar must have at least one proof point from the top 3 tiers. Lower-tier proof points should supplement, not replace, higher-tier ones.

### The "So What?" Test

For every pillar, ask "so what?" three times:

```
Feature: "AI-powered code review"
So what? -> "Catches issues linters miss"
So what? -> "Reduces review cycle from days to hours"
So what? -> "Engineers ship 40% faster, hitting roadmap commitments"
```

The third "so what?" is the message. The first "so what?" is a feature description. Never lead with the first.

## Channel Selection Guide

| Channel  | Best For                            | Content Types        | Frequency  | Copy Structure |
| -------- | ----------------------------------- | -------------------- | ---------- | -------------- |
| LinkedIn | B2B awareness, thought leadership   | Posts, articles, ads | 3-5x/week  | PAS for organic, AIDA for ads |
| Twitter  | Real-time engagement, announcements | Threads, updates     | 5-10x/week | Hook + thread format |
| Email    | Nurture, direct communication       | Drips, newsletters   | 1-2x/week  | AIDA per email, Hook Model across sequence |
| Blog     | SEO, education, long-form           | Articles, guides     | 2-4x/month | Content-Market Fit validated topics |
| Webinar  | Lead gen, deep education            | Live/recorded        | 1-2x/month | StoryBrand narrative structure |
| Community| Trust, retention, advocacy          | Discussion, events   | Daily       | Belonging > broadcasting |
| Podcast  | Thought leadership, founder story   | Interviews, series   | 1-2x/month | Brand Narrative Arc |

### Channel Risk Check

Every campaign must use >= 2 channels. If a campaign depends on a single channel, it is fragile. For each channel, answer:

1. What happens if this channel's algorithm changes tomorrow? (platform risk)
2. What is our organic reach on this channel? (paid dependency)
3. How long until content on this channel compounds? (time to value)
4. Can we measure attribution from this channel? (measurement capability)

## Attribution Model Selection

| Campaign Type | Recommended Model | Why |
|--------------|-------------------|-----|
| Brand awareness | Estimated lift study | Direct attribution is unreliable for brand |
| Content/SEO | First-touch + assisted | Content often starts journeys but does not close them |
| Paid acquisition | Last-touch + assisted | Paid should show direct impact but acknowledge assists |
| Nurture/email | Multi-touch, 30-day | Email touches happen across the journey |
| Full-funnel | Multi-touch, 90-day | Acknowledge the full journey, weight by recency |

Always state the attribution model in the campaign brief. Never claim credit without specifying how you measured it.
