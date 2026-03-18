# Worked Example: Interaction Spec — Multi-step Initiative Configuration Modal

This is a complete, worked example of an interaction specification produced by the OrgX Design Agent. It demonstrates the expected depth for state definitions, transitions, keyboard behavior, responsive adaptation, and error handling.

## Context

- **Product**: OrgX Live Dashboard
- **Component**: Initiative creation modal (3-step flow)
- **Platform**: Web (responsive)
- **Framework**: React, Radix Dialog, Framer Motion
- **Context Signal**: Web application (productivity-focused, keyboard shortcuts essential)
- **Users**: Engineering managers creating initiatives 2-3 times per week

## Artifact

```json
{
  "name": "Initiative Configuration Modal",
  "description": "A 3-step modal dialog that guides the user through creating a new initiative: (1) name and description, (2) workstream assignment, (3) review and launch. Each step validates before proceeding. Supports backward navigation, keyboard-driven operation, and graceful handling of unsaved changes.",
  "states": [
    {
      "name": "closed",
      "visual_description": "Modal is not rendered in the DOM. The 'New Initiative' trigger button is visible and focusable in the main interface.",
      "entry_conditions": [
        "User clicks Close button",
        "User presses Escape with no unsaved changes",
        "User confirms discard in the unsaved changes dialog",
        "User clicks the backdrop overlay with no unsaved changes",
        "User completes step 3 and clicks Launch"
      ],
      "exit_conditions": [
        "User clicks 'New Initiative' button",
        "User presses keyboard shortcut Cmd+N / Ctrl+N (when enabled)"
      ]
    },
    {
      "name": "open-step-1",
      "visual_description": "Modal visible with backdrop overlay at 50% opacity. Step 1 content shows: initiative name input (required, autofocused), description textarea (optional), and a category dropdown. Progress indicator shows step 1 of 3 active. Footer contains Cancel and Next buttons.",
      "entry_conditions": [
        "Modal opens from closed state",
        "User clicks Back from step 2"
      ],
      "exit_conditions": [
        "User clicks Next (triggers validation)",
        "User presses Enter (triggers validation)",
        "User dismisses modal"
      ]
    },
    {
      "name": "step-1-validating",
      "visual_description": "Next button shows loading spinner. Form fields are disabled. Brief validation state (typically under 100ms for client-side validation).",
      "entry_conditions": [
        "User clicks Next or presses Enter on step 1"
      ],
      "exit_conditions": [
        "Validation passes — transition to open-step-2",
        "Validation fails — transition to step-1-error"
      ]
    },
    {
      "name": "step-1-error",
      "visual_description": "Same as open-step-1 but with inline error messages below invalid fields. Invalid fields have a red border (var(--color-error)). Error icon appears to the left of the error message text. Focus moves to the first invalid field.",
      "entry_conditions": [
        "Step 1 validation fails"
      ],
      "exit_conditions": [
        "User corrects the field and the error clears on blur",
        "User clicks Next again (re-triggers validation)",
        "User dismisses modal"
      ]
    },
    {
      "name": "open-step-2",
      "visual_description": "Step 2 content shows: a searchable list of available workstreams with checkboxes. Selected workstreams appear in a tag-style chip row above the list. Minimum 1 workstream required. Progress indicator shows step 2 of 3 active. Footer contains Back, Cancel, and Next buttons.",
      "entry_conditions": [
        "Step 1 validation passes",
        "User clicks Back from step 3"
      ],
      "exit_conditions": [
        "User clicks Next (triggers validation)",
        "User clicks Back (returns to step 1)",
        "User dismisses modal"
      ]
    },
    {
      "name": "step-2-validating",
      "visual_description": "Next button shows loading spinner. Workstream selection is disabled.",
      "entry_conditions": [
        "User clicks Next on step 2"
      ],
      "exit_conditions": [
        "Validation passes (at least 1 workstream selected) — transition to open-step-3",
        "Validation fails — transition to step-2-error"
      ]
    },
    {
      "name": "step-2-error",
      "visual_description": "Same as open-step-2 but with an error banner above the workstream list: 'Select at least one workstream to continue.' The error banner has role='alert' for screen reader announcement.",
      "entry_conditions": [
        "Step 2 validation fails (no workstreams selected)"
      ],
      "exit_conditions": [
        "User selects a workstream (error clears automatically)",
        "User dismisses modal"
      ]
    },
    {
      "name": "open-step-3",
      "visual_description": "Step 3 content shows: a read-only summary of the initiative name, description, category, and selected workstreams. Each section has an Edit link that navigates back to the relevant step. Progress indicator shows step 3 of 3 active. Footer contains Back, Cancel, and Launch buttons. Launch button is primary variant.",
      "entry_conditions": [
        "Step 2 validation passes"
      ],
      "exit_conditions": [
        "User clicks Launch (triggers submission)",
        "User clicks Back (returns to step 2)",
        "User clicks Edit on a section (returns to that step)",
        "User dismisses modal"
      ]
    },
    {
      "name": "submitting",
      "visual_description": "Launch button shows loading spinner with text 'Launching...' All form content is visible but non-interactive. A subtle progress bar animates below the modal header. Backdrop click and Escape are disabled during submission.",
      "entry_conditions": [
        "User clicks Launch on step 3"
      ],
      "exit_conditions": [
        "Submission succeeds — transition to success",
        "Submission fails — transition to submission-error"
      ]
    },
    {
      "name": "success",
      "visual_description": "Modal content replaced with a success illustration, the initiative name, and a 'View Initiative' button. Confetti or checkmark animation plays. Auto-closes after 3 seconds if user does not interact.",
      "entry_conditions": [
        "Submission succeeds"
      ],
      "exit_conditions": [
        "User clicks 'View Initiative' (navigates and closes modal)",
        "3-second auto-close timer fires",
        "User presses Escape"
      ]
    },
    {
      "name": "submission-error",
      "visual_description": "Same as open-step-3 but with an error banner at the top of the modal: 'Something went wrong. Please try again.' A Retry button appears alongside the Launch button.",
      "entry_conditions": [
        "Submission API call fails"
      ],
      "exit_conditions": [
        "User clicks Retry (returns to submitting state)",
        "User clicks Back to edit",
        "User dismisses modal"
      ]
    },
    {
      "name": "confirming-close",
      "visual_description": "A confirmation dialog overlays the modal (not a second modal — uses the same Dialog layer with swapped content). Text: 'You have unsaved changes. Discard and close?' Two buttons: 'Keep editing' (secondary) and 'Discard' (destructive). The main modal content is visible but blurred behind the confirmation.",
      "entry_conditions": [
        "User attempts to dismiss (Escape, backdrop click, or Close button) when form has unsaved changes"
      ],
      "exit_conditions": [
        "User clicks 'Keep editing' — returns to the current step",
        "User clicks 'Discard' — transitions to closed",
        "User presses Escape — returns to current step (safe default)"
      ]
    }
  ],
  "transitions": [
    {
      "from_state": "closed",
      "to_state": "open-step-1",
      "trigger": "Click on 'New Initiative' button or Cmd+N / Ctrl+N shortcut",
      "duration": "200ms",
      "easing": "cubic-bezier(0, 0, 0, 1)",
      "properties_animated": ["opacity: 0 -> 1", "transform: scale(0.95) -> scale(1)"],
      "notes": "Backdrop fades in simultaneously. Focus moves to the name input field after animation completes."
    },
    {
      "from_state": "open-step-1",
      "to_state": "open-step-2",
      "trigger": "Step 1 validation passes",
      "duration": "250ms",
      "easing": "cubic-bezier(0.2, 0, 0, 1)",
      "properties_animated": ["Step 1 content slides left and fades out", "Step 2 content slides in from right and fades in"],
      "notes": "Progress bar fills from 33% to 66% over 300ms ease-in-out. Focus moves to the workstream search input."
    },
    {
      "from_state": "open-step-2",
      "to_state": "open-step-1",
      "trigger": "User clicks Back",
      "duration": "250ms",
      "easing": "cubic-bezier(0.2, 0, 0, 1)",
      "properties_animated": ["Step 2 content slides right and fades out", "Step 1 content slides in from left and fades in"],
      "notes": "Progress bar fills back from 66% to 33%. Focus moves to the name input. Previously entered data is preserved."
    },
    {
      "from_state": "open-step-2",
      "to_state": "open-step-3",
      "trigger": "Step 2 validation passes",
      "duration": "250ms",
      "easing": "cubic-bezier(0.2, 0, 0, 1)",
      "properties_animated": ["Step 2 slides left and fades out", "Step 3 slides in from right and fades in"],
      "notes": "Progress bar fills from 66% to 100%. Focus moves to the Launch button."
    },
    {
      "from_state": "open-step-3",
      "to_state": "open-step-2",
      "trigger": "User clicks Back",
      "duration": "250ms",
      "easing": "cubic-bezier(0.2, 0, 0, 1)",
      "properties_animated": ["Step 3 slides right, step 2 slides in from left"],
      "notes": "Progress bar returns to 66%. Focus moves to the workstream search input."
    },
    {
      "from_state": "open-step-3",
      "to_state": "open-step-1",
      "trigger": "User clicks Edit on name/description section",
      "duration": "250ms",
      "easing": "cubic-bezier(0.2, 0, 0, 1)",
      "properties_animated": ["Step 3 slides right, step 1 slides in from left"],
      "notes": "Progress bar returns to 33%. Focus moves to the field that was clicked for editing."
    },
    {
      "from_state": "submitting",
      "to_state": "success",
      "trigger": "API returns 200",
      "duration": "300ms",
      "easing": "cubic-bezier(0, 0, 0, 1)",
      "properties_animated": ["Form content fades out, success content scales up from 0.9 to 1 and fades in"],
      "notes": "Checkmark animation plays with a 150ms delay after content transition completes."
    },
    {
      "from_state": "any-open-state",
      "to_state": "closed",
      "trigger": "Modal closes (no unsaved changes, or user confirms discard)",
      "duration": "150ms",
      "easing": "cubic-bezier(0.3, 0, 1, 1)",
      "properties_animated": ["opacity: 1 -> 0", "transform: scale(1) -> scale(0.95)"],
      "notes": "Faster than open animation (accelerate easing). Focus returns to the trigger button."
    },
    {
      "from_state": "any-open-state",
      "to_state": "confirming-close",
      "trigger": "Dismiss attempt with unsaved changes",
      "duration": "150ms",
      "easing": "cubic-bezier(0, 0, 0, 1)",
      "properties_animated": ["Main content blurs (filter: blur(4px))", "Confirmation dialog fades in and slides down 8px"],
      "notes": "Focus moves to the 'Keep editing' button (safe default)."
    }
  ],
  "micro_interactions": [
    {
      "name": "step-progress-fill",
      "trigger": "Step transition completes",
      "purpose": "feedback",
      "spec": "Progress bar width animates to new percentage (33%, 66%, 100%) over 300ms with ease-in-out easing. Color transitions from gray to primary blue as each segment fills."
    },
    {
      "name": "field-focus-ring",
      "trigger": "Input field receives focus",
      "purpose": "feedback",
      "spec": "2px solid outline in var(--color-primary) appears with 2px offset. Transition: outline-color 100ms ease. When field is invalid, outline color is var(--color-error)."
    },
    {
      "name": "error-shake",
      "trigger": "Validation fails and focus moves to invalid field",
      "purpose": "feedback",
      "spec": "Invalid field translates horizontally: 0 -> -4px -> 4px -> -2px -> 2px -> 0 over 300ms. Uses a keyframe animation, not a transition. Fires only once per validation attempt."
    },
    {
      "name": "workstream-chip-add",
      "trigger": "User selects a workstream checkbox",
      "purpose": "feedback",
      "spec": "New chip scales from 0.8 to 1 and fades from 0 to 1 over 150ms with spring easing. Existing chips slide left to make room over 200ms."
    },
    {
      "name": "workstream-chip-remove",
      "trigger": "User unchecks a workstream or clicks X on chip",
      "purpose": "feedback",
      "spec": "Chip scales from 1 to 0.8 and fades out over 100ms. Remaining chips slide to close the gap over 150ms."
    },
    {
      "name": "launch-button-pulse",
      "trigger": "User arrives at step 3 (review)",
      "purpose": "delight",
      "spec": "Launch button has a single subtle scale pulse (1 -> 1.02 -> 1) over 600ms with ease-in-out, played once after a 500ms delay. Draws attention to the primary action without being distracting."
    },
    {
      "name": "success-checkmark",
      "trigger": "Submission succeeds",
      "purpose": "delight",
      "spec": "SVG checkmark draws itself using stroke-dashoffset animation over 400ms with decelerate easing. Circle scales from 0 to 1 over 300ms, then checkmark stroke animates from 0% to 100% visible."
    }
  ],
  "keyboard_behavior": {
    "tab_order": "When modal opens: Close button (top-right) -> Form fields in DOM order (name, description, category for step 1) -> Back button (if not step 1) -> Cancel button -> Next/Launch button. Tab wraps from last to first element (focus trap).",
    "shortcuts": [
      { "key": "Escape", "action": "If no unsaved changes: close modal and return focus to trigger. If unsaved changes: open confirmation dialog." },
      { "key": "Enter", "action": "Submit current step (equivalent to clicking Next/Launch). Does not submit if focus is on a textarea (allows newlines)." },
      { "key": "Cmd+Enter / Ctrl+Enter", "action": "Submit current step regardless of focus position. Works even from within textarea." },
      { "key": "Shift+Tab", "action": "Move focus to previous focusable element. Wraps from first to last element (reverse tab trap)." },
      { "key": "Alt+Left / Alt+Backspace", "action": "Navigate to previous step (equivalent to clicking Back). No-op on step 1." },
      { "key": "Alt+Right", "action": "Navigate to next step if current step is valid. Triggers validation." }
    ],
    "escape_handling": "First Escape press: if unsaved changes exist, show confirmation dialog. If no changes, close immediately. Second Escape press (while confirmation is showing): dismiss confirmation and return to editing (safe default). Focus returns to the element that opened the modal.",
    "focus_trap": true,
    "focus_restoration": "On close, focus returns to the 'New Initiative' button that triggered the modal. On success with 'View Initiative' click, focus moves to the initiative page heading."
  },
  "responsive_behavior": {
    "320-767": {
      "layout": "Modal becomes a full-screen sheet sliding up from the bottom of the viewport. Border-radius removed. Padding reduced to 16px.",
      "navigation": "Back button moves to the header left position. Close becomes an X in the header right. Next/Launch remain in a sticky footer bar.",
      "adaptations": "Category dropdown becomes full-width. Workstream list items are larger (48px touch targets). Progress indicator uses dots instead of a bar.",
      "animation": "Sheet slides up with translateY(100%) -> translateY(0) over 300ms decelerate."
    },
    "768-1023": {
      "layout": "Centered modal overlay. Width: 600px. Max-height: 85vh. Internal scrolling for long content. 24px padding.",
      "navigation": "Standard button layout in footer.",
      "adaptations": "Workstream list shows 6 items before scrolling. Category dropdown is inline.",
      "animation": "Standard scale + fade animation."
    },
    "1024+": {
      "layout": "Centered modal overlay. Width: 640px. Max-height: 80vh. 32px padding.",
      "navigation": "Standard button layout. Keyboard shortcuts fully active.",
      "adaptations": "Workstream list shows 8 items before scrolling. Side-by-side layout for name and category on step 1.",
      "animation": "Standard scale + fade animation."
    }
  },
  "error_states": [
    {
      "trigger": "Step 1 validation: name field is empty",
      "visual_treatment": "Name input border turns red (var(--color-error)). Error message appears below: 'Initiative name is required.' Error icon (exclamation circle) precedes the message. Field receives focus.",
      "recovery_action": "User types in the name field. Error clears on blur if field is non-empty, or on next submit attempt.",
      "aria_behavior": "Error message has role='alert' and is linked via aria-describedby. Screen reader announces 'Initiative name is required' when focus moves to the field."
    },
    {
      "trigger": "Step 1 validation: name exceeds 100 characters",
      "visual_treatment": "Character counter below name field turns red. Error message: 'Name must be 100 characters or fewer (currently 117).'",
      "recovery_action": "User shortens the name. Counter updates in real time. Error clears when length is at or below 100.",
      "aria_behavior": "Character count announced via aria-live='polite' region when it crosses the threshold."
    },
    {
      "trigger": "Step 2 validation: no workstreams selected",
      "visual_treatment": "Error banner appears above the workstream list with yellow warning background: 'Select at least one workstream to continue.' The workstream list border highlights.",
      "recovery_action": "User checks any workstream checkbox. Error banner fades out over 150ms when at least one is selected.",
      "aria_behavior": "Banner has role='alert'. Screen reader announces the error text immediately."
    },
    {
      "trigger": "Step 3 submission: API returns 500 error",
      "visual_treatment": "Red error banner at the top of the modal: 'Something went wrong creating your initiative. Please try again.' Launch button text changes to 'Retry'. A 'View details' expandable shows the error code for support purposes.",
      "recovery_action": "User clicks Retry to re-submit. If error persists after 2 retries, message changes to 'Please contact support' with a link.",
      "aria_behavior": "Error banner has role='alert'. Focus moves to the Retry button."
    },
    {
      "trigger": "Step 3 submission: network timeout after 10 seconds",
      "visual_treatment": "Loading spinner stops. Error banner: 'Request timed out. Check your connection and try again.' Show last-known network status indicator.",
      "recovery_action": "User clicks Retry. If the initiative was actually created (duplicate detection), show success state with a note: 'Initiative was already created.'",
      "aria_behavior": "Timeout announced via aria-live. Focus moves to Retry button."
    }
  ],
  "accessibility_notes": {
    "dialog_role": "Modal uses role='dialog' with aria-modal='true' and aria-labelledby pointing to the step title.",
    "progress_indication": "Step progress is communicated via aria-label on the progress component: 'Step 2 of 3: Assign workstreams'.",
    "live_regions": "Form validation errors use role='alert'. Character count uses aria-live='polite'. Submission status uses aria-live='assertive'.",
    "reduced_motion": "When prefers-reduced-motion is active: all slide transitions become instant opacity fades at 100ms. Error shake animation is removed. Success checkmark draws instantly. Launch button pulse is removed."
  }
}
```

## Summary

- **12 states** defined covering the full lifecycle: closed, 3 steps with validation and error variants, submission, success, error, and unsaved changes confirmation
- **9 transitions** with specific duration, easing, and animated properties for each
- **7 micro-interactions** providing feedback (validation, selection) and delight (launch pulse, success checkmark)
- **Full keyboard spec** with 6 shortcuts, focus trap, and focus restoration
- **3 responsive breakpoints** with layout, navigation, and animation adaptations
- **5 error states** with visual treatment, recovery paths, and ARIA behavior

## Next Steps

1. **Engineering Agent**: Implement the modal using Radix Dialog and Framer Motion, following the state machine and transition specs. Use the keyboard shortcuts table as acceptance criteria.
2. **Design Agent**: Create a motion spec artifact for the step transition and success animations, suitable for QA validation.
3. **Product Agent**: Add the multi-step modal to the usability testing plan for the next research cycle, specifically testing the back-navigation and unsaved changes flows.
