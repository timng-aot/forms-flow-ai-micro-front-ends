# Design Token Methodology

This document covers the extraction methodology from SCSS to DTCG format, naming conventions, architecture decisions, pipeline maintenance, and component adoption guidance for developers maintaining the Forms Flow AI design system.

## Target Audience

Developers maintaining the design system, extending the token pipeline, debugging build issues, and adopting tokens in component code.

## Why Design Tokens?

- **Single source of truth:** Design values defined once in JSON, consumed by code and design tools
- **Design-dev synchronization:** Figma and codebase share the same token values via Token Studio
- **Theme switching capability:** Semantic tokens enable light/dark mode and multi-brand themes
- **Consistency enforcement:** Prevents hardcoded values and design drift across components

## Architecture Decisions

### Why W3C DTCG Format?

The W3C Design Tokens Community Group (DTCG) format was chosen as the foundational format for several strategic reasons:

**Industry standard:** The DTCG specification reached stable status in October 2025 and is being adopted across the design systems community as the standard token format.

**Tool compatibility:** Both Token Studio (Figma plugin) and Style Dictionary (build tool) have full DTCG support, enabling a bidirectional pipeline where tokens can be extracted from code OR exported from Figma.

**Future-proof W3C standard:** As a W3C specification, DTCG ensures long-term compatibility and broad ecosystem support. Adopting it now prevents future migration costs.

### Why Two Files (core.json + semantic.json)?

The two-file structure mirrors design thinking and enables flexible theming:

**Mirrors design thinking:** Designers think in two layers - primitives (raw values like #3248F4) and semantic tokens (purpose-based like "primary action color"). The core/semantic split reflects this mental model.

**Enables theme switching:** Semantic tokens can reference different core values for light mode vs dark mode, or different brand themes, without changing component code.

**Matches Figma structure:** Token Studio in Figma uses the same core/semantic pattern, ensuring design and code stay synchronized.

**Transformation example - SCSS source to DTCG token:**

In the v8 SCSS theme (`forms-flow-theme/scss/v8-scss/_theme.scss`), the indigo color is defined in a SCSS map:

```scss
$base-colors: (
  indigo: #3248F4
);
```

The extraction scripts parse this SCSS and generate a DTCG core token in `tokens/core.json`:

```json
{
  "ff": {
    "color": {
      "indigo-100": {
        "$value": "#3248f4",
        "$type": "color",
        "$description": "v8 indigo palette shade 100"
      }
    }
  }
}
```

Then the semantic layer in `tokens/semantic.json` references this core token:

```json
{
  "color": {
    "primary": {
      "$value": "{ff.color.indigo-100}",
      "$type": "color",
      "$description": "Bootstrap semantic: primary"
    }
  }
}
```

This two-layer structure allows changing the primary color by updating a single reference, rather than hunting through component code.

### Why --ff- Prefix?

The `ff` prefix serves as a namespace for all Forms Flow tokens:

**Namespaces tokens:** Prevents naming collisions with Bootstrap variables, third-party libraries, or browser built-ins.

**Identifies source:** Developers can instantly recognize Forms Flow tokens by the `--ff-` prefix in CSS custom properties.

**Follows existing convention:** The codebase already uses `ff-` prefixes in some SCSS variables, so this continues the established pattern.

**Implementation:** The prefix is configured via a custom name transform in Style Dictionary (`forms-flow-theme/config/style-dictionary.config.js`):

```javascript
StyleDictionary.registerTransform({
  name: 'name/css/ff-prefix',
  type: 'name',
  transform: (token) => {
    const path = token.path[0] === 'ff' ? token.path : ['ff', ...token.path];
    return path.join('-');
  }
});
```

Core tokens have the `ff` group in their JSON structure, while semantic tokens get the prefix added by the transform, ensuring all CSS variables use the `--ff-` prefix.

## Token Pipeline

The token pipeline consists of three stages:

### Stage 1: Extraction

Python scripts parse SCSS files and extract design values into DTCG-compliant JSON files.

**Scripts:** Located in `tokens/scripts/` directory
- `extract-scss-tokens.py` - Main extraction script
- `validate-tokens.py` - DTCG format validation

**Process:** The script uses the `pyScss` library to parse SCSS variable definitions, resolves variable references up to 10 levels deep (recursion limit), and outputs tokens in DTCG format with `$value`, `$type`, and `$description` properties.

**Note:** Custom SCSS functions like `blend-with-white-to-hex()` are preserved as-is during extraction because pyScss doesn't support custom functions. These are resolved in Stage 2.

### Stage 2: Pre-computation

Pre-computation scripts resolve SCSS expressions before Style Dictionary runs.

**Script:** `tokens/scripts/precompute-colors.js`

**Purpose:** Resolves `blend-with-white-to-hex($color, $opacity)` expressions to clean hex values. This custom SCSS function blends colors with white backgrounds to achieve exact Figma variants.

**Formula:** Alpha compositing for color blending
```
newRGB = (baseRGB * opacity) + (whiteRGB * (1 - opacity))
```

**Example:** A token with value `"blend-with-white-to-hex(#3248F4, 0.5)"` is pre-computed to `"#99a4fa"` before Style Dictionary processes it.

**Usage:** Run via `npm run precompute:colors` or automatically as part of `npm run build:tokens`.

### Stage 3: CSS Generation

Style Dictionary transforms DTCG JSON files into CSS custom properties.

**Build command:** `npm run build:tokens` in the forms-flow-theme directory

**Configuration:** `forms-flow-theme/config/style-dictionary.config.js`

**Process:**
1. Token Studio transforms expand DTCG-specific features (math expressions, type validation)
2. Custom name transform adds `--ff-` prefix to all tokens
3. CSS variables format outputs to `tokens/dist/core-tokens.css` and `tokens/dist/semantic-tokens.css`
4. Semantic tokens use `outputReferences: true` to generate `var()` references to core tokens
5. Merge script combines core + semantic into `tokens/dist/tokens-figma.json` for Token Studio import

**Output example:**

From `tokens/core.json`:
```json
{
  "ff": {
    "color": {
      "indigo-100": { "$value": "#3248f4", "$type": "color" }
    }
  }
}
```

Generates in `tokens/dist/core-tokens.css`:
```css
:root {
  --ff-color-indigo-100: #3248f4;
}
```

From `tokens/semantic.json`:
```json
{
  "color": {
    "primary": { "$value": "{ff.color.indigo-100}", "$type": "color" }
  }
}
```

Generates in `tokens/dist/semantic-tokens.css`:
```css
:root {
  --ff-color-primary: var(--ff-color-indigo-100);
}
```

## Extraction Examples

### Example 1: Color Palette Extraction

**SCSS source** (`forms-flow-theme/scss/v8-scss/_theme.scss`):

```scss
$base-colors: (
  yellow: #EFC005,
  green:  #00C49A,
  cyan:   #00BCD4,
  blue:   #0087D9,
  orange: #FF9100,
  vivid:  #7C80FE,
  red:    #E57373,
  indigo: #3248F4
);

$opacities: (
  100: 1,
  200: 0.5,
  300: 0.25
);
```

The v8 theme uses a `blend-with-white-to-hex()` function in SCSS to generate color variants. For example, `yellow-200` is defined as `blend-with-white-to-hex($yellow, 0.5)`.

**DTCG token** (after extraction and pre-computation in `tokens/core.json`):

```json
{
  "ff": {
    "color": {
      "$type": "color",
      "yellow-100": {
        "$value": "#efc005",
        "$description": "v8 yellow palette shade 100"
      },
      "yellow-200": {
        "$value": "#f7e082",
        "$description": "v8 yellow palette shade 200"
      },
      "yellow-300": {
        "$value": "#fbefc1",
        "$description": "v8 yellow palette shade 300"
      }
    }
  }
}
```

The blend expressions are pre-computed to clean hex values, making the tokens compatible with both Style Dictionary and Figma Token Studio.

### Example 2: Spacing with Semantic References

**Core numeric scale** (`tokens/core.json`):

```json
{
  "ff": {
    "spacing": {
      "$type": "dimension",
      "025": {
        "$value": "0.25rem",
        "$description": "Spacing scale 025 (v8)"
      },
      "050": {
        "$value": "0.5rem",
        "$description": "Spacing scale 050 (v8)"
      },
      "100": {
        "$value": "1rem",
        "$description": "Spacing scale 100 (v8)"
      }
    }
  }
}
```

**Semantic references** (`tokens/semantic.json`):

```json
{
  "spacing": {
    "$type": "dimension",
    "xs": {
      "$value": "{ff.spacing.025}",
      "$description": "Semantic spacing: xs"
    },
    "sm": {
      "$value": "{ff.spacing.050}",
      "$description": "Semantic spacing: sm"
    },
    "md": {
      "$value": "{ff.spacing.100}",
      "$description": "Semantic spacing: md"
    }
  }
}
```

This enables components to use semantic names like `spacing.md` while the actual value can be updated centrally in the core scale.

### Example 3: Shadow CSS String to DTCG Object Conversion

**SCSS source** (shadow as CSS string):

```scss
$button-shadow-primary: 0px 0.125rem 0.5rem 0px rgba(137, 105, 242, 0.15);
```

**DTCG token** (`tokens/core.json`):

```json
{
  "ff": {
    "shadow": {
      "$type": "shadow",
      "button-shadow-primary": {
        "$value": {
          "color": "rgba(137, 105, 242, 0.15)",
          "offsetX": "0px",
          "offsetY": "0.125rem",
          "blur": "0.5rem",
          "spread": "0px"
        },
        "$description": "Source: scss/v8-scss/_button.scss:28"
      }
    }
  }
}
```

The extraction scripts parse the CSS shadow string and convert it to the DTCG shadow object format with separate properties for color, offsets, blur, and spread. This format is compatible with Token Studio and enables manipulation of individual shadow properties.

## Naming Conventions

### General Rules

- **kebab-case:** All token names use lowercase with hyphens: `indigo-100`, `font-weight-medium`
- **No reserved characters:** Token names cannot contain dots, braces, or dollar signs (reserved by DTCG spec)
- **Dot notation via JSON nesting:** Groups are created through nested JSON objects, not dots in names
- **ff- prefix:** All tokens use the `ff` top-level group in core.json for namespacing

### Bootstrap Semantic Names Preserved

Bootstrap semantic color names are kept unchanged for developer familiarity:
- `primary`, `secondary`, `success`, `danger`, `warning`, `info`, `light`, `dark`

These appear in semantic.json and map to the appropriate core color tokens.

### Per-Category Naming Patterns

#### Color

**Core pattern:** `ff.color.{hue}-{shade}` where shade uses 100-900 numeric scale

**Rules:**
- Hues use descriptive names: `indigo`, `yellow`, `green`, `cyan`, `blue`, `orange`, `red`
- Shades use numeric scale: `100` (lightest), `200`, `300` (darkest for v8 palettes)
- Bootstrap colors use semantic names in semantic.json: `primary`, `success`, `danger`

**Valid examples:**
- `ff.color.indigo-100` (#3248f4)
- `ff.color.yellow-200` (#f7e082)
- `ff.color.white-300` (#ffffff)

**Invalid examples:**
- `ff.color.indigo.100` (dot in name instead of hyphen)
- `ff.color.Indigo-100` (uppercase)
- `ff.color.indigo_100` (underscore instead of hyphen)

#### Spacing

**Core pattern:** `ff.spacing.{zero-padded-numeric}`

**Rules:**
- Values are zero-padded 3-digit numbers: `025`, `050`, `100`, `200`
- Numbers represent the multiplier (100 = 1rem base)
- Semantic tokens use t-shirt sizes: `xs`, `sm`, `md`, `lg`, `xl`

**Valid examples:**
- `ff.spacing.025` (0.25rem)
- `ff.spacing.100` (1rem)
- `spacing.md` → {ff.spacing.100} (semantic)

**Invalid examples:**
- `ff.spacing.25` (not zero-padded)
- `ff.spacing.1rem` (unit in name)
- `ff.spacing.small` (descriptive name in core tokens)

#### Typography

**Font size pattern:** `ff.font-size.{descriptive-name}` or numeric

**Rules:**
- Core tokens use descriptive names from SCSS: `font-smallest`, `font-modal-title`, `drp-font-size`
- Values can include SCSS expressions (e.g., `0.5rem*0.875`) or direct values (`0.9375rem`, `14px`)
- Semantic tokens can use t-shirt sizes if desired

**Font weight pattern:** `ff.font-weight.{descriptive-name}`

**Rules:**
- Values are numbers (100-900), not strings
- Core tokens: `font-weight-xs` (300), `font-weight-sm` (400), `font-weight-regular` (400)
- Semantic tokens: `normal`, `medium`, `semibold`, `bold`

**Font family pattern:** `ff.font-family.{name}`

**Rules:**
- Core tokens: `font-family-base` ("Figtree", sans-serif)
- Semantic tokens: `body`, `heading`

**Valid examples:**
- `ff.font-size.drp-font-size` (0.9375rem)
- `ff.font-weight.font-weight-regular` (400)
- `ff.font-family.font-family-base`

**Invalid examples:**
- `ff.font-weight.regular` ("regular" string instead of number in $value)
- `ff.font-size.14` (raw number without context)

#### Border Radius

**Core pattern:** `ff.radius.{descriptive-name}`

**Rules:**
- Use descriptive names from source: `button-border-radius`, `checkbox-border-radius`
- Semantic tokens use sizes: `sm`, `md`, `lg`, `modal`

**Valid examples:**
- `ff.radius.button-border-radius` (1.5625rem)
- `radius.sm` (1.09375rem)

**Invalid examples:**
- `ff.radius.1` (numeric-only name)
- `ff.radius.large` (use `lg` abbreviation in semantic)

#### Shadow

**Core pattern:** `ff.shadow.{descriptive-name}`

**Rules:**
- Values are DTCG shadow objects with color, offsetX, offsetY, blur, spread properties
- Use descriptive names: `button-shadow-primary`, `drp-shadow-calendar`
- Semantic tokens use sizes: `sm`, `md`, `lg`, `xl`, `2xl`, `3xl`, `nav`

**Valid examples:**
- `ff.shadow.button-shadow-primary` (DTCG object)
- `shadow.sm` (DTCG object)

**Invalid examples:**
- Shadow as CSS string: `"0px 2px 4px rgba(0,0,0,0.1)"` (must be DTCG object)

### Valid vs Invalid Examples Table

| Token | Valid | Invalid | Reason |
|-------|-------|---------|--------|
| Color | `ff.color.indigo-100` | `ff.color.indigo.100` | Dot in name (reserved for path separator) |
| Color | `ff.color.white-300` | `ff.color.White-300` | Uppercase in name |
| Spacing | `ff.spacing.025` | `ff.spacing.25` | Not zero-padded |
| Spacing | `ff.spacing.100` | `ff.spacing.1rem` | Unit in token name |
| Font weight | `400` (as number) | `"regular"` (as string) | Font weights must be numbers |
| Shadow | `{color, offsetX, offsetY...}` | `"0px 2px 4px..."` | Shadow must be DTCG object, not CSS string |
| Token name | `button-border-radius` | `button.borderRadius` | Dot reserved for group paths |
| Token name | `font-weight-medium` | `font_weight_medium` | Use kebab-case not snake_case |

## What's NOT Tokenized

Understanding what should NOT be extracted as tokens prevents scope creep and keeps the token system focused:

**Component-specific z-index values:** Z-index layering is often context-dependent and changes based on component hierarchy. Tokenizing z-index creates rigid stacking contexts that can break when components are composed differently.

**CSS animation keyframes:** Keyframe definitions are declarative animation logic, not design values. They don't benefit from being tokens and would make the token system unnecessarily complex.

**One-off layout measurements:** Layout values used in a single component instance (e.g., a specific modal's width) are not candidates for tokens. Tokens should represent reusable, system-level values.

**Computed values requiring runtime context:** Values that depend on JavaScript calculation, viewport size, or user interaction cannot be static tokens. Example: dynamic container widths, scroll-based transforms.

**SCSS map functions:** Functions like `map-merge()` and `map-get()` are SCSS utilities for manipulating data structures, not design values. They were excluded during extraction.

## Maintenance Tasks

### Adding a New Token

**Step 1:** Determine if the token is a core primitive or semantic reference.

**Step 2:** Open the appropriate file (`tokens/core.json` or `tokens/semantic.json`).

**Step 3:** Add the token in DTCG format with required properties.

**Example - Adding a new core color:**

```json
{
  "ff": {
    "color": {
      "$type": "color",
      "purple-100": {
        "$value": "#9c27b0",
        "$description": "Purple palette shade 100"
      }
    }
  }
}
```

**Example - Adding a semantic token that references core:**

```json
{
  "color": {
    "$type": "color",
    "accent": {
      "$value": "{ff.color.purple-100}",
      "$description": "Accent color for CTAs"
    }
  }
}
```

**Step 4:** Run validation: `python3 tokens/scripts/validate-tokens.py`

**Step 5:** Rebuild CSS: `cd forms-flow-theme && npm run build:tokens`

**Step 6:** Verify generated CSS in `tokens/dist/` contains the new variable.

### Updating an Existing Token

**Step 1:** Locate the token in `tokens/core.json` or `tokens/semantic.json`.

**Step 2:** Update the `$value` property (and `$description` if needed).

**Step 3:** Run validation: `python3 tokens/scripts/validate-tokens.py`

**Step 4:** Rebuild CSS: `cd forms-flow-theme && npm run build:tokens`

**Step 5:** Test components that use the token to ensure visual changes are intended.

**Note:** Changing a core token value affects all semantic tokens and components that reference it. Check the impact before committing.

### Debugging Failed Builds

**JSON syntax errors:**

**Symptom:** Build fails with "Unexpected token" or "JSON parse error"

**Solution:**
1. Validate JSON: `jq . tokens/core.json` or `jq . tokens/semantic.json`
2. Check for missing commas, trailing commas, or unescaped quotes
3. Ensure all objects and arrays are properly closed

**Broken references:**

**Symptom:** Build succeeds but CSS contains `undefined` or reference path as raw string

**Solution:**
1. Verify the reference path matches the JSON structure: `{ff.color.indigo-100}` must exist in core.json
2. Check for typos in reference syntax (missing braces, incorrect dot notation)
3. Run validation script: `python3 tokens/scripts/validate-tokens.py`

**Invalid $type:**

**Symptom:** DTCG validation error: "invalid $type"

**Solution:**
1. Check valid DTCG types: `color`, `dimension`, `fontFamily`, `fontWeight`, `shadow`, `duration`, `number`
2. Ensure `$type` is inherited from parent group or explicitly set on token
3. Font weights must be numbers (400), not strings ("regular")
4. Shadows must be DTCG objects, not CSS strings

**Build hangs or crashes:**

**Symptom:** `npm run build:tokens` never completes

**Solution:**
1. Check for circular references (Token A → Token B → Token A)
2. Validate JSON structure: `jq . tokens/core.json`
3. Clear node_modules cache: `rm -rf forms-flow-theme/node_modules/.cache`
4. Re-run build with verbose logging: `node forms-flow-theme/config/style-dictionary.config.js ../../tokens/core.json core-tokens.css`

### Re-running Extraction Scripts

If SCSS theme files are updated, re-run extraction to capture new values:

**Step 1:** Navigate to project root: `cd /path/to/forms-flow-ai-micro-front-ends`

**Step 2:** Run extraction script:
```bash
python3 tokens/scripts/extract-scss-tokens.py
```

**Step 3:** Run pre-computation for color blending:
```bash
node tokens/scripts/precompute-colors.js
```

**Step 4:** Validate extracted tokens:
```bash
python3 tokens/scripts/validate-tokens.py
```

**Step 5:** Review changes with git diff:
```bash
git diff tokens/core.json tokens/semantic.json
```

**Step 6:** Rebuild CSS if extraction succeeded:
```bash
cd forms-flow-theme && npm run build:tokens
```

## Adopting Tokens in Components

This section provides a quick overview of replacing hardcoded values with token references in component code. For a full list of hardcoded values that need replacement, see `tokens/audit/gap-analysis.json`.

### Before and After Example

**Before - Hardcoded color in component:**

```tsx
const Button = styled.button`
  background-color: #3248f4;
  padding: 0.5rem 1rem;
  border-radius: 1.5625rem;
`;
```

**After - CSS variable reference:**

```tsx
const Button = styled.button`
  background-color: var(--ff-color-primary);
  padding: var(--ff-spacing-050) var(--ff-spacing-100);
  border-radius: var(--ff-radius-button-border-radius);
`;
```

### Finding Hardcoded Values to Replace

The gap analysis JSON file (`tokens/audit/gap-analysis.json`) identifies hardcoded values in components:

```json
{
  "shadows": [
    {
      "value": "0px 2px 8px rgba(66, 66, 66, 0.07)",
      "count": 4,
      "match": "none",
      "recommendation": "Create token: ff.shadow.card-subtle"
    }
  ]
}
```

Look for entries with:
- `"match": "exact"` - Token exists, replace hardcoded value with `var(--ff-*)`
- `"match": "close"` - Token is similar, evaluate if close enough or needs adjustment
- `"match": "none"` - Create new token following naming conventions

### Adoption Strategy

**Priority 1:** Replace hardcoded values that have exact token matches (lowest effort, immediate consistency gain)

**Priority 2:** Create missing tokens for frequently-used values (gap-analysis.json shows `count` field)

**Priority 3:** Migrate component-specific values to tokens when refactoring components

**Guidelines:**
- Import CSS in component: `import 'tokens/dist/core-tokens.css'` and `import 'tokens/dist/semantic-tokens.css'`
- Use semantic tokens when possible (`--ff-color-primary` over `--ff-color-indigo-100`)
- Fallback values for safety: `var(--ff-color-primary, #3248f4)`
- Test visual regression after replacement to catch unintended changes

## References

- [W3C DTCG Specification](https://design-tokens.github.io/community-group/format/) - Official DTCG format spec
- [Token Studio Documentation](https://docs.tokens.studio/) - Figma plugin for token management
- [Style Dictionary Documentation](https://amzn.github.io/style-dictionary/) - Token transformation platform
- [Project DTCG Specification](../../tokens/audit/dtcg-spec.md) - Forms Flow AI token format contract
