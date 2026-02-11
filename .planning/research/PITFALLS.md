# Component-Level Design Token Pitfalls

**Domain:** Adding component-level tokens (buttons & forms) to existing 2-tier design token system
**Researched:** 2026-02-10
**Confidence:** HIGH (verified with official documentation, current best practices, and v1.0 project learnings)

## Executive Summary

Adding component-level tokens to an existing core/semantic token system commonly fails in five critical areas: token explosion (replicating v1.0's 192-token problem), CSS property naming mismatches with Figma components, reference chain overcomplexity, incomplete implementation (design tools without code sync), and integration failures between component tokens and existing tiers. This document catalogs specific pitfalls for narrowing from comprehensive extraction to component-scoped tokens, with prevention strategies mapped to implementation phases.

**Context:** v1.0 extracted 192 tokens but they were overwhelming in Figma, poorly named for component mapping, and missing component-level structure. v2.0 narrows to buttons & forms with CSS property naming conventions, requiring careful integration with existing core/semantic tokens while avoiding v1.0's mistakes.

---

## Critical Pitfalls

Mistakes that cause rewrites, component adoption failures, or complete project blockage.

### Pitfall 1: Component Token Explosion (500+ tokens)

**What goes wrong:** Creating tokens for every component property × variant × state × size results in unmanageable token counts.

**Why it happens:**
- Systematic approach without editorial judgment
- Formula: Component with 3 variants × 3 sizes × 4 states × 12 properties = 432 tokens *per component*
- Fear of missing edge cases leads to "tokenize everything" approach
- No distinction between "tokens designers need" vs "tokens that exist"
- Bootstrap 5 has 600+ variables; extracting all creates unusable system

**Real-world example:**
```
Button component breakdown:
- Variants: primary, secondary, tertiary (3)
- Sizes: small, medium, large (3)
- States: default, hover, focus, active, disabled (5)
- Properties: background, border, text-color, padding-x, padding-y, font-size,
             font-weight, border-radius, box-shadow, min-height, icon-spacing, gap (12)

Total: 3 × 3 × 5 × 12 = 540 tokens for buttons alone
```

**Consequences:**
- Token Studio performance degradation (500+ tokens = slow, difficult to search)
- Designers overwhelmed: "Which token do I use?"
- Maintenance nightmare: updating 1 design decision requires 50 token changes
- Long token names engineers can't parse: `button-m-warning-quiet-overbackground-textonly-focus-ring-animation-duration`
- Documentation becomes unmanageable
- Contradicts v2.0 goal of narrowing from 192 tokens

**How to avoid:**
- **Inheritance over duplication:** Don't create separate tokens for properties that inherit from semantic layer
- **State modifiers, not separate tokens:** Use single `button-primary-background` with separate `button-state-hover-opacity` modifier
- **Size through existing spacing:** Reference existing spacing tokens, don't create button-specific padding tokens
- **Component-specific only when necessary:** Only create component token if value differs from semantic token
- **80/20 rule:** Focus on tokens designers actually change (background, border, text-color), not immutable properties

**Prevention structure:**
```json
{
  "// WRONG - 540 tokens for buttons": "",
  "button": {
    "primary": {
      "small": {
        "default": {
          "background": { "$value": "{color.brand.primary}" },
          "border": { "$value": "{color.brand.primary}" },
          "text-color": { "$value": "{color.text.on-brand}" },
          "padding-x": { "$value": "12px" },
          "padding-y": { "$value": "6px" },
          "font-size": { "$value": "14px" }
        },
        "hover": { "...": "..." },
        "focus": { "...": "..." }
      },
      "medium": { "...": "..." },
      "large": { "...": "..." }
    }
  },

  "// CORRECT - ~20 tokens for buttons": "",
  "button": {
    "primary": {
      "background": { "$value": "{color.action.primary}" },
      "background-hover": { "$value": "{color.action.primary-hover}" },
      "border-color": { "$value": "{color.action.primary}" },
      "text-color": { "$value": "{color.text.inverse}" }
    },
    "secondary": {
      "background": { "$value": "{color.surface.secondary}" },
      "border-color": { "$value": "{color.border.default}" },
      "text-color": { "$value": "{color.text.primary}" }
    }
  },
  "// Size handled by existing spacing tokens, states by opacity modifiers": ""
}
```

**Warning signs:**
- Token count >100 for single component
- Many tokens with identical values but different state/size names
- Designer feedback: "Too many options, can't find what I need"
- Token names exceed 60 characters
- Multiple tokens for properties that could use calculation (padding-x vs padding-y)

**Phase to address:**
- **Phase 1 (Research):** Define component token scope criteria — what deserves a token?
- **Phase 2 (Architecture):** Document inheritance model — component → semantic → core
- **Phase 3 (Implementation):** Editorial review of every proposed token — justify existence

**Recovery cost if occurs:** HIGH - Requires complete restructuring, token deprecation strategy, migration of existing Figma files

**Sources:**
- [Component-level Design Tokens: are they worth it?](https://medium.com/@NateBaldwin/component-level-design-tokens-are-they-worth-it-d1ae4c6b19d4) - Real-world 500+ token example
- [The context dilemma: design tokens and components](https://frontside.com/blog/2021-01-15-design-tokens-and-components/) - Token explosion analysis
- v1.0 project learnings: 192 tokens proved too many for practical Figma use

---

### Pitfall 2: CSS Property Naming Without Figma Component Property Mapping

**What goes wrong:** Token names follow CSS property conventions but don't match Figma component property names, breaking designer adoption.

**Why it happens:**
- Developer-first naming: `button-primary-background-color` matches CSS `background-color`
- Figma Auto Layout uses different terms: "Fill" not "background", "Padding" not "padding-x/padding-y"
- Token Studio can't auto-map CSS property names to Figma properties
- No bridge between developer CSS thinking and designer Figma thinking
- v1.0 learned this: tokens existed but designers didn't know which token mapped to which Figma property

**Real-world disconnect:**
```
CSS Property          Figma Property         Token Name Problem
-----------------------------------------------------------------
background-color   →  Fill                  button-background vs button-fill?
border             →  Stroke                button-border vs button-stroke?
padding-left       →  Padding (left)        Figma shows "Padding" not "padding-x"
font-weight        →  Weight (in typography) font-weight vs typography-weight?
box-shadow         →  Effects               button-shadow vs button-effect?
opacity            →  Layer opacity         state-opacity or layer-opacity?
```

**Consequences:**
- Designers can't find correct token when looking at Figma component properties
- Token Studio requires manual application instead of auto-mapping
- Documentation must explain "use button-background for Figma's Fill property"
- Low adoption: designers give up and use hard-coded values
- v2.0 goal of component-property mapping fails

**How to avoid:**
- **Dual naming consideration:** Token names should work for both CSS developers AND Figma designers
- **Property-first naming:** `button-primary-fill` (Figma term) with CSS variable `--button-primary-background-color` (developer term)
- **Documentation layer:** Explicit mapping table in docs: "button-fill → background-color in CSS"
- **Figma-first for designer-facing tokens:** Component tokens are designer-first, build process handles CSS translation
- **Metadata for mapping:** Use `$description` to document CSS property mapping

**Prevention structure:**
```json
{
  "button": {
    "primary": {
      "fill": {
        "$type": "color",
        "$value": "{color.action.primary}",
        "$description": "Button background fill. Maps to CSS background-color property."
      },
      "stroke": {
        "$type": "color",
        "$value": "{color.action.primary}",
        "$description": "Button border stroke. Maps to CSS border-color property."
      },
      "padding": {
        "$type": "dimension",
        "$value": "{spacing.md}",
        "$description": "Button internal padding. Maps to CSS padding property."
      }
    }
  }
}
```

**Style Dictionary transform for CSS output:**
```javascript
// Transform Figma-style names to CSS properties
{
  name: 'name/figma-to-css',
  type: 'name',
  transformer: (token) => {
    return token.path
      .join('-')
      .replace('-fill', '-background-color')
      .replace('-stroke', '-border-color');
  }
}
```

**Warning signs:**
- Designers asking "Which token controls the button background?"
- Token Studio applications require manual searching
- Disconnect between design handoff and developer implementation
- Designers reverting to hard-coded hex values instead of tokens
- Documentation has extensive "token translation" sections

**Phase to address:**
- **Phase 1 (Research):** Document Figma component property names vs CSS properties
- **Phase 2 (Architecture):** Define naming convention that bridges both worlds
- **Phase 3 (Implementation):** Build Style Dictionary transform for CSS output renaming
- **Phase 4 (Documentation):** Create explicit mapping table in designer documentation

**Recovery cost if occurs:** MEDIUM - Token renaming strategy, Figma file updates, developer CSS updates

**Sources:**
- [Design Tokens in Practice: From Figma Variables to Production Code](https://www.designsystemscollective.com/design-tokens-in-practice-from-figma-variables-to-production-code-fd40aeccd6f5)
- [Figma Variable Settings for Design-to-Code Workflows](https://medium.com/design-bootcamp/figma-variable-settings-for-design-to-code-workflows-186e97efbac9)
- v1.0 learnings: Token names didn't match Figma component properties, blocking adoption

---

### Pitfall 3: Reference Chain Overcomplexity (4+ levels deep)

**What goes wrong:** Component tokens reference semantic tokens which reference other semantic tokens which reference core tokens, creating unresolvable chains and circular references.

**Why it happens:**
- Three-tier architecture (core → semantic → component) encourages multi-level aliasing
- No limit in DTCG spec: "no limit to how far a series of token references can go"
- Each tier adds references: `{button.primary.fill}` → `{color.action.primary}` → `{color.interactive.base}` → `{color.blue.500}` → `#0066cc`
- Token Studio free tier merged file resolution can't handle deep chains
- Style Dictionary `outputReferences: true` breaks when intermediate tokens filtered

**Real-world problem chain:**
```json
{
  "// Level 0 - Core (primitives)": "",
  "color": {
    "blue": {
      "500": { "$value": "#0066cc" }
    }
  },

  "// Level 1 - Semantic (functional)": "",
  "color": {
    "interactive": {
      "base": { "$value": "{color.blue.500}" }
    }
  },

  "// Level 2 - Semantic (context)": "",
  "color": {
    "action": {
      "primary": { "$value": "{color.interactive.base}" }
    }
  },

  "// Level 3 - Component": "",
  "button": {
    "primary": {
      "fill": { "$value": "{color.action.primary}" }
    }
  },

  "// RESULT: 4-level chain": "",
  "// {button.primary.fill} → {color.action.primary} → {color.interactive.base} → {color.blue.500} → #0066cc": "",

  "// PROBLEM: If Token Studio free tier can't resolve cross-file refs, merged file must flatten ALL": ""
}
```

**Consequences:**
- Token Studio import failures on merged file with deep references
- Circular reference errors when component tokens accidentally reference each other
- Style Dictionary warnings: "broken reference" when intermediate token filtered
- Debugging becomes impossible: "What's the actual value of this token?"
- Performance degradation in Figma with deep resolution chains
- v1.0 merge script requirement compounds this: merged file must flatten references

**How to avoid:**
- **Maximum 2-level references:** Component → Semantic → Core. No semantic → semantic chains
- **Direct core references acceptable:** Skip semantic layer for unique component values
- **Flatten at build time:** Use Style Dictionary to resolve references before Figma export
- **Validation:** Automated tests detect reference depth >2 levels
- **Token Studio constraint:** Merged file (free tier) should have pre-resolved values, not references

**Prevention structure:**
```json
{
  "// WRONG - 4 levels deep": "",
  "{button.primary.fill} → {color.action.primary} → {color.interactive.base} → {color.blue.500}": "",

  "// CORRECT - Maximum 2 levels": "",
  "button": {
    "primary": {
      "fill": { "$value": "{color.action.primary}" }
    }
  },
  "color": {
    "action": {
      "primary": { "$value": "{color.blue.500}" }
    }
  },
  "color": {
    "blue": {
      "500": { "$value": "#0066cc" }
    }
  },

  "// OR - Direct reference when appropriate": "",
  "button": {
    "primary": {
      "fill": { "$value": "{color.blue.500}" }
    }
  }
}
```

**Detection strategy:**
```javascript
// Automated reference depth checker
function checkReferenceDepth(tokens, maxDepth = 2) {
  const resolveDepth = (tokenValue, depth = 0) => {
    if (depth > maxDepth) {
      throw new Error(`Reference chain exceeds ${maxDepth} levels`);
    }

    const refMatch = tokenValue.match(/\{([^}]+)\}/);
    if (!refMatch) return depth; // No reference, base case

    const referencedToken = getTokenByPath(tokens, refMatch[1]);
    return resolveDepth(referencedToken.$value, depth + 1);
  };

  // Check all tokens
  Object.values(tokens).forEach(token => {
    if (token.$value?.startsWith('{')) {
      resolveDepth(token.$value);
    }
  });
}
```

**Warning signs:**
- Style Dictionary build warnings about broken references
- Token Studio slow performance or import failures
- Circular reference errors during build
- Merged Figma file has `{color.action.primary}` instead of resolved values
- Debugging requires tracing through 4+ token definitions

**Phase to address:**
- **Phase 1 (Research):** Define reference depth policy (recommend max 2 levels)
- **Phase 2 (Architecture):** Document valid reference patterns in token structure
- **Phase 3 (Implementation):** Build validation script rejecting deep chains
- **Phase 4 (Build):** Style Dictionary config resolves references for Figma output

**Recovery cost if occurs:** MEDIUM - Refactor semantic layer to flatten chains, update all component tokens

**Sources:**
- [Design Tokens Format Module 2025.10](https://www.designtokens.org/tr/drafts/format/) - No reference depth limit in spec
- [The Essential Principles of a Scalable Token Architecture](https://www.supernova.io/blog/scalable-token-architecture-principles)
- v1.0 learnings: Token Studio free tier merged file required, cross-file resolution failed

---

### Pitfall 4: Incomplete Implementation (Figma Variables Without Code Sync)

**What goes wrong:** Team creates Figma variables and Token Studio tokens but never establishes automated sync to production code, leaving design and development diverged.

**Why it happens:**
- "Figma variables don't automatically sync to code" - requires build pipeline
- v1.0 achieved Token Studio → JSON → Style Dictionary → CSS pipeline, but it's manual
- No automated trigger: designer changes in Figma don't trigger builds
- Missing reverse sync: developer CSS changes don't update Figma
- "Most teams implement tokens halfway—they set up Figma variables, export some JSON, and wonder why their design system still feels disconnected"

**Consequences:**
- Design files show one token value, production code uses different value
- Designers change tokens in Figma, developers never get updates
- Developers update CSS variables, designers unaware of changes
- "Design-code drift" undermines token system value proposition
- Manual export/import process fragile, depends on individual remembering to sync
- v2.0 can't achieve component-level adoption without reliable sync

**How to avoid:**
- **Automated pipeline:** GitHub Actions workflow triggered on token file changes
- **Single source of truth decision:** Either Figma Variables (designer-led) OR Token JSON (developer-led), not both
- **Build-time validation:** CI fails if Figma export doesn't match production tokens
- **Documentation of sync process:** Explicit instructions for "How to update tokens"
- **Versioning:** Token changes trigger version bump, changelog entry

**Prevention architecture:**
```yaml
# .github/workflows/tokens-sync.yml
name: Sync Design Tokens

on:
  push:
    paths:
      - 'tokens/**/*.json'
  workflow_dispatch:

jobs:
  build-tokens:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Validate token JSON
        run: npm run validate:tokens

      - name: Build Style Dictionary
        run: npm run build:tokens

      - name: Generate Figma merged file
        run: npm run build:tokens-figma

      - name: Run token tests
        run: npm run test:tokens

      - name: Commit generated files
        run: |
          git config user.name "Token Bot"
          git add tokens/dist/
          git commit -m "chore: rebuild tokens"
          git push
```

**Single source of truth options:**
```
Option A: Figma-first (designer-led)
- Designers update Figma Variables
- Token Studio exports to JSON (manual step)
- Developer commits JSON, triggers build
- Downside: Manual export step, depends on designer remembering

Option B: Code-first (developer-led) [RECOMMENDED for v2.0]
- Developers update tokens/*.json directly
- Style Dictionary builds CSS variables
- Separate script builds tokens-figma.json (merged file)
- Designers import merged file to Token Studio
- Figma Variables updated from Token Studio
- Upside: Git versioning, automated builds, CI validation

Option C: Bidirectional sync (complex)
- Requires custom tooling
- High maintenance cost
- Risk of conflicts
- Not recommended unless large team with dedicated tooling engineer
```

**Warning signs:**
- Designer asks "Why doesn't production match my Figma file?"
- Developer updates CSS variables without updating token JSON
- Token export/import happens <1x per month (indicates broken workflow)
- Production CSS variables diverge from tokens/*.json
- No automated tests for token consistency

**Phase to address:**
- **Phase 1 (Research):** Decide single source of truth (Figma vs code)
- **Phase 2 (Architecture):** Design automated sync pipeline
- **Phase 3 (Implementation):** Build GitHub Actions workflow
- **Phase 4 (Documentation):** Document token update process for team

**Recovery cost if occurs:** HIGH - Requires manual audit of design vs code, reconciliation, then building automation

**Sources:**
- [Design Tokens in Practice: From Figma Variables to Production Code](https://www.designsystemscollective.com/design-tokens-in-practice-from-figma-variables-to-production-code-fd40aeccd6f5) - "Most teams implement tokens halfway"
- [Understanding the Differences Between Figma Variables and Design Tokens](https://www.supernova.io/blog/understanding-the-differences-between-figma-variables-and-design-tokens)
- v1.0 learnings: Manual build process works but requires discipline

---

### Pitfall 5: Integration Failures Between Component Tokens and Existing Core/Semantic Tiers

**What goes wrong:** Component tokens added to existing system don't properly reference semantic layer, creating isolated token silos and duplicating values.

**Why it happens:**
- Component tokens developed in isolation from existing v1.0 core/semantic tokens
- Developers create new semantic tokens for components instead of reusing existing
- No validation that component tokens reference existing tiers
- Token Studio free tier merged file obscures reference relationships
- Bootstrap 5 integration adds third token source (Bootstrap vars, v1.0 tokens, v2.0 component tokens)

**Real-world integration failure:**
```json
{
  "// EXISTING v1.0 semantic tokens": "",
  "color": {
    "action": {
      "primary": { "$value": "{color.blue.500}" }
    },
    "text": {
      "on-brand": { "$value": "{color.white}" }
    }
  },

  "// WRONG - v2.0 component tokens bypass existing semantic layer": "",
  "button": {
    "primary": {
      "background": { "$value": "#0066cc" },  // Hard-coded, not referencing existing semantic
      "text-color": { "$value": "#ffffff" }   // Duplicates color.text.on-brand
    }
  },

  "// CORRECT - v2.0 integrates with existing semantic tokens": "",
  "button": {
    "primary": {
      "background": { "$value": "{color.action.primary}" },  // References existing
      "text-color": { "$value": "{color.text.on-brand}" }    // Reuses existing
    }
  }
}
```

**Consequences:**
- Value duplication: same color `#0066cc` defined in 3 places (core, semantic, component)
- Rebrand requires updating component tokens separately from semantic tokens
- Component tokens don't inherit theming changes to semantic layer
- Token count increases unnecessarily (v1.0 had 192, v2.0 adds 150 more instead of 20)
- No single source of truth for brand colors
- Bootstrap variables disconnected from token system

**Bootstrap-specific integration challenge:**
```scss
// Bootstrap 5 existing variables
$primary: #0066cc;
$btn-padding-y: 0.375rem;
$btn-border-radius: 0.25rem;

// v1.0 extracted as core tokens
color.blue.500: #0066cc
spacing.xs: 0.375rem
border-radius.sm: 0.25rem

// v2.0 component tokens must bridge both:
button.primary.background → {color.action.primary} → {color.blue.500} → matches $primary ✓
button.padding-y → {spacing.xs} → matches $btn-padding-y ✓

// WRONG - bypassing existing tokens:
button.primary.background: #0066cc  // Duplicates Bootstrap $primary and color.blue.500
```

**How to avoid:**
- **Audit existing tokens first:** Inventory all v1.0 core and semantic tokens before creating component tokens
- **Reuse-first policy:** Component tokens MUST reference existing semantic tokens unless unique value required
- **Integration validation:** Automated test ensures component tokens don't duplicate core/semantic values
- **Bootstrap mapping:** Document which Bootstrap variables map to which tokens
- **Three-tier enforcement:** Component → Semantic → Core. No skipping layers (except for truly unique values)

**Prevention workflow:**
```
Before creating new component token:

1. Check: Does semantic layer have this concept?
   → YES: Reference semantic token
   → NO: Proceed to step 2

2. Check: Does core layer have this value?
   → YES: Create new semantic token referencing core, then reference semantic from component
   → NO: Proceed to step 3

3. Check: Does Bootstrap have this variable?
   → YES: Extract to core, create semantic, reference from component
   → NO: Create as truly unique component token (rare)

Example:
Need: button.primary.background

1. Semantic layer has color.action.primary? YES → Use it
   button.primary.background: {color.action.primary}

2. If NO semantic exists:
   Core has color.blue.500? YES → Create semantic first
   color.action.primary: {color.blue.500}
   button.primary.background: {color.action.primary}

3. If neither exist:
   Bootstrap has $primary? YES → Extract to core, build up
   color.blue.500: #0066cc (from $primary)
   color.action.primary: {color.blue.500}
   button.primary.background: {color.action.primary}
```

**Detection:**
- Duplicate values: Same hex color/dimension in multiple tokens
- Component tokens with hard-coded values instead of references
- Grep for `"$value": "#"` in component tokens (indicates hard-coded color)
- Reference graph analysis: orphaned component tokens not connected to semantic layer
- Style Dictionary build output shows no references for component tokens

**Warning signs:**
- v2.0 adds >100 tokens when <30 expected
- Component tokens can't be themed (hard-coded values)
- Changing semantic token doesn't affect component tokens
- Documentation doesn't show token hierarchy
- Bootstrap updates require updating tokens separately

**Phase to address:**
- **Phase 1 (Research):** Audit all v1.0 tokens, categorize as core/semantic
- **Phase 2 (Architecture):** Design integration strategy - how component tokens reference existing tiers
- **Phase 3 (Implementation):** Build validation ensuring component tokens reference existing tokens
- **Phase 4 (Migration):** Refactor any duplicated values to use references

**Recovery cost if occurs:** HIGH - Requires refactoring all component tokens to add proper references, potentially restructuring semantic layer

**Sources:**
- [Component-tokens first? Hear me out...](https://medium.com/@hereinthehive/component-tokens-first-hear-me-out-6258f54935a9)
- [The context dilemma: design tokens and components](https://frontside.com/blog/2021-01-15-design-tokens-and-components/)
- v1.0 learnings: 192 tokens extracted without clear tier separation, needed refactoring

---

## Moderate Pitfalls

Mistakes that cause delays, technical debt, or require significant refactoring but don't block project.

### Pitfall 6: Form Component Token Overspecificity

**What goes wrong:** Creating separate token sets for every form element (text input, select, checkbox, radio, textarea, date picker) instead of shared form tokens.

**Why it happens:**
- HTML form elements are semantically different (`<input>`, `<select>`, `<textarea>`)
- Bootstrap has element-specific variables (`$input-padding-y`, `$select-padding-y`)
- Component-first thinking: "Each component needs its own tokens"
- Missing abstraction: "Form control" as shared concept

**Consequences:**
- Token explosion: 20 properties × 6 form elements = 120 tokens
- Inconsistent forms: text input padding differs from select padding (unintentional)
- Maintenance burden: updating form styling requires 6 token changes
- Missed opportunity for form consistency

**How to avoid:**
- **Shared form tokens:** `form.control.padding` applies to all form elements
- **Override pattern:** `form.select.padding` only when select needs different value
- **Default + exception:** Most form elements share tokens, exceptions documented

**Prevention structure:**
```json
{
  "// WRONG - Element-specific duplication": "",
  "form": {
    "input": {
      "padding-y": { "$value": "8px" },
      "border-color": { "$value": "{color.border.default}" },
      "background": { "$value": "{color.surface.default}" }
    },
    "select": {
      "padding-y": { "$value": "8px" },  // Duplicate
      "border-color": { "$value": "{color.border.default}" },  // Duplicate
      "background": { "$value": "{color.surface.default}" }  // Duplicate
    },
    "textarea": { "...": "..." }
  },

  "// CORRECT - Shared form control tokens": "",
  "form": {
    "control": {
      "padding-y": { "$value": "{spacing.sm}" },
      "padding-x": { "$value": "{spacing.md}" },
      "border-color": { "$value": "{color.border.default}" },
      "border-radius": { "$value": "{border-radius.sm}" },
      "background": { "$value": "{color.surface.default}" },
      "text-color": { "$value": "{color.text.primary}" }
    },
    "select": {
      "icon-padding": { "$value": "{spacing.lg}" }  // Only unique property
    }
  }
}
```

**Warning signs:**
- Multiple form element tokens with identical values
- Form controls visually inconsistent (unintended differences)
- Token count for forms >50

**Phase to address:**
- **Phase 2 (Architecture):** Define shared form control concept
- **Phase 3 (Implementation):** Create shared tokens first, exceptions second

---

### Pitfall 7: State Token Misapplication (Hover/Focus/Active/Disabled)

**What goes wrong:** Creating fully specified tokens for every state instead of using state modifiers.

**Why it happens:**
- Literal translation of CSS: `:hover`, `:focus`, `:active` are separate selectors
- Component-focused extraction: button has 5 states, create 5 token sets
- Missing abstraction: state as modifier, not separate token

**Consequences:**
- Token explosion: 3 variants × 5 states = 15 background color tokens for buttons
- State inconsistency: hover opacity differs between buttons and forms (unintentional)
- Can't change hover effect globally (must update 15 tokens)

**How to avoid:**
- **State modifiers:** `state.hover.opacity: 0.9` applied to any component
- **Semantic state colors:** `color.interactive.hover` references core color
- **Component base + state modifier:** `button.primary.background` + `state.hover.overlay`

**Prevention structure:**
```json
{
  "// WRONG - State-specific duplication": "",
  "button": {
    "primary": {
      "background": { "$value": "{color.action.primary}" },
      "background-hover": { "$value": "#0052a3" },  // Darker version
      "background-focus": { "$value": "#0052a3" },  // Same as hover
      "background-active": { "$value": "#003d7a" }, // Even darker
      "background-disabled": { "$value": "#cccccc" }
    }
  },

  "// CORRECT - Base + state modifiers": "",
  "button": {
    "primary": {
      "background": { "$value": "{color.action.primary}" }
    }
  },
  "state": {
    "hover": {
      "darken": { "$value": "10%" }  // CSS filter or mix-color
    },
    "active": {
      "darken": { "$value": "20%" }
    },
    "disabled": {
      "opacity": { "$value": "0.5" }
    }
  }
}
```

**CSS implementation with modifiers:**
```css
.btn-primary {
  background-color: var(--button-primary-background);
}

.btn-primary:hover {
  filter: brightness(calc(1 - var(--state-hover-darken)));
}

.btn-primary:disabled {
  opacity: var(--state-disabled-opacity);
}
```

**Warning signs:**
- Many component tokens ending in `-hover`, `-focus`, `-active`
- Same state treatment duplicated across components
- Can't change hover effect globally

**Phase to address:**
- **Phase 2 (Architecture):** Define state modifier strategy
- **Phase 3 (Implementation):** Create shared state tokens

---

### Pitfall 8: Token Studio Free Tier Merged File Reference Loss

**What goes wrong:** Flattening tokens to merged file for Token Studio free tier loses reference relationships, breaking semantic structure.

**Why it happens:**
- v1.0 learned: Token Studio free tier can't resolve cross-file references
- Merge script resolves all references to final values
- Merged file shows `#0066cc` instead of `{color.action.primary}`
- Designers lose understanding of token relationships

**Consequences:**
- Designers don't understand token hierarchy
- Can't see what changes when rebrand updates core colors
- Merged file becomes source of truth, bypassing semantic structure
- Token Studio shows flat list, not organized hierarchy

**How to avoid:**
- **Documentation:** Explain that Figma file shows resolved values, JSON has references
- **Maintain both:** tokens/*.json (with references) + tokens-figma.json (resolved)
- **Token Studio organization:** Use Token Sets to group related tokens
- **Comments in merged file:** Include comments explaining reference structure

**Prevention approach:**
```json
{
  "// tokens-figma.json (merged file for Token Studio)": "",
  "$comment": "This file contains resolved values. See tokens/core.json and tokens/semantic.json for reference structure.",

  "button": {
    "primary": {
      "background": {
        "$value": "#0066cc",
        "$description": "References {color.action.primary} which references {color.blue.500}"
      }
    }
  }
}
```

**Warning signs:**
- Designers unaware of token hierarchy
- Questions like "If I change this blue, what else changes?"
- Merged file is only file designers look at

**Phase to address:**
- **Phase 3 (Implementation):** Build merge script that preserves reference info in descriptions
- **Phase 4 (Documentation):** Explain token hierarchy to designers

**Source:** v1.0 learnings: Token Studio free tier merge requirement

---

### Pitfall 9: Bootstrap 5 Variable Collision with Component Tokens

**What goes wrong:** Component tokens use same names as Bootstrap 5 SCSS variables, creating namespace conflicts.

**Why it happens:**
- Bootstrap has `$btn-*` variables
- Component tokens create `button-*` tokens
- Both compile to CSS variables in same namespace
- Bootstrap 5.3+ uses CSS variables with `--bs-` prefix
- Token system uses `--ff-` prefix but references Bootstrap variables

**Consequences:**
- Naming confusion: `--bs-btn-padding-y` vs `--ff-button-padding-y`
- Unclear precedence: which one wins?
- Bootstrap updates overwrite custom tokens
- Dual maintenance: Bootstrap variables + design tokens

**How to avoid:**
- **Namespace separation:** `--ff-` prefix for all design tokens
- **Explicit override strategy:** Document which Bootstrap variables are overridden vs extended
- **Token → Bootstrap mapping:** Show how tokens compile to Bootstrap variable overrides

**Prevention approach:**
```scss
// Bootstrap 5 default
$btn-padding-y: 0.375rem;
$btn-padding-x: 0.75rem;

// Design token system
--ff-button-padding-y: 0.5rem;  // Different value
--ff-button-padding-x: 1rem;

// Bootstrap override (if needed)
$btn-padding-y: var(--ff-button-padding-y);  // Use token value
```

**Warning signs:**
- Bootstrap updates break token styling
- Unclear which system controls which properties
- Developers unsure whether to use `--bs-*` or `--ff-*` variables

**Phase to address:**
- **Phase 2 (Architecture):** Define Bootstrap integration strategy
- **Phase 3 (Implementation):** Document Bootstrap override approach

---

## Technical Debt Patterns

Shortcuts that seem reasonable but create long-term problems.

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Hard-code component token values instead of references | Faster initial setup, no semantic layer needed | Token system becomes brittle, can't theme, duplicated values everywhere | Never - defeats token system purpose |
| Skip state modifiers, create separate state tokens | Matches CSS structure 1:1, easier mental model | Token explosion, inconsistent state behavior, hard to update globally | Never for v2.0 - contradicts narrowing goal |
| Create component tokens without auditing existing v1.0 tokens | Faster development, no coordination needed | Duplicated values, integration failures, missed reuse opportunities | Never - integration is critical |
| Merge all tokens into single flat file | Simpler file structure, fewer files to manage | Loses semantic organization, hard to maintain, no reference visibility | Only for Token Studio free tier export (keep structured source) |
| Skip Figma property mapping research | Developer-first naming is faster | Designers can't find tokens, low adoption, manual application required | Only if designers aren't primary consumers (dev-only system) |
| Use CSS property names for tokens | Matches developer mental model perfectly | Figma designers confused, misalignment with Figma component properties | Only if code-first and designers use dev mode exclusively |
| Create tokens for all form elements separately | Covers all edge cases, element-specific control | 120+ tokens for forms, maintenance nightmare, inconsistency risk | Only if forms are genuinely highly differentiated (rare) |

---

## Integration Gotchas

Common mistakes when connecting component tokens to existing v1.0 system and external tools.

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| **Token Studio Free Tier** | Storing separate files expecting cross-file resolution | Use merge script to create single `tokens-figma.json` with resolved values |
| **Style Dictionary v5.3.0** | Using `outputReferences: true` without `outputReferencesFilter` | Import and use `outputReferencesFilter` utility to prevent broken refs |
| **Bootstrap 5** | Mixing `--bs-*` and `--ff-*` variables without override strategy | Document which Bootstrap variables are overridden by tokens vs coexist |
| **Figma Variables** | Expecting auto-sync from Token Studio to production CSS | Build GitHub Actions workflow for automated token builds |
| **v1.0 Core/Semantic Tokens** | Creating component tokens in isolation | Audit existing tokens first, reuse semantic layer, validate references |
| **CSS Custom Properties** | Using CSS property names that don't match Figma properties | Use Figma-friendly names, transform to CSS names in Style Dictionary |
| **Multi-file Token Structure** | Token Studio import fails with "Contents Don't Pass Schema Validation" | Merge script must output valid DTCG format with `$type` and `$value` |
| **Reference Chains** | Deep aliasing (4+ levels) breaks Token Studio resolution | Enforce maximum 2-level references: Component → Semantic → Core |

---

## Performance Traps

Patterns that work at small scale but fail as token system grows.

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| **Token Studio 500+ tokens** | Slow search, laggy UI, hard to find tokens | Editorial review, limit to designer-facing tokens only | >300 tokens in single file |
| **Deep reference chains** | Slow Figma variable resolution, Token Studio hangs | Max 2-level references, flatten at build | >3 levels deep |
| **Unorganized Token Sets** | Can't find tokens, designers overwhelmed | Use Token Studio folders/sets to categorize | >100 tokens without organization |
| **No token filtering** | Every token exposed to designers, even internal ones | Public vs private token separation | All 192 v1.0 tokens visible |
| **Build-time reference resolution** | Style Dictionary build takes >10s | Cache builds, only rebuild changed files | >1000 tokens |

---

## "Looks Done But Isn't" Checklist

Things that appear complete but are missing critical pieces for v2.0 component tokens.

- [ ] **Component tokens created:** Often missing integration with existing v1.0 semantic layer — verify all component tokens reference existing semantic or core tokens, not hard-coded values
- [ ] **Figma file updated:** Often missing automated sync workflow — verify GitHub Actions builds tokens on every commit, not manual export
- [ ] **Token names defined:** Often missing Figma property mapping — verify designers can find tokens by looking at Figma component property names
- [ ] **Button tokens complete:** Often missing form tokens — verify both buttons AND forms covered (v2.0 scope)
- [ ] **CSS variables generated:** Often missing `--ff-` prefix consistency — verify all component tokens compile to `--ff-component-*` format
- [ ] **Token documentation:** Often missing token hierarchy diagram — verify docs show Core → Semantic → Component reference structure
- [ ] **Style Dictionary config:** Often missing Figma output format — verify `tokens-figma.json` merged file is built automatically
- [ ] **Reference validation:** Often missing depth checking — verify no reference chains >2 levels deep
- [ ] **Bootstrap integration:** Often missing override documentation — verify which Bootstrap variables are replaced vs coexist with tokens

---

## Recovery Strategies

When pitfalls occur despite prevention, how to recover.

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| **Token explosion (500+)** | HIGH | 1. Audit all tokens for duplicates/unnecessary variants<br>2. Consolidate states into modifiers<br>3. Remove size-specific tokens, use existing spacing<br>4. Deprecation strategy for removed tokens<br>5. Figma file updates to use consolidated tokens |
| **CSS property naming mismatch** | MEDIUM | 1. Create mapping table (Figma property → CSS property)<br>2. Add `$description` with CSS property mapping<br>3. Style Dictionary transform for renaming<br>4. Documentation update<br>5. Designer training |
| **Deep reference chains** | MEDIUM | 1. Analyze reference graph depth<br>2. Flatten semantic layer (remove semantic → semantic refs)<br>3. Update component tokens to reference flattened semantic<br>4. Rebuild merged Figma file<br>5. Validation script prevents future deep chains |
| **No code sync** | HIGH | 1. Decide single source of truth (code-first recommended)<br>2. Build GitHub Actions workflow<br>3. Reconcile current Figma vs code differences<br>4. Document token update process<br>5. Test automated pipeline |
| **Integration failure (v1.0 tokens)** | HIGH | 1. Audit v1.0 core and semantic tokens<br>2. Identify duplicated values in v2.0<br>3. Refactor component tokens to use references<br>4. Add missing semantic tokens if needed<br>5. Validation ensuring references resolve |
| **Form token overspecificity** | LOW | 1. Create shared `form.control` tokens<br>2. Migrate element-specific to shared<br>3. Keep only truly unique element tokens<br>4. Update Figma components<br>5. Documentation of shared tokens |
| **State duplication** | MEDIUM | 1. Create shared `state.*` modifier tokens<br>2. Refactor component tokens to base values only<br>3. Update CSS to apply modifiers<br>4. Test all state interactions<br>5. Remove state-specific tokens |
| **Bootstrap namespace collision** | LOW | 1. Document `--bs-*` vs `--ff-*` usage<br>2. Explicit Bootstrap override strategy<br>3. Update imports order (tokens before Bootstrap)<br>4. Test precedence<br>5. Team training |

---

## Pitfall-to-Phase Mapping

How v2.0 roadmap phases should address these pitfalls.

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| **Token explosion (500+)** | Phase 1 (Research): Define scope criteria<br>Phase 2 (Architecture): Document inheritance model | Token count <50 for buttons+forms combined |
| **CSS property naming mismatch** | Phase 1 (Research): Audit Figma component properties<br>Phase 2 (Architecture): Define naming convention | Designers can find tokens without documentation |
| **Reference chain overcomplexity** | Phase 2 (Architecture): Define max depth policy<br>Phase 3 (Implementation): Build validation | Automated test: no chains >2 levels |
| **Incomplete implementation (no sync)** | Phase 1 (Research): Decide source of truth<br>Phase 3 (Implementation): Build GitHub Actions | GitHub commit triggers automated build |
| **Integration failure (v1.0 tokens)** | Phase 1 (Research): Audit existing v1.0 tokens<br>Phase 3 (Implementation): Reference validation | All component tokens reference semantic/core |
| **Form token overspecificity** | Phase 2 (Architecture): Define shared form tokens<br>Phase 3 (Implementation): Create shared first | <30 form tokens total |
| **State token misapplication** | Phase 2 (Architecture): Define state modifier strategy<br>Phase 3 (Implementation): Shared state tokens | No `-hover`/`-focus` suffixes in component tokens |
| **Token Studio merged file reference loss** | Phase 3 (Implementation): Merge script with reference info<br>Phase 4 (Documentation): Explain hierarchy | Designers understand token relationships |
| **Bootstrap collision** | Phase 2 (Architecture): Define Bootstrap integration<br>Phase 3 (Implementation): Override documentation | Clear precedence rules documented |

---

## Narrowing-Specific Pitfalls

Unique challenges when narrowing from comprehensive extraction (v1.0: 192 tokens) to component-scoped (v2.0: buttons & forms).

### Pitfall 10: Scope Creep During Narrowing

**What goes wrong:** Starting with "buttons and forms only" but gradually expanding to "let's also do badges, alerts, cards..."

**Why it happens:**
- Component boundaries blur (badge is like a small button?)
- Designer requests: "While you're at it, can we also..."
- Fear of missing related components
- Momentum: "We're on a roll, let's keep going"

**Consequences:**
- v2.0 never ships (always "just one more component")
- Defeats purpose of narrowing from v1.0's 192 tokens
- Dilutes focus, quality suffers
- Team burnout

**How to avoid:**
- **Explicit scope document:** List included/excluded components
- **v2.0 scope:** Buttons (primary, secondary, tertiary) + Forms (input, select, checkbox, radio, textarea) ONLY
- **Parking lot:** Track "future components" for v3.0
- **Completion criteria:** v2.0 ships when buttons+forms done, not when all components done

**Warning signs:**
- Roadmap phases keep getting added
- Token count exceeds estimate
- "Just one more component" discussions
- Timeline slipping

**Phase to address:**
- **Phase 0 (Planning):** Explicit scope document with exclusions
- **All phases:** Scope enforcement — reject out-of-scope additions

---

### Pitfall 11: Premature Generalization

**What goes wrong:** Trying to design a "perfect" component token structure that works for all future components, not just buttons/forms.

**Why it happens:**
- "We'll need to add more components later, so let's design for that now"
- Over-engineering: anticipating needs that may never materialize
- Fear of refactoring later

**Consequences:**
- Analysis paralysis: can't start because structure isn't "perfect"
- Overly complex token structure for simple buttons/forms
- YAGNI violation: "You Aren't Gonna Need It"
- v2.0 delayed

**How to avoid:**
- **Design for v2.0 scope only:** Buttons + forms, not all future components
- **Refactor later:** Accept that v3.0 may require structure changes
- **Iterate:** Ship v2.0, learn, improve in v3.0
- **Good enough:** Structure that works for buttons/forms is sufficient

**Warning signs:**
- Token structure has 5+ levels for 2 components
- Lengthy debates about "what if we add..."
- Architecture phase exceeds implementation phase
- No tokens created yet, still designing structure

**Phase to address:**
- **Phase 2 (Architecture):** Design for current scope, not future scope
- **Phase 3 (Implementation):** Ship buttons+forms, defer generalization

---

## Sources

### Official Documentation (HIGH confidence)
- [W3C Design Tokens Format Module 2025.10](https://www.designtokens.org/tr/drafts/format/) - Reference depth, DTCG spec
- [Style Dictionary: Configuration](https://styledictionary.com/reference/config/) - Build configuration, output references
- [Token Studio: Token Sets](https://docs.tokens.studio/manage-tokens/token-sets) - Token organization
- [Token Studio: Composition (legacy)](https://docs.tokens.studio/manage-tokens/token-types/composition) - Composition token issues
- [Token Studio: Variables and Tokens Studio](https://docs.tokens.studio/figma/variables-overview) - Figma Variables integration
- [Figma: Guide to Variables](https://help.figma.com/hc/en-us/articles/15339657135383-Guide-to-variables-in-Figma) - Figma Variables documentation
- v1.0 project audit findings: 192 tokens too many, poor naming for Figma adoption

### Design Token Best Practices (HIGH confidence)
- [Component-level Design Tokens: are they worth it?](https://medium.com/@NateBaldwin/component-level-design-tokens-are-they-worth-it-d1ae4c6b19d4) - Token explosion example (500+ tokens)
- [99% of the Design Tokens share this mistake!](https://medium.com/design-bootcamp/99-of-the-design-tokens-in-the-world-of-design-systems-share-this-mistake-8f84c1bdf54d) - Naming inconsistencies
- [Common Mistakes in Design Tokens Adoption](https://designtokens.substack.com/p/common-mistakes-in-design-tokens) - Component coupling, documentation
- [The context dilemma: design tokens and components](https://frontside.com/blog/2021-01-15-design-tokens-and-components/) - Component token integration
- [Component-tokens first? Hear me out...](https://medium.com/@hereinthehive/component-tokens-first-hear-me-out-6258f54935a9) - Component-first approach

### Figma Variables & Integration (MEDIUM-HIGH confidence)
- [Design System Mastery with Figma Variables: 2025/2026 Best-Practice Playbook](https://www.designsystemscollective.com/design-system-mastery-with-figma-variables-the-2025-2026-best-practice-playbook-da0500ca0e66)
- [Design Tokens in Practice: From Figma Variables to Production Code](https://www.designsystemscollective.com/design-tokens-in-practice-from-figma-variables-to-production-code-fd40aeccd6f5) - "Halfway implementation"
- [Understanding the Differences Between Figma Variables and Design Tokens](https://www.supernova.io/blog/understanding-the-differences-between-figma-variables-and-design-tokens)
- [Figma Variable Settings for Design-to-Code Workflows](https://medium.com/design-bootcamp/figma-variable-settings-for-design-to-code-workflows-186e97efbac9)

### Naming & Architecture (MEDIUM-HIGH confidence)
- [Best Practices For Naming Design Tokens - Smashing Magazine](https://www.smashingmagazine.com/2024/05/naming-best-practices/)
- [A Semantic Approach to Buttons (& More) Using Design Tokens](https://medium.com/design-bootcamp/a-semantic-approach-to-buttons-more-a218aee69f47)
- [The Essential Principles of a Scalable Token Architecture](https://www.supernova.io/blog/scalable-token-architecture-principles)
- [The Pyramid Design Token Structure](https://stefaniefluin.medium.com/the-pyramid-design-token-structure-the-best-way-to-format-organize-and-name-your-design-tokens-ca81b9d8836d)

### Style Dictionary & Tooling (HIGH confidence)
- [How to manage your Design Tokens with Style Dictionary](https://didoo.medium.com/how-to-manage-your-design-tokens-with-style-dictionary-98c795b938aa)
- [Dark Mode with Style Dictionary](https://dbanks.design/blog/dark-mode-with-style-dictionary/) - Complex configurations
- [Style Dictionary: Support Composite Tokens Issue](https://github.com/amzn/style-dictionary/issues/848) - Composite token handling

### Bootstrap Integration (MEDIUM confidence)
- [Use design tokens to customise Bootstrap](https://smth.uk/use-design-tokens-to-customise-bootstrap/)
- [Bootstrap UI Components With Design Tokens](https://www.michaelmang.dev/blog/bootstrap-ui-components-with-design-tokens-and-headless-ui/)
- [Bootstrap: Use custom properties (CSS variables) Issue](https://github.com/twbs/bootstrap/issues/26596) - Bootstrap CSS variable limitations

### Migration & Refactoring (MEDIUM confidence)
- [Refactoring Token Names for Seamless Design System Maintenance](https://medium.com/sas-software-design/refactoring-token-names-for-seamless-design-system-maintenance-79f222cd57f3)
- [The problem(s) with design tokens](https://andretorgal.com/posts/2025-01/the-problem-with-design-tokens) - Token system challenges

---

## Confidence Assessment

| Area | Sources | Confidence |
|------|---------|------------|
| Token explosion (500+) | Real-world examples, multiple articles | HIGH |
| CSS property naming mismatch | Figma documentation, design-to-code articles | HIGH |
| Reference chain depth | W3C spec, Token Studio limitations, v1.0 learnings | HIGH |
| Incomplete implementation (no sync) | Design Systems Collective articles, industry patterns | MEDIUM-HIGH |
| Integration with v1.0 tokens | Component token best practices, v1.0 audit | HIGH |
| Form token specificity | Bootstrap structure, component token patterns | MEDIUM |
| State token patterns | Design token naming conventions, CSS patterns | MEDIUM-HIGH |
| Token Studio free tier | v1.0 project learnings, Token Studio docs | HIGH |
| Bootstrap collision | Bootstrap documentation, integration articles | MEDIUM |
| Scope creep during narrowing | Project management best practices, v1.0 learnings | MEDIUM |

---

## Usage Notes for v2.0 Roadmap Planning

**This document should inform:**
1. **Phase structure:** Each phase must prevent specific pitfalls identified here
2. **Scope enforcement:** v2.0 is buttons+forms ONLY, defer other components to v3.0
3. **Integration validation:** Component tokens MUST reference existing v1.0 semantic/core tokens
4. **Naming convention:** Bridge Figma property names and CSS property names
5. **Token count target:** <50 tokens total for buttons+forms (not 500+)

**Red flags requiring deeper research:**
- If component token count exceeds 100, Phase 1 needs stricter scope criteria
- If reference chains exceed 2 levels, Phase 2 architecture needs flattening
- If Figma-to-code sync not automated, Phase 3 requires GitHub Actions workflow
- If component tokens bypass v1.0 semantic layer, Phase 3 needs integration validation

**Safe to proceed if:**
- Token scope limited to buttons (3 variants) + forms (5 elements)
- Naming convention defined bridging Figma and CSS terminology
- Integration strategy with v1.0 core/semantic tokens documented
- Automated sync workflow planned (GitHub Actions)
- Maximum 2-level reference depth enforced
- Token count estimate <50 total
