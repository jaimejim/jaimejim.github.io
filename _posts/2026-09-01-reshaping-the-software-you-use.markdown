---
title: "You can shape your Internet content"
layout: post
date: 2026-09-01 09:00
image: /assets/images/2026-09-01-header.png
tag:
- ai
- userscripts
- safari
- youtube
category: blog
author: jaime
headerImage: true
---

User interfaces feel a bit hostile at times, but we can now shape the content we consume in ways we couldn't before. For the last ten or twenty years software has consolidated into a handful of big vendors, and somewhere along the way the user stopped mattering much. Especially for anything paid for by ads, but not only there. We turned into data points to study, attention to grab, and someone to sell a product to. IMO there is no respect for the user anymore.

The clearest example is short-form video. Reels, Shorts, whatever each app calls them. They are built to hook you with quick hits of dopamine, and they work too well. One [brain-imaging study](https://doi.org/10.1016/j.neuroimage.2021.118136) found that the personalized clips the algorithm picks for you light up the brain's reward system far more than generic ones. It is terrible for kids, and it is not much better for adults or the elderly. The companies know this and keep pushing it anyway, because your time in the feed is time they can sell ads.

And you cannot turn it off. Go to YouTube and try to disable Shorts. The best you get is "show fewer", and only for a while. There is no switch that removes it. You can block YouTube itself via DNS, or fiddle with Apple settings to block some URL paths, but it is a mess and nobody seems to care. Neither platform has much reason to give you a clean off switch, they make plenty from the current setup, like the roughly [20 billion dollars](https://appleinsider.com/articles/26/05/23/googles-20b-safari-search-deal-with-apple-was-fair-and-square) Google pays Apple to stay the default search. For most people it is basically impossible to get any granular control, so you are left with the clumsy mess you are given.

But now with AI, things are quite different. Essentially anyone mildly technically aware can describe what annoys them
of their selected interface in plain english and after tinkering a bit get a solution that fixes it, be it a new app,
a little script, or something else. I am particularly fond of
["Userscripts"](https://en.wikipedia.org/wiki/Userscript) myself and I recommend everyone to play with them and take
back control of their devices. Below are two examples I used it for recently.

**Shorts and reels** basically are slot machines designed to keep you glued to the screen. There is, by design, no setting to switch them off. The same companies pushing more of them are also making ad blockers harder to run. Chrome recently disabled the classic uBlock Origin for example. So if you want the feed gone, you are on your own.

My script does two small things, because I still want to watch the occasional YouTube long-form video. It turns any Short back into a normal video in the usual player, and it removes the Shorts icon from the bottom bar. That kills Shorts while leaving the rest of YouTube working. After a few days I noticed I did not crave them anymore, because there was nothing to reach for. And my kids will not get the craving in the first place, since hopefully they will not even know Shorts exists, at least for a while.

<img src="/assets/images/2026-09-01-youtube-no-shorts.jpg" alt="YouTube's bottom bar with the Shorts tab removed" style="width:70%;display:block;margin:1.2rem auto 0.2rem;">
*The bottom bar after the script runs. The Shorts tab is gone, so there is nothing to tap and nothing to crave.*

The second script solves a daily annoyance rather than a temptation. Chrome has excellent Google Translate built into every site, Apple not so much. On the iPhone, Chrome cannot run userscripts but Safari can, so I use Safari, which means I needed to come up with something myself. I checked, and there are apps asking for **hundreds** of euros for live translation, bundled with a lot of bloat and crap nobody wants.

Doing **site translation** properly means translating inside the HTML content and rendering in real time, and nowadays it is trivial to write a script that does that. Not so long ago, that would have been tricky to script. 

![A Finnish yle.fi article and, beside it, the same article translated to English in place](/assets/images/2026-09-01-translate-fi-en.jpg)
*The same yle.fi article before and after, side by side: identical layout, photo and working links, only the words turn English.*

The setup itself is just Safari on the phone, the free **Userscripts** extension, and one folder holding the scripts so they sync across my devices. Each script is a small file I can read top to bottom, so I know *exactly* what it does and what it sends where. You cannot say that about most extensions you install.

<img src="/assets/images/2026-09-01-userscript.jpg" alt="The Userscripts extension open in Safari, listing the in-place translate script" style="width:70%;display:block;margin:1.2rem auto 0.2rem;">
*How it works: the Userscripts extension in Safari, with the translate script sitting in the list. Flip it on and it runs on the pages you allow.*

So there you go, the time between "I wish this thing did not do that" and a working solution is now the time it takes to describe the problem to a model. Completely permissionless, faster, cleaner and comprehensible (since they are just little scripts you can read).
