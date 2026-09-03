---
title: "Building with Claude Code"
layout: post
header: 2026-01-10
image: /assets/images/2026-01-10-header.webp
date: 2026-01-10 13:30
tag:
- AI
- Claude Code
- personal projects
category: blog
author: jaime
---

This Christmas I built [cuentos.jaime.win](https://cuentos.jaime.win/) from my phone. My daughter was learning to read and I wanted something interactive for her practice. The entire stack was just my iPhone, Claude Code Premium, Midjourney for some images, Vercel, and a CNAME subdomain. Built it between family dinners. I also made [mira.jaime.win](https://mira.jaime.win), a food scanner I use when grocery shopping in Finnish - convenient for finding food labels I don't know.

My daughter liked the stories a lot. She plays with them and keeps asking for more, so nice outcome.

The way I worked was describing what I wanted, giving feedback, adjusting prompts. The traditional programming was mostly absent. Making a good plan and verifying the output of the agent is fundamental, but you can vibecode a lot with confidence. Some errors are hard for Claude to debug simply because it lacks a feedback loop to the error. When errors persist you need to start doing actual debugging. So far for me it's been mostly old libraries, lack of Vercel feedback on some CI/CD issues, and misunderstandings in the planning phase.

The numbers are interesting. Claude Code went from zero to [a million users](https://x.com/sammcallister/status/2004999397923598841) in under two years. Sam McAllister called the growth "physically impossible" - exponential for 11 straight quarters. This time last year it didn't exist publicly. Research preview came February 2025. Now Anthropic is [preparing for an IPO](https://archive.is/MrZMg) potentially valuing the company at $300+ billion. They've appointed Wilson Sonsini for preparations.

While OpenAI gets the headlines, the Claude Code adoption feels more real to me. My impression is that in the developer community Claude Code seems to be the most popular one. Anthropic's business customer base has grown from under 1,000 to more than 300,000 in two years, and their revenue is 85% business compared to OpenAI's consumer focus. These are people actually building things, not just enterprise contracts.

The downside is that as it abstracts away the actual coding, it's not great for very junior people if they want to learn. However it is good to build things quickly if you know what you want. For professional developers that work on huge codebases there are different challenges - the scale and complexity introduce problems that are harder for the agent to navigate.
