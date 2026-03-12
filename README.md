# ritmex-skills

A collection of reusable [Cursor Agent Skills](https://docs.cursor.com/context/skills) for AI-assisted workflows.

## Skills

| Skill | Description |
|---|---|
| **[use-ctx7](skills/use-ctx7/SKILL.md)** | Fetch up-to-date library documentation via the `ctx7` CLI. Proactively queries matching version docs before writing code for any project dependency. |
| **[svg-logo-maker](skills/svg-logo-maker/SKILL.md)** | Design and generate production-quality SVG logos in modern minimalist style using svg.js and browser-based visual verification. |
| **[airdrop-tracker](skills/airdrop-tracker/SKILL.md)** | Track recently updated airdrop projects from CryptoRank, save reports locally, and send Telegram notifications. |

## Installation

Install individual skills into your project using `npx skills`:

```bash
# use-ctx7 — Library documentation fetcher
npx skills add https://github.com/discountry/ritmex-skills --skill use-ctx7

# svg-logo-maker — SVG logo generator
npx skills add https://github.com/discountry/ritmex-skills --skill svg-logo-maker

# airdrop-tracker — Airdrop project tracker
npx skills add https://github.com/discountry/ritmex-skills --skill airdrop-tracker
```

## License

ISC
