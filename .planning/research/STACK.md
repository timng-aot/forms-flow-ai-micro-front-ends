# Stack Research: Component-Level Design Tokens

**Domain:** Component-level design tokens for buttons and forms
**Researched:** 2026-02-10
**Confidence:** HIGH

## Executive Summary

v2.0 requires **zero new dependencies**. The existing v1.0 stack (Style Dictionary v5.3.0 + @tokens-studio/sd-transforms v2.0.3 + Token Studio free tier) fully supports 3-tier token hierarchies. This milestone adds a third token file (`tokens/component.json`) and extends the existing build pipeline with component-specific naming transforms. No breaking changes to v1.0 infrastructure.

## Recommended Stack

### Core Technologies (No Changes)

| Technology | Version | Purpose | Why No Change Needed |
|------------|---------|---------|---------------------|
| Style Dictionary | v5.3.0 | Token build pipeline | Already handles multi-file sources and reference resolution for 3-tier hierarchies. Supports arbitrary nesting and custom transforms. |
| @tokens-studio/sd-transforms | ^2.0.3 | DTCG token transforms | Already includes all necessary transforms for component tokens (ts/resolveMath, ts/color/css/hexrgba, ts/shadow/innerShadow). Version 2.0.3 compatible with Style Dictionary v5. |
| Token Studio (Figma Plugin) | Free Tier | Figma token import | Free tier supports unlimited token sets. v1.0 merge script pattern (tokens-figma.json) extends to 3 files seamlessly. |

### Supporting Libraries (No Changes)

| Library | Version | Purpose | Status |
|---------|---------|---------|--------|
| W3C DTCG Format | 2025.10 spec | Token format standard | Already adopted in v1.0. Component tokens use same format. |
| Bootstrap 5 | ^5.3.3 | CSS foundation | Already generates --ff- prefixed CSS custom properties. Component tokens reference these. |

## What's Changing (Configuration Only)

### 1. New Token File Structure

```
tokens/
├── core.json           # [NO CHANGE] Primitive values
├── semantic.json       # [NO CHANGE] Purpose-based tokens
└── component.json      # [NEW] Component-specific tokens for buttons & forms
```

**Implementation:** Add `component.json` with CSS property-based naming convention (see Naming Conventions section).

### 2. Extended Build Pipeline

```bash
# New build command in forms-flow-theme/package.json
"build:tokens:component": "node config/style-dictionary.config.js ../../tokens/component.json component-tokens.css"

# Updated composite command
"build:tokens": "npm run build:tokens:precompute && npm run build:tokens:core && npm run build:tokens:semantic && npm run build:tokens:component && npm run build:tokens:figma"
```

**Implementation:** Style Dictionary config already supports this pattern. Semantic token build (lines 148-154 of existing config) demonstrates the multi-source reference resolution pattern needed for component tokens.

### 3. Style Dictionary Configuration Pattern

The existing `style-dictionary.config.js` (lines 148-154) shows the pattern for component tokens:

```javascript
// For component tokens, include both core and semantic for reference resolution
const isComponentBuild = sourcePath.includes('component');
const sources = isComponentBuild
  ? [
      resolve(__dirname, '../../tokens/core.json'),
      resolve(__dirname, '../../tokens/semantic.json'),
      absoluteSourcePath  // component.json
    ]
  : isSemanticBuild
    ? [resolve(__dirname, '../../tokens/core.json'), absoluteSourcePath]
    : [absoluteSourcePath];
```

**Rationale:** Component tokens reference semantic tokens (e.g., `{color.primary}`), which in turn reference core tokens (e.g., `{ff.color.indigo-100}`). Style Dictionary resolves this chain when all source files are loaded.

### 4. Figma Merge Script Extension

Extend `tokens/scripts/merge-for-figma.js` to include `component.json`:

```javascript
// Current (v1.0): merges core.json + semantic.json
// v2.0: merges core.json + semantic.json + component.json
```

**Rationale:** Token Studio free tier can't resolve cross-file references. The merge script creates a single file where all references are resolvable.

## CSS Property Naming Convention for Component Tokens

Component tokens use a CSS property-based naming structure that mirrors the actual CSS properties they control. This is a departure from the semantic naming in v1.0 and aligns with industry best practices for component-level tokens.

### Naming Pattern

```
{component}-{css-property}-{variant}-{state}
```

### Examples

**Button Background Colors:**
```json
{
  "button": {
    "background": {
      "primary-default": { "$value": "{color.primary}", "$type": "color" },
      "primary-hover": { "$value": "{color.primary-hover}", "$type": "color" },
      "primary-active": { "$value": "{color.primary-active}", "$type": "color" },
      "primary-disabled": { "$value": "{color.disabled}", "$type": "color" },
      "secondary-default": { "$value": "{color.secondary}", "$type": "color" }
    }
  }
}
```

**Form Border:**
```json
{
  "input": {
    "border": {
      "default": { "$value": "{border.default}", "$type": "border" },
      "focus": { "$value": "{border.focus}", "$type": "border" },
      "error": { "$value": "{border.error}", "$type": "border" }
    }
  }
}
```

**CSS Output:**
```css
:root {
  --ff-button-background-primary-default: var(--ff-color-primary);
  --ff-button-background-primary-hover: var(--ff-color-primary-hover);
  --ff-input-border-default: var(--ff-border-default);
  --ff-input-border-focus: var(--ff-border-focus);
}
```

### Why This Pattern?

**Maps to CSS properties:** Developers immediately understand that `button-background-*` controls the `background` property, not padding or border.

**Self-documenting:** `button-background-primary-hover` is clearer than `button-color-primary-light` when reading component code.

**Follows industry standards:** Design systems like GitHub Primer, Shopify Polaris, and Mozilla Firefox use this CSS property-based approach for component tokens.

**Reduces cognitive load:** Designers and developers think in CSS properties (background, border, color, shadow), not abstract semantic names.

## Token Studio Structuring for Component Tokens

### Token Set Structure (Free Tier)

Token Studio free tier supports unlimited token sets. Recommended structure:

```
Token Sets:
├── core          # [EXISTING] Primitive values
├── semantic      # [EXISTING] Purpose-based tokens
└── component     # [NEW] Component-specific tokens
```

**Configuration:** Each set maps to one JSON file. The merge script combines all three into `tokens-figma.json` for import.

### Cross-File References in Merged Format

Token Studio free tier limitation: Can't resolve references across separate token set files during import.

**v1.0 Solution (Already Validated):** The `merge-for-figma.js` script combines all files into a single JSON where Token Studio can resolve references:

```json
{
  "core": { /* core tokens */ },
  "semantic": { /* semantic tokens */ },
  "component": { /* component tokens */ }
}
```

**v2.0 Extension:** Add component tokens to the same merge pattern. No structural changes needed.

### Token Studio Import Workflow (No Changes)

1. Build tokens: `npm run build:tokens` (generates `tokens-figma.json`)
2. Open Figma → Plugins → Token Studio
3. Import → Select `tokens/dist/tokens-figma.json`
4. Token Studio loads all three token sets
5. References resolve within the merged file

## 3-Tier Token Hierarchy Configuration

### Hierarchy Structure

```
Core Tokens (Primitive)
    ↓ references
Semantic Tokens (Purpose)
    ↓ references
Component Tokens (Specific)
    ↓ consumed by
Component CSS
```

### Style Dictionary Reference Resolution

Style Dictionary's `outputReferences: true` option (already enabled in v1.0 config, line 199) generates CSS with `var()` references:

```css
/* Without outputReferences */
--ff-button-background-primary-default: #3248f4;

/* With outputReferences (current v1.0 behavior) */
--ff-button-background-primary-default: var(--ff-color-primary);
```

**Benefit:** Changing `--ff-color-primary` updates all component tokens that reference it, enabling runtime theme switching.

### Filter Pattern for Component Builds

The existing v1.0 config (lines 203-209) shows how to filter tokens by source file:

```javascript
filter: isSemanticBuild
  ? (token) => token.filePath && token.filePath.includes('semantic.json')
  : undefined
```

**v2.0 Extension:** Apply same pattern for component builds to avoid re-outputting core/semantic tokens:

```javascript
filter: isComponentBuild
  ? (token) => token.filePath && token.filePath.includes('component.json')
  : isSemanticBuild
    ? (token) => token.filePath && token.filePath.includes('semantic.json')
    : undefined
```

## What NOT to Change

| DO NOT Change | Why | Instead |
|---------------|-----|---------|
| Style Dictionary version | v5.3.0 is stable and working. v2.0 is configuration-only. | Keep v5.3.0. |
| @tokens-studio/sd-transforms version | v2.0.3 is latest and compatible with SD v5. | Keep ^2.0.3. |
| v1.0 token files (core.json, semantic.json) | Component tokens reference these. Breaking changes cascade. | Add component.json, don't modify existing files. |
| --ff- prefix convention | Used across 192 existing tokens and Bootstrap config. | Continue --ff- prefix for component tokens. |
| DTCG validation preprocessor | Already validates $type and token names. Works for component tokens. | No changes needed. |
| Build output directory (tokens/dist/) | Established in v1.0, referenced in documentation. | Keep same directory. |

## Installation (No New Packages Required)

```bash
# v2.0 requires ZERO new installations
# All dependencies already present from v1.0:
# - style-dictionary: ^5.3.0
# - @tokens-studio/sd-transforms: ^2.0.3
```

## Component Token Scope for v2.0

### In Scope (Buttons & Forms)

Component tokens will be created for:

**Button:**
- `button.background.{variant}-{state}` (e.g., primary-default, secondary-hover)
- `button.border.{variant}-{state}`
- `button.color.{variant}-{state}` (text color)
- `button.shadow.{variant}-{state}`

**Form Controls (input, select, textarea, checkbox, radio):**
- `input.background.{state}` (e.g., default, focus, disabled)
- `input.border.{state}`
- `input.color.{state}` (text color)
- `input.shadow.{state}` (focus rings, validation shadows)

### Out of Scope

- Typography component tokens (buttons/forms use semantic typography tokens)
- Layout component tokens (spacing uses semantic spacing tokens)
- Icon component tokens (future milestone)
- Animation/transition tokens (future milestone)

## Alternatives Considered

| Recommended | Alternative | Why Not |
|-------------|-------------|---------|
| CSS property-based naming (button-background-primary) | Semantic naming (button-primary-bg-color) | CSS property-based is industry standard (GitHub Primer, Shopify Polaris). Maps directly to CSS properties developers write. |
| Single component.json file | Separate button.json + form.json | Adds unnecessary file splits for only 2 component types. Single file easier to manage. |
| Extend v1.0 merge script | Token Studio Pro (multi-file support) | Free tier proven sufficient in v1.0. No budget for Pro. Merge script works. |
| Keep --ff- prefix | New --component- prefix | Breaking change. --ff- already established for 192 tokens. Consistency matters. |

## Version Compatibility

| Package | Version | Compatible With | Notes |
|---------|---------|-----------------|-------|
| style-dictionary | ^5.3.0 | @tokens-studio/sd-transforms@^2.0.3 | Verified in v1.0 milestone. No issues. |
| @tokens-studio/sd-transforms | ^2.0.3 | style-dictionary@^5.0.0+ | Latest version. Released Dec 2025. Peer dependency satisfied. |
| Bootstrap | ^5.3.3 | Custom --ff- prefix config | Generates --ff- CSS custom properties. No conflicts. |

## Confidence Assessment

| Technology | Confidence | Source | Notes |
|------------|------------|--------|-------|
| Style Dictionary 3-tier support | HIGH | Official docs, v1.0 validated | Semantic build already demonstrates multi-file reference resolution. |
| @tokens-studio/sd-transforms | HIGH | npm package page, GitHub releases | Latest v2.0.3 confirmed. Compatible with SD v5. |
| Token Studio free tier | HIGH | v1.0 validated, official docs | Unlimited token sets confirmed. Merge script pattern proven. |
| CSS property naming convention | MEDIUM | Multiple design systems (GitHub, Shopify), blog posts | Industry standard but not W3C specified. |
| Component token DTCG format | HIGH | W3C DTCG spec 2025.10, Style Dictionary DTCG docs | Same format as core/semantic tokens. No ambiguity. |

## Sources

### High Confidence (Official Documentation)
- [Style Dictionary - Design Tokens](https://styledictionary.com/info/tokens/) — Token organization, CTI pattern (optional), multi-file sources
- [Style Dictionary - DTCG](https://styledictionary.com/info/dtcg/) — W3C DTCG format support
- [@tokens-studio/sd-transforms - npm](https://www.npmjs.com/package/@tokens-studio/sd-transforms) — Version confirmation, peer dependencies
- [GitHub: tokens-studio/sd-transforms](https://github.com/tokens-studio/sd-transforms) — Transform documentation, component token examples
- [W3C Design Tokens Community Group](https://www.w3.org/community/design-tokens/) — DTCG specification status (stable 2025.10)
- [Design Tokens specification reaches first stable version](https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/) — DTCG 2025.10 announcement

### Medium Confidence (Industry Patterns)
- [Best Practices For Naming Design Tokens, Components And Variables — Smashing Magazine](https://www.smashingmagazine.com/2024/05/naming-best-practices/) — CSS property-based naming for component tokens
- [Naming Tokens in Design Systems | Nathan Curtis | EightShapes](https://medium.com/eightshapes-llc/naming-tokens-in-design-systems-9e86c7444676) — 3-tier hierarchy patterns
- [Component-Specific Design Tokens – Cloud Four](https://cloudfour.com/thinks/component-specific-design-tokens/) — Button/form component token examples
- [Design Systems & Design Tokens Complete Guide - design.dev](https://design.dev/guides/design-systems/) — 3-tier hierarchy (global → alias → component)
- [Button States: Communicate Interaction - NN/G](https://www.nngroup.com/articles/button-states-communicate-interaction/) — State naming (default, hover, active, focus, disabled)

### Low Confidence (Validation Needed)
- [Token Studio Plugin for Figma | Tokens Studio](https://docs.tokens.studio) — Free tier token set limits (blocked by 403, couldn't verify)
- Token Studio free tier cross-file reference limitations — Inferred from v1.0 merge script necessity, not explicitly documented

---

**Stack research for:** Component-level design tokens (buttons & forms)
**Researched:** 2026-02-10
**Confidence:** HIGH (existing stack fully capable, configuration-only changes)
