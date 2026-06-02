# Design Tokens

Authoritative values for the Teenage Engineering aesthetic. Copy these rather
than improvising — coherence across every control is what makes the look read as
a single manufactured object. `assets/te-tokens.css` is the same content as a
drop-in stylesheet.

## Table of contents
- [Fonts & imports](#fonts--imports)
- [Bone theme (default, light)](#bone-theme-default-light)
- [Graphite theme (dark)](#graphite-theme-dark)
- [Accents (pick ONE hero)](#accents-pick-one-hero)
- [Function dots (coded system)](#function-dots-coded-system)
- [Display / screen palettes](#display--screen-palettes)
- [Typography scale](#typography-scale)
- [Spacing, radius, sizing](#spacing-radius-sizing)
- [Depth recipes (shadows)](#depth-recipes-shadows)

## Fonts & imports

Geometric grotesque for labels/headings, monospace for data, optional
pixel/segment for displays. All available on Google Fonts:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Space+Mono:wght@400;700&family=JetBrains+Mono:wght@400;500;700&family=VT323&display=swap" rel="stylesheet">
```

Stacks:
```
--font-display: "Space Grotesk", "Archivo", "Helvetica Neue", system-ui, sans-serif;
--font-mono:    "Space Mono", "JetBrains Mono", ui-monospace, "SF Mono", Menlo, monospace;
--font-screen:  "VT323", "Space Mono", ui-monospace, monospace; /* displays */
```
For true 7-segment numerals, use the open-source **DSEG** family (self-host) and
set it as `--font-screen`.

## Bone theme (default, light)

Warm off-white "bone" plastic. The TE/Braun default.

```
--bg:            #D9D6CB;  /* deep backdrop behind the device */
--enclosure:     #E7E4DA;  /* outer device shell */
--panel:         #EDEBE2;  /* raised module surface */
--panel-2:       #F3F1EA;  /* lightest raised element */
--inset:         #DAD7CC;  /* recessed surface (fields, screens wells) */
--seam:          rgba(40, 36, 28, 0.10);   /* 1px hairline borders */
--text:          #2B2A26;  /* primary text */
--text-2:        #6F6C63;  /* secondary text */
--text-3:        #9C9991;  /* labels, captions, placeholders */
--hi:            rgba(255, 255, 255, 0.90); /* top highlight in shadows */
--sh:            rgba(76, 70, 54, 0.22);    /* bottom drop shadow */
--sh-soft:       rgba(76, 70, 54, 0.12);
```

## Graphite theme (dark)

Warm charcoal. Use the same token names so components are theme-agnostic.

```
--bg:            #161614;
--enclosure:     #232220;
--panel:         #2B2A28;
--panel-2:       #343230;
--inset:         #1B1A18;
--seam:          rgba(0, 0, 0, 0.45);
--text:          #ECE9E0;
--text-2:        #A8A49B;
--text-3:        #6E6B63;
--hi:            rgba(255, 255, 255, 0.06);
--sh:            rgba(0, 0, 0, 0.55);
--sh-soft:       rgba(0, 0, 0, 0.35);
```

## Accents (pick ONE hero)

Choose a single hero accent per project. Use it for the primary action, the
active state, and key indicators — nowhere else.

```
--accent-orange: #FF5A00;  /* the canonical TE accent — default */
--accent-red:    #E8412B;
--accent-yellow: #F5A623;  /* "signal yellow" */
--accent-lime:   #B5D000;
```
Set the chosen one to `--accent`, and define a pressed/darker variant:
```
--accent:        #FF5A00;
--accent-press:  #E04E00;  /* ~8% darker for active/pressed */
--on-accent:     #1A1206;  /* text/icon ON an accent surface (near-black) */
```

## Function dots (coded system)

Small status/category dots are allowed as a *coded* system — distinct from the
hero accent and never used for large fills. Keep them ~7–9px.

```
--dot-red:   #E8412B;
--dot-amber: #F5A623;
--dot-green: #46B45A;
--dot-teal:  #29A99A;
--dot-blue:  #2D6CDF;
--dot-pink:  #DD5C93;
```

## Display / screen palettes

Screens are always **recessed** into the panel. Two idioms:

**Sage LCD** (dark text on green glass — like a backlit reflective LCD):
```
--lcd-bg:    #B6C29C;
--lcd-bg-2:  #AEBB92;  /* for a faint vertical gradient */
--lcd-fg:    #36402B;  /* primary text */
--lcd-fg-2:  #5C6B49;  /* dim text / labels */
--lcd-glow:  rgba(54, 64, 43, 0.25);
```

**CRT phosphor** (bright text on near-black, with glow):
```
--crt-bg:    #0C140C;
--crt-green: #5BF870;  --crt-green-glow: rgba(91, 248, 112, 0.55);
--crt-amber: #FFB000;  --crt-amber-glow: rgba(255, 176, 0, 0.50);
```

## Typography scale

Use sparingly — instruments have few type sizes.

```
--fs-screen:  22px;  /* display readout (VT323 reads small, size up) */
--fs-body:    15px;  /* user/assistant content, field text */
--fs-wordmark:18px;  /* product name */
--fs-label:   11px;  /* UPPERCASE section/control labels */
--fs-micro:   10px;  /* serials, units, status-bar metadata */
```

Label rule (apply to every caption/section/control name):
```css
.te-label {
  font-family: var(--font-mono);
  font-size: var(--fs-label);
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--text-3);
}
```
Wordmark: `--font-display`, weight 700, `letter-spacing: 0.14em`, uppercase.
Numbers/data/metadata: `--font-mono`. Body content inside screens:
`--font-screen` or `--font-mono`.

## Spacing, radius, sizing

4px base grid. Be generous; instruments breathe.
```
--sp-1: 4px;  --sp-2: 8px;  --sp-3: 12px; --sp-4: 16px;
--sp-5: 24px; --sp-6: 32px; --sp-7: 48px; --sp-8: 64px;

--r-enclosure: 24px;
--r-module:    14px;
--r-control:   10px;   /* buttons, fields */
--r-pill:      999px;  /* mode chips, switches */

--screw:       12px;   /* corner screw diameter */
--led:         9px;    /* indicator LED diameter */
--knob:        92px;   /* default knob diameter */
--touch-min:   44px;   /* minimum interactive height */
```

## Depth recipes (shadows)

Crisp, not mushy. The signature is **top highlight + bottom drop + 1px seam**,
with recessed elements inverting it via `inset`. Copy verbatim.

**Raised element** (modules, buttons at rest):
```css
box-shadow:
  0 1px 0 var(--hi) inset,            /* crisp top sheen */
  0 -1px 0 var(--sh-soft) inset,      /* faint bottom lip */
  0 2px 4px var(--sh-soft),
  0 6px 14px var(--sh);
border: 1px solid var(--seam);
```

**Pressed / active** (button down, active chip):
```css
box-shadow:
  0 1px 2px var(--sh) inset,
  0 2px 6px var(--sh-soft) inset;
transform: translateY(1px);
```

**Recessed well** (input fields, screen wells, knob seat):
```css
box-shadow:
  0 2px 5px var(--sh) inset,
  0 -1px 0 var(--hi) inset;
border: 1px solid var(--seam);
```

**Enclosure** (the whole device, sitting on `--bg`):
```css
box-shadow:
  0 1px 0 var(--hi) inset,
  0 2px 1px var(--sh-soft),
  0 24px 48px -12px var(--sh);
border: 1px solid var(--seam);
```

**Phosphor glow** (screen text): `text-shadow: 0 0 6px var(--crt-green-glow);`
