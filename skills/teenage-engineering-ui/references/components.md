# Component Recipes

Working HTML/CSS for the Teenage Engineering kit. Every recipe assumes the
tokens from `design-tokens.md` (or `assets/te-tokens.css`) are loaded as CSS
custom properties. Keep radii, shadows, and label styling identical across all
components — that consistency is what makes the parts read as one device.

## Table of contents
- [Enclosure / device frame](#enclosure--device-frame)
- [Corner screw](#corner-screw)
- [Module / panel](#module--panel)
- [Label (with leading dot)](#label-with-leading-dot)
- [Knob](#knob)
- [Buttons](#buttons)
- [Mode selector (segmented chips)](#mode-selector-segmented-chips)
- [Toggle switch](#toggle-switch)
- [LED indicator](#led-indicator)
- [Input field](#input-field)
- [Display screen (LCD / CRT)](#display-screen-lcd--crt)
- [Dot-matrix grid](#dot-matrix-grid)
- [Status bar](#status-bar)

---

## Enclosure / device frame

The container that sells everything. Build it first.

```html
<div class="te-device">
  <header class="te-header">
    <div class="te-wordmark">AETHER·1 <span>NEURAL TERMINAL</span></div>
    <div class="te-header-right">
      <span class="te-micro">SN 47-Δ</span>
      <span class="te-led-label"><i class="te-led on"></i> PWR</span>
    </div>
  </header>
  <!-- modules go here -->
</div>
```
```css
.te-device {
  position: relative;
  padding: var(--sp-5);
  background: linear-gradient(180deg, var(--panel-2), var(--enclosure));
  border-radius: var(--r-enclosure);
  border: 1px solid var(--seam);
  box-shadow:
    0 1px 0 var(--hi) inset,
    0 2px 1px var(--sh-soft),
    0 24px 48px -12px var(--sh);
}
.te-header { display:flex; align-items:center; justify-content:space-between; margin-bottom: var(--sp-5); }
.te-wordmark { font-family: var(--font-display); font-weight:700; font-size: var(--fs-wordmark);
  letter-spacing:.14em; text-transform:uppercase; color: var(--text); }
.te-wordmark span { color: var(--text-3); font-size: var(--fs-label); letter-spacing:.2em; margin-left: var(--sp-2); }
.te-header-right { display:flex; align-items:center; gap: var(--sp-4); }
.te-micro { font-family: var(--font-mono); font-size: var(--fs-micro); letter-spacing:.12em; color: var(--text-3); }
.te-led-label { display:flex; align-items:center; gap: var(--sp-2);
  font-family: var(--font-mono); font-size: var(--fs-micro); letter-spacing:.12em; color: var(--text-2); }
```
Add corner screws by placing four `.te-screw` elements absolutely in the device
corners (see next recipe).

## Corner screw

```css
.te-screw {
  position: absolute; width: var(--screw); height: var(--screw); border-radius:50%;
  background: radial-gradient(circle at 35% 30%, var(--panel-2), var(--inset));
  box-shadow: 0 1px 1px var(--hi), 0 1px 2px var(--sh) inset;
  border: 1px solid var(--seam);
}
.te-screw::after { /* slot */
  content:""; position:absolute; inset:0; margin:auto; width:60%; height:1.5px;
  background: var(--sh); border-radius:1px; transform: rotate(-35deg);
}
/* place: top:10px/left:10px, top:10px/right:10px, bottom:10px/left:10px, bottom:10px/right:10px */
```

## Module / panel

A labeled sub-surface grouping related controls.

```html
<section class="te-module">
  <div class="te-label"><i class="te-dot" style="background:var(--dot-teal)"></i> SYSTEM</div>
  <!-- controls -->
</section>
```
```css
.te-module {
  background: var(--panel);
  border-radius: var(--r-module);
  border: 1px solid var(--seam);
  padding: var(--sp-4);
  box-shadow: 0 1px 0 var(--hi) inset, 0 6px 14px var(--sh-soft);
}
```

## Label (with leading dot)

```css
.te-label { font-family: var(--font-mono); font-size: var(--fs-label); font-weight:700;
  letter-spacing:.14em; text-transform:uppercase; color: var(--text-3);
  display:flex; align-items:center; gap: var(--sp-2); margin-bottom: var(--sp-3); }
.te-dot { width:8px; height:8px; border-radius:50%; flex:none; }
```

## Knob

Rotary control with indicator notch and a ring of tick marks. The ticks are a
repeating conic gradient masked to a ring; the notch is a pseudo-element.

```html
<div class="te-knob-wrap">
  <div class="te-knob" style="--angle: -30deg"></div>
  <div class="te-label" style="justify-content:center">TURN TO SET</div>
</div>
```
```css
.te-knob {
  --angle: 0deg;
  position: relative; width: var(--knob); height: var(--knob); margin: 0 auto;
  border-radius: 50%;
  background:
    radial-gradient(circle at 50% 35%, var(--panel-2), var(--panel) 60%, var(--inset));
  border: 1px solid var(--seam);
  box-shadow: 0 1px 0 var(--hi) inset, 0 4px 10px var(--sh), 0 1px 2px var(--sh) inset;
}
/* tick ring */
.te-knob::before {
  content:""; position:absolute; inset:-9px; border-radius:50%;
  background: repeating-conic-gradient(var(--text-3) 0 1.2deg, transparent 1.2deg 12deg);
  -webkit-mask: radial-gradient(farthest-side, transparent calc(100% - 7px), #000 calc(100% - 6px));
          mask: radial-gradient(farthest-side, transparent calc(100% - 7px), #000 calc(100% - 6px));
  opacity:.55;
}
/* indicator notch (accent), rotated by --angle */
.te-knob::after {
  content:""; position:absolute; left:50%; top:8px; width:3px; height:26%;
  background: var(--accent); border-radius:2px; transform-origin: 50% 100%;
  transform: translateX(-50%) rotate(var(--angle));
}
```

## Buttons

Neutral tactile button + the single accent primary.

```html
<button class="te-btn">PROGRAMMER</button>
<button class="te-btn te-btn--primary">SUBMIT</button>
```
```css
.te-btn {
  font-family: var(--font-display); font-weight:600; font-size: var(--fs-body);
  letter-spacing:.04em; color: var(--text);
  min-height: var(--touch-min); padding: 0 var(--sp-4);
  background: linear-gradient(180deg, var(--panel-2), var(--panel));
  border: 1px solid var(--seam); border-radius: var(--r-control); cursor:pointer;
  box-shadow: 0 1px 0 var(--hi) inset, 0 -1px 0 var(--sh-soft) inset,
              0 2px 4px var(--sh-soft), 0 6px 14px var(--sh);
  transition: transform .04s ease, box-shadow .08s ease;
}
.te-btn:active { transform: translateY(1px);
  box-shadow: 0 1px 2px var(--sh) inset, 0 2px 6px var(--sh-soft) inset; }
.te-btn--primary {
  color: var(--on-accent);
  background: linear-gradient(180deg, color-mix(in srgb, var(--accent) 88%, white), var(--accent));
  border-color: var(--accent-press);
  box-shadow: 0 1px 0 rgba(255,255,255,.35) inset,
              0 2px 6px color-mix(in srgb, var(--accent) 40%, transparent),
              0 8px 18px var(--sh);
}
.te-btn--primary:active { background: var(--accent-press); }
```

## Mode selector (segmented chips)

A row of chips; one active (accent). Each carries a small corner indicator dot.

```html
<div class="te-modes">
  <button class="te-chip is-active">Translator <i class="te-chip-dot"></i></button>
  <button class="te-chip">Programmer <i class="te-chip-dot"></i></button>
  <button class="te-chip">Email <i class="te-chip-dot"></i></button>
</div>
```
```css
.te-modes { display:flex; gap: var(--sp-2); }
.te-chip {
  position:relative; flex:1; min-height: var(--touch-min); padding: 0 var(--sp-3);
  font-family: var(--font-display); font-weight:600; font-size: var(--fs-body);
  color: var(--text-2); background: linear-gradient(180deg, var(--panel-2), var(--panel));
  border:1px solid var(--seam); border-radius: var(--r-control); cursor:pointer;
  box-shadow: 0 1px 0 var(--hi) inset, 0 3px 8px var(--sh-soft);
}
.te-chip-dot { position:absolute; top:8px; right:8px; width:7px; height:7px; border-radius:50%;
  background: var(--text-3); box-shadow: 0 0 0 1px var(--seam) inset; }
.te-chip.is-active { color: var(--accent); border-color: color-mix(in srgb, var(--accent) 45%, var(--seam)); }
.te-chip.is-active .te-chip-dot { background: var(--accent); box-shadow: 0 0 6px var(--accent); }
```

## Toggle switch

```css
.te-switch { position:relative; width:52px; height:28px; border-radius: var(--r-pill);
  background: var(--inset); border:1px solid var(--seam);
  box-shadow: 0 2px 5px var(--sh) inset; cursor:pointer; }
.te-switch::after { content:""; position:absolute; top:2px; left:2px; width:22px; height:22px;
  border-radius:50%; background: linear-gradient(180deg, var(--panel-2), var(--panel));
  box-shadow: 0 1px 0 var(--hi) inset, 0 2px 4px var(--sh); transition: left .12s ease; }
.te-switch.is-on { background: color-mix(in srgb, var(--accent) 28%, var(--inset)); }
.te-switch.is-on::after { left:28px; }
```

## LED indicator

```css
.te-led { width: var(--led); height: var(--led); border-radius:50%; flex:none;
  background: var(--text-3); box-shadow: 0 0 0 1px var(--seam) inset; }
.te-led.on { background: var(--dot-green); box-shadow: 0 0 7px var(--dot-green); }
.te-led.warn { background: var(--accent); box-shadow: 0 0 7px var(--accent); }
```

## Input field

Recessed well with monospace placeholder.

```css
.te-field {
  width:100%; font-family: var(--font-mono); font-size: var(--fs-body); color: var(--text);
  padding: var(--sp-3) var(--sp-4); background: var(--inset);
  border:1px solid var(--seam); border-radius: var(--r-control);
  box-shadow: 0 2px 5px var(--sh) inset, 0 -1px 0 var(--hi) inset; outline:none;
}
.te-field::placeholder { color: var(--text-3); }
.te-field:focus { border-color: color-mix(in srgb, var(--accent) 50%, var(--seam)); }
/* password dots: use letter-spacing on a text input showing • characters, or type=password */
```

## Display screen (LCD / CRT)

Always recessed, with faint scanlines and (for CRT) phosphor glow.

```html
<div class="te-screen te-screen--lcd">
  <div class="te-screen-line"><span class="te-screen-tag">USER</span> &gt; Hello, I am a human.</div>
  <div class="te-screen-line"><span class="te-screen-tag">ASSISTANT</span> Greetings.</div>
</div>
```
```css
.te-screen {
  position:relative; overflow:hidden; padding: var(--sp-4);
  border-radius: var(--r-control); border:1px solid var(--seam);
  box-shadow: 0 3px 8px var(--sh) inset, 0 -1px 0 var(--hi) inset;
  font-family: var(--font-screen); line-height:1.5;
}
.te-screen--lcd { background: linear-gradient(180deg, var(--lcd-bg), var(--lcd-bg-2)); color: var(--lcd-fg); }
.te-screen--crt { background: var(--crt-bg); color: var(--crt-green);
  text-shadow: 0 0 6px var(--crt-green-glow); }
.te-screen::after { /* scanlines */
  content:""; position:absolute; inset:0; pointer-events:none;
  background: repeating-linear-gradient(0deg, rgba(0,0,0,.05) 0 1px, transparent 1px 3px);
}
.te-screen--crt::after { background: repeating-linear-gradient(0deg, rgba(0,0,0,.25) 0 1px, transparent 1px 3px); }
.te-screen-tag { display:block; font-size: var(--fs-micro); letter-spacing:.12em; opacity:.7; text-transform:uppercase; }
.te-screen-line { margin-bottom: var(--sp-3); }
```

## Dot-matrix grid

Decorative vent / LED grid for the chrome. Pure CSS via radial-gradient.

```css
.te-matrix { width:64px; height:36px; border-radius:4px;
  background-image: radial-gradient(var(--text-3) 1.1px, transparent 1.3px);
  background-size: 8px 8px; opacity:.5; }
```

## Status bar

Bottom strip of deadpan metadata.

```html
<footer class="te-status">
  <span>MODEL: GPT-X</span><span>MODE: TRANSLATOR</span><span>CH 01 · 38400 BAUD</span>
</footer>
```
```css
.te-status { display:flex; justify-content:space-between; gap: var(--sp-4);
  margin-top: var(--sp-4); padding-top: var(--sp-3); border-top:1px solid var(--seam);
  font-family: var(--font-mono); font-size: var(--fs-micro); letter-spacing:.12em; color: var(--text-3); }
```
