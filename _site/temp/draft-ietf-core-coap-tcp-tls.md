## Status of CoAP TCP/TLS
Author: [Jaime Jiménez](http://jaimejim.github.io/)

### Timeline
1. [x] Announce Brian as editor.
2. [x] Announce Carsten as author for this doc, no chair hat.
3. [x] Announce the new Github repo.
4. [x] Move issues (10) to Github, copy-paste (Brian to confirm to Jaime) and then close on the tracker. Add Travis validation.
5. [x] Hannes and Carsten to work on one signaling document...
	* ... ~~as part of draft-ietf-core-coap-tcp-tls-03?~~
	* [x] ... as draft-bormann-core-coap-sig-00, then merge afterwards with tcp-tls-xx . Make draft available on separate Github repo.
6. [x] When ready add core-coap-websockets-XX. Get help from Klaus. Ready for merging now. Brian to start merging.
7. [x] WG Call for consensus of draft-bormann-core-block-bert-01 as we need to add that to tcp-tls-xx too.
8. [x] Keep working on <https://github.com/core-wg/coap-tcp-tls>

------
#### Summary draft-ietf-core-coap-tcp-tls-03
A TCP and TLS Transport for the Constrained Application Protocol (CoAP)](https://tools.ietf.org/html/draft-ietf-core-coap-tcp-tls-03)

This is the first merger by Brian Raymor. The main purpose of the draft is to enable TCP in networks where UDP-based connections could be blocked. It has three transports at the moment: TCP, TCP/TLS and WebSockets.  The assumption is that TCP can help NAT traversal as the NAT bindings will be kept for a longer time.

### CoAP over TCP

TCP does not have reliability-related messages (CON, NON CONF) Type and Message ID fields are also not used. The document indicates aso how to use UDP-to-TCP gateways.

##TBD

------
#### Summary draft-ietf-core-coap-tcp-tls-02

A TCP and TLS Transport for the Constrained Application Protocol (CoAP)](https://tools.ietf.org/html/draft-ietf-core-coap-tcp-tls-02)

This is a draft that simply describes a shim header that conveys length information about each CoAP message for use over TCP. CoAP header is changed from:

~~~
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Ver| T |  TKL  |      Code     |      Message ID   ...
| Token				                ...
~~~

to

~~~
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Len=13 |  TKL  | Length (8-bit)|      Code     | TKL bytes ...
~~~

Although message size limitations do not apply, [core-block](https://tools.ietf.org/html/draft-ietf-core-coap-tcp-tls-02#ref-I-D.ietf-core-block) should still be used for large payloads (>1k), the main reason (IMO) is to prevent head-of-line blocking and allow for other operations on the device.

Two new URI schemes are defined: `coap+tcp` (port 5683) or `coaps+tcp` (port 443, and using [RFC7301](https://tools.ietf.org/html/rfc7301), APLN Extension for CoAP)

**Comments**

* Add link to [http://conferences.sigcomm.org/imc/2010/papers/p260.pdf](http://conferences.sigcomm.org/imc/2010/papers/p260.pdf). Isn't the author Seppo Hätönen?
* Which is the status of ref-I-D.bormann-core-cocoa?
* Is the APLN Extension for CoAP defined? Section 8.3 the only part neded?
* **Very nice** comparison between `coap+udp` and `coap+tcp` headers, would be nice to have it in the other docs.

------

#### Summary Hannes' draft-ietf-core-coap-tcp-tls-02
[I need a link here]

It adds a new section, Shim Layer Protocol that is used for signaling and a framing section. It also presents some possible client/server exchange.

The handshake has a serve name indication, a version indication, connection closure and keep-alive exchanges.

**Comments**

* The introduction that explains the use cases on TCP-02-03 could use some more work to make it more similar to draft-savolainen-core-coap-websockets-06.  
* The new parts as they are do not seem as implementable/complete as the other documents.
* Are the keep-alive exchanges exactly the same as ping-pong messages on signalling&websockets docs cause it looks like that to me.
* Carsten should read. Carsten&Hannes should sync.

------

#### Summary draft-bormann-core-coap-sig-00
[CoAP Signaling Messages](https://tools.ietf.org/html/draft-bormann-core-coap-sig-00)

Signaling goes as any other CoAP message. Options, which can be elective or critical, have a different number space as the rest of the options. The draft defines 5 types of signaling messages.

1. Capability Messages
2. Settings Messages
3. Ping and Pong Messages
4. Release Messages
5. Abort Messages

**Comments**

* Early version. Hannes should read. Carsten&Hannes should sync.
* Capability and Settings should probably be separated.
* Diagrams, etc.

------

#### Summary draft-bormann-core-block-bert-01
[Block-wise transfers in CoAP](https://tools.ietf.org/html/draft-bormann-core-block-bert-01)

It connects back to the draft-ietf-core-coap-tcp-tls-02 document and how to use block for large payloads.

**Comments**

* References on TCP/TLS doc needed.
* The document could have been writen in more simple terms, it is quite hard to read.  
* Which of the 3 roles of block option is intended here?
* Value 7 for SZX would indicate a block size of 2048 and was reserved. the usage in this document would indicate that it isn't reserved anymore?
* Add something like the following to explain the diagrams: `Block Option:NUM/M/BlockSize`
* Sequence diagrams don't work well as visual representations for blocks.


------

#### Summary draft-savolainen-core-coap-websockets-06
[CoAP over WebSockets](https://tools.ietf.org/html/draft-savolainen-core-coap-websockets-06)

This document specifies how to retrieve and update CoAP resources using CoAP requests and responses over the WebSocket Protocol.

It introduces few senarios where this would be needed and the rationale for its usage: btw WS endpoints, with a CoAP Forwarding Proxy, and a CoAP Server inside a Web Browser (!?).

`coap+ws` uses port 80 as default. The WebSocket client includes `coap.v1` in the list of protocols to identify this one.

**Comments**

* What is the different between websockets and a plain tcp socket?
* **Shouldn't we have one document for "stream-based transports"?**
* The introduction and overview are **very good** and useful, I would have like to have this already on draft-ietf-core-coap-tcp-tls-02.
* **Shouldn't we have some template structure for all these documents?**
* CoAP Server inside a Web Browser (!?). This sounds like something from "Inception".
* The way it is presented, as a Delta over [RFC7252](https://tools.ietf.org/html/rfc7252) makes it **very readable**.
* Presents a similar problematic as the signalling document, shouldn't these be merged?

------

# CoAP-TCP-TLS Webex calls
### 10th June 2016


### Attendees

* Brian Raymor
* Hannes Tschofenig
* Carsten Bormann
* Simon Levy
* Klaus Hartke
* Matthias Kovatsch
* Jaime Jiménez

### Discussion

*Hannes*: Procedures, multiple drafts... merging with the CoAP over Websockets document. Some feel CoAP TCP draft is progressing a bit slow.
[CoAP-TCP-TLS](https://tools.ietf.org/html/draft-tschofenig-core-coap-tcp-tls-05)

*Carsten*: Let's do the Issue tracker later. Target is to move completely to github.  Technically the document is stable. There are some items:

**Open Issues**

- 387	Should ALPN always be required?
Yes, this is important.
- 390	Connection close reason	coap-tcp-tls			protocol enhancement.
Yes, this should be a feature of the signalling.
- 394	Ping/pong
There is a need to keep the NAT binding alive.
- 395	Session resumption.
No, makes it too complex for the server.
- 400	Give better guidance on message sizes for CoAP over TCP/TLS.
Warning that this won't easilly interface with UDP ones.
- Shim layer issues?

*Hannes*: I feel that there are still several issues open.

*Carsten*: Well we agree on the problem maybe on the solution.

*Hannes*: I proposed a solution and there can be very issues. However, it seems that there is no "bert document"(?!) is about reinterpreting the message length differently.

*Carsten*: Today we had a discussion about the bert approach and was useful, we need to maintain the architectural integrity.

*Hannes*: My hope was to get something out soon, get feedback, spin the document again, etc. Discussions need to happen on the mailing list. We need to involve them.

*Carsten*: Agreed we got some formal contributions and we need to discuss them.

*Brian*: It feels a bit discouraging to have to wait for your approval on the direction. We should have iterative discussions. The draft is not stable now at 0.2.

*Hannes*: It takes too long to move this forward.

*Brian*: I agree with Hannes. We can work on the ping-pong issues.

*Carsten*: Some of the changes are big architectural changes. The pingpong issue is rather small. That's why this is done in separate drafts. Right now the TCP draft is implementable, if we start adding half-baked stuff it is no longer implementable.

*Brian*: It is fine to have some period of unstability. I am concern that the chair is also the editor.

*Carsten*: I am not the chair on this one, Jaime is...

*Jaime*: Have to read it through and understand it better to provide meaningful feedback.

... audio choppy ...

*Hannes*: Is the expectation that each version is implementable standalone? Other issues? Many folks on OMA are interested.

*Matthias*: We don't care about the speed that much. We need more ...


----------

(choppy audio change to phone call)

----------

*Discussion*: With Websockets people believe you don't get firewall, ...issues with proxies, firewalls, etc... it is all funky stuff.

*Hannes*: I would like more information on this, cause it could be interesting.

*Carsten*: Websockets integration is editorial work. A single document for applications, websockets text should be on the tcp/tls document. It is easier to integrate the two documents.

*Hannes*: What about timeline for the integration.

*Brian*: Are we going to use it as is? MQTT uses it. Why would we change the framing.

*Carsten*: Which changes?

*Brian*: The websocket draft calls out a number of cases where there is information removed. The TCP draft would remove the same.

*Carsten*: It is more about ... (couldn't get that) ...

*Hannes*: The use cases have been described are not the same. The websockets document, the initial handshacking happens over TCP.

*Klaus*: It is more or less the same.

*Hannes*: Simon was suggesting to focus on the handshake mechanism.

*Klaus*: Websockets and TLS is not the same as TLS and TCP.

*Hannes*: Simon, do you still think the idea of using TLS is a good idea?

*Simon*:I think it is something we should entertain, the direction that QUIK took is good.

*Hannes*: Some of the LoWPAN think that link layer security is sufficient. It is just a question about which cypher.

*Matthias*: Do we get the lenght information, signaling, etc, that we need?

*Hannes*: Length yes... rest somewhat.

*Carsten*: There is no way to use the TLS framing as the CoAP framing. We can simply use the websockets framing. We have CoAP over UDP and was good. CoAP over TCP does not add complexity.

*Hannes*: Why was it a good decission?

*Carsten*: CoAP would not exist if we have said that it only works over DTLS.

*Matthias*: The length information we can get it with all three transports, even if there is redundant information. For the signalling, people wanna have some keepalive for their applicaitons, I am not sure this works with TLS.

*Hannes*: I tried to capture all this options in the issue tracker.

*Matthias*: We have a nice assumption that TCP/TLS and Websockets would work, what I see is missing is the signalling.

*Hannes*: I provided a write-up for how to do that. We have two write-ups on the signalling exchange, we have a websockets document, how do we make everyone happy.

*Klaus*: Make divisions for the draft...

*Matthias*: Websockets draft has a technical description is a bit outdated but there is useful text that we could move over. We have to be careful with

*Hannes*: Have Carsten edited the document We have two incomplete versions and we need to ... Brian was confused about which draft to integrate.

*Klaus*: Websockets should be made later. First the signalling document.

- Stable 0.2 Document.
- Bert part can be put back.
- Signalling part needs discussion. Best way to do it would be to extract Hannes work and put it on the right place.
- Issues are on the document sent by Hannes/Brian.

*Matthias/Carsten/Hannes*:
ClientHello/ServerHello solves issues raised in the issue tracker.

ETC ETC

------

### 16th June 2016

### Attendees

* Brian Raymor
* Hannes Tschofenig
* Carsten Bormann
* Simon Levy
* Klaus Hartke
* Jaime Jiménez

### Discussion

**387**	Should ALPN always be required?

* Yes. To be closed.

**400**	Give better guidance on message sizes for CoAP over TCP/TLS

* Length information sufficient?
* Is Max-Message-Size option sufficient?

**409**	CoAP over TCP: Supporting block-wise for larger block sizes (BERT)

* Wait for 22nd on BERT. Move to repo

**388**	Multiple versions over the same connection

* No multiple version over same connection.
* On earlier doc was possible, now after changes it no longer applies.
* How do we indicate the version now? (independent issue)

**390**	Connection close reason

* Scenario is a server reboot, tell clients you are not going to be available or that there is a failover server.
* Retry after alternative service

**391**	Server name indication

* Move issue to Github signalling draft.

**392**	Converting URIs to options and back

* Closed.

**393**	Observing resource over reliable transports

* Move to Github.
* Take it on mailing list.

**394**	Ping/pong

* PinPong using resource does not allow for custody option. Also it is too verbose messagewise.
* [Hybi discussion as reference](http://www.ietf.org/mail-archive/web/hybi/current/msg09540.html). Focuses more on liveness than keepalives, just sends Ping. [Firefox discussion](https://groups.google.com/forum/#!searchin/spdy-dev/ping/spdy-dev/xgyPztsAKls/HdQUvRdmMZMJ)
* [HTTP/2 RFC](https://tools.ietf.org/html/rfc7540#section-6.7)
* [Heartbeat extension in TLS](https://tools.ietf.org/html/rfc6520) as reference.
* Discussion on mailing list.
* Move to the Signalling Github.
