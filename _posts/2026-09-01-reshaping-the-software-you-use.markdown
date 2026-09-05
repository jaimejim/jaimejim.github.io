---
title: "You can shape your Internet content"
layout: post
header: 2026-09-01
image: /assets/images/2026-09-01-header.webp
date: 2026-09-01 09:00
tag:
- ai
- userscripts
- safari
- youtube
category: blog
author: jaime
---

User interfaces feel a bit hostile at times, but we can now shape the content we consume in ways we couldn't before. For the last ten or twenty years software has consolidated into a handful of big vendors, and somewhere along the way the user stopped mattering much. Especially for anything paid for by ads, but not only there. We turned into data points to study, attention to grab, and someone to sell a product to. IMO there is no respect for the user anymore.

The clearest example is short-form video. Reels, Shorts, whatever each app calls them. They are built to hook you with quick hits of dopamine, and they work too well. One [brain-imaging study](https://doi.org/10.1016/j.neuroimage.2021.118136) found that the personalized clips the algorithm picks for you light up the brain's reward system far more than generic ones. It is terrible for kids, and it is not much better for adults or the elderly. The companies know this and keep pushing it anyway, because your time in the feed is time they can sell ads.

And you cannot turn it off. Go to YouTube and try to disable Shorts. The best you get is "show fewer", and only for a while. There is no switch that removes it. You can block YouTube itself via DNS, or fiddle with Apple settings to block some URL paths, but it is a mess and nobody seems to care. Neither Google nor Apple has much reason to give you a clean off switch, they make plenty from the current setup, like the roughly [20 billion dollars](https://appleinsider.com/articles/26/05/23/googles-20b-safari-search-deal-with-apple-was-fair-and-square) Google pays Apple to stay the default search. For most people it is basically impossible to get any granular control, so you are left with the clumsy mess you are given.

But now with AI, things are quite different. Anyone mildly technical can describe what annoys them about an interface in plain English and, after tinkering a bit, get something that fixes it: a new app, a little script, or whatever fits. I am particularly fond of [userscripts](https://en.wikipedia.org/wiki/Userscript) myself and I recommend everyone to play with them and take back control of their devices. Below are two I wrote recently.

With the first one I wanted to get rid of Shorts. I still want to watch the occasional long-form YouTube video, so the script does two small things: it turns any Short back into a normal video in the usual player, and it removes the Shorts icon from the bottom bar. The rest of YouTube keeps working. After a few days I noticed I did not crave them anymore, because there was nothing to reach for.

<img src="/assets/images/2026-09-01-youtube-no-shorts.jpg" alt="YouTube's bottom bar with the Shorts tab removed" style="width:70%;display:block;margin:1.2rem auto 0.2rem;">
*The bottom bar after the script runs, with the Shorts tab gone.*

The second script is for translation. Chrome has Google Translate built into every site, Safari does not. On the iPhone, Chrome cannot run userscripts but Safari can, so I use Safari, which meant coming up with something myself. The apps I found ask for hundreds of euros for live translation, bundled with a lot of bloat and crap nobody wants. Translating a site properly means replacing the text inside the HTML and rendering it in place, and a model writes a script that does that in one go.

![A Finnish yle.fi article and, beside it, the same article translated to English in place](/assets/images/2026-09-01-translate-fi-en.webp)
*The same yle.fi article before and after, side by side: identical layout, photo and working links, only the words turn English.*

The setup itself is just Safari on the phone, the free **Userscripts** extension, and one folder holding the scripts so they sync across my devices. Each script is a small file I can read top to bottom, so I know *exactly* what it does and what it sends where. You cannot say that about most extensions you install.

<img src="/assets/images/2026-09-01-userscript.jpg" alt="The Userscripts extension open in Safari, listing the in-place translate script" style="width:70%;display:block;margin:1.2rem auto 0.2rem;">
*The Userscripts extension in Safari, with the translate script in the list. Flip it on and it runs on the pages you allow.*

The time from "I wish this thing did not do that" to a working fix is now the time it takes to describe the problem to a model. If you want either script, ask.
