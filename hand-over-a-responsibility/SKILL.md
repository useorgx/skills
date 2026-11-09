---
name: Hand Over a Responsibility
version: "1.0.0"
description: |
  Set up an ongoing responsibility in OrgX for a person (for example, "keep
  qualified sales conversations coming"), as an operating agreement they can
  read in one screen: outcome, measure, owner, how the work runs, what stays
  theirs to decide, and what OrgX cannot do yet. Ships one worked path, sales
  follow-ups, that stays drafts only until the person says otherwise.
---

# Hand Over a Responsibility

A responsibility is work someone hands over, not a project with an end: it
has an outcome, a way to tell it is working, an owner, and a few points where
the person decides. OrgX stores it as an operating process and shows it as an
operating agreement. Nothing here sends, books or spends on the person's
behalf.

## 1. Read what is already there

Call `mcp__orgx__orgx_get_workspace_context`. Read three parts of it:

- `responsibilities`: what is already handed over. Do not set up a second
  copy; extend the one that exists.
- `capability_report`: per system, whether it is connected, what agents may
  do with it without asking, and whether work can continue unattended. Its
  `next_unlock` says the one thing that would let more run without the person.
- `quality_bars`: the bars work here is checked against.

## 2. Do the work first, then ask only what changes it

Draft the agreement from what the person already said. Ask only for a clause
the server reports missing that changes the work:

- the measure (what result counts, and where OrgX reads it), and
- the accountable owner.

Do not ask about anything you can read from the workspace.

## 3. Propose it inside a plan

Start a plan with `mcp__orgx__orgx_start_plan`, write the plan, and pass the
responsibility with each `mcp__orgx__orgx_save_plan`. The save returns
`responsibility_preview`: the agreement as the person will read it, plus the
questions still open (`status` is `ready` or `needs_answers`). Show the person
the agreement, not the JSON.

When the person agrees, finish with `mcp__orgx__orgx_complete_plan` carrying
the same responsibility. OrgX records it as confirmed. It is not active, and
activation does not yet run work on a schedule by itself; say so.

## 4. Do the work and record it against the responsibility

Each time work is done under it, submit a receipt with
`mcp__orgx__orgx_submit_work_receipt` whose receipt carries the extension
`org.orgx.responsibility/v1`: the responsibility id, the rules it followed
(`claimId@version` from the brief), and one line per effect outside OrgX
(`none`, `draft`, `sent`, `changed`, `deleted`, with a target and whether it
can be undone). OrgX records it against the responsibility, so the next agent
sees it as done.

## 5. Pick up where the last agent left off

Read one responsibility's brief from `mcp__orgx__orgx_get_workspace_context`
by naming it, optionally with a time to see only what changed since then. The
brief says the next action, who it waits on and why, the dated history, the
rules in force (and whether each came from the person, a decision, or was
learned), and what OrgX cannot do for it yet.

## Worked path: sales follow-ups, drafts only

The responsibility:

```json
{
  "name": "Qualified sales conversations",
  "kind": "maintain",
  "outcome": "Every warm lead gets a useful reply within one working day",
  "measure": "Share of new leads with a drafted reply inside 24 hours, read from the CRM",
  "trigger": { "kind": "event", "event": "a new lead or reply arrives" },
  "stages": [
    { "name": "Read the lead and its history", "authority": "observe" },
    { "name": "Draft the reply and next step", "authority": "prepare" },
    { "name": "Send", "authority": "gated" }
  ],
  "limitations": ["Drafts only: nothing is sent until the person approves each one."]
}
```

How it runs:

1. Read the lead and every earlier message with it before drafting.
2. Draft in the person's voice. Name one concrete next step (a time, a
   question, a link they asked for). No invented numbers, customers or
   claims; if a fact is missing, leave a marked gap for the person.
3. Leave the draft where the person sends from (their mail or CRM drafts),
   never send it.
4. Submit a receipt with one `draft` effect per reply, `reversible: true`.
5. When the person sends, edits, or throws a draft away, that is the signal
   the rules learn from. Do not argue with an edit; record it.

Turning on sending is the person's decision, made per responsibility. Until
they make it, the `Send` stage stays gated and the brief shows it as theirs.

## Do not

- Do not send, schedule, book or pay on the person's behalf in this skill.
- Do not approve, reject or settle a decision for the person.
- Do not mark a responsibility ready while its measure or owner is missing.
