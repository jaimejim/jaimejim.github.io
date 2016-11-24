---
title: "On dropping the language part of URLs"
layout: post
date: 2016-10-05 16:00
tag:
- Web Design
- HTTP
- Language
blog: true
star: true
---

I am having some issues with the language settings of some sites I visit. It seems as if there were no best practices or standard settings for language regionalization.

On the one hand it seems that web design is taking into account cultures and language preferences and therefore most companies translate their websites to almost any language. On the other hand there are lot of assumptions as to **which language the reader speaks** and a lot of interest to know the preferences of the reader.

I'm a spaniard in Finland but I use a Swedish proxy server. Often, I am forced to perform some trick to get the website I am visiting the way I want. I like Spanish websites in spanish, Finnish ones in english (there is no spanish option and I haven't learned the language), German ones in german (to practice reading) and Swedish ones ~~blocked~~ in swedish. These are the usual actions I have to try:

1. Explicitly prepend the language part of the URL on `http://website.com` , changing it to`http://en.website.com`, or appending `?hl=en` or similar. I don't know how this works from the SEO perspective as it does seem a bit inconsistent, but it is very convenient for me as an user as it forces the server to serve the content in english.

2. Changing some setting on the website I visit. It can get tricky if you visit online stores because you have country, currency, language and then international sites depending on where you are from. You can go to Skyscanner and check it out, those concepts get mixed and interwoven. In some cases, like Spotify, advertising is linked to the country your credit card was issued or where you reside, so I get ads in finnish even if I don't understand it.

3. Use some tracking mechanism like cookies. This would be fine if I trusted every website I visit to keep my information private, however that is not always the case.

The trend I have discovered is that options 1 and 2 are slowly disapearing. Service providers have found a nifty excuse to track their users by forcing them to register in order to get the content in the language they want. For example I was just checking the [Google Store](https://store.google.com/product/pixel_phone) (because of the new phone they announced) and I was surprised that I couldn't change the language anywhere, cause they usually have very clear guidelines for [multilingual URLs](https://support.google.com/webmasters/answer/189077). There is no URL path for me to edit and there is no user interface either. It assumes that the [natural language field is FI](https://www.w3.org/TR/WCAG10-TECHS/#tech-identify-lang) I have to register with Google so that I can read the english version of the site.

![Google Store assumes I speak finnish](/assets/images/google_store.jpg)

I am no web developer but I personally prefer option 1, as it is independent of the website implementation and it lets me decide, moreover it **decouples language from nationality, billing information or country of residence** while maintaining some form of anonymity.
