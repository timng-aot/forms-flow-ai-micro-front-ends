---
phase: quick
plan: 1
subsystem: theme/scss
tags: [audit, scrollbar, css, accessibility]
dependency_graph:
  requires: []
  provides: [scrollbar-audit-report]
  affects: [forms-flow-theme]
tech_stack:
  added: []
  patterns: [custom-scroll-mixin]
key_files:
  created:
    - .planning/quick/1-audit-missing-scrollbar-behavior-across-/SCROLLBAR-AUDIT-REPORT.md
  modified: []
decisions:
  - Global scrollbar hide in _layout.scss lines 8-12 is the root cause of all gaps
  - custom-scroll mixin in _mixins.scss lines 380-393 is the canonical fix pattern
  - Resizable tables have a CSS variable typo (triple-dash) that should be fixed
metrics:
  duration: 110s
  completed: 2026-03-10
---

# Quick Task 1: Scrollbar Behavior Audit Summary

Comprehensive audit of missing and inconsistent scrollbar behavior across all frontend SCSS components, producing a structured report with exact file paths, line numbers, CSS selectors, and QA verification steps.

## What Was Done

### Task 1: Generate scrollbar behavior audit report
- **Commit:** 785c0e9d
- Created `SCROLLBAR-AUDIT-REPORT.md` (312 lines) documenting:
  - Root cause: global `::-webkit-scrollbar { display: none }` in `_layout.scss` lines 8-12
  - Reference implementation: `custom-scroll` mixin in `_mixins.scss` lines 380-393
  - 3 properly implemented examples (modal body, filterable dropdown, select dropdown)
  - 6 components with completely missing scrollbar styling
  - 2 components with partial/inconsistent implementations
  - Visual verification checklist with 8 items for QA testing

## Key Findings

| # | Component | File | Issue |
|---|-----------|------|-------|
| 1 | Filter Dropdown | `_filterDropdown.scss:91-106` | `overflow-y: auto` with no scrollbar styling |
| 2 | History Modal | `historyModal.scss:5-138` | No independent scroll control |
| 3 | Form History Modal | `formHistoryModal.scss:7-15` | No overflow-y or scrollbar styling |
| 4 | Expression Builder Operators | `_modal.scss:1014-1021` | `overflow-y: scroll` with no scrollbar styling |
| 5 | Task Filter Reorder | `_modal.scss:1452-1456` | `overflow-y: auto` with no scrollbar styling |
| 6 | Form Template List | `_modal.scss:405-411` | `overflow-y: scroll` + explicit `-ms-overflow-style: none` |
| 7 | Roles List (partial) | `roles.scss:1-9` | `overflow-y: scroll` with no scrollbar styling |
| 8 | Resizable Tables (partial) | `_table.scss:761-800` | Has custom scrollbar but CSS variable typo and inconsistent styling |

## Deviations from Plan

None - plan executed exactly as written.

## Self-Check: PASSED

- [x] SCROLLBAR-AUDIT-REPORT.md exists (312 lines, exceeds 80-line minimum)
- [x] All 6 gap components documented with file paths, line numbers, CSS selectors
- [x] Both partial implementations documented
- [x] Reference implementation section shows correct pattern
- [x] Visual verification checklist covers all 8 findings
- [x] Commit 785c0e9d verified
