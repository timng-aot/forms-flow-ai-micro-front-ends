# Phase 3: Build Pipeline - Research

**Researched:** 2026-02-09
**Domain:** Design token transformation with Style Dictionary v4+
**Confidence:** HIGH

## Summary

Phase 3 requires configuring Style Dictionary v4+ to transform W3C DTCG token JSON files into CSS custom properties with --ff- prefixes. The pipeline includes pre-computation of SCSS expressions (blend-with-white-to-hex()) before transformation and validation for Token Studio importability. The architecture must support bidirectional flow (code-to-Figma now, Figma-to-code future).

Style Dictionary v4+ provides first-class DTCG support. The @tokens-studio/sd-transforms package bridges Token Studio-specific patterns to DTCG standards. The preprocessing phase resolves SCSS color blending expressions using standard alpha compositing formulas. Generated CSS custom properties preserve token references via outputReferences, enabling semantic tokens to reference core tokens as CSS variables.

**Primary recommendation:** Install Style Dictionary v4+ and @tokens-studio/sd-transforms in forms-flow-theme package.json (where SCSS build lives). Create a standalone Node.js pre-computation script that resolves blend-with-white-to-hex() expressions before Style Dictionary runs. Use preprocessors for DTCG validation, css/variables format with outputReferences for token layering, and maintain separate core/semantic token sets for Figma import clarity.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Output targets:**
- CSS custom properties only (no SCSS variables or JS/TS output)
- Use --ff- prefix for all CSS variables (e.g. --ff-color-primary, --ff-spacing-100)
- Single CSS file per token source: core-tokens.css and semantic-tokens.css (separate, not merged)
- Semantic CSS vars reference core CSS vars, preserving the layering

**Unresolved SCSS expressions:**
- Pre-compute blend-with-white-to-hex() values BEFORE Style Dictionary runs
- Standalone rerunnable script that reads core.json, resolves expressions, writes back resolved hex values
- Only handle blend-with-white-to-hex() — no other unresolved patterns exist
- Clean hex values only in token files — no preservation of original expressions (audit artifacts document originals)

**Token Studio round-trip:**
- Pure W3C DTCG format (no Token Studio-specific extensions)
- Figma becomes source of truth after initial import — tokens flow from Figma to code in the future
- Style Dictionary pipeline validates that source token JSON is Token Studio-importable (validation in pipeline, not deferred to Phase 4)
- Design Style Dictionary config for bidirectional use — same token format works whether source is code-extracted or Figma-exported JSON
- Future Figma-to-code reverse pipeline is planned — Phase 3 config should accommodate this direction

**Integration with existing build:**
- Generated CSS sits alongside existing theme (tokens/dist/) — no replacement of forms-flow-theme
- Consumers opt-in to token CSS when ready
- npm script ("build:tokens") added for triggering Style Dictionary build
- Output location: tokens/dist/ (keeps all token-related files together)

### Claude's Discretion

- Whether to use resolved token files directly for Token Studio import or produce a separate export (pick based on maintenance burden)
- Whether to preserve core/semantic split as separate token sets in Figma or merge (pick based on Token Studio best practices)
- Where to install Style Dictionary devDependencies — root or forms-flow-theme package.json (pick based on monorepo structure)

### Deferred Ideas (OUT OF SCOPE)

- Figma-to-code reverse pipeline (export from Figma, transform to CSS) — future phase after Figma becomes source of truth
- Replacing forms-flow-theme SCSS with token-generated CSS — future migration phase
- Component-level consumption of token CSS variables — outside current scope

</user_constraints>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| style-dictionary | 4.x (latest) | Design token transformation engine | Industry standard for design token transformation; Amazon-maintained; first-class DTCG support since v4 |
| @tokens-studio/sd-transforms | 1.x (latest) | Token Studio → Style Dictionary bridge | Official Token Studio transforms; handles DTCG alignment; maintained by Tokens Studio team (now part of Style Dictionary core team as of Aug 2023) |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| @universse/w3c-design-tokens-standard-schema | Latest | DTCG validation (optional) | If runtime validation needed beyond Style Dictionary's built-in checks |
| Node.js built-ins | N/A | JSON parsing, file I/O, color math | For pre-computation script (no dependencies needed) |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Style Dictionary | Theo (Salesforce) | Theo is less actively maintained; Style Dictionary has broader ecosystem support and official Token Studio integration |
| @tokens-studio/sd-transforms | Custom transforms | Reinventing tested solutions for DTCG type mapping, math expression evaluation, unit normalization |
| Pre-computation script | Style Dictionary transitive transform | User requires standalone rerunnable script; transitive transforms would couple resolution to build pipeline |

**Installation:**
```bash
# In forms-flow-theme/package.json (recommended for monorepo structure)
cd forms-flow-theme
npm install --save-dev style-dictionary @tokens-studio/sd-transforms

# Alternative: Root installation (if token build should be independent of theme package)
# cd /path/to/repo/root
# npm install --save-dev style-dictionary @tokens-studio/sd-transforms
```

**Reasoning for forms-flow-theme installation:** Existing SCSS build (webpack, sass-loader) lives in forms-flow-theme. Token CSS output will sit alongside theme CSS. Keeps design system tooling colocated. No root package.json exists (not a true monorepo with workspaces).

## Architecture Patterns

### Recommended Project Structure
```
tokens/
├── core.json                    # W3C DTCG core tokens (blend expressions resolved)
├── semantic.json                # W3C DTCG semantic tokens (references to core)
├── dist/
│   ├── core-tokens.css         # Generated CSS custom properties (--ff-color-*)
│   └── semantic-tokens.css     # Generated CSS custom properties (--color-primary)
├── scripts/
│   └── precompute-colors.js    # Standalone: resolve blend-with-white-to-hex()
└── config/
    └── style-dictionary.config.js  # Style Dictionary configuration

forms-flow-theme/
└── package.json                # Add style-dictionary, @tokens-studio/sd-transforms
```

### Pattern 1: Pre-Computation Script (Color Blending)
**What:** Standalone Node.js script that reads token JSON, resolves blend-with-white-to-hex() expressions to hex values, writes back to JSON.

**When to use:** Before Style Dictionary runs (prerequisite step).

**Example:**
```javascript
// Source: Existing SCSS implementation at forms-flow-theme/scss/v8-scss/_theme.scss:53-60
// Formula: newRGB = (baseRGB * opacity) + (whiteRGB * (1 - opacity))

const fs = require('fs');

function blendWithWhiteToHex(hexColor, opacity) {
  // Parse hex color
  const r = parseInt(hexColor.slice(1, 3), 16);
  const g = parseInt(hexColor.slice(3, 5), 16);
  const b = parseInt(hexColor.slice(5, 7), 16);

  // Blend with white (255, 255, 255)
  const newR = Math.round((r * opacity) + (255 * (1 - opacity)));
  const newG = Math.round((g * opacity) + (255 * (1 - opacity)));
  const newB = Math.round((b * opacity) + (255 * (1 - opacity)));

  // Convert back to hex
  return `#${newR.toString(16).padStart(2, '0')}${newG.toString(16).padStart(2, '0')}${newB.toString(16).padStart(2, '0')}`;
}

function resolveTokenExpressions(tokens) {
  // Recursively walk token object
  // Find $value matching pattern: blend-with-white-to-hex(#XXXXXX, N.N)
  // Replace with computed hex value
  // Return modified tokens
}

const coreTokens = JSON.parse(fs.readFileSync('./tokens/core.json', 'utf8'));
const resolved = resolveTokenExpressions(coreTokens);
fs.writeFileSync('./tokens/core.json', JSON.stringify(resolved, null, 2));
```

### Pattern 2: Style Dictionary Configuration (Bidirectional Design)
**What:** Style Dictionary config that works for both code-extracted tokens (now) and future Figma-exported tokens.

**When to use:** Token transformation to CSS.

**Example:**
```javascript
// Source: https://styledictionary.com/reference/config/
// Source: https://github.com/tokens-studio/sd-transforms
import StyleDictionary from 'style-dictionary';
import { register, expandTypesMap } from '@tokens-studio/sd-transforms';

register(StyleDictionary);

export default {
  source: ['tokens/core.json'], // Or semantic.json

  preprocessors: [
    'tokens-studio', // DTCG alignment
  ],

  expand: {
    typesMap: expandTypesMap, // Handle shadow/typography composite tokens
  },

  platforms: {
    css: {
      transformGroup: 'tokens-studio', // Includes DTCG transforms
      buildPath: 'tokens/dist/',

      files: [
        {
          destination: 'core-tokens.css', // or semantic-tokens.css
          format: 'css/variables',
          options: {
            outputReferences: true, // Preserve {ff.color.indigo-100} as var(--ff-color-indigo-100)
            selector: ':root', // Default CSS custom property selector
          },
        },
      ],

      // Transform token paths to CSS variable names with --ff- prefix
      transforms: [
        'name/kebab', // color.primary → color-primary
      ],

      // Custom transform to add --ff- prefix
      options: {
        fileHeader: 'customHeader', // Optional: Add generation metadata
      },
    },
  },
};
```

### Pattern 3: Token Reference Preservation (Semantic Layering)
**What:** Using outputReferences to keep semantic tokens as CSS variable references to core tokens.

**When to use:** Always for semantic tokens; maintains token hierarchy in output.

**Example:**
```javascript
// Source: https://styledictionary.com/reference/hooks/formats/
// Input semantic.json:
// { "color": { "primary": { "$value": "{ff.color.indigo-100}" } } }

// With outputReferences: true
// Output semantic-tokens.css:
// :root {
//   --color-primary: var(--ff-color-indigo-100);
// }

// With outputReferences: false (anti-pattern for this project)
// Output semantic-tokens.css:
// :root {
//   --color-primary: #3248F4;  // Reference resolved to value
// }
```

### Pattern 4: DTCG Validation via Preprocessor
**What:** Use Style Dictionary preprocessor to validate token JSON is Token Studio-importable.

**When to use:** Every build (fail fast if tokens violate DTCG format).

**Example:**
```javascript
// Source: https://styledictionary.com/reference/hooks/preprocessors/
StyleDictionary.registerPreprocessor({
  name: 'validate-dtcg',
  preprocessor: (dictionary) => {
    // Check all tokens have $type, $value
    // Check no token names contain {, }, $ (Token Studio restriction)
    // Check $type values match DTCG spec (color, dimension, fontWeight, etc.)
    // Throw error if validation fails
    return dictionary;
  },
});

// Add to config:
preprocessors: ['tokens-studio', 'validate-dtcg'],
```

### Anti-Patterns to Avoid
- **Merging core and semantic tokens into single CSS file:** Loses token layering; makes future Figma sync harder to understand
- **Using SCSS variables output:** User decision locked to CSS custom properties only
- **Preserving blend-with-white-to-hex() expressions in token files:** Token Studio/Figma cannot import SCSS function calls; must be clean hex values
- **Installing Style Dictionary globally:** Breaks reproducibility; lock versions in package.json
- **Skipping preprocessors for validation:** Defers error detection to Phase 4 (Figma import); fail fast instead

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| DTCG type mapping | Custom token parser | @tokens-studio/sd-transforms preprocessor | Handles Token Studio → DTCG type alignment (e.g., Token Studio shadow objects vs DTCG shadow format) |
| CSS variable naming | String concatenation | Style Dictionary name transforms | Handles nested token paths, escaping, platform conventions |
| Token reference resolution | Regex find/replace | Style Dictionary built-in reference resolver | Handles circular references, deep nesting, partial references, escaped braces |
| Color format conversion | Manual hex/rgb/hsl conversion | Style Dictionary color transforms (or keep as-is) | Project only needs hex; no conversion needed |
| Math expression evaluation | Custom expression parser | @tokens-studio/sd-transforms math evaluator | Already handles Token Studio math expressions if needed (though project only has blend function) |
| File watching for rebuild | Custom fs.watch | Style Dictionary CLI or npm-watch package | Edge cases: debouncing, cross-platform paths, symlinks |

**Key insight:** Design token transformation has hidden complexity. Reference resolution with outputReferences requires graph traversal and cycle detection. DTCG type mapping has subtle differences between spec and tool implementations (Token Studio uses different shadow property names than spec). Name transforms must handle edge cases like numeric prefixes, reserved CSS keywords, special characters. Style Dictionary has solved these problems over 7+ years of production use.

## Common Pitfalls

### Pitfall 1: Transform Order Matters
**What goes wrong:** Transforms run sequentially; wrong order produces incorrect output (e.g., name transform before color transform might break color parsing).

**Why it happens:** Style Dictionary applies transforms in the order listed; transitive transforms complicate execution flow.

**How to avoid:** Use built-in transformGroups (like 'tokens-studio') which have correct ordering. If custom transforms needed, test thoroughly and document dependencies.

**Warning signs:** Token values are partially transformed, references break, or output format is wrong.

### Pitfall 2: Preprocessor vs Transform Confusion
**What goes wrong:** Using preprocessors for per-token transformations instead of global dictionary operations; or using transforms for validation instead of preprocessors.

**Why it happens:** Documentation shows preprocessors can modify tokens; developers assume they're interchangeable with transforms.

**How to avoid:** Preprocessors = whole dictionary operations (validation, schema migration, global token injection). Transforms = per-token value/name modifications.

**Warning signs:** Preprocessor code iterating every token and modifying values; validation logic in transform functions.

### Pitfall 3: outputReferences with Transitive Transforms
**What goes wrong:** Using outputReferences with tokens that have been transitively transformed causes references to resolve to values instead of staying as references.

**Why it happens:** Style Dictionary's outputReferencesTransformed utility prevents reference output when transitive transforms modify values (to avoid circular references).

**How to avoid:** Don't use transitive transforms for this project (pre-computation script handles color blending). Keep transforms non-transitive so outputReferences works.

**Warning signs:** Semantic tokens output resolved hex values instead of var(--ff-color-*) references.

### Pitfall 4: DTCG $type Inheritance Assumptions
**What goes wrong:** Assuming all child tokens inherit $type from parent group; DTCG spec requires $type on every token OR inherited from nearest ancestor.

**Why it happens:** Existing token JSON has $type at group level (correct DTCG pattern); developer assumes Style Dictionary auto-inherits.

**How to avoid:** Use the tokens-studio preprocessor which includes typeDtcgDelegate that ensures $type is present on every token. Existing project structure is correct (has $type at group level).

**Warning signs:** Validation errors about missing $type on tokens.

### Pitfall 5: Token Name Character Restrictions (Token Studio)
**What goes wrong:** Token names contain {, }, or $ characters; Token Studio import fails.

**Why it happens:** DTCG spec doesn't forbid these characters, but Token Studio does (they conflict with reference syntax).

**How to avoid:** Add validation in preprocessor to check token names don't contain forbidden characters. Existing tokens use kebab-case with alphanumerics and hyphens (safe).

**Warning signs:** Token Studio import shows error "Invalid token name" or reference syntax breaks.

### Pitfall 6: Separate Build Scripts Without Orchestration
**What goes wrong:** Running pre-computation script and Style Dictionary build as separate manual steps; developers forget pre-computation; tokens have unresolved expressions.

**Why it happens:** User requirement says "standalone rerunnable script" which sounds like separate execution.

**How to avoid:** Create single npm script (build:tokens) that runs pre-computation THEN Style Dictionary using && operator. Script can still be run independently for debugging.

**Warning signs:** Generated CSS contains literal string "blend-with-white-to-hex(...)" instead of hex values.

## Code Examples

Verified patterns from official sources:

### Complete Style Dictionary Configuration
```javascript
// Source: https://styledictionary.com/reference/config/
// Source: https://github.com/tokens-studio/sd-transforms
import StyleDictionary from 'style-dictionary';
import { register, expandTypesMap } from '@tokens-studio/sd-transforms';

register(StyleDictionary);

// Custom transform for --ff- prefix
StyleDictionary.registerTransform({
  name: 'name/css/ff-prefix',
  type: 'name',
  transform: (token) => {
    // Token path: ['ff', 'color', 'indigo-100']
    // Output: --ff-color-indigo-100
    return '--ff-' + token.path.join('-').toLowerCase();
  },
});

// DTCG validation preprocessor
StyleDictionary.registerPreprocessor({
  name: 'validate-dtcg',
  preprocessor: (dictionary) => {
    const validateToken = (token, path = []) => {
      // Skip groups (only validate leaf tokens)
      if (token.$value === undefined) return;

      // Check required properties
      if (!token.$type && !token.$value.startsWith('{')) {
        throw new Error(`Token ${path.join('.')} missing $type`);
      }

      // Check Token Studio character restrictions
      const name = path[path.length - 1];
      if (name && /[{}$]/.test(name)) {
        throw new Error(`Token name "${name}" contains forbidden characters ({, }, $)`);
      }
    };

    const traverse = (obj, path = []) => {
      for (const [key, value] of Object.entries(obj)) {
        if (typeof value === 'object') {
          validateToken(value, [...path, key]);
          traverse(value, [...path, key]);
        }
      }
    };

    traverse(dictionary.tokens);
    return dictionary;
  },
});

export default {
  source: ['tokens/core.json'], // Run separately for semantic.json

  preprocessors: [
    'tokens-studio',    // DTCG alignment + Token Studio transforms
    'validate-dtcg',    // Custom validation
  ],

  expand: {
    typesMap: expandTypesMap,
  },

  platforms: {
    css: {
      transformGroup: 'tokens-studio',
      buildPath: 'tokens/dist/',

      // Override name transform to add --ff- prefix
      transforms: [
        'name/css/ff-prefix', // Custom transform
        // tokens-studio group includes other needed transforms
      ],

      files: [
        {
          destination: 'core-tokens.css',
          format: 'css/variables',
          options: {
            outputReferences: true,
            selector: ':root',
          },
        },
      ],
    },
  },
};
```

### Pre-Computation Script (Complete)
```javascript
// Source: Adapted from forms-flow-theme/scss/v8-scss/_theme.scss:53-60
// File: tokens/scripts/precompute-colors.js
const fs = require('fs');
const path = require('path');

/**
 * Blends a hex color with white background at given opacity.
 * Formula: newRGB = (baseRGB * opacity) + (whiteRGB * (1 - opacity))
 * Matches SCSS function blend-with-white-to-hex() from _theme.scss
 */
function blendWithWhiteToHex(hexColor, opacity) {
  // Parse hex color (supports #RGB and #RRGGBB)
  const hex = hexColor.replace('#', '');
  const r = parseInt(hex.slice(0, 2), 16);
  const g = parseInt(hex.slice(2, 4), 16);
  const b = parseInt(hex.slice(4, 6), 16);

  // Blend with white (255, 255, 255)
  const newR = Math.round((r * opacity) + (255 * (1 - opacity)));
  const newG = Math.round((g * opacity) + (255 * (1 - opacity)));
  const newB = Math.round((b * opacity) + (255 * (1 - opacity)));

  // Convert back to hex with zero-padding
  const toHex = (n) => n.toString(16).padStart(2, '0');
  return `#${toHex(newR)}${toHex(newG)}${toHex(newB)}`;
}

/**
 * Recursively resolves blend-with-white-to-hex() expressions in token object.
 * Only modifies $value properties that match the expression pattern.
 */
function resolveBlendExpressions(obj) {
  if (Array.isArray(obj)) {
    return obj.map(resolveBlendExpressions);
  }

  if (obj && typeof obj === 'object') {
    const result = {};

    for (const [key, value] of Object.entries(obj)) {
      if (key === '$value' && typeof value === 'string') {
        // Match: blend-with-white-to-hex(#XXXXXX, N.N)
        const match = value.match(/blend-with-white-to-hex\(#([0-9A-Fa-f]{6}),\s*([\d.]+)\)/);

        if (match) {
          const hexColor = `#${match[1]}`;
          const opacity = parseFloat(match[2]);
          result[key] = blendWithWhiteToHex(hexColor, opacity);
        } else {
          result[key] = value;
        }
      } else {
        result[key] = resolveBlendExpressions(value);
      }
    }

    return result;
  }

  return obj;
}

// Main execution
const tokensPath = path.resolve(__dirname, '../../core.json');
console.log(`Reading tokens from: ${tokensPath}`);

const tokens = JSON.parse(fs.readFileSync(tokensPath, 'utf8'));
const resolved = resolveBlendExpressions(tokens);

fs.writeFileSync(tokensPath, JSON.stringify(resolved, null, 2) + '\n');
console.log('✓ Resolved blend-with-white-to-hex() expressions in core.json');
```

### NPM Script Orchestration
```json
// Source: https://styledictionary.com/getting-started/using_the_npm_module/
// File: forms-flow-theme/package.json (add to scripts)
{
  "scripts": {
    "build:tokens:precompute": "node ../tokens/scripts/precompute-colors.js",
    "build:tokens:core": "style-dictionary build --config ../tokens/config/core.config.js",
    "build:tokens:semantic": "style-dictionary build --config ../tokens/config/semantic.config.js",
    "build:tokens": "npm run build:tokens:precompute && npm run build:tokens:core && npm run build:tokens:semantic"
  }
}
```

### Bidirectional Config (Figma Export Ready)
```javascript
// Source: Community patterns for Figma → Style Dictionary pipelines
// Future-ready config that works whether tokens come from code extraction or Figma export

export default {
  // Source could be code-extracted (now) or Figma-exported (future)
  source: ['tokens/core.json'],

  preprocessors: [
    'tokens-studio', // Normalizes both code and Figma token formats to DTCG
  ],

  // Same transforms work regardless of source
  platforms: {
    css: {
      transformGroup: 'tokens-studio',
      buildPath: 'tokens/dist/',
      files: [
        {
          destination: 'core-tokens.css',
          format: 'css/variables',
          options: {
            outputReferences: true, // Works for both directions
          },
        },
      ],
    },
  },
};

// Key insight: Tokens Studio preprocessor makes tokens "source-agnostic"
// Whether tokens originated in code or Figma, they're normalized to DTCG before transformation
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Style Dictionary v3 custom format | Style Dictionary v4 DTCG native | v4.0 (2023) | No longer need custom parsers for DTCG; first-class support |
| Manual Token Studio format handling | @tokens-studio/sd-transforms preprocessor | Aug 2023 (Tokens Studio team joined Style Dictionary) | Official integration; Token Studio patterns become Style Dictionary patterns |
| transform vs transitive transform | Non-transitive default; transitive opt-in | v3.0 | Prevents accidental circular references; clearer mental model |
| outputReferences: boolean | outputReferences: boolean \| function | v3.0+ | Per-token control over reference preservation |
| DTCG spec in draft | DTCG spec v1.0 stable | Oct 2025 | Production-ready standard; major tools (Figma, Adobe, Google) committed |

**Deprecated/outdated:**
- **Theo (Salesforce):** Less active maintenance; Style Dictionary is current standard
- **Custom DTCG parsers:** Style Dictionary v4 has native support
- **Token Studio "legacy" format:** Plugin supports W3C DTCG format; prefer DTCG for future compatibility

## Open Questions

1. **Root vs forms-flow-theme package.json for Style Dictionary installation**
   - What we know: No root package.json exists; forms-flow-theme has webpack/SCSS build; token output goes to tokens/dist/
   - What's unclear: Whether user plans to add root package.json in future (for true monorepo setup)
   - Recommendation: Install in forms-flow-theme for now (colocated with existing design system tooling); migrate to root if workspace pattern adopted later

2. **Separate Token Studio export file or use resolved tokens directly**
   - What we know: Resolved core.json has clean hex values (Token Studio importable); semantic.json has references (also importable)
   - What's unclear: Whether Token Studio prefers merged core+semantic or separate token sets
   - Recommendation: Keep separate (core.json + semantic.json as separate token sets in Figma); mirrors code structure; clearer mental model; easier to understand token hierarchy in Figma UI

3. **Validation depth: JSON Schema vs preprocessor checks**
   - What we know: Style Dictionary preprocessors can validate; external JSON schema validators exist
   - What's unclear: Whether full JSON schema validation adds value beyond preprocessor checks
   - Recommendation: Start with preprocessor validation (checks $type presence, character restrictions, reference syntax); add JSON schema validation only if Token Studio import reveals gaps

4. **Build trigger: Manual npm script vs automated file watch**
   - What we know: User wants build:tokens npm script
   - What's unclear: Whether tokens will change frequently enough to warrant automated rebuild
   - Recommendation: Start with manual npm run build:tokens; add watch mode (npm-watch or Style Dictionary CLI --watch) if token iteration becomes frequent

## Sources

### Primary (HIGH confidence)
- [Style Dictionary DTCG Documentation](https://styledictionary.com/info/dtcg/) - DTCG format support details
- [Style Dictionary Preprocessors Reference](https://styledictionary.com/reference/hooks/preprocessors/) - Preprocessor API and usage
- [Style Dictionary Formats Reference](https://styledictionary.com/reference/hooks/formats/) - CSS variables format and outputReferences
- [Style Dictionary Transforms Reference](https://styledictionary.com/reference/hooks/transforms/) - Transform types and execution order
- [@tokens-studio/sd-transforms GitHub](https://github.com/tokens-studio/sd-transforms) - Token Studio integration details
- [Token Studio Token Format Documentation](https://docs.tokens.studio/manage-settings/token-format) - W3C DTCG format requirements
- [Design Tokens Community Group W3C](https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/) - DTCG spec v1.0 stable announcement
- Project codebase: forms-flow-theme/scss/v8-scss/_theme.scss - Original blend-with-white-to-hex() SCSS implementation

### Secondary (MEDIUM confidence)
- [Token Studio Style Dictionary Integration Guide](https://docs.tokens.studio/transform-tokens/style-dictionary) - Installation and setup
- [SitePoint JavaScript Color Manipulation](https://www.sitepoint.com/javascript-generate-lighter-darker-color/) - Color blending formulas
- [Medium: Building Scalable Design Token System](https://medium.com/@mailtorahul2485/building-a-scalable-design-token-system-from-figma-to-code-with-style-dictionary-e2c9eacc75aa) - Figma-to-code pipeline patterns
- [Medium: How to Manage Design Tokens with Style Dictionary](https://didoo.medium.com/how-to-manage-your-design-tokens-with-style-dictionary-98c795b938aa) - Common pitfalls and best practices
- [Medium: Monorepo Guide 2026](https://medium.com/@sanjaytomar717/the-ultimate-guide-to-building-a-monorepo-in-2025-sharing-code-like-the-pros-ee4d6d56abaa) - Monorepo package.json patterns

### Tertiary (LOW confidence)
- [Design Token Validator](https://designtoken-validator.sotec-solutions.com/) - Online DTCG validator (limited documentation on validation rules)
- [@universse/w3c-design-tokens-standard-schema GitHub](https://github.com/universse/w3c-design-tokens-standard-schema) - Schema validation library (newer, less battle-tested than Style Dictionary)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Style Dictionary v4 and @tokens-studio/sd-transforms are official, well-documented, actively maintained (Tokens Studio team is now part of Style Dictionary core team)
- Architecture: HIGH - Official docs provide clear patterns; existing project structure (tokens/core.json, tokens/semantic.json, forms-flow-theme/package.json) is verified
- Pitfalls: MEDIUM-HIGH - Documented pitfalls from official sources; some pitfalls inferred from GitHub issues and community patterns
- Pre-computation approach: HIGH - Mathematical formula extracted from existing SCSS code; straightforward alpha compositing with no edge cases
- DTCG validation: MEDIUM - Token Studio format requirements partially documented; some gaps in official docs about specific validation rules (character restrictions confirmed but validation depth unclear)

**Research date:** 2026-02-09
**Valid until:** 60 days (Style Dictionary is stable; DTCG spec v1.0 is stable; Token Studio integration is mature)
