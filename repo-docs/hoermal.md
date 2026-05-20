# `hoermal` audio/admonition format

## Purpose

This document records the current `hoermal` container as implemented in the Lehrbuch project.

Scope:

- Markdown authoring pattern
- rendered HTML structure
- project CSS and inherited theme mechanics that affect the component
- design tokens and variables used by the component
- audio player markup and JavaScript behavior
- currently used variants versus CSS-supported-but-not-currently-used variants

This is a reference document only. No structural or style changes are proposed here.

## Source locations

Primary source files evaluated:

- `zensical.toml`
  - CSS/JS load order via `extra_css` and `extra_javascript`
  - confirms `audio_src_fixup.js` is loaded site-wide
- `docs/assets/styles/00_tokens.css`
  - admonition hue tokens, tint ratios, global spacing/shadow/radius tokens
- `docs/assets/styles/10_typography.css`
  - `--book-font-body`, `--book-font-ui`
- `docs/assets/styles/20_book.css`
  - general `.md-typeset .admonition` / `details` baseline in the project layer
- `docs/assets/styles/30_components.css`
  - confirms `hoermal` styles were migrated to `40_custom.css`
- `docs/assets/styles/40_custom.css`
  - primary `hoermal` container, icon and audio layout rules
- `docs/assets/javascripts/audio_src_fixup.js`
  - runtime source-path fixup for audio `<source>` elements using `data-zc-src`

Representative Markdown content files:

- `docs/aussprache.md`
- `docs/orthographie.md`
- `docs/fehlerlinguistik.md`
- `docs/variation/variation_aussprache.md`
- `docs/variation/variation_anrede.md`
- `docs/variation/variation_morphosyntax.md`

Representative rendered HTML files:

- `site/aussprache/index.html`
- `site/orthographie/index.html`
- `site/fehlerlinguistik/index.html`
- `site/variation/variation_aussprache/index.html`
- `site/variation/variation_anrede/index.html`
- `site/variation/variation_morphosyntax/index.html`

Theme/base CSS checked indirectly:

- `site/assets/stylesheets/modern/main.28978c9b.min.css`
  - Material/Zensical base admonition and `details/summary` mechanics

Negative findings:

- No `hoermal`-specific code was found in `overrides/`
- No repo-local shortcode, macro or snippet system was found for `hoermal`
- No current `!!! hoermal` usage was found in `docs/`
- No current content usage of `.audio-pair` or `.audio-label` was found in `docs/`

## Markdown usage patterns

### General pattern

In the current repo, `hoermal` is authored as a collapsible admonition using `??? hoermal`, not as an always-open `!!! hoermal` admonition.

The audio internals are written as raw HTML inside the admonition body.

Typical structure:

```md
??? hoermal "Titel der Hörbox"
    Einleitender Text.

    <div class="audio-comparison">
      ... raw HTML blocks ...
    </div>

    <p class="audio-source">Audios aus ...</p>
```

### Minimal comparison pattern

Used for target pronunciation vs. learner pronunciation.

```md
??? hoermal "Vokale am Wortanfang: Mit und ohne ‚Knacklaut‘"
    Anhand der folgenden Audios kannst Du ... vergleichen:

    <div class="audio-comparison">
    <div class="audio-block">
    <h4>Zielaussprache:</h4> <div class="example-ipa">[o.ˈai]</div>
    <audio controls preload="metadata">
    <source class="zc-audio-src" data-zc-src="assets/audiofiles/marele/glottis_l1.mp3" type="audio/mpeg">
    Dein Browser unterstützt das Audio-Format nicht.
    </audio>
    </div>
    <div class="audio-block">
    <h4>Lernendenaussprache:</h4> <div class="example-ipa">[ʔo.ʔai]</div>
    <audio controls preload="metadata">
    <source class="zc-audio-src" data-zc-src="assets/audiofiles/marele/glottis_ele.mp3" type="audio/mpeg">
    Dein Browser unterstützt das Audio-Format nicht.
    </audio>
    </div>
    </div>

    <p class="audio-source">Audios aus <a href="https://marele.online.uni-marburg.de">MAR.ELE</a></p>
```

Observed in:

- `docs/aussprache.md`
- `docs/orthographie.md`
- `docs/fehlerlinguistik.md`

### Multiple comparison groups inside one `hoermal`

One `hoermal` can contain multiple stacked `.audio-comparison` blocks.

```md
??? hoermal "`/b d g/`: spanische vs. deutsche Aussprache"
    Vergleiche ...

    <div class="audio-comparison">...</div>

    Vergleiche ...

    <div class="audio-comparison">...</div>

    <p class="audio-source">Audios aus ... MAR.ELE</p>
```

This is the current pattern for “mehrere Beispiele” inside one box.

### Grid pattern for collections of equal examples

Used for region sets or multiple parallel examples.

```md
??? hoermal "*Seseo* vs. *distinción*: Hörbeispiele"
    Die folgenden Ausschnitte ...

    <div class="audio-grid">
    <div class="audio-block">
    <h4>Mexiko:</h4>
    <div class="example">
    „(...) esta mujer ...“
    <span class="token-id">(MEXb80def27c)</span>
    </div>
    <audio controls preload="metadata">
    <source class="zc-audio-src" data-zc-src="assets/audiofiles/corapan/MEXb80def27c.mp3" type="audio/mpeg">
    Dein Browser unterstützt das Audio-Format nicht.
    </audio>
    </div>
    ...
    </div>

    <p class="audio-source">Audios aus <a href="https://corapan.hispanistica.com">CO.RA.PAN</a></p>
```

Observed in:

- `docs/variation/variation_aussprache.md`
- `docs/variation/variation_anrede.md`
- `docs/variation/variation_morphosyntax.md`

### Inline IPA and lexical example variants

Two content boxes are used inside `.audio-block`:

- `.example-ipa`
  - compact IPA-only or phonetic-form box
- `.example`
  - lexical or sentence example box, often containing `.ipa` inline spans and `.token-id`

Observed lexical variant:

```md
<span class="example"><i><strong>b</strong>arón</i> <span class="ipa">[baˈɾon]</span> ...</span>
```

Observed sentence example variant:

```md
<div class="example">
„Entonces <strong>vos</strong> cómo <strong>imaginás</strong> ..."
<span class="token-id">(SLVd96cd5aec)</span>
</div>
```

### Source / attribution line

The attribution is manually authored as a separate paragraph with `.audio-source`.

Observed sources:

- `Audios aus MAR.ELE`
- `Audios aus Pronunciation Matters und MAR.ELE`
- `Audios aus CO.RA.PAN`

### Attributes on `<audio>` / `<source>`

Observed patterns:

- `<audio controls preload="metadata">`
- occasional `<audio controls controlsList="nodownload" preload="metadata">`
- `<source class="zc-audio-src" data-zc-src="...">`
- `<source src="/assets/audiofiles/...">`

This means there are two source-addressing modes in content:

- runtime-fixed relative asset path via `data-zc-src`
- direct absolute site path via `src="/assets/..."`

## Rendered HTML structure

### Current rendered shell

Because the current content uses `??? hoermal`, the rendered outer shell is:

```html
<details class="hoermal">
  <summary>...</summary>
  ... body content ...
</details>
```

Representative rendered output from `site/aussprache/index.html`:

```html
<details class="hoermal">
<summary>Vokale am Wortanfang: Mit und ohne ‚Knacklaut‘</summary>
<p>Anhand der folgenden Audios ... vergleichen:</p>
<p><div class="audio-comparison">
<div class="audio-block">
<h4>Zielaussprache:</h4> <div class="example-ipa">[o.ˈai]</div>
<audio controls preload="metadata">
<source class="zc-audio-src" data-zc-src="assets/audiofiles/marele/glottis_l1.mp3" type="audio/mpeg">
Dein Browser unterstützt das Audio-Format nicht.
</audio>
</div>
...
</div></p>
<p><p class="audio-source">Audios aus <a href="https://marele.online.uni-marburg.de">MAR.ELE</a></p></p>
</details>
```

Important: the built HTML currently shows paragraph wrappers around raw block HTML (`<p><div ...>` and `<p><p class="audio-source">...`). That is an observed output detail of the current Markdown/raw-HTML interaction, not an intentional semantic wrapper.

### Supported-but-not-currently-used open variant

CSS explicitly supports both:

```html
<div class="admonition hoermal">
  <p class="admonition-title">...</p>
  ... body ...
</div>
```

and

```html
<details class="hoermal">
  <summary>...</summary>
  ... body ...
</details>
```

However, no current `!!! hoermal` source usage was found in `docs/`, so the `div.admonition.hoermal` variant is CSS-supported but not evidenced in current authored content.

### Semantic structure

- Container
  - `details.hoermal` in current content; visually a tinted admonition shell with a strong left rail
- Collapse button
  - the `summary` row carries the title and the default `details` chevron from the theme
- Icon
  - injected through the admonition-title/summary `::before` pseudo-element and swapped to a speaker icon in project CSS
- Title
  - comes from the admonition title string in Markdown, rendered in `<summary>`
- Intro
  - usually a plain paragraph before any audio grid/comparison
- Comparison region
  - either `.audio-comparison` for paired contrast or `.audio-grid` for equal example collections
- Audio block
  - `.audio-block` contains heading/label, example box and native `<audio>` player
- Transcript / IPA box
  - `.example-ipa` for phonetic forms; `.example` for lexical/sentence material; `.ipa` can appear inline inside `.example`
- Token / source identifier
  - `.token-id` sits inside `.example` and is anchored bottom-right
- Audio player
  - native browser `<audio controls>` element, width 100%
- Source line
  - `.audio-source`, right-aligned, smaller and quieter than main text

What makes the component read as “Hörmaterial”:

- dedicated speaker icon
- blue-tinted background and blue 4px left rail
- collapsible title row
- repeated native audio players at the bottom of each content block
- compact UI typography for labels plus separate example box above the player

What creates internal order:

- intro paragraph before media content
- grid gaps between audio blocks
- example/transcript box separated visually from player control
- token-id pushed into the lower corner of the example box
- source line detached at the bottom and right-aligned

Optional elements observed:

- intro paragraph
- one or multiple comparison groups
- `.example` versus `.example-ipa`
- inline `.ipa` span within `.example`
- `.token-id`
- source attribution line
- `controlsList="nodownload"`

Typical for two-audio contrast:

- heading/title in summary
- short intro paragraph
- one or more `.audio-comparison` groups
- inside each comparison: one “Zielaussprache” block and one “Lernendenaussprache” block
- final `.audio-source`

### Element order in current content

Current order is generally:

1. container (`details.hoermal`)
2. title row (`summary`)
3. intro text paragraph
4. comparison/grid wrapper
5. per-block label (`h4`; CSS also supports `.audio-label`)
6. transcript/example box (`.example` or `.example-ipa`)
7. optional inline `.token-id` inside `.example`
8. native audio player
9. source/attribution line (`.audio-source`)

The collapse chevron belongs to the `summary` row; there is no separate custom collapse button in content markup.

## CSS rules

### Cascade order relevant to `hoermal`

From `zensical.toml`, the relevant CSS order is:

1. theme base CSS (Material/Zensical bundled stylesheet)
2. `docs/assets/styles/00_tokens.css`
3. `docs/assets/styles/10_typography.css`
4. `docs/assets/styles/20_book.css`
5. `docs/assets/styles/30_components.css`
6. `docs/assets/styles/40_custom.css`

Practical effect:

- theme CSS provides the base admonition and `details/summary` behavior
- `20_book.css` normalizes the project-wide admonition shell
- `40_custom.css` specializes `hoermal` with its own tint, rail, icon and audio layouts

### `site/assets/stylesheets/modern/main.28978c9b.min.css` (theme base, indirect)

Relevant base rules, reformatted from the minified theme bundle:

```css
.md-typeset .admonition,
.md-typeset details {
  background-color: #448aff1a;
  border-radius: .4rem;
  color: var(--md-admonition-fg-color);
  display: flow-root;
  font-size: .64rem;
  margin: 1.5625em 0;
  padding: 0 .8rem;
  page-break-inside: avoid;
}

.md-typeset .admonition > *,
.md-typeset details > * {
  box-sizing: border-box;
}

.md-typeset .admonition-title,
.md-typeset summary {
  font-weight: 700;
  margin-bottom: 1em;
  margin-top: .6rem;
  position: relative;
}

.md-typeset .admonition-title::before,
.md-typeset summary::before {
  content: "";
  position: absolute;
  top: .125em;
  width: 1rem;
  height: 1rem;
  background-color: #448aff;
  -webkit-mask-position: center;
  mask-position: center;
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-size: contain;
  mask-size: contain;
}

.md-typeset details {
  display: flow-root;
  overflow: visible;
  padding-top: 0;
}

.md-typeset details[open] > summary::after {
  transform: rotate(90deg);
}

.md-typeset details:not([open]) {
  box-shadow: none;
  padding-bottom: 0;
}

.md-typeset details:not([open]) > summary {
  border-radius: .1rem;
  margin-bottom: .6rem;
}

.md-typeset summary {
  cursor: pointer;
  display: block;
  min-height: 1rem;
  overflow: hidden;
}

.md-typeset summary::after {
  content: "";
  position: absolute;
  top: .125em;
  width: 1rem;
  height: 1rem;
  background-color: currentcolor;
  -webkit-mask-image: var(--md-details-icon);
  mask-image: var(--md-details-icon);
  -webkit-mask-position: center;
  mask-position: center;
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-size: contain;
  mask-size: contain;
  transition: transform .25s;
}
```

Effect on `hoermal`:

- provides the admonition box model
- provides summary interaction and chevron rotation
- provides pseudo-element slots for icon and chevron
- project CSS later recolors/replaces the icon and rewrites shell colors

### `docs/assets/styles/20_book.css`

Project-wide admonition/details baseline:

```css
.md-typeset .admonition,
.md-typeset details {
  font-size: 0.78rem;
  line-height: 1.65;
  margin: 1.15em 0;
  background: var(--book-surface-1);
  border: 1px solid var(--book-border);
  box-shadow: none;
}

.md-typeset .admonition-title,
.md-typeset summary {
  font-family: var(--book-font-ui);
  margin-bottom: 0.65em;
}

.md-typeset details:not([open]) > summary {
  margin-bottom: 0.65em;
}
```

Effect on `hoermal`:

- enlarges text from the theme base
- swaps title/summary to UI font
- removes theme-like shadow emphasis
- gives `hoermal` the same calmer container geometry as other project admonitions before `40_custom.css` specializes it further

### `docs/assets/styles/30_components.css`

No active `hoermal` selectors remain here. The file explicitly states that `hoermal` moved to `40_custom.css`.

```css
/* Admonition: hoermal -> migriert nach 40_custom.css (Container + Icon + Audio-Layout) */
```

### `docs/assets/styles/40_custom.css`

#### Icon definition and shell specialization

```css
:root {
  --md-typeset-hoermal-icon: url('data:image/svg+xml;charset=utf-8,...speaker svg...');
}

.md-typeset .admonition.hoermal,
.md-typeset details.hoermal {
  background: color-mix(in srgb, var(--book-bg) var(--book-adm-tint-light), var(--book-adm-hoermal));
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-left: 4px solid var(--book-adm-hoermal);
  border-radius: 0.4rem;
  box-shadow: none;
}

body[data-md-color-scheme="slate"] .md-typeset .admonition.hoermal,
body[data-md-color-scheme="slate"] .md-typeset details.hoermal {
  background: color-mix(in srgb, var(--book-surface-1) var(--book-adm-tint-dark), var(--book-adm-hoermal));
  border-color: rgba(255, 255, 255, 0.08);
  border-left-color: var(--book-adm-hoermal);
}

.md-typeset .admonition.hoermal {
  --md-admonition-icon: var(--md-typeset-hoermal-icon);
}

.md-typeset .admonition.hoermal > .admonition-title,
.md-typeset details.hoermal > summary {
  color: var(--book-fg);
  font-weight: 500;
}

.md-typeset .hoermal > .admonition-title:before,
.md-typeset .hoermal > summary:before {
  background-color: var(--book-adm-hoermal);
  -webkit-mask-image: var(--md-typeset-hoermal-icon);
  mask-image: var(--md-typeset-hoermal-icon);
}

.md-typeset .hoermal > .admonition-title::before,
.md-typeset .hoermal > summary::before {
  transform: translateY(0.06em);
}
```

Notes:

- both open `div.admonition.hoermal` and collapsible `details.hoermal` are styled together
- the left rail, not a full border tint alone, is the strongest semantic marker
- summary/title color is reset to `var(--book-fg)` rather than the theme accent

#### Audio comparison wrapper

```css
.md-typeset .admonition.hoermal .audio-comparison,
.md-typeset details.hoermal .audio-comparison {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.1rem 1.4rem;
  margin-top: 0.9rem;
  align-items: stretch;
}

@media (min-width: 720px) {
  .md-typeset .admonition.hoermal .audio-comparison,
  .md-typeset details.hoermal .audio-comparison {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
```

Observed use:

- current paired target-vs-learner examples
- one or several `.audio-comparison` wrappers can be stacked in a single `hoermal`

#### Audio pair wrapper

```css
.md-typeset .admonition.hoermal .audio-pair,
.md-typeset details.hoermal .audio-pair {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.1rem 1.4rem;
  align-items: stretch;
}

@media (min-width: 720px) {
  .md-typeset .admonition.hoermal .audio-pair,
  .md-typeset details.hoermal .audio-pair {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
```

Current status:

- supported in CSS
- no content usage found in `docs/`

#### Audio grid wrapper

```css
.md-typeset .admonition.hoermal .audio-grid,
.md-typeset details.hoermal .audio-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.1rem 1.4rem;
  margin-top: 0.9rem;
  align-items: stretch;
}

@media (min-width: 720px) {
  .md-typeset .admonition.hoermal .audio-grid,
  .md-typeset details.hoermal .audio-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
```

Observed use:

- region/example collections in variation chapters

#### Shared audio block styling

```css
.md-typeset .admonition.hoermal .audio-block,
.md-typeset details.hoermal .audio-block {
  position: relative;
  display: flex;
  flex-direction: column;
  min-width: 0;
  text-align: left;
  padding-bottom: 1.4rem;
}

.md-typeset .admonition.hoermal .audio-label,
.md-typeset details.hoermal .audio-label,
.md-typeset .admonition.hoermal .audio-block h4,
.md-typeset details.hoermal .audio-block h4 {
  font-family: var(--book-font-ui);
  font-weight: 600;
  letter-spacing: -0.01em;
  font-size: 0.85em;
  line-height: 1.35;
  margin: 0 0 0.35rem 0;
}
```

Notes:

- `.audio-label` exists as a CSS-ready semantic class
- current content uses `h4`, not `.audio-label`
- `padding-bottom: 1.4rem` reserves visual room for `.token-id`

#### Example / transcript boxes

```css
.md-typeset .admonition.hoermal .example,
.md-typeset .admonition.hoermal .example-ipa,
.md-typeset details.hoermal .example,
.md-typeset details.hoermal .example-ipa {
  position: relative;
  display: block;
  font-size: 0.92em;
  font-weight: 500;
  line-height: 1.5;
  opacity: 0.9;
  margin: 0 0 0.55rem 0;
  flex: 1 1 auto;
  background: color-mix(in srgb, var(--book-bg) 92%, var(--book-border));
  border: 1px solid color-mix(in srgb, var(--book-border) 70%, transparent);
  border-radius: 0.35rem;
}

.md-typeset .admonition.hoermal .example,
.md-typeset details.hoermal .example {
  padding: 0.45rem 0.6rem 1.5rem 0.6rem;
  font-family: var(--book-font-body);
}

.md-typeset .admonition.hoermal .example-ipa,
.md-typeset details.hoermal .example-ipa {
  padding: 0.45rem 0.6rem;
  font-family: "Noto Sans", "Inter", var(--book-font-body), sans-serif;
}

.md-typeset .admonition.hoermal .example-text,
.md-typeset details.hoermal .example-text {
  display: block;
}

.md-typeset .admonition.hoermal .ipa,
.md-typeset details.hoermal .ipa {
  font-family: "Noto Sans", "Inter", var(--book-font-body), sans-serif;
  margin-left: 0.08em;
}
```

Notes:

- `.example` reserves extra bottom room for token ids
- `.example-ipa` is tighter and does not reserve bottom room
- the IPA stack explicitly adds `Noto Sans` and `Inter` before the serif body stack

#### Token id and dark-mode example adjustments

```css
.md-typeset .admonition.hoermal .token-id,
.md-typeset details.hoermal .token-id {
  position: absolute;
  right: 0.6rem;
  bottom: 0.4rem;
  display: block;
  text-align: right;
  font-size: 0.85em;
  color: var(--md-default-fg-color--light);
  opacity: 0.95;
  line-height: 1;
}

body[data-md-color-scheme="slate"] .md-typeset .admonition.hoermal .example,
body[data-md-color-scheme="slate"] .md-typeset .admonition.hoermal .example-ipa,
body[data-md-color-scheme="slate"] .md-typeset details.hoermal .example,
body[data-md-color-scheme="slate"] .md-typeset details.hoermal .example-ipa {
  background: color-mix(in srgb, var(--book-surface-1) 88%, var(--book-border));
  border-color: color-mix(in srgb, rgba(255,255,255,0.14) 70%, transparent);
}
```

#### Native audio element and source line

```css
.md-typeset .admonition.hoermal .audio-block audio,
.md-typeset details.hoermal .audio-block audio {
  display: block;
  width: 100%;
  margin: 0;
  margin-top: auto;
}

.md-typeset .admonition.hoermal .audio-source,
.md-typeset details.hoermal .audio-source {
  margin-top: 0.9rem;
  font-size: 0.85em;
  opacity: 0.7;
  text-align: right;
  font-style: normal;
}

.md-typeset .admonition.hoermal audio::-webkit-media-controls-timeline,
.md-typeset details.hoermal audio::-webkit-media-controls-timeline {
  flex: 1;
}
```

Notes:

- player is always stretched to full block width
- `margin-top: auto` pushes player to the bottom of each flex column for vertical alignment
- no project-wide custom styling of the whole player chrome was found
- only a scoped WebKit timeline flex fix is present

## Design tokens and variables

### Project tokens from `docs/assets/styles/00_tokens.css`

#### Tint mixing

```css
:root {
  --book-adm-tint-light: 93%;
  --book-adm-tint-dark: 90%;
}
```

- `--book-adm-tint-light`
  - defined in `00_tokens.css`
  - used by light-mode `hoermal` background mixing in `40_custom.css`
  - no fallback in the usage site
- `--book-adm-tint-dark`
  - defined in `00_tokens.css`
  - used by dark-mode `hoermal` background mixing in `40_custom.css`
  - no fallback in the usage site

#### `hoermal` hue token

```css
body[data-md-color-scheme="default"] {
  --book-adm-hoermal: #4f6b88;
}

body[data-md-color-scheme="slate"] {
  --book-adm-hoermal: #82a4c7;
}
```

- `--book-adm-hoermal`
  - defined per color scheme in `00_tokens.css`
  - used for the left rail, icon color and mixed shell background
  - no fallback in the usage site

#### Surface and border tokens used in mixes

- `--book-bg`
  - defined per scheme in `00_tokens.css`
  - used in light-mode shell and example background mixing
- `--book-surface-1`
  - defined per scheme in `00_tokens.css`
  - used in dark-mode shell/example mixing and general admonition baseline
- `--book-border`
  - defined per scheme in `00_tokens.css`
  - used for general admonition border and example box borders
- `--book-fg`
  - defined per scheme in `00_tokens.css`
  - used for summary/title text color

Other global tokens exist (`--book-radius`, `--book-shadow`, spacing scale), but `hoermal` does not directly consume them in its selectors.

### Typography tokens from `docs/assets/styles/10_typography.css`

```css
:root {
  --book-font-body: "Source Serif 4", Georgia, "Times New Roman", "Noto Serif", serif;
  --book-font-ui: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
}
```

- `--book-font-body`
  - defined in `10_typography.css`
  - used for `.example` boxes and general prose
  - explicit fallback stack included in definition
- `--book-font-ui`
  - defined in `10_typography.css`
  - used for title row, labels and `h4` headings in audio blocks
  - explicit fallback stack included in definition

### `hoermal` icon variable from `docs/assets/styles/40_custom.css`

```css
:root {
  --md-typeset-hoermal-icon: url('data:image/svg+xml;charset=utf-8,...');
}
```

- `--md-typeset-hoermal-icon`
  - defined in `40_custom.css`
  - used as the speaker icon mask on `.hoermal > .admonition-title::before` / `.hoermal > summary::before`
  - no fallback in the usage site

### Theme/base variables inherited from bundled Material/Zensical CSS

- `--md-details-icon`
  - defined upstream in bundled theme CSS
  - used for the chevron on `summary::after`
  - no repo-local override found
- `--md-admonition-fg-color`
  - defined upstream in bundled theme CSS
  - used by the generic admonition/details shell before project overrides replace local colors
  - no repo-local override specific to `hoermal`
- `--md-default-fg-color--light`
  - defined upstream in bundled theme CSS
  - used for `.token-id` text color
  - no repo-local fallback found

### Breakpoints and dimensions used by `hoermal`

- `720px`
  - defined inline in `40_custom.css`
  - switches `.audio-comparison`, `.audio-pair` and `.audio-grid` from one column to two columns
- `0.4rem`
  - border radius for the shell
- `4px`
  - left rail width
- `1.1rem 1.4rem`
  - grid gaps
- `0.9rem`
  - top margin before audio wrappers and source line
- `1.4rem`
  - reserved bottom space in `.audio-block` for content breathing room around the lower edge

## Audio player behavior

### Player type

The component uses the native browser player:

```html
<audio controls preload="metadata">
  <source ... type="audio/mpeg">
  Dein Browser unterstützt das Audio-Format nicht.
</audio>
```

There is no custom player chrome, no custom play/pause buttons, and no project-local JS that replaces the native player UI.

### JavaScript involvement

Only one relevant script was found:

`docs/assets/javascripts/audio_src_fixup.js`

Behavior:

- selects `source.zc-audio-src[data-zc-src]`
- resolves the `data-zc-src` value against `window.ZENSICAL_BASE_PATH || "/"`
- writes the computed value into `src`
- calls `audio.load()` on the parent `<audio>` element
- reruns on `DOMContentLoaded`
- reruns after instant-navigation page swaps via `document$.subscribe(...)`

This means the script is path-fixup infrastructure, not player behavior logic.

### Wrapper model around audio

Per current content, the player usually sits inside this structure:

```html
<div class="audio-block">
  <h4>...</h4>
  <div class="example">...</div>
  <audio controls preload="metadata">
    <source ...>
  </audio>
</div>
```

or:

```html
<div class="audio-block">
  <h4>...</h4>
  <div class="example-ipa">...</div>
  <audio controls preload="metadata">
    <source ...>
  </audio>
</div>
```

### Target pronunciation vs. learner pronunciation

Current structure is not encoded by special classes such as `.target` or `.learner`.

Instead, the distinction is conveyed by the content heading text inside each block:

- `Zielaussprache:`
- `Lernendenaussprache:`

This is a content convention, not a dedicated CSS API.

### Downloads, duration, sizing, controls

- width: forced to `100%`
- alignment: `margin-top: auto` aligns controls to the bottom of flex columns
- preload: almost always `metadata`
- download suppression: only occasional `controlsList="nodownload"`, not standard across all `hoermal` boxes
- duration display: native browser behavior only
- timeline styling: only WebKit flex fix, no visual skinning

## Responsive behavior

Current responsive logic is simple and localized.

### Container shell

- no `hoermal`-specific shell breakpoint exists
- it inherits the page/content width behavior from the wider layout system

### Audio comparison and grid

At viewport widths below `720px`:

- `.audio-comparison` is one column
- `.audio-pair` is one column
- `.audio-grid` is one column

At `min-width: 720px`:

- `.audio-comparison` becomes two equal columns
- `.audio-pair` becomes two equal columns
- `.audio-grid` becomes two equal columns

So the mobile behavior is a full vertical stack; the desktop/tablet-up behavior is a clean two-column grid.

### Typography

Indirectly relevant from `10_typography.css`:

- `.md-typeset` base font size drops from `20px` to `18px` below `767px`

That change affects the perceived scale of labels, examples and player context text, since many `hoermal` measurements are expressed in `em` or `rem`.

## Variants found

### Variant 1: paired pronunciation contrast

Observed structure:

- `details.hoermal`
- intro paragraph
- one or more `.audio-comparison`
- each comparison contains two `.audio-block`s
- block heading usually via `h4`
- transcript box via `.example-ipa` or `.example`
- native audio player
- source line

Typical use:

- target pronunciation vs learner pronunciation
- German transfer vs Spanish target pronunciation

### Variant 2: flat example collection

Observed structure:

- `details.hoermal`
- intro paragraph
- `.audio-grid`
- multiple `.audio-block`s of equal status
- each block contains region label, sentence example, token id and native player
- source line

Typical use:

- regional comparison
- multiple country examples
- morphosyntactic/audio variation sets

### Variant 3: stacked comparison groups inside one box

Observed structure:

- one `details.hoermal`
- multiple `.audio-comparison` wrappers one after another

Typical use:

- one box containing more than one target-vs-learner pair

### CSS-supported but not currently evidenced in content

- open `div.admonition.hoermal`
- `.audio-pair`
- `.audio-label`
- `.example-text`

These should be treated as part of the available styling API, but not as currently validated authoring patterns in this repo.

## Notes for reuse in PROMAT Teaching

Directly transferable ideas:

- `details`-based shell for collapsible listening material
- strong semantic left rail plus dedicated speaker icon
- native `<audio controls>` instead of a custom player
- per-example wrapper with transcript/example box above the player
- one responsive layout vocabulary for both paired contrasts and flat collections
- right-aligned compact source line

Useful more as inspiration than 1:1 copy:

- the exact raw-HTML-in-Markdown authoring style
- the mixed use of `h4` and implicit content conventions instead of stricter semantic helper classes
- the current paragraph-wrapper artifacts in rendered HTML

What should not be copied 1:1 into another app/CSS stack without adaptation:

- reliance on Material/Zensical `details/summary` mechanics and pseudo-element slots
- reliance on project tokens such as `--book-adm-hoermal`, `--book-bg`, `--book-surface-1`, `--book-font-ui`
- use of `source.zc-audio-src[data-zc-src]` plus `audio_src_fixup.js`, unless the target project also has a base-path problem to solve
- current font assumptions (`Source Serif 4`, `Inter`, `Noto Sans`)
- current theme variable inheritance like `--md-default-fg-color--light`

Practical reuse takeaway:

- the reusable core is the shell + grid + native-player composition
- the repo-specific parts are mostly the token names, theme hook variables and path-fixup infrastructure

## Open questions

1. The current build output wraps some raw HTML blocks in paragraph tags (`<p><div ...>` and `<p><p class="audio-source">...`). Browsers tolerate this, but it is worth confirming whether this output is considered acceptable or merely incidental.
2. `40_custom.css` supports `.audio-pair`, `.audio-label` and open `.admonition.hoermal`, but no current authored examples were found. If these are intended authoring APIs, an explicit example page would make reuse safer.
3. `--md-default-fg-color--light`, `--md-details-icon` and other theme variables are inherited from the bundled Material/Zensical base CSS, not defined in repo-local source files. If the upstream theme bundle changes, some inherited behavior may shift without local CSS changes.