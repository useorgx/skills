---
name: orgx-quality-bar
version: "1.0.0"
description: |
  How OrgX judges artifacts — and how to produce work that passes honestly.
  Use whenever an agent writes, attaches, or reworks any artifact. Teaches the
  four-lens verification system (judged, measured, observed, outcome), domain
  layer stacks, the 0.85 quality gate, artifact type codes and the mistype
  guard, deterministic GTM sendability checks, and the rework loop.
---

# OrgX Quality Bar

Every artifact you attach to OrgX is verified by a four-lens system. This skill
tells you what the lenses check so you can pass them by doing the work well —
not by writing around the judge.

The honesty contract: **no verdict without evidence**. Every score drills to a
quoted span in your artifact. The same contract binds you: every claim of done
carries its receipt.

## The Four Lenses

1. **Judged** — an LLM comparison judge scores each layer of your domain's
   layer stack separately (0–1), often against pinned reference artifacts.
   Layer scores are never averaged into one number that hides weakness.
2. **Measured** — deterministic, hand-checkable pass/fail findings (placeholder
   scan, unsourced-stat scan, word count, CTA count, hype words). These run
   before any judge opines. A check only runs where its canon applies;
   inapplicable checks are omitted, never passed.
3. **Observed** — quality-bearing issues flagged outside the versioned
   criteria, with evidence and severity. Observations cap confidence; they
   never change the score. Recurring observations get promoted into the
   criteria, so the bar tightens over time.
4. **Outcome** — reality events (sent, replied, merged, shipped) recorded
   independently. Scored separately, never blended into judged scores.

## The 0.85 Gate

- AQ (artifact quality) ≥ **0.85** → ship. Below → held for review or rework.
- Weak layers are visible individually ("evidence_density 0.62 below
  reference") — you cannot hide a weak layer behind strong ones.
- Verdicts that say "artifact not provided / empty / cannot read" are
  self-invalidating and dropped. If your verdicts keep self-invalidating,
  the artifact body is not reaching the judge — fix the attachment, don't
  resubmit the same call.

## Layer Stacks (what "good" means per domain)

Each domain is judged on 4–5 weighted layers. Full stacks with weights,
questions, and anchors: see [reference/layer-stacks.md](reference/layer-stacks.md).
The one-line version:

| Domain | Layers (heaviest first) |
| --- | --- |
| Sales | claim_sharpness, evidence_density, personalization_fit, voice, actionability |
| Marketing | differentiation, proof_points, category_clarity, voice_brand_fit, distribution_fitness |
| Design | composition, information_hierarchy, world_coherence, craft_materiality, intent_legibility |
| Engineering | correctness_risk, verifiability, scope_discipline, operability, clarity |
| Product | problem_grounding, decision_quality, user_evidence, measurability, scope_sequencing |
| Ops | actionability_under_stress, failure_paths, ownership_clarity, timeliness, evidence |
| Research | source_quality, synthesis_over_summary, falsifiability, coverage, actionable_findings |
| Orchestration | dependency_truth, receipt_completeness, progress_honesty, coordination_clarity, next_action_sharpness |

Type overrides that change which stack judges you:

- Design **audits/critiques** are judged as criticism (observation acuity,
  evidence specificity, prioritization, actionability) — not as visual work.
- **Plans** (`orchestration.next_initiative`, `orchestration.dispatch_plan`)
  are judged as plans: checkable acceptance criteria and honest sizing — not
  as status reports with receipts they cannot have yet.
- Any `*.structured_blocker` is judged as an operational document (ops stack):
  a marketing blocker at 3am must still be actionable.

## Artifact Type Codes and the Mistype Guard

Type codes are `<domain>.<type_name>` (e.g. `sales.icp_offer_sequence`,
`eng.pull_request`, `design.audit`, `ops.runbook`,
`orchestration.next_initiative`). The type decides which layer stack and which
measured checks apply — a mistyped artifact is judged on the wrong bar.

- **Declare the type when you know it** — as `artifact_type` on
  `orgx_attach` / `orgx_write` (artifact create) / `orgx_submit_receipt`.
- If you don't declare, a classifier infers the type. Generic outputs may be
  flagged `artifact_type_provisional: true` and judged on the general stack
  (fitness_to_intent, evidence, clarity, actionability) until promoted.
- Never declare a flattering type to get an easier stack. The mistype guard
  re-classifies, and a wrong stack produces feedback you cannot act on.

## GTM Sendability (measured checks for sales/marketing)

The applicability mode decides which checks run:

- **instance** (send-ready outreach — the default): full battery.
- **template** (`sales.outreach_sequence`, `sales.follow_up_sequence`,
  `sales.send_plan`, `sales.icp_offer_sequence`, `sales.territory_plan`,
  `marketing.nurture_sequence`): declared `{{merge_field}}` tokens are design,
  not defects; word/CTA canons still apply per variant.
- **doc** (`sales.strategy`, `sales.battlecard`, `marketing.positioning_brief`,
  `marketing.positioning_document`, `marketing.launch_plan`,
  `marketing.messaging_matrix`, `marketing.competitive_narrative`): no word or
  CTA canon — a strategy doc is not "too long" against outreach rules.

The five checks:

1. **Placeholders**: any unreplaced `TBD`, `[Name]`, `{{first_name}}` fails an
   instance. Replace all of them or type the artifact as a template.
2. **Unsourced stats**: a number used as a claim needs a source marker within
   ~80 characters — "per our data", "according to …", a URL, or a citation.
3. **Word count**: cold outreach ≤ 120 words per variant.
4. **CTA count**: exactly one ask per piece. Two CTAs convert like zero.
5. **Hype words**: revolutionize, game-changing, supercharge, seamless,
   cutting-edge, next-gen, world-class, unleash, skyrocket, 10x — all fail.
   Use concrete verbs: show, save, deliver.

## The Rework Loop

When an operator requests changes, your draft parks in `changes_requested`
(non-terminal) and the linked task reopens with the note stamped as
`metadata.rework_feedback`.

1. Read `metadata.rework_feedback` on the task before doing anything else.
2. Change what the feedback names. Below-bar feedback is specific — layer,
   quoted evidence, reference comparison. Resubmitting near-identical work
   fails the same layers again.
3. Produce a fresh artifact version; it supersedes on pass (≥ 0.85). Version
   lineage records the chain (v1 → changes_requested → v2 → approved), so
   the iteration history is visible — make each version a real response.

## Scoring Honestly

Do:

- Deliver the layers, not descriptions of them. Cite sources with resolving
  URLs. Name failure modes (engineering), quote real users (product), give
  numbered steps with expected output and an if-this-fails branch (ops),
  commit to one lead claim (sales).
- Study pinned references when shown — comparison against references is the
  primary scoring mechanism, and they are the bar for "above".
- Keep scope tight. Tightness is a clarity signal; a positioning doc is not
  5,000 words.

Don't:

- Open with self-describing preambles ("This well-researched brief
  demonstrates…"). Meta-commentary about your own quality can prime or annoy
  the judge and is never evidence. Deliver the work.
- Grade-shop: re-running evaluation on unchanged content to fish for a higher
  score is visible in the audit trail (multi-eval with zero content change).
  Change the artifact or accept the score.
- Pad receipts. `orgx_submit_receipt` with a `quality` receipt should carry a
  self-assessed score you can defend layer by layer, plus at least one
  verifiable URL in evidence.

## Wiring It Into the Loop

- Before writing: check the type code you'll produce and skim its layer stack.
- On attach: `orgx_attach` (or `orgx_act action=complete_with_proof`) with
  `artifact_type`, `business_outcome`, `owner`, `verification`.
- On completion: `orgx_submit_receipt receipt_type=proof|quality|outcome` with
  evidence URLs; `verification_status` reflecting what actually ran.
- On rework: respond to `metadata.rework_feedback`, then resubmit through the
  same attach path so lineage links the versions.
