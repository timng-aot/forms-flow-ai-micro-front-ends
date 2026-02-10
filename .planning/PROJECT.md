# Design Token Extraction

## What This Is

A design token system for forms-flow-ai-micro-front-ends that extracts existing SCSS design values into W3C DTCG-formatted JSON tokens, transforms them via Style Dictionary into CSS custom properties, and enables import into Figma via Token Studio. This creates a bidirectional design-to-code pipeline using Figma MCP and Claude.

## Core Value

Accurate extraction of design values that actually exist in the codebase -- reflecting reality before restructuring, enabling Figma to become the source of truth for future design iterations.

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

(No active requirements -- next milestone not yet defined)

### Out of Scope

- Refactoring codebase to consume generated tokens -- v2 scope
- Component-level token layer (3-tier hierarchy) -- v2 scope
- Multi-theme support (light/dark) -- not in codebase yet
- Figma-to-code generation -- downstream separate project
- Token versioning and governance -- v2 scope
- Automated Figma sync via Token Studio GitHub integration -- v2 scope
- CI/CD pipeline for token validation -- v2 scope

## Context

**Current state (v1.0 shipped):**
- 192 W3C DTCG tokens (160 core + 32 semantic) across 9 categories
- Automated Python extraction pipeline (scripts/extract-tokens.py)
- Style Dictionary v5.3.0 build pipeline (npm run build:tokens)
- 273 CSS custom properties generated (216 core + 57 semantic)
- Token Studio import validated by human testing
- 1,356 lines of documentation (methodology, naming, Figma import, gaps)
- Tech stack: Python (extraction), Node.js/Style Dictionary (build), SCSS (source)

**Codebase structure:**
- Micro-frontend architecture with 7 modules sharing `@formsflow/theme`
- Theme layer at `/forms-flow-theme/scss` provides centralized CSS variables
- Bootstrap 5 foundation with dual design systems (legacy + v8)
- v8 design system takes precedence where conflicts exist

**Known gaps:**
- 18 component-specific hardcoded values not yet tokenized (documented in gaps-and-coverage.md)
- 41.2% component coverage from shared theme (33 exist, 29 close match, 18 missing)
- forms-flow-admin has most hardcoded values (51 unique) -- primary migration target

## Constraints

- **Format**: W3C DTCG JSON specification -- required for Token Studio compatibility
- **Scope**: Shared styles only (`forms-flow-theme`) -- not component-specific styles
- **Naming**: ff- prefix for all tokens, kebab-case, Bootstrap semantic names preserved
- **Files**: Two token files (tokens/core.json + tokens/semantic.json)
- **Build**: Style Dictionary in forms-flow-theme/config/ with ES module support

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

---
*Last updated: 2026-02-10 after v1.0 milestone*
