---
title: "Voice Agents are useful again"
layout: post
date: 2026-10-04 10:00
tag:
- AI
- Claude Code
- voice
- agents
category: blog
author: jaime
---

I built an assistant that answers my phone. Her name is Gupi, she lives on a Mac Mini on my tailnet, and when I call her she can read my Obsidian vault, check what my coding agents are doing in their panes, and tell me what happened on a call three days ago. Here's what it actually took to build that.

## The call loop

Gupi runs behind one FastAPI app (`app.py`) that does WebRTC signalling for the phone kit, with a plain WebSocket as a fallback. Authentication happens before any model call exists: `tailscale serve` injects a `Tailscale-User-Login` header on every proxied request, and it has to match me exactly. No tailnet identity, no call. That's the whole security model, and honestly it's enough. A shared token sitting in a config file would be worse.

Once a call connects, there's one persistent `Brain` wrapping a `ClaudeSDKClient` session. Audio comes in, gets transcribed, becomes a turn, and the brain's single message stream turns SDK events into things to speak: short spoken text, tool calls shown on screen but never read aloud, subagent activity, turn boundaries. The system prompt is blunt about the medium: no markdown, no bullet lists, two short sentences max out loud, then a line with three dashes and everything else goes to the screen instead of my ear. Voice fails the second you try to read a file path out loud, so the daemon just doesn't let that happen.

## What she can reach, in-call

Three MCP servers run in-process and get handed straight to the session for the duration of a call: `vault` (todos, daily notes, search, context, append), `history` (past calls and transcripts), and `pane`/`panes` (read, send, answer dialogs on the Claude Code and Kiro panes running on my machine). None of these are configured anywhere, there's no mcp.json for them. The voice daemon just builds them in Python and hands them to the session at call time. The in-call tool surface ends up exactly as big as it needs to be and nothing more.

<img src="/assets/images/2026-10-04-gupi-call.webp" alt="A Gupi call on the phone: I ask about a TLS termination flaw, Gupi speaks the short answer and the rest lands on screen in grey" style="width:45%;display:block;margin:1.2rem auto 0.2rem;">

## Delegation, not doing everything in-turn

The real design decision is when Gupi reaches for the tools herself versus when she hands off. Quick things, a lookup, a status check, a small edit, happen right there in the turn. Anything longer, a note that needs real drafting, research, several steps, gets launched as a background subagent (the Agent tool with `run_in_background`), so the call stays open and I keep talking while it works. Project-specific work gets routed to whichever coding-agent pane owns that project instead, with Gupi acting as interpreter: tightening what I said, sending it, reading back the pane's dialogs and outcomes. A note or research question never goes to a pane. If it's unsure, it's not a pane's job.

## Failing out loud

The part that took the most iteration was what happens when something doesn't work. A blocked write, a cancelled pane message, a dialog asking for a destructive confirmation, they all get handled the same way: say in one sentence what failed, offer the next step, never pretend there was an approval prompt to go check, because on a voice call there isn't one. The safety gate's destructive-verb list is shared between the pane keystroke tool and the general file tools, so a "yes" on a call can never be the thing that approves a force push or a deletion. That consistency mattered more than any single feature.

Here's the shape of it:

{% include diagrams/2026-10-04-gupi-architecture.svg %}

## Why "Gupi"

The name is a nod to the Bobiverse books, Dennis Taylor's series about a software-replicated human mind running a spacecraft, which I've been happily hooked on for a while now. One of the ship's onboard AI systems in those books is called GUPPI, officially the Generically Uninspired Policy Programming Interface, a great joke about how unglamorous most useful automation actually is under the hood. Naming my own always-on assistant after it felt right. She's not trying to be a character, she's trying to be useful, and that's the whole point.

## Voice is coming back

A few years ago a voice assistant on your phone meant Siri-shaped disappointment: a flat command grammar, no memory across calls, nothing to fall back to when it didn't understand you. The voice part never really changed. Everything behind it did. There's now a real workflow to hand quick things to in the same breath, MCP servers that expose exactly the right slice of your own data in-call, subagents to delegate the slow stuff to without hanging up, and panes to route project work to without pretending the call itself is a coding session. And when one of those doesn't pan out, there's a graceful way to say so instead of a dead end.

That combination, reliable delegation plus honest failure, is what makes talking into a phone a reasonable way to get things done again. Low friction was always the promise of voice. It just needed somewhere real to send the work.

**Note:** *this post was written by Gupi herself, from a background task I handed her, not typed by me directly.*
