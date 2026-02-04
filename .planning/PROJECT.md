# Design Token Extraction

## What This Is

A design token audit and extraction project for the forms-flow-ai-micro-front-ends codebase. The goal is to document existing design values (colors, spacing, typography, border radius, shadows) from shared styles and export them as W3C DTCG-formatted JSON files for import into Figma via Token Studio. This creates the foundation for a design-to-code pipeline using Figma MCP and Claude.

## Core Value

Accurate extraction of design values that actually exist in the codebase — reflecting reality before restructuring, enabling Figma to become the source of truth for future design iterations.

## Requirements

### Validated

- ✓ Centralized theme layer exists at `forms-flow-theme/scss` — existing
- ✓ CSS variables used for theming — existing
- ✓ SCSS-based styling with Bootstrap 5 foundation — existing
- ✓ React Bootstrap and Material-UI component libraries in use — existing

### Active

- [ ] Audit shared styles in `forms-flow-theme` for design token candidates
- [ ] Extract color tokens (brand, semantic, state colors)
- [ ] Extract spacing tokens (margins, padding, gaps)
- [ ] Extract typography tokens (font families, sizes, weights, line heights)
- [ ] Extract border radius tokens
- [ ] Extract shadow tokens
- [ ] Generate W3C DTCG-formatted JSON files for each token category
- [ ] Document audit findings (what was found, naming patterns, gaps)
- [ ] Organize tokens to match existing codebase naming conventions

### Out of Scope

- Refactoring codebase to consume generated tokens — future phase
- Component-level style extraction (only shared/common styles) — reduces scope
- Creating primitive + semantic token hierarchy — match current naming first
- Automated sync between Figma and codebase — future tooling concern

## Context

**Codebase structure:**
- Micro-frontend architecture with 7 modules sharing `@formsflow/theme`
- Theme layer at `/forms-flow-theme/scss` provides centralized CSS variables
- Bootstrap 5 is the CSS framework foundation
- SCSS used throughout with variables and mixins
- React Bootstrap and Material-UI provide component styling

**Design system context:**
- Recent design language update driving standardization effort
- Enterprise product requiring professional, cohesive interface
- Figma is the design tool; Token Studio plugin for variable management
- End goal: Figma MCP + Claude for production-ready component generation

**Token format:**
- W3C Design Tokens Community Group (DTCG) specification
- Uses `$value` and `$type` prefixes (not `value`/`type`)
- Compatible with Token Studio import

## Constraints

- **Format**: W3C DTCG JSON specification — required for Token Studio compatibility
- **Scope**: Shared styles only (`forms-flow-theme`) — not component-specific styles
- **Naming**: Mirror existing codebase conventions — document reality before restructuring
- **Output**: JSON files + documentation — no code changes in this phase

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Focus on forms-flow-theme only | Shared styles have highest impact; component styles vary | — Pending |
| Match existing naming | Reduces translation friction; restructure later | — Pending |
| W3C DTCG format | Industry standard, Token Studio native support | — Pending |
| Documentation alongside JSON | Understand what exists before importing to Figma | — Pending |

---
*Last updated: 2026-02-03 after initialization*
