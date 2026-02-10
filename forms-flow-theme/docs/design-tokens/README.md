# Design Tokens - Quick Start

This is your quick reference for working with the Forms Flow AI design token system. For developers maintaining the design token pipeline, common tasks, and immediate reference.

## Quick Start

### How to add a new token

1. Add the token to `tokens/core.json` (primitives) or `tokens/semantic.json` (purpose-based) in DTCG format
2. Run `npm run build:tokens` in the forms-flow-theme directory
3. Import the updated JSON files to Figma via Token Studio plugin (Plugins → Token Studio)

### How to rebuild CSS after token changes

1. Navigate to forms-flow-theme directory: `cd forms-flow-theme`
2. Run the build command: `npm run build:tokens`
3. Generated CSS will be in `tokens/dist/` directory

### How to import tokens to Figma

1. Open Figma → Plugins → Token Studio
2. Import → Select `tokens/dist/tokens-figma.json` from your local filesystem
3. Sync Variables → Export to Figma

## Full Documentation

- [methodology.md](./methodology.md) - Developer-focused extraction methodology, architecture decisions, naming conventions, and maintenance guide
- [figma-import.md](./figma-import.md) - Designer-focused guide for importing tokens into Figma
- [gaps-and-coverage.md](./gaps-and-coverage.md) - Actionable gap analysis showing which component values are tokenized vs hardcoded

## File Structure

```
tokens/
├── core.json              # Primitive design values (colors, spacing, typography)
├── semantic.json          # Purpose-based tokens (references to core tokens)
├── dist/
│   ├── core-tokens.css    # Generated CSS custom properties from core.json
│   ├── semantic-tokens.css # Generated CSS custom properties from semantic.json
│   └── tokens-figma.json  # Merged token file for Token Studio import
├── audit/
│   ├── dtcg-spec.md       # W3C DTCG format specification for this project
│   ├── gap-analysis.json  # Component hardcoded values analysis
│   └── theme-audit.json   # Extracted theme values from SCSS
└── scripts/
    ├── extract-scss-tokens.py      # Extracts tokens from SCSS to DTCG JSON
    ├── validate-tokens.py          # Validates DTCG format compliance
    ├── precompute-colors.js        # Resolves blend-with-white-to-hex() expressions
    └── merge-for-figma.js          # Merges core + semantic into single file for Token Studio
```

## Token Categories

| Category | Description | Example Core Token | Example Semantic Token |
|----------|-------------|-------------------|------------------------|
| Color | Color palette and semantic colors | `ff.color.indigo-100` (#3248F4) | `color.primary` → {ff.color.indigo-100} |
| Spacing | Spacing scale and layout spacing | `ff.spacing.100` (1rem) | `spacing.md` → {ff.spacing.100} |
| Typography | Font families, sizes, weights, line heights | `ff.font-family.font-family-base` | `font-family.body` → {ff.font-family.font-family-base} |
| Border Radius | Component border radius values | `ff.radius.button-border-radius` (1.5625rem) | `radius.sm` (1.09375rem) |
| Shadow | Box shadow definitions | `ff.shadow.button-shadow-primary` | `shadow.sm` (DTCG object) |

## Need Help?

- **Architecture decisions:** See [methodology.md](./methodology.md) for WHY behind DTCG format, two-file split, and ff- prefix
- **Naming rules:** See [methodology.md](./methodology.md) Naming Conventions section for per-category rules and valid/invalid examples
- **DTCG specification:** See `tokens/audit/dtcg-spec.md` for complete format specification
- **Gap analysis:** See [gaps-and-coverage.md](./gaps-and-coverage.md) for components that need token adoption
