---
phase: 05-architecture-integration-planning
plan: 02
subsystem: ui
tags: [style-dictionary, design-tokens, dtcg, css-custom-properties, component-tokens]

# Dependency graph
requires:
  - phase: 05-architecture-integration-planning
    provides: CONTEXT.md with locked decisions on naming convention, token reduction, CSS property model
provides:
  - Component token naming convention spec (component.variant.state.property)
  - Validated components.json stub with DTCG structure
  - Proven architecture integration with Style Dictionary v1.0 pipeline
  - CSS custom property naming examples and transform chain documentation
affects:
  - phase: 06-button-tokens
  - phase: 07-form-tokens

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Component token naming: component.variant.state.property segment order"
    - "Default state omission: button.primary.background (not button.primary.default.background)"
    - "CSS transform chain: JSON path -> prepend ff -> join with hyphens -> CSS var"
    - "Per-leaf $type declarations in mixed-type groups (never group-level)"
    - "DTCG $description fields must not contain curly-brace notation (parsed as references)"

key-files:
  created:
    - tokens/audit/naming-convention.md
    - tokens/components.json
  modified: []

key-decisions:
  - "Default state omission confirmed: button.primary.background not button.primary.default.background"
  - "DTCG $description fields cannot contain curly-brace token references — Style Dictionary resolves them as token paths"
  - "components.json uses $type on each leaf token (mixed types within button group — color, dimension, shadow)"
  - "Placeholder references use closest existing semantic token with description noting what the final reference will be"

patterns-established:
  - "Per-leaf $type: each leaf token in components.json declares its own $type; no group-level type inheritance"
  - "Static property shortening: button.primary.border-radius (no state) vs button.primary.hover.background (state present)"
  - "Placeholder pattern: reference existing semantic token + $description noting target token to be created in later phase"

requirements-completed: [ARCH-02, ARCH-04]

# Metrics
duration: 5min
completed: 2026-02-23
---

# Phase 05 Plan 02: Component Token Naming Convention and Validated Stub Summary

**Component token naming spec (component.variant.state.property) and validated components.json stub proven to build with Style Dictionary — catching description-field reference parsing edge case**

## Performance

- **Duration:** 5 min
- **Started:** 2026-02-24T00:14:40Z
- **Completed:** 2026-02-24T00:19:40Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments

- Complete naming convention specification covering all locked decisions: segment order, default omission rule, CSS transform chain, static property shortening, type handling, and 9 anti-patterns
- Validated components.json stub with button.primary (default + hover states) and input.text (default state) — all tokens use DTCG reference syntax with explicit leaf-level $type
- Style Dictionary dry-run build confirmed: references resolve, CSS custom properties follow --ff-{component}-{variant}-{state}-{property} pattern exactly
- Discovered and fixed DTCG $description parsing edge case: curly-brace notation in descriptions is treated as token references by Style Dictionary

## Task Commits

Each task was committed atomically:

1. **Task 1: Create naming convention specification** - `2b1e995d` (feat)
2. **Task 2: Create and validate components.json stub** - `591ba855` (feat)

**Plan metadata:** (pending final commit)

## Files Created/Modified

- `tokens/audit/naming-convention.md` - Complete naming convention spec with 6 sections, enumeration tables, examples, and anti-patterns
- `tokens/components.json` - Validated DTCG-format component token stub with button.primary and input.text

## Decisions Made

- DTCG `$description` fields must not contain curly-brace notation (`{token.path}`) — Style Dictionary's reference resolver scans all string fields including descriptions. Use plain text instead (e.g., "color.action.primary-hover" not "{color.action.primary-hover}")
- Placeholder references (for tokens that don't exist yet in semantic.json) use the closest existing semantic token as `$value`, with the `$description` noting what the final reference will be after semantic.json is extended in Phase 6/7
- The `shadow` token type is handled by the Style Dictionary `expandTypesMap` — shadow tokens are expanded to individual sub-properties (`-color`, `-offsetX`, `-offsetY`, etc.) in CSS output. This is expected and correct behavior.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed DTCG $description fields containing curly-brace notation**
- **Found during:** Task 2 (dry-run build validation)
- **Issue:** Original descriptions included notation like `{color.action.primary-border}` to document intended future references. Style Dictionary's reference resolver treats all curly-brace strings in any field as token references, causing 3 "could not be found" build errors.
- **Fix:** Replaced curly-brace notation in descriptions with plain text references (e.g., "color.action.primary-border" without curly braces)
- **Files modified:** tokens/components.json
- **Verification:** Style Dictionary dry-run build passed with zero reference errors
- **Committed in:** 591ba855 (Task 2 commit)

---

**Total deviations:** 1 auto-fixed (Rule 1 - bug during build validation)
**Impact on plan:** Fix required for build pipeline compatibility. No scope creep. The pattern (no curly braces in descriptions) is now documented in naming-convention.md's anti-patterns section.

## Issues Encountered

- Style Dictionary npm dependencies were not installed in forms-flow-theme (no node_modules). Installed with `npm install` to enable dry-run build validation. This is a pre-existing environment state, not caused by this plan.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Phase 6 (button tokens) implementer can follow `tokens/audit/naming-convention.md` without referencing CONTEXT.md
- `tokens/components.json` is the target file to expand in Phase 6 — replace stub button.primary with full token set
- `tokens/semantic.json` will need new tokens (color.action.primary-hover, color.action.primary-border, etc.) in Phase 6 — the placeholder descriptions in components.json document exactly which tokens are needed
- Style Dictionary build pipeline confirmed working with 3-source file configuration (core + semantic + components)

---
*Phase: 05-architecture-integration-planning*
*Completed: 2026-02-23*
