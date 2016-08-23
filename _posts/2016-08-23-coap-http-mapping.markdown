---
title: "HTTP-to-CoAP Mapping"
layout: post
date: 2016-06-10 09:00
tag:
- CoAP
- HTTP
blog: true
star: true
---

When discussing the state of current standardization and specially in my role as [CoRE WG](https://datatracker.ietf.org/wg/core/charter/) co-chair I often find myself having to think through on how to summarize and simplify what a draft is about. I find that exercise very useful and I thought of providing a series of short summaries about the drafts the WG is currently working on.

The first of such documents is the [Guidelines for HTTP-to-CoAP Mapping Implementations](https://tools.ietf.org/html/draft-ietf-core-http-mapping-13).

The point of the draft (soon RFC) is to describe how to do HTTP-to-CoAP Mapping to allow HTTP clients to access a CoAP Server via a proxy. This works under the assumption that, despite the similarities between CoAP and HTTP, not all browsers will implement support for it and that some legacy devices will need proxying. Another assumption is that users will like to use their smartphones with their home sensors.

The mapping is fairly straightforward in its **simple form**, you simply append one URI after the other (i.e. adding target uri or `/{+tu}` to the existing URI), for example: `http://p.example.com/hc/coap://s.example.com/light`. Other mapping might be discovered on `./well-known/core`, on those cases the HC should use resource type: `core.hc` and attribute type `hct`.

In the **enhanced form** more sophisticated mappings can be expressed. And certain template variables have been created for it, namely:

```java
s  = "coap" / "coaps"
hp = host [":" port]  
p  = path-abempty     
q  = query           
qq = [ "?" query ]      
```
The ABNF forms make use of RFC5234, RFC7252 and RFC6690. So you can do things like queries or specific paths to the sensor. For example you can specify you use secure coap and query for lights that are *on*.

`http://p.example.com/hc?s=coaps&hp=s.example.com&p=/light&q=on`

**Discovery** is also important both on the HTTP and the CoAP side. A sample discovery on the HTTP would look like this:

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

For CoAP devices, they should also get back an anchor URI of the HC proxy as well as the URI mapping. The following example shows a CoaP request with the `hct` attribute.

```java
Req:  GET coap://[ff02::1]/.well-known/core?rt=core.hc
Res:  2.05 Content
      </hc>;anchor="http://p.example.com";
      rt="core.hc";hct="?uri={+tu}"
```

The HC proxy also performs bidirectional **Media Type Mapping** of [Media Types](https://tools.ietf.org/html/rfc7231#section-3.1.1.1) and [content encodings](https://tools.ietf.org/html/rfc7231#section-3.1.2.2) into [CoAP Content-Formats](https://tools.ietf.org/html/rfc7252#section-12.3)

The mapping will depend on whether the application is tightly or loosely coupled with the proxy. For HTTP unsupported media types the HC Proxy should simply answer with a `415 Unsupported Media Type` response.
When dealing with an unrecognised CoAP "cf" the HC proxy can use the `application/coap-payload` and append that content format `;cf=` whichever is the content format number.

Although possible, **content transcoding** is generally not advisable as it would tamper with the payload and might cause loss of information.

At a really high level view, that is what the draft is about, if you are interested I really encourage you to read the draft, and if you want to use it there are several implementations available:

1. Squid HTTP-CoAP mapping module. <http://telecom.dei.unipd.it/iot>
2. HTTP-CoAP proxy based on EvCoAP. <https://github.com/koanlogic/webthings/tree/master/bridge/sw/lib/evcoap>
3. [Luebeck implementation](https://media.itm.uni-luebeck.de/people/kleine/poster_kleine_ssp.pdf) available here: <http://core.ietf.narkive.com/d4MCPLLl/http-coap-proxy-setup>
4. Californium also supports a HTTP-CoAP proxy function but they do not explicitly state that it is based on the draft. <http://www.eclipse.org/californium/>
