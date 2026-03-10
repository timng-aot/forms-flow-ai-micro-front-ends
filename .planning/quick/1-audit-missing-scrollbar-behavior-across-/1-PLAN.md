---
phase: quick
plan: 1
type: execute
wave: 1
depends_on: []
files_modified:
  - .planning/quick/1-audit-missing-scrollbar-behavior-across-/SCROLLBAR-AUDIT-REPORT.md
autonomous: true
requirements: [FWF-6141]
must_haves:
  truths:
    - "Team can identify every component with missing or inconsistent scrollbar behavior"
    - "Team can navigate to exact file, line number, and CSS selector for each gap"
    - "Team knows what correct scrollbar behavior looks like (reference implementation)"
    - "Team has a checklist for visual verification in production"
  artifacts:
    - path: ".planning/quick/1-audit-missing-scrollbar-behavior-across-/SCROLLBAR-AUDIT-REPORT.md"
      provides: "Structured audit report with all scrollbar gaps, verification steps, and reference implementations"
      min_lines: 80
  key_links: []
---

<objective>
Produce a structured audit report documenting all missing and inconsistent scrollbar behavior across frontend components.

Purpose: Give the team a single reference document for visually verifying scrollbar gaps in production, with exact file paths, line numbers, CSS selectors, and UI navigation steps for each finding.
Output: SCROLLBAR-AUDIT-REPORT.md in this plan directory.
</objective>

<execution_context>
@/Users/tngaot/.claude/get-shit-done/workflows/execute-plan.md
@/Users/tngaot/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/STATE.md

Source files to reference for exact line numbers and selectors:
@forms-flow-theme/scss/_layout.scss (root cause: global scrollbar hide)
@forms-flow-theme/scss/v8-scss/_mixins.scss (fix pattern: custom-scroll mixin)
@forms-flow-theme/scss/v8-scss/_filterDropdown.scss (gap: filter dropdown)
@forms-flow-theme/scss/historyModal.scss (gap: history modal)
@forms-flow-theme/scss/formHistoryModal.scss (gap: form history modal)
@forms-flow-theme/scss/_modal.scss (gaps: expression builder, task filter reorder, form template list)
@forms-flow-admin/src/components/roles/roles.scss (partial: roles list)
@forms-flow-theme/scss/_table.scss (partial: resizable tables)
@forms-flow-theme/scss/v8-scss/_filterableDropdown.scss (reference: good implementation)
@forms-flow-theme/scss/v8-scss/_selectDropdown.scss (reference: good implementation)
</context>

<tasks>

<task type="auto">
  <name>Task 1: Generate scrollbar behavior audit report</name>
  <files>.planning/quick/1-audit-missing-scrollbar-behavior-across-/SCROLLBAR-AUDIT-REPORT.md</files>
  <action>
Create SCROLLBAR-AUDIT-REPORT.md with the following structure:

**1. Executive Summary**
- Jira references: FWF-5920 (original implementation), FWF-6141 (this audit)
- Root cause: Global CSS in `forms-flow-theme/scss/_layout.scss` lines 8-12 hides all webkit scrollbars via `::-webkit-scrollbar { display: none; }`. Components must explicitly opt-in to visible scrollbars using the `.custom-scroll` class or `@include custom-scroll()` mixin.
- Fix pattern reference: `forms-flow-theme/scss/v8-scss/_mixins.scss` lines 380-393

**2. Reference Implementation (What "Good" Looks Like)**
- Extract the exact `custom-scroll` mixin code from `_mixins.scss` lines 380-393
- List 2-3 properly implemented components as examples:
  - Filterable Dropdown (`_filterableDropdown.scss`) -- note exact selector and line
  - Select Dropdown (`_selectDropdown.scss`) -- note exact selector and line
  - Modal Bodies (`_modal.scss` lines 150-302) -- note exact selector and line

**3. Gaps -- Missing Scrollbar Behavior**
For each of these 6 components, create a subsection with:
- Component name and what it does in the UI
- File path and exact line numbers
- The CSS selector(s) affected
- Current CSS (the `overflow-y: auto/scroll` without custom-scroll)
- What a tester should do in the UI to trigger the scrollable area (e.g., "Open filter dropdown with >10 items")
- Expected behavior: scrollbar should be visible and styled
- Actual behavior: scrollbar hidden or browser-default

Components (read each file to get exact selectors and line numbers):
1. Filter Dropdown -- `forms-flow-theme/scss/v8-scss/_filterDropdown.scss` ~lines 91-106
2. History Modal -- `forms-flow-theme/scss/historyModal.scss`
3. Form History Modal -- `forms-flow-theme/scss/formHistoryModal.scss`
4. Expression Builder Operator List -- `forms-flow-theme/scss/_modal.scss` ~lines 1014-1021
5. Task Filter Reorder Modal -- `forms-flow-theme/scss/_modal.scss` ~lines 1454-1456
6. Form Template List -- `forms-flow-theme/scss/_modal.scss` ~lines 405-411

**4. Partial Implementations -- Inconsistent Behavior**
Same structure as above but noting what IS present vs what is missing:
1. Roles List Container -- `forms-flow-admin/src/components/roles/roles.scss` lines 1-9
2. Resizable Tables -- `forms-flow-theme/scss/_table.scss` lines 761-800

**5. Visual Verification Checklist**
A markdown checkbox list combining all gaps and partials, formatted for a QA tester:
```
- [ ] Filter Dropdown: Open any filter dropdown with enough items to scroll. Verify styled scrollbar appears.
- [ ] History Modal: Open submission history. Verify styled scrollbar on long lists.
...
```

Each checklist item should state: where to navigate, what action triggers scrolling, what to verify.

IMPORTANT: Read each source file listed in context to extract EXACT current selectors, line numbers, and CSS property values. Do not guess -- use the actual code.
  </action>
  <verify>
    <automated>test -f .planning/quick/1-audit-missing-scrollbar-behavior-across-/SCROLLBAR-AUDIT-REPORT.md && wc -l .planning/quick/1-audit-missing-scrollbar-behavior-across-/SCROLLBAR-AUDIT-REPORT.md | awk '{if ($1 >= 80) print "PASS: " $1 " lines"; else print "FAIL: only " $1 " lines"}'</automated>
  </verify>
  <done>SCROLLBAR-AUDIT-REPORT.md exists with 80+ lines covering all 6 gaps, 2 partials, reference implementations, exact file/line/selector details, and a visual verification checklist</done>
</task>

</tasks>

<verification>
- Report file exists at `.planning/quick/1-audit-missing-scrollbar-behavior-across-/SCROLLBAR-AUDIT-REPORT.md`
- All 6 gap components documented with file paths, line numbers, CSS selectors
- Both partial implementations documented
- Reference implementation section shows the correct pattern
- Visual verification checklist covers all 8 findings
</verification>

<success_criteria>
- Single structured document that a QA tester or developer can use to systematically verify every scrollbar gap in production
- Every finding includes exact file path, line number, CSS selector, and UI navigation steps
- No code changes made -- this is audit documentation only
</success_criteria>

<output>
After completion, create `.planning/quick/1-audit-missing-scrollbar-behavior-across-/1-SUMMARY.md`
</output>
