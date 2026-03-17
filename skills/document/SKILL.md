---
name: document
description: Spawn a subagent to produce high-quality project documentation (README, integration guide, tutorials, product docs) from the current repo state.
---

# Role: Documentation Lead (agentic, subagent-driven)

## When to use
Use this skill when the user asks to:
- Write or improve `README.md`
- Create “getting started”, “integration”, “tutorial”, “how-to”, “FAQ”, “troubleshooting”, or “product” documentation
- Generate docs from existing code/configs, or align docs with current repo behavior
- Do documentation work via “Spawn a subagent to …”

## Goal
Create **concise, complete, and clear** documentation that matches the repository’s actual behavior and setup steps.

## Inputs to collect (from the repo)
The documentation subagent must ground claims in the codebase. It should extract:
- **Project identity**: name, purpose, audience, supported platforms
- **How to run**: install steps, required env vars, commands, ports
- **How to use**: main flows, examples, typical use-cases
- **How to extend**: configuration, architecture overview (high level), key directories
- **How to troubleshoot**: common errors, fixes, logs, support channels

## Output requirements
Depending on the user request, produce one or more:
- `README.md` (default)
- `docs/integration.md`
- `docs/tutorial.md`
- `docs/product.md`
- `docs/faq.md`
- `docs/troubleshooting.md`

Every doc must include:
- **What** the project is
- **Who** it is for
- **How** to install/run/use (copy-pasteable commands)
- **Verification** steps (how to confirm it works)
- **Known constraints** (OS, versions, limitations) when discoverable

## Subagent protocol (MANDATORY)
Spawn a subagent that reads the repo and returns a structured “docs brief” plus ready-to-paste markdown.

### Recommended subagent prompt (copy/paste)
Spawn a subagent to write documentation for the repository at `<WORKSPACE_ROOT>`.

Constraints:
- Ground every setup step and command in files present in the repo.
- Prefer the simplest working path; avoid speculative features.
- If there are multiple runtimes (Node/Python/etc.), document the one actually used by this repo.
- Use consistent terminology and minimal jargon.

Tasks:
1) Identify how the project is installed, configured, run, and tested (from package files, scripts, Makefiles, CI, examples).
2) List required environment variables and defaults (from `.env.example`, config files, code).
3) Draft:
   - `README.md` with: Overview, Features, Requirements, Quickstart, Configuration, Usage, Development, Troubleshooting, License.
   - If the repo is a skill-collection/library: include install + usage examples, and a table of modules/skills.
4) Return:
   - A “Docs Brief” section (facts, assumptions, open questions as TODOs).
   - Final markdown content ready to commit.

Deliverable format:
- `## Docs Brief` (bullets)
- `## Proposed README.md` (full markdown)
- `## Optional Additional Docs` (only if needed)

## Quality bar checklist
- Commands run from correct directories and use existing scripts.
- No references to files that do not exist.
- Examples compile logically with repo conventions.
- Sections are skimmable: short paragraphs, bullet lists, consistent headings.