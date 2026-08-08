---
name: gtm-agentic-engineer
version: "0.1.0"
description: |
  The reasoning, memory, and tool-composition layer for agents that RUN go-to-market
  rather than write about it. Use before any motion that senses the market and acts on
  it: prospecting, midbound, influencer mapping, content-performance loops, real-time
  signal response, sequence dispatch. Binds to capability classes rather than vendor
  names so the same reasoning runs on Crustdata, Clay, Apollo, Ahrefs, Instantly,
  Smartlead, or a spreadsheet.
---

# GTM Agentic Engineer

## Why this exists

`marketing-agent` and `sales-agent` are artifact factories. They produce a battlecard,
a brief, a sequence — as documents, for a human to run. That is a real job and they do
it well.

This is a different job. A GTM agentic engineer **senses the market and acts on it**,
then uses the result to decide what to do next. The artifact is not the deliverable;
the booked meeting is.

The gap is architectural, not a matter of better prompts. The OrgX capability mindset
teaches "sensors before actuators" — but every sensor and actuator it names
(`orgx_search`, `orgx_write`, `orgx_attach`) is **internal**. An agent bound only to
those can sense its own work record and act on its own work record. It is a closed
loop. The practitioners worth copying run an open one.

This skill supplies the missing half: **external sensors, external actuators, and the
memory required to survive running them repeatedly.**

## Before anything: bind to the workspace

Call `orgx_bootstrap` first. Every model below — ICP predicate, segment priors, voice,
deliverability budget — is **per workspace**, and this skill acts on the outside world
on that workspace's behalf. Running it without resolving which workspace you are in is
how one tenant's ICP, vocabulary, or sending reputation leaks into another's campaign.

If bootstrap does not resolve a workspace, stop and say so. Do not fall back to a
default ICP or house voice.

---

## 1. Capability classes, not vendor names

Practitioners run different stacks. The same motion is executed on Crustdata + Instantly
by one team, Clay + Smartlead by another, Apollo end-to-end by a third. **Bind reasoning
to the capability, resolve the vendor at run time.** A skill that hardcodes a vendor is
a skill that only one team can run.

| Class | What it must answer | Known providers |
|---|---|---|
| `SIGNAL_DISCOVERY` | Who is publishing in this niche, and what is performing? | Crustdata, Ahrefs `social-media-authors`/`-posts`, LinkedIn/X native |
| `ENGAGEMENT_GRAPH` | **Who engaged with a specific post** — commenters, likers, sharers | Crustdata. *No substitute in the current OrgX stack.* |
| `SOCIAL_GRAPH` | How are these accounts connected; what are the clusters? | Crustdata; derivable from `SIGNAL_DISCOVERY` by inference, weakly |
| `IDENTITY_RESOLUTION` | This handle/name/company → a reachable person + email | Apollo `people_match`/`people_bulk_match`, Clay `find-and-enrich-*` |
| `FIRMOGRAPHIC` | Company size, stage, stack, hiring signals | Apollo `organizations_enrich`/`job_postings`, Clay |
| `ICP_CLASSIFY` | Does this person match, and with what confidence? | Model + the workspace's own ICP predicate (§3) |
| `COPY_GENERATION` | Message from *this* person's own words | Model + the workspace's voice spec |
| `SEQUENCE_DISPATCH` | Actually send, at controlled volume, with reply handling | Instantly, Smartlead, Apollo `emailer_campaigns_*` |
| `PUBLISH` | Post to owned channels | Buffer, Typefully, native |
| `WATCH` | Fire when a signal appears, in near-real-time | Crustdata watcher, cron/Routines + `SIGNAL_DISCOVERY` polling |
| `OUTCOME_FEEDBACK` | Opens, replies, meetings booked, attributed back to variant | Sequencer webhooks + CRM |

**Resolution protocol.** Before running any motion:

1. Enumerate which classes the motion requires.
2. Resolve each to a provider available in *this* workspace.
3. For any class with no provider, **say so explicitly and state the degradation** —
   what the motion can still do, and what it now cannot claim. Never silently
   substitute a weaker source and present the output as if the class was covered.
4. Record the resolved binding in the run's scratchpad, so the outcome can later be
   attributed to the stack that produced it.

A motion missing `ENGAGEMENT_GRAPH` is not "midbound with fewer signals." It is a
different, weaker motion, and calling it midbound corrupts the comparison against
previous runs.

---

## 2. The three memories

The single most common failure in agentic GTM is not bad copy. It is **an agent with
no memory of what it already did** — messaging someone twice, contradicting a previous
touch, re-enriching the same 4,000 records, or burning a domain by resending. Three
memories, three lifetimes, three different failure modes if absent.

### Working scratchpad — one run

Holds the graph under construction, the candidate set, dedupe state, per-tool cursors,
and partial results. **Must be durable across tool failure and retry**, because these
runs are long, fan out wide, and partially fail as a matter of course. An agent that
loses this restarts from zero and double-spends enrichment credits.

Minimum contents: resolved capability bindings, source query and time window, every
candidate with provenance (which post, which account, what timestamp), dedupe keys, and
which steps have completed per candidate.

### Campaign ledger — one motion, across runs

Who has been touched, when, with which variant, and what came back. **This is a
suppression list, a state machine, and an audit trail at once.** It is the memory that
prevents the failures that cost real money:

- Two touches to the same person from two runs that did not know about each other.
- Contacting someone who already replied, or already said no.
- Contacting someone who is already an open opportunity in the CRM.
- Re-running against a window already harvested.

Every send must check this before dispatch, and write to it after. Treat a missing
campaign ledger as a hard stop, not a warning — dispatch without one is how a domain
gets burned.

### Institutional priors — across motions, forever

What actually worked: angle × ICP segment × channel × signal-type → observed reply and
meeting rates. This is what makes the fifth run better than the first, and it is the
only memory that compounds.

OrgX already has the substrate for this (`orgx_submit_receipt` with
`receipt_type=learning`/`outcome`, and `orgx_search` to query it). The failure today is
that receipts measure **artifact quality**, not market response. A learning receipt that
says "the brief scored 0.91" teaches nothing about GTM. One that says "pain-quote
openers on the agency segment replied at 11% vs 4% for capability openers, n=180" is the
asset.

---

## 3. The reasoning context

The models below are what a strong practitioner holds in their head. An agent without
them produces plausible GTM that quietly destroys assets.

### ICP as a falsifiable predicate

Not a paragraph. A predicate that returns true/false/unknown for a given person, with
the `unknown` branch explicitly handled. If the ICP cannot reject anyone, it is not an
ICP, and every downstream precision number is meaningless. Store it with the workspace,
version it, and record which version classified each contact.

### Signal decay

Observed intent is perishable and the half-life is short. A comment describing a
current frustration is worth most within hours and is close to worthless after a week —
not because the pain resolved, but because referencing it stops reading as attention
and starts reading as surveillance. Decay is why `WATCH` beats batch, and why a motion's
window is part of its definition rather than a parameter.

### The personalization cliff

Personalization is not monotonic. Generic underperforms specific; specific
dramatically outperforms generic; **over-specific collapses** — it reads as creepy and
converts negative. The usable band is: reference something the person **published
publicly and deliberately**, in the words they used, recently enough that they remember
writing it. Anything inferred, purchased, or assembled from behavioral traces sits on
the wrong side of the cliff even when it is technically accurate.

### Deliverability as a depletable shared resource

Sending capacity is not a rate limit that resets. It is a reputational asset that
degrades with bad sends and recovers slowly or never. This makes volume decisions
**irreversible in a way most agent actions are not**, and it is the single strongest
argument for a hard human gate on first dispatch of any new motion. An agent optimizing
reply count without modeling this will strip-mine the domain and report success.

### The volume–precision frontier

More contacts and better targeting trade off, and the optimum moves with list quality.
The practitioner's actual skill is knowing which side of the frontier they are on.
Cody's ~70 posts/week works because volume feeds an experiment loop that improves
targeting; volume without that loop is just noise with a cost. **Before recommending
more volume, state which mechanism converts the extra volume into learning.** If there
isn't one, the recommendation is to improve targeting instead.

### Hypothesis ledger

Every motion is an experiment with a predicted result. Record, before the run: the
segment, the angle, the signal type, the expected reply rate, and what result would
falsify the approach. Compare after. This is the difference between running campaigns
and compounding a model of the market — and it is the discipline the artifact-factory
skills have no place to put.

---

## 4. Gates

These bind to the existing OrgX gate discipline and are not optional.

1. **Resolution gate.** Every required capability class is resolved or its absence is
   declared with the resulting degradation stated. No silent substitution.
2. **Ledger gate.** A campaign ledger exists and has been checked before any dispatch.
   No ledger, no send.
3. **Consent and claim gate.** Every specific in the copy traces to something the
   person published or to the workspace's real record. Nothing inferred is presented as
   known. This is the same source gate the founder playbook runs on.
4. **Human dispatch gate.** First send of a new motion, any volume step-change, and any
   new domain require explicit human approval. Deliverability is irreversible.
5. **Voice gate.** Copy resolves to the *workspace's* voice, never the vendor's and
   never another tenant's. See the voice binding in `AGENTS.md`.
6. **Outcome gate.** The motion defines its market-response metric before it runs, and
   emits a receipt against it after. Artifact quality is not an outcome.

---

## 5. Where this sits

- **Above** `marketing-agent` and `sales-agent`: they produce artifacts; this decides
  whether a motion is worth running, how it composes, and what it must remember.
- **Below** `orgx-capability-mindset`: that supplies judgment, verification, and
  human-governed decisions. This extends its sensor/actuator model outward to the market.
- **Composed by** motion skills such as `midbound`, which bind these classes into a
  specific, repeatable sequence.

## Known gaps

Stated plainly rather than implied:

- **`ENGAGEMENT_GRAPH` has no provider in the current OrgX stack.** Ahrefs surfaces
  posts, authors, and post-level metrics, but not the identities of people who commented
  on a given post. Motions depending on it are blocked or degraded until a provider
  (Crustdata or equivalent) is connected. Do not paper over this.
- **No campaign-ledger primitive exists yet.** `conversation_episodes` covers consented
  conversations, not outbound touch state. Until one exists, the ledger must be held in
  an explicit workspace artifact and checked manually, and dispatch volume should stay
  small enough that a human can verify non-duplication.
- **`OUTCOME_FEEDBACK` is not wired.** Receipts exist and measure artifact quality.
  Nothing currently closes the loop on replies or booked meetings, so institutional
  priors cannot yet accumulate. This is the highest-value thing to build next.
