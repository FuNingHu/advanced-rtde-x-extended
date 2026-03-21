---
name: panel-height-guide
description: Provide optimal panel height values for PolyScope X Application Node panels. Use when creating a new application node panel, setting panel height, or when the user mentions panel sizing, filling display height, or avoiding gaps/overflow in the PolyScope X UI.
---

# Application Node Panel Height Guide

## When to Use

Apply this skill when:
- Creating a new Application Node component that needs to fill the available display height
- Setting or adjusting panel height in an existing Application Node
- The user mentions: panel height, panel sizing, fill height, full height, display gap, content clipping, or overflow in the PolyScope X UI
- Debugging layout issues where panels appear too short (visible gap) or too tall (content cut off)

Do NOT apply when working with Program Nodes, Operator Screens, Sidebar items, or non-panel UI elements.

## Core Principle

Application Node panels in PolyScope X are embedded in a host iframe. Available height = `100vh` minus the space occupied by the host UI (top navbar, tab bar, bottom status bar, etc.).

## Height Quick Reference

| Element Role | Recommended Height | Notes |
|---|---|---|
| **Root container** | `height: calc(100vh - 160px)` | Subtracts PolyScope navbar + tab bar + status bar |
| **First-level child panel** | `height: 100%` | Inherits root container height |
| **Content card** | `height: auto; max-height: calc(100% - Npx)` | N depends on sibling elements (title, padding, etc.) |
| **Scrollable area** | `height: 100%; overflow-y: auto` | Fills parent, scrolls on overflow |

## Root Container Height

```scss
.your-container {
  display: flex;
  height: calc(100vh - 160px);
  max-height: 100%;
  overflow: hidden;
}
```

**Why 160px**: The PolyScope X host UI occupies ~160px (top navigation bar + application tab bar + bottom status bar). This value is empirically tested in the advanced-rtde project.

### Fine-Tuning

If 160px doesn't perfectly fit your scenario:

| Symptom | Adjustment |
|---|---|
| Visible gap at the bottom | Decrease offset (e.g. `100vh - 140px`) |
| Content clipped at the bottom | Increase offset (e.g. `100vh - 180px`) |
| Inconsistent across screens | Add `max-height: 100%` as a safety cap |

## Child Panel Patterns

### Fixed Sidebar + Flexible Main Area

```scss
.side-panel {
  width: 300px;
  height: 100%;
  flex-shrink: 0;
  overflow-y: auto;
}

.main-area {
  flex: 1;
  height: 100%;
  overflow-x: auto;
  overflow-y: hidden;
}
```

### Content Card (with title/margins)

When the card has a title bar or extra padding, subtract with `calc(100% - Npx)`:

```scss
.content-card {
  height: auto;
  max-height: calc(100% - 50px);
  overflow-y: auto;
}
```

**How to determine N**: Sum up the title bar height + top/bottom padding + gap of sibling elements at the same level. Typical range: 30px ~ 60px.

### Scrollable Content Area

```scss
.scrollable-wrapper {
  height: 100%;
  overflow-y: auto;
  padding: 15px;
}
```

## Full Template

Copy this template when creating a new Application Node panel:

```scss
.app-container {
  display: flex;
  height: calc(100vh - 160px);
  max-height: 100%;
  overflow: hidden;
}

.left-panel {
  width: 300px;
  height: 100%;
  flex-shrink: 0;
  overflow-y: auto;
  padding: 15px;
  box-sizing: border-box;
}

.main-panel {
  flex: 1;
  height: 100%;
  overflow: auto;
  padding: 15px;
  box-sizing: border-box;
}
```

## Important Notes

- Always set `max-height: 100%` on the root container to prevent overflow
- Explicitly set `overflow-y: auto` on scrollable areas and `overflow: hidden` on non-scrollable ones
- Pass height down through nested children with `height: 100%` — avoid breaking the height chain at any intermediate layer
- Use `box-sizing: border-box` to ensure padding doesn't push elements beyond their container
- For panels with dynamic content (e.g. variable-length lists), prefer `max-height` + `overflow-y: auto` over a fixed `height`
