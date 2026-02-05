"""
DTCG Token Validation Module

Validates token files against DTCG schema requirements:
- Schema validation (proper $type, $value, $description)
- Reference resolution ({ff.*} references)
- Naming conventions (kebab-case, ff prefix)
- Token counting and categorization
"""

import re
from typing import Dict, List, Any, Set, Tuple


def validate_dtcg_schema(token_data: Dict, file_label: str) -> List[str]:
    """
    Validate tokens against DTCG schema requirements.

    Checks:
    - Every leaf token has $value (non-null)
    - Every leaf token has $type (explicit or inherited)
    - Every leaf token has $description (Phase 2 requirement)
    - No reserved characters in keys (except $ properties)
    - Type-specific format validation

    Returns list of error messages.
    """
    errors = []

    def walk_tree(obj: Any, path: List[str], inherited_type: str = None):
        """Recursively walk token tree."""
        if not isinstance(obj, dict):
            return

        # Check if this is a leaf token (has $value)
        if "$value" in obj:
            # This is a token - validate it
            token_path = ".".join(path)

            # Check $value exists and is non-null
            if obj["$value"] is None:
                errors.append(f"{file_label}: {token_path} - $value is null")

            # Check $description exists (Phase 2 requirement)
            if "$description" not in obj:
                errors.append(f"{file_label}: {token_path} - missing $description")

            # Determine token type
            token_type = obj.get("$type", inherited_type)
            if not token_type:
                errors.append(f"{file_label}: {token_path} - no $type (explicit or inherited)")
            else:
                # Type-specific validation
                validate_type_format(obj["$value"], token_type, token_path, file_label)

        # Check for reserved characters in keys
        for key in obj.keys():
            if key.startswith("$"):
                # DTCG properties are allowed
                continue
            if any(char in key for char in ["{", "}", "."]):
                errors.append(f"{file_label}: {'.'.join(path + [key])} - key contains reserved character ({{, }}, or .)")

        # Recurse into children
        current_type = obj.get("$type", inherited_type)
        for key, value in obj.items():
            if not key.startswith("$"):
                walk_tree(value, path + [key], current_type)

    def validate_type_format(value: Any, token_type: str, token_path: str, file_label: str):
        """Validate type-specific format requirements."""
        if token_type == "fontWeight":
            if not isinstance(value, (int, float)):
                # Check if it's a reference
                if not (isinstance(value, str) and value.startswith("{")):
                    errors.append(f"{file_label}: {token_path} - fontWeight $value must be a number, got {type(value).__name__}")

        elif token_type == "shadow":
            # Shadow must be an object with specific keys
            if isinstance(value, str) and value.startswith("{"):
                # It's a reference, skip validation
                pass
            elif isinstance(value, dict):
                required_keys = ["color", "offsetX", "offsetY", "blur", "spread"]
                missing = [k for k in required_keys if k not in value]
                if missing:
                    errors.append(f"{file_label}: {token_path} - shadow missing keys: {', '.join(missing)}")
            else:
                errors.append(f"{file_label}: {token_path} - shadow $value must be an object, got {type(value).__name__}")

        elif token_type == "dimension":
            if isinstance(value, str) and not value.startswith("{"):
                # Check for unit (rem, px, em, ms, s, %)
                if not re.search(r'(rem|px|em|ms|s|%)', value):
                    errors.append(f"{file_label}: {token_path} - dimension $value must contain a unit (rem, px, em, ms, s, %), got: {value}")

        elif token_type == "color":
            if isinstance(value, str) and not value.startswith("{"):
                # Check for valid color format
                hex_pattern = r'^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$'  # Support 8-digit hex (with alpha)
                rgb_pattern = r'^rgba?\([^)]+\)$'
                # Allow blend-with-white-to-hex() expressions
                blend_pattern = r'^blend-with-white-to-hex\('
                named_colors = ['transparent', 'black', 'white']

                is_valid = (
                    re.match(hex_pattern, value) or
                    re.match(rgb_pattern, value) or
                    re.match(blend_pattern, value) or
                    value.lower() in named_colors
                )

                if not is_valid:
                    errors.append(f"{file_label}: {token_path} - color $value has invalid format: {value}")

        elif token_type == "fontFamily":
            if not isinstance(value, str):
                if not (isinstance(value, str) and value.startswith("{")):
                    errors.append(f"{file_label}: {token_path} - fontFamily $value must be a string")

    # Start walking from root
    walk_tree(token_data, [])
    return errors


def validate_references(core_data: Dict, semantic_data: Dict) -> List[str]:
    """
    Validate that all references in semantic tokens resolve to core tokens.

    Extracts {ff.*} reference patterns and resolves them against core_data.
    Returns list of unresolved references.
    """
    errors = []
    references_found = []

    def extract_references(obj: Any, path: List[str]):
        """Recursively extract reference patterns."""
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == "$value" and isinstance(value, str) and "{" in value:
                    # Extract reference pattern
                    match = re.match(r'\{([^}]+)\}', value)
                    if match:
                        ref_path = match.group(1)
                        references_found.append((ref_path, ".".join(path)))

                extract_references(value, path + [key] if not key.startswith("$") else path)
        elif isinstance(obj, list):
            for item in obj:
                extract_references(item, path)

    # Extract all references from semantic tokens
    extract_references(semantic_data, [])

    # Resolve each reference
    for ref_path, semantic_path in references_found:
        # Split reference path (e.g., "ff.color.primary-500")
        parts = ref_path.split(".")

        # Navigate through core_data
        current = core_data
        resolved = True
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                errors.append(f"Unresolved reference: {ref_path} (used in {semantic_path})")
                resolved = False
                break

        # Check if we ended at a valid token (has $value)
        if resolved and isinstance(current, dict) and "$value" not in current:
            errors.append(f"Reference points to group, not token: {ref_path} (used in {semantic_path})")

    # Simple circular reference check (would need more sophisticated tracking for deep cycles)
    # For now, just check if semantic tokens reference other semantic tokens
    semantic_refs = [ref for ref, _ in references_found if not ref.startswith("ff.")]
    if semantic_refs:
        errors.append(f"Semantic tokens reference non-ff tokens (possible circular ref): {semantic_refs}")

    return errors


def check_naming_conventions(token_data: Dict, file_label: str) -> List[str]:
    """
    Check naming conventions:
    - All tokens under 'ff' top-level group (for core.json)
    - All keys are kebab-case (lowercase, numbers, hyphens only)
    - No duplicate keys within any group

    Returns list of violations.
    """
    errors = []

    # Check top-level structure for core.json
    if file_label == "core.json":
        if "ff" not in token_data:
            errors.append(f"{file_label}: Missing 'ff' top-level group")
        elif len(token_data) > 1:
            extra_keys = [k for k in token_data.keys() if k != "ff"]
            errors.append(f"{file_label}: Extra top-level keys (should only have 'ff'): {extra_keys}")

    # Kebab-case pattern: lowercase letters, numbers, hyphens
    kebab_pattern = r'^[a-z0-9]+(-[a-z0-9]+)*$'

    def check_keys(obj: Any, path: List[str], seen_keys: Dict[str, Set[str]]):
        """Recursively check key naming."""
        if not isinstance(obj, dict):
            return

        current_path = ".".join(path)
        if current_path not in seen_keys:
            seen_keys[current_path] = set()

        for key, value in obj.items():
            # Skip DTCG properties
            if key.startswith("$"):
                continue

            # Check for duplicates
            if key in seen_keys[current_path]:
                errors.append(f"{file_label}: {current_path}.{key} - duplicate key")
            seen_keys[current_path].add(key)

            # Check kebab-case
            if not re.match(kebab_pattern, key):
                errors.append(f"{file_label}: {current_path}.{key} - not kebab-case (use lowercase-with-hyphens)")

            # Recurse
            check_keys(value, path + [key], seen_keys)

    seen_keys = {}
    check_keys(token_data, [], seen_keys)
    return errors


def count_tokens(token_data: Dict) -> Tuple[int, Dict[str, int]]:
    """
    Count total tokens and per-category breakdown.

    Returns (total_count, category_counts)
    """
    total = 0
    categories = {}

    def walk_and_count(obj: Any, path: List[str], current_category: str = None):
        nonlocal total

        if not isinstance(obj, dict):
            return

        # If this is a leaf token
        if "$value" in obj:
            total += 1
            if current_category:
                categories[current_category] = categories.get(current_category, 0) + 1
            return

        # Recurse
        for key, value in obj.items():
            if not key.startswith("$"):
                # Track category based on second-level keys under 'ff'
                next_category = current_category
                if len(path) == 1 and path[0] == "ff":
                    next_category = key
                walk_and_count(value, path + [key], next_category)

    walk_and_count(token_data, [])
    return total, categories
