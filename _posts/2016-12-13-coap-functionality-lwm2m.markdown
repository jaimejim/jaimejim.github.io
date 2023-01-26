---
title: "CoAP functionality on LWM2M"
layout: post
date: 2016-12-13 16:00
tag:
- Device Management
- CoAP
- LWM2M
- IETF
blog: true
star: true
---

Last [IETF 97](https://datatracker.ietf.org/meeting/97/agenda.html) has been particularly interesting for me. Not only did CoRE WG had 3 sessions instead of the usual two, which shows how many topics we have ongoing, but also there was a lot of extra discussion around security and management of IoT Devices. In particular there are other IETF groups that are starting to look into the alternatives built around CoAP for managing networks.

There has been a lot of excellent work done by the LWM2M groups in Eclipse and OMA over the years, building the necessary interfaces and data models for managing constrained devices. Two very popular Open Source Implementations have arisen as a result, Wakaama and [Leshan](https://github.com/eclipse/leshan/). We have been using both together with [coap-node](https://www.npmjs.com/package/coap-node) for our prototyping.

One thing that has proven problematic for some use cases has been that LWM2M was designed focusing on operators and direct device management. This is not a bad thing per se, but some of the use cases we are interested in are for **device to device** communication without having to contact *the mothership*.

Reusing LWM2M for applications seemed straighforward at first but perhaps the best way to present it is using LWM2M purely for management and CoAP with the same Object Model (i.e. IPSO) for Applications.

I gave a short presentation at the "Managing Networks of Things workshop", organized by the Network Management Research Group. The [presentation slides](http://jaimejim.github.io/slides/nmrgsoulfinal.pdf) present the possible CoAP usages for Device Management available and illustrates the [draft-jimenez-t2trg-coap-functionality-lwm2m internet draft](https://datatracker.ietf.org/doc/draft-jimenez-t2trg-coap-functionality-lwm2m/) with the same title that I recently submitted to the T2TRG.

The diagram below shows some of the cases. (1) would be the pure LWM2M, for device management, (2) would be device to device and (3) would be for applications on the browser or phone.

```
    Device               +
    +--------+--------+  |     (1)         +----------+--------------+
    |        |        |  |    LWM2M        |          | LWM2M Server |
    | LWM2M  | IPSO   |  | <-------------> |  Manager +--------------+
    +--------+--------+  |                 |          | BS Server    |
    |                 |  |                 +----------+--------------+
    |      CoAP       |  |     (2)
    +--------+--------+  |    CoAP+IPSO    +----------+
    |        |        |  | <-------------> | Device   |
    | UDP    |  TCP   |  |                 +----------+
    +-----------------+  |     (3)
    |      IPv6       |  |    CoAP+IPSO    +-------------------------+
    |                 |  | <-------------> | User / Application      |
    +-----------------+  |                 +-------------------------+
                         +    
```

Some of the suggestions on (1) like TLS for CoAP over TCP and using better compression mechanisms like CBOR were actually already on the Eclipse pipeline and will be added soon. However, developers targeting to do (2) have to be aware of LWM2M caveats and will have to follow [CoAP](https://tools.ietf.org/html/rfc7252), [CoAP Observe](https://tools.ietf.org/html/rfc7641) and [Resource Directory](https://datatracker.ietf.org/doc/draft-ietf-core-resource-directory/) more closely.

Last, it is also noteworthy the work at CoRE WG on [Management over CoAP (COMI/COOL)](https://datatracker.ietf.org/doc/slides-97-core-consolidated-slides/). It has several similarities with LWM2M but also many differences, one of the biggest being the the use of YANG as modeling language ([you can model LWM2M Objects in YANG](https://tools.ietf.org/html/draft-vanderstok-core-yang-lwm2m-00) btw, although it does not look pretty) and the use of numbers as identifiers (SID identifiers) which will affect the IANA Registry in the near future (slide 169 and onwards).

It seems clear now that we will have more collaboration between organizations developing CoAP-based device management standards.
