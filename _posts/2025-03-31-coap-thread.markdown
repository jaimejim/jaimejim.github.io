---
title: "Thread use of CoAP"
layout: post
date: 2025-03-31 14:50
tag:
- IoT
- Thread
- IETF
category: blog
author: jaime
headerImage: true
---

I have read the Thread v1.4.0 Specification (from sept 26,2024) and focused a bit on Chapter 10, these are my notes about it based only on the spec, as I am not a member of Thread.

First, for high level context [Thread](https://www.threadgroup.org/) is a standard for low-power, wireless communication of IP-meshed devices with a throughput in the range of the 250 kbps. The network is designed explicitly to avoid single points of failure. It is widely used for home automation, but also in smart buildings ([KNX IoT](https://www.knx.org/knx-en/for-professionals/benefits/knx-iot/)), smart lightning ([DALI+](https://www.dali-alliance.org/daliplus/)) and in other products via [Matter](https://csa-iot.org/all-solutions/matter/).

Every [iPhone 16](https://www.apple.com/iphone-16/specs/) model as well as new iPads and MacBooks quietly already come with Thread networking enabled. Also many home routers will also include Thread from the factory and it is present in Android [smart hubs](https://www.androidauthority.com/google-tv-streamer-smart-hub-3467634/). So it is a very relevant standard for those intereste din the IoT domain.

At a high level, Thread Devices can be Full Thread Devices (FTDs), like a router or a device acting as one on ocassion or End Devices (EDs); which can be always on or sleepy ones that do not route or forward messages and capable of running several years on AA batteries through optimized power cycles. Limited devices attach to more powerful router-like ones as the network topology or the device conditions change. See below a sample topology where a phone acts as commissioning tool.

![thread](/assets/images/thread-stack.png)

Thread uses several protocols standarized at the IETF; DHCP, URIs, URNs, UDP, DTLS, mDNS, DNS-SD, IPv6 and CoAP among many others. At the lowest layers (Physical and MAC) it uses IEEE 802.15.4 and IETF's IPv6 6LowPAN adaptation layers on top.

On top of 802.15.4 and IP, Thread uses UDP transport and has a protocol layer called Mesh Link Establishment (MLE), used for setting up and maintaining the mesh network. MLE messages are basically a dictionary-based command registered in IANA and a TLV sereies of parameters.

![thread](/assets/images/thread-net.png)

Thread also has a **Thread Management Framework (TMF)** for Thread devices to exchange network-wide configuration and operational data. These management procedures cover tasks such as commissioning (joining and authenticating devices), propagating shared network parameters (channel/PAN ID changes), maintaining connectivity, and collecting diagnostic information about devices and links.

TMF is founded on the **Constrained Application Protocol (CoAP)**. All Thread Management messages are carried over CoAP. There are some particularities:

- CoAP URIs: TMF uses specialized URIs (`coap://[<address>]:<port>/<api>/<message>`) where the scheme can be coap (when using underlying layer's security) or coaps over DTLS. No OSCORE is used atm, which would be beneficial for cases of untrusted gateways.
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