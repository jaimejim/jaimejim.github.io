---
title: "Emails, vCons, and the Knowledge Base Problem"
layout: post
date: 2026-03-16 08:00
tag:
- agents
- email
- vCon
- knowledge-base
- Obsidian
- LLM
category: blog
author: jaime
headerImage: false
---

Agents will need to work with human conversation data. Emails, call transcripts, chat logs. The naive approach is to dump everything into the LLM's context window and hope for the best. That doesn't scale, and it's expensive. The better approach is to build a knowledge base first, then let the agent query it.

## What emails actually are

An email is a structured object defined by [RFC 5322](https://www.rfc-editor.org/rfc/rfc5322) (and its MIME extensions in [RFC 2045](https://www.rfc-editor.org/rfc/rfc2045)). It has headers (From, To, Date, Subject, Message-ID, In-Reply-To, References) and a body. The headers carry metadata that encodes relationships: who talked to whom, when, and which messages form a thread. The References header is a linked list of Message-IDs that traces a conversation back to its origin.

This structure is already a graph. Every email points to its parent, every thread is a chain, every participant is a node. But most email clients flatten this into a chronological list, and most agents treat emails as bags of text.

## What vCons are

A [vCon](https://datatracker.ietf.org/doc/draft-ietf-vcon-vcon-container/) (Virtualized Conversation) is a container format for conversation data being standardized at the IETF. Where email captures asynchronous text exchanges, vCons capture synchronous conversations: voice calls, video meetings, chat sessions. A vCon packages the recording, transcript, participants, timestamps, and analysis (sentiment, summary, action items) into a single signed JSON object.

Think of it as: email is the letter, vCon is the phone call. Both are conversation records. Both have structured metadata. Both are terrible to search through at scale.

The [vCon community](https://www.vonevolution.com/spring26vcon) (Jeff Pulver's crowd, Vonage, Vconic) is pushing these as "robot food for AI," which is the right framing. Raw audio is useless to an agent. A structured vCon with transcript, participants, and timestamps is something an agent can actually reason over.

## The token problem

Here's the math. A typical corporate email thread runs 2-5K tokens. A 30-minute call transcript runs 8-15K tokens. An agent trying to understand a customer relationship might need to review 50 emails and 10 calls. That's 100K-225K tokens of raw conversation data, before system prompt, tools, or instructions.

At [$3-15/MTok](https://platform.claude.com/docs/en/about-claude/pricing) for input, that's $0.30-$3.40 per query. Run that 100 times a day across a team and you're burning real money on context that's 90% irrelevant to the question being asked.

The problem isn't reading the data. The problem is knowing which 3 emails and 1 call transcript actually matter for the question "what did we agree on pricing with Acme Corp?"

## Building a knowledge base to reduce tokens

The solution is a distillation layer between raw conversation data and the LLM. Instead of feeding the agent 200K tokens of emails, you build a knowledge base that captures the entity relationships, key decisions, and conversation threads in a structured, navigable form. The agent queries the knowledge base, finds the 3-5 relevant items, and only then reads the full content.

This is what I've been experimenting with using [Fastmail's CLI tool](https://github.com/fastmail/fm) (`fm`) and Obsidian.

### The fm experiment

`fm` gives you programmatic access to your Fastmail mailbox. You can search, fetch, and process emails from the command line. The experiment was simple: pull emails by thread or participant, extract the key entities (people, companies, decisions, dates, action items), and write them into Obsidian as linked notes.

The pipeline looks like this:

1. `fm` fetches emails matching a query (sender, thread, date range)
2. The agent reads the raw emails and extracts: participants, topics, decisions, action items, references to other threads
3. Each entity becomes a linked note: `[[Acme Corp]]`, `[[Jane Smith]]`, `[[Project Alpha]]`
4. The email summary goes into a daily note or meeting note with wikilinks to all entities
5. Next time the agent needs context on Acme Corp, it reads the `[[Acme Corp]]` note, follows links to related conversations, and only fetches the 2-3 full emails that matter

The token reduction is dramatic. Instead of 200K tokens of raw email, the agent reads maybe 2K tokens of linked notes to understand the relationship graph, then 5-10K tokens of the specific emails it needs. That's a 10-20x reduction.

### Obsidian as the distilled knowledge base

My [Obsidian vault](https://jaime.win/obsidian-q-chat-notes/) already works this way for IETF meetings, research, and daily work. The agent navigates it by following wikilinks: a meeting note links to `[[Person Name]]`, which links to their company, their drafts, their previous conversations. The vault is a graph of entity relationships that the agent traverses instead of re-reading raw source material.

What the `fm` experiment showed is that the same pattern works for email. The vault becomes the distilled memory layer:

- **People notes** accumulate context across emails, calls, and meetings. The agent reads one note instead of scanning 50 emails to understand a relationship.
- **Project notes** track decisions and action items extracted from conversations. The agent checks the project note before searching email.
- **Daily notes** capture what happened chronologically, with links to the entities involved. The agent can reconstruct a day's context from a single file.

The wikilink graph is the key. It's what lets the agent do 2-hop lookups ("find all conversations with people from Acme Corp about pricing") without scanning every email in the mailbox.

## vCons fit the same pattern

vCons slot into this pipeline naturally. A call transcript gets the same treatment as an email thread: extract participants, decisions, action items, and write linked notes. The vCon's structured metadata (participants, timestamps, analysis) makes extraction easier than email, where you're parsing unstructured text.

The combination would look like: `fm` for email, a vCon processor for calls, both feeding into the same Obsidian knowledge graph. The agent doesn't care whether a decision came from an email or a phone call. It follows `[[Acme Corp]]` → `[[Pricing Discussion 2026-03-10]]` and gets the context it needs.

Henk Birkholz's [Verifiable Agent Conversation Records](https://datatracker.ietf.org/doc/draft-birkholz-verifiable-agent-conversations/) draft (presented at IETF 125 DISPATCH this morning) adds another layer: tamper-evident logs of what agents themselves did. So you'd have human conversations (email, vCon) feeding into a knowledge base, agents querying that knowledge base and acting, and verifiable records of those agent actions feeding back in. The full loop.

## What's missing

The tooling to do this end-to-end doesn't exist yet. `fm` gives you email access. vCon gives you a container format. Obsidian gives you the knowledge graph. But the extraction pipeline (conversation → structured entities → linked notes) is still manual or semi-automated with LLM calls.

What would make this real:

- A standard way to express entity relationships extracted from conversations (not just NER, but "X agreed to Y with Z on date D")
- Incremental updates: new emails and calls should update existing entity notes, not create duplicates
- Bidirectional links from the knowledge base back to source material, so the agent can always drill down to the original email or call recording when it needs full context

The pattern is clear though. Raw conversation data is too expensive and too noisy to feed directly to agents. A distilled knowledge base with entity relationships, navigable via links, is the right intermediate layer. Emails and vCons are the input. The knowledge graph is the output. The agent queries the graph, not the inbox.
