# teenage-engineering-ui (Claude/agent skill)

A portable **skill** that teaches an agentic coding tool how to design UIs in the
Teenage Engineering / Dieter Rams functionalist-hardware aesthetic: neutral
molded panels, one bold accent, tactile knobs and buttons, LED/segment displays,
uppercase monospace labels, and visible "device chrome."

## Contents

```
teenage-engineering-ui/
├── SKILL.md                     # entry point: philosophy, principles, workflow
├── references/
│   ├── design-tokens.md         # full color/type/spacing/shadow values (2 themes)
│   ├── components.md            # working HTML/CSS recipes for every control
│   └── checklist.md             # pre-delivery self-review + common-mistake fixes
└── assets/
    ├── te-tokens.css            # drop-in CSS custom properties (bone + graphite)
    └── starter-template.html    # complete, self-contained working device
```

The skill uses progressive disclosure: the agent reads `SKILL.md` first, then
pulls in the `references/` files only as needed. `assets/` are meant to be used
directly in the output.

## Install

### Claude Code
Place the `teenage-engineering-ui/` folder in your skills directory:

- Project-level: `.claude/skills/teenage-engineering-ui/`
- User-level (all projects): `~/.claude/skills/teenage-engineering-ui/`

Claude Code auto-discovers `SKILL.md` and surfaces the skill by its frontmatter
`description`. Then just ask, e.g. *"Build the settings screen in a Teenage
Engineering style."*

### Codex / other agentic tools
Drop the folder into your project (e.g. `./skills/teenage-engineering-ui/`) and
point the agent at it, or paste the contents of `SKILL.md` into the system /
context for the task. The skill is plain Markdown + CSS/HTML with no runtime
dependencies, so it works with any tool that can read repo files.

### Quick preview
Open `assets/starter-template.html` in a browser to see the target aesthetic
before generating anything.

## Notes
- No build step, no dependencies. Fonts load from Google Fonts (swap for
  self-hosted if offline). For true 7-segment numerals, self-host the open-source
  DSEG font and set it as `--font-screen`.
- Pick ONE theme (bone or graphite) and ONE hero accent per project — restraint
  is the whole point.
