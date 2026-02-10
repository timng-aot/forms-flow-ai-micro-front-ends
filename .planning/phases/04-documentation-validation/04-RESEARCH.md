# Phase 4: Documentation & Validation - Research

**Researched:** 2026-02-09
**Domain:** Technical documentation, design token methodology documentation, Figma/Token Studio import guides, validation testing
**Confidence:** HIGH

## Summary

Phase 4 requires creating comprehensive documentation that serves two distinct audiences (designers using Figma/Token Studio and developers maintaining the pipeline) while validating the token extraction and transformation outputs. The documentation explains extraction methodology from SCSS to DTCG, naming conventions, and provides step-by-step Token Studio import instructions. Documentation lives in forms-flow-theme/docs/ with a quick-start section for common tasks.

Modern technical documentation best practices (2026) emphasize audience segmentation, code examples with visual aids, and lean documentation that answers specific questions rather than exhaustive coverage. For designer-facing content, screenshot-heavy step-by-step guides work best (600px width, PNG format, annotated with callouts). For developer-facing content, methodology documentation should explain the "why" behind decisions (why DTCG, why two files, why ff- prefix) alongside the "how" of maintaining the pipeline.

The W3C DTCG specification v1.0 (stable as of Oct 2025) provides the authoritative format reference. Token Studio official docs detail the Figma Variables import process with specific requirements (no forbidden characters in token names, proper $type inheritance, valid reference syntax). Validation involves importing tokens into Figma/Token Studio and confirming variables are created with correct names and values.

**Primary recommendation:** Create modular markdown documentation in forms-flow-theme/docs/ with quick-start at top (common tasks in 3-line format), separate sections for designers (Figma import guide with annotated screenshots) and developers (methodology with transformation examples), and comprehensive gap documentation with actionable next-steps linking back to Phase 1 audit data. Validation uses manual Figma import test to confirm Token Studio compatibility.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Audience & depth:**
- Two distinct audiences: designers (Figma import) and developers (pipeline maintenance)
- Designer-facing import guide: screenshot-heavy walkthrough, step-by-step, minimal jargon
- Developer-facing methodology: includes WHY behind decisions (why DTCG, why two files, why ff- prefix) plus HOW to maintain
- Transformation examples show SCSS source → DTCG token only (skip CSS output side)

**Document structure:**
- Location: forms-flow-theme/docs/
- Quick-start section at the top of docs covering common tasks: "How to add a token", "How to rebuild CSS", "How to import to Figma"
- Update forms-flow-theme README with a "Design Tokens" section linking to docs/

**Validation scope:**
- Figma import test: import tokens into Figma/Token Studio and confirm variables are created with correct names and values
- No CSS output spot-check (Phase 3 build-time validation covers this)
- No token count summary in docs (counts change over time)

**Gap documentation:**
- Gaps presented with actionable next-steps (each gap includes what to do about it)
- Reference Phase 1 component audit data with file paths so readers can trace gaps back to source
- Gaps include specific instructions (e.g., "To add shadow tokens for forms-flow-admin, run X and add to semantic.json")

### Claude's Discretion

- Single doc vs multiple files split (based on content volume and readability)
- Whether to include Figma import screenshots in the guide (based on value-add assessment)
- Whether to include a "What's NOT tokenized" exclusion section (based on confusion-prevention value)
- Whether to include a brief component adoption/migration section (based on value without scope creep)

### Deferred Ideas (OUT OF SCOPE)

None — discussion stayed within phase scope

</user_constraints>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Markdown | CommonMark | Documentation format | Universal support, readable as source, renders well in GitHub/GitLab, compatible with static site generators |
| Token Studio plugin | Latest (2026) | Figma Variables import | Official Token Studio integration for DTCG format, imports JSON tokens as Figma Variables |
| Figma Desktop | Latest | Design tool for testing import | Industry standard design tool, native Variables feature for design tokens |
| JSON Schema | Draft 2020-12 | Token validation (Phase 3) | Used by Style Dictionary and DTCG validators for format checking |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| Screenshot tools | System native | Capture Figma UI for docs | macOS Screenshot (Cmd+Shift+4), Windows Snip & Sketch for annotated captures |
| Mermaid.js | Latest | Flow diagrams | If adding pipeline flow diagrams to methodology docs (optional) |
| Markdown linters | markdownlint | Format consistency | CI/CD validation of markdown files for consistent style |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Markdown | Notion/Confluence | Markdown is version-controlled, lives with code, no external dependencies, readable in GitHub |
| Manual screenshots | ScribeHow (auto-capture) | Manual gives control over annotations and callouts; ScribeHow is faster but less precise |
| Token Studio | Figma API direct import | Token Studio is officially supported and user-friendly; API is for advanced automation only |

**Installation:**
```bash
# Documentation tools (all free)
# - Markdown editor: VS Code (built-in), Obsidian, or Typora
# - Screenshot tool: System native (macOS: Cmd+Shift+4, Windows: Snip & Sketch)
# - Figma Desktop: https://www.figma.com/downloads/
# - Token Studio plugin: Install from Figma Community (search "Token Studio")

# Optional: Markdown linting (for CI/CD)
npm install --save-dev markdownlint markdownlint-cli
```

## Architecture Patterns

### Recommended Documentation Structure
```
forms-flow-theme/
├── README.md                     # Add "Design Tokens" section linking to docs/
└── docs/
    ├── design-tokens/
    │   ├── README.md             # Quick-start + table of contents
    │   ├── methodology.md        # Developer-facing: extraction, naming, pipeline
    │   ├── figma-import.md       # Designer-facing: Token Studio import guide
    │   ├── gaps-and-coverage.md  # Gap analysis with actionable next-steps
    │   └── assets/
    │       ├── figma-import-01-plugin.png
    │       ├── figma-import-02-sync.png
    │       └── transformation-example.png
    └── (other documentation as needed)
```

**Structure rationale:**
- Separate directory (docs/design-tokens/) keeps token docs colocated and findable
- README.md serves as landing page with quick-start (common tasks in 3 lines each)
- Separate files for methodology (developer) and figma-import (designer) based on audience
- gaps-and-coverage.md documents what's missing and how to add it
- assets/ subfolder keeps screenshots organized

### Pattern 1: Quick-Start Task Format
**What:** Common tasks presented as 3-line "cheat sheet" entries at top of main README
**When to use:** Always — provides immediate value for returning users
**Example:**
```markdown
## Quick Start

### How to add a new token
1. Add to `tokens/core.json` or `tokens/semantic.json` following DTCG format
2. Run `npm run build:tokens` to regenerate CSS
3. Import updated JSON to Figma via Token Studio plugin

### How to rebuild CSS after token changes
1. `cd forms-flow-theme`
2. `npm run build:tokens` (runs precompute → Style Dictionary)
3. Output: `tokens/dist/core-tokens.css` and `semantic-tokens.css`

### How to import tokens to Figma
1. Open Figma file → Plugins → Token Studio
2. New file or Attach to existing → Import → Select `tokens/core.json`
3. Repeat for `tokens/semantic.json` as separate token set
```

### Pattern 2: Developer Methodology Documentation
**What:** Explain WHY behind decisions (DTCG format, two-file split, ff- prefix) plus HOW to maintain
**When to use:** Developer-facing methodology docs
**Example:**
```markdown
## Token Extraction Methodology

### Why W3C DTCG Format?

We use the W3C Design Tokens Community Group (DTCG) specification v1.0 for three reasons:

1. **Industry standard** — Stable spec (Oct 2025), supported by Figma, Adobe, Google
2. **Tool compatibility** — Token Studio, Style Dictionary, and other tools have first-class support
3. **Future-proof** — Official W3C standard ensures long-term compatibility

Reference: [W3C DTCG Format Module](https://www.designtokens.org/)

### Why Two Files (core.json + semantic.json)?

**core.json** contains primitive design values (raw colors, spacing values) with no semantic meaning.
**semantic.json** contains purpose-based tokens that reference core tokens.

This separation:
- **Mirrors design thinking** — Primitives (palette) vs semantic (usage)
- **Enables theme switching** — Swap semantic layer, keep core unchanged
- **Matches Figma structure** — Two token sets in Token Studio mirror code structure

Example transformation:
```scss
// SCSS source (forms-flow-theme/scss/v8-scss/_theme.scss)
$indigo-100: #3248F4;
$color-action-primary: var(--ff-indigo-100);
```

Becomes:
```json
// core.json
{
  "ff": {
    "color": {
      "indigo-100": {
        "$value": "#3248F4",
        "$type": "color"
      }
    }
  }
}

// semantic.json
{
  "color": {
    "action": {
      "primary": {
        "$value": "{ff.color.indigo-100}",
        "$type": "color"
      }
    }
  }
}
```

### Why --ff- Prefix?

CSS custom properties use `--ff-` prefix (e.g., `--ff-color-indigo-100`) to:
- **Namespace tokens** — Avoids collisions with Bootstrap or other libraries
- **Identify source** — "ff" = Forms Flow, clearly distinguishes our tokens
- **Follow convention** — Matches existing forms-flow-theme naming patterns

Configured in Style Dictionary via custom name transform.
```

### Pattern 3: Designer-Facing Figma Import Guide
**What:** Screenshot-heavy step-by-step walkthrough with minimal jargon
**When to use:** Designer-facing import guide
**Example:**
```markdown
## Importing Tokens to Figma

This guide walks you through importing design tokens into Figma using the Token Studio plugin.

### Prerequisites
- Figma Desktop app installed
- Token Studio plugin installed (search "Token Studio" in Figma Community)
- Access to token JSON files: `tokens/core.json` and `tokens/semantic.json`

### Step 1: Open Token Studio Plugin

1. Open your Figma file
2. Go to **Plugins** → **Token Studio for Figma**
3. Click **New empty file** if this is your first time

![Token Studio plugin launch](./assets/figma-import-01-plugin.png)

### Step 2: Import Core Tokens

1. In Token Studio, click **Styles & Variables** button (icon with paint bucket)
2. Select **Import** tab
3. Click **Select JSON file** and choose `tokens/core.json`
4. Review the token list (you should see color, spacing, typography tokens)
5. Click **Import** to create Figma Variables

![Import core tokens](./assets/figma-import-02-import-core.png)

**What you'll see:**
- New variable collection named "ff" with all core tokens
- Variables organized by category (color, spacing, etc.)

### Step 3: Import Semantic Tokens

1. Repeat Step 2, but select `tokens/semantic.json`
2. Token Studio will create a second token set
3. Semantic tokens will reference core tokens (you'll see `{ff.color.indigo-100}` syntax)

### Step 4: Verify Import

Check that variables were created correctly:
1. Open **Variables** panel in Figma (right sidebar)
2. Confirm you see two collections: "ff" (core) and "semantic"
3. Check a few variables to ensure values match the JSON

**Common issues:**
- **"Invalid token name" error** — Token names can't contain `{`, `}`, or `$` characters
- **References not resolving** — Ensure core.json was imported before semantic.json
- **Duplicate variables** — Delete existing variables before re-importing
```

### Pattern 4: Gap Documentation with Actionable Next-Steps
**What:** Present gaps found in Phase 1 audit with specific instructions for adding missing tokens
**When to use:** Gap documentation section
**Example:**
```markdown
## Token Coverage Gaps

Phase 1 component audit identified design values in components that don't exist in the shared theme. This section documents those gaps and provides instructions for adding them.

### Summary
- **Total component values analyzed:** 80
- **Exists in theme:** 33 (41.2% coverage)
- **Close match:** 29
- **Missing from theme:** 18

Source: `tokens/audit/gap-analysis.json`

### Missing Shadow Tokens

**Gap:** 10 shadow values used in `forms-flow-nav` and `forms-flow-admin` don't have corresponding theme tokens.

**Most common missing shadows:**
- `none` (7 occurrences)
- `0px 2px 8px rgba(66, 66, 66, 0.07)` (4 occurrences)
- `0 1px 3px rgba(0, 0, 0, 0.1)` (1 occurrence)

**How to add:**

1. Add to `tokens/semantic.json` under `ff.shadow` group:
```json
{
  "ff": {
    "shadow": {
      "$type": "shadow",
      "none": {
        "$value": {
          "color": "#00000000",
          "offsetX": "0px",
          "offsetY": "0px",
          "blur": "0px",
          "spread": "0px"
        },
        "$description": "No shadow (used for forms-flow-nav, forms-flow-admin)"
      },
      "md": {
        "$value": {
          "color": "rgba(66, 66, 66, 0.07)",
          "offsetX": "0px",
          "offsetY": "2px",
          "blur": "8px",
          "spread": "0px"
        },
        "$description": "Medium shadow (forms-flow-admin cards)"
      }
    }
  }
}
```

2. Rebuild CSS: `npm run build:tokens`
3. Re-import to Figma via Token Studio

**Source components:**
- `forms-flow-nav/src/components/NavBar.js` (7 occurrences)
- `forms-flow-admin/src/components/Card.js` (4 occurrences)

Reference: `tokens/audit/gap-analysis.json` lines 10-93

### Missing Typography Tokens

**Gap:** 3 font-size values (2rem, 3rem, 36px) used in headings don't have theme equivalents.

**How to add:**

1. Add to `tokens/core.json`:
```json
{
  "ff": {
    "font-size": {
      "$type": "dimension",
      "xxl": {
        "$value": "2rem",
        "$description": "Extra-large font size for page headings"
      }
    }
  }
}
```

2. Reference in `tokens/semantic.json`:
```json
{
  "typography": {
    "heading": {
      "h1": {
        "$value": "{ff.font-size.xxl}",
        "$type": "dimension"
      }
    }
  }
}
```

**Source components:**
- `forms-flow-submissions/src/components/Header.js` (2 occurrences)
- `forms-flow-admin/src/components/Title.js` (1 occurrence)

Reference: `tokens/audit/gap-analysis.json` lines 706-747
```

### Pattern 5: Transformation Example (SCSS → DTCG)
**What:** Show before/after examples of extraction from SCSS to DTCG format
**When to use:** Methodology docs to illustrate extraction process
**Example:**
```markdown
## Extraction Examples

### Example 1: Color Palette Extraction

**SCSS source** (forms-flow-theme/scss/v8-scss/_theme.scss:16-21):
```scss
$indigo-100: #3248F4;
$indigo-200: blend-with-white-to-hex($indigo-100, 0.5);
$indigo-300: blend-with-white-to-hex($indigo-100, 0.2);
```

**Extracted to DTCG** (tokens/core.json):
```json
{
  "ff": {
    "color": {
      "$type": "color",
      "indigo-100": {
        "$value": "#3248F4",
        "$description": "v8 indigo palette shade 100"
      },
      "indigo-200": {
        "$value": "#99A4FA",
        "$description": "v8 indigo palette shade 200"
      },
      "indigo-300": {
        "$value": "#CCD1FC",
        "$description": "v8 indigo palette shade 300"
      }
    }
  }
}
```

**Notes:**
- SCSS function `blend-with-white-to-hex()` is pre-computed to hex values
- Original expression documented in Phase 1 audit data
- Type inheritance: `$type: "color"` set at group level

### Example 2: Spacing with Semantic References

**SCSS source** (forms-flow-theme/scss/_theme.scss:89-90):
```scss
$base: 1rem;
$button-padding: $base * 0.5;
```

**Extracted to core.json:**
```json
{
  "ff": {
    "spacing": {
      "$type": "dimension",
      "base": {
        "$value": "1rem",
        "$description": "Base spacing unit"
      },
      "050": {
        "$value": "0.5rem",
        "$description": "Half base spacing"
      }
    }
  }
}
```

**Semantic reference** (semantic.json):
```json
{
  "button": {
    "padding": {
      "$value": "{ff.spacing.050}",
      "$type": "dimension",
      "$description": "Button padding (0.5× base)"
    }
  }
}
```

**Notes:**
- Core tokens use numeric scale (050 = 0.5× multiplier)
- Semantic tokens reference core via `{ff.spacing.050}` syntax
- Style Dictionary resolves references at build time
```

### Anti-Patterns to Avoid
- **Dense wall-of-text docs** — Break up with headings, code blocks, screenshots
- **Outdated screenshots** — Screenshots require maintenance; annotate with callouts to reduce fragility
- **Jargon overload for designers** — "DTCG specification" → "token format that Figma understands"
- **Methodology without examples** — Always show before/after code snippets
- **Gaps without solutions** — Every gap entry needs "How to add" instructions
- **Generic file names** — Name screenshots descriptively (figma-import-step-2.png, not screenshot-5.png)

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Screenshot annotations | Manual image editing | macOS Preview (Markup), Windows Paint 3D | Built-in tools support callouts, arrows, highlights |
| Markdown rendering | Custom HTML converter | GitHub rendering, VS Code preview, Obsidian | Markdown renders natively in most developer tools |
| Token validation | Custom JSON checker | Style Dictionary validation (Phase 3 config) | Already validates DTCG schema, references, types |
| Figma import automation | Custom Figma API script | Token Studio plugin manual import | Plugin is user-tested, handles edge cases, official support |
| Documentation search | Custom index | GitHub file search, VS Code search | Built-in search is sufficient for markdown docs |
| Diagram generation | Manual drawing | Mermaid.js code blocks | Version-controlled, renders in GitHub, easy to update |

**Key insight:** Documentation is valuable because it's accurate and maintained, not because it's exhaustive. Use standard tools (markdown, screenshots, Token Studio) that non-technical team members can update. Custom automation creates maintenance burden and breaks when underlying systems change.

## Common Pitfalls

### Pitfall 1: Screenshots Without Context
**What goes wrong:** Screenshot shows Figma UI with no explanation of what to click or why.
**Why it happens:** Assuming reader has same context as writer; forgetting that screenshots alone aren't accessible.
**How to avoid:**
- Add numbered callouts on screenshots (1, 2, 3) matching step numbers
- Include alt text describing screenshot content for accessibility
- Annotate important UI elements with arrows or highlight boxes
**Warning signs:** Reader feedback: "I don't know what to click" or "screenshot is unclear"

### Pitfall 2: Methodology Docs Without "Why"
**What goes wrong:** Documentation explains HOW to run commands but not WHY design decisions were made.
**Why it happens:** Technical writers focus on process, skip rationale; readers assume decisions are arbitrary.
**How to avoid:**
- User decision specifies "includes WHY behind decisions (why DTCG, why two files, why ff- prefix)"
- Start methodology sections with "Why [decision]?" heading
- Link to authoritative sources (W3C DTCG spec, Token Studio docs) for context
**Warning signs:** Developers ask "why not X instead?" in PR comments; documentation gets ignored

### Pitfall 3: Outdated Screenshots After UI Changes
**What goes wrong:** Figma or Token Studio updates UI; screenshots no longer match current interface.
**Why it happens:** Screenshots are expensive to update; UI changes faster than docs maintenance.
**How to avoid:**
- Annotate screenshots to focus on concepts, not exact button labels
- Add "Last verified: 2026-02" date to screenshot-heavy sections
- Use descriptive text alongside screenshots ("look for the import icon")
- Prefer fewer, high-value screenshots over exhaustive step coverage
**Warning signs:** User feedback: "I don't see that button" or "UI looks different"

### Pitfall 4: Gap Documentation Without Source Traceability
**What goes wrong:** Gap doc says "missing shadow tokens" but doesn't link to source components or audit data.
**Why it happens:** Extracting gaps from JSON without preserving audit metadata.
**How to avoid:**
- User decision: "Reference Phase 1 component audit data with file paths so readers can trace gaps back to source"
- Include audit file reference: `tokens/audit/gap-analysis.json lines 10-93`
- List source components: `forms-flow-nav/src/components/NavBar.js (7 occurrences)`
- Link to original SCSS if values came from theme
**Warning signs:** Developers can't verify gaps are real; no way to update component to use tokens

### Pitfall 5: Quick-Start That Isn't Quick
**What goes wrong:** "Quick start" section is 20 lines of prerequisites and edge cases.
**Why it happens:** Over-documenting to cover all scenarios; forgetting 80% of users need 20% of info.
**How to avoid:**
- User decision: "common tasks in 3 lines each"
- Limit to most common tasks: add token, rebuild CSS, import to Figma
- Move edge cases and troubleshooting to separate sections
- Use command-line examples that can be copy-pasted
**Warning signs:** Quick-start is longer than main content sections

### Pitfall 6: Designer Docs with Developer Jargon
**What goes wrong:** Figma import guide uses terms like "DTCG schema validation" or "reference resolution"
**Why it happens:** Writer has developer background; doesn't adjust language for designer audience.
**How to avoid:**
- User decision: "Designer-facing import guide: screenshot-heavy walkthrough, step-by-step, minimal jargon"
- Replace jargon: "DTCG format" → "token format that Figma understands"
- Test docs with designer who hasn't used Token Studio before
- Use screenshots to show, not just tell
**Warning signs:** Designers skip documentation and ask questions on Slack

### Pitfall 7: Validation Without Success Criteria
**What goes wrong:** "Import tokens to Figma" without defining what successful import looks like.
**Why it happens:** Assuming reader knows what correct output should be; skipping validation step.
**How to avoid:**
- User decision: "confirm variables are created with correct names and values"
- Add "What you'll see" section after import steps
- Include verification checklist: "Check Variables panel shows two collections"
- Document common issues: "If you see 'Invalid token name' error..."
**Warning signs:** Users complete import but don't know if it worked correctly

### Pitfall 8: Transformation Examples Without Source Context
**What goes wrong:** Show DTCG JSON without showing original SCSS source or explaining transformation logic.
**Why it happens:** Focusing on output format; forgetting readers need to understand extraction process.
**How to avoid:**
- User decision: "Transformation examples show SCSS source → DTCG token only"
- Always show before/after pairs with file paths
- Explain what changed: "SCSS function pre-computed to hex values"
- Note special cases: "Type inheritance set at group level"
**Warning signs:** Developers can't replicate extraction for new tokens

## Code Examples

Verified patterns from project and official sources.

### Complete Methodology Documentation Template
```markdown
# Design Token Methodology

## Overview

This document explains how design tokens are extracted from forms-flow-theme SCSS files, transformed to W3C DTCG format, and imported into Figma. It covers the "why" behind architectural decisions and the "how" of maintaining the token pipeline.

**Target audience:** Developers maintaining the design system
**Last updated:** 2026-02-09

## Why Design Tokens?

Design tokens are platform-agnostic design values (colors, spacing, typography) stored in JSON format. They enable:

1. **Single source of truth** — Design values defined once, used everywhere (CSS, React, Figma)
2. **Design-dev sync** — Designers update tokens in Figma, developers consume via JSON export
3. **Theme switching** — Swap token sets without changing component code
4. **Consistency** — No hardcoded values; all components reference same palette

## Architecture Decisions

### Why W3C DTCG Format?

[Content from Pattern 2 example above]

### Why Two Files (core.json + semantic.json)?

[Content from Pattern 2 example above]

### Why --ff- Prefix?

[Content from Pattern 2 example above]

## Token Pipeline

The token pipeline has three stages:

```
SCSS source → DTCG JSON → CSS custom properties
```

### Stage 1: Extraction (Phase 2)

SCSS variables from forms-flow-theme are parsed and transformed to DTCG format:

[Include transformation examples from Pattern 5]

### Stage 2: Pre-computation (Phase 3)

SCSS color functions like `blend-with-white-to-hex()` are computed to static hex values:

```bash
npm run build:tokens:precompute
```

This runs `tokens/scripts/precompute-colors.js` which resolves expressions in core.json.

### Stage 3: CSS Generation (Phase 3)

Style Dictionary transforms DTCG JSON to CSS custom properties:

```bash
npm run build:tokens:core      # Generates tokens/dist/core-tokens.css
npm run build:tokens:semantic  # Generates tokens/dist/semantic-tokens.css
```

Output:
```css
:root {
  --ff-color-indigo-100: #3248F4;
  --ff-color-indigo-200: #99A4FA;
}
```

## Naming Conventions

[Reference tokens/audit/dtcg-spec.md naming section]

## Maintenance Tasks

### Adding a new token

1. Decide if token is primitive (core.json) or semantic (semantic.json)
2. Add to appropriate file following DTCG format
3. Rebuild CSS: `npm run build:tokens`
4. Re-import to Figma via Token Studio

### Updating an existing token

1. Edit value in core.json or semantic.json
2. Rebuild CSS: `npm run build:tokens`
3. Re-import to Figma (Token Studio will detect changes)
4. Update components consuming the token

### Debugging failed builds

Build fails if:
- JSON syntax error (use `jq . tokens/core.json` to validate)
- Broken reference (semantic token references non-existent core token)
- Invalid $type value (must be DTCG-compliant type)

Style Dictionary validation runs automatically and reports specific errors.

## References

- W3C DTCG Format Module: https://www.designtokens.org/
- Token Studio Documentation: https://docs.tokens.studio
- Style Dictionary Reference: https://styledictionary.com/
- Project DTCG Spec: tokens/audit/dtcg-spec.md
```

### Complete Figma Import Guide Template
```markdown
# Importing Design Tokens to Figma

This guide walks you through importing design tokens into Figma using the Token Studio plugin. No coding required.

**Target audience:** Designers using Figma
**Time required:** 10 minutes
**Last updated:** 2026-02-09

## Prerequisites

Before starting, make sure you have:

- [ ] Figma Desktop app installed ([download here](https://www.figma.com/downloads/))
- [ ] Token Studio plugin installed ([install from Figma Community](https://www.figma.com/community/plugin/843461159747178978))
- [ ] Access to token files: `tokens/core.json` and `tokens/semantic.json`

## Step 1: Open Token Studio Plugin

[Content from Pattern 3 example above with screenshots]

## Step 2: Import Core Tokens

[Content from Pattern 3 example above with screenshots]

## Step 3: Import Semantic Tokens

[Content from Pattern 3 example above]

## Step 4: Verify Import

[Content from Pattern 3 example above]

## Troubleshooting

### "Invalid token name" error

**Problem:** Token Studio can't import tokens with `{`, `}`, or `$` in the name.

**Solution:** Check token JSON files for forbidden characters. Token names should use kebab-case only (letters, numbers, hyphens).

### References not resolving

**Problem:** Semantic tokens show raw reference text like `{ff.color.indigo-100}` instead of actual color.

**Solution:** Ensure core.json was imported before semantic.json. Delete both token sets and re-import in order.

### Duplicate variables

**Problem:** Re-importing creates duplicate variables instead of updating existing ones.

**Solution:** In Token Studio, go to Settings → Delete all token sets. Then re-import fresh.

## Next Steps

After importing tokens:

1. **Apply to designs** — Use Variables panel to apply tokens to layers
2. **Create modes** — Set up light/dark themes using variable modes
3. **Export changes** — When making token updates in Figma, export JSON and update code repository

## References

- Token Studio Import Guide: https://docs.tokens.studio/figma/import
- Figma Variables Documentation: https://help.figma.com/hc/en-us/articles/15339657135383-Guide-to-variables-in-Figma
```

### Quick-Start README Template
```markdown
# Design Tokens — Quick Start

**Location:** forms-flow-theme/docs/design-tokens/README.md

This is your quick reference for common design token tasks.

## Quick Start

[Content from Pattern 1 example above]

## Full Documentation

- [**Methodology**](./methodology.md) — How tokens are extracted, transformed, and why we made these choices (developer-focused)
- [**Figma Import Guide**](./figma-import.md) — Step-by-step Token Studio import instructions (designer-focused)
- [**Gaps & Coverage**](./gaps-and-coverage.md) — What's missing from the token system and how to add it

## File Structure

```
tokens/
├── core.json                 # Primitive tokens (raw design values)
├── semantic.json             # Purpose-based tokens (references to core)
├── dist/
│   ├── core-tokens.css      # Generated CSS custom properties
│   └── semantic-tokens.css  # Generated CSS custom properties
└── audit/                   # Phase 1 audit data (reference only)
    ├── theme-audit.json
    ├── gap-analysis.json
    └── dtcg-spec.md
```

## Token Categories

| Category | Core Tokens | Semantic Tokens | Example |
|----------|-------------|-----------------|---------|
| **Color** | `ff.color.indigo-100` | `color.action.primary` | Brand colors, UI states |
| **Spacing** | `ff.spacing.100` (1rem) | `spacing.md`, `button.padding` | Margins, padding |
| **Typography** | `ff.font-size.14` | `font-size.body`, `typography.heading.h1` | Font sizes, families |
| **Border Radius** | `ff.radius.md` | `radius.button`, `radius.card` | Corner rounding |
| **Shadow** | `ff.shadow.sm` | `shadow.card`, `shadow.dropdown` | Elevations |

## Need Help?

- **Found a bug?** Open an issue in the repository
- **Need a new token?** Follow "How to add a token" guide above
- **Figma import broken?** Check [Troubleshooting](./figma-import.md#troubleshooting)
```

### Gap Documentation Template
```markdown
# Token Coverage Gaps

**Last updated:** 2026-02-09
**Source data:** tokens/audit/gap-analysis.json

Phase 1 component audit identified design values in micro-frontend components that don't exist in the shared theme. This document lists those gaps with instructions for adding them.

[Content from Pattern 4 example above]
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Inline documentation in code | Dedicated docs/ directory | 2024+ industry trend | Separation of concerns, easier to find, version-controlled |
| PDF/Word documentation | Markdown in repository | 2020+ industry shift | Lives with code, version-controlled, renders in GitHub |
| Manual Figma sync | Token Studio JSON import | 2023 (Token Studio maturity) | Bidirectional sync, design-to-code pipeline |
| Single audience docs | Audience segmentation (designer/developer) | 2026 best practice | Tailored content, skip irrelevant details |
| Exhaustive documentation | Lean "quick-start" approach | 2026 trend | Focus on common tasks, answers specific questions |
| Manual screenshots | Auto-capture tools (ScribeHow) | 2025+ tools available | Faster creation but less control over annotations |

**Deprecated/outdated:**
- **Word/PDF documentation:** Not version-controlled, requires separate storage, hard to update
- **Confluence/Notion for code docs:** External dependency, often goes stale, not near code
- **Storybook as token documentation:** Overkill for token reference, better for component API docs
- **Token count summaries in docs:** User decision: "No token count summary in docs (counts change over time)"

## Open Questions

1. **Single doc vs multiple files**
   - What we know: 4 main sections (quick-start, methodology, figma-import, gaps)
   - What's unclear: Content volume unknown until written; might be too long for single file
   - Recommendation: Start with 4 separate files (per architecture pattern). Easier to navigate, better for audience segmentation (designer can skip methodology). Each file 300-500 lines max.

2. **Figma import screenshots inclusion**
   - What we know: User decision allows Claude's discretion based on value-add assessment
   - What's unclear: Token Studio UI is well-designed but import steps aren't obvious to first-time users
   - Recommendation: Include 3-4 annotated screenshots showing plugin launch, import dialog, verification. Screenshots add significant value for designer audience unfamiliar with Token Studio. Use PNG format, 600px width, compress under 100KB.

3. **"What's NOT tokenized" exclusion section**
   - What we know: User decision allows discretion based on confusion-prevention value
   - What's unclear: Whether readers will try to tokenize things that shouldn't be (component-specific animations, one-off layout values)
   - Recommendation: Add brief "Out of Scope" section in methodology.md listing: component-specific z-index, CSS animation keyframes, one-off layout measurements, computed values. Prevents confusion and sets boundaries.

4. **Component adoption/migration section**
   - What we know: User decision allows discretion based on value without scope creep
   - What's unclear: Whether developers need guidance on migrating components to use tokens
   - Recommendation: Add brief "Adopting Tokens in Components" subsection (50-100 lines) in methodology.md showing before/after example of replacing hardcoded values with CSS variables. Stays within scope (documentation phase), enables Phase 5 work.

5. **Markdown linting in CI/CD**
   - What we know: Markdown is standard format, linters exist
   - What's unclear: Whether automated validation adds value for small docs set
   - Recommendation: Skip for now. Four markdown files don't justify CI/CD setup. Add markdownlint if docs expand to 10+ files.

## Sources

### Primary (HIGH confidence)
- [W3C Design Tokens Format Module 2025.10](https://www.designtokens.org/tr/drafts/format/) - DTCG specification v1.0 stable
- [Token Studio Import Variables from Figma](https://docs.tokens.studio/figma/import/variables) - Official Token Studio import guide
- [Token Studio Variables Overview](https://docs.tokens.studio/figma/variables-overview) - Token Studio + Figma Variables integration
- [Figma Variables Help Center](https://help.figma.com/hc/en-us/articles/18490793776023-Update-1-Tokens-variables-and-styles) - Official Figma Variables documentation
- Project codebase: tokens/audit/dtcg-spec.md - DTCG structure specification from Phase 1
- Project codebase: tokens/audit/gap-analysis.json - Gap analysis data from Phase 1
- Project codebase: forms-flow-theme/config/style-dictionary.config.js - Style Dictionary configuration from Phase 3

### Secondary (MEDIUM confidence)
- [Qodo: Code Documentation Best Practices 2026](https://www.qodo.ai/blog/code-documentation-best-practices-2026/) - Technical documentation trends
- [Documind: Technical Documentation Best Practices](https://www.documind.chat/blog/technical-documentation-best-practices) - Audience segmentation guidance
- [Document360: Developer Documentation Guide](https://document360.com/blog/write-developer-documentation/) - Code examples and clarity principles
- [Archbee: Screenshots in Technical Documentation](https://www.archbee.com/blog/screenshots-in-technical-documentation) - Screenshot best practices
- [Ritza: Screenshot Guidelines for Technical Documentation](https://styleguide.ritza.co/screenshots/screenshot-guidelines-for-technical-documentation/) - Screenshot specifications
- [Figr Design: Design System Documentation Guide](https://figr.design/blog/design-system-documentation-guide) - Design system docs structure
- [Figma Blog: Documentation That Drives Adoption](https://www.figma.com/blog/design-systems-103-documentation-that-drives-adoption/) - Design system adoption via docs
- [Supernova: Documenting Design Tokens](https://www.supernova.io/blog/documenting-design-tokens-a-guide-to-best-practices-with-supernova) - Token documentation methodology

### Tertiary (LOW confidence)
- [Medium: Technical Writing Screenshots](https://medium.com/technical-writing-is-easy/screenshots-in-documentation-27b45342aad8) - General screenshot guidance (not token-specific)
- [Medium: 2026 Design-Dev Gap](https://medium.com/@EmiliaBiblioKit/the-2026-shift-bridging-the-gap-between-design-and-dev-eeefb781af30) - Trends overview (not specific methodology)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Markdown, Token Studio, Figma are industry standards with stable APIs and documentation
- Architecture: HIGH - Documentation structure patterns are well-established; project already has token files and audit data to document
- Pitfalls: MEDIUM-HIGH - Based on technical documentation best practices and Token Studio known issues; screenshot maintenance is known challenge
- Validation: HIGH - Figma import test is straightforward manual process; Token Studio provides clear error messages
- Gap documentation: HIGH - Phase 1 gap-analysis.json provides complete source data with traceability

**Research date:** 2026-02-09
**Valid until:** 60 days (documentation practices are stable; Token Studio and Figma update quarterly but import process is stable)
