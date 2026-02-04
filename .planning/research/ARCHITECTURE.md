# Design Token Architecture

**Domain:** Design Tokens Extraction from SCSS to W3C DTCG/Token Studio Format
**Researched:** 2026-02-03
**Confidence:** HIGH

## Executive Summary

This document defines the architectural structure for extracting design tokens from forms-flow-theme SCSS variables and organizing them according to W3C Design Tokens Community Group (DTCG) specification version 2025.10 (first stable release) and Token Studio compatibility requirements.

The architecture balances three competing needs:
1. **W3C DTCG compliance** - Following official specification for interoperability
2. **Token Studio import compatibility** - Ensuring smooth import into Figma plugin
3. **Codebase consistency** - Maintaining naming patterns from existing SCSS where appropriate

## Recommended Architecture

### File Organization Strategy

**Recommendation: Multi-file organization with category-based separation**

The extraction should produce **multiple JSON files organized by token category**, stored in a folder structure rather than a single monolithic file. This follows 2026 industry best practices for scalability and maintainability.

```
tokens/
├── $themes.json              # Theme configurations (required by Token Studio)
├── $metadata.json            # Metadata file (Token Studio)
├── core/                     # Primitive/foundation tokens
│   ├── colors.json          # Base color palette
│   ├── spacing.json         # Base spacing scale
│   ├── typography.json      # Font families, base sizes
│   └── borders.json         # Border widths, radii
├── semantic/                 # Contextual tokens
│   ├── colors.json          # Semantic color assignments
│   ├── typography.json      # Text styles
│   └── spacing.json         # Layout spacing
└── component/                # Component-specific tokens
    ├── buttons.json
    ├── modals.json
    ├── tables.json
    └── forms.json
```

**Rationale:**

1. **Token Studio Multi-file Sync**: Token Studio Pro's multi-file sync feature creates one JSON file per token set in a folder structure, and this is **required** when using Token Studio's Themes feature with engineering workflows.

2. **Style Dictionary Compatibility**: Style Dictionary performs deep merge on all token files, making file structure purely organizational. Engineers can reorganize files without affecting output.

3. **Scalability**: Multiple files prevent the navigation difficulties, unintended change risks, and reduced flexibility that plague large single-file systems.

4. **Separation of Concerns**: Splitting tokens by category (colors, typography, spacing) provides easier maintenance and enhanced clarity for teams.

5. **Build Tool Support**: Transform tools like Style Dictionary can generate tailored outputs per file, enabling platform-specific builds (CSS, SCSS, JS) from categorical sources.

### Token Group Hierarchy and Nesting

**Recommendation: Three-tier hierarchy matching DTCG specification**

Design tokens should follow the industry-standard three-tier structure:

#### Tier 1: Core (Primitive) Tokens
- **Purpose**: Foundation layer with all raw values
- **Naming Pattern**: `{category}.{attribute}.{scale}`
- **Values**: Always CSS values (hex codes, pixels, rem)
- **Usage**: Should almost never be used directly outside token package - exist to be referenced
- **Example**:
  ```json
  {
    "colors": {
      "blue": {
        "500": {
          "$type": "color",
          "$value": "#253DF4"
        }
      }
    }
  }
  ```

#### Tier 2: Semantic Tokens
- **Purpose**: Context layer providing meaning to primitives
- **Naming Pattern**: `{context}.{role}.{variant}`
- **Values**: Reference primitive tokens using curly brace syntax
- **Usage**: Preferred for most application usage
- **Example**:
  ```json
  {
    "color": {
      "action": {
        "primary": {
          "$type": "color",
          "$value": "{colors.blue.500}"
        }
      }
    }
  }
  ```

#### Tier 3: Component Tokens
- **Purpose**: Component-specific design decisions
- **Naming Pattern**: `{component}.{element}.{property}.{state}`
- **Values**: Can reference any tier (primitive, semantic, or other component tokens)
- **Usage**: Most specific token level - use first when available
- **Example**:
  ```json
  {
    "button": {
      "primary": {
        "background": {
          "default": {
            "$type": "color",
            "$value": "{color.action.primary}"
          }
        }
      }
    }
  }
  ```

**Nesting Rules per W3C DTCG:**

1. **Groups vs Tokens**: Groups are JSON objects WITHOUT `$value` property. Tokens MUST have `$value`.
2. **Unlimited Depth**: Nesting can be arbitrarily deep, though 3-5 levels is typical.
3. **Type Inheritance**: Child tokens inherit `$type` from nearest parent group with `$type` defined.
4. **Path Uniqueness**: Translation tools use full path as unique identifier within a file.
5. **Root Tokens**: Groups may include special `$root` token to provide base value while allowing variants.

### Token Naming Conventions

**Recommendation: Kebab-case for token names, period (.) delimiters for grouping**

#### Primary Convention: kebab-case

```json
{
  "color": {
    "gray-darkest": {
      "$type": "color",
      "$value": "#303436"
    },
    "gray-medium-dark": {
      "$type": "color",
      "$value": "#AFB4B6"
    }
  }
}
```

**Rationale:**

1. **CSS Variable Compatibility**: Transforms cleanly to `--color-gray-darkest` without case conversion
2. **Readability**: Easier to read than camelCase in JSON files
3. **Existing Codebase Alignment**: Matches current SCSS naming like `$gray-darkest`, `$gray-medium-dark`
4. **Platform Agnostic**: Style Dictionary can transform to any target case (camelCase for JS, snake_case for Android)

#### Grouping with Period Delimiters

Use periods (`.`) to create hierarchical structure, NOT as part of token names:

```json
{
  "spacing": {
    "base": {
      "050": {
        "$type": "dimension",
        "$value": "0.25rem"
      },
      "100": {
        "$type": "dimension",
        "$value": "0.5rem"
      }
    }
  }
}
```

**This creates path**: `spacing.base.050` → SCSS variable `$spacing-base-050`

**Token Studio Note**: Periods become forward slashes in Figma Variables (`spacing/base/050`), creating visual grouping.

#### Reserved Characters to AVOID

Per W3C DTCG specification and Token Studio compatibility:

- **Dollar sign ($)**: Reserved for spec properties (`$value`, `$type`, `$description`)
- **Curly braces ({, })**: Reserved for reference syntax
- **Period (.)**: Reserved for path traversal in references
- **Forward slash (/)**: Avoid in Token Studio; converted from periods on export
- **Brackets, parentheses, emojis, spaces**: Cause transformation problems

#### Case Sensitivity

Token names are **case-sensitive**. `tokenName`, `TokenName`, and `tokenname` are three distinct tokens. Establish and maintain consistent casing strategy.

#### Numeric Scale Naming

For fractional values, use text to avoid collisions:

- **WRONG**: `spacing.1.5` → flattens to `spacing15`
- **RIGHT**: `spacing.1half` → flattens to `spacing1half`

During transformation, engineers flatten names by removing periods/dashes, causing `spacing.1.5` and `spacing.15` to both become `spacing15`.

### Reference/Alias Syntax

**Recommendation: Curly brace syntax for standard references, JSON Pointer for advanced use**

#### Standard Reference Syntax

Use curly braces `{path.to.token}` for token aliases:

```json
{
  "colors": {
    "blue": {
      "500": {
        "$type": "color",
        "$value": "#253DF4"
      }
    }
  },
  "color": {
    "action": {
      "primary": {
        "$type": "color",
        "$value": "{colors.blue.500}"
      }
    }
  }
}
```

**Syntax Rules:**

1. **No spaces**: `{token-name}` NOT `{ token-name }`
2. **Case-sensitive**: Must match exact token path
3. **Dot notation**: Use periods to traverse groups
4. **Auto-resolution**: Automatically resolves to `$value` property
5. **Chained references**: Allowed - tools follow chain to final value
6. **Circular references**: Invalid - tools must detect and report as errors

**Best Practice - Multiple Aliases:**

Create as many aliases as needed. All can reference same primitive:

```json
{
  "color": {
    "brand": {
      "primary": {
        "$value": "{colors.blue.500}"
      }
    },
    "semantic": {
      "action": {
        "$value": "{colors.blue.500}"
      },
      "info": {
        "$value": "{colors.blue.500}"
      }
    }
  }
}
```

This allows managing one color instead of multiple - change `colors.blue.500` and all aliases update automatically.

#### Advanced: JSON Pointer Syntax

For property-level references within composite tokens:

```json
{
  "colors": {
    "brand": {
      "blue": {
        "$type": "color",
        "$value": {
          "r": 37,
          "g": 61,
          "b": 244,
          "a": 1
        }
      }
    }
  },
  "component": {
    "accent": {
      "$type": "color",
      "$ref": "#/colors/brand/blue/$value/r"
    }
  }
}
```

This follows RFC 6901 JSON Pointer notation. **Only use when needed** - curly brace syntax is simpler for complete token references.

#### Math Operations with References

Token Studio supports math operations:

```json
{
  "spacing": {
    "base": {
      "$value": "8px"
    },
    "large": {
      "$value": "{spacing.base} * 2"
    }
  }
}
```

**Token Studio Limitation**: Math is evaluated at export time, not in JSON storage.

### Token Studio-Specific Requirements

#### File Export Options

Token Studio supports two export modes:

1. **Single File**: All token sets in one JSON file
   - Requires `parentKey` in structure (token set name)
   - Causes conflicts when tokens have same names in different sets
   - Only suitable for small systems

2. **Multi-file (Folder)**: Each token set as individual JSON file (RECOMMENDED)
   - Token sets with `/` in names export as folders and files
   - `$themes.json` and `$metadata.json` as separate files
   - **Required for Token Studio Themes feature**
   - **Required for engineering transformation workflows**

#### Format: W3C DTCG vs Legacy

Token Studio supports two formats:

**W3C DTCG Format (RECOMMENDED):**
```json
{
  "color": {
    "primary": {
      "$type": "color",
      "$value": "#253DF4",
      "$description": "Primary brand color"
    }
  }
}
```

**Legacy Format:**
```json
{
  "color": {
    "primary": {
      "type": "color",
      "value": "#253DF4",
      "description": "Primary brand color"
    }
  }
}
```

**Recommendation**: Use W3C DTCG format for:
- Compliance with official specification
- Future-proofing as ecosystem standardizes
- Interoperability with other DTCG-compliant tools

#### Token Set Organization

Each Token Set in Token Studio becomes one JSON file when using multi-file export. Organize token sets to match the three-tier structure:

- **Core Token Sets**: `core/colors`, `core/spacing`, `core/typography`, `core/borders`
- **Semantic Token Sets**: `semantic/colors`, `semantic/typography`, `semantic/spacing`
- **Component Token Sets**: `component/buttons`, `component/modals`, `component/tables`

Token sets with `/` in their names automatically create folder hierarchies on export.

#### Active Token Sets for References

In Token Studio, only tokens from **active token sets** (showing checkmarks) are available to reference. When creating references, ensure source token sets are active.

## Build Order Implications

### Extraction Phase Order

**Phase 1: Core/Primitive Tokens First**

Extract foundation tokens that have no dependencies:

1. **Colors** (`core/colors.json`)
   - Raw color values from `_theme.scss`
   - Example: `$black`, `$white`, `$primary`, `$gray-darkest`
   - Map to: `colors.black`, `colors.white`, `colors.blue.500`, `colors.gray.900`

2. **Spacing Base** (`core/spacing.json`)
   - Base spacing unit and scales
   - Example: `$base: 0.5rem`
   - Map to: `spacing.base`, with derived scale `spacing.050`, `spacing.100`

3. **Typography Base** (`core/typography.json`)
   - Font families and base sizes
   - Example: `$fontBase`, `$fontLineHeight`
   - Map to: `typography.font-family.base`, `typography.size.base`

4. **Borders** (`core/borders.json`)
   - Border widths and radii
   - Example: `$lineThin`, `$borderRadiusModal`
   - Map to: `border.width.thin`, `border.radius.modal`

**Rationale**: Core tokens have concrete CSS values and no dependencies. Must be extracted first so semantic and component tokens can reference them.

**Phase 2: Semantic Tokens Second**

Extract contextual tokens that reference core tokens:

1. **Semantic Colors** (`semantic/colors.json`)
   - Role-based color assignments
   - Example: `$primary-color: var(--ff-primary)`
   - Map to: `color.primary { "$value": "{colors.blue.500}" }`

2. **Semantic Spacing** (`semantic/spacing.json`)
   - Layout-specific spacing
   - Example: `$navPadding`, `$modalOutterPadding`
   - Map to: `spacing.nav.padding`, `spacing.modal.outer`

3. **Semantic Typography** (`semantic/typography.json`)
   - Text role assignments
   - Example: `$fontSectionHead`, `$fontModalTitle`
   - Map to: `typography.heading.section`, `typography.heading.modal`

**Rationale**: Semantic tokens provide meaning but depend on core tokens existing. Extract after core tokens are defined.

**Phase 3: Component Tokens Last**

Extract component-specific tokens that may reference either tier:

1. **Component Tokens** (`component/*.json`)
   - Button styles, modal configurations, table styles
   - Can reference core OR semantic tokens
   - Most specific level with highest number of dependencies

**Rationale**: Component tokens are the most specific and may reference any lower tier. Extract last to ensure all dependencies exist.

### Token Consumption Order

When consuming design tokens in application code:

1. **Look for Component Token first** - Most specific, if it exists use it
2. **Fall back to Semantic Token** - If no component token, use semantic
3. **Avoid direct Core Token usage** - Core tokens lack meaning outside token system

This ensures proper abstraction and makes theme changes easier.

### Validation Build Order

When validating extracted tokens:

1. **Validate Core tokens** - Check all have concrete CSS values, no references
2. **Validate Semantic tokens** - Check all references point to existing core tokens
3. **Validate Component tokens** - Check all references resolve through chain
4. **Check circular references** - Ensure no token reference loops exist

## Pattern Matching to Existing SCSS

### Current SCSS Naming Patterns

From `forms-flow-theme/scss/_theme.scss`:

```scss
// Literal values
$black: #000000;
$gray-darkest: #303436;
$gray-medium-dark: #AFB4B6;

// Calculations
$fontBase: $base;
$fontSmallest: $fontBase*0.875;
$borderRadiusModal: $base*1.5;

// Derived values
$success: $green-dark;
$colorDivider: $gray-medium;
```

### Mapping Strategy

**Preserve semantic intent while improving structure:**

| SCSS Variable | Token Path | Notes |
|--------------|-----------|-------|
| `$black` | `colors.black` | Core color |
| `$gray-darkest` | `colors.gray.900` | Use numeric scale |
| `$gray-medium-dark` | `colors.gray.600` | Use numeric scale |
| `$primary` | `colors.blue.500` | Core color |
| `$primary-color` | `color.primary` | Semantic reference |
| `$success` | `color.success` | Semantic reference |
| `$fontBase` | `typography.size.base` | Core size |
| `$fontSmallest` | `typography.size.sm` | Semantic size |
| `$base` | `spacing.base` | Core spacing unit |
| `$borderRadiusModal` | `border.radius.modal` | Semantic radius |

**Key Transformations:**

1. **Add numeric scales**: Convert `$gray-darkest` → `colors.gray.900` for flexibility
2. **Separate core/semantic**: `$primary` (core) vs `$primary-color` (semantic)
3. **Add category prefixes**: `colors.`, `spacing.`, `typography.` for clarity
4. **Preserve calculations**: Convert SCSS math to token references with math operations

## File Structure Recommendations

### Minimal Viable Structure

For greenfield extraction, start with:

```
tokens/
├── $themes.json              # Empty themes config initially
├── $metadata.json            # Plugin metadata
├── core-colors.json          # All primitive colors
├── core-spacing.json         # All primitive spacing
├── semantic-colors.json      # Color roles
└── semantic-spacing.json     # Spacing roles
```

**Rationale**: Start simple with core and one semantic layer. Add component tokens as needs emerge.

### Production-Scale Structure

For complete design system:

```
tokens/
├── $themes.json
├── $metadata.json
├── core/
│   ├── colors.json          # Primitive color palette
│   ├── spacing.json         # Base spacing scale
│   ├── typography.json      # Font stacks and base sizes
│   ├── borders.json         # Border widths and radii
│   ├── shadows.json         # Shadow definitions
│   └── sizing.json          # Dimension scale
├── semantic/
│   ├── colors.json          # Contextual colors (action, danger, success)
│   ├── typography.json      # Text roles (heading, body, caption)
│   ├── spacing.json         # Layout spacing (padding, margin, gap)
│   └── effects.json         # Elevation, focus states
└── component/
    ├── button.json
    ├── modal.json
    ├── table.json
    ├── form.json
    ├── card.json
    └── navigation.json
```

**Rationale**:
- Folder separation by tier makes dependencies clear
- Category files within tiers match Style Dictionary transform expectations
- Component files align with React component structure

### Theme Support Structure

When adding theme variants (light/dark, brand variations):

```
tokens/
├── $themes.json             # Theme definitions
├── core/                    # Shared across themes
│   └── colors.json
├── themes/
│   ├── light/
│   │   ├── semantic-colors.json
│   │   └── component-colors.json
│   └── dark/
│       ├── semantic-colors.json
│       └── component-colors.json
└── components/              # Reference theme tokens
    └── button.json
```

**$themes.json Example:**
```json
{
  "light": {
    "selectedTokenSets": {
      "core/colors": "enabled",
      "themes/light/semantic-colors": "enabled",
      "components/button": "enabled"
    }
  },
  "dark": {
    "selectedTokenSets": {
      "core/colors": "enabled",
      "themes/dark/semantic-colors": "enabled",
      "components/button": "enabled"
    }
  }
}
```

## Architecture Anti-Patterns

### Anti-Pattern 1: Single Monolithic File

**What:** Storing all tokens in one large JSON file

**Why Bad:**
- Difficult to navigate with large token counts
- High risk of unintended changes affecting unrelated areas
- Reduced flexibility for generating platform-specific outputs
- Conflicts with Token Studio's multi-file workflow for themes

**Instead:** Use category-based multi-file organization with folder structure

### Anti-Pattern 2: Flat Token Structure

**What:** All tokens at same level without hierarchy

```json
{
  "color-primary": "#253DF4",
  "color-gray-900": "#303436",
  "button-bg-primary": "#253DF4"
}
```

**Why Bad:**
- No semantic meaning or relationships
- Can't leverage references/aliases
- Difficult to maintain consistency
- Doesn't scale with design system growth

**Instead:** Use three-tier hierarchy (core/semantic/component) with references

### Anti-Pattern 3: Using Core Tokens Directly

**What:** Application code referencing primitive tokens

```scss
.button {
  background: $colors-blue-500; // WRONG - using core token
}
```

**Why Bad:**
- Core tokens lack semantic meaning
- Makes theme changes difficult (must update many files)
- Breaks abstraction layers

**Instead:** Always use semantic or component tokens in application code

```scss
.button {
  background: $button-primary-background; // RIGHT - component token
}
```

### Anti-Pattern 4: Inconsistent Naming Conventions

**What:** Mixing camelCase, kebab-case, snake_case within same token system

**Why Bad:**
- Creates cognitive overhead for developers
- Can cause naming collisions when transformed
- Harder to write transformation rules

**Instead:** Choose one convention (kebab-case recommended) and enforce consistently

### Anti-Pattern 5: Numeric Scales Without Text

**What:** Using `spacing.1.5` for fractional values

**Why Bad:**
- Flattening transforms `spacing.1.5` and `spacing.15` both become `spacing15`
- Creates naming collisions in generated code

**Instead:** Use text like `spacing.1half` to prevent collisions

### Anti-Pattern 6: Calculation in Core Tokens

**What:** Defining core tokens with math operations

```json
{
  "spacing": {
    "large": {
      "$value": "{spacing.base} * 2"  // WRONG in core tier
    }
  }
}
```

**Why Bad:**
- Core tokens should be concrete values that others reference
- Math belongs in semantic/component tiers that derive from core

**Instead:** Keep core tokens concrete, use math in higher tiers

```json
{
  "core": {
    "spacing": {
      "base": { "$value": "8px" },
      "16": { "$value": "16px" }
    }
  },
  "semantic": {
    "spacing": {
      "large": { "$value": "{core.spacing.base} * 2" }  // OK in semantic
    }
  }
}
```

## Scalability Considerations

| Concern | Initial Extraction | Medium Scale (50-100 tokens) | Large Scale (500+ tokens) |
|---------|-------------------|------------------------------|---------------------------|
| **File Organization** | Single folder, 4-6 files | Category folders (core/semantic/component) | Multi-level folders with theme support |
| **Token Count** | ~30-50 tokens | ~100-200 tokens | 500+ tokens |
| **Reference Depth** | 2 levels (core → semantic) | 3 levels (core → semantic → component) | 3 levels + theme layer |
| **Build Time** | < 1 second | 1-3 seconds | 5-10 seconds with optimization |
| **Team Size** | 1-2 developers | 3-5 developers | 5+ developers, dedicated designer |
| **Maintenance** | Manual JSON edits | Manual with validation scripts | Token Studio + Git sync + CI/CD validation |
| **Documentation** | Inline `$description` fields | + External docs | + Auto-generated docs from tokens |

## Technology Integration Points

### Style Dictionary Integration

Style Dictionary consumes token JSON files and transforms them for different platforms:

```javascript
// style-dictionary.config.js
module.exports = {
  source: ['tokens/**/*.json'],  // Multi-file input
  platforms: {
    scss: {
      transformGroup: 'scss',
      buildPath: 'build/scss/',
      files: [{
        destination: '_variables.scss',
        format: 'scss/variables'
      }]
    },
    css: {
      transformGroup: 'css',
      buildPath: 'build/css/',
      files: [{
        destination: 'variables.css',
        format: 'css/variables'
      }]
    }
  }
};
```

**Key Integration Points:**

1. **Deep Merge**: Style Dictionary merges all source files, so file structure is purely organizational
2. **Transform Groups**: `scss`, `css`, `js` transform groups handle naming conventions automatically
3. **Custom Transforms**: Can add custom transforms for specific token types (e.g., converting `$base * 2` math)

### Token Studio Integration

Token Studio syncs tokens to/from Git providers:

1. **Export from Figma**: Multi-file folder export creates one JSON per token set
2. **Git Sync**: Pro feature syncs to GitHub, GitLab, Azure DevOps
3. **Import to Figma**: Folder import creates token sets from file structure

**Integration Flow:**

```
Figma (Token Studio)
  ↓ Multi-file Export
JSON Files (Git Repository)
  ↓ Style Dictionary Transform
SCSS/CSS Variables (Build Output)
  ↓ Import
React/Angular Components
```

## Sources and Confidence

### HIGH Confidence Sources

- [W3C Design Tokens Format Module 2025.10](https://www.designtokens.org/tr/drafts/format/) - Official specification
- [Design Tokens Specification Stable Release](https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/) - W3C announcement
- [Token Studio Token Format Documentation](https://docs.tokens.studio/manage-settings/token-format) - Official plugin docs
- [Token Studio Multi-file Sync](https://docs.tokens.studio/token-storage/remote-multi-file-sync) - Official feature docs
- [Token Studio Token Name Technical Specs](https://docs.tokens.studio/manage-tokens/token-names/technical-specs) - Official naming rules

### MEDIUM Confidence Sources

- [Design Tokens with Confidence (UX Collective)](https://uxdesign.cc/design-tokens-with-confidence-862119eb819b) - Jan 2026 article on DTCG standard
- [Style Dictionary Documentation](https://styledictionary.com/info/tokens/) - Transform tool documentation
- [How to Manage Design Tokens with Style Dictionary](https://didoo.medium.com/how-to-manage-your-design-tokens-with-style-dictionary-98c795b938aa) - Comprehensive guide
- [Token Values with References](https://docs.tokens.studio/manage-tokens/token-values/references) - Token Studio reference syntax

## Quality Gate Validation

- [x] **File structure clearly defined** - Multi-file folder structure with core/semantic/component separation
- [x] **Naming conventions explicit** - Kebab-case with period delimiters, character restrictions documented
- [x] **Build order implications noted** - Three-phase extraction (core → semantic → component) with validation order
- [x] **W3C DTCG compliance verified** - All recommendations align with specification 2025.10
- [x] **Token Studio compatibility confirmed** - Multi-file export, format requirements, and integration flow documented
- [x] **Existing codebase patterns analyzed** - SCSS variable mapping strategy defined
- [x] **Scalability considerations addressed** - Growth path from initial extraction to production scale
- [x] **Anti-patterns documented** - Common mistakes and prevention strategies identified

## Next Steps for Roadmap Creation

This architecture document informs roadmap phase structure as follows:

**Phase 1: Foundation Setup**
- Set up multi-file folder structure
- Extract core tokens (colors, spacing, typography, borders)
- Validate W3C DTCG compliance
- **Dependency**: Must complete before semantic tokens

**Phase 2: Semantic Layer**
- Extract semantic tokens with references to core
- Implement reference validation
- Test Token Studio import
- **Dependency**: Requires Phase 1 core tokens

**Phase 3: Component Tokens**
- Extract component-specific tokens
- Create complete reference chains
- **Dependency**: Requires Phase 1 + 2

**Phase 4: Build Pipeline**
- Integrate Style Dictionary
- Create SCSS/CSS output transforms
- Set up validation CI/CD
- **Dependency**: Can run parallel to Phase 2-3, requires Phase 1

**Phases Likely Needing Deeper Research:**
- **Theme Support**: If multi-theme required (light/dark), needs research into Token Studio's theme system
- **Math Operations**: If complex calculations needed, research Token Studio vs Style Dictionary math evaluation
- **Custom Transforms**: If special token types emerge (gradients, animations), research custom Style Dictionary transforms

**Phases Using Standard Patterns:**
- Core token extraction (well-documented pattern)
- Multi-file organization (industry standard)
- Reference/alias creation (DTCG specification)
