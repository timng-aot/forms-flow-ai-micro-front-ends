"""
DTCG formatter for transforming audit data into W3C DTCG token structure.

Transforms theme-audit.json into:
- core.json: Primitive design tokens
- semantic.json: Purpose-based tokens referencing core
"""

import re
import logging
from typing import Dict, Any, Optional, Tuple


def format_core_tokens(audit_data: Dict[str, Any], resolver) -> Dict[str, Any]:
    """
    Format audit data into DTCG core tokens structure.

    Args:
        audit_data: The theme-audit.json data
        resolver: The scss_resolver module with resolve_scss_expression function

    Returns:
        DTCG-formatted core tokens under "ff" top-level group
    """
    # Build variable context for resolution
    var_context = resolver.build_variable_context(audit_data)

    # Initialize core structure
    core = {
        "ff": {}
    }

    # Extract tokens by category
    _extract_colors(core["ff"], audit_data, var_context, resolver)
    _extract_spacing(core["ff"], audit_data, var_context, resolver)
    _extract_typography(core["ff"], audit_data, var_context, resolver)
    _extract_radius(core["ff"], audit_data, var_context, resolver)
    _extract_shadows(core["ff"], audit_data, var_context, resolver)
    _extract_durations(core["ff"], audit_data, var_context, resolver)

    return core


def format_semantic_tokens(audit_data: Dict[str, Any], core_tokens: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format semantic tokens that reference core tokens.

    Args:
        audit_data: The theme-audit.json data
        core_tokens: The generated core tokens for reference validation

    Returns:
        DTCG-formatted semantic tokens
    """
    semantic = {}

    # Extract semantic color tokens
    _extract_semantic_colors(semantic, audit_data, core_tokens)

    # Extract semantic spacing tokens
    _extract_semantic_spacing(semantic, audit_data, core_tokens)

    # Extract semantic typography tokens
    _extract_semantic_typography(semantic, audit_data, core_tokens)

    # Extract semantic radius tokens
    _extract_semantic_radius(semantic, core_tokens)

    # Extract semantic shadow tokens
    _extract_semantic_shadows(semantic, core_tokens)

    # Extract semantic duration tokens
    _extract_semantic_durations(semantic, core_tokens)

    return semantic


def _extract_colors(target: Dict, audit_data: Dict, var_context: Dict, resolver) -> None:
    """Extract color tokens from audit data."""
    target["color"] = {"$type": "color"}

    scss_vars = audit_data.get('scssVariables', {})
    css_props = audit_data.get('cssCustomProperties', {})

    # First, extract v8 color palettes from CSS custom properties
    v8_palettes = _extract_v8_color_palettes(css_props, var_context, resolver)
    for color_name, shades in v8_palettes.items():
        for shade_num, shade_value in shades.items():
            token_name = f"{color_name}-{shade_num}"
            target["color"][token_name] = {
                "$value": shade_value["value"],
                "$description": shade_value["description"]
            }

    # Extract SCSS color variables
    for var_name, var_data in scss_vars.items():
        if var_data.get('category') != 'color':
            continue

        # Skip variables that are just var() references (already handled via v8)
        value = var_data.get('value', '')
        if value.startswith('var('):
            continue

        # Resolve the expression
        computed = var_data.get('computedValue') or value
        resolved = resolver.resolve_scss_expression(value, var_context)

        # Create token name from variable name
        token_name = var_name.lstrip('$').replace('_', '-')

        # Build description
        desc_parts = []
        desc_parts.append(f"Source: {var_data.get('sourceFile', 'unknown')}:{var_data.get('sourceLine', '?')}")

        if value != resolved and not value.startswith('var('):
            desc_parts.append(f"Original: {value}")

        if var_data.get('isBootstrapOverride'):
            desc_parts.append("Bootstrap override")

        usage = var_data.get('usageCount', 0)
        if usage > 0:
            desc_parts.append(f"Used {usage} times")

        target["color"][token_name] = {
            "$value": resolved,
            "$description": " | ".join(desc_parts)
        }


def _extract_v8_color_palettes(css_props: Dict, var_context: Dict, resolver) -> Dict[str, Dict[str, Dict]]:
    """
    Extract v8 color palettes (100-900 shades for each base color).

    Returns: Dict of {color_name: {shade_num: {value, description}}}
    """
    palettes = {}

    for prop_name, prop_data in css_props.items():
        if prop_data.get('rootBlock') != 'v8-theme':
            continue

        # Look for color shade patterns like --ff-primary-500
        match = re.match(r'--ff-([a-z]+)-(\d{3})$', prop_name)
        if not match:
            continue

        color_name, shade_num = match.groups()

        # Initialize palette if needed
        if color_name not in palettes:
            palettes[color_name] = {}

        # Get value
        value = prop_data.get('value', '')

        # Resolve if it's an expression
        resolved = resolver.resolve_scss_expression(value, var_context)

        # Build description
        desc_parts = [f"v8 {color_name} palette shade {shade_num}"]
        if value != resolved and not _is_simple_value(value):
            desc_parts.append(f"Computed from: {value}")

        palettes[color_name][shade_num] = {
            "value": resolved,
            "description": " | ".join(desc_parts)
        }

    return palettes


def _extract_spacing(target: Dict, audit_data: Dict, var_context: Dict, resolver) -> None:
    """Extract spacing tokens."""
    target["spacing"] = {"$type": "dimension"}

    scss_vars = audit_data.get('scssVariables', {})

    # Collect spacing variables
    spacing_vars = {}
    for var_name, var_data in scss_vars.items():
        if var_data.get('category') != 'spacing':
            continue

        value = var_data.get('value', '')
        if value.startswith('var('):
            continue

        resolved = resolver.resolve_scss_expression(value, var_context)

        # Try to extract numeric multiplier for naming
        # e.g., $spacer * 0.25 -> 025, $spacer * 1 -> 100, $spacer * 2 -> 200
        spacing_vars[var_name] = {
            "value": resolved,
            "data": var_data
        }

    # Also check CSS custom properties for v8 spacing scale
    css_props = audit_data.get('cssCustomProperties', {})
    for prop_name, prop_data in css_props.items():
        if prop_data.get('rootBlock') == 'v8-theme' and '--spacer-' in prop_name:
            # Extract shade number
            match = re.match(r'--(?:ff-)?spacer-(\d{3})$', prop_name)
            if match:
                shade_num = match.group(1)
                value = prop_data.get('value', '')
                resolved = resolver.resolve_scss_expression(value, var_context)

                target["spacing"][shade_num] = {
                    "$value": resolved,
                    "$description": f"Spacing scale {shade_num} (v8)"
                }

    # Add common SCSS spacing variables with inferred numeric names
    for var_name, var_info in spacing_vars.items():
        token_name = _infer_spacing_token_name(var_name, var_info["value"])
        if token_name and token_name not in target["spacing"]:
            desc_parts = [f"Source: {var_info['data'].get('sourceFile', 'unknown')}:{var_info['data'].get('sourceLine', '?')}"]

            original_value = var_info['data'].get('value', '')
            if original_value != var_info["value"] and not original_value.startswith('var('):
                desc_parts.append(f"Original: {original_value}")

            target["spacing"][token_name] = {
                "$value": var_info["value"],
                "$description": " | ".join(desc_parts)
            }


def _extract_typography(target: Dict, audit_data: Dict, var_context: Dict, resolver) -> None:
    """Extract typography tokens (font-family, font-size, font-weight, line-height)."""
    scss_vars = audit_data.get('scssVariables', {})

    # Font families
    target["font-family"] = {"$type": "fontFamily"}
    for var_name, var_data in scss_vars.items():
        if 'font-family' not in var_name.lower():
            continue

        value = var_data.get('value', '')
        if value.startswith('var('):
            continue

        resolved = resolver.resolve_scss_expression(value, var_context)
        token_name = var_name.lstrip('$').replace('_', '-')

        target["font-family"][token_name] = {
            "$value": resolved.strip('"').strip("'"),
            "$description": f"Source: {var_data.get('sourceFile', 'unknown')}:{var_data.get('sourceLine', '?')}"
        }

    # Font sizes
    target["font-size"] = {"$type": "dimension"}
    for var_name, var_data in scss_vars.items():
        if var_data.get('category') != 'typography':
            continue
        if 'font-size' not in var_name.lower() and 'font' not in var_name.lower():
            continue
        if 'family' in var_name.lower() or 'weight' in var_name.lower():
            continue

        value = var_data.get('value', '')
        if value.startswith('var('):
            continue

        resolved = resolver.resolve_scss_expression(value, var_context)

        # Only include if it looks like a size (has rem, px, em)
        if not re.search(r'(rem|px|em)', resolved):
            continue

        token_name = var_name.lstrip('$').replace('_', '-')

        target["font-size"][token_name] = {
            "$value": resolved,
            "$description": f"Source: {var_data.get('sourceFile', 'unknown')}:{var_data.get('sourceLine', '?')}"
        }

    # Font weights - MUST be numbers, not strings
    target["font-weight"] = {"$type": "fontWeight"}
    for var_name, var_data in scss_vars.items():
        if 'font-weight' not in var_name.lower() and 'weight' not in var_name.lower():
            continue

        value = var_data.get('value', '')
        if value.startswith('var('):
            continue

        resolved = resolver.resolve_scss_expression(value, var_context)

        # Convert to number
        try:
            weight_num = int(resolved)
        except (ValueError, TypeError):
            continue

        token_name = var_name.lstrip('$').replace('_', '-')

        target["font-weight"][token_name] = {
            "$value": weight_num,  # Number, not string!
            "$description": f"Source: {var_data.get('sourceFile', 'unknown')}:{var_data.get('sourceLine', '?')}"
        }

    # Line heights
    target["line-height"] = {"$type": "number"}
    for var_name, var_data in scss_vars.items():
        if 'line-height' not in var_name.lower():
            continue

        value = var_data.get('value', '')
        if value.startswith('var('):
            continue

        resolved = resolver.resolve_scss_expression(value, var_context)
        token_name = var_name.lstrip('$').replace('_', '-')

        # Determine if it's unitless (number) or has units (dimension)
        try:
            # Try to parse as float for unitless values
            float_val = float(resolved)
            target["line-height"][token_name] = {
                "$value": float_val,
                "$type": "number",
                "$description": f"Source: {var_data.get('sourceFile', 'unknown')}:{var_data.get('sourceLine', '?')}"
            }
        except (ValueError, TypeError):
            # Has units, treat as dimension
            target["line-height"][token_name] = {
                "$value": resolved,
                "$type": "dimension",
                "$description": f"Source: {var_data.get('sourceFile', 'unknown')}:{var_data.get('sourceLine', '?')}"
            }


def _extract_radius(target: Dict, audit_data: Dict, var_context: Dict, resolver) -> None:
    """Extract border-radius tokens."""
    target["radius"] = {"$type": "dimension"}

    scss_vars = audit_data.get('scssVariables', {})
    for var_name, var_data in scss_vars.items():
        if var_data.get('category') != 'borderRadius':
            continue

        value = var_data.get('value', '')
        if value.startswith('var('):
            continue

        resolved = resolver.resolve_scss_expression(value, var_context)
        token_name = var_name.lstrip('$').replace('_', '-')

        target["radius"][token_name] = {
            "$value": resolved,
            "$description": f"Source: {var_data.get('sourceFile', 'unknown')}:{var_data.get('sourceLine', '?')}"
        }


def _extract_shadows(target: Dict, audit_data: Dict, var_context: Dict, resolver) -> None:
    """Extract shadow tokens in DTCG object format."""
    target["shadow"] = {"$type": "shadow"}

    scss_vars = audit_data.get('scssVariables', {})
    for var_name, var_data in scss_vars.items():
        if var_data.get('category') != 'shadow':
            continue

        value = var_data.get('value', '')
        if value.startswith('var('):
            continue

        resolved = resolver.resolve_scss_expression(value, var_context)

        # Convert CSS shadow string to DTCG object
        shadow_obj = shadow_css_to_dtcg(resolved)
        if not shadow_obj:
            continue

        token_name = var_name.lstrip('$').replace('_', '-')

        target["shadow"][token_name] = {
            "$value": shadow_obj,
            "$description": f"Source: {var_data.get('sourceFile', 'unknown')}:{var_data.get('sourceLine', '?')}"
        }


def _extract_durations(target: Dict, audit_data: Dict, var_context: Dict, resolver) -> None:
    """Extract transition/duration tokens."""
    target["duration"] = {"$type": "duration"}

    scss_vars = audit_data.get('scssVariables', {})
    for var_name, var_data in scss_vars.items():
        if var_data.get('category') != 'transition':
            continue

        value = var_data.get('value', '')
        if value.startswith('var('):
            continue

        resolved = resolver.resolve_scss_expression(value, var_context)

        # Only include if it looks like a duration (has ms or s)
        if not re.search(r'(ms|s)', resolved):
            continue

        token_name = var_name.lstrip('$').replace('_', '-')

        target["duration"][token_name] = {
            "$value": resolved,
            "$description": f"Source: {var_data.get('sourceFile', 'unknown')}:{var_data.get('sourceLine', '?')}"
        }


def shadow_css_to_dtcg(css_shadow: str) -> Optional[Dict[str, str]]:
    """
    Convert CSS box-shadow string to DTCG shadow object format.

    Example: "0px 2px 8px rgba(66, 66, 66, 0.07)" ->
    {
        "color": "rgba(66, 66, 66, 0.07)",
        "offsetX": "0px",
        "offsetY": "2px",
        "blur": "8px",
        "spread": "0px"
    }
    """
    if not css_shadow or css_shadow == 'none':
        return None

    # Pattern: offsetX offsetY blur spread color
    # or: offsetX offsetY blur color
    pattern = r'^\s*(-?\d+(?:\.\d+)?(?:px|rem)?)\s+(-?\d+(?:\.\d+)?(?:px|rem)?)\s+(-?\d+(?:\.\d+)?(?:px|rem)?)\s+(?:(-?\d+(?:\.\d+)?(?:px|rem)?)\s+)?(.+?)\s*$'

    match = re.match(pattern, css_shadow.strip())
    if not match:
        logging.warning(f"Could not parse shadow: {css_shadow}")
        return None

    offset_x, offset_y, blur, spread, color = match.groups()

    # If spread wasn't captured, it means it was omitted (defaults to 0)
    if spread is None:
        spread = "0px"
        # Color was actually in the spread position
        if color:
            pass
        else:
            color = spread

    # Ensure units
    def add_unit(val):
        if val and not re.search(r'(px|rem|em)$', val):
            return f"{val}px"
        return val

    return {
        "color": color.strip(),
        "offsetX": add_unit(offset_x),
        "offsetY": add_unit(offset_y),
        "blur": add_unit(blur),
        "spread": add_unit(spread)
    }


def _extract_semantic_colors(target: Dict, audit_data: Dict, core_tokens: Dict) -> None:
    """Extract semantic color tokens."""
    target["color"] = {"$type": "color"}

    # Bootstrap semantic names
    bootstrap_colors = {
        "primary": "primary-500",
        "secondary": "secondary-500",
        "success": "success-500",
        "danger": "danger-500",
        "warning": "warning-500",
        "info": "info-500",
        "light": "light-500",
        "dark": "dark-500"
    }

    for semantic_name, core_ref in bootstrap_colors.items():
        # Check if the core token exists
        if core_ref in core_tokens.get("ff", {}).get("color", {}):
            target["color"][semantic_name] = {
                "$value": f"{{ff.color.{core_ref}}}",
                "$description": f"Bootstrap semantic: {semantic_name}"
            }

    # Add action/background/text semantic groups
    if "action" not in target["color"]:
        target["color"]["action"] = {}

    if "background" not in target["color"]:
        target["color"]["background"] = {}

    if "text" not in target["color"]:
        target["color"]["text"] = {}


def _extract_semantic_spacing(target: Dict, audit_data: Dict, core_tokens: Dict) -> None:
    """Extract semantic spacing tokens (t-shirt sizes)."""
    target["spacing"] = {"$type": "dimension"}

    # Map t-shirt sizes to core spacing tokens
    spacing_map = {
        "xs": "025",
        "sm": "050",
        "md": "100",
        "lg": "150",
        "xl": "200"
    }

    for size, core_ref in spacing_map.items():
        if core_ref in core_tokens.get("ff", {}).get("spacing", {}):
            target["spacing"][size] = {
                "$value": f"{{ff.spacing.{core_ref}}}",
                "$description": f"Semantic spacing: {size}"
            }


def _extract_semantic_typography(target: Dict, audit_data: Dict, core_tokens: Dict) -> None:
    """Extract semantic typography tokens."""
    # Font family semantic
    target["font-family"] = {"$type": "fontFamily"}
    # Font weight semantic
    target["font-weight"] = {"$type": "fontWeight"}


def _extract_semantic_radius(target: Dict, core_tokens: Dict) -> None:
    """Extract semantic radius tokens."""
    target["radius"] = {"$type": "dimension"}


def _extract_semantic_shadows(target: Dict, core_tokens: Dict) -> None:
    """Extract semantic shadow tokens."""
    target["shadow"] = {"$type": "shadow"}


def _extract_semantic_durations(target: Dict, core_tokens: Dict) -> None:
    """Extract semantic duration tokens."""
    target["duration"] = {"$type": "duration"}


def _infer_spacing_token_name(var_name: str, value: str) -> Optional[str]:
    """
    Infer a numeric token name for spacing variables.

    Examples:
    - $spacer * 0.25 -> 025
    - $spacer * 1 -> 100
    - $spacer * 2 -> 200
    """
    # Try to extract multiplier from common patterns
    if 'spacer' in var_name.lower():
        # Check for patterns like spacer-sm, spacer-lg
        if '-sm' in var_name:
            return '050'
        elif '-md' in var_name or var_name == '$spacer':
            return '100'
        elif '-lg' in var_name:
            return '150'
        elif '-xl' in var_name:
            return '200'

    # Try to infer from value
    rem_match = re.match(r'^(\d+(?:\.\d+)?)rem$', value)
    if rem_match:
        rem_value = float(rem_match.group(1))
        if rem_value == 0.25:
            return '025'
        elif rem_value == 0.5:
            return '050'
        elif rem_value == 1.0:
            return '100'
        elif rem_value == 1.5:
            return '150'
        elif rem_value == 2.0:
            return '200'
        elif rem_value == 3.0:
            return '300'

    return None


def _is_simple_value(value: str) -> bool:
    """Check if a value is simple (not an expression)."""
    if not value:
        return True

    # Check for function calls
    if '(' in value and ')' in value:
        return False

    # Check for arithmetic
    if any(op in value for op in ['*', '/', '+', '-']):
        return False

    # Check for variable references
    if '$' in value or 'var(' in value:
        return False

    return True
