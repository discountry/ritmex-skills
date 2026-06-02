# Self-Review Checklist

Run through this before delivering. The four most common failures are at the
top. If any "must" fails, fix it before shipping.

## Must-pass (the four killers)

- [ ] **One accent only.** Exactly one hero accent color appears, and only on
  the primary action + active state + a few key indicators. If a second
  saturated color is doing decorative work, remove it. (Coded function dots are
  the one exception, kept small.)
- [ ] **Everything is labeled.** Each section and control has an uppercase
  monospace label. No bare controls, no icon-only mystery buttons.
- [ ] **Depth is crisp, not mushy.** Each raised/recessed element uses the
  top-highlight + bottom-drop + 1px seam recipe. No giant uniform blurs that
  make everything look like soap. Recessed wells actually look inset.
- [ ] **It's framed as a device.** There is an enclosure with a bezel, a
  wordmark + product line, and at least a couple pieces of chrome (corner
  screws, serial number, power LED, status bar). It does not look like a plain
  card floating on a web page.

## Color & material

- [ ] Neutral base is warm (bone or graphite), not pure white/black/cool grey.
- [ ] No gloss, no chrome reflections, no leather/wood/metal photo textures.
- [ ] Accent has a darker pressed variant; text on accent is near-black, legible.

## Typography

- [ ] Labels are UPPERCASE, monospace, ~10–12px, letter-spaced (~0.12–0.18em).
- [ ] Few type sizes overall (an instrument has 3–5, not 10).
- [ ] Data, serials, units, and screen text are monospace.
- [ ] Wordmark is the geometric grotesque, uppercase, letter-spaced.

## Layout & geometry

- [ ] Aligned to a 4px grid; gutters are even and generous.
- [ ] Controls are grouped into labeled modules with visible seams between them.
- [ ] Radii are consistent per tier (enclosure > module > control); knobs and
  LEDs are perfect circles.
- [ ] Interactive targets are ≥ 44px tall.

## Controls

- [ ] Knobs have an indicator notch and a tick ring (they look turnable).
- [ ] Buttons depress on `:active` (translate + inset shadow).
- [ ] The active mode chip is clearly distinguished by the accent.
- [ ] Inputs are recessed wells with monospace placeholder text.

## Displays

- [ ] Screens are recessed into the panel, not raised.
- [ ] LCD = dark text on sage green; CRT = phosphor text on near-black with glow.
- [ ] Faint scanlines present; glow is subtle, not a blur bomb.

## The wink

- [ ] At least 2–3 pieces of deadpan technical fiction (SN, BAUD/CH, version,
  PWR, a dot-matrix vent). Dry, not jokey, never breaking the functionalist
  tone.

## Accessibility sanity (don't skip)

- [ ] Body and label text meet contrast against their surface (the warm-neutral
  palette is forgiving, but verify accent-on-panel and text-3 captions).
- [ ] State is never conveyed by color alone — the active chip also changes via
  the indicator dot / border, not just hue.
- [ ] Focus styles exist for keyboard users (the accent border on `:focus`).
- [ ] Decorative chrome (screws, matrix, inert dots) is `aria-hidden`.

## Common mistakes → fixes

- *"Looks like soft mushy neumorphism."* → Add the 1px seams, sharpen the
  highlight, introduce the accent, add chrome and labels.
- *"Looks like a flat dashboard."* → You skipped the enclosure. Frame the device
  first; add depth recipes and chrome.
- *"Too busy / toy-like."* → Too many accents or too much fiction. Cut to one
  accent; make the metadata dry and sparse.
- *"Sterile / lifeless."* → Missing the wink and the warm neutral. Warm the base,
  add a serial number and status bar.
