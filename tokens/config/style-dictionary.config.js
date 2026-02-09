import StyleDictionary from 'style-dictionary';
import { register, expandTypesMap } from '@tokens-studio/sd-transforms';
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';
import fs from 'fs';

// Register Token Studio transforms
register(StyleDictionary);

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

/**
 * Custom transform: name/css/ff-prefix
 * Converts token paths to CSS variable names with --ff- prefix
 * Example: ['ff', 'color', 'indigo-100'] -> 'ff-color-indigo-100'
 * (css/variables format will prepend -- automatically)
 */
StyleDictionary.registerTransform({
  name: 'name/css/ff-prefix',
  type: 'name',
  transform: (token) => {
    // Join path with hyphens
    // Style Dictionary's css/variables format will add -- prefix
    return token.path.join('-');
  }
});

/**
 * DTCG validation preprocessor
 * Validates tokens before transformation:
 * - All leaf tokens must have $type (directly or inherited)
 * - Token names cannot contain forbidden characters: {, }, $
 * - $type values must match DTCG spec
 */
StyleDictionary.registerPreprocessor({
  name: 'validate-dtcg',
  preprocessor: (dictionary) => {
    const validTypes = [
      'color',
      'dimension',
      'fontFamily',
      'fontWeight',
      'duration',
      'cubicBezier',
      'number',
      'shadow',
      'strokeStyle',
      'border',
      'transition',
      'gradient',
      'typography'
    ];

    const forbiddenChars = ['{', '}', '$'];

    function validateToken(token, path = [], inheritedType = null) {
      const currentPath = [...path, token.name || 'root'];

      // If this is a leaf token (has $value)
      if (token.$value !== undefined) {
        // Check for $type (directly or inherited)
        const tokenType = token.$type || inheritedType;
        if (!tokenType) {
          throw new Error(
            `DTCG Validation Error: Token at path "${currentPath.join('.')}" has $value but no $type (directly or inherited from parent)`
          );
        }

        // Validate $type value
        if (!validTypes.includes(tokenType)) {
          throw new Error(
            `DTCG Validation Error: Token at path "${currentPath.join('.')}" has invalid $type="${tokenType}". Valid types: ${validTypes.join(', ')}`
          );
        }

        // Check token name for forbidden characters
        if (token.name) {
          for (const char of forbiddenChars) {
            if (token.name.includes(char)) {
              throw new Error(
                `DTCG Validation Error: Token name "${token.name}" at path "${currentPath.join('.')}" contains forbidden character "${char}"`
              );
            }
          }
        }
      } else {
        // This is a group - recurse into children
        const groupType = token.$type || inheritedType;

        for (const [key, value] of Object.entries(token)) {
          // Skip DTCG metadata properties
          if (key.startsWith('$')) continue;

          // Validate child token names
          for (const char of forbiddenChars) {
            if (key.includes(char)) {
              throw new Error(
                `DTCG Validation Error: Token name "${key}" at path "${currentPath.join('.')}" contains forbidden character "${char}"`
              );
            }
          }

          // Recurse with inherited type
          if (typeof value === 'object' && value !== null) {
            validateToken({ ...value, name: key }, currentPath, groupType);
          }
        }
      }
    }

    // Validate all tokens in dictionary
    try {
      validateToken(dictionary);
    } catch (error) {
      console.error('\n❌ DTCG Validation Failed:\n');
      throw error;
    }

    console.log('✓ DTCG validation passed');
    return dictionary;
  }
});

/**
 * Build function for generating CSS custom properties from token JSON
 * @param {string} sourcePath - Path to token JSON file (relative to config)
 * @param {string} destinationFilename - Output CSS filename
 */
async function buildTokens(sourcePath, destinationFilename) {
  // Resolve absolute paths
  const absoluteSourcePath = resolve(__dirname, sourcePath);
  const buildPath = resolve(__dirname, '../dist/');

  // Verify source file exists
  if (!fs.existsSync(absoluteSourcePath)) {
    throw new Error(`Source token file not found: ${absoluteSourcePath}`);
  }

  console.log(`\n🔨 Building tokens from ${sourcePath}...`);
  console.log(`   Output: ${buildPath}${destinationFilename}`);

  // For semantic tokens, we need to include core tokens as well for reference resolution
  const isSemanticBuild = sourcePath.includes('semantic');
  const sources = isSemanticBuild
    ? [
        resolve(__dirname, '../core.json'),
        absoluteSourcePath
      ]
    : [absoluteSourcePath];

  // Create Style Dictionary configuration
  const sd = new StyleDictionary({
    source: sources,
    preprocessors: ['tokens-studio', 'validate-dtcg'],
    expand: {
      typesMap: expandTypesMap
    },
    platforms: {
      css: {
        transformGroup: 'tokens-studio',
        transforms: [
          // Token Studio transforms for DTCG format
          'ts/descriptionToComment',
          'ts/size/px',
          'ts/opacity',
          'ts/size/lineheight',
          'ts/type/fontWeight',
          'ts/resolveMath',
          'ts/size/css/letterspacing',
          'ts/typography/css/shorthand',
          'ts/border/css/shorthand',
          'ts/shadow/css/shorthand',
          'ts/color/css/hexrgba',
          'ts/color/modifiers',
          // Custom name transform for --ff- prefix
          'name/css/ff-prefix'
        ],
        buildPath: buildPath,
        files: [
          {
            destination: destinationFilename,
            format: 'css/variables',
            options: {
              outputReferences: true,
              selector: ':root'
            },
            // For semantic builds, only output semantic tokens (not core)
            filter: isSemanticBuild
              ? (token) => {
                  // Only include tokens from semantic.json source
                  // Core tokens will be referenced via var() but not redefined
                  return token.filePath && token.filePath.includes('semantic.json');
                }
              : undefined
          }
        ]
      }
    }
  });

  // Build and clean
  await sd.buildAllPlatforms();
  console.log(`✓ Build complete: ${destinationFilename}\n`);
}

// CLI entry point
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const [,, sourcePath, destinationFilename] = process.argv;

  if (!sourcePath || !destinationFilename) {
    console.error('Usage: node style-dictionary.config.js <source-path> <destination-filename>');
    console.error('Example: node style-dictionary.config.js ../core.json core-tokens.css');
    process.exit(1);
  }

  buildTokens(sourcePath, destinationFilename).catch((error) => {
    console.error('Build failed:', error);
    process.exit(1);
  });
}

export { buildTokens };
