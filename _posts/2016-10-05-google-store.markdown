---
title: "On dropping the language part of the URL"
layout: post
date: 2016-10-05 16:00
tag:
- Web Design
- HTTP
- Language
blog: true
star: true
---

I am having some issues with websites languages and I am noticing that there does not seem to be any standard way of doing *language regionalization* (is that the term?).

On the one hand it seems that web design is taking more into account the local cultures and languages and therefore most companies translate their websites to almost any language. On the other hand there are lot of assumptions as to **which language the reader speaks** and a lot of interest to know the preferences of the reader.

As a spaniard in Finland but using a Swedish proxy server I usually have to do some action to get the website I am visiting the way I want. I like Spanish websites in spanish, Finnish ones in english (there is no spanish option and I haven't learned the language), German ones in german (to practice reading) and Swedish ones ~~blocked~~ in swedish. These are the usual methods:

1. Prepending the language part on the URL from `http://website.com` to `http://en.website.com`, appending `?hl=en` or similar tricks. I don't know how this works from the SEO perspective as it does seem a bit inconsistent, but it is very convenient for me as an user.

2. Changing some setting on the website I visit. It can get tricky if you visit online stores because you have country, currency, language and then international sites depending on where you are from. You can go to Skyscanner and check it out.

3. Use some tracking mechanism like cookies. This would be fine if I trusted every website I visit to keep my information private, however that is not always the case.

The latest trend I am seeing is that options 1 and 2 are slowly disapearing. For example I was just checking the [Google Store](https://store.google.com/product/pixel_phone) (because of the new phone they announced) and I was surprised that I couldn't change the language anywhere, cause they usually have very clear guidelines for [multilingual URLs](https://support.google.com/webmasters/answer/189077). There is no URL path for me to edit and there is no user interface either. It assumes that the [natural language field is FI](https://www.w3.org/TR/WCAG10-TECHS/#tech-identify-lang) I have to register with Google so that they can have my preferences.

![Google Store assumes I speak finnish](/assets/images/google_store.jpg)

I am no web developer but I personally prefer option 1, as it is independent of the website implementation and it lets me decide, moreover it **decouples language from nationality or country of residence**.
