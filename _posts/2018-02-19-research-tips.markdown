---
title: "Finding that paper you are looking for"
layout: post
date: 2018-02-19 18:14
tag:
- CoAP
- Research
- Time-saving
blog: true
star: true
---


We all are living very busy lives, with little time to be spend on things that, maybe some years ago, was OK to spend time with, One of those things are scientific publications.

Every year there are more publications available on a larger number of topics. The fact that univerisities and even whole countries have metrics based on number of published articles ([1](https://link.springer.com/article/10.1007/s11192-017-2504-x),
[2](https://www.snowballmetrics.com/wp-content/uploads/assessing-europe-university-based-research_en.pdf),[3](http://www.keepeek.com/Digital-Asset-Management/oecd/science-and-technology/oecd-science-technology-and-innovation-outlook-2016_sti_in_outlook-2016-en#page149)) does not help.

Yet, scientific knowledge needs to be spread and people need to find out quickly the articles they are interested in. Of course there are well-known tools like sci-hub or google scholar, but often we also have a repository of published papers that we want to look into. For example the [IEEE PIMRC17](http://pimrc2017.ieee-pimrc.org) conference had 549 papers; are we supposed to go through each of them? Of course not, and yet, they publish those papers in PDF, making it harder to do
searchers on the documents.

What I normally do is convert all of them to text using ´pdftotext´ which you can install using the [poppler-utils](https://poppler.freedesktop.org) package under various Linux distributions.  

```
~/Desktop/Papers/ » find . -name \*.pdf -exec pdftotext "{}" \;
~/Desktop/Papers/ » ls
1570347974.txt 1570368376.txt 1570368959.txt 1570373144.txt 1570388857.txt
1570350772.txt 1570368379.txt 1570368961.txt 1570373147.txt 1570388907.txt
1570351129.txt 1570368391.txt 1570368967.txt 1570373149.txt 1570388920.txt
1570351906.txt 1570368392.txt 1570368974.txt 1570373155.txt 1570388948.txt
1570356083.txt 1570368393.txt 1570368975.txt 1570373157.txt 1570388983.txt
1570359771.txt 1570368414.txt 1570368976.txt 1570373168.txt 1570388989.txt
1570360123.txt 1570368426.txt 1570368978.txt 1570373169.txt 1570389029.txt
1570360781.txt 1570368445.txt 1570368982.txt 1570373170.txt 1570389050.txt
1570362275.txt 1570368456.txt 1570368984.txt 1570373171.txt 1570389051.txt
1570362636.txt 1570368460.txt 1570368987.txt 1570373176.txt 1570389119.txt
1570363485.txt 1570368461.txt 1570368989.txt 1570373177.txt 1570389163.txt
...
```

Now that the documents are searchable we can use grep or similar tools to search them. If there are a large number of files involved you might want to check [ripgrep](https://github.com/BurntSushi/ripgrep) which is orders of magnitude faster when searching. In fact, with ripgrep you can also search binary files (PDF) with the option "-a/--text".

For example, I like to search recursively for papers that talk about CoAP, in text format, without minding the capital letters and showing 1 line of context before and after the term is found. Below is the result.

```
~/Desktop/Papers/ » rg -i "CoAP" -g "*.txt" -C 1
s1-1.txt
16-protocols will co-exist, including the Constrained Application
17:Protocol (CoAP), Message Queue Telemetry Transport (MQTT),
18-and HTTP.
--
128-includes several potential federation or integration points: At
129:the lowest network layer there are CoAP and/or HTTP ReSTful
130-APIs. The semantic, processing, and storage layers provide
--
151-and interaction model that can be used for managing things that
152:support the CoAP protocol.
153-B. Decentralised security

s3-2.txt
239-can be used to instantiate a TD for a particular IoT protocol
240:binding, such as OCF, HTTP(S), COAP etc.
241-A WoT Servient can also host a WoT Runtime and a
--
310-the Web of Things concept [13], the current WoT draft
311:supports other choices as well, such as CoAP and MQTT.
312-However, use of HTTP conveniently allows Things acting as
--
465-transport security, object security, or both.
466:If multiple transport protocols are used, such as a combination of HTTP/TLS and CoAP/DTLS, bridging those protocols
467-may create another compromise possibility. A mechanism
```

This way I can immediately spot the papers that talk about something I might be working on too, without browsing hundreds of them. I can even adjust the search to show me only the abstract of those papers, conclusions, etc.

For example if I wanted I could read every abstract pretty quickly by doing the following command:

```
~/Desktop/Papers/ » rg -i "Abstract" -g "*.txt" -C 2

1570368018.txt
3-Farouk Mezghani, Nathalie Mitton
4-Inria Lille Nord – Europe, France - {farouk.mezghani, nathalie.mitton}@inria.fr
5:Abstract—Opportunistic communications present a
6-promising solution as a disaster network recovery in
7-emergency situations such as hurricanes, earthquakes and

1570368756.txt
6-Email: vanessamendes@get.inatel.br
7-
8:Abstract—The aim of this paper is to propose a simple
9-and efficient algorithm to generate white samples for the
10-envelope of the α-η-κ-µ fading model. To this end, capitalizing on results available in the literature, the random

1570372054.txt
9-CNRS 6074 IRISA GRANIT UR1 Lannion, France, Email: firstname.lastname@irisa.fr
10-
11:Abstract—The linear closed-loop MIMO precoding technique employs the channel state information (CSI) at both
12-sides of the link to optimize various criteria such as the
13-capacity, the mean square error, the signal to noise ratio

...
```
