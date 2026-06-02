---
name: teenage-engineering-ui
description: >-
  Teenage Engineering / Dieter Rams functionalist-hardware aesthetic: neutral
  molded panels, a single bold accent color, tactile knobs and buttons, LED and
  segmented displays, uppercase monospace labels, visible "device chrome"
  (screws, bezels, serial numbers, power LEDs), and playful retro-futurist
  technical detailing. Triggers: "TE style", "OP-1 style", "Pocket Operator
  look", "Braun / Dieter Rams style", "functionalist hardware UI", "retro
  hardware / synth / audio-gear interface", "device-like UI", "tactile /
  physical interface", "minimal skeuomorphic panels", or descriptions involving
  cream/charcoal panels, knobs, screws, LED dots, a single accent, monospace
  labels, phosphor/LCD screens, or anything that should look like hardware.
---

# Teenage Engineering UI

Interfaces that look like beautifully made physical instruments — in the lineage
of Braun under Dieter Rams, carried forward by Teenage Engineering (OP-1, OP-Z,
Pocket Operators, TX-6). **Functionalism with a wink**: rigorously minimal and
honest about function, warmed up with one confident accent color and a few pieces
of playful technical fiction.

NOT generic neumorphism, not leather-and-wood skeuomorphism, not flat material
design. Tokens and component recipes are in `references/`.

## What it is / is NOT

| It IS | It is NOT |
| --- | --- |
| Neutral base (bone/cream OR graphite) + **one** saturated accent | Rainbow gradients; multiple competing accents |
| Molded-plastic / brushed-metal tactility, subtle and crisp | Mushy all-over neumorphism with no crisp edges |
| Everything labeled in uppercase monospace | Decorative labels, lorem ipsum, vague icons-only UI |
| Visible device chrome: screws, bezels, serials, LEDs | A floating card on a blank web page |
| Honest controls (a knob looks turnable, a button pressable) | Skeuomorphic leather, wood grain, glossy reflections |
| Tight modular grid, generous breathing room | Cramped or asymmetric ad-hoc layout |
| A wink of retro-futurist fiction (SN, BAUD, CH 01, v0.4) | Over-serious enterprise chrome with no personality |

## The six principles

1. **Less, but better.** Remove everything non-essential, then make what
   remains excellent. If an element has no function, it must earn its place as
   either structure (chrome) or a deliberate playful detail — never noise.
2. **Be honest.** Controls communicate their function through form. A knob has
   an indicator line and tick marks. A primary action is one big confident
   button. Recessed things look pressed-in; raised things look pressable.
3. **Label everything.** Real instruments are covered in small uppercase
   labels. Use them generously: section names, control names, units, modes.
   This is the single fastest way to read as "hardware."
4. **One accent, used sparingly.** Pick ONE bold color (TE orange `#FF5A00`, or
   red, or signal yellow). Use it for the single most important action, the
   active state, and a few status dots — and nowhere else. Restraint is what
   makes it pop. A small *coded* set of function dots (red/green/blue/amber) is
   allowed as a system, distinct from the hero accent.
5. **Build the device, not the page.** Frame the whole UI as a physical unit:
   an outer bezel/enclosure with corner screws, a product name, a serial
   number, a power/ready LED. Group controls into labeled modules with seams
   between them.
6. **Add a wink.** Sprinkle plausible technical fiction — `SN 47-Δ`,
   `CH 01 · 38400 BAUD`, `v0.4.2`, `PWR`, a dot-matrix grid that does nothing.
   This is the difference between sterile functionalism and the TE personality.
   Keep it dry and deadpan, never jokey.

## Visual system at a glance

Full values, both themes, and font imports are in
`references/design-tokens.md`. Quick orientation:

- **Two themes.** "Bone" (warm off-white panels, the default) and "Graphite"
  (warm charcoal). Pick one per project; don't mix.
- **Accent.** Exactly one hero accent. Default `#FF5A00`. Everything else is
  neutral.
- **Type.** Geometric grotesque for labels/headings (Space Grotesk / Archivo),
  monospace for data and small labels (Space Mono / JetBrains Mono), an optional
  pixel or 7-segment face (VT323 / DSEG) for displays. Labels are UPPERCASE with
  `letter-spacing: 0.12–0.18em`, ~10–12px, secondary color.
- **Depth.** Crisp not mushy: a soft top highlight + a soft bottom drop shadow +
  a 1px hairline seam. Recessed elements invert the shadow (inset). See the
  shadow recipes in the tokens file — copy them, don't improvise blur values.
- **Geometry.** 4px spacing grid. Soft-rounded rectangles: ~20–24px on the
  enclosure, ~12–16px on modules, ~8–10px on buttons/fields, full circles for
  knobs and LEDs. Pills are good for mode chips.
- **Displays.** Sage-green LCD (dark text on green) or dark CRT (green/amber
  phosphor on near-black), always recessed into the panel, with faint scanlines
  and a subtle phosphor glow.

## Component catalogue

Working HTML/CSS recipes for each are in `references/components.md`. The core
kit:

- **Enclosure / device frame** — outer bezel, corner screws, product wordmark,
  serial number, power LED.
- **Module / panel** — a labeled, slightly raised sub-surface grouping related
  controls, separated by seams.
- **Label** — uppercase mono caption, often with a small leading status dot.
- **Knob** — rotary control with an indicator notch and a ring of tick marks;
  optional caption "TURN TO SET".
- **Button** — neutral tactile button and the one accent primary button.
- **Mode selector** — a row of segmented chips with one active (accent) chip and
  small corner indicator dots.
- **Toggle / switch** — physical sliding switch.
- **LED indicator** — small glowing status dot (solid + soft halo).
- **Input field** — recessed text field with mono placeholder.
- **Display screen** — recessed LCD/CRT with phosphor text and scanlines.
- **Dot-matrix grid** — decorative ventilation/LED grid for the chrome.
- **Status bar** — bottom strip with deadpan metadata (model, mode, channel,
  baud).

## Build workflow

1. **Choose theme + accent.** Bone or Graphite; one accent.
2. **Load fonts + tokens.** Use `references/design-tokens.md` or drop in
   `assets/te-tokens.css`. Never hardcode hex values — use variables.
3. **Frame the device first.** Enclosure: bezel, corner screws, wordmark,
   serial number, power LED, dot-matrix vent. This sells the aesthetic.
4. **Lay modules on the grid.** Group controls into labeled modules. Even
   gutters, 4px grid.
5. **Drop in controls from the catalogue.** Consistent radii, shadows, labels.
6. **Add the wink.** Status bar, serials, channel/baud, version string, inert
   indicator dots. Deadpan, not jokey.
7. **Self-review** against `references/checklist.md`. Common failures: too many
   accents, missing labels, mushy depth, no device chrome.

## Starter template

`assets/starter-template.html` — a complete, self-contained working device
demonstrating the entire system (enclosure, knob, mode chips, LEDs, recessed
field, CRT screen, status bar). Use it as a starting point or read it to
calibrate the look before building fresh.

## Adapting to React / native

The aesthetic is carried by tokens and the chrome metaphor, not by any framework.
In React, expose tokens as CSS variables on a wrapper and build the catalogue
items as components. In native UI, translate the token tables directly. The
principles are the contract; the CSS is one implementation.
