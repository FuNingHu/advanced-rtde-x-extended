---
name: urcap-sdk-upgrade
description: >-
  Upgrade URCap project SDK dependencies by comparing with a reference project.
  Use when upgrading SDK versions, updating @universal-robots/* packages,
  aligning dependencies with sample-generate or another reference project,
  or when the user mentions SDK upgrade, dependency update, or version bump.
---

# URCap SDK Dependency Upgrade

## When to Use

Apply this skill when:
- Upgrading `@universal-robots/*` SDK packages to a newer version
- Aligning a URCap project's dependencies with a reference project (e.g. `sample-generate`)
- The user mentions: SDK upgrade, dependency update, version bump, align versions

## Prerequisites

Before starting, identify:
1. **Target project**: The URCap project to upgrade (e.g. `advanced-rtde-x-extended`)
2. **Reference project**: The project with the desired SDK versions (default: `sample-generate`)

Both projects should be in the same workspace root.

## Upgrade Workflow

Follow these 6 steps **in order**. After each step, report what changed (old → new) to the user.

---

### Step 1: Compare Backend Dependencies

Read `<target>/*/package.json` and `<reference>/*/package.json` for any backend folders.

Check and update:

| Package | Notes |
|---------|-------|
| `rimraf` | Align version exactly |
| Any other `devDependencies` | Align with reference |

> If the target project has no backend folder, skip this step.

---

### Step 2: Compare Frontend Dependencies

Read `<target>/*-frontend/package.json` and `<reference>/*-frontend/package.json`.

#### dependencies — update these `@universal-robots/*` packages:

| Package | Example |
|---------|---------|
| `@universal-robots/ui-angular-components` | 21.2.25 → 21.3.189 |

#### devDependencies — update these `@universal-robots/*` packages:

| Package | Example |
|---------|---------|
| `@universal-robots/contribution-api` | 21.2.25 → 21.3.131 |
| `@universal-robots/designtokens` | 21.2.25 → 21.3.85 |
| `@universal-robots/ui-models` | 21.2.25 → 21.3.85 |
| `@universal-robots/utilities-units` | 21.2.25 → 21.4.17 |
| `@universal-robots/urcap-utils` | Usually unchanged, verify |

#### Do NOT change:
- `@angular/*`, `rxjs`, `zone.js`, `typescript` — unless they also differ
- Project-specific packages (e.g. `jszip`) — keep as-is

---

### Step 3: Compare Root Directory Dependencies

Read `<target>/package.json` and `<reference>/package.json`.

Check and update:

| Item | What to look for |
|------|-----------------|
| `devDependencies` | Align `rimraf`, `ncp`, `@universal-robots/urcap-utils` versions |
| `install-urcap` script | Update `manifest-spec-*.json` path to match reference |
| `validate-manifest` script | Update `manifest-spec-*.json` path to match reference |

#### Do NOT change:
- `delete-urcap` vendor identifier (project-specific, e.g. `funh`, `urcaps-r-us`)
- Backend-related scripts if the target project has no backend

---

### Step 4: Delete All package-lock.json

Remove every `package-lock.json` in the target project to force a clean reinstall.

```bash
cd <target-project>
find . -name "package-lock.json" -not -path "./.git/*" -delete
```

Also ensure `.gitignore` includes `package-lock.json` so they won't be tracked again.

If any `package-lock.json` was previously committed, run:

```bash
git rm --cached $(git ls-files | grep package-lock.json)
```

---

### Step 5: Remove All NgModule References

Search for `NgModule` usage in the frontend source code and remove/refactor it to standalone components.

```
Grep pattern: NgModule
Scope: <target>/*-frontend/src/**/*.ts
```

For each file found:
1. Remove `@NgModule` decorator and its metadata object
2. Convert components to standalone: add `standalone: true` to `@Component` decorator
3. Move `imports` from the module into each component's `imports` array
4. Delete the module file if it becomes empty
5. Update `main.ts` to bootstrap with `bootstrapApplication()` instead of `platformBrowserDynamic().bootstrapModule()`

> Refer to the reference project's frontend source for the target pattern.
> Always read the reference project's `main.ts` and component files first to understand the expected structure.

---

### Step 6: Run npm install

```bash
cd <target-project>
rm -rf node_modules */node_modules
npm install
```

Verify the install completes without errors. If there are peer dependency warnings, report them to the user.

---

## Post-Upgrade Verification

After all steps, run:

```bash
npm run validate-manifest
npm run build
```

Report any build errors to the user with suggested fixes.

## Output Summary

After completing all steps, provide a summary table:

```markdown
| File | Changes |
|------|---------|
| `*-backend/package.json` | rimraf: X → Y |
| `*-frontend/package.json` | 5 SDK packages updated |
| `package.json` (root) | rimraf + manifest-spec path |
| `.gitignore` | Added package-lock.json |
| `*-frontend/src/**` | NgModule → standalone |
```
