# Architecture Research: Component-Level Design Tokens

**Domain:** Design Token System - Component Token Layer Integration
**Researched:** 2026-02-10
**Confidence:** HIGH

## Standard Architecture

### Three-Tier Token Hierarchy

The industry-standard design token architecture uses three layers of abstraction: Core (primitive) → Semantic (theme) → Component (specific). This project already has the foundation (Core + Semantic) from v1.0; v2.0 adds the Component layer.

```
┌─────────────────────────────────────────────────────────────┐
│                     Component Layer (NEW)                    │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐    │
│  │    Button     │  │     Input     │  │   Checkbox    │    │
│  │  Tokens       │  │   Tokens      │  │   Tokens      │    │
│  │  (variants +  │  │  (states +    │  │  (states +    │    │
│  │   states)     │  │   variants)   │  │   variants)   │    │
│  └───────┬───────┘  └───────┬───────┘  └───────┬───────┘    │
│          │                  │                  │             │
├──────────┴──────────────────┴──────────────────┴─────────────┤
│                    Semantic Layer (v1.0)                      │
│  ┌─────────────────────────────────────────────────────┐     │
│  │  color.primary, color.action.primary, spacing.md,   │     │
│  │  font-weight.normal, radius.md, shadow.sm           │     │
│  └────────────────────────┬────────────────────────────┘     │
│                           │                                   │
├───────────────────────────┴───────────────────────────────────┤
│                      Core Layer (v1.0)                        │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  ff.color.indigo-100, ff.spacing.100, ff.radius.*,  │    │
│  │  ff.shadow.*, ff.font-weight.*, ff.duration.*       │    │
│  └──────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### Token Layer Responsibilities

| Layer | Responsibility | Typical Values | Reference Pattern |
|-------|----------------|----------------|-------------------|
| **Core** (v1.0) | Raw CSS values, no semantic meaning | `#3248f4`, `1rem`, `0.15s` | No references - direct values only |
| **Semantic** (v1.0) | Context and usage meaning | `{ff.color.indigo-100}` | References Core tokens |
| **Component** (v2.0) | Component-specific design decisions | `{color.primary}`, `{radius.md}` | References Semantic OR Core tokens |

**Critical constraint:** Component tokens SHOULD reference Semantic tokens when possible, but CAN reference Core tokens directly when no semantic equivalent exists. This provides flexibility for component-specific needs while maintaining the semantic layer for global changes.

## Recommended Project Structure

### File Organization

```
tokens/
├── core.json                    # Core tokens (v1.0 - EXISTING)
├── semantic.json                # Semantic tokens (v1.0 - EXISTING)
├── component/                   # Component tokens (v2.0 - NEW)
│   ├── button.json              # Button variants + states
│   └── forms.json               # All form elements
├── dist/                        # Build outputs
│   ├── core-tokens.css          # Core CSS vars (v1.0 - EXISTING)
│   ├── semantic-tokens.css      # Semantic CSS vars (v1.0 - EXISTING)
│   ├── component-tokens.css     # Component CSS vars (v2.0 - NEW)
│   └── tokens-figma.json        # Merged file for Token Studio (MODIFIED)
└── scripts/                     # Build tooling
    └── merge-tokens.js          # Token Studio merger (MODIFIED)

forms-flow-theme/
├── config/
│   └── style-dictionary.config.js   # Build config (MODIFIED)
├── scss/
│   ├── v8-scss/
│   │   └── _button.scss             # Button implementation (CONSUMES tokens)
│   └── _forms.scss                  # Form implementation (CONSUMES tokens)
└── package.json                      # Build scripts (MODIFIED)
```

### Structure Rationale

**tokens/component/ directory (NEW):**
- **Why separate directory:** Component tokens are logically distinct from core/semantic layers
- **Why split files:** `button.json` vs `forms.json` keeps related tokens together, easier to maintain
- **Why flat (not nested):** Token Studio free tier limitation - can't resolve cross-file references, so merged file approach requires flat structure for simplicity

**Modified files:**
- **style-dictionary.config.js:** Add component token build configuration (third build target)
- **merge-tokens.js:** Include component tokens in merged Figma output
- **tokens-figma.json:** Now merges three layers instead of two

**Why this organization:**
- Maintains v1.0 file locations (no breaking changes)
- Component tokens clearly separated (easy to identify what's new)
- Build outputs parallel the source structure (predictable)
- Token Studio constraints satisfied (merge strategy works with free tier)

## Component Token Architecture

### Pattern 1: CSS Property-Based Naming

**What:** Token names map directly to CSS properties they control, organized by component → variant → element → property → state.

**Structure:** `{component}.{variant}.{element}.{property}.{state}`

**Examples:**
```json
{
  "button": {
    "primary": {
      "background": {
        "$type": "color",
        "default": {
          "$value": "{color.background.default}",
          "$description": "Primary button background - default state"
        },
        "hover": {
          "$value": "{color.action.primary}",
          "$description": "Primary button background - hover state"
        },
        "active": {
          "$value": "{color.action.primary}",
          "$description": "Primary button background - active state"
        },
        "disabled": {
          "$value": "{ff.color.white-100}",
          "$description": "Primary button background - disabled state"
        }
      },
      "border-color": {
        "$type": "color",
        "default": {
          "$value": "{ff.color.indigo-100}",
          "$description": "Primary button border - default state"
        },
        "hover": {
          "$value": "{ff.color.indigo-200}",
          "$description": "Primary button border - hover state"
        }
      },
      "text-color": {
        "$type": "color",
        "default": {
          "$value": "{ff.color.black}",
          "$description": "Primary button text - default state"
        }
      }
    },
    "secondary": {
      "background": {
        "$type": "color",
        "default": { "$value": "{color.background.default}" },
        "hover": { "$value": "{ff.color.white}" }
      }
    }
  }
}
```

**When to use:** For components with clear state-based variations (buttons, inputs, checkboxes). Maps directly to CSS custom properties in SCSS.

**Trade-offs:**
- **Pro:** Direct mapping to CSS properties makes implementation obvious
- **Pro:** State variations explicit and discoverable
- **Pro:** Easy to audit completeness (missing hover state is obvious)
- **Con:** More verbose than flat naming
- **Con:** Nested structure increases token count

### Pattern 2: Composite Property Grouping

**What:** Related CSS properties grouped under a single token for complex properties like shadows, borders, typography.

**Structure:** Use W3C DTCG composite types (`shadow`, `border`, `typography`) where multiple CSS properties form a cohesive unit.

**Examples:**
```json
{
  "button": {
    "shadow": {
      "$type": "shadow",
      "primary": {
        "$value": "{ff.shadow.button-shadow-primary}",
        "$description": "Shadow for primary button hover state"
      },
      "secondary": {
        "$value": "{ff.shadow.button-shadow-secondary}",
        "$description": "Shadow for secondary button hover state"
      }
    },
    "border": {
      "$type": "dimension",
      "width": {
        "$value": "1px",
        "$description": "Border width for all button variants"
      }
    },
    "radius": {
      "$type": "dimension",
      "$value": "{ff.radius.button-border-radius}",
      "$description": "Border radius for all button variants"
    }
  }
}
```

**When to use:** For properties that are always used together (shadow values, border shorthand). Reduces token count by treating related properties as a unit.

**Trade-offs:**
- **Pro:** Fewer tokens to manage
- **Pro:** Enforces consistency (shadow always has correct values)
- **Con:** Less granular control (can't change just blur value)
- **Con:** Style Dictionary composite expansion may create unexpected CSS var names

### Pattern 3: Shared Base + Variant Overrides

**What:** Define common properties once at component level, variants only override what changes.

**Structure:** `{component}.{shared-property}` for base, `{component}.{variant}.{property}` for overrides.

**Examples:**
```json
{
  "button": {
    "$description": "Button component tokens",
    "padding": {
      "$type": "dimension",
      "$value": "0.6875rem 1.375rem",
      "$description": "Default padding for all button variants"
    },
    "min-width": {
      "$type": "dimension",
      "$value": "5rem",
      "$description": "Minimum width for all buttons"
    },
    "min-height": {
      "$type": "dimension",
      "$value": "2.5rem",
      "$description": "Minimum height for all buttons"
    },
    "gap": {
      "$type": "dimension",
      "$value": "{spacing.sm}",
      "$description": "Gap between button icon and text"
    },
    "transition": {
      "duration": {
        "$type": "duration",
        "$value": "{ff.duration.button-transition-duration}",
        "$description": "Transition duration for all button states"
      },
      "timing": {
        "$type": "duration",
        "$value": "{ff.duration.button-transition-timing}",
        "$description": "Transition timing function"
      }
    },
    "primary": {
      "$description": "Primary button variant overrides"
    },
    "secondary": {
      "$description": "Secondary button variant overrides"
    }
  }
}
```

**When to use:** When most properties are shared across variants (sizing, spacing, transitions) and only color/state properties differ.

**Trade-offs:**
- **Pro:** DRY - don't repeat shared values
- **Pro:** Clearer what differs between variants
- **Pro:** Easier to change global button properties
- **Con:** Two lookup locations (base + variant)
- **Con:** Requires documentation about inheritance model

### Pattern 4: State Matrix for Interactive Elements

**What:** Systematic state coverage for interactive components using a consistent state vocabulary.

**State vocabulary:** `default`, `hover`, `active`, `focus`, `disabled`, `selected`, `loading`, `error`

**Structure:** Every interactive property needs state definitions where applicable.

**Examples:**
```json
{
  "button": {
    "primary": {
      "background": {
        "$type": "color",
        "default": { "$value": "{color.background.default}" },
        "hover": { "$value": "{ff.color.white}" },
        "active": { "$value": "{ff.color.white}" },
        "disabled": { "$value": "{ff.color.white-100}" }
      },
      "border-color": {
        "$type": "color",
        "default": { "$value": "{ff.color.indigo-100}" },
        "hover": { "$value": "{ff.color.indigo-200}" },
        "focus": { "$value": "{color.primary}" },
        "disabled": { "$value": "{ff.color.gray-medium}" }
      },
      "box-shadow": {
        "$type": "shadow",
        "default": { "$value": "none" },
        "hover": { "$value": "{ff.shadow.button-shadow-primary}" }
      }
    }
  }
}
```

**When to use:** For all interactive components (buttons, inputs, checkboxes, radios, selects). Ensures comprehensive state coverage.

**Trade-offs:**
- **Pro:** No missing states (explicit > implicit)
- **Pro:** Consistent state naming across components
- **Pro:** Easier to review for accessibility (disabled state always defined)
- **Con:** Verbose - every property × states = many tokens
- **Con:** Some states may not apply (not all properties change on focus)

**Best practice:** Define states only where they differ. If `active` = `default`, omit `active` and document that it falls back to default.

## Data Flow

### Token Build Pipeline (v2.0)

```
┌──────────────────────────────────────────────────────────────┐
│                   Source: JSON Files (Git)                    │
├──────────────────────────────────────────────────────────────┤
│  tokens/core.json (v1.0)                                      │
│  tokens/semantic.json (v1.0)                                  │
│  tokens/component/button.json (v2.0 - NEW)                    │
│  tokens/component/forms.json (v2.0 - NEW)                     │
└────────┬─────────────────────────────────────────────────────┘
         │
         ├─────────────────────────────────────────────────────┐
         │                                                      │
         ▼                                                      ▼
┌────────────────────────┐                    ┌────────────────────────┐
│  Style Dictionary      │                    │  Token Studio Merge    │
│  (forms-flow-theme/)   │                    │  (tokens/scripts/)     │
├────────────────────────┤                    ├────────────────────────┤
│  Build 1: Core         │                    │  Merge all JSON files  │
│    Input: core.json    │                    │  into single Figma     │
│    Output: core.css    │                    │  format with Token     │
│                        │                    │  Studio metadata       │
│  Build 2: Semantic     │                    └────────┬───────────────┘
│    Input: core.json +  │                             │
│            semantic.json│                            ▼
│    Output: semantic.css│               ┌──────────────────────────┐
│                        │               │  tokens/dist/            │
│  Build 3: Component    │               │  tokens-figma.json       │
│    Input: core.json +  │               │  (MODIFIED - 3 layers)   │
│            semantic.json│               └────────┬─────────────────┘
│            component/*  │                        │
│    Output: component.css│                        ▼
└────────┬───────────────┘               ┌──────────────────────────┐
         │                               │  Token Studio Plugin     │
         ▼                               │  (Figma import)          │
┌──────────────────────────┐             └──────────────────────────┘
│  tokens/dist/            │
│  core-tokens.css         │
│  semantic-tokens.css     │
│  component-tokens.css    │
│  (NEW)                   │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│  SCSS Implementation     │
│  (forms-flow-theme/scss/)│
│  - Uses CSS vars         │
│  - Consumes tokens       │
└──────────────────────────┘
```

### Style Dictionary Configuration Changes

**Existing configuration (v1.0):**
```javascript
// Two separate builds with filtering
buildTokens('../../tokens/core.json', 'core-tokens.css');
buildTokens('../../tokens/semantic.json', 'semantic-tokens.css');
```

**New configuration (v2.0):**
```javascript
// Add third build with multi-source input
buildTokens('../../tokens/component/button.json', 'component-tokens.css');
// OR combine all component files in one build:
buildTokens([
  '../../tokens/component/button.json',
  '../../tokens/component/forms.json'
], 'component-tokens.css');
```

**Source resolution strategy:**
1. Component build includes all three layers as sources (for reference resolution)
2. Filter output to only component tokens (exclude core/semantic from output)
3. Use `outputReferences: true` to emit `var(--ff-color-primary)` instead of resolved values

**Key configuration addition:**
```javascript
// Component tokens build - include all layers for reference resolution
const isComponentBuild = sourcePath.includes('component');
const sources = isComponentBuild
  ? [
      resolve(__dirname, '../../tokens/core.json'),
      resolve(__dirname, '../../tokens/semantic.json'),
      ...componentSourcePaths  // All component/*.json files
    ]
  : // ... existing core/semantic logic

// Filter to only output component tokens (not core/semantic)
filter: isComponentBuild
  ? (token) => {
      return token.filePath && token.filePath.includes('component/');
    }
  : // ... existing filters
```

### Token Reference Chain

**How references resolve across layers:**

```
Component Token: button.primary.background.hover
    ↓ references
Semantic Token: color.action.primary = "{ff.color.indigo-100}"
    ↓ references
Core Token: ff.color.indigo-100 = "#3248f4"
    ↓ builds to
CSS Output: --ff-button-primary-background-hover: var(--ff-color-action-primary);
            --ff-color-action-primary: var(--ff-color-indigo-100);
            --ff-color-indigo-100: #3248f4;
```

**Benefits of this chain:**
1. Change semantic token → all components update
2. Change core token → semantic + components update
3. CSS cascade allows runtime overrides at any level

**Critical requirement:** Style Dictionary must include ALL layers as sources when building component tokens, otherwise reference resolution fails (dangling references in output).

## Token Studio Integration

### Free Tier Constraint: No Cross-File References

**Problem:** Token Studio free tier cannot resolve references across separate JSON files. References only work within the same file.

**Failing pattern (multi-file):**
```
// tokens/semantic.json
{ "color": { "primary": { "$value": "{ff.color.indigo-100}" } } }

// tokens/component/button.json
{ "button": { "background": { "$value": "{color.primary}" } } }
// ❌ Token Studio can't resolve {color.primary} - it's in different file
```

**Working pattern (merged file):**
```
// tokens/dist/tokens-figma.json (merged by script)
{
  "$themes": [],
  "$metadata": { "tokenSetOrder": ["global"] },
  "global": {
    "ff": { "color": { "indigo-100": { "$value": "#3248f4" } } },
    "color": { "primary": { "$value": "{ff.color.indigo-100}" } },
    "button": { "background": { "$value": "{color.primary}" } }
  }
}
// ✅ All tokens in same file - references resolve
```

### Merge Script Strategy (v2.0 Update)

**Existing v1.0 merge script:**
- Merges `core.json` + `semantic.json` into `tokens-figma.json`
- Wraps in Token Studio format with `$themes` and `$metadata`

**v2.0 update:**
- **Add component token sources:** Include `component/*.json` files
- **Preserve token paths:** Use deep merge to maintain structure
- **Single "global" token set:** All three layers in one set (free tier limitation)

**Merge script pseudocode:**
```javascript
// tokens/scripts/merge-tokens.js (MODIFIED)
const core = JSON.parse(fs.readFileSync('tokens/core.json'));
const semantic = JSON.parse(fs.readFileSync('tokens/semantic.json'));
const button = JSON.parse(fs.readFileSync('tokens/component/button.json'));  // NEW
const forms = JSON.parse(fs.readFileSync('tokens/component/forms.json'));    // NEW

const merged = {
  "$themes": [],
  "$metadata": { "tokenSetOrder": ["global"] },
  "global": deepMerge(core, semantic, button, forms)  // Merge all layers
};

fs.writeFileSync('tokens/dist/tokens-figma.json', JSON.stringify(merged, null, 2));
```

**Token Studio import:**
1. Open Token Studio plugin in Figma
2. Load `tokens/dist/tokens-figma.json`
3. All tokens appear in single "global" set
4. References resolve within the merged file

**Trade-off:** Can't use Token Studio "Themes" feature (requires Pro) or organize tokens into multiple sets. All tokens live in one flat "global" set, organized by nested groups.

### Figma Variable Mapping

**Component tokens → Figma Variables:**

Token Studio can export component tokens to Figma Variables, but with free tier constraints:

**What works:**
- Primitive tokens → Figma Styles (colors, text styles)
- Semantic tokens → Figma Variables (can reference Styles)
- Component tokens → Figma Variables (can reference Semantic variables)

**What doesn't work (free tier):**
- Multiple Variable Collections (requires Pro)
- Modes within Collections (requires Pro)
- Cross-file references during import

**Recommended workflow:**
1. Import merged `tokens-figma.json` into Token Studio
2. Export from Token Studio to Figma Variables/Styles
3. Designers use Variables in components
4. Changes sync back to JSON → rebuild CSS

**Design/dev sync point:** Token Studio is the single source of truth. Designers should NOT manually edit Figma Variables - changes must go through JSON → Token Studio → Figma workflow.

## Integration with Existing v1.0 Architecture

### What Changes (Modified Files)

| File | Change Type | Why |
|------|-------------|-----|
| `style-dictionary.config.js` | **MODIFIED** | Add component token build configuration (third build target) |
| `tokens/scripts/merge-tokens.js` | **MODIFIED** | Include component tokens in Figma merged file |
| `forms-flow-theme/package.json` | **MODIFIED** | Add `build:component-tokens` script to build process |
| `tokens/dist/tokens-figma.json` | **MODIFIED** | Now merges three layers instead of two |

### What's New (New Files)

| File | Purpose |
|------|---------|
| `tokens/component/button.json` | Button component tokens (variants + states) |
| `tokens/component/forms.json` | Form element tokens (inputs, checkboxes, radios, selects, etc.) |
| `tokens/dist/component-tokens.css` | Generated CSS custom properties for components |

### What Stays the Same (Unchanged)

| File | Status |
|------|--------|
| `tokens/core.json` | **UNCHANGED** - Core tokens remain stable |
| `tokens/semantic.json` | **UNCHANGED** - Semantic tokens remain stable |
| `tokens/dist/core-tokens.css` | **UNCHANGED** - Core CSS output unchanged |
| `tokens/dist/semantic-tokens.css` | **UNCHANGED** - Semantic CSS output unchanged |
| SCSS implementation files | **CONSUMES** new component tokens via CSS vars |

### Build Order and Dependencies

**Critical: Build order matters for reference resolution.**

```
Step 1: Extract component tokens from SCSS
        (Manual process - identify patterns)

Step 2: Write component JSON files
        (tokens/component/button.json, forms.json)

Step 3: Update Style Dictionary config
        (Add component build target)

Step 4: Run Style Dictionary build
        npm run build:tokens
        (Builds all three layers: core → semantic → component)

Step 5: Update merge script
        (Include component tokens)

Step 6: Run merge script
        npm run merge:figma
        (Creates tokens-figma.json with all layers)

Step 7: Import to Figma
        (Token Studio plugin import)
```

**Build script integration (package.json):**
```json
{
  "scripts": {
    "build:tokens": "npm run build:core && npm run build:semantic && npm run build:component",
    "build:core": "node config/style-dictionary.config.js ../../tokens/core.json core-tokens.css",
    "build:semantic": "node config/style-dictionary.config.js ../../tokens/semantic.json semantic-tokens.css",
    "build:component": "node config/style-dictionary.config.js ../../tokens/component/button.json component-tokens.css",
    "merge:figma": "node ../tokens/scripts/merge-tokens.js"
  }
}
```

### SCSS Consumption Pattern

**Before (v1.0) - Direct CSS var usage:**
```scss
// scss/v8-scss/_button.scss
.custom-button--primary {
  background-color: var(--white-200);
  border-color: var(--primary-dark);
  color: var(--gray-darkest);

  &:hover {
    border-color: var(--primary-dark);
    background-color: var(--white-300);
  }
}
```

**After (v2.0) - Component token usage:**
```scss
// scss/v8-scss/_button.scss
.custom-button--primary {
  background-color: var(--ff-button-primary-background-default);
  border-color: var(--ff-button-primary-border-color-default);
  color: var(--ff-button-primary-text-color-default);

  &:hover {
    border-color: var(--ff-button-primary-border-color-hover);
    background-color: var(--ff-button-primary-background-hover);
  }
}
```

**Benefits:**
- Self-documenting - var name indicates component, variant, property, state
- Centralized - change token → all instances update
- Themeable - override component tokens for variants
- Figma-synced - designers see same token names

## Anti-Patterns

### Anti-Pattern 1: Duplicating Core/Semantic Values in Component Tokens

**What people do:** Copy raw values from core/semantic to component tokens instead of referencing.

```json
// ❌ WRONG - Duplicates values
{
  "button": {
    "primary": {
      "background": {
        "default": { "$value": "#3248f4" }  // Duplicates ff.color.indigo-100
      }
    }
  }
}
```

**Why it's wrong:**
- Breaks the reference chain - changing core/semantic doesn't update components
- Creates maintenance burden - must update multiple places
- Defeats purpose of token abstraction

**Do this instead:** Always reference semantic (or core if no semantic exists).

```json
// ✅ CORRECT - References semantic
{
  "button": {
    "primary": {
      "background": {
        "default": {
          "$value": "{color.action.primary}",
          "$description": "References semantic token for consistency"
        }
      }
    }
  }
}
```

### Anti-Pattern 2: Inconsistent State Naming

**What people do:** Use different state names across components (hover/hovered/hovering, disabled/inactive).

```json
// ❌ WRONG - Inconsistent states
{
  "button": { "primary": { "background": { "hover": "..." } } },
  "input": { "background": { "hovering": "..." } },
  "checkbox": { "border": { "hovered": "..." } }
}
```

**Why it's wrong:**
- Developers can't remember which state name to use
- Search/replace fails (can't find all hover states)
- Token Studio grouping breaks (expects consistent naming)

**Do this instead:** Use standard state vocabulary across all components.

```json
// ✅ CORRECT - Consistent state vocabulary
// Standard states: default, hover, active, focus, disabled, selected, loading, error
{
  "button": { "primary": { "background": { "hover": "..." } } },
  "input": { "background": { "hover": "..." } },
  "checkbox": { "border": { "hover": "..." } }
}
```

### Anti-Pattern 3: Over-Tokenizing Shared Properties

**What people do:** Create separate component tokens for properties that are identical across all variants.

```json
// ❌ WRONG - Redundant tokens
{
  "button": {
    "primary": { "border-width": { "$value": "1px" } },
    "secondary": { "border-width": { "$value": "1px" } },
    "error": { "border-width": { "$value": "1px" } }
  }
}
```

**Why it's wrong:**
- Token explosion - more tokens to maintain
- Harder to change globally (must update 3 tokens)
- Obscures what actually differs between variants

**Do this instead:** Use shared base property, variants override only what changes.

```json
// ✅ CORRECT - Shared base property
{
  "button": {
    "border-width": {
      "$type": "dimension",
      "$value": "1px",
      "$description": "Border width for all button variants"
    },
    "primary": { /* only color properties that differ */ },
    "secondary": { /* only color properties that differ */ }
  }
}
```

### Anti-Pattern 4: Skipping Style Dictionary Source Inclusion

**What people do:** Build component tokens without including core/semantic as sources.

```javascript
// ❌ WRONG - Component build missing sources
const sd = new StyleDictionary({
  source: ['tokens/component/button.json'],  // Missing core + semantic!
  // ... config
});
```

**Why it's wrong:**
- Reference resolution fails - `{color.primary}` can't be found
- Style Dictionary outputs raw reference strings instead of resolved values
- CSS custom properties break - `--button-bg: {color.primary}` (invalid CSS)

**Do this instead:** Always include all upstream layers as sources.

```javascript
// ✅ CORRECT - Include all layers for reference resolution
const sd = new StyleDictionary({
  source: [
    'tokens/core.json',        // Layer 1
    'tokens/semantic.json',    // Layer 2
    'tokens/component/button.json'  // Layer 3
  ],
  // Filter output to only component tokens
  files: [{
    filter: (token) => token.filePath.includes('component/')
  }]
});
```

### Anti-Pattern 5: Flat Component Token Structure

**What people do:** Use flat naming without grouping (all tokens at same level).

```json
// ❌ WRONG - Flat structure, hard to navigate
{
  "button-primary-background-default": { "$value": "..." },
  "button-primary-background-hover": { "$value": "..." },
  "button-primary-border-default": { "$value": "..." },
  "button-secondary-background-default": { "$value": "..." }
}
```

**Why it's wrong:**
- No visual grouping in Token Studio (can't collapse button.primary)
- Harder to find related tokens (must scan entire list)
- Can't set $type at group level (must repeat on every token)

**Do this instead:** Use nested structure for logical grouping.

```json
// ✅ CORRECT - Nested structure for grouping
{
  "button": {
    "primary": {
      "background": {
        "$type": "color",
        "default": { "$value": "..." },
        "hover": { "$value": "..." }
      },
      "border-color": {
        "$type": "color",
        "default": { "$value": "..." }
      }
    },
    "secondary": {
      "background": {
        "$type": "color",
        "default": { "$value": "..." }
      }
    }
  }
}
```

## Scaling Considerations

| Scale | Architecture Approach |
|-------|------------------------|
| **2 components (v2.0)** | Single `component-tokens.css` file. Two JSON files (`button.json`, `forms.json`). Merged into one Figma file. Build time negligible. |
| **5-10 components** | Single `component-tokens.css` still works. Consider splitting CSS output by component if file gets large (>1000 lines). Still merge into single Figma file (free tier constraint). |
| **20+ components** | Split CSS output per component (`button-tokens.css`, `forms-tokens.css`, etc.). Consider Token Studio Pro for multi-file sync (avoid merge script complexity). Build time starts mattering - use caching. |

### Scaling Priorities

**First bottleneck: Token Studio merge file size**
- **Symptom:** Figma import slow, Token Studio plugin laggy
- **Threshold:** ~500+ tokens in merged file
- **Solution:** Upgrade to Token Studio Pro for multi-file sync, eliminate merge step

**Second bottleneck: Style Dictionary build time**
- **Symptom:** `npm run build:tokens` takes >5 seconds
- **Threshold:** 10+ component JSON files
- **Solution:** Implement incremental builds (only rebuild changed files), use Style Dictionary caching

**For v2.0 scope (buttons + forms):** No scaling issues. 2-3 JSON files, ~100-150 component tokens, build time <1 second.

## Sources

**Design Token Architecture:**
- [Inside Design Tokens: The Three Class Token Society](https://gos.si/blog/inside-design-tokens-the-three-class-token-society) - Three-tier hierarchy (primitive, semantic, component)
- [The Pyramid Design Token Structure](https://stefaniefluin.medium.com/the-pyramid-design-token-structure-the-best-way-to-format-organize-and-name-your-design-tokens-ca81b9d8836d) - Token naming and structure
- [Design Tokens (variables) architecture in Tetrisly Design System](https://medium.com/design-bootcamp/design-tokens-variables-architecture-in-tetrisly-design-system-part-2-taxonomy-2504f959cbb1) - Taxonomy and organization

**Style Dictionary Multi-Tier Configuration:**
- [Style Dictionary: Design Tokens](https://styledictionary.com/info/tokens/) - Official token hierarchy documentation
- [How to manage your Design Tokens with Style Dictionary](https://didoo.medium.com/how-to-manage-your-design-tokens-with-style-dictionary-98c795b938aa) - Multi-file configuration
- [A Design Tokens Workflow (part 6)](https://www.alwaystwisted.com/articles/a-design-tokens-workflow-part-6) - Layering and referencing
- [Managing And Exporting Design Tokens With Style Dictionary](https://www.michaelmang.dev/blog/managing-and-exporting-design-tokens-with-style-dictionary/) - File structure patterns

**Component Token Naming:**
- [Naming Tokens in Design Systems](https://medium.com/eightshapes-llc/naming-tokens-in-design-systems-9e86c7444676) - Nathan Curtis on component token naming (EightShapes)
- [Best Practices For Naming Design Tokens, Components And Variables](https://www.smashingmagazine.com/2024/05/naming-best-practices/) - 2024 Smashing Magazine naming guide
- [Design Token Naming Best Practices](https://www.netguru.com/blog/design-token-naming-best-practices) - Netguru practical guide
- [Nord Design System: Naming](https://nordhealth.design/naming/) - Component naming conventions

**Button State Architecture:**
- [Button States Explained (2026)](https://www.designrush.com/best-designs/websites/trends/button-states) - Modern button state patterns
- [Design System Breakdown: Button](https://clipcontent.substack.com/p/design-system-breakdown-button-22-11-08) - Steve Dennis on button variants
- [Carbon Design System: Button](https://carbondesignsystem.com/components/button/usage/) - IBM Carbon button tokens

**Token Studio Integration:**
- [Token Studio: Token Sets](https://docs.tokens.studio/manage-tokens/token-sets) - Token set organization
- [Token Studio: Token Groups](https://docs.tokens.studio/manage-tokens/token-names/groups) - Grouping strategy
- [Token Studio: Multi-file Sync (pro)](https://docs.tokens.studio/token-storage/remote-multi-file-sync) - Free tier limitations

**W3C DTCG Specification:**
- [Design Tokens Community Group](https://www.designtokens.org/) - Official DTCG specification
- [Design Tokens specification reaches first stable version](https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/) - v1.0 stable (Oct 2025)
- [Style Dictionary: Design Tokens Community Group](https://styledictionary.com/info/dtcg/) - DTCG support in Style Dictionary

---
*Architecture research for: Component-Level Design Token Integration*
*Researched: 2026-02-10*
*Confidence: HIGH - Based on W3C DTCG v1.0 spec (Oct 2025), Style Dictionary v5 docs, Token Studio v2 constraints, and established design system patterns from Carbon, Nord, SAP, and Cloudscape.*
