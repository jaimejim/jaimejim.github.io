---
title: "AI automated content generation"
layout: post
date: 2023-02-07 21:50
image: /assets/images/automation.png
tag:
- AI
- art
category: blog
author: jaime
headerImage: true
---

The past few weeks have been extremely busy for me as I've been fully immersed in the world of AI. Specifically, I've been focused on automating tasks with AI, experimenting with image generation AIs, coding-enhancing AIs, various web APIs, my own server, and a handful of new `npm` libraries. I have found that the tooling in the AI world is both reliable and enjoyable.

As part of my exploration, I decided to take on a challenge from a journalist friend in Spain and create a news generation site called [espoo.today](https://espoo.today). My goal was to demonstrate how easy it is to have a functioning domain and how AI can write articles, find relevant images, and publish them on its own.

As an example, one of the articles it generated is a piece about Runeberg Day, which you can view here: [Runeberg Day](https://espoo.today/2023/02/05/Celebrating-Johan-Ludvig-591/). While the text is still relatively simple, I think it's good enough for what I wanted to achieve as a proof of concept.

![espoo](/assets/images/espoo-today.png)

The process to generate is now very straightfoward as shown in the script below: 
1. The script retrieves local tweets and sort them to select the right tweet candidate.
2. Pass it to OpenAI model for processing, generate markdown and caption text.
3. Get image from OpenAI.
4. Get audio transcript from elevenlabs.
5. Writes the markdown, audio, and image files and push the changes to a git repo on GitHub.

Some interesting bits are that ChatGPT returns [structured](https://jaime.win/chat-gpt/) JSON, which saves me few API calls and allows my code to be more straighforward.

```sh
❯ sh ~/code/scribai/publish-something-new.sh
0.380s [scribai] debug: OpenAI auth: sk-DXMhD...
0.382s [scribai] debug: Twitter auth: AAAAAAAA...
0.383s [scribai] debug: Internet connection: true
0.383s [scribai] info: get tweets
0.849s [scribai] info: Very carefully select tweet candidate
0.851s [scribai] info: ask the big 🤖 🧠 
13.975s [scribai] debug: id: cmpl-6lxLhZQt2ebuFuErOzMMcP1GImnis | temp: 0.8
13.975s [scribai] debug: type: text_completion | mod: text-davinci-003
13.975s [scribai] info: 488 tokens [276p+212c]
13.976s [scribai] info: 200 OK processed in 12 seconds
13.977s [scribai] info: 🙈 JSON text successfully parsed
13.977s [scribai] info: Monday Blues? Escape with Bear Cubs
19.677s [scribai] debug: generating image1676887590.png
19.679s [scribai] debug: downloading image1676887590.png
19.681s [scribai] debug: 2023-02-20-Monday-Blues-Escape-488.markdown
19.681s [scribai] debug: generating "2023-02-20-Monday-Blues-Escape-488.markdown" contents
19.684s [scribai] info: Total cost: 0.01 euros
19.690s [scribai] info: 0.948 kb written
30.681s [scribai] info: audio: 1676887590.mp3 downloaded successfully
/Users/ejajimn/code/JAIME/espoo-news
[master dd024f8] new posts
 3 files changed, 20 insertions(+)
 create mode 100644 _posts/2023-02-20-Monday-Blues-Escape-488.markdown
 create mode 100644 audios/1676887590.mp3
 create mode 100644 images/1676887590.png
Enumerating objects: 12, done.
Counting objects: 100% (12/12), done.
Delta compression using up to 8 threads
Compressing objects: 100% (8/8), done.
Writing objects: 100% (8/8), 2.35 MiB | 1.85 MiB/s, done.
Total 8 (delta 4), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (4/4), completed with 4 local objects.
To https://github.com/jaimejim/espoo-news.git
   da85f4b..dd024f8  master -> master
```

All is running mostly well with few bugs here and there. The missing -very important- piece is that MidJourney for image generation requires manual work, as they support no API. I implemented a bot with `discord.j` but it turns out bots are not allowed to talk to each other on discord :(. So I am back to using the much inferior chatgpt image generation.