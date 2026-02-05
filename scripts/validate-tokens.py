#!/usr/bin/env python3
"""
Token Validation Pipeline

Validates extracted tokens against:
1. DTCG schema requirements
2. Reference resolution
3. Naming conventions
4. Audit data comparison

Exit code 0 = all pass, 1 = any failures
"""

import argparse
import json
import sys
from pathlib import Path

# Add scripts/lib to path
sys.path.insert(0, str(Path(__file__).parent / "lib"))

from validators import validate_dtcg_schema, validate_references, check_naming_conventions, count_tokens
from diff_validator import compare_to_audit


def main():
    parser = argparse.ArgumentParser(description="Validate design tokens")
    parser.add_argument("--core", default="tokens/core.json", help="Path to core tokens")
    parser.add_argument("--semantic", default="tokens/semantic.json", help="Path to semantic tokens")
    parser.add_argument("--audit", default="tokens/audit/theme-audit.json", help="Path to audit data")
    parser.add_argument("--output", default="tokens/validation-report.json", help="Output report path")
    args = parser.parse_args()

    # Load token files
    print("Loading token files...")
    with open(args.core, 'r') as f:
        core_data = json.load(f)
    with open(args.semantic, 'r') as f:
        semantic_data = json.load(f)

    # Initialize results
    results = {
        "timestamp": None,
        "files": {
            "core": args.core,
            "semantic": args.semantic,
            "audit": args.audit
        },
        "checks": {},
        "overall": "PASS"
    }

    all_passed = True

    # Check 1: DTCG Schema Validation - Core
    print("\n1. Validating DTCG schema (core.json)...")
    core_schema_errors = validate_dtcg_schema(core_data, "core.json")
    core_count, core_categories = count_tokens(core_data)

    if core_schema_errors:
        print(f"   FAIL: {len(core_schema_errors)} errors")
        for error in core_schema_errors[:5]:  # Show first 5
            print(f"     - {error}")
        if len(core_schema_errors) > 5:
            print(f"     ... and {len(core_schema_errors) - 5} more")
        all_passed = False
    else:
        print(f"   PASS ({core_count} tokens validated)")

    results["checks"]["dtcg_schema_core"] = {
        "status": "PASS" if not core_schema_errors else "FAIL",
        "token_count": core_count,
        "categories": core_categories,
        "errors": core_schema_errors
    }

    # Check 2: DTCG Schema Validation - Semantic
    print("\n2. Validating DTCG schema (semantic.json)...")
    semantic_schema_errors = validate_dtcg_schema(semantic_data, "semantic.json")
    semantic_count, semantic_categories = count_tokens(semantic_data)

    if semantic_schema_errors:
        print(f"   FAIL: {len(semantic_schema_errors)} errors")
        for error in semantic_schema_errors[:5]:
            print(f"     - {error}")
        if len(semantic_schema_errors) > 5:
            print(f"     ... and {len(semantic_schema_errors) - 5} more")
        all_passed = False
    else:
        print(f"   PASS ({semantic_count} tokens validated)")

    results["checks"]["dtcg_schema_semantic"] = {
        "status": "PASS" if not semantic_schema_errors else "FAIL",
        "token_count": semantic_count,
        "categories": semantic_categories,
        "errors": semantic_schema_errors
    }

    # Check 3: Reference Resolution
    print("\n3. Validating reference resolution...")
    reference_errors = validate_references(core_data, semantic_data)

    if reference_errors:
        print(f"   FAIL: {len(reference_errors)} unresolved references")
        for error in reference_errors[:5]:
            print(f"     - {error}")
        if len(reference_errors) > 5:
            print(f"     ... and {len(reference_errors) - 5} more")
        all_passed = False
    else:
        # Count references in semantic
        import re
        ref_count = 0
        def count_refs(obj):
            nonlocal ref_count
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if k == "$value" and isinstance(v, str) and "{ff." in v:
                        ref_count += 1
                    else:
                        count_refs(v)
        count_refs(semantic_data)
        print(f"   PASS ({ref_count}/{ref_count} references resolved)")

    results["checks"]["reference_resolution"] = {
        "status": "PASS" if not reference_errors else "FAIL",
        "errors": reference_errors
    }

    # Check 4: Naming Conventions - Core
    print("\n4. Checking naming conventions (core.json)...")
    core_naming_errors = check_naming_conventions(core_data, "core.json")

    if core_naming_errors:
        print(f"   FAIL: {len(core_naming_errors)} violations")
        for error in core_naming_errors[:5]:
            print(f"     - {error}")
        if len(core_naming_errors) > 5:
            print(f"     ... and {len(core_naming_errors) - 5} more")
        all_passed = False
    else:
        print(f"   PASS (0 violations)")

    results["checks"]["naming_conventions_core"] = {
        "status": "PASS" if not core_naming_errors else "FAIL",
        "errors": core_naming_errors
    }

    # Check 5: Naming Conventions - Semantic
    print("\n5. Checking naming conventions (semantic.json)...")
    semantic_naming_errors = check_naming_conventions(semantic_data, "semantic.json")

    if semantic_naming_errors:
        print(f"   FAIL: {len(semantic_naming_errors)} violations")
        for error in semantic_naming_errors[:5]:
            print(f"     - {error}")
        if len(semantic_naming_errors) > 5:
            print(f"     ... and {len(semantic_naming_errors) - 5} more")
        all_passed = False
    else:
        print(f"   PASS (0 violations)")

    results["checks"]["naming_conventions_semantic"] = {
        "status": "PASS" if not semantic_naming_errors else "FAIL",
        "errors": semantic_naming_errors
    }

    # Check 6: Audit Diff Comparison
    print("\n6. Comparing to audit data...")
    audit_report = compare_to_audit(args.core, args.semantic, args.audit)

    if audit_report["mismatches"]:
        print(f"   FAIL: {len(audit_report['mismatches'])} value mismatches")
        for mismatch in audit_report["mismatches"][:5]:
            print(f"     - {mismatch['audit_var']}: expected '{mismatch['audit_value']}', got '{mismatch['token_value']}'")
        if len(audit_report["mismatches"]) > 5:
            print(f"     ... and {len(audit_report['mismatches']) - 5} more")
        all_passed = False
    else:
        print(f"   PASS (0 mismatches, {audit_report['coverage_percent']}% coverage)")

    results["checks"]["audit_diff"] = {
        "status": "PASS" if not audit_report["mismatches"] else "FAIL",
        "coverage_percent": audit_report["coverage_percent"],
        "found_in_tokens": audit_report["found_in_tokens"],
        "total_extractable": audit_report["total_extractable"],
        "mismatches": audit_report["mismatches"],
        "not_found_count": audit_report["not_found_count"]
    }

    # Overall result
    results["overall"] = "PASS" if all_passed else "FAIL"

    # Print summary table
    print("\n" + "=" * 70)
    print("VALIDATION RESULTS")
    print("=" * 70)
    print(f"DTCG Schema (core.json):       {'PASS' if not core_schema_errors else 'FAIL':<10} ({core_count} tokens)")
    print(f"DTCG Schema (semantic.json):   {'PASS' if not semantic_schema_errors else 'FAIL':<10} ({semantic_count} tokens)")

    ref_status = 'PASS' if not reference_errors else 'FAIL'
    print(f"Reference Resolution:          {ref_status:<10}")

    print(f"Naming Conventions (core):     {'PASS' if not core_naming_errors else 'FAIL':<10} ({len(core_naming_errors)} violations)")
    print(f"Naming Conventions (semantic): {'PASS' if not semantic_naming_errors else 'FAIL':<10} ({len(semantic_naming_errors)} violations)")

    audit_status = 'PASS' if not audit_report["mismatches"] else 'FAIL'
    print(f"Audit Diff:                    {audit_status:<10} ({audit_report['coverage_percent']}% coverage, {len(audit_report['mismatches'])} mismatches)")

    print("-" * 70)
    print(f"OVERALL: {results['overall']}")
    print("=" * 70)

    # Write report
    import datetime
    results["timestamp"] = datetime.datetime.now().isoformat()

    with open(args.output, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nValidation report written to: {args.output}")

    # Exit with appropriate code
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
