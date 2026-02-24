# Unused Core Tokens

**Status:** v2.0 audit (buttons & forms only)
**Date:** 2026-02-23
**Audited by:** Cross-referencing `core.json` against `semantic.json` references and the component token reference map

**Counts:**
- Total core tokens: 85
- Referenced by `semantic.json`: 46
- Referenced by components only (not via semantic): 3 (`ff.color.primary`, `ff.color.secondary`, `ff.color.gray-dark`)
- Total referenced (semantic + components): 49
- Unreferenced: 36

> **Note on research estimate:** The Phase 5 research document estimated 160 core tokens based on a prior Phase 1 audit. The actual count after reading `core.json` directly is 85. The discrepancy likely reflects that the v1.0 implementation was scoped down from the original audit scope. The 85-token count is the source of truth for this document.

---

## Unreferenced Tokens

These 36 tokens are not referenced by `semantic.json` $value fields or by any button/form component in the v2.0 scope. They may still be used directly in SCSS files via hardcoded CSS custom property references (e.g., `var(--blue-100)`) that bypass the token system.

### Color — Opacity Variants (palette shades -200 and -300)

The -200 and -300 suffix tokens are opacity variants of their base palette color. Most are unused because semantic.json references only the base (-100) color and applies opacity modifications via `$extensions.studio.tokens.modify` where needed.

| Token Path | Category | Value | Likely Future Use |
|---|---|---|---|
| `ff.color.yellow-200` | color/opacity | `rgba(239, 192, 5, 0.5)` | Warning backgrounds (hover states in alert components) |
| `ff.color.yellow-300` | color/opacity | `rgba(239, 192, 5, 0.25)` | Warning subtle backgrounds |
| `ff.color.green-200` | color/opacity | `rgba(0, 196, 154, 0.5)` | Success backgrounds |
| `ff.color.green-300` | color/opacity | `rgba(0, 196, 154, 0.25)` | Success subtle backgrounds |
| `ff.color.cyan-200` | color/opacity | `rgba(0, 188, 212, 0.5)` | Info backgrounds |
| `ff.color.cyan-300` | color/opacity | `rgba(0, 188, 212, 0.25)` | Info subtle backgrounds |
| `ff.color.blue-200` | color/opacity | `rgba(0, 135, 217, 0.5)` | Info/link hover backgrounds |
| `ff.color.blue-300` | color/opacity | `rgba(0, 135, 217, 0.25)` | Info/link subtle backgrounds |
| `ff.color.orange-200` | color/opacity | `rgba(255, 145, 0, 0.5)` | Danger hover backgrounds |
| `ff.color.orange-300` | color/opacity | `rgba(255, 145, 0, 0.25)` | Danger subtle backgrounds |
| `ff.color.vivid-200` | color/opacity | `rgba(124, 128, 254, 0.5)` | Primary focus rings / selected backgrounds |
| `ff.color.vivid-300` | color/opacity | `rgba(124, 128, 254, 0.25)` | Primary subtle backgrounds |
| `ff.color.red-200` | color/opacity | `rgba(229, 115, 115, 0.5)` | Error/warning hover backgrounds |
| `ff.color.red-300` | color/opacity | `rgba(229, 115, 115, 0.25)` | Error/warning subtle backgrounds |
| `ff.color.indigo-200` | color/opacity | `rgba(50, 72, 244, 0.5)` | Primary action focus rings |
| `ff.color.indigo-300` | color/opacity | `rgba(50, 72, 244, 0.25)` | Primary action subtle backgrounds |

### Color — Solid Colors Not Referenced

| Token Path | Category | Value | Notes |
|---|---|---|---|
| `ff.color.green-100` | color/solid | `#00c49a` | Teal-green. v1.0 uses `ff.color.green` (`#57C20A`) and `ff.color.green-dark` for bootstrap-success. This palette green not yet referenced. |
| `ff.color.blue-100` | color/solid | `#0087d9` | Blue. No blue-themed component in v2.0 scope. Likely for future link/info tokens. |
| `ff.color.gray-medium-darker` | color/solid | `#9E9E9E` | Neutral gray between `gray-dark` (`#7C7D7F`) and `gray-medium-dark` (`#B7B7B8`). Not directly used in button/form SCSS. |
| `ff.color.gray-light` | color/solid | `#D9D9D9` | Very close to `gray-x-light` (`#E5E5E5`). Not directly referenced in button/form SCSS. |
| `ff.color.green` | color/solid | `#57C20A` | Legacy green (non-palette). Distinct from `green-100` (teal). Used in some SCSS but not tokenized in semantic.json for buttons/forms. |

### Spacing — Odd-step Scale Values

The semantic spacing tokens use every-other step of the scale (025, 050, 100, 150, 200, 300). The odd-step values are in core.json for completeness but have no semantic alias yet.

| Token Path | Category | Value | Notes |
|---|---|---|---|
| `ff.spacing.075` | spacing | `0.75rem` | Between xs/sm (0.25/0.5rem) and md (1rem). |
| `ff.spacing.125` | spacing | `1.25rem` | Between md (1rem) and lg (1.5rem). |
| `ff.spacing.175` | spacing | `1.75rem` | Between lg (1.5rem) and xl (2rem). |
| `ff.spacing.225` | spacing | `2.25rem` | Above xl (2rem). |
| `ff.spacing.250` | spacing | `2.5rem` | Text input height uses `2.5rem` hardcoded — no spacing token covers this. |
| `ff.spacing.275` | spacing | `2.75rem` | Above spacing.225. |

> `ff.spacing.250` is particularly notable: the text input component has `height: 2.5rem` hardcoded. This token exists in core.json and could be used for a `form.text-input.height` token, but height is a layout dimension excluded from v2.0 component token scope.

### Font Size — Larger Scale Values

| Token Path | Category | Value | Notes |
|---|---|---|---|
| `ff.font-size.font-size-xl` | font-size | `20px` | Heading size. Not used by buttons or form inputs. |
| `ff.font-size.font-size-l` | font-size | `18px` | Sub-heading size. Not used by buttons or form inputs. |

### Font Weight — Redundant or Unused Scale Values

The font-weight scale has both numeric suffix names (`font-weight-xs`, `-sm`, `-md`, `-lg`, `-xl`) and descriptive names (`font-weight-light`, `-regular`, `-medium`, `-semibold`). Semantic.json references only the descriptive names, leaving the numeric names orphaned.

| Token Path | Category | Value | Notes |
|---|---|---|---|
| `ff.font-weight.font-weight-xs` | font-weight | `300` | Duplicate of `font-weight-light`. Numeric name alias, unreferenced. |
| `ff.font-weight.font-weight-sm` | font-weight | `400` | Duplicate of `font-weight-regular`. Numeric name alias, unreferenced. |
| `ff.font-weight.font-weight-md` | font-weight | `500` | Duplicate of `font-weight-medium`. Numeric name alias, unreferenced. |
| `ff.font-weight.font-weight-lg` | font-weight | `600` | Duplicate of `font-weight-semibold`. Numeric name alias, unreferenced. |
| `ff.font-weight.font-weight-light` | font-weight | `300` | Descriptive name exists but not referenced by semantic.json or components. |

> **Deduplication opportunity (deferred):** The font-weight scale has two naming systems for the same values. A future pass could remove the numeric aliases (`font-weight-xs` through `font-weight-xl`) and use only the descriptive names. This is OUT OF SCOPE for v2.0.

### Typography — Line Height and Letter Spacing

| Token Path | Category | Value | Notes |
|---|---|---|---|
| `ff.line-height.line-height-default` | line-height | `100%` | Exists in core.json. No semantic.json reference. The button SCSS uses `var(--line-height-default)` directly but the CSS custom property is not bridged through a semantic token. |
| `ff.letter-spacing.letter-spacing-default` | letter-spacing | `0%` | Exists in core.json. The text input SCSS uses `letter-spacing: 0` hardcoded without referencing the token. |

---

## Referenced Tokens Summary

For completeness, the 49 tokens that ARE referenced (directly by semantic.json or by components):

**Referenced by semantic.json (46):**

| Token Path | Referenced By |
|---|---|
| `ff.color.indigo-100` | `color.action.primary`, `color.bootstrap-primary` |
| `ff.color.green-dark` | `color.bootstrap-success` |
| `ff.color.red-100` | `color.bootstrap-danger` |
| `ff.color.yellow-100` | `color.bootstrap-warning` |
| `ff.color.cyan-100` | `color.bootstrap-info` |
| `ff.color.white-100` | `color.bootstrap-light`, `color.navbar.bg-color` |
| `ff.color.black` | `color.bootstrap-dark`, `color.button.btn-color`, `color.text.primary`, `color.table.shadow` |
| `ff.color.white` | `color.background.default` |
| `ff.color.primary-dark` | `color.app.progress-bar-bg-color`, `color.multiselect.primary-border`, `color.dropdown.primary-border` |
| `ff.color.white-300` | `color.app.main-bg` |
| `ff.color.gray-x-light` | `color.app.pill-bg-color`, `color.select-custom-value.border-color` |
| `ff.color.secondary-dark` | `color.navbar.menu-font-color` |
| `ff.color.gray-dark` | `color.navbar.submenu-font-color` |
| `ff.color.vivid-100` | `color.navbar.menu-font-color-active` |
| `ff.color.secondary` | `color.color-border-light` |
| `ff.color.gray-medium` | `color.color-divider`, `color.color-secondary` |
| `ff.color.gray-medium-dark` | `color.color-divider-dark`, `color.color-text-placeholder`, `color.color-text-light` |
| `ff.color.gray-darkest` | `color.color-main` |
| `ff.color.gray-xx-light` | `color.table.border-color` |
| `ff.color.transparent` | `color.form-builder.bg-transparent`, `color.url-input.copy-button-bg` |
| `ff.color.white-200` | (indirectly via multiselect/dropdown alpha modifications) |
| `ff.spacing.025` | `spacing.xs` |
| `ff.spacing.050` | `spacing.sm` |
| `ff.spacing.100` | `spacing.md` |
| `ff.spacing.150` | `spacing.lg` |
| `ff.spacing.200` | `spacing.xl` |
| `ff.spacing.300` | `spacing.navbar-width` |
| `ff.font-family.font-family-base` | `font-family.body`, `font-family.heading` |
| `ff.font-size.font-size-m` | `font-size.font-size-15`, `font-size.drp.default`, `font-size.url-input.default` |
| `ff.font-size.font-size-s` | `font-size.font-modal-title`, `font-size.font-size-12`, `font-size.breadcrumb.minimized` |
| `ff.font-size.font-size-xs` | `font-size.font-choice-head` |
| `ff.font-weight.font-weight-regular` | `font-weight.normal`, `font-weight.drp-font-weight` |
| `ff.font-weight.font-weight-medium` | `font-weight.medium`, `font-weight.drp-font-weight-medium`, `font-weight.url-input-font-weight` |
| `ff.font-weight.font-weight-semibold` | `font-weight.semibold` |
| `ff.font-weight.font-weight-xl` | `font-weight.bold` |
| `ff.radius.xs` | `radius.checkbox.small` |
| `ff.radius.sm` | `radius.checkbox.default`, `radius.form-builder.default` |
| `ff.radius.md` | `radius.multiselect.default`, `radius.dropdown.default/menu/item`, `radius.drp.container`, `radius.alert.default`, `radius.search-input.default`, `radius.url-input.default` |
| `ff.radius.lg` | `radius.drp.calendar` |
| `ff.radius.xl` | `radius.switch.default` |
| `ff.radius.pill` | `radius.button.default`, `radius.multiselect.chip` |
| `ff.radius.full` | `radius.button.round`, `radius.form-builder.round`, `radius.status.default` |
| `ff.duration.fast` | `duration.button.duration`, `duration.checkbox.duration`, `duration.radio.duration`, `duration.dropdown.duration`, `duration.filterable-dropdown.duration`, `duration.url-input.duration`, `duration.breadcrumb.duration` |
| `ff.duration.normal` | `duration.dropdown-button.transition`, `duration.drp.duration`, `duration.search.duration`, `duration.switch.duration`, `duration.alert.exit-duration` |
| `ff.duration.slow` | `duration.drag-and-drop.anim-speed`, `duration.alert.duration/enter-duration` |
| `ff.duration.timing-ease` | `duration.dropdown-button.timing`, `duration.drp.timing`, `duration.search.timing` |
| `ff.duration.timing-ease-in-out` | `duration.button.timing`, `duration.checkbox.timing`, `duration.radio.timing`, `duration.dropdown.timing`, `duration.filterable-dropdown.timing`, `duration.url-input.timing`, `duration.switch.timing`, `duration.alert.timing`, `duration.breadcrumb.timing` |

**Referenced by components only (not via semantic, 3 tokens):**

| Token Path | Used By | Notes |
|---|---|---|
| `ff.color.primary` | Button primary selected background (`var(--primary)` -> `#F1EEFF`) | No semantic alias. Component token can reference core directly (2-level chain). |
| `ff.color.secondary` | Button secondary selected background (`var(--secondary)` -> `#EDEDED`) | No semantic alias. Component token can reference core directly (2-level chain). |
| `ff.color.gray-dark` | Text input placeholder color and focus border-color (`var(--gray-dark)` -> `#7C7D7F`) | No semantic alias for this exact purpose. Component token references core directly. |

---

## Notes

- **No pruning:** Per user decision, `core.json` is kept complete as the v1.0 primitive layer. Unused tokens are flagged here without removing them from `core.json`. Future component expansions (nav, tables, modals, cards) will likely reference many of these tokens.
- **Separate document approach:** Token usage is tracked in this external document rather than annotating `core.json` with `[UNUSED]` comments. This keeps `core.json` as pure DTCG format without editorial metadata.
- **SCSS usage not captured:** Some of these "unused" tokens may be referenced directly in SCSS files via CSS custom properties (e.g., `var(--blue-100)`) without going through the token system. This audit only captures token-system references (semantic.json `$value` and component token references). Direct SCSS usage is not tracked here.
- **Opacity variants pattern:** The -200 and -300 opacity variants (e.g., `ff.color.yellow-200`) are likely intentional placeholder tokens for future expansion. The current semantic.json applies opacity modifications via `$extensions.studio.tokens.modify` on the base token rather than referencing pre-computed opacity variants.
