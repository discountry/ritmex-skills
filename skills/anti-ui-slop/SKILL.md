---
name: anti-ui-slop
description: >
  Detect and fix AI-generated UI anti-patterns ("AI slop") in frontend code, and prevent
  them while writing new UI. Use whenever you are building or styling any UI, reviewing
  UI code, or when the user says "check for slop", "remove the AI look", "make it look
  human-designed", "why does this look AI-generated", or "polish the UI". Works on HTML,
  CSS, JSX/TSX, Vue, Svelte, and Tailwind by reading source files — no browser, no
  dependencies.
license: MIT
---

# Anti UI Slop

## The core insight — read this before any rule

AI-generated UIs are recognizable not because of any single CSS property, but because they **converge**. Every generator, asked for "a modern clean UI", reaches for the same defaults: the same fonts, the same purple gradient, the same icon-tile-above-heading card, the same hero→metrics→features template. In 2022 it was purple gradients and glassmorphism; in 2024 it was cream backgrounds and Instrument Serif italic heroes. **The specific tells change every year. The disease is constant: a reflex where a decision should be.**

This has two consequences that govern everything below:

1. **Deleting a tell is not a fix.** If you remove the purple gradient and reach for the next "safe" default, you have produced next year's slop. Every fix must substitute a *deliberate choice derived from this product's context* — its domain, brand, audience, content. Before editing anything, articulate (in one or two sentences) what this interface's design direction actually is. Then make every fix serve that direction.
2. **Slop rules are judgment calls; quality rules are not.** An italic serif headline is legitimate on an editorial magazine and a tell on a SaaS landing page — judge by context. But low contrast, broken images, and tiny text are objectively broken for every user, always. The two categories below are handled differently.

A reliable smell test for your own output: if you could swap this UI onto a different product and nothing would feel wrong, no decisions were made. Distinctive design is *specific* — it could only belong to this product.

## Workflow

1. **Establish direction.** Read enough of the project (copy, domain, existing brand tokens) to state what the design should feel like and why. One sentence is enough. Every fix will be checked against it.
2. **Scan.** Read the UI source files. Match against the rules below.
3. **Judge.** Quality violations are always findings. Slop tells are findings *unless the context genuinely earns the pattern* (e.g., numbered sections for actual sequential steps; blur for a real layering problem). When you exempt one, say why.
4. **Fix.** Rewrite the code. Apply the remedy as a deliberate choice, not the nearest alternative default. Prefer minimal, targeted edits.
5. **Report.** Output a table: `File:Line | Rule | Before → After`, grouped: Quality (must fix) first, then Slop.

When *writing* new UI rather than reviewing, invert this: establish direction first, then write code that never introduces the patterns below.

---

## Part 1 — Quality failures (objective, always fix)

These are not style opinions. Each one makes the interface harder to read or use.

| Rule | Detect | Fix |
|---|---|---|
| **Q1 Low contrast** | text/background contrast < 4.5:1 body, < 3:1 large text | Darken text or lighten background to WCAG AA |
| **Q2 Gray text on colored background** | `text-gray-*` / `#9ca3af`-like on a non-neutral surface | White/near-white, or a darker shade of the background hue. Gray washes out on color |
| **Q3 Tiny body text** | body `font-size < 14px` (labels/captions exempt) | ≥ 14px body, 16px ideal |
| **Q4 Tight line height** | `line-height < 1.3` on multi-line text | 1.5–1.7 for body |
| **Q5 Wide tracking on body** | `letter-spacing > 0.05em` on paragraphs | Remove. Reserve wide tracking for short uppercase labels |
| **Q6 All-caps body text** | `uppercase` on blocks > ~20 words | We read by word shape; caps destroy it. Sentence case for body, caps only for short labels |
| **Q7 Justified text** | `text-align: justify` without `hyphens: auto` | Left-align. Justification without hyphenation creates rivers of white |
| **Q8 Line length too long** | body text container without `max-width`, or > 75ch | `max-width: 65ch–75ch` |
| **Q9 Cramped padding** | bordered/colored container with padding < 8px | ≥ 12px inside bordered containers |
| **Q10 Skipped heading level** | `h1` → `h3` with no `h2`, etc. | Sequential levels; style with classes, not by picking a different tag |
| **Q11 Broken/placeholder image** | `<img>` with empty src, `#`, `via.placeholder.com`, `/api/placeholder/` | Real asset, generated asset, or remove the tag. Never ship a broken box |
| **Q12 Content overflow** | `white-space: nowrap` without truncation; children wider than parents | Wrap, constrain, or add deliberate ellipsis |
| **Q13 Layout-property animation** | `transition`/`animation` on width/height/padding/margin/top/left | Animate `transform` and `opacity`; `grid-template-rows: 0fr→1fr` for height |

## Part 2 — Slop tells (convergence signals, fix by making a decision)

For each tell: what to detect, and what *making a decision* looks like instead. "Remove X" is always shorthand for "remove X and let the deliberate design carry the weight."

### Surfaces & depth

- **S1 Side-tab accent border** — single-side border ≥ 3px on a card (`border-l-4`). The single most recognizable AI tell. Decision: if the accent encodes meaning (status, category), find a subtler carrier — a dot, a tinted background, an inline icon. If it encodes nothing, it goes.
- **S2 Thick border on rounded element** — `border ≥ 2px` colored + `border-radius ≥ 12px` together. They fight. Commit to one: a defined 1px edge, or rounding with no colored border.
- **S3 Hairline border + wide shadow** — `border: 1px` plus `box-shadow` blur ≥ 20px on the same element. Two elevation strategies at once. Commit to one: crisp edge *or* soft elevation.
- **S4 Glassmorphism as decoration** — `backdrop-filter: blur` / translucent white cards with no real layering problem to solve. Blur exists to keep context visible under an overlay; used on static cards it's a hackathon costume. Solid, opaque surfaces.
- **S5 Extreme border-radius** — ≥ 24px on cards/sections/inputs rounds everything into the same soft blob. Cards top out at 12–16px; full-pill is for tags and buttons only.
- **S6 Nested cards** — bordered/shadowed container inside another, 3+ levels. Flatten: spacing, typography, and dividers express grouping without stacking depth cues.
- **S7 Repeating-gradient stripes** — `repeating-linear-gradient` as surface texture. Plain surface, or a texture that comes from the brand.

### Typography

- **S8 Overused font** — Inter, Geist, Space Grotesk, Instrument Serif as primary face. These aren't bad fonts; they're *exhausted* — every generator reaches for them, so they read as "no one chose this." Decision: pick a face that expresses *this* product's character. Do not substitute from a memorized list of "good alternatives" — that list becomes the next convergence. Derive the choice from the product: what register (technical, warm, editorial, institutional)? Then find a face in that register.
- **S9 Single font for everything** — one family across the whole page. Pair a display face with a body face; the contrast between them is itself a design decision.
- **S10 Flat type hierarchy** — adjacent type steps < 1.25× apart. Fewer sizes, more contrast between them.
- **S11 Oversized hero headline** — a full sentence (≥ 8 words) at display size (≥ 48px). One or two punchy words at that size is fine; the tell is *long* copy blown up. Tighten the copy or shrink the type.
- **S12 Italic serif display hero** — italic serif ≥ 32px as the primary headline. Became the universal AI-startup hero overnight. Set it roman or use a non-serif display face. Exemption: genuinely editorial contexts — judge by what the product is.
- **S13 Crushed letter spacing** — tracking tighter than −0.05em. Tighten display type optically, to the point where characters still keep their shapes.
- **S14 Hero eyebrow chip** — tiny uppercase tracked label or ✨-pill above the hero headline. Default AI hero scaffolding. Fold it into the headline or cut it.
- **S15 Repeated section kickers** — 3+ sections each opening with a tracked uppercase mini-label. Structure should come from hierarchy and content, not a repeated scaffold.
- **S16 Numbered section markers** — display-size `01 / 02 / 03` as section décor. Numbers earn their place only when the content is actually a sequence.

### Color

- **S17 The AI palette** — purple/violet gradients (`#7c3aed`, `#8b5cf6` family) or cyan-on-dark as the primary accent. The most recognizable tell of all. Decision: derive the palette from the brand or domain. Purple is only wrong when it's a reflex; if it *is* the brand, keep it and make everything else prove the intentionality.
- **S18 Dark mode with glows** — dark background + colored `box-shadow`/`text-shadow` glow. Cyberpunk-by-default. Neutral, subtle shadows on dark surfaces, or no dark theme at all.
- **S19 Gradient text** — `bg-clip-text text-transparent`. Decoration wearing the costume of emphasis. Solid text colors, always.
- **S20 Cream/beige reflex** — warm off-white page background (`#faf7f2`, `bg-amber-50`) as the default "tasteful" surface. The 2024-era successor to the purple gradient: same reflex, different costume. Use it only if the palette around it proves it was chosen.

### Layout

- **S21 Identical card grids** — 4+ siblings with the same icon+heading+text anatomy in a uniform grid. The default AI homepage. Decision: does this content even want cards? Consider a table, an inline list, an accordion, or an asymmetric layout that ranks one item above the rest.
- **S22 Icon tile above heading** — small rounded-square icon container stacked over a heading inside a card. Every generator outputs this exact shape. Put icon and heading side by side, or drop the container and let the icon sit in flow.
- **S23 Massive icon containers** — icon tile larger than the text it introduces. When decoration outweighs the message, priorities are inverted. Shrink or remove.
- **S24 The hero→metrics→features template** — page reads: hero, stats strip, 3-col feature grid, CTA. Break the template: lead with the actual product, cut the stats strip if the numbers aren't real, vary section anatomy so each one is shaped by its content.
- **S25 Monotonous spacing** — one gap/padding value everywhere (`p-6 gap-6` on everything). Spacing is information: tight (4–8px) inside related groups, generous (48–96px) between sections. Uniform spacing says nothing is more related than anything else.

### Motion

- **S26 Bounce/elastic easing** — `cubic-bezier` with overshoot values, `bounce`/`elastic`/`spring` on UI chrome. Dialogs are not physical objects. `cubic-bezier(0.16, 1, 0.3, 1)` or similar ease-out.
- **S27 Animate-everything** — entrance animations, hover wiggles, floating badges on many elements at once. Motion is for meaning (state change, spatial continuity). Default to stillness; animate the one thing that matters.
- **S28 Image hover scale** — `hover:scale-*` on images. Let imagery sit still; if feedback is needed, a subtle overlay or border change.

### Copy

- **S29 Em-dash cadence** — 3+ em-dashes in one block of body copy. Commas, colons, periods.
- **S30 Aphorism cadence** — repeated "Not X. Y." / "Less noise. More signal." constructions. Once is voice; the pattern is the tell. Say plainly what the thing does.
- **S31 Buzzword filler** — "supercharge", "seamlessly", "unlock", "empower", "world-class", "next-generation", "game-changing". Replace with the specific verb and noun of what the product literally does.
- **S32 Redundant UX writing** — label + sublabel + helper + placeholder all restating one fact on a form field. Say it once. Helper text exists only to add new information.
- **S33 Hand-coded SVG illustrations** — inline SVG mascots/scenes drawn from path data. They read as doodles, not whimsy. Ship no illustration rather than a sketchy fallback.

### Structure

- **S34 Modal abuse** — complex multi-section settings crammed into a modal. If it scrolls and has columns, it deserves a page.

---

## After fixing: the convergence check

Before reporting, reread your own edits as if they were someone else's and ask:

- Did any fix just swap one default for another? (Inter → the same trendy alternative every time; purple → the same teal every time; cream → plain white with no palette at all)
- Could the result be swapped onto a different product without anything feeling wrong? If yes, the direction from step 1 wasn't applied — go back.
- Did fixing tells leave the page *blander* instead of more deliberate? Removing slop must be paired with adding intent: a real palette, a real type pairing, spacing rhythm, one section that's shaped unlike the others.

## Example report

```
DIRECTION: Internal logistics dashboard — dense, calm, utilitarian; data is the hero.

QUALITY (must fix)
src/Form.tsx:31    | Q2  | text-gray-400 on bg-blue-600     → text-blue-100
src/globals.css:12 | Q4  | line-height: 1.2 on body         → 1.55

SLOP
src/Card.tsx:12    | S1  | border-l-4 border-indigo-500     → status dot, neutral card edge
src/Hero.tsx:5     | S14 | "✨ Introducing" pill            → removed; headline carries it
src/page.tsx:44    | S21 | 6 identical feature cards        → comparison table (content is tabular)
src/globals.css:3  | S8  | Inter only                       → IBM Plex Sans + Plex Mono for figures
                          (chosen for the technical/ops register, tabular numerals)

EXEMPTED
src/Steps.tsx:9    | S16 | 01/02/03 markers kept — content is an actual 3-step sequence
```

## Non-goals

- No external tools, packages, browsers, or runtime measurement. Source-reading only.
- Patterns that need computed layout (true rendered overflow, real contrast of layered transparency) are flagged best-effort; recommend a browser-based check when certainty matters.
