---
title: "A personal AI knowledge assistant"
layout: post
date: 2025-07-09 14:00
image: /assets/images/obsidian-q.png
tag:
- AI
- productivity
- notes
- obsidian
category: blog
author: jaime
headerImage: true
---


Many people either take no notes at all or document their work poorly. I try to keep a knowledge management setup that combines work, research, and personal life documentation. I keep a diary but also have deep dives on specific technologies, projects I work on, technical ideas, or random thoughts. I also use todos and reminders, similar to how I used org-mode in the past. This type of information management is usual when you work in research.

I used to use orgmode but migrated to [Obsidian](https://obsidian.md/) about a year ago. I try to store everything in Obsidian and I use search, templates, and tags to find specific information. It basically functions as an external memory; once written, I do not need to keep it in my own memory all the time.

My setup is pretty straightforward. Every day gets its own markdown file like `2025-07-09.md`. I include basic templated stuff like weather, location, meetings, and write down whatever happened that day.

The magic is in the linking. With wikilinks you can create entries like `[[John Doe]]` to link to people, `[[Project X]]` for projects, `[[Company Name]]` for companies. Obsidian builds a knowledge graph automatically, connecting everything.

Although not needed, I also structure things in folders, like:

```sh
/Events/           # Conferences and workshops
/Dailies/          # One file per day
/Meetings/         # Detailed meeting notes  
/People/           # Contact info and history
/Projects/         # Project documentation
/Companies/        # Organization profiles
/IETF/             # Standard documents
....               # and more
```

Nothing fancy, but consistent and more importantly, linked with each other when relevant, so that if I check `[[John Doe]]`, in the entry I can also see the references to meetings or project discussions we had. For that I use `dataview` scripting.

Recently started combining it with **Amazon Q Chat**. The result is pretty interesting. I can ask very specific questions and get answers from my own notes or generate specific reports or insights that span multiple days and documents. Amazon Q Chat can read my files and answer questions about them; I have a profile configured just for that. Instead of searching manually, I just ask. Q Chat searches through my daily notes using common CLI commands like `rg`, `find` and so on.

For example, maybe I have the vague notion that there was a chip company in Boise from a book I read called "Chip Wars". This would be the interaction:

```sh
[obsidian] > I remember there was a chip company in Boise

🛠️  Using tool: execute_bash
 ⋮ 
 ● I will run the following shell command: 
grep -r -i "boise\|chip.*company\|semiconductor" "/Users/ejajimn/Library/Mobile Documents/iCloud~md~obsidian/Documents/obs" --include="*.md" -A 2 -B 2
 ⋮ 
 ↳ Purpose: Search for Boise and chip company mentions
 ```

Then it would read a bunch of my files and return:

```sh
 ⋮ 
 ● Completed in 0.412s


> Perfect! Based on your notes, the chip company in Boise you're remembering is Micron Technology. 

From your "Chip War" book notes, I can see that:

Micron Technology was founded in 1978 by twin brothers Joe and Ward Parkinson in the basement of a Boise 
dentist office. It was backed by John Simplot, Idaho's "potato plutocrat" who made his fortune with the J.R. 
Simplot Company (the agricultural supplier that partnered with McDonald's for frozen french fries).

Key details:
• Founded in Boise, Idaho in 1978
• Started in a dentist's basement 
• Founded at "the worst possible time to start a memory chip company"
• Backed by John Simplot's investment
• Specializes in DRAM memory chips and data storage solutions
• Now recognized as the only U.S.-based manufacturer of memory

It's quite a story - from a potato fortune to backing one of America's major semiconductor companies, all 
starting in a Boise dentist's basement!
```

Another example:

![robodog](/assets/images/robodog.png)

Maybe there are things you saw on previous occasions and you don't want to dig through your notes like:

```sh
[obsidian] > what was ECDH PSI?

> ECDH PSI stands for Elliptic Curve Diffie-Hellman Private Set Intersection.

From your March 16th notes, you learned about this from Yuchen Wang and Wenting Chang at IETF 122 Hackathon.
They presented "A python POC implementation of ECDH PSI's math" which is reflected in their draft: https://
datatracker.ietf.org/doc/html/draft-wang-ppm-ecdh-psi-01

PSI (Private Set Intersection) is a cryptographic technique that allows two parties to compute the 
intersection of their datasets without revealing the elements that are not in the intersection. The ECDH 
variant uses elliptic curve cryptography for this purpose.
```

Unfortunately this does not improve my understanding about elliptic curve cryptography but at least I remember the context!

You can also do more complex queries like:

```
[obsidian] > write a report only with the work related items I did on the 2nd week of march
```

```
[obsidian] > how often did I meet John Doe and were?
```

```
[obsidian] > What was the outcome of draft xyz?
```

In summary, combining Obsidian with Amazon Q Chat transforms personal note-taking into a powerful, searchable knowledge base. It is hacky still but I am sure this will be incorporated into future voice-enabled assistants that are always available and always contextualized to your own information.