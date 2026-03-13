---
name: clickup
description: Use for ClickUp tasks and docs. Trigger on ClickUp URLs, task IDs, list IDs, doc IDs, page IDs, assignees, statuses, due dates, comments, checklists, and document workflows. Use the global `clickup` CLI.
---

# ClickUp

Use the global `clickup` CLI. See `README.md` for installation, configuration, and command reference.

## Rules

- Do not read `.env` or secrets.
- Read shell environment variables.
- Use `--json` for structured output.
- Read current state before writes unless the requested change is already exact.

## Checks

1. Run `clickup --help`.
2. On missing CLI, auth, or workspace errors, point to `README.md`.

## Commands

| Intent | Command |
| --- | --- |
| Read task | `clickup get <url-or-id>` |
| Read comments | `clickup comments <url-or-id>` |
| Add comment | `clickup comment <url-or-id> "message"` |
| Read or update status | `clickup status <url-or-id> [status]` |
| List tasks in list | `clickup tasks <list_id>` |
| Show current user | `clickup me` |
| Create task | `clickup create [list_id] "title"` |
| List my tasks | `clickup my-tasks` |
| Search tasks | `clickup search "query"` |
| Assign task | `clickup assign <task> <user>` |
| Set due date | `clickup due <task> "date"` |
| Set priority | `clickup priority <task> <level>` |
| Create subtask | `clickup subtask <task> "title"` |
| Move task | `clickup move <task> <list_id>` |
| Add link | `clickup link <task> <url> ["description"]` |
| Add checklist item | `clickup checklist <task> "item"` |
| Delete comment | `clickup delete-comment <comment_id>` |
| Notify watcher | `clickup watch <task> <user>` |
| Add tag | `clickup tag <task> "tag_name"` |
| Update description | `clickup description <task> "text"` |
| List docs | `clickup docs ["query"]` |
| Read doc | `clickup doc <doc_id>` |
| Create doc | `clickup create-doc "title" [--content "..."]` |
| Read page | `clickup page <doc_id> <page_id> [--content-format text/plain]` |
| Create page | `clickup create-page <doc_id> "title" [--content "..."] [--sub-title "..."]` |
| Update page | `clickup edit-page <doc_id> <page_id> [--name "..."] [--sub-title "..."] [--content "..."]` |

## Execution

1. Normalize the target.
2. Read with the narrowest command.
3. Apply the smallest write.
4. Re-read only when the user needs confirmation.

## Notes

- `clickup status <task>` lists valid statuses.
- Status updates allow partial matching.
- `assign` and `watch` resolve username, email, or user ID.
- `clickup due <task> clear` and `clickup due <task> none` clear due dates.
- `clickup docs ["query"]` also supports `--id`, `--creator`, `--deleted`, `--archived`, `--parent-id`, `--parent-type`, `--limit`.
- `clickup doc <doc_id>` supports `--max-page-depth`.
- `clickup create-page <doc_id> "title"` supports `--parent-page-id`, `--sub-title`, `--content-format`.
- `clickup edit-page <doc_id> <page_id>` requires `--name`, `--sub-title`, or `--content`. It also supports `--content-edit-mode` and `--content-format`.
- `watch` posts an `@mention` comment.

