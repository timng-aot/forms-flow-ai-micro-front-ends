/**
 * Extract inline SVG icons/images from JSX component files into standalone .svg files.
 *
 * Usage:  node extract-svgs.mjs
 * Output: svg-export/icons/  and  svg-export/images/
 */

import { readFileSync, mkdirSync, writeFileSync } from "fs";
import { join } from "path";

const ICONS_FILE =
  "forms-flow-components/src/components/SvgIcons/index.tsx";
const IMAGES_FILE =
  "forms-flow-components/src/components/SvgImages/index.tsx";

// Additional standalone SVG component files
const EXTRA_FILES = [
  {
    file: "forms-flow-admin/src/components/AccessDenied/AccessDenied.js",
    name: "AccessDeniedIcon",
    outDir: "images",
  },
  {
    file: "forms-flow-integration/src/components/PremiumSubscription/integrationImage.tsx",
    name: "IntegrationSVG",
    outDir: "images",
  },
];

// ── JSX attr → HTML attr mapping ────────────────────────────────────────────
const JSX_ATTR_MAP = {
  className: "class",
  strokeLinecap: "stroke-linecap",
  strokeLinejoin: "stroke-linejoin",
  strokeWidth: "stroke-width",
  strokeDasharray: "stroke-dasharray",
  strokeMiterlimit: "stroke-miterlimit",
  fillRule: "fill-rule",
  clipRule: "clip-rule",
  clipPath: "clip-path",
  fillOpacity: "fill-opacity",
  strokeOpacity: "stroke-opacity",
  stopColor: "stop-color",
  stopOpacity: "stop-opacity",
  floodColor: "flood-color",
  floodOpacity: "flood-opacity",
  colorInterpolation: "color-interpolation",
  colorInterpolationFilters: "color-interpolation-filters",
  dominantBaseline: "dominant-baseline",
  shapeRendering: "shape-rendering",
  textAnchor: "text-anchor",
  alignmentBaseline: "alignment-baseline",
  baselineShift: "baseline-shift",
  vectorEffect: "vector-effect",
  pointerEvents: "pointer-events",
  xlinkHref: "xlink:href",
  xmlSpace: "xml:space",
  gradientUnits: "gradientUnits",
  gradientTransform: "gradientTransform",
  patternUnits: "patternUnits",
  patternTransform: "patternTransform",
  preserveAspectRatio: "preserveAspectRatio",
  viewBox: "viewBox",
  enableBackground: "enable-background",
};

// Default colour values used when JSX references variables
const COLOR_DEFAULTS = {
  baseColor: "#1976d2",       // --ff-primary (Material-UI blue is a safe fallback)
  grayColor: "#757575",       // --ff-gray-dark
  whiteColor: "#ffffff",      // --ff-white
  grayDarkestColor: "#424242",// --ff-gray-darkest
  grayMediumColor: "#9e9e9e", // --ff-gray-medium-dark
  secondaryDarkColor: "#455a64", // --secondary-dark
  dangerColor: "#f44336",     // --red-100
  color: "#1976d2",           // generic fallback
  fillColor: "#1976d2",
};

/**
 * Extract the raw SVG from a file that contains a single component.
 * Handles both `=> ( <svg>...</svg> )` and `=> { return ( <svg>...</svg> ) }` patterns,
 * as well as `const Name = () => (` without an `export` keyword.
 */
function extractSvgFromSingleComponentFile(source) {
  const svgStart = source.indexOf("<svg");
  if (svgStart === -1) return null;

  // Find the last closing </svg> tag
  const svgEnd = source.lastIndexOf("</svg>");
  if (svgEnd === -1) return null;

  return source.substring(svgStart, svgEnd + "</svg>".length);
}

function extractComponents(source) {
  const components = [];
  // Match:  export const Name = (...) => ( ... );
  // We find each export const and then balance parens to grab the JSX body.
  const exportRe = /export\s+const\s+(\w+)\s*=\s*\(/g;
  let match;

  while ((match = exportRe.exec(source)) !== null) {
    const name = match[1];
    const startOfParams = match.index + match[0].length;

    // Walk forward to find the `) => (` pattern, then grab balanced JSX
    const arrowIdx = source.indexOf("=> (", startOfParams);
    if (arrowIdx === -1) continue;

    // Also try => (\n and single-line => (<svg
    let jsxStart = arrowIdx + 4; // right after "=> ("

    // Balance parens to find the matching closing `);`
    let depth = 1;
    let i = jsxStart;
    while (i < source.length && depth > 0) {
      const ch = source[i];
      if (ch === "(") depth++;
      else if (ch === ")") depth--;
      i++;
    }

    const jsxBody = source.substring(jsxStart, i - 1).trim();

    // Only keep components that contain an <svg element
    if (!jsxBody.includes("<svg")) continue;

    components.push({ name, jsx: jsxBody });
  }

  return components;
}

function jsxToSvg(jsx) {
  let svg = jsx;

  // Remove {/* ... */} JSX comments
  svg = svg.replace(/\{\/\*[\s\S]*?\*\/\}/g, "");

  // Remove lines that are JS comments (// ...)
  svg = svg.replace(/^\s*\/\/.*$/gm, "");

  // Replace JSX expression attributes with static values:
  //   stroke={color}  →  stroke="#1976d2"
  //   fill={baseColor} → fill="#1976d2"
  //   attr={`...`}     → remove (template literals)
  svg = svg.replace(
    /(\w[\w-]*)=\{([^}]+)\}/g,
    (full, attr, expr) => {
      const trimmed = expr.trim();

      // Skip event handlers, spread, and complex expressions
      if (
        attr === "onClick" ||
        attr === "onChange" ||
        attr === "onMouseEnter" ||
        attr === "onMouseLeave" ||
        trimmed.startsWith("props.") ||
        trimmed.startsWith("...") ||
        trimmed.includes("?") ||
        trimmed.includes("&&")
      ) {
        return ""; // remove it
      }

      // String literal: {"#fff"} or {'#fff'}
      const strMatch = trimmed.match(/^["'](.+)["']$/);
      if (strMatch) return `${attr}="${strMatch[1]}"`;

      // Known colour variable
      if (COLOR_DEFAULTS[trimmed]) {
        const htmlAttr = JSX_ATTR_MAP[attr] || attr;
        return `${htmlAttr}="${COLOR_DEFAULTS[trimmed]}"`;
      }

      // Numeric
      if (/^\d+$/.test(trimmed)) {
        return `${attr}="${trimmed}"`;
      }

      // Fallback: use a neutral color for color-like attrs
      const lowerAttr = attr.toLowerCase();
      if (
        lowerAttr === "fill" ||
        lowerAttr === "stroke" ||
        lowerAttr === "color" ||
        lowerAttr === "stop-color"
      ) {
        return `${attr}="${COLOR_DEFAULTS.baseColor}"`;
      }

      // Drop unknown expressions
      return "";
    }
  );

  // Remove {...props} and {...rest} spreads
  svg = svg.replace(/\{\.\.\.[\w]+\}/g, "");

  // Convert remaining JSX attribute names to HTML equivalents
  for (const [jsxAttr, htmlAttr] of Object.entries(JSX_ATTR_MAP)) {
    // Only replace attribute names (preceded by space or newline), not element names
    const re = new RegExp(`(\\s)${jsxAttr}=`, "g");
    svg = svg.replace(re, `$1${htmlAttr}=`);
  }

  // Remove className/class attributes (not needed in standalone SVG)
  svg = svg.replace(/\s+class="[^"]*"/g, "");

  // Self-close tags that have no children: <tag ... ></tag> → <tag ... />
  // (but not <svg>)
  svg = svg.replace(/<(\w+)([^>]*)><\/\1>/g, (m, tag, attrs) => {
    if (tag === "svg") return m;
    return `<${tag}${attrs}/>`;
  });

  // Ensure the SVG has xmlns
  if (!svg.includes('xmlns="http://www.w3.org/2000/svg"')) {
    svg = svg.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"');
  }

  // Clean up extra whitespace / blank lines
  svg = svg
    .split("\n")
    .map((l) => l.trimEnd())
    .filter((l) => l.length > 0)
    .join("\n");

  return svg;
}

function kebabCase(name) {
  return name
    .replace(/([a-z])([A-Z])/g, "$1-$2")
    .replace(/([A-Z]+)([A-Z][a-z])/g, "$1-$2")
    .toLowerCase();
}

// ── Main ────────────────────────────────────────────────────────────────────
const iconsDir = join("svg-export", "icons");
const imagesDir = join("svg-export", "images");
mkdirSync(iconsDir, { recursive: true });
mkdirSync(imagesDir, { recursive: true });

let totalCount = 0;

for (const [file, outDir, label] of [
  [ICONS_FILE, iconsDir, "icons"],
  [IMAGES_FILE, imagesDir, "images"],
]) {
  console.log(`\nProcessing ${label}: ${file}`);
  const source = readFileSync(file, "utf-8");
  const components = extractComponents(source);
  console.log(`  Found ${components.length} components`);

  for (const { name, jsx } of components) {
    const svg = jsxToSvg(jsx);
    const filename = `${kebabCase(name)}.svg`;
    const outPath = join(outDir, filename);
    writeFileSync(outPath, svg + "\n");
    totalCount++;
  }
}

// ── Extra standalone component files ────────────────────────────────────────
for (const { file, name, outDir } of EXTRA_FILES) {
  const dir = outDir === "icons" ? iconsDir : imagesDir;
  console.log(`\nProcessing extra: ${file}`);
  const source = readFileSync(file, "utf-8");
  const rawSvg = extractSvgFromSingleComponentFile(source);
  if (!rawSvg) {
    console.log(`  WARNING: no <svg> found in ${file}, skipping`);
    continue;
  }
  const svg = jsxToSvg(rawSvg);
  const filename = `${kebabCase(name)}.svg`;
  const outPath = join(dir, filename);
  writeFileSync(outPath, svg + "\n");
  totalCount++;
  console.log(`  Exported ${name} → ${outPath}`);
}

console.log(`\nDone! Exported ${totalCount} SVGs to svg-export/`);
console.log("Drag the svg-export folder contents into Figma to import them.");
