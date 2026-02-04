#!/usr/bin/env python3
"""
Generate human-readable markdown audit summary from theme-audit.json.
"""

import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

def generate_markdown(audit_data: dict) -> str:
    """Generate markdown content from audit data."""

    md = []

    # Header
    md.append("# Forms-Flow Theme Audit\n")
    md.append(f"**Date:** {audit_data['metadata']['auditDate']}\n")
    md.append(f"**Source:** {audit_data['metadata']['sourceDirectory']}\n")
    md.append(f"**Total SCSS Variables:** {audit_data['metadata']['totalVariables']}\n")
    md.append(f"**Total CSS Custom Properties:** {audit_data['metadata']['totalCustomProperties']}\n")
    md.append(f"**Total SCSS Maps:** {audit_data['metadata']['totalMaps']}\n")

    # Summary Statistics
    md.append("\n## Summary Statistics\n")
    md.append("\n| Category | SCSS Variables | CSS Custom Properties | Total |\n")
    md.append("|----------|---------------|----------------------|-------|\n")

    # Count by category
    scss_by_category = defaultdict(int)
    css_by_category = defaultdict(int)

    for var_name, var_data in audit_data['scssVariables'].items():
        category = var_data['category']
        scss_by_category[category] += 1

    for prop_name, prop_data in audit_data['cssCustomProperties'].items():
        category = prop_data['category']
        css_by_category[category] += 1

    categories = sorted(set(list(scss_by_category.keys()) + list(css_by_category.keys())))

    for category in categories:
        scss_count = scss_by_category[category]
        css_count = css_by_category[category]
        total = scss_count + css_count
        md.append(f"| {category.title()} | {scss_count} | {css_count} | {total} |\n")

    # Total row
    total_scss = sum(scss_by_category.values())
    total_css = sum(css_by_category.values())
    md.append(f"| **Total** | **{total_scss}** | **{total_css}** | **{total_scss + total_css}** |\n")

    # Categories
    for category in categories:
        md.append(f"\n## {category.title()}\n")

        # SCSS Variables
        md.append("\n### SCSS Variables\n")
        md.append("\n| Variable | Value | Computed | Source File | Usages |\n")
        md.append("|----------|-------|----------|-------------|--------|\n")

        scss_vars = {k: v for k, v in audit_data['scssVariables'].items() if v['category'] == category}
        if scss_vars:
            for var_name in sorted(scss_vars.keys()):
                var_data = scss_vars[var_name]
                value = var_data['value'][:50]  # Truncate long values
                computed = var_data.get('computedValue', 'N/A')
                if computed:
                    computed = str(computed)[:50]
                else:
                    computed = 'N/A'
                source = var_data['sourceFile'].replace('forms-flow-theme/', '')
                usages = var_data['usageCount']
                md.append(f"| `{var_name}` | `{value}` | `{computed}` | {source} | {usages} |\n")
        else:
            md.append("| - | - | - | - | - |\n")

        # CSS Custom Properties
        md.append("\n### CSS Custom Properties\n")
        md.append("\n| Property | Value | Root Block | Source File | Usages |\n")
        md.append("|----------|-------|------------|-------------|--------|\n")

        css_props = {k: v for k, v in audit_data['cssCustomProperties'].items() if v['category'] == category}
        if css_props:
            for prop_name in sorted(css_props.keys()):
                prop_data = css_props[prop_name]
                value = prop_data['value'][:60]  # Truncate long values
                root_block = prop_data.get('rootBlock', 'N/A')
                source = prop_data['sourceFile'].replace('forms-flow-theme/', '')
                usages = prop_data.get('usageCount', 0)
                md.append(f"| `{prop_name}` | `{value}` | {root_block} | {source} | {usages} |\n")
        else:
            md.append("| - | - | - | - | - |\n")

    # Color Maps
    md.append("\n## SCSS Maps\n")

    for map_name, map_data in sorted(audit_data['scssMaps'].items()):
        if not map_data['entries']:
            continue

        md.append(f"\n### {map_name}\n")
        md.append("\n| Key | Value | Computed |\n")
        md.append("|-----|-------|----------|\n")

        for key, entry in sorted(map_data['entries'].items()):
            value = entry['value']
            computed = entry.get('computedValue', value)
            md.append(f"| `{key}` | `{value}` | `{computed}` |\n")

    # Bootstrap Overrides
    md.append("\n## Bootstrap Overrides\n")
    md.append("\n| Variable | Bootstrap Default | Project Override | Type |\n")
    md.append("|----------|-------------------|------------------|------|\n")

    bootstrap_overrides = {k: v for k, v in audit_data['scssVariables'].items() if v.get('isBootstrapOverride')}
    if bootstrap_overrides:
        for var_name in sorted(bootstrap_overrides.keys()):
            var_data = bootstrap_overrides[var_name]
            bs_default = var_data.get('bootstrapDefault', 'N/A')
            project_value = var_data['value']
            var_type = var_data['type']
            md.append(f"| `{var_name}` | `{bs_default}` | `{project_value}` | {var_type} |\n")
    else:
        md.append("| - | - | - | - |\n")

    # Dual :root Blocks
    md.append("\n## Dual :root Blocks\n")
    md.append("\nNote: Two :root blocks exist with overlapping properties. ")
    md.append("The v8-scss/_theme.scss file is loaded after _theme.scss (per index.scss import order), ")
    md.append("so v8-theme properties take precedence when there are conflicts.\n")

    md.append("\n| Property | _theme.scss Value | v8-scss/_theme.scss Value | Active |\n")
    md.append("|----------|-------------------|---------------------------|--------|\n")

    # Find overlapping properties
    theme_props = {k: v for k, v in audit_data['cssCustomProperties'].items() if v.get('rootBlock') == 'theme'}
    v8_props = {k: v for k, v in audit_data['cssCustomProperties'].items() if v.get('rootBlock') == 'v8-theme'}

    overlaps = set(theme_props.keys()) & set(v8_props.keys())

    if overlaps:
        for prop in sorted(overlaps):
            theme_val = theme_props[prop]['value'][:40]
            v8_val = v8_props[prop]['value'][:40]
            active = "same" if theme_val == v8_val else "v8 (last loaded)"
            md.append(f"| `{prop}` | `{theme_val}` | `{v8_val}` | {active} |\n")
    else:
        md.append("| No overlapping properties found | - | - | - |\n")

    # Computed Values (Manual Review Required)
    md.append("\n## Computed Values (Manual Review Required)\n")
    md.append("\nValues that use SCSS functions/expressions and may require manual resolution for token extraction.\n")

    md.append("\n| Variable | Expression | Resolved Value | Notes |\n")
    md.append("|----------|-----------|----------------|-------|\n")

    computed_vars = []
    for var_name, var_data in audit_data['scssVariables'].items():
        value = var_data['value']
        # Check if it's an expression (contains operators or functions)
        if any(op in value for op in ['*', '/', '+', '-', 'calc(', 'var(', 'blend-']):
            computed = var_data.get('computedValue')
            computed_str = str(computed) if computed else "manual resolution needed"
            notes = ""
            if '$base' in value:
                notes = "$base differs: _theme.scss (0.5rem) vs _variables.scss (1rem)"
            computed_vars.append((var_name, value, computed_str, notes))

    if computed_vars:
        for var_name, expr, resolved, notes in sorted(computed_vars)[:30]:  # Show first 30
            md.append(f"| `{var_name}` | `{expr[:40]}` | `{resolved[:40]}` | {notes} |\n")
    else:
        md.append("| No computed values found | - | - | - |\n")

    if len(computed_vars) > 30:
        md.append(f"\n*Showing 30 of {len(computed_vars)} computed values. See theme-audit.json for complete list.*\n")

    # Naming Patterns
    md.append("\n## Naming Patterns\n")
    md.append("\nObserved naming conventions in the codebase:\n")
    md.append("\n### SCSS Variables\n")
    md.append("- **Convention:** `$kebab-case` (e.g., `$gray-darkest`, `$primary-light`, `$font-base`)\n")
    md.append("- **Color names:** Descriptive (e.g., `$gray-darkest`, `$primary`, `$green-dark`)\n")
    md.append("- **Size/spacing:** Base multipliers (e.g., `$base*0.78`, `$fontBase*1.5`)\n")

    md.append("\n### CSS Custom Properties\n")
    md.append("- **Convention:** `--kebab-case` (e.g., `--spacer-100`, `--font-size-xs`)\n")
    md.append("- **Prefix patterns:**\n")
    md.append("  - `--ff-*`: Form.io/forms-flow specific properties\n")
    md.append("  - `--no-code-*`: No-code feature properties\n")
    md.append("  - No prefix: v8 design system properties\n")
    md.append("- **Size scales:**\n")
    md.append("  - Numeric: `--spacer-025` through `--spacer-300` (increments of 25)\n")
    md.append("  - T-shirt: `--font-size-xs`, `--font-size-sm`, `--font-size-md`, `--font-size-lg`, `--font-size-xl`\n")
    md.append("  - Opacity variants: `--color-100`, `--color-200`, `--color-300` (100%, 50%, 25%)\n")

    md.append("\n### Color Variants\n")
    md.append("- **Base colors:** 8 base colors (yellow, green, cyan, blue, orange, vivid, red, indigo)\n")
    md.append("- **Variants:** Each base color has 3 opacity levels (-100, -200, -300)\n")
    md.append("- **Generated via:** `blend-with-white-to-hex()` function\n")
    md.append("- **Example:** `--yellow-100` (solid), `--yellow-200` (50%), `--yellow-300` (25%)\n")

    # Mixins and Functions
    md.append("\n## SCSS Mixins\n")
    for mixin_name, mixin_data in sorted(audit_data['scssMixins'].items()):
        md.append(f"\n### `@mixin {mixin_name}`\n")
        md.append(f"- **Source:** {mixin_data['sourceFile']}\n")
        md.append(f"- **Parameters:** {', '.join(f'`{p}`' for p in mixin_data['parameters'])}\n")
        md.append(f"- **Design Impact:** {mixin_data['designValuesProduced']}\n")

    md.append("\n## SCSS Functions\n")
    for func_name, func_data in sorted(audit_data['scssFunctions'].items()):
        md.append(f"\n### `@function {func_name}`\n")
        md.append(f"- **Source:** {func_data['sourceFile']}\n")
        md.append(f"- **Purpose:** {func_data['purpose']}\n")
        md.append(f"- **Design Impact:** {func_data['designImpact']}\n")

    # Key Findings
    md.append("\n## Key Findings\n")
    md.append("\n### Version 8 Design System\n")
    md.append("- **Status:** Partial implementation alongside legacy theme\n")
    md.append("- **Location:** `v8-scss/` subdirectory\n")
    md.append(f"- **Properties:** {len(v8_props)} CSS custom properties in v8 :root block\n")
    md.append("- **Approach:** Token-based design with systematic color variants\n")

    md.append("\n### Legacy Theme\n")
    md.append("- **Status:** Active, used throughout codebase\n")
    md.append("- **Location:** Root SCSS files (`_theme.scss`, `_variables.scss`)\n")
    md.append(f"- **Properties:** {len(theme_props)} CSS custom properties in theme :root block\n")
    md.append("- **Characteristics:** Mix of hard-coded values and computed expressions\n")

    md.append("\n### Design Token Readiness\n")
    md.append(f"- **Direct convertible tokens:** ~{total_scss + total_css - len(computed_vars)} values\n")
    md.append(f"- **Requires computation:** {len(computed_vars)} SCSS expressions\n")
    md.append("- **Bootstrap dependencies:** Need to resolve Bootstrap variable references\n")
    md.append("- **Dual :root complexity:** Property precedence requires careful handling\n")

    return ''.join(md)


def main():
    """Generate markdown from audit JSON."""
    audit_path = Path("tokens/audit/theme-audit.json")
    output_path = Path("tokens/audit/theme-audit.md")

    print(f"Loading audit data from {audit_path}...")
    with open(audit_path, 'r', encoding='utf-8') as f:
        audit_data = json.load(f)

    print("Generating markdown...")
    markdown_content = generate_markdown(audit_data)

    print(f"Writing to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print(f"✓ Markdown audit generated: {output_path}")
    print(f"  Total lines: {len(markdown_content.splitlines())}")


if __name__ == "__main__":
    main()
