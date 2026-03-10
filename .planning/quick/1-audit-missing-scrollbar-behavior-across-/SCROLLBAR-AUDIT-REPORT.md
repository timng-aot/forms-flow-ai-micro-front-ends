# Scrollbar Behavior Audit Report

**Jira References:** FWF-5920 (original scrollbar implementation), FWF-6141 (this audit)
**Date:** 2026-03-10
**Scope:** All frontend components in forms-flow-ai-micro-front-ends

---

## 1. Executive Summary

A global CSS rule in `forms-flow-theme/scss/_layout.scss` (lines 8-12) hides all WebKit scrollbars site-wide:

```scss
::-webkit-scrollbar {
  display: none;
  -ms-overflow-style: none;
  // scrollbar-width: none;
}
```

This means every scrollable container renders with **hidden scrollbars by default**. Components must explicitly opt-in to visible, styled scrollbars using the `.custom-scroll` class or the `@include custom-scroll()` mixin defined in `forms-flow-theme/scss/v8-scss/_mixins.scss`.

This audit identifies **5 components with completely missing scrollbar styling** and **2 components with partial/inconsistent implementations**. (The filter dropdown menu was initially flagged but confirmed to have scrollbar styling applied at the component level via the `dropdown-custom-scroll` class.)

---

## 2. Reference Implementation (What "Good" Looks Like)

### The `custom-scroll` Mixin

**File:** `forms-flow-theme/scss/v8-scss/_mixins.scss`, lines 380-393

```scss
@mixin custom-scroll($width: 0.5rem, $thumb-height: 6.75rem) {
  &::-webkit-scrollbar {
    display: block;
    width: $width;
    background-color: transparent;
    opacity: 1;
  }
  &::-webkit-scrollbar-thumb {
    background-color: var(--gray-medium-dark);
    border-radius: 5rem;
    cursor: pointer;
    min-height: $thumb-height !important;
  }
}
```

This mixin overrides the global `display: none` with `display: block`, sets a narrow width, transparent track, and a rounded gray thumb.

### Properly Implemented Components

**A. Modal Body (generic)**
- **File:** `forms-flow-theme/scss/_modal.scss`, lines 150-158
- **Selector:** `.modal .modal-dialog .modal-content .modal-body`
- **How:** Uses `@extend .custom-scroll` on line 152, combined with `overflow: auto` on line 154 and `scrollbar-gutter: stable` on line 158.

**B. Filterable Dropdown**
- **File:** `forms-flow-theme/scss/v8-scss/_filterableDropdown.scss`, lines 88-100
- **Selector:** `.filterable-dropdown-container .filterable-dropdown-menu`
- **How:** Implements its own inline scrollbar styles at lines 89-100 (`&::-webkit-scrollbar { width: 6px; }`, `scrollbar-width: thin; scrollbar-color: #C4C4C4 transparent;`). This is functionally equivalent to the mixin approach -- scrollbar is visible and styled.

**C. Select Dropdown**
- **File:** `forms-flow-theme/scss/v8-scss/_selectDropdown.scss`, lines 244-265
- **Selector:** `.custom-dropdown-options`
- **How:** Implements inline scrollbar styles at lines 244-258 (`&::-webkit-scrollbar { width: 0.25rem; background-color: transparent; }` with a styled thumb). Scrollbar visible and styled.

---

## 3. Gaps -- Missing Scrollbar Behavior

### ~~3.1 Filter Dropdown Menu~~ — NOT A GAP

- **Component:** Task/field filter dropdown menu -- used for selecting filter values in task lists and form lists.
- **File (SCSS):** `forms-flow-theme/scss/v8-scss/_filterDropdown.scss`, lines 91-106
- **File (Component):** `forms-flow-components/src/components/CustomComponents/FilterDropDown.tsx`, line 504
- **Selector:** `.filter-dropdown-menu`
- **Status:** Scrollbar IS present. The `FilterDropDown` component applies the `dropdown-custom-scroll` class at the JSX level (line 504), which uses `@include custom-scroll($width: 1px, $thumb-height: 13px)` (defined in `_theme.scss:419-421`). This was not visible in the SCSS-only audit because the class is applied in the component code, not the stylesheet.
- **UX note:** The scrollbar is intentionally very narrow (1px width, 13px thumb) and may be difficult to discover. Whether this width is sufficient for usability is a UX decision, not a code gap.

### 3.2 History Tables

There are **two separate history views** in the application:

**A. Submission History Tab (Submissions page)**
- **Component:** `AnalyzeSubmissionView.tsx` renders a `ReusableTable` (MUI DataGrid) inside the "History" tab at `forms-flow-submissions/src/components/AnalyzeSubmissionView.tsx`, lines 393-416.
- **Rendering:** This is a tab within the submission detail page (Form / History / Export PDF), NOT a modal. The DataGrid is constrained to `height: 500` with `hideFooter` and `disableColumnResize`.
- **Scrollbar behavior:** Falls under the MUI DataGrid pattern — `.MuiDataGrid-main` has `overflow-x: scroll` (`_table.scss:392-394`) but no visible scrollbar styling due to the global hide rule. Vertical scrolling is handled by MUI's virtual scroller.
- **UI Navigation:** Open a form submission > click the "History" tab > ensure enough history entries to overflow the 500px container.

**B. Task History Modal (Task Details page)**
- **Component:** `TaskHistory.tsx` renders a modal with `.history-modal-body` class at `forms-flow-review/src/components/TaskHistory.tsx`, line 110.
- **File (SCSS):** `forms-flow-theme/scss/historyModal.scss`, lines 5-138
- **Selector:** `.history-modal-body`
- **Scrollbar behavior:** The `.history-modal-body` has no `overflow-y` or scrollbar styling. The parent `.modal-body` does have `@extend .custom-scroll` (from `_modal.scss` line 152), so the modal itself scrolls — but the history body has no independent scroll control.
- **UI Navigation:** Open a task from the task list > click "History" button > ensure enough history entries to overflow the modal body.

### 3.3 Form History Tab — CORRECTED

- **Component:** `HistoryPage` component at `forms-flow-components/src/components/CustomComponents/HistoryPage.tsx`, rendered as a tab (Builder / Settings / History) within the form editor page.
- **Rendering:** Uses `ReusableTable` (MUI DataGrid) with `sx={{ height: "auto" }}` and `hideFooter`. Although the component passes `height: "auto"`, the form editor's layout constrains the tab content area to a fixed viewport height, so the DataGrid does scroll internally.
- **SCSS file `formHistoryModal.scss`:** This stylesheet is NOT used by the history listing. It styles `FormSubmissionHistoryModal.tsx` and `SubmissionHistoryWithViewButton.tsx`, which render a modal for viewing a specific submission's diff (triggered by the "View" button on a history row).
- **Scrollbar assessment:** The DataGrid's `.MuiDataGrid-main` has `overflow-x: scroll !important` (`_table.scss:392-394`) and MUI's virtual scroller manages vertical overflow — both with hidden scrollbars due to the global `::-webkit-scrollbar { display: none }` rule. This is the same MUI DataGrid scrollbar gap as 3.2A.
- **UI Navigation:** Open a form > Form tab > Builder / Settings / History sub-tabs > click "History" with enough versions to overflow the constrained height.

### 3.4 Expression Builder -- Operand Dropdown — CORRECTED

- **Original audit:** Flagged `.pick-operator` as missing scrollbar. **User testing found the operator dropdown ("Choose an operator") DOES have a scrollbar.** The actual gap is on the **operand dropdown** ("Choose a variable or value").
- **Component:** `SelectWithCustomValue` at `forms-flow-components/src/components/CustomComponents/SelectWithCustomValue.tsx`
- **Selector:** `.custom-dropdown-options` (rendered with class `custom-dropdown-options--{variant}`)
- **Root cause:** The dropdown is correctly constrained to `max-height: 14.75rem` (`_selectWithCustomValue.scss:5,14`) and overflow is triggered. The base scrollbar pseudo-element styling exists in `_selectDropdown.scss:244-265`, but the global `::-webkit-scrollbar { display: none }` rule overrides it and hides the scrollbar. Users can scroll via trackpad or mousewheel, but there is no visual scrollbar indicator.
- **UI Navigation:** Open Expression Builder > click the "Choose a variable or value" operand dropdown with enough items to exceed the `14.75rem` max-height.
- **Expected:** Dropdown constrained to `14.75rem` max-height with styled scrollbar.
- **Actual:** Dropdown is correctly constrained, but scrollbar is hidden by the global rule. No visual scroll indicator.

### 3.5 Task Filter Reorder Modal Body

- **Component:** Modal for reordering task filters -- allows drag-and-drop reordering of saved filter items.
- **File:** `forms-flow-theme/scss/_modal.scss`, lines 1452-1457
- **Selector:** `.reorder-task-filter-modal .reorder-task-filter-modal-body`
- **Current CSS (lines 1452-1456):**
  ```scss
  .reorder-task-filter-modal-body {
    padding: var(--spacer-200) var(--spacer-225);
    max-height: calc(100vh - 15.79rem);
    overflow-y: auto;
  }
  ```
- **Issue:** Has `overflow-y: auto` and `max-height` constraint but NO scrollbar styling. The global rule hides the scrollbar.
- **UI Navigation:** Open task list > click filter settings > click "Reorder filters" > ensure enough saved filters exist to overflow the modal body.
- **Expected:** Styled scrollbar appears when filter list exceeds available height.
- **Actual:** Scrollbar is hidden.

### 3.6 Form Template List

- **Component:** The template list panel in the "Choose Template" modal -- lists available form templates for selection.
- **File:** `forms-flow-theme/scss/_modal.scss`, lines 405-411
- **Selector:** `.choose-template-modal .form-template-list`
- **Current CSS (lines 405-411):**
  ```scss
  .form-template-list {
    overflow-y: scroll;
    -ms-overflow-style: none;
    max-height: 75vh;
    height: 59vh;
    border-top: 1px solid $gray-medium;
  }
  ```
- **Issue:** Has `overflow-y: scroll` AND explicitly sets `-ms-overflow-style: none` (further hiding scrollbar in Edge/IE). No `custom-scroll` mixin or inline WebKit scrollbar styles. The global rule hides the WebKit scrollbar.
- **UI Navigation:** Click "Create Form" > select "Use a template" > the left panel shows the template list. Ensure enough templates exist to require scrolling.
- **Expected:** Styled scrollbar appears on the template list.
- **Actual:** Scrollbar is completely hidden (both WebKit via global rule, and MS via explicit `-ms-overflow-style: none`).

### 3.7 MUI DataGrid Horizontal Scrollbar

- **Component:** The `ReusableTable` component wraps a MUI `DataGrid` and is used across multiple pages for tabular data with resizable columns.
- **Component File:** `forms-flow-components/src/components/CustomComponents/ReusableTable.tsx`
- **SCSS File:** `forms-flow-theme/scss/v8-scss/_table.scss`, line 392-394
- **Selector:** `.MuiDataGrid-main`
- **Current CSS (line 392-394):**
  ```scss
  .MuiDataGrid-main {
    overflow-x: scroll!important;
  }
  ```
- **What IS present:** `overflow-x: scroll` forces the horizontal scroll container to always be scrollable.
- **What is MISSING:** No `custom-scroll` mixin or WebKit scrollbar pseudo-element styling. The global `::-webkit-scrollbar { display: none }` rule hides the horizontal scrollbar entirely.
- **Affected consumers:**
  - `forms-flow-submissions/src/Routes/SubmissionListing.tsx` — Submissions listing page
  - `forms-flow-submissions/src/components/AnalyzeSubmissionView.tsx` — Submission detail view
  - `forms-flow-review/src/components/TaskList/TasklistTable.tsx` — Task list table
  - `forms-flow-review/src/components/TaskList/TaskDetailsModal.tsx` — Task details modal
  - `forms-flow-components/src/components/CustomComponents/HistoryPage.tsx` — History tables
- **Note:** The `custom-scroll` mixin only styles the vertical scrollbar (sets `width` but not `height` on `::-webkit-scrollbar`). A horizontal scrollbar requires setting `height` on the pseudo-element as well. This may require extending the mixin or adding dedicated horizontal scrollbar styles for `.MuiDataGrid-main`.
- **UI Navigation:** Open any page using `ReusableTable` (e.g., Submissions list, Task list) with enough columns or wide enough content to exceed the viewport width.
- **Expected:** Styled horizontal scrollbar appears below the table when content overflows horizontally.
- **Actual:** Horizontal scrollbar is hidden by the global rule.

---

## 4. Partial Implementations -- Inconsistent Behavior

### 4.1 Roles List Container

- **Component:** Admin roles management page -- displays a scrollable list of roles with user counts.
- **File:** `forms-flow-admin/src/components/roles/roles.scss`, lines 1-9
- **Selector:** `.table-container`
- **Current CSS (lines 1-9):**
  ```scss
  .table-container {
    background: #FFFFFF;
    border: 1px solid #ECECEC;
    box-shadow: 0px 2px 8px rgba(66, 66, 66, 0.07);
    border-radius: 8px;
    overflow-y: scroll;
    max-height: 25rem;
  }
  ```
- **What IS present:** `overflow-y: scroll` and `max-height: 25rem` -- the container is scroll-enabled and height-constrained.
- **What is MISSING:** No `custom-scroll` mixin/class and no inline scrollbar styling. The global rule hides the scrollbar entirely.
- **Additional concern:** This file uses hardcoded hex colors (`#FFFFFF`, `#ECECEC`) instead of CSS custom properties, indicating it predates the design system update.
- **UI Navigation:** Go to Admin panel > Roles section > ensure enough roles exist to exceed 25rem height.
- **Expected:** Styled scrollbar matching the application design system.
- **Actual:** Scrollbar hidden by global rule.

### 4.2 Resizable Tables

- **Component:** Resizable data tables used in task lists and form lists -- provides horizontally resizable columns with scrollable content.
- **File:** `forms-flow-theme/scss/_table.scss`, lines 761-800
- **Selector:** `.resizable-scroll`
- **Current CSS (lines 761-799):**
  ```scss
  .resizable-scroll {
    &::-webkit-scrollbar {
      width: 8px;
      height: 8px;
      margin-top: 2px;
      background-color: transparent;
      display: block;
      opacity: 0;
    }
    &::-webkit-scrollbar-track {
      background: var(---ff-gray-medium-dark); // NOTE: triple-dash typo
      border-radius: 4px;
    }
    &::-webkit-scrollbar-thumb {
      background: var(--ff-primary-light);
      border-radius: var(--radius-md);
      background-clip: padding-box;
      border: var(--spacer-025) solid transparent;
      opacity: 1;
      &:hover {
        background: var(--ff-primary-light);
        box-shadow: inset 0 0 0 0.0625rem $primary;
      }
    }
    &:hover {
      &::-webkit-scrollbar { opacity: 1; }
      &::-webkit-scrollbar-thumb {
        background: var(--ff-primary-light);
        box-shadow: inset 0 0 0 0.0625rem $primary;
      }
    }
  }
  ```
- **What IS present:** Custom scrollbar styles that override the global rule (`display: block`), with hover-reveal behavior (opacity 0 to 1).
- **What is INCONSISTENT:**
  1. **CSS variable typo on line 772:** `var(---ff-gray-medium-dark)` has a triple-dash prefix instead of double-dash. This causes the track background to be ignored/transparent.
  2. **Different styling pattern:** Uses `opacity: 0` on the scrollbar (hidden until hover) instead of the standard `custom-scroll` mixin which shows scrollbar at all times. This is a different UX from the rest of the application.
  3. **Different thumb color:** Uses `var(--ff-primary-light)` (purple-tinted) instead of `var(--gray-medium-dark)` used by the `custom-scroll` mixin.
- **UI Navigation:** Open any task list or form list that uses the resizable table layout > scroll vertically or horizontally. Hover over the table area to reveal the scrollbar.
- **Expected:** Scrollbar styling consistent with the `custom-scroll` mixin (always visible, gray thumb).
- **Actual:** Scrollbar uses a different color scheme, only appears on hover, and has a CSS variable typo in the track background.

---

## 5. Visual Verification Checklist

Use this checklist to systematically verify each scrollbar gap in a running instance of the application. For each item, navigate to the specified location, trigger the scrollable area, and verify the scrollbar behavior.

- [x] **Filter Dropdown:** ~~Open any task list or form list > click a filter dropdown with enough items to scroll.~~ **Not a gap.** Scrollbar is present via `dropdown-custom-scroll` class (1px width, 13px thumb). Narrow by design — UX review may be warranted for discoverability.

- [ ] **History Modal (Submissions):** Open a form submission > click "History" or "Submission History" with enough versions to overflow. **Verify:** Styled scrollbar appears on the modal body when scrolling through version entries.

- [ ] **Form History Modal:** Open a form in the designer > click "Version History" with enough versions to overflow. **Verify:** Styled scrollbar appears when scrolling through form version entries.

- [ ] **Expression Builder -- Operator List:** Open the Expression Builder modal > navigate to the operator selection panel. **Verify:** A styled scrollbar appears on the operator list when it overflows.

- [ ] **Task Filter Reorder Modal:** Open task list > filter settings > "Reorder filters" with enough saved filters to overflow. **Verify:** Styled scrollbar appears on the reorder list.

- [ ] **Form Template List:** Click "Create Form" > "Use a template" > ensure enough templates to require scrolling in the left panel. **Verify:** Styled scrollbar appears on the template list.

- [ ] **Roles List Container (Admin):** Go to Admin > Roles with enough roles to exceed the 25rem container height. **Verify:** Styled scrollbar appears on the roles table container.

- [ ] **Resizable Tables:** Open any task list or form list with resizable columns > scroll vertically. **Verify:** Scrollbar is consistently styled (check for triple-dash CSS variable typo fix, consistent thumb color, consistent visibility behavior).

---

## 6. Fix Pattern Summary

For each gap identified above, the fix follows a consistent pattern:

1. **Add the mixin include** to the scrollable selector:
   ```scss
   @include custom-scroll();
   ```
   OR extend the class:
   ```scss
   @extend .custom-scroll;
   ```

2. **Remove any explicit scrollbar-hiding** rules like `-ms-overflow-style: none`.

3. **For the resizable tables partial:** Fix the CSS variable typo (`---ff-gray-medium-dark` to `--ff-gray-medium-dark`) and consider aligning the scrollbar color and visibility behavior with the `custom-scroll` mixin standard.

The `custom-scroll` mixin is already available in `_mixins.scss` and imported across the theme, so no new dependencies are needed.
