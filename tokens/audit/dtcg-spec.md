# W3C DTCG Token Structure Specification

This document defines the complete token structure specification for the Forms Flow AI design token system. This is the format contract that Phase 2 extraction MUST follow.

## 1. File Structure

The token system consists of exactly two files at the project root:

```
tokens/
  core.json     -- Primitive tokens (raw design values)
  semantic.json -- Purpose-based tokens (references to core tokens)
```

**CRITICAL RULES:**
- There are exactly **two token files**
- Do NOT create subdirectories like `tokens/core/` or `tokens/semantic/`
- Do NOT create per-category files like `colors.json` or `spacing.json`
- Both files live at the root of the `tokens/` directory
- File naming is exact: `core.json` and `semantic.json` (lowercase, no prefixes)

### File Responsibilities

**core.json**: Contains primitive design values extracted directly from the theme audit. These are raw values with no semantic meaning attached. Example: `#253DF4`, `0.25rem`, `300ms`.

**semantic.json**: Contains purpose-based tokens that reference core tokens using curly brace syntax. These tokens have semantic meaning in the design system. Example: `color.action.primary` references `{ff.color.primary-500}`.

## 2. W3C DTCG Format Rules

All tokens must conform to the W3C Design Tokens Community Group (DTCG) specification.

### Token Properties

Every token MUST have:
- `$value`: The token's value (required)
- `$type`: The token's type (required, can be inherited from group)

Every token SHOULD have:
- `$description`: Human-readable description of the token's purpose

### Reserved Characters

Token names MUST NOT contain these reserved characters:
- `$` (dollar sign) - reserved for DTCG properties
- `{` (opening brace) - reserved for reference syntax
- `}` (closing brace) - reserved for reference syntax
- `.` (period) - reserved for group path separator

### Reference Syntax

Tokens can reference other tokens using curly brace notation with dot-separated paths:

```json
{
  "color": {
    "action": {
      "primary": {
        "$value": "{ff.color.primary-500}",
        "$type": "color"
      }
    }
  }
}
```

The reference path follows the JSON nesting structure: `{topGroup.subGroup.tokenName}`

### Valid Type Values

The following `$type` values are valid for our design token categories:

| Category | DTCG Type | Notes |
|----------|-----------|-------|
| Color | `color` | Hex, RGB, RGBA, named colors |
| Spacing | `dimension` | Values with units (rem, px, em) |
| Sizing | `dimension` | Width, height, max-width, etc. |
| Font family | `fontFamily` | Font stack as string or array |
| Font weight | `fontWeight` | Number (100-900) |
| Font size | `dimension` | Values with units |
| Line height | `number` or `dimension` | Unitless or with units |
| Border radius | `dimension` | Values with units |
| Shadow | `shadow` | Object with color, offsets, blur, spread |
| Duration | `duration` | Time values (ms, s) |

## 3. Naming Conventions

### Prefix

All tokens use the `ff` prefix as the top-level group:

```json
{
  "ff": {
    "color": { ... },
    "spacing": { ... }
  }
}
```

### Group Separator

Groups are created through JSON object nesting. The dot notation appears in reference paths, not in token names.

**Correct:**
```json
{
  "ff": {
    "color": {
      "primary-500": { "$value": "#253DF4", "$type": "color" }
    }
  }
}
```
Reference: `{ff.color.primary-500}`

**Incorrect:**
```json
{
  "ff.color.primary-500": { ... }  // WRONG - dot in key name
}
```

### Bootstrap-Originated Names

Keep Bootstrap semantic names unchanged:
- `primary`, `secondary`, `success`, `danger`, `warning`, `info`, `light`, `dark`

These are familiar to developers and should be preserved in semantic tokens.

### Token Name Format

Use kebab-case for all token names:
- `primary-500` (correct)
- `primary_500` (incorrect)
- `Primary500` (incorrect)

### Naming Convention Table

| Category | Core Token Pattern | Semantic Token Pattern | Examples |
|----------|-------------------|------------------------|----------|
| **Color** | Numeric scale (100-900) for shades | Purpose-based names | `ff.color.primary-500`, `ff.color.gray-100` → `color.action.primary`, `color.background.default` |
| **Spacing** | Numeric scale (025, 050, 100, 200) | T-shirt sizes | `ff.spacing.025`, `ff.spacing.100` → `spacing.xs`, `spacing.sm`, `spacing.md` |
| **Typography (font-size)** | Numeric scale or descriptive | T-shirt sizes | `ff.font-size.12`, `ff.font-size.14` → `font-size.xs`, `font-size.sm` |
| **Typography (font-family)** | Descriptive names | Semantic names | `ff.font-family.figtree`, `ff.font-family.system` → `font-family.body`, `font-family.heading` |
| **Typography (font-weight)** | Numeric values (100-900) | Descriptive names | `ff.font-weight.400`, `ff.font-weight.700` → `font-weight.normal`, `font-weight.bold` |
| **Border Radius** | Descriptive names | Component-based | `ff.radius.sm`, `ff.radius.md` → `radius.button`, `radius.card`, `radius.modal` |
| **Shadow** | Descriptive names | Component-based | `ff.shadow.sm`, `ff.shadow.md` → `shadow.card`, `shadow.dropdown` |
| **Duration** | Numeric milliseconds | Purpose-based | `ff.duration.150`, `ff.duration.300` → `duration.fast`, `duration.normal` |

### Color Shade Naming

Colors use a numeric scale where:
- `100` = lightest shade
- `500` = base/primary color
- `900` = darkest shade

Example progression:
```
primary-100 (lightest)
primary-200
primary-300
primary-400
primary-500 (base)
primary-600
primary-700
primary-800
primary-900 (darkest)
```

### Spacing Scale Naming

Core spacing tokens use zero-padded numeric values representing the multiplier:
- `spacing.025` = 0.25rem (0.25× base)
- `spacing.050` = 0.5rem (0.5× base)
- `spacing.100` = 1rem (1× base)
- `spacing.200` = 2rem (2× base)

Semantic spacing uses t-shirt sizes:
- `spacing.xs` → `{ff.spacing.025}`
- `spacing.sm` → `{ff.spacing.050}`
- `spacing.md` → `{ff.spacing.100}`
- `spacing.lg` → `{ff.spacing.150}`
- `spacing.xl` → `{ff.spacing.200}`

## 4. Type Inheritance

The `$type` property can be set at the group level and inherited by all tokens within that group:

```json
{
  "ff": {
    "color": {
      "$type": "color",
      "primary-500": {
        "$value": "#253DF4"
      },
      "primary-600": {
        "$value": "#1E31C3"
      }
    }
  }
}
```

This avoids repetition when all tokens in a group share the same type.

**Inheritance Rules:**
- Child tokens inherit the nearest parent `$type`
- Explicit `$type` on a token overrides inherited type
- Groups can override parent group `$type`

## 5. Shadow Token Format

The DTCG `shadow` type requires an object structure with these properties:

```json
{
  "ff": {
    "shadow": {
      "sm": {
        "$value": {
          "color": "#30343614",
          "offsetX": "0px",
          "offsetY": "2px",
          "blur": "2px",
          "spread": "0px"
        },
        "$type": "shadow"
      }
    }
  }
}
```

**Required Properties:**
- `color`: Color value (hex, RGB, RGBA)
- `offsetX`: Horizontal offset with unit
- `offsetY`: Vertical offset with unit
- `blur`: Blur radius with unit
- `spread`: Spread radius with unit

**Converting from CSS:**
CSS: `0px 2px 2px 0px rgba(48, 52, 54, 0.04)`

Becomes:
```json
{
  "color": "#30343614",  // or "rgba(48, 52, 54, 0.04)"
  "offsetX": "0px",
  "offsetY": "2px",
  "blur": "2px",
  "spread": "0px"
}
```

## 6. v8 vs Legacy Theme Handling

The theme audit identified two coexisting design systems:
1. **Legacy theme** (scss/_theme.scss)
2. **v8 theme** (scss/v8-scss/_theme.scss)

**Resolution Rules:**

When a design token exists in both systems:
- **v8 values take precedence** in core.json
- Document the legacy value in `$description` if significantly different
- The v8 design system represents the current/intended design direction

Example:
```json
{
  "spacing": {
    "base": {
      "$value": "0.5rem",
      "$type": "dimension",
      "$description": "Base spacing unit (v8). Legacy used 1rem."
    }
  }
}
```

**Dual Definitions:**
The audit found dual `$base` definitions:
- `_theme.scss`: `$base: 0.5rem`
- `_variables.scss`: `$base: 1rem`

Import order makes 1rem active in the current codebase, but v8 shows the intended direction is 0.5rem.

## 7. Validation Requirements

All token files must pass these validation checks:

### 1. Valid JSON
Files must parse as valid JSON with no syntax errors.

### 2. Required Properties
Every token must have:
- `$value` property (explicit value or reference)
- `$type` property (explicit or inherited from parent group)

### 3. Reference Resolution
All references must:
- Point to tokens that exist in core.json
- Use correct dot-separated path syntax
- Not create circular references

### 4. No Reserved Characters
Token names (object keys) must not contain: `$`, `{`, `}`, `.`

### 5. Type-Specific Format
- **fontWeight**: Must be number (100-900), not string
- **shadow**: Must be object with all required properties
- **dimension**: Must include unit (rem, px, em)
- **color**: Must be valid color format (hex, rgb, rgba, named)

### 6. No Circular References
References must not create loops:
- Token A references Token B
- Token B references Token A ❌ INVALID

### 7. Consistent Naming
- All tokens under `ff` prefix
- kebab-case for all names
- No mixed naming conventions

## Validation Tools

**Manual Checks:**
1. JSON lint: `jq . tokens/core.json`
2. Reference validation: Verify all `{ff.*}` references exist
3. Type checking: Confirm `$type` exists for every token (explicit or inherited)

**Automated Validation (Phase 2+):**
- Schema validation against DTCG spec
- Reference resolver to detect broken links
- Circular dependency detector

---

**Document Version:** 1.0
**Last Updated:** 2026-02-04
**Phase:** 01-audit-foundation (Plan 03)
