# OrgX Widget SDK

The runtime layer that makes widgets work across ChatGPT, Claude.ai (MCP-apps), and standalone pages.

## Protocol Detection

Every widget starts by detecting its rendering context:

```js
function _detectProtocol() {
  if (typeof window.openai !== 'undefined') return 'chatgpt';
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
- **MCP-apps**: Sends `ui/initialize` via postMessage, listens for `ui/notifications/tool-result`
- **Standalone**: Calls render immediately with demo or null data

### Boot Sequence
1. Show skeleton loading state
2. `initWidget` registers render callback
3. Data arrives → `applyBootPayload` → minimum 220ms loading time → render
4. Skeleton fades out (opacity 0.3s) → content fades in

## Inline Actions via `callTool`

Widgets can call OrgX MCP tools directly from the UI:

```js
// Approve a decision
callTool('approve_decision', {
  decision_id: 'dec-123',
  note: 'Approved via widget'
}).then(function(result) {
  // Update UI to show resolution
}).catch(function(err) {
  // Show error state
});
```

`callTool` dispatches via:
- **ChatGPT**: `window.openai.callTool(name, args)`
- **MCP-apps**: `postMessage` with `tools/call` method, 30s timeout
- **Standalone**: Returns `null` (demo mode)

## Navigation via `openWidgetLink`

All deep links MUST use `openWidgetLink` instead of raw `<a>` navigation:

```js
function openWidgetLink(url, event) {
  if (!url) return false;
  var protocol = _detectProtocol();
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

## Size Reporting

MCP-apps need to know the widget's dimensions:

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
```js
function renderAvatar(agent) {
  var profile = resolveAgentProfile(agent);
  if (profile.avatarPath) {
    var src = 'https://mcp.useorgx.com/widgets/shared/' + profile.avatarPath;
    return '<img src="' + src + '" onerror="this.style.display=\'none\'; this.previousElementSibling.style.display=\'flex\';" />';
  }
  return '<span class="avatar-fallback">' + profile.name[0] + '</span>';
}
```

Always include a letter-fallback `<span>` before the `<img>` with `display:none` — the `onerror` handler reveals it on image load failure.

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

Widget shared assets (avatars, CSS, JS) served from:
```
https://mcp.useorgx.com/widgets/shared/
```

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
