---
name: airdrop-tracker
description: Track recently updated airdrop projects from CryptoRank (last 3 days). Save report locally, then send a concise Telegram notification.
disable-model-invocation: true
---

# Airdrop Tracker

## Workflow

1. **Scrape**: Open `https://cryptorank.io/drophunting?rows=50&page=1`. Filter projects updated within 3 days (1d, 2d, 3d or equivalent dates). Extract: project name, funding amount, investors, website URL, X link.

2. **Save locally (required)**: Write to `~/Documents/airdrops/` as `airdrops_YYYY-MM-DD.json` and `airdrops_YYYY-MM-DD.md`.

3. **Notify**: After saving, ask the user before sending. Use `mcp__telegram-notification__send_notification` with `parse_mode: "HTML"`.

## Telegram Format

```
🪂 Airdrop Daily - YYYY-MM-DD

Found N recently updated airdrop projects:

1. <a href="WEBSITE_URL">ProjectName</a> - $XXM raised
2. <a href="WEBSITE_URL">ProjectName</a> - $XXM raised
...
```

## Notes

- Prioritize the top 10 most recent projects.
- Mark missing funding as "N/A".
- Retry on page load failures.
