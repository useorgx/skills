# Full-Surface Audit

Use this contract for a route, a flow, onboarding, or a product-wide audit.
The output must be a durable registry, not a one-time list of opinions.

## Start with the journey

Map every retained surface to one move:

1. Orient — understand OrgX and establish a credible goal.
2. Frame — turn intent into a reviewable goal and initiative.
3. Organize — decompose work without losing outcome, owner, or proof.
4. Execute — see the next ready action, motion, and blockers.
5. Decide — ask for human judgment only when it changes the outcome.
6. Prove — connect artifacts and receipts back to the goal.
7. Continue — resume from the next action without reconstructing context.

If a surface advances none of these, it must justify its existence.

## Registry fields

Record for every page or feature:

| Field | Meaning |
| --- | --- |
| Route / entry point | The canonical address or invocation. |
| Family | Core app, core-adjacent, internal/dev, public/proof, or compatibility. |
| User job | One sentence beginning with a verb. |
| Journey move | Orient, Frame, Organize, Execute, Decide, Prove, or Continue. |
| Data owner | The hook, service, or server boundary that owns truth. |
| Action owner | The one control system that mutates the job. |
| States | Loading, empty, populated, long, degraded, urgent, resolved, permission. |
| Breakpoints | Desktop, tablet, phone evidence. |
| Disposition | Retain, redesign, consolidate, redirect, remove, or verify boundary. |
| Evidence | Screenshot, test, receipt, commit, PR, deploy, or outcome. |
| Next gap | The highest-risk unverified behavior. |

Keep a complete route appendix so hidden and parallel routes cannot disappear
from scope.

## Interaction review

For each user job, test:

- Can the user predict the result before acting?
- Is the action next to its consequence?
- Does the UI acknowledge input within 400ms?
- Can the user undo, cancel, go back, or recover?
- Is selection shareable/addressable when it should be?
- Are destructive or consequential actions clearly distinguished?
- Does an empty state create value rather than describe emptiness?
- Does an error preserve entered work and offer a next step?
- Does the default view answer the page question without scrolling?

## Cognitive-load review

Flag:

- more than three equally visible choices;
- repeated nouns, metrics, titles, or explanations;
- controls shown before the user has the context to use them;
- filters with no meaningful result set;
- permanent chrome for rare actions;
- paragraphs where a state, consequence, or next action would suffice;
- multiple status vocabularies for the same concept;
- detail competing with the dominant signal.

Fix structure before styling. Prefer removal, grouping, inline consequence, and
progressive disclosure over smaller type or tighter cards.

## Onboarding

Audit onboarding as a time-to-value pipeline, not a slideshow.

1. Promise: show what OrgX will do in concrete language.
2. Input: capture the smallest credible goal and required context.
3. Interpretation: reflect back a draft the user can correct.
4. Commitment: make the first meaningful action explicit.
5. Proof: show the first generated plan, artifact, decision, or next action.

Requirements:

- Value appears before configuration.
- Optional personalization waits until it improves the current result.
- Existing data is reused; do not ask twice.
- Progress describes meaningful moves, not arbitrary screen count.
- Exit, resume, back, and error recovery preserve work.
- Mobile keyboards and small viewports do not obscure the primary action.
- Versioned onboarding routes are consolidation candidates, not permanent
  alternatives.

## Cut protocol

Before removing a feature or route:

1. Search code, navigation, docs, links, tests, analytics references, and live
   entry points.
2. Name the canonical replacement and confirm it covers the user job.
3. Preserve useful deep links with a redirect and query parameters.
4. Remove duplicate UI, data, copy, fixtures, and tests together.
5. Add redirect/contract tests.
6. Report removal, merge, deployment, and observed traffic separately.

Unknown use is a research gap, not proof of value or permission to break links.
