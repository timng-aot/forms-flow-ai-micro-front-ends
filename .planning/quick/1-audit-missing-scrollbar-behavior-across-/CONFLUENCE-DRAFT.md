# v8.2 Scrollbar Audit — Suggested Confluence Update

## Context

A global CSS rule hides all WebKit scrollbars application-wide. This means every scrollable container renders with hidden scrollbars by default, impacting the discoverability of items in tables, dropdown menus, and other components.

Currently, components **must** opt-in to visible, styled scrollbars using one of three patterns:

1. A `.custom-scroll` class
2. A `@include custom-scroll()` mixin defined in `forms-flow-theme/scss/v8-scss/_mixins.scss`
3. Inline `::-webkit-scrollbar` rules

This audit identifies components with partial, inconsistent, or missing implementations.

**Relevant tickets:**

- [FWF-5920](https://aottech.atlassian.net/browse/FWF-5920)
- [FWF-6141](https://aottech.atlassian.net/browse/FWF-6141)

---

## Findings

### 1. Missing scrollbars

These components have scrollable containers with no visible scrollbar styling. The global `::-webkit-scrollbar { display: none }` rule hides the scrollbar entirely.

#### 1a. History tables (task history modal, form history tab)

**Severity:** High — users have no visual indication that content extends beyond the visible area.

**Navigation:**
- *Task history:* Open the task list (`/task`), open a task, and click the "History" tab. Ensure the task has enough history to overflow the modal body.
- *Form history:* Open a form in the builder and navigate to the "History" tab. Ensure enough versions exist to overflow the table.

**Expected:** Styled scrollbar appears when history entries overflow the fixed table height. Alternatively, remove the fixed height from the table and allow the container to handle vertical scrolling. This is how data tables with pagination already behave.

**Actual:** No scrollbar is present.

**Root cause:** Both views use the `HistoryPage` component (`forms-flow-components/src/components/CustomComponents/HistoryPage.tsx`), which renders a `ReusableTable` (MUI DataGrid). The DataGrid's internal virtual scroller manages overflow, but the global rule hides its scrollbar. The task history modal's parent `.modal-body` does extend `.custom-scroll` (`_modal.scss:152`), but this styles the modal's own scrollbar — not the DataGrid's internal one.

**Recommended fix:** Remove the fixed height constraint from the `HistoryPage` DataGrid and let the parent container (`.body-section.custom-scroll` or `.modal-body.custom-scroll`) handle vertical scrolling. This aligns with how paginated data tables (submissions, tasks) already work — the table expands to fit its content while the page-level container provides the styled scrollbar. The `HistoryPage` component already supports `autoHeight` and `hideFooter` props, so this may only require ensuring the consuming pages pass `autoHeight={true}` and wrap the component in a scrollable parent with `custom-scroll`.

---

#### 1b. Task filter reorder modal

**Severity:** High — users cannot scroll to see or reorder filters beyond the visible area.

**Navigation:** Open the task list (`/task`) and click the filter selection dropdown. Click "Reorder/hide filters" to trigger the reorder modal.

**Expected:** Styled scrollbar appears when filter list exceeds modal content height.

**Actual:** Scrollbar is hidden.

**Root cause:** `.reorder-task-filter-modal-body` (`_modal.scss:1452-1456`) has `overflow-y: auto` and `max-height: calc(100vh - 15.79rem)`, but no `custom-scroll` class or mixin. The global rule hides the scrollbar.

**Recommended fix:** Add `@include custom-scroll()` to `.reorder-task-filter-modal-body` in `_modal.scss`, or add the `custom-scroll` class to the element in the component JSX.

---

#### 1c. Expression builder — variable selection dropdown

**Severity:** Medium — dropdown is scrollable but users have no visual indication that more items exist below the fold.

**Navigation:** Add a new block to the no-code workflow builder graph and select "Condition". Select the "Choose a variable or value" dropdown. Ensure enough variables exist to exceed the `14.75rem` max-height.

**Expected:** Styled scrollbar appears in the variable selection dropdown menu.

**Actual:** No scrollbar is visible. Users can scroll via trackpad or mousewheel, but there is no visual scrollbar indicator.

**Root cause:** The dropdown has `max-height: 14.75rem` (`_selectWithCustomValue.scss:5,14`) and overflow is triggered correctly. The base scrollbar pseudo-element styling exists in `_selectDropdown.scss:244-265`, but the global `::-webkit-scrollbar { display: none }` rule overrides it and hides the scrollbar.

**Recommended fix:** Add `@include custom-scroll()` to `.selectdropdown-container--custom-value .custom-dropdown-options` in `_selectWithCustomValue.scss`, which will override the global `display: none` with `display: block` on the scrollbar pseudo-element.

---

#### 1d. User & role management tables

**Severity:** Medium — users cannot scroll to see all roles or users when the list exceeds the container height.

**Navigation:** Open the admin console ("Manage" in the sidebar) and navigate to the "Users" or "Roles" tab. Ensure enough items exist to exceed the maximum height of the table container.

**Expected:** Styled scrollbar matching the application design system.

**Actual:** No scrollbar is present.

**Root cause:** The roles list container has `overflow-y: scroll` and `max-height: 25rem` but no `custom-scroll` mixin or WebKit scrollbar styling. The Users tab should be verified separately — it may use a different container structure.

**Recommended fix:** Add `@include custom-scroll()` to the roles/users list container, or add the `custom-scroll` class to the element in the component JSX. Verify that both the Users and Roles tabs share the same container structure; if they differ, each may need its own fix.

---

#### 1e. Horizontal scrollbars (MUI DataGrid tables)

**Severity:** Medium — users cannot discover horizontal scroll on wide tables without a visible scrollbar.

**Navigation:** Open any page using the `ReusableTable` component (submissions list, task list, form list) with enough columns or wide enough content to exceed the table width.

**Expected:** Styled horizontal scrollbar appears when content overflows horizontally.

**Actual:** No scrollbar is visible.

**Root cause:** `.MuiDataGrid-main` in `_table.scss:392-394` has `overflow-x: scroll !important` but no scrollbar pseudo-element styling. The global rule hides the horizontal scrollbar. This affects all consumers of `ReusableTable`: submissions listing, submission detail view, task list table, task details modal, and history tables.

**Recommended fix:** Add `::-webkit-scrollbar` styling to `.MuiDataGrid-main` with `display: block` and an appropriate `height` value. The existing `custom-scroll` mixin only sets `width` (for vertical scrollbars), so either extend the mixin to accept a direction parameter or add dedicated horizontal scrollbar styles for `.MuiDataGrid-main`.

---

### 2. Inconsistent scrollbar styling

These components have visible scrollbars that don't match the application design system.

#### 2a. Task filter dropdown

**Severity:** Low — a scrollbar is present but may be difficult to discover due to its narrow width.

**Navigation:** Open the task list (`/task`) and click the filter selection dropdown.

**Expected:** Styled scrollbar appears when the list contains enough items to exceed 383px height.

**Actual:** A very narrow scrollbar (1px width) appears that is inconsistent with the expected style.

**Root cause:** The component applies a `dropdown-custom-scroll` class (`_theme.scss:419-421`) which uses `@include custom-scroll($width: 1px, $thumb-height: 13px)`. The 1px width is intentional for dropdown menus but may be too narrow for discoverability.

**Recommended fix:** This is a UX decision. If the narrow scrollbar is acceptable for dropdown menus, document it as intentional. If not, increase the `$width` parameter in the `dropdown-custom-scroll` class to match the standard `0.5rem` used by `custom-scroll`, or choose an intermediate value that balances aesthetics with discoverability.
