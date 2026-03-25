# Cursor AI-Assisted URCap Development Report

> Date: 2026-03-25

---
# AI Model

**Claude Opus 4.6** — Anthropic's most capable model. Deep reasoning, large context window, precise code editing.

# Development Environment

![Cursor Development Environment](./images/cursor_environment.png)

---

# Use Case 1: SDK Dependency Upgrade

## Challenge

Upgrading URCap SDK requires comparing multiple `package.json` across backend, frontend, and root directories — manual, repetitive, error-prone.

## Solution: 3-Stage AI-Assisted Workflow

### Stage 1 — Granular Comparison & Automated Modification

Cursor batch-reads all `package.json` files, diffs every version, and applies precise updates.

**What Cursor identified and updated automatically:**


| Package                                   | Before   | After    |
| ----------------------------------------- | -------- | -------- |
| `@universal-robots/ui-angular-components` | 21.2.25  | 21.3.189 |
| `@universal-robots/contribution-api`      | 21.2.25  | 21.3.131 |
| `@universal-robots/designtokens`          | 21.2.25  | 21.3.85  |
| `@universal-robots/ui-models`             | 21.2.25  | 21.3.85  |
| `@universal-robots/utilities-units`       | 21.2.25  | 21.4.17  |
| `rimraf` (root)                           | 3.0.2    | 5.0.7    |
| `rimraf` (backend)                        | ^3.0.2   | 5.0.7    |
| `manifest-spec` path                      | 19.10.24 | 19.10.31 |

### Stage 2 — Auto-Generated Documentation

Cursor generated `SDK-UPGRADE.md` with checklist, change table, post-upgrade commands, and notes — replacing 20–30 min of manual writing with ~30 seconds.

### Stage 3 — Reusable Skill

Created `.cursor/skills/urcap-sdk-upgrade/SKILL.md` encoding 6 steps:

| Step                                                 | Manual                                    | Cursor AI                                 |
| ---------------------------------------------------- | ----------------------------------------- | ----------------------------------------- |
| Read & compare 6+ package.json files                 | Open tabs side by side, line-by-line scan | Batch read in one operation, instant diff |
| Identify version mismatches                          | Easy to miss subtle differences           | Zero misses — every package checked       |
| Apply updates                                        | Copy-paste one by one, risk of typos      | Targeted string replacement, exact edits  |
| Catch non-obvious issues (manifest path, .gitignore) | Often overlooked                          | Automatically detected and fixed          |
| **Total time**                                       | **~1 hour**                               | **~5 minutes**                            |

Any team member can trigger this Skill with *"Upgrade the SDK"*.

This Skill is open-sourced for all URCap developers: [urcap-sdk-upgrade Skill on GitHub](https://github.com/FuNingHu/advanced-rtde-x-extended/tree/main/.cursor/skills/urcap-sdk-upgrade)

## Summary

| Metric | Before | After | Improvement |
|--------|:------:|:-----:|:-----------:|
| Execution time | ~1 hour | ~5 min | **10x faster** |
| Documentation | 20–30 min | ~30 sec | **Automated** |
| Repeatability | Tribal knowledge | Codified Skill | **Permanent** |
| Error rate | Human-dependent | Near zero | **Reliable** |

---

# Use Case 2: Advanced UI — Dynamic Draggable Panels

## Challenge

Building draggable panels, resizable areas, or dynamic layouts in URCap requires deep Angular/CSS expertise and PolyScope X iframe constraints knowledge — a high barrier for most developers.

## Solution

Developers describe desired UI in natural language; Cursor generates complete implementations.

### Result Demo

![Draggable Card UI Demo](./images/jog-card.gif)


### Advanced URCap Features Enabled


| Feature                          | Description                                                                |
| -------------------------------- | -------------------------------------------------------------------------- |
| **Drag-and-drop reordering**     | Operators rearrange parameter cards, signal lists, or configuration blocks |                     |
| **Dynamic form builder**         | Add/remove/reorder form fields at runtime                                  |
| **Collapsible sections**         | Expand/collapse content areas to manage screen real estate                 |
| **Interactive data tables**      | Sortable, filterable tables with inline editing                            |
| **Real-time data visualization** | Live charts and graphs for RTDE data streams                               |


### Development Acceleration


| Task                                          | Manual                              | Cursor AI                                    |
| --------------------------------------------- | ----------------------------------- | -------------------------------------------- |
| Implement drag-and-drop from scratch          | 4–8 hours (research + code + debug) | ~15 minutes (describe + generate + refine)   |
| Create responsive resizable layout            | 2–4 hours                           | ~10 minutes                                  |
| Add layout persistence with localStorage      | 1–2 hours                           | ~5 minutes                                   |
| Integrate with PolyScope X height constraints | Trial and error                     | Instant — leverages existing Skill knowledge |



## Use Case 2 Summary


| Metric                     | Before           | After                         | Improvement           |
| -------------------------- | ---------------- | ----------------------------- | --------------------- |
| Advanced UI implementation | 4–8 hours        | ~15 minutes                   | **16–32x faster**     |
| Required Angular expertise | Advanced         | Basic (AI handles complexity) | **Lower barrier**     |
| UI feature richness        | Static layouts   | Dynamic, interactive panels   | **Enhanced UX**       |
| Iteration speed            | Hours per change | Minutes per change            | **Rapid prototyping** |
