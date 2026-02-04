# Project Research Summary

**Project:** Design Token Extraction from SCSS to Figma
**Domain:** Design System / Design Token Management
**Researched:** 2026-02-03
**Confidence:** HIGH

## Executive Summary

Design token extraction in 2026 follows a JSON-first workflow where the W3C Design Tokens Community Group (DTCG) specification (v1.0 stable, October 2025) serves as the interchange format. The critical finding is that extracting FROM SCSS is an anti-pattern—modern best practice treats JSON as the source of truth and transforms TO platform outputs (SCSS, CSS, JS). For an existing SCSS codebase like forms-flow-ai-micro-front-ends, this requires a one-time migration rather than ongoing extraction.

The recommended approach uses a three-tier token architecture (primitive → semantic → component) with a multi-file organization strategy. Style Dictionary v4+ handles transformation from W3C DTCG JSON to platform outputs, while Tokens Studio for Figma provides the design-to-code sync. The existing Bootstrap 5 SCSS foundation contains approximately 60 variables spanning colors, spacing, typography, border radius, and shadows—all of which map cleanly to DTCG token types.

Key risks center on format compliance (missing `$type` properties), naming restrictions (reserved characters break toolchains), and extraction granularity (over-extracting creates maintenance burden, under-extracting loses semantic meaning). Mitigation requires manual extraction with semantic restructuring, strict W3C DTCG format adherence from the start, and a phased approach that establishes primitives before building semantic and component layers.

## Key Findings

### Recommended Stack

The 2025/2026 standard stack has consolidated around W3C DTCG as the universal interchange format, with Style Dictionary v4+ as the transformation engine and Tokens Studio as the Figma integration layer. The critical shift is JSON-first workflows: establish JSON as source of truth, then generate platform outputs.

**Core technologies:**
- **W3C DTCG Specification v1.0** (October 2025): Industry standard format with first-class support from Adobe, Amazon, Google, Microsoft, Meta, and Figma
- **Style Dictionary v5.2.0+**: Transformation engine with native DTCG support, generates CSS/SCSS/JS/iOS/Android from single JSON source
- **@tokens-studio/sd-transforms v2.0.1+**: Required middleware bridging Tokens Studio token types to DTCG standard types
- **Tokens Studio for Figma**: De facto standard plugin for syncing tokens between JSON files and Figma Variables/Styles
- **Manual extraction**: Recommended for one-time SCSS-to-JSON migration (automated tools unmaintained for 4-7 years, depend on deprecated node-sass)

**Critical context:** This is a one-time migration task, not an ongoing workflow. After migration, JSON becomes the source of truth and Style Dictionary generates SCSS outputs.

### Expected Features

The feature landscape is defined by W3C DTCG compliance requirements and Tokens Studio compatibility constraints. The five target categories (colors, spacing, typography, border radius, shadows) are all officially supported token types.

**Must have (table stakes):**
- W3C DTCG format compliance with `$value`, `$type`, `$description` properties
- Core token categories matching official DTCG types: `color`, `dimension`, `typography` (composite), `shadow` (composite)
- Hierarchical token organization with groups (objects without `$value`) and tokens (objects with `$value`)
- Token aliasing/referencing using `{group.token}` syntax for semantic abstraction
- Style Dictionary integration with `@tokens-studio/sd-transforms` package (hard dependency)
- Multi-file token organization for maintainability and Tokens Studio Themes feature

**Should have (competitive):**
- Component-level tokens (third tier) bridging semantic tokens to UI components
- Token metadata and documentation via `$description` fields
- Multi-file organization by category (colors.json, spacing.json, typography.json)
- Deprecation strategy using `$deprecated` property for safe token evolution
- Token versioning for API-like change management

**Defer (v2+):**
- Automated SCSS extraction tooling (manual migration acceptable for ~60 variables)
- Theme support (light/dark modes) using `$themes.json` configuration
- Cross-file references for complex token relationships
- Token transformer preprocessing for advanced Tokens Studio features

**Anti-features (explicitly avoid):**
- Component-specific primitive tokens (defeats purpose of abstraction)
- Over-engineering on first pass (creating hundreds of unused tokens)
- Pixel-based dimension values (breaks accessibility, use rem/em)
- Mixing W3C DTCG and legacy formats in same instance
- Direct primitive token usage in components (violates semantic layer)
- Reserved characters in token names (`$`, `{}`, `.`, `/`, spaces)
- Lack of team documentation and governance process

### Architecture Approach

Design tokens follow a three-tier hierarchical architecture with multi-file organization by category. Files are structured as core/semantic/component folders with JSON files per token category, enabling Style Dictionary's deep merge strategy and Tokens Studio's multi-file sync requirements.

**Major components:**

1. **Core (Primitive) Tokens** — Foundation layer with raw CSS values, no dependencies, named `{category}.{attribute}.{scale}` (e.g., `colors.blue.500`, `spacing.base`). Used internally for reference, not directly in application code.

2. **Semantic Tokens** — Context layer providing meaning to primitives, references core tokens using `{path}` syntax, named `{context}.{role}.{variant}` (e.g., `color.action.primary` → `{colors.blue.500}`). Preferred for most application usage.

3. **Component Tokens** — Component-specific design decisions, can reference any tier, named `{component}.{element}.{property}.{state}` (e.g., `button.primary.background.default` → `{color.action.primary}`). Most specific level used when available.

**File structure:** Multi-file organization (tokens/core/, tokens/semantic/, tokens/component/) with category-based JSON files (colors.json, spacing.json, typography.json, borders.json, shadows.json). `$themes.json` and `$metadata.json` as separate Token Studio configuration files.

**Naming conventions:** Kebab-case for token names with period delimiters for grouping, avoiding reserved characters (`$`, `{}`, `.`, `/`, brackets, spaces). Numeric scales use text for fractional values (`spacing.1half` not `spacing.1.5` to prevent flattening collisions).

**Integration flow:** JSON files (Git) → Style Dictionary transform → SCSS/CSS/JS outputs → React components. Parallel: JSON files → Tokens Studio sync → Figma Variables/Styles → designers.

### Critical Pitfalls

From PITFALLS.md, the most dangerous issues that cause rewrites or project blockage:

1. **Missing `$type` or incorrect DTCG format** — Using legacy `"type"/"value"` instead of `"$type"/"$value"` causes validation failures and Token Studio import rejection. W3C DTCG format is non-negotiable; use it from day one. Type values changed (`"size"` → `"dimension"`), requiring manual updates that automated converters miss.

2. **Token names using reserved characters** — Names with `$`, `{}`, `.`, `/`, `[]`, `()`, or spaces break parsing, cause reference failures, and prevent Token Studio import. Naming restrictions differ across tools (Figma uses `/` for grouping, DTCG forbids `$` prefix, references use `{}`). Validation must happen before extraction.

3. **CSS custom property interpolation missing** — SCSS variables assigned to CSS custom properties require `#{...}` interpolation syntax or they appear as literal text (`--color: $primary-blue`) instead of resolved values. This is a Sass parsing requirement that extraction scripts must handle.

4. **Broken token references after filtering** — Using `outputReferences: true` with filters creates dangling references when referenced tokens are filtered out. Style Dictionary's `outputReferencesFilter` utility solves this by only outputting references when target tokens exist in the same file.

5. **Over-extraction (token explosion)** — Extracting every SCSS variable without editorial judgment creates hundreds of tokens, overwhelming designers and causing maintenance burden. Start with 5 core categories and ~80 tokens for MVP, not 200+ speculatively.

6. **Under-extraction (missing semantic layer)** — Extracting only primitive values without semantic aliases creates brittle designs. Rebrand requires changing 100 components instead of 1 token. Three-tier structure (primitive → semantic → component) is non-negotiable for maintainability.

## Implications for Roadmap

Based on research, the project should follow a five-phase structure with clear dependencies and validation gates:

### Phase 1: Foundation Setup & Core Token Extraction
**Rationale:** Must establish JSON structure and extract primitives before any higher-tier tokens can reference them. W3C DTCG compliance is prerequisite for everything that follows.

**Delivers:**
- Multi-file folder structure (tokens/core/, tokens/semantic/, tokens/component/)
- Core primitive tokens extracted from SCSS (~50 tokens: colors, spacing, typography, borders, shadows)
- W3C DTCG format compliance validated
- Naming convention enforcement (kebab-case, no reserved characters)

**Addresses:**
- W3C DTCG format compliance (table stakes)
- Core 5 token categories (table stakes)
- Multi-file organization (competitive feature)

**Avoids:**
- Reserved character pitfalls (critical)
- CSS custom property interpolation issues (critical)
- Over-extraction (moderate) — use inclusion list, not "extract everything"

**Dependency:** None, this is the foundation.

### Phase 2: Semantic Token Layer & Aliasing
**Rationale:** Semantic tokens provide meaning and abstraction, enabling theme changes without touching primitives. Must come after primitives exist but before components reference tokens.

**Delivers:**
- Semantic token layer with ~30 alias tokens
- Token references using `{group.token}` syntax
- `$description` documentation for all semantic tokens
- Reference validation ensuring all aliases resolve

**Uses:**
- Style Dictionary v5.2+ reference resolution
- `@tokens-studio/sd-transforms` for token type mapping

**Implements:**
- Three-tier architecture (semantic layer)
- Token aliasing/referencing pattern

**Addresses:**
- Token aliasing/referencing (table stakes)
- Token metadata documentation (competitive)

**Avoids:**
- Under-extraction pitfall (moderate) — semantic layer is mandatory
- Component-coupled naming (moderate) — use intent-based names

**Dependency:** Requires Phase 1 (core tokens must exist to be referenced).

### Phase 3: Style Dictionary Integration & Build Pipeline
**Rationale:** Can happen parallel to Phase 2 once core tokens exist. Enables platform output generation and validates that token structure works with transformation tooling.

**Delivers:**
- Style Dictionary configuration with DTCG format support
- CSS custom property output for React components
- SCSS variable output maintaining compatibility with existing codebase
- JavaScript/TypeScript token exports for typed usage
- Automated build validation (reference resolution, schema validation)

**Uses:**
- Style Dictionary v5.2+ with native DTCG support
- `@tokens-studio/sd-transforms` v2.0.1+ middleware
- `outputReferencesFilter` utility for safe reference handling

**Implements:**
- Technology integration point from ARCHITECTURE.md
- Transformation pipeline (JSON → platform outputs)

**Addresses:**
- Style Dictionary integration (table stakes)
- Platform output generation

**Avoids:**
- Broken references pitfall (critical) — use `outputReferencesFilter`
- Format mixing pitfall (moderate) — DTCG-only, no legacy

**Dependency:** Requires Phase 1 (core tokens). Can run parallel to Phase 2.

### Phase 4: Token Studio Integration & Figma Sync
**Rationale:** Once token JSON is validated via Style Dictionary, integrate with design tool. Tests end-to-end workflow (Figma → JSON → code).

**Delivers:**
- Tokens Studio plugin configured with GitHub sync
- Multi-file import into Figma Variables/Styles
- Bidirectional sync workflow (designer updates → Git → build)
- Token Studio format validation (W3C DTCG mode enabled)
- Documentation for team token workflow

**Uses:**
- Tokens Studio for Figma latest version
- GitHub Personal Access Token with repo scope
- Multi-file folder export/import

**Implements:**
- Token Studio integration point from ARCHITECTURE.md
- Design-to-code sync workflow

**Addresses:**
- Tokens Studio compatibility (table stakes)
- Multi-file organization (competitive) — required for Themes feature

**Avoids:**
- Token Studio sync errors (minor) — correct PAT setup, no leading slashes in paths
- Schema validation failures (minor) — validate before import

**Dependency:** Requires Phase 1 (valid DTCG JSON) and Phase 3 (validated token structure).

### Phase 5: Component Tokens & Documentation (Post-MVP)
**Rationale:** Component tokens require component inventory and usage pattern analysis. Defer until semantic tokens proven stable for 1-2 months.

**Delivers:**
- Component token layer (~30 tokens for buttons, modals, tables, forms)
- Complete reference chains (component → semantic → primitive)
- Usage documentation with examples
- Governance process for token changes

**Addresses:**
- Component-level tokens (competitive feature)
- Token versioning (competitive feature)
- Deprecation strategy (competitive feature)

**Avoids:**
- Component-specific primitive tokens (anti-feature)
- Overspecific component-coupled naming (moderate)

**Dependency:** Requires Phase 1 + Phase 2 (primitives and semantics established).

### Phase Ordering Rationale

- **Foundation-first:** Core tokens have zero dependencies and are referenced by all higher tiers. Must be extracted first or semantic/component tokens have nothing to reference.
- **Semantic before components:** Semantic layer provides abstraction that components should use. Building components directly on primitives violates architecture pattern.
- **Build pipeline parallel:** Style Dictionary can be configured once core tokens exist, doesn't need to wait for semantic layer completion.
- **Figma integration last:** Validates the complete token structure but isn't a dependency for other phases. Can be deferred if design tool sync isn't immediate priority.
- **Components post-MVP:** Highest complexity, most dependencies, requires component inventory that may not exist yet.

### Research Flags

**Phases likely needing deeper research during planning:**
- **Phase 5 (Component Tokens):** Requires component inventory and usage pattern analysis before determining which component tokens are needed. May need research into component-specific patterns.
- **Future: Theme Support:** If light/dark mode or brand variants needed, research Token Studio's `$themes.json` configuration and theme-specific token organization.
- **Future: Complex Calculations:** If advanced math expressions needed beyond simple references, research Token Studio vs Style Dictionary math evaluation capabilities.

**Phases with standard patterns (skip research-phase):**
- **Phase 1 (Core Extraction):** Well-documented pattern, SCSS variable extraction is straightforward for primitive values.
- **Phase 2 (Semantic Layer):** Industry-standard three-tier architecture, extensively documented in design token literature.
- **Phase 3 (Style Dictionary):** Mature tooling with comprehensive documentation and large ecosystem.
- **Phase 4 (Tokens Studio):** De facto standard plugin with official documentation and troubleshooting guides.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | **HIGH** | W3C DTCG v1.0 stable (Oct 2025), Style Dictionary proven at enterprise scale (Amazon, Adobe, Shopify), Tokens Studio de facto standard |
| Features | **HIGH** | All 5 target categories officially supported by DTCG spec and Tokens Studio, table stakes features clearly defined by industry standards |
| Architecture | **HIGH** | Three-tier pattern (primitive/semantic/component) is industry consensus, multi-file organization validated by Style Dictionary and Token Studio requirements |
| Pitfalls | **HIGH** | Critical pitfalls verified with official documentation (W3C spec, Sass docs, Token Studio troubleshooting), moderate pitfalls synthesized from multiple authoritative sources |

**Overall confidence:** **HIGH**

All core findings verified with official specifications (W3C DTCG v1.0, Sass documentation, Style Dictionary v5 docs, Token Studio official guides). Technology choices reflect 2025/2026 ecosystem consolidation around DTCG standard. Project-specific analysis based on actual codebase inspection (~60 SCSS variables identified, Bootstrap 5 foundation confirmed).

### Gaps to Address

- **SCSS computed values:** Current codebase uses calculations like `$borderRadiusModal: $base*1.5`. During extraction, these need manual evaluation (0.5rem * 1.5 = 0.75rem) since SCSS functions can't be directly tokenized. Accept that dynamic patterns won't be preserved.

- **Component inventory completeness:** Phase 5 (component tokens) requires knowing which components exist and their token usage patterns. This information isn't available from SCSS extraction alone—needs component library audit.

- **Team workflow readiness:** Token Studio GitHub sync requires team members to have appropriate PATs and understand feature branch workflow. Plan training/onboarding before Phase 4.

- **Existing SCSS deprecation strategy:** After migration, generated SCSS files will replace hand-authored SCSS variables. Define how to transition existing component imports from old `_variables.scss` to generated `_tokens.scss` without breaking builds.

## Sources

### Primary (HIGH confidence)
- [W3C Design Tokens Format Module 2025.10](https://www.designtokens.org/tr/drafts/format/) — Official specification
- [Design Tokens Specification Stable Release Announcement](https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/) — W3C official announcement
- [Token Studio for Figma Documentation](https://docs.tokens.studio) — Official plugin documentation
- [Style Dictionary Official Documentation](https://styledictionary.com/) — Transformation engine documentation
- [Sass Breaking Changes: CSS Variables](https://sass-lang.com/documentation/breaking-changes/css-vars/) — Official Sass documentation
- [LibSass/node-sass Deprecation](https://sass-lang.com/blog/libsass-is-deprecated/) — Official Sass blog

### Secondary (MEDIUM confidence)
- [Design Token Management Tools 2025](https://cssauthor.com/design-token-management-tools/) — Industry tool comparison
- [Design Tokens Beyond Colors, Typography, Spacing](https://medium.com/bumble-tech/design-tokens-beyond-colors-typography-and-spacing-ad7c98f4f228) — Bumble Tech design token categories
- [Common Mistakes in Design Tokens Adoption](https://designtokens.substack.com/p/common-mistakes-in-design-tokens) — Design token best practices newsletter
- [Naming Tokens in Design Systems](https://medium.com/eightshapes-llc/naming-tokens-in-design-systems-9e86c7444676) — Nathan Curtis naming patterns
- [Design Token System](https://www.contentful.com/blog/design-token-system/) — Contentful implementation guide

### Tertiary (validation needed)
- [@tokens-studio/sd-transforms npm](https://www.npmjs.com/package/@tokens-studio/sd-transforms) — Package documentation
- [token-transformer npm](https://www.npmjs.com/package/token-transformer) — Preprocessing tool documentation
- [scss-to-json npm](https://www.npmjs.com/package/scss-to-json) — Legacy extraction tool (unmaintained)

---
*Research completed: 2026-02-03*
*Ready for roadmap: yes*
