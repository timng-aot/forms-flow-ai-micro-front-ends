# Requirements: Design Token Extraction

**Defined:** 2026-02-03
**Core Value:** Accurate extraction of design values from forms-flow-theme for Figma Variable libraries

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Audit — Shared Theme

- [ ] **AUDIT-01**: Identify all SCSS variables in `forms-flow-theme/scss`
- [ ] **AUDIT-02**: Identify all CSS custom properties in `forms-flow-theme/scss`
- [ ] **AUDIT-03**: Categorize variables into token types (color, spacing, typography, border-radius, shadow)
- [ ] **AUDIT-04**: Document computed values requiring manual handling (SCSS functions/mixins)
- [ ] **AUDIT-05**: Create audit report documenting findings and naming patterns

### Audit — Component Micro-Frontends

- [ ] **AUDIT-06**: Scan SCSS/CSS files in forms-flow-admin for hardcoded design values
- [ ] **AUDIT-07**: Scan SCSS/CSS files in forms-flow-nav for hardcoded design values
- [ ] **AUDIT-08**: Scan SCSS/CSS files in forms-flow-review for hardcoded design values
- [ ] **AUDIT-09**: Scan SCSS/CSS files in forms-flow-submissions for hardcoded design values
- [ ] **AUDIT-10**: Scan SCSS/CSS files in forms-flow-components for hardcoded design values
- [ ] **AUDIT-11**: Categorize component values by token type (color, spacing, typography, radius, shadow)
- [ ] **AUDIT-12**: Identify values used in components but missing from shared theme (gap analysis)
- [ ] **AUDIT-13**: Document component-specific values that should become shared tokens

### Color Tokens

- [ ] **COLOR-01**: Extract primitive color tokens (brand colors, grays, semantic colors)
- [ ] **COLOR-02**: Create semantic color tokens referencing primitives (primary, surface, text, etc.)
- [ ] **COLOR-03**: Add $description to all color tokens documenting usage

### Spacing Tokens

- [ ] **SPACE-01**: Extract primitive spacing tokens from spacer variables
- [ ] **SPACE-02**: Create semantic spacing tokens for common patterns (padding, gaps)
- [ ] **SPACE-03**: Add $description to all spacing tokens documenting usage

### Typography Tokens

- [ ] **TYPE-01**: Extract font family tokens
- [ ] **TYPE-02**: Extract font size tokens (--font-size-xs through --font-size-xxl)
- [ ] **TYPE-03**: Extract font weight tokens
- [ ] **TYPE-04**: Extract line height tokens
- [ ] **TYPE-05**: Create semantic typography tokens for text styles
- [ ] **TYPE-06**: Add $description to all typography tokens documenting usage

### Border Radius Tokens

- [ ] **RADIUS-01**: Extract primitive border radius tokens (--radius-sm through --radius-modal)
- [ ] **RADIUS-02**: Create semantic radius tokens for component patterns
- [ ] **RADIUS-03**: Add $description to all radius tokens documenting usage

### Shadow Tokens

- [ ] **SHADOW-01**: Extract primitive shadow tokens (--shadow-sm through --shadow-2xl)
- [ ] **SHADOW-02**: Create semantic shadow tokens for elevation patterns
- [ ] **SHADOW-03**: Add $description to all shadow tokens documenting usage

### Token Format

- [ ] **FORMAT-01**: All tokens use W3C DTCG format ($value, $type properties)
- [ ] **FORMAT-02**: Token names follow DTCG naming restrictions (no $, {, }, . in names)
- [ ] **FORMAT-03**: Semantic tokens use curly brace reference syntax ({group.token})
- [ ] **FORMAT-04**: Tokens organized in primitive/semantic group hierarchy

### Extraction Tooling

- [ ] **TOOL-01**: Create automated script to parse SCSS variables
- [ ] **TOOL-02**: Create automated script to parse CSS custom properties
- [ ] **TOOL-03**: Script outputs W3C DTCG-compliant JSON
- [ ] **TOOL-04**: Script handles unit conversion (preserves rem units)

### Build Pipeline

- [ ] **BUILD-01**: Configure Style Dictionary v4+ for token transformation
- [ ] **BUILD-02**: Integrate @tokens-studio/sd-transforms for Token Studio compatibility
- [ ] **BUILD-03**: Generate CSS custom properties output from tokens
- [ ] **BUILD-04**: Validate token JSON before transformation

### Documentation

- [ ] **DOCS-01**: Document token extraction methodology
- [ ] **DOCS-02**: Document token naming conventions used
- [ ] **DOCS-03**: Create usage guide for Token Studio import
- [ ] **DOCS-04**: Document any gaps or manual interventions required

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Organization

- **ORG-01**: Split tokens into multiple files (one per category)
- **ORG-02**: Configure Style Dictionary for multi-file token merging

### Component Tokens

- **COMP-01**: Create component-level token layer (3-tier hierarchy)
- **COMP-02**: Map components to semantic tokens

### Governance

- **GOV-01**: Token versioning with semver
- **GOV-02**: Deprecation strategy with $deprecated property
- **GOV-03**: Token change approval workflow

### Automation

- **AUTO-01**: Automated Figma sync via Token Studio GitHub integration
- **AUTO-02**: CI/CD pipeline for token validation

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| Codebase refactoring to consume tokens | Future phase; extract first, consume later |
| Extracting component-specific values as tokens | Audit only; gaps documented for future consolidation |
| Creating new token hierarchy | Match existing naming; restructure later |
| Figma-to-code generation | Downstream of token import; separate project |
| Multi-theme support (light/dark) | Not currently in codebase; defer |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| AUDIT-01 | Phase 1 | Pending |
| AUDIT-02 | Phase 1 | Pending |
| AUDIT-03 | Phase 1 | Pending |
| AUDIT-04 | Phase 1 | Pending |
| AUDIT-05 | Phase 1 | Pending |
| AUDIT-06 | Phase 1 | Pending |
| AUDIT-07 | Phase 1 | Pending |
| AUDIT-08 | Phase 1 | Pending |
| AUDIT-09 | Phase 1 | Pending |
| AUDIT-10 | Phase 1 | Pending |
| AUDIT-11 | Phase 1 | Pending |
| AUDIT-12 | Phase 1 | Pending |
| AUDIT-13 | Phase 1 | Pending |
| FORMAT-01 | Phase 1 | Pending |
| FORMAT-02 | Phase 1 | Pending |
| FORMAT-03 | Phase 1 | Pending |
| FORMAT-04 | Phase 1 | Pending |
| COLOR-01 | Phase 2 | Pending |
| COLOR-02 | Phase 2 | Pending |
| COLOR-03 | Phase 2 | Pending |
| SPACE-01 | Phase 2 | Pending |
| SPACE-02 | Phase 2 | Pending |
| SPACE-03 | Phase 2 | Pending |
| TYPE-01 | Phase 2 | Pending |
| TYPE-02 | Phase 2 | Pending |
| TYPE-03 | Phase 2 | Pending |
| TYPE-04 | Phase 2 | Pending |
| TYPE-05 | Phase 2 | Pending |
| TYPE-06 | Phase 2 | Pending |
| RADIUS-01 | Phase 2 | Pending |
| RADIUS-02 | Phase 2 | Pending |
| RADIUS-03 | Phase 2 | Pending |
| SHADOW-01 | Phase 2 | Pending |
| SHADOW-02 | Phase 2 | Pending |
| SHADOW-03 | Phase 2 | Pending |
| TOOL-01 | Phase 2 | Pending |
| TOOL-02 | Phase 2 | Pending |
| TOOL-03 | Phase 2 | Pending |
| TOOL-04 | Phase 2 | Pending |
| BUILD-01 | Phase 3 | Pending |
| BUILD-02 | Phase 3 | Pending |
| BUILD-03 | Phase 3 | Pending |
| BUILD-04 | Phase 3 | Pending |
| DOCS-01 | Phase 4 | Pending |
| DOCS-02 | Phase 4 | Pending |
| DOCS-03 | Phase 4 | Pending |
| DOCS-04 | Phase 4 | Pending |

**Coverage:**
- v1 requirements: 46 total
- Mapped to phases: 46
- Unmapped: 0

---
*Requirements defined: 2026-02-03*
*Last updated: 2026-02-03 after roadmap creation*
