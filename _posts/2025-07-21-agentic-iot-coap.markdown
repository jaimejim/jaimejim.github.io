---
title: "AI Agents Don't Need to Know Your Devices"
layout: post
date: 2025-07-21 14:00
tag:
- IoT
- agents
- CoAP
- IETF
- HATEOAS
category: blog
author: jaime
headerImage: false
---

I presented at [IETF 123 T2TRG](https://datatracker.ietf.org/meeting/123/session/t2trg) in Madrid on agentic AI operation of IoT systems. The talk showed a working system where an AI agent discovers, reads, writes, and subscribes to IoT devices over CoAP with zero prior knowledge of the deployment. No configuration files. No device manifests. No MCP bridge. Just an entry point and standardized affordances.

Here's the recording, cued to the presentation:

<iframe width="560" height="315" src="https://www.youtube.com/embed/7y4fBymxKDI?start=4780" frameborder="0" allowfullscreen></iframe>

[Slides (PDF)](https://datatracker.ietf.org/meeting/123/materials/slides-123-t2trg-agentic-ai-operation-of-iot-systems-00)

## The Problem

Most AI-IoT integrations today require someone to write tool definitions for every device, every capability, every endpoint. You add a new sensor, you write a new tool. You change a device's API, you update the tool. The agent only knows what you explicitly told it.

This is the opposite of how the web works. A browser doesn't need a pre-built tool for every website. It follows links, reads forms, discovers capabilities at runtime. The web's architectural principle for this is HATEOAS: Hypermedia as the Engine of Application State.

IoT has the same building blocks. CoAP has resource discovery via `/.well-known/core`. CoRE Link Format describes resources with types, interfaces, and content formats. SenML gives you structured sensor data. The pieces exist. Nobody had wired them to an agent.

## The Architecture

The system has 3 layers:

- **Agent framework** ([smolagents](https://github.com/huggingface/smolagents)): takes a high-level request, plans a sequence of actions, generates Python code to execute them. The code generation makes runs more deterministic than pure prompt chaining.
- **CoAP tools**: 4 operations the agent can invoke: discover, read, write, subscribe. These are generic. They work against any CoAP server, not specific devices.
- **Knowledge base**: IETF specs (CoAP, CoRE Link Format, SenML) plus the LLM's own training data on these protocols. No device-specific knowledge.

The test environment was a Docker setup with several virtualized IoT devices exposing CoAP endpoints with JSON serialization. Each device advertised its resources through standard CoRE links, with brief descriptions and available methods.

## "It's Dark"

The live demo started with a vague request: "it's dark."

The agent's reasoning chain:

1. Discover all resources via `/.well-known/core`
2. Identify light-related sensors and actuators from resource descriptions
3. Read the light sensor value to confirm it's actually dark
4. Find the light actuator
5. Turn it on
6. Read the sensor again to verify the change took effect

No one told the agent which device controls the lights. No one mapped "dark" to a specific actuator URI. The agent figured it out from the resource descriptions in the CoRE links, the same way a human would browse an API.

It also handled edge cases. When asked to "make a pancake," it searched for relevant resources, found none, and reported it couldn't help. When running in closed-loop mode, it continuously monitored all sensors and corrected anything that drifted out of bounds.

## Why This Matters

The key insight from the talk: agents don't need a priori knowledge about the devices or systems they connect to. They learn by discovering and interacting with endpoints. They need exactly one thing: a well-defined entry point.

This is HATEOAS applied to AI. The agent is a hypermedia client that follows links, reads affordances, and acts on them. IETF protocols already support this pattern. CoAP resource discovery is the entry point. CoRE links are the affordances. SenML is the data format. The agent just walks the graph.

A few specific observations from the implementation:

- **IETF specs are in the training data.** Every LLM we tested already understood CoAP, SenML, and CoRE Link Format. The agent could parse and reason about these formats without custom prompting.
- **CoAP is well suited for agents.** Request/response over UDP, resource discovery built in, observable resources for subscriptions. The protocol was designed for constrained environments, but its simplicity makes it ideal for autonomous clients too.
- **Error recovery works.** The agent recovered from execution errors (bad URI), interaction errors (timeout), and outcome errors (actuator didn't change the value). The ReAct loop naturally retries and adapts.
- **Runtime adaptability.** When new devices appeared in the environment, the agent discovered them on the next discovery pass. No restart, no reconfiguration.

## The MCP Question

Alexander Pelov asked during Q&A how this would scale to more complex environments with many sensors. The honest answer: you'd need richer semantics in the resource descriptions to help the agent pick the right sensor for the job. The CoRE links need enough context for the agent to reason about relevance.

But the important architectural point is that this system uses CoAP natively. There's no MCP server sitting between the agent and the devices. No translation layer. The agent speaks the device's own protocol. This matters because every translation layer is a place where affordances get lost, capabilities get frozen in tool definitions, and the system stops being discoverable.

## What's Next

The conversation continues at IETF. The open questions are around scaling (hundreds of devices, richer semantics), security (agent authentication, authorization scoping), and standardizing the affordance descriptions that make this work.

The code demonstrated at IETF 123 is a proof of concept, but the architectural pattern is general. Any protocol with resource discovery and self-describing endpoints can work this way. The web already proved it. IoT just needs to follow through.

---

*Presented at [IETF 123 T2TRG](https://datatracker.ietf.org/meeting/123/session/t2trg), July 21, 2025. [Video](https://youtu.be/7y4fBymxKDI?t=4780) · [Slides](https://datatracker.ietf.org/meeting/123/materials/slides-123-t2trg-agentic-ai-operation-of-iot-systems-00) · [Minutes](https://datatracker.ietf.org/meeting/123/materials/minutes-123-t2trg-202507210730-02)*
