# Design Token Extraction Pitfalls

**Domain:** Design Token Extraction from SCSS
**Researched:** 2026-02-03
**Confidence:** HIGH (verified with official documentation and multiple authoritative sources)

## Executive Summary

Design token extraction projects commonly fail due to five critical areas: SCSS parsing edge cases, W3C DTCG format compliance errors, Token Studio import incompatibilities, naming problems that break toolchains, and extraction granularity issues. This document catalogs specific pitfalls with detection strategies and prevention approaches mapped to project phases.

---

## Critical Pitfalls

Mistakes that cause rewrites, major tool failures, or complete project blockage.

### Pitfall 1: CSS Custom Property Interpolation Missing

**What goes wrong:** SCSS variables assigned to CSS custom properties without interpolation syntax appear as literal text (`--color: $primary-blue`) instead of resolved values (`--color: #0066cc`).

**Why it happens:** Sass requires SassScript expressions in custom properties to use `#{...}` interpolation to maintain compatibility with plain CSS. The CSS spec allows almost any string in custom properties, so Sass doesn't parse them as SassScript by default.

**Consequences:**
- Generated CSS contains SCSS variable names instead of values
- Runtime failures when JavaScript tries to read CSS custom properties
- Tokenized values are strings like `"$primary-blue"` instead of actual color codes
- Downstream tools (Token Studio, validators) reject invalid color/dimension values

**Prevention:**
```scss
// WRONG - Variable appears as literal text
--accent-color: $accent-color;

// CORRECT - Variable is interpolated
--accent-color: #{$accent-color};
```

**Detection:**
- Search extracted CSS for `--*: $` patterns
- Validate CSS custom property values against expected types (hex colors, px units)
- Run CSS through a linter that validates custom property syntax
- Test a sample import into Token Studio with a known SCSS variable

**Phase mapping:** Address in Phase 1 (SCSS Analysis). Document all SCSS→CSS variable conversions and ensure extraction script adds interpolation.

**Source confidence:** HIGH - [Official Sass documentation](https://sass-lang.com/documentation/breaking-changes/css-vars/)

---

### Pitfall 2: Missing or Incorrect `$type` in W3C DTCG Format

**What goes wrong:** Design token JSON missing `$type` properties or using legacy type names causes validation failures and tool incompatibility.

**Why it happens:**
- Style Dictionary v3 (legacy) format used `"type"` without dollar sign
- DTCG spec requires `"$type"` with dollar prefix
- Type values changed: `"size"` → `"dimension"`, requiring manual updates
- Automated converters don't refactor type values, only property names

**Consequences:**
- Token validators reject files: "Contents Don't Pass Schema Validation"
- Token Studio import fails or imports tokens with wrong type
- Type inference breaks, treating dimensions as strings
- Cross-tool compatibility fails (Figma Variables expects DTCG types)

**Prevention:**
```json
// WRONG - Legacy Style Dictionary v3 format
{
  "spacing": {
    "small": {
      "type": "size",
      "value": "8px"
    }
  }
}

// CORRECT - W3C DTCG format
{
  "spacing": {
    "small": {
      "$type": "dimension",
      "$value": "8px"
    }
  }
}
```

**Detection:**
- Validate JSON against W3C DTCG schema before Token Studio import
- Use official validators: [Design Token Validator](https://designtoken-validator.sotec-solutions.com/)
- Check for presence of `$` prefix on all spec-defined properties
- Verify type values match DTCG spec (not legacy Style Dictionary types)
- Warning signs: TypeScript errors from `@nclsndr/w3c-design-tokens-parser`

**Phase mapping:**
- Phase 1: Choose DTCG format from start (don't use legacy)
- Phase 2: Validate all generated JSON against DTCG schema
- Phase 3: Automated tests that fail if `$type` is missing from any token

**Source confidence:** HIGH - [W3C DTCG Specification (stable v1, Oct 2025)](https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/), [Style Dictionary DTCG docs](https://styledictionary.com/info/dtcg/)

---

### Pitfall 3: Token Names Using Reserved Characters

**What goes wrong:** Token names with special characters cause parsing failures, reference breakage, and import errors in Token Studio.

**Why it happens:** Different tools have conflicting constraints:
- Figma uses `/` for grouping
- DTCG spec forbids `$` prefix on token names
- Reference syntax uses `{ }` braces
- Programming languages restrict `( ) [ ]` brackets
- Periods `.` convert to slashes `/` creating unintended folder structures

**Consequences:**
- Token Studio import completely fails with syntax errors
- Token references break: `{color.primary.500}` becomes unresolvable
- Generated code has syntax errors from invalid identifiers
- Naming collisions: `spacing.1.5` and `spacing.1-5` both flatten to `spacing15`
- Case sensitivity issues: `tokenName` vs `TokenName` create duplicates

**Forbidden characters:**
- `/` - Creates groups in Figma
- `$` - Reserved for spec properties (`$type`, `$value`)
- `{ }` - Reference syntax, "totally breaks the code"
- `[ ] ( )` - Cause "undesirable results" in code transformation
- Spaces, emojis, special symbols - Require custom transformations

**Forbidden names (anatomical terms):**
- `name`, `type`, `value`, `description` - Functionally reserved by spec

**Prevention:**
```
// WRONG - Multiple problems
{
  "$primary-color": { ... },           // Starts with $
  "spacing/large": { ... },            // Contains /
  "color{accent}": { ... },            // Contains { }
  "font-size[mobile]": { ... },        // Contains [ ]
  "spacing.1.5": { ... },              // Ambiguous flattening
  "Primary Color": { ... }             // Contains space
}

// CORRECT - Clean, safe names
{
  "color-primary": { ... },
  "spacing-large": { ... },
  "color-accent": { ... },
  "font-size-mobile": { ... },
  "spacing-xs": { ... },               // Or spacing-150
  "primary-color": { ... }
}
```

**Detection:**
- Regex validation: `/[$/\{\}\[\]\(\)\s]|^(name|type|value|description)$/`
- Check for numeric patterns that flatten to same identifier
- Test case sensitivity collisions
- Lint SCSS variable names before extraction
- Validate against Token Studio technical specs before import

**Phase mapping:**
- Phase 1: Define naming convention that forbids all reserved characters
- Phase 2: Automated validation in extraction script
- Phase 3: Pre-commit hook rejecting forbidden characters

**Source confidence:** HIGH - [Token Studio Technical Specs](https://docs.tokens.studio/manage-tokens/token-names/technical-specs)

---

### Pitfall 4: Broken Token References After Filtering

**What goes wrong:** Using `outputReferences: true` with filters creates broken references when referenced tokens are filtered out.

**Why it happens:** Style Dictionary outputs token references (`{color.primary}`) instead of values, but if `color.primary` is filtered from the output, the reference points to nothing.

**Consequences:**
- Generated CSS/JSON contains unresolved references: `var(--color-primary)` where `--color-primary` doesn't exist
- Runtime errors in consuming applications
- Token Studio can't import files with dangling references
- Build succeeds but output is broken

**Prevention:**
```javascript
// WRONG - References break when target is filtered
{
  platforms: {
    css: {
      transformGroup: 'css',
      files: [{
        destination: 'variables.css',
        format: 'css/variables',
        options: {
          outputReferences: true // Dangerous with filters!
        },
        filter: (token) => token.attributes.category === 'color'
      }]
    }
  }
}

// CORRECT - Use outputReferencesFilter utility
import { outputReferencesFilter } from 'style-dictionary/utils';

{
  files: [{
    destination: 'variables.css',
    format: 'css/variables',
    filter: outputReferencesFilter, // Only outputs refs when target exists
    options: {
      outputReferences: true
    }
  }]
}
```

**Detection:**
- Style Dictionary warnings: "broken reference" in build output
- Search generated files for undefined variable references
- Validate that every `{reference}` has a corresponding token definition
- Test import into Token Studio (fails on unresolved references)

**Phase mapping:**
- Phase 2: Use `outputReferencesFilter` utility from start
- Phase 3: Automated tests validating all references resolve
- Phase 4: CI/CD validation that imports succeed

**Source confidence:** HIGH - [Style Dictionary References docs](https://styledictionary.com/reference/utils/references/)

---

## Moderate Pitfalls

Mistakes that cause delays, technical debt, or require significant refactoring.

### Pitfall 5: Extracting SCSS Functions and Mixins as Tokens

**What goes wrong:** Attempting to extract computed values from SCSS `@function` or `@mixin` calls fails because they require runtime evaluation.

**Why it happens:** Design tokens must be static values. SCSS functions/mixins are code that computes values dynamically, which can't be represented in JSON without executing the Sass compiler.

**Consequences:**
- Extraction scripts skip function calls, losing design decisions
- Manually computed values diverge from SCSS source of truth
- No way to represent logic in token format: `spacing(2)` can't become JSON
- Missing semantic relationships (e.g., "spacing-medium is 2× spacing-base")

**Examples of unextractable patterns:**
```scss
// Functions - require evaluation
$spacing-large: spacing-scale(3); // What's the output without running Sass?

// Mixins - generate multiple properties
@mixin button-primary {
  background: $color-primary;
  padding: spacing(2);
}

// Calculations
$header-height: $base-unit * 8 + $border-width;

// Interpolation in selectors
.theme-#{$brand-color} { ... }
```

**Prevention:**
- **Audit strategy:** Identify computed values before extraction
- **Compile-first approach:** Run `sass` to generate CSS, then extract from CSS (loses semantic structure)
- **Manual decomposition:** Replace function calls with static values in a tokens-only SCSS file
- **Accept limitations:** Document that dynamic patterns won't be tokenized

**Detection:**
- Grep for `@function`, `@mixin`, `@include` in SCSS files
- Search for arithmetic operators: `* / + -` in value positions
- Identify interpolation: `#{...}` in values
- Count how many "design decisions" are in functions vs variables

**Phase mapping:**
- Phase 1: Audit all SCSS for computed patterns (categorize as extractable/not)
- Phase 2: Create static token file from computed values (compile to get values)
- Phase 3: Document unextractable patterns for manual maintenance

**Source confidence:** MEDIUM - Verified through [Sass documentation](https://sass-lang.com/documentation/at-rules/mixin/) and community articles

---

### Pitfall 6: Over-Extraction (Token Explosion)

**What goes wrong:** Extracting every SCSS variable creates hundreds of tokens that are too granular for practical use.

**Why it happens:**
- Programmatic extraction captures everything without editorial judgment
- Bootstrap 5 has 600+ variables, many internal/computed
- No distinction between "API tokens" (public) and "internal variables" (private)
- Fear of missing something leads to "extract everything" approach

**Consequences:**
- Token Studio performance degradation with 500+ tokens
- Designers overwhelmed by choice, can't find the right token
- Maintenance burden: updating 1 design decision requires changing 20 tokens
- Documentation becomes unmanageable
- "Excessive design choice can slow down design work and make communication unnecessarily granular" ([The Design System Guide](https://thedesignsystem.guide/design-tokens))

**Prevention:**
- **Tiered extraction:** Extract only primitive/global tokens first
  - Primitives: `color-blue-500`, `spacing-base`
  - Skip component tokens: `button-padding-x` (let components reference primitives)
- **Editorial review:** Not every variable is a token
- **80/20 rule:** 20% of tokens drive 80% of usage
- **Bootstrap-specific:** Extract `$theme-colors`, `$spacers`, `$font-sizes` but skip internal calculation variables

**Detection:**
- Token count >200 for initial extraction (warning sign)
- Many tokens with zero usage in designs
- Tokens that are just mathematical variations of others
- Naming conflicts indicating over-granularity

**Phase mapping:**
- Phase 1: Define extraction criteria (what makes a variable a token?)
- Phase 2: Extract only tier-1 primitives (colors, spacing, typography)
- Phase 3: Add semantic aliases based on actual usage patterns
- Phase 4: Add component tokens only if needed

**Source confidence:** MEDIUM - Synthesized from multiple sources including design token best practices articles

---

### Pitfall 7: Under-Extraction (Missing Semantic Layer)

**What goes wrong:** Extracting only primitive values without semantic aliases creates brittle designs that break when brand changes.

**Why it happens:**
- Focus on SCSS variables as-is without considering token tiers
- Extraction treats `$primary-color: #0066cc` as complete
- Missing intermediate layer: primitive → semantic → component

**Consequences:**
- Designs hard-code `color-blue-500` everywhere
- Rebrand requires changing 100 components instead of 1 token
- No semantic meaning: "What's the accent color?" requires reading code
- Components coupled to primitives instead of semantic intent

**Prevention - Three-tier structure:**
```json
{
  "// TIER 1: Primitives (from SCSS extraction)": "",
  "color": {
    "blue": {
      "500": { "$type": "color", "$value": "#0066cc" }
    }
  },

  "// TIER 2: Semantic aliases (add during Phase 3)": "",
  "color": {
    "brand": {
      "primary": { "$type": "color", "$value": "{color.blue.500}" }
    }
  },

  "// TIER 3: Component tokens (add in Phase 4)": "",
  "button": {
    "primary": {
      "background": { "$type": "color", "$value": "{color.brand.primary}" }
    }
  }
}
```

**Detection:**
- All token references are primitives (no semantic meaning)
- Component updates require changing multiple primitive references
- Designers ask "Which blue should I use?" (no clear answer)

**Phase mapping:**
- Phase 1-2: Extract primitives from SCSS
- Phase 3: Add semantic layer (brand colors, functional roles)
- Phase 4: Add component layer based on usage patterns

**Source confidence:** HIGH - [Design token naming best practices](https://www.netguru.com/blog/design-token-naming-best-practices)

---

### Pitfall 8: Overspecific Component-Coupled Naming

**What goes wrong:** Token names tied to specific components (`button-primary-background`) can't be reused elsewhere.

**Why it happens:** Naming mirrors SCSS structure which is component-focused. Extraction process preserves component coupling without considering reusability.

**Consequences:**
- "Design tokens tied to particular components limit reusability and adaptability" ([Common Mistakes in Design Tokens](https://designtokens.substack.com/p/common-mistakes-in-design-tokens))
- Can't reuse `button-primary-background` for cards/badges
- Token proliferation: need `card-primary-background`, `badge-primary-background` for same color
- Difficult to enforce consistency across similar components

**Prevention:**
```json
// WRONG - Component-coupled
{
  "button-primary-background": { "$value": "#0066cc" },
  "card-accent-background": { "$value": "#0066cc" },
  "badge-highlight-background": { "$value": "#0066cc" }
}

// CORRECT - Semantic function
{
  "color-action-primary": { "$value": "#0066cc" },
  "color-surface-emphasis": { "$value": "#0066cc" }
}
```

**Detection:**
- Many tokens with identical values but different component names
- Token names start with component names: `button-*`, `card-*`, `input-*`
- Requests to add "the same color but for X component"

**Phase mapping:**
- Phase 1: Flag component-specific variables during SCSS audit
- Phase 2: Extract as primitives, not component tokens
- Phase 3: Create semantic tokens representing intent, not component
- Phase 4: Document which components use which semantic tokens

**Source confidence:** HIGH - [Common Mistakes in Design Tokens](https://designtokens.substack.com/p/common-mistakes-in-design-tokens)

---

## Minor Pitfalls

Mistakes that cause annoyance or require cleanup but are easily fixable.

### Pitfall 9: Inconsistent Naming Conventions

**What goes wrong:** Mixing naming styles (kebab-case, snake_case, camelCase) within the same token set.

**Why it happens:** Different SCSS files use different conventions, extraction preserves inconsistency.

**Consequences:**
- Hard to remember which tokens use which style
- Autocomplete less helpful (can't predict format)
- Looks unprofessional in documentation
- Sorting/grouping becomes arbitrary

**Prevention:**
- Choose one convention (kebab-case recommended for cross-platform compatibility)
- Transform all extracted names to match convention
- Document the standard in Phase 1

**Detection:**
- Regex search for multiple case styles in same file
- Linter rules for token naming

**Phase mapping:** Phase 2 (extraction script normalizes all names)

---

### Pitfall 10: Missing Token Documentation

**What goes wrong:** Tokens without `$description` leave teams guessing at proper usage.

**Why it happens:** SCSS variables rarely have comments, extraction doesn't add descriptions.

**Consequences:**
- "Lack of documentation confuses teams about proper token usage" ([Common Mistakes](https://designtokens.substack.com/p/common-mistakes-in-design-tokens))
- Duplicate tokens created because existing ones aren't discoverable
- Misuse of tokens for unintended purposes

**Prevention:**
```json
{
  "color-action-primary": {
    "$type": "color",
    "$value": "#0066cc",
    "$description": "Primary interactive color for buttons, links, and CTAs. Meets WCAG AA on white backgrounds."
  }
}
```

**Detection:**
- Count tokens without `$description` property
- User research: do designers know when to use each token?

**Phase mapping:**
- Phase 2: Extract with placeholder descriptions
- Phase 3: Designer reviews and writes real descriptions
- Phase 4: Documentation site generation

---

### Pitfall 11: Token Studio Sync Configuration Errors

**What goes wrong:** Leading slashes in file paths, expired PATs, or missing permissions prevent Token Studio from syncing.

**Why it happens:** Token Studio requires specific path formats and GitHub token configurations.

**Consequences:**
- "Error syncing with Provider" message
- Buttons grayed out (read-only mode)
- Push failures after previous successful syncs
- Developers can't contribute because branch protection blocks main

**Prevention:**
```
// WRONG file paths
"/Themes"
"/tokens/colors.json"

// CORRECT file paths
"Themes"
"tokens/colors.json"

// Required PAT scopes
✓ repo (or public_repo for public repos)
✓ Read & Write access
✓ Not expired

// Workflow
✓ Feature branch strategy (not direct to main)
✓ Pull request workflow for protected branches
```

**Detection:**
- Sync errors in Token Studio UI
- Grayed-out push/pull buttons
- 403/404 errors in browser console

**Phase mapping:**
- Phase 0: Set up GitHub integration correctly before extraction
- Phase 4: Document Token Studio setup for team members

**Source confidence:** HIGH - [Token Studio Troubleshooting](https://docs.tokens.studio/token-storage/troubleshooting-common-sync-provider-errors)

---

### Pitfall 12: Schema Validation Failure (Malformed JSON)

**What goes wrong:** Syntax errors in generated JSON (missing commas, mismatched brackets) prevent import.

**Why it happens:**
- Manual edits introduce errors
- Generation script has bugs
- Tokens placed at root level instead of nested in groups

**Consequences:**
- "Contents Don't Pass Schema Validation" error
- Token Studio refuses to import
- Build fails

**Prevention:**
- Use JSON schema validation in IDE
- Run `jq` or JSON validator before committing
- Never manually edit generated JSON (edit source, regenerate)
- Ensure tokens nest within group objects, not at root

**Detection:**
```bash
# Validate JSON syntax
jq empty tokens.json

# Validate against DTCG schema
npx @nclsndr/w3c-design-tokens-parser tokens.json
```

**Phase mapping:**
- Phase 2: Add JSON validation to extraction script
- Phase 3: Pre-commit hook validates JSON
- Phase 4: CI/CD fails on invalid JSON

---

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Mitigation |
|-------------|---------------|------------|
| **Phase 1: SCSS Audit** | Missing computed values and functions | Document all `@function`, `@mixin`, calculated values. Categorize as extractable vs manual. |
| **Phase 1: Format Selection** | Choosing legacy format by accident | Explicitly use W3C DTCG format with `$type`, `$value` from start. Don't use Style Dictionary v3 legacy format. |
| **Phase 2: Initial Extraction** | Over-extraction (500+ tokens) | Extract only tier-1 primitives. Use inclusion list, not "extract everything". |
| **Phase 2: SCSS→JSON Conversion** | CSS custom property interpolation missing | Ensure script adds `#{...}` around all SCSS variables assigned to `--custom-properties`. |
| **Phase 2: Naming Transformation** | Reserved characters in names | Validate names against Token Studio constraints. Strip forbidden characters. |
| **Phase 3: Token Studio Import** | File path with leading slash | Remove leading `/` from Token Storage Location field. Use relative paths. |
| **Phase 3: Token Studio Import** | Expired GitHub PAT | Generate new PAT with repo scope and write access before import. |
| **Phase 3: Semantic Layer** | Under-extraction (no aliases) | Add semantic tokens referencing primitives. Don't skip this layer. |
| **Phase 4: Component Tokens** | Component-coupled naming | Use functional/intent-based names. Avoid `button-*` in favor of `action-*` or `interactive-*`. |
| **Phase 4: Reference Setup** | Broken references after filtering | Use `outputReferencesFilter` utility. Test that all `{refs}` resolve. |
| **Phase 5: Documentation** | Missing `$description` | Require descriptions for all public tokens. Block PRs without descriptions. |
| **Phase 5: Validation** | No automated schema validation | Add validators to CI/CD. Use DTCG validator and Token Studio import test. |

---

## Detection Strategies Summary

### Early Warning Signs (detect in Phase 1-2)

1. **SCSS contains `@function` or `@mixin` with design values** → Can't extract without compilation
2. **SCSS variables assigned to CSS custom properties without `#{}`** → Will output literal variable names
3. **Variable names contain `/`, `$`, `{}`, `[]`, spaces** → Token Studio will reject
4. **More than 200 variables in SCSS** → Risk of over-extraction
5. **No semantic naming layer in SCSS** → Risk of under-extraction

### Build-Time Detection (Phase 2-3)

1. **JSON syntax errors** → Run `jq empty tokens.json` in extraction script
2. **Missing `$type` or wrong types** → Validate against DTCG schema
3. **Broken references** → Style Dictionary warnings about filtered references
4. **Case sensitivity collisions** → Check for duplicate names after case normalization

### Import-Time Detection (Phase 3-4)

1. **Token Studio sync errors** → Check PAT expiration, file path format, permissions
2. **Schema validation failures** → Validate JSON structure before import
3. **Type mismatch errors** → Ensure `$type` values match DTCG spec, not legacy

### Runtime Detection (Phase 4-5)

1. **CSS custom properties undefined** → Generated CSS references non-existent variables
2. **Component coupling** → Same color value repeated across multiple component-specific tokens
3. **Missing documentation** → Designers ask "Which token should I use?" frequently

---

## Confidence Assessment

| Pitfall Area | Sources | Confidence |
|--------------|---------|------------|
| SCSS interpolation | Official Sass docs | HIGH |
| DTCG format | W3C spec (v1 stable, Oct 2025) | HIGH |
| Token Studio import | Official troubleshooting docs | HIGH |
| Reserved characters | Token Studio technical specs | HIGH |
| Broken references | Style Dictionary docs | HIGH |
| Over/under extraction | Multiple design system articles | MEDIUM |
| Component coupling | Design token best practices | HIGH |
| SCSS functions/mixins | Sass docs + community | MEDIUM |

---

## Sources

### Official Documentation (HIGH confidence)
- [Sass: CSS Variable Syntax Breaking Change](https://sass-lang.com/documentation/breaking-changes/css-vars/)
- [W3C Design Tokens Specification v1 (October 2025)](https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/)
- [Token Studio: Troubleshooting Common Sync Provider Errors](https://docs.tokens.studio/token-storage/troubleshooting-common-sync-provider-errors)
- [Token Studio: Token Name Technical Specs](https://docs.tokens.studio/manage-tokens/token-names/technical-specs)
- [Style Dictionary: DTCG Format](https://styledictionary.com/info/dtcg/)
- [Style Dictionary: References](https://styledictionary.com/reference/utils/references/)
- [Design Token Validator](https://designtoken-validator.sotec-solutions.com/)

### Best Practices & Community (MEDIUM-HIGH confidence)
- [Common Mistakes in Design Tokens Adoption](https://designtokens.substack.com/p/common-mistakes-in-design-tokens)
- [Best Practices For Naming Design Tokens - Smashing Magazine (2024)](https://www.smashingmagazine.com/2024/05/naming-best-practices/)
- [Design Token Naming Best Practices - Netguru (November 2025)](https://www.netguru.com/blog/design-token-naming-best-practices)
- [Naming Tokens in Design Systems - Nathan Curtis](https://medium.com/eightshapes-llc/naming-tokens-in-design-systems-9e86c7444676)
- [The Design System Guide - Design Tokens](https://thedesignsystem.guide/design-tokens)
- [Design Tokens with Confidence - UX Collective (January 2026)](https://uxdesign.cc/design-tokens-with-confidence-862119eb819b)

### Technical References (MEDIUM confidence)
- [GitHub: w3c-design-tokens-standard-schema](https://github.com/universse/w3c-design-tokens-standard-schema)
- [NPM: @nclsndr/w3c-design-tokens-parser](https://www.npmjs.com/package/@nclsndr/w3c-design-tokens-parser)
- [Sass: Interpolation](https://sass-lang.com/documentation/interpolation/)
- [Sass: @function](https://sass-lang.com/documentation/at-rules/function/)
- [Sass: @mixin](https://sass-lang.com/documentation/at-rules/mixin/)

---

## Usage Notes for Roadmap Planning

**This document should inform:**
1. **Phase structure** - Each phase should address specific pitfalls
2. **Validation gates** - Don't proceed to next phase until pitfalls are mitigated
3. **Tooling decisions** - Choose tools that prevent common pitfalls
4. **Team training** - Focus training on critical pitfalls

**Red flags requiring deeper research:**
- If SCSS contains extensive computed values (functions/mixins), Phase 1 research must evaluate compile-first vs manual decomposition approaches
- If token count exceeds 300, Phase 2 needs editorial review strategy
- If existing SCSS uses non-standard naming, Phase 2 needs name transformation specification

**Safe to proceed if:**
- SCSS is primarily static variables (few functions/mixins)
- Naming follows kebab-case or snake_case consistently
- Bootstrap version is 5.x (well-documented variable structure)
- Team commits to three-tier token architecture from start
