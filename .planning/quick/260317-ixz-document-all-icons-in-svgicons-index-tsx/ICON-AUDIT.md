# SvgIcons Component Audit

**Source file:** `forms-flow-components/src/components/SvgIcons/index.tsx`
**Date generated:** 2026-03-17
**Total lines:** 1796
**Barrel export:** `forms-flow-components/src/components/index.ts` (`export * from "./SvgIcons"`)
**Figma reference:** [FormsFlow V8 -- Icon sheet](https://www.figma.com/design/HeAKsFFx2ND3FwD9gLKf7I/branch/KG3w1FOa4urCyXVjTYMsCe/FormsFlow-V8?node-id=20874-1145)

---

## Summary Statistics

| Metric | Count | Percent |
|--------|-------|---------|
| Total icons | 89 | 100% |
| Used icons | 55 | 61.8% |
| Unused icons | 34 | 38.2% |
| Legacy-only icons | 3 | 3.4% |
| Removal candidates | up to 37 | 41.6% |

- **Legacy-only icons** are used exclusively in `TaskList-old`, which appears to be a deprecated component.
- **Removal candidates** = 34 unused + 3 legacy-only.

---

## Color Variables

Defined at the top of the file (lines 1-8) via `getComputedStyle(document.documentElement)`:

| Variable | CSS Custom Property |
|----------|-------------------|
| `baseColor` | `--ff-primary` |
| `grayColor` | `--ff-gray-dark` |
| `whiteColor` | `--ff-white` |
| `grayDarkestColor` | `--ff-gray-darkest` |
| `grayMediumColor` | `--ff-gray-medium-dark` |
| `secondaryDarkColor` | `--secondary-dark` |
| `dangerColor` | `--red-100` |

Note: `dangerColor` is defined but never used as a default by any icon.

---

## Icon Catalog

### 1. Navigation

Icons for nav menus, page movement, and sidebar.

| Icon Component | Description | Default Color | Status | Usage Locations |
|----------------|-------------|---------------|--------|-----------------|
| `NavbarHomeIcon` | Circle with house silhouette inside | (none -- hardcoded #7C7D7F) | Used | forms-flow-nav: MenuComponent |
| `NavbarTaskIcon` | Circle with checkmark inside | fillColor=grayColor, strokeColor=whiteColor | Used | forms-flow-nav: MenuComponent |
| `NavbarSubmitIcon` | Circle with upward arrow inside | fillColor=grayColor, strokeColor=whiteColor | Used | forms-flow-nav: MenuComponent |
| `NavbarAnalyzeIcon` | Circle with line chart inside | fillColor=grayDarkestColor, strokeColor=whiteColor | Used | forms-flow-nav: MenuComponent |
| `NavbarBuildIcon` | Circle with horizontal text lines inside | fillColor=grayDarkestColor, strokeColor=whiteColor | Used | forms-flow-nav: MenuComponent |
| `NavbarManageIcon` | Circle with person silhouette and badge inside | fillColor=grayDarkestColor, strokeColor=whiteColor | Used | forms-flow-nav: MenuComponent |
| `MenuToggleIcon` | Square panel with right-pointing chevron (sidebar toggle) | (none -- hardcoded #7C7D7F) | Used | forms-flow-nav: Sidebar |
| `HamburgerIcon` | Three horizontal bars (hamburger menu) | baseColor | Unused | None |
| `AngleLeftIcon` | Left-pointing angle bracket | baseColor | Used | forms-flow-components: CollapsibleSearch, TableFooter |
| `AngleRightIcon` | Right-pointing angle bracket | baseColor | Used | forms-flow-components: CollapsibleSearch, TableFooter |
| `BackIcon` | Left-pointing filled chevron arrow | (color prop, no default) | Used | forms-flow-components: VariableSelection |
| `BackToPrevIcon` | Left-pointing arrow with horizontal line | baseColor | Used | forms-flow-review: TaskDetails |
| `ChevronIcon` | Small right-pointing chevron stroke | grayColor | Used | forms-flow-components: Button, ButtonDropdown, CustomDropdownButton, InputDropdown; forms-flow-nav: MenuComponent |

### 2. Actions

Icons for user actions such as edit, delete, copy, save, etc.

| Icon Component | Description | Default Color | Status | Usage Locations |
|----------------|-------------|---------------|--------|-----------------|
| `AddIcon` | Plus sign (cross shape) | "#7C7D7F" | Used | forms-flow-review: AttributeFilterDropdown, TaskFilterDropdown; forms-flow-submissions: SubmissionListing |
| `CopyIcon` | Two overlapping rectangles (copy/duplicate) | baseColor | Used | forms-flow-components: CustomUrl |
| `DeleteIcon` | Trash can with vertical line inside | baseColor | Used | forms-flow-admin: roles; forms-flow-review: SaveFilterTab |
| `DraggableIcon` | Two horizontal parallel lines (drag handle) | (color prop, no default) | Used | forms-flow-components: DragandDropSort |
| `DuplicateIcon` | Two overlapping rectangles (document copy) | baseColor | Unused | None |
| `EditPencilIcon` | Pencil with edit path (filled style) | secondaryDarkColor | Unused | None |
| `EditIconforFilter` | Small pencil with edit path (outlined style) | (color prop, no default) | Used | forms-flow-components: FilterDropDown |
| `ExportIcon` | Downward arrow with horizontal bar at bottom | baseColor | Unused | None |
| `ImportIcon` | Upward arrow with horizontal bar at top | baseColor | Unused | None |
| `PencilIcon` | Pencil on diagonal with edit path (stroke style) | (none) | Used | forms-flow-components: CollapsibleSearch, FilterDropDown |
| `PreviewIcon` | Diagonal arrow pointing upper-right (external link) | baseColor | Unused | None |
| `RefreshIcon` | Two curved arrows forming a circular refresh loop | baseColor | Used | forms-flow-components: FilterSortAction |
| `ReorderIcon` | Two vertical arrows (one up, one down) | (none -- hardcoded #7C7D7F) | Used | forms-flow-review: AttributeFilterDropdown, TaskFilterDropdown |
| `RoundedAddMoreIcon` | Circle with plus sign inside | (color prop, no default) | Unused | None |
| `RoundedCloseIcon` | Circle with X inside | (color prop, no default) | Unused | None |
| `SaveIcon` | Floppy disk | whiteColor | Used | forms-flow-review: SaveFilterTab |
| `TrashIcon` | Trash can outline (stroke style) | baseColor | Unused | None |
| `UpdateIcon` | Two curved arrows forming an oval refresh loop | baseColor | Used | forms-flow-review: SaveFilterTab |
| `UploadIcon` | Upward arrow with platform base (large, 32x32) | baseColor | Unused | None |

### 3. Status / Feedback

Icons indicating state or result.

| Icon Component | Description | Default Color | Status | Usage Locations |
|----------------|-------------|---------------|--------|-----------------|
| `CheckIcon` | Simple checkmark stroke | baseColor | Unused | None |
| `CheckboxCheckedIcon` | Rounded rectangle with checkmark inside | (none) | Legacy Only | forms-flow-review: TaskList-old |
| `CheckboxUncheckedIcon` | Empty rounded rectangle | (none) | Legacy Only | forms-flow-review: TaskList-old |
| `FailedIcon` | Circle with X inside (red accents) | baseColor | Used | forms-flow-components: ImportModal |
| `InfoIcon` | Circle with "i" letter inside (variant-based coloring) | (variant system: primary=#B8ABFF) | Used | forms-flow-components: CustomInfo |
| `LoadingIcon` | Dashed circle arc (spinning animation via CSS class) | (none) | Used | forms-flow-components: Button |
| `SuccessIcon` | Circle with checkmark inside (blue accents) | baseColor | Used | forms-flow-components: ImportModal |
| `TickIcon` | Standalone checkmark (thick stroke) | baseColor | Unused | None |

### 4. Form / Input

Icons used within form controls, dropdowns, filters, and date pickers.

| Icon Component | Description | Default Color | Status | Usage Locations |
|----------------|-------------|---------------|--------|-----------------|
| `CalenderLeftIcon` | Left-pointing filled arrow (calendar nav) | baseColor | Used | forms-flow-components: DateFilter |
| `CalenderRightIcon` | Right-pointing filled arrow (calendar nav) | baseColor | Used | forms-flow-components: DateFilter |
| `ClearIcon` | Small X (clear/dismiss input) | (none) | Used | forms-flow-components: FormInput, InputDropdown |
| `CloseIcon` | Diagonal X lines (close modal/panel) | baseColor | Used | forms-flow-admin: roles, users; forms-flow-components: BuildModal, ConfirmModal, DateFilter, ErrorModal, FormBuilderModal, FormSubmissionHistoryModal, FormViewModal, ImportModal, InputDropdown, MultiSelect, ReusableLargeModal, ReusableStandardModal, Search, SortModal, SubmissionHistoryWithViewButton, VariableSelection; forms-flow-nav: hamburgerMenu, ProfileSettingsModal; forms-flow-review: AttributeFilterModal, ReorderAttributeFilterModal, ReorderTaskFilterModal, TaskFilterModal, TaskHistory; forms-flow-submissions: ManageFieldsSortModal |
| `CurlyBracketsIcon` | Pair of curly braces `{ }` | "red" | Unused | None |
| `DownArrowIcon` | Downward-pointing chevron (thick stroke) | baseColor | Used | forms-flow-admin: manage, organization; forms-flow-components: DateFilter, FilterableDropdown, FilterDropDown, SelectDropdown, SelectWithCustomValue, TableFooter |
| `DropdownIcon` | Downward-pointing chevron (dropdown indicator) | baseColor | Unused | None |
| `FileUploadIcon` | Document with upward arrow inside | (none) | Used | forms-flow-components: FileUploadArea |
| `FilterIcon` | Three horizontal lines of decreasing width | baseColor | Used | forms-flow-components: FilterSortAction |
| `FormVariableIcon` | Square with horizontal text lines inside | baseColor | Used | forms-flow-components: DragandDropSort; forms-flow-submissions: ManageFieldsSortModal |
| `IButton` | Circle with "i" letter inside (info tooltip) | grayColor | Used | forms-flow-components: ImportModal |
| `NewSortDownIcon` | Downward-pointing filled triangle/chevron | baseColor | Used | forms-flow-components: ReusableTable |
| `QuickFilterIcon` | Lightning bolt inside circle | (color prop, no default) | Used | forms-flow-review: AttributeFilterModalBody, TaskFilterModalBody |
| `SmallSearchIcon` | Small magnifying glass | (color prop, no default) | Unused | None |
| `SortIcon` | Upward-pointing arrow (sort indicator) | grayColor | Used | forms-flow-components: SortableHeadder |
| `SwitchCrossIcon` | Small X (switch off indicator) | baseColor | Used | forms-flow-components: Switch |
| `SwitchTickIcon` | Small checkmark (switch on indicator) | baseColor | Used | forms-flow-components: Switch |
| `UpArrowIcon` | Upward-pointing chevron (thick stroke) | baseColor | Used | forms-flow-admin: manage, organization; forms-flow-components: DateFilter, FilterableDropdown, FilterDropDown, SelectDropdown, SelectWithCustomValue |
| `VerticalArrowDownIcon` | Long vertical line with downward arrow tip | grayDarkestColor | Unused | None |
| `VerticalLineIcon` | Tall thin vertical separator line | baseColor | Used | forms-flow-components: DropdownMultiselect, SelectDropdown, SelectWithCustomValue |

### 5. Branding / Identity

Logos, social, and integration platform icons.

| Icon Component | Description | Default Color | Status | Usage Locations |
|----------------|-------------|---------------|--------|-----------------|
| `ApplicationLogo` | FormsFlow.ai circular checkmark logo | (complex -- multi-color, default #1B34FB) | Used | forms-flow-nav: hamburgerMenu, ProfileSettingsModal, Sidebar |
| `GoogleIcon` | Google "G" logo (4-color) | (color prop, no default -- uses brand colors) | Used | forms-flow-nav: ProfileSettingsModal |
| `GoogleFormsIcon` | Google Forms document icon (purple) | (color prop, no default -- uses brand colors) | Unused | None |
| `JotformIcon` | Jotform logo (multi-color geometric shapes) | (color prop, no default -- uses brand colors) | Unused | None |
| `LinkFileIcon` | Paperclip attachment icon | (color prop, no default) | Unused | None |
| `MailChimpIcon` | Mailchimp monkey face logo | (color prop, no default -- uses brand colors) | Unused | None |
| `MicrosoftIcon` | Microsoft 4-pane window logo | (color prop, no default -- uses brand colors) | Used | forms-flow-nav: ProfileSettingsModal |
| `MicrosoftFormsIcon` | Microsoft Forms "F" icon (teal) | (color prop, no default -- uses brand colors) | Unused | None |
| `FormStackIcon` | Formstack stacked-cards logo (green) | (color prop, no default -- uses brand colors) | Unused | None |

### 6. AI / Premium

AI-related and premium feature icons.

| Icon Component | Description | Default Color | Status | Usage Locations |
|----------------|-------------|---------------|--------|-----------------|
| `AiFormBuilderIcon` | Three sparkle stars (AI form builder variant) | (color prop, no default -- hardcoded #7C80FE) | Unused | None |
| `AiIcon` | Three sparkle stars (AI feature indicator) | baseColor | Unused | None |
| `AiImageSearchIcon` | Magnifying glass (AI image search) | (color prop, no default -- hardcoded #E5E5E5) | Unused | None |
| `EditPromptIcon` | Two curved arrows in circular motion (edit/retry prompt) | (color prop, no default -- hardcoded #E5E5E5) | Unused | None |
| `SparkIcon` | Lightning bolt (small spark indicator) | (color prop, no default -- hardcoded #B8ABFF) | Unused | None |
| `StarPremiumIcon` | Five-pointed star outline | baseColor | Unused | None |
| `TextPromptIcon` | Chat bubble with three dots inside | (color prop, no default -- hardcoded #E5E5E5) | Unused | None |

### 7. Domain / Workflow

Icons specific to formsflow.ai domain concepts.

| Icon Component | Description | Default Color | Status | Usage Locations |
|----------------|-------------|---------------|--------|-----------------|
| `ConnectIcon` | Short horizontal dashed line (connection indicator) | (none -- hardcoded #E5E5E5) | Legacy Only | forms-flow-review: TaskList-old |
| `CreatorIcon` | Circle with lightbulb/person inside (creator role) | (color prop, no default -- hardcoded #7C80FE) | Unused | None |
| `FormStatusIcon` | Solid filled circle (status dot) | baseColor | Used | forms-flow-review: TaskDetailsModal |
| `HistoryIcon` | Clock with circular arrow (history/audit trail) | baseColor | Unused | None |
| `HomeAddUserIcon` | Circle with plus sign inside (add user on home) | "#9E9E9E" | Unused | None |
| `HomeAnalyzeIcon` | Circle with line chart inside (home analytics) | "#7C7D7F" | Unused | None |
| `HomeSubmitIcon` | Circle with upward arrow inside (home submit) | "#7C7D7F" | Unused | None |
| `LogoutIcon` | Circle with right-pointing exit arrow | grayColor | Used | forms-flow-nav: Sidebar |
| `ManagerIcon` | Circle with checkmark and document inside (manager role) | (color prop, no default -- hardcoded #7C80FE) | Unused | None |
| `NotSureIcon` | Circle with question mark inside (unsure role) | (color prop, no default -- hardcoded #7C80FE) | Unused | None |
| `PairEyesIcon` | Pair of cartoon eyes (observer/reviewer indicator) | "#7C7D7F" | Unused | None |
| `SharedWithMeIcon` | Person silhouette with incoming arrow | grayMediumColor | Used | forms-flow-review: ReorderAttributeFilterModal |
| `SharedWithOthersIcon` | Person silhouette with outgoing arrow | grayDarkestColor | Used | forms-flow-review: ReorderAttributeFilterModal |
| `URLCopyIcon` | Circle with two overlapping rectangles inside (copy URL) | baseColor | Used | forms-flow-components: CustomUrl |

---

## Removal Candidates

### Unused Icons (34)

These icons have zero imports across the entire codebase:

- `AiFormBuilderIcon`
- `AiIcon`
- `AiImageSearchIcon`
- `CheckIcon`
- `CreatorIcon`
- `CurlyBracketsIcon`
- `DuplicateIcon`
- `DropdownIcon`
- `EditPencilIcon`
- `EditPromptIcon`
- `ExportIcon`
- `FormStackIcon`
- `GoogleFormsIcon`
- `HamburgerIcon`
- `HistoryIcon`
- `HomeAddUserIcon`
- `HomeAnalyzeIcon`
- `HomeSubmitIcon`
- `ImportIcon`
- `JotformIcon`
- `LinkFileIcon`
- `MailChimpIcon`
- `ManagerIcon`
- `MicrosoftFormsIcon`
- `NotSureIcon`
- `PairEyesIcon`
- `PreviewIcon`
- `RoundedAddMoreIcon`
- `RoundedCloseIcon`
- `SmallSearchIcon`
- `SparkIcon`
- `StarPremiumIcon`
- `TextPromptIcon`
- `TickIcon`
- `TrashIcon`
- `UploadIcon`
- `VerticalArrowDownIcon`

### Legacy-Only Icons (3)

These are only referenced in `TaskList-old`, which appears to be a deprecated component:

- `CheckboxCheckedIcon` -- checked checkbox for task list
- `CheckboxUncheckedIcon` -- unchecked checkbox for task list
- `ConnectIcon` -- horizontal connector line between tasks

---

## Recommendations

1. **Remove 34 unused icons** to reduce bundle size. These have zero imports and add dead code to every consuming micro-frontend.

2. **Evaluate 3 legacy-only icons** -- remove when `TaskList-old` is fully deprecated and deleted. Until then, consider moving them into `TaskList-old` as local components.

3. **Extract high-usage icons into their own files** for better tree-shaking:
   - `CloseIcon` has 25+ usage locations across 5 micro-frontends -- the most imported icon in the system.
   - `ChevronIcon` has 5+ usage locations.
   - `DownArrowIcon` and `UpArrowIcon` are used in 6+ components each.

4. **Split the monolithic 1796-line file into category-based modules** (e.g., `NavigationIcons.tsx`, `ActionIcons.tsx`, `FormIcons.tsx`) to improve maintainability and enable partial imports.

5. **Standardize color prop patterns** -- currently three patterns exist:
   - `color = baseColor` (most common -- 40+ icons)
   - `color` with no default (16 icons -- requires caller to always pass a color)
   - Hardcoded hex values in SVG paths (bypasses the color prop entirely in some icons like `SuccessIcon`, `FailedIcon`)

6. **Audit the `dangerColor` variable** -- it is defined (`--red-100`) but never used as a default by any icon. Either use it or remove it.
