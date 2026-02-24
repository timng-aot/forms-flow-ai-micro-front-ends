# Phase 5: Architecture & Integration Planning - Research

**Researched:** 2026-02-23
**Domain:** Design token architecture — component token layer integrating with DTCG-format v1.0 core/semantic tokens
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Token hierarchy depth**
- Max 3 reference levels: component → semantic → core
- Skip semantic layer when it adds no value — component can reference core directly when obvious
- When multiple components share the same value, create a shared semantic token (don't have independent core references)
- Expand the v1.0 semantic.json with new semantic tokens as needed to support component references (e.g. action.primary, feedback.error)

**Naming structure**
- Dot-separated groups following W3C DTCG nesting: `button.primary.hover.background`
- Segment order: **component.variant.state.property** (industry standard)
- Default state is omitted — `button.primary.background` implies default; state only appears for hover/active/focus/disabled
- CSS custom properties mirror dot path directly: `button.primary.hover.background` → `--ff-button-primary-hover-background`
- No abbreviations in generated CSS vars — full readable names

**File organization**
- Single `components.json` file containing both button and form token sections
- New semantic tokens added to existing `semantic.json` (extend, not separate file)
- Merged Token Studio file (`tokens.json`) includes core + semantic + components — single import
- Keep v1.0 `core.json` complete but flag unused tokens (don't prune yet)

**Variant & state coverage**
- **Button variants:** primary, secondary, outline, danger — core variants only, not every codebase variant
- **Interactive states:** full set — default, hover, active, focus, disabled
- **CSS properties per token:** visual properties only — background, border-color, color (text), shadow
- **Shared tokens for static properties:** when a property doesn't change across states (e.g. border-radius), use a shared token without state segment rather than duplicating per-state

### Claude's Discretion
- Exact semantic token names for shared component values
- How to flag unused core tokens (comment, metadata, or separate mapping)
- Form element variant breakdown (inputs, selects, checkboxes, radios — how granular)
- Whether border-width and font properties warrant tokens for base component definition (non-state-changing)

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| ARCH-01 | Audit v1.0 tokens to identify which core/semantic tokens buttons and forms actually reference | Covered by: v1.0 token inventory analysis below; button and form SCSS cross-reference maps |
| ARCH-02 | Define CSS property naming convention for component tokens (e.g. `button.primary.background.default`) | Covered by: DTCG naming pattern analysis, custom name/css/ff-prefix transform behavior documentation |
| ARCH-03 | Establish max 2-level reference depth policy (component → semantic → core) — note: user decision upgrades to max 3 levels | Covered by: Style Dictionary reference resolution mechanics, depth policy rationale |
| ARCH-04 | Define component token file structure (`tokens/component/button.json`, `tokens/component/forms.json`) — note: user decision consolidates to single `components.json` | Covered by: existing build pipeline analysis, merge-for-figma.js extension pattern |
</phase_requirements>

---

## Summary

Phase 5 is a planning and documentation phase — no code ships. The output is a documented architecture specification that answers five questions: which v1.0 tokens do buttons and forms actually use, what naming convention governs component tokens, what file structure holds them, how deep can reference chains go, and how does the component layer connect to v1.0 without duplication.

The v1.0 infrastructure is solid and well-understood. The existing `core.json` (160 tokens, DTCG-compliant), `semantic.json` (32 tokens), Style Dictionary config with custom `name/css/ff-prefix` transform, and `merge-for-figma.js` script all provide clear extension points. The key architectural decision already made is component → semantic → core with max 3 levels, single `components.json` file, and a naming pattern of `component.variant.state.property`.

The primary planning risk is scope drift during the audit task (ARCH-01): the `_button.scss` uses hardcoded SCSS vars (`$color-primary: var(--vivid-100)`) rather than consuming token CSS vars directly, so the audit must trace through two indirection layers to map component properties to core token values. The form SCSS (`_textInput.scss`, `_checkbox.scss`) has a similar pattern and also contains hardcoded hex values not yet tokenized.

**Primary recommendation:** Phase 5 produces three artifacts — (1) a token reference map documenting which v1.0 tokens buttons and forms use, (2) a naming convention decision record, and (3) a `components.json` schema stub that validates against the existing build pipeline before Phase 6 writes real tokens.

---

## Standard Stack

### Core (already in place — no new dependencies)

| Tool | Version | Purpose | Why Standard |
|------|---------|---------|--------------|
| Style Dictionary | already installed | Transforms DTCG JSON to CSS custom properties | Established build pipeline from Phase 3 |
| @tokens-studio/sd-transforms | already installed | DTCG expand, Token Studio preprocessing | Required for Token Studio → SD pipeline |
| Token Studio (Figma plugin) | free tier | Figma sync via merged tokens.json | Locked in by Token Studio free tier constraint |

### No New Dependencies Required

Phase 5 is a planning phase. All tooling is already in place. The deliverables are JSON stub files and documentation, not executable code.

---

## Architecture Patterns

### v1.0 Token Inventory (Confirmed by Source Reading)

The v1.0 system provides the following token categories that component tokens will reference:

**core.json — 160 tokens across:**
- `ff.color.*` — 65 color tokens (palette + brand colors)
- `ff.spacing.*` — 12 spacing scale tokens (0.25rem → 3rem)
- `ff.radius.*` — 7 radius tokens (xs/sm/md/lg/xl/pill/full)
- `ff.font-size.*`, `ff.font-weight.*`, `ff.font-family.*`
- `ff.duration.*` — transition durations and timing functions
- `ff.shadow.*` (via semantic) — button and input shadow values exist in semantic.json

**semantic.json — 32 tokens including:**
- `color.action.primary` → `{ff.color.indigo-100}` (already exists)
- `color.bootstrap-danger` → `{ff.color.red-100}`
- `radius.button.default` → `{ff.radius.pill}` (already exists)
- `shadow.button.primary/secondary/error/warning` (already exists)
- `duration.button.duration/timing` (already exists)

### Button → v1.0 Token Reference Map

Derived from reading `forms-flow-theme/scss/v8-scss/_button.scss`:

| Button CSS Property | SCSS Variable | Resolves to Core Token | Semantic Token Exists? |
|--------------------|---------------|----------------------|----------------------|
| background (default) | `$color-light-gray` | `ff.color.white-200` | No — needs `color.background.surface` |
| background (hover) | `$color-white` | `ff.color.white-300` | `color.background.default` (partial) |
| border-color (primary default) | `$color-primary-border` = `var(--primary-dark)` | `ff.color.primary-dark` | No — needs `color.action.primary-border` |
| border-color (primary hover) | `$color-primary-light` = `var(--primary-dark)` | `ff.color.primary-dark` | No |
| border-color (secondary default) | `$color-medium-gray` = `var(--gray-x-light)` | `ff.color.gray-x-light` | No |
| color/text (primary default) | `$color-dark-gray` = `var(--gray-darkest)` | `ff.color.gray-darkest` | `color.text.primary` → `{ff.color.black}` (wrong value) |
| color/text (disabled) | `$color-medium-gray` = `var(--gray-x-light)` | `ff.color.gray-x-light` | No |
| shadow (primary hover) | `$button-shadow-primary` | `shadow.button.primary` in semantic.json | YES — already exists |
| shadow (secondary hover) | `$button-shadow-secondary` | `shadow.button.secondary` in semantic.json | YES — already exists |
| border-radius | `$button-border-radius: 1.5625rem` | `ff.radius.pill` | `radius.button.default` → `{ff.radius.pill}` — YES |
| transition duration | `$button-transition-duration: 0.15s` | `ff.duration.fast` | `duration.button.duration` → `{ff.duration.fast}` — YES |

**Key finding:** The danger/error variant maps to `ff.color.orange-100` (not red). The warning variant maps to `ff.color.red-100`. This naming is counterintuitive and ARCH-01 audit must document it explicitly.

### Form → v1.0 Token Reference Map

Derived from reading `_textInput.scss` and `_checkbox.scss`:

**Text input (`_textInput.scss`):**
| CSS Property | SCSS Variable | Core Token |
|-------------|---------------|------------|
| color | `var(--gray-darkest)` | `ff.color.gray-darkest` |
| placeholder color | `var(--gray-dark)` | `ff.color.gray-dark` |
| placeholder disabled | `var(--gray-xx-light)` | `ff.color.gray-xx-light` |
| border-color (default) | `var(--gray-x-light)` | `ff.color.gray-x-light` |
| border-color (hover) | `var(--secondary-dark)` | `ff.color.secondary-dark` |
| border-color (focus) | `var(--gray-dark)` | `ff.color.gray-dark` |
| background | `var(--white-200)` | `ff.color.white-200` |
| font-size | `var(--font-size-m)` | `ff.font-size.font-size-m` |
| font-weight | `var(--font-weight-regular)` | `ff.font-weight.font-weight-regular` |
| border-radius | hardcoded `5px` | `ff.radius.md` (0.3125rem ≈ 5px) |
| height/padding | hardcoded `2.5rem`, `11px 10px` | No exact core token |

**Checkbox (`_checkbox.scss`):**
- Uses hardcoded hex values (`#ffffff`, `#fcfcfc`, `#B7B7B8`, `#4a4a4a`, etc.) — NOT using CSS var references
- These map to `ff.color.white-300`, `ff.color.white-200`, `ff.color.gray-medium-dark`, `ff.color.gray-darkest`
- `$color-primary-selected: #8969f2` — does NOT map cleanly to any existing core token (closest: `ff.color.vivid-100` = `#7c80fe`)
- `$color-primary: rgba(184, 171, 255, 1)` = `ff.color.primary-dark` = `#B8ABFF`

### Recommended File Structure

```
tokens/
├── core.json              # Unchanged (v1.0) — 160 tokens
├── semantic.json          # Extended (v1.0 + new component-shared tokens)
├── components.json        # NEW — component tokens (button + form sections)
├── tokens.json            # Extended merge: core + semantic + components
└── scripts/
    └── merge-for-figma.js # Update to include components.json
```

The `components.json` top-level structure follows the same DTCG pattern as `core.json`:

```json
{
  "button": {
    "primary": {
      "$type": "color",
      "background": {
        "$value": "{color.background.surface}",
        "$description": "Primary button default background"
      },
      "border-color": {
        "$value": "{color.action.primary-border}",
        "$description": "Primary button default border"
      },
      "color": {
        "$value": "{color.text.primary}",
        "$description": "Primary button default text color"
      },
      "hover": {
        "background": {
          "$value": "{color.background.default}",
          "$description": "Primary button hover background"
        },
        "border-color": {
          "$value": "{color.action.primary}",
          "$description": "Primary button hover border"
        },
        "shadow": {
          "$value": "{shadow.button.primary}",
          "$description": "Primary button hover shadow"
        }
      }
    }
  }
}
```

Note: `$type` inheritance works in DTCG — group-level `$type: "color"` applies to all children without their own `$type`. Shadow tokens need their own `$type: "shadow"`.

### CSS Custom Property Naming — Confirmed Output Behavior

The existing `name/css/ff-prefix` transform in `style-dictionary.config.js` handles all tokens that don't start with `ff` by prepending `ff`:

```javascript
const path = token.path[0] === 'ff' ? token.path : ['ff', ...token.path];
return path.join('-');
```

For `components.json` token at path `['button', 'primary', 'hover', 'background']`:
- Transform prepends `ff` → `['ff', 'button', 'primary', 'hover', 'background']`
- Joined with hyphens → `ff-button-primary-hover-background`
- Style Dictionary adds `--` prefix → `--ff-button-primary-hover-background`

This matches the locked naming decision exactly. No changes to the transform are needed.

### Reference Depth Policy — How It Works in Practice

The Style Dictionary config uses `outputReferences: true`, which means CSS output resolves reference chains to `var()` chains:

```css
/* 3-level chain: component → semantic → core */
--ff-button-primary-border-color: var(--ff-color-action-primary-border);
--ff-color-action-primary-border: var(--ff-color-primary-dark);
--ff-color-primary-dark: #B8ABFF;
```

The existing build already resolves semantic → core (2 levels). Adding component → semantic → core (3 levels) requires the `buildTokens()` function to include all three source files when building `components.json`.

The policy "skip semantic when no value" produces a direct component → core reference:
```css
/* 2-level chain: component → core (semantic adds no value here) */
--ff-button-border-radius: var(--ff-radius-pill);
```

### New Semantic Tokens Needed

Based on the button/form audit, these semantic tokens need to be added to `semantic.json`:

**Color — action intent:**
- `color.action.primary-border` → `{ff.color.primary-dark}` (button primary border)
- `color.action.secondary-border` → `{ff.color.gray-x-light}` (button secondary border)
- `color.action.danger` → `{ff.color.orange-100}` (button error/danger variant — note: named "error" in SCSS but maps to orange)
- `color.feedback.error` → `{ff.color.red-100}` (form validation error)
- `color.feedback.warning` → `{ff.color.yellow-100}` (warning state)

**Color — surface/text:**
- `color.background.surface` → `{ff.color.white-200}` (component surface — button/input default bg)
- `color.text.default` → `{ff.color.gray-darkest}` (body text in components — distinct from existing `color.text.primary` → `{ff.color.black}` which is wrong value for buttons)

**Shared existing semantic tokens that buttons/forms CAN use directly:**
- `shadow.button.primary` — already exists
- `shadow.button.secondary` — already exists
- `shadow.button.error` — already exists
- `radius.button.default` → `{ff.radius.pill}` — already exists
- `duration.button.duration` → `{ff.duration.fast}` — already exists
- `color.action.primary` → `{ff.color.indigo-100}` — already exists

### Anti-Patterns to Avoid

**Anti-pattern: Component-scoped semantic tokens**
Do NOT create `color.button.primary-border` in semantic.json — that collapses the semantic layer into a component-specific alias, defeating the sharing purpose. Semantic tokens must be intent-based (`color.action.primary-border`) so multiple components can reference them.

**Anti-pattern: Duplicating existing semantic tokens**
`shadow.button.primary` already exists in semantic.json. Phase 6 must reference it (`{shadow.button.primary}`), not define a new `button.primary.shadow` token with the same value.

**Anti-pattern: Mixing $type inheritance with shadow tokens**
Grouping shadow tokens under a `$type: "color"` parent will fail validation. Shadow tokens need explicit `"$type": "shadow"` on the token or a shadow-typed parent group.

**Anti-pattern: State explosion**
Static properties (border-radius, transition duration) must NOT be duplicated per-state. Use a single shared token without a state segment: `button.primary.border-radius` not `button.primary.hover.border-radius` AND `button.primary.focus.border-radius`.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| CSS var name generation | Custom string join | Existing `name/css/ff-prefix` transform | Already handles ff-prefix logic |
| Token reference validation | Manual JSON linting | Existing `validate-dtcg` preprocessor + `reference_resolution` check | Already integrated in build pipeline |
| Token Studio Figma merge | Manual file editing | `merge-for-figma.js` extended to include `components.json` | Pattern already established |
| Multi-source resolution | Custom resolver | Style Dictionary `source` array with all 3 files | SD resolves cross-file references natively |

**Key insight:** The v1.0 build pipeline already handles everything Phase 5 needs. The only change is extending `buildTokens()` to accept a 3-file source array and extending `merge-for-figma.js` to include `components.json`.

---

## Common Pitfalls

### Pitfall 1: Conflating "error" and "danger" naming with actual color values

**What goes wrong:** The button SCSS calls a variant "error" but it maps to `ff.color.orange-100` (#ff9100 — orange). The semantic naming `color.bootstrap-danger` maps to `ff.color.red-100`. This is counterintuitive.
**Why it happens:** The SCSS was written without a formal naming system.
**How to avoid:** ARCH-01 audit must explicitly document: "button 'error' variant → orange-100", "button 'danger' variant (v2.0 name) → red-100 (semantic bootstrap-danger)". The v2.0 component tokens use the correct semantic names (danger = red, warning = orange/yellow).
**Warning signs:** Any component token referencing `ff.color.orange-100` for a token named "danger".

### Pitfall 2: Checkbox SCSS does not use CSS var references

**What goes wrong:** `_checkbox.scss` uses hardcoded hex values (`#8969f2`, `#b8abff`), not `var(--vivid-100)` etc. ARCH-01 audit must trace these hex values to core tokens, not follow CSS var chains.
**Why it happens:** Checkbox predates the v1.0 token system.
**How to avoid:** Cross-reference hex values in checkbox against core.json color values directly. `#8969f2` does not exist in core.json (closest is `ff.color.vivid-100` = `#7c80fe`). This is a gap that component tokens must bridge by choosing the correct core token.
**Warning signs:** Any component token that must hardcode a hex because no core token matches.

### Pitfall 3: tokens.json merge structure breaks Token Studio resolution

**What goes wrong:** The current `merge-for-figma.js` spreads `...core` and `...semantic` into a single `global` key. Adding `...components` naively will work if `components.json` top-level keys (`button`, `form`) don't conflict with core/semantic top-level keys.
**Why it happens:** Token Studio requires all tokens in one set for reference resolution on the free tier.
**How to avoid:** Verify `components.json` top-level keys don't collide with existing `core.json` keys (`ff`) or `semantic.json` keys (`color`, `spacing`, `radius`, etc.). The key `button` and `form` (or `components`) are safe.
**Warning signs:** Token Studio shows "unresolved reference" warnings after import.

### Pitfall 4: $type inheritance breaks with mixed token types in a group

**What goes wrong:** If you declare `$type: "color"` at the `button.primary` group level, then add a shadow sub-token (`button.primary.hover.shadow`), the shadow token inherits `$type: "color"` and fails DTCG validation.
**Why it happens:** The existing `validate-dtcg` preprocessor enforces type correctness.
**How to avoid:** In `components.json`, do NOT declare `$type` at the variant group level. Instead, use explicit `$type` on each leaf token or group tokens by type within a variant.
**Warning signs:** `DTCG Validation Error: Token has invalid $type="color"` for shadow tokens.

### Pitfall 5: Style Dictionary source order affects reference resolution

**What goes wrong:** When building `components.json`, if core.json is not in the `source` array, references like `{ff.color.indigo-100}` fail to resolve.
**Why it happens:** Style Dictionary resolves references across all files in `source`.
**How to avoid:** The component build must include: `[core.json, semantic.json, components.json]`. The existing build already does this pattern for semantic (core + semantic). Extend the same pattern.
**Warning signs:** `"Error: Reference not found"` during `sd.buildAllPlatforms()`.

---

## Code Examples

### Minimal valid components.json structure (validated against existing pipeline)

```json
{
  "button": {
    "primary": {
      "background": {
        "$type": "color",
        "$value": "{color.background.surface}",
        "$description": "Primary button default background"
      },
      "border-color": {
        "$type": "color",
        "$value": "{color.action.primary-border}",
        "$description": "Primary button default border"
      },
      "color": {
        "$type": "color",
        "$value": "{color.text.default}",
        "$description": "Primary button default text"
      },
      "border-radius": {
        "$type": "dimension",
        "$value": "{radius.button.default}",
        "$description": "Primary button border-radius (shared, no state segment)"
      },
      "hover": {
        "border-color": {
          "$type": "color",
          "$value": "{color.action.primary}",
          "$description": "Primary button hover border"
        },
        "shadow": {
          "$type": "shadow",
          "$value": "{shadow.button.primary}",
          "$description": "Primary button hover shadow"
        }
      }
    }
  }
}
```

### Extending merge-for-figma.js for components

```javascript
// Add to existing merge-for-figma.js
const components = JSON.parse(readFileSync(resolve(tokensDir, 'components.json'), 'utf8'));

const merged = {
  $themes: [],
  $metadata: {
    tokenSetOrder: ['global']
  },
  global: {
    ...core,
    ...semantic,
    ...components  // components keys: 'button', 'form' — no collision with 'ff', 'color', etc.
  }
};
```

### Extending buildTokens() for 3-source builds

```javascript
// In style-dictionary.config.js buildTokens()
const isComponentBuild = sourcePath.includes('components');
const sources = isComponentBuild
  ? [
      resolve(__dirname, '../../tokens/core.json'),
      resolve(__dirname, '../../tokens/semantic.json'),
      absoluteSourcePath
    ]
  : isSemanticBuild
  ? [resolve(__dirname, '../../tokens/core.json'), absoluteSourcePath]
  : [absoluteSourcePath];
```

### Flagging unused core tokens (Claude's Discretion recommendation)

Use `$description` annotation — lowest friction, no structural change:

```json
"yellow-100": {
  "$value": "#efc005",
  "$description": "v8 yellow palette shade 100 [UNUSED: no component references as of v2.0]"
}
```

Alternative: maintain a separate `tokens/audit/unused-core-tokens.md` document listing unreferenced token paths. This keeps `core.json` clean while making orphaned tokens visible. Prefer the external document approach so `core.json` stays pure DTCG without editorial metadata.

---

## State of the Art

| Old Approach | Current Approach | Notes |
|--------------|------------------|-------|
| Separate file per component (button.json, form.json) | Single `components.json` | User decision — Token Studio free tier drives this |
| Style-only audit | Trace SCSS vars through two indirection layers | Button SCSS uses `$color-primary: var(--vivid-100)` not direct CSS vars |
| Hardcoded hex in checkbox | Map to nearest core token | `#8969f2` (vivid active) has no exact core match — architecture must acknowledge gap |

---

## Open Questions

1. **Checkbox has a hardcoded purple (#8969f2) with no exact core token match**
   - What we know: `ff.color.vivid-100` = `#7c80fe` (blue-purple). `ff.color.primary-dark` = `#B8ABFF` (light purple). Neither matches `#8969f2`.
   - What's unclear: Was `#8969f2` intentional? Is it a design error or an intentional midtone?
   - Recommendation: For ARCH-01 audit output, document this as a gap. The component token should reference the nearest semantic color (`color.action.primary` or a new `color.action.primary-selected`). Do not add `#8969f2` to core.json.

2. **Form element granularity for v2.0 (Claude's Discretion)**
   - What we know: Locked scope is "buttons and forms". Text input and checkbox SCSS exist. Radio, textarea, select also exist.
   - What's unclear: Does v2.0 mean text-input only, or all form controls?
   - Recommendation: Cover text input (primary form element) and one selection control (checkbox or radio). Skip select/textarea for v2.0 to stay under the ~75-token limit. Document this as a scoping decision in the architecture plan.

3. **Border-width and font properties for component tokens (Claude's Discretion)**
   - What we know: Border-width (1px) and font-size (--font-size-m) are used by buttons and inputs but don't change across states.
   - What's unclear: Whether these warrant component tokens vs. being left as direct semantic references.
   - Recommendation: Include font-size and font-weight as component-level tokens for completeness (`button.font-size`, `button.font-weight`) with direct semantic references. Skip border-width — 1px is a dimension primitive, not a semantic concept. This keeps token count manageable.

---

## Sources

### Primary (HIGH confidence)

- `/Users/tngaot/Documents/forms-flow-ai-micro-front-ends/tokens/core.json` — full v1.0 token inventory, 160 tokens, confirmed by reading
- `/Users/tngaot/Documents/forms-flow-ai-micro-front-ends/tokens/semantic.json` — 32 existing semantic tokens, confirmed reference structure
- `/Users/tngaot/Documents/forms-flow-ai-micro-front-ends/forms-flow-theme/config/style-dictionary.config.js` — confirmed `name/css/ff-prefix` transform behavior, `buildTokens()` source array pattern
- `/Users/tngaot/Documents/forms-flow-ai-micro-front-ends/forms-flow-theme/scss/v8-scss/_button.scss` — confirmed button CSS property to SCSS variable to CSS custom property mapping
- `/Users/tngaot/Documents/forms-flow-ai-micro-front-ends/forms-flow-theme/scss/v8-scss/_textInput.scss` — confirmed form text input token references
- `/Users/tngaot/Documents/forms-flow-ai-micro-front-ends/forms-flow-theme/scss/v8-scss/_checkbox.scss` — confirmed hardcoded hex pattern, confirmed gap
- `/Users/tngaot/Documents/forms-flow-ai-micro-front-ends/tokens/scripts/merge-for-figma.js` — confirmed merge structure for Figma single-set pattern
- `/Users/tngaot/Documents/forms-flow-ai-micro-front-ends/tokens/validation-report.json` — confirmed token counts (core: 160, semantic: 32)

### Secondary (MEDIUM confidence)

- `.planning/phases/05-architecture-integration-planning/05-CONTEXT.md` — user decisions locked in prior discussion session
- `.planning/REQUIREMENTS.md` — formal requirement definitions (ARCH-01 through ARCH-04)
- `tokens/audit/gap-analysis.json` and `components-audit.md` — Phase 1 audit data confirming component value coverage (41.2%)

---

## Metadata

**Confidence breakdown:**
- v1.0 token inventory: HIGH — read directly from source files
- Button/form token reference map: HIGH — traced through SCSS source with two indirection layers
- New semantic tokens needed: HIGH — derived from gap between current semantic.json and what SCSS actually references
- File structure and build extension patterns: HIGH — read existing build pipeline code
- Checkbox color gap (#8969f2): HIGH — confirmed by reading both checkbox SCSS and all core.json color values

**Research date:** 2026-02-23
**Valid until:** 2026-04-23 (stable — v1.0 token files and build pipeline are unlikely to change before Phase 6)
