---
title: "Mapping HTTP to CoAP"
layout: post
date: 2016-08-23 11:00
tag:
- CoAP
- HTTP
- IETF
blog: true
star: true
---

**Menu 2:** this is a menu this is a [url](asasass.google.com)

When discussing the state of current standardization I often find myself having to think through on how to summarize and simplify what a draft is about. I find that exercise very useful and I thought of providing a series of short summaries about the drafts the WG is currently working on.

The first of such documents is the [Guidelines for HTTP-to-CoAP Mapping Implementations](https://tools.ietf.org/html/draft-ietf-core-http-mapping-13).

The point of the draft (soon RFC) is to describe how to do HTTP-to-CoAP Mapping to allow HTTP clients to access a CoAP Server via a proxy. This works under the assumption that, despite the similarities between CoAP and HTTP, not all browsers will implement support for it and that some legacy devices will need proxying. Another assumption is that users will like to use their smartphones with their home sensors. The set up would look like this:

![HTTP-to_CoAP Mapping Scenario](/assets/images/pic_http_coap.jpg)

The mapping is fairly straightforward as CoAP is designed to mirror HTTP. In its **simple form**, you simply append one URI after the other, for example:

`http://p.example.com/hc/coap://s.example.com/light`

If you are using other mappings, you might do a search on `./well-known/core` to discover them, they should be using resource type: `core.hc` and attribute type `hct`.

In the **enhanced form** more sophisticated mappings can be expressed. And certain template variables have been created for it:

```java
s  = "coap" / "coaps"
hp = host [":" port]  
p  = path-abempty     
q  = query           
qq = [ "?" query ]      
```
The ABNF forms make use of RFC5234, RFC7252 and RFC6690, for ~~morbid curiosity~~ simplicity you can check the [list of CoAP-related ABNF forms I made](http://jaimejim.github.io/temp/coap-abnf). Thanks to all this, we can specify for example that we want to use secure CoAP and query for lights that are *on*.

```c
Req:  GET http://p.example.com/hc?s=coaps&hp=s.example.com&p=/light&q=on
```

**Discovery** is also important both on the HTTP and the CoAP side. A sample HTTP discovery on the proxy would look like this:

```c
Req:  GET /.well-known/core?rt=core.hc HTTP/1.1
      Host: p.example.com

Res:  HTTP/1.1 200 OK
      Content-Type: application/link-format
      Content-Length: 18
	  // if plain link-format
	  </hc>;rt="core.hc"
	  // if JSON link-format
	  [{"href":"/hc","rt":"core.hc"}]
```

If it is the CoAP devices that are querying the proxy, they should also get back an anchor URI of the HC proxy as well as the URI mapping.

```c
Req:  GET coap://[ff02::1]/.well-known/core?rt=core.hc
Res:  2.05 Content
      </hc>;anchor="http://p.example.com";
      rt="core.hc";hct="?uri={+tu}"
```

The HC proxy also performs bidirectional **Media Type Mapping** of [Media Types](https://tools.ietf.org/html/rfc7231#section-3.1.1.1) and [content encodings](https://tools.ietf.org/html/rfc7231#section-3.1.2.2) into [CoAP Content-Formats](https://tools.ietf.org/html/rfc7252#section-12.3)

The mapping will depend on whether the application is tightly or loosely coupled with the proxy. For HTTP unsupported media types the HC Proxy should simply answer with a `415 Unsupported Media Type` response.
When dealing with an unrecognised CoAP "cf" the HC proxy can use the `application/coap-payload` and append that content format `;cf=` whichever is the content format number.

Although possible, **content transcoding** is generally not advisable as it would tamper the payload and might cause loss of information (and mess other things in general).

At a really high level view, that is what the draft is about, if you are interested I really encourage you to read the draft, and if you want to use it there are several implementations available:

1. [Squid HTTP-CoAP mapping module.](http://telecom.dei.unipd.it/iot)
2. [HTTP-CoAP proxy based on EvCoAP.](https://github.com/koanlogic/webthings/tree/master/bridge/sw/lib/evcoap)
3. [Luebeck implementation](http://core.ietf.narkive.com/d4MCPLLl/http-coap-proxy-setup)
4. Californium also supports a [HTTP-CoAP proxy function](http://www.eclipse.org/californium/) but they do not explicitly state that it is based on the draft.
