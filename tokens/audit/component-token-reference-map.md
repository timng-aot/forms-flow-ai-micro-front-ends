# Component Token Reference Map

**Version:** v2.0 planning audit
**Date:** 2026-02-23
**Scope:** Button variants (primary, secondary, error/danger, warning) and form elements (text input, checkbox)
**Purpose:** Phase 6 and 7 implementers use this document to know exactly which v1.0 tokens to reference when writing `components.json`.

---

## 1. Button Token Reference Map

Button SCSS uses two indirection layers before reaching a core token value:
- **Layer 1:** SCSS variable (e.g. `$color-primary-border`) defined at top of `_button.scss`
- **Layer 2:** CSS custom property (e.g. `var(--primary-dark)`) that the SCSS var resolves to
- **Layer 3:** Core token path (e.g. `ff.color.primary-dark`) and hex value

### Shared Static Properties (state-independent, no state segment in component token name)

These properties do not change across interactive states. They use a shared component token without a state segment (e.g., `button.primary.border-radius`, not `button.primary.hover.border-radius`).

| CSS Property | SCSS Variable | CSS Custom Property | Core Token | Value | Semantic Token |
|---|---|---|---|---|---|
| border-radius | `$button-border-radius: 1.5625rem` | (hardcoded rem) | `ff.radius.pill` | `1.5625rem` | `radius.button.default` -> `{ff.radius.pill}` YES |
| font-size | `$button-font-size` | `var(--font-size-m)` | `ff.font-size.font-size-m` | `15px` | `font-size.font-size-15` -> `{ff.font-size.font-size-m}` (alias exists) |
| font-weight | `$button-font-weight` | `var(--font-weight-regular)` | `ff.font-weight.font-weight-regular` | `400` | `font-weight.normal` -> `{ff.font-weight.font-weight-regular}` YES |
| transition-duration | `$button-transition-duration: 0.15s` | (hardcoded) | `ff.duration.fast` | `0.15s` | `duration.button.duration` -> `{ff.duration.fast}` YES |
| transition-timing | `$button-transition-timing: ease-in-out` | (hardcoded) | `ff.duration.timing-ease-in-out` | `ease-in-out` | `duration.button.timing` -> `{ff.duration.timing-ease-in-out}` YES |

### Primary Button (`custom-button--primary`)

SCSS color variables for primary: `$color-primary = var(--vivid-100)`, `$color-primary-light = var(--primary-dark)`, `$color-primary-border = var(--primary-dark)`, `$color-primary-selected = var(--primary)`, `$color-light-gray = var(--white-200)`, `$color-white = var(--white-300)`, `$color-dark-gray = var(--gray-darkest)`, `$color-medium-gray = var(--gray-x-light)`, `$color-primary-disabled = var(--gray-medium)`.

| State | CSS Property | SCSS Variable | CSS Custom Property | Core Token | Value | Semantic Token |
|---|---|---|---|---|---|---|
| default | background | `$color-light-gray` | `var(--white-200)` | `ff.color.white-200` | `#FCFCFC` | needs `color.background.surface` |
| default | border-color | `$color-primary-border` | `var(--primary-dark)` | `ff.color.primary-dark` | `#B8ABFF` | needs `color.action.primary-border` |
| default | color (text) | `$color-dark-gray` | `var(--gray-darkest)` | `ff.color.gray-darkest` | `#4A4A4A` | needs `color.text.default` |
| hover | background | `$color-white` | `var(--white-300)` | `ff.color.white-300` | `#FFFFFF` | `color.background.default` -> `{ff.color.white}` YES (partial — `white` = `#fff`) |
| hover | border-color | `$color-primary-light` | `var(--primary-dark)` | `ff.color.primary-dark` | `#B8ABFF` | needs `color.action.primary-border` (same as default) |
| hover | shadow | `$button-shadow-primary` | (hardcoded rgba) | — | `rgba(137, 105, 242, 0.15)` | `shadow.button.primary` YES |
| focus | border-color | `$color-primary` | `var(--vivid-100)` | `ff.color.vivid-100` | `#7c80fe` | `color.action.primary` -> `{ff.color.indigo-100}` (WRONG — `indigo-100` is `#3248f4`, not `#7c80fe`) |
| selected | background | `$color-primary-selected` | `var(--primary)` | `ff.color.primary` | `#F1EEFF` | no exact semantic token |
| selected | border-color | `$color-primary-light` | `var(--primary-dark)` | `ff.color.primary-dark` | `#B8ABFF` | needs `color.action.primary-border` |
| disabled | background | `$color-light-gray` | `var(--white-200)` | `ff.color.white-200` | `#FCFCFC` | needs `color.background.surface` |
| disabled | border-color | `$color-primary-disabled` | `var(--gray-medium)` | `ff.color.gray-medium` | `#D1D2D3` | no semantic token for disabled state |
| disabled | color (text) | `$color-medium-gray` | `var(--gray-x-light)` | `ff.color.gray-x-light` | `#E5E5E5` | no semantic token |

> **Note on focus:** `$color-primary = var(--vivid-100)` resolves to `ff.color.vivid-100` (`#7c80fe`). The existing `color.action.primary` semantic token references `ff.color.indigo-100` (`#3248f4`), which is a different blue. For v2.0 component tokens, the focus border-color should reference `ff.color.vivid-100` directly (2-level chain) rather than the incorrectly named `color.action.primary`.

### Secondary Button (`custom-button--secondary`)

SCSS color variables: `$color-medium-gray = var(--gray-x-light)`, `$color-darker-gray = var(--secondary-dark)`, `$color-selected-gray = var(--secondary)`, `$color-disabled-gray = var(--gray-medium)`.

| State | CSS Property | SCSS Variable | CSS Custom Property | Core Token | Value | Semantic Token |
|---|---|---|---|---|---|---|
| default | background | `$color-light-gray` | `var(--white-200)` | `ff.color.white-200` | `#FCFCFC` | needs `color.background.surface` |
| default | border-color | `$color-medium-gray` | `var(--gray-x-light)` | `ff.color.gray-x-light` | `#E5E5E5` | needs `color.action.secondary-border` |
| default | color (text) | `$color-dark-gray` | `var(--gray-darkest)` | `ff.color.gray-darkest` | `#4A4A4A` | needs `color.text.default` |
| hover | background | `$color-white` | `var(--white-300)` | `ff.color.white-300` | `#FFFFFF` | `color.background.default` YES |
| hover | border-color | `$color-darker-gray` | `var(--secondary-dark)` | `ff.color.secondary-dark` | `#525254` | no semantic token |
| hover | shadow | `$button-shadow-secondary` | (hardcoded rgba) | — | `rgba(0, 0, 0, 0.1)` | `shadow.button.secondary` YES |
| focus | border-color | `$color-darker-gray` | `var(--secondary-dark)` | `ff.color.secondary-dark` | `#525254` | no semantic token |
| selected | background | `$color-selected-gray` | `var(--secondary)` | `ff.color.secondary` | `#EDEDED` | no semantic token |
| selected | border-color | `$color-darker-gray` | `var(--secondary-dark)` | `ff.color.secondary-dark` | `#525254` | no semantic token |
| disabled | background | `$color-light-gray` | `var(--white-200)` | `ff.color.white-200` | `#FCFCFC` | needs `color.background.surface` |
| disabled | border-color | `$color-medium-gray` | `var(--gray-x-light)` | `ff.color.gray-x-light` | `#E5E5E5` | needs `color.action.secondary-border` |
| disabled | color (text) | `$color-disabled-gray` | `var(--gray-medium)` | `ff.color.gray-medium` | `#D1D2D3` | no semantic token |

### Error Button (`custom-button--error`) — v2.0 Name: "danger"

> **CRITICAL NAMING FINDING — Error vs. Danger:** The SCSS variant is named `--error` and uses `$color-error = var(--orange-100)` (`ff.color.orange-100`, `#ff9100` — orange). The existing `color.bootstrap-danger` semantic token references `ff.color.red-100` (`#e57373` — red). These are different colors mapped to confusingly inverted names.
>
> **v2.0 resolution:** The v2.0 component token will be named `button.danger` (matching the user-intent: destructive/danger action). It will reference `color.action.danger` -> `{ff.color.orange-100}` to preserve the v1.0 visual behavior. The separate `color.feedback.error` token maps to `ff.color.red-100` for form validation errors. This separates UI feedback color (error = red) from button danger action color (danger = orange).

SCSS color variables for error variant: `$color-error = var(--orange-100)`, `$color-error-light = var(--orange-100)`, `$color-error-border = var(--orange-100)`, `$color-error-selected = var(--orange-100)`, `$color-error-disabled = var(--gray-medium)`.

| State | CSS Property | SCSS Variable | CSS Custom Property | Core Token | Value | Semantic Token |
|---|---|---|---|---|---|---|
| default | background | `$color-light-gray` | `var(--white-200)` | `ff.color.white-200` | `#FCFCFC` | needs `color.background.surface` |
| default | border-color | `$color-error-border` | `var(--orange-100)` | `ff.color.orange-100` | `#ff9100` | needs `color.action.danger` |
| default | color (text) | `$color-dark-gray` | `var(--gray-darkest)` | `ff.color.gray-darkest` | `#4A4A4A` | needs `color.text.default` |
| hover | background | `$color-white` | `var(--white-300)` | `ff.color.white-300` | `#FFFFFF` | `color.background.default` YES |
| hover | border-color | `$color-error-light` | `var(--orange-100)` | `ff.color.orange-100` | `#ff9100` | needs `color.action.danger` |
| hover | shadow | `$button-shadow-error` | (hardcoded rgba) | — | `rgba(255, 87, 34, 0.1)` | `shadow.button.error` YES |
| focus | border-color | `$color-error` | `var(--orange-100)` | `ff.color.orange-100` | `#ff9100` | needs `color.action.danger` |
| selected | background | `$color-error-selected` | `var(--orange-100)` | `ff.color.orange-100` | `#ff9100` | needs `color.action.danger` |
| selected | color (text) | `$color-white` | `var(--white-300)` | `ff.color.white-300` | `#FFFFFF` | `color.background.default` (same value) |
| disabled | background | `$color-light-gray` | `var(--white-200)` | `ff.color.white-200` | `#FCFCFC` | needs `color.background.surface` |
| disabled | border-color | `$color-error-disabled` | `var(--gray-medium)` | `ff.color.gray-medium` | `#D1D2D3` | no semantic token |
| disabled | color (text) | `$color-medium-gray` | `var(--gray-x-light)` | `ff.color.gray-x-light` | `#E5E5E5` | no semantic token |

### Warning Button (`custom-button--warning`)

> **NAMING INVERSION FINDING:** The SCSS `--warning` variant uses `$color-warning = var(--red-100)` (`ff.color.red-100`, `#e57373` — red). This is the opposite of typical convention where warning = yellow/orange and danger/error = red. The v1.0 system uses warning = red and error = orange. The v2.0 component tokens will preserve this visual behavior but this finding should be tracked for a future normalization pass.

SCSS color variables for warning variant: `$color-warning = var(--red-100)`, `$color-warning-light = var(--red-100)`, `$color-warning-border = var(--red-100)`, `$color-warning-selected = var(--red-100)`, `$color-warning-disabled = var(--gray-medium)`.

| State | CSS Property | SCSS Variable | CSS Custom Property | Core Token | Value | Semantic Token |
|---|---|---|---|---|---|---|
| default | background | `$color-light-gray` | `var(--white-200)` | `ff.color.white-200` | `#FCFCFC` | needs `color.background.surface` |
| default | border-color | `$color-warning-border` | `var(--red-100)` | `ff.color.red-100` | `#e57373` | `color.bootstrap-danger` -> `{ff.color.red-100}` exists but wrong intent name |
| default | color (text) | `$color-dark-gray` | `var(--gray-darkest)` | `ff.color.gray-darkest` | `#4A4A4A` | needs `color.text.default` |
| hover | background | `$color-white` | `var(--white-300)` | `ff.color.white-300` | `#FFFFFF` | `color.background.default` YES |
| hover | border-color | `$color-warning-light` | `var(--red-100)` | `ff.color.red-100` | `#e57373` | `color.bootstrap-danger` (wrong intent) |
| hover | shadow | `$button-shadow-warning` | (hardcoded rgba) | — | `rgba(255, 152, 0, 0.1)` | `shadow.button.warning` YES |
| focus | border-color | `$color-warning` | `var(--red-100)` | `ff.color.red-100` | `#e57373` | `color.bootstrap-danger` (wrong intent) |
| selected | background | `$color-warning-selected` | `var(--red-100)` | `ff.color.red-100` | `#e57373` | `color.bootstrap-danger` (wrong intent) |
| selected | color (text) | `$color-white` | `var(--white-300)` | `ff.color.white-300` | `#FFFFFF` | `color.background.default` |
| disabled | background | `$color-light-gray` | `var(--white-200)` | `ff.color.white-200` | `#FCFCFC` | needs `color.background.surface` |
| disabled | border-color | `$color-warning-disabled` | `var(--gray-medium)` | `ff.color.gray-medium` | `#D1D2D3` | no semantic token |
| disabled | color (text) | `$color-medium-gray` | `var(--gray-x-light)` | `ff.color.gray-x-light` | `#E5E5E5` | no semantic token |

> **v2.0 resolution for warning:** Create `color.feedback.warning` -> `{ff.color.red-100}` to give intent-correct naming. The v2.0 `button.warning` component token will reference `color.feedback.warning`. This leaves the door open to fix the orange/red inversion in a future color palette update.

---

## 2. Form Token Reference Map

### Text Input (`_textInput.scss`)

The text input SCSS uses a clean one-layer mapping: SCSS vars (`$ti-*`) resolve directly to CSS custom properties, which map to core tokens.

**Shared static properties (state-independent):**

| CSS Property | SCSS Variable | CSS Custom Property | Core Token | Value | Semantic Token |
|---|---|---|---|---|---|
| background | `$ti-color-bg` | `var(--white-200)` | `ff.color.white-200` | `#FCFCFC` | needs `color.background.surface` |
| font-size | `$ti-font-size` | `var(--font-size-m)` | `ff.font-size.font-size-m` | `15px` | `font-size.font-size-15` -> `{ff.font-size.font-size-m}` YES |
| font-weight | `$ti-font-weight` | `var(--font-weight-regular)` | `ff.font-weight.font-weight-regular` | `400` | `font-weight.normal` -> `{ff.font-weight.font-weight-regular}` YES |
| border-radius | (hardcoded `5px`) | — | `ff.radius.md` | `0.3125rem` (≈5px) | no direct semantic; use core directly |
| color (text) | `$ti-color-text` | `var(--gray-darkest)` | `ff.color.gray-darkest` | `#4A4A4A` | needs `color.text.default` |

**State-dependent properties:**

| State | CSS Property | SCSS Variable | CSS Custom Property | Core Token | Value | Semantic Token |
|---|---|---|---|---|---|---|
| default | border-color | `$ti-color-border` | `var(--gray-x-light)` | `ff.color.gray-x-light` | `#E5E5E5` | needs `color.action.secondary-border` |
| placeholder | color | `$ti-color-placeholder` | `var(--gray-dark)` | `ff.color.gray-dark` | `#7C7D7F` | no semantic token |
| placeholder disabled | color | `$ti-color-placeholder-disabled` | `var(--gray-xx-light)` | `ff.color.gray-xx-light` | `#DAD9DA` | no semantic token |
| hover | border-color | `$ti-color-border-hover` | `var(--secondary-dark)` | `ff.color.secondary-dark` | `#525254` | no semantic token |
| focus/active | border-color | `$ti-color-border-focus` | `var(--gray-dark)` | `ff.color.gray-dark` | `#7C7D7F` | no semantic token |

**Out-of-scope for v2.0 component tokens (layout/dimension properties, not visual tokens):**
- `height: 2.5rem` — hardcoded, no core token
- `padding: 11px 10px` — hardcoded, no core token match

### Checkbox (`_checkbox.scss`)

> **CRITICAL FINDING — Checkbox does not use CSS var references.** Unlike buttons and text input, the checkbox SCSS uses hardcoded hex values and rgba values, NOT CSS custom property references (e.g. `var(--primary-dark)`). The v1.0 token system did not reach the checkbox component. This means the mapping requires hex-to-core-token cross-reference, not CSS var chain tracing.

**Hardcoded hex values used in `_checkbox.scss` and their core token equivalents:**

| SCSS Variable | Hardcoded Value | Closest Core Token | Core Value | Match Quality | Notes |
|---|---|---|---|---|---|
| `$color-white` | `#ffffff` | `ff.color.white-300` | `#FFFFFF` | Exact | Use `ff.color.white-300` |
| `$color-light-gray` | `#fcfcfc` | `ff.color.white-200` | `#FCFCFC` | Exact | Use `ff.color.white-200` |
| `$color-medium-gray` | `#B7B7B8` | `ff.color.gray-medium-dark` | `#B7B7B8` | Exact | Use `ff.color.gray-medium-dark` |
| `$color-dark-gray` | `#4a4a4a` | `ff.color.gray-darkest` | `#4A4A4A` | Exact | Use `ff.color.gray-darkest` |
| `$color-darker-gray` | `#525254` | `ff.color.secondary-dark` | `#525254` | Exact | Use `ff.color.secondary-dark` |
| `$color-disabled-gray` | `#c5c5c5` | — | — | No match | `gray-medium` is `#D1D2D3`, `gray-x-light` is `#E5E5E5` — no exact match |
| `$color-primary-selected` | `#8969f2` | — | — | No match | GAP: see below |
| `$color-primary` (rgba) | `rgba(184, 171, 255, 1)` = `#B8ABFF` | `ff.color.primary-dark` | `#B8ABFF` | Exact | Use `ff.color.primary-dark` |
| `$color-primary-light` | `#b8abff` | `ff.color.primary-dark` | `#B8ABFF` | Exact | Same as above |

> **The `#8969f2` gap — `$color-primary-selected`:** This value (`#8969f2`, a medium purple) does not match any token in `core.json`. The closest tokens are `ff.color.vivid-100` (`#7c80fe`, blue-purple) and `ff.color.primary-dark` (`#B8ABFF`, light purple). Neither is close enough to use without a visual change.
>
> **Recommendation:** Do NOT add `#8969f2` to `core.json`. For v2.0 component tokens, reference `ff.color.vivid-100` as the closest available value, or introduce a new semantic token `color.action.primary-selected` -> `{ff.color.vivid-100}` to acknowledge the gap explicitly. This will produce a slight visual change from `#8969f2` to `#7c80fe` (both are blue-purple, different shade). Document this as an intentional normalization in Phase 6.

**Checkbox state mapping:**

| State | CSS Property | Hardcoded Value | Core Token | Semantic Token |
|---|---|---|---|---|
| default | border-color | `#b8abff` (`$color-primary-light`) | `ff.color.primary-dark` | needs `color.action.primary-border` |
| default | background | `#ffffff` (`$color-white`) | `ff.color.white-300` | `color.background.default` |
| hover/focus | border-color | `#8969f2` (`$color-primary-selected`) | `ff.color.vivid-100` (approximate) | needs `color.action.primary-selected` (new) |
| checked | border-color | `rgba(184, 171, 255, 1)` (`$color-primary`) | `ff.color.primary-dark` | needs `color.action.primary-border` |
| checked | background | `#ffffff` | `ff.color.white-300` | `color.background.default` |
| checked (checkmark) | border-color | `rgba(184, 171, 255, 1)` | `ff.color.primary-dark` | needs `color.action.primary-border` |
| checked+focus | border-color | `#8969f2` | `ff.color.vivid-100` (approximate) | needs `color.action.primary-selected` |
| checked+focus | background | `#8969f2` | `ff.color.vivid-100` (approximate) | needs `color.action.primary-selected` |
| disabled | border-color | `#fcfcfc` (`$color-light-gray`) | `ff.color.white-200` | needs `color.background.surface` |
| disabled | background | `#fcfcfc` | `ff.color.white-200` | needs `color.background.surface` |
| disabled (label) | color | `#c5c5c5` (`$color-disabled-gray`) | — | no core match — use `ff.color.gray-medium` as nearest |
| label | color | `#4a4a4a` (`$color-dark-gray`) | `ff.color.gray-darkest` | needs `color.text.default` |

---

## 3. New Semantic Tokens Needed

These semantic tokens must be added to `semantic.json` to support component token references. None of these exist in the current v1.0 `semantic.json`.

| Semantic Token Path | Core Token Reference | Core Value | Rationale |
|---|---|---|---|
| `color.action.primary-border` | `{ff.color.primary-dark}` | `#B8ABFF` | Used by primary button (default, hover, selected border-color) and checkbox default border. Shared across multiple components — semantic layer adds value. |
| `color.action.secondary-border` | `{ff.color.gray-x-light}` | `#E5E5E5` | Used by secondary button default border and text input default border. Shared value justifies semantic token. |
| `color.action.danger` | `{ff.color.orange-100}` | `#ff9100` | Used by the SCSS `--error` button variant (renamed `danger` in v2.0). Named `danger` because it signals a destructive action. Orange color is the v1.0 visual for this intent. |
| `color.action.primary-selected` | `{ff.color.vivid-100}` | `#7c80fe` | Used by checkbox hover/focus state. Bridges the `#8969f2` gap with nearest available core token. |
| `color.feedback.error` | `{ff.color.red-100}` | `#e57373` | Used by form validation error states. Distinct from `color.action.danger` (destructive action) — this is a feedback signal, not an action variant. |
| `color.feedback.warning` | `{ff.color.red-100}` | `#e57373` | Used by the SCSS `--warning` button variant. Maps to red because v1.0 used red for warning (inverted from convention). Documents the existing behavior without hiding it. |
| `color.background.surface` | `{ff.color.white-200}` | `#FCFCFC` | Used as the default background for buttons (all variants, default/disabled state) and text input. Shared across components — semantic layer adds value as it names the intent (surface vs. pure white). |
| `color.text.default` | `{ff.color.gray-darkest}` | `#4A4A4A` | Used as text color in primary, secondary, error buttons (default state) and text input, checkbox label. The existing `color.text.primary` -> `{ff.color.black}` maps to `#000000` — wrong value. This token correctly names the actual text color used. |

**Existing semantic tokens that components CAN already reference (no new tokens needed):**

| Semantic Token | Core Reference | Used By |
|---|---|---|
| `shadow.button.primary` | inline value | Primary button hover shadow |
| `shadow.button.secondary` | inline value | Secondary button hover shadow |
| `shadow.button.error` | inline value | Error/danger button hover shadow |
| `shadow.button.warning` | inline value | Warning button hover shadow |
| `radius.button.default` | `{ff.radius.pill}` | All button border-radius |
| `duration.button.duration` | `{ff.duration.fast}` | Button transition duration |
| `duration.button.timing` | `{ff.duration.timing-ease-in-out}` | Button transition timing |
| `color.background.default` | `{ff.color.white}` | Button hover/active background |
| `font-weight.normal` | `{ff.font-weight.font-weight-regular}` | Button and input font-weight |

---

## 4. Reference Depth Policy

**Rule:** Maximum 3 reference levels: `component -> semantic -> core`.
**Rule:** Skip the semantic layer when it adds no naming value. When the semantic name would only be an alias for a specific core token without meaningful intent difference, reference core directly (2-level chain).
**Rule:** When multiple components reference the same value with the same intent, use a shared semantic token. Do not have independent core references that could drift out of sync.

### 3-Level Chain: Component -> Semantic -> Core

Use when: multiple components share the value, or the semantic name communicates intent that the core name does not.

**Example — Primary button border-color (default):**
```
button.primary.border-color
  -> {color.action.primary-border}       (semantic: "this is the primary action border")
     -> {ff.color.primary-dark}          (core: brand palette token)
        -> #B8ABFF                       (resolved value)
```

CSS output with `outputReferences: true`:
```css
--ff-button-primary-border-color: var(--ff-color-action-primary-border);
--ff-color-action-primary-border: var(--ff-color-primary-dark);
--ff-color-primary-dark: #B8ABFF;
```

**Example — Primary button hover shadow:**
```
button.primary.hover.shadow
  -> {shadow.button.primary}             (semantic: "primary button hover shadow definition")
     -> rgba(137, 105, 242, 0.15) ...   (inline value — shadow tokens don't reference core)
```

**Example — Text input default text color:**
```
form.text-input.color
  -> {color.text.default}                (semantic: "default text color in components")
     -> {ff.color.gray-darkest}          (core: specific gray palette token)
        -> #4A4A4A
```

### 2-Level Chain: Component -> Core (skip semantic)

Use when: only one component uses the value, or a semantic name would add no meaningful intent — it would just be a pass-through alias with no shared usage.

**Example — Button border-radius:**
```
button.border-radius
  -> {radius.button.default}            (semantic already exists and has clear intent)
     -> {ff.radius.pill}                (core)
        -> 1.5625rem
```

Note: `radius.button.default` is pre-existing in semantic.json, so this is still a 3-level chain. A true 2-level example:

**Example — Button focus border-color (primary):**
```
button.primary.focus.border-color
  -> {ff.color.vivid-100}              (core: directly, because only primary focus uses vivid-100)
     -> #7c80fe
```

CSS output:
```css
--ff-button-primary-focus-border-color: var(--ff-color-vivid-100);
--ff-color-vivid-100: #7c80fe;
```

**Example — Text input border-radius:**
```
form.text-input.border-radius
  -> {ff.radius.md}                    (core: directly, 5px, hardcoded in SCSS — only one component)
     -> 0.3125rem
```

### Decision Flowchart

```
Is the value shared across 2+ components with the same intent?
  YES -> Use semantic token (3-level chain)
  NO  -> Does a semantic token already exist for this value/intent?
           YES -> Use it (3-level chain is fine)
           NO  -> Reference core directly (2-level chain)
```

---

## 5. Form Element Scope Decision (v2.0)

**In scope for v2.0:**
- Text input (`_textInput.scss`) — primary form element, covers the key text entry pattern
- Checkbox (`_checkbox.scss`) — selection control, covers the binary choice pattern

**Out of scope for v2.0 (deferred to v3.0):**
- Select / filterable dropdown — similar pattern to text input but adds complexity (open/close states, option highlighting)
- Textarea — extends text input with height dimension; can be addressed in v3.0 by extending form tokens
- Radio button — similar pattern to checkbox; can be addressed with minimal delta in v3.0

**Rationale:** Proving the component token pattern with two representative form elements (text entry + selection) is sufficient for v2.0. Expanding to all form controls in one pass risks scope explosion past the ~75-token budget and delays Phase 6 delivery. The two-element scope still demonstrates: CSS var chain tracing, hardcoded hex gap handling (`#8969f2`), and shared semantic token reuse between form elements and buttons.

---

## 6. Static Property Token Decision (v2.0)

**Included in v2.0 component tokens:**

| Property | Decision | Rationale |
|---|---|---|
| `font-size` | Include as shared button token | Both buttons and form inputs use `ff.font-size.font-size-m`. A single `button.font-size` token (2-level: -> `{ff.font-size.font-size-m}`) establishes the pattern and makes font size inspectable in Figma Token Studio without state explosion. |
| `font-weight` | Include as shared button token | Both buttons and form inputs use `font-weight.normal`. A single `button.font-weight` token (3-level: -> `{font-weight.normal}` -> `{ff.font-weight.font-weight-regular}`) demonstrates the chain correctly. |
| `transition-duration` | Include via existing semantic | `duration.button.duration` already exists in `semantic.json`. Reference it directly. No new token needed. |
| `transition-timing` | Include via existing semantic | `duration.button.timing` already exists. Reference it directly. |

**Excluded from v2.0 component tokens:**

| Property | Decision | Rationale |
|---|---|---|
| `border-width` | Exclude | `1px` is a dimension primitive with no semantic meaning. It does not change across variants or states. Making it a token would produce `button.border-width: {ff.spacing.???}` — but no `1px` spacing token exists in core.json (spacing starts at `0.25rem`). Direct hardcoded value is cleaner here. |
| `min-width` | Exclude | Layout dimension (`5rem`) is not a visual token. Not relevant to Figma Token Studio's use case (visual properties). |
| `min-height` | Exclude | Same as min-width — layout dimension not appropriate for token layer. |
| `padding` | Exclude | Multi-value shorthand (`0.6875rem 1.375rem`) doesn't map cleanly to the spacing scale and is not a visual token. |
| `opacity` (disabled) | Exclude | `opacity: 0.6` is a hardcoded value applied to the disabled modifier class. No core token for opacity exists; prefer keeping it as a CSS rule rather than tokenizing a single magic number. |
