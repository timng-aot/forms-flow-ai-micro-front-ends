#!/usr/bin/env python3
"""
Extract all SCSS variables and CSS custom properties from forms-flow-theme.
Generates comprehensive audit JSON with full traceability.
"""

import json
import re
import os
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime

# Base path to SCSS files
SCSS_BASE = Path("/Users/tng/GitHub/forms-flow-ai-micro-front-ends/forms-flow-theme/scss")

# Bootstrap defaults for comparison
BOOTSTRAP_DEFAULTS = {
    "$primary": "#007bff",
    "$success": "#28a745",
    "$danger": "#dc3545",
    "$warning": "#ffc107",
    "$info": "#17a2b8",
}

def categorize_token(name: str, value: str) -> str:
    """Categorize a token based on name and value patterns."""
    name_lower = name.lower()
    value_lower = value.lower()

    # Color patterns
    if any(x in name_lower for x in ['color', 'primary', 'secondary', 'danger', 'success',
                                       'warning', 'info', 'gray', 'black', 'white', 'green',
                                       'blue', 'red', 'yellow', 'orange', 'cyan', 'indigo',
                                       'vivid', 'neutral', 'brand']):
        return "color"
    if re.match(r'^#[0-9a-fA-F]{3,8}$', value_lower):
        return "color"
    if any(x in value_lower for x in ['rgb', 'rgba', 'hsl', 'hsla']):
        return "color"

    # Spacing/dimension patterns
    if any(x in name_lower for x in ['spacer', 'padding', 'margin', 'width', 'height',
                                       'gap', 'base', 'nav']):
        return "spacing"
    if re.search(r'\d+(\.\d+)?(rem|px|em|%)', value_lower):
        if not any(x in name_lower for x in ['font', 'line', 'radius', 'shadow']):
            return "spacing"

    # Typography patterns
    if any(x in name_lower for x in ['font', 'text', 'letter', 'line-height', 'weight']):
        return "typography"

    # Border radius patterns
    if 'radius' in name_lower:
        return "borderRadius"

    # Shadow patterns
    if 'shadow' in name_lower:
        return "shadow"

    # Transition patterns
    if any(x in name_lower for x in ['transition', 'anim', 'speed', 'duration']):
        return "transition"

    return "other"

def extract_scss_variables(file_path: Path) -> Dict[str, Any]:
    """Extract SCSS variables from a file."""
    variables = {}

    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')

        for line_num, line in enumerate(lines, 1):
            # Match SCSS variable declarations: $var-name: value;
            match = re.match(r'^\s*\$([a-zA-Z0-9_-]+)\s*:\s*(.+?)\s*;', line)
            if match:
                var_name = f"${match.group(1)}"
                value = match.group(2).strip()

                # Determine if this is a Bootstrap override
                is_bootstrap_override = var_name in BOOTSTRAP_DEFAULTS
                bootstrap_default = BOOTSTRAP_DEFAULTS.get(var_name)

                variables[var_name] = {
                    "value": value,
                    "computedValue": compute_value(value, variables),
                    "type": categorize_token(var_name, value),
                    "category": categorize_token(var_name, value),
                    "sourceFile": str(file_path.relative_to(SCSS_BASE.parent)),
                    "sourceLine": line_num,
                    "references": [],
                    "usageCount": 0,
                    "isBootstrapOverride": is_bootstrap_override,
                    "bootstrapDefault": bootstrap_default
                }
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

    return variables

def compute_value(value: str, known_vars: Dict[str, Any]) -> str:
    """Attempt to compute/resolve a value expression."""
    # If it's a variable reference, try to resolve it
    if value.startswith('$') and value in known_vars:
        return known_vars[value].get("computedValue", value)

    # If it's a var() reference, return as-is
    if value.startswith('var('):
        return None

    # If it contains simple arithmetic with known base
    if '*' in value or '/' in value:
        # Try to evaluate simple expressions like $base*0.78
        try:
            # Extract variable references
            var_refs = re.findall(r'\$[a-zA-Z0-9_-]+', value)
            eval_expr = value
            for var_ref in var_refs:
                if var_ref in known_vars:
                    var_val = known_vars[var_ref].get("computedValue") or known_vars[var_ref].get("value")
                    # Extract numeric value
                    num_match = re.search(r'([\d.]+)', var_val)
                    if num_match:
                        eval_expr = eval_expr.replace(var_ref, num_match.group(1))

            # Try to evaluate
            if '$' not in eval_expr:
                result = eval(eval_expr)
                # Preserve unit from original value
                unit_match = re.search(r'(rem|px|em|%)', value)
                if unit_match:
                    return f"{result}{unit_match.group(1)}"
        except:
            pass

    # Return original if can't compute
    return value

def extract_css_custom_properties(file_path: Path) -> Dict[str, Any]:
    """Extract CSS custom properties from :root blocks."""
    properties = {}

    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')

        # Determine which root block context
        root_context = "v8-theme" if "v8-scss" in str(file_path) else "theme"

        # Track whether we're inside a :root block
        in_root = False
        brace_depth = 0
        root_start_line = 0

        for line_num, line in enumerate(lines, 1):
            # Check for :root block start
            if ':root' in line and '{' in line:
                in_root = True
                brace_depth = 1
                root_start_line = line_num
                continue

            # Track braces if we're in :root
            if in_root:
                brace_depth += line.count('{') - line.count('}')

                # Extract CSS custom properties
                match = re.match(r'^\s*--([a-zA-Z0-9_-]+)\s*:\s*(.+?)\s*;', line)
                if match:
                    prop_name = f"--{match.group(1)}"
                    value = match.group(2).strip()

                    properties[prop_name] = {
                        "value": value,
                        "type": categorize_token(prop_name, value),
                        "category": categorize_token(prop_name, value),
                        "sourceFile": str(file_path.relative_to(SCSS_BASE.parent)),
                        "sourceLine": line_num,
                        "rootBlock": root_context,
                        "references": [],
                        "usageCount": 0
                    }

                # Exit :root block when braces close
                if brace_depth == 0:
                    in_root = False

    except Exception as e:
        print(f"Error extracting custom properties from {file_path}: {e}")

    return properties

def extract_scss_maps(file_path: Path) -> Dict[str, Any]:
    """Extract SCSS maps with their key-value pairs."""
    maps = {}

    try:
        content = file_path.read_text(encoding='utf-8')

        # Match SCSS map declarations
        map_pattern = r'\$([a-zA-Z0-9_-]+)\s*:\s*\(([^;]+)\);'
        matches = re.finditer(map_pattern, content, re.DOTALL)

        for match in matches:
            map_name = f"${match.group(1)}"
            map_content = match.group(2)

            # Extract key-value pairs
            entries = {}
            pair_pattern = r'["\']?([a-zA-Z0-9_-]+)["\']?\s*:\s*([^,\n]+)'
            for pair_match in re.finditer(pair_pattern, map_content):
                key = pair_match.group(1).strip()
                value = pair_match.group(2).strip()
                entries[key] = {
                    "value": value,
                    "computedValue": value  # Could enhance this
                }

            maps[map_name] = {
                "sourceFile": str(file_path.relative_to(SCSS_BASE.parent)),
                "entries": entries
            }
    except Exception as e:
        print(f"Error extracting maps from {file_path}: {e}")

    return maps

def find_references(search_term: str, scss_files: List[Path]) -> List[Dict[str, Any]]:
    """Find all references to a variable/property across SCSS files."""
    references = []

    for file_path in scss_files:
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')

            for line_num, line in enumerate(lines, 1):
                # Look for usage (not declaration)
                if search_term in line and not line.strip().startswith(search_term + ':'):
                    # Exclude the declaration line itself
                    if not re.match(rf'^\s*{re.escape(search_term)}\s*:', line):
                        references.append({
                            "file": str(file_path.relative_to(SCSS_BASE.parent)),
                            "line": line_num,
                            "context": line.strip()[:100]  # First 100 chars
                        })
        except Exception as e:
            print(f"Error searching {file_path}: {e}")

    return references

def expand_generated_properties() -> Dict[str, Any]:
    """Expand loop-generated CSS custom properties from v8-scss/_theme.scss."""
    generated = {}

    # Base colors x opacities
    base_colors = {
        'yellow': '#EFC005',
        'green': '#00C49A',
        'cyan': '#00BCD4',
        'blue': '#0087D9',
        'orange': '#FF9100',
        'vivid': '#7C80FE',
        'red': '#E57373',
        'indigo': '#3248F4'
    }

    opacities = {
        '100': 1.0,
        '200': 0.5,
        '300': 0.25
    }

    for color_name, color_value in base_colors.items():
        for opacity_suffix, opacity_value in opacities.items():
            prop_name = f"--{color_name}-{opacity_suffix}"
            # Compute blended color (simplified - actual blend-with-white calculation)
            generated[prop_name] = {
                "value": f"blend-with-white-to-hex({color_value}, {opacity_value})",
                "type": "color",
                "category": "color",
                "sourceFile": "forms-flow-theme/scss/v8-scss/_theme.scss",
                "sourceLine": 106,  # @each loop line
                "rootBlock": "v8-theme",
                "references": [],
                "usageCount": 0,
                "generatedBy": "@each $name, $color in $base-colors loop"
            }

    # Brand colors
    brand_colors = {
        'primary': '#F1EEFF',
        'primary-dark': '#B8ABFF',
        'secondary': '#EDEDED',
        'secondary-dark': '#525254',
        'vivid': '#7C80FE'
    }

    for name, value in brand_colors.items():
        prop_name = f"--{name}"
        if prop_name not in generated:  # Don't override if already exists
            generated[prop_name] = {
                "value": value,
                "type": "color",
                "category": "color",
                "sourceFile": "forms-flow-theme/scss/v8-scss/_theme.scss",
                "sourceLine": 112,
                "rootBlock": "v8-theme",
                "references": [],
                "usageCount": 0,
                "generatedBy": "@each $name, $color in $brand-colors loop"
            }

    # Neutral colors
    neutral_colors = {
        'gray-darkest': '#4A4A4A',
        'gray-dark': '#7C7D7F',
        'gray-medium-darker': '#9E9E9E',
        'gray-medium-dark': '#B7B7B8',
        'gray-medium': '#D1D2D3',
        'gray-light': '#D9D9D9',
        'gray-x-light': '#E5E5E5',
        'gray-xx-light': '#DAD9DA',
        'white-100': '#F6F6F6',
        'white-200': '#FCFCFC',
        'white-300': '#FFFFFF'
    }

    for name, value in neutral_colors.items():
        prop_name = f"--{name}"
        generated[prop_name] = {
            "value": value,
            "type": "color",
            "category": "color",
            "sourceFile": "forms-flow-theme/scss/v8-scss/_theme.scss",
            "sourceLine": 116,
            "rootBlock": "v8-theme",
            "references": [],
            "usageCount": 0,
            "generatedBy": "@each $name, $color in $neutral-colors loop"
        }

    # Font tokens
    font_tokens = {
        'font-family-base': '"Figtree", sans-serif',
        'font-weight-light': '300',
        'font-weight-regular': '400',
        'font-weight-medium': '500',
        'font-weight-semibold': '600',
        'line-height-default': '100%',
        'letter-spacing-default': '0%',
        'font-size-xl': '20px',
        'font-size-l': '18px',
        'font-size-m': '15px',
        'font-size-s': '12px',
        'font-size-xs': '10px'
    }

    for name, value in font_tokens.items():
        prop_name = f"--{name}"
        generated[prop_name] = {
            "value": value,
            "type": categorize_token(prop_name, value),
            "category": categorize_token(prop_name, value),
            "sourceFile": "forms-flow-theme/scss/v8-scss/_theme.scss",
            "sourceLine": 181,
            "rootBlock": "v8-theme",
            "references": [],
            "usageCount": 0,
            "generatedBy": "@each $name, $value in $font-tokens loop"
        }

    return generated

def main():
    """Main extraction logic."""
    print("Starting SCSS theme audit extraction...")

    # Find all SCSS files
    scss_files = list(SCSS_BASE.rglob("*.scss"))
    print(f"Found {len(scss_files)} SCSS files")

    # Extract all variables
    all_scss_vars = {}
    all_css_props = {}
    all_maps = {}

    for scss_file in scss_files:
        print(f"Processing {scss_file.name}...")

        # Extract SCSS variables
        vars_in_file = extract_scss_variables(scss_file)
        all_scss_vars.update(vars_in_file)

        # Extract CSS custom properties
        props_in_file = extract_css_custom_properties(scss_file)
        all_css_props.update(props_in_file)

        # Extract SCSS maps
        maps_in_file = extract_scss_maps(scss_file)
        all_maps.update(maps_in_file)

    # Add loop-generated properties
    print("Expanding loop-generated CSS properties...")
    generated_props = expand_generated_properties()
    all_css_props.update(generated_props)

    # Find references for commonly-used variables
    print("Finding cross-file references...")
    common_vars = ['$primary', '$white', '$black', '$gray-darkest', '$gray-medium', '$base']
    common_props = ['--spacer-100', '--primary', '--navbar-width']

    for var in common_vars:
        if var in all_scss_vars:
            refs = find_references(var, scss_files)
            all_scss_vars[var]["references"] = refs
            all_scss_vars[var]["usageCount"] = len(refs)

    for prop in common_props:
        if prop in all_css_props:
            refs = find_references(prop, scss_files)
            all_css_props[prop]["references"] = refs
            all_css_props[prop]["usageCount"] = len(refs)

    # Extract mixins and functions
    print("Documenting mixins and functions...")
    mixins = {
        "font-style": {
            "sourceFile": "forms-flow-theme/scss/v8-scss/_mixins.scss",
            "parameters": ["$font-size", "$font-weight", "$color"],
            "designValuesProduced": "Typography styles using v8 design tokens"
        },
        "custom-scroll": {
            "sourceFile": "forms-flow-theme/scss/v8-scss/_mixins.scss",
            "parameters": ["$width", "$thumb-height"],
            "designValuesProduced": "Custom scrollbar styling"
        },
        "vertical-padding": {
            "sourceFile": "forms-flow-theme/scss/v8-scss/_mixins.scss",
            "parameters": [],
            "designValuesProduced": "Consistent vertical padding for containers"
        },
        "generate-overflow": {
            "sourceFile": "forms-flow-theme/scss/_variables.scss",
            "parameters": ["$axis", "$value"],
            "designValuesProduced": "Overflow utility classes"
        }
    }

    functions = {
        "blend-with-white-to-hex": {
            "sourceFile": "forms-flow-theme/scss/v8-scss/_theme.scss",
            "purpose": "Blend colors with white background to achieve opacity variants",
            "designImpact": "Generates 50% and 25% opacity variants of base colors for the v8 design system"
        }
    }

    # Build final audit object
    audit = {
        "metadata": {
            "auditDate": datetime.now().strftime("%Y-%m-%d"),
            "sourceDirectory": "forms-flow-theme/scss",
            "totalFiles": len(scss_files),
            "totalVariables": len(all_scss_vars),
            "totalCustomProperties": len(all_css_props),
            "totalMaps": len(all_maps)
        },
        "scssVariables": all_scss_vars,
        "cssCustomProperties": all_css_props,
        "scssMaps": all_maps,
        "scssMixins": mixins,
        "scssFunctions": functions
    }

    # Write to JSON
    output_path = SCSS_BASE.parent.parent / "tokens" / "audit" / "theme-audit.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(audit, f, indent=2, ensure_ascii=False)

    print(f"\nAudit complete!")
    print(f"Total SCSS Variables: {len(all_scss_vars)}")
    print(f"Total CSS Custom Properties: {len(all_css_props)}")
    print(f"Total SCSS Maps: {len(all_maps)}")
    print(f"Output: {output_path}")

if __name__ == "__main__":
    main()
