# advanced-rtde-x-extended SDK Dependency Upgrade

> Reference project: `sample-generate` (PolyScope X SDK 0.20.37)  
> Date: 2026-03-25

---

## 1. Checklist

| File | What to check | Modified |
|------|---------------|:--------:|
| `advanced-rtde-frontend/package.json` | `@universal-robots/*` SDK versions | ✅ Yes |
| `package.json` (root) | `devDependencies` versions | ✅ Yes |
| `package.json` (root) | `manifest-spec` reference path | ✅ Yes |
| `advanced-rtde-backend/package.json` | `devDependencies` versions | ✅ Yes |
| `.gitignore` | Missing ignore rules | ✅ Yes |

---

## 2. Changes

### 2.1 Frontend SDK Dependencies (`advanced-rtde-frontend/package.json`)

#### dependencies

| Package | Old Version | New Version |
|---------|:----------:|:-----------:|
| `@universal-robots/ui-angular-components` | 21.2.25 | **21.3.189** |

#### devDependencies

| Package | Old Version | New Version |
|---------|:----------:|:-----------:|
| `@universal-robots/contribution-api` | 21.2.25 | **21.3.131** |
| `@universal-robots/designtokens` | 21.2.25 | **21.3.85** |
| `@universal-robots/ui-models` | 21.2.25 | **21.3.85** |
| `@universal-robots/utilities-units` | 21.2.25 | **21.4.17** |
| `@universal-robots/urcap-utils` | 2.1.2 | 2.1.2 (unchanged) |

#### Unchanged dependencies (already aligned with sample-generate)

- `@angular/*`: 21.0.8
- `@angular/cdk`: 21.0.6
- `@ngx-translate/core`: 17.0.0
- `ngx-translate-multi-http-loader`: 20.0.0
- `rxjs`: ^7.3.0
- `zone.js`: 0.16.0
- `typescript`: 5.9.3
- All Angular / ESLint / Karma toolchain versions are already consistent

### 2.2 Root Build Scripts & Dependencies (`package.json`)

| Item | Old Value | New Value |
|------|-----------|-----------|
| `rimraf` | 3.0.2 | **5.0.7** |
| `install-urcap` path | `../manifest-spec-19.10.24.json` | `../manifest-spec-19.10.31.json` |
| `validate-manifest` path | `../manifest-spec-19.10.24.json` | `../manifest-spec-19.10.31.json` |

> `@universal-robots/urcap-utils` (2.1.2), `cpy-cli` (3.1.1), `ncp` (2.0.0) are unchanged.

### 2.3 Backend Dependencies (`advanced-rtde-backend/package.json`)

| Package | Old Version | New Value |
|---------|:----------:|:-----------:|
| `rimraf` | ^3.0.2 | **5.0.7** |

### 2.4 `.gitignore` Additions

New entry:

- `package-lock.json` — lock files excluded from version control

> `target/` and `dist/` were already present in the original `.gitignore`.

---

## 3. Post-Upgrade Steps

```bash
# 1. Navigate to the project directory
cd advanced-rtde-x-extended

# 2. Remove previously tracked lock files
git rm --cached advanced-rtde-backend/package-lock.json advanced-rtde-frontend/package-lock.json

# 3. Clean old dependencies and reinstall
rm -rf node_modules advanced-rtde-frontend/node_modules advanced-rtde-backend/node_modules
npm install

# 4. Verify manifest validation passes
npm run validate-manifest

# 5. Build the project
npm run build
```

---

## 4. Notes

- The vendor identifier `urcaps-r-us` in the `delete-urcap` script is project-specific and was **not** changed to match sample-generate's `urplus`.
- The frontend-specific package `jszip` (3.10.1) is not present in sample-generate — it was kept as-is since it is project-specific.
- If any APIs have breaking changes, consult the [PolyScope X SDK changelog](https://docs.universal-robots.com).
