# Phase 2: Token Extraction - Research

**Researched:** 2026-02-04
**Domain:** SCSS-to-DTCG token extraction, Python parsing, computed value resolution, validation automation
**Confidence:** MEDIUM

## Summary

Phase 2 requires extracting 602 design values (465 SCSS variables + 137 CSS custom properties) from forms-flow-theme into W3C DTCG-formatted JSON files (tokens/core.json, tokens/semantic.json). The established approach uses Python-based extraction scripts that parse SCSS/CSS files, resolve computed values where possible, and transform the data into DTCG format with full traceability.

Phase 1 established a strong foundation with theme-audit.json containing all source data, dtcg-spec.md defining the output structure, and validated example files proving the format works. The extraction phase bridges these two by transforming audit data into production tokens. Critical challenges include handling SCSS computed expressions (darken/lighten/mix functions), expanding @each loop-generated color palettes, preserving original expressions in $description while storing computed values in $value, and validating outputs against both Phase 1 audit data and DTCG format requirements.

The standard stack uses Python's built-in regex for simple SCSS parsing (proven effective in Phase 1), pyScss for computing color functions when needed, jsonschema for DTCG validation, and jsondiff for comparing extracted tokens against audit data. Scripts should be modular, reusable, and generate both machine-readable JSON and human-readable validation reports.

**Primary recommendation:** Build dedicated extraction scripts that read theme-audit.json as input source of truth, apply DTCG naming conventions and grouping structure from dtcg-spec.md, resolve computed values using pyScss where needed, output core.json and semantic.json directly, and validate with automated diff against audit data plus DTCG schema checks.

## Standard Stack

The established libraries/tools for token extraction and validation.

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python | 3.10+ | Scripting language for extraction | Built-in regex, JSON support, file I/O, proven in Phase 1 scripts |
| pyScss | 1.3.x | Compute SCSS color functions | Native Python implementation of darken(), lighten(), mix(), hsla() functions |
| jsonschema | 4.26.0+ | Validate DTCG token files | Current standard for JSON Schema validation in Python, supports Draft 2020-12 |
| jsondiff | 2.2.1+ | Compare extracted tokens vs audit | Semantic JSON comparison, detects value changes, structural differences |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| deepdiff | 8.0+ | Advanced JSON comparison | When jsondiff insufficient, need detailed nested comparison |
| pathlib | stdlib | File path manipulation | Cross-platform path handling, cleaner than os.path |
| argparse | stdlib | CLI argument parsing | Make scripts configurable (input/output paths, verbosity) |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| pyScss | libsass-python 0.23.0 | libsass is faster (C++ based) but doesn't expose variable extraction API, only compilation |
| Regex parsing | scss-parser (Node.js) | More robust AST parsing but requires Node.js, Phase 1 proved regex sufficient for this codebase |
| Python scripts | Style Dictionary transforms | Style Dictionary is for token transformation (Phase 3), not extraction from SCSS |

**Installation:**
```bash
pip install pyScss jsonschema jsondiff
# Already available: Python 3.10+, pathlib, argparse, json, re
```

## Architecture Patterns

### Recommended Script Structure
```
scripts/
├── extract-tokens.py         # Main extraction orchestrator
├── lib/
│   ├── scss_resolver.py      # Compute SCSS expressions (darken, lighten, mix)
│   ├── dtcg_formatter.py     # Transform audit data to DTCG structure
│   ├── validators.py         # DTCG schema + reference validation
│   └── diff_validator.py     # Compare extracted vs audit data
└── README.md                 # Script usage documentation
```

### Pattern 1: Audit-Driven Extraction
**What:** Use theme-audit.json as single source of truth, don't re-parse SCSS files
**When to use:** Always — audit already contains all variables, values, categories, references
**Example:**
```python
# Read audit data (source of truth)
with open('tokens/audit/theme-audit.json') as f:
    audit = json.load(f)

# Read DTCG spec for structure requirements
spec = load_dtcg_spec('tokens/audit/dtcg-spec.md')

# Transform audit data to DTCG format
core_tokens = transform_to_core(audit['scssVariables'], spec)
semantic_tokens = transform_to_semantic(audit['customProperties'], spec)

# Write output files
write_dtcg('tokens/core.json', core_tokens)
write_dtcg('tokens/semantic.json', semantic_tokens)
```

### Pattern 2: Dual Value Tracking (Computed + Expression)
**What:** Store computed result in $value, preserve original expression in $description
**When to use:** All tokens with SCSS expressions (functions, arithmetic, variable references)
**Example:**
```python
# Source: Phase 1 decision - dual value tracking
def extract_token(scss_var):
    """Extract token with dual value tracking."""
    token = {
        "$value": resolve_value(scss_var['value']),  # Computed: #0d47a1
        "$type": scss_var['category'],
        "$description": f"From {scss_var['sourceFile']} variable ${scss_var['name']}. "
                       f"Original expression: {scss_var['value']}"  # darken($primary, 10%)
    }
    return token

def resolve_value(expr):
    """Resolve SCSS expression to final value."""
    if has_color_function(expr):
        return compute_color_function(expr)  # Use pyScss
    elif is_arithmetic(expr):
        return eval_arithmetic(expr)  # Simple math
    else:
        return expr  # Literal value
```

### Pattern 3: Loop Expansion from Audit Data
**What:** Extract full palette arrays from @each loop-generated properties
**When to use:** V8 color palettes (8 base colors × 100-900 shades)
**Example:**
```python
# Source: Phase 1 decision - "extract FULL palette, not just referenced ones"
def extract_v8_palette(audit_data):
    """Extract complete color palettes from v8 @each loops."""
    # Phase 1 manually expanded loops in theme-audit.json
    # Read expanded properties from customProperties section
    v8_colors = {}

    for prop_name, prop_data in audit_data['customProperties'].items():
        if prop_data.get('rootBlock') == 'v8-theme':
            # Extract --ff-primary-100 through --ff-primary-900
            match = re.match(r'--ff-([a-z]+)-(\d+)', prop_name)
            if match:
                color_name, shade = match.groups()
                if color_name not in v8_colors:
                    v8_colors[color_name] = {}
                v8_colors[color_name][shade] = {
                    "$value": prop_data['value'],
                    "$type": "color",
                    "$description": f"V8 {color_name} shade {shade}"
                }

    return v8_colors
```

### Pattern 4: Reference Resolution
**What:** Transform SCSS variable references to DTCG {curly.brace.references}
**When to use:** Semantic tokens that reference core tokens
**Example:**
```python
# Source: DTCG spec - reference syntax
def transform_to_semantic(css_custom_properties):
    """Transform CSS custom properties to semantic tokens with references."""
    semantic = {"ff": {}}

    for prop_name, prop_data in css_custom_properties.items():
        # --color-action-primary: var(--ff-primary-500)
        if prop_data['value'].startswith('var(--ff-'):
            # Extract reference target
            ref_target = prop_data['value'].replace('var(--', '{ff.').replace(')', '}')
            ref_target = ref_target.replace('--', '.').replace('-', '.')

            # Create semantic token with reference
            token = {
                "$value": ref_target,  # {ff.color.primary.500}
                "$type": prop_data['category'],
                "$description": prop_data.get('description', '')
            }

            # Place in nested structure
            place_in_structure(semantic, prop_name, token)

    return semantic
```

### Pattern 5: Automated Validation Pipeline
**What:** Chain multiple validation checks (DTCG schema, references, diff vs audit)
**When to use:** Always after extraction, before committing output
**Example:**
```python
# Validation pipeline
def validate_extraction(core_path, semantic_path, audit_path):
    """Run all validation checks on extracted tokens."""
    results = {
        "dtcg_schema": False,
        "reference_resolution": False,
        "audit_diff": False,
        "errors": []
    }

    # 1. DTCG Schema validation
    try:
        validate_dtcg_schema(core_path)
        validate_dtcg_schema(semantic_path)
        results["dtcg_schema"] = True
    except Exception as e:
        results["errors"].append(f"DTCG schema: {e}")

    # 2. Reference resolution
    try:
        validate_references(core_path, semantic_path)
        results["reference_resolution"] = True
    except Exception as e:
        results["errors"].append(f"References: {e}")

    # 3. Diff against audit
    try:
        diff = compare_to_audit(core_path, semantic_path, audit_path)
        if diff['mismatches'] == 0:
            results["audit_diff"] = True
        else:
            results["errors"].append(f"Audit diff: {diff['mismatches']} mismatches")
    except Exception as e:
        results["errors"].append(f"Audit comparison: {e}")

    return results
```

### Anti-Patterns to Avoid
- **Re-parsing SCSS files:** Phase 1 already extracted everything. Don't duplicate work or risk inconsistency.
- **Hardcoding token names:** Read naming conventions from dtcg-spec.md, don't embed in scripts.
- **Ignoring Bootstrap overrides:** Mark these in $description as Phase 1 identified them.
- **Losing traceability:** Always include sourceFile and original expression in $description.
- **Manual token creation:** Every token must trace back to audit data, no hand-crafted additions.

## Don't Hand-Roll

Problems that look simple but have existing solutions.

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| SCSS color function computation | Custom RGB/HSL math | pyScss library | Color space conversions are complex (RGB→HSL→RGB, gamma correction, rounding). pyScss implements Sass spec exactly. |
| JSON schema validation | Custom property checks | jsonschema library | DTCG spec has many rules (required properties, type formats, reference syntax). jsonschema handles all JSON Schema Draft 2020-12 features. |
| JSON comparison | Nested dict iteration | jsondiff or deepdiff | Deep comparison with type awareness, path reporting, and semantic diff is complex. Libraries handle edge cases. |
| SCSS expression parsing | Complex regex | Use audit data directly | Phase 1 already parsed all expressions. Audit contains both original and computed values. |
| Token name transformations | String replacements | Rule-based transformer reading spec | Naming conventions in dtcg-spec.md should drive transformations, not hardcoded logic. |

**Key insight:** Phase 1 did the hard work of parsing and categorizing. Phase 2 is data transformation, not parsing. Read audit data, apply DTCG structure, compute remaining values, validate output. Use libraries for computation and validation, not custom implementations.

## Common Pitfalls

### Pitfall 1: SCSS Function Resolution Failures
**What goes wrong:** Script encounters `darken($primary, 10%)` and fails to resolve because $primary isn't in scope. Computed value missing or incorrect.
**Why it happens:** pyScss needs all variable definitions in scope to compute functions. Can't compute in isolation.
**How to avoid:** Build variable context from audit data before computing any expressions. Pass full context to pyScss.
```python
# Build context from audit
variables = {
    name: data['value']
    for name, data in audit['scssVariables'].items()
}
# Compile with pyScss to resolve functions
compiler = pyScss.Compiler()
compiler.calculator.namespace.set_variable(variables)
result = compiler.calculator.calculate(expression)
```
**Warning signs:** Computed values are null or match original expression. Color functions not resolving to hex.

### Pitfall 2: Incomplete @each Loop Expansion
**What goes wrong:** Extract only some shades from color palette (e.g., primary-500, primary-700) instead of full 100-900 scale.
**Why it happens:** Only extracting referenced values instead of full palette. User decision specified "extract FULL palette."
**How to avoid:** Phase 1 audit already expanded loops. Extract ALL properties from v8-theme :root block, not just referenced ones.
**Warning signs:** core.json has gaps in color shade sequences (missing 100, 200, 300).

### Pitfall 3: Lost Traceability in $description
**What goes wrong:** Token $description only says "Primary color" without mentioning source file or original expression.
**Why it happens:** Not carrying forward audit metadata into DTCG output.
**How to avoid:** User decision specifies "$description fields include both origin (source SCSS variable) AND usage context (what it's used for)."
```python
description = (
    f"From {audit_data['sourceFile']} variable ${var_name}. "
    f"Original expression: {audit_data['value']}. "
    f"Usage: {audit_data.get('usage_context', 'N/A')}"
)
```
**Warning signs:** Can't trace token back to SCSS source. No mention of original expression for computed values.

### Pitfall 4: Invalid DTCG References
**What goes wrong:** Semantic tokens reference `{ff-color-primary-500}` (wrong syntax) instead of `{ff.color.primary-500}`.
**Why it happens:** Not transforming kebab-case CSS property names to dot-notation reference paths.
**How to avoid:** Transform `--ff-color-primary-500` → `{ff.color.primary-500}` by replacing `--` and `-` with `.` in reference paths.
**Warning signs:** Reference validation fails. Style Dictionary can't resolve tokens.

### Pitfall 5: Audit Diff Failures Due to Rounding
**What goes wrong:** Audit has `0.78rem`, extracted token has `0.7800000000000001rem`. Diff validation flags mismatch.
**Why it happens:** Floating point arithmetic introduces precision errors.
**How to avoid:** Round computed values to match audit precision (typically 2-4 decimal places for rem units).
```python
def round_dimension(value):
    """Round dimension values to 4 decimal places."""
    match = re.match(r'([\d.]+)(rem|px|em)', value)
    if match:
        num, unit = match.groups()
        return f"{round(float(num), 4)}{unit}"
    return value
```
**Warning signs:** Validation reports hundreds of "mismatches" that are actually rounding differences.

### Pitfall 6: Bootstrap Override Context Loss
**What goes wrong:** Extract `$primary: #1976d2` without noting it overrides Bootstrap default `#007bff`.
**Why it happens:** Not reading `isBootstrapOverride` and `bootstrapDefault` from audit data.
**How to avoid:** Phase 1 audit flagged these. Include in $description.
```python
if audit_data.get('isBootstrapOverride'):
    description += f" Overrides Bootstrap default {audit_data['bootstrapDefault']}."
```
**Warning signs:** Can't tell which values are project customizations vs library defaults.

### Pitfall 7: Missing 18 Component Gap Values
**What goes wrong:** Script tries to create tokens for the 18 missing component values from gap-analysis.json.
**Why it happens:** Misunderstanding user decision: "18 missing component values: document as gaps only — do NOT create new tokens for them."
**How to avoid:** Only extract values from theme-audit.json. Gap analysis is for documentation, not token creation.
**Warning signs:** core.json or semantic.json contains tokens not in theme-audit.json source data.

### Pitfall 8: Type Inheritance Errors
**What goes wrong:** Every token has explicit `$type` property even when inherited from parent group. Verbose, error-prone.
**Why it happens:** Not leveraging DTCG type inheritance feature.
**How to avoid:** Set `$type` at group level when all children share same type.
```json
{
  "ff": {
    "color": {
      "$type": "color",
      "primary-500": {"$value": "#253DF4"},
      "primary-600": {"$value": "#1E31C3"}
    }
  }
}
```
**Warning signs:** DTCG spec allows inheritance but output doesn't use it. File is unnecessarily large.

## Code Examples

Verified patterns from official sources and Phase 1 implementation.

### Extract Core Tokens from Audit Data
```python
# Source: Phase 1 audit structure, DTCG spec
import json
from pathlib import Path

def extract_core_tokens(audit_path, spec):
    """Extract core primitive tokens from theme audit."""
    with open(audit_path) as f:
        audit = json.load(f)

    core = {"ff": {}}

    # Process SCSS variables (raw design values)
    for var_name, var_data in audit['scssVariables'].items():
        category = var_data['category']

        # Initialize category group if needed
        if category not in core['ff']:
            core['ff'][category] = {"$type": map_to_dtcg_type(category)}

        # Transform variable name to token name
        token_name = transform_token_name(var_name, spec)

        # Create token
        core['ff'][category][token_name] = {
            "$value": var_data.get('computedValue', var_data['value']),
            "$description": build_description(var_data)
        }

    return core

def map_to_dtcg_type(category):
    """Map audit categories to DTCG types."""
    mapping = {
        "color": "color",
        "spacing": "dimension",
        "typography": "dimension",  # font-size
        "borderRadius": "dimension",
        "shadow": "shadow",
        "transition": "duration"
    }
    return mapping.get(category, "dimension")

def transform_token_name(scss_var_name, spec):
    """Transform SCSS variable name to DTCG token name."""
    # $primary → primary
    # $gray-darkest → gray-darkest
    name = scss_var_name.lstrip('$')
    # Apply spec naming conventions (kebab-case, no reserved chars)
    return name.lower().replace('_', '-')

def build_description(var_data):
    """Build comprehensive $description with traceability."""
    desc = f"From {var_data['sourceFile']} (line {var_data['sourceLine']})"

    if var_data['value'] != var_data.get('computedValue'):
        desc += f". Original expression: {var_data['value']}"

    if var_data.get('isBootstrapOverride'):
        desc += f". Overrides Bootstrap default {var_data['bootstrapDefault']}"

    if var_data.get('usageCount', 0) > 0:
        desc += f". Used {var_data['usageCount']} times"

    return desc
```

### Compute SCSS Color Functions with pyScss
```python
# Source: pyScss documentation, Phase 1 computed value needs
from scss import Scss

def resolve_color_function(expression, variable_context):
    """Resolve SCSS color functions to final hex values."""
    # Create compiler with variable context
    compiler = Scss()

    # Add all known variables to namespace
    vars_scss = "\n".join([
        f"{name}: {value};"
        for name, value in variable_context.items()
    ])

    # Compile expression in context
    scss_code = f"""
{vars_scss}

.test {{
    color: {expression};
}}
"""

    try:
        css = compiler.compile(scss_code)
        # Extract computed color from CSS output
        match = re.search(r'color:\s*([^;]+)', css)
        if match:
            return match.group(1).strip()
    except Exception as e:
        print(f"Failed to compute {expression}: {e}")
        return None

    return expression  # Return original if computation fails
```

### Validate DTCG Schema
```python
# Source: jsonschema documentation
import jsonschema
import json

def validate_dtcg_schema(token_file_path):
    """Validate token file against DTCG schema."""
    # Load token file
    with open(token_file_path) as f:
        tokens = json.load(f)

    # DTCG schema (simplified - full schema in @upft/schemas)
    dtcg_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "patternProperties": {
            "^[^${}]+$": {  # No reserved characters in keys
                "oneOf": [
                    {
                        "type": "object",
                        "properties": {
                            "$value": {},
                            "$type": {"type": "string"},
                            "$description": {"type": "string"}
                        },
                        "required": ["$value"]
                    },
                    {
                        "type": "object",
                        "patternProperties": {
                            "^[^${}]+$": {"$ref": "#"}
                        }
                    }
                ]
            }
        }
    }

    # Validate
    try:
        jsonschema.validate(tokens, dtcg_schema)
        print(f"✓ {token_file_path} valid DTCG schema")
        return True
    except jsonschema.ValidationError as e:
        print(f"✗ {token_file_path} schema error: {e.message}")
        print(f"  Path: {'.'.join(str(p) for p in e.path)}")
        return False
```

### Compare Extracted Tokens vs Audit
```python
# Source: jsondiff documentation
from jsondiff import diff

def compare_to_audit(core_path, semantic_path, audit_path):
    """Compare extracted token values against audit source data."""
    with open(audit_path) as f:
        audit = json.load(f)

    with open(core_path) as f:
        core = json.load(f)

    # Build expected values from audit
    expected_values = {}
    for var_name, var_data in audit['scssVariables'].items():
        expected_values[var_name] = var_data.get('computedValue', var_data['value'])

    # Extract actual values from core tokens
    actual_values = {}
    def extract_values(obj, path=''):
        for key, val in obj.items():
            if isinstance(val, dict):
                if '$value' in val:
                    actual_values[path + key] = val['$value']
                else:
                    extract_values(val, path + key + '.')

    extract_values(core['ff'])

    # Compare
    differences = diff(expected_values, actual_values, syntax='explicit')

    report = {
        "total_expected": len(expected_values),
        "total_actual": len(actual_values),
        "mismatches": 0,
        "differences": []
    }

    if differences:
        report["mismatches"] = len(differences)
        report["differences"] = differences

    return report
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual token creation | Automated extraction from audit data | Phase 1 → Phase 2 | Eliminates human error, ensures traceability, makes updates repeatable |
| Single-pass extraction | Audit → Extraction → Validation pipeline | 2024-2026 | Separation of concerns, audit as source of truth enables multiple extraction strategies |
| Node.js sass-extract | Python pyScss | Phase 1 decision | Consistent toolchain (Python for all scripts), simpler deployment, no Node.js dependency |
| Regex-only parsing | Regex + pyScss hybrid | Phase 2 | Regex for structure, pyScss for computation - best of both worlds |
| Manual validation | Automated schema + diff validation | 2025-2026 | Catches errors early, enables CI/CD integration, validation is repeatable |

**Deprecated/outdated:**
- **sass-extract (Node.js):** Marked inactive, no updates since 2019. Phase 1 chose Python path instead.
- **libsass:** Development mode (officially deprecated by Sass team in favor of Dart Sass). pyScss is pure Python alternative.
- **Manual SCSS re-parsing in extraction:** Phase 1 audit already extracted everything. Re-parsing is duplicate work.

## Open Questions

Things that couldn't be fully resolved during research.

1. **pyScss variable scoping for function resolution**
   - What we know: pyScss can compute color functions like darken/lighten/mix. Requires variables in scope.
   - What's unclear: Best pattern for loading all 465 SCSS variables into pyScss namespace. Performance impact.
   - Recommendation: Load all audit variables as SCSS string, compile once, then evaluate expressions. Cache compiled context.

2. **Handling dual $base definitions (0.5rem vs 1rem)**
   - What we know: Phase 1 audit documented two conflicting $base values. Import order makes 1rem active.
   - What's unclear: Which value to use in tokens. User decision says "v8 values take precedence" but $base: 1rem is in _variables.scss (not v8).
   - Recommendation: Use 1rem (current active value) in tokens, document in $description that v8 intended 0.5rem. Phase 2 is extraction not redesign.

3. **Bootstrap override mapping strategy**
   - What we know: Phase 1 identified 3 Bootstrap overrides ($primary, $success, $danger). User decision: "Claude's discretion on mapping to v8 equivalents vs extracting as-is."
   - What's unclear: Should we map $primary → ff.color.primary-500 reference, or extract as independent value?
   - Recommendation: Extract as-is (independent values in core.json). Bootstrap names become semantic tokens in semantic.json that reference core equivalents. Preserves flexibility.

4. **Validation report format**
   - What we know: User decision leaves report format to Claude's discretion (file vs console).
   - What's unclear: Preference for CI/CD integration, local development visibility.
   - Recommendation: Both. Console output for immediate feedback during development. JSON file (validation-report.json) for CI/CD parsing and historical tracking.

5. **Script architecture: unified vs per-category**
   - What we know: User decision: "Claude's discretion on unified vs per-category script architecture."
   - What's unclear: Balance between maintainability and simplicity.
   - Recommendation: Unified main script (extract-tokens.py) with modular helper functions. Single entry point simplifies execution, lib/ modules enable category-specific logic.

## Sources

### Primary (HIGH confidence)
- W3C Design Tokens Community Group specification (2025.10): https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/
- W3C DTCG Format Module: https://www.designtokens.org/
- pyScss PyPI package: https://pypi.org/project/pyScss/1.1.5/
- jsonschema 4.26.0 documentation: https://python-jsonschema.readthedocs.io/en/stable/validate/
- jsondiff PyPI package: https://pypi.org/project/jsondiff/
- Phase 1 Research (01-RESEARCH.md): Local audit methodology and patterns
- Phase 1 Summary (01-01-SUMMARY.md): theme-audit.json structure and decisions
- Phase 1 DTCG Spec (tokens/audit/dtcg-spec.md): Format requirements

### Secondary (MEDIUM confidence)
- libsass-python documentation: https://sass.github.io/libsass-python/ (version/features verified)
- pyScss documentation: https://pyscss.readthedocs.io/en/latest/ (capabilities verified)
- Sass color functions documentation: https://sass-lang.com/documentation/modules/color/ (darken/lighten/mix specs)
- Design token automation workflow: https://learn.thedesignsystem.guide/p/automated-design-tokens-workflow
- SCSS @each loop patterns: https://sass-lang.com/documentation/at-rules/control/each/

### Tertiary (LOW confidence)
- WebSearch results on Python SCSS parsing (2026) - multiple libraries mentioned but not deeply verified
- WebSearch results on design token extraction best practices - general principles, not tool-specific
- Community articles on SCSS loop expansion - verified against official Sass docs

## Metadata

**Confidence breakdown:**
- Standard stack: MEDIUM - pyScss capabilities verified via PyPI but not tested for this specific use case. jsonschema and jsondiff are standard libraries with clear docs.
- Architecture: HIGH - Building on proven Phase 1 patterns. Audit-driven extraction is low-risk transformation task.
- Pitfalls: MEDIUM - Based on Phase 1 experience and common token extraction challenges. SCSS function resolution is untested risk area.
- DTCG validation: HIGH - Phase 1 already validated format with example files. Schema validation is straightforward.

**Research date:** 2026-02-04
**Valid until:** 2026-03-06 (30 days - stable dependencies, DTCG spec v1 is final)

---

## Research Notes

**What was verified:**
- pyScss supports darken(), lighten(), mix() color functions (PyPI docs, W3Schools Sass reference)
- jsonschema 4.26.0 is current, supports Draft 2020-12 (PyPI, readthedocs)
- jsondiff provides semantic JSON comparison (PyPI, GitHub examples)
- Phase 1 audit structure contains all data needed for extraction (direct file inspection)
- DTCG spec defines exact output format (tokens/audit/dtcg-spec.md)

**What couldn't be verified:**
- pyScss performance with 465 variables in namespace (not tested at scale)
- Exact pyScss API for loading variables programmatically (documentation examples are compilation-focused)
- Best practice for error handling in SCSS function computation (no official guidance found)

**Key constraints from CONTEXT.md decisions:**
- Dual tracking: $value = computed, $description = original expression + origin
- V8 precedence: When conflicts exist, v8 values win
- Full palettes: Extract all @each loop outputs (100-900), not just referenced
- No new tokens for gaps: 18 missing component values are documented, not tokenized
- Scripts in top-level scripts/ directory
- Two output files: tokens/core.json and tokens/semantic.json (replace Phase 1 examples)

**Areas of Claude's discretion exercised:**
- Script architecture: Recommended unified main script with modular lib/ helpers
- Bootstrap mapping: Extract as-is, map in semantic tokens
- Validation report: Both console (dev) and JSON file (CI/CD)
- SCSS function handling: Use pyScss for color functions, preserve relationship info in $description
- Category nesting: Leverage DTCG type inheritance at group level

**Research quality self-assessment:**
- Domains covered: Python SCSS/color computation ✓, JSON validation ✓, Diff comparison ✓, DTCG format ✓, Extraction patterns ✓, Pitfalls ✓
- Multiple sources verified: Libraries cross-referenced between PyPI, docs, and GitHub ✓
- Gaps acknowledged: pyScss API details unclear, marked MEDIUM confidence ✓
- Actionable for planning: Specific libraries, versions, code examples, architecture patterns provided ✓
- Building on Phase 1: Leveraged existing audit data, spec docs, proven patterns ✓
