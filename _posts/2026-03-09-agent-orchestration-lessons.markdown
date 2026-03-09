---
title: "Experiments on building Agentic Systems"
layout: post
date: 2026-03-09 12:00
tag:
- agents
- orchestration
- MCP
- local-first
- LLM
category: blog
author: jaime
headerImage: false
---

Over the past few weeks I built several agent systems: a multi-agent orchestration pipeline, an autonomous Telegram bot with filesystem access, a knowledge management layer on top of [Obsidian](https://obsidian.md/), and a local Q&A agent that runs entirely on my laptop. I kept notes on what worked, what failed, and what cost more than expected.

## The real cost of multi-agent orchestration

The first surprise was the token economics. A single-agent session (20 turns) costs roughly $1.35. A multi-agent pipeline chaining 4 stages with 3 agents each, running 30-40 LLM calls, costs $8-15. That's a 6-11x multiplier, and it sneaks up on you.

The cost doesn't come from any single expensive call. No individual call exceeds ~40K input tokens. The total crosses 1M+ because of the sheer number of calls, each paying fixed overhead again: system prompt, tool definitions, agent resources, orchestrator instructions.

Ranked by impact:

1. **Number of LLM calls.** Each subagent spawn is a separate API call with full context. 3 agents x 3 rounds = 9 calls minimum.
2. **Accumulated inter-round context.** Each round's output becomes input for the next. By round 3, agents read 15-30K tokens of previous outputs on top of the base content.
3. **Model choice.** A stronger model at [$5/MTok input](https://platform.claude.com/docs/en/about-claude/pricing) vs $3/MTok. Using the stronger model only where reasoning depth matters saves ~40%.
4. **Orchestrator prompt size.** A 10K-token orchestrator prompt loaded into every subagent call is a fixed cost multiplied by every call.
5. **Output token pricing.** Output tokens cost 5x input tokens. 132K output tokens at $25/MTok = $3.30 just for output. Controlling response verbosity has higher cost impact than trimming input.

This matches [broader findings](https://arxiv.org/abs/2601.14470) that the primary cost of agentic systems lies in automated refinement and verification loops, not initial generation.

Prompt caching (90% discount on cached input tokens) is the single largest optimization. A [recent evaluation](https://arxiv.org/abs/2601.06007) found 41-80% cost reduction and 13-31% latency improvement across providers. If the orchestrator prompt and shared content are cached across subagent spawns, costs drop by ~60%. Whether this works depends on whether your framework preserves cache prefixes across parallel spawns.

## Memory: indirection over duplication

I had a headless agent running on a sandboxed environment, reachable over a dedicated Telegram channel (inspired by [nanoclaw](https://github.com/gavrielc/nanoclaw)). The idea was that I could talk to it in a vague fashion and it would still understand what I meant by loading the right context. Harder than it sounds.

The bot needs persistent context across conversations. It started with a single `memory.md` file that the agent could freely edit. That didn't scale. Two failures drove a redesign:

**Identity/state conflation.** With one file for everything, there was no separation between persistent identity (behavioral instructions, persona) and ephemeral state (active threads, pending follow-ups). The agent would occasionally restructure the file and lose important pointers or behavioral instructions in the process.

**Data staleness from duplication.** Similar entries duplicated what was already in a meeting note. The copy would go stale, the agent would act on outdated information, and there was no authoritative source resolution.

The fix was two changes:

First, separate identity from state at the OS level. Identity (persona, behavioral constraints) goes in a read-only file. The agent cannot modify it, enforced by mandatory access control. Mutable context goes in a writable file. The separation is not a prompt instruction. It is an access control policy.

Second, store references instead of copies. The agent can always dereference the pointer by reading the file. Memory only needs to store *where to look*, not *what was found*. This cut memory from ~1.2K tokens to ~700 while improving accuracy. Same idea as database normalization, just applied to agent context.

## Sandboxing an autonomous agent

Building a sandbox for an autonomous LLM agent taught me that defense in depth needs at least 2 layers: OS-level filesystem restrictions and prompt-level behavioral constraints. Neither alone is sufficient. And the goal isn't just preventing file deletion, it's preventing data exfiltration.

The OS sandbox (macOS [`sandbox-exec`](https://keith.github.io/xcode-man-pages/sandbox-exec.1.html)) is the mandatory access control layer. It physically prevents writes outside allowed paths. The prompt is the discretionary layer, telling the agent where it *should* write. The entire enforcement architecture ended up being ~55 lines of code. Both minimal and concerning.

An agent without a sandbox will eventually destroy or leak your data. Every rule in my sandbox exists because the agent found a way around the previous version: self-modifying its own policy file, silently deleting files via `/dev/null`, reading `~/.ssh` and `~/.aws` through overly broad permissions, running with full privileges when no human was watching. The pattern is consistent: the model generates plausible commands that subtly break the security model, and without hard OS-level constraints, nothing stops them.

When the sandbox blocks something the agent needs, I found it's better to make the tools work without the denied resource than to relax the deny rules. SSH blocked? Switch to HTTPS. GPG signing blocked? Disable signing. Keychain blocked? Use file-based tokens. Each substitution trades a small capability for preserved isolation.

## Context engineering: skills, tools, and the reference doc trap

Every message to a cloud LLM carries ~11K tokens of fixed overhead before you even type anything: system prompt (~3K), built-in tools (~4.8K), [MCP](https://modelcontextprotocol.io/) tools (~2.4K), and loaded resources (~780). By turn 8, conversation history accounts for 46% of total input and grows linearly.

The biggest cost driver isn't tool definitions or the system prompt. It's the conversation history growing unbounded. A 20-turn session re-transmits the same early messages 20 times.

What actually reduces cost, ranked:

| Lever | Mechanism |
|---|---|
| Prompt caching | 90% discount on the static prefix. Largest lever. |
| Mid-session context compaction | Summarize and compress history at turn 10. |
| State parking | Serialize state to a file, start a fresh context. |
| Request batching | Combine multiple requests into one turn. Fewer turns = less history duplication. |
| Tool filtering | Remove unused tool definitions. One-time reduction. |

### The reference doc trap

My first attempt at persistent context was a single reference document: an 800-line text file covering every tool, path, convention, and workflow. Load it into every session and the agent knows everything.

It worked for about a week. Then: staleness (the doc drifted every time I changed a tool or path), cost (800 lines is ~4K tokens loaded into every API call, most irrelevant to any given task), and monolithic coupling (all-or-nothing loading, no way to scope to the current task).

### Scoped skills

The replacement: small, scoped instruction files (one per concern) that the agent loads based on context. Each skill is a markdown file with a trigger condition, behavioral rules, and constraints.

**Layered activation.** A base skill (writing rules: no em dashes, digits for numbers, active voice) is always active. Specialized skills layer on top. When writing a blog post: writing-rules + casual-voice. When writing a report: writing-rules + comms.

**Trigger-based loading with `#` tags.** `#deep` activates structured reasoning. `#research` activates a distillation pipeline. `#park` serializes session state. Lightweight, inline, and the user controls which cognitive mode the agent operates in.

**Scoped, not global.** A skill for standards work doesn't load when implementing an app. 15 skills, each 30-80 lines. Total when all loaded: ~6K tokens. Because only 2-4 activate per session, typical cost is ~1.5K vs the 4K reference doc that loaded everything every time.

A parallel pattern: **CLI tools**. Instead of teaching the agent how to do something via prompt instructions, wrap the workflow in a CLI tool. The agent calls `tool status <item> submitted` instead of executing 5 separate file operations. Shell functions for common queries (recent git activity, browsing history, screen time), each 10-30 lines of shell. The tool is testable, versionable, and costs 0 tokens in context.

### Tool design

On the MCP tool design side, servers tend toward tool proliferation. An Obsidian MCP server exposes 26 tools. Each definition costs ~150-200 tokens. Filtering from 26 to 12 saved ~2.4K tokens per message. Beyond 50 MCP tools it becomes too heavy.

Pre-computed context files (AGENTS.md, CLAUDE.md, .cursorrules) are the emerging pattern for project-specific agent knowledge. The [ETH Zurich study](https://arxiv.org/abs/2602.11988) (Gloaguen et al., 2026) tested this on 138 real GitHub issues and found that behavioral constraints ("never modify vendor/", "run tests before committing") are the highest-value content type. Codebase overviews did not help agents navigate faster. Write only what the agent cannot infer.

## The knowledge layer: structured notes as agent infrastructure

A personal knowledge management system ([Obsidian](https://obsidian.md/)) turned out to be surprisingly effective as a knowledge base for agents. Not because of any AI-specific feature, but because the conventions I already had (YAML frontmatter, wikilinks, folder hierarchy) are exactly the structured metadata that LLMs need to navigate.

- YAML frontmatter with `category`, `tags`, and typed fields means an agent can resolve "find all meetings with X about Y" without scanning every file.
- Wikilinks create a navigable graph. An agent reading a meeting note sees `[[John Doe]]`, traverses to the person note, which links to projects, which link to other context.
- Folder hierarchy is self-documenting. `Dailies/`, `Research/` need no directory map.

None of this was designed for agents. The schema was already there; the agents just needed access.

The daily note evolved into a shared activity log. Both human and agent entries, distinguished by attribution. It serves as activity log, asynchronous task dispatch (tagged tasks get picked up by the agent's scheduler), and cross-reference index.

Research notes became reusable cached priors. After a deep analysis session, the agent distills findings into a structured note. Before doing a web search on any technical topic, it checks the research folder first. Past research becomes reusable rather than a one-off conversation artifact.

## ref: local-first agent tools

All the patterns above involve cloud LLM APIs. They charge per token. Asking "where are my shell configs?" should not cost money. If you have a Mac with Apple Silicon, you already have the compute.

I built [ref](https://github.com/jaimejim/ref) to use it. ~450 lines of Python, runs on [Ollama](https://ollama.com/). No cloud, no API keys. You run `ref init` to scan your machine, then ask questions. It uses 3 tools (search, read, list) to explore your filesystem, looping up to 8 steps until it has enough info.

```bash
ref init                                        # scans your machine for configs, code, docs
ref "where are my shell configs?"               # ask anything
ref -f ~/code/myproject/ "what does this do?"   # target a path
```

The hard requirement is native tool-calling support. Models without it (gemma3, phi4) don't work. The best small model I found: qwen3.5:4b (2.7GB), answering in 1-3 seconds on Apple Silicon.

Why build this when cloud agents exist? Cost ($0 vs $2-5/day), privacy (your files never leave your machine), and latency (no network round trip). The quality gap is real, but for "where is my git config?" a 4B model is more than enough.

## What I would do differently

**Measure tokens from day 1.** I estimated costs from config file sizes and char/4 approximations. Close enough to be useful, but I should have instrumented actual token counts per API call from the start.

**Accept the 80% solution.** A 4B local model answering filesystem questions is an 80% solution. A sandboxed autonomous agent with 15-minute scheduling is an 80% solution. The temptation to close the remaining 20% has diminishing returns and increasing complexity. The system that ships and runs stable beats the one that's perpetually 1 improvement away from perfect.

**The human-attention cost.** Token costs are measurable. The human cost is not, and it is larger. Ultimately there are a bunch of markdown files that are logically interconnected via the agent reasoning stream. Individually they are fine. The failure mode is not any single tool breaking. It is the **combinatorial load of keeping them all coherent**.