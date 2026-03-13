# ClickUp Skill

Codex skill for ClickUp. Uses the global `clickup` command.

## Install

```bash
npm install -g @discountry/clickup-cli
npx skills add discountry/clickup-cli --skill clickup
# or
npx skills add https://github.com/discountry/clickup-cli --skill clickup
clickup --help
```

Local package install:

```bash
npm install -g .
```

## Configure

Set shell environment variables:

```bash
export CLICKUP_API_TOKEN=pk_your_token_here
export CLICKUP_WORKSPACE_ID=123456
export CLICKUP_USER_ID=7890
export CLICKUP_DEFAULT_LIST_ID=901111220963
```

Variables:

| Variable | Usage |
| --- | --- |
| `CLICKUP_API_TOKEN` | Required. Personal API Token |
| `CLICKUP_WORKSPACE_ID` | Optional. Workspace ID |
| `CLICKUP_TEAM_ID` | Optional. Alias for `CLICKUP_WORKSPACE_ID` |
| `CLICKUP_USER_ID` | Optional. Current user ID |
| `CLICKUP_DEFAULT_LIST_ID` | Optional. Default list for `clickup create "Task title"` |

## Commands

### Tasks and comments

```bash
clickup me
clickup get 86a1b2c3d
clickup get "https://app.clickup.com/t/86a1b2c3d" --subtasks
clickup comments 86a1b2c3d
clickup comment 86a1b2c3d "Starting work"
clickup status 86a1b2c3d
clickup status 86a1b2c3d "in progress"
clickup status 86a1b2c3d "progress"
clickup tasks 901111220963 --me
clickup my-tasks
clickup search "authentication"
```

- `status <task>`: list valid statuses.
- `status <task> "<text>"`: partial matching supported.

### Create and update tasks

```bash
clickup create "Quick task"
clickup create 901111220963 "New feature" --assignee me --due tomorrow --description "## Scope"
clickup assign 86a1b2c3d jane
clickup assign 86a1b2c3d jane@example.com
clickup assign 86a1b2c3d 123456
clickup due 86a1b2c3d "+3d"
clickup due 86a1b2c3d clear
clickup due 86a1b2c3d "2026-03-20"
clickup priority 86a1b2c3d high
clickup subtask 86a1b2c3d "Write tests"
clickup move 86a1b2c3d 901111220964
clickup link 86a1b2c3d "https://github.com/org/repo/pull/123" "PR #123"
clickup checklist 86a1b2c3d "Review code"
clickup delete-comment 90110200841741
clickup watch 86a1b2c3d alex
clickup watch 86a1b2c3d jane@example.com
clickup watch 86a1b2c3d 123456
clickup tag 86a1b2c3d "DevOps"
clickup description 86a1b2c3d "# Summary"
```

- `assign`, `watch`: username, email, or user ID.
- `watch`: posts an `@mention` comment.
- `priority`: `urgent`, `high`, `normal`, `low`, `none`.
- `due`: `today`, `tomorrow`, `next friday`, `next week`, `+3d`, `YYYY-MM-DD`, `clear`, `none`.

### Docs and pages

```bash
clickup docs
clickup docs "API"
clickup docs "Sprint1" --parent-type FOLDER --limit 100
clickup doc abc123
clickup create-doc "Project Notes" --content "# Notes"
clickup page abc123 page456 --content-format text/plain
clickup create-page abc123 "New Section" --content "Hello" --sub-title "Summary"
clickup edit-page abc123 page456 --name "Renamed"
clickup edit-page abc123 page456 --content "# Updated" --content-edit-mode append
clickup edit-page abc123 page456 --name "Renamed" --sub-title "Updated" --content "# Updated"
```

- `docs`: supports `--id`, `--creator`, `--deleted`, `--archived`, `--parent-id`, `--parent-type`, `--limit`.
- `doc`: supports `--max-page-depth`.
- `page`: supports `--content-format text/md|text/plain`.
- `create-page`: supports `--sub-title`, `--parent-page-id`, `--content-format`.
- `edit-page`: pass `--name`, `--sub-title`, `--content`, or any combination of them. Also supports `--content-edit-mode` and `--content-format`.

## Usage rules

- Add `--json` for structured output.
- Read current state before writes.
- Run `clickup status <task>` before a status update when needed.
- Run `clickup due <task> clear` to clear a due date.

## Troubleshooting

- `clickup: command not found`: install the CLI.
- `401`: check `CLICKUP_API_TOKEN`.
- Workspace or list errors: check `CLICKUP_WORKSPACE_ID` and `CLICKUP_DEFAULT_LIST_ID`.