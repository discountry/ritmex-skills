---
name: create-design-md
description: Generate a complete DESIGN.md design-system specification at the root of the current project, synthesized from whatever material is available — a written description, UI screenshots, code snippets, a reference brand, or the project's own codebase (CSS variables, Tailwind config, theme files, component styles). Use whenever the user asks to create or update a DESIGN.md, document or extract a design system, pull design tokens out of code or screenshots, "写一份设计规范 / 生成设计文档", wants their UI to follow a named brand's look (e.g. "make it feel like Stripe/Linear/Vercel"), or needs a machine-readable token spec (colors / typography / spacing / radius / components) so future UI work stays consistent.
---

# Create DESIGN.md

Produce a `DESIGN.md` in the [`@google/design.md`](https://www.npmjs.com/package/@google/design.md) format: YAML frontmatter holding the machine-readable token system (colors, typography, rounded, spacing, components) plus a human-readable body explaining how the system behaves. The file becomes the single source of truth that humans and agents consult before touching UI — so every value in it must be defensible, and vague filler is worse than an honest gap.

Read `references/format.md` before writing the file. It contains the exact frontmatter schema, the token-reference syntax, and the required body sections.

## Workflow

### 1. Inventory the inputs

Establish what evidence exists before extracting anything:

- **Screenshots / images** — the user attached them or gave paths. Read each one.
- **Code or codebase** — the user pointed at files, or the working directory is a project with UI code. Detect UI code with a quick scan (`package.json` deps, `*.css`, `tailwind.config.*`, theme files).
- **Written description** — the user described the look they want ("dark, dense, terminal-inspired…").
- **Brand reference** — the user named a brand. Check `resources/design-md/` in this skill's directory for a ready-made analysis (stripe, linear.app, vercel, notion). If present, use it as the base and adapt it to the project rather than re-deriving from scratch. For other brands, derive the system from screenshots or the brand's live site; getdesign.md hosts downloadable analyses of many more brands the user can supply.

Sources combine. When they conflict, trust in this order: **actual code values > screenshot measurements > description inferences > brand-reference defaults**. Code is ground truth for what the project ships today; everything else is interpretation.

### 2. Gather evidence

**From a codebase** — mine the places design decisions actually live:

- Tailwind: `tailwind.config.{js,ts}` `theme` / `theme.extend`; Tailwind v4 `@theme` blocks in CSS.
- CSS custom properties: `:root` / `[data-theme]` blocks in `globals.css`, `index.css`, `variables.css`, `*.scss`.
- Theme objects: `theme.ts`, `tokens.{ts,json}`, styled-components / Emotion themes, MUI `createTheme`, Chakra `extendTheme`, `components.json` (shadcn).
- Real components: read `Button`, `Card`, `Input`, nav, and modal implementations for padding, radius, type sizes, and state colors — these are the values users actually see, and they override stale config entries.
- Frequency matters: grep for how often each color/size is used. The most-used interactive color is `primary`; a value used once is an accent or a candidate for **Known Gaps**, not a core token.

**From screenshots** — read every image and extract systematically: dominant surface colors, text colors, the one color used for primary actions, corner radii (sharp / subtle / pill), type scale and weight contrast between headings and body, spacing density, shadows or borders as the depth medium, and any signature element (gradient, texture, unusual component). Hex values sampled from screenshots are estimates — normalize obvious near-duplicates (e.g. `#fefefe` → `#ffffff`) instead of minting a token per artifact.

**From a description alone** — synthesize a coherent system that honors every stated constraint, choose concrete values (real hex codes, real px sizes, a real font stack with fallbacks), and record every assumption you invented in **Known Gaps** so the user knows what to correct. Never leave placeholders like "TBD" or "your color here" in token values.

### 3. Build the token system

Follow the schema in `references/format.md`. Principles that make the file useful rather than decorative:

- **Semantic names, not appearance names.** `primary`, `ink`, `canvas`, `hairline` — not `blue-500` or `light-gray`. The body text explains what each token is for. The main interactive color must be named exactly `primary` — the linter checks for that key, even if the source code calls it `brand` or `accent`.
- **Small and closed.** 10–25 colors, 8–15 typography roles, 5–8 radii, 6–10 spacing steps. A token system's value is what it *excludes*; don't catalog every hex that appears once in the code.
- **Components reference tokens.** Every component field uses `{colors.primary}` / `{typography.body-md}` syntax — never a raw value. If a component needs a value no token covers, that's a signal to add the token or normalize the component.
- **Cover the core set.** At minimum: primary button (+ pressed/hover variant if evidence exists), secondary button, text input (+ focus), card, and one navigation surface. Add the system's signature components beyond that.

### 4. Write the body

Use the section template in `references/format.md` (Overview → Colors → Typography → Layout → Elevation & Depth → Shapes → Components → Do's and Don'ts → Responsive Behavior → Iteration Guide → Known Gaps). Two sections carry most of the value:

- **Overview** must end with **Key Characteristics** — 5–8 bullets naming the system's signature moves, specific enough that someone could recognize the product from the bullets alone.
- **Do's and Don'ts** must be rules specific to *this* system ("Don't use `{colors.primary}` as body-text color", "Don't round buttons below `{rounded.pill}`") — generic design advice ("use consistent spacing") wastes the section.

For calibration on depth and tone, skim one example from `resources/design-md/` (e.g. `stripe/DESIGN.md` for a light marketing system, `linear.app/DESIGN.md` for a dark product system).

### 5. Write the file to the project root

Target path: `<git root>/DESIGN.md` (`git rev-parse --show-toplevel`); fall back to the current working directory when not in a git repo.

If `DESIGN.md` already exists, read it first. Preserve its intent: update tokens that changed, keep sections the user hand-wrote, and say what you changed. Don't silently replace a file you didn't create.

### 6. Validate

```bash
npx -y @google/design.md lint DESIGN.md
```

- **Errors** — fix them; the file must lint clean of errors.
- **Unused-token warnings** — either wire the token into a component that genuinely uses it, or delete it. Exception: border/hairline colors always warn because the component schema has no border field — keep them, describe their use in prose, and note the expected warning in **Known Gaps**.
- **Contrast warnings** — if you are *designing* the system (description-driven), fix the pair to meet WCAG AA. If you are *documenting* an existing UI faithfully, keep the value and note the contrast issue in **Known Gaps** — the document's job is accuracy first.

The export subcommand (`npx -y @google/design.md export DESIGN.md --format css-tailwind`) is a useful smoke test that the tokens are machine-consumable; mention it to the user as a follow-up, don't run it unasked.

### 7. Report

Tell the user: where the file was written, which sources fed it (with file paths for code evidence), token counts, lint result, and the contents of Known Gaps — the assumptions they should review are the most important part of the report.

## Reference files

- `references/format.md` — frontmatter schema, token syntax, body section template, lint behavior. Read before writing.
- `resources/design-md/<brand>/DESIGN.md` — four finished brand analyses covering distinct archetypes: `stripe` (light marketing), `linear.app` (dark product), `vercel` (black-and-white developer platform), `notion` (document tool). Use as the base when the user names one; use one as a calibration example otherwise.
