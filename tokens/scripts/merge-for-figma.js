/**
 * Merge core.json and semantic.json into a single file for Token Studio import.
 *
 * Token Studio's free tier cannot resolve cross-file references. This script
 * combines both files so that semantic references like {ff.color.indigo-100}
 * resolve within a single token set.
 *
 * Usage: node tokens/scripts/merge-for-figma.js
 * Output: tokens/dist/tokens-figma.json
 */

import { readFileSync, writeFileSync, mkdirSync } from 'fs';
import { dirname, resolve } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const tokensDir = resolve(__dirname, '..');
const distDir = resolve(tokensDir, 'dist');

const core = JSON.parse(readFileSync(resolve(tokensDir, 'core.json'), 'utf8'));
const semantic = JSON.parse(readFileSync(resolve(tokensDir, 'semantic.json'), 'utf8'));

// Merge: core tokens (under "ff" group) + semantic tokens (at root level).
// Semantic tokens reference core via {ff.color.xxx} — both must be in the
// same file for Token Studio free tier to resolve them.
const merged = { ...core, ...semantic };

mkdirSync(distDir, { recursive: true });
writeFileSync(
  resolve(distDir, 'tokens-figma.json'),
  JSON.stringify(merged, null, 2) + '\n'
);

console.log('Merged tokens written to tokens/dist/tokens-figma.json');
