# Design Token System

## What This Is

A design token system for forms-flow-ai-micro-front-ends that provides component-level tokens for buttons and forms, built on top of the v1.0 core primitives extracted from SCSS. Tokens use CSS property naming and are structured for practical use in both code and Figma via Token Studio.

## Core Value

Usable component tokens that map cleanly between code (CSS properties) and Figma components -- fewer, well-named tokens that designers and developers can actually adopt.

## Current Milestone: v2.0 Component Token System (Buttons & Forms)

**Goal:** Create component-level tokens for buttons and forms that reduce the v1.0 token set to what these components actually use, with CSS property naming that maps to Figma component properties.

**Target features:**
- Audit button and form SCSS to identify which v1.0 core tokens are actually used
- Create component-level tokens (e.g. button.primary.background, input.border.color)
- Reduce core token set to primitives these components reference
- Align token naming with CSS properties (background, border, color, shadow)
- Update Style Dictionary pipeline for component token output
- Update Figma Token Studio import for component-level structure

## Requirements

### Validated

- ✓ Centralized theme layer exists at `forms-flow-theme/scss` -- existing
- ✓ CSS variables used for theming -- existing
- ✓ SCSS-based styling with Bootstrap 5 foundation -- existing
- ✓ React Bootstrap and Material-UI component libraries in use -- existing
- ✓ Audit shared styles in `forms-flow-theme` for design token candidates -- v1.0
- ✓ Extract color tokens (65 primitive + 10 semantic) -- v1.0
- ✓ Extract spacing tokens (12 primitive + 5 semantic) -- v1.0
- ✓ Extract typography tokens (25 primitive + 6 semantic) -- v1.0
- ✓ Extract border radius tokens (19 primitive + 4 semantic) -- v1.0
- ✓ Extract shadow tokens (14 primitive + 7 semantic) -- v1.0
- ✓ Generate W3C DTCG-formatted JSON files (core.json + semantic.json) -- v1.0
- ✓ Document audit findings, naming patterns, and gaps -- v1.0
- ✓ Organize tokens to match existing codebase naming conventions -- v1.0
- ✓ Style Dictionary build pipeline with CSS custom property output -- v1.0
- ✓ Token Studio import guide with human-verified Figma workflow -- v1.0

### Active

- [ ] Component-level tokens for buttons (all variants)
- [ ] Component-level tokens for forms (inputs, selects, checkboxes, radios)
- [ ] Reduced core token set scoped to button/form usage
- [ ] CSS property naming convention (background, border, color, shadow)
- [ ] Updated Style Dictionary pipeline for component tokens
- [ ] Updated Figma Token Studio import

### Out of Scope

- Full codebase refactoring to consume generated tokens -- future scope
- Component tokens beyond buttons & forms -- v2.0 proves the pattern first
- Multi-theme support (light/dark) -- not in codebase yet
- Figma-to-code generation -- downstream separate project
- Token versioning and governance -- future scope
- Automated Figma sync via Token Studio GitHub integration -- future scope
- CI/CD pipeline for token validation -- future scope
- Figma property naming model (fill, stroke, effect) -- using CSS model instead

## Context

**v1.0 foundation (shipped 2026-02-10):**
- 192 W3C DTCG tokens (160 core + 32 semantic) across 9 categories
- Style Dictionary v5.3.0 build pipeline (npm run build:tokens)
- 273 CSS custom properties generated with --ff- prefix
- Token Studio import validated by human testing

**v1.0 pain points driving v2.0:**
- Too many tokens -- 192 is overwhelming, hard to know which to use for a given component
- No component-level mapping -- core/semantic tokens don't tell you what a button's primary background is
- Naming confusion -- token names don't map to component properties in Figma
- Figma adoption impractical without component-level structure

**Codebase structure:**
- Micro-frontend architecture with 7 modules sharing `@formsflow/theme`
- Theme layer at `/forms-flow-theme/scss` provides centralized CSS variables
- Bootstrap 5 foundation with `$prefix: "ff-"` generating --ff- CSS custom properties
- Dual design systems (legacy + v8); v8 takes precedence
- Button SCSS: `scss/v8-scss/_button.scss`, `scss/_button.scss`
- Form SCSS: `scss/v8-scss/_checkbox.scss`, `scss/v8-scss/_radio.scss`, `scss/v8-scss/_selectDropdown.scss`, `scss/v8-scss/_search.scss`, `scss/v8-scss/_urlInput.scss`, `scss/inputBox.scss`, `scss/_forms.scss`

**Figma state:**
- Preliminary component standardization underway (buttons & forms)
- Token Studio import working from v1.0 merged token file
- Component library being built alongside token organization

## Constraints

- **Format**: W3C DTCG JSON specification -- required for Token Studio compatibility
- **Scope**: Buttons and forms only -- prove the component token pattern before expanding
- **Naming**: CSS property model (background, border, color, shadow) with ff- prefix
- **Foundation**: v1.0 core tokens as primitives; component tokens reference them
- **Build**: Style Dictionary v5.3.0 in forms-flow-theme/ with ES module support
- **Figma**: Must work with Token Studio free tier (merged file approach from v1.0)

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Focus on forms-flow-theme only | Shared styles have highest impact; component styles vary | ✓ Good -- 192 tokens extracted successfully |
| Match existing naming with ff- prefix | Reduces translation friction; consistent CSS variable namespacing | ✓ Good -- all tokens use --ff- prefix |
| W3C DTCG format | Industry standard, Token Studio native support | ✓ Good -- validated by Figma import |
| Two-file structure (core + semantic) | Enables theme switching, clear primitive/semantic separation | ✓ Good -- references resolve correctly |
| Python for extraction | Captures raw SCSS expressions, not just computed values | ✓ Good -- 602 values extracted with expressions |
| Style Dictionary v5 for build | DTCG native support, Token Studio integration | ✓ Good -- 273 CSS vars generated |
| Pre-compute blend expressions | Clean hex values for Figma import, no SCSS runtime needed | ✓ Good -- 24 expressions resolved |
| Merged token file for Figma | Token Studio free tier can't resolve cross-file references | ✓ Good -- human-verified import |
| Documentation split (quick-start + methodology) | Different audiences: returning users vs maintainers | ✓ Good -- actionable and comprehensive |
| Narrow v2.0 to buttons & forms | Proves component token pattern on highest-touch components before expanding | -- Pending |
| CSS property naming over Figma property naming | Code is source of truth; Figma adapts to code conventions | -- Pending |
| Reduce core tokens to component usage | 192 tokens is overwhelming; only include what buttons & forms reference | -- Pending |

---
*Last updated: 2026-02-10 after v2.0 milestone started*
