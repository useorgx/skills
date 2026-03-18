# Worked Example: Accessibility Audit — Checkout Flow

This is a complete, worked example of a WCAG AA accessibility audit produced by the OrgX Design Agent. It demonstrates the expected depth, specificity, and structure for production audits.

## Context

- **Product**: OrgX SaaS platform
- **Scope**: Checkout flow from cart review through order confirmation (4 screens)
- **WCAG Target**: AA
- **Platform**: Web (desktop and mobile responsive)
- **Tech Stack**: Next.js 14, Tailwind CSS, Radix UI primitives
- **Context Signal**: Scaling (5-20 engineers, design system in progress)

## Artifact

```json
{
  "scope": "Checkout flow: cart review, shipping address form, payment entry, order confirmation",
  "wcag_level": "AA",
  "assumptions": [
    {
      "assumption": "Color palette is the current production palette as of 2026-03-18",
      "confidence": "high"
    },
    {
      "assumption": "Radix Dialog is used for the address selection overlay",
      "confidence": "medium"
    }
  ],
  "summary": {
    "total_issues": 11,
    "critical_count": 3,
    "major_count": 5,
    "minor_count": 3,
    "top_finding": "Payment form is not keyboard-navigable — blocks task completion for keyboard-only users"
  },
  "issues": [
    {
      "id": "A-001",
      "severity": "critical",
      "wcag_criterion": "2.1.1 Keyboard",
      "wcag_level": "A",
      "location": "Payment form — credit card number, expiry, and CVV fields",
      "description": "Custom card input fields built with div elements are not focusable via keyboard. Tab key skips from the shipping summary directly to the Submit button, bypassing all payment fields.",
      "impact": "Keyboard-only users and screen reader users cannot enter payment information. Complete task blocker.",
      "remediation": "Replace custom div-based inputs with native <input> elements or add tabindex='0', role='textbox', and aria-label to each field. Ensure the payment iframe (if using Stripe Elements) has a title attribute and is in the tab order. Specific fix:\n\n```html\n<input\n  type=\"text\"\n  inputmode=\"numeric\"\n  pattern=\"[0-9 ]*\"\n  aria-label=\"Credit card number\"\n  autocomplete=\"cc-number\"\n/>\n```",
      "effort": "medium"
    },
    {
      "id": "A-002",
      "severity": "critical",
      "wcag_criterion": "1.3.1 Info and Relationships",
      "wcag_level": "A",
      "location": "Shipping address form",
      "description": "Form fields lack associated <label> elements. Placeholder text is used as the only label, which disappears on focus and is not announced by screen readers as the field purpose.",
      "impact": "Screen reader users cannot determine what each field requires. Cognitive disability users lose context when placeholder disappears.",
      "remediation": "Add visible <label> elements associated with each input via the for/id pattern. Keep placeholder as supplementary hint, not the primary label.\n\n```html\n<div class=\"field-group\">\n  <label for=\"shipping-street\" class=\"text-sm font-medium text-gray-700\">\n    Street address\n  </label>\n  <input\n    id=\"shipping-street\"\n    type=\"text\"\n    placeholder=\"123 Main St\"\n    autocomplete=\"street-address\"\n  />\n</div>\n```",
      "effort": "low"
    },
    {
      "id": "A-003",
      "severity": "critical",
      "wcag_criterion": "4.1.3 Status Messages",
      "wcag_level": "AA",
      "location": "Cart review — item removal and quantity update",
      "description": "When a user removes an item or changes quantity, the cart total updates visually but no announcement is made to assistive technology. The success/error toast notifications are not in a live region.",
      "impact": "Screen reader users do not know their action succeeded. They may repeat the action or believe the cart is unchanged.",
      "remediation": "Wrap the cart total in an aria-live='polite' region. Add role='status' to toast notifications.\n\n```html\n<div aria-live=\"polite\" aria-atomic=\"true\">\n  <span class=\"cart-total\">Total: $149.99</span>\n</div>\n\n<div role=\"status\" aria-live=\"polite\" class=\"toast\">\n  Item removed from cart\n</div>\n```",
      "effort": "low"
    },
    {
      "id": "A-004",
      "severity": "major",
      "wcag_criterion": "2.4.7 Focus Visible",
      "wcag_level": "AA",
      "location": "All interactive elements across the checkout flow",
      "description": "The global CSS includes outline: none on focus for all elements. The custom focus style (a subtle box-shadow) has insufficient contrast against the white background — measured at 1.8:1, below the 3:1 minimum.",
      "impact": "Keyboard users cannot reliably see which element is focused, causing navigation confusion and potential errors.",
      "remediation": "Remove the blanket outline: none. Replace with a visible focus ring that meets 3:1 contrast.\n\n```css\n:focus-visible {\n  outline: 2px solid #0057B8;\n  outline-offset: 2px;\n}\n```\n\nThis provides a blue ring (#0057B8 on #FFFFFF) at 4.5:1 contrast ratio.",
      "effort": "low"
    },
    {
      "id": "A-005",
      "severity": "major",
      "wcag_criterion": "3.3.1 Error Identification",
      "wcag_level": "A",
      "location": "Shipping address form and payment form — validation errors",
      "description": "Error messages appear as red text below fields but disappear after 3 seconds on a timer. The error text color (#EF4444 on #FFFFFF) passes contrast (4.6:1), but the disappearance means users who are slow readers or using screen magnification may miss the error.",
      "impact": "Users with cognitive disabilities, low vision using magnification, or slow reading speed cannot process error messages before they vanish.",
      "remediation": "Remove the auto-dismiss timer. Error messages should persist until the user corrects the field. Add aria-describedby linking the input to its error message.\n\n```html\n<input\n  id=\"email\"\n  type=\"email\"\n  aria-invalid=\"true\"\n  aria-describedby=\"email-error\"\n/>\n<span id=\"email-error\" class=\"text-red-500 text-sm\" role=\"alert\">\n  Please enter a valid email address\n</span>\n```",
      "effort": "low"
    },
    {
      "id": "A-006",
      "severity": "major",
      "wcag_criterion": "1.4.3 Contrast (Minimum)",
      "wcag_level": "AA",
      "location": "Cart review — item descriptions and quantity labels",
      "description": "Secondary text uses #9CA3AF (gray-400) on #FFFFFF background, yielding a contrast ratio of 2.9:1. Normal text requires 4.5:1 minimum.",
      "impact": "Low vision users cannot read item descriptions and quantities.",
      "remediation": "Darken the secondary text to at least #6B7280 (gray-500) which achieves 4.6:1, or #4B5563 (gray-600) at 7.0:1 for comfortable reading.\n\n```css\n.text-secondary {\n  color: #6B7280; /* 4.6:1 on white — passes AA */\n}\n```",
      "effort": "low"
    },
    {
      "id": "A-007",
      "severity": "major",
      "wcag_criterion": "2.4.6 Headings and Labels",
      "wcag_level": "AA",
      "location": "All checkout steps",
      "description": "Steps are visually separated by large bold text but these are styled <div> elements, not semantic heading elements. The heading hierarchy jumps from h1 (page title) directly to styled divs with no h2 or h3 structure.",
      "impact": "Screen reader users navigating by headings (a primary navigation strategy) cannot find or skip to checkout steps.",
      "remediation": "Use semantic heading elements with a logical hierarchy.\n\n```html\n<h1>Checkout</h1>\n  <h2>Step 1: Review your cart</h2>\n  <h2>Step 2: Shipping address</h2>\n  <h2>Step 3: Payment</h2>\n```\n\nStyle with Tailwind classes to match the existing visual design.",
      "effort": "low"
    },
    {
      "id": "A-008",
      "severity": "major",
      "wcag_criterion": "2.4.3 Focus Order",
      "wcag_level": "A",
      "location": "Address selection overlay (modal)",
      "description": "When the saved address selection overlay opens, focus remains on the trigger button behind the overlay. Users can tab to elements behind the modal. No focus trap is implemented.",
      "impact": "Keyboard users can interact with hidden content. Screen reader users lose context and may not realize a modal is open.",
      "remediation": "Implement focus trap using the Radix Dialog primitive (which handles this natively) or manually. On open, move focus to the first interactive element inside the modal. On close, return focus to the trigger.\n\n```tsx\nimport * as Dialog from '@radix-ui/react-dialog';\n\n<Dialog.Root>\n  <Dialog.Trigger>Select saved address</Dialog.Trigger>\n  <Dialog.Portal>\n    <Dialog.Overlay className=\"fixed inset-0 bg-black/50\" />\n    <Dialog.Content className=\"fixed top-1/2 left-1/2 ...\">\n      <Dialog.Title>Choose an address</Dialog.Title>\n      {/* Focus automatically trapped by Radix */}\n    </Dialog.Content>\n  </Dialog.Portal>\n</Dialog.Root>\n```",
      "effort": "medium"
    },
    {
      "id": "A-009",
      "severity": "minor",
      "wcag_criterion": "1.4.11 Non-text Contrast",
      "wcag_level": "AA",
      "location": "Step progress indicator at the top of the checkout flow",
      "description": "The progress steps use a light gray circle (#D1D5DB) for incomplete steps on a white background. The contrast ratio is 1.8:1, below the 3:1 minimum for graphical objects.",
      "impact": "Low vision users cannot distinguish completed from incomplete steps.",
      "remediation": "Darken incomplete step indicators to #9CA3AF (3.5:1 on white) or add a border/stroke.\n\n```css\n.step-incomplete {\n  background-color: #9CA3AF; /* 3.5:1 on white */\n}\n.step-complete {\n  background-color: #0057B8; /* 4.5:1 on white */\n}\n```",
      "effort": "low"
    },
    {
      "id": "A-010",
      "severity": "minor",
      "wcag_criterion": "2.4.4 Link Purpose (In Context)",
      "wcag_level": "A",
      "location": "Cart review — product item cards",
      "description": "Each cart item has a 'View' link. When multiple items are present, screen readers announce 'View link, View link, View link' with no distinguishing context.",
      "impact": "Screen reader users cannot differentiate which product each 'View' link refers to without reading the surrounding content.",
      "remediation": "Add aria-label with the product name, or use visually hidden text.\n\n```html\n<a href=\"/product/widget-pro\" aria-label=\"View Widget Pro details\">\n  View\n</a>\n```\n\nAlternatively, use aria-describedby pointing to the product name element.",
      "effort": "low"
    },
    {
      "id": "A-011",
      "severity": "minor",
      "wcag_criterion": "2.5.8 Target Size (Minimum)",
      "wcag_level": "AA",
      "location": "Cart review — quantity increment/decrement buttons",
      "description": "The +/- buttons for quantity adjustment are 24x24px, below the 24x24px WCAG 2.5.8 minimum (which allows 24px only if spacing from other targets is sufficient). These buttons are adjacent with only 4px gap, making the effective target area problematic on touch devices.",
      "impact": "Touch device users may hit the wrong button when adjusting quantities.",
      "remediation": "Increase button size to 44x44px (recommended) or 32x32px minimum with 8px spacing.\n\n```css\n.qty-button {\n  width: 44px;\n  height: 44px;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n}\n```",
      "effort": "low"
    }
  ],
  "testing_notes": {
    "screen_readers_tested": [
      "VoiceOver on macOS Sonoma with Safari 17",
      "NVDA 2024.1 with Chrome 120 on Windows 11"
    ],
    "browsers_tested": [
      "Chrome 120 (macOS, Windows)",
      "Safari 17 (macOS)",
      "Firefox 121 (macOS)",
      "Edge 120 (Windows)"
    ],
    "tools_used": [
      "axe-core 4.8 (browser extension)",
      "Lighthouse accessibility audit",
      "WAVE Web Accessibility Evaluation Tool",
      "manual keyboard-only navigation test"
    ],
    "methodology": "Automated scan with axe-core and Lighthouse on all 4 checkout screens, followed by manual keyboard navigation through the complete flow, then screen reader testing of the full happy path and two error paths (invalid address, declined payment)."
  },
  "recommendations": [
    "Fix critical payment form keyboard access (A-001) immediately — this blocks all keyboard and screen reader users from completing checkout",
    "Add visible labels to all form fields (A-002) and make error messages persistent (A-005) — these are low-effort, high-impact fixes",
    "Implement focus management: visible focus rings (A-004), focus trap in address modal (A-008), and focus restoration on modal close",
    "Add aria-live regions for cart total updates (A-003) and toast notifications to support screen reader users",
    "Establish a heading hierarchy across all checkout steps (A-007) to enable screen reader navigation",
    "Increase touch target sizes for quantity buttons (A-011) and review all interactive elements against the 44px minimum"
  ],
  "pass_criteria": "Zero critical issues remaining. Zero major issues remaining. All automated axe-core and Lighthouse scans return zero violations. Manual keyboard navigation completes the full checkout flow without traps or skipped fields.",
  "estimated_remediation_effort": {
    "critical_fixes": "2-3 engineering days",
    "major_fixes": "2-3 engineering days",
    "minor_fixes": "1 engineering day",
    "total": "5-7 engineering days",
    "recommended_approach": "Address critical issues in Sprint N, major issues in Sprint N+1, minor issues as tech debt"
  }
}
```

## Summary

- **11 issues found**: 3 critical (task blockers), 5 major (significant barriers), 3 minor (friction)
- **Top blocker**: Payment form fields are not keyboard-accessible, preventing checkout completion for keyboard and screen reader users
- **Lowest-hanging fruit**: Adding visible labels (A-002), persistent errors (A-005), and focus rings (A-004) are all low-effort, high-impact
- **Estimated fix effort**: 5-7 engineering days total
- **Highest-risk area**: Payment form needs the most attention (keyboard access + label association)

## Next Steps

1. **Engineering Agent**: Implement A-001 (payment keyboard access) and A-004 (focus rings) as P0 hotfix in current sprint
2. **Product Agent**: Add acceptance criteria to all checkout-related stories requiring axe-core zero violations before merge
3. **Design Agent**: Schedule a follow-up audit after remediation to verify pass criteria are met and no regressions introduced
