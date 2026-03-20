---
title: "An Agentic Email Client"
layout: post
date: 2026-03-20 08:30
tag:
- email
- CLI
- JMAP
- TUI
- Fastmail
- Python
- Textual
category: blog
author: jaime
headerImage: false
---

I built a terminal email client for [Fastmail](https://www.fastmail.com). It started as a stateless CLI for scripting and agent workflows, then grew a TUI with vim keys and an AI chat pane. It talks JMAP ([RFC 8620](https://www.rfc-editor.org/rfc/rfc8620), [RFC 8621](https://www.rfc-editor.org/rfc/rfc8621)) directly.

<link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/asciinema-player@3.8.0/dist/bundle/asciinema-player.css">
<script src="https://cdn.jsdelivr.net/npm/asciinema-player@3.8.0/dist/bundle/asciinema-player.min.js"></script>
<div id="player"></div>
<script>
AsciinemaPlayer.create('/assets/tui.cast', document.getElementById('player'), {
  cols: 155,
  rows: 50,
  autoPlay: true,
  loop: true,
  speed: 1.5,
  theme: 'monokai',
  fit: 'width'
});
</script>

## Why

I am not very good at handling it email, it's just too many emails and I feel overwhelmed by it. So I wanted an agent that could help me read and reply to messages, and web clients don't have an API for that. IMAP is painful for programmatic access. Fastmail's JMAP API is stateless and well-documented, so that's what I built on.

The CLI came first, a tool an agent could shell out to. The TUI came later because I wanted to browse email without leaving the terminal. The chat pane came after that because I got tired of switching windows to talk to the agent.

## The thin CLI: `fm`

`fm` is about 340 lines of Node.js. Stateless, no daemon, no local database. Each invocation hits the JMAP API, prints what it finds, and exits.

```
fm inbox [N]                   Recent inbox (default 10)
fm folder <name> [N]           Recent emails from folder
fm mailboxes                   List all mailboxes
fm search <query> [options]    Full-text search
   --from, --to, --after, --before, --folder, --limit
fm headers <id> [id...]        Headers + preview (no body)
fm read <id>                   Full email body
fm markread <id> [id...]       Mark emails as read
fm open                        Launch TUI
fm send [options]              Send email
fm reply <id> [options]        Reply (threads properly)
```

The commands are layered on purpose. `fm inbox 20` returns IDs and subjects. `fm headers id1 id2` adds full headers and a preview. `fm read id` gives you the body. Each step narrows scope, and that matters for token cost. An agent scanning 20 emails with `fm inbox` burns maybe 50 tokens per message. `fm headers` costs around 200 each. Only the messages worth reading get the full `fm read`. A typical inbox pass costs a few hundred tokens instead of tens of thousands.

Search runs server-side via JMAP's `text` filter, so there's no local index and only matching messages come back. Same idea: don't pay for what you don't need.

## The Agentic TUI

The TUI is Python, built with [Textual](https://textual.textualize.io/). Textual gives you focus management, key routing, CSS layout, and async workers out of the box, so I didn't have to wire any of that up myself.

The bottom pane is a chat interface. The agent sees which folder is selected, which email is open, and the body text. It can summarize what you're looking at, draft replies, and answer questions about the current message.

When you ask for a reply, the pane splits: chat on the left, compose editor on the right. The agent writes a draft in `<reply>` tags, which fills the editor. Edit it, ask for revisions then `Ctrl+D` to send.

The agent runs as a subprocess that can fetch context from my vault. Other agents can use the CLI + the associated SKILL to get current context too `fm inbox`, `fm search`, `fm read`, anything that can shell out can read and reply to email without opening a browser.
