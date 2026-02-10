# Roadmap: Design Token Extraction

## Overview

This roadmap transforms the existing forms-flow-theme SCSS codebase into W3C DTCG-formatted JSON tokens for import into Figma. The journey starts with auditing shared styles and component files to understand what exists, then extracts design values across five categories (colors, spacing, typography, border radius, shadows) into properly formatted JSON files, builds the transformation pipeline using Style Dictionary, and concludes with comprehensive documentation. The end result is a validated set of design tokens that accurately reflect the codebase reality and can serve as the foundation for a design-to-code pipeline.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Audit & Foundation** - Identify design values and establish DTCG structure
- [x] **Phase 2: Token Extraction** - Extract tokens across all categories with tooling
- [x] **Phase 3: Build Pipeline** - Configure Style Dictionary transformation
- [ ] **Phase 4: Documentation & Validation** - Document methodology and validate outputs

## Phase Details

### Phase 1: Audit & Foundation
**Goal**: Team understands what design values exist in the codebase and has validated DTCG structure ready for token extraction.

**Depends on**: Nothing (first phase)

**Requirements**: AUDIT-01, AUDIT-02, AUDIT-03, AUDIT-04, AUDIT-05, AUDIT-06, AUDIT-07, AUDIT-08, AUDIT-09, AUDIT-10, AUDIT-11, AUDIT-12, AUDIT-13, FORMAT-01, FORMAT-02, FORMAT-03, FORMAT-04

**Success Criteria** (what must be TRUE):
  1. All SCSS variables and CSS custom properties in forms-flow-theme are documented with their computed values
  2. Component micro-frontends audited with hardcoded values categorized and gap analysis complete
  3. Two-file structure (tokens/core.json, tokens/semantic.json) defined and example files validate against W3C DTCG format requirements
  4. Token naming conventions defined (kebab-case, no reserved characters) with validation passing

**Plans**: 3 plans in 2 waves

Plans:
- [x] 01-01-PLAN.md -- Shared theme audit (SCSS variables + CSS custom properties)
- [x] 01-02-PLAN.md -- Component audit + gap analysis
- [x] 01-03-PLAN.md -- DTCG structure specification + example token validation

### Phase 2: Token Extraction
**Goal**: All design values from shared theme are extracted into W3C DTCG-formatted JSON files, organized by category with proper semantic structure.

**Depends on**: Phase 1 (audit must identify values before extraction)

**Requirements**: COLOR-01, COLOR-02, COLOR-03, SPACE-01, SPACE-02, SPACE-03, TYPE-01, TYPE-02, TYPE-03, TYPE-04, TYPE-05, TYPE-06, RADIUS-01, RADIUS-02, RADIUS-03, SHADOW-01, SHADOW-02, SHADOW-03, TOOL-01, TOOL-02, TOOL-03, TOOL-04

**Success Criteria** (what must be TRUE):
  1. Primitive and semantic tokens exist for all five categories (colors, spacing, typography, border-radius, shadows) with proper type annotations
  2. Token references use curly brace syntax and resolve correctly (no dangling references)
  3. All tokens include $description fields documenting their usage and origin
  4. Automated extraction scripts successfully parse SCSS variables and CSS custom properties, outputting valid DTCG JSON

**Plans**: 3 plans in 3 waves

Plans:
- [x] 02-01-PLAN.md -- Build extraction scripts and generate production token files (core.json + semantic.json)
- [x] 02-02-PLAN.md -- Validate tokens against DTCG schema, references, and audit data
- [x] 02-03-PLAN.md -- Gap closure: Add semantic radius and shadow tokens (closes RADIUS-02, SHADOW-02)

### Phase 3: Build Pipeline
**Goal**: Style Dictionary successfully transforms token JSON into CSS custom properties and SCSS outputs, with validation ensuring reference integrity.

**Depends on**: Phase 2 (tokens must exist before transformation)

**Requirements**: BUILD-01, BUILD-02, BUILD-03, BUILD-04

**Success Criteria** (what must be TRUE):
  1. Style Dictionary v4+ configured with DTCG format support and @tokens-studio/sd-transforms integrated
  2. Token transformation generates CSS custom properties matching original forms-flow-theme structure
  3. Build validation catches broken references, invalid types, and schema violations before transformation
  4. Generated output files can be imported by React components without breaking existing builds

**Plans**: 2 plans in 2 waves

Plans:
- [x] 03-01-PLAN.md -- Pre-computation script and Style Dictionary dependencies
- [x] 03-02-PLAN.md -- Style Dictionary pipeline configuration, CSS generation, and npm script orchestration

### Phase 4: Documentation & Validation
**Goal**: Complete documentation exists explaining extraction methodology, naming conventions, and Token Studio import workflow, with all outputs validated.

**Depends on**: Phase 3 (pipeline must work before documenting workflow)

**Requirements**: DOCS-01, DOCS-02, DOCS-03, DOCS-04

**Success Criteria** (what must be TRUE):
  1. Extraction methodology documented with examples showing SCSS-to-DTCG transformations
  2. Token naming conventions documented with rationale and examples of valid/invalid names
  3. Token Studio import guide created with step-by-step Figma Variable import instructions
  4. Gaps and manual interventions documented (computed values, missing semantic tokens, component-specific values)

**Plans**: 2 plans in 1 wave

Plans:
- [ ] 04-01-PLAN.md -- Developer docs: quick-start README + methodology + naming conventions (DOCS-01, DOCS-02)
- [ ] 04-02-PLAN.md -- Designer docs: Figma import guide + gap documentation + README update + Figma validation (DOCS-03, DOCS-04)

## Progress

**Execution Order:**
Phases execute in numeric order: 1 -> 2 -> 3 -> 4

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Audit & Foundation | 3/3 | Complete | 2026-02-04 |
| 2. Token Extraction | 3/3 | Complete | 2026-02-05 |
| 3. Build Pipeline | 2/2 | Complete | 2026-02-09 |
| 4. Documentation & Validation | 0/2 | Not started | - |

---
*Roadmap created: 2026-02-03*
*Last updated: 2026-02-09 (Phase 3 complete)*
