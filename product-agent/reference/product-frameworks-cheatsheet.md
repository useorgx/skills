# Product Frameworks Cheatsheet

Quick-reference guide for the product agent. Use the right framework for the right situation.

## Framework Selection Guide

| Situation | Recommended Framework | Why |
|-----------|----------------------|-----|
| Ranking 5+ features with data | RICE | Quantitative, forces estimation of reach and effort |
| Quick prioritization, small team | ICE | Fast, gut-calibrated, good for < 20 items |
| Deciding "fix basics" vs. "build delight" | Kano | Categorizes features by user expectation type |
| SAFe environment with dependencies | WSJF | Captures cost of delay and shared resource constraints |
| Understanding what users really need | JTBD | Focuses on progress users want, not features they request |
| Continuous discovery rhythm | Opportunity Solution Tree | Prevents orphan solutions, ties everything to outcomes |
| Diagnosing growth problems | AARRR / Pirate Metrics | Identifies the leakiest funnel stage |
| Articulating why users should choose you | Value Proposition Canvas | Maps pains/gains to product capabilities |
| Aligning multiple teams | North Star Metric | Single metric with decomposed input metrics per team |
| Structuring the discovery process | Double Diamond | Prevents jumping to solutions before understanding problems |
| Assessing product-market fit | PMF Engine | Quantitative and qualitative PMF signals |
| Scoping an MVP | MVP Spectrum | Picks the right fidelity for what you need to learn |

---

## RICE Scoring

**Formula:** Score = (Reach x Impact x Confidence) / Effort

| Dimension | Scale | Notes |
|-----------|-------|-------|
| Reach | Users per quarter | Estimated number of users who will encounter the feature |
| Impact | 3=massive, 2=high, 1=medium, 0.5=low, 0.25=minimal | How much the feature moves the target metric for each user |
| Confidence | 100%, 80%, 50% | How sure you are about the above estimates |
| Effort | Person-months | Total effort including design, engineering, QA |

**Example:**

| Feature | Reach | Impact | Confidence | Effort | Score |
|---------|-------|--------|------------|--------|-------|
| Dark mode | 5000 | 1 | 80% | 2 | 2000 |
| CSV import | 2000 | 2 | 100% | 1 | 4000 |
| SSO | 500 | 3 | 100% | 3 | 500 |

**When to use:** Established products with 5+ items to rank and reasonable data on reach.

**Watch out for:** Garbage-in-garbage-out. If reach estimates are fabricated, the scoring is theater.

---

## ICE Scoring

**Formula:** Score = Impact x Confidence x Ease (each 1-10)

| Dimension | Scale | Notes |
|-----------|-------|-------|
| Impact | 1-10 | How much this moves the needle on the target metric |
| Confidence | 1-10 | How sure you are about impact and ease estimates |
| Ease | 1-10 | How easy this is to implement (10=trivial, 1=massive) |

**When to use:** Early-stage, small teams, fast decisions, backlogs under 20 items.

**Watch out for:** All scores drift toward 7. Force at least 2 items to score below 4 and 2 above 8 to maintain discrimination.

---

## Kano Model

### Feature Categories

| Category | User Reaction When Present | User Reaction When Absent | Strategy |
|----------|---------------------------|--------------------------|----------|
| Must-be | "Of course" (no satisfaction increase) | Strong dissatisfaction, churn | Implement first. Never skip. |
| One-dimensional | Satisfaction scales linearly | Proportional dissatisfaction | Invest based on competitive context |
| Attractive | Surprise and delight | No dissatisfaction | Use for differentiation. Low risk to skip. |
| Indifferent | No reaction | No reaction | Do not build. |
| Reverse | Dissatisfaction | Satisfaction (or no reaction) | Actively avoid. |

### Classification Method

Survey users with two questions per feature:
1. "If the product HAD this feature, how would you feel?" (Functional)
2. "If the product DID NOT have this feature, how would you feel?" (Dysfunctional)

Answer options: Like it, Expect it, Neutral, Can live with it, Dislike it.

Cross-reference answers to classify:

| | Like | Expect | Neutral | Live with | Dislike |
|---|---|---|---|---|---|
| **Like** | Q | A | A | A | O |
| **Expect** | R | I | I | I | M |
| **Neutral** | R | I | I | I | M |
| **Live with** | R | I | I | I | M |
| **Dislike** | R | R | R | R | Q |

(Rows = Dysfunctional answer, Columns = Functional answer)
A=Attractive, O=One-dimensional, M=Must-be, I=Indifferent, R=Reverse, Q=Questionable

**When to use:** Deciding between "fix the basics" and "build something exciting." Feature categorization for roadmap planning.

---

## Jobs-to-Be-Done (JTBD)

### Job Statement Format

```
When [situation/context],
I want to [motivation/action],
So I can [desired outcome].
```

### Finding Jobs

1. Interview users about a recent time they "hired" a product to do a job
2. Focus on the struggling moment: what was happening when they decided to seek a solution?
3. Map the forces: Push (current pain), Pull (new solution appeal), Anxiety (fear of change), Habit (comfort with status quo)

### Forces Diagram

```
        PUSH (pain of current situation)
              |
              v
  HABIT <--- USER ---> PULL (appeal of new solution)
              ^
              |
        ANXIETY (fear of switching)
```

Switch happens when: Push + Pull > Anxiety + Habit

**When to use:** Feature requests conflict. Users ask for contradictory things. You need to understand demand, not just stated preferences.

---

## Opportunity Solution Tree

```
                    TARGET OUTCOME
                    (metric to move)
                   /       |        \
            Opportunity  Opportunity  Opportunity
            (unmet need) (unmet need) (unmet need)
           /    |           |    \         |
       Solution Solution  Solution Solution Solution
       /    \      |        |       |        |
    Exp.  Exp.   Exp.     Exp.    Exp.     Exp.
```

### Rules

1. Every solution must trace to an opportunity
2. Every opportunity must trace to the target outcome
3. Orphan solutions are banned (solutions without a parent opportunity)
4. Multiple solutions per opportunity = good (more options to test)
5. Experiments validate solutions before full investment

**When to use:** Continuous discovery. Weekly discovery rhythm. Preventing solution-first thinking.

---

## Pirate Metrics (AARRR)

### Funnel Stages

| Stage | Question | Example Metrics |
|-------|----------|----------------|
| **Acquisition** | How do users find you? | Visitors, signups, channel attribution |
| **Activation** | Do they have a great first experience? | Onboarding completion, time-to-value, "aha moment" rate |
| **Retention** | Do they come back? | D1/D7/D30 retention, MAU/DAU ratio, churn rate |
| **Revenue** | Do they pay? | Conversion rate, ARPU, LTV, expansion revenue |
| **Referral** | Do they tell others? | NPS, referral rate, viral coefficient |

### Optimization Priority

Always optimize the leakiest stage first. Never optimize acquisition when retention is broken — you are filling a leaky bucket.

**Diagnostic sequence:**
1. Check retention first. If broken, nothing else matters.
2. Check activation. If users never reach the "aha moment," retention will always be bad.
3. Check acquisition. Only after activation and retention are healthy.
4. Check revenue. Monetization of an engaged user base.
5. Check referral. The multiplier on everything above.

---

## Value Proposition Canvas

### Customer Profile Side

| Element | Description | Example |
|---------|-------------|---------|
| Jobs | What the customer is trying to accomplish (functional, social, emotional) | "Prepare a board presentation showing team productivity" |
| Pains | Obstacles, risks, undesired outcomes related to the jobs | "Spends 4 hours manually aggregating data from 3 tools" |
| Gains | Desired outcomes, benefits, aspirations | "Look competent in front of the board without weekend prep" |

### Value Map Side

| Element | Description | Must Map To |
|---------|-------------|------------|
| Products/Services | What you offer | Jobs |
| Pain Relievers | How you alleviate pains | Specific pains |
| Gain Creators | How you create gains | Specific gains |

### Fit Test

Every Pain Reliever must map to a documented Pain. Every Gain Creator must map to a documented Gain. Unmapped items are solutions looking for problems — remove them or find the pain/gain they address.

---

## North Star Metric Framework

### Structure

```
              NORTH STAR METRIC
         (captures core value delivery)
          /      |       |       \
      Input    Input   Input    Input
      Metric   Metric  Metric   Metric
      (Team A) (Team B) (Team C) (Team D)
```

### Good North Star Metrics

| Product Type | North Star Metric | Why |
|-------------|------------------|-----|
| Marketplace | Number of transactions completed per week | Captures value for both sides |
| SaaS tool | Weekly active tasks completed | Measures real value delivery |
| Content platform | Time spent consuming content | Proxy for value received |
| Communication tool | Messages sent per week | Core value loop |

### Bad North Star Metrics

- Revenue (lagging indicator, not value delivery)
- Signups (vanity, not value)
- Page views (activity, not value)
- NPS (subjective, infrequent)

---

## WSJF (Weighted Shortest Job First)

**Formula:** WSJF = (User/Business Value + Time Criticality + Risk Reduction) / Job Duration

| Dimension | Scale | Notes |
|-----------|-------|-------|
| User/Business Value | 1, 2, 3, 5, 8, 13, 20 (Fibonacci) | Relative value to users or the business |
| Time Criticality | 1, 2, 3, 5, 8, 13, 20 | Cost of delay. Higher = more urgent. |
| Risk Reduction / Opportunity Enablement | 1, 2, 3, 5, 8, 13, 20 | Does this reduce risk or enable other work? |
| Job Duration | 1, 2, 3, 5, 8, 13, 20 | Relative effort (not absolute time) |

**When to use:** SAFe environments. Teams with shared resources and dependencies. When cost of delay is a primary concern.

---

## MVP Spectrum

| MVP Type | What It Is | What It Tests | Investment | Example |
|----------|-----------|--------------|-----------|---------|
| **Concierge** | Manually deliver the value, no product | Demand: will people pay for this outcome? | Minimal (time) | Personally curate playlists for each user |
| **Wizard of Oz** | Appears automated, manual behind the scenes | UX: does the experience work? | Low (facade + manual ops) | AI chatbot that is actually a human typing |
| **Single-feature** | One thing, done adequately | Feasibility + basic value | Medium | Only the core workflow, no settings/admin |
| **MLP (Minimum Lovable)** | One thing, done delightfully | Retention: will people come back? | Medium-High | Core workflow with polish, onboarding, delight moments |

### Selection Criteria

- "We don't know if anyone wants this" -> Concierge MVP
- "We think people want this but don't know if our UX works" -> Wizard of Oz MVP
- "We know the UX works but need to prove we can build it" -> Single-feature MVP
- "We can build it but need to prove people will keep using it" -> MLP

---

## Product-Market Fit Engine

### Sean Ellis Test

Survey users: "How would you feel if you could no longer use [product]?"

| Response | Meaning |
|----------|---------|
| Very disappointed | Core users. PMF signal. |
| Somewhat disappointed | Users who see value but have alternatives. |
| Not disappointed | Not your users. |

**PMF threshold:** >40% "Very disappointed"

### Complementary Signals

| Signal | PMF Present | PMF Absent |
|--------|------------|-----------|
| Retention curve | Flattens (users stick) | Continues declining |
| NPS | Promoter reasons = core value | Promoter reasons = minor features |
| Organic growth | Word of mouth increasing | All growth from paid channels |
| Usage depth | Users discover new features over time | Usage stays shallow |
| Willingness to pay | Users pay without negotiation | Constant discounting needed |

---

## Double Diamond

```
  DISCOVER          DEFINE          DEVELOP          DELIVER
  (diverge)        (converge)      (diverge)        (converge)

    /\                /\              /\                /\
   /  \              /  \            /  \              /  \
  /    \            /    \          /    \            /    \
 /      \          /      \        /      \          /      \
/        \________/        \______/        \________/        \

 Explore           Frame the        Generate          Build and
 the problem       right problem    solutions          ship
 space             to solve         broadly            the best one
```

### Key Principle

The first diamond is about getting the problem right. The second diamond is about getting the solution right. Most teams skip the first diamond entirely and wonder why their solutions do not resonate.
