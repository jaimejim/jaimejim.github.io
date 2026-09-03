---
title: "Analyzing AI usage in IETF drafts"
layout: post
header: 2026-05-01
image: /assets/images/2026-05-01-header.webp
date: 2026-05-01 12:00
tag:
- IETF
- AI
- research
category: blog
author: jaime
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

![Dashboard of the batch scan over about 1,400 recent IETF drafts]({{ site.url }}/assets/images/is-it-ai-dashboard.webp)

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

![Per-draft page showing the four-model breakdown, per-dimension scores and the statistical signals]({{ site.url }}/assets/images/is-it-ai-sample-draft.webp)

One detail worth mentioning, of the eight statistical heuristics only
*hedging density* is actually discriminative. The others are decorative.
I just picked the ones I found online while putting this together on my
spare time, so if someone is into this kind of thing and knows better
heuristics, let me know and I can re-run that part.

The LLMs do the real work, and they do not fully agree with each other.

One caveat I want to be upfront about: the signals this tool flags
(uniform sentence structure, hedging language, Latinate vocabulary)
overlap heavily with how non-native English speakers write. Liang et al.
showed this in 2023 ([paper](https://arxiv.org/abs/2304.02819)), and it
is directly relevant for the IETF where many contributors write in their
second or third language. A high score does not mean AI; it means the
writing deviates from the typical IETF style, for whatever reason.

More broadly, reliable AI detection in technical prose may not be a
solvable problem. Sadasivan et al.
([paper](https://arxiv.org/abs/2303.11156)) proved that detector
accuracy degrades toward a coin flip as models improve, and that
paraphrasing defeats every detector they tested. For low-entropy text
like protocol specs, where the writing is formulaic by nature, the
ceiling is even lower. So think of this as a stylistic outlier detector,
not an oracle.

The tool is live, the raw data is available on the page. If you find a
draft whose verdict looks off to you, let me know.
