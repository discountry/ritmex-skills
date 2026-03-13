---
name: ignore
description: Generate or update a .gitignore file based on the current project stack and tools. Use when the user invokes /ignore or asks to create, fix, or audit a .gitignore for the current repository.
---

# /ignore – Project-Aware .gitignore

## Intent

This skill helps the agent create or update a `.gitignore` file **based on the actual project layout and tech stack**, instead of using a one-size-fits-all template.

Use it when:
- The user types `/ignore`
- The user asks to create, update, or audit a `.gitignore`
- A new project is initialized and no `.gitignore` exists yet

## High-Level Workflow

1. **Discover project type and tools**
2. **Decide which ignore templates apply**
3. **Generate a `.gitignore` candidate**
4. **Safely merge with any existing `.gitignore`**
5. **Show a short summary of what was added/changed**

Keep changes **minimal and reversible** (back up existing `.gitignore` before modifying).

## Step 1 – Discover Project Stack

Work from the repository root.

1. **Detect languages / frameworks** (examples, not exhaustive):
   - Node/JS/TS: `package.json`, `pnpm-lock.yaml`, `yarn.lock`, `node_modules/`
   - Python: `pyproject.toml`, `requirements.txt`, `.venv/`, `__pycache__/`
   - Go: `go.mod`, `go.sum`
   - Rust: `Cargo.toml`, `Cargo.lock`, `target/`
   - Java / JVM: `pom.xml`, `build.gradle`, `.gradle/`, `*.iml`
   - Frontend frameworks: `next.config.*`, `vite.config.*`, `webpack.config.*`
2. **Detect tools / editors**:
   - VS Code: `.vscode/`
   - JetBrains: `.idea/`
   - OS junk: `.DS_Store`, `Thumbs.db`
3. **Detect build / artifact directories**:
   - `dist/`, `build/`, `.turbo/`, `.next/`, `coverage/`, `out/`, `tmp/`, `logs/`

You do not need to be perfect; detect the obvious signals and choose sensible defaults.

## Step 2 – Choose Ignore Coverage

Based on discovery, decide which groups to include:

- **Core OS / editor noise**: macOS, Windows, IDEs
- **Language / runtime specific**: Node, Python, Go, Rust, etc.
- **Tooling / build artifacts**: bundlers, coverage, temporary directories

Prefer **including too little** over **too much**:
- Do **not** ignore lockfiles (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `Cargo.lock`, etc.).
- Do **not** ignore source directories (`src/`, `app/`, etc.).
- Only ignore `env`/`.env.*` if consistent with workspace conventions and security rules; never remove existing entries that intentionally ignore env files.

## Step 3 – Generate .gitignore Content

Create an in-memory list of lines for the candidate `.gitignore` with **small, focused sections**.

Suggested structure (keep each section short):

```text
# OS
.DS_Store
Thumbs.db

# Editors
.vscode/
.idea/

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# Build output
dist/
build/
coverage/
.next/
.turbo/
out/

# Environments
.env.local
.env.development.local
.env.test.local
.env.production.local
```

Add or remove sections depending on the detected stack (for non-Node projects, skip Node‑specific lines, etc.).

## Step 4 – Merge with Existing .gitignore

When a `.gitignore` already exists:

1. **Read existing contents** into a set of lines.
2. **Back up** the file to `.gitignore.bak` in the repository root before modifying.
3. For each candidate line:
   - If the line is already present (exact string match, ignoring trailing whitespace), do nothing.
   - If it is new, append it at the end in the appropriate section, preserving section comments as much as possible.
4. Avoid deleting or rewriting user-defined patterns; **never remove custom rules** unless explicitly asked.

When no `.gitignore` exists:

1. Create a new `.gitignore` in the project root.
2. Write only the lines relevant to the detected stack and tools.

## Step 5 – Report Back to the User

After writing the file, summarize:

- **Created vs updated**: whether `.gitignore` was new or modified.
- **Key sections added**: e.g., “Node artifacts”, “macOS junk files”, “VS Code project settings”.
- **Number of new patterns** added.

Example summary:

> **Result**: Updated existing `.gitignore` (backed up to `.gitignore.bak`).  
> **Added**: Node build artifacts, macOS `.DS_Store`, VS Code workspace folder ignores.  
> **Patterns added**: 14 new entries.

## Notes & Safety

- Be conservative when inferring what to ignore; it is better to under‑ignore and let the user add more entries than to hide important files.
- Never ignore the entire project directory, `.*` generically, or critical configuration directories unless the repository already does so.
- If the user asks to regenerate from scratch, confirm by backing up the existing `.gitignore` and clearly stating that you are replacing its contents.

