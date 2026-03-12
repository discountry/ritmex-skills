---
name: codex
description: Use when the user asks to run Codex CLI (codex exec, codex resume) or references OpenAI Codex for code analysis, refactoring, or automated editing
---

# Codex Skill Guide

## Codex Models (current)
- **Recommended**
  - `gpt-5.4` (default)
  - `gpt-5.3-codex`

## Configure models
- Default local model: `model="<name>"` in `~/.codex/config.toml`. If absent, CLI/IDE picks.
- Switch temporarily: `/model` in-session; IDE dropdown; or `codex -m gpt-5.3-codex`.
- Profiles: `[profiles.<name>]` bundles; precedence is CLI flags > profile > root config > defaults.

## Fast start (interactive)
- Launch TUI: `codex`.
- Attach images: `codex -i img.png "prompt"`.
- Approvals: `/approvals` to toggle `auto` (default), `read-only`, `full access`.
- Exit: `Ctrl+C` or `/exit`.

## Resuming
- Interactive: `codex resume`, `codex resume --last`, or `codex resume <SESSION_ID>`.
- Exec: `codex exec resume --last "prompt"` or `codex exec resume <ID> "prompt"`.
- Resume keeps transcript/approvals; override cwd with `--cd` or add roots with `--add-dir`.

## Models & reasoning
- Override model with `/model` or `--model`.
- Reasoning effort: `--config model_reasoning_effort="<high|medium|low>"` or set in config.

## Image inputs
- Paste into TUI or pass files: `codex -i img1.png,img2.jpg "text"`.

## Local code review
- `/review` presets: base branch, uncommitted changes, commit, or custom prompt. Produces prioritized findings without modifying the tree.

## Web search
- Opt-in via config:
  ```toml
  [features]
  web_search_request = true
  [sandbox_workspace_write]
  network_access = true
  ```
- Or per-run: `codex --search`.

## One-shot prompt
- `codex "prompt"` reads workspace, plans, responds. Combine with `--path` or `--model`.

## Shell completions
- `codex completion {bash|zsh|fish|power-shell|elvish}`; add to shell rc (zsh needs `autoload -Uz compinit && compinit` before eval).

## Approval modes
- `auto` (default): read/edit/run in workspace; prompts for risky actions.
- `read-only`: consultative, no edits/exec without approval.
- `full access`: broad permissions; use sparingly.

## Codex Cloud
- `codex cloud` opens picker. `codex cloud exec --env ENV_ID --attempts 1-4 "task"` submits; auth via CLI login.

## Slash commands
- Built-ins like `/review`, `/plan`; custom commands supported via slash command guide.

## MCP (Model Context Protocol)
- Configure servers in `~/.codex/config.toml`; manage via `codex mcp`. Run Codex as MCP server with `codex mcp-server`.

## Tips & shortcuts
- `@` for fuzzy file search; `Esc Esc` to edit previous user message; `--cd` sets workspace; `--add-dir` grants extra writable roots.

## Codex CLI reference (core)
- Global flags: `PROMPT`, `--image/-i`, `--model/-m`, `--oss`, `--sandbox/-s`, `--ask-for-approval/-a`, `--full-auto`, `--dangerously-bypass-approvals-and-sandbox/--yolo`, `--cd/-C`, `--profile/-p`, `--search`, `--add-dir`, `--enable/--disable <feature>`, `--config/-c key=value`, `--skip-git-repo-check`, `--output-schema`, `--color`, `--json`, `--output-last-message/-o`.
- Commands: `codex` (interactive), `codex exec`/`codex e` (+ `resume`), `codex login|logout|login status`, `codex resume` (interactive), `codex apply`, `codex sandbox` (mac seatbelt / Linux landlock), `codex completion`, `codex mcp`, `codex mcp-server`, `codex app-server`, `codex cloud`/`codex cloud exec`.

## Running a task (assistant playbook)
1) Ask the user which model (`gpt-5.4` or `gpt-5.3-codex`) **and** which reasoning effort (`high|medium|low`) in one prompt.  
2) Pick sandbox (default `--sandbox read-only`; move to `workspace-write` when edits are needed).  
3) Build command with `--skip-git-repo-check` always, plus needed flags (`-m`, `--config model_reasoning_effort=...`, `--sandbox ...`, `--full-auto` if approved, `-C <dir>`). Append `2>/dev/null` to `codex exec` unless user wants stderr.  
4) Resume exec: `echo "prompt" | codex exec --skip-git-repo-check resume --last 2>/dev/null` (no extra flags unless user asks).  
5) Run, summarize stdout (include stderr only if requested/needed).  
6) After completion: “You can resume this Codex session anytime with `codex resume` or ask me to continue.”  
7) After each run, use `AskUserQuestion` to confirm next steps or resume; restate chosen model, reasoning effort, sandbox.  
8) On non-zero exits, stop and ask; do not retry without approval. For high-impact flags (`--full-auto`, `--sandbox danger-full-access`, `--skip-git-repo-check`), get permission first. Summarize warnings and ask how to adjust.

## Configuring Codex (config.toml)
- Location: `~/.codex/config.toml`; shared by CLI and IDE (IDE: gear > Codex Settings > Open config.toml).
- Common settings:
  - Default model: `model = "<name>"`.
  - Provider: `model_provider = "<provider>"` (define under `[model_providers.*]`; supports OpenAI/Responses, Ollama, Mistral, Azure, etc.).
  - Approval policy: `approval_policy = "on-request|untrusted|on-failure|never"`.
  - Sandbox: `sandbox_mode = "read-only|workspace-write|danger-full-access"`.
  - Reasoning: `model_reasoning_effort = "high|medium|low"`.
  - Env policy: `[shell_environment_policy]` with `inherit`, `include_only`, `exclude`, `set`.
  - Profiles: `[profiles.<name>]`; set `profile = "<name>"` to make default.
  - Features: `[features]` keys like `web_search_request`, `streamable_shell`, `unified_exec`, `rmcp_client`, `apply_patch_freeform`, `view_image_tool`; enable via config or `codex --enable <feature>`.
- Advanced:
  - Custom providers: define `model_providers.<name>` (base_url, env_key, wire_api, headers).
  - Azure Responses example: `query_params = { api-version = "2025-04-01-preview" }`, `wire_api = "responses"`.
  - Reasoning/verbosity caps: `model_reasoning_summary`, `model_verbosity`, `model_context_window`, `model_max_output_tokens`.
  - Sandbox tuning: `[sandbox_workspace_write]` for tmp access, `network_access`, extra writable roots; disable sandbox only if environment is already isolated (`sandbox_mode = "danger-full-access"`).
  - Shell env templates to avoid secret leakage (`inherit = "none"` with `include_only` or `exclude` globs).
  - MCP servers: add under `[mcp_servers.<name>]` (stdio `command`/`args` or streamable `url` + optional bearer env). OAuth for streamable requires `rmcp_client`.
  - Observability: `[otel]` exporter (`otlp-http`/`otlp-grpc`), headers, environment tag, prompt logging toggle.
  - Notifications: `notify = ["python3", "/path/to/notify.py"]` for `agent-turn-complete`.
  - IDE personalization: set IDE settings/keyboard shortcuts via the extension gear menu.
