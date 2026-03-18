# WCAG Quick Reference: Most-Violated Criteria with Fix Patterns

This reference covers the WCAG 2.2 success criteria most frequently violated in web applications, ordered by how often they appear in real-world audits. Each entry includes the criterion, what it requires, the common violation pattern, and a concrete fix.

## How to Use This Reference

During an accessibility audit, check each of these criteria against the target surface. These 20 criteria account for approximately 85% of all WCAG violations found in production web applications. Start here before diving into the full WCAG specification.

Severity mapping used in OrgX audits:
- **Critical**: Task blocker. User cannot complete their goal.
- **Major**: Significant barrier. User can complete the task but with substantial difficulty.
- **Minor**: Friction. User is inconvenienced but can accomplish the task.

---

## Level A Criteria (Minimum Baseline)

### 1.1.1 Non-text Content (Level A)

**Requirement**: All non-text content has a text alternative that serves the equivalent purpose.

**Most common violations**:
- Images missing alt attributes entirely
- Decorative images with descriptive alt text (should be `alt=""`)
- Icon buttons with no accessible name
- Complex charts or graphs with no text summary

**Fix patterns**:

Informative image:
```html
<img src="quarterly-growth.png" alt="Revenue grew 34% from Q1 to Q2 2026" />
```

Decorative image:
```html
<img src="decorative-swoosh.svg" alt="" role="presentation" />
```

Icon button:
```html
<button aria-label="Close dialog">
  <svg aria-hidden="true"><!-- X icon --></svg>
</button>
```

Complex image with long description:
```html
<figure>
  <img src="architecture-diagram.png" alt="System architecture overview" aria-describedby="arch-desc" />
  <figcaption id="arch-desc">
    The system consists of three layers: the client application (React),
    the API gateway (Next.js), and the agent runtime (Node.js workers).
    Data flows from client to gateway via REST, and from gateway to workers via event queue.
  </figcaption>
</figure>
```

### 1.3.1 Info and Relationships (Level A)

**Requirement**: Information, structure, and relationships conveyed through presentation are programmatically determinable.

**Most common violations**:
- Form fields without associated labels
- Visual headings using styled `<div>` or `<span>` instead of `<h1>`-`<h6>`
- Data tables without `<th>` headers
- Lists styled with CSS but not using `<ul>`/`<ol>`/`<li>`
- Required fields indicated only by color (red asterisk without programmatic indication)

**Fix patterns**:

Form field with label:
```html
<label for="initiative-name">Initiative name</label>
<input id="initiative-name" type="text" required aria-required="true" />
```

Required field indicator:
```html
<label for="email">
  Email address <span aria-hidden="true">*</span>
  <span class="sr-only">(required)</span>
</label>
<input id="email" type="email" required aria-required="true" />
```

Data table:
```html
<table>
  <thead>
    <tr>
      <th scope="col">Initiative</th>
      <th scope="col">Status</th>
      <th scope="col">Owner</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Onboarding redesign</td>
      <td>In progress</td>
      <td>Sarah K.</td>
    </tr>
  </tbody>
</table>
```

### 1.3.2 Meaningful Sequence (Level A)

**Requirement**: When the order of content affects its meaning, the correct reading sequence is programmatically determinable.

**Most common violations**:
- CSS flexbox/grid reordering that differs from DOM order
- Content that makes sense visually but reads nonsensically with a screen reader
- Step indicators where the visual order does not match tab order

**Fix pattern**: Ensure DOM order matches visual order. If you must use CSS `order`, verify that a screen reader reads the content in a logical sequence. Test by disabling CSS and confirming the content still makes sense.

### 2.1.1 Keyboard (Level A)

**Requirement**: All functionality is operable through a keyboard interface without requiring specific timings for individual keystrokes.

**Most common violations**:
- Click handlers on `<div>` or `<span>` elements without keyboard event support
- Custom dropdowns that cannot be operated with arrow keys
- Drag-and-drop without a keyboard alternative
- Modal dialogs without focus trap (user tabs into background content)

**Fix patterns**:

Clickable div made keyboard-accessible:
```html
<!-- Bad -->
<div onclick="handleClick()">Click me</div>

<!-- Good -->
<button onclick="handleClick()">Click me</button>

<!-- If you must use a div -->
<div role="button" tabindex="0" onclick="handleClick()" onkeydown="if(event.key==='Enter'||event.key===' ')handleClick()">
  Click me
</div>
```

Focus trap for modal (conceptual):
```javascript
// On modal open:
// 1. Save the previously focused element
// 2. Move focus to first focusable element in modal
// 3. Trap Tab/Shift+Tab within modal
// 4. On close, restore focus to saved element
```

### 2.4.1 Bypass Blocks (Level A)

**Requirement**: A mechanism is available to bypass blocks of content that are repeated on multiple pages.

**Most common violation**: No skip-to-content link at the top of the page.

**Fix pattern**:
```html
<body>
  <a href="#main-content" class="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:bg-white focus:p-4 focus:text-blue-600">
    Skip to main content
  </a>
  <nav><!-- Site navigation --></nav>
  <main id="main-content">
    <!-- Page content -->
  </main>
</body>
```

### 2.4.3 Focus Order (Level A)

**Requirement**: Focusable components receive focus in an order that preserves meaning and operability.

**Most common violations**:
- Positive `tabindex` values (`tabindex="5"`) creating unexpected tab order
- Modals not trapping focus (user can tab behind the modal)
- Dynamically injected content that receives focus before existing content

**Fix pattern**: Never use `tabindex` values greater than 0. Use `tabindex="0"` to add elements to the natural tab order, and `tabindex="-1"` to make elements programmatically focusable but not in the tab order. Ensure DOM order matches intended focus order.

### 2.4.4 Link Purpose (In Context) (Level A)

**Requirement**: The purpose of each link can be determined from the link text alone, or from the link text together with its context.

**Most common violations**:
- Multiple "Read more" or "Click here" links on a page
- Icon-only links with no accessible name
- "View" links in a list where all link text is identical

**Fix patterns**:
```html
<!-- Bad -->
<a href="/initiative/42">Read more</a>

<!-- Good: descriptive link text -->
<a href="/initiative/42">Read more about the onboarding redesign initiative</a>

<!-- Good: visually hidden context -->
<a href="/initiative/42">
  Read more<span class="sr-only"> about the onboarding redesign initiative</span>
</a>

<!-- Good: aria-label -->
<a href="/initiative/42" aria-label="Read more about onboarding redesign">Read more</a>
```

### 3.3.1 Error Identification (Level A)

**Requirement**: If an input error is automatically detected, the item in error is identified and the error is described in text.

**Most common violations**:
- Error indicated only by a red border (no text message)
- Error messages not associated with their fields
- Errors that disappear on a timer before the user can read them

**Fix pattern**:
```html
<label for="email">Email address</label>
<input
  id="email"
  type="email"
  aria-invalid="true"
  aria-describedby="email-error"
/>
<span id="email-error" role="alert" class="text-red-600 text-sm mt-1">
  Please enter a valid email address (e.g., name@example.com)
</span>
```

### 3.3.2 Labels or Instructions (Level A)

**Requirement**: Labels or instructions are provided when content requires user input.

**Most common violations**:
- Placeholder text as the only label (disappears on focus)
- Complex form fields with no instructions (e.g., password requirements)
- Date fields with no format indication

**Fix pattern**:
```html
<label for="password">Password</label>
<input id="password" type="password" aria-describedby="password-help" />
<p id="password-help" class="text-sm text-gray-600">
  Must be at least 8 characters with one uppercase letter and one number.
</p>
```

---

## Level AA Criteria (Standard Target)

### 1.4.3 Contrast (Minimum) (Level AA)

**Requirement**: Text has a contrast ratio of at least 4.5:1 (normal text) or 3:1 (large text: 18pt regular or 14pt bold).

**Most common violations**:
- Light gray placeholder text (often around 2:1 ratio)
- Secondary text in gray-400 on white (often 2.5-3.5:1)
- White text on colored backgrounds that are too light
- Disabled state text that is intentionally low contrast but still meant to be readable

**Fix reference table**:

| Foreground | Background | Ratio | Passes AA? |
|-----------|-----------|-------|-----------|
| #6B7280 (gray-500) | #FFFFFF | 4.6:1 | Yes (normal text) |
| #9CA3AF (gray-400) | #FFFFFF | 2.9:1 | No |
| #4B5563 (gray-600) | #FFFFFF | 7.0:1 | Yes (AAA) |
| #FFFFFF | #2563EB (blue-600) | 4.7:1 | Yes (normal text) |
| #FFFFFF | #3B82F6 (blue-500) | 3.1:1 | Large text only |
| #FFFFFF | #60A5FA (blue-400) | 2.1:1 | No |
| #111827 (gray-900) | #F9FAFB (gray-50) | 17.2:1 | Yes (AAA) |
| #E0E0E0 | #121212 (dark bg) | 13.2:1 | Yes (AAA) |
| #A0A0A0 | #1E1E1E (dark raised) | 5.4:1 | Yes (AA) |

**Tool**: Use the WebAIM Contrast Checker (https://webaim.org/resources/contrastchecker/) or axe DevTools to verify ratios.

### 1.4.11 Non-text Contrast (Level AA)

**Requirement**: Visual information required to identify UI components and graphical objects has a contrast ratio of at least 3:1 against adjacent colors.

**Most common violations**:
- Form field borders that are too light against the background
- Icon-only buttons where the icon has insufficient contrast
- Progress bars, charts, and data visualizations with low-contrast elements
- Custom checkboxes and radio buttons

**Fix pattern**: Ensure borders, icons, and graphical elements meet 3:1 minimum.
```css
/* Bad: 1.8:1 contrast */
.input { border: 1px solid #D1D5DB; }

/* Good: 3.2:1 contrast */
.input { border: 1px solid #9CA3AF; }
```

### 2.4.6 Headings and Labels (Level AA)

**Requirement**: Headings and labels describe topic or purpose.

**Most common violations**:
- Generic headings like "Section 1", "Details", or "Info"
- Missing heading hierarchy (jumping from h1 to h4)
- Form labels that do not clearly indicate what information is expected

**Fix pattern**: Use descriptive headings that allow users to understand page structure from headings alone. Maintain a sequential hierarchy: h1, h2, h3 (never skip levels).

### 2.4.7 Focus Visible (Level AA)

**Requirement**: Any keyboard operable user interface has a mode of operation where the keyboard focus indicator is visible.

**Most common violations**:
- `outline: none` applied globally without replacement
- Custom focus styles with insufficient contrast (less than 3:1)
- Focus styles that are only visible on certain background colors

**Fix pattern**:
```css
/* Remove the browser default but provide a clear custom focus indicator */
:focus-visible {
  outline: 2px solid #0057B8;
  outline-offset: 2px;
  border-radius: 2px;
}

/* For dark backgrounds, ensure the focus color works */
.dark-bg :focus-visible {
  outline-color: #60A5FA;
}
```

The `:focus-visible` pseudo-class only shows focus for keyboard navigation, not mouse clicks, which is the standard modern approach.

### 2.5.8 Target Size (Minimum) (Level AA — WCAG 2.2)

**Requirement**: Targets have a size of at least 24x24 CSS pixels, except when the target has sufficient spacing from other targets, is inline text, is user-agent controlled, or is essential.

**Recommended minimum**: 44x44px for touch targets (Apple HIG), 48x48px for Android (Material Design).

**Most common violations**:
- Small icon buttons (close, edit, delete) at 16-20px
- Table row action buttons with insufficient spacing
- Dense control panels with tightly packed small buttons

**Fix pattern**:
```css
.icon-button {
  /* Visual size can be smaller, but tappable area must be at least 44x44 */
  min-width: 44px;
  min-height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-button svg {
  width: 20px; /* Visual icon size */
  height: 20px;
}
```

### 3.3.3 Error Suggestion (Level AA)

**Requirement**: If an input error is automatically detected and suggestions for correction are known, the suggestions are provided to the user.

**Most common violation**: Error says "Invalid input" without explaining what is expected.

**Fix pattern**:
```html
<!-- Bad -->
<span class="error">Invalid email</span>

<!-- Good -->
<span class="error" role="alert">
  Please enter a valid email address. Example: name@company.com
</span>
```

### 4.1.3 Status Messages (Level AA)

**Requirement**: Status messages can be programmatically determined through role or properties such that they can be presented to the user by assistive technologies without receiving focus.

**Most common violations**:
- Toast notifications not in a live region
- Cart total updates not announced
- Search result count changes not communicated
- Form submission success messages not announced

**Fix patterns**:

Toast notification:
```html
<div role="status" aria-live="polite" class="toast">
  Changes saved successfully
</div>
```

Search results:
```html
<div aria-live="polite" aria-atomic="true">
  Showing 24 results for "onboarding"
</div>
```

For urgent messages (errors):
```html
<div role="alert">
  Connection lost. Attempting to reconnect...
</div>
```

---

## Level AAA Criteria (Enhanced — Reference Only)

These are not typically required but are worth pursuing for critical user flows.

### 1.4.6 Contrast (Enhanced) (Level AAA)

**Requirement**: 7:1 contrast for normal text, 4.5:1 for large text.

**When to target**: Login pages, error messages, legal text, accessibility-focused products.

**Safe values for white backgrounds**: Use gray-600 (#4B5563) or darker for all text. Use gray-700 (#374151) for body text.

### 1.4.8 Visual Presentation (Level AAA)

**Requirement**: Text can be resized up to 200% without loss of content or functionality. Line spacing is at least 1.5 within paragraphs. Maximum line width is 80 characters.

**Fix pattern**:
```css
body {
  font-size: 1rem; /* Respects user's browser settings */
  line-height: 1.5;
  max-width: 65ch; /* ~65 characters per line for comfortable reading */
}
```

### 2.4.10 Section Headings (Level AAA)

**Requirement**: Section headings are used to organize the content.

**Best practice**: Every distinct section of a page should have a heading, even if the heading is visually hidden. This enables screen reader users to navigate by heading.

```html
<section aria-labelledby="activity-heading">
  <h2 id="activity-heading" class="sr-only">Recent activity</h2>
  <!-- Activity feed content -->
</section>
```

---

## Common Contrast Ratios Quick Reference

For rapid checks during an audit:

| Use Case | Minimum Ratio | WCAG Level | Rule |
|----------|:------------:|:----------:|------|
| Normal text (under 18px regular / 14px bold) | 4.5:1 | AA | 1.4.3 |
| Large text (18px+ regular or 14px+ bold) | 3:1 | AA | 1.4.3 |
| UI components and graphical objects | 3:1 | AA | 1.4.11 |
| Focus indicators | 3:1 | AA | 2.4.11 (2.2) |
| Enhanced normal text | 7:1 | AAA | 1.4.6 |
| Enhanced large text | 4.5:1 | AAA | 1.4.6 |
| Placeholder text | 4.5:1 | AA | Technically exempt but strongly recommended |
| Disabled controls | Exempt | -- | Not required but consider readability |

## Assistive Technology Testing Checklist

Minimum testing matrix for OrgX audits:

| Combination | Priority | Notes |
|------------|---------|-------|
| VoiceOver + Safari (macOS) | Required | Most common Mac screen reader pairing |
| NVDA + Chrome (Windows) | Required | Most common free screen reader pairing |
| JAWS + Chrome (Windows) | Recommended | Most common commercial screen reader |
| VoiceOver + Safari (iOS) | Recommended for mobile | Default mobile screen reader on iOS |
| TalkBack + Chrome (Android) | Recommended for mobile | Default Android screen reader |
| Keyboard only (no screen reader) | Required | Tests focus management and operability |
| Browser zoom 200% | Required | Tests responsive layout under magnification |
| Windows High Contrast Mode | Recommended | Tests forced-colors behavior |

## Automated Tools and Their Limitations

| Tool | What It Catches | What It Misses |
|------|----------------|---------------|
| axe-core | ~30% of WCAG issues (structural, contrast, missing attributes) | Logical order, meaningful labels, keyboard traps, focus management |
| Lighthouse | Similar to axe-core, plus performance impact | Same as axe-core |
| WAVE | Visual overlay of issues, color contrast | Complex interaction issues |
| pa11y | CI-friendly automated checks | Interactive component behavior |

**Key insight**: Automated tools catch roughly 30% of accessibility issues. The remaining 70% require manual testing: keyboard navigation, screen reader walkthrough, and cognitive review. Always combine automated scans with manual testing.
