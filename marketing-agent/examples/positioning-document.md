# Example Positioning Document: CodePilot AI

## Framework Applied

April Dunford positioning framework (Obviously Awesome). Every section below maps to a step in the framework.

## Positioning Document

```json
{
  "company_name": "CodePilot AI",
  "product_name": "CodePilot",
  "document_version": "1.0",
  "last_updated": "2026-03-15",
  "framework": "April Dunford — Obviously Awesome",

  "competitive_alternatives": [
    {
      "alternative": "Manual code review by senior engineers",
      "description": "Senior engineers review every PR manually, spending 8-12 hours per week on reviews instead of architecture and mentoring",
      "why_customers_use_it": "It is the default. No setup required. Senior engineers have deep context about the codebase."
    },
    {
      "alternative": "GitHub Copilot + basic linting",
      "description": "AI-assisted code completion plus static analysis rules that catch syntax and style issues",
      "why_customers_use_it": "Already bundled into their GitHub subscription. Helps write code faster. Catches surface-level issues automatically."
    },
    {
      "alternative": "Custom linter rules and CI checks",
      "description": "Teams build internal linting rules and CI pipelines that enforce coding standards",
      "why_customers_use_it": "Highly customizable. No external dependency. Fits into existing CI/CD workflow."
    },
    {
      "alternative": "Hiring more senior engineers",
      "description": "Scaling the review bottleneck by adding headcount",
      "why_customers_use_it": "More reviewers means shorter review queues. New hires bring fresh perspectives."
    }
  ],

  "unique_attributes": [
    {
      "attribute": "Learns team-specific coding patterns and conventions",
      "why_alternatives_lack_it": "Manual review depends on tribal knowledge that walks out the door. Copilot knows general patterns but not your team's patterns. Linters only catch what you explicitly write rules for.",
      "customer_outcome": "New engineers write code that matches team conventions from day one, reducing onboarding review cycles from 3 weeks to 3 days"
    },
    {
      "attribute": "Identifies architectural drift across PRs",
      "why_alternatives_lack_it": "Manual reviewers catch drift in individual PRs but miss slow drift across dozens of PRs over weeks. Static analysis cannot reason about architectural intent.",
      "customer_outcome": "Engineering leaders see architectural violations before they compound, preventing the 2-3 month refactoring cycles that derail roadmaps"
    },
    {
      "attribute": "Reduces review cycle time from days to hours",
      "why_alternatives_lack_it": "Manual review is gated on senior engineer availability. Linters run fast but only catch surface issues. Copilot helps writing but not reviewing.",
      "customer_outcome": "Developers ship features 40% faster because they are not waiting 24-48 hours for review feedback"
    },
    {
      "attribute": "Captures and codifies institutional knowledge",
      "why_alternatives_lack_it": "When a senior engineer leaves, their review knowledge leaves with them. No alternative systematically captures what good code looks like for this specific team.",
      "customer_outcome": "The team's code quality standards persist regardless of team turnover, reducing the knowledge-loss risk that keeps engineering leaders up at night"
    }
  ],

  "value_proposition": "CodePilot is the AI code review assistant that learns how your team writes code, catches the architectural and convention issues that linters miss, and reduces review cycle time from days to hours -- so your senior engineers can focus on architecture and mentoring instead of spending half their week reviewing PRs.",

  "best_fit_customers": {
    "job_title": "VP Engineering, Head of Engineering, Engineering Director",
    "company_stage": "Series B through Series D",
    "company_size": "50-500 engineers",
    "industry": "B2B SaaS, Developer Tools, Fintech, Enterprise Software",
    "triggering_event": "The team has grown past 30 engineers and review queues are now a top-3 complaint in engineering surveys. Or: a senior engineer who was the primary reviewer just left, and review quality has visibly dropped.",
    "current_workaround": "Relying on 2-3 senior engineers who each spend 10+ hours per week on reviews, supplemented by basic linting. The senior engineers are burning out and the review bottleneck is the number one blocker to shipping velocity.",
    "disqualifying_signals": [
      "Teams smaller than 15 engineers (review bottleneck is not yet painful enough)",
      "Teams that do not do code review at all (cultural mismatch)",
      "Highly regulated industries where AI-assisted review faces compliance barriers (healthcare, defense)"
    ]
  },

  "market_category": {
    "name": "AI Code Review Intelligence",
    "category_type": "adjacent",
    "category_story": "Code review has been treated as a manual process supplemented by dumb automation (linters, static analysis). AI coding tools have focused on code generation (Copilot, Cursor) but ignored the review side of the workflow. AI Code Review Intelligence is the adjacent category that applies machine learning to the review process itself -- not to write code, but to evaluate it with the same contextual understanding that your best senior engineers have. This category exists because teams have scaled past the point where manual review works, but the tools available for review automation are still rule-based, not intelligence-based."
  },

  "proof_points": [
    {
      "type": "customer",
      "statement": "After deploying CodePilot, our average PR review cycle dropped from 36 hours to 4 hours. Our senior engineers got 8 hours per week back for architecture work.",
      "source": "Marcus Chen, VP Engineering at Stackline (Series C, 120 engineers)"
    },
    {
      "type": "data",
      "statement": "Design partners reduced review cycle time by 60% on average within the first 30 days of deployment",
      "source": "Internal measurement across 3 design partners, December 2025 - February 2026"
    },
    {
      "type": "data",
      "statement": "CodePilot identified 12 architectural violations in the first week at one design partner -- issues that had been accumulating for months undetected",
      "source": "Deployment report, Nexus Financial (Series B, 80 engineers)"
    },
    {
      "type": "customer",
      "statement": "We had a senior engineer leave and were terrified about code quality dropping. CodePilot had already learned his review patterns. Quality actually improved because the feedback was faster and more consistent.",
      "source": "Sarah Park, Engineering Director at FlowState (Series B, 65 engineers)"
    },
    {
      "type": "data",
      "statement": "NPS of 72 among beta users, with primary satisfaction driver being 'catches things I would have missed'",
      "source": "Beta program survey, January 2026, n=48 engineering leads"
    }
  ],

  "messaging_pillars": [
    {
      "headline": "Your best reviewer, available on every PR",
      "supporting_copy": "CodePilot learns how your team writes code -- your conventions, your architectural patterns, your quality bar. It reviews every PR with the same contextual understanding as your most experienced engineer, but it never takes a day off and it never has a queue.",
      "proof": "Design partners reduced review cycle time by 60%. Marcus Chen at Stackline: 'Our senior engineers got 8 hours per week back for architecture work.'"
    },
    {
      "headline": "Catch architectural drift before it costs you a quarter",
      "supporting_copy": "Individual PRs look fine. But across dozens of PRs over weeks, your architecture slowly drifts from intent. CodePilot tracks architectural patterns across your entire codebase and flags drift before it compounds into a multi-month refactoring project.",
      "proof": "Identified 12 architectural violations in the first week at Nexus Financial -- issues that had accumulated undetected for months."
    },
    {
      "headline": "Institutional knowledge that does not walk out the door",
      "supporting_copy": "When your best reviewer leaves, their knowledge leaves with them. CodePilot codifies your team's review standards so quality persists through turnover. New engineers get the same caliber of feedback on day one that they would have gotten from a 5-year veteran.",
      "proof": "Sarah Park at FlowState: 'A senior engineer left and quality actually improved because CodePilot's feedback was faster and more consistent.'"
    },
    {
      "headline": "Intelligence, not rules",
      "supporting_copy": "Linters catch what you tell them to catch. CodePilot understands what you are trying to build. It reasons about intent, context, and team patterns -- not just syntax and style. This is the difference between a spell-checker and an editor.",
      "proof": "NPS of 72 among beta users, with primary satisfaction driver being 'catches things I would have missed.'"
    }
  ]
}
```

## How This Document Was Built

### Framework Application

Each section maps directly to April Dunford's positioning framework:

1. **Competitive alternatives** -- started from the customer's perspective. What would they do if CodePilot did not exist? Not "other AI code review tools" (which barely exist) but the actual alternatives: manual review, linters, hiring more people.

2. **Unique attributes** -- only attributes that alternatives genuinely lack. Each attribute is stated as a capability and then immediately connected to why alternatives cannot do this.

3. **Value** -- each unique attribute is mapped to a specific customer outcome with quantification where possible. "Learns team patterns" is a feature. "New engineers write convention-matching code from day one, reducing onboarding review cycles from 3 weeks to 3 days" is value.

4. **Best-fit customers** -- specific enough to find on LinkedIn. Includes triggering events (when do they start looking?) and current workarounds (what are they doing today?). Also includes disqualifying signals to prevent wasted effort.

5. **Market category** -- chose "adjacent" because AI code review does not exist as a recognized category yet, but it is adjacent to the known categories of code review tooling and AI coding assistants. The category story explains why this category needs to exist now.

### Context Adaptation

Company stage: Series A, 18 months post-founding. This means:
- Message testing > brand building (positioning document is more important than brand guidelines)
- Founder-led content will be the primary distribution channel
- Proof points from design partners are the strongest available evidence
- The category story needs to be simple enough for a founder to tell in a 2-minute pitch

### "So What?" Test Results

Every unique attribute was tested:

| Attribute | So What? | Passes? |
|-----------|----------|---------|
| Learns team-specific patterns | New engineers match conventions from day one, 3-week onboarding becomes 3-day | Yes |
| Identifies architectural drift | Prevents 2-3 month refactoring cycles that derail roadmaps | Yes |
| Reduces review cycle time | Ship 40% faster, unblock developers waiting 24-48 hours for feedback | Yes |
| Captures institutional knowledge | Quality persists through team turnover, reducing key-person risk | Yes |

### Proof Point Coverage

| Pillar | Proof Type | Strength |
|--------|-----------|----------|
| Best reviewer on every PR | Customer + Data | Strong -- named customer, quantified result |
| Catch architectural drift | Data | Medium -- single customer example, needs more |
| Institutional knowledge | Customer | Medium -- compelling story, needs quantification |
| Intelligence, not rules | Data (NPS) | Medium -- NPS is strong but "catches things I missed" needs specific examples |

### Gaps and Next Steps

1. **Analyst proof needed**: No analyst or award proof points yet. Recommend scheduling Forrester briefing within 60 days to pursue inclusion in code quality tooling research.
2. **Architectural drift pillar needs more proof**: One customer example is not enough. Run a 30-day measurement across all design partners to quantify drift detection frequency and cost avoidance.
3. **Competitive narrative needed**: This positioning document should be followed by a `--type competitive-narrative` artifact that details head-to-head scenarios against GitHub Copilot and manual review.
4. **Message testing needed**: Before scaling to paid channels, test the four messaging pillars via A/B tested LinkedIn ads. Minimum 3 variants, 5,000 impressions per variant, track CTR and demo request conversion.
