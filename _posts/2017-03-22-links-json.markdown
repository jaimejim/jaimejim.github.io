---
title: "Representing CoRE Formats in JSON and CBOR"
layout: post
date: 2017-03-22 11:00
image: /assets/images/dolls.jpg
tag:
- CoAP
- JSON
- CBOR
- IETF

blog: true
star: true
---

Continuing with the summary series about coming standards, I will explain a bit about the [Representing CoRE Formats in JSON and CBOR](https://tools.ietf.org/html/draft-ietf-core-links-json-07) draft. If you are interested on other such posts, please check [Mapping HTTP to CoAP](/coap-http-mapping/) too.

The point of this draft (soon RFC) is to define a format for representing and translating Web links [RFC5988](https://tools.ietf.org/html/rfc5988) from CoRE link format [RFC6690](https://tools.ietf.org/html/rfc6690) to JSON [RFC7159](https://tools.ietf.org/html/rfc7159) and CBOR [RFC7049](https://tools.ietf.org/html/rfc7049). While JSON is a very generic and well-known format at the moment, we expect CBOR to become popular for those bandwidth savy or working on constrained devices. What this draft then defines is then the translations: Link-Format --> JSON --> CBOR.

Let's explain it with examples. If your CoAP client sends a query to a CoAP server as below.

```
REQ: GET /.well-known/core
```

What would you get back?

**1. Response in Link-Format**
Link-Format is a series of web links. Each link (or `link-value`) is composed of attributes `link-param` applied to a `URI-Reference`. The uncompressed example below shows one such collection that could be received as response.

``` c
</sensors>;ct=40;title="Sensor Index",

</sensors/temp>;rt="temperature-c";if="sensor",

</sensors/light>;rt="light-lux";if="sensor",

<http://www.example.com/sensors/t123>; anchor="/sensors/temp";rel="describedby",

</t>;anchor="/sensors/temp";rel="alternate"
```

**2. Response in JSON**

Same as before but this time we would do a mapping adding the appropriate JSON tags.

``` c
"[ {"href":"/sensors","ct":"40","title":"Sensor
 Index"},

 {"href":"/sensors/temp","rt":"temperature-
 c","if":"sensor"},

 {"href":"/sensors/light","rt":"light-
 lux","if":"sensor"},

 {"href":"http://www.example.com/sensors/
 t123","anchor":"/sensors/
 temp","rel":"describedby"},

 {"href":"/t","anchor":"/sensors/
 temp","rel":"alternate"}]"
```

**3. Response in CBOR**

CBOR would have two variants, pure CBOR in hexadecimal, which would a priori be unintelligible for readers:

``` c
85a301680c623430076c ...
```

Or CBOR diagnostic format which would look like this:

``` c
[{1: "/sensors", 12: "40", 7: "Sensor Index"},
  {1: "/sensors/temp", 9: "temperature-c", 10: "sensor"},
  {1: "/sensors/light", 9: "light-lux", 10: "sensor"},
  {1: "http://www.example.com/sensors/t123", 3: "/sensors/temp",
   2: "describedby"},
  {1: "/t", 3: "/sensors/temp", 2: "alternate"}]
```  

The [model mapping](https://tools.ietf.org/html/draft-ietf-core-links-json-06#section-2.2) is straightforward for the collection of links and attributes, requiring CBOR an a bit of an extra mapping to the encoded values, its CDDL being:

``` c
                                   +           +
links = [* link]                   |           |
link = {                           |  JSON     |
  href: tstr    ; resource URI     |           |
  * label => tstr / true           |           |
}                                  |           |
href =1                            +           |
label = tstr / &(                              | CBOR
  rel: 2,        anchor: 3,                    |
  rev: 4,    hreflang: 5,   media: 6,          |
  title: 7,  type: 8,       rt: 9,             |
  if: 10,    sz: 11,        ct: 12,            |
  obs: 13,                                     |
)                                              +
```

In general lines, this was the draft. If you wonder how much more efficient each format is over the others, the CBOR is definitely more compact:

|Notation|Binary|Size|% to Link Format|
|:--|:-:|--:|--:|
|Link Format|no|257 bytes| -------- |
|JSON|no|321 bytes| > 25 % |
|CBOR|yes|203 bytes| < 21 % |
