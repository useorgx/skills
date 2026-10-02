# OrgX Widget SDK

The runtime layer that makes widgets work across ChatGPT, Claude.ai (MCP-apps), and standalone pages.

## Protocol Detection

Every widget starts by detecting its rendering context:

```js
function _detectProtocol() {
  if (typeof window.openai !== 'undefined') return 'chatgpt';
  if (window.McpApps?.App && window.parent && window.parent !== window) return 'mcp-apps-sdk';
  if (window.parent && window.parent !== window) return 'mcp-apps';
  return 'standalone';
}
```

This determines how data arrives and how actions are dispatched.

## Widget Lifecycle

```js
initWidget({
  render: function(data) {
    // data is null on first call (loading state)
    // data is the parsed tool output on subsequent calls
    if (!data) { showSkeleton(); return; }
    renderContent(data);
  }
});
```

The `initWidget` function handles:
- **ChatGPT**: Reads `window.openai.toolOutput`, listens for `openai:set_globals`
- **MCP Apps SDK**: Connects an official `App`, receives `ontoolresult`, and applies `styles.variables` plus `styles.css.fonts` from host context
- **Legacy MCP-apps**: Uses the compatibility postMessage bridge only for widgets not yet migrated
- **Standalone**: Calls render immediately with demo or null data

### Boot Sequence
1. Show skeleton loading state
2. `initWidget` registers render callback
3. Data arrives → `applyBootPayload` → minimum 220ms loading time → render
4. Skeleton fades out (opacity 0.3s) → content fades in

## Design Kit

Widgets are built on the shared OrgX design kit (`@useorgx/orgx-ui-kit`),
vendored into the widget server as `public/widgets/shared/kit/ox-tokens.css`
(the `--ox-*` and `--agent-<key>` variables) and
`public/widgets/shared/kit/ox-elements.js` (framework-free custom elements,
exposed as `window.OrgXElements`). Load both before widget code:

```html
<link rel="stylesheet" href="shared/kit/ox-tokens.css" />
<script src="shared/kit/ox-elements.js"></script>
```

Reach for an element before writing bespoke markup:

| Element | Use |
| --- | --- |
| `<ox-state-chip state>` | One pill for every action state (`needs_you`, `sending`, `held`, `queued`, `running`, `succeeded`, `failed`, `handed_off`, `confirmed`, ...). It shows the person-facing wording, never the stored name. |
| `<ox-attention-line tone count oldest>` | The one line that opens a surface: "2 need your decision · oldest 2d", or "Nothing needs your decision." |
| `<ox-receipt-row status label value detail href>` | One line of proof (`met`, `fail`, `yours`, `unverified`, `pending`). With `href` it fires a cancelable `ox-open` event; route it through `openWidgetLink`. |
| `<ox-footer variant state>` | The action footer: `finishes-here`, `confirms-in-orgx`, `queues-work`, or `reads`, with hold-to-confirm and undo windows. |
| `<ox-glyph kind>` | Entity glyphs: `goal`, `initiative`, `workstream`, `milestone`, `task`, `run`, `decision`, `question`, `artifact`, `receipt`. |
| `<ox-avatar agent form size>` | Real agent avatars from `https://mcp.useorgx.com/widgets/shared/avatars/`, with an initial fallback. |

The kit files are generated from the kit package; never edit them in place.
Show the state the server reports: a chip or footer moves to `succeeded`/done
only after the tool call (or `orgx_command_status`) says so.

## Inline Actions via `callTool`

Widgets can call OrgX MCP tools directly from the UI. A person's click is the
only thing that settles a decision, so the decisions widget settles one with
`orgx_widget_decide` and the single-use approval token that arrives in
widget-only result metadata (`orgx/widgetApproval`). The model never sees that
token and never calls `orgx_widget_decide`; `approve_decision` /
`reject_decision` only point the person to where they decide.

```js
// The person clicked Approve on an ordinary decision
var meta = window.OrgXWidgetRuntime.getToolResponseMetadata('orgx/widgetApproval');
var token = meta && meta.approval_tokens ? meta.approval_tokens[decisionId] : null;
if (!token) {
  // No token: this decision is made in OrgX. Show "Open in OrgX" (review_url);
  // never pretend the widget settled it.
} else {
  callTool('orgx_widget_decide', {
    decision_id: decisionId,
    action: 'approve', // or 'reject' with a reason
    approval_token: token
  }).then(function(result) {
    // Show the settled state only after the call succeeds
  }).catch(function(err) {
    // Show the error; the decision is still waiting on the person
  });
}
```

Critical decisions, decisions with options to choose between, agent-run
approvals, and protected or artifact-review decisions carry no token: they are
always decided on the decision page in OrgX.

To show what happened after something was started, read
`orgx_command_status({ kind: 'decision' | 'run' | 'command', id })`. Its
`state` is `queued`, `held`, `running`, `succeeded`, `failed`, `cancelled`, or
`not_found`; `waiting_on` names a `person` or `agent`; check again after
`next_poll_after_ms`, and stop when it is `null` (final). Never render
"Done" for a state that is not `succeeded`.

`callTool` dispatches via:
- **ChatGPT**: `window.openai.callTool(name, args)`
- **MCP Apps SDK**: `App.callServerTool({ name, arguments })`
- **Legacy MCP-apps**: `postMessage` with `tools/call` method, 30s timeout
- **Standalone**: Returns `null` (demo mode)

## Navigation via `openWidgetLink`

All deep links MUST use `openWidgetLink` instead of raw `<a>` navigation:

```js
function openWidgetLink(url, event) {
  if (!url) return false;
  var protocol = _detectProtocol();
  if (protocol === 'mcp-apps-sdk') {
    if (event) event.preventDefault();
    void getBridge(true).openLink(url);
    return false;
  }
  if (protocol === 'mcp-apps') {
    if (event) event.preventDefault();
    window.parent.postMessage({
      jsonrpc: '2.0',
      id: _mcpNextId++,
      method: 'ui/open-link',
      params: { url: url }
    }, '*');
    return false;
  }
  return true; // Allow normal navigation in standalone
}
```

Usage in HTML:
```html
<a href="https://useorgx.com/live/init-123"
   onclick="return openWidgetLink('https://useorgx.com/live/init-123', event)"
   class="deep-link">
  Open live view →
</a>
```

## Legacy Size Reporting

The official SDK owns host communication. Only legacy widgets report size with
the compatibility postMessage bridge:

```js
function _sendSize() {
  var w = Math.ceil(document.documentElement.getBoundingClientRect().width);
  var h = Math.ceil(document.documentElement.getBoundingClientRect().height);
  window.parent.postMessage({
    jsonrpc: '2.0',
    method: 'ui/notifications/size-changed',
    params: { width: w, height: h }
  }, '*');
}
```

Called via `ResizeObserver` on `documentElement` and `body`.

## Theme Sync

Widgets support theme override via URL parameter:
```js
const theme = new URLSearchParams(window.location.search).get('theme');
if (theme) document.documentElement.setAttribute('data-theme', theme);
```

Plus `prefers-color-scheme` media queries in CSS for automatic detection.

## Embed Modes

Some widgets support embed-specific layouts:
```js
const embed = new URLSearchParams(window.location.search).get('embed');
if (embed) document.documentElement.setAttribute('data-embed', embed);
```

Example: `?embed=og-decision` triggers compact layout for OpenGraph cards:
```css
:root[data-embed="og-decision"] .ox-card-inner { padding: 20px; }
:root[data-embed="og-decision"] .widget-shell-card { display: none; }
```

## Data Normalization

LLM-generated tool output uses inconsistent field names. The `firstString` / `firstArray` / `firstNumber` helpers try multiple variants:

```js
var firstString = function(values) {
  for (var i = 0; i < values.length; i++) {
    var value = values[i];
    if (typeof value === 'string' && value.trim()) return value.trim();
  }
  return '';
};

// Usage: resolve agent name from any of 6 possible field names
agent_name: firstString([
  source.agent_name,
  source.agentName,
  source.name,
  source.title,
  source.label,
  source.agent_id
])
```

### Status Normalization
```js
var normalizeTaskStatus = function(value) {
  var slug = value.toLowerCase().replace(/[^a-z0-9]+/g, '_');
  if (['in_progress','running','active','executing','working'].includes(slug)) return 'in_progress';
  if (['blocked','paused','waiting','at_risk'].includes(slug)) return 'blocked';
  if (['done','complete','completed','approved','shipped'].includes(slug)) return 'done';
  if (['todo','not_started','queued','pending','draft','backlog'].includes(slug)) return 'todo';
  return '';
};
```

### Agent Profile Resolution
The `AGENT_DIRECTORY` maps agent names/roles to display profiles:
```js
var AGENT_DIRECTORY = {
  pace:    { name: 'Pace', role: 'Product',      avatarPath: 'product_orchestrator.png',    accentRgb: '22, 163, 74' },
  eli:     { name: 'Eli',  role: 'Engineering',   avatarPath: 'engineering_autopilot.png',   accentRgb: '6, 182, 212' },
  mark:    { name: 'Mark', role: 'Marketing',     avatarPath: 'launch_captain.png',          accentRgb: '249, 115, 22' },
  // ... etc
};
```

Resolution tries: direct name → agent type → role. Falls back to generic "OrgX Agent".

### Avatar Rendering

Use `<ox-avatar>` from the design kit (below) rather than hand-built `<img>`
markup. It renders the real agent avatar at
`https://mcp.useorgx.com/widgets/shared/avatars/<agent>-<form>-<size>.webp`
(agents `pace`, `eli`, `mark`, `sage`, `orion`, `dana`, `xandy`; forms `base`,
`strategic`, `proactive`, `working`, `asking`, `verifying`; sizes 48/96/192
with a 2x `srcset`), and falls back to the agent's initial in the same
footprint when the image fails:

```js
function renderAvatar(agentKey, name, sizePx) {
  if (agentKey && window.customElements && window.customElements.get('ox-avatar')) {
    return '<ox-avatar agent="' + agentKey + '" form="asking" size="' + sizePx + '" name="' + escapeHtml(name) + '"></ox-avatar>';
  }
  return '<span class="avatar-fallback">' + escapeHtml(name.charAt(0)) + '</span>';
}
```

Pick the form from state: `working` for a run in progress, `asking` when it
needs the person, `verifying` while proof is checked, `base` otherwise.

## Icon System

Inline SVG helper for consistent icon rendering:
```js
var _svg = function(content, size) {
  var sz = typeof size === 'number' ? size + 'px' : (size || '1em');
  return '<svg width="' + sz + '" height="' + sz + '" viewBox="0 0 24 24" fill="none" '
    + 'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
    + 'class="icon" aria-hidden="true">' + content + '</svg>';
};
```

Standard icon set: `agent`, `task`, `blocked`, `stream`, `check`, `warning`, `error`, `clock`, `search`, `file`, `link`, `external`.

## Remote Assets

Widget shared assets (design kit, avatars, CSS, JS) served from:
```
https://mcp.useorgx.com/widgets/shared/
```

Design kit files live under `kit/` and agent avatar renders under `avatars/`.

Resolve via:
```js
var REMOTE_WIDGET_ASSET_BASE = 'https://mcp.useorgx.com/widgets/shared/';
function resolveWidgetAsset(path) {
  return REMOTE_WIDGET_ASSET_BASE + path;
}
```

## URL Builders

```js
var ORGX_BASE_URL = 'https://useorgx.com';

// Agent settings page
var buildAgentUrl = function(agentId) {
  return agentId
    ? ORGX_BASE_URL + '/settings/agents?agent=' + encodeURIComponent(agentId)
    : ORGX_BASE_URL + '/settings/agents';
};

// Initiative live view
var buildInitiativeUrl = function(initiativeId) {
  return ORGX_BASE_URL + '/live/' + encodeURIComponent(initiativeId);
};
```
