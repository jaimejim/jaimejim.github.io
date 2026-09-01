---
title: "Dynamic Mashups with Vonage and MCP"
layout: post
date: 2025-09-25 10:00
image: /assets/images/web-agent.webp
tag:
- agents
- MCP
- APIs
- UX
- CPaaS
category: blog
author: jaime
headerImage: true
---

A quiet change that AI agents are bringing is how we think about user interfaces. The old concept of **web mashups** might make a comeback with AI Agents. When agents interact with APIs dynamically (with no a priori knowledge of the subset of APIs they will use), something more fluid emerges: interfaces that generate themselves based on what the agent discovers and decides to do!

These context-driven **dynamic mashups** are such that the experience isn't predetermined by frontend code but composed in real-time as agents interact with services.

At [Ericsson Research](https://www.ericsson.com/en/blog/2025/11/network-apis-for-ai-agents), together with [Vonage](https://www.vonage.com), we've been exploring how [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) enables agents to access both Communications Platform as a Service (CPaaS) APIs and Network APIs. MCP is an open standard that lets AI systems discover and use external tools without manual integration.

The technical implementation is simple: wrap APIs as MCP tools with defined schemas. For example, Vonage's SMS API becomes a `send_sms` tool. The agent sees it's available, understands its purpose from the schema, and can invoke it when needed. No hardcoded integration, no custom prompts, only dynamic capability discovery. Same thing goes for `device_location`, `contact_information` and others.

<div style="text-align: center; margin: 2em 0;">
  <video width="100%" controls playsinline webkit-playsinline>
    <source src="/assets/videos/vonage-final-mobile.mp4" type="video/mp4">
    Your browser does not support the video tag.
  </video>
  <p style="font-style: italic; color: #666; margin-top: 0.5em;">Demo: Agent dynamically composing Vonage APIs and network capabilities</p>
</div>

But agents don't just call APIs. They also compose the **user interface**, when a user asked about device location, the agent:

1. Called the Device Location API to get coordinates
2. Recognized coordinates alone weren't useful
3. Automatically crafted the HTML/CSS/JS bits to visualize the location
4. Added the embedded map as the response in the chat

No developer wrote "if location query, then show map". The agent made that compositional decision based on available tools and context. The UX was generated from the interface descriptions and the user intents.

In a future where you have [agentic browsers like Atlas](https://openai.com/index/introducing-chatgpt-atlas/) we will see more interfaces that assemble themselves based on runtime context, available services, and agent reasoning rather than static frontend templates and side-chatbots.
