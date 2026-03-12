---
name: airdrop-tracker
description: 追踪和整理 CryptoRank 上最近 3 天更新的空投项目。先保存报告到本地，再发送精简的 Telegram 通知。
---

# Airdrop Tracker

## 工作流程

1. **抓取数据**:
   - 打开 `https://cryptorank.io/drophunting?rows=50&page=1`。
   - 识别最近 3 天更新的项目（1d, 2d, 3d 或对应日期）。
   - 提取：项目名称、融资额、投资机构、官网链接、X 链接。

2. **保存本地 (必须完成)**:
   - 保存至 `~/Documents/airdrops/`。
   - 文件：`airdrops_YYYY-MM-DD.json` 和 `airdrops_YYYY-MM-DD.md`。

3. **发送通知**:
   - 完成保存后询问用户。
   - 使用 `mcp__telegram-notification__send_notification` 发送，指定 `parse_mode: "HTML"`。

## Telegram 通知格式

```
🪂 空投项目日报 - YYYY-MM-DD

发现 N 个近期更新的空投项目：

1. <a href="WEBSITE_URL">ProjectName</a> - $XXM 融资
2. <a href="WEBSITE_URL">ProjectName</a> - $XXM 融资
...
```

## 注意事项

- 优先处理前 10 个最新项目。
- 融资额缺失标记为 "N/A"。
- 页面加载问题请重试。
