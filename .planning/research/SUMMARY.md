# Project Research Summary

**Project:** forms-flow-ai-micro-front-ends v2.0 — Component Token System
**Domain:** Design token system (component layer for buttons & forms)
**Researched:** 2026-02-10
**Confidence:** HIGH

## Executive Summary

v2.0 Component Token System represents a strategic narrowing from v1.0's 192-token extraction (overwhelming in Figma) to 60-75 focused component-level tokens for buttons and forms. The research validates a zero-new-dependencies approach: the existing v1.0 stack (Style Dictionary v5.3.0 + @tokens-studio/sd-transforms v2.0.3 + Token Studio free tier) fully supports 3-tier hierarchies (Core → Semantic → Component). The critical shift is **CSS property-based naming** replacing v1.0's Figma-centric naming, directly addressing the lesson learned that developers couldn't map tokens to implementation.

The recommended approach adds a single `tokens/component.json` file (or split `button.json` + `forms.json`) that references existing v1.0 semantic tokens, extends the Style Dictionary build pipeline with component-specific transforms, and updates the Figma merge script to include three layers. This is configuration-only work with no architectural rewrites required. The primary risk is token explosion (500+ tokens if not editorial) and integration failure (bypassing v1.0's semantic layer), both preventable through strict scope enforcement and reference validation.

Button and form components demand comprehensive state coverage (default, hover, active, focus, disabled) across variants, creating complexity in the 60-75 token range. Industry patterns from Material Design, Carbon, and Atlassian provide well-documented component token structures, reducing architectural uncertainty. The key mitigation strategy is **inheritance over duplication**: shared base properties (padding, radius, transitions) referenced once, variants override only colors/borders, states use modifiers not separate tokens.

## Key Findings

### Recommended Stack

**Zero new dependencies required.** v1.0's infrastructure handles component tokens without changes:

**Core technologies:**
- **Style Dictionary v5.3.0**: Already handles multi-file sources and reference resolution for 3-tier hierarchies. Component tokens are a third build target using existing `outputReferences: true` pattern from semantic build (lines 148-154, 199 of existing config).
- **@tokens-studio/sd-transforms v2.0.3**: Latest version compatible with SD v5. Includes all transforms needed for component tokens (ts/resolveMath, ts/color/css/hexrgba, ts/shadow/innerShadow).
- **Token Studio free tier**: Unlimited token sets confirmed in v1.0. Merge script pattern (tokens-figma.json) extends from 2 files to 3 files seamlessly.

**What's changing (configuration only):**
1. New token file: `tokens/component.json` with CSS property-based naming (`button.background.primary-default` not `button.fill.primary`)
2. Extended build pipeline: `build:tokens:component` added to composite build command
3. Style Dictionary config: Component build includes all three layers as sources (core + semantic + component) for reference resolution, filtered to output only component tokens
4. Figma merge script: Updated to include component tokens in merged file

**CSS property naming convention:**
```
{component}-{css-property}-{variant}-{state}

Examples:
- button-background-primary-default → CSS background-color
- button-border-primary-hover → CSS border-color
- input-shadow-focus → CSS box-shadow
```

### Expected Features

**Must have (table stakes):**
- **Button variant tokens** (primary, secondary, outlined, ghost): Standard across all design systems. Each variant needs 4-5 states × 3-5 CSS properties = 60-100 tokens total.
- **Button state coverage** (default, hover, active, focus, disabled): CSS requires distinct values for proper UX. WCAG 2.1 focus indicators mandatory.
- **Button CSS property tokens** (background, border, color, shadow, padding, height, border-radius, font-size): Direct mapping to CSS properties for developer experience.
- **Form input state tokens** (default, focus, error/invalid, disabled, valid): HTML form validation requires distinct visual states. Uses `:valid/:invalid/:user-valid/:user-invalid` pseudo-classes.
- **Form input CSS property tokens** (border, background, color, outline, shadow): Core styling properties for text inputs, selects, textareas.
- **Checkbox/radio state tokens** (unchecked, checked, indeterminate, hover, focus, disabled): HTML checkbox supports indeterminate state. Requires geometric tokens for checkmark styling.

**Should have (differentiators):**
- **CSS property naming** (background not fill): Matches developer mental model, reduces translation overhead. v1.0 used Figma naming; v2.0 switches for better DX.
- **Component-scoped CSS vars** (--ff-button-primary-background vs --ff-color-action-primary): Clear intent, prevents semantic token misuse in wrong contexts.
- **Single token for button height** (vs separate padding-top/bottom): Matches existing SCSS pattern ($button-min-height: 2.5rem).
- **Transition duration/timing tokens**: Animation consistency, supports prefers-reduced-motion. Existing SCSS has $button-transition-duration: 0.15s.

**Defer (v2+):**
- **Secondary/outlined/ghost variants** (~45 tokens): Prove architecture with primary button first, then extend.
- **Radio buttons** (~20 tokens): Similar to checkboxes, lower priority.
- **Size variants** (small, large): Adds ~30-40% more tokens, test standard size first.
- **Dark mode / theming variants**: No requirement in project scope, document as future enhancement.
- **Comprehensive component coverage** (accordions, modals, badges): v2.0 scope is buttons + forms ONLY.

### Architecture Approach

**Three-tier token hierarchy** (industry standard): Core (primitives) → Semantic (purpose) → Component (specific). v1.0 established first two tiers; v2.0 adds Component layer.

**Major components:**

1. **Component Token Files** (`tokens/component.json` or split `button.json` + `forms.json`): CSS property-based naming structure. References semantic tokens preferentially, core tokens when no semantic exists. State matrix pattern ensures complete coverage (default, hover, active, focus, disabled). Shared base properties (padding, transitions) referenced once; variants override only what differs.

2. **Style Dictionary Build Extension**: Third build target includes all three layers as sources for reference resolution. Filters output to only component tokens (exclude core/semantic from re-output). Uses existing `outputReferences: true` to generate CSS with `var()` references, enabling runtime theme switching.

3. **Token Studio Merge Script Update**: Extends v1.0's 2-file merge (core + semantic) to 3-file merge (core + semantic + component). Free tier constraint requires single merged file where all references resolve within same file. Deep merge preserves token paths, wraps in Token Studio format with `$themes` and `$metadata`.

**Data flow:**
```
Source: tokens/core.json (v1.0) + tokens/semantic.json (v1.0) + tokens/component.json (NEW)
    ↓
Style Dictionary (3 separate builds with shared sources for reference resolution)
    ↓
Output: tokens/dist/component-tokens.css (NEW, alongside existing core/semantic CSS)
    ↓
SCSS: Consumes via var(--ff-button-primary-background-default)

Parallel flow:
Merge script → tokens/dist/tokens-figma.json (3 layers) → Token Studio import → Figma Variables
```

**Key architectural patterns:**
- **Pattern 1: CSS Property-Based Naming** — `button.primary.background.default` maps directly to CSS `background-color`
- **Pattern 2: Shared Base + Variant Overrides** — `button.padding` shared, `button.primary.background` variant-specific
- **Pattern 3: State Matrix for Interactive Elements** — Every interactive property gets state definitions (default, hover, active, focus, disabled)
- **Pattern 4: Maximum 2-Level References** — Component → Semantic → Core. No semantic → semantic chains to avoid resolution failures.

### Critical Pitfalls

1. **Token Explosion (500+ tokens)** — Creating tokens for every property × variant × state × size results in unmanageable systems. Formula: 3 variants × 3 sizes × 5 states × 12 properties = 432 tokens per component. **Avoidance:** Inheritance over duplication. Shared properties referenced once. Size through existing spacing tokens. State modifiers not separate tokens. Editorial review: only create component token if value differs from semantic token. **Target: <50 tokens for buttons+forms combined.**

2. **CSS Property Naming Without Figma Mapping** — Token names follow CSS conventions (`background-color`) but don't match Figma properties (Fill). Designers can't find tokens when looking at Figma components. **Avoidance:** Dual naming consideration (Figma-friendly with CSS translation). Style Dictionary transform renames for CSS output (`-fill` → `-background-color`). Documentation includes explicit mapping table. Use `$description` to document CSS property mapping.

3. **Reference Chain Overcomplexity (4+ levels deep)** — Component → Semantic → Semantic → Core chains cause Token Studio resolution failures and Style Dictionary warnings. **Avoidance:** Maximum 2-level references enforced. Component tokens reference semantic OR core directly. Automated validation detects chains >2 levels. Flatten semantic layer to eliminate semantic → semantic chains.

4. **Integration Failures with v1.0 Core/Semantic Tiers** — Component tokens developed in isolation, bypassing existing semantic layer, duplicating values. **Avoidance:** Audit all v1.0 tokens before creating component tokens. Reuse-first policy: component tokens MUST reference existing semantic unless unique value required. Integration validation ensures no hard-coded values duplicating existing tokens. Bootstrap mapping documented.

5. **Scope Creep During Narrowing** — Starting with "buttons and forms" but expanding to badges, alerts, cards. v2.0 never ships. **Avoidance:** Explicit scope document. v2.0 = Buttons (primary, secondary, outlined, ghost) + Forms (input, select, checkbox, radio, textarea) ONLY. Parking lot for v3.0 components. Completion criteria: ship when buttons+forms done, not when all components done.

## Implications for Roadmap

Based on research, suggested phase structure for v2.0:

### Phase 1: Token Architecture & Integration Planning

**Rationale:** Component tokens must integrate with v1.0's existing 192 core/semantic tokens. Defining integration strategy first prevents duplication and ensures proper reference chains.

**Delivers:**
- Audit of existing v1.0 core/semantic tokens (identify what exists for reuse)
- CSS property naming convention specification (bridging Figma and CSS terminology)
- Component token scope criteria (what deserves a token vs inherits from semantic)
- Reference depth policy (max 2 levels: Component → Semantic → Core)
- Integration validation strategy (automated checks for hard-coded duplicates)

**Addresses (from FEATURES.md):**
- Semantic → component aliasing requirement
- Component-scoped CSS vars (--ff-button-* namespace)

**Avoids (from PITFALLS.md):**
- Integration failure with v1.0 tokens (Pitfall 5)
- Token explosion through duplication (Pitfall 1)
- Reference chain overcomplexity (Pitfall 3)

**Uses (from STACK.md):**
- Style Dictionary multi-source configuration pattern (existing semantic build as template)

**Research flag:** Standard patterns. v1.0 established the integration approach; this phase documents extension to component layer.

---

### Phase 2: Button Component Tokens (Primary Variant)

**Rationale:** Prove component token architecture with single variant before expanding. Primary button is highest usage, validates naming convention and state coverage.

**Delivers:**
- `tokens/component.json` (or `button.json`) with primary button variant
- 5 states: default, hover, active, focus, disabled
- CSS properties: background, border, color, shadow (focus only), plus shared properties (padding, height, radius, font-size, font-weight, border-width, gap, transitions)
- Style Dictionary component build configuration
- ~15-20 tokens

**Addresses (from FEATURES.md):**
- Button variant tokens (starting with primary)
- Button state coverage (all 5 states)
- Button CSS property tokens
- Focus indicators (WCAG 2.1 compliance)

**Avoids (from PITFALLS.md):**
- Premature generalization (Pitfall 11) — Design for buttons only, not all future components
- State token misapplication (Pitfall 7) — Use base + modifiers pattern

**Uses (from STACK.md):**
- Style Dictionary v5.3.0 third build target
- CSS property naming convention from Phase 1

**Implements (from ARCHITECTURE.md):**
- Pattern 1: CSS Property-Based Naming
- Pattern 2: Shared Base + Variant Overrides
- Pattern 3: State Matrix for Interactive Elements

**Research flag:** Standard patterns. Button states well-documented across Material Design, Carbon, Atlassian. Skip `/gsd:research-phase`.

---

### Phase 3: Form Input Component Tokens

**Rationale:** Forms share architectural patterns with buttons (states, variants) but introduce validation states. Builds on proven Phase 2 approach.

**Delivers:**
- Form control tokens in `component.json` (or `forms.json`)
- 5 states: default, focus, error, valid, disabled
- CSS properties: border, background, color, outline (focus), shadow (focus, error)
- Shared form control tokens (applies to input, select, textarea)
- ~15-20 tokens

**Addresses (from FEATURES.md):**
- Form input state tokens
- Form input CSS property tokens
- Form validation visual feedback (error/success borders, shadows)

**Avoids (from PITFALLS.md):**
- Form component token overspecificity (Pitfall 6) — Shared form.control tokens, not separate per element
- CSS property naming mismatch (Pitfall 2) — Consistent with button naming from Phase 2

**Uses (from STACK.md):**
- Same Style Dictionary build configuration as Phase 2, additional source file

**Implements (from ARCHITECTURE.md):**
- Pattern 2: Shared Base (form.control.*) + Variant Overrides (form.select.icon-padding)
- Pattern 3: State Matrix (default, focus, error, valid, disabled)

**Research flag:** Standard patterns. HTML form validation and Bootstrap 5 form styling well-documented. Skip `/gsd:research-phase`.

---

### Phase 4: Checkbox/Radio Component Tokens

**Rationale:** More complex than text inputs due to indeterminate state (checkboxes) and geometric checkmark tokens. Benefits from validated architecture from Phases 2-3.

**Delivers:**
- Checkbox tokens in `component.json` (or `forms.json`)
- 6 states: unchecked, checked, indeterminate, hover, focus, disabled
- CSS properties: border, background, checkmark color/width/height/border-width, box sizing
- Radio button tokens (similar structure)
- ~20-25 tokens per control type

**Addresses (from FEATURES.md):**
- Checkbox/radio state tokens (including indeterminate)
- Size variants (standard, small)

**Avoids (from PITFALLS.md):**
- Token explosion (Pitfall 1) — Checkmark properties tokenized but sizing inherits from existing spacing tokens

**Uses (from STACK.md):**
- Existing SCSS patterns ($checkbox-size, $checkmark-width) guide token extraction

**Implements (from ARCHITECTURE.md):**
- Pattern 3: State Matrix (6 states for checkbox)
- Pattern 4: Maximum 2-Level References (checkbox.checked.background → color.action.primary)

**Research flag:** Moderate complexity. Indeterminate state and checkmark geometry may need specific CSS research if existing SCSS patterns insufficient.

---

### Phase 5: Figma Integration & Sync Automation

**Rationale:** Component tokens exist in code but require Figma sync for designer adoption. Automation prevents design-code drift (v1.0 lesson: manual sync is fragile).

**Delivers:**
- Updated `tokens/scripts/merge-tokens.js` (includes component.json in merge)
- `tokens/dist/tokens-figma.json` (3-layer merged file)
- Token Studio import workflow documentation
- GitHub Actions workflow for automated token builds (triggered on JSON changes)
- Validation: CI fails if component tokens don't reference v1.0 tokens

**Addresses (from FEATURES.md):**
- (Implicitly all features — makes tokens usable by designers)

**Avoids (from PITFALLS.md):**
- Incomplete implementation (Pitfall 4) — Automated sync prevents Figma-code divergence
- Token Studio merged file reference loss (Pitfall 8) — Merge script preserves reference info in `$description`

**Uses (from STACK.md):**
- Token Studio free tier merged file pattern (extended from v1.0)
- Style Dictionary `outputReferences: true` for CSS var() generation

**Implements (from ARCHITECTURE.md):**
- Token Studio Integration (free tier constraints)
- Data Flow (end-to-end: JSON → Style Dictionary → CSS + Figma)

**Research flag:** Standard tooling. GitHub Actions workflows and merge scripts are established patterns. Skip `/gsd:research-phase`.

---

### Phase 6: Documentation & Migration

**Rationale:** Component tokens exist and sync to Figma, but adoption requires documentation and SCSS migration. v1.0 had tokens that designers/developers didn't use due to poor documentation.

**Delivers:**
- Token hierarchy diagram (Core → Semantic → Component)
- CSS property mapping table (Figma Fill → background-color in CSS)
- Token update workflow documentation (code-first: JSON → build → Figma)
- SCSS migration guide (replace hard-coded values with component tokens)
- Example implementations (primary button, text input)

**Addresses (from FEATURES.md):**
- (Enables adoption of all features delivered in Phases 2-4)

**Avoids (from PITFALLS.md):**
- CSS property naming mismatch (Pitfall 2) — Explicit mapping table resolves Figma/CSS terminology gap
- Incomplete implementation (Pitfall 4) — Documented update process ensures team follows sync workflow

**Uses (from STACK.md):**
- forms-flow-theme/docs/design-tokens/ directory (extends v1.0 documentation)

**Implements (from ARCHITECTURE.md):**
- SCSS Consumption Pattern (before/after examples)

**Research flag:** None. Documentation phase based on implementation outputs.

---

### Phase Ordering Rationale

**Sequential dependencies:**
1. **Phase 1 before all others:** Integration strategy must be defined before creating tokens. Prevents duplication and reference chain issues.
2. **Phase 2 (buttons) before Phase 3 (forms):** Buttons prove architecture, forms extend proven pattern.
3. **Phase 4 (checkbox) after forms:** Most complex component, benefits from validated patterns.
4. **Phase 5 (Figma) after token creation:** Sync automation requires completed tokens.
5. **Phase 6 (documentation) last:** Requires all implementation complete.

**Why this grouping:**
- Phases 2-4 are token creation (can partially parallelize after Phase 1 completes)
- Phase 5 is tooling/automation (depends on token structure being stable)
- Phase 6 is enablement (requires everything working)

**How this avoids pitfalls:**
- Phase 1 prevents integration failures (Pitfall 5) by auditing v1.0 tokens first
- Phases 2-4 enforce scope (buttons+forms only) preventing scope creep (Pitfall 10)
- Phase 5 prevents incomplete implementation (Pitfall 4) through automation
- Editorial review in each token phase prevents explosion (Pitfall 1)

### Research Flags

**Phases with standard patterns (skip `/gsd:research-phase`):**
- **Phase 1:** Integration planning — extends v1.0 approach, no new research needed
- **Phase 2:** Button tokens — Material Design, Carbon, Atlassian patterns well-documented
- **Phase 3:** Form input tokens — Bootstrap 5, HTML validation patterns established
- **Phase 5:** Figma sync — GitHub Actions and merge scripts are standard tooling
- **Phase 6:** Documentation — based on implementation outputs

**Phases potentially needing deeper research:**
- **Phase 4:** Checkbox/radio tokens — If existing SCSS doesn't provide clear checkmark geometry patterns, may need CSS pseudo-element research. **Likelihood: LOW** — existing SCSS in `_checkbox.scss` has established patterns ($checkmark-width, $checkmark-height, indeterminate state).

**Overall research depth:** Project has **HIGH confidence** due to:
- v1.0 established infrastructure (Style Dictionary, Token Studio, merge script)
- Well-documented industry patterns for component tokens (Material, Carbon, Atlassian)
- Narrow scope (buttons + forms, not comprehensive coverage)
- Existing SCSS provides token extraction baseline

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| **Stack** | **HIGH** | v1.0 infrastructure proven. Style Dictionary v5.3.0 semantic build demonstrates multi-file reference resolution. @tokens-studio/sd-transforms v2.0.3 latest compatible version. Token Studio free tier validated with unlimited token sets. |
| **Features** | **HIGH** | Button and form component features are table stakes across all design systems. State requirements (hover, focus, disabled) are CSS fundamentals. WCAG 2.1 focus indicators mandatory. Validation states standard in HTML forms. |
| **Architecture** | **HIGH** | Three-tier hierarchy (Core → Semantic → Component) is industry standard (verified across GitHub Primer, Shopify Polaris, Carbon, Atlassian). CSS property-based naming pattern documented in multiple sources. Token Studio free tier constraints known from v1.0. |
| **Pitfalls** | **HIGH** | Token explosion documented with real-world 500+ token examples. CSS property naming mismatch validated through Figma-to-code workflow articles. Reference chain depth issues confirmed in Token Studio limitations. v1.0 learnings provide project-specific pitfall evidence. |

**Overall confidence:** **HIGH**

### Gaps to Address

**Resolved gaps:**
- **Shadow tokens in v1.0:** Research indicates core tokens include `ff.shadow.*` based on STACK.md references. If missing, create during Phase 2 for button focus shadows.
- **Opacity tokens in v1.0:** Research doesn't confirm existence. If missing, create in Phase 2 for disabled states (0.6 typical). Alternatively, bake opacity into color values using rgba().
- **Button size variants:** Deferred to v2.1+. Phase 2 delivers standard size only, validating architecture before adding complexity.

**Validation needed during planning:**
1. **Existing v1.0 token inventory:** Phase 1 must audit actual v1.0 core/semantic tokens to confirm what exists for reuse. Research assumes standard coverage based on 192-token count, but explicit list required.
2. **Bootstrap variable mapping:** Phase 1 must document which Bootstrap 5 variables map to which tokens to prevent namespace collisions (--bs-btn-* vs --ff-button-*).
3. **Existing SCSS token usage:** Audit how v1.0 tokens are currently used (or not used) in SCSS to guide migration strategy in Phase 6.

**Acceptable uncertainties:**
- **Exact token count:** Research estimates 60-75 tokens total. Actual count depends on editorial decisions during implementation. Range is acceptable; >100 tokens triggers re-evaluation.
- **State modifier pattern adoption:** Research recommends base + modifiers over separate state tokens. If CSS implementation complexity too high, fallback to separate state tokens acceptable (increases token count ~20%).
- **Figma component property naming:** Research identifies mismatch risk but exact Figma component structure unknown. Phase 1 documentation resolves through explicit mapping table.

## Sources

### Primary (HIGH confidence)

**From STACK.md:**
- Style Dictionary v5.3.0 official documentation — Token organization, multi-file sources, DTCG format
- @tokens-studio/sd-transforms npm package — Version confirmation v2.0.3, compatibility
- W3C Design Tokens Community Group — DTCG 2025.10 stable specification
- GitHub: tokens-studio/sd-transforms — Transform documentation, component token examples

**From FEATURES.md:**
- Material Design Theming & Tokens — Component token patterns, state coverage
- Atlassian Design Tokens — Component-specific design decisions
- Carbon Design System Color Tokens — Token hierarchy examples
- Bootstrap Form Validation — HTML form state patterns (:invalid, :user-invalid)
- Nielsen Norman Group: Button States — State requirements (default, hover, active, focus, disabled)

**From ARCHITECTURE.md:**
- Inside Design Tokens: The Three Class Token Society — Three-tier hierarchy (primitive, semantic, component)
- Style Dictionary: Design Tokens — Official token hierarchy documentation
- Naming Tokens in Design Systems (Nathan Curtis, EightShapes) — Component token naming conventions
- Token Studio: Token Sets — Token organization, free tier limitations
- W3C DTCG Specification v1.0 (Oct 2025) — Design token format standard

**From PITFALLS.md:**
- Component-level Design Tokens: are they worth it? (Nate Baldwin) — Real-world 500+ token explosion example
- Design Tokens in Practice: Figma Variables to Production Code — "Halfway implementation" warning
- The context dilemma: design tokens and components — Component token integration patterns
- Best Practices For Naming Design Tokens (Smashing Magazine 2024) — Naming conventions

### Secondary (MEDIUM confidence)

**From STACK.md:**
- Smashing Magazine: Best Practices For Naming Design Tokens (2024) — CSS property-based naming for components
- Cloud Four: Component-Specific Design Tokens — Button/form component token examples
- design.dev: Design Systems & Design Tokens Complete Guide — 3-tier hierarchy (global → alias → component)

**From FEATURES.md:**
- DesignRush: Button States Explained — Modern button state patterns
- LogRocket: Designing Button States — State-based variations
- Sitelint: Definitive Guide to Indeterminate Checkbox State — Checkbox indeterminate state
- Contentful: Design Tokens Explained — Token architecture
- Martin Fowler: Design Token-Based UI Architecture — Component tokens first approach

**From ARCHITECTURE.md:**
- The Pyramid Design Token Structure (Stefanie Fluin) — Token naming and structure
- Tetrisly Design System: Design Tokens Architecture — Taxonomy and organization
- Managing And Exporting Design Tokens With Style Dictionary (Michael Mang) — File structure patterns
- Nord Design System: Naming — Component naming conventions
- Carbon Button Component — IBM Carbon button tokens

**From PITFALLS.md:**
- Design System Mastery with Figma Variables: 2025/2026 Best-Practice Playbook — Figma integration
- Understanding Differences Between Figma Variables and Design Tokens (Supernova) — Tooling distinctions
- Refactoring Token Names for Seamless Design System Maintenance — Token migration patterns
- Use design tokens to customise Bootstrap (smth.uk) — Bootstrap integration

### Tertiary (LOW confidence)

**From STACK.md:**
- Token Studio Plugin documentation (blocked by 403, couldn't verify free tier limits) — Inferred from v1.0 merge script necessity

**From PITFALLS.md:**
- Token Studio free tier cross-file reference limitations — Not explicitly documented, inferred from v1.0 merge script requirement
- Bootstrap CSS variable limitations (GitHub issue #26596) — Bootstrap 5.3+ uses --bs- prefix, potential collision needs validation

### v1.0 Project Learnings (HIGH confidence)

- 192 tokens (160 core + 32 semantic) proved overwhelming in Figma Token Studio interface
- Token Studio free tier requires merged file; cross-file references don't resolve
- Figma-centric naming (fill, stroke) poor for developer adoption
- Manual build process works but requires discipline (automation needed for v2.0)
- Style Dictionary v5.3.0 + @tokens-studio/sd-transforms v2.0.3 stable, no issues
- ES module support required in forms-flow-theme/package.json ("type": "module")
- --ff- prefix established for all CSS custom properties (192 existing tokens use this)

---

**Research completed:** 2026-02-10
**Ready for roadmap:** Yes
**Recommended next step:** Proceed to requirements definition with 6-phase roadmap structure outlined above.
