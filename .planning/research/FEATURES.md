# Feature Landscape: Design Token Extraction

**Domain:** Design token extraction from SCSS to W3C DTCG format
**Researched:** 2026-02-03
**Confidence:** HIGH

## Executive Summary

Design token extraction for Token Studio/Figma integration requires careful attention to W3C DTCG format compliance, semantic organization, and transformation tooling. The landscape has matured significantly with the W3C DTCG specification reaching its first stable version (v1.0) in October 2025, establishing clear standards for interoperability.

For an SCSS-based React codebase with Bootstrap 5 foundation, the extraction project must prioritize proper JSON format structure, token type compliance, and semantic layering over primitive values. The five target categories (colors, spacing, typography, border radius, shadows) are all officially supported by the W3C DTCG specification and Token Studio.

**Critical finding:** Token Studio requires the `@tokens-studio/sd-transforms` npm package to prepare tokens for Style Dictionary, which then handles platform-specific code generation. This is a hard dependency for the transformation pipeline.

---

## Table Stakes

Features users expect. Missing = product feels incomplete or Token Studio import will fail.

### 1. W3C DTCG Format Compliance
**Why Expected:** Industry standard format; Token Studio requires it for modern workflows
**Complexity:** Medium
**Notes:**
- Required file structure: JSON with `$value`, `$type`, `$description` properties
- File extensions: `.tokens` or `.tokens.json`
- Media type: `application/design-tokens+json`
- Naming restrictions: No `$`, `{`, `}`, or `.` in token/group names
- **Dependencies:** Without this, tokens won't import into Token Studio correctly

**Technical Requirements:**
```json
{
  "tokenName": {
    "$value": "value-here",
    "$type": "color",
    "$description": "Optional description"
  }
}
```

**Sources:**
- [W3C DTCG Format Specification](https://www.designtokens.org/TR/drafts/format/)
- [Token Studio Format Documentation](https://docs.tokens.studio/manage-settings/token-format)

### 2. Core Token Categories (Official W3C Types)
**Why Expected:** Five prioritized categories align with W3C DTCG spec and Token Studio support
**Complexity:** Medium
**Notes:**

| Category | W3C Type | Bootstrap 5 Source | Extraction Complexity |
|----------|----------|-------------------|----------------------|
| **Colors** | `color` | `$gray-darkest`, `$primary`, etc. | Low - direct mapping |
| **Spacing** | `dimension` | CSS variables like `--spacer-050` | Low - unit conversion |
| **Typography** | `typography` (composite) | `$fontBase`, `--font-size-xs`, etc. | Medium - multi-property |
| **Border Radius** | `dimension` | `$borderRadiusHeightSM`, `--radius-md` | Low - direct mapping |
| **Shadows** | `shadow` (composite) | `--shadow-sm`, `--shadow-2xl` | Medium - parse syntax |

**Token Studio Support:**
- Colors: Official type ✓
- Dimension (spacing, border radius): Official type ✓
- Typography: Official composite type ✓
- Shadow: Official composite type ✓

**Note:** Current codebase uses mix of SCSS variables (`$variable`) and CSS custom properties (`--variable`). Extraction must handle both.

**Sources:**
- [Token Studio Token Types](https://docs.tokens.studio/manage-tokens/token-types)
- [Design Token Categories Overview](https://medium.com/bumble-tech/design-tokens-beyond-colors-typography-and-spacing-ad7c98f4f228)

### 3. Required Token Properties
**Why Expected:** W3C spec mandate; Token Studio validation
**Complexity:** Low
**Notes:**

**Required (per W3C spec):**
- `$value` - The actual token value (REQUIRED)
- Token name - Valid JSON key (REQUIRED)

**Strongly Recommended:**
- `$type` - Token category (color, dimension, etc.)
  - If missing, must be inherited from parent group
  - Token Studio treats tokens without `$type` as invalid
- `$description` - Plain text explanation of purpose/usage

**Optional but Valuable:**
- `$extensions` - Vendor-specific metadata (use reverse domain notation)
- `$deprecated` - Boolean or string marking obsolete tokens

**Sources:**
- [W3C DTCG Required Fields](https://www.designtokens.org/TR/drafts/format/)

### 4. Token Aliasing/Referencing
**Why Expected:** Core feature for semantic token architecture; prevents duplication
**Complexity:** Medium
**Notes:**

**Syntax:** `{groupName.tokenName}` within `$value` field

```json
{
  "primitive": {
    "blue": {
      "$value": "#253DF4",
      "$type": "color"
    }
  },
  "semantic": {
    "primary": {
      "$value": "{primitive.blue}",
      "$type": "color",
      "$description": "Primary brand color for buttons, links"
    }
  }
}
```

**Bootstrap 5 Example Mapping:**
```scss
// Current SCSS
$primary: #253DF4;
$primary-light: #E2E1FC;

// Extracted Tokens
{
  "color": {
    "base": {
      "blue-500": { "$value": "#253DF4", "$type": "color" }
    },
    "semantic": {
      "primary": {
        "$value": "{color.base.blue-500}",
        "$type": "color",
        "$description": "Primary brand color"
      }
    }
  }
}
```

**Reference Syntax Rules:**
- Opening character: `{`
- Closing character: `}`
- Separator: `.` (dot notation for nested groups)
- Cannot reference across files unless multi-file support implemented

**Sources:**
- [Design Token Aliasing Patterns](https://medium.com/design-bootcamp/design-tokens-2-0-the-ultimate-guide-32b4a047503)
- [W3C DTCG Reference Syntax](https://www.designtokens.org/TR/drafts/format/)

### 5. Hierarchical Token Organization (Groups)
**Why Expected:** Required for semantic layering; makes tokens maintainable
**Complexity:** Medium
**Notes:**

**Group Structure:**
- Objects without `$value` property = groups (containers)
- Objects with `$value` property = tokens (values)
- Groups can nest infinitely
- `$type` inheritance: Child tokens inherit parent group's `$type` if not explicitly set

**Recommended Hierarchy:**
```
root
├── primitive (raw values)
│   ├── colors
│   ├── spacing
│   └── typography
└── semantic (meaningful references)
    ├── colors (references primitive)
    ├── spacing (references primitive)
    └── typography (references primitive)
```

**Bootstrap 5 Mapping Example:**
```json
{
  "spacing": {
    "$type": "dimension",
    "primitive": {
      "base": { "$value": "0.5rem" },
      "050": { "$value": "0.5rem" },
      "100": { "$value": "1rem" }
    },
    "semantic": {
      "container-padding": { "$value": "{spacing.primitive.050}" },
      "button-padding": { "$value": "{spacing.primitive.100}" }
    }
  }
}
```

**Sources:**
- [Design Token Organization Best Practices](https://www.contentful.com/blog/design-token-system/)
- [Semantic vs Primitive Token Structure](https://goodpractices.design/articles/design-tokens)

### 6. Style Dictionary Integration
**Why Expected:** Industry standard transformation tool; required for platform output
**Complexity:** High
**Notes:**

**Transformation Pipeline:**
```
SCSS Variables → W3C DTCG JSON → Style Dictionary → Platform Outputs
                                      ↑
                          @tokens-studio/sd-transforms
```

**Required Setup:**
1. Install `@tokens-studio/sd-transforms` (Token Studio-specific preprocessor)
2. Install `style-dictionary` v4.0+ (W3C DTCG format support)
3. Configure Style Dictionary config file
4. Define output targets (CSS variables, SCSS, JS, etc.)

**Style Dictionary v4 Features:**
- First-class W3C DTCG format support
- Format conversion tools (legacy → DTCG)
- Reference syntax aligned with spec
- Dual format support (can't mix within single instance)

**Token Studio Specific Requirement:**
Token Studio tokens require `@tokens-studio/sd-transforms` package to convert unofficial token types (e.g., `borderRadius`, `spacing`) to official W3C types before Style Dictionary processes them.

**Sources:**
- [Style Dictionary DTCG Support](https://styledictionary.com/info/dtcg/)
- [Token Studio Style Dictionary Integration](https://docs.tokens.studio/transform-tokens/style-dictionary)
- [Style Dictionary v4 Features](https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/)

---

## Differentiators

Features that set product apart. Not expected, but valued when implementing design tokens.

### 1. Multi-File Token Organization
**Value Proposition:** Improves maintainability; allows team collaboration on different token categories
**Complexity:** Medium
**Notes:**

W3C DTCG spec supports multi-file token systems. Style Dictionary can merge multiple JSON files.

**Structure Example:**
```
tokens/
├── colors.tokens.json
├── spacing.tokens.json
├── typography.tokens.json
├── shadows.tokens.json
└── border-radius.tokens.json
```

**Benefits:**
- Smaller, focused files easier to review/edit
- Parallel development on different categories
- Selective loading/import
- Better git diff/merge behavior

**Cross-File References:**
Tokens can reference tokens in other files if transformation tool supports it (Style Dictionary does).

**Sources:**
- [Design Tokens Specification Multi-File Support](https://zeroheight.com/blog/whats-new-in-the-design-tokens-spec/)

### 2. Component-Level Tokens (Third Layer)
**Value Proposition:** Bridge between semantic tokens and actual UI components
**Complexity:** High
**Notes:**

**Three-Tier Architecture:**
```
Primitive → Semantic → Component
```

**Example:**
```json
{
  "primitive": {
    "blue-500": { "$value": "#253DF4", "$type": "color" }
  },
  "semantic": {
    "action-primary": { "$value": "{primitive.blue-500}", "$type": "color" }
  },
  "component": {
    "button": {
      "primary": {
        "background": { "$value": "{semantic.action-primary}", "$type": "color" },
        "border-radius": { "$value": "{semantic.radius-md}", "$type": "dimension" }
      }
    }
  }
}
```

**When to Use:**
- Large component libraries
- Multiple themes/brands
- Complex design systems with component-specific overrides

**Trade-off:** Adds complexity; only valuable for mature design systems.

**Sources:**
- [Design Token Hierarchy Best Practices](https://medium.com/eightshapes-llc/naming-tokens-in-design-systems-9e86c7444676)

### 3. Token Metadata & Documentation
**Value Proposition:** Self-documenting tokens; improves adoption and correct usage
**Complexity:** Low
**Notes:**

**Metadata Fields:**
- `$description` - Usage guidelines, context, examples
- `$extensions` - Custom metadata (vendor-specific)
  - Use reverse domain notation: `com.yourcompany.customField`

**Example:**
```json
{
  "color": {
    "primary": {
      "$value": "#253DF4",
      "$type": "color",
      "$description": "Primary brand color. Use for CTAs, primary buttons, and active states.",
      "$extensions": {
        "com.formsflow.figmaId": "S:abc123",
        "com.formsflow.wcagContrast": "AA"
      }
    }
  }
}
```

**Value:**
- Tokens become self-documenting
- Designers/developers understand intent without external docs
- Can store tooling-specific metadata (Figma IDs, accessibility ratings)

**Sources:**
- [W3C DTCG Optional Properties](https://www.designtokens.org/TR/drafts/format/)

### 4. Automated SCSS → JSON Extraction
**Value Proposition:** Reduces manual work; keeps tokens in sync with codebase
**Complexity:** High
**Notes:**

Build tooling to parse existing SCSS variables and automatically generate W3C DTCG JSON.

**Extraction Challenges:**
- Parsing SCSS syntax (variables, calculations, color functions)
- Determining appropriate `$type` for each token
- Categorizing into primitive vs semantic
- Handling Bootstrap 5 theme maps (`$theme-colors`)
- Converting units (px → rem)

**Tools to Consider:**
- Custom Node.js script with SCSS parser
- `sass` package for variable extraction
- `postcss` for CSS custom property extraction

**Bootstrap 5 Specific:**
Current codebase mixes:
- SCSS variables: `$primary`, `$gray-darkest`
- CSS custom properties: `--spacer-050`, `--shadow-md`
- Computed values: `$base*1.5`

Extraction script must handle all three patterns.

**Sources:**
- [SCSS to Design Token Conversion](https://smth.uk/use-design-tokens-to-customise-bootstrap/)

### 5. Deprecation Strategy
**Value Proposition:** Safe token evolution; prevents breaking changes
**Complexity:** Medium
**Notes:**

**Using `$deprecated` Property:**
```json
{
  "color": {
    "old-primary": {
      "$value": "#FF0000",
      "$type": "color",
      "$deprecated": "Use color.primary instead. Will be removed in v2.0.0"
    },
    "primary": {
      "$value": "#253DF4",
      "$type": "color"
    }
  }
}
```

**Deprecation Workflow:**
1. Mark old token as `$deprecated` with migration instructions
2. Add replacement token
3. Update codebase to use new token
4. Remove deprecated token in next major version

**Value:**
- Prevents breaking changes
- Provides migration path
- Documents token evolution history

**Sources:**
- [Common Mistakes in Design Tokens Adoption](https://designtokens.substack.com/p/common-mistakes-in-design-tokens)

### 6. Token Versioning
**Value Proposition:** Treat tokens like APIs; enable safe updates
**Complexity:** Medium
**Notes:**

**Versioning Approaches:**
- File-level: `tokens-v1.0.0.json`
- Package-level: npm package with semver
- Property-level: Version metadata in `$extensions`

**Example:**
```json
{
  "$version": "1.0.0",
  "$extensions": {
    "com.formsflow.schemaVersion": "1.0.0"
  },
  "tokens": {
    "color": { ... }
  }
}
```

**Best Practices:**
- Semantic versioning (semver)
- Major version for breaking changes
- Minor version for additions
- Patch version for fixes

**Sources:**
- [Design Tokens as Versioned APIs](https://designtokens.substack.com/p/common-mistakes-in-design-tokens)

---

## Anti-Features

Features to explicitly NOT build. Common mistakes in design token extraction.

### 1. Component-Specific Primitive Tokens
**Why Avoid:** Defeats purpose of tokens; creates tight coupling
**What to Do Instead:** Use semantic layer as abstraction

**Bad Example:**
```json
{
  "button-blue": { "$value": "#253DF4", "$type": "color" },
  "link-blue": { "$value": "#253DF4", "$type": "color" }
}
```

**Good Example:**
```json
{
  "primitive": {
    "blue-500": { "$value": "#253DF4", "$type": "color" }
  },
  "semantic": {
    "action-primary": { "$value": "{primitive.blue-500}", "$type": "color" }
  }
}
```

**Sources:**
- [Design Token Anti-Patterns](https://designtokens.substack.com/p/common-mistakes-in-design-tokens)

### 2. Over-Engineering on First Pass
**Why Avoid:** Creates hundreds of unused tokens; causes decision paralysis
**What to Do Instead:** Start with 5 core categories, iterate based on needs

**Anti-Pattern:**
Creating exhaustive tokens for every possible value in first sprint.

**Better Approach:**
1. Extract only the 5 prioritized categories (colors, spacing, typography, shadows, border radius)
2. Focus on actively used values in codebase
3. Add categories incrementally based on actual requirements
4. Measure token adoption before expanding

**Project-Specific Recommendation:**
Bootstrap 5 codebase has ~60 SCSS variables currently. Start with these, don't generate 200+ tokens speculatively.

**Sources:**
- [Common Mistakes in Design Tokens Adoption](https://designtokens.substack.com/p/common-mistakes-in-design-tokens)
- [Design Tokens Best Practices](https://goodpractices.design/articles/design-tokens)

### 3. Pixel-Based Token Values
**Why Avoid:** Not responsive; breaks accessibility
**What to Do Instead:** Use rem/em units for dimension tokens

**Bad Example:**
```json
{
  "spacing": {
    "sm": { "$value": "8px", "$type": "dimension" }
  }
}
```

**Good Example:**
```json
{
  "spacing": {
    "sm": { "$value": "0.5rem", "$type": "dimension" }
  }
}
```

**Bootstrap 5 Note:**
Current codebase uses `rem` extensively (e.g., `$base: 0.5rem`). Maintain this pattern in extracted tokens.

**Sources:**
- [Design Token Dimension Units](https://www.duetds.com/tokens/)

### 4. Mixing Token Formats
**Why Avoid:** Style Dictionary v4 cannot combine W3C DTCG and legacy formats in single instance
**What to Do Instead:** Choose one format (W3C DTCG) and stick with it

**Anti-Pattern:**
```json
{
  "token1": {
    "value": "#FF0000",
    "type": "color"
  },
  "token2": {
    "$value": "#00FF00",
    "$type": "color"
  }
}
```

**Recommendation:**
Use W3C DTCG format exclusively (`$value`, `$type`, `$description`).

**Sources:**
- [Style Dictionary Format Requirements](https://styledictionary.com/info/dtcg/)

### 5. Direct Primitive Token Usage in Components
**Why Avoid:** Makes theming/rebranding difficult; violates semantic abstraction
**What to Do Instead:** Always reference semantic tokens from component code

**Bad Example (React Component):**
```jsx
<Button style={{ color: tokens.primitive.blue500 }} />
```

**Good Example:**
```jsx
<Button style={{ color: tokens.semantic.actionPrimary }} />
```

**Enforcement Strategy:**
- Hide primitive tokens from team library (Figma)
- Document that primitives are internal-only
- Code review to catch direct primitive references

**Sources:**
- [Semantic vs Primitive Token Usage](https://www.contentful.com/blog/design-token-system/)

### 6. Ignoring Naming Restrictions
**Why Avoid:** Breaks W3C DTCG parsers; causes import failures
**What to Do Instead:** Follow naming rules strictly

**Forbidden Characters in Token Names:**
- `$` (reserved for spec properties)
- `{` and `}` (reserved for references)
- `.` (reserved for group separator)

**Bad Example:**
```json
{
  "$primary-color": { ... },  // ❌ starts with $
  "button.primary": { ... },  // ❌ contains .
  "color-{brand}": { ... }    // ❌ contains { }
}
```

**Good Example:**
```json
{
  "primary-color": { ... },
  "button-primary": { ... },
  "color-brand": { ... }
}
```

**Sources:**
- [W3C DTCG Naming Restrictions](https://www.designtokens.org/TR/drafts/format/)

### 7. Lack of Team Documentation
**Why Avoid:** Tokens fail when only one team uses them; no adoption
**What to Do Instead:** Document usage guidelines, examples, and governance

**Anti-Pattern:**
Creating tokens without:
- Usage guidelines
- Visual examples
- Governance process (who can add/change tokens)
- Onboarding for designers/developers

**Better Approach:**
- `$description` field on every token
- Separate design token documentation
- Team training on token usage
- Clear process for proposing new tokens

**Sources:**
- [Design Token Adoption Pitfalls](https://designtokens.substack.com/p/common-mistakes-in-design-tokens)

---

## Feature Dependencies

Understanding how features build on each other.

```
Foundation Layer (Must Have First):
├── W3C DTCG Format Compliance
├── Core Token Categories (5 types)
├── Required Token Properties ($value, $type)
└── Hierarchical Token Organization (Groups)
    │
    ├── Enables: Token Aliasing/Referencing
    │   │
    │   └── Enables: Semantic Token Layer
    │       │
    │       └── Enables: Component Token Layer (optional)
    │
    └── Requires: Style Dictionary Integration
        │
        ├── Depends on: @tokens-studio/sd-transforms
        └── Enables: Platform Output (CSS, SCSS, JS)

Enhancement Layer (Add After Foundation):
├── Multi-File Organization
├── Token Metadata & Documentation
├── Deprecation Strategy
├── Token Versioning
└── Automated Extraction Tooling
```

**Dependency Notes:**

1. **Must complete first:** W3C DTCG format compliance is prerequisite for everything
2. **Sequential:** Primitive tokens → Semantic tokens → Component tokens (can't skip levels)
3. **Parallel:** After foundation, metadata/versioning/multi-file can be added independently
4. **Critical path:** Foundation layer → Style Dictionary → Platform outputs

---

## MVP Recommendation

For MVP (Minimum Viable Product) design token extraction, prioritize:

### Phase 1: Foundation (2-3 weeks)
1. **W3C DTCG Format Compliance**
   - Set up JSON file structure
   - Implement required properties (`$value`, `$type`)
   - Enforce naming restrictions

2. **Core 5 Token Categories**
   - Colors (primitive layer only)
   - Spacing (primitive layer only)
   - Typography (primitive layer only)
   - Border Radius (primitive layer only)
   - Shadows (primitive layer only)

3. **Style Dictionary Pipeline**
   - Install `@tokens-studio/sd-transforms`
   - Install `style-dictionary` v4.0+
   - Configure basic transformation
   - Output to CSS custom properties

**Success Criteria:**
- Tokens import cleanly into Token Studio
- Style Dictionary generates valid CSS output
- 5 core categories fully extracted from current SCSS

### Phase 2: Semantic Layer (1-2 weeks)
4. **Token Aliasing & Semantic Organization**
   - Create semantic token layer
   - Reference primitive tokens
   - Add `$description` to all semantic tokens

5. **Documentation**
   - Usage guidelines for each category
   - Examples for designers/developers

**Success Criteria:**
- Semantic tokens properly reference primitives
- Team understands semantic vs primitive distinction
- Token Studio shows correct hierarchy

### Defer to Post-MVP:

**Component Token Layer**
- **Reason:** Complex; requires component inventory first
- **When:** After semantic tokens proven stable for 1-2 months

**Multi-File Organization**
- **Reason:** Single file sufficient for 5 categories initially
- **When:** When token count exceeds ~100 or team collaboration becomes bottleneck

**Automated Extraction**
- **Reason:** Manual extraction acceptable for initial 60 variables
- **When:** When tokens need frequent updates from SCSS source

**Token Versioning**
- **Reason:** Not critical until tokens are consumed by multiple teams/projects
- **When:** After tokens published as shared package

---

## Project-Specific Observations

Based on codebase analysis (`forms-flow-theme/scss/_theme.scss` and `_variables.scss`):

### Current State
- **~60 SCSS variables** across colors, spacing, typography, shadows, border radius
- **Mix of SCSS vars and CSS custom properties**
  - SCSS: `$primary`, `$gray-darkest`, `$base`
  - CSS: `--spacer-050`, `--shadow-md`, `--radius-lg`
- **Bootstrap 5 foundation** with custom theme
- **Computed values:** `$borderRadiusHeightSM: $base*1.094`

### Extraction Strategy
1. **Colors:** 14 color values (`$primary`, `$white`, `$gray-*`, etc.)
2. **Spacing:** 13 spacer values (`--spacer-025` through `--spacer-300`)
3. **Typography:** 11 values (font sizes, weights, line heights)
4. **Shadows:** 7 shadow values (`--shadow-sm` through `--shadow-nav`)
5. **Border Radius:** 5 radius values (`--radius-sm` through `--radius-modal`)

**Total Initial Tokens:** ~50 primitive tokens + ~30 semantic references = ~80 tokens for MVP

### Recommended Token Structure
```json
{
  "color": {
    "$type": "color",
    "primitive": {
      "blue-500": { "$value": "#253DF4" },
      "gray-900": { "$value": "#303436" },
      ...
    },
    "semantic": {
      "primary": { "$value": "{color.primitive.blue-500}" },
      "surface-default": { "$value": "{color.primitive.gray-100}" }
    }
  },
  "spacing": {
    "$type": "dimension",
    "primitive": {
      "050": { "$value": "0.5rem" },
      "100": { "$value": "1rem" },
      ...
    },
    "semantic": {
      "container-padding": { "$value": "{spacing.primitive.050}" }
    }
  },
  ...
}
```

---

## Complexity Assessment

| Feature | Complexity | Effort | Risk | Priority |
|---------|-----------|--------|------|----------|
| W3C DTCG Format | Medium | 1 week | Low | P0 |
| Core 5 Categories | Medium | 1 week | Low | P0 |
| Required Properties | Low | 2 days | Low | P0 |
| Token Aliasing | Medium | 3 days | Medium | P0 |
| Hierarchical Organization | Medium | 3 days | Low | P0 |
| Style Dictionary Setup | High | 1 week | High | P0 |
| Multi-File Organization | Medium | 2 days | Low | P1 |
| Component Tokens | High | 2 weeks | High | P2 |
| Token Metadata | Low | 1 day | Low | P1 |
| Automated Extraction | High | 1-2 weeks | High | P2 |
| Deprecation Strategy | Medium | 2 days | Low | P2 |
| Token Versioning | Medium | 3 days | Low | P2 |

**Risk Factors:**
- **Style Dictionary setup:** Highest risk; transformation pipeline can be tricky
- **Component tokens:** High complexity; requires extensive component mapping
- **Automated extraction:** High risk; SCSS parsing can be fragile

---

## Sources

### High Confidence (Official Documentation)
- [W3C DTCG Format Specification](https://www.designtokens.org/TR/drafts/format/)
- [W3C Design Tokens Community Group](https://www.w3.org/community/design-tokens/)
- [Design Tokens Stable Version Announcement (2025)](https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/)
- [Token Studio for Figma Documentation](https://docs.tokens.studio)
- [Token Studio Token Types](https://docs.tokens.studio/manage-tokens/token-types)
- [Token Studio Format Guide](https://docs.tokens.studio/manage-settings/token-format)
- [Style Dictionary DTCG Documentation](https://styledictionary.com/info/dtcg/)
- [Style Dictionary v4 Tokens](https://styledictionary.com/info/tokens/)

### Medium Confidence (Industry Resources)
- [Design Tokens Beyond Colors, Typography, and Spacing](https://medium.com/bumble-tech/design-tokens-beyond-colors-typography-and-spacing-ad7c98f4f228)
- [What Are Design Tokens? - Penpot Complete Guide](https://penpot.app/blog/what-are-design-tokens-a-complete-guide/)
- [Design Tokens Explained - Contentful](https://www.contentful.com/blog/design-token-system/)
- [Design Tokens Good Practices](https://goodpractices.design/articles/design-tokens)
- [Design Tokens 2.0 Ultimate Guide](https://medium.com/design-bootcamp/design-tokens-2-0-the-ultimate-guide-32b4a047503)
- [Naming Tokens in Design Systems](https://medium.com/eightshapes-llc/naming-tokens-in-design-systems-9e86c7444676)
- [Common Mistakes in Design Tokens Adoption](https://designtokens.substack.com/p/common-mistakes-in-design-tokens)
- [Bootstrap Design Token Integration](https://smth.uk/use-design-tokens-to-customise-bootstrap/)
- [Design Tokens with Style Dictionary](https://didoo.medium.com/how-to-manage-your-design-tokens-with-style-dictionary-98c795b938aa)
- [What's New in Design Tokens Spec](https://zeroheight.com/blog/whats-new-in-the-design-tokens-spec/)

---

## Quality Gate Assessment

- [x] **Categories are clear** - Table stakes, differentiators, and anti-features explicitly categorized
- [x] **Complexity noted** - Each feature includes complexity rating (Low/Medium/High) and effort estimate
- [x] **Dependencies identified** - Feature dependency tree and sequential requirements documented
- [x] **Project-specific** - Analyzed actual codebase (Bootstrap 5 SCSS) and sized to ~80 tokens for MVP
- [x] **Sources cited** - All findings reference W3C spec, Token Studio docs, or verified industry sources
- [x] **Confidence levels** - HIGH confidence on technical requirements; MEDIUM on best practices
- [x] **Actionable** - MVP recommendation provides clear phase structure and success criteria

---

## Ready for Requirements Definition

This feature landscape provides:
1. **Table stakes features** - What Token Studio import requires (W3C DTCG compliance, core types, aliasing)
2. **Differentiators** - What improves usability (multi-file, metadata, versioning)
3. **Anti-features** - What to avoid (component-specific primitives, over-engineering, pixel units)
4. **Dependencies** - What must be built in what order (foundation → semantic → component)
5. **MVP scope** - 5 core categories, ~80 tokens, Style Dictionary pipeline

**Next step:** Use this research to define precise requirements for design token extraction tooling and process.
