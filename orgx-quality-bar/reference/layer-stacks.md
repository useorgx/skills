# Domain Layer Stacks

The dimensions OrgX's layered judge scores per domain. Weights sum to 1.0 per
stack. Layers are scored separately and never averaged — a weak layer stays
visible. Source of truth: `lib/quality/layerStacks.ts` in the OrgX monorepo
(bar version `stack-v1`).

## Sales

| Layer | Weight | Question |
| --- | --- | --- |
| claim_sharpness | 0.25 | Is there ONE promise a specific buyer would repeat back? |
| evidence_density | 0.25 | Are claims carried by verifiable proof, not adjectives? |
| personalization_fit | 0.20 | Would the named ICP feel this was written for them? |
| voice | 0.15 | Founder-plain and specific — zero hype vocabulary? |
| actionability | 0.15 | Exactly one clear, low-friction next step? |

Anchor: one lead claim per piece — competing claims read as none.

## Marketing

| Layer | Weight | Question |
| --- | --- | --- |
| differentiation | 0.25 | Is the against-what explicit — not just "better"? |
| proof_points | 0.25 | Concrete, checkable proof — numbers, names, receipts? |
| category_clarity | 0.20 | Does the reader know what this IS in one pass? |
| voice_brand_fit | 0.15 | Reads like the brand's one voice, not template SaaS? |
| distribution_fitness | 0.15 | Is the format native to where it will actually run? |

## Design

| Layer | Weight | Question |
| --- | --- | --- |
| composition | 0.25 | Framing, negative space, eye-trace — or one layout ×N? |
| information_hierarchy | 0.25 | One anchor; is every fact said once, in one voice? |
| world_coherence | 0.20 | One coherent place/system — or disconnected voids? |
| craft_materiality | 0.15 | Surfaces, type, and motion built — or "dark render" defaults? |
| intent_legibility | 0.15 | Does every element answer "what breaks if removed?" |

Anchors: real text and imagery (no lorem ipsum), alt text on every image,
type-scale discipline (≤6 distinct sizes, ideally 3).

### Override: audits and critiques

`design.audit`, `design.critique`, `design.accessibility_audit`,
`design.dark_mode_audit` are judged as criticism, not visual composition:

| Layer | Weight | Question |
| --- | --- | --- |
| observation_acuity | 0.30 | Do the observations see what matters? |
| evidence_specificity | 0.25 | Is each finding anchored to a concrete, quotable instance? |
| actionability | 0.25 | Can a builder act on each finding without the author? |
| prioritization | 0.20 | Are findings ranked by impact, not listed flat? |

## Engineering

| Layer | Weight | Question |
| --- | --- | --- |
| correctness_risk | 0.30 | Are the failure modes named and risky seams tested? |
| verifiability | 0.25 | Can someone else prove it works — tests, receipts, repro? |
| scope_discipline | 0.15 | Smallest change that fully solves it — no drive-bys? |
| operability | 0.15 | Rollback, flags, monitoring — safe to own at 3am? |
| clarity | 0.15 | Could the next engineer act on this without the author? |

Anchors: file:line references beat prose; no merge-conflict markers; no
credential-shaped strings.

## Product

| Layer | Weight | Question |
| --- | --- | --- |
| problem_grounding | 0.25 | Is the pain real, felt, and quoted — not asserted? |
| decision_quality | 0.25 | Options weighed with real trade-offs and a committed pick? |
| user_evidence | 0.20 | Do real usage data or transcripts carry the argument? |
| measurability | 0.15 | Will we know if this worked — metric, gate, falsifier? |
| scope_sequencing | 0.15 | Is the first slice real value, not scaffolding theater? |

Anchors: decision language ("we chose", "we will not", "instead of");
named metrics ("success = 15% signup rate"), not "we'll measure success".

## Ops

| Layer | Weight | Question |
| --- | --- | --- |
| actionability_under_stress | 0.30 | Usable by a stressed human at 3am — steps, not essays? |
| failure_paths | 0.25 | Does it cover what happens when the step FAILS? |
| ownership_clarity | 0.15 | Who acts, who decides, who is informed — by name? |
| timeliness | 0.15 | Are time bounds explicit — SLAs, escalation clocks? |
| evidence | 0.15 | Are claims backed by logs, queries, receipts? |

Anchors: numbered steps with expected output per step; every step has an
"if this fails" branch; time bounds like "within 5 minutes", not "promptly".

Note: any `*.structured_blocker` artifact from any domain is judged on this
stack.

## Research

| Layer | Weight | Question |
| --- | --- | --- |
| source_quality | 0.25 | Named, primary, verifiable sources — URLs that resolve? |
| synthesis_over_summary | 0.25 | Does it produce a NEW claim the sources don't state alone? |
| falsifiability | 0.20 | Are the claims testable — and is the killing test named? |
| coverage | 0.15 | Were the disconfirming lanes searched, not just friendly ones? |
| actionable_findings | 0.15 | Does it end in decisions someone can execute this week? |

## Orchestration

| Layer | Weight | Question |
| --- | --- | --- |
| dependency_truth | 0.25 | Are the real blocking edges named — not a flat task list? |
| receipt_completeness | 0.25 | Does every claim of done carry its receipt? |
| progress_honesty | 0.20 | Built / wired / running distinguished, unprompted? |
| coordination_clarity | 0.15 | Could a new agent pick this up without the author? |
| next_action_sharpness | 0.15 | Is the single highest-leverage next move stated? |

### Override: plans

`orchestration.next_initiative` and `orchestration.dispatch_plan` are judged
as plans — they have no completed work to receipt yet:

| Layer | Weight | Question |
| --- | --- | --- |
| dependency_truth | 0.25 | Are the real blocking edges named? |
| coordination_clarity | 0.25 | Could a new agent execute this without the author? |
| acceptance_checkability | 0.20 | Is "done" checkable for every workstream? |
| scope_realism | 0.15 | Is the sizing honest — no theater milestones? |
| next_action_sharpness | 0.15 | Is the first move stated and executable now? |

## General (fallback)

Used for provisional / unrecognized types until promoted to a domain stack:

| Layer | Weight | Question |
| --- | --- | --- |
| fitness_to_intent | 0.35 | Does it deliver exactly what the task DoD asked for? |
| evidence | 0.25 | Are claims carried by checkable specifics? |
| clarity | 0.20 | Readable by its real audience in one pass? |
| actionability | 0.20 | Does it end somewhere someone can act from? |
