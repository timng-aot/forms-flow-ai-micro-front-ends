# Design Tokens Changelog

## 2026-02-19 — Semantic token audit and Tokens Studio setup

### Changes made

**Bootstrap token prefixing**
- Prefixed 7 Bootstrap semantic color tokens with `bootstrap-` to avoid naming confusion: `primary`, `success`, `danger`, `warning`, `info`, `light`, `dark`

**Semantic-to-core reference linking**
- Audited all hardcoded values in `semantic.json` against `core.json`
- Replaced exact matches with `{ff.*}` references:
  - `color.color-border-light` → `{ff.color.secondary}` (#EDEDED)
  - `font-size.font-choice-head` → `{ff.font-size.font-size-xs}` (10px)
  - `font-size.font-modal-title` → `{ff.font-size.font-size-s}` (12px)
  - `font-size.breadcrumb.minimized` → `{ff.font-size.font-size-s}` (12px)
  - `font-size.drp.default` → `{ff.font-size.font-size-m}` (15px)
  - `font-size.url-input.default` → `{ff.font-size.font-size-m}` (15px)
  - `spacing.navbar-width` → `{ff.spacing.300}` (3rem)
  - `duration.drag-and-drop.anim-speed` → `{ff.duration.slow}` (0.3s)

**Tokens Studio alpha modifiers**
- Added `$extensions.studio.tokens.modify` for opacity-derived tokens that reference core colors:
  - `multiselect.primary-border` → `{ff.color.primary-dark}` + alpha 0.5
  - `multiselect.primary-border-disabled` → `{ff.color.primary-dark}` + alpha 0.25
  - `dropdown.primary-border` → `{ff.color.primary-dark}` + alpha 0.5
  - `dropdown.primary-disabled-border` → `{ff.color.primary-dark}` + alpha 0.25
  - `table.shadow` → `{ff.color.black}` + alpha 0.25

**Combined tokens file**
- Created `tokens/tokens.json` combining core and semantic sets for Tokens Studio free-tier single-file GitHub sync
- Top-level keys `"core"` and `"semantic"` map to token sets in Tokens Studio

### Decisions

- **No new core tokens** — hardcoded values that don't match existing core tokens remain in `semantic.json`
- **Tokens Studio + Style Dictionary** pipeline: `studio.tokens` `$extensions` format used for alpha modifiers (compatible with both tools)
- `core.json` and `semantic.json` remain as source-of-truth files; `tokens.json` is the combined sync target

### Observations

- `secondary-hover-border` (`rgba(107, 114, 128, 0.3)`) — base `#6B7280` has no core token match; closest is `ff.color.gray-dark` (`#7C7D7F`). Used only on `:hover:not(.selected)` for secondary variant in `DropdownMultiSelect` and `SelectDropdown`. No production consumer currently passes `variant="secondary"` — only exercised in Storybook.
- `text.primary` / `color-text-primary` (`#212529`) — declared in `_dateRangePicker.scss:35` but the SCSS variable is never consumed by any component.
- Semantic `radius.sm/md/lg/modal` (17.5–25.5px) are a separate, larger scale from core `ff.radius.*` (3–6px). The semantic radii are legacy values defined as CSS custom properties in `_theme.scss:199-202`, heavily used (~40 instances) across modals, buttons, cards, and containers.
- Four brand colours (`primary`, `primary-dark`, `secondary`, `secondary-dark`) exist in core but serve different roles than the Bootstrap semantic tokens (e.g., `bootstrap-primary` maps to `indigo-100`, not `primary`).
