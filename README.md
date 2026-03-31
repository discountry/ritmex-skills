# ritmex-skills

A collection of reusable AI coding agent skills compatible with mainstream AI-powered coding tools.

## Skills

| Skill | Description |
|---|---|
| **[use-ctx7](skills/use-ctx7/SKILL.md)** | Fetch up-to-date library documentation via the `ctx7` CLI. Proactively queries matching version docs before writing code for any project dependency. |
| **[svg-logo-maker](skills/svg-logo-maker/SKILL.md)** | Design and generate production-quality SVG logos in modern minimalist style using svg.js and browser-based visual verification. |
| **[document](skills/document/SKILL.md)** | Spawn a subagent to produce high-quality project documentation (README, integration guide, tutorials, product docs) from the current repo state. |
| **[ignore](skills/ignore/SKILL.md)** | Generate or update a `.gitignore` file based on the current project stack and tools. |
| **[airdrop-tracker](skills/airdrop-tracker/SKILL.md)** | Track recently updated airdrop projects from CryptoRank, save reports locally, and send Telegram notifications. |
| **[refactor](skills/refactor/SKILL.md)** | Iteratively refactor any codebase for readability, maintainability, and reuse. Enforces size budgets, naming rules, single-responsibility, and decoupling — guided by Fowler, Martin, and Boswell & Foucher. |
| **[codex](skills/codex/SKILL.md)** | Master guide for the OpenAI Codex CLI — models, best practices, AGENTS.md configuration, interactive and non-interactive modes, session management, MCP integration, and multi-agent workflows. |
| **[debug](skills/debug/SKILL.md)** | Systematically surface logic flaws, latent bugs, performance bottlenecks, security vulnerabilities, and test gaps. Biases toward recently changed code — commits, staged changes, and modified files. |
| **[tdd](skills/tdd/SKILL.md)** | Drive net-new features with a strict red→green→refactor loop. Test-first behavior slices, minimal diffs, deterministic verification. |
| **[react-principles](skills/react-principles/SKILL.md)** | React best practices for component design, state management, and Effect discipline. Use when writing, reviewing, or refactoring React components and hooks. |
| **[clickup](skills/clickup/SKILL.md)** | Work with ClickUp tasks and docs using the `clickup` CLI. |
| **[slack](skills/slack/SKILL.md)** | Control Slack via the `slack` CLI to read, search, and manage messages, threads, files, reactions, channels, DMs, and canvases. |
| **[humanizer-zh](skills/humanizer-zh/SKILL.md)** | 去除文本中的 AI 生成痕迹，使其更自然、更像人类书写。基于维基百科"AI 写作特征"综合指南。 |
| **[refine](skills/refine/SKILL.md)** | Improve UI/UX aesthetics and hierarchy — color, spacing, typography, layout, components. Trigger on beautify/polish/refine/modernize requests. |
| **[post-tweet](skills/tweet/post-tweet.md)** | Post a tweet to X (Twitter) using the x-post-mcp server. Supports replies and quote tweets. |
| **[codex-prompt-optimize](skills/codex-prompt-optimize/SKILL.md)** | Auto-trigger in Codex when user input is vague, ambiguous, or incomplete. Analyzes intent and emits a well-formed prompt before execution. |

## Installation

Install individual skills into your project using `npx skills`:

```bash
# use-ctx7 — Library documentation fetcher
npx skills add discountry/ritmex-skills --skill use-ctx7

# svg-logo-maker — SVG logo generator
npx skills add discountry/ritmex-skills --skill svg-logo-maker

# document — Subagent-driven documentation writer
npx skills add discountry/ritmex-skills --skill document

# ignore — Project-aware .gitignore management
npx skills add discountry/ritmex-skills --skill ignore

# airdrop-tracker — Airdrop project tracker
npx skills add discountry/ritmex-skills --skill airdrop-tracker

# refactor — Iterative code refactoring
npx skills add discountry/ritmex-skills --skill refactor

# codex — OpenAI Codex CLI guide
npx skills add discountry/ritmex-skills --skill codex

# debug — Systematic code debugger
npx skills add discountry/ritmex-skills --skill debug

# react-principles — React component + Effect discipline
npx skills add discountry/ritmex-skills --skill react-principles

# clickup — ClickUp tasks and docs
npx skills add discountry/ritmex-skills --skill clickup

# slack — Control Slack via the `slack` CLI
npx skills add discountry/ritmex-skills --skill slack

# humanizer-zh — AI 文本人性化（中文）
npx skills add discountry/ritmex-skills --skill humanizer-zh

# refine — UI/UX aesthetics optimizer
npx skills add discountry/ritmex-skills --skill refine

# post-tweet — Post tweets to X (Twitter)
npx skills add discountry/ritmex-skills --skill tweet

# codex-prompt-optimize — Auto prompt optimization for Codex
npx skills add discountry/ritmex-skills --skill codex-prompt-optimize
```

## License

ISC