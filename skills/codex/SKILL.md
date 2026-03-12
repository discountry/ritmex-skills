---
name: codex
description: >
  Use when the user asks about OpenAI Codex CLI (codex, codex exec, codex resume, codex review, codex cloud),
  wants to run code analysis, refactoring, or automated editing via Codex, needs help configuring
  AGENTS.md, config.toml, MCP servers, Skills, or Automations, or asks about Codex best practices,
  approval modes, sandboxing, or multi-agent workflows.
---

# Codex Skill Guide

## Models

| Model | Notes |
|---|---|
| `gpt-5.4` | **Default & recommended** — frontier reasoning + coding |
| `gpt-5.3-codex` | Strong coding focus |
| `gpt-5.3-codex-spark` | Extra fast; ChatGPT Pro only (research preview) |

- Set default: `model = "gpt-5.4"` in `~/.codex/config.toml`
- Override per-run: `codex -m gpt-5.4` or `/model` in-session
- Reasoning effort: `--config model_reasoning_effort="high|medium|low"` (or set in config)
  - Low → fast, well-scoped tasks; Medium/High → complex changes or debugging; Extra High → long agentic tasks

---

## Best Practices

### Effective prompting
A strong prompt includes four things:
1. **Goal** — what to change or build
2. **Context** — relevant files, folders, docs, errors (use `@file` mentions)
3. **Constraints** — standards, architecture, conventions to follow
4. **Done when** — tests pass, behavior changes, bug no longer reproduces

### Plan before complex tasks
- **Plan mode**: toggle with `/plan` or `Shift+Tab` — Codex gathers context, asks questions, builds a plan before coding
- **Interview mode**: ask Codex to question you first to sharpen fuzzy requirements
- **PLANS.md template**: configure an execution-plan template for multi-step work

### AGENTS.md — durable guidance
`AGENTS.md` loads into context automatically; encode how your team wants Codex to work.

A good `AGENTS.md` covers:
- Repo layout and important directories
- How to run, build, test, and lint the project
- Engineering conventions and PR expectations
- Constraints / do-not rules
- Definition of done

Layering precedence (most specific wins):
- `~/.codex/AGENTS.md` — personal global defaults
- `<repo>/AGENTS.md` — shared repo standards
- `<repo>/subdir/AGENTS.md` — local rules for a subtree

Use `/init` in the CLI to scaffold a starter `AGENTS.md`, then edit it for your team.
> When Codex makes the same mistake twice, ask for a retrospective and update `AGENTS.md`.

### Skills & Automations
- **Skills**: package a repeatable workflow into a `SKILL.md` file; stored in `$HOME/.agents/skills` (personal) or `.agents/skills/` in a repo (shared)
- Use `$skill-creator` to scaffold a new skill; `$skill-installer` to install it
- **Automations**: schedule stable skills to run in the background via the Codex app Automations tab
- Rule of thumb: if you keep reusing the same prompt → skill; if the skill is stable and predictable → automation

---

## Interactive Mode

```bash
codex                        # Launch TUI
codex "explain this codebase" # Launch with initial prompt
codex -i screenshot.png "Fix this error"  # Attach image(s)
codex --cd <path>            # Set working directory
codex --add-dir ../backend   # Grant extra writable root(s)
codex --full-auto            # workspace-write sandbox + on-request approvals
```

**In-session shortcuts:**
- `@` → fuzzy file search; Tab/Enter to insert path
- `Enter` while running → inject instructions mid-turn; `Tab` → queue follow-up
- `!command` → run a local shell command inline
- `Esc Esc` (empty composer) → edit previous message; continue pressing to walk back
- `Ctrl+G` → open `$VISUAL`/`$EDITOR` for long prompts
- `Up/Down` → navigate draft history
- `/clear` or `Ctrl+L` → clear screen; `/copy` → copy latest output
- `/permissions` → switch approval mode live
- `/theme` → pick syntax highlight theme
- `/model` → switch model mid-session
- `Ctrl+C` or `/exit` → close session

---

## Session Management

```bash
# Resume interactive sessions
codex resume                 # Picker of recent sessions
codex resume --last          # Most recent session (current dir)
codex resume --last --all    # Most recent session (any dir)
codex resume <SESSION_ID>    # Specific session

# Fork a session (preserves original transcript)
codex fork                   # Picker
codex fork --last            # Fork most recent

# Non-interactive resume
codex exec resume --last "Follow-up instruction"
codex exec resume <ID> "Follow-up instruction"
```

**Session controls (slash commands):**
- `/resume` — reopen a saved conversation
- `/fork` — branch into a new thread
- `/compact` — summarize long context (Codex also does this automatically)
- `/agent` — switch between active agents in multi-agent mode
- `/status` — inspect current session state

> Keep one thread per coherent unit of work. Fork only when work truly branches.

---

## Local Code Review

```bash
# Type /review inside an interactive session, or:
codex exec "/review"
```

Review presets (no working-tree modifications):
- **Review against base branch** — diffs to merge base, highlights risks before PR
- **Review uncommitted changes** — staged + unstaged + untracked
- **Review a commit** — pick a SHA from recent list
- **Custom review instructions** — e.g. "Focus on accessibility regressions"

Each review appears as its own turn; re-run as code evolves.
Reference a `code_review.md` from `AGENTS.md` for consistent team review behavior.

---

## Non-Interactive / Scripted Runs (`codex exec`)

```bash
codex exec "fix the CI failure"
codex e "summarize open bugs"                    # short alias

# Pipe prompt from stdin
echo "Refactor auth module" | codex exec -

# JSON output for scripting
codex exec --json "task"

# Capture final message to file
codex exec --json --output-last-message result.md "task"

# Resume non-interactive
codex exec resume --last "Continue the refactor"
```

Key `exec` flags:
| Flag | Purpose |
|---|---|
| `--sandbox/-s read-only\|workspace-write\|danger-full-access` | Sandbox policy |
| `--full-auto` | `workspace-write` + `on-request` approvals |
| `--yolo` / `--dangerously-bypass-approvals-and-sandbox` | No approvals or sandbox — isolated runner only |
| `--skip-git-repo-check` | Allow running outside a git repo |
| `--ephemeral` | No session files persisted to disk |
| `--output-schema <path>` | Validate final response against JSON Schema |
| `--json` | Newline-delimited JSON events |
| `--output-last-message/-o <path>` | Write final assistant message to file |
| `--cd/-C <path>` | Set workspace root |
| `--add-dir <path>` | Grant extra writable root |

---

## Approval & Sandbox Modes

**Approval** (`--ask-for-approval`):
- `on-request` — interactive default; Codex pauses for confirmation before risky actions
- `untrusted` — stricter; prompts more often
- `never` — non-interactive / CI runs

**Sandbox** (`--sandbox`):
- `read-only` — browse only, no edits/exec
- `workspace-write` — read/edit/run within workspace (default in `--full-auto`)
- `danger-full-access` — full machine access; use inside an isolated VM only

Toggle live with `/permissions` in an interactive session.

---

## Web Search

```bash
codex --search               # Live search for one run
```

Config options in `~/.codex/config.toml`:
```toml
web_search = "live"          # always live
web_search = "cached"        # default (pre-indexed, lower injection risk)
web_search = "disabled"      # off

[features]
web_search_request = true

[sandbox_workspace_write]
network_access = true
```

---

## Codex Cloud

```bash
codex cloud                              # Interactive picker
codex cloud exec --env ENV_ID "task"     # Submit task directly
codex cloud exec --env ENV_ID --attempts 3 "task"  # Best-of-N (1–4)
codex cloud list                         # Recent tasks
codex cloud list --env ENV_ID --json     # Filtered + machine-readable
codex apply <TASK_ID>                    # Apply cloud task diff locally
```

---

## MCP (Model Context Protocol)

```bash
codex mcp list               # List configured servers
codex mcp add <name> -- <cmd> [args]   # Register stdio server
codex mcp add <name> --url https://...  # Register streamable HTTP server
codex mcp remove <name>
codex mcp login <name>       # OAuth for HTTP servers
codex mcp-server             # Run Codex itself as an MCP server (stdio)
```

Config in `~/.codex/config.toml`:
```toml
[mcp_servers.my_tool]
command = "npx"
args = ["-y", "@my/tool-server"]

[mcp_servers.my_http_tool]
url = "https://api.example.com/mcp"
bearer_token_env_var = "MY_TOOL_API_KEY"
```

> Add MCP servers only when they remove a real manual loop. Start with 1–2 tools.

---

## Multi-Agent (Experimental)

- Enable via `codex features enable unified_exec` or `[agents]` section in `config.toml`
- Use `/agent` to switch between active agent threads
- Offload bounded subtasks (exploration, tests, triage) to subagents; keep the main agent focused
- Configure roles, parallelism, and routing under `[agents]` in `config.toml`

---

## Shell Completions

```bash
codex completion zsh          # Print zsh completion script

# Add to ~/.zshrc:
autoload -Uz compinit && compinit
eval "$(codex completion zsh)"
```

Supports: `bash`, `zsh`, `fish`, `power-shell`, `elvish`

---

## Feature Flags

```bash
codex features list
codex features enable unified_exec
codex features disable shell_snapshot
```

Or per-run: `codex --enable <feature>` / `--disable <feature>`

Common flags: `web_search_request`, `streamable_shell`, `unified_exec`, `rmcp_client`, `apply_patch_freeform`, `view_image_tool`

---

## CLI Reference

### Global flags (apply to all commands)
| Flag | Type | Description |
|---|---|---|
| `PROMPT` | string | Initial prompt (optional) |
| `--image/-i` | path[,...] | Attach image file(s) |
| `--model/-m` | string | Override model |
| `--oss` | bool | Use local OSS provider (Ollama) |
| `--sandbox/-s` | enum | Sandbox policy |
| `--ask-for-approval/-a` | enum | Approval trigger |
| `--full-auto` | bool | `workspace-write` + `on-request` shortcut |
| `--yolo` | bool | Bypass all approvals/sandbox |
| `--cd/-C` | path | Set working directory |
| `--profile/-p` | string | Load named config profile |
| `--search` | bool | Enable live web search |
| `--add-dir` | path | Grant extra writable root (repeatable) |
| `--enable/--disable` | feature | Toggle feature flag |
| `--config/-c` | key=value | Inline config override (repeatable) |
| `--no-alt-screen` | bool | Disable TUI alternate screen |

### Command overview
| Command | Notes |
|---|---|
| `codex` | Interactive TUI |
| `codex exec` / `codex e` | Non-interactive run; `+ resume` subcommand |
| `codex resume` | Continue interactive session |
| `codex fork` | Fork interactive session |
| `codex apply` | Apply Codex Cloud diff locally |
| `codex cloud` / `codex cloud exec` | Cloud task management |
| `codex login / logout / login status` | Authentication |
| `codex mcp` | Manage MCP servers |
| `codex mcp-server` | Run Codex as MCP server |
| `codex completion` | Generate shell completion scripts |
| `codex features` | Manage feature flags |
| `codex sandbox` | Run commands in Codex sandbox (macOS/Linux) |
| `codex app` | Launch Codex Desktop (macOS) |
| `codex execpolicy` | Evaluate execpolicy rule files |

---

## config.toml Reference

Location: `~/.codex/config.toml` (shared by CLI + IDE)

```toml
# Core
model = "gpt-5.4"
model_provider = "openai"
approval_policy = "on-request"          # on-request | untrusted | never
sandbox_mode = "workspace-write"        # read-only | workspace-write | danger-full-access
model_reasoning_effort = "medium"       # high | medium | low
model_reasoning_summary = "concise"
model_verbosity = "normal"
model_context_window = 200000
model_max_output_tokens = 32768

# TUI
[tui]
theme = "Monokai Extended"
alternate_screen = true

# Web search
web_search = "cached"                   # live | cached | disabled

# Shell environment policy (prevent secret leakage)
[shell_environment_policy]
inherit = "none"
include_only = ["PATH", "HOME", "LANG"]
# or: exclude = ["*_KEY", "*_SECRET", "*_TOKEN"]

# Profiles
[profiles.ci]
model = "gpt-5.3-codex"
sandbox_mode = "read-only"
approval_policy = "never"

# Feature flags
[features]
web_search_request = true
unified_exec = true
rmcp_client = true

# Custom provider example (Ollama)
[model_providers.ollama]
base_url = "http://localhost:11434/v1"
wire_api = "chat"

# Sandbox tuning
[sandbox_workspace_write]
network_access = false
# writable_roots = ["/tmp/extra"]

# MCP servers
[mcp_servers.github]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-github"]
env = { GITHUB_TOKEN = "$GITHUB_TOKEN" }

# Notifications
notify = ["python3", "/path/to/notify.py"]

# Observability
[otel]
exporter = "otlp-http"
endpoint = "http://localhost:4318"
```

Config precedence: **CLI flags > profile > repo `.codex/config.toml` > `~/.codex/config.toml` > defaults**

---

## Assistant Playbook

When helping a user run a Codex task:

1. **Clarify in one prompt**: confirm model (`gpt-5.4` default), reasoning effort (`high|medium|low`), and target directory
2. **Choose sandbox**: default `--sandbox read-only` for analysis; `workspace-write` when edits are needed; never suggest `danger-full-access` without explicit user approval
3. **Build the command** with:
   - `-m <model>` if non-default
   - `--config model_reasoning_effort=<effort>` if specified
   - `--sandbox <mode>` appropriate for task
   - `--skip-git-repo-check` when running outside a git repo
   - `-C <dir>` to set working directory
   - Append `2>/dev/null` to `codex exec` unless user wants stderr
4. **For resume**: `codex exec resume --last "follow-up" 2>/dev/null` — no extra flags unless user requests
5. **Run, then summarize** stdout; include stderr only if relevant or requested
6. **After completion**: remind user they can run `codex resume` to continue interactively
7. **Confirm next steps**: ask whether to resume, adjust, or close; restate model/effort/sandbox in summary
8. **On non-zero exit**: stop and ask before retrying; never retry high-impact flags automatically
9. **For high-impact flags** (`--full-auto`, `--yolo`, `--sandbox danger-full-access`): explicitly ask for permission and explain the risk first
10. **For complex tasks**: suggest Plan mode (`/plan` or `Shift+Tab`) before implementation

---

## Common Mistakes to Avoid

- Overloading prompts with rules that belong in `AGENTS.md` or a skill
- Not specifying build/test commands so Codex can't verify its own work
- Skipping planning for multi-step or ambiguous tasks
- Granting `danger-full-access` before understanding the workflow
- Running concurrent threads on the same files without git worktrees
- Automating a workflow before it's reliable manually
- Using one long-running thread per project instead of one thread per task
- Treating Codex as a step-by-step tool instead of running it in parallel with other work