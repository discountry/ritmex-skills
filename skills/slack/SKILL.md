name: slack
description: |
  Control Slack via the `agent-slack` CLI to read, search, and manage messages, threads, files, reactions, channels, DMs, and canvases. Trigger on requests involving Slack messages, threads, URLs, channel history, unread or recent DMs, or sending/replying to messages (English or Chinese queries mentioning Slack).
---

## Usage

`agent-slack` is a CLI on `$PATH`. Call it directly, for example:

```bash
agent-slack user list
```

## Bash command rules

1. No `#` in commands. Use `general` not `#general`. No `#` comments; use the Bash tool `description` field instead.
2. No `''` or `""`. Avoid patterns like `d.get('key', '')`.
3. Only `| jq` for filtering. No `python3 -c` or other pipes. Use single-quoted jq expressions only.
4. No `||` or `&&`. Run separate commands in separate Bash tool calls.
5. No `>` or `>>`. Consume JSON output directly.

## Messages and threads

Fetch a single message (with thread summary):

```bash
agent-slack message get "https://workspace.slack.com/archives/C123/p1700000000000000"
```

Fetch the full thread:

```bash
agent-slack message list "https://workspace.slack.com/archives/C123/p1700000000000000"
```

Browse recent channel messages:

```bash
agent-slack message list "general" --limit 20
agent-slack message list "C0123ABC" --limit 10
agent-slack message list "general" --with-reaction eyes --oldest "1770165109.000000" --limit 20
agent-slack message list "general" --without-reaction dart --oldest "1770165109.000000" --limit 20
```

`message get/list` and `search` auto-download attachments and include absolute file paths in JSON (for example `message.files[].path`, `files[].path`).

## Draft and send messages

Open a browser-based rich-text editor:

```bash
agent-slack message draft "general"
agent-slack message draft "general" "initial text"
agent-slack message draft "https://workspace.slack.com/archives/C123/p1700000000000000"
```

Send, edit, delete, react:

```bash
agent-slack message send "https://workspace.slack.com/archives/C123/p1700000000000000" "I can take this."
agent-slack message send "alerts-staging" "here's the report" --attach ./report.md
agent-slack message edit "https://workspace.slack.com/archives/C123/p1700000000000000" "I can take this today."
agent-slack message delete "https://workspace.slack.com/archives/C123/p1700000000000000"

agent-slack message send "general" "Here's the plan:
- Step 1: do the thing
- Step 2: verify it worked
  - Sub-step: check logs"
agent-slack message react add "https://workspace.slack.com/archives/C123/p1700000000000000" "eyes"
agent-slack message react remove "https://workspace.slack.com/archives/C123/p1700000000000000" "eyes"
```

Channel mode edit/delete (requires `--ts`):

```bash
agent-slack message edit "general" "Updated text" --workspace "myteam" --ts "1770165109.628379"
agent-slack message delete "general" --workspace "myteam" --ts "1770165109.628379"
```

Attachments for `message send`:

- `--attach <path>` upload a local file (repeatable).

## Channels and invites

The `--limit` flag controls the scan range. Use a high value to cover large workspaces:

```bash
agent-slack channel list --all --limit 500
```

Use channel IDs when known:

```bash
agent-slack message list "C0123ABC" --limit 10
```

Channel operations:

```bash
agent-slack channel list
agent-slack channel list --user "@alice" --limit 50
agent-slack channel list --all --limit 500
agent-slack channel new --name "incident-war-room"
agent-slack channel new --name "incident-leads" --private
agent-slack channel invite --channel "incident-war-room" --users "U01AAAA,@alice,bob@example.com"
agent-slack channel invite --channel "incident-war-room" --users "partner@vendor.com" --external
agent-slack channel invite --channel "incident-war-room" --users "partner@vendor.com" --external --allow-external-user-invites
```

For `--external`, invite targets must be emails. `--allow-external-user-invites` lets them invite others.

## Search (messages and files)

Prefer channel-scoped search:

```bash
agent-slack search all "smoke tests failed" --channel "alerts" --after 2026-01-01 --before 2026-02-01
agent-slack search messages "stably test" --user "@alice" --channel general
agent-slack search files "testing" --content-type snippet --limit 10
```

## Multiple workspaces

When using channel names with multiple workspaces, pass `--workspace` or set `SLACK_WORKSPACE_URL`:

```bash
agent-slack message get "general" --workspace "https://myteam.slack.com" --ts "1770165109.628379"
agent-slack message get "general" --workspace "myteam" --ts "1770165109.628379"
```

## DM and group DM

Open a DM or group DM and get its channel ID:

```bash
agent-slack user dm-open @alice @bob
agent-slack user dm-open U01AAAA U02BBBB U03CCCC
```

## Mark as read

Mark read up to a message:

```bash
agent-slack channel mark "https://workspace.slack.com/archives/C123/p1700000000000000"
agent-slack channel mark "general" --workspace "myteam" --ts "1770165109.628379"
agent-slack channel mark "D0A04PB2QBW" --workspace "myteam" --ts "1770165109.628379"
```

Make a specific message appear unread by setting `--ts` just before it:

```bash
agent-slack channel mark "general" --workspace "myteam" --ts "1770165109.628378"
```

## Canvas and users

```bash
agent-slack canvas get "https://workspace.slack.com/docs/T123/F456"
agent-slack user list --workspace "https://workspace.slack.com" --limit 100
agent-slack user get "@alice" --workspace "https://workspace.slack.com"
```

## References

- [references/commands.md](references/commands.md): command map and flags
- [references/targets.md](references/targets.md): URL vs `channel` targeting rules
- [references/output.md](references/output.md): JSON shapes and download paths
