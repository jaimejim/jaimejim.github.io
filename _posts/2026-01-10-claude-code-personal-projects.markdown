---
title: "Building with Claude Code"
layout: post
date: 2026-01-10 13:30
image: https://cdn.midjourney.com/977d305e-6456-40ac-acf1-4772ab24e5ff/0_1.png
tag:
- AI
- Claude Code
- personal projects
category: blog
author: jaime
headerImage: true
---

This Christmas I built [cuentos.jaime.win](https://cuentos.jaime.win/) from my phone. My daughter was learning to read and I wanted something interactive for her practice. The entire stack was just my iPhone, Claude Code Premium, Midjourney for some images, Vercel, and a CNAME subdomain. Built it between family dinners. I also made [mira.jaime.win](https://mira.jaime.win), a food scanner for when I go grocery shopping in Finnish.

She liked the stories a lot. She plays with them and keeps asking for more, so nice outcome.

The way I worked was describing what I wanted, giving feedback, adjusting prompts. The traditional programming was mostly absent. Making a good plan and verifying the output of the agent is fundamental, but you can vibecode a lot with confidence. Some errors are hard for Claude to debug simply because it lacks a feedback loop to the error. When errors persist you need to start doing actual debugging. So far for me it's been mostly old libraries, lack of Vercel feedback on some CI/CD issues, and misunderstandings in the planning phase.

The numbers are interesting. Claude Code went from zero to [a million users](https://x.com/sammcallister/status/2004999397923598841) in under two years. Sam McAllister called the growth "physically impossible" - exponential for 11 straight quarters. This time last year it didn't exist publicly. Research preview came February 2025. Now Anthropic is [preparing for an IPO](https://archive.is/MrZMg) potentially valuing the company at $300+ billion. They've appointed Wilson Sonsini for preparations.

While OpenAI gets the headlines, the Claude Code adoption feels more real to me. My impression is that in the developer community Claude Code seems to be the most popular one. These are people actually building things, not just enterprise contracts.

The downside is that as it abstracts away the actual coding, it's not great for very junior people if they want to learn. However it is good to build things quickly if you know what you want. For professional developers that work on huge codebases there are different challenges - the scale and complexity introduce problems that are harder for the agent to navigate.
