---
title: "Thread use of CoAP"
layout: post
date: 2025-03-31 14:50
image: /assets/images/thread-coap.png
tag:
- IoT
- Thread
- IETF
category: blog
author: jaime
headerImage: true
---

Thread networking is quietly becoming ubiquitous. Every [iPhone 16](https://www.apple.com/iphone-16/specs/) and newer iPad already has Thread support built-in, Android smart hubs are shipping with it, and [home routers](https://www.androidauthority.com/google-tv-streamer-smart-hub-3467634/) increasingly include it by default. Given this momentum, I wanted to understand how Thread actually works under the hood—specifically, how it uses CoAP.

I spent some time with the Thread v1.4.0 specification (September 2024) and found the CoAP implementation quite interesting. Here's what I learned.

[Thread](https://www.threadgroup.org/) is designed for low-power, wireless mesh networks running at around 250 kbps. The key design principle is avoiding single points of failure—if one device goes down, the network routes around it. You'll find Thread in home automation, smart buildings ([KNX IoT](https://www.knx.org/knx-en/for-professionals/benefits/knx-iot/)), lighting systems ([DALI+](https://www.dali-alliance.org/daliplus/)), and increasingly in [Matter](https://csa-iot.org/all-solutions/matter/) devices.

Thread networks have two main device types: Full Thread Devices (FTDs) that can route traffic, and End Devices (EDs) that connect to the network but don't forward messages. End devices can be always-on or "sleepy"—the sleepy ones use optimized power cycles to run for years on AA batteries. The network topology adapts as devices join, leave, or change roles.

![thread](/assets/images/thread-stack.jpg)

The protocol stack builds on familiar IETF standards: IPv6, UDP, DTLS, mDNS, and CoAP, running over IEEE 802.15.4 with 6LoWPAN adaptation. Thread adds its own Mesh Link Establishment (MLE) protocol for setting up and maintaining the mesh network using IANA-registered commands and TLV parameters.

![thread](/assets/images/thread-net.png)

Thread also has a **Thread Management Framework (TMF)** for Thread devices to exchange network-wide configuration and operational data. These management procedures cover tasks such as commissioning (joining and authenticating devices), propagating shared network parameters (channel/PAN ID changes), maintaining connectivity, and collecting diagnostic information about devices and links.

TMF is founded on the **Constrained Application Protocol (CoAP)**. All Thread Management messages are carried over CoAP. There are some particularities:

- CoAP URIs: TMF uses specialized URIs (`coap://[<address>]:<port>/<api>/<message>`) where the scheme can be coap (when using underlying layer's security) or coaps over DTLS. No OSCORE is used atm, which could be beneficial for cases of untrusted gateways.
- Thread uses specialized ports: “Management Port” (abbreviated `:MM`) and "Commissioner Port" (:MC) depending on the transaction. It is unclear to me if those are used to identify the transactions.
- CoAP Methods: Only the `POST` method is used for Thread Management messages, no GET/PUT/DELETE and no PATCH or FETCH either. Also unclear to me atm why this was the design choice.
- CoAP Options: only a handful are used, Uri-Path, Content-Format, Accept and Block2 from the blockwise transfer RFC. It seems this is for retrieving large diagnostic files but could also be used for firmware updates.

TMF also defines 5 message types mapped onto CoAP:
1.	Request (.req) / Response (.rsp)
2.	Query (.qry) / Answer (.ans)
3.	Notification (.ntf)

As TMF run over UDP they use CoAP's in built reliability mechanisms with Confirmable (CON) messages. They combine the messages, to create different "transaction patterns" depending on the purpose of the interaction. I will not go into details on those but for example I they do not seem to use CoAP Observe on the notification pattern, which could be useful.

Messages can be addressed to unicast Ipv6 endpoints or multicast targetting link-local multicast groups. I did not see mentions to CoAP's default multicast address `FF0X::FD` rather `FF02::1`, `FF03::1`, or the “All Thread Nodes” addresses.

TMF's functionality is Commissioning & Configuration, Address Resolution & Routing, Diagnostics (e.g., battery/supply voltage, child tables, neighbor info, ...) and Network Management. In these CoAP is used as application layer encapsulation mostly, as I did not see a lot of web linking features that could be useful for discovery or querying.

The Commissioner is a special device (likely to be the smartphone) that helps manage authentication and provisioning of Joiners. I did not go into details but I would assume OAuth or PASSKEY would be used.

It was quite interesting to read about TMF cause on [LwM2M](https://www.openmobilealliance.org/release/LightweightM2M/V1_2_2-20240613-A/OMA-TS-LightweightM2M_Core-V1_2_2-20240613-A.pdf) we also use CoAP but in aslightly different way (also for different use cases) specifying components coming from a larger subset of RFCs done at [CoRE](https://datatracker.ietf.org/wg/core/about/) and other IETF WGs (e.g., RFC6690, RFC7641, RFC8613 or RFC9176 for example).