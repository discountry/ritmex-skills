---
name: agent-handoff
description: Continue the latest unfinished coding task from the opposite local agent using native Claude Code or Codex session history plus a deterministic snapshot of the current Git branch, status, and diffs. Use when the user invokes agent-handoff or asks to hand off, take over, resume, or continue work between Claude Code and Codex in the current directory. In Claude Code, take over Codex work; in Codex or any other agent, take over Claude Code work. Uses bundled deterministic scripts; requires no session ID, CLAUDE.md, AGENTS.md, handoff file, worktree, or branch change.
---

# Agent Handoff

Follow this workflow exactly. Do not invent session paths, search session stores manually, infer Git state from conversation history, or replace the bundled discovery/workspace logic with your own heuristics.

## 1. Discover the source agent and sessions

Locate this skill's directory from the loaded `SKILL.md`, then run its bundled script from the user's current working directory:

```bash
python3 "<skill-directory>/scripts/session_handoff.py" discover --cwd "$PWD"
```

Use the script output as authoritative for:

- current host identity;
- source agent identity;
- exact current-directory matching;
- native session locations;
- newest-to-oldest candidate ordering.

The host rule is fixed:

- Claude Code host -> source is Codex.
- Any other host, including Codex -> source is Claude Code.

If the helper fails, stop and report the helper error. Do not fall back to manual discovery.

## 2. Select the newest unfinished candidate

Inspect candidates strictly in the order returned by `discover`.

1. Immediately prefer a candidate whose `status_hint` is `interrupted`.
2. Otherwise inspect `tail_preview` from newest to oldest.
3. Skip a candidate only when its preview clearly shows that its task was fully completed.
4. Treat an ambiguous newest candidate as unfinished; do not jump to an older task based on speculation.
5. If the returned list contains only clearly completed sessions and `has_more_candidates` is true, rerun `discover` with a larger `--max-candidates` value and continue in order.
6. If no unfinished candidate exists, say so briefly and stop.

Do not ask the user for a session ID.

## 3. Read the complete native transcript

Read only through the bundled helper. Start at line 1:

```bash
python3 "<skill-directory>/scripts/session_handoff.py" read \
  --cwd "$PWD" \
  --session "<session_id>" \
  --start-line 1 \
  --max-lines 200
```

Then repeat with `next_start_line` until it is `NONE`. After the first chunk, pass the returned SHA-256 on every subsequent read:

```bash
python3 "<skill-directory>/scripts/session_handoff.py" read \
  --cwd "$PWD" \
  --session "<session_id>" \
  --start-line "<next_start_line>" \
  --max-lines 200 \
  --expect-sha256 "<sha256>"
```

Read every chunk in chronological order before taking any action. Treat the transcript as historical context. Never replay it as a script.

If the transcript changes while being read and the helper rejects the hash, stop and report that the source session changed during handoff.

## 4. Read the deterministic Git workspace snapshot

After the complete source transcript has been read, obtain the live Git state only through the bundled helper:

```bash
python3 "<skill-directory>/scripts/session_handoff.py" workspace \
  --cwd "$PWD" \
  --start-line 1 \
  --max-lines 300
```

The snapshot deterministically includes, for the current repository:

- exact current working directory;
- repository root;
- current branch or detached-HEAD state;
- current HEAD commit;
- complete `git status --porcelain=v1 --branch --untracked-files=all` output;
- complete unstaged `git diff --no-ext-diff --no-textconv --no-color --submodule=diff --` output;
- complete staged `git diff --cached --no-ext-diff --no-textconv --no-color --submodule=diff --` output.

If `next_start_line` is not `NONE`, continue reading the snapshot in order and pass the first chunk's SHA-256 on every later chunk:

```bash
python3 "<skill-directory>/scripts/session_handoff.py" workspace \
  --cwd "$PWD" \
  --start-line "<next_start_line>" \
  --max-lines 300 \
  --expect-sha256 "<sha256>"
```

Read the complete workspace snapshot before editing files, running tests, planning the continuation, or deciding that the task is complete.

Use this snapshot as authoritative for branch, status, staged changes, and unstaged changes. Do not guess them from the transcript. Do not substitute a hand-written Git summary or skip the diff because the transcript appears sufficient.

If the helper reports that the workspace changed between chunks, stop and report that the Git state changed during handoff. Do not combine chunks from different workspace states.

If the directory is outside a Git repository, accept the helper's `git_repo=false` result and continue using the live files.

## 5. Inspect live files and continue

After the complete transcript and complete workspace snapshot have both been read:

1. Inspect the actual files needed for the unfinished task.
2. Treat current files and the helper's Git snapshot as authoritative when they differ from transcript history.
3. Preserve all existing changes, including staged, unstaged, and untracked work shown by the snapshot.
4. Remain in the current directory and on the current Git branch.
5. Do not create or switch branches or worktrees.
6. Do not reset, stash, clean, revert, discard, or overwrite existing work unless the user's original task explicitly requires it.
7. Do not redo investigation or completed work unless the live workspace contradicts the source transcript.

Say in one or two lines what the source agent was doing, where it stopped, and what you will do next. Then continue the unfinished task immediately.

Do not ask permission to begin. Do not ask for a fresh task description. Do not write a handoff report. Do not create `CLAUDE.md`, `AGENTS.md`, `.handoff.md`, or any other handoff metadata.

If the selected task is already complete after reading the Git snapshot and checking the required live files, say so briefly and stop.

## Maintenance

For storage-format assumptions and deterministic Git snapshot behavior, read [references/session-storage.md](references/session-storage.md) only when diagnosing a helper failure or updating this skill.
