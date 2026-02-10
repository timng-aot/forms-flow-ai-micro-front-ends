# Token Coverage Gaps

This document identifies design values found in component code that are not yet available in the shared theme, based on the Phase 1 component audit. Each gap includes specific values, source components, and instructions for adding missing tokens.

## Source Data

All gap data comes from the automated component audit:
- **Audit file:** `tokens/audit/gap-analysis.json`
- **Analysis date:** 2026-02-04
- **Audit scripts:** `tokens/scripts/analyze-components.py`, `tokens/scripts/gap-analysis.py`

## Coverage Summary

| Metric | Count | Percentage |
|--------|-------|------------|
| **Component values analyzed** | 80 | 100% |
| **Exists in theme** | 33 | 41.2% |
| **Close match (within threshold)** | 29 | 36.2% |
| **Missing from theme** | 18 | 22.5% |

**What this means:**
- 41% of component values already have matching tokens in the theme
- 36% are close matches (within 2px or RGB distance <40) — may or may not need separate tokens
- 23% are completely missing and should be added as new tokens

## Component Priority

**Primary migration target:** `forms-flow-admin`
- 51 unique hardcoded values
- 92 total occurrences
- Largest opportunity for token adoption

**Reference example:** `forms-flow-components`
- 0 hardcoded values
- Already uses theme properly
- Good example of proper token usage

## Missing Shadows

Shadows are the most common gap category. Components use hardcoded shadow values that don't exist in the theme.

### Gap: Most Common Shadow Missing

**Value:** `0px 2px 8px rgba(66, 66, 66, 0.07)`
**Occurrences:** 4 times
**Found in:** forms-flow-admin

**Source file paths:**
- `forms-flow-admin/src/...` (exact paths available in gap-analysis.json)

**How to add:**

Open `tokens/core.json` and add to the `ff.shadow` group:

```json
"shadow-card": {
  "$value": {
    "color": "rgba(66, 66, 66, 0.07)",
    "offsetX": "0px",
    "offsetY": "2px",
    "blur": "8px",
    "spread": "0px"
  },
  "$description": "Common card shadow used in forms-flow-admin",
  "$type": "shadow"
}
```

**After adding:** Run `npm run build:tokens` in the `forms-flow-theme` directory, then re-import to Figma.

---

### Gap: Small Drop Shadow

**Value:** `0 1px 3px rgba(0, 0, 0, 0.1)`
**Occurrences:** 1 time
**Found in:** forms-flow-admin

**How to add:**

```json
"shadow-drop-sm": {
  "$value": {
    "color": "rgba(0, 0, 0, 0.1)",
    "offsetX": "0px",
    "offsetY": "1px",
    "blur": "3px",
    "spread": "0px"
  },
  "$description": "Small drop shadow for subtle elevation",
  "$type": "shadow"
}
```

**After adding:** Rebuild tokens and re-import to Figma.

---

### Gap: Navigation Shadow

**Value:** `0px 2px 4px 0px rgba(48, 52, 54, 0.08)`
**Occurrences:** 1 time
**Found in:** forms-flow-nav

**How to add:**

```json
"shadow-nav-alt": {
  "$value": {
    "color": "rgba(48, 52, 54, 0.08)",
    "offsetX": "0px",
    "offsetY": "2px",
    "blur": "4px",
    "spread": "0px"
  },
  "$description": "Alternative navigation shadow",
  "$type": "shadow"
}
```

**After adding:** Rebuild tokens and re-import to Figma.

---

### Gap: "none" Shadow Value

**Value:** `none`
**Occurrences:** 7 times
**Found in:** forms-flow-nav, forms-flow-admin

**How to add:**

```json
"shadow-none": {
  "$value": {
    "color": "rgba(0, 0, 0, 0)",
    "offsetX": "0px",
    "offsetY": "0px",
    "blur": "0px",
    "spread": "0px"
  },
  "$description": "No shadow (explicit removal)",
  "$type": "shadow"
}
```

**After adding:** Rebuild tokens and re-import to Figma.

---

### Gap: Individual Shadow Offset Values

Several components use individual shadow offset values (`0px`, `1px`, `2px`, `3px`, `4px`, `8px`) as CSS properties, not full shadow definitions.

**Values:**
- `0px` — 6 occurrences (forms-flow-nav, forms-flow-admin)
- `2px` — 5 occurrences (forms-flow-nav, forms-flow-admin)
- `8px` — 4 occurrences (forms-flow-admin)
- `1px` — 1 occurrence (forms-flow-admin)
- `3px` — 1 occurrence (forms-flow-admin)
- `4px` — 1 occurrence (forms-flow-nav)

**Note:** These are categorized as "shadows" by the audit script but are actually dimension values used in shadow CSS. Consider whether they need separate tokens or if they should use existing spacing tokens.

**Suggested token (if needed):**

```json
"shadow-offset-sm": {
  "$value": "2px",
  "$description": "Small shadow offset for custom shadow composition",
  "$type": "dimension"
}
```

**After adding:** Rebuild tokens and re-import to Figma.

---

**Source:** `tokens/audit/gap-analysis.json` lines 10-103 (shadow-related gaps)

## Missing Colors

### Gap: Dark Blue Color

**Value:** `#09174A`
**Occurrences:** 2 times
**Found in:** forms-flow-admin

**How to add:**

Open `tokens/core.json` and add to the `ff.color` group:

```json
"indigo-900": {
  "$value": "#09174A",
  "$description": "Very dark blue used in forms-flow-admin",
  "$type": "color"
}
```

**After adding:** Run `npm run build:tokens`, then re-import to Figma.

---

**Source:** `tokens/audit/gap-analysis.json` lines 621-628 (color gap)

## Missing Spacing Values

### Gap: Large Sidebar Width

**Value:** `12.1rem`
**Occurrences:** 2 times
**Found in:** forms-flow-nav

**How to add:**

Open `tokens/core.json` and add to the `ff.spacing` group:

```json
"485": {
  "$value": "12.1rem",
  "$description": "Large component width (navigation sidebar)",
  "$type": "dimension"
}
```

**After adding:** Run `npm run build:tokens`, then re-import to Figma.

---

### Gap: Component Width

**Value:** `4.25rem`
**Occurrences:** 1 time
**Found in:** forms-flow-admin

**How to add:**

```json
"170": {
  "$value": "4.25rem",
  "$description": "Component width for specific UI elements",
  "$type": "dimension"
}
```

**After adding:** Rebuild tokens and re-import to Figma.

---

### Gap: Modal Max Width

**Value:** `5.188rem`
**Occurrences:** 1 time
**Found in:** forms-flow-admin

**How to add:**

```json
"208": {
  "$value": "5.188rem",
  "$description": "Modal or component max width",
  "$type": "dimension"
}
```

**After adding:** Rebuild tokens and re-import to Figma.

---

### Gap: Content Width

**Value:** `4rem`
**Occurrences:** 1 time
**Found in:** forms-flow-admin

**How to add:**

```json
"160": {
  "$value": "4rem",
  "$description": "Standard content block width",
  "$type": "dimension"
}
```

**After adding:** Rebuild tokens and re-import to Figma.

---

**Source:** `tokens/audit/gap-analysis.json` lines 261-417 (spacing gaps with status "missing")

## Missing Typography Values

### Gap: Extra Large Font Size

**Value:** `2rem` (and equivalent `36px`, `3rem`)
**Occurrences:**
- `2rem` — 2 times (forms-flow-submissions, forms-flow-admin)
- `36px` — 2 times (forms-flow-review, forms-flow-submissions)
- `3rem` — 1 time (forms-flow-admin)

**Found in:** forms-flow-submissions, forms-flow-admin, forms-flow-review

**How to add:**

Open `tokens/core.json` and add to the `ff.font-size` group:

```json
"font-size-xxl": {
  "$value": "2rem",
  "$description": "Extra large font size for headings",
  "$type": "dimension"
},
"font-size-xxxl": {
  "$value": "3rem",
  "$description": "Extra extra large font size for hero text",
  "$type": "dimension"
}
```

**After adding:** Run `npm run build:tokens`, then re-import to Figma.

---

**Source:** `tokens/audit/gap-analysis.json` lines 706-746 (typography gaps with status "missing")

## Close Matches

Close matches are values that are similar to existing theme tokens but not exact. They fall within the audit threshold (dimension: ±2px, color: RGB distance <40).

**What to do:**
1. **Review intent:** Determine if the difference is intentional or accidental
2. **If intentional:** Add as a separate token using the instructions above
3. **If accidental:** Migrate component code to use the existing theme token

**Common close matches:**
- **Colors:** `rgba(66, 66, 66, 0.07)` vs `$gray-darker` (distance: 1.0)
- **Spacing:** `0.3rem` vs `$checkmark-width-small` (distance: 0.2px)
- **Border radius:** `8px` vs `$drp-calendar-radius` (distance: 2px)

Close matches account for 29 of the 80 component values analyzed (36.2% of total).

**Source:** `tokens/audit/gap-analysis.json` entries with `"status": "close-match"`

## How to Run the Audit Again

After adding new tokens to `core.json` or `semantic.json`, re-run the audit to verify coverage improvement:

1. **Analyze components:**
   ```bash
   cd tokens/scripts
   python3 analyze-components.py
   ```

   This scans all component packages and extracts hardcoded design values.

2. **Generate gap analysis:**
   ```bash
   python3 gap-analysis.py
   ```

   This compares component values against theme tokens and produces the updated `tokens/audit/gap-analysis.json`.

3. **Review results:** Open `gap-analysis.json` to see updated coverage percentages and remaining gaps.

## Summary by Category

| Category | Missing | Close Match | Exists in Theme | Total |
|----------|---------|-------------|-----------------|-------|
| **Shadows** | 10 | 0 | 0 | 10 |
| **Spacing** | 4 | 17 | 22 | 43 |
| **Colors** | 1 | 6 | 3 | 10 |
| **Typography** | 3 | 4 | 4 | 11 |
| **Border Radius** | 0 | 1 | 2 | 3 |

**Focus areas for improvement:**
1. **Shadows** — Highest gap rate (10 missing, 0% coverage)
2. **Spacing** — Largest category (43 values, 51% coverage)
3. **Colors** — Good coverage (30% exists, 60% close matches)
4. **Typography** — Moderate coverage (36% exists, 36% close matches)

---

**Last updated:** 2026-02-04 (from Phase 1 audit)
**Audit coverage:** 4 packages (forms-flow-admin, forms-flow-nav, forms-flow-review, forms-flow-submissions)
