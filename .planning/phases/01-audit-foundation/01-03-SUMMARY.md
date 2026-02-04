---
phase: 01-audit-foundation
plan: 03
subsystem: design-system
tags: [w3c-dtcg, design-tokens, json-schema, validation, specification]

# Dependency graph
requires:
  - phase: 01-audit-foundation
    plan: 01
    provides: theme-audit.json with 465 SCSS variables and 137 CSS custom properties
provides:
  - W3C DTCG token structure specification (dtcg-spec.md)
  - Naming conventions for 8 token categories
  - Validated example token files (core + semantic)
  - Reference syntax validation
  - Format contract for Phase 2 extraction
affects: [02-extraction, design-tokens, token-validation]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - W3C DTCG format with $value, $type, $description properties
    - Two-tier token architecture (core primitive + semantic purpose-based)
    - Reference syntax using {group.subgroup.token} notation
    - Type inheritance at group level
    - Shadow object format with color, offsetX, offsetY, blur, spread

key-files:
  created:
    - tokens/audit/dtcg-spec.md
    - tokens/audit/example-core.json
    - tokens/audit/example-semantic.json
  modified: []

key-decisions:
  - "Exactly two token files at project root: tokens/core.json and tokens/semantic.json (no subdirectories)"
  - "ff- prefix for all tokens via top-level group structure"
  - "Keep Bootstrap semantic names (primary, secondary, success, danger) unchanged"
  - "Color shades use 100-900 numeric scale, spacing uses zero-padded numeric (025, 050, 100)"
  - "Shadow tokens use DTCG object format, fontWeight values are numbers not strings"
  - "v8 design system values take precedence over legacy theme where conflicts exist"

patterns-established:
  - "DTCG validation: JSON syntax, required properties, reference resolution, type-specific formats, no reserved characters, no circular references"
  - "Token naming: kebab-case, no dots/braces/dollars in names, dot notation via JSON nesting"
  - "Reference validation: verify all {ff.*} references resolve to existing core tokens"

# Metrics
duration: 3min
completed: 2026-02-04
---

# Phase 1 Plan 3: DTCG Token Specification Summary

**W3C DTCG format specification with validated two-tier token examples (35 core primitives + 33 semantic references) using real theme values**

## Performance

- **Duration:** 3 min
- **Started:** 2026-02-04T23:34:52Z
- **Completed:** 2026-02-04T23:37:52Z
- **Tasks:** 2
- **Files created:** 3

## Accomplishments

- Comprehensive DTCG specification document (7 sections, 342 lines) defining complete format contract for Phase 2 extraction
- Validated example token files with 100% coverage of 8 token categories (color, spacing, font-family, font-size, font-weight, radius, shadow, duration)
- All 33 semantic token references validated to resolve to core tokens
- Naming conventions established for all categories with Bootstrap name preservation

## Task Commits

Each task was committed atomically:

1. **Task 1: Write DTCG structure specification with naming conventions** - `1b28100f` (docs)
2. **Task 2: Create and validate example DTCG token files using real theme values** - `cc9fe86a` (feat)

## Files Created/Modified

- `tokens/audit/dtcg-spec.md` - Complete W3C DTCG format specification with 7 sections: file structure, DTCG format rules, naming conventions, type inheritance, shadow format, v8 vs legacy handling, validation requirements
- `tokens/audit/example-core.json` - 35 primitive tokens across 8 categories using real values from theme audit (#253DF4, #006621, 0.25rem, Figtree, etc.)
- `tokens/audit/example-semantic.json` - 33 semantic tokens with reference syntax pointing to core tokens

## Decisions Made

**File Structure:**
- Locked to exactly two files: `tokens/core.json` and `tokens/semantic.json`
- No subdirectories (no `tokens/core/` or `tokens/semantic/`)
- No per-category splits (no `colors.json` or `spacing.json`)

**Naming Conventions:**
- All tokens under `ff` top-level group
- kebab-case for all token names
- Bootstrap semantic names preserved (primary, secondary, success, danger)
- Color shades: 100-900 numeric scale (100 = lightest, 500 = base, 900 = darkest)
- Spacing: zero-padded numeric (025, 050, 100, 200) for core, t-shirt sizes (xs, sm, md, lg, xl) for semantic

**Format Specifications:**
- Shadow tokens use object format (color, offsetX, offsetY, blur, spread) not CSS string format
- fontWeight values are numbers (400, 500, 600, 700) not strings
- Type inheritance allowed at group level
- Reference syntax: `{ff.group.subgroup.token}` using dot-separated path

**v8 Precedence:**
- When dual values exist (legacy vs v8), v8 values take precedence in core tokens
- Legacy values documented in $description if significantly different

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## Validation Results

**Example token files passed all 7 validation checks:**

1. ✓ Valid JSON syntax
2. ✓ Required properties: Every token has $value and $type (explicit or inherited)
3. ✓ Reference resolution: All 33 references resolve to existing core tokens
4. ✓ No reserved characters: No $, {, }, or . in token names
5. ✓ Type-specific format: fontWeight are numbers, shadows are objects
6. ✓ Consistent naming: All tokens use kebab-case under ff prefix
7. ✓ No circular references: Reference graph validated

**Token Counts:**
- Core tokens: 35 across 8 categories
- Semantic tokens: 33 with 100% reference coverage
- Reference validation: 33/33 resolved successfully

**Category Coverage:**
- ✓ color (9 tokens in core, 6 in semantic)
- ✓ spacing (5 tokens in core, 5 in semantic)
- ✓ font-family (2 tokens in core, 2 in semantic)
- ✓ font-size (5 tokens in core, 5 in semantic)
- ✓ font-weight (4 tokens in core, 4 in semantic)
- ✓ radius (4 tokens in core, 4 in semantic)
- ✓ shadow (3 tokens in core, 3 in semantic)
- ✓ duration (3 tokens in core, 3 in semantic)

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

**Phase 2 (Token Extraction) is ready to proceed:**

✓ Format contract established and documented (dtcg-spec.md)
✓ Naming conventions defined for all categories
✓ Example tokens validated to prove format works
✓ Reference syntax validated
✓ Type-specific formats documented (shadow objects, fontWeight numbers)
✓ Real values from theme audit confirmed to work in DTCG format

**Format Contract Details:**
- Exact file structure: 2 files at tokens/ root
- All DTCG reserved properties documented ($value, $type, $description)
- Reference syntax validated with 33 working examples
- Shadow RGBA → object conversion pattern established
- Type inheritance pattern demonstrated

**No Blockers:**
- All validation rules clearly defined
- Real theme values confirmed compatible with DTCG format
- Example files provide reference implementation for extraction scripts

**Handoff to Phase 2:**
Phase 2 extraction scripts can read dtcg-spec.md sections 1-7 for complete implementation requirements. Example files provide test cases to validate extraction output matches expected format.

---
*Phase: 01-audit-foundation*
*Completed: 2026-02-04*
