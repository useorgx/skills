# Public Product Theater

Use this contract for OrgX homepages, launch pages, pricing pages, and any
public surface that embeds product UI in atmospheric imagery.

The aim is not to decorate marketing copy with dashboard screenshots. It is to
let a buyer **feel the product while preserving product truth**. Borrow the
principle from the best product-led pages, not their visual skin: the interface
must remain recognizably OrgX and the evidence must stay honest.

## Product-truth gate

Before drawing a product scene, name its canonical route, component, state
owner, and product noun. Prefer this order:

1. Reuse the real production component when its dependencies are safe.
2. Render a faithful responsive crop using the real information architecture,
   labels, statuses, and interaction model.
3. Build an illustrative functional demo only for a concept that spans clients
   or surfaces and cannot appear as one application screenshot.

Never invent a unified console and present it as shipped product. An
illustrative demo must say what it is, for example:
`Functional handoff demo · mirrors the shared work record, not client UI.`
Fixture or example data must never read as live telemetry.

The public product sequence should map to the real OrgX value loop. A useful
default is:

`cross-client handoff → Quality Studio → live current slice → proof room → real pricing boundary`

Change the sequence when the buyer question demands it, but do not replace the
whole product with repeated verifier consoles.

When a scene represents live work, preserve the canonical orientation chain:
initiative → workstream → milestone → task. Use real entity names, glyphs, and
interaction ownership from the application. Do not expose the internal acronym
`IWMT` as marketing language. Carry the scope chain into artifacts and proof
only when the underlying projection supplies it; never infer lineage for a
cleaner composition.

## Image and interface composition

Atmospheric imagery establishes the world around the work. The interface
proves the product exists. Each must have a distinct job.

- The product surface carries the legible decision, action, state, and proof.
- The image carries context, tension, scale, or emotional elevation.
- Keep functional product UI in the DOM. Do not flatten controls, state, or
  evidence into a generated image and present the result as interactive UI.
- The image never reduces product contrast or competes with the primary action.
- Use a localized edge, mask, or material transition to embed UI in the scene;
  avoid global glass blur and glossy floating-card stacks.
- Preserve meaningful image anchors at every breakpoint instead of using a
  generic center crop.
- Vary the page grammar. Alternate atmospheric theater, flat handoff strip,
  live process surface, dark public-proof document with a light print mode, and decisive pricing
  readout. Four copies of `caption + landscape + dark console` are one idea,
  not a full page.
- Keep one dominant visual per section. Supporting art should become quiet
  when the product surface needs attention.

When new atmospheric artwork is authorized and generation is available, use
GPT Image 2 as the default OrgX image generator. Treat its output as source
material, not product evidence: avoid embedded words, logos, charts, UI chrome,
or claims; record the prompt and generated asset provenance; and inspect the
meaningful anchor at 1440, 768, and 375px before acceptance. Generated imagery
must survive responsive cropping without forcing the product UI into a fixed
height.

## Page measure

Every block on a public page, including theaters and CTA strips that are
direct children of `<main>`, uses the shared measure
(`width: min(var(--hv3-max), calc(100% - clamp(32px, 6vw, 48px)))` with auto
inline margins). The hero shares that measure so the H1 and every section
heading start on one left edge; fixed rails hang a constant distance outside
it. A rounded panel that touches the viewport edge is a measure bug.

Label/value readouts inside scenes use `auto minmax(0, 1fr)` columns so a long
value wraps instead of collapsing its label. Headline promises use
`text-wrap: pretty`; `balance` splits short sentences mid-phrase.

## Color contract

Color is semantic across public and authenticated surfaces:

- **Lime = execution and primary action.** Navigation, hero, plan, and final
  conversion actions use the same lime treatment.
- **Teal = health, verification, and proof.** Use it for verified receipts and
  evidence, not every button.
- **Amber = attention and human judgment.** Decisions, approvals, blockers,
  and unresolved consequences use amber.
- **Iris = creation and quality configuration.** Quality Studio, reference
  selection, and authored standards may use iris.

Tier identity, status, and primary action are different jobs. A selected tier
may carry its identity color on an edge or rail; the action still uses lime.
Never recolor the shell-wide primary token merely to fix one CTA.

## Pricing completeness

Pricing is a product boundary, not a decorative end card.

- Derive plan names, amounts, features, billing cycles, and entitlements from
  canonical product sources.
- Show every current self-serve tier, including Enterprise when a live purchase
  path exists. Label genuinely sales-led or custom tiers as such.
- Keep managed installations or founding deployments visibly separate from
  software subscriptions, with their real price, scope, timing, and route.
- Prefer one selected plan readout with a tier rail over four equal pricing
  cards.
- Do not surface unpublished, channel-specific, stale, or experimental offers
  on the public homepage.
- Ensure crawler and no-JavaScript content exposes the same current buying
  paths as the rendered page.

## Responsive scene contract

Product theater must be content-sized. Fixed scene heights and one-pixel
breakpoint cliffs are release blockers.

- Verify 375, 768, 1024, and 1440 widths. Capture both sides of every breakpoint
  that changes composition and compare page height, overflow, and first-product
  position so a one-pixel cliff cannot hide.
- Use a stacked flow through tablet and a compact two-column composition only
  when the caption, gap, and real product surface fit without overlap.
- Let embedded UI determine scene height. Do not add empty fields to clear an
  absolutely positioned card.
- Preserve at least 44px for every interactive target, including decorative
  signal-strip buttons and compact tabs.
- Keep mobile art bands intentional and short enough that product content
  enters the viewport quickly; never crop away the meaningful image anchor.
- Require zero horizontal overflow, readable type, reachable tabs, visible
  focus, and reduced-motion behavior.
- A long mobile page is acceptable when each screen advances the buyer's
  understanding. Empty art fields, repeated captions, and duplicated proof are
  not.

## Verification receipt

A public product-theater change is not verified until the receipt includes:

- rendered desktop, tablet, and phone captures;
- the canonical route or component represented by every embedded surface;
- interaction checks for tabs, selection, focus, and disclosure;
- exact action-color comparison across navigation, hero, pricing, and final
  CTA;
- touch-target and horizontal-overflow measurements;
- a two-sided height comparison for every composition-changing breakpoint;
- an explicit label for every illustrative or fixture-backed state;
- a clear separation between local render, deployed behavior, and business
  outcome proof.
