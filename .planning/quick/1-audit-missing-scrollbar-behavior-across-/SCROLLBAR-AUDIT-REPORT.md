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

This audit identifies **6 components with completely missing scrollbar styling** and **2 components with partial/inconsistent implementations**.

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

### 3.1 Filter Dropdown Menu

- **Component:** Task/field filter dropdown menu -- used for selecting filter values in task lists and form lists.
- **File:** `forms-flow-theme/scss/v8-scss/_filterDropdown.scss`, lines 91-106
- **Selector:** `.filter-dropdown-menu`
- **Current CSS (lines 91-106):**
  ```scss
  .filter-dropdown-menu {
    width: 18.75rem;
    max-height: 23.9375rem;
    flex-shrink: 0;
    overflow-y: auto;
    padding: 0;
    margin-top: 0.5625rem;
    border-radius: 0.3125rem;
    border: 0.0625rem solid $gray-x-light;
    background: $white-200;
    box-shadow: 0 0.25rem 0.25rem 0 rgba(0, 0, 0, 0.25);
  }
  ```
- **Issue:** Has `overflow-y: auto` but NO `custom-scroll` class, mixin include, or inline scrollbar styling. The global rule hides the scrollbar entirely.
- **UI Navigation:** Open any task list page > click a filter dropdown (e.g., Status, Created By) that contains enough items to exceed 383px height.
- **Expected:** A styled scrollbar (narrow, rounded gray thumb) appears when list overflows.
- **Actual:** Scrollbar is hidden. User can scroll via trackpad/mouse wheel but has no visual indicator of scrollable content.

### 3.2 History Modal

- **Component:** Submission history modal -- displays version history timeline for form submissions.
- **File:** `forms-flow-theme/scss/historyModal.scss`, lines 5-138
- **Selector:** `.history-modal-body`
- **Current CSS (lines 5-18):**
  ```scss
  .history-modal-body {
    @include paddingLvl2();
    position: relative;
    container: history-modal-body / inline-size;
  }
  ```
- **Issue:** The `.history-modal-body` has no `overflow-y` property set directly, and no scrollbar styling. The parent `.modal-body` does have `@extend .custom-scroll` (from `_modal.scss` line 152), so the modal body itself scrolls correctly. However, the `.analyse-submision-history-modal` (line 141-143) sets `min-height: 80vh` without scroll management. If the history content exceeds the modal body height, scrolling works via the parent but the history body itself has no independent scroll behavior.
- **UI Navigation:** Open any form submission > click "History" or "Submission History" button > ensure there are enough versions to overflow the modal body.
- **Expected:** Styled scrollbar visible on the modal body when history entries overflow.
- **Actual:** The parent modal-body scrollbar applies (via `.custom-scroll`), but if `.history-modal-body` or `.analyse-submision-history-modal` is used as a standalone scrollable container, no scrollbar appears.

### 3.3 Form History Modal

- **Component:** Form version history modal -- shows form definition version history with timeline.
- **File:** `forms-flow-theme/scss/formHistoryModal.scss`, lines 5-16
- **Selector:** `.form-submission-history-modal .form-history-modal-body`
- **Current CSS (lines 7-15):**
  ```scss
  .form-history-modal-body {
    padding: var(--spacer-200) var(--spacer-250) !important;
    margin-top: var(--spacer-200);
    position: relative;
    font-size: var(--font-size-xs);
    font-weight: var(--font-weight-xl);
  }
  ```
- **Issue:** No `overflow-y` property and no scrollbar styling. Relies entirely on parent modal body for scrolling. If the form history entries are numerous, the container has no independent scroll control.
- **UI Navigation:** Open a form in the designer > click "History" or "Version History" > ensure enough versions exist to overflow the modal.
- **Expected:** Styled scrollbar visible when form history entries overflow.
- **Actual:** No scrollbar on `.form-history-modal-body` itself; relies on parent modal-body scroll.

### 3.4 Expression Builder -- Operator List

- **Component:** The operator picker panel inside the expression builder modal -- lists available operators (equals, not equals, contains, etc.).
- **File:** `forms-flow-theme/scss/_modal.scss`, lines 1014-1021
- **Selector:** `.expression-builder .pick-operator`
- **Current CSS (lines 1014-1021):**
  ```scss
  .pick-operator {
    display: flex;
    flex-direction: column;
    padding: var(--spacer-200);
    gap: var(--spacer-050);
    max-height: calc(100vh - 26.375rem);
    overflow-y: scroll;
  }
  ```
- **Issue:** Has `overflow-y: scroll` but NO `custom-scroll` mixin, class, or inline scrollbar styles. The global rule hides the scrollbar.
- **UI Navigation:** Open the Expression Builder modal (available in workflow/form configuration) > navigate to the operator selection panel on the right side.
- **Expected:** A styled scrollbar appears when the operator list exceeds the available height.
- **Actual:** Scrollbar is hidden. Content scrolls via trackpad/wheel but no visual scrollbar indicator.

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

- [ ] **Filter Dropdown:** Open any task list or form list > click a filter dropdown (Status, Created By, etc.) with enough items to scroll. **Verify:** A styled scrollbar (narrow, gray, rounded thumb) appears in the dropdown menu.

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
