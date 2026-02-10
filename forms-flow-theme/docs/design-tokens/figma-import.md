# Importing Design Tokens to Figma

This guide walks you through importing design tokens into Figma using the Token Studio plugin. No coding experience required.

## Who This Guide Is For

**Audience:** Designers using Figma
**Time Required:** 10 minutes
**Difficulty:** Beginner-friendly

## What You'll Need

Before you start, make sure you have:

- [ ] **Figma Desktop app** installed ([download here](https://www.figma.com/downloads/))
- [ ] **Token Studio for Figma** plugin installed ([get it from Figma Community](https://www.figma.com/community/plugin/843461159747178978/Tokens-Studio-for-Figma))
- [ ] Access to the token files in your repository:
  - `tokens/core.json` — Base design values (colors, spacing, fonts, etc.)
  - `tokens/semantic.json` — Design decisions (primary color, button styles, etc.)

## Step 1: Open Token Studio Plugin

1. Open your Figma file (or create a new one to test)
2. Go to the top menu and click **Plugins** → **Token Studio for Figma**
   - Or use the keyboard shortcut (Mac: `Cmd+/`, Windows: `Ctrl+/`) and search for "Token Studio"
3. The plugin panel will open on the right side of your screen
4. If this is your first time using the plugin, click **"New empty file"** to start fresh

**What you'll see:** A sidebar panel with tabs at the top (Tokens, Themes, Styles & Variables) and an empty token list below.

## Step 2: Import Core Tokens

Core tokens are the foundation — the actual colors, spacing values, font sizes, and other design primitives extracted from the shared theme.

1. In the Token Studio sidebar, look for the **gear icon** (Settings) or **"Load"** button in the bottom toolbar
2. Click it to open the settings menu
3. Select **"JSON"** as your sync method (not GitHub, not URL — just JSON)
4. Click the **"Import JSON"** button
5. Navigate to your repository folder and select **`tokens/core.json`**
6. Click **"Open"** to import

**What you'll see:** The token list fills with categories under an "ff" group:
- **color** — All color values from the theme (yellow-100, indigo-100, white, black, etc.)
- **spacing** — Spacing scale (025, 050, 100, 150, 200, etc.)
- **font-family** — Font family values
- **font-size** — Font size values
- **font-weight** — Font weight values (300, 400, 500, 600, 700)
- **line-height** — Line height values
- **radius** — Border radius values
- **shadow** — Shadow definitions (shown as objects with color, offsetX, offsetY, blur, spread)
- **duration** — Animation timing values

You should see over 160 tokens organized by category.

## Step 3: Import Semantic Tokens

Semantic tokens are design decisions that reference the core tokens — things like "primary color" or "button shadow" that point to specific core values.

**Important:** Import semantic tokens AFTER core tokens so the references can resolve properly.

1. Repeat the import process from Step 2
2. This time, select **`tokens/semantic.json`**
3. Click **"Open"** to import

**What you'll see:** New semantic token categories appear:
- **color** — primary, success, danger, warning, info, light, dark, action, background, text
- **spacing** — xs, sm, md, lg, xl
- **font-family** — body, heading
- **font-weight** — normal, medium, semibold, bold
- **radius** — sm, md, lg, modal
- **shadow** — sm, md, lg, xl, 2xl, 3xl, nav

These tokens show reference syntax like `{ff.color.indigo-100}` — that means they point to values from the core tokens. The plugin will automatically resolve these to the actual values.

## Step 4: Sync to Figma Variables

Now we convert the tokens into Figma Variables so they can be used in your designs.

1. In the Token Studio sidebar, click the **"Styles & Variables"** tab at the top
2. Scroll down to the **"Export to Figma"** section
3. Check the boxes next to the token sets you want to sync:
   - ✅ **core** (or whatever name was assigned to core.json)
   - ✅ **semantic** (or whatever name was assigned to semantic.json)
4. Click **"Sync Variables"** or **"Export to Figma"** button
5. Wait a few seconds while the plugin creates Figma Variables

**What happens:** Token Studio creates Figma Variable Collections for each category (color, spacing, radius, shadow, etc.) with all the token values.

## Step 5: Verify Import

Let's make sure everything worked correctly.

1. Open the **Variables panel** in Figma:
   - Click the **four-dot icon** in the right sidebar
   - Or go to the top menu: **View** → **Variables**
2. You should see Variable Collections with names like:
   - `ff/color`
   - `ff/spacing`
   - `ff/radius`
   - `ff/shadow`
   - `color` (semantic)
   - `spacing` (semantic)
   - `radius` (semantic)
   - `shadow` (semantic)
3. **Spot-check some values:**
   - Click on `ff/color` collection
   - Find `indigo-100` — it should show **#3248F4**
   - Find `white` — it should show **#FFFFFF**
4. **Check reference resolution:**
   - Click on the `color` (semantic) collection
   - Find `primary` — it should show the resolved color (#3248F4), not the reference text
   - If you see `{ff.color.indigo-100}` as text, the references didn't resolve — try re-importing core.json first

**Success:** If you see variables with correct values and semantic tokens showing colors (not reference text), you're done!

## Troubleshooting

### "Invalid token name" error

**Problem:** Token Studio can't import because token names contain forbidden characters.

**Solution:** Token names in the JSON files should not contain `{`, `}`, or `$` characters. Our tokens use kebab-case (hyphens) which is supported. If you see this error, check that you haven't manually edited the token files.

### References not resolving (showing `{ff.color.indigo-100}` as text)

**Problem:** Semantic tokens show reference syntax instead of resolved values.

**Solution:**
1. Make sure you imported `core.json` BEFORE `semantic.json`
2. Delete the semantic token set in Token Studio and re-import it
3. The references can only resolve if the core tokens they point to already exist

### Duplicate variables error

**Problem:** Figma says variables already exist with these names.

**Solution:**
1. In Token Studio, delete the existing token sets (click trash icon next to each set name)
2. In Figma's Variables panel, delete the old Variable Collections
3. Re-import both JSON files fresh

### Plugin not showing or won't open

**Problem:** Token Studio doesn't appear in the Plugins menu.

**Solution:**
1. Make sure you installed it from Figma Community: [Token Studio for Figma](https://www.figma.com/community/plugin/843461159747178978/Tokens-Studio-for-Figma)
2. Try restarting Figma Desktop
3. Check that you're using Figma Desktop, not the browser version (the plugin works best in the desktop app)

## Next Steps

Now that your tokens are in Figma as Variables, you can:

1. **Apply them to designs:** Use variables instead of hardcoded colors/spacing
2. **Create modes:** Set up light/dark themes using Variable Modes
3. **Export changes:** If you modify token values in Figma, you can export them back to JSON and update the theme
4. **Share with your team:** Variables sync across Figma files when published to a library

## References

- **Token Studio documentation:** [docs.tokens.studio](https://docs.tokens.studio/)
- **Figma Variables help:** [Figma Variables Guide](https://help.figma.com/hc/en-us/articles/15339657135383-Guide-to-variables-in-Figma)
- **W3C Design Token Format:** [Design Tokens Community Group](https://tr.designtokens.org/format/)

---

**Note:** Screenshots can be added to an `assets/` directory to enhance this guide with visual aids for each step.
