---
phase: 05-architecture-integration-planning
plan: 01
subsystem: ui
tags: [design-tokens, dtcg, scss, token-audit, component-tokens]

requires:
  - phase: 04-documentation-validation
    provides: validated v1.0 core.json and semantic.json token files

provides:
  - Component token reference map tracing button and form SCSS through two indirection layers to core tokens
  - Documented error/danger naming inversion (SCSS error=orange, warning=red)
  - Checkbox hardcoded hex gap analysis with #8969f2 recommendation
  - 8 new semantic tokens specified for semantic.json (color.action.*, color.feedback.*, color.background.surface, color.text.default)
  - Reference depth policy with 2-level and 3-level examples using real token paths
  - v2.0 form element scope decision (text input + checkbox only)
  - Unused core tokens tracking: 36 of 85 core tokens unreferenced by buttons/forms/semantic

affects:
  - 05-02 (subsequent phase 5 plans if any)
  - 06-component-token-creation (primary consumer — implementers read reference map to write components.json)
  - 07-form-token-creation (uses form reference map section)

tech-stack:
  added: []
  patterns:
    - "Two-layer SCSS indirection tracing: SCSS var -> CSS custom property -> core token"
    - "Hex-to-core-token cross-reference for SCSS files that bypass the token system"
    - "Separate audit document approach for unused token tracking (keep core.json as pure DTCG)"

key-files:
  created:
    - tokens/audit/component-token-reference-map.md
    - tokens/audit/unused-core-tokens.md
  modified: []

key-decisions:
  - "v2.0 form scope: text input + checkbox only (skip select/textarea/radio to stay under ~75 token budget)"
  - "Static property tokens: include font-size and font-weight, exclude border-width (1px is not semantic)"
  - "color.action.danger -> ff.color.orange-100 (preserves v1.0 visual, names the intent correctly despite counterintuitive color)"
  - "color.action.primary-selected -> ff.color.vivid-100 (bridges #8969f2 gap — nearest available core token)"
  - "8 new semantic tokens needed: color.action.primary-border, color.action.secondary-border, color.action.danger, color.action.primary-selected, color.feedback.error, color.feedback.warning, color.background.surface, color.text.default"
  - "Actual core.json count is 85 tokens (not 160 as estimated in research — v1.0 was scoped down from original audit)"

patterns-established:
  - "Reference depth rule: 3-level (component -> semantic -> core) when multiple components share value; 2-level (component -> core) when value is component-specific"
  - "Naming inversion documentation: always call out when SCSS names don't match color semantics (error=orange, warning=red)"

requirements-completed:
  - ARCH-01
  - ARCH-03

duration: 4min
completed: 2026-02-23
---

# Phase 5 Plan 01: Component Token Reference Map Summary

**SCSS-to-core token tracing for 4 button variants and 2 form elements, with depth policy and 8 new semantic tokens specified for Phase 6.**

## Performance

- **Duration:** 4 min
- **Started:** 2026-02-23T~05:54Z
- **Completed:** 2026-02-23T~05:58Z
- **Tasks:** 2
- **Files created:** 2

## Accomplishments

- Button reference map: all 4 variants (primary, secondary, error/danger, warning) traced through SCSS var -> CSS custom property -> core token for every interactive state (default, hover, focus, selected, disabled)
- Form reference map: text input (clean CSS var chain) and checkbox (hardcoded hex cross-reference) — documented `#8969f2` gap with recommendation
- Documented critical naming inversion: SCSS `--error` variant uses orange (`ff.color.orange-100`) while `--warning` uses red (`ff.color.red-100`) — counterintuitive vs standard convention
- 8 new semantic tokens fully specified with core references and rationale, ready to add to `semantic.json` in Phase 6
- Reference depth policy documented with concrete examples using real token paths from the audit
- Unused core tokens: 36 of 85 tokens not referenced by components or semantic.json, organized by category with no pruning per user decision
- Corrected core.json token count: 85 (not 160 as estimated in research — research was based on a prior Phase 1 estimate)

## Task Commits

1. **Task 1: Create component token reference map with button and form audit** - `cb355682` (feat)
2. **Task 2: Create unused core tokens tracking document** - `3ea8875a` (feat)

## Files Created/Modified

- `tokens/audit/component-token-reference-map.md` - Complete button and form SCSS-to-core token mapping with 6 sections: button map, form map, new semantic tokens needed, depth policy, form scope decision, static property token decision
- `tokens/audit/unused-core-tokens.md` - Cross-referenced all 85 core tokens against semantic.json and components; 36 unreferenced tokens listed by category

## Decisions Made

- **Form element scope:** Text input and checkbox only for v2.0. Rationale: proves the pattern with two representative elements (text entry + selection control) without exceeding ~75 token budget. Textarea, select, radio deferred to v3.0.
- **Static property tokens:** Include `font-size` and `font-weight` (both used by buttons and forms, useful in Figma). Exclude `border-width` (1px has no semantic meaning, no matching core token for pixel values).
- **`#8969f2` gap resolution:** Reference `ff.color.vivid-100` (`#7c80fe`) as nearest available core token via new `color.action.primary-selected` semantic token. Slight visual change from `#8969f2` to `#7c80fe` treated as intentional normalization.
- **error/danger naming:** v2.0 component tokens use `button.danger` (not `button.error`) to better communicate destructive action intent. References `color.action.danger` -> `{ff.color.orange-100}` to preserve v1.0 visual behavior.

## Deviations from Plan

None — plan executed exactly as written. The research data in `05-RESEARCH.md` was accurate and complete. The one discovery beyond the plan was that `core.json` contains 85 tokens, not 160 as estimated in the research document. This was handled by using the actual count in `unused-core-tokens.md` and noting the discrepancy.

## Issues Encountered

- **Token count discrepancy:** Research estimated 160 core tokens (from Phase 1 audit). Actual `core.json` has 85 tokens. The discrepancy is because the Phase 1 audit counted CSS custom properties from SCSS, while core.json was subsequently scoped to primitives only. The 85-token count from direct file reading is the source of truth.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

Phase 6 (component token creation) is fully unblocked. The implementer can:
1. Read `tokens/audit/component-token-reference-map.md` Section 3 for the exact 8 semantic tokens to add to `semantic.json`
2. Read Sections 1-2 for the complete button and form token reference data to write `components.json`
3. Use Section 4 to determine whether each token uses a 2-level or 3-level reference chain
4. Treat `tokens/audit/unused-core-tokens.md` as the orphan-tracking document; no core.json changes needed

No blockers. No concerns.

---
*Phase: 05-architecture-integration-planning*
*Completed: 2026-02-23*
