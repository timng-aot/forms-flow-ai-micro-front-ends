"""
Audit Diff Validator

Compares extracted tokens against Phase 1 audit data to ensure values match.
"""

import json
import re
from typing import Dict, List, Tuple, Any


def compare_to_audit(core_path: str, semantic_path: str, audit_path: str) -> Dict[str, Any]:
    """
    Compare extracted tokens to audit data.

    Checks:
    - Token values match audit computedValue (or value if no computedValue)
    - Coverage: how many audit variables are represented in tokens

    Returns structured report dict.
    """
    # Load files
    with open(core_path, 'r') as f:
        core_data = json.load(f)
    with open(semantic_path, 'r') as f:
        semantic_data = json.load(f)
    with open(audit_path, 'r') as f:
        audit_data = json.load(f)

    mismatches = []
    audit_vars = audit_data.get("scssVariables", {})
    custom_props = audit_data.get("cssCustomProperties", {})

    # Count extractable variables (not 'other' category)
    extractable_vars = {k: v for k, v in audit_vars.items() if v.get("category") != "other"}
    total_extractable = len(extractable_vars) + len(custom_props)

    # Track which audit items were found in tokens
    found_in_tokens = 0
    not_found = []

    # Build a flat map of all tokens for easy lookup
    token_map = {}
    _flatten_tokens(core_data, token_map, [])
    _flatten_tokens(semantic_data, token_map, [])

    # Check SCSS variables
    for var_name, var_data in extractable_vars.items():
        # Look for token by matching $description (contains "Original: $var-name")
        matching_token = None
        normalized_var = _normalize_name(var_name)

        for token_path, token_value in token_map.items():
            if isinstance(token_value, dict):
                desc = token_value.get("$description", "")

                # First priority: exact variable name in description source
                if f":{var_name}" in desc or f"{var_name};" in desc:
                    matching_token = (token_path, token_value)
                    break

                # Second priority: normalized name at end of token path (exact match)
                if token_path.endswith(f".{normalized_var}"):
                    matching_token = (token_path, token_value)
                    break

        if matching_token:
            token_path, token_obj = matching_token
            found_in_tokens += 1

            # Compare values
            audit_value = var_data.get("computedValue") or var_data.get("value")
            token_value = token_obj.get("$value")

            # Skip comparison if audit value is a var() reference (not computed)
            if isinstance(audit_value, str) and audit_value.startswith("var("):
                continue

            # Skip comparison if audit value is an SCSS variable reference (not resolved)
            if isinstance(audit_value, str) and audit_value.startswith("$"):
                continue

            # Skip comparison if token value is a reference or expression
            if isinstance(token_value, str) and ("{" in token_value or "blend-with-white-to-hex" in token_value):
                continue

            # Skip comparison if audit value contains SCSS expressions
            if isinstance(audit_value, str) and ("$" in audit_value or "map-" in audit_value):
                continue

            # Skip shadow comparisons (shadows are now DTCG objects, audit has CSS strings)
            category = var_data.get("category", "")
            if isinstance(token_value, dict) and "color" in token_value and "offsetX" in token_value:
                # This is a DTCG shadow object, skip comparison
                continue

            # Type-specific comparison
            if not _values_match(audit_value, token_value, category):
                mismatches.append({
                    "audit_var": var_name,
                    "audit_value": audit_value,
                    "token_path": token_path,
                    "token_value": token_value,
                    "category": category
                })
        else:
            # Not found in tokens (might be intentionally skipped)
            not_found.append(var_name)

    # Check CSS custom properties
    for prop_name, prop_data in custom_props.items():
        # Look for token by matching description
        matching_token = None
        for token_path, token_value in token_map.items():
            if isinstance(token_value, dict):
                desc = token_value.get("$description", "")
                if prop_name in desc:
                    matching_token = (token_path, token_value)
                    break

        if matching_token:
            token_path, token_obj = matching_token
            found_in_tokens += 1

            # Compare values
            prop_value = prop_data.get("value")
            token_value = token_obj.get("$value")

            # Skip if reference
            if isinstance(token_value, str) and "{" in token_value:
                continue

            # Skip shadow comparisons (shadows are now DTCG objects, audit has CSS strings)
            if isinstance(token_value, dict) and "color" in token_value and "offsetX" in token_value:
                continue

            # Skip if audit value is a var() reference (not computed)
            if isinstance(prop_value, str) and prop_value.startswith("var("):
                continue

            if not _values_match(prop_value, token_value, "css-prop"):
                mismatches.append({
                    "audit_var": prop_name,
                    "audit_value": prop_value,
                    "token_path": token_path,
                    "token_value": token_value,
                    "category": "css-prop"
                })

    # Calculate coverage
    coverage_percent = (found_in_tokens / total_extractable * 100) if total_extractable > 0 else 0

    return {
        "total_extractable": total_extractable,
        "found_in_tokens": found_in_tokens,
        "coverage_percent": round(coverage_percent, 1),
        "mismatches": mismatches,
        "not_found_count": len(not_found),
        "not_found_sample": not_found[:10]  # First 10 for reference
    }


def _flatten_tokens(obj: Any, result: Dict, path: List[str]):
    """Flatten nested token structure into path -> token map."""
    if not isinstance(obj, dict):
        return

    if "$value" in obj:
        # This is a leaf token
        result[".".join(path)] = obj
        return

    for key, value in obj.items():
        if not key.startswith("$"):
            _flatten_tokens(value, result, path + [key])


def _normalize_name(var_name: str) -> str:
    """Normalize SCSS variable name for comparison."""
    # Remove $ prefix
    name = var_name.lstrip("$")
    # Convert underscores to hyphens
    name = name.replace("_", "-")
    return name.lower()


def _values_match(audit_value: Any, token_value: Any, category: str) -> bool:
    """
    Check if audit and token values match within tolerance.

    - Dimensions: within 0.001 units
    - Colors: exact match (or close for computed values)
    - Others: exact match
    """
    if audit_value is None or token_value is None:
        return audit_value == token_value

    # Convert to strings for comparison
    audit_str = str(audit_value).strip().strip('"').strip("'")
    token_str = str(token_value).strip().strip('"').strip("'")

    # Exact match first
    if audit_str.lower() == token_str.lower():
        return True

    # Dimension comparison with tolerance
    if category in ["spacing", "dimension", "size", "radius", "borderRadius"]:
        audit_num = _extract_number(audit_str)
        token_num = _extract_number(token_str)
        if audit_num is not None and token_num is not None:
            return abs(audit_num - token_num) < 0.001

    # For fontWeight, compare numeric values
    if category == "font-weight" or "weight" in category.lower() or category == "typography":
        audit_num = _extract_number(audit_str)
        token_num = _extract_number(token_str)
        if audit_num is not None and token_num is not None:
            return audit_num == token_num

    # Color comparison (normalize hex)
    if category == "color":
        return _normalize_color(audit_str) == _normalize_color(token_str)

    # Default: exact match required
    return False


def _extract_number(value_str: str) -> float:
    """Extract numeric value from string like '1.5rem' or '300'."""
    match = re.search(r'[-+]?\d*\.?\d+', value_str)
    if match:
        return float(match.group())
    return None


def _normalize_color(color_str: str) -> str:
    """Normalize color format for comparison."""
    color_str = color_str.strip().lower()

    # Expand 3-digit hex to 6-digit
    if re.match(r'^#[0-9a-f]{3}$', color_str):
        r, g, b = color_str[1], color_str[2], color_str[3]
        color_str = f"#{r}{r}{g}{g}{b}{b}"

    return color_str
