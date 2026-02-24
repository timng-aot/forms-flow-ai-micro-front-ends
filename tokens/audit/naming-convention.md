# Component Token Naming Convention

This document defines the naming convention for all component tokens introduced in Phase 6 (buttons) and Phase 7 (forms). It is the authoritative reference — implementers must follow this spec without consulting CONTEXT.md.

---

## 1. Segment Order

Locked decision: **`component.variant.state.property`**

| Segment | Description | Examples |
|---------|-------------|---------|
| `component` | The UI component type | `button`, `input`, `checkbox` |
| `variant` | The visual or semantic variant | `primary`, `secondary`, `outline`, `danger` (buttons); `text`, `checkbox` (forms) |
| `state` | The interactive state (omitted for default) | `hover`, `active`, `focus`, `disabled` |
| `property` | The CSS property being described | `background`, `border-color`, `color`, `shadow` |

### Valid Segment Values by Component

**Button variants:** `primary`, `secondary`, `outline`, `danger`
**Button states:** *(default — omitted)*, `hover`, `active`, `focus`, `disabled`
**Button properties:** `background`, `border-color`, `color`, `shadow`

**Form elements:** `input`, `checkbox`
**Form variants (input):** `text`
**Form states:** *(default — omitted)*, `hover`, `focus`, `disabled`, `error`
**Form properties:** `background`, `border-color`, `color`

### Complete Enumeration — Button Tokens

The table below shows all addressable state/property combinations for each button variant. Properties that are shared across states (static) use a shortened path — see Section 4.

| Variant | State | Property | Token Path |
|---------|-------|----------|-----------|
| primary | default | background | `button.primary.background` |
| primary | default | border-color | `button.primary.border-color` |
| primary | default | color | `button.primary.color` |
| primary | hover | background | `button.primary.hover.background` |
| primary | hover | border-color | `button.primary.hover.border-color` |
| primary | hover | shadow | `button.primary.hover.shadow` |
| primary | active | background | `button.primary.active.background` |
| primary | active | border-color | `button.primary.active.border-color` |
| primary | focus | background | `button.primary.focus.background` |
| primary | focus | border-color | `button.primary.focus.border-color` |
| primary | focus | shadow | `button.primary.focus.shadow` |
| primary | disabled | background | `button.primary.disabled.background` |
| primary | disabled | border-color | `button.primary.disabled.border-color` |
| primary | disabled | color | `button.primary.disabled.color` |
| secondary | default | background | `button.secondary.background` |
| secondary | default | border-color | `button.secondary.border-color` |
| secondary | default | color | `button.secondary.color` |
| secondary | hover | background | `button.secondary.hover.background` |
| secondary | hover | border-color | `button.secondary.hover.border-color` |
| secondary | hover | shadow | `button.secondary.hover.shadow` |
| secondary | active | background | `button.secondary.active.background` |
| secondary | disabled | background | `button.secondary.disabled.background` |
| secondary | disabled | color | `button.secondary.disabled.color` |
| outline | default | background | `button.outline.background` |
| outline | default | border-color | `button.outline.border-color` |
| outline | default | color | `button.outline.color` |
| outline | hover | background | `button.outline.hover.background` |
| outline | hover | border-color | `button.outline.hover.border-color` |
| outline | focus | shadow | `button.outline.focus.shadow` |
| outline | disabled | background | `button.outline.disabled.background` |
| outline | disabled | border-color | `button.outline.disabled.border-color` |
| outline | disabled | color | `button.outline.disabled.color` |
| danger | default | background | `button.danger.background` |
| danger | default | border-color | `button.danger.border-color` |
| danger | default | color | `button.danger.color` |
| danger | hover | background | `button.danger.hover.background` |
| danger | hover | shadow | `button.danger.hover.shadow` |
| danger | disabled | background | `button.danger.disabled.background` |
| danger | disabled | color | `button.danger.disabled.color` |

> Static properties (`border-radius`, `font-size`, `font-weight`) use shorter paths — see Section 4.

---

## 2. Default State Omission Rule

**Rule:** The default (resting) state MUST omit the state segment. All non-default states include the state segment explicitly.

| Token Path | Meaning |
|-----------|---------|
| `button.primary.background` | Default state background (no state segment) |
| `button.primary.hover.background` | Hover state background |
| `button.primary.active.background` | Active/pressed state background |
| `button.primary.focus.background` | Focus state background |
| `button.primary.disabled.background` | Disabled state background |

Additional examples:

```
button.primary.background          -- default state (no state segment)
button.primary.hover.background    -- hover state
button.primary.active.background   -- active state
button.primary.focus.background    -- focus state
button.primary.disabled.background -- disabled state
```

```
button.secondary.border-color          -- default state
button.secondary.hover.border-color    -- hover state
button.secondary.disabled.border-color -- disabled state
```

**Rationale:** Default is the most commonly referenced state. Omitting it reduces token count and keeps the most-used references short. Explicit state names are unambiguous — `hover.background` is clearer than `default.background`.

---

## 3. CSS Custom Property Mapping

**Rule:** The JSON dot-path maps directly to the CSS custom property name via the `name/css/ff-prefix` transform. No abbreviations. Dots become hyphens.

### Transform Chain

```
JSON path:   ["button", "primary", "hover", "background"]
Transform:   prepend "ff" -> ["ff", "button", "primary", "hover", "background"]
Join:        "ff-button-primary-hover-background"
CSS output:  --ff-button-primary-hover-background
```

The `name/css/ff-prefix` transform in `forms-flow-theme/config/style-dictionary.config.js` handles this automatically:
- If path starts with `ff`, keep as-is
- Otherwise, prepend `ff` to the path
- Join all segments with hyphens
- The `css/variables` format prepends `--`

### Full Mapping Examples

| JSON token path | CSS custom property |
|----------------|---------------------|
| `button.primary.background` | `--ff-button-primary-background` |
| `button.primary.hover.background` | `--ff-button-primary-hover-background` |
| `button.primary.active.background` | `--ff-button-primary-active-background` |
| `button.primary.focus.shadow` | `--ff-button-primary-focus-shadow` |
| `button.primary.disabled.color` | `--ff-button-primary-disabled-color` |
| `button.primary.border-radius` | `--ff-button-primary-border-radius` |
| `button.font-size` | `--ff-button-font-size` |
| `button.secondary.background` | `--ff-button-secondary-background` |
| `button.danger.hover.shadow` | `--ff-button-danger-hover-shadow` |
| `input.text.background` | `--ff-input-text-background` |
| `input.text.focus.border-color` | `--ff-input-text-focus-border-color` |

**No abbreviations in CSS variable names.** `background` is never `bg`, `border-color` is never `bc` or `border`.

---

## 4. Shared/Static Property Naming

Some properties do not change across states or variants. These properties use a shortened path that omits the constant segment(s).

### Per-Variant Static Properties

Properties that are the same regardless of state for a given variant omit the state segment:

```
button.primary.border-radius   -- same in default, hover, active, focus, disabled
button.secondary.border-radius -- same across all states of secondary
button.outline.border-radius   -- same across all states of outline
```

### Per-Component Static Properties

Properties that are the same across ALL variants AND states omit both state and variant segments:

```
button.font-size    -- same for primary, secondary, outline, danger in all states
button.font-weight  -- same across all variants and states
```

### Decision Rule

Ask: "Does this property value change between states (or between variants)?"
- Changes between states? Include the state segment.
- Same across all states for one variant? Omit the state segment. Keep the variant segment.
- Same across all variants AND all states? Omit both state and variant segments.

### Examples

| Token | Why |
|-------|-----|
| `button.primary.border-radius` | Static per-variant: pill shape for primary, may differ for outline |
| `button.font-size` | Static per-component: all button variants use the same font size |
| `button.font-weight` | Static per-component: all button variants use the same font weight |
| `button.primary.background` | Stateful: changes in hover, disabled, etc. |
| `button.primary.hover.shadow` | State-specific: only present on hover, not in default |

---

## 5. Token Type Handling

**Rule:** Declare `$type` on each **leaf token** (token with `$value`). Do NOT declare `$type` at a group/variant level when the group contains mixed types.

### Valid DTCG Types for Component Tokens

| CSS property | DTCG `$type` |
|-------------|------------|
| background, color, border-color | `"color"` |
| box-shadow, shadow | `"shadow"` |
| border-radius, font-size | `"dimension"` |
| font-weight | `"fontWeight"` |

### Correct Pattern

```json
{
  "button": {
    "primary": {
      "background": { "$type": "color", "$value": "..." },
      "border-color": { "$type": "color", "$value": "..." },
      "color": { "$type": "color", "$value": "..." },
      "border-radius": { "$type": "dimension", "$value": "..." },
      "hover": {
        "background": { "$type": "color", "$value": "..." },
        "shadow": { "$type": "shadow", "$value": "..." }
      }
    }
  }
}
```

### Anti-Pattern: Group-Level Type Declaration

```json
{
  "button": {
    "primary": {
      "$type": "color",  // WRONG: group has shadow and dimension tokens too
      "background": { "$value": "..." },
      "border-radius": { "$value": "..." },  // Would wrongly inherit $type: "color"
      "hover": {
        "shadow": { "$value": "..." }        // Would wrongly inherit $type: "color"
      }
    }
  }
}
```

This fails because `border-radius` and `shadow` tokens would inherit `$type: "color"`, causing the Style Dictionary DTCG validator to process them incorrectly.

**Exception:** Single-type groups (like `ff.color` in core.json which only contains color tokens) may declare `$type` at group level. Component token groups contain mixed types — always use per-leaf `$type`.

---

## 6. Anti-Patterns

The following naming patterns are NOT allowed. Each example includes the correct alternative.

| Anti-Pattern | Why Forbidden | Correct Pattern |
|-------------|--------------|----------------|
| `button.primary.default.background` | Default state must omit the state segment | `button.primary.background` |
| `button.primary.hover.border-radius` | Static properties must not include state segments | `button.primary.border-radius` |
| `btn.pri.bg` | No abbreviations anywhere in token paths | `button.primary.background` |
| `button-primary-background` | Use dots in JSON paths; hyphens only appear in the generated CSS output | `button.primary.background` (JSON), `--ff-button-primary-background` (CSS) |
| `color.button.primary-border` in semantic.json | Component-scoped tokens in semantic.json defeat the purpose of shared semantic tokens; components reference semantic tokens, not the reverse | Define in `components.json` as `button.primary.border-color` |
| `button.primary.active.border-radius` | Static property (border-radius does not change on active) must omit state | `button.primary.border-radius` |
| `BUTTON.PRIMARY.BACKGROUND` | All segments must be lowercase | `button.primary.background` |
| `button.primary.focussed.background` | Use canonical state names only: `focus`, not `focussed` | `button.primary.focus.background` |
| `button.primary.background.color` | Property is the last segment; do not add sub-segments | `button.primary.background` |

---

## Summary

| Rule | Decision |
|------|----------|
| Segment order | `component.variant.state.property` |
| Default state | Omit — `button.primary.background` not `button.primary.default.background` |
| CSS output | `--ff-{component}-{variant}-{state}-{property}` (transform handles this) |
| Abbreviations | None — full names only |
| JSON notation | Dots (`.`); hyphens only in generated CSS |
| Mixed-type groups | Declare `$type` on each leaf token, not on the group |
| Static properties | Omit state segment (and variant segment if shared across all variants) |
