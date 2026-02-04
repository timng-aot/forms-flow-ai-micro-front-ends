# Phase 1: Audit & Foundation - Research

**Researched:** 2026-02-04
**Domain:** Design token auditing, SCSS/CSS parsing, W3C DTCG format specification
**Confidence:** MEDIUM

## Summary

Phase 1 requires auditing SCSS variables, CSS custom properties, and hardcoded design values across forms-flow-theme and component micro-frontends, then defining a W3C DTCG-compliant token structure. The established approach combines programmatic parsing tools (sass-extract for computed values, postcss-scss for AST traversal) with manual categorization and gap analysis. The W3C Design Tokens Community Group specification reached version 1 (2025.10) as a stable foundation in October 2025, providing authoritative format requirements for $value/$type properties, naming restrictions, and reference syntax.

Key challenges identified include handling SCSS computed values (functions like darken/lighten, mixins), maintaining full traceability (which files reference which variables), detecting hardcoded values in components, and avoiding common pitfalls like poor naming conventions or lack of developer adoption. The audit outputs JSON as source of truth with generated markdown summaries, structured by token type, with dedicated gap analysis reports.

**Primary recommendation:** Use sass-extract for SCSS variable extraction with computed values, postcss-scss for CSS custom property parsing, and custom scripts for hardcoded value detection. Structure audit outputs as JSON grouped by token type with full traceability data (file references, usage counts). Define DTCG structure in specification documents during Phase 1, defer actual token JSON creation to Phase 2.

## Standard Stack

The established libraries/tools for design token auditing and DTCG format compliance.

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| sass-extract | 2.x | Extract SCSS variables with computed values | Uses native libsass features to get identical values to generated CSS, handles complex expressions like `$var * 200px / 10` |
| postcss-scss | latest | Parse SCSS into AST for analysis | Official PostCSS parser for SCSS, parses mixins as custom at-rules and variables as properties |
| Style Dictionary | 4+ | Transform tokens to platform outputs (Phase 3) | Industry standard, supports both DTCG ($value/$type) and legacy formats, extensible plugin system |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| scss-parser | latest | Create queryable AST from SCSS | When need jQuery-like selectors for AST traversal (combine with query-ast) |
| postcss-extract-custom-properties | latest | Extract CSS custom properties | Dedicated plugin for CSS variable extraction if postcss-scss insufficient |
| @upft/schemas | latest | JSON Schema validation for DTCG tokens | Validate token JSON against DTCG spec (JSON Schema Draft 2020-12) |
| w3c-design-tokens-standard-schema | latest | TypeScript/Zod validation for DTCG | Type-safe token validation in TypeScript projects |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| sass-extract | string-extract-sass-vars | Regex-based extraction misses computed values, doesn't handle imports |
| postcss-scss | sass-parser (npm) | Only supports old .sass syntax, not SCSS; still in active development |
| Custom scripts | TokenLens (web tool) | Good for one-time audits but not automatable in CI/CD pipelines |

**Installation:**
```bash
npm install sass-extract postcss postcss-scss --save-dev
npm install style-dictionary @tokens-studio/sd-transforms --save-dev  # For Phase 3
npm install @upft/schemas --save-dev  # For validation
```

## Architecture Patterns

### Recommended Project Structure
```
tokens/
├── audit/                    # Phase 1 outputs (documentation only)
│   ├── theme-audit.json      # SCSS variables + CSS custom properties
│   ├── theme-audit.md        # Human-readable summary
│   ├── components-audit.json # Hardcoded values from micro-frontends
│   ├── components-audit.md   # Component audit summary
│   └── gap-analysis.json     # Dedicated gap report
├── core.json                 # Phase 2: Primitive tokens (documented structure in Phase 1)
└── semantic.json             # Phase 2: Semantic tokens (documented structure in Phase 1)
```

### Pattern 1: Full Traceability Audit Schema
**What:** Document every design value with name, computed value, type, and all file references
**When to use:** Always for audit outputs — enables gap analysis and extraction planning
**Example:**
```json
{
  "variables": {
    "$primary": {
      "value": "#1976d2",
      "computedValue": "#1976d2",
      "type": "color",
      "category": "color",
      "references": [
        {
          "file": "scss/_variables.scss",
          "line": 42,
          "context": "variable declaration"
        },
        {
          "file": "scss/components/_button.scss",
          "line": 15,
          "context": "background-color: $primary"
        }
      ],
      "usageCount": 47
    }
  },
  "customProperties": {
    "--font-size-base": {
      "value": "1rem",
      "computedValue": "16px",
      "type": "dimension",
      "category": "typography",
      "references": [
        {
          "file": "scss/_typography.scss",
          "line": 8,
          "context": "custom property declaration"
        }
      ],
      "usageCount": 23
    }
  }
}
```

### Pattern 2: Hardcoded Value Detection with Deduplication
**What:** Scan components for design values, report unique values with occurrence counts
**When to use:** Component micro-frontend audits to identify gaps
**Example:**
```json
{
  "hardcodedValues": {
    "colors": [
      {
        "value": "#e0e0e0",
        "type": "color",
        "occurrences": 12,
        "locations": [
          {
            "package": "forms-flow-admin",
            "file": "src/components/Table.scss",
            "line": 34,
            "property": "border-color"
          }
        ],
        "suggestedToken": "ff.color.border.default"
      }
    ],
    "spacing": [
      {
        "value": "0.75rem",
        "type": "dimension",
        "occurrences": 8,
        "locations": [
          {
            "package": "forms-flow-nav",
            "file": "src/Navigation.scss",
            "line": 56,
            "property": "padding"
          }
        ],
        "suggestedToken": "ff.spacing.sm"
      }
    ]
  }
}
```

### Pattern 3: Bootstrap Override Documentation
**What:** Capture both Bootstrap defaults and project overrides for context
**When to use:** When auditing Bootstrap-based themes to understand what changed and why
**Example:**
```json
{
  "bootstrapOverrides": {
    "$primary": {
      "bootstrapDefault": "#007bff",
      "projectOverride": "#1976d2",
      "computedValue": "#1976d2",
      "type": "color",
      "rationale": "Brand color alignment"
    }
  }
}
```

### Pattern 4: DTCG Structure Specification (Documentation)
**What:** Define token structure in spec document, don't create actual JSON files yet
**When to use:** Phase 1 to validate structure before extraction in Phase 2
**Example (in DTCG-SPEC.md):**
```markdown
## Token File Structure

### core.json
Primitive tokens - raw design values

{
  "ff": {
    "color": {
      "primary-500": {
        "$value": "#1976d2",
        "$type": "color",
        "$description": "Primary brand color"
      }
    },
    "spacing": {
      "md": {
        "$value": "1rem",
        "$type": "dimension",
        "$description": "Medium spacing unit"
      }
    }
  }
}

### semantic.json
Purpose-based tokens referencing primitives

{
  "ff": {
    "color": {
      "action": {
        "primary": {
          "$value": "{ff.color.primary-500}",
          "$type": "color",
          "$description": "Primary action color for buttons, links"
        }
      }
    }
  }
}
```

### Anti-Patterns to Avoid
- **Losing computed values:** Don't use regex/string parsing for SCSS variables — functions like `darken($color, 10%)` won't compute correctly. Use sass-extract which compiles SCSS to get actual values.
- **No file traceability:** Audits without "which files use this variable" data make gap analysis impossible. Always track references.
- **Manual audit only:** Hand-cataloging hundreds of variables is error-prone and unmaintainable. Script it, generate JSON, review markdown summaries.
- **Creating token JSON in Phase 1:** Phase 1 is documentation/specification only. Actual token files created in Phase 2 after structure validated.

## Don't Hand-Roll

Problems that look simple but have existing solutions.

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| SCSS variable extraction | Custom regex parser | sass-extract | Regex can't handle imports, functions, mixins, or compute values like `darken()`. sass-extract uses libsass to compile and extract actual computed values. |
| CSS custom property parsing | String scanning | postcss-scss + PostCSS plugins | PostCSS has battle-tested parsers for CSS syntax including custom properties, handles edge cases, provides AST for reliable extraction. |
| Hardcoded value detection | Manual grep | Combination of regex + postcss + validation | Detecting all color formats (hex, rgb, hsl), spacing units, and typography values requires comprehensive patterns. TokenLens does this but isn't CLI-automatable. |
| DTCG validation | Custom JSON checks | @upft/schemas or w3c-design-tokens-standard-schema | DTCG spec has many rules (naming restrictions, reference syntax, type requirements). Existing schemas encode these correctly. |
| Token transformation | Custom build scripts | Style Dictionary | Cross-platform token transformation is complex (unit conversion, color formats, etc.). Style Dictionary is industry standard with plugins for DTCG. |

**Key insight:** SCSS compilation and CSS parsing have edge cases that tools solve (import resolution, function evaluation, vendor prefixes, syntax variations). Design token validation has strict W3C spec requirements. Use established tools rather than reimplementing parsers and validators.

## Common Pitfalls

### Pitfall 1: Ignoring Computed SCSS Values
**What goes wrong:** Audit reports `$button-bg: darken($primary, 10%)` as string value, not actual computed color. Phase 2 extraction fails because value can't be converted to hex.
**Why it happens:** Using simple file parsing (grep, regex) instead of SCSS compilation. Variables that reference other variables or use functions don't get resolved.
**How to avoid:** Use sass-extract which compiles SCSS via libsass and extracts computed values identical to generated CSS. Mark computed values in audit for manual review if function can't be represented in DTCG.
**Warning signs:** Audit JSON contains string values like `"darken($primary, 10%)"` instead of `"#0d47a1"`.

### Pitfall 2: Poor Token Naming Leads to Unmaintainable System
**What goes wrong:** Tokens named `color.blue` or `spacing.16px` instead of semantic names. When brand colors change from blue to purple, token names become misleading. Developers ignore token system and hardcode values.
**Why it happens:** Copying variable names directly from SCSS without considering token tier (primitive vs semantic). Not establishing naming conventions before audit.
**How to avoid:** User decisions specify: primitives use numeric scales (`primary-100` through `primary-900`), semantics use purpose-based names (`ff.color.action.primary`), spacing uses t-shirt sizes (`xs`, `sm`, `md`, `lg`, `xl`). Document conventions in Phase 1 before extraction.
**Warning signs:** Audit suggests token names based on current values rather than purpose. Example: `button-blue-color` instead of `button-primary-color`.

### Pitfall 3: Missing File References Breaks Gap Analysis
**What goes wrong:** Audit lists all SCSS variables but doesn't track where they're used. Can't identify which component hardcoded values should map to which theme variables. Gap analysis incomplete.
**Why it happens:** Simple extraction scripts only parse variable declarations, don't scan usage. Faster to build but loses critical traceability.
**How to avoid:** Audit schema must include `references` array with file paths, line numbers, and usage context for every variable. Scan all SCSS/CSS files, not just declaration files.
**Warning signs:** Audit JSON has variables but no usage data. Can't answer "which components use this color?"

### Pitfall 4: Treating Audit as One-Time Activity
**What goes wrong:** Run audit once, generate report, never update. Codebase changes, audit data becomes stale. Phase 2 extraction based on outdated information.
**Why it happens:** Audit is manual process or hard to re-run. No version control, no automation.
**How to avoid:** Audit should be scriptable and repeatable. Store audit data in git with commit history. When SCSS changes, re-run audit to validate assumptions before extraction.
**Warning signs:** Audit report is dated weeks before extraction work begins. No script to regenerate audit.

### Pitfall 5: Bootstrap Override Blindness
**What goes wrong:** Audit captures project's Bootstrap variable overrides but not original Bootstrap defaults. Can't tell if override is intentional brand customization or accidental divergence.
**Why it happens:** Only scanning project SCSS files, not checking Bootstrap source or documentation.
**How to avoid:** User decision: "Claude's discretion on whether to capture original Bootstrap defaults alongside overrides." Recommendation: YES — document both default and override in audit for context. Helps Phase 2 distinguish intentional customization from potential consolidation candidates.
**Warning signs:** Audit shows `$primary: #1976d2` but no indication this overrides Bootstrap's `#007bff` default.

### Pitfall 6: DTCG Naming Violations
**What goes wrong:** Token names include reserved characters (`$`, `{`, `}`, `.`) causing parser errors. References break because curly braces in names conflict with reference syntax.
**Why it happens:** Copying SCSS variable names directly (`$primary` → token name includes `$`). Not validating against DTCG restrictions.
**How to avoid:** DTCG spec reserves `{`, `}` for references, `$` for property prefixes. Token names must avoid these. User decision: prefix `ff-` (formsflow), use dot notation for groups (`ff.color.primary` where `ff`, `color` are groups, `primary` is token name). Validate names before creating structure.
**Warning signs:** Token names like `$primary` or `color.primary.default` (dot in token name itself, not group separator).

### Pitfall 7: No Validation Before Phase 2
**What goes wrong:** Define token structure in Phase 1 docs, discover format violations in Phase 2 when creating actual JSON. Rework delays extraction.
**Why it happens:** Documentation only, no validation step. Assumptions about DTCG format prove incorrect.
**How to avoid:** Create minimal example token files in Phase 1 to test structure validity. Use @upft/schemas or w3c-design-tokens-standard-schema to validate. Iterate on structure before Phase 2 extraction.
**Warning signs:** DTCG spec document has structure examples but no validated JSON, no schema checks.

## Code Examples

Verified patterns from official sources and package documentation.

### Extract SCSS Variables with Computed Values
```javascript
// Using sass-extract to get computed values
// Source: https://github.com/jgranstrom/sass-extract

const sassExtract = require('sass-extract');
const path = require('path');

async function extractScssVariables(scssFilePath) {
  const rendered = await sassExtract.render({
    file: scssFilePath,
  });

  // rendered.vars contains all variables with computed values
  const variables = {};

  for (const [varName, varData] of Object.entries(rendered.vars.global)) {
    variables[varName] = {
      value: varData.value,           // Original SCSS value
      compiledValue: varData.value,   // Computed value
      type: varData.type,             // 'SassColor', 'SassDimension', etc.
      unit: varData.unit || null,     // 'px', 'rem', etc.
    };
  }

  return variables;
}

// Extract from forms-flow-theme
const themeVars = await extractScssVariables(
  path.join(__dirname, '../forms-flow-theme/scss/_variables.scss')
);
```

### Parse CSS Custom Properties with PostCSS
```javascript
// Using postcss-scss for CSS custom property extraction
// Source: https://github.com/postcss/postcss-scss

const postcss = require('postcss');
const scss = require('postcss-scss');
const fs = require('fs');

function extractCssCustomProperties(scssContent) {
  const customProperties = {};

  const root = postcss.parse(scssContent, { syntax: scss });

  root.walkDecls(decl => {
    // Check if declaration is a CSS custom property
    if (decl.prop.startsWith('--')) {
      customProperties[decl.prop] = {
        value: decl.value,
        file: decl.source.input.file,
        line: decl.source.start.line,
      };
    }
  });

  return customProperties;
}

const scssContent = fs.readFileSync('path/to/file.scss', 'utf-8');
const cssVars = extractCssCustomProperties(scssContent);
```

### Detect Hardcoded Color Values
```javascript
// Pattern for detecting hardcoded colors in SCSS/CSS
// Source: Regex patterns from https://gist.github.com/olmokramer/82ccce673f86db7cda5e

const colorPatterns = {
  hex: /#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})\b/g,
  rgb: /rgba?\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([\d.]+)\s*)?\)/g,
  hsl: /hsla?\s*\(\s*([\d.]+)\s*,\s*([\d.]+)%\s*,\s*([\d.]+)%\s*(?:,\s*([\d.]+)\s*)?\)/g,
};

function detectHardcodedColors(cssContent, filePath) {
  const hardcodedColors = [];

  for (const [format, pattern] of Object.entries(colorPatterns)) {
    let match;
    while ((match = pattern.exec(cssContent)) !== null) {
      hardcodedColors.push({
        value: match[0],
        format: format,
        file: filePath,
        index: match.index,
      });
    }
  }

  return hardcodedColors;
}
```

### Validate DTCG Token JSON
```javascript
// Using @upft/schemas for DTCG validation
// Source: https://www.npmjs.com/package/@upft/schemas

const Ajv = require('ajv');
const { tokenFileSchema } = require('@upft/schemas');

function validateTokenFile(tokenJson) {
  const ajv = new Ajv({ strict: false });
  const validate = ajv.compile(tokenFileSchema);

  const valid = validate(tokenJson);

  if (!valid) {
    console.error('DTCG validation errors:', validate.errors);
    return false;
  }

  return true;
}

// Example token structure to validate
const exampleTokens = {
  "ff": {
    "color": {
      "primary-500": {
        "$value": "#1976d2",
        "$type": "color",
        "$description": "Primary brand color"
      }
    }
  }
};

const isValid = validateTokenFile(exampleTokens);
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual SCSS variable cataloging | Automated extraction via sass-extract | 2018-2020 | Eliminated human error, captured computed values accurately, made audits repeatable |
| Proprietary token formats | W3C DTCG format ($value, $type) | Oct 2025 (v1 stable) | Industry standardization, tool interoperability (Figma Variables, Style Dictionary, Token Studio all support DTCG) |
| Single-tier token structure | Multi-tier (primitive/semantic/component) | 2020-2022 | Improved maintainability, clearer token relationships, easier theme customization |
| Regex-based hardcoded value detection | PostCSS AST parsing | 2019-present | More reliable detection, fewer false positives, handles complex CSS syntax |
| Style Dictionary legacy format | Style Dictionary v4 with DTCG support | 2023-2024 | Can use $value/$type or legacy value/type, forward compatibility with spec |

**Deprecated/outdated:**
- **@import in SCSS:** Sass team deprecated @import, use @use and @forward instead (Dart Sass 3.0 will remove @import support)
- **Style Dictionary v3 legacy format:** v4 supports both DTCG and legacy, but DTCG is recommended for new projects
- **sass-extract maintenance:** Package marked "Inactive" (no npm updates in 12+ months), but still widely used and functional. Consider forking if critical bugs emerge.

## Open Questions

Things that couldn't be fully resolved during research.

1. **Optimal handling of SCSS functions in DTCG tokens**
   - What we know: sass-extract computes final values (e.g., `darken($primary, 10%)` → `#0d47a1`). DTCG format doesn't have native "function" type.
   - What's unclear: Best practice for documenting "this value is computed via SCSS function" in audit. Should $description note this? Should audit capture original expression?
   - Recommendation: Audit JSON captures both `value` (original expression) and `computedValue` (hex result). Document in Phase 1 spec that computed values lose function context — acceptable tradeoff for DTCG compatibility.

2. **Bootstrap override documentation scope**
   - What we know: User decision leaves this to "Claude's discretion based on what's useful for extraction."
   - What's unclear: Effort vs. value. Requires fetching Bootstrap source for specific version used.
   - Recommendation: YES, document Bootstrap defaults alongside overrides. Check package.json for Bootstrap version, reference official _variables.scss for that version. Adds context for extraction decisions (keep override vs. consolidate to default).

3. **Validation timing and tooling**
   - What we know: Multiple DTCG validation tools exist (@upft/schemas, w3c-design-tokens-standard-schema), both JSON Schema-based.
   - What's unclear: Which to choose? When to run validation (Phase 1 on spec examples, or Phase 2 on actual tokens)?
   - Recommendation: Use @upft/schemas (more comprehensive, validates token files, manifests, type safety). Run validation in Phase 1 on minimal example tokens to validate structure before Phase 2 extraction. Prevents rework.

4. **Component audit depth vs. effort**
   - What we know: User decision specifies "lighter pass on component micro-frontends, scan for hardcoded values, report unique values with occurrence counts."
   - What's unclear: Definition of "lighter pass" — which file types to scan (.scss only, or .jsx/.tsx inline styles too)?
   - Recommendation: Phase 1 scans .scss and .css files only in component packages. Defer inline JS/TS styles to v2 if time permits. Focuses effort on stylesheet consolidation first.

## Sources

### Primary (HIGH confidence)
- W3C Design Tokens Community Group specification (2025.10): https://www.designtokens.org/tr/drafts/format/
- W3C DTCG announcement (Oct 2025): https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/
- sass-extract GitHub repository: https://github.com/jgranstrom/sass-extract
- postcss-scss GitHub repository: https://github.com/postcss/postcss-scss
- Style Dictionary official docs: https://styledictionary.com/
- Tokens Studio DTCG format reference: https://docs.tokens.studio/manage-settings/token-format

### Secondary (MEDIUM confidence)
- Design tokens audit methodology (UX Collective, Jan 2026): https://uxdesign.cc/design-tokens-with-confidence-862119eb819b
- Design token management tools guide (CSS Author, 2025): https://cssauthor.com/design-token-management-tools/
- TokenLens hardcoded value detection: https://tokenlens.app/
- Bootstrap SCSS override best practices: https://getbootstrap.com/docs/5.3/customize/sass/
- Design token tier hierarchy (Contentful): https://www.contentful.com/blog/design-token-system/

### Tertiary (LOW confidence)
- WebSearch results for SCSS parsing tools (no specific 2026 updates found, tools remain current standard)
- Community discussions on design token pitfalls (marked for validation with official sources)

## Metadata

**Confidence breakdown:**
- Standard stack: MEDIUM - Tools verified via official repositories and npm, but sass-extract maintenance status unclear (marked inactive)
- Architecture: HIGH - Patterns align with DTCG spec, user decisions, and industry best practices from multiple sources
- Pitfalls: MEDIUM - Based on 2025-2026 articles and community sources, cross-referenced with official documentation where possible
- DTCG format rules: MEDIUM - Specification URL redirects multiple times, couldn't fetch full technical spec directly, relied on secondary sources (Tokens Studio docs, community articles) describing DTCG requirements

**Research date:** 2026-02-04
**Valid until:** 2026-03-06 (30 days - DTCG spec is stable v1, tool ecosystem changes slowly)

---

## Research Notes

**What couldn't be verified:**
- Direct access to W3C DTCG format specification (URL redirects, 403 errors) — relied on secondary sources (Tokens Studio, Style Dictionary docs, community articles) that describe DTCG requirements
- sass-extract current maintenance status uncertain (marked "Inactive" but widely used) — may need alternative if bugs found
- Bootstrap default values for specific version (requires checking forms-flow-theme's package.json for version, then referencing Bootstrap source)

**Key constraints from CONTEXT.md decisions:**
- Two-tier structure only (core/semantic), component tier deferred
- Single file per tier (core.json, semantic.json)
- Phase 1 is documentation only — no actual token JSON files created
- Audit outputs: JSON as source of truth, markdown for review
- Gap analysis: separate dedicated report
- All audit files in tokens/audit/ directory

**Areas of Claude's discretion exercised:**
- Recommended YES to capturing Bootstrap defaults alongside overrides (useful context for extraction)
- Audit JSON schema: proposed structure with full traceability (value, computedValue, type, references array, usageCount)
- Markdown summary: recommend grouping by token type with usage statistics
- SCSS computed values: capture both original expression and computed result, document in spec that DTCG loses function context

**Research quality self-assessment:**
- Domains covered: SCSS parsing ✓, CSS custom properties ✓, hardcoded value detection ✓, DTCG format ✓, audit patterns ✓, common pitfalls ✓
- Multiple sources verified: Tool capabilities cross-referenced between GitHub, npm, official docs ✓
- Gaps acknowledged: Direct DTCG spec access failed, relying on authoritative secondary sources ✓
- Actionable for planning: Specific tools, versions, code examples, schema patterns provided ✓
