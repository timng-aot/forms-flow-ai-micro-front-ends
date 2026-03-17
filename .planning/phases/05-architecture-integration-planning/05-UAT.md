---
status: testing
phase: 05-architecture-integration-planning
source: [05-01-SUMMARY.md, 05-02-SUMMARY.md]
started: 2026-02-24T00:30:00Z
updated: 2026-02-24T00:30:00Z
---

## Current Test
<!-- OVERWRITE each test - shows where we are -->

number: 1
name: Button reference map traces real SCSS indirection
expected: |
  Open `tokens/audit/component-token-reference-map.md`. The button section should cover all 4 variants (primary, secondary, error/danger, warning) with tables tracing each CSS property through: SCSS variable -> CSS custom property -> core token. Cross-check one entry against the actual SCSS file (e.g. `forms-flow-theme/scss/v8-scss/_button.scss`) — the traced path should match real code.
awaiting: user response

## Tests

### 1. Button reference map traces real SCSS indirection
expected: Open `tokens/audit/component-token-reference-map.md`. The button section should cover all 4 variants (primary, secondary, error/danger, warning) with tables tracing each CSS property through: SCSS variable -> CSS custom property -> core token. Cross-check one entry against the actual SCSS file (e.g. `forms-flow-theme/scss/v8-scss/_button.scss`) — the traced path should match real code.
result: [pending]

### 2. Form reference map covers text input and checkbox with gap analysis
expected: Same file, form section should trace text input properties from `_textInput.scss` and checkbox from `_checkbox.scss`. The checkbox `#8969f2` hardcoded hex gap should be explicitly called out with a recommendation (referencing nearest core token via `color.action.primary-selected`).
result: [pending]

### 3. New semantic tokens are fully specified
expected: The reference map's "New Semantic Tokens Needed" section lists 8 tokens with their core token references and rationale. Each entry should have: token name, `$value` reference (e.g. `{ff.color.primary-dark}`), and why the semantic layer adds value.
result: [pending]

### 4. Reference depth policy has concrete examples
expected: The depth policy section documents 3-level max rule (component -> semantic -> core) and the 2-level shortcut (component -> core when semantic adds no value). Should include at least one concrete example of each using real token paths from the audit (not hypothetical).
result: [pending]

### 5. Naming convention matches locked decisions
expected: Open `tokens/audit/naming-convention.md`. Verify segment order is `component.variant.state.property`. Default state omission rule should show `button.primary.background` (no state segment) vs `button.primary.hover.background`. Anti-patterns section should list at least 5 invalid naming examples with explanations.
result: [pending]

### 6. components.json stub builds with Style Dictionary
expected: Run `cd forms-flow-theme && npx style-dictionary build` (or the project's build command). The build should succeed without reference errors. `tokens/components.json` should contain `button.primary` (default + hover states) and `input.text` with all `$value` fields using reference syntax (no hardcoded hex values).
result: [pending]

### 7. Unused core tokens tracking is accurate
expected: Open `tokens/audit/unused-core-tokens.md`. Should show total count (85 core tokens), how many are referenced vs unreferenced (36 unreferenced). Spot-check one "unreferenced" token — it should NOT appear in the reference map or semantic.json.
result: [pending]

## Summary

total: 7
passed: 0
issues: 0
pending: 7
skipped: 0

## Gaps

[none yet]
