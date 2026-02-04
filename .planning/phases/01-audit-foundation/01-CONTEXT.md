# Phase 1: Audit & Foundation - Context

**Gathered:** 2026-02-04
**Status:** Ready for planning

<domain>
## Phase Boundary

Identify all design values in the forms-flow-theme SCSS codebase and component micro-frontends, document them with full traceability, and define the W3C DTCG token structure (folder layout, file conventions, naming rules). No actual token JSON files are created in this phase — structure is documented, extraction happens in Phase 2.

</domain>

<decisions>
## Implementation Decisions

### Audit Scope & Depth
- Theme-first approach: deep audit of forms-flow-theme, lighter pass on component micro-frontends scanning for hardcoded values that should be tokens
- Hardcoded values in components: report unique values only, with count of occurrences (deduplicated)
- Full traceability: each variable/property documented with name, computed value, and list of files/components that reference it
- Bootstrap overrides: Claude's discretion on whether to capture original Bootstrap defaults alongside overrides (based on what's useful for extraction)

### Token Organization
- Two tiers: core (primitives) and semantic (purpose-based). Component-tier tokens deferred — can be added later if needed
- One file per tier: tokens/core.json and tokens/semantic.json
- Token files live at project root: tokens/ directory alongside existing packages
- Phase 1 is documentation only — define the structure in spec docs, actual JSON files created in Phase 2

### Naming Conventions
- Project prefix: ff- (formsflow) on all tokens (e.g., ff.color.primary, ff.spacing.md)
- Bootstrap-originated names kept as-is: ff.color.primary, ff.color.secondary (familiar to devs)
- Spacing/sizing: t-shirt sizes (ff.spacing.xs, ff.spacing.sm, ff.spacing.md, ff.spacing.lg, ff.spacing.xl)
- Color shades: numeric scale (ff.color.primary-100 through ff.color.primary-900)

### Audit Output Format
- Dual format: JSON as source of truth, with generated markdown summary for human review
- Primary grouping by token type (all colors together, all spacing together, etc.)
- Gap analysis in separate dedicated report: each hardcoded component value listed with source component and suggested token name
- Audit output files live in tokens/audit/ (co-located with where tokens will eventually live)

### Claude's Discretion
- Whether to capture original Bootstrap defaults alongside overrides
- Exact JSON schema for audit data files
- Markdown summary formatting and level of detail
- How to handle SCSS computed values (functions, mixins, darken/lighten calls)

</decisions>

<specifics>
## Specific Ideas

No specific requirements — open to standard approaches

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 01-audit-foundation*
*Context gathered: 2026-02-04*
