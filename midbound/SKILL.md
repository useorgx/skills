---
name: midbound
version: "0.1.0"
description: |
  The midbound motion — acting on observed, timestamped, public intent from people
  inside the ICP. Not inbound (they came to you), not outbound (you hit a bought list).
  Use to book demos from engagement under competitor and creator content, to build a
  creator/competitor map of a category, or to stand up a real-time keyword watcher.
  Requires the gtm-agentic-engineer reasoning layer.
---

# Midbound

> Run [gtm-agentic-engineer](../gtm-agentic-engineer) first. It supplies the capability
> resolution protocol, the three memories, and the gates this motion depends on. This
> file is the motion; that file is why it works and how it fails.

## What midbound is

**Inbound**: they find you. High intent, low volume, no control over timing.
**Outbound**: you hit a list. High volume, low intent, timing unrelated to the buyer.
**Midbound**: you act on intent the buyer **published themselves, publicly, recently.**

The asset is not the contact. Anyone can buy the contact. The asset is **the sentence
they wrote** — a specific frustration, in their words, timestamped — plus the fact that
you are reaching them while it is still true.

This is why midbound survives the collapse of cold outbound. The reply rate does not
come from better copy; it comes from arriving during a window the buyer opened.

## Required capability classes

Resolve every one before running. Declare any that are missing and the resulting
degradation — see the resolution protocol in the reasoning layer.

| Step | Class | Blocking? |
|---|---|---|
| 1. Map the category | `SIGNAL_DISCOVERY` | Yes |
| 2. Rank by performance | `SIGNAL_DISCOVERY` (metrics) | No — degrades to unranked |
| 3. Cluster and graph | `SOCIAL_GRAPH` | No — model can infer weakly from 1+2 |
| 4. Harvest engagement | `ENGAGEMENT_GRAPH` | **Yes — no substitute in the OrgX stack today** |
| 5. Enrich to a person | `IDENTITY_RESOLUTION`, `FIRMOGRAPHIC` | Yes |
| 6. Classify | `ICP_CLASSIFY` | Yes |
| 7. Write | `COPY_GENERATION` | Yes |
| 8. Send | `SEQUENCE_DISPATCH` | Yes |
| 9. Learn | `OUTCOME_FEEDBACK` | No — but without it the motion cannot improve |

**Step 4 is the load-bearing one and it is the one OrgX cannot currently do.** Ahrefs
returns posts, authors, and post-level metrics; it does not return who commented.
Without a provider for `ENGAGEMENT_GRAPH`, steps 1–3 still produce a genuinely useful
creator map (reusable for influencer work), but the personalized-list motion does not
run. Say that rather than substituting a follower scrape and calling it the same thing.

---

## Phase 1 — Map the category

Build the account map: competitors' founders, plus every creator posting into the
category, plus anything that outperformed in the window.

Go **beyond the named competitors.** The instruction that makes this work is asking for
accounts niched to the category that are *performing*, not accounts you already know.
The known list is the seed, not the answer.

Output per account: handle, niche classification (what they actually post about, not
their bio), engagement per post, posting cadence, and cluster membership. Make
engagement a filter, not a footnote — the map is only useful if it can be sorted by who
actually reaches the ICP.

**This artifact has a second life.** The same map is the influencer-marketing target
list and the competitive-content baseline. Attach it once, reuse it; do not rebuild it
per campaign. Refresh on a cadence, since cluster structure moves slowly and engagement
moves fast.

## Phase 2 — Harvest engagement into a personalized list

Take every comment under every mapped account's posts inside the window. The window is
part of the motion's definition, not a tunable — signal decay is steep, and 24 hours is
the default for a reason.

For each commenter:

1. Capture **the comment verbatim**, with the post it sat under and its timestamp.
   Verbatim matters: the comment is the personalization asset, and a paraphrase of it
   is worth roughly nothing.
2. Categorize by pain and relevance. The highest-value shape is a stated failed
   attempt — *"I tried X before and it didn't work well"* — because it names the pain,
   the alternative, and the dissatisfaction in one line.
3. Enrich to a person and company. Resolve email only for those inside the ICP;
   enriching everyone burns credits on people you will not contact.
4. Classify against the ICP predicate, and record the confidence and the predicate
   version used.

Write everything to the campaign ledger **as you go**, not at the end. These runs
partially fail; a ledger written only on success is a ledger that does not exist.

## Phase 3 — Write from their words

The copy is built from the captured comment, not from a template with a merge field.

- Open on the specific thing they said, in their language.
- Connect it to the outcome they were reaching for, not to your feature list.
- Keep the ask small and reversible.
- Resolve voice from **the workspace's** spec. Never the vendor's, never another
  tenant's.

Stay inside the personalization band: reference what they **published deliberately**.
The comment qualifies. Their inferred job change, their company's funding event, or
anything assembled from behavioral traces does not — it crosses the cliff and converts
negative even when accurate.

## Phase 4 — Dispatch

Push to sequences through the resolved `SEQUENCE_DISPATCH` provider.

**Before any send:** check the campaign ledger, check the CRM for open opportunities,
and confirm the human dispatch gate for a first run, a volume step-change, or a new
domain. Deliverability does not reset — it is the one resource an agent can permanently
destroy while reporting success.

Record per contact: variant, send time, signal that sourced them, and ICP predicate
version. Without that, a reply rate is a number with no attribution and teaches nothing.

## Phase 5 — Watch

The standing version of this motion. A watcher fires when someone posts about a
keyword or topic, filtered to the ICP, and routes it to a human or an agent to **engage
publicly** — comment, reply, be visible — rather than to send.

This is the highest-conversion and lowest-cost surface in the whole motion, because a
useful public reply during the window costs nothing, is not deliverability-bound, and
is seen by everyone else reading the thread. Treat it as the default and treat email as
the escalation.

Without a native watcher, approximate it: poll `SIGNAL_DISCOVERY` on a short cadence
against a keyword set, diff against the campaign ledger, and notify. Polling is worse
than a push watcher and the gap should be recorded rather than hidden — a slower loop
means arriving later in a window where lateness is the whole cost.

---

## Hypothesis ledger

Record before the run, compare after:

- Segment, angle, and signal type
- Predicted reply rate, and what result would falsify the approach
- Capability binding actually used

A midbound run with `ENGAGEMENT_GRAPH` and one without are **different motions** and
must not be compared as though they were the same. Attribution to the stack is part of
the result.

## Failure modes

| Failure | What it looks like | Guard |
|---|---|---|
| Stale signal | Referencing a comment from last month | Enforce the window; decay is steep |
| Cliff crossing | Citing inferred data they never published | Only reference deliberate public output |
| Double touch | Two runs, same person, no shared state | Campaign ledger checked before dispatch |
| Silent degradation | Running without `ENGAGEMENT_GRAPH` and calling it midbound | Resolution gate; declare degradation |
| Domain burn | Volume raised because reply count looked good | Human dispatch gate on any step-change |
| Uncompounding | Every run starts from zero | Outcome receipts on market response, not artifact quality |

## Provenance

The motion is Cody Schneider's, described publicly and run by his team since their YC
batch, in a more targeted form. Their reference stack is Crustdata for discovery,
engagement, and watching, with Instantly for dispatch. This file abstracts that to
capability classes so the same reasoning runs on a different stack — and marks honestly
where the OrgX stack currently cannot reach.
