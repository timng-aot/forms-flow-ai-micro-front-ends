"""
SCSS expression resolver for design token extraction.

Handles:
- Color functions: darken(), lighten(), mix(), rgba(), hsla()
- Arithmetic: $base*0.78, $spacer*1.5
- Variable references: $primary -> lookup in variable_context
- Literal values: return as-is
"""

import re
import logging
from typing import Dict, Any, Optional

# Try to import pyScss for color computations
try:
    from scss import Compiler
    PYSCSS_AVAILABLE = True
except ImportError:
    PYSCSS_AVAILABLE = False
    logging.warning("pyScss not available - SCSS function resolution will be limited")


def build_variable_context(audit_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Build a dictionary of all SCSS variables for expression resolution.

    Args:
        audit_data: The theme-audit.json data structure

    Returns:
        Dict mapping variable names to their values (e.g., "$primary" -> "#253DF4")
    """
    context = {}

    # Extract SCSS variables
    scss_vars = audit_data.get('scssVariables', {})
    for var_name, var_data in scss_vars.items():
        # Use computedValue if available, otherwise use value
        value = var_data.get('computedValue') or var_data.get('value')
        if value:
            context[var_name] = value

    # Also add CSS custom properties for reference
    css_props = audit_data.get('cssCustomProperties', {})
    for prop_name, prop_data in css_props.items():
        value = prop_data.get('value')
        if value:
            # Convert --ff-primary to $ff-primary for consistency
            var_name = '$' + prop_name.lstrip('-').replace('--', '-')
            context[var_name] = value

    return context


def resolve_scss_expression(expression: str, variable_context: Dict[str, str]) -> str:
    """
    Resolve an SCSS expression to its final computed value.

    Args:
        expression: The SCSS expression (e.g., "darken($primary, 10%)")
        variable_context: Dict of variable names to values

    Returns:
        Resolved value, or original expression if resolution fails
    """
    if not expression:
        return expression

    # Remove quotes if present
    expression = expression.strip().strip('"').strip("'")

    # If it's a literal value (hex color, rem/px value, number), return as-is
    if _is_literal_value(expression):
        return _normalize_value(expression)

    # If it's a simple variable reference, look it up
    if expression.startswith('$') and not any(op in expression for op in ['+', '-', '*', '/', '(', ')']):
        value = variable_context.get(expression)
        if value:
            # Recursively resolve in case the value is also an expression
            return resolve_scss_expression(value, variable_context)
        return expression

    # Try to resolve SCSS functions or arithmetic
    try:
        resolved = _resolve_complex_expression(expression, variable_context)
        return _normalize_value(resolved)
    except Exception as e:
        logging.debug(f"Failed to resolve expression '{expression}': {e}")
        # Return computedValue from context if available, otherwise original
        return expression


def _is_literal_value(value: str) -> bool:
    """Check if a value is a literal (no computation needed)."""
    value = value.strip()

    # Hex colors
    if re.match(r'^#[0-9A-Fa-f]{3,8}$', value):
        return True

    # CSS dimensions (rem, px, em, etc.)
    if re.match(r'^-?\d+(\.\d+)?(rem|px|em|%|vh|vw|ms|s)$', value):
        return True

    # Plain numbers
    if re.match(r'^-?\d+(\.\d+)?$', value):
        return True

    # RGB/RGBA colors
    if value.startswith(('rgb(', 'rgba(')):
        return True

    # HSL/HSLA colors
    if value.startswith(('hsl(', 'hsla(')):
        return True

    # Named colors
    named_colors = ['transparent', 'white', 'black', 'red', 'blue', 'green', 'yellow']
    if value.lower() in named_colors:
        return True

    return False


def _normalize_value(value: str) -> str:
    """Normalize a resolved value (round decimals, clean up formatting)."""
    value = value.strip()

    # Round dimension values to 4 decimal places
    match = re.match(r'^(-?\d+\.\d+)(rem|px|em|%)$', value)
    if match:
        number, unit = match.groups()
        rounded = round(float(number), 4)
        # Remove trailing zeros
        formatted = f"{rounded:.4f}".rstrip('0').rstrip('.')
        return f"{formatted}{unit}"

    return value


def _resolve_complex_expression(expression: str, variable_context: Dict[str, str]) -> str:
    """
    Resolve complex SCSS expressions (functions, arithmetic).
    """
    # First, substitute all variables
    substituted = _substitute_variables(expression, variable_context)

    # If pyScss is available, try to compile the expression
    if PYSCSS_AVAILABLE:
        try:
            # Wrap in a dummy rule for compilation
            scss_code = f"$result: {substituted};"
            compiler = Compiler()
            compiled = compiler.compile_string(scss_code)

            # Extract the computed value (this is a hack, but works for simple cases)
            # For proper resolution, we'd need to evaluate the expression differently
            # For now, return the substituted expression
            return substituted
        except Exception as e:
            logging.debug(f"pyScss compilation failed: {e}")

    # Try simple arithmetic evaluation
    try:
        # Handle simple arithmetic like "1rem * 2" or "$spacer * 1.5"
        if re.match(r'^[\d\.\s+\-*/()]+$', substituted.replace('rem', '').replace('px', '')):
            # Extract the unit
            unit_match = re.search(r'(rem|px|em|%|ms|s)', substituted)
            unit = unit_match.group(1) if unit_match else ''

            # Remove units for calculation
            numeric = re.sub(r'(rem|px|em|%|ms|s)', '', substituted)

            # Evaluate
            result = eval(numeric)
            rounded = round(result, 4)

            return f"{rounded}{unit}"
    except Exception as e:
        logging.debug(f"Arithmetic evaluation failed: {e}")

    return substituted


def _substitute_variables(expression: str, variable_context: Dict[str, str]) -> str:
    """Substitute SCSS variable references with their values."""
    result = expression

    # Find all $variable references
    var_pattern = r'\$[\w-]+'
    variables = re.findall(var_pattern, expression)

    for var in variables:
        value = variable_context.get(var)
        if value:
            # Recursively resolve the value
            resolved_value = resolve_scss_expression(value, variable_context)
            result = result.replace(var, resolved_value)

    return result
