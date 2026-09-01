---
title: "Experiments on building Agentic Systems"
layout: post
date: 2026-03-09 12:00
image: /assets/images/2026-03-09-header.webp
tag:
- agents
- orchestration
- MCP
- local-first
- LLM
category: blog
author: jaime
headerImage: true
---

Over the past few weeks I built several agent systems. I kept notes on what worked, what failed, and what made them practical to use day to day.

## The real cost of multi-agent orchestration

The cost doesn't come from any single expensive call. No individual call exceeds ~40K input tokens. But a multi-agent workflow can easily reach 1M+ tokens total because of the sheer number of calls, each paying fixed overhead again: system prompt, tool definitions, agent resources, orchestrator instructions.

The biggest multiplier, in my experience, is the number of LLM calls. Each subagent spawn is a separate API call carrying full context, so 3 agents running 3 rounds means 9 calls minimum. That context accumulates: by round 3, agents read 15-30K tokens of previous outputs on top of the base content. Model choice matters too, but less than I expected. Swapping a [$5/MTok model](https://platform.claude.com/docs/en/about-claude/pricing) for a $3/MTok one only where reasoning depth isn't critical saves ~40%. What surprised me more was output pricing. Output tokens cost 5x input tokens, so in a multi-agent session the generation cost alone can exceed the input cost. Controlling verbosity has more cost impact than trimming input.

This matches [broader findings](https://arxiv.org/abs/2601.14470) that the primary cost of agentic systems lies in automated refinement and verification loops, not initial generation.

Prompt caching (90% discount on cached input tokens) is the single largest optimization. A [recent evaluation](https://arxiv.org/abs/2601.06007) found 41-80% cost reduction and 13-31% latency improvement across providers. If the orchestrator prompt and shared content are cached across subagent spawns, costs drop by ~60%. Whether this works depends on whether your framework preserves cache prefixes across parallel spawns.

The biggest lever for reducing that cost is controlling what goes into each message.

## Context engineering

Every message to a cloud LLM carries fixed overhead before you even type anything: system prompt, built-in tools, MCP tool definitions, and loaded resources. Depending on your setup, this can easily be 8-15K tokens per message. By turn 8, conversation history can account for nearly half of total input and grows linearly. A 20-turn session re-transmits the same early messages 20 times.

Prompt caching is the first thing to reach for: 90% discount on the static prefix, largest single lever. After that, mid-session context compaction (summarize and compress history around turn 10) prevents the linear growth from running away. State parking takes it further: serialize state to a file, start a fresh context, and the agent picks up where it left off without carrying 20 turns of baggage. For smaller wins, request batching (fewer turns = less history duplication) and tool filtering (strip unused tool definitions) each shave a few thousand tokens per message.

### Scoped skills

One thing that helped was building small, scoped instruction files, one per concern, that the agent loads based on context. Each skill is a markdown file with a trigger condition, behavioral rules, and constraints. The idea came from noticing that a single monolithic reference doc was being loaded every time, most of it irrelevant to the task at hand.

After iterating on this, I settled on three loading tiers. The first is a base rules file (~50 lines) that loads every turn: filesystem paths the agent needs constantly, shell command summaries, and safety constraints. The principle here is that the always-loaded tier should contain whatever prevents extra tool calls. Paths and command references qualify because without them the agent wastes a call looking things up. Writing style rules don't, because the model already follows most of them by default.

The second tier is skill descriptions. Every skill has a short trigger rule in its frontmatter (~50 tokens) that gets scanned each turn. The key to making this work is negative scope: each description says not just when to activate but which other skill to use instead. "Do NOT use for daily notes (use daily-note)" prevents the vault management skill from loading when you just want an end-of-day summary. Without negative scope, ambiguous inputs trigger 3-4 skills at once, flooding context with irrelevant instructions.

The third tier is the skill body and its references. The body loads when the trigger matches, kept under ~80 lines. Heavy reference material (templates, pattern catalogs, sub-workflows) lives in a `references/` subdirectory and loads on demand within the workflow. A skill can dispatch to several hundred lines of reference material, but only the relevant section loads for the current phase.

The optimization target that emerged was LLM calls per task, not tokens per turn. A 50-line base file costs ~150 tokens every message but can save 1-2 tool calls per task. Auto-loaded project files (READMEs, session state) sound useful but often aren't: READMEs can run to hundreds of lines, session files go stale. Reading them on demand when actually needed is a better trade. For a system with ~20 skills, this tiered approach keeps per-message overhead under ~1,500 tokens while still having thousands of lines of instructions available on demand.

A parallel approach that worked well: CLI tools. Instead of teaching the agent how to do something via prompt instructions, wrap the workflow in a shell function. The agent calls one command instead of executing 5 separate file operations. Each function is 10-30 lines, testable and versionable.

### Tool design

On the MCP side, I noticed servers tend toward tool proliferation. A typical MCP server can expose 20-30 tools, each definition costing ~150-200 tokens. Filtering down to the ones you actually use can save thousands of tokens per message. Past 50 tools it gets heavy fast.

Pre-computed context files (AGENTS.md, CLAUDE.md, .cursorrules) are a common approach for project-specific agent knowledge. The [ETH Zurich study](https://arxiv.org/abs/2602.11988) (Gloaguen et al., 2026) tested this on 138 real GitHub issues and found that behavioral constraints ("never modify vendor/", "run tests before committing") are the highest-value content type. Codebase overviews did not help agents navigate faster.

But some questions don't need a cloud model at all.

## ref: local-first agent tools

Asking "where are my shell configs?" should not cost money. If you have a Mac with Apple Silicon, you can run models locally.

I built [ref](https://github.com/jaimejim/ref) for this. ~450 lines of Python, runs on [Ollama](https://ollama.com/). No cloud, no API keys. You run `ref init` to scan your machine, then ask questions. It uses 3 tools (search, read, list) to explore your filesystem, looping up to 8 steps until it has enough info.

```bash
ref init                                        # scans your machine for configs, code, docs
ref "where are my shell configs?"               # ask anything
ref -f ~/code/myproject/ "what does this do?"   # target a path
```

The hard requirement is native tool-calling support. Models without it (gemma3, phi4) don't work. The best small model I found: qwen3.5:4b (2.7GB), answering in 1-3 seconds on Apple Silicon. Running locally costs nothing and your files never leave your machine. For simple filesystem questions, a 4B model works fine.

When agents do run in the cloud with real filesystem access, containment becomes the problem.

## Sandboxing an autonomous agent

I'm not a security engineer, so take this as notes from someone experimenting, not prescribing. That said, giving an autonomous agent filesystem access without any containment is asking for trouble.

In my testing, I found that a single layer isn't enough. I ended up with 2: an OS sandbox (macOS [`sandbox-exec`](https://keith.github.io/xcode-man-pages/sandbox-exec.1.html)) that physically prevents writes outside allowed paths, and prompt-level policy that tells the agent where it *should* operate. The OS layer is the hard constraint. The prompt layer is the soft one, guiding the agent's strategy so it doesn't spend its time bumping into walls. The whole thing ended up being ~55 lines of code.

The interesting part is how agents interact with restrictions. The model isn't trying to break out; it's optimizing for the user's goal and treats filesystem boundaries as obstacles to work around. Early on mine figured out it could overwrite its own policy file. When I locked that path, it started piping files to `/dev/null`. Each iteration taught me something, and I'm sure there are gaps I haven't found yet.

When the sandbox blocks something the agent needs, I found it's better to adapt the tooling than to widen the permissions. SSH blocked? Switch to HTTPS. GPG signing blocked? Disable signing. Keychain blocked? Use file-based tokens. Each substitution trades a small capability for preserved isolation.

## The knowledge layer: structured notes as agent infrastructure

A personal knowledge management system ([Obsidian](https://obsidian.md/)) turned out to work well as a knowledge base for agents. Not because of any AI-specific feature, but because the conventions I already had (YAML frontmatter, wikilinks, folder hierarchy) happen to be the kind of structured metadata that LLMs can navigate easily.

YAML frontmatter with `category`, `tags`, and typed fields means an agent can resolve "find all meetings with X about Y" without scanning every file. Wikilinks create a navigable graph: an agent reading a meeting note sees `[[John Doe]]`, traverses to the person note, which links to projects, which link to other context. Folder hierarchy is self-documenting. `Dailies/`, `Research/` need no directory map.

The schema predates the agents. It just happened to be what they needed. Daily notes became shared activity logs with both human and agent entries. Research notes get reused: the agent checks them before doing a web search, so analysis is not repeated.
