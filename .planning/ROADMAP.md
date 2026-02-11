# Roadmap: Design Token System

## Milestones

- ✅ **v1.0 Design Token Extraction** - Phases 1-4 (shipped 2026-02-10)
- 🚧 **v2.0 Component Token System (Buttons & Forms)** - Phases 5-9 (in progress)

## Phases

<details>
<summary>✅ v1.0 Design Token Extraction (Phases 1-4) - SHIPPED 2026-02-10</summary>

- [x] Phase 1: Audit & Foundation (3/3 plans) - completed 2026-02-04
- [x] Phase 2: Token Extraction (3/3 plans) - completed 2026-02-05
- [x] Phase 3: Build Pipeline (2/2 plans) - completed 2026-02-09
- [x] Phase 4: Documentation & Validation (2/2 plans) - completed 2026-02-09

Full details: milestones/v1.0-ROADMAP.md

</details>

### 🚧 v2.0 Component Token System (Buttons & Forms) (In Progress)

**Milestone Goal:** Create component-level tokens for buttons and forms that reduce the v1.0 token set to what these components actually use, with CSS property naming that maps to Figma component properties.

#### Phase 5: Architecture & Integration Planning
**Goal**: Define component token architecture that integrates with v1.0 core/semantic tokens
**Depends on**: Phase 4 (v1.0 complete)
**Requirements**: ARCH-01, ARCH-02, ARCH-03, ARCH-04
**Success Criteria** (what must be TRUE):
  1. Developer knows which v1.0 core/semantic tokens buttons and forms reference
  2. Team has documented CSS property naming convention for component tokens
  3. Component token file structure is defined and validated
  4. Reference depth policy prevents overcomplexity in token chains
  5. Integration strategy prevents duplication of existing v1.0 tokens
**Plans**: TBD

Plans:
- [ ] 05-01: TBD

#### Phase 6: Button Component Tokens
**Goal**: Create component-level tokens for all button variants with complete state coverage
**Depends on**: Phase 5
**Requirements**: BTN-01, BTN-02, BTN-03, BTN-04
**Success Criteria** (what must be TRUE):
  1. Designer can apply button variant tokens in Figma matching code implementation
  2. Developer can style button states using component tokens without hardcoded values
  3. All button interactive states have distinct visual tokens (default, hover, active, focus, disabled)
  4. Button component tokens reference existing semantic/core tokens with no duplicated values
**Plans**: TBD

Plans:
- [ ] 06-01: TBD

#### Phase 7: Form Component Tokens
**Goal**: Create component-level tokens for form elements with validation state coverage
**Depends on**: Phase 6
**Requirements**: FORM-01, FORM-02, FORM-03, FORM-04
**Success Criteria** (what must be TRUE):
  1. Designer can apply form element tokens in Figma matching code implementation
  2. Developer can style form validation states using component tokens
  3. Form elements show distinct visual feedback for error, valid, focus, and disabled states
  4. Form component tokens reference existing semantic/core tokens with no duplicated values
**Plans**: TBD

Plans:
- [ ] 07-01: TBD

#### Phase 8: Build Pipeline & Figma Sync
**Goal**: Extend Style Dictionary to build component tokens and automate Figma Token Studio sync
**Depends on**: Phase 7
**Requirements**: BUILD-01, BUILD-02, BUILD-03, BUILD-04
**Success Criteria** (what must be TRUE):
  1. Running npm run build:tokens generates CSS custom properties for component tokens
  2. Component tokens resolve 3-tier reference chain (component → semantic → core) correctly
  3. Figma Token Studio import file includes component tokens with proper references
  4. GitHub Actions automatically rebuilds tokens when JSON files change
**Plans**: TBD

Plans:
- [ ] 08-01: TBD

#### Phase 9: Documentation
**Goal**: Document component token hierarchy and enable team adoption
**Depends on**: Phase 8
**Requirements**: DOCS-01
**Success Criteria** (what must be TRUE):
  1. Developer can understand token hierarchy from core to component level
  2. Team can see visual examples of reference chains with real button/form tokens
  3. Documentation shows how component tokens map to CSS properties
**Plans**: TBD

Plans:
- [ ] 09-01: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 5 → 6 → 7 → 8 → 9

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Audit & Foundation | v1.0 | 3/3 | Complete | 2026-02-04 |
| 2. Token Extraction | v1.0 | 3/3 | Complete | 2026-02-05 |
| 3. Build Pipeline | v1.0 | 2/2 | Complete | 2026-02-09 |
| 4. Documentation & Validation | v1.0 | 2/2 | Complete | 2026-02-09 |
| 5. Architecture & Integration | v2.0 | 0/? | Not started | - |
| 6. Button Tokens | v2.0 | 0/? | Not started | - |
| 7. Form Tokens | v2.0 | 0/? | Not started | - |
| 8. Build & Sync | v2.0 | 0/? | Not started | - |
| 9. Documentation | v2.0 | 0/? | Not started | - |

---
*Roadmap created: 2026-02-03*
*Last updated: 2026-02-10 (v2.0 milestone added)*
