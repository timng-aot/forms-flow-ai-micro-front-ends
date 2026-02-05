# Phase 2: Token Extraction - Context

**Gathered:** 2026-02-04
**Status:** Ready for planning

<domain>
## Phase Boundary

Extract all design values from forms-flow-theme into W3C DTCG-formatted JSON files (tokens/core.json, tokens/semantic.json), organized by category (colors, spacing, typography, border-radius, shadows) with automated extraction scripts and validation. Missing component values are documented as gaps, not tokenized. Replaces Phase 1 example files with production token files.

</domain>

<decisions>
## Implementation Decisions

### Extraction approach
- Claude's discretion on whether to extend Phase 1 audit scripts or build new dedicated extractors
- Computed SCSS expressions: resolve to final values AND preserve original expression in $description (dual tracking)
- Claude's discretion on unified vs per-category script architecture
- Scripts live in top-level `scripts/` directory

### Token organization
- V8 design system values only — legacy values excluded UNLESS actively used in components
- Active legacy values (Bootstrap semantics like primary, secondary) included with $description noting legacy origin
- Claude's discretion on category nesting structure within files (groups vs flat prefixes)
- $description fields include both origin (source SCSS variable) AND usage context (what it's used for)

### Edge case handling
- 18 missing component values: document as gaps only — do NOT create new tokens for them
- Bootstrap overrides ($primary, $secondary, etc.): Claude's discretion on mapping to v8 equivalents vs extracting as-is
- SCSS function expressions (darken, lighten, mix): Claude's discretion on preserving relationship info
- V8 @each loop palettes: extract FULL palette (all generated values), not just referenced ones

### Output validation
- Automated diff script compares extracted token values against Phase 1 audit data — flags mismatches
- Full DTCG validation: valid $type on every token, all {references} resolve, $description present, no duplicate names, schema-valid JSON
- Claude's discretion on report format (file vs console)
- Final token files written directly to tokens/core.json and tokens/semantic.json (replace Phase 1 examples)

### Claude's Discretion
- Script architecture: extend audit scripts vs new extractors, unified vs per-category
- Category nesting within JSON files
- Bootstrap override mapping strategy
- SCSS function expression handling in descriptions
- Validation report format

</decisions>

<specifics>
## Specific Ideas

- Dual value tracking pattern established in Phase 1: token $value is the computed result, $description preserves the original SCSS expression
- Phase 1 decision: v8 design system values take precedence over legacy where conflicts exist
- Full color palettes from @each loops (100-900 scales) should be complete even if some shades aren't currently used — Figma needs complete scales
- Token naming convention from Phase 1: ff-{category}-{descriptor}, kebab-case, no reserved characters

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 02-token-extraction*
*Context gathered: 2026-02-04*
