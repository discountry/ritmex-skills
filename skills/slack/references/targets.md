# Targets: URL vs channel (reference)

`slack` accepts either a **Slack message URL** (preferred) or a **channel reference**.

## Preferred: Slack message URL

Use the message permalink whenever you have it:

```text
https://<workspace>.slack.com/archives/<channel_id>/p<digits>[?thread_ts=...]
```

Examples:

- `slack message get "<url>"`
- `slack message list "<url>"`
- `slack message send "<url>" "reply text"`
- `slack message edit "<url>" "updated text"`
- `slack message delete "<url>"`
- `slack message react add "<url>" "eyes"`
- `slack channel mark "<url>"`

## Channel targets (when you don’t have a URL)

Channel references can be:

- channel name: `general` (bare name, without `#` prefix)
- channel id: `C...` (or `G...`/`D...`)

### `message get` by channel + `--ts`

```bash
slack message get "general" --ts "1770165109.628379"
```

### `message list` by channel + `--thread-ts` (or `--ts` to resolve)

```bash
slack message list "general" --thread-ts "1770165109.000001"
slack message list "general" --ts "1770165109.628379"
slack message list "general" --without-reaction dart --limit 20
```

### Reactions by channel + `--ts`

```bash
slack message react add "general" "eyes" --ts "1770165109.628379"
```

### Edit/delete by channel + `--ts`

```bash
slack message edit "general" "updated text" --ts "1770165109.628379"
slack message delete "general" --ts "1770165109.628379"
```

### Mark as read by channel + `--ts`

```bash
slack channel mark "general" --ts "1770165109.628379"
slack channel mark "D0A04PB2QBW" --ts "1770165109.628379"
```

### Channel admin by id/name

```bash
slack channel invite --channel "general" --users "@alice,bob@example.com"
slack channel invite --channel "C0123ABCDEF" --users "U01234567"
slack channel invite --channel "shared-room" --users "partner@vendor.com" --external
slack channel invite --channel "shared-room" --users "partner@vendor.com" --external --allow-external-user-invites
```

## Multi-workspace ambiguity (channel names only)

If you have multiple workspaces configured and your target is a channel **name** (e.g. `general`), you must disambiguate:

- pass `--workspace "https://myteam.slack.com"` (or a unique substring like `--workspace "myteam"`), or
- set `SLACK_WORKSPACE_URL` to the same selector format

Channel IDs (`C...`/`G...`/`D...`) do not require `--workspace`.
