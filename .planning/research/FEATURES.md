# Feature Landscape: Component-Level Design Tokens for Buttons & Forms

**Domain:** Design token system (component layer)
**Researched:** 2026-02-10
**Focus:** Button and form component tokens for forms-flow-ai micro-frontends

## Context

This research builds on v1.0 (192 W3C DTCG tokens: 160 core + 32 semantic). v2.0 narrows scope to component-level tokens for buttons and forms, using CSS property-based naming instead of Figma-centric naming.

**Existing foundation:**
- Core tokens: colors (palettes), spacing, typography, borders, shadows, radius
- Semantic tokens: action.primary, background.default, text.primary, spacing.xs-xl
- Current SCSS: hardcoded values and basic var() references scattered across 7+ files

**Gap:** No component token layer mapping semantic tokens to specific button/form CSS properties and states.

---

## Table Stakes

Features users expect from component tokens. Missing = incomplete system, poor DX.

| Feature | Why Expected | Complexity | Dependencies | Notes |
|---------|--------------|------------|--------------|-------|
| **Button variant tokens** (primary, secondary, outlined, ghost) | Standard across all design systems (Material, Carbon, Atlassian) | Medium | Semantic color, spacing tokens | Each variant needs 4-5 states (default, hover, active, focus, disabled) |
| **Button state coverage** (default, hover, active, focus, disabled) | CSS requires state-specific values for proper UX | High | Core colors, opacity tokens | 5 states × 4 variants × 3-5 CSS properties = 60-100 tokens |
| **Button CSS property tokens** (background, border, color, shadow, padding, height, border-radius, font-size) | Direct mapping to CSS needed for DX | Medium | Core typography, spacing, shadow, radius | Must match CSS property names exactly |
| **Form input state tokens** (default, focus, error/invalid, disabled, valid) | HTML form validation requires distinct visual states | High | Semantic color tokens (success, danger, warning) | :focus, :invalid, :valid, :disabled pseudo-classes |
| **Form input CSS property tokens** (border, background, color, outline, shadow) | Core styling properties for text inputs, selects, textareas | Medium | Core colors, borders, shadows | Focus ring pattern especially critical for a11y |
| **Checkbox/radio state tokens** (unchecked, checked, indeterminate, hover, focus, disabled) | HTML checkbox supports indeterminate state via JS | High | Core colors for checkmark, box background, border | Indeterminate = horizontal line icon state |
| **Form validation visual feedback** (error border, error shadow, success border, warning) | Expected pattern across Bootstrap, Material, Carbon | Medium | Semantic danger, success, warning colors | Uses :valid/:invalid/:user-valid/:user-invalid pseudo-classes |
| **Size variants** (small, medium, large for buttons; standard, small for checkboxes) | Common across all component libraries | Low | Spacing, typography scale tokens | Existing SCSS has checkbox-size vs checkbox-size-small |
| **Semantic → component aliasing** (e.g., button.primary.background → color.action.primary) | Token architecture best practice (primitive → semantic → component) | Low | v1.0 semantic tokens | Establishes token relationships and single source of truth |
| **Focus indicators** (outline width, outline offset, outline color) | WCAG 2.1 accessibility requirement | Medium | Core colors (high contrast), spacing for offset | Must meet 3:1 contrast ratio minimum |

---

## Differentiators

Features that set this system apart. Not expected, but valued for this project.

| Feature | Value Proposition | Complexity | Dependencies | Notes |
|---------|-------------------|------------|--------------|-------|
| **CSS property naming** (background not fill, border not stroke) | Matches developer mental model, reduces translation overhead | Low | None | v1.0 used Figma naming; v2.0 switches to CSS naming for better DX |
| **Component-scoped CSS vars** (--ff-button-primary-background vs --ff-color-action-primary) | Clear intent, avoids semantic token misuse in wrong contexts | Medium | Naming convention design | Prevents using button.background on forms, etc. |
| **Single token for button height** (vs separate padding-top/bottom) | Matches existing SCSS pattern ($button-min-height: 2.5rem) | Low | Spacing tokens | Simpler than Bootstrap's padding-y approach |
| **Transition duration/timing tokens** (button.transition.duration, checkbox.transition.timing) | Animation consistency, supports prefers-reduced-motion | Low | Core duration tokens (if created) | Existing SCSS has $button-transition-duration: 0.15s |
| **Transform tokens for active state** (button.active.transform: translateY(1px)) | Existing pattern in _button.scss worth tokenizing | Low | None | Tactile feedback on button press |
| **Validation state prefixes** (input.error.*, input.valid.*) | Clearer than input.invalid.* for error messaging context | Low | Semantic danger/success/warning | Aligns with project terminology |
| **Explicit button gap token** (button.gap for icon spacing) | Existing SCSS pattern: $button-gap: var(--spacer-050) | Low | Spacing tokens | For icon + label layouts |
| **Spinner/loading state tokens** (button.spinner.size, button.spinner.border-width) | Existing SCSS pattern worth tokenizing | Low | None | For async button states |

---

## Anti-Features

Features to explicitly NOT build. Prevents scope creep.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| **Figma-centric naming** (fill, stroke, effects) | v1.0 lesson learned: poor DX for developers | Use CSS property names (background, border, shadow) |
| **Comprehensive component coverage** (accordions, modals, badges, etc.) | v2.0 scope is buttons + forms only | Document as future milestone, stay focused |
| **Platform-specific outputs** (iOS, Android, React Native) | Web-only project | CSS custom properties only |
| **Per-variant padding tokens** (button.primary.padding vs button.secondary.padding) | All button variants share same padding | Single button.padding token, reference spacing.md |
| **Dark mode / theming variants** | No requirement in project context | Single light theme, document as future enhancement |
| **Granular border tokens** (border-top-color separate from border-color) | Over-engineering, no use case identified | Single border-color token per component state |
| **Icon color tokens separate from text color** | Icons inherit button text color in existing SCSS | Use button.*.color for both text and icons |
| **Hover state for disabled buttons** | Disabled = pointer-events: none, no hover | Only default state for disabled |
| **Component tokens for units** (px, rem, em decisions) | Core token concern, not component-specific | Reference existing core tokens which already have units |

---

## Feature Dependencies

Component tokens build on v1.0 foundation:

```
Core Tokens (v1.0)
├─ color.* (yellow-100, blue-100, indigo-100, etc.)
├─ spacing.* (025, 050, 100, 150, 200, etc.)
├─ font-size.* (sm, m, l, xl, etc.)
├─ font-weight.* (regular, medium, semibold, xl)
├─ radius.* (sm, md, lg)
├─ shadow.* (if exists, else create)
└─ opacity.* (if exists, else create for disabled states)
    ↓
Semantic Tokens (v1.0)
├─ color.action.primary → {ff.color.indigo-100}
├─ color.danger → {ff.color.red-100}
├─ color.success → {ff.color.success}
├─ color.warning → {ff.color.yellow-100}
├─ spacing.xs → {ff.spacing.025}
└─ spacing.md → {ff.spacing.100}
    ↓
Component Tokens (v2.0 - NEW)
├─ button.primary.background → {color.action.primary}
├─ button.primary.color → {color.text.primary}
├─ button.primary.hover.background → (darken action.primary)
├─ input.border → {semantic.border.default}
├─ input.focus.outline → {color.action.primary}
├─ input.error.border → {color.danger}
└─ checkbox.checked.background → {color.action.primary}
```

**Critical dependencies for v2.0:**
- Must have: color.action.primary, color.danger, color.success, spacing tokens
- May need to create: shadow tokens (if not in v1.0), opacity tokens (0.6 for disabled)
- Migration path: Replace SCSS variables ($color-primary) with component tokens (var(--ff-button-primary-background))

---

## CSS Properties Requiring Tokenization

### Buttons (All Variants: Primary, Secondary, Outlined, Ghost)

Per variant, per state (default, hover, active, focus, disabled):

| CSS Property | Token Pattern | Example | States Needed |
|--------------|---------------|---------|---------------|
| `background-color` | `button.{variant}.{state}.background` | `button.primary.hover.background` | 5 states × 4 variants = 20 tokens |
| `border-color` | `button.{variant}.{state}.border` | `button.outlined.default.border` | 5 states × 4 variants = 20 tokens |
| `color` (text) | `button.{variant}.{state}.color` | `button.ghost.disabled.color` | 5 states × 4 variants = 20 tokens |
| `box-shadow` | `button.{variant}.{state}.shadow` | `button.primary.focus.shadow` | 2-3 states (focus, maybe hover) × 4 variants = ~10 tokens |
| `padding` | `button.padding` (shared) | `button.padding` | 1 token (all variants share) |
| `height` | `button.height` (shared) | `button.height` | 1 token (or min-height) |
| `border-radius` | `button.border-radius` (shared) | `button.border-radius` | 1 token |
| `font-size` | `button.font-size` (shared) | `button.font-size` | 1 token |
| `font-weight` | `button.font-weight` (shared) | `button.font-weight` | 1 token |
| `border-width` | `button.border-width` (shared) | `button.border-width` | 1 token |
| `gap` | `button.gap` (for icon spacing) | `button.gap` | 1 token |
| `transform` | `button.active.transform` (shared) | `button.active.transform` | 1 token (translateY) |
| `transition-duration` | `button.transition.duration` | `button.transition.duration` | 1 token |
| `transition-timing-function` | `button.transition.timing` | `button.transition.timing` | 1 token |
| `outline-width` (focus) | `button.focus.outline-width` | `button.focus.outline-width` | 1 token |
| `outline-offset` (focus) | `button.focus.outline-offset` | `button.focus.outline-offset` | 1 token |

**Estimated total button tokens:** ~70-80 (60 state-specific + 12 shared properties)

### Text Inputs (text, email, number, textarea, select)

| CSS Property | Token Pattern | Example | States Needed |
|--------------|---------------|---------|---------------|
| `border-color` | `input.{state}.border` | `input.focus.border`, `input.error.border` | 4-5 states (default, focus, error, valid, disabled) |
| `background-color` | `input.{state}.background` | `input.disabled.background` | 3 states (default, disabled, maybe focus) |
| `color` (text) | `input.{state}.color` | `input.default.color`, `input.disabled.color` | 2-3 states |
| `outline` (focus) | `input.focus.outline` | `input.focus.outline` (or split to outline-color, outline-width) | 1-2 tokens |
| `box-shadow` (focus, error) | `input.{state}.shadow` | `input.focus.shadow`, `input.error.shadow` | 2-3 tokens |
| `border-radius` | `input.border-radius` | `input.border-radius` | 1 token |
| `height` | `input.height` | `input.height` | 1 token |
| `padding` | `input.padding` | `input.padding` | 1 token |
| `font-size` | `input.font-size` | `input.font-size` | 1 token |
| `border-width` | `input.border-width` | `input.border-width` | 1 token |

**Estimated total input tokens:** ~20-25

### Checkboxes & Radio Buttons

| CSS Property | Token Pattern | Example | States Needed |
|--------------|---------------|---------|---------------|
| `border-color` | `checkbox.{state}.border` | `checkbox.checked.border`, `checkbox.indeterminate.border` | 6 states (unchecked, checked, indeterminate, hover, focus, disabled) |
| `background-color` | `checkbox.{state}.background` | `checkbox.disabled.background` | 3-4 states |
| `width`, `height` (box size) | `checkbox.size` | `checkbox.size` | 1 token (+ size variant) |
| Checkmark `border-color` | `checkbox.checkmark.{state}.color` | `checkbox.checkmark.checked.color` | 2-3 states |
| Checkmark `width`, `height` | `checkbox.checkmark.width`, `checkbox.checkmark.height` | Dimensions | 2 tokens |
| Checkmark `border-width` | `checkbox.checkmark.border-width` | Line thickness | 1 token |
| `border-width` (box) | `checkbox.border-width` | Box outline | 1 token |
| `border-radius` | `checkbox.border-radius` | Rounded corners | 1 token |
| `opacity` (disabled) | `checkbox.disabled.opacity` | 0.6 typical | 1 token |

**Estimated total checkbox tokens:** ~20-25
**Radio button tokens:** Similar structure (~20-25)

---

## State Coverage Requirements

### Button States (Each Variant)

| State | CSS Selector | Visual Changes | Token Properties Needed |
|-------|--------------|----------------|-------------------------|
| **Default** | `button` | Base appearance | background, border, color, shadow (optional) |
| **Hover** | `button:hover` | Subtle highlight | background (lighter/darker), border (optional), shadow (optional) |
| **Active** | `button:active` | Pressed feedback | background (darker), transform (translateY), shadow (inset or removed) |
| **Focus** | `button:focus` or `button:focus-visible` | Accessibility outline | outline-color, outline-width, outline-offset, shadow (focus ring) |
| **Disabled** | `button:disabled` or `.is-disabled` | Muted appearance, no hover | background (gray), border (gray), color (gray), opacity (0.6), cursor (not-allowed) |
| **Loading** (optional) | `.is-loading` | Spinner replaces content | spinner.size, spinner.border-width, spinner.color |

**Critical:** Focus state must meet WCAG 2.1 contrast requirements (3:1 minimum).

### Form Input States

| State | CSS Selector | Visual Changes | Token Properties Needed |
|-------|--------------|----------------|-------------------------|
| **Default** | `input` | Base appearance | border, background, color |
| **Focus** | `input:focus` | Active editing indicator | border (or outline), shadow (focus ring) |
| **Error/Invalid** | `input:invalid`, `input.is-invalid`, `input:user-invalid` | Validation failure | border (red), shadow (red glow), background (light red tint optional) |
| **Valid** | `input:valid`, `input:user-valid` | Validation success | border (green), shadow (green glow optional) |
| **Disabled** | `input:disabled` | Read-only state | background (gray), border (gray), color (gray), cursor (not-allowed) |
| **Placeholder** | `input::placeholder` | Helper text | color (muted gray) |

**Note:** Prefer `:user-invalid` / `:user-valid` over `:invalid` / `:valid` to avoid showing errors before user interaction.

### Checkbox/Radio States

| State | CSS Selector | Visual Changes | Token Properties Needed |
|-------|--------------|----------------|-------------------------|
| **Unchecked** | `input[type="checkbox"]` | Empty box | border, background |
| **Checked** | `input[type="checkbox"]:checked` | Checkmark visible | background (or checkmark color), border |
| **Indeterminate** | `input[type="checkbox"]:indeterminate` | Horizontal line (JS-only state) | background (or line color), border |
| **Hover** | `input[type="checkbox"]:hover` | Interactive feedback | border (darker) |
| **Focus** | `input[type="checkbox"]:focus-visible` | Keyboard navigation indicator | border, shadow (focus ring) |
| **Disabled** | `input[type="checkbox"]:disabled` | Non-interactive | background (gray), border (gray), opacity (0.6), checkmark color (muted) |

**Critical:** Indeterminate state requires JavaScript to set (`checkbox.indeterminate = true`). Visual-only state.

---

## Button Variant Characteristics

Based on research across Material Design, Carbon, Atlassian, Salesforce Lightning:

### Primary Buttons
- **Purpose:** Main call-to-action (submit, save, confirm)
- **Visual:** Solid background (brand color), high contrast text (usually white)
- **Tokens:** background (brand color), color (white/high contrast), border (optional, same as background or none)
- **States:** All 5 states required

### Secondary Buttons
- **Purpose:** Alternative actions (cancel, back, secondary CTA)
- **Visual:** Less prominent than primary (lighter background or outlined)
- **Tokens:** background (lighter tint or transparent), color (brand color or gray), border (visible, medium gray or brand)
- **States:** All 5 states required

### Outlined (Ghost) Buttons
- **Purpose:** Tertiary actions, minimal emphasis
- **Visual:** Transparent background, visible border, text color matches border
- **Tokens:** background (transparent), border (brand or gray), color (brand or gray)
- **Hover:** Add subtle background tint
- **States:** All 5 states required

### Ghost Buttons
- **Purpose:** Least emphasis, blends with UI (modals, cards, toolbars)
- **Visual:** No border, transparent background, text-only
- **Tokens:** background (transparent, tint on hover), border (none), color (brand or gray)
- **States:** All 5 states required

---

## Complexity Assessment

| Feature Category | Complexity | Reason |
|------------------|------------|--------|
| Button variant tokens | **Medium** | 4 variants × 5 states × 3-4 CSS properties = ~60-80 tokens, but pattern is repetitive |
| Button state coverage | **High** | Must coordinate background, border, color, shadow across states; hover + active + focus interactions tricky |
| Form input states | **High** | Validation pseudo-classes (:invalid, :user-invalid) require careful styling; error + focus state combination |
| Checkbox states | **High** | Indeterminate state adds complexity; checkmark styling (::after pseudo-element) requires geometric tokens |
| CSS property naming | **Low** | Straightforward mapping (background → background-color) |
| Token aliasing (semantic → component) | **Low** | Reference syntax: `{color.action.primary}` |
| Size variants | **Low** | Multiplier pattern or separate token sets |
| Focus indicators | **Medium** | Must meet WCAG contrast requirements, test across backgrounds |

---

## MVP Recommendation

**Prioritize:** (for initial v2.0 milestone)

1. **Button primary variant** (5 states: default, hover, active, focus, disabled)
   - CSS properties: background, border, color, shadow (focus only), shared properties (padding, height, radius, font-size)
   - ~15-20 tokens
   - **Rationale:** Highest usage, proves token architecture

2. **Text input states** (5 states: default, focus, error, valid, disabled)
   - CSS properties: border, background, color, outline (focus), shadow (focus, error)
   - ~15-20 tokens
   - **Rationale:** Forms are project focus, validation critical

3. **Checkbox states** (6 states: unchecked, checked, indeterminate, hover, focus, disabled)
   - CSS properties: border, background, checkmark color, sizes
   - ~20-25 tokens
   - **Rationale:** Complex enough to stress-test token system, common in forms

4. **Shared button properties** (padding, height, radius, font-size, border-width, gap, transitions)
   - ~10 tokens
   - **Rationale:** Foundation for all button variants

**Total MVP tokens:** ~60-75 tokens

---

**Defer to Phase 2:**

- **Button secondary, outlined, ghost variants** (~45 tokens) — Prove architecture with primary first
- **Radio buttons** (~20 tokens) — Similar to checkboxes, lower priority
- **Select dropdowns** (~15 tokens) — More complex, needs icon tokens
- **Textarea** (~5 tokens) — Shares input tokens, minor differences
- **Size variants** (small, large) — Adds ~30-40% more tokens, test standard size first
- **Loading/spinner states** (~5 tokens) — Nice-to-have, not critical for v2.0
- **Validation message styling** (color, font-size) — Could use semantic tokens directly

---

**Defer indefinitely (anti-features):**

- Dark mode variants
- Platform-specific outputs (iOS, Android)
- Non-button/form components (accordions, modals, cards)

---

## Existing SCSS Audit Findings

**Current patterns worth tokenizing:**

From `scss/v8-scss/_button.scss`:
- `$button-border-radius: 1.5625rem` → `button.border-radius`
- `$button-min-height: 2.5rem` → `button.height`
- `$button-padding: 0.6875rem 1.375rem` → `button.padding`
- `$button-gap: var(--spacer-050)` → `button.gap`
- `$button-transition-duration: 0.15s` → `button.transition.duration`
- `$button-active-transform: 1px` → `button.active.transform`
- `$button-shadow-primary: 0 0.125rem 0.5rem rgba(...)` → `button.primary.shadow`

From `scss/v8-scss/_checkbox.scss`:
- `$checkbox-size: 33px` → `checkbox.size`
- `$checkbox-border-width: 2px` → `checkbox.border-width`
- `$checkbox-border-radius: 0.25rem` → `checkbox.border-radius`
- `$checkmark-width: 9px` → `checkbox.checkmark.width`
- `$checkmark-height: 16px` → `checkbox.checkmark.height`
- Indeterminate state pattern exists

From `scss/inputBox.scss`:
- `$form-input-border-radius: var(--radius-lg)` → `input.border-radius`
- `$form-input-focus-outline: 2px solid var(--ff-primary)` → `input.focus.outline`
- `$input-error-box-shadow: 0 0 0 0.2rem rgba(255, 0, 0, 0.25)` → `input.error.shadow`

**Migration strategy:** Replace SCSS variables with component tokens incrementally, validate visual regression.

---

## Open Questions for Phase-Specific Research

1. **Shadow tokens:** Does v1.0 have shadow tokens (elevation system)? If not, create them first or hardcode shadows in component tokens?
2. **Opacity tokens:** Does v1.0 have opacity tokens (e.g., 0.6 for disabled)? Or bake opacity into color values (rgba)?
3. **Color generation:** Should hover/active states reference new core tokens (e.g., indigo-200 for lighter) or use opacity overlays?
4. **Focus ring pattern:** Outline vs box-shadow for focus indicators? Existing SCSS uses box-shadow for inputs, outline for buttons.
5. **Checkbox checkmark:** Token for checkmark as separate shape, or reference checkbox.checked.color for the checkmark border?
6. **Size variants:** Separate token files (button-small.json, button-large.json) or single file with size namespace (button.small.*, button.large.*)?
7. **Validation states:** Map to existing Bootstrap semantic tokens (color.danger, color.success) or create input-specific (input.error.color)?

---

## Sources

**Design System Research:**
- [Material Design Theming](https://material-web.dev/theming/material-theming/)
- [Material Design Tokens](https://m3.material.io/foundations/design-tokens)
- [Atlassian Design Tokens](https://atlassian.design/components/tokens/)
- [Carbon Design System Color Tokens](https://carbondesignsystem.com/elements/color/tokens/)
- [Salesforce SLDS Design Tokens](https://developer.salesforce.com/docs/platform/lwc/guide/create-components-css-design-tokens.html)

**Button States & Variants:**
- [Button States Explained (DesignRush)](https://www.designrush.com/best-designs/websites/trends/button-states)
- [Button States - Nielsen Norman Group](https://www.nngroup.com/articles/button-states-communicate-interaction/)
- [Designing Button States (LogRocket)](https://blog.logrocket.com/ux-design/designing-button-states/)
- [Carbon Button Component](https://v10.carbondesignsystem.com/components/button/usage/)
- [Ghost Buttons in UX Design](https://uxplanet.org/ghost-buttons-in-ux-design-4cf3717334f8)

**Form Validation States:**
- [Styling Form Input Validity (DigitalOcean)](https://www.digitalocean.com/community/tutorials/css-styling-form-input-validity)
- [Bootstrap Form Validation](https://getbootstrap.com/docs/5.0/forms/validation/)
- [Form Validation Styling (CSS-Tricks)](https://css-tricks.com/snippets/css/form-validation-styling-on-input-focus/)
- [:invalid CSS Pseudo-Class (MDN)](https://developer.mozilla.org/en-US/docs/Web/CSS/:invalid)
- [Styling Valid and Invalid Forms with CSS](https://blog.openreplay.com/styling-valid-invalid-form-css/)

**Checkbox/Radio States:**
- [Definitive Guide to Indeterminate Checkbox State](https://www.sitelint.com/blog/definitive-guide-to-indeterminate-state-of-a-checkbox)
- [:indeterminate CSS Pseudo-Class (MDN)](https://developer.mozilla.org/en-US/docs/Web/CSS/:indeterminate)
- [Bootstrap Checks and Radios](https://getbootstrap.com/docs/5.0/forms/checks-radios/)
- [Material UI Checkbox](https://mui.com/material-ui/react-checkbox/)

**Design Token Architecture:**
- [Design Tokens Explained (Contentful)](https://www.contentful.com/blog/design-token-system/)
- [Design Tokens Overview (GitLab Pajamas)](https://design.gitlab.com/product-foundations/design-tokens/)
- [Component Tokens First (Medium)](https://medium.com/@hereinthehive/component-tokens-first-hear-me-out-6258f54935a9)
- [Design Token-Based UI Architecture (Martin Fowler)](https://martinfowler.com/articles/design-token-based-ui-architecture.html)
- [The Design System Guide - Design Tokens](https://thedesignsystem.guide/design-tokens)

**Best Practices:**
- [Tailwind CSS Best Practices (FrontendTools)](https://www.frontendtools.tech/blog/tailwind-css-best-practices-design-system-patterns)
- [Developer's Guide to Design Tokens and CSS Variables (Penpot)](https://penpot.app/blog/the-developers-guide-to-design-tokens-and-css-variables/)
- [Naming Best Practices (Smashing Magazine)](https://www.smashingmagazine.com/2024/05/naming-best-practices/)
- [Naming Tokens in Design Systems (Nathan Curtis)](https://medium.com/eightshapes-llc/naming-tokens-in-design-systems-9e86c7444676)
