#!/usr/bin/env python3
"""
Design Token Extraction Script

Transforms Phase 1 audit data (theme-audit.json) into production W3C DTCG-formatted
token files (tokens/core.json and tokens/semantic.json).

Usage:
    python3 scripts/extract-tokens.py
    python3 scripts/extract-tokens.py --audit-path custom/path.json --output-dir custom/dir/
"""

import json
import argparse
import logging
import sys
from pathlib import Path

# Add scripts dir to path for lib imports
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from lib import scss_resolver, dtcg_formatter


def setup_logging(verbose: bool = False):
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(levelname)s: %(message)s'
    )


def load_audit_data(audit_path: Path) -> dict:
    """Load and validate theme-audit.json."""
    if not audit_path.exists():
        logging.error(f"Audit file not found: {audit_path}")
        sys.exit(1)

    logging.info(f"Loading audit data from: {audit_path}")

    with open(audit_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Validate structure
    required_keys = ['scssVariables', 'cssCustomProperties', 'metadata']
    for key in required_keys:
        if key not in data:
            logging.error(f"Invalid audit data: missing '{key}' key")
            sys.exit(1)

    logging.info(f"Loaded {data['metadata']['totalVariables']} SCSS variables and "
                 f"{data['metadata']['totalCustomProperties']} CSS custom properties")

    return data


def write_token_file(output_path: Path, tokens: dict):
    """Write tokens to JSON file with proper formatting."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Ensure valid JSON
    json_str = json.dumps(tokens, ensure_ascii=False, indent=2)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(json_str)
        f.write('\n')  # Add trailing newline

    logging.info(f"Written: {output_path}")


def count_tokens(tokens: dict, prefix: str = "") -> int:
    """Recursively count token definitions (excludes groups)."""
    count = 0
    for key, value in tokens.items():
        if key.startswith('$'):
            # Skip DTCG properties
            continue
        if isinstance(value, dict):
            if '$value' in value:
                # This is a token
                count += 1
            else:
                # This is a group, recurse
                count += count_tokens(value, prefix=f"{prefix}.{key}" if prefix else key)
    return count


def count_tokens_by_category(tokens: dict) -> dict:
    """Count tokens by top-level category."""
    counts = {}

    if "ff" in tokens:
        ff_tokens = tokens["ff"]
        for category, category_data in ff_tokens.items():
            if category.startswith('$'):
                continue
            counts[category] = count_tokens(category_data)
    else:
        # Semantic tokens
        for category, category_data in tokens.items():
            if category.startswith('$'):
                continue
            counts[category] = count_tokens(category_data)

    return counts


def main():
    """Main extraction pipeline."""
    parser = argparse.ArgumentParser(
        description='Extract design tokens from theme audit data'
    )
    parser.add_argument(
        '--audit-path',
        type=Path,
        default=Path('tokens/audit/theme-audit.json'),
        help='Path to theme-audit.json (default: tokens/audit/theme-audit.json)'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('tokens'),
        help='Output directory for token files (default: tokens/)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    setup_logging(args.verbose)

    logging.info("=" * 60)
    logging.info("Design Token Extraction Pipeline")
    logging.info("=" * 60)

    # Load audit data
    audit_data = load_audit_data(args.audit_path)

    # Build SCSS variable context
    logging.info("Building SCSS variable context...")
    var_context = scss_resolver.build_variable_context(audit_data)
    logging.info(f"Context contains {len(var_context)} variables")

    # Generate core tokens
    logging.info("Generating core tokens...")
    core_tokens = dtcg_formatter.format_core_tokens(audit_data, scss_resolver)

    # Count core tokens
    core_counts = count_tokens_by_category(core_tokens)
    total_core = sum(core_counts.values())
    logging.info(f"Generated {total_core} core tokens:")
    for category, count in sorted(core_counts.items()):
        logging.info(f"  {category}: {count}")

    # Write core tokens
    core_path = args.output_dir / 'core.json'
    write_token_file(core_path, core_tokens)

    # Generate semantic tokens
    logging.info("Generating semantic tokens...")
    semantic_tokens = dtcg_formatter.format_semantic_tokens(audit_data, core_tokens)

    # Count semantic tokens
    semantic_counts = count_tokens_by_category(semantic_tokens)
    total_semantic = sum(semantic_counts.values())
    logging.info(f"Generated {total_semantic} semantic tokens:")
    for category, count in sorted(semantic_counts.items()):
        logging.info(f"  {category}: {count}")

    # Write semantic tokens
    semantic_path = args.output_dir / 'semantic.json'
    write_token_file(semantic_path, semantic_tokens)

    # Summary
    logging.info("=" * 60)
    logging.info("Extraction Complete")
    logging.info("=" * 60)
    logging.info(f"Core tokens: {total_core} (across {len(core_counts)} categories)")
    logging.info(f"Semantic tokens: {total_semantic} (across {len(semantic_counts)} categories)")
    logging.info(f"Total tokens: {total_core + total_semantic}")
    logging.info("")
    logging.info(f"Output files:")
    logging.info(f"  {core_path}")
    logging.info(f"  {semantic_path}")


if __name__ == '__main__':
    main()
