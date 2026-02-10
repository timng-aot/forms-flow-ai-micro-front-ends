# forms-flow-theme

Shared theme package for forms-flow-ai micro-frontends. Contains SCSS styles, CSS variables, and design tokens extracted from the existing design system.

## Overview

This package provides:
- **SCSS source files** — Shared theme styles for consistent UI across all micro-frontends
- **CSS variables** — Compiled CSS custom properties for runtime theming
- **Design tokens** — W3C DTCG format tokens for Figma import and tooling integration

## Design Tokens

Design tokens are the design values extracted from the shared theme in W3C DTCG format. They're ready for import into Figma via Token Studio and can be used by other design tools.

**Full documentation:** [Design Tokens Documentation](./docs/design-tokens/README.md)

### Quick Links

- **[Quick Start Guide](./docs/design-tokens/README.md)** — Common tasks cheat sheet for developers and designers
- **[Methodology](./docs/design-tokens/methodology.md)** — How and why tokens are structured this way
- **[Figma Import Guide](./docs/design-tokens/figma-import.md)** — Step-by-step Token Studio import instructions
- **[Coverage Gaps](./docs/design-tokens/gaps-and-coverage.md)** — What's missing and how to add it

### Build Tokens

To generate CSS custom properties from the token files:

```bash
npm run build:tokens
```

This command:
1. Pre-computes color expressions (blend-with-white-to-hex)
2. Transforms core tokens to CSS (`tokens/dist/core-tokens.css`)
3. Transforms semantic tokens to CSS (`tokens/dist/semantic-tokens.css`)

**Output:** CSS files with `--ff-` prefixed custom properties in `tokens/dist/`

## Token Files

- **`tokens/core.json`** — Base design values (colors, spacing, typography, shadows, etc.)
- **`tokens/semantic.json`** — Design decisions that reference core tokens
- **`tokens/dist/`** — Generated CSS custom properties (created by `npm run build:tokens`)

## Development

### Install Dependencies

```bash
npm install
```

### Build Tokens

```bash
npm run build:tokens
```

### Validate Tokens

```bash
python3 tokens/scripts/validate-tokens.py
```

This validates that all tokens conform to W3C DTCG specification.

## Integration

Micro-frontend packages import this theme to ensure consistent styling:

```javascript
import 'forms-flow-theme/dist/theme.css';
```

## License

See repository root for license information.
