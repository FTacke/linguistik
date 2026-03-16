# Popup Standardization for Zensical Maps

This document defines a **single unified popup system** for all interactive maps in the Zensical project.  
It serves both as **design specification** and as a **prompt/instruction set** for implementing the popup system across the codebase.

Affected maps:

- variation_tempora map
- herkunftssprachen map
- countries map

Affected files (likely):

- `50_map.css`
- `map_variation_tempora.js`
- `map.js`
- `map_countries.js`
- JSON data sources such as:
  - `variation_tempora.json`
  - `herkunftssprachen.json`
  - `countries.json`

The goal is to implement **one consistent popup layout system** with different content modules depending on the map type.

---

# 1. Design Goals

The popup system must:

1. Be **compact and quickly scannable**
2. Use **clear typographic hierarchy**
3. Avoid verbose label-value lists
4. Work **consistently across all maps**
5. Keep the **map visually dominant**
6. Use **minimal color inside popups**
7. Avoid large popups that obscure the map

Popups should feel like **small editorial information cards**, not data tables.

---

# 2. Popup Layout System

All popups must follow the same structural pattern.

## General Structure

```

Title

(optional metric block)

Section label
Content

Section label
Content

```

Spacing should be tight but readable.

---

# 3. Typography Hierarchy

The popup hierarchy should be:

| Element | Role |
|-------|------|
| Title | Primary identifier |
| Metric block | Key numeric information |
| Section labels | Structural markers |
| Body text | Information |
| Example text | Linguistic examples |
| Interpretation | Explanation lines |

---

# 4. Global Popup CSS Specification

Update `50_map.css` to implement a shared popup design system.

### Popup width

Increase slightly for readability:

```

--map-popup-max-width: 300px

```

### Base popup typography

```

font-size: 0.78rem
line-height: 1.4

```

### Title

```

.popup-title
font-weight: 700
font-size: 1rem
margin-bottom: 8px
color: var(--book-fg)
line-height: 1.2

```

Title should **not use accent colors**.

---

### Section labels

```

.popup-section-label
font-size: 0.68rem
font-weight: 600
letter-spacing: 0.04em
text-transform: uppercase
color: var(--book-muted)
margin-top: 10px
margin-bottom: 4px

```

Section labels must be **visually quiet but structured**.

---

### Body content

```

.popup-body
font-size: 0.78rem
color: var(--book-fg)
line-height: 1.35

```

---

### Metric block

Used for numeric information like frequencies or speaker counts.

```

.popup-metric-label
font-size: 0.68rem
font-weight: 600
color: var(--book-muted)
letter-spacing: 0.04em
margin-bottom: 4px

```
```

.popup-metric
font-weight: 600
font-variant-numeric: tabular-nums
line-height: 1.3
margin-bottom: 10px

```

Optional subtle background:

```

padding: 4px 6px
border-radius: 6px
background: color-mix(in srgb, var(--book-surface-1) 92%, white)

```

---

### Example sentences

Examples should be slightly differentiated from normal text.

```

.popup-example
font-style: italic
line-height: 1.35
margin-top: 2px

```

---

### Interpretation lines

Interpretations should be visually secondary.

```

.popup-interpretation
font-size: 0.92em
color: var(--book-muted)
line-height: 1.3
margin-top: 2px

```

---

# 5. Content Modules per Map Type

Each map uses the same popup structure but different modules.

---

# 5.1 Tempus Variation Map

Popup structure:

```

Title

(optional frequency block)

Gebrauchssystem <System name>

Beispiel <example sentences>

```

### Frequency block

Only shown for empirical measurement points.

```

Frequenz (freie Rede)

59 % compuesto | 41 % simple

```

If no frequency data exists:

- Entire block is omitted
- No placeholder text.

---

### Usage systems

Allowed values:

- Prototypischer Gebrauch des perfecto compuesto
- Dominanz des perfecto simple
- Aspektuelles Gebrauchssystem
- Expansion des perfecto compuesto

No separate transition-zone system.

---

### Examples

Use these examples consistently:

**Prototypischer Gebrauch**

```

Hoy he hablado con Ana.
Ayer hablé con Ana.

```

**Dominanz des simple**

```

Hoy hablé con Ana.

```

**Aspektuelles System**

```

Viví en Puebla dos años.
→ Zeitraum abgeschlossen

He vivido en Puebla dos años.
→ bis heute, meist weiterhin

```

**Expansion des compuesto**

```

He llegado ayer.

```

---

# 5.2 Herkunftssprachen Map

Popup structure:

```

Title

Sprachfamilie <family>

Herkunft <region description>

```

Example:

```

Arabisch
Semitisch (Afroasiatisch)

Syrien (arabisch dominiert)

```

No metric block.

---

# 5.3 Countries Map

Popup structure:

```

Title

Hauptstadt <city>

Sprecher:innen <number>

Anteil Hispanophonie <percentage>

```

Example:

```

Venezuela

Hauptstadt
Caracas

Sprecher:innen
28.632.291

Anteil Hispanophonie
5.8 %

```

Numbers should use tabular numerals.

---

# 6. JSON Data Adjustments

JSON files may require minor adjustments to support the unified popup renderer.

Examples:

### Tempus map

Fields should include:

```

name
system
exampleType
frequency_compuesto
frequency_simple
hasData

```

### Countries

```

name
capital
speakers
share

```

### Herkunftssprachen

```

name
family
origin

```

---

# 7. JavaScript Renderer Refactor

JS files should generate popups using the same structural classes.

Avoid ad-hoc HTML generation.

All popups should use:

```

.popup-title
.popup-metric-label
.popup-metric
.popup-section-label
.popup-body
.popup-example
.popup-interpretation

```

The renderer should conditionally include modules depending on the map type.

---

# 8. Size Optimization

Popups must remain visually lightweight.

Target properties:

- max width ~300px
- minimal vertical padding
- compact spacing
- no oversized titles
- minimal color use

The popup must **never dominate the map view**.

---

# 9. Map Marker Behavior

Popups should not alter marker logic.

Markers remain:

- colored by system
- visually stronger than popup text

The popup is purely informational.

---

# 10. Final Objective

After implementation:

- All maps share **one popup design language**
- Tooltips feel **editorial, clean, and modern**
- Content is **compact and easy to scan**
- Layout is **consistent across maps**
- Implementation is **modular and maintainable**
```
