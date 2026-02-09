// Pre-computation script for resolving blend-with-white-to-hex() expressions
// Reads tokens/core.json, resolves color blending expressions to hex values, writes back
// Standalone, rerunnable, idempotent - no external dependencies

const fs = require('fs');
const path = require('path');

/**
 * Blends a hex color with white background at given opacity.
 * Formula: newRGB = (baseRGB * opacity) + (whiteRGB * (1 - opacity))
 * Matches SCSS function blend-with-white-to-hex() from forms-flow-theme/scss/v8-scss/_theme.scss
 *
 * @param {string} hexColor - Hex color string (e.g., "#3248F4")
 * @param {number} opacity - Opacity value 0.0-1.0
 * @returns {string} Blended hex color (lowercase)
 */
function blendWithWhiteToHex(hexColor, opacity) {
  // Parse hex color (supports #RRGGBB format)
  const hex = hexColor.replace('#', '');
  const r = parseInt(hex.slice(0, 2), 16);
  const g = parseInt(hex.slice(2, 4), 16);
  const b = parseInt(hex.slice(4, 6), 16);

  // Blend with white (255, 255, 255)
  const newR = Math.round((r * opacity) + (255 * (1 - opacity)));
  const newG = Math.round((g * opacity) + (255 * (1 - opacity)));
  const newB = Math.round((b * opacity) + (255 * (1 - opacity)));

  // Convert back to hex with zero-padding (lowercase for consistency)
  const toHex = (n) => n.toString(16).padStart(2, '0');
  return `#${toHex(newR)}${toHex(newG)}${toHex(newB)}`;
}

/**
 * Recursively resolves blend-with-white-to-hex() expressions in token object.
 * Only modifies $value properties that match the expression pattern.
 * Idempotent: running on already-resolved hex values produces no changes.
 *
 * @param {any} obj - Token object to process
 * @returns {any} Processed token object with resolved expressions
 */
function resolveBlendExpressions(obj) {
  if (Array.isArray(obj)) {
    return obj.map(resolveBlendExpressions);
  }

  if (obj && typeof obj === 'object') {
    const result = {};

    for (const [key, value] of Object.entries(obj)) {
      if (key === '$value' && typeof value === 'string') {
        // Match: blend-with-white-to-hex(#XXXXXX, N.N)
        const match = value.match(/blend-with-white-to-hex\(#([0-9A-Fa-f]{6}),\s*([\d.]+)\)/);

        if (match) {
          const hexColor = `#${match[1]}`;
          const opacity = parseFloat(match[2]);
          result[key] = blendWithWhiteToHex(hexColor, opacity);
        } else {
          result[key] = value; // Already resolved or not a blend expression
        }
      } else {
        result[key] = resolveBlendExpressions(value);
      }
    }

    return result;
  }

  return obj;
}

// Main execution
const tokensPath = path.resolve(__dirname, '../../core.json');
console.log(`Reading tokens from: ${tokensPath}`);

try {
  const tokensContent = fs.readFileSync(tokensPath, 'utf8');
  const tokens = JSON.parse(tokensContent);

  // Count blend expressions before resolution
  const beforeCount = (tokensContent.match(/blend-with-white-to-hex/g) || []).length;

  const resolved = resolveBlendExpressions(tokens);

  // Write back with 2-space indentation + trailing newline
  fs.writeFileSync(tokensPath, JSON.stringify(resolved, null, 2) + '\n');

  // Verify expressions were resolved
  const afterContent = fs.readFileSync(tokensPath, 'utf8');
  const afterCount = (afterContent.match(/blend-with-white-to-hex/g) || []).length;

  console.log(`✓ Resolved ${beforeCount - afterCount} blend-with-white-to-hex() expressions`);
  console.log(`✓ Remaining blend expressions: ${afterCount}`);
  console.log('✓ core.json updated successfully');
} catch (error) {
  console.error('Error processing tokens:', error.message);
  process.exit(1);
}
