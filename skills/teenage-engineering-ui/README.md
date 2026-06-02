# teenage-engineering-ui

Functionalist-hardware aesthetic for UI: neutral molded panels, one bold accent,
tactile knobs and buttons, LED/segment displays, uppercase monospace labels, and
visible "device chrome."

## Contents

```
teenage-engineering-ui/
├── SKILL.md                     # philosophy, principles, workflow
├── references/
│   ├── design-tokens.md         # full color/type/spacing/shadow values (2 themes)
│   ├── components.md            # working HTML/CSS recipes for every control
│   └── checklist.md             # pre-delivery self-review + common-mistake fixes
└── assets/
    ├── te-tokens.css            # drop-in CSS custom properties (bone + graphite)
    └── starter-template.html    # complete, self-contained working device
```

## Quick preview

Open `assets/starter-template.html` in a browser to see the target aesthetic.

## Notes
- No build step, no dependencies. Fonts load from Google Fonts (swap for
  self-hosted if offline). For true 7-segment numerals, self-host the open-source
  DSEG font and set it as `--font-screen`.
- Pick ONE theme (bone or graphite) and ONE hero accent per project — restraint
  is the whole point.
