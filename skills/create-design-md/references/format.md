# DESIGN.md Format Reference

The file has two halves: **YAML frontmatter** (the machine-readable token system, consumed by `@google/design.md` lint/export) and a **Markdown body** (the human-readable explanation). The linter validates the frontmatter; the body is convention — but the convention is what makes the file useful, so follow it.

## Frontmatter schema

```yaml
---
version: alpha
name: <project-name>-design            # kebab-case identifier
description: >-
  One dense paragraph summarizing the design language: the surface strategy
  (light/dark, canvas colors), the primary color and how it's deployed, the
  typographic voice (family, weights, tracking), the shape language, and the
  one or two signature elements that make the system recognizable.

colors:
  # Flat map of kebab-case token → hex string (quoted).
  primary: "#533afd"          # THE interactive/brand color — the token MUST
                              # be named exactly `primary`; the linter warns
                              # when no `primary` key exists
  on-primary: "#ffffff"       # text on primary fills
  ink: "#0d253d"              # default body text
  ink-mute: "#64748d"         # secondary/helper text
  canvas: "#ffffff"           # default page background
  canvas-soft: "#f6f9fc"      # tinted alternate surface
  hairline: "#e3e8ee"         # 1px borders
  # + semantic colors (success/warning/error) when the system has them,
  # + accent colors only when evidence shows they are systematic.

typography:
  # Map of role → spec. Role names describe function: display-*, heading-*,
  # body-*, button-*, caption, micro, mono/code when relevant.
  display-xl:
    fontFamily: "Inter, system-ui, -apple-system, sans-serif"
    fontSize: 48px
    fontWeight: 600
    lineHeight: 1.1          # unitless ratio or px, either lints
    letterSpacing: -0.96px
    fontFeature: ss01        # optional; OpenType features like tnum, ss01
  body-md:
    fontFamily: "Inter, system-ui, -apple-system, sans-serif"
    fontSize: 15px
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: 0

rounded:
  xs: 4px
  sm: 6px
  md: 8px
  lg: 12px
  pill: 9999px

spacing:
  xs: 4px
  sm: 8px
  md: 12px
  lg: 16px
  xl: 24px
  xxl: 32px

components:
  # Map of kebab-case component → spec. Every field that has a matching
  # token category MUST use a {reference}, never a raw value.
  # Recognized sub-tokens (anything else triggers a lint warning):
  #   backgroundColor, textColor, typography, rounded, padding,
  #   size, height, width
  # There is NO border field — describe borders in the body prose.
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button-md}"
    rounded: "{rounded.pill}"
    padding: 8px 16px        # padding is literal: "V H" or "T R B L"
---
```

### Token reference syntax

`{<category>.<token-name>}` — e.g. `{colors.primary}`, `{typography.body-md}`, `{rounded.pill}`. The linter resolves references and errors on any that point at a missing token. Use the same syntax inside body prose so text stays tied to the actual tokens.

### Component naming

`<type>-<variant>[-<state>]`: `button-primary`, `button-primary-pressed`, `text-input`, `text-input-focused`, `card-feature`, `nav-bar`, `pill-tag`, `footer`. States are separate component entries, not nested fields.

### What the linter checks

`npx -y @google/design.md lint DESIGN.md` reports JSON findings:

- **errors** — malformed YAML, missing required fields, unresolvable `{references}`. Must be zero.
- **warnings** — no color named `primary`; unrecognized component sub-tokens; text/background pairs in a component below WCAG AA 4.5:1 contrast; tokens never referenced by any component. Resolve deliberately (fix, or justify in Known Gaps).
- **info** — token counts; a sanity check that all categories parsed.

Border/hairline color tokens will always warn as "never referenced" because the component schema has no border field — keep them (borders are real), document their use in body prose, and note the expected warning in Known Gaps.

Export is the machine-consumption path and doubles as a smoke test:

```bash
npx -y @google/design.md export DESIGN.md --format css-tailwind   # Tailwind v4 @theme
npx -y @google/design.md export DESIGN.md --format dtcg           # W3C Design Tokens
```

## Body section template

Use exactly these `##` sections, in this order. Reference tokens inline with `{...}` syntax throughout.

```markdown
## Overview
Two to four paragraphs: how the system reads at a glance, how color is
deployed (which color does what job), the typographic voice, the depth
medium (shadows vs borders vs color). End with:

**Key Characteristics:**
- 5–8 bullets, each naming one signature move with its tokens.

## Colors
Subsections as the palette warrants: `### Brand & Accent`, `### Surface`,
`### Text`, `### Semantic`. One bullet per token: **Name** (`{colors.x}` —
`#hex`): what it is for and where it appears. If there is no semantic
palette, say so explicitly rather than omitting the subsection.

## Typography
`### Font Family` — the stack, weights used, licensing note if the font is
proprietary, and a named open-source substitute with the settings needed to
approximate it.
`### Hierarchy` — a table: Token | Size | Weight | Line Height | Letter
Spacing | Use.
`### Principles` — 3–5 rules about how type behaves in this system.

## Layout
`### Spacing System` — base unit and the token scale.
`### Grid & Container` — max-widths, column behavior.
`### Whitespace Philosophy` — how dense or airy, and where density changes.

## Elevation & Depth
A table of levels (0–3) with the exact `box-shadow` values and their uses.
Note the system's real depth medium — many systems use borders or color
instead of shadows; say which.

## Shapes
`### Border Radius Scale` — table: Token | Value | Use.
Plus any geometry rules for images/media.

## Components
Subsections: `### Buttons`, `### Cards & Containers`, `### Inputs & Forms`,
`### Navigation`, `### Pills, Tags, and Chips`, `### Signature Components`.
For each component: bold name, then bullets giving background, text color,
typography, padding, radius — all as `{token}` references — plus state
behavior. Signature Components documents the elements unique to this system
(a gradient treatment, a particular composite, a texture).

## Do's and Don'ts
`### Do` / `### Don't` — 5–7 bullets each, every one specific to this
system and citing tokens. A bullet that could appear in any design doc
does not belong here.

## Responsive Behavior
`### Breakpoints` — table: Name | Width | Key Changes.
`### Touch Targets` — minimum sizes.
`### Collapsing Strategy` — how grids, type, and nav degrade.

## Iteration Guide
Numbered rules for whoever edits UI against this file: change one component
at a time, reference tokens not raw values, run the linter after edits,
which token is the default body style, which rules are non-negotiable.

## Known Gaps
Honest list of what the evidence did not cover: assumed values, missing
states (hover/disabled/dark mode), tokens estimated from screenshots,
contrast issues faithfully documented from the source. Omit the section
only when there are genuinely no gaps.
```

## Calibration

A finished file runs 250–500 lines total. Under 200 lines usually means components or body sections are too thin; over 600 usually means the token set is bloated or the prose is padded. The `resources/design-md/` gallery shows the target density — `stripe/DESIGN.md` (light, marketing-led) and `linear.app/DESIGN.md` (dark, product-led) are good anchors.
