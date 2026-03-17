---
phase: quick
plan: 260317-ixz
type: execute
wave: 1
depends_on: []
files_modified:
  - .planning/quick/260317-ixz-document-all-icons-in-svgicons-index-tsx/ICON-AUDIT.md
autonomous: true
requirements: [QUICK-260317-IXZ]
must_haves:
  truths:
    - "Every exported icon component in SvgIcons/index.tsx is documented"
    - "Each icon entry includes name, description, default color, usage status, and usage locations"
    - "Icons are grouped by functional category"
    - "Summary statistics show used vs unused counts"
    - "Legacy-only icons and removal candidates are clearly flagged"
  artifacts:
    - path: ".planning/quick/260317-ixz-document-all-icons-in-svgicons-index-tsx/ICON-AUDIT.md"
      provides: "Complete icon audit documentation"
      contains: "89 icon entries"
  key_links: []
---

<objective>
Create a comprehensive markdown audit document cataloging all 89 icon components in SvgIcons/index.tsx with usage mapping, categorization, and actionable recommendations.

Purpose: Provide a single reference for which icons exist, where they are used, and which are candidates for removal.
Output: ICON-AUDIT.md with full icon catalog.
</objective>

<execution_context>
@/Users/tngaot/.claude/get-shit-done/workflows/execute-plan.md
@/Users/tngaot/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@forms-flow-components/src/components/SvgIcons/index.tsx
</context>

<tasks>

<task type="auto">
  <name>Task 1: Read SvgIcons source and generate ICON-AUDIT.md</name>
  <files>.planning/quick/260317-ixz-document-all-icons-in-svgicons-index-tsx/ICON-AUDIT.md</files>
  <action>
Read the full SvgIcons/index.tsx file (1796 lines, 89 exported components). For each icon component, extract:
- Component name
- Default color parameter (e.g., baseColor, grayColor, whiteColor, etc.)
- SVG visual description based on the path data and viewBox (e.g., "chevron arrow pointing right", "circular refresh arrow")

Create ICON-AUDIT.md with the following structure:

**Header section:**
- Title: "SvgIcons Component Audit"
- Source file path: `forms-flow-components/src/components/SvgIcons/index.tsx`
- Date generated
- Figma reference link: https://www.figma.com/design/HeAKsFFx2ND3FwD9gLKf7I/branch/KG3w1FOa4urCyXVjTYMsCe/FormsFlow-V8?node-id=20874-1145

**Summary statistics section:**
- Total icons: 89
- Used icons: 55 (61.8%)
- Unused icons: 34 (38.2%)
- Legacy-only icons: 3 (CheckboxCheckedIcon, CheckboxUncheckedIcon, ConnectIcon -- only in TaskList-old)
- Removal candidates: 34 unused + 3 legacy-only = up to 37

**Color variables section:**
Document the 7 color variables defined at the top of the file:
- baseColor -> --ff-primary
- grayColor -> --ff-gray-dark
- whiteColor -> --ff-white
- grayDarkestColor -> --ff-gray-darkest
- grayMediumColor -> --ff-gray-medium-dark
- secondaryDarkColor -> --secondary-dark
- dangerColor -> --red-100

**Icon catalog grouped by category.**
Use these categories (assign each icon to exactly one):

1. **Navigation** -- icons for nav menus, page movement, sidebar
   Includes: NavbarAnalyzeIcon, NavbarBuildIcon, NavbarHomeIcon, NavbarManageIcon, NavbarSubmitIcon, NavbarTaskIcon, MenuToggleIcon, HamburgerIcon, AngleLeftIcon, AngleRightIcon, BackIcon, BackToPrevIcon, ChevronIcon

2. **Actions** -- icons for user actions (edit, delete, copy, save, etc.)
   Includes: AddIcon, CopyIcon, DeleteIcon, DraggableIcon, DuplicateIcon, EditPencilIcon, EditIconforFilter, ExportIcon, ImportIcon, PencilIcon, PreviewIcon, RefreshIcon, ReorderIcon, RoundedAddMoreIcon, RoundedCloseIcon, SaveIcon, TrashIcon, UpdateIcon, UploadIcon

3. **Status / Feedback** -- icons indicating state or result
   Includes: CheckIcon, CheckboxCheckedIcon, CheckboxUncheckedIcon, FailedIcon, InfoIcon, LoadingIcon, SuccessIcon, TickIcon

4. **Form / Input** -- icons used within form controls
   Includes: CalenderLeftIcon, CalenderRightIcon, ClearIcon, CloseIcon, DownArrowIcon, FileUploadIcon, FilterIcon, FormVariableIcon, IButton, NewSortDownIcon, QuickFilterIcon, SearchIcon (SmallSearchIcon), SelectDropdown-related (VerticalLineIcon), SortIcon, SwitchCrossIcon, SwitchTickIcon, UpArrowIcon, VerticalArrowDownIcon, CurlyBracketsIcon

5. **Branding / Identity** -- logos, social/integration icons
   Includes: ApplicationLogo, GoogleIcon, GoogleFormsIcon, JotformIcon, LinkFileIcon, MailChimpIcon, MicrosoftIcon, MicrosoftFormsIcon

6. **AI / Premium** -- AI-related and premium feature icons
   Includes: AiFormBuilderIcon, AiIcon, AiImageSearchIcon, EditPromptIcon, SparkIcon, StarPremiumIcon, TextPromptIcon

7. **Domain / Workflow** -- icons specific to forms-flow domain concepts
   Includes: ConnectIcon, CreatorIcon, FormStackIcon, FormStatusIcon, GoogleIcon (if workflow), HomeAddUserIcon, HomeAnalyzeIcon, HomeSubmitIcon, LogoutIcon, ManagerIcon, NotSureIcon, PairEyesIcon, SharedWithMeIcon, SharedWithOthersIcon, URLCopyIcon

Each icon entry in the table should have columns:
| Icon Component | Description | Default Color | Status | Usage Locations |

Where Status is one of: "Used", "Unused", "Legacy Only"
And Usage Locations lists the micro-frontend and component (or "None" for unused).

**Removal candidates section:**
List all 34 unused icons in a simple bullet list, noting they have zero imports across the codebase.
List the 3 legacy-only icons separately, noting they are only referenced in TaskList-old which appears to be deprecated.

**Recommendations section:**
- Remove 34 unused icons to reduce bundle size
- Evaluate 3 legacy-only icons -- remove when TaskList-old is fully deprecated
- Consider extracting high-usage icons (CloseIcon with 25+ usages, ChevronIcon with 5+ usages) into their own files for tree-shaking
- Consider splitting the monolithic 1796-line file into category-based modules
  </action>
  <verify>
    <automated>test -f ".planning/quick/260317-ixz-document-all-icons-in-svgicons-index-tsx/ICON-AUDIT.md" && grep -c "##" ".planning/quick/260317-ixz-document-all-icons-in-svgicons-index-tsx/ICON-AUDIT.md" | xargs test 5 -le</automated>
  </verify>
  <done>ICON-AUDIT.md exists with all 89 icons documented, grouped by category, with usage data and removal recommendations</done>
</task>

</tasks>

<verification>
- ICON-AUDIT.md contains entries for all 89 exported icon components
- Every used icon (55) has its usage locations listed
- Every unused icon (34) is marked as unused and listed as removal candidate
- 3 legacy-only icons are flagged
- Summary statistics are accurate
</verification>

<success_criteria>
- Single markdown file at .planning/quick/260317-ixz-document-all-icons-in-svgicons-index-tsx/ICON-AUDIT.md
- All 89 icons accounted for (55 used + 34 unused)
- Categorized into 7 groups
- Actionable recommendations included
</success_criteria>

<output>
After completion, create `.planning/quick/260317-ixz-document-all-icons-in-svgicons-index-tsx/260317-ixz-SUMMARY.md`
</output>
