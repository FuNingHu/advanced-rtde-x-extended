# Cursor AI-Assisted URCap Development Report

> Date: 2026-03-25

---

## Development Environment

![Cursor Development Environment](images/cursor_environment.png)

## Adopted AI Model

**Claude Opus 4.6** — Anthropic's most capable model in the Claude 4 family. Features deep multi-step reasoning, large context window for cross-file analysis, and precise code editing. Powers the Cursor agent in both use cases below.

---

## Use Case 1: URCap SDK Dependency Upgrade — Accelerating URCap Development

### Challenge

Upgrading SDK dependencies in a URCap project requires comparing multiple `package.json` files across backend, frontend, and root directories, identifying version differences across dozens of packages, and updating them without mistakes. This process is manual, repetitive, and error-prone.

### Solution: 3-Stage AI-Assisted Workflow

#### Stage 1 — Granular Comparison & Automated Modification

Cursor reads all `package.json` files from both the target and reference projects simultaneously, diffs every `@universal-robots/*` version, and applies precise updates — eliminating the need to manually edit each line.

**What Cursor identified and updated automatically:**

| Package | Before | After |
|---------|:------:|:-----:|
| `@universal-robots/ui-angular-components` | 21.2.25 | 21.3.189 |
| `@universal-robots/contribution-api` | 21.2.25 | 21.3.131 |
| `@universal-robots/designtokens` | 21.2.25 | 21.3.85 |
| `@universal-robots/ui-models` | 21.2.25 | 21.3.85 |
| `@universal-robots/utilities-units` | 21.2.25 | 21.4.17 |
| `rimraf` (root) | 3.0.2 | 5.0.7 |
| `rimraf` (backend) | ^3.0.2 | 5.0.7 |
| `manifest-spec` path | 19.10.24 | 19.10.31 |

Beyond version numbers, Cursor also detected that `.gitignore` was missing `package-lock.json` and `target/` entries, and fixed them proactively.

**Comparison — Manual vs. AI-Assisted:**

| Step | Manual | Cursor AI |
|------|--------|-----------|
| Read & compare 6+ package.json files | Open tabs side by side, line-by-line scan | Batch read in one operation, instant diff |
| Identify version mismatches | Easy to miss subtle differences | Zero misses — every package checked |
| Apply updates | Copy-paste one by one, risk of typos | Targeted string replacement, exact edits |
| Catch non-obvious issues (manifest path, .gitignore) | Often overlooked | Automatically detected and fixed |
| **Total time** | **~1 hour** | **~5 minutes** |

#### Stage 2 — Auto-Generated Upgrade Documentation

After completing the upgrade, Cursor instantly generated a `SDK-UPGRADE.md` document containing:

- A **checklist** of every file inspected and whether it was modified
- A **change table** with old → new versions for each package
- **Post-upgrade steps** — ready-to-run commands for reinstall, validation, and build
- **Notes** on project-specific items intentionally left unchanged

This turns what would be 20–30 minutes of manual documentation (often skipped entirely) into a 30-second automatic generation — ensuring every upgrade is traceable and reviewable.

#### Stage 3 — Reusable Skill for Future Automation

Cursor created a **Skill** (`.cursor/skills/urcap-sdk-upgrade/SKILL.md`) that encodes the entire upgrade workflow into 6 repeatable steps:

| Step | Action |
|------|--------|
| 1 | Compare backend dependencies with reference project |
| 2 | Compare frontend `@universal-robots/*` packages with reference |
| 3 | Compare root directory dependencies and build script paths |
| 4 | Delete all `package-lock.json` and update `.gitignore` |
| 5 | Remove deprecated `NgModule`, migrate to standalone components |
| 6 | Clean reinstall with `npm install` |

For future SDK releases, any team member can simply tell Cursor *"Upgrade the SDK dependencies"* — the Skill activates automatically and walks through every step with zero tribal knowledge required.

### Use Case 1 Summary

| Metric | Before | After | Improvement |
|--------|:------:|:-----:|:-----------:|
| Upgrade execution time | ~1 hour | ~3 min | **20x faster** |
| Upgrade documentation | 20–30 min (often skipped) | ~30 sec | **Automated** |
| Process repeatability | Tribal knowledge | Codified Skill | **Permanent** |
| Error rate | Human-dependent | Near zero | **Reliable** |

---

## Use Case 2: URCap Advanced UI Creation — Dynamic Draggable Panels

### Challenge

Standard URCap application nodes use static layouts with fixed-position UI elements. Building advanced UI features — such as draggable panels, resizable areas, or dynamic content rearrangement — requires deep knowledge of Angular component architecture, CSS layout techniques, and PolyScope X iframe constraints. This is a significant barrier for developers who want to create more interactive and professional URCap interfaces.

### Solution: AI-Assisted Advanced UI Development

With Cursor AI, developers can describe the desired UI behavior in natural language and receive complete, working implementations.

#### Dynamic Draggable Panels

Cursor can generate drag-and-drop panel layouts that allow operators to customize their workspace:

- **Draggable panel components** with Angular CDK `DragDropModule` integration
- **Resizable split views** using CSS Grid or Flexbox with drag handles
- **Persistent layout state** that saves operator preferences across sessions
- **Responsive constraints** that respect PolyScope X's iframe boundaries (`calc(100vh - 160px)`)

#### Advanced URCap Features Enabled

| Feature | Description |
|---------|-------------|
| **Drag-and-drop reordering** | Operators rearrange parameter cards, signal lists, or configuration blocks |
| **Resizable panels** | Adjustable sidebar/main area split with drag handles |
| **Dynamic form builder** | Add/remove/reorder form fields at runtime |
| **Collapsible sections** | Expand/collapse content areas to manage screen real estate |
| **Interactive data tables** | Sortable, filterable tables with inline editing |
| **Real-time data visualization** | Live charts and graphs for RTDE data streams |

#### Development Acceleration

| Task | Manual | Cursor AI |
|------|--------|-----------|
| Implement drag-and-drop from scratch | 4–8 hours (research + code + debug) | ~15 minutes (describe + generate + refine) |
| Create responsive resizable layout | 2–4 hours | ~10 minutes |
| Add layout persistence with localStorage | 1–2 hours | ~5 minutes |
| Integrate with PolyScope X height constraints | Trial and error | Instant — leverages existing Skill knowledge |

#### Example Workflow

1. Developer describes: *"Create a draggable panel layout with a sidebar for signal configuration and a main area for real-time data display"*
2. Cursor generates the complete component: TypeScript, HTML template, SCSS styles
3. Cursor applies PolyScope X-specific height calculations automatically (using the `panel-height-guide` Skill)
4. Developer reviews, requests refinements in natural language
5. Final result: a production-ready interactive UI in minutes instead of hours

### Use Case 2 Summary

| Metric | Before | After | Improvement |
|--------|:------:|:-----:|:-----------:|
| Advanced UI implementation | 4–8 hours | ~15 minutes | **16–32x faster** |
| Required Angular expertise | Advanced | Basic (AI handles complexity) | **Lower barrier** |
| UI feature richness | Static layouts | Dynamic, interactive panels | **Enhanced UX** |
| Iteration speed | Hours per change | Minutes per change | **Rapid prototyping** |

---

## Overall Conclusion

| Use Case | Core Benefit |
|----------|-------------|
| **SDK Dependency Upgrade** | Transforms a tedious, error-prone maintenance task into a fast, documented, and repeatable automated workflow |
| **Advanced UI Creation** | Unlocks interactive UI capabilities that were previously too time-consuming to implement, enabling richer URCap experiences |

Cursor AI shifts developer focus from **repetitive mechanics** to **creative problem-solving** — accelerating both maintenance and innovation in URCap development.
