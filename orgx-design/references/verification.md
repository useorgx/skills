# Verification and Evidence

“Looks correct in code” is not a visual verdict. Verify the rendered experience
and preserve enough evidence for the next audit to start from truth.

## Evidence ladder

Report each layer separately:

1. Source inspected.
2. Focused unit/contract tests passed.
3. Typecheck and relevant lint passed.
4. Local route rendered.
5. Desktop/tablet/phone behavior inspected.
6. Keyboard and state behavior inspected.
7. Commit created.
8. PR checks passed and merged.
9. Deployment live.
10. Real usage or outcome observed.

Never infer a later layer from an earlier one.

## Viewport matrix

Minimum:

| Viewport | Required checks |
| --- | --- |
| 1440px desktop | First-paint hierarchy, max width, density, pointer states, no wasted stage. |
| 768px tablet | Intentional reflow, no clipped rails/tabs, useful touch layout, portrait behavior. |
| 375px phone | No horizontal overflow, 44px targets, readable type, primary action visible, safe keyboard behavior. |

Also inspect 200% zoom and long-content fixtures for surfaces with variable
copy, names, paths, artifacts, or generated text.

## State matrix

Capture or exercise every applicable state:

- cold loading and warm refresh;
- empty/first use;
- populated default;
- long labels/content and large lists;
- degraded, offline, permission, and error;
- urgent/Needs You;
- resolved/complete/idle;
- modal/menu/disclosure open and closed.

An unavailable backend may require deterministic fixtures. Label fixture proof
as fixture proof; it is not production-data proof.

## Interaction checks

- Keyboard order follows visual order.
- Focus is visible, persistent, and restored after closing a transient layer.
- Enter/Space semantics match the native control.
- Escape and Back behave predictably.
- Actions acknowledge within 400ms with pending, success, or error feedback.
- Double activation is prevented.
- Input survives recoverable errors.
- URL state survives reload/share when the selection is meaningful.
- Reduced motion preserves state comprehension.

## Visual critique protocol

Use screenshots or computer/browser inspection:

1. Two-second test — can a new viewer name the page question?
2. Squint test — is one dominant read still clear?
3. Blur test — do urgency and hierarchy remain visible without reading?
4. Silent-state test — is healthy work calm?
5. Stress-state test — does Needs You reshape the surface?
6. Generic SaaS test — remove the logo; is it still recognizably OrgX?
7. Overflow sweep — inspect every edge at each viewport.

## Performance

For changed routes, record cold and warm behavior separately:

- cold compilation/startup;
- first meaningful content;
- loading-to-ready transitions;
- unnecessary polling, duplicate requests, or layout shifts;
- interaction acknowledgement.

Performance findings may be documented separately from visual changes, but they
must not disappear from the registry.

## Durable audit artifact

Update the canonical surface registry with disposition, evidence, exact
viewport/state coverage, and the next unverified gap. Store screenshots or
reports at stable paths and reference them from the registry or PR.
