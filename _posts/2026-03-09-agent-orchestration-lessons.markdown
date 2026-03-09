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

Over the past few weeks I built several agent systems: a multi-agent orchestration pipeline, an autonomous Telegram bot with filesystem access (inspired more by [nanoclaw](https://github.com/gavrielc/nanoclaw) than [openclaw](https://github.com/openclaw/openclaw)), a knowledge management layer on top of [Obsidian](https://obsidian.md/), and a local Q&A agent that runs entirely on my laptop. Along the way I kept research notes on what worked, what failed, and what cost more than expected. This post distills those notes into general patterns and techniques.

## The real cost of multi-agent orchestration

The first surprise was the token economics. A single-agent session (20 turns with a cloud LLM) costs roughly $1.35. A multi-agent pipeline that chains 4 stages with 3 agents each, running 30-40 separate LLM calls, costs $8-15. That is a 6-11x multiplier.

The cost does not come from any single expensive call. No individual call exceeds ~40K input tokens. The total crosses 1M+ input tokens because of the sheer number of calls, each paying fixed overhead again: system prompt, tool definitions, agent resources, and the orchestrator's instructions.

Ranked by impact, the cost drivers are:

1. **Number of LLM calls.** Each subagent spawn is a separate API call with full context. 3 agents x 3 rounds = 9 calls minimum.
2. **Accumulated inter-round context.** Each round's output becomes input for the next round. By round 3, agents read 15-30K tokens of previous outputs on top of the base content. This grows linearly.
3. **Model choice.** A stronger model at [$5/MTok input](https://platform.claude.com/docs/en/about-claude/pricing) costs 1.7x more than a capable model at $3/MTok. Using the stronger model only where reasoning depth matters (spec analysis, complex evaluation) and the cheaper model for everything else saves ~40%.
4. **Orchestrator prompt size.** A 10K-token orchestrator prompt loaded into every subagent call is a fixed cost multiplied by every call.
5. **Output token pricing.** Output tokens cost 5x input tokens. 132K output tokens at $25/MTok = $3.30 just for output. Controlling response verbosity has higher cost impact than trimming input definitions.

The per-million pricing that API providers advertise is misleading when you have many small calls. You pay fractions of a cent per call, but 35 calls at $0.25 average = $8.75. This matches [broader findings](https://arxiv.org/abs/2601.14470) that the primary cost of agentic systems lies in automated refinement and verification loops, not initial generation.

Prompt caching (90% discount on cached input tokens) is the single largest optimization opportunity. A [recent evaluation of prompt caching for agentic tasks](https://arxiv.org/abs/2601.06007) found 41-80% cost reduction and 13-31% latency improvement across providers. If the orchestrator prompt and shared content are cached across subagent spawns, costs drop by ~60%. Whether this works depends on whether your framework preserves cache prefixes across parallel spawns, which is worth verifying before assuming savings.

Then again, this is experimentation and I expect for those numbers to be optimized to 1/10x of the cost with some changes.

## Memory: indirection over duplication

I had a headless agent running on a sandboxed environment that I could interact over a dedicated Telegram channel. The goal being me talking in a vague fashion and the agent still understanding what I meant by loading the context. This makes it a bit more complex than normal sessions with other agents and it is also documented by similar projects like [nanoclaw](https://github.com/gavrielc/nanoclaw) or [openclaw](https://github.com/openclaw/openclaw).

The bot needs to keep some sort of context of previous conversations that can be loaded efficiently. It started with a single `memory.md` file that the agent could freely edit. It did not scale. Two failures drove a redesign:

**Identity/state conflation.** With one file for everything, there was no separation between persistent identity (behavioral instructions, persona) and ephemeral state (active threads, pending follow-ups). The agent would occasionally restructure the file and lose important pointers or behavioral instructions in the process.

**Data staleness from duplication.** Similar entries duplicated what was already in a meeting note. The copy would go stale, the agent would act on outdated information, and there was no authoritative source resolution.

The fix was two changes:

First, separate identity from state at the OS level. Identity (persona, behavioral constraints) goes in a read-only file. The agent cannot modify it, enforced by mandatory access control. Mutable context (active threads, pending follow-ups) goes in a writable file. The separation is not a prompt instruction. It is an access control policy.

Second, store references instead of copies, brings the same recall capability, fraction of the token cost, and the authoritative source stays in one place. The agent can always dereference the pointer by reading the file. Memory only needs to store *where to look*, not *what was found*.

This reduced memory from ~1.2K tokens to ~700 tokens while improving accuracy. The pattern is analogous to database normalization: store the fact once, reference it everywhere.

A related pattern that worked well: two-phase retrieval. First, a deterministic scan (no LLM) enumerates recent files, calendar entries, project status. Pure data collection with no risk of hallucinated file names. Then the LLM compresses the retrieved data into structured context under 3KB. The retrieval phase ensures completeness. The synthesis phase ensures conciseness. Structurally similar to RAG but operating over local filesystem state rather than a vector store.

## Sandboxing an autonomous agent

Building a sandbox for an LLM agent that runs autonomously revealed that defense in depth requires at least 2 layers: OS-level filesystem restrictions and prompt-level behavioral constraints. Neither alone is sufficient and it seems an ongoing process. The main point being not just prevent file deletion but data exfiltration.

The OS sandbox (macOS [`sandbox-exec`](https://keith.github.io/xcode-man-pages/sandbox-exec.1.html) in my case) is the mandatory access control layer. It physically prevents writes outside allowed paths. The prompt is the discretionary layer, telling the agent where it *should* write, preventing wasted attempts against the MAC policy. But there is no output validation layer that checks whether what the agent *chose* to write was correct. If it writes malformed content to a note, nothing catches that.

The entire enforcement architecture ended up being ~55 lines of code. Both minimal and concerning.

Every sandbox rule came from a real failure:

**Self-modification.** The agent needed `/dev/null` access for git operations and suggested a sed command to patch the sandbox policy file. The command dropped the glob patterns from the profile, disabling the entire sandbox. Lesson: the agent must never have write access to its own constraint definitions, even indirectly. The model will generate plausible-looking commands that subtly break the security model.

**Silent deletion via /dev/null.** `mv important-file /dev/null` works as a destructive move with no confirmation. Had to wrap `mv` and `cp` with custom scripts that block `/dev/null` as a destination.

**Overly broad read permissions.** Never allow broad access cause you may also expose `~/.ssh`, `~/.aws`, `~/.gnupg`. Fix: targeted deny rules on top of the broad allow. Write allowlisting is intuitive, but read denylisting for sensitive paths is equally necessary. Increase allowlist ONLY when truly required.

**No privilege separation between attended and unattended execution.** When a scheduler runs tasks without a user present, the agent should operate under tighter constraints. Reduced supervision requires reduced privilege.

The operational reality of sandboxing an autonomous agent: access requirements cannot be fully predicted. Start with minimal permissions, expand based on actual failures, and expect each expansion to surface new constraint violations. One task (adding a recipe to a git repo) required 3 separate permission fixes across 3 different sandbox boundaries (write access, `/dev/null`, authentication chain).

A useful principle that emerged: when the sandbox blocks something the agent needs, make the tools work without the denied resources rather than relaxing the deny rules. SSH blocked? Switch to HTTPS. GPG signing blocked? Disable signing. Keychain blocked? Use file-based tokens. Each substitution trades a small capability for preserved isolation and depending on the case it might be sufficient. The implicit tradeoff is spending countless hours adding complexity to the sandbox, which also increases your brain load, thus making it prone to errors. I prefer to keep it very simple and understandable.

## Context engineering: skills, tools, and the reference doc trap

Every message to a cloud LLM carries ~11K tokens of fixed overhead before the user types anything: system prompt (~3K), built-in tools (~4.8K), [MCP](https://modelcontextprotocol.io/) tools (~2.4K), and loaded resources (~780). By turn 8, conversation history accounts for 46% of total input and grows linearly. Every turn re-sends all prior turns.

The biggest cost driver is not tool definitions or the system prompt. It is the conversation history growing unbounded. A 20-turn session re-transmits the same early messages 20 times.

What actually reduces cost, ranked:

| Lever | Mechanism |
|---|---|
| Prompt caching | 90% discount on the static prefix. Largest lever. |
| Mid-session context compaction | Summarize and compress history at turn 10. |
| State parking | Serialize state to a file, start a fresh context. |
| Request batching | Combine multiple requests into one turn. Fewer turns = less history duplication. |
| Tool filtering | Remove unused tool definitions. One-time reduction. |

### The reference doc approach (and why it breaks)

My first attempt at giving agents persistent context was a single reference document: an 800-line text file covering every tool, path, convention, and workflow in the system. 16 sections, table of contents, ASCII diagrams. The idea was simple: load this file into every agent session and the agent knows everything.

It worked for about a week. Then 3 problems appeared:

1. **Staleness.** The reference doc was a snapshot. Every time I added a tool, changed a path, or modified a workflow, the doc drifted. Updating it was manual and I forgot more often than I remembered.
2. **Cost.** 800 lines is ~4K tokens loaded into every single API call. Most of it irrelevant to any given task. An agent writing a blog post does not need the sandbox policy or the deployment workflow.
3. **Monolithic coupling.** One file meant all-or-nothing. I could not give the agent just the parts relevant to the current task without manually extracting sections.

The reference doc is the "god object" of agent context. It works when the system is small and stable. It collapses under change.

### Skills as modular behavioral units

The replacement was a skill system: small, scoped instruction files (one per concern) that the agent loads based on context. Each skill is a markdown file with a trigger condition, behavioral rules, and constraints.

The key design choices:

**Layered activation.** A base skill (writing rules: no em dashes, digits for numbers, active voice) is always active beneath everything else. Specialized skills layer on top. When writing a blog post, the agent loads writing-rules + casual-voice. When writing a professional report, writing-rules + comms. The base layer enforces consistency; the top layer sets tone.

**Trigger-based loading with `#` tags.** Some skills activate on explicit user triggers: `#deep` activates structured reasoning (extract requirements, identify risks, check contradictions before generating). `#research` activates a distillation pipeline that stores findings as structured notes. `#park` serializes session state to a file for cross-session persistence. The `#` convention is lightweight (type it inline in any message) and gives the user explicit control over which cognitive mode the agent operates in.

**Scoped, not global.** A skill for writing patent disclosures does not need to load when the agent is deploying an app. A skill for app deployment does not need to load during a research session. Scoping skills to their domain keeps per-message overhead low and prevents behavioral interference between unrelated concerns.

The practical result: 15 skills, each 30-80 lines, covering writing, deployment, research, reasoning, knowledge management, and domain-specific workflows. Total token cost when all are loaded: ~6K. But because only 2-4 activate per session, the typical cost is ~1.5K. Compare that to the 4K reference doc that loaded everything every time.

### CLI tools as agent infrastructure

A parallel pattern emerged with CLI tools. Instead of teaching the agent how to do something via prompt instructions, wrap the workflow in a CLI tool and give the agent the tool.

Examples from my setup:

- A lifecycle management CLI that handles status transitions, file generation, and cross-system sync for a document workflow. The agent calls `tool status <item> submitted` instead of executing 5 separate file operations.
- A reference tool (`ref`) that wraps local Q&A into a single command. The agent does not need to know about Ollama, model selection, or path scanning.
- Shell functions for common queries: recent git activity, browsing history search, screen time. Each is 10-30 lines of shell. Each replaces a multi-step prompt instruction.

The pattern: if you find yourself writing the same 5-step prompt instruction repeatedly, wrap it in a CLI tool. The tool is testable, versionable, and costs 0 tokens in context (the agent just calls it). The prompt instruction is none of those things.

The combination of skills + CLI tools is where the real leverage is. Skills define *how* the agent should behave. CLI tools define *what* the agent can do. Together they replace the monolithic reference doc with composable, scoped, maintainable pieces.

### Tool design and consolidation

On the [MCP](https://modelcontextprotocol.io/) tool design side, servers tend toward tool proliferation. An Obsidian MCP server exposes 26 tools. Each tool definition costs ~150-200 tokens in context window overhead. Most are never invoked. Filtering from 26 to 12 saved ~2.4K tokens per message, real but modest.

The deeper question: could 12 separate tools be consolidated into 5-6 with mode parameters? Fewer tools means less context overhead, but more complex tool schemas might degrade model tool-selection accuracy. This is an open design question with no clear answer yet.

Pre-computed context files (AGENTS.md, CLAUDE.md, .cursorrules) are the emerging pattern for giving agents persistent, project-specific knowledge. The [ETH Zurich study](https://arxiv.org/abs/2602.11988) (Gloaguen et al., 2026) tested this rigorously on 138 real GitHub issues:

- Human-written context files: +4% success rate, +19% cost
- LLM-generated context files: -3% success rate, +20-23% cost
- Agents faithfully follow context file instructions (tool usage jumps from ~0 to 1.6 calls/instance when mentioned)
- LLM-generated overviews are redundant with existing docs

The takeaway: behavioral constraints ("never modify vendor/", "run tests before committing") are the highest-value content type. Codebase overviews do not help agents navigate faster. Write only what the agent cannot infer.

## The knowledge layer: structured notes as agent infrastructure

A personal knowledge management system (I use [Obsidian](https://obsidian.md/)) turned out to be a surprisingly effective knowledge base for LLM agents. Not because of any AI-specific feature, but because its existing conventions provide exactly the structured metadata and navigable graph that LLMs need.

What makes it work:

- YAML frontmatter with `category`, `tags`, and typed fields enables structured metadata queries. An agent can resolve "find all meetings with X about Y" without scanning every file.
- Wikilinks create a navigable knowledge graph. An agent reading a meeting note sees a person link and can traverse to the person note, which links to projects, which link to other context. The graph provides contextual navigation.
- Folder hierarchy is self-documenting. `Dailies/`, `Research/` need no explicit directory map.

None of this was designed for agents. The schemas, link conventions, and folder hierarchy all predate any AI integration. A well-structured PKM system turned out to be a well-structured knowledge base for LLMs. The schema was already there; the agents just needed access.

The daily note evolved from a personal journal into a shared activity log. Both human and agent entries, distinguished by attribution. It now serves 3 roles: activity log (visibility into what the agent did), asynchronous task dispatch (tagged tasks get picked up by the agent's scheduler), and cross-reference index (temporal index of all activity regardless of authorship).

Research notes became reusable cached priors. After a deep analysis session, the agent distills findings into a structured note with frontmatter, cross-references, and open questions. Before performing a web search on any technical topic, the agent checks the research folder first. If a verified note exists, it uses that as the primary source. Past research becomes reusable rather than a one-off conversation artifact.

The inherent tension: the more agents use the knowledge base, the more important structural consistency becomes. But the agents are also the ones maintaining that structure. This is a positive feedback loop when it works and a schema corruption risk when the agent gets a convention wrong.

## ref: the case for local-first agent tools

All the patterns above involve cloud LLM APIs. They charge per token. Asking "where are my shell configs?" should not cost money.

If you have a Mac with Apple Silicon (or any machine with a GPU), you already have the compute. I built [ref](https://github.com/jaimejim/ref) to use it.

`ref` is a local, agentic Q&A tool for your computer. ~450 lines of Python. Runs on [Ollama](https://ollama.com/). No cloud, no API keys, no token costs.

```bash
ref init                          # scans your machine for configs, code, docs
ref "where are my shell configs?"  # ask anything
ref -f ~/code/myproject/ "what does this do?"  # target a path
cat ~/.zshrc | ref "what aliases do I have?"   # pipe support
```

The architecture is simple:

1. `ref init` scans your machine for common locations (shell configs, code dirs, documents).
2. You ask a question. The model gets your configured paths as context.
3. It uses 3 tools (search, read, list) to explore your filesystem, deciding what to look at.
4. It loops up to 8 steps until it has enough info, then answers.

No embeddings, no vector DB, no indexing. The model explores your filesystem with tools, the same agentic pattern as the cloud tools, just running locally on Ollama.

The tool functions are sandboxed to configured paths. `ref` never writes, modifies, or deletes files. The `-f` flag bypasses sandboxing for the path you explicitly provide, which is the right tradeoff: explicit user intent overrides the default restriction.

I tested 7 models for tool-calling compatibility:

| Model | Size | Quality |
|---|---|---|
| qwen3.5:4b | 2.7GB | Very good, best small model |
| qwen3:4b | 2.5GB | Good |
| granite4:3b | 2.1GB | Decent, smallest that works |
| glm-4.7-flash-64k | 19GB | Excellent, 64k context |
| gpt-oss | 13GB | Good |

Models without tool-calling support (gemma3, phi4) do not work. Tool calling is the hard requirement. The model needs to decide when to search, what to read, and when it has enough information to answer. Without native tool-calling support, the agent loop breaks.

The key design choice: using Ollama's [native tool-calling SDK](https://docs.ollama.com/capabilities/tool-calling) instead of prompt-engineering tool use. The SDK handles the tool call/response protocol. The agent loop is ~60 lines. The tool functions are ~80 lines. The rest is CLI scaffolding and init.

Why build this when cloud agents exist? Three reasons:

1. **Cost.** Asking 50 questions a day about your own files should cost $0, not $2-5.
2. **Privacy.** Your shell history, git configs, and project files never leave your machine.
3. **Latency.** A 2.7GB model on Apple Silicon answers in 1-3 seconds. No network round trip.

The quality gap between a 4B local model and a cloud model is real. The local model will not write you a research paper. But for "where is my git config?", "what shell plugins do I use?", "what does this project do?", the 4B model is more than sufficient. Match the tool to the task.

## The human-attention cost

Token costs are measurable. The human cost is not, and it is larger. Ultimately there are a bunch of markdown files that are logically interconnected via the agent reasoning stream. Individually they are fine. The failure mode is not any single tool breaking. It is the **combinatorial load of keeping them all coherent**. A schema change in the vault's frontmatter means updating 4 skills, 2 agent configs, and the Dataview queries. A new sandbox rule means testing it against 3 different execution contexts (interactive, scheduled, SSH). A new research note means verifying it does not contradict 8 existing notes. The individual tasks take minutes. The cognitive overhead of tracking which tasks exist takes longer.

Some specific costs I did not anticipate:

**Monitoring an autonomous agent.** When the bot runs tasks on a 15-minute scheduler, you check what it did. You review the daily note for malformed entries. You scan git diffs for unexpected changes. You verify the sandbox held. This is not optional. An unmonitored autonomous agent is a liability. The monitoring cost scales with the agent's autonomy, not with the task complexity.

**Debugging across abstraction layers.** When a tool call fails, the cause could be in the model's reasoning, the tool function, the MCP transport, the sandbox policy, the filesystem permissions, or the underlying CLI binary. A single "permission denied" error required tracing through 4 layers to find that `sandbox-exec` was blocking `/dev/null` access needed by `git commit`. Each layer is simple. The debugging surface area is the product of all layers.

**Maintaining prompt/code coherence.** The agent's behavior is split between code (sandbox rules, tool functions, scheduler logic) and prompts (system prompts, skill files, orchestrator instructions). When you change one, you need to verify the other still makes sense. There is no type checker for prompt-code interfaces. The only validation is running the agent and observing what happens.

**The "one more tool" trap.** Every problem looks solvable with one more small CLI, one more skill file, one more MCP server. Each addition is justified. The accumulation is not. I went from 0 to 15 skills and 25+ MCP tools in 6 days. Each solved a real problem. The aggregate system became harder to reason about than any individual problem it solved.

The honest assessment: for a single person running agents as a productivity multiplier, the system works when everything is stable. The cost hits when you are actively building and iterating. The build phase demands more attention than the tasks the agents are supposed to handle. Whether the investment pays off depends on how long the stable phase lasts before the next round of changes.


## What I would do differently

**Measure tokens from day 1.** I estimated costs from config file sizes and char/4 approximations. Directionally correct, but I should have instrumented actual token counts per API call from the start.

**Start with 3 skills, not 15.** The skill system is the right architecture. But I wrote 15 skills in 6 days, which meant constant churn as I figured out the right boundaries. Start with writing-rules (always-on base layer), 1 domain skill, and 1 workflow skill. Add more only when you hit a concrete failure that a new skill would prevent.

**Build the CLI tools first, then the agent.** I built the agent and then wrapped repeated prompt patterns into CLI tools after the fact. The reverse order is better: build the CLI tool, verify it works standalone, then give the agent access. The tool is easier to debug in isolation than embedded in an agent loop.

**Separate build phase from use phase.** The build phase (writing skills, configuring sandboxes, testing models, iterating on memory architecture) is high-attention, high-cost work. The use phase (agent runs tasks on a schedule, you review results) is low-attention. I mixed them, which meant I was simultaneously building and relying on the system. Dedicate a week to building, then switch to using. Do not iterate on the foundation while standing on it.

**Accept the 80% solution.** A 4B local model answering filesystem questions is an 80% solution. A sandboxed autonomous agent with 15-minute scheduling is an 80% solution. The temptation to close the remaining 20% (better model, tighter sandbox, more skills) has diminishing returns and increasing complexity. The system that ships and runs stable beats the system that is perpetually 1 improvement away from perfect.
