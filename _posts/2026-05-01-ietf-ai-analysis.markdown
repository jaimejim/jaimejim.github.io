---
title: "Analyzing AI usage in IETF drafts"
layout: post
date: 2026-05-01 12:00
image: /assets/images/vangogh-noon-rest.jpg
tag:
- IETF
- AI
- research
category: blog
author: jaime
headerImage: true
---

During the last IETF in Shenzhen, on a Saturday after the meeting, I went
to [Dafen](https://en.wikipedia.org/wiki/Dafen_Village), an artist village
where painters produce handmade copies of well known oil paintings,
specially Van Gogh and the usual classics. I stood watching a couple of
them for a while. They are incredibly skilled and the copies are
beautiful. Of course to produce so many they take shortcuts, also because
they have painted them hundreds of times. Some put a printed copy of the
painting on the canvas and trace over it with a pen to get the main lines
and the composition right before they start. The brushwork is still
theirs, the colours are still theirs, but of course deciding *where*
things go is not.

A different example is [Midjourney](https://www.midjourney.com) and
similar tools. Online you can see people using them to generate beautiful
digital art pieces. You can design the composition from the beginning,
but the image itself is AI generated. You maybe generate dozens of them
and dozens of variations. Whether you are skilled or not, you can create
something reasonably beautiful. Real artists are also increasingly using
Midjourney in their workflows, for ideation or concept art, blending the
AI outputs with Photoshop or traditional editing for their final pieces.
They argue it is a tool like a camera, where the creative input sits in
the prompting and the post-processing.

I see these as good analogies for AI and how people use it. You may not
use it at all, you may use it to add meaty details to some parts of your
text or code, or you may delegate everything to it.

In the IETF we have all noticed a lot more of AI production lately, and
many drafts read very *AI-like*. That alone is not a problem, I use AI
myself when writing and I think everyone will end up doing so. What is a
problem is that some of them are *more* AI than not, they are not
curated, and they lack quite a bit of depth. Nobody went back to check
if the result actually makes sense.

So to save time for everybody I made - with AI - a tool to analyze a
draft and tell if it has too much AI in it to begin with, so that we can
filter out the ones that clearly have not been reviewed by the author.
It is at [ietf.jaime.win/is-it-ai](https://ietf.jaime.win/is-it-ai).

This is a bit of an AI arms race in the sense that you could always make
an AI-generated text look less AI, but at some point the effort of trying
to hide that something is AI is larger than the effort of just checking
your own draft before submitting it. So I hope it stays useful for a while.

It started as something quick to run on a few drafts, then I thought I
could offer it as a free service for colleagues. After a bit I realized
that I could also just run the same code on every recent draft and get
an idea of how things look at the moment. So I ran it on around 1400
drafts submitted since January.

The tool combines two things. First, eight deterministic statistical
metrics on the text - sentence length variance, hedging density,
vocabulary richness, and similar. Second, an excerpt of the draft is sent
to four different LLMs (Sonnet 4.5, Haiku 4.5, Opus 4.6 and GPT-4o) that
score it on five dimensions. The results are then averaged into a
consensus.

The results are more or less what I would expect. Most drafts cluster
around 15-25% AI, which is consistent with authors using AI to polish
text but still writing it themselves. Around 7% score above 50% AI, and
those are the ones worth looking at more carefully. No draft in the
corpus is unanimously flagged by all four models, which tells you how
fuzzy this whole thing is.

One detail worth mentioning, of the eight statistical heuristics only
*hedging density* is actually discriminative. The others are decorative.
I just picked the ones I found online while putting this together on my
spare time, so if someone is into this kind of thing and knows better
heuristics, let me know and I can re-run that part.

The LLMs do the real work, and they do not fully agree with each other.

The tool is live, the raw data is available on the page. If you find a
draft whose verdict looks off to you, let me know.
