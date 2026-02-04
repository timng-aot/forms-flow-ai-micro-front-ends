#!/usr/bin/env python3
"""
Gap analysis: Compare component hardcoded values against shared theme audit.
Produces gap-analysis.json.
"""

import json
import re
from pathlib import Path
from datetime import date
from collections import defaultdict


class GapAnalyzer:
    def __init__(self, theme_path, components_path):
        self.theme_path = theme_path
        self.components_path = components_path
        self.theme_data = None
        self.components_data = None

    def load_data(self):
        """Load theme and component audit data."""
        with open(self.theme_path, 'r', encoding='utf-8') as f:
            self.theme_data = json.load(f)

        with open(self.components_path, 'r', encoding='utf-8') as f:
            self.components_data = json.load(f)

    def normalize_color(self, color):
        """Normalize color to lowercase 6-digit hex for comparison."""
        color = color.strip().lower()

        # Handle 3-digit hex
        if re.match(r'^#[0-9a-f]{3}$', color):
            r, g, b = color[1], color[2], color[3]
            return f'#{r}{r}{g}{g}{b}{b}'

        # Handle 6-digit hex
        if re.match(r'^#[0-9a-f]{6}$', color):
            return color

        # Handle 8-digit hex (RGBA) - ignore alpha for comparison
        if re.match(r'^#[0-9a-f]{8}$', color):
            return color[:7]

        # Handle rgba(r, g, b, a) - convert to hex
        rgba_match = re.match(r'rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*[\d.]+)?\)', color)
        if rgba_match:
            r, g, b = int(rgba_match.group(1)), int(rgba_match.group(2)), int(rgba_match.group(3))
            return f'#{r:02x}{g:02x}{b:02x}'

        return color

    def rgb_distance(self, color1, color2):
        """Calculate Euclidean distance between two RGB colors."""
        try:
            # Convert hex to RGB
            c1 = self.normalize_color(color1)
            c2 = self.normalize_color(color2)

            if not (c1.startswith('#') and len(c1) == 7):
                return 999
            if not (c2.startswith('#') and len(c2) == 7):
                return 999

            r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
            r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)

            return ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5
        except:
            return 999

    def normalize_dimension(self, value):
        """Normalize dimension to pixels for comparison."""
        value = value.strip().lower()

        # Handle px
        px_match = re.match(r'^([\d.]+)px$', value)
        if px_match:
            return float(px_match.group(1))

        # Handle rem (assuming 1rem = 16px)
        rem_match = re.match(r'^([\d.]+)rem$', value)
        if rem_match:
            return float(rem_match.group(1)) * 16

        # Handle em (assuming 1em = 16px)
        em_match = re.match(r'^([\d.]+)em$', value)
        if em_match:
            return float(em_match.group(1)) * 16

        return None

    def compare_colors(self, comp_value, theme_values):
        """Compare component color against theme colors."""
        normalized_comp = self.normalize_color(comp_value)

        # Check exact match
        for theme_var, theme_info in theme_values.items():
            theme_val = theme_info.get('value', '')
            computed_val = theme_info.get('computedValue', '')

            if self.normalize_color(theme_val) == normalized_comp:
                return 'exists-in-theme', theme_var, None

            if computed_val and self.normalize_color(computed_val) == normalized_comp:
                return 'exists-in-theme', theme_var, None

        # Check close match (RGB distance < 40)
        closest_var = None
        closest_distance = 999

        for theme_var, theme_info in theme_values.items():
            theme_val = theme_info.get('value', '')
            computed_val = theme_info.get('computedValue', '')

            dist1 = self.rgb_distance(comp_value, theme_val)
            dist2 = self.rgb_distance(comp_value, computed_val) if computed_val else 999

            min_dist = min(dist1, dist2)

            if min_dist < closest_distance:
                closest_distance = min_dist
                closest_var = theme_var

        if closest_distance < 40:
            return 'close-match', closest_var, closest_distance

        return 'missing', None, None

    def compare_dimensions(self, comp_value, theme_values):
        """Compare component dimension against theme dimensions."""
        normalized_comp = self.normalize_dimension(comp_value)

        if normalized_comp is None:
            return 'missing', None, None

        # Check exact match
        for theme_var, theme_info in theme_values.items():
            theme_val = theme_info.get('value', '')
            computed_val = theme_info.get('computedValue', '')

            if self.normalize_dimension(theme_val) == normalized_comp:
                return 'exists-in-theme', theme_var, None

            if computed_val and self.normalize_dimension(computed_val) == normalized_comp:
                return 'exists-in-theme', theme_var, None

        # Check close match (within +/-2px)
        for theme_var, theme_info in theme_values.items():
            theme_val = theme_info.get('value', '')
            computed_val = theme_info.get('computedValue', '')

            theme_norm = self.normalize_dimension(theme_val)
            if theme_norm and abs(theme_norm - normalized_comp) <= 2:
                return 'close-match', theme_var, abs(theme_norm - normalized_comp)

            if computed_val:
                computed_norm = self.normalize_dimension(computed_val)
                if computed_norm and abs(computed_norm - normalized_comp) <= 2:
                    return 'close-match', theme_var, abs(computed_norm - normalized_comp)

        return 'missing', None, None

    def suggest_token_name(self, value, value_type):
        """Suggest a token name following ff- convention."""
        value_type = value_type.lower()

        if value_type == 'colors':
            # Extract color characteristics
            normalized = self.normalize_color(value)
            if normalized.startswith('#'):
                # Simple naming based on brightness
                try:
                    r, g, b = int(normalized[1:3], 16), int(normalized[3:5], 16), int(normalized[5:7], 16)
                    brightness = (r + g + b) / 3

                    if brightness < 64:
                        shade = 'darkest'
                    elif brightness < 128:
                        shade = 'dark'
                    elif brightness < 192:
                        shade = 'medium'
                    else:
                        shade = 'light'

                    # Detect color hue
                    if r > g and r > b:
                        hue = 'red'
                    elif g > r and g > b:
                        hue = 'green'
                    elif b > r and b > g:
                        hue = 'blue'
                    elif r == g == b:
                        hue = 'gray'
                    else:
                        hue = 'neutral'

                    if hue == 'gray':
                        return f'ff-gray-{shade}'
                    else:
                        return f'ff-{hue}-{shade}'
                except:
                    return 'ff-color-custom'
            else:
                return 'ff-color-custom'

        elif value_type == 'spacing':
            # Extract numeric value
            normalized = self.normalize_dimension(value)
            if normalized:
                px_val = int(normalized)
                if px_val <= 4:
                    return 'ff-spacer-025'
                elif px_val <= 8:
                    return 'ff-spacer-050'
                elif px_val <= 12:
                    return 'ff-spacer-075'
                elif px_val <= 16:
                    return 'ff-spacer-100'
                elif px_val <= 24:
                    return 'ff-spacer-150'
                elif px_val <= 32:
                    return 'ff-spacer-200'
                else:
                    return f'ff-spacer-{px_val // 4}'
            return 'ff-spacer-custom'

        elif value_type == 'typography':
            normalized = self.normalize_dimension(value)
            if normalized:
                px_val = int(normalized)
                if px_val <= 12:
                    return 'ff-font-size-xs'
                elif px_val <= 14:
                    return 'ff-font-size-sm'
                elif px_val <= 16:
                    return 'ff-font-size-md'
                elif px_val <= 18:
                    return 'ff-font-size-lg'
                elif px_val <= 24:
                    return 'ff-font-size-xl'
                else:
                    return 'ff-font-size-xxl'
            return 'ff-font-size-custom'

        elif value_type == 'borderradius':
            normalized = self.normalize_dimension(value)
            if normalized:
                px_val = int(normalized)
                if px_val <= 4:
                    return 'ff-radius-sm'
                elif px_val <= 8:
                    return 'ff-radius-md'
                else:
                    return 'ff-radius-lg'
            return 'ff-radius-custom'

        elif value_type == 'shadows':
            if value.lower() == 'none':
                return 'ff-shadow-none'
            elif '0px 1px' in value or '0 1px' in value:
                return 'ff-shadow-sm'
            elif '0px 2px' in value or '0 2px' in value:
                return 'ff-shadow-md'
            else:
                return 'ff-shadow-lg'

        return f'ff-{value_type}-custom'

    def get_theme_values_by_type(self, value_type):
        """Get theme values filtered by type."""
        theme_values = {}

        scss_vars = self.theme_data.get('scssVariables', {})
        css_props = self.theme_data.get('cssCustomProperties', {})

        category_map = {
            'colors': 'color',
            'spacing': 'spacing',
            'typography': 'typography',
            'borderRadius': 'borderRadius',
            'shadows': 'shadow'
        }

        target_category = category_map.get(value_type)

        for var_name, var_info in scss_vars.items():
            if var_info.get('category') == target_category or var_info.get('type') == target_category:
                theme_values[var_name] = var_info

        for prop_name, prop_info in css_props.items():
            if prop_info.get('category') == target_category or prop_info.get('type') == target_category:
                theme_values[prop_name] = prop_info

        return theme_values

    def analyze(self):
        """Perform gap analysis."""
        gaps = []

        for category, values in self.components_data['hardcodedValues'].items():
            theme_values = self.get_theme_values_by_type(category)

            for value_entry in values:
                value = value_entry['value']
                occurrences = value_entry['occurrences']
                locations = value_entry['locations']

                # Get unique source packages
                source_packages = list(set(loc['package'] for loc in locations))

                # Perform comparison
                if category == 'colors':
                    status, theme_var, distance = self.compare_colors(value, theme_values)
                elif category in ['spacing', 'typography', 'borderRadius']:
                    status, theme_var, distance = self.compare_dimensions(value, theme_values)
                else:
                    # For shadows and other types, do simple string matching
                    status = 'missing'
                    theme_var = None
                    distance = None

                    for tv, ti in theme_values.items():
                        if ti.get('value', '').lower() == value.lower():
                            status = 'exists-in-theme'
                            theme_var = tv
                            break

                gap_entry = {
                    'value': value,
                    'type': category,
                    'status': status,
                    'occurrences': occurrences,
                    'sourcePackages': source_packages
                }

                if status == 'exists-in-theme':
                    gap_entry['themeVariable'] = theme_var
                elif status == 'close-match':
                    gap_entry['closestThemeValue'] = theme_var
                    if distance is not None:
                        gap_entry['distance'] = distance
                elif status == 'missing':
                    gap_entry['suggestedToken'] = self.suggest_token_name(value, category)

                gaps.append(gap_entry)

        return gaps

    def generate_output(self, gaps):
        """Generate gap-analysis.json."""
        total_values = len(gaps)
        exists_count = sum(1 for g in gaps if g['status'] == 'exists-in-theme')
        close_count = sum(1 for g in gaps if g['status'] == 'close-match')
        missing_count = sum(1 for g in gaps if g['status'] == 'missing')

        output = {
            'metadata': {
                'analysisDate': str(date.today()),
                'totalComponentValues': total_values,
                'existsInTheme': exists_count,
                'closeMatch': close_count,
                'missingFromTheme': missing_count,
                'coveragePercentage': round((exists_count / total_values * 100) if total_values > 0 else 0, 1)
            },
            'gaps': gaps
        }

        return output


def main():
    theme_path = Path('tokens/audit/theme-audit.json')
    components_path = Path('tokens/audit/components-audit.json')

    if not theme_path.exists():
        print(f"Error: {theme_path} not found")
        return

    if not components_path.exists():
        print(f"Error: {components_path} not found")
        return

    analyzer = GapAnalyzer(theme_path, components_path)

    print("Loading audit data...")
    analyzer.load_data()

    print("Analyzing gaps...")
    gaps = analyzer.analyze()

    print("Generating output...")
    output = analyzer.generate_output(gaps)

    output_path = Path('tokens/audit/gap-analysis.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)

    print(f"✓ Created {output_path}")

    print(f"\nSummary:")
    print(f"  Total component values: {output['metadata']['totalComponentValues']}")
    print(f"  Exists in theme: {output['metadata']['existsInTheme']}")
    print(f"  Close match: {output['metadata']['closeMatch']}")
    print(f"  Missing from theme: {output['metadata']['missingFromTheme']}")
    print(f"  Coverage: {output['metadata']['coveragePercentage']}%")


if __name__ == '__main__':
    main()
