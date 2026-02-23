# Phase 5: Architecture & Integration Planning - Context

**Gathered:** 2026-02-23
**Status:** Ready for planning

<domain>
## Phase Boundary

Define the component token architecture that integrates with v1.0 core/semantic tokens. Covers token hierarchy, naming conventions, file structure, and variant/state coverage for buttons and forms. Does not create the actual component tokens (Phase 6-7) or update the build pipeline (Phase 8).

</domain>

<decisions>
## Implementation Decisions

### Token hierarchy depth
- Max 3 reference levels: component → semantic → core
- Skip semantic layer when it adds no value — component can reference core directly when obvious
- When multiple components share the same value, create a shared semantic token (don't have independent core references)
- Expand the v1.0 semantic.json with new semantic tokens as needed to support component references (e.g. action.primary, feedback.error)

### Naming structure
- Dot-separated groups following W3C DTCG nesting: `button.primary.hover.background`
- Segment order: **component.variant.state.property** (industry standard)
- Default state is omitted — `button.primary.background` implies default; state only appears for hover/active/focus/disabled
- CSS custom properties mirror dot path directly: `button.primary.hover.background` → `--ff-button-primary-hover-background`
- No abbreviations in generated CSS vars — full readable names

### File organization
- Single `components.json` file containing both button and form token sections
- New semantic tokens added to existing `semantic.json` (extend, not separate file)
- Merged Token Studio file (`tokens.json`) includes core + semantic + components — single import
- Keep v1.0 `core.json` complete but flag unused tokens (don't prune yet)

### Variant & state coverage
- **Button variants:** primary, secondary, outline, danger — core variants only, not every codebase variant
- **Interactive states:** full set — default, hover, active, focus, disabled
- **CSS properties per token:** visual properties only — background, border-color, color (text), shadow
- **Shared tokens for static properties:** when a property doesn't change across states (e.g. border-radius), use a shared token without state segment rather than duplicating per-state

### Claude's Discretion
- Exact semantic token names for shared component values
- How to flag unused core tokens (comment, metadata, or separate mapping)
- Form element variant breakdown (inputs, selects, checkboxes, radios — how granular)
- Whether border-width and font properties warrant tokens for base component definition (non-state-changing)

</decisions>

<specifics>
## Specific Ideas

- CSS property naming model confirmed: background, border-color, color, shadow (not Figma's fill/stroke/effect)
- Token Studio free tier constraint drives single merged file approach
- The architecture should make it obvious which v1.0 tokens are actually used vs. orphaned

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 05-architecture-integration-planning*
*Context gathered: 2026-02-23*
