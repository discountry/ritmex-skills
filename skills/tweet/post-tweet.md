---
name: post-tweet
allowed-tools: send_tweet
argument-hint: [text] | --reply-to [tweet-id] | --quote [tweet-id]
description: Post a tweet to X (Twitter) using the x-post-mcp server
disable-model-invocation: true
---

# Post Tweet Skill

Post a tweet to X (Twitter) using the x-post-mcp server.

## Instructions

1. Confirm the tweet content with the user before posting
2. Call the `send_tweet` tool with the user's message
3. Report the result back to the user

## Examples

**Simple tweet:**
User: 帮我发一条推文：Hello World!
Assistant: [calls send_tweet with text: "Hello World!"]

**Reply to a tweet:**
User: 回复这条推文 1234567890：感谢分享！
Assistant: [calls send_tweet with text: "感谢分享!", reply_to_tweet_id: "1234567890"]

**Quote tweet:**
User: 引用推文 1234567890 并评论：这个观点很有意思
Assistant: [calls send_tweet with text: "这个观点很有意思", quote_tweet_id: "1234567890"]
