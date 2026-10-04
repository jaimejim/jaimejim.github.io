---
title: "Notifications for agents: cue, observe, or query"
layout: post
header: 2026-08-20
image: /assets/images/2026-08-20-header.webp
date: 2026-08-20 12:00
tag:
- agents
- protocols
- MCP
- CoAP
- IETF
category: blog
author: jaime
---

An agent that wants to know when a resource changes has a harder problem than a browser does. It usually cannot be dialed back: it runs ephemerally, behind a NAT, or as a CLI process, so it has no inbound endpoint for a webhook to hit. That leaves polling (which burns round-trips and tokens) or opening an outbound connection and holding it open. This is the same constraint that shaped CoAP Observe for sensors. In this one respect an agent is the HTTP equivalent of a constrained device: it can make requests, it cannot easily receive them.

So every workable answer is client-initiated: the subscriber opens the stream and the server pushes down it. Three designs do this today with the same instinct and very different mechanics. I recently built a small proof of concept on the newest of them, MCP's `subscriptions/listen`, which is what got me comparing.

## The cue model: MCP subscriptions/listen

In [MCP's subscription pattern](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/subscriptions) the client sends `subscriptions/listen` with a filter (which notification types, which resource URIs) and the server holds the stream open, sending notifications down it.

The catch is what a notification contains: only the identity of what changed. `notifications/resources/updated` carries the URI, not the new value. The client treats it as a cue and issues a separate `resources/read` to get the state.

- **Solves:** polling avoidance, client-initiated, works behind a NAT.
- **Limitations:** a round-trip per event, since every notification needs a follow-up read to get the data (in my PoC the cue-then-read latency ran a few times the bare notification latency); coarse selectivity, since the filter is notification type plus exact URI, with no query, no predicate, no "only when the value crosses a threshold", and server-side matching is exact-string so you cannot subscribe to a pattern; and no replay, so a dropped stream is not resumable and the client re-subscribes and refetches.

The cue model earns something for those costs. Because a cue carries no data, coalescing 50 rapid changes into one loses nothing (you just read the latest once), and a reconnect is trivially safe (re-listen, read, converge to current truth). It is a deliberate, defensible design. It just pushes all the data, and all the selectivity, into a second request.

## Observe the resource: CoAP Observe

[CoAP Observe](https://www.rfc-editor.org/rfc/rfc7641) decorates a `GET` with an `Observe` option: notify me of this resource. The first notification is the current representation, and every later one is a full representation too, in the same content format.

- **Solves:** the data arrives inband, with no separate read, and it carries the machinery a lossy transport needs: a sequence number for reordering and a `Max-Age` per notification so the client knows how long a value stays fresh. Congestion control is built in.
- **Limitations:** it is UDP and message-oriented, tuned for constrained networks; delivery is best-effort and eventually consistent; and it is CoAP, not something a generic HTTP agent speaks.

For an agent the appeal is granularity and directness: you observe exactly the resource you care about, and the notification is the state. It slots into a simple four-verb agent (list, get, set, observe) as just another call on the uniform interface.

## Query the resource: HTTP Events-Query

[draft-gupta-httpapi-events-query](https://datatracker.ietf.org/doc/draft-gupta-httpapi-events-query/) is the HTTP-world successor to Observe. Instead of decorating `GET`, it uses the [QUERY method](https://datatracker.ietf.org/doc/draft-ietf-httpbis-safe-method-w-body/) with a structured body: what events you want, in what media type, optionally with the representation. The response is a stream.

- **Solves:** it goes beyond Observe in two ways. Notifications are content-negotiated, so you can ask for full state, a delta, or a patch, in whatever media type. And it can combine the representation and the notification stream in one response, saving the initial round-trip and closing the state-versus-stream sync gap. It is client-initiated and reliable (TCP in-order), so no sequence numbers are needed.
- **Limitations:** it is an individual draft, not a working-group document, and it depends on other drafts still in flight (QUERY as a method, `Incremental` for intermediaries). The intermediary and caching story that Observe fully specifies is, for now, aspirational. And it has no per-notification freshness model: TCP gives you reliable delivery, not staleness bounds.

## What this means for agents

The axis an agent cares about is: how do I get the new state, and how much can I say about what I want to be told?

| Approach | Data inband? | Selectivity | Freshness / ordering | Maturity |
|---|---|---|---|---|
| MCP `subscriptions/listen` | No: cue, then read | Type + exact URI | None per-notification; no replay | Shipping (spec 2026-07-28) |
| CoAP Observe | Yes: full representation | The resource itself | `Max-Age` + sequence numbers | RFC 7641, mature |
| HTTP Events-Query | Yes: full, delta, or patch | QUERY body (events + format) | Reliable, no freshness model | Individual I-D |

The cue model is the safest to implement and to reason about, and for many agent cases "something changed, go look" is genuinely enough. But it costs a round-trip per event and cannot express what you actually want to be told about. Observe and Events-Query both subscribe at the resource and carry the data inband, which is fewer round-trips and a cleaner fit for the uniform interface an agent already uses to list, get, and set. Observe has the freshness and ordering machinery; Events-Query has the richer content negotiation but not yet the maturity or the intermediary story.

The gap I keep returning to: the Events-Query discussion is framed around web apps replacing SSE and long-polling, and nobody has framed it for agents, even though the fit is natural since an agent is exactly the consumer that cannot host a webhook. Meanwhile MCP shipped the cue model, which works but leaves both the data and the selectivity for a second call. The interesting design space is in between: a client-initiated, resource-scoped subscription that can carry a delta inband and still coalesce and reconnect safely. The conversation continues at the IETF.
