---
title: "Distilling YouTube Into a Queryable Graph"
layout: post
date: 2026-04-23 02:00
tag:
- distillation
- LLM
- Cloudflare
- Ollama
- Gemini
- knowledge-graph
category: blog
author: jaime
headerImage: false
---

I built [tertulia.jaime.win](https://tertulia.jaime.win) to test one idea: replace chunk-based RAG with local distillation and a topic graph. 202 YouTube videos in, 200 structured Markdown notes out, linked by 665 topics, served as a chat from a single Cloudflare Worker. The chunk-RAG baseline kept answering "no information available" on questions the corpus clearly covered. I'm dropping RAG for this class of problem. The distilled-graph version answers quickly and stays close to the source.

<video controls loop muted playsinline width="100%" poster="/assets/images/tertulia-poster.jpg">
  <source src="/assets/videos/tertulia-demo.mp4" type="video/mp4">
</video>

## Why chunks fail

Naive RAG over transcripts is four steps:

1. `yt-dlp --write-auto-sub --sub-lang es --skip-download <url>` pulls a WebVTT file per video.
2. Parse the VTT, concatenate cue text into 60-second buckets.
3. Store `(video_id, start_seconds, text)` rows in SQLite.
4. At query time, tokenise the question, score chunks by term frequency, stuff the top-K into an LLM prompt.

This works when the answer looks like the question. "March 2025 CPI in Spain?" hits a chunk that literally contains the number. The LLM reads it and repeats it. Factual recall, done.

It breaks on opinion questions. "What does the author think about housing?" matches chunks from thirty videos, each one a fragment of a longer argument surrounded by tangents, ads, and filler. The model sees thirty sentence pieces and the safety-trained behaviour takes over: *no hay información suficiente*.

The retrieval found the right documents. The representation of those documents was wrong. A transcript is a sequence of utterances. An opinion is a synthesis across many of them. Chunk-RAG only ever indexes the first.

## Distilling first

The fix is to convert each transcript into a structured artifact before anything else touches it. A rigid-format prompt through [Ollama](https://ollama.com/) against `qwen3.5` on the laptop. About 30 seconds per transcript, ~90 minutes for 200 videos, nothing leaves the machine, zero API bill.

```
Dado el siguiente texto de un vídeo de {author}, produce una nota
estructurada en markdown con EXACTAMENTE este formato:

# {title}

## Tesis principal
Una frase clara con la posición del autor.

## Argumentos
- Argumento 1 con datos concretos si los hay
- (máximo 8)

## Datos citados
- Dato específico: cifra, fecha, fuente mencionada

## Conceptos relacionados
[[concepto1]], [[concepto2]], [[concepto3]]

## Fuente
{url}
```

What comes out for one video:

```markdown
# Sobre el crecimiento económico...

## Tesis principal
El crecimiento del PIB español reciente se debe principalmente al
aumento demográfico y no a una mejora real en la productividad.

## Argumentos
- El PIB creció un 13% entre 2018 y 2024 frente a menos del 10%
  de Alemania, Francia e Italia, pero esto se explica por el
  aumento poblacional.
- La productividad aparente del trabajo decreció un 2% entre
  2018 y 2024, mientras que en la UE subió un 3,2%.

## Conceptos relacionados
[[pib per capita]], [[productividad]], [[inmigración]],
[[deuda pública]], [[mercado laboral]]

## Fuente
https://www.youtube.com/watch?v=-5l7FdzSFwg
```

Two things matter here. First, the structure is load-bearing: at query time the model sees an argument, not a transcript. Second, the `[[wikilinks]]` are the seed of a graph. Every note declares which concepts it touches, and after 200 runs the union of those declarations is a concept index over the corpus. No manual taxonomy, no embedding cluster, no LDA. The distillation prompt just biases the model toward reusing existing concepts.

Building the graph is ten lines of Python, basically a regex over every note file into a topic→notes dict. The result:

```
200 notes · 665 topics · 1,287 topic→note edges

Top hubs:
  inflación              21 notes
  deuda pública          11
  mercado laboral         9
  tipos de interés        8
  inteligencia artificial 8
  política fiscal         7
```

Power-law distribution, long tail of one-offs. The hubs are the navigable product.

## Retrieval as graph walk

At query time the Worker does a cheap graph walk instead of a vector search:

```javascript
function retrieveNotes(question, persona, maxNotes = 6) {
  const qWords = tokenize(question);
  const candidates = DATA.notes.filter(n => n.source === persona);

  const scored = candidates.map(note => {
    let score = 0;
    const nTitle = norm(note.title), nContent = norm(note.content);

    for (const w of qWords) if (nTitle.includes(w)) score += 5;

    for (const topic of note.links) {
      const nt = norm(topic);
      for (const w of qWords) {
        if (nt === w) score += 4;
        else if (nt.includes(w)) score += 2;
      }
    }

    let hits = 0;
    for (const w of qWords) if (nContent.includes(w)) hits++;
    score += Math.min(hits, 5);

    return { note, score };
  }).filter(x => x.score > 0);

  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, maxNotes).map(x => x.note);
}
```

Three signals, three weights, hand-tuned in five minutes. No embeddings, no vector store, no Vectorize. The full index is a 187 KB JSON file bundled with the Worker and the walk runs in sub-millisecond time inside V8. For 200 notes this is overkill on the retrieval side; the heavy lifting already happened at distillation time.

The top-6 notes get concatenated as context. Separately, I pick one or two 60-second chunks per retrieved note, score them by query-word overlap, enforce a 3-minute minimum gap between picks within the same video, and hand them to the LLM as numbered citations:

```
CITAS DISPONIBLES (usa [#N] al final de la frase que respalden):
[#1] 1:32 — "el PIB español creció un 13% entre 2018 y 2024..."
[#2] 8:00 — "la productividad aparente del trabajo decreció..."
[#3] 7:00 — "la población española creció más del 4%..."
```

The model inserts `[#1]` markers in its answer, the frontend swaps them for clickable timestamp pills, and clicking one opens a YouTube iframe at that exact second.

The picker has three behaviours that came straight out of watching early outputs go wrong:

1. **First-chunk penalty.** Intros always state the topic (*"Hoy hablamos de la inflación..."*), so keyword-match puts chunk 0 at the top of every video. A `-2` penalty pushes picks to where the *argument* is, not the table of contents.
2. **Minimum gap.** A 180-second floor between picks inside the same note, so two citations don't point at adjacent minutes.
3. **Sub-minute refinement.** Find the first query-word hit inside the picked chunk, back up to the start of its sentence, offset the timestamp proportionally. Pills land at `4:25` and `11:27`, not `4:00` and `11:00`.

All three were debug-driven. The first batch of deployed citations clustered at `0:00`, `1:00`, `2:00`. Once I logged what the picker was actually selecting, each fix was a handful of lines.

## The prompt that made it speak

Graph-nav retrieval is half the fix. The other half is the prompt. The baseline used "summarise the retrieved information", which produced deflections. The distilled version uses a persona prompt:

```
Eres {author}. Respondes en primera persona, con tu voz.

No eres un asistente hablando sobre {author}: eres {author}.
Las notas que recibes son destilaciones de tus propios vídeos.

- Primera persona: "creo", "defiendo", "argumenté".
- NO digas "según las notas", "según la información
  proporcionada", "en el contexto".
- Las críticas del autor a políticas SON su opinión sobre
  ellas. No digas "no hay declaración directa" si hay un
  análisis crítico en las notas.
```

Same model (`gemini-2.5-flash`, `thinkingBudget: 0`), same six retrieved notes, different prompt. The output goes from *"Según la información proporcionada, no hay una declaración directa..."* to *"En mi opinión, X es un problema estructural. Mis datos: PIB +13%, productividad -2% [#1]..."*. Not a model change. A representation change plus a framing change.

One wrinkle: in longer contexts Gemini starts ignoring rules that live in the system prompt. Moving format rules to the end of the user message recovered compliance. The pattern that survived looks like this:

```
<framing>
<distilled notes>
<available citations [#1]..[#8]>
<available topics [[a]], [[b]], ...>
<the user question>
<format reminder: use [[topics]] and [#N]>
```

Handing the model a *closed set* of available topics in-message, rather than hoping it picks them up from the note bodies, roughly doubled the wikilink density in the answer.

## Stack

<img src="/assets/images/tertulia-stack.svg" alt="Tertulia stack diagram" style="width:100%; max-width:720px; background:#f4efe4; padding:1rem; border-radius:8px;">

Everything but the Ollama distillation runs in a single Cloudflare Worker. `run_worker_first = true`, assets via `env.ASSETS.fetch`, SPA fallback for client-side routing. Data is imported as `src/data.json` at build time and lives in the Worker bundle. Gzipped, around 1.3 MB on the wire, well inside the 10 MB module limit. At ~2,000 notes this moves to D1 or Vectorize. At 200 it would be silly to.

Bindings worth naming:

- `env.AI`: Workers AI for the Llama 3.3 70B fallback, free tier, no key.
- `env.SHARES`: KV namespace for the `?s=XXXXXX` short-URL conversation sharing, 6-char base32 IDs, 90-day TTL.
- `env.GEMINI_API_KEY`, `env.OPENROUTER_API_KEY`: Wrangler secrets.

The fallback chain is three nested `try/catch` blocks, not a library. Any upstream failure (401, 429, 5xx, body parse error) falls through to the next provider. The frontend never knows which model served the answer because the SSE envelope is the same on the way out.

## Insights

**Distillation is not summarisation.** A summary is a shorter version of the source. A distilled note is a different kind of object: a structured claim, plus supporting arguments, plus topic memberships. The difference is whether you can query it. You can't query a summary. You can query a structured claim.

**The topic graph is the product.** I built it as an intermediate artifact for retrieval scoring. It turned out to be the best way to browse the corpus. Click any `[[topic]]` in any answer and `/api/topic?t=X` returns every note tagged with X. The chat is one way in. The graph is the other, and probably the one I'll use more.

**Closed palettes beat open prompts.** "Add relevant topic links" produces made-up terms that don't link anywhere. Giving the model the closed list of topics present in the retrieved notes, in the same message, gets you consistent, navigable output.

**Recency beats specificity in long contexts.** Rules at the end of a long user message are followed more reliably than rules at the start of the system prompt. The system prompt is for voice and identity. The user message is where format rules earn their keep.

**Build the fallback chain before you need it.** Halfway through this the tool I code with went down with a service error. Adding an alternate LLM path took ten minutes and the same pattern ended up in the Worker itself: Gemini → OpenRouter → Workers AI. None of it was planned; all of it compounds.

## What's missing

One persona isn't the interesting version. Three or four, with the topic graph bridging them, is: `[[inflación]]` through one author versus through a heterodox economist, in the same UI. That's a different product from what's live now.

At two thousand notes, pure keyword-match starts to miss. I'd add a semantic pass using a small embedding model through Workers AI (`bge-m3` has a free tier), keep vectors in Vectorize, and score them on top of the topic graph. The retrieval unit stays the distilled note. Chunks are only for citations.

Code lives in `~/code/apps/personas/` and `~/code/apps/kb/`. Site is [tertulia.jaime.win](https://tertulia.jaime.win). Ask it something specific.
