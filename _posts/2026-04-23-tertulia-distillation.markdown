---
title: "Distilling YouTube Into a Queryable Graph"
layout: post
date: 2026-04-23 02:00
tag:
- distillation
- LLM
- Cloudflare
- Ollama
- knowledge-graph
category: blog
author: jaime
headerImage: false
---

I wanted to talk to a corpus of YouTube videos the way I talk to my Obsidian vault. One author, a few hundred videos, questions like "what do you think about housing?" that chunk-based RAG is never going to answer well. That became [tertulia.jaime.win](https://tertulia.jaime.win): 202 videos in, 200 structured notes and a topic graph out, served as a chat from a single Cloudflare Worker.

<video controls loop muted playsinline width="100%" poster="/assets/images/tertulia-poster.jpg">
  <source src="/assets/videos/tertulia-demo.mp4" type="video/mp4">
</video>

## Why not RAG

I tried chunk-RAG first. It works for factual lookups, "what was March 2025 CPI in Spain?" hits the right chunk and the model reads it back. Ask for an opinion and retrieval returns thirty sentence fragments from thirty videos, the model looks at the pile, decides it doesn't have enough context, and refuses.

The retrieval found the right documents. The representation was the problem. A transcript is a sequence of utterances, an opinion is a synthesis across many of them, and chunks only ever index the utterances.

[Karpathy made this point more generally](https://x.com/karpathy/status/2039805659525644595) and [domleca's llm-wiki](https://github.com/domleca/llm-wiki) does it nicely for Obsidian. I wanted the same for a video corpus.

## Two passes

The build is two distillation passes, both done before anyone asks a question.

**Pass 1, per video.** A local Ollama model (`qwen3.5`) reads each transcript and produces a fixed-format markdown note: thesis, arguments, data cited, three to eight `[[topic]]` links. About thirty seconds per video, ninety minutes for two hundred, nothing leaves the laptop.

```markdown
# Sobre el crecimiento económico...

## Tesis principal
El crecimiento del PIB español reciente se debe principalmente al
aumento demográfico, no a una mejora en la productividad.

## Argumentos
- PIB +13% entre 2018 y 2024, pero población +4%.
- Productividad aparente del trabajo −2% en el mismo período.

## Conceptos relacionados
[[pib per capita]], [[productividad]], [[inmigración]]

## Fuente
https://www.youtube.com/watch?v=-5l7FdzSFwg
```

**Pass 2, per topic.** For every `[[topic]]` that shows up in at least three notes, a second pass reads all the notes that mention it and writes a consolidated concept note. Position, recurring arguments, date-keyed nuances when the view has shifted, and citations back to the source notes. The prompt is "state the consolidated position, argue for it, cite the evidence", not "summarise these notes". This is where the heavy lifting happens.

```markdown
# Inflación

## Posición consolidada
El autor sostiene que la inflación 2021–24 no es sólo monetaria:
cuello de botella en oferta, revisiones salariales reactivas, y una
política fiscal expansiva que el BCE no puede compensar sola. ...

## Matices por fecha
- 2022-03: énfasis en causas de oferta (Ucrania, energía).
- 2023-11: giro hacia el componente fiscal y expectativas.
- 2024-09: coste social de la desinflación, efectos distributivos.

## Evidencia
- [[2022-03-14-inflacion-no-solo-monetaria]] (2022-03-14): ...
- [[2023-11-02-bce-fiscal]] (2023-11-02): ...
```

That second pass is what makes the "what do you think about X" questions work. At query time the model isn't stitching fragments, the synthesis is already on disk.

## Learnings

The `[[topic]]` links aren't decoration. Across 200 notes, the union of all those links is a 665-topic index of the whole corpus: `inflación` shows up in 21 notes, `deuda pública` in 11, and a long tail of one-offs. The power law is what you'd expect, and the hubs emerged on their own without any taxonomy or clustering.

I added the graph as a retrieval signal. I ended up using it as the main way to browse. Click any `[[topic]]` in any answer and you get every note tagged with it, which turned out to be more useful than the chat.

## Stack

Both distillation passes run locally through Ollama. Serving is a single Cloudflare Worker. The entire knowledge base, notes and graph, fits in a 187 KB JSON that's bundled into the Worker, so retrieval is a keyword walk over the topic graph that runs in sub-millisecond time. No vector DB, no separate storage.

## Work in progress

Past ~2,000 notes the keyword walk stops being enough and a semantic pass (likely `bge-m3` through Workers AI) makes sense, with the distilled note staying as the retrieval unit. Pass 2 also wants to be incremental so adding a new video doesn't re-synthesise every concept. The version I actually want has two or three authors in the same UI, bridged through the topic graph, so `[[inflación]]` can be read through one voice versus another.

Code lives in `~/code/apps/personas/` and `~/code/apps/kb/`. The site is [tertulia.jaime.win](https://tertulia.jaime.win). Ask it something specific.
