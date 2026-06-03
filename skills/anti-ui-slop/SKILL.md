---
name: anti-ui-slop
description: >
  Detect and fix AI-generated UI anti-patterns ("AI slop") in frontend code.
  Use when: building new UI, reviewing existing UI code, refining visual design,
  or whenever the user says "check for slop", "remove AI look", "make it look human-designed",
  "why does this look AI-generated", or "polish the UI".
  Scans HTML, CSS, JSX/TSX, and Tailwind for ~40 known tells of machine-generated interfaces,
  then rewrites the offending code. Zero dependencies — pure static analysis by reading source files.
license: MIT
---

# Anti UI Slop

Detect and eliminate the visual fingerprints of AI-generated UIs. Every pattern below is a known tell that makes an interface look machine-made. This skill operates on source code alone — no browser, no CLI tool, no npm package required.

---

## Workflow

1. **Scan** — Read all UI source files (HTML, CSS, JSX/TSX, Vue, Svelte, Tailwind config). Grep for the signatures listed in each rule.
2. **Diagnose** — For every match, cite the file, line, and rule violated.
3. **Fix** — Rewrite the offending code. Apply the remedy described in each rule. Prefer minimal, targeted edits.
4. **Report** — Output a table: `File:Line | Rule | Before → After`. Group by severity (Critical / Warning / Info).

---

## Rules

### A. Visual Details

#### A1 · Side-tab accent border
**Detect:** `border-left: *px solid`, `border-l-{n}` (Tailwind), or any single-side border ≥ 3px on a card/container.
**Why:** Thick colored stripe on one side of a card is the single most recognizable AI-UI tell.
**Fix:** Remove the side border. If the accent is needed, use a subtle top highlight (`border-top: 2px`) or a colored dot/icon inline.

#### A2 · Border accent on rounded element
**Detect:** Element has both `border-radius ≥ 12px` (or `rounded-xl`+) and `border ≥ 2px solid <color>`.
**Why:** Thick colored borders clash with large radii — a generated-card signature.
**Fix:** Remove the colored border (keep a 1px neutral border if needed), or reduce `border-radius` to ≤ 8px.

#### A3 · Hairline border + wide shadow (opt-in)
**Detect:** `border: 1px` combined with `box-shadow` blur ≥ 20px on the same element.
**Why:** A hairline edge plus a diffuse glow is a GPT-era card signature. Commit to one elevation strategy.
**Fix:** Drop the border (shadow alone) or drop the shadow (border alone).

#### A4 · Repeating-gradient stripes (opt-in)
**Detect:** `repeating-linear-gradient` or `repeating-conic-gradient` used as surface decoration.
**Why:** Decorative candy-stripes are a recurring generated-UI texture.
**Fix:** Remove the gradient. Use a solid surface or a deliberate brand texture.

#### A5 · Extreme border-radius
**Detect:** `border-radius ≥ 24px` on cards, sections, or inputs (not pill badges/tags).
**Why:** Over-rounding turns every container into the same soft blob.
**Fix:** Cap card radius at 12–16px. Reserve `9999px`/full-pill for tags and small buttons only.

#### A6 · Nested cards
**Detect:** A bordered/shadowed container directly inside another bordered/shadowed container, more than 2 levels.
**Why:** Cards-inside-cards create visual noise with redundant depth cues.
**Fix:** Flatten: use spacing, typography, and dividers instead of nesting containers.

#### A7 · Glassmorphism everywhere
**Detect:** `backdrop-filter: blur`, `background: rgba(255,255,255,0.*)`, glass-like styling used decoratively (not for modals/overlays with a functional reason).
**Why:** Frosted glass as decoration rather than layering solution is a hackathon aesthetic.
**Fix:** Use solid, opaque backgrounds. Reserve blur only for overlays that must reveal content beneath.

---

### B. Typography

#### B1 · Flat type hierarchy
**Detect:** Heading and body font sizes differ by < 1.25× ratio (e.g., heading 18px, body 16px).
**Why:** No visual contrast between levels — everything reads at the same importance.
**Fix:** Enforce ≥ 1.25× ratio between each type step. Example scale: 14 / 18 / 22 / 28 / 36.

#### B2 · Icon tile stacked above heading
**Detect:** A small rounded-square container (`w-10 h-10 rounded-lg` or similar) holding an icon, placed directly above a heading inside a card.
**Why:** The universal AI feature-card template. Every generator outputs this exact layout.
**Fix:** Place icon and heading side-by-side, or let the icon sit inline without its own container.

#### B3 · Hero eyebrow / pill chip
**Detect:** A tiny uppercase letter-spaced label or pill-shaped chip immediately above a hero headline.
**Why:** Default AI SaaS hero scaffolding.
**Fix:** Drop the eyebrow, fold the kicker into the headline, or run it as a breadcrumb.

#### B4 · Repeated section kicker labels
**Detect:** ≥ 3 sections each with a tiny uppercase tracked label (e.g., `text-xs uppercase tracking-wider`) above the section heading.
**Why:** Turns a page into AI editorial scaffolding.
**Fix:** Remove most kickers. Use stronger structural hierarchy, imagery, or a deliberate brand system instead.

#### B5 · Italic serif display headline
**Detect:** `font-style: italic` combined with a serif font at display size (≥ 32px).
**Why:** Oversized italic serif hero has become the universal AI-startup landing page look.
**Fix:** Set it roman, or switch to a non-serif display face. Exception: editorial/magazine contexts.

#### B6 · Oversized hero headline
**Detect:** A headline with ≥ 8 words set at ≥ 48px (or `text-5xl`+).
**Why:** A full sentence blown up to display size dominates the viewport and leaves no room above the fold.
**Fix:** Shorten the copy to 2–4 words at that size, or reduce font size for long headlines.

#### B7 · Crushed letter spacing
**Detect:** `letter-spacing` more negative than `-0.05em` (or `tracking-tighter` in Tailwind).
**Why:** Destructive tightening costs legibility.
**Fix:** Tighten display type to at most `-0.02em`. Remove negative tracking from body text entirely.

#### B8 · Overused font
**Detect:** `font-family` contains Inter, Geist, Space Grotesk, or Instrument Serif as the primary face.
**Why:** These faces have converged into the "AI default" — they no longer feel distinctive.
**Fix:** Choose a face with personality. Suggestions: Satoshi, General Sans, Cabinet Grotesk, Switzer, or a curated serif.

#### B9 · Single font for everything
**Detect:** Only one `font-family` declaration across the entire page/app.
**Why:** No typographic contrast — headings and body text blur together.
**Fix:** Pair a distinctive display font with a refined body font.

#### B10 · All-caps body text
**Detect:** `text-transform: uppercase` on paragraphs or long text blocks (> 20 words).
**Why:** Uppercase removes ascender/descender shapes, killing word recognition.
**Fix:** Reserve uppercase for short labels and headings (≤ 4 words). Use sentence case for body.

#### B11 · Numbered section markers (01 / 02 / 03)
**Detect:** Display-sized numbers like `01`, `02`, `03` used as section labels.
**Why:** AI editorial scaffolding, not meaningful numbering.
**Fix:** Remove unless the content is genuinely sequential (steps, a timeline).

---

### C. Color & Contrast

#### C1 · AI color palette
**Detect:** Purple/violet gradients (`#7c3aed`, `#8b5cf6`, `oklch(60% 0.22 265–290)`), or cyan-on-dark as primary accent.
**Why:** Purple-to-blue gradient is the most recognizable AI palette. Cyan-on-dark is its dark-mode twin.
**Fix:** Choose a distinctive, intentional brand palette. Avoid purple as primary unless it is the actual brand color.

#### C2 · Dark mode with glowing accents
**Detect:** Dark background (`bg-gray-900`, `#0a0b14`, etc.) combined with `box-shadow` using a colored glow (`0 0 Npx <color>`), neon `text-shadow`, or colored shadow utilities.
**Why:** Cyberpunk-by-default — the "cool" AI look.
**Fix:** Use subtle, neutral shadows on dark surfaces. Skip colored glows entirely.

#### C3 · Gradient text
**Detect:** `background-clip: text` + `text-fill-color: transparent` (or Tailwind `bg-clip-text text-transparent bg-gradient-to-*`).
**Why:** Decorative gradient text is a common AI tell on headings and metrics.
**Fix:** Use solid colors for all text. Reserve gradients for surface backgrounds if needed.

#### C4 · Gray text on colored background
**Detect:** Gray text (`text-gray-*`, `color: #9ca3af`, etc.) rendered on a non-white/non-gray background.
**Why:** Gray washes out on colored surfaces — unreadable.
**Fix:** Use white/near-white text on dark surfaces, or a darker shade of the background color.

#### C5 · Cream / beige palette
**Detect:** Page background is a warm off-white (`#f5efe2`, `#faf7f2`, `bg-amber-50`, `bg-orange-50`).
**Why:** Cream has become the default AI "tasteful" surface, reached for by reflex.
**Fix:** Use a deliberate palette. If warmth is intentional, pair it with a strong secondary color to prove it's a choice, not a default.

---

### D. Layout & Space

#### D1 · Identical card grids
**Detect:** ≥ 4 sibling cards with identical structure (icon + heading + paragraph), same sizing, in a uniform grid.
**Why:** The default AI homepage layout — "features section."
**Fix:** Vary card sizes, use asymmetric layouts, highlight one card, or replace with a different pattern (table, accordion, inline list).

#### D2 · Monotonous spacing
**Detect:** The same gap/padding value (e.g., `gap-6`, `p-6`) used uniformly across unrelated sections.
**Why:** No spatial rhythm — everything feels equidistant and flat.
**Fix:** Use tight spacing (4–8px) for related items, generous spacing (32–64px) between sections. Create contrast.

#### D3 · Copy-paste hero-metric-features layout
**Detect:** The page follows: hero section → stats/metrics row → 3-column feature grid → CTA. Repeated with different colors.
**Why:** Every AI generator outputs this exact template.
**Fix:** Break the template. Lead with the product, use asymmetric layouts, eliminate the stats strip if the numbers aren't real.

#### D4 · Line length too long
**Detect:** Text containers without `max-width` or with `max-width > 75ch` for body paragraphs.
**Why:** Lines wider than ~80 characters are hard to track back to the next line.
**Fix:** Add `max-width: 65ch` to `max-width: 75ch` on text containers.

#### D5 · Content overflow
**Detect:** `white-space: nowrap` on text without `overflow: hidden` + `text-overflow: ellipsis`, or containers with `overflow: visible` holding content wider than the parent.
**Why:** Content spills out of its box, creating horizontal scrollbars.
**Fix:** Let text wrap, constrain widths, or add deliberate truncation with ellipsis.

---

### E. Motion

#### E1 · Bounce / elastic easing
**Detect:** CSS `cubic-bezier` with negative values or values > 1 (e.g., `cubic-bezier(0.68, -0.55, 0.27, 1.55)`), or keywords `bounce`, `elastic`, `spring` in animation names/libraries.
**Why:** Spring physics on UI chrome (dialogs, cards) feels tacky.
**Fix:** Use smooth ease-out curves: `cubic-bezier(0.16, 1, 0.3, 1)` (ease-out-expo) or similar.

#### E2 · Layout property animation
**Detect:** `transition` or `animation` applied to `width`, `height`, `padding`, `margin`, `top`, `left`.
**Why:** Animating layout properties causes reflow jank.
**Fix:** Use `transform` (scale, translate) and `opacity`. For height, use `grid-template-rows: 0fr → 1fr`.

#### E3 · Image hover transform (opt-in)
**Detect:** `hover:scale-*`, `:hover { transform: scale() }` on `<img>` or image containers.
**Why:** Scaling images on hover is a recurring AI-generated interaction pattern.
**Fix:** Remove the hover transform. If interaction feedback is needed, use a subtle overlay or border change.

---

### F. Copy

#### F1 · Em-dash overuse
**Detect:** ≥ 3 em-dashes (`—` or `&mdash;`) in a single block of body copy.
**Why:** Frequent em-dashes are an AI cadence tell.
**Fix:** Replace with commas, colons, periods, or parentheses.

#### F2 · Marketing buzzwords
**Detect:** Phrases: "supercharge", "streamline", "empower", "world-class", "enterprise-grade", "next-generation", "seamlessly", "unlock", "revolutionize", "cutting-edge", "game-changing".
**Why:** Generic SaaS filler — instant AI tell.
**Fix:** Replace with a specific verb + noun that describes what the product literally does.

#### F3 · Aphoristic-cadence copy
**Detect:** ≥ 2 instances of the pattern: short declarative sentence, then a rebuttal/contrast ("Not X. Y." / "Less noise. More signal.").
**Why:** Manufactured-contrast aphorisms are AI cadence, not voice.
**Fix:** Write naturally. One instance is fine; the repeated pattern is the tell.

#### F4 · Redundant UX writing
**Detect:** A label, sublabel, helper text, and/or placeholder all saying the same thing on one form field.
**Why:** Multiple layers of copy restating the same information is AI over-explaining.
**Fix:** Say it once. Label is usually enough; add helper text only when it provides new information.

---

### G. General Quality

#### G1 · Broken / placeholder images
**Detect:** `<img>` with empty `src`, `src="placeholder"`, `src="#"`, `src="https://via.placeholder.com"`, or `/api/placeholder/`.
**Why:** Placeholder images ship as broken boxes.
**Fix:** Use real images, generate actual assets, or remove the `<img>` tag entirely.

#### G2 · Low contrast text
**Detect:** Text color and background color with contrast ratio < 4.5:1 (body) or < 3:1 (large text, ≥ 18px bold or ≥ 24px regular).
**Why:** Fails WCAG AA — unreadable for many users.
**Fix:** Darken the text or lighten the background until ratio ≥ 4.5:1.

#### G3 · Tight line height
**Detect:** `line-height < 1.3` on multi-line body text.
**Why:** Crammed lines are hard to track.
**Fix:** Set `line-height: 1.5` to `1.7` for body text.

#### G4 · Tiny body text
**Detect:** Body `font-size < 14px` (not labels, captions, or footnotes).
**Why:** Below 14px body text strains reading, especially on high-DPI screens.
**Fix:** Use ≥ 14px for body; 16px is ideal.

#### G5 · Skipped heading level
**Detect:** `<h1>` followed by `<h3>` (no `<h2>`), or similar gaps.
**Why:** Breaks the document outline for screen readers.
**Fix:** Use sequential heading levels. Style visually with classes, not by picking a different heading tag.

#### G6 · Cramped padding
**Detect:** Bordered or colored containers with padding < 8px.
**Why:** Text crushed against edges looks broken.
**Fix:** Use ≥ 12px padding inside bordered containers; 16px is ideal.

#### G7 · Justified text
**Detect:** `text-align: justify` without `hyphens: auto`.
**Why:** Creates uneven word spacing ("rivers of white") on screens.
**Fix:** Use `text-align: left` for body text.

#### G8 · Wide letter spacing on body text
**Detect:** `letter-spacing > 0.05em` on body paragraphs (not uppercase labels).
**Why:** Disrupts natural character groupings and slows reading.
**Fix:** Remove letter-spacing from body text. Reserve wide tracking for short uppercase labels.

---

## Severity Classification

| Level | Criteria |
|---|---|
| **Critical** | Accessibility failure (G2, G5), broken images (G1), unreadable text (G3, G4, G6) |
| **Warning** | Strong AI tell visible to trained eyes (A1, A2, B2, B3, C1, C2, C3, D1, F2) |
| **Info** | Stylistic preference or opt-in pattern (A3, A4, B8, C5, E3, F1) |

---

## Example Report

```
File:Line         | Rule | Finding                              | Fix
------------------|------|--------------------------------------|--------------------------------------
src/Card.tsx:12   | A1   | border-l-4 border-indigo-500         | Remove border-l-4, add top-2 neutral
src/Hero.tsx:8    | C3   | bg-gradient-to-r bg-clip-text         | Replace with solid text-gray-900
src/Hero.tsx:5    | B3   | Pill chip "✨ Introducing"            | Remove or fold into headline
src/page.tsx:44   | D1   | 6 identical feature cards in grid    | Vary sizes, highlight lead card
src/globals.css:3 | B9   | Only Inter loaded                    | Add display font pairing
```

---

## Non-Goals

- This skill does not install or invoke any external tool, extension, or package.
- It does not open a browser or run Puppeteer.
- It works solely by reading and editing source files.
- It intentionally does not flag patterns that require runtime layout measurement (e.g., computed overflow). For those, recommend the user run a browser-based tool.
