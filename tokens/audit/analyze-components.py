#!/usr/bin/env python3
"""
Analyze component SCSS files for hardcoded design values.
Produces components-audit.json and components-audit.md.
"""

import json
import re
from pathlib import Path
from datetime import date
from collections import defaultdict

# Component packages to scan
PACKAGES = {
    "forms-flow-admin": "forms-flow-admin/src",
    "forms-flow-nav": "forms-flow-nav/src",
    "forms-flow-review": "forms-flow-review/src",
    "forms-flow-submissions": "forms-flow-submissions/src",
    "forms-flow-components": "forms-flow-components/src"
}

# Patterns for detection
HEX_COLOR = re.compile(r'#[0-9a-fA-F]{3,8}\b')
RGB_RGBA = re.compile(r'rgba?\([^)]+\)')
HSL_HSLA = re.compile(r'hsla?\([^)]+\)')
PIXEL_VALUE = re.compile(r'\b(\d+\.?\d*)px\b')
REM_VALUE = re.compile(r'\b(\d+\.?\d*)rem\b')
EM_VALUE = re.compile(r'\b(\d+\.?\d*)em\b')
PERCENTAGE = re.compile(r'\b(\d+\.?\d*)%\b')

# Properties for spacing
SPACING_PROPS = {
    'padding', 'padding-top', 'padding-right', 'padding-bottom', 'padding-left',
    'margin', 'margin-top', 'margin-right', 'margin-bottom', 'margin-left',
    'gap', 'top', 'right', 'bottom', 'left', 'row-gap', 'column-gap'
}

# Typography properties
TYPOGRAPHY_PROPS = {
    'font-family', 'font-size', 'font-weight', 'line-height', 'letter-spacing'
}

# Border radius properties
BORDER_RADIUS_PROPS = {'border-radius', 'border-top-left-radius', 'border-top-right-radius',
                        'border-bottom-left-radius', 'border-bottom-right-radius'}

# Shadow properties
SHADOW_PROPS = {'box-shadow', 'text-shadow'}


class ComponentAuditor:
    def __init__(self):
        self.hardcoded_values = defaultdict(list)
        self.total_files = 0

    def is_variable_reference(self, value):
        """Check if value is a variable reference (SCSS or CSS custom property)."""
        if not value:
            return True
        value = value.strip()
        # SCSS variable
        if value.startswith('$'):
            return True
        # CSS custom property
        if 'var(--' in value:
            return True
        # Empty or whitespace
        if not value:
            return True
        return False

    def extract_property_value(self, line):
        """Extract CSS property and value from a line."""
        # Match property: value; or property: value
        match = re.match(r'\s*([a-z-]+)\s*:\s*([^;]+)', line, re.IGNORECASE)
        if match:
            return match.group(1).strip().lower(), match.group(2).strip()
        return None, None

    def categorize_value(self, value, prop):
        """Determine token type category for a value."""
        if prop in SPACING_PROPS:
            return 'spacing'
        elif prop in TYPOGRAPHY_PROPS:
            return 'typography'
        elif prop in BORDER_RADIUS_PROPS:
            return 'borderRadius'
        elif prop in SHADOW_PROPS:
            return 'shadows'
        elif prop in {'color', 'background-color', 'border-color', 'background'}:
            return 'colors'
        else:
            # Default based on value pattern
            if HEX_COLOR.search(value) or RGB_RGBA.search(value) or HSL_HSLA.search(value):
                return 'colors'
            elif PIXEL_VALUE.search(value) or REM_VALUE.search(value) or EM_VALUE.search(value):
                return 'spacing'
            else:
                return 'other'

    def extract_colors(self, value, prop, package, file_path, line_num):
        """Extract color values from CSS value."""
        colors = []

        # Hex colors
        for match in HEX_COLOR.finditer(value):
            color = match.group(0)
            colors.append({
                'value': color,
                'type': 'color',
                'package': package,
                'file': file_path,
                'line': line_num,
                'property': prop
            })

        # RGB/RGBA
        for match in RGB_RGBA.finditer(value):
            color = match.group(0)
            colors.append({
                'value': color,
                'type': 'color',
                'package': package,
                'file': file_path,
                'line': line_num,
                'property': prop
            })

        # HSL/HSLA
        for match in HSL_HSLA.finditer(value):
            color = match.group(0)
            colors.append({
                'value': color,
                'type': 'color',
                'package': package,
                'file': file_path,
                'line': line_num,
                'property': prop
            })

        return colors

    def extract_dimensions(self, value, prop, package, file_path, line_num):
        """Extract dimension values (px, rem, em)."""
        dimensions = []

        # Skip if this is a variable reference
        if self.is_variable_reference(value):
            return dimensions

        # Pixels
        for match in PIXEL_VALUE.finditer(value):
            dim_value = match.group(0)
            dimensions.append({
                'value': dim_value,
                'type': self.categorize_value(dim_value, prop),
                'package': package,
                'file': file_path,
                'line': line_num,
                'property': prop
            })

        # Rems
        for match in REM_VALUE.finditer(value):
            dim_value = match.group(0)
            dimensions.append({
                'value': dim_value,
                'type': self.categorize_value(dim_value, prop),
                'package': package,
                'file': file_path,
                'line': line_num,
                'property': prop
            })

        # Ems
        for match in EM_VALUE.finditer(value):
            dim_value = match.group(0)
            dimensions.append({
                'value': dim_value,
                'type': self.categorize_value(dim_value, prop),
                'package': package,
                'file': file_path,
                'line': line_num,
                'property': prop
            })

        return dimensions

    def scan_file(self, file_path, package):
        """Scan a single SCSS file for hardcoded values."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return

        rel_path = str(file_path).replace(str(Path.cwd()) + '/', '')

        in_variable_declaration = False

        for line_num, line in enumerate(lines, 1):
            # Skip comments
            if line.strip().startswith('//'):
                continue

            # Detect SCSS variable declarations
            if line.strip().startswith('$'):
                in_variable_declaration = True
                continue

            # Extract property and value
            prop, value = self.extract_property_value(line)

            if not prop or not value:
                continue

            # Skip variable references
            if self.is_variable_reference(value):
                continue

            # Extract colors
            colors = self.extract_colors(value, prop, package, rel_path, line_num)
            for color in colors:
                if not self.is_variable_reference(color['value']):
                    self.hardcoded_values['colors'].append(color)

            # Extract dimensions
            dimensions = self.extract_dimensions(value, prop, package, rel_path, line_num)
            for dim in dimensions:
                self.hardcoded_values[dim['type']].append(dim)

            # Extract shadows
            if prop in SHADOW_PROPS and not self.is_variable_reference(value):
                self.hardcoded_values['shadows'].append({
                    'value': value,
                    'type': 'shadows',
                    'package': package,
                    'file': rel_path,
                    'line': line_num,
                    'property': prop
                })

    def deduplicate(self):
        """Deduplicate hardcoded values and count occurrences."""
        deduplicated = {}

        for category, values in self.hardcoded_values.items():
            value_map = defaultdict(list)

            for entry in values:
                value_map[entry['value']].append({
                    'package': entry['package'],
                    'file': entry['file'],
                    'line': entry['line'],
                    'property': entry['property']
                })

            deduplicated[category] = [
                {
                    'value': value,
                    'type': category,
                    'occurrences': len(locations),
                    'locations': locations
                }
                for value, locations in value_map.items()
            ]

            # Sort by occurrence count (descending)
            deduplicated[category].sort(key=lambda x: x['occurrences'], reverse=True)

        return deduplicated

    def scan_packages(self):
        """Scan all component packages."""
        base_path = Path.cwd()

        for package_name, package_path in PACKAGES.items():
            full_path = base_path / package_path

            if not full_path.exists():
                print(f"Warning: Package path does not exist: {full_path}")
                continue

            # Find all SCSS and CSS files
            scss_files = list(full_path.rglob('*.scss'))
            css_files = list(full_path.rglob('*.css'))

            all_files = scss_files + css_files
            self.total_files += len(all_files)

            for file_path in all_files:
                self.scan_file(file_path, package_name)

        return self.deduplicate()

    def generate_json(self, deduplicated):
        """Generate components-audit.json."""
        total_unique = sum(len(values) for values in deduplicated.values())
        total_occurrences = sum(
            sum(v['occurrences'] for v in values)
            for values in deduplicated.values()
        )

        output = {
            'metadata': {
                'auditDate': str(date.today()),
                'packagesScanned': list(PACKAGES.keys()),
                'totalFiles': self.total_files,
                'totalUniqueValues': total_unique,
                'totalOccurrences': total_occurrences
            },
            'hardcodedValues': deduplicated
        }

        return output

    def generate_markdown(self, deduplicated):
        """Generate components-audit.md."""
        lines = ['# Component Audit Summary', '']

        # Overall statistics
        total_unique = sum(len(values) for values in deduplicated.values())
        total_occurrences = sum(
            sum(v['occurrences'] for v in values)
            for values in deduplicated.values()
        )

        lines.append(f"**Audit Date:** {date.today()}")
        lines.append(f"**Packages Scanned:** {len(PACKAGES)}")
        lines.append(f"**Total Files:** {self.total_files}")
        lines.append(f"**Total Unique Values:** {total_unique}")
        lines.append(f"**Total Occurrences:** {total_occurrences}")
        lines.append('')

        # Per-category breakdown
        lines.append('## Breakdown by Category')
        lines.append('')

        for category in ['colors', 'spacing', 'typography', 'borderRadius', 'shadows']:
            if category not in deduplicated or not deduplicated[category]:
                continue

            values = deduplicated[category]
            cat_occurrences = sum(v['occurrences'] for v in values)

            lines.append(f"### {category.title()}")
            lines.append('')
            lines.append(f"**Unique Values:** {len(values)}")
            lines.append(f"**Total Occurrences:** {cat_occurrences}")
            lines.append('')

            # Top 10 most used values
            lines.append('**Top Values by Usage:**')
            lines.append('')
            lines.append('| Value | Occurrences | Sample Location |')
            lines.append('|-------|-------------|-----------------|')

            for value_entry in values[:10]:
                value = value_entry['value']
                count = value_entry['occurrences']
                loc = value_entry['locations'][0]
                sample = f"{loc['package']}: {loc['property']}"
                lines.append(f"| `{value}` | {count} | {sample} |")

            lines.append('')

        # Per-package breakdown
        lines.append('## Breakdown by Package')
        lines.append('')

        package_stats = defaultdict(lambda: {'unique': 0, 'occurrences': 0})

        for category, values in deduplicated.items():
            for value_entry in values:
                packages_seen = set()
                for loc in value_entry['locations']:
                    pkg = loc['package']
                    if pkg not in packages_seen:
                        package_stats[pkg]['unique'] += 1
                        packages_seen.add(pkg)
                    package_stats[pkg]['occurrences'] += 1

        lines.append('| Package | Unique Values | Total Occurrences |')
        lines.append('|---------|---------------|-------------------|')

        for package in PACKAGES.keys():
            stats = package_stats[package]
            lines.append(f"| {package} | {stats['unique']} | {stats['occurrences']} |")

        lines.append('')

        return '\n'.join(lines)


def main():
    auditor = ComponentAuditor()

    print("Scanning component packages...")
    deduplicated = auditor.scan_packages()

    print("Generating JSON output...")
    json_output = auditor.generate_json(deduplicated)

    output_dir = Path('tokens/audit')
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / 'components-audit.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_output, f, indent=2)

    print(f"✓ Created {json_path}")

    print("Generating Markdown summary...")
    md_output = auditor.generate_markdown(deduplicated)

    md_path = output_dir / 'components-audit.md'
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_output)

    print(f"✓ Created {md_path}")

    print(f"\nSummary:")
    print(f"  Files scanned: {auditor.total_files}")
    print(f"  Unique values: {json_output['metadata']['totalUniqueValues']}")
    print(f"  Total occurrences: {json_output['metadata']['totalOccurrences']}")


if __name__ == '__main__':
    main()
