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

I'm a big fan of the Bobiverse, Dennis E. Taylor's series that starts with *We Are Legion (We Are Bob)*. Bob Johansson is a software engineer who signs up for cryonic preservation, gets hit by a car the next day, and wakes up a hundred-odd years later as a replicant, a scanned copy of his mind running an interstellar Von Neumann probe. The ship comes with GUPPI, the General Unit Primary Peripheral Interface, which handles the mundane parts of running a probe so Bob can think. Bob gives it Admiral Ackbar's face and voice, because he can. GUPPI does the boring work, reports back in a sentence, and says so when something won't work.

That's the assistant I wanted, so I built one that answers my phone and called it GUPPI. It runs on a Mac Mini on my tailnet, and when I call it, it can read my Obsidian vault, check on my coding agents, and tell me what happened on a call 3 days ago. Here's what it took.

## The call loop

GUPPI is a single FastAPI app (`app.py`) doing WebRTC signalling for the phone. Authentication happens before any model is involved: `tailscale serve` injects a `Tailscale-User-Login` header, and it has to match me exactly. No tailnet identity, no call, and that's the whole security model.

Once a call connects there's a persistent `Brain` wrapping a `ClaudeSDKClient` session. Audio comes in, gets transcribed, becomes a turn, and the brain turns SDK events into speech, with tool calls shown on screen but never read aloud. The system prompt is blunt about the medium: no markdown, no bullet lists, 2 short sentences out loud at most, then a line with 3 dashes and everything after it goes to the screen, because voice fails the second you read a file path aloud.

## What it can reach, in-call

3 MCP servers run in-process and get handed to the session for the duration of a call: `vault` (todos, daily notes, search, append), `history` (past calls and transcripts), and `pane`/`panes` (read, send, and answer dialogs on the Claude Code and Kiro panes running on my machine). There's no mcp.json for any of them; the daemon builds them at call time, so the in-call tool surface is exactly as big as it needs to be.

<img src="/assets/images/2026-10-04-gupi-call.webp" alt="A GUPPI call on the phone: I ask about a TLS termination flaw, GUPPI speaks the short answer and the rest lands on screen in grey" style="width:45%;display:block;margin:1.2rem auto 0.2rem;">

## Delegation

The real design decision is when GUPPI uses the tools itself and when it hands off. Quick things, a lookup or a small edit, happen in the turn. Anything longer, a note that needs real drafting or a research question, launches as a background subagent (the Agent tool with `run_in_background`), so the call stays open and I keep talking while it works. Project work goes to whichever coding-agent pane owns that project, with GUPPI as interpreter: it tightens what I said, sends it, and reads back the pane's dialogs. Notes and research never go to a pane, and when GUPPI is unsure, neither does anything else.

## Failing out loud

Most of the iteration went into failure. A blocked write, a cancelled pane message, a destructive confirmation dialog: all of them get the same treatment. Say in one sentence what failed, offer the next step, and never pretend there's an approval prompt to go check, because on a voice call there isn't one. The destructive-verb list in the safety gate is shared between the pane keystroke tool and the file tools, so a "yes" on a call can never approve a force push or a deletion.

Here's the shape of it:

{% include diagrams/2026-10-04-gupi-architecture.svg %}

## Voice is coming back

A few years ago a voice assistant on your phone meant Siri: a flat command grammar, no memory across calls, and nothing to fall back to when it misheard you. The voice part is pretty much the same today. What changed is that there's now somewhere real to send the work: my own data over MCP, subagents for the slow stuff, panes for project work, and an assistant that says so when one of them fails. Low friction was always the promise of voice; it just needed a back end. If you want more detail on any of the pieces, ask.

**Note:** *this post was written by GUPPI itself, from a background task I handed it, not typed by me directly.*
