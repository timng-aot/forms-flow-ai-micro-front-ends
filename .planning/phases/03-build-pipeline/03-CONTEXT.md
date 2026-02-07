# Phase 3: Build Pipeline - Context

**Gathered:** 2026-02-06
**Status:** Ready for planning

<domain>
## Phase Boundary

Configure Style Dictionary to transform W3C DTCG token JSON (tokens/core.json + tokens/semantic.json) into CSS custom properties, with pre-computation of unresolved SCSS expressions and validation for Token Studio importability. Output sits alongside the existing theme — no replacement of current styles.

</domain>

<decisions>
## Implementation Decisions

### Output targets
- CSS custom properties only (no SCSS variables or JS/TS output)
- Use --ff- prefix for all CSS variables (e.g. --ff-color-primary, --ff-spacing-100)
- Single CSS file per token source: core-tokens.css and semantic-tokens.css (separate, not merged)
- Semantic CSS vars reference core CSS vars, preserving the layering

### Unresolved SCSS expressions
- Pre-compute blend-with-white-to-hex() values BEFORE Style Dictionary runs
- Standalone rerunnable script that reads core.json, resolves expressions, writes back resolved hex values
- Only handle blend-with-white-to-hex() — no other unresolved patterns exist
- Clean hex values only in token files — no preservation of original expressions (audit artifacts document originals)

### Token Studio round-trip
- Pure W3C DTCG format (no Token Studio-specific extensions)
- Figma becomes source of truth after initial import — tokens flow from Figma to code in the future
- Style Dictionary pipeline validates that source token JSON is Token Studio-importable (validation in pipeline, not deferred to Phase 4)
- Design Style Dictionary config for bidirectional use — same token format works whether source is code-extracted or Figma-exported JSON
- Future Figma-to-code reverse pipeline is planned — Phase 3 config should accommodate this direction

### Integration with existing build
- Generated CSS sits alongside existing theme (tokens/dist/) — no replacement of forms-flow-theme
- Consumers opt-in to token CSS when ready
- npm script ("build:tokens") added for triggering Style Dictionary build
- Output location: tokens/dist/ (keeps all token-related files together)

### Claude's Discretion
- Whether to use resolved token files directly for Token Studio import or produce a separate export (pick based on maintenance burden)
- Whether to preserve core/semantic split as separate token sets in Figma or merge (pick based on Token Studio best practices)
- Where to install Style Dictionary devDependencies — root or forms-flow-theme package.json (pick based on monorepo structure)

</decisions>

<specifics>
## Specific Ideas

- Bidirectional pipeline design: the same Style Dictionary config should work for both code-to-Figma and future Figma-to-code directions
- Token files should be self-contained after pre-computation (no SCSS runtime dependencies)
- The blend-with-white-to-hex() function blends a base color with white at a given ratio — mathematically straightforward to resolve

</specifics>

<deferred>
## Deferred Ideas

- Figma-to-code reverse pipeline (export from Figma, transform to CSS) — future phase after Figma becomes source of truth
- Replacing forms-flow-theme SCSS with token-generated CSS — future migration phase
- Component-level consumption of token CSS variables — outside current scope

</deferred>

---

*Phase: 03-build-pipeline*
*Context gathered: 2026-02-06*
