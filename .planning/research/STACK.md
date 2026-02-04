# Technology Stack: Design Token Extraction

**Project:** Design Token Extraction from SCSS to Figma
**Researched:** 2026-02-03
**Overall Confidence:** HIGH

## Executive Summary

The 2025/2026 standard stack for design token extraction has consolidated around the W3C Design Tokens Community Group (DTCG) specification as the interchange format. The workflow has **inverted from the older SCSS-first approach**: modern best practice is to treat JSON as the source of truth and transform to SCSS, not extract from SCSS.

**Critical Finding:** Extracting design tokens FROM SCSS is an anti-pattern in 2026. The ecosystem has moved to JSON-first workflows. If you have an existing SCSS codebase, you'll need a one-time migration to establish JSON as the source of truth.

## Recommended Stack

### 1. Token Standard & Format

| Technology | Version | Purpose | Confidence |
|------------|---------|---------|------------|
| **W3C DTCG Specification** | 2025.10 (First Stable) | Token interchange format | HIGH |
| **Media Type** | `application/design-tokens+json` | File format standard | HIGH |
| **File Extension** | `.tokens.json` or `.tokens` | Recommended extensions | HIGH |

**Why:** The W3C Design Tokens Community Group specification reached its first stable version (2025.10) in October 2025. This is THE industry standard for 2026, supported by Adobe, Amazon, Google, Microsoft, Meta, Figma, Tokens Studio, and 20+ major organizations.

**Key DTCG Format Requirements:**
- Required fields: `$value` (the token value) and name (parent object key)
- Reserved prefix: All properties starting with `$` are reserved (`$value`, `$type`, `$description`, `$extensions`, `$deprecated`)
- Reference syntax: Curly braces `{group.token}` or JSON Pointer `#/path`
- Token types supported: Color, Dimension, Font family, Font weight, Duration, Cubic bezier, Number, plus composite types (Shadow, Border, Transition, Stroke style, Gradient, Typography)

**Sources:**
- [Design Tokens specification reaches first stable version](https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/)
- [Design Tokens Community Group](https://www.designtokens.org/)
- [Design Tokens Format Module 2025.10](https://www.designtokens.org/tr/drafts/format/)

### 2. Figma Integration

| Technology | Version | Purpose | Confidence |
|------------|---------|---------|------------|
| **Tokens Studio for Figma** | Latest (2.x+) | Figma plugin for token management | HIGH |

**Why:** Tokens Studio is the de facto standard Figma plugin for design tokens. It supports both W3C DTCG and legacy formats, and is specifically mentioned in the W3C DTCG ecosystem.

**Format Requirements:**
- Supports W3C DTCG format with `$value`, `$type`, `$description` properties
- Can export 21 unique Token Types to Figma as Styles or Variables
- Includes Dimension, Number, Spacing, Sizing, Border Radius, Border Width, Opacity, Boolean types
- **Character restrictions in DTCG mode:** Cannot use `{`, `}`, or `$` in token names

**Workflow:**
1. Design tokens maintained in JSON files (W3C DTCG format)
2. Tokens Studio plugin syncs tokens to Figma
3. Tokens exported as Figma Variables or Styles
4. Designers work with tokens in Figma
5. Changes flow back to JSON source of truth

**Sources:**
- [Tokens Studio for Figma Plugin](https://docs.tokens.studio)
- [Token Format - W3C DTCG vs Legacy](https://docs.tokens.studio/manage-settings/token-format)
- [Export to Figma Guide](https://docs.tokens.studio/figma/export)

### 3. Token Transformation Engine

| Technology | Version | Purpose | Confidence |
|------------|---------|---------|------------|
| **Style Dictionary** | 5.2.0+ (v4+ required) | Token transformation to platform outputs | HIGH |
| **@tokens-studio/sd-transforms** | 2.0.1+ | Tokens Studio to Style Dictionary bridge | HIGH |

**Why Style Dictionary:** Industry standard transformation engine from Amazon, with first-class W3C DTCG support as of v4. Generates platform-specific outputs (CSS, SCSS, JS/TS, iOS, Android) from a single source.

**Version 4+ Critical Features:**
- Native W3C DTCG format support (handles `$value`, `$type`, `$description`)
- ES Modules (browser-compatible, modern JavaScript)
- Class-based API (create multiple instances)
- Async/await support throughout
- Removed CTI (Category/Type/Item) hard coupling
- Token type-based transformations aligned with DTCG spec
- Requires Node.js 18+

**Why @tokens-studio/sd-transforms:** Required middleware when using Tokens Studio. Provides custom transforms that:
- Map Tokens Studio token types to DTCG standard types
- Resolve math expressions in token values
- Extract fontStyles when embedded in fontWeights
- Add px units to dimensions appropriately
- Map token descriptions to code comments

**Installation:**
```bash
npm install style-dictionary@latest
npm install @tokens-studio/sd-transforms@latest
```

**Sources:**
- [Style Dictionary](https://styledictionary.com/)
- [Style Dictionary DTCG Support](https://styledictionary.com/info/dtcg/)
- [@tokens-studio/sd-transforms npm](https://www.npmjs.com/package/@tokens-studio/sd-transforms)
- [Style Dictionary GitHub Releases](https://github.com/style-dictionary/style-dictionary/releases)

### 4. SCSS Variable Parsing (One-Time Migration Only)

| Technology | Version | Purpose | Confidence | Status |
|------------|---------|---------|------------|--------|
| **Manual extraction** | N/A | One-time SCSS to JSON migration | MEDIUM | Recommended |
| **scss-to-json** | 2.0.0 | Automated SCSS variable parsing | LOW | Unmaintained (7 years) |
| **@crocsx/scss-to-json** | 3.0.0 | Maintained fork of scss-to-json | LOW | Last update 4 years ago |
| **sass-extract** | Latest | Extract variables from Sass | LOW | Depends on deprecated node-sass |

**Critical Context:** You are extracting from an SCSS-based React codebase. This is a **one-time migration task**, not an ongoing workflow.

**Why Manual Extraction is Recommended:**
1. **Tooling is unmaintained:** All SCSS-to-JSON parsers are 4-7 years old with no active maintenance
2. **LibSass/node-sass deprecated:** sass-extract depends on node-sass, which reached end-of-life in July 2024
3. **Semantic naming required:** Automated extraction produces variable names, but you need semantic token names for a proper design system
4. **Type inference needed:** SCSS variables don't declare types; you must infer whether a value is a color, dimension, spacing, etc.
5. **Relationship mapping:** Design tokens have semantic relationships (e.g., `button-primary-bg` references `color-brand-500`); SCSS variables may not encode these

**Recommended Approach for One-Time Migration:**

1. **Audit existing SCSS variables** (use grep/search)
   ```bash
   # Find all SCSS variable declarations
   grep -r "^\$" --include="*.scss"
   ```

2. **Categorize by token type:**
   - Colors (hex, rgb, hsl values)
   - Spacing (px, rem values for margins, padding)
   - Typography (font-family, font-size, font-weight, line-height)
   - Border radius (px, % values)
   - Shadows (box-shadow values)

3. **Create semantic token structure manually:**
   ```json
   {
     "color": {
       "brand": {
         "500": {
           "$type": "color",
           "$value": "#0066cc"
         }
       }
     },
     "spacing": {
       "md": {
         "$type": "dimension",
         "$value": "16px"
       }
     }
   }
   ```

4. **Validate with Style Dictionary transformation:**
   ```bash
   npx style-dictionary build
   ```

**If You Choose Automated Extraction:**

Use **scss-to-json** for a quick initial pass, then manually review and restructure:

```bash
npm install scss-to-json
```

```javascript
const scssToJson = require('scss-to-json');
const scssVars = scssToJson('path/to/variables.scss');
// Output: { variable: value } object
// You'll need to transform this to DTCG format
```

**Important Limitations:**
- Does NOT output DTCG format (you must transform)
- Does NOT infer token types (you must add `$type`)
- Does NOT create semantic naming (you must restructure)
- May not handle complex Sass functions/mixins

**Sources:**
- [scss-to-json npm](https://www.npmjs.com/package/scss-to-json)
- [sass-extract npm](https://www.npmjs.com/package/sass-extract)
- [LibSass is Deprecated](https://sass-lang.com/blog/libsass-is-deprecated/)
- [SCSS to design tokens workflow best practices](https://www.frontendtools.tech/blog/tailwind-css-best-practices-design-system-patterns)

### 5. Optional: Token Transformer

| Technology | Version | Purpose | Confidence |
|------------|---------|---------|------------|
| **token-transformer** | 0.0.33+ | Tokens Studio to Style Dictionary preprocessor | MEDIUM |

**Why:** Useful if you're using Tokens Studio Pro features (themes, token sets). Resolves tokens without file system access and can expand composite tokens.

**When to Use:**
- You're using Tokens Studio themes
- You have complex token sets with multiple layers
- You need to resolve references before Style Dictionary

**When to Skip:**
- Simple, flat token structures
- Using @tokens-studio/sd-transforms directly (it handles most transformations)

**Installation:**
```bash
npm install token-transformer -g
```

**Features:**
- Expands typography, shadow, composition, border properties
- Resolves references and math expressions
- Handles token aliases and sets
- Can preserve raw values if needed

**Sources:**
- [token-transformer npm](https://www.npmjs.com/package/token-transformer)
- [GitHub - design-token-transformer](https://github.com/lukasoppermann/design-token-transformer)

## Alternatives Considered

### Cobalt vs Style Dictionary

| Criterion | Style Dictionary | Cobalt |
|-----------|-----------------|--------|
| **DTCG Support** | First-class (v4+) | Native, DTCG-first |
| **Maturity** | Industry standard, proven at scale | Newer, less battle-tested |
| **Version** | 5.2.0 (Feb 2026) | 1.12.0 |
| **Ecosystem** | Massive plugin ecosystem, Amazon-backed | Growing, community-driven |
| **Migration Path** | Handles DTCG + legacy formats | DTCG-only (provides SD migration tool) |
| **Complexity** | More configuration | Simpler, opinionated defaults |
| **Best for** | Large enterprises, complex requirements | New projects, simpler setups |

**Verdict:** **Use Style Dictionary** for this project.

**Rationale:**
1. **Proven at scale:** Used by Amazon, Adobe, Shopify, Salesforce, and hundreds of enterprise design systems
2. **Mature ecosystem:** Extensive plugin library, well-documented, active community
3. **Required for Tokens Studio:** @tokens-studio/sd-transforms is built for Style Dictionary
4. **Migration-friendly:** Handles both DTCG and legacy formats during transition
5. **Your use case:** Extracting from existing SCSS codebase requires flexibility that Style Dictionary provides

**When to Use Cobalt:**
- Greenfield projects with no legacy formats
- Preference for simpler, opinionated tooling
- Already using DTCG format exclusively
- Smaller teams that value simplicity over flexibility

**Cobalt Advantages:**
- Simpler configuration (less boilerplate)
- DTCG-native from ground up
- Built-in linting (@cobalt-ui/lint-a11y)
- Can work alongside Style Dictionary (Style Dictionary integration available)

**Sources:**
- [Cobalt](https://cobalt-ui.pages.dev/)
- [Style Dictionary Integration | Cobalt](https://cobalt-ui.pages.dev/integrations/style-dictionary)
- [Design Token Management Tools 2025](https://cssauthor.com/design-token-management-tools/)

### JSON-to-SCSS vs SCSS-to-JSON Direction

| Approach | Pros | Cons | Confidence |
|----------|------|------|------------|
| **JSON → SCSS** (Recommended) | Platform-agnostic source, multi-output, tooling support, design-dev sync | Requires initial migration | HIGH |
| **SCSS → JSON** (Anti-pattern) | Leverages existing SCSS | Unmaintained tools, no type inference, coupling to Sass, one-way only | LOW |

**Recommendation:** **JSON → SCSS (JSON as source of truth)**

**Rationale:**
1. **Industry consensus:** All modern design token workflows in 2025/2026 use JSON as source of truth
2. **Multi-platform output:** Generate CSS, SCSS, JS, TS, iOS, Android from one source
3. **Design-dev sync:** Figma → Tokens Studio → JSON → Code creates bidirectional workflow
4. **Tooling ecosystem:** Style Dictionary, Cobalt, and all major tools expect JSON input
5. **Semantic clarity:** JSON format forces explicit token types, relationships, and semantic naming

**Your Migration Path:**
1. **One-time:** Extract SCSS variables → DTCG JSON (manual or semi-automated)
2. **Establish:** JSON files as source of truth in Git
3. **Configure:** Style Dictionary to generate SCSS files from JSON
4. **Integrate:** Tokens Studio for Figma to consume JSON
5. **Ongoing:** Update JSON tokens → regenerate SCSS + sync to Figma

**Sources:**
- [SCSS to design tokens workflow 2026](https://blogs.halodoc.io/implementation-of-design-token-at-halodoc/)
- [Design tokens best practices](https://www.frontendtools.tech/blog/tailwind-css-best-practices-design-system-patterns)

## What NOT to Use (and Why)

| Technology | Why Avoid | Alternative |
|------------|-----------|-------------|
| **sass-extract** | Depends on deprecated node-sass (EOL July 2024) | Manual extraction or scss-to-json for one-time use |
| **node-sass** | Officially deprecated, EOL | Dart Sass (but not needed for token workflow) |
| **scss-to-json (original)** | Last update 7 years ago, unmaintained | Manual extraction with semantic naming |
| **Legacy Tokens Studio format** | Non-standard, won't interoperate | W3C DTCG format (plugin supports both, choose DTCG) |
| **Style Dictionary v3** | Lacks native DTCG support | Style Dictionary v4+ (major breaking changes) |
| **Theo (Salesforce)** | Less active development vs Style Dictionary | Style Dictionary (larger ecosystem) |
| **SCSS as source of truth** | Anti-pattern in 2026, limits multi-platform output | JSON as source of truth, generate SCSS as output |
| **Hard-coded design values** | No single source of truth, design-dev drift | Design tokens with DTCG format |

**Critical Deprecations:**
- **LibSass/node-sass:** Deprecated, reached EOL in 2024. All tooling relying on node-sass is technical debt.
- **Sass @import:** Deprecated, removed in Dart Sass 3.0. Use @use rule instead.
- **Style Dictionary v3:** Lacks DTCG support. Migration to v4 has breaking changes but necessary.

**Sources:**
- [LibSass is Deprecated](https://sass-lang.com/blog/libsass-is-deprecated/)
- [Sass @import is Deprecated](https://sass-lang.com/blog/import-is-deprecated/)

## Installation & Setup

### Complete Stack Installation

```bash
# Core transformation engine
npm install style-dictionary@latest

# Tokens Studio integration (required if using Tokens Studio)
npm install @tokens-studio/sd-transforms@latest

# Optional: Token transformer (if using Tokens Studio themes)
npm install token-transformer

# Optional: One-time SCSS extraction (use with caution)
npm install scss-to-json
```

### Requirements
- **Node.js:** 18+ (required for Style Dictionary v4+)
- **Package Manager:** npm, yarn, or pnpm
- **Git:** For syncing tokens with Tokens Studio

### Basic Style Dictionary Configuration

Create `tokens.config.js`:

```javascript
import StyleDictionary from 'style-dictionary';
import { registerTransforms } from '@tokens-studio/sd-transforms';

// Register Tokens Studio transforms
registerTransforms(StyleDictionary);

const sd = new StyleDictionary({
  source: ['tokens/**/*.json'], // Your DTCG token files
  preprocessors: ['tokens-studio'], // Tokens Studio preprocessor
  platforms: {
    scss: {
      transformGroup: 'tokens-studio', // Tokens Studio transform group
      buildPath: 'build/scss/',
      files: [
        {
          destination: '_variables.scss',
          format: 'scss/variables',
        },
      ],
    },
    css: {
      transformGroup: 'tokens-studio',
      buildPath: 'build/css/',
      files: [
        {
          destination: 'variables.css',
          format: 'css/variables',
        },
      ],
    },
    js: {
      transformGroup: 'tokens-studio',
      buildPath: 'build/js/',
      files: [
        {
          destination: 'tokens.js',
          format: 'javascript/es6',
        },
      ],
    },
  },
});

sd.buildAllPlatforms();
```

**Build Command:**
```bash
npx style-dictionary build
```

**Output:** Generates `_variables.scss`, `variables.css`, and `tokens.js` from your DTCG JSON tokens.

### Tokens Studio Setup

1. **Install plugin in Figma:**
   - Open Figma
   - Plugins → Browse plugins → Search "Tokens Studio"
   - Install and open

2. **Configure storage:**
   - Settings → Storage → GitHub (recommended)
   - Connect to your repository
   - Point to `tokens/` directory

3. **Set format to W3C DTCG:**
   - Settings → Token Format → W3C DTCG
   - Converts existing tokens if switching from legacy

4. **Sync workflow:**
   - Designers update tokens in Figma
   - Push changes to GitHub branch
   - Developers pull, run Style Dictionary build
   - Generated SCSS/CSS/JS available for React app

**Sources:**
- [Install the Figma Plugin | Tokens Studio](https://docs.tokens.studio/get-started/install-figma-plugin)
- [Style Dictionary + SD Transforms](https://docs.tokens.studio/transform-tokens/style-dictionary)

## Recommended Workflow (Greenfield Token Initiative)

### Phase 1: One-Time Migration (SCSS → JSON)

1. **Audit SCSS variables:**
   ```bash
   grep -r "^\$" --include="*.scss" forms-flow-ai-micro-front-ends/
   ```

2. **Categorize by token type:**
   - Colors → `$type: "color"`
   - Spacing/sizing → `$type: "dimension"`
   - Typography → Composite tokens (font-family, font-size, font-weight, line-height)
   - Border radius → `$type: "dimension"`
   - Shadows → `$type: "shadow"`

3. **Create DTCG JSON structure:**
   ```
   tokens/
     color/
       brand.tokens.json
       semantic.tokens.json
     spacing.tokens.json
     typography.tokens.json
     border-radius.tokens.json
     shadow.tokens.json
   ```

4. **Manual extraction with semantic naming:**
   - Transform `$primary-color` → `color.brand.primary.$value`
   - Transform `$spacing-md` → `spacing.md.$value`
   - Add `$type` to each token
   - Establish token relationships with references `{color.brand.primary}`

5. **Validate extraction:**
   ```bash
   npx style-dictionary build
   ```
   - Verify generated SCSS matches original values
   - Check for missing/incorrect transformations

### Phase 2: Setup Token Infrastructure

1. **Install dependencies:**
   ```bash
   npm install style-dictionary @tokens-studio/sd-transforms
   ```

2. **Configure Style Dictionary** (see config above)

3. **Setup Tokens Studio in Figma:**
   - Install plugin
   - Configure GitHub sync
   - Set to W3C DTCG format
   - Import migrated tokens

4. **Verify bidirectional sync:**
   - Update token in JSON → builds to SCSS → imports to Figma
   - Update token in Figma → syncs to GitHub → builds to SCSS

### Phase 3: Integrate with React Codebase

1. **Update build process:**
   ```json
   // package.json
   {
     "scripts": {
       "tokens:build": "style-dictionary build",
       "prebuild": "npm run tokens:build"
     }
   }
   ```

2. **Import generated SCSS in React:**
   ```scss
   // src/styles/tokens.scss
   @use '../build/scss/variables' as tokens;

   .button-primary {
     background-color: tokens.$color-brand-primary;
     padding: tokens.$spacing-md;
     border-radius: tokens.$border-radius-md;
   }
   ```

3. **Replace hard-coded values:**
   - Find: `color: #0066cc;`
   - Replace: `color: tokens.$color-brand-primary;`

4. **Enable Figma MCP + Claude:**
   - Tokens available in Figma Variables
   - Claude can query token values via Figma MCP
   - Generate production-ready components with correct token references

### Phase 4: Ongoing Maintenance

1. **Token updates flow:**
   - Designer updates in Figma → Syncs to GitHub
   - Developer runs `npm run tokens:build`
   - SCSS/CSS/JS regenerated automatically
   - React app consumes updated tokens

2. **Version control:**
   - Commit token JSON files (source of truth)
   - DON'T commit generated SCSS/CSS/JS (build artifacts)
   - Add to `.gitignore`: `build/scss/`, `build/css/`, `build/js/`

3. **CI/CD integration:**
   ```yaml
   # .github/workflows/tokens.yml
   - name: Build Design Tokens
     run: npm run tokens:build

   - name: Verify Token Build
     run: test -f build/scss/_variables.scss
   ```

## Confidence Levels by Component

| Component | Confidence | Notes |
|-----------|-----------|-------|
| W3C DTCG Specification | **HIGH** | First stable version released Oct 2025, industry standard |
| Style Dictionary v4+ | **HIGH** | Latest 5.2.0, native DTCG support, proven at scale |
| Tokens Studio | **HIGH** | De facto Figma plugin, W3C DTCG compliant |
| @tokens-studio/sd-transforms | **HIGH** | Required bridge, latest 2.0.1, actively maintained |
| SCSS Extraction Tools | **LOW** | All tools unmaintained 4-7 years, recommend manual migration |
| token-transformer | **MEDIUM** | Maintained but optional, use if needed for complex setups |
| Cobalt | **MEDIUM** | Good alternative but less mature than Style Dictionary |
| Manual Migration Approach | **HIGH** | Most reliable for one-time SCSS → JSON migration |

## Open Questions / Validation Needed

1. **Existing SCSS Structure:**
   - What is the organization of SCSS variables in the codebase?
   - Are variables centralized or scattered across components?
   - How complex are the Sass functions/calculations?

2. **Token Scope:**
   - Which design tokens are in scope: Colors, spacing, typography, border-radius, shadows?
   - Are there component-specific tokens or only global tokens?
   - How many token values exist (estimate)?

3. **Team Workflow:**
   - Will designers own token updates in Figma going forward?
   - Does the team have GitHub access for Tokens Studio sync?
   - What is the approval process for token changes?

4. **Figma Setup:**
   - Is Figma already using Variables/Styles?
   - Are design files structured for token import?
   - Which Figma plan (Free, Pro, Enterprise)?

## Sources Summary

All findings verified with official documentation and recent sources (2025-2026):

**Primary Sources (HIGH Confidence):**
- [W3C Design Tokens Community Group](https://www.designtokens.org/)
- [Design Tokens Format Specification 2025.10](https://www.designtokens.org/tr/drafts/format/)
- [Style Dictionary Official Docs](https://styledictionary.com/)
- [Tokens Studio for Figma Docs](https://docs.tokens.studio)
- [@tokens-studio/sd-transforms npm](https://www.npmjs.com/package/@tokens-studio/sd-transforms)

**Secondary Sources (MEDIUM Confidence):**
- [Cobalt UI](https://cobalt-ui.pages.dev/)
- [token-transformer npm](https://www.npmjs.com/package/token-transformer)
- [Design Token Best Practices 2025-2026](https://www.frontendtools.tech/blog/tailwind-css-best-practices-design-system-patterns)

**Deprecation Notices (Official):**
- [LibSass is Deprecated](https://sass-lang.com/blog/libsass-is-deprecated/)
- [Sass @import is Deprecated](https://sass-lang.com/blog/import-is-deprecated/)

**Community/Ecosystem (MEDIUM-LOW Confidence):**
- Web search results for tool comparisons and workflow patterns
- npm package status and maintenance indicators

---

## Quick Decision Matrix

**If you're starting fresh (greenfield):**
→ W3C DTCG JSON + Style Dictionary v5 + Tokens Studio + JSON as source of truth

**If you have existing SCSS variables:**
→ One-time manual migration to DTCG JSON + Style Dictionary v5 + Tokens Studio + deprecate SCSS as source

**If you want simplest setup:**
→ W3C DTCG JSON + Cobalt + Tokens Studio (fewer tools, more opinionated)

**If you need enterprise scale:**
→ W3C DTCG JSON + Style Dictionary v5 + @tokens-studio/sd-transforms + token-transformer (maximum flexibility)

**For your specific use case (SCSS extraction to Figma):**
→ Manual SCSS audit → DTCG JSON migration → Style Dictionary v5 → Tokens Studio → Figma Variables

---

**Last Updated:** 2026-02-03
**Next Review:** When W3C DTCG publishes next specification version or Style Dictionary releases v6
