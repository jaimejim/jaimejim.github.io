## Status T2TRG CoRAL
Author: [Jaime Jiménez](http://jaimejim.github.io/)

### Comments on v00

**[JJ]** On CoRE Apps
>  Applications that don't wish to register a relation type can use an
   extension relation type, which is a URI that uniquely identifies the
   relation type (similar to a URI used as an XML namespace names).  For
   example, an application can use "http://example.com/foo" as link
   relation type without having to register it.

   * Is the link relation "http://example.com/foo" or is it what comes after the host (i.e. "foo").

**[KH]** It's "http://example.com/foo". The idea is to avoid registration in a central place by including a domain name under your control in the link relation type. So there is no collision between "http://uni-bremen.de/foo" and "http://ericsson.com/foo". The same concept is used in XML namespace names.

**[JJ]** On the first example `"/abs_link/", "/terms... " etc are not part of the serialization. Which is the format of the example (does not look like CBOR)?

**[KH]** That's CBOR Extended Diagnostic Format <https://tools.ietf.org/html/draft-greevenbosch-appsawg-cbor-cddl-08#appendix-G>. Text enclosed in slashes are comments <https://tools.ietf.org/html/draft-greevenbosch-appsawg-cbor-cddl-08#appendix-G.5>.

In JSON the same example would be written as `[ 0, 64, [ 3, 0, 4, "coap", 6, "example.com", 11, 5683, 12, "info", 12, "tos" ] ]`.

So it's really just arrays with a bunch of numbers and strings.

**[JJ]** To represent multiple transport support, you would need to make another section where you define the numeric identifier for each transport. The serialization will contain then one link relation per transport supported, right? If so is there a link relation type called "transport" just like the one you have for "format"?

**[KH]** Let's say there is a CoAP server that supports both CoAP-over-UDP and CoAP-over-TCP. Then the easiest way to inform a CoAP client of the transports is to provide two links; for example

```
  <link rel="stylesheet" type="text/css" href="coap://example.org/bla.css"/>
  <link rel="stylesheet" type="text/css" href="coap+tcp://example.org/bla.css"/>
```
in HTML syntax (except that a web browser would try to load both stylesheets and not pick the link with the preferred transport).

("stylesheet" is the link relation type here; it indicates the meaning of the link, namely that the link target is a stylesheet that should be applied to the link source. "type" is a link attribute, not a link relation type; it indicates the media type of the stylesheet; since we have content formats in CoAP, the equivalent link attribute is called "format" in Coral)

Note how the hrefs in the two links are the same except for the URI scheme. So one could imagine a more compact way to express two links that differ only in the URI scheme, like

`<link rel="stylesheet" type="text/css" href="{coap or coap+tcp}://example.org/bla.css"/>`

That's what I plan for the next version of Coral.

**[JJ]** Are there other registries that should be known other than these three?
  <http://www.iana.org/assignments/media-types>.
  <http://www.iana.org/assignments/media-type-structured-suffix>.
  <http://www.iana.org/assignments/core-parameters>.

**[KH]** The complete list from the core-apps draft is

* URI schemes: http://www.iana.org/assignments/uri-schemes
* Media types and content formats
<http://www.iana.org/assignments/media-types>
<http://www.iana.org/assignments/media-type-structured-suffix>
<http://www.iana.org/assignments/core-parameters>
* Link relation types : <http://www.iana.org/assignments/link-relations>
* Form relation types needs to be Well-known URIs
<http://www.iana.org/assignments/well-known-uris>

**[JJ]** Are there other changes to the serialisation other than using numeric identifiers for the link relations? New symbols or formats that extend CBOR?

**[KH]** I'm using numeric identifiers for content formats, methods, link relation types and form relation types. URIs and link attributes are expressed as array elements; this does not require anything that CBOR (or JSON) does not already provide.

**[JJ]** Are `<<<` and `>>>` new separators? Are they already part of CBOR?

**[KH]** Yes, these are new separators. They represent binary data (which CBOR already supports, so it's just an extension to the CBOR Diagnostic Format).

**[JJ]** Which is flag in the example?
> A flag in the serialized link indicates

**[KH]** The flags are a bit difficult to spot in the example. They are encoded in the first array element; see Figure 1 in the Coral draft.

**[JJ]** I don't get the namespaces in 2.3. Does CoRAL also gives numeric identifiers to those? Who hosts the registry of those identifiers?

**[KH]** There are two types of link relation types: link relation types registered in the IANA registry and extension link relation types (see <https://tools.ietf.org/html/rfc5988#section-4>). In Coral, you can only use numeric relation type identifiers, not string identifiers. So someone has to map the string identifiers to the numeric identifiers somewhere. For registered relation types, the idea is to delegate this  task to IANA. For extension relation types, the idea is that the application designers maintains the mapping somewhere.

**[JJ]** You don't use ABNF notation in Section 3. How does CBOR validate it?

**[KH]** That's CDDL notation (<https://tools.ietf.org/html/draft-greevenbosch-appsawg-cbor-cddl-07>).


### Summary of v00
[The Constrained RESTful Application Language (CoRAL)](https://tools.ietf.org/html/draft-hartke-t2trg-coral-00)

CoRAL is
> a compact, binary representation format (serialization format) for Web links and forms that is based on the Concise Binary Object Representation (CBOR)

Web links, as defined by [RFC5988](https://tools.ietf.org/html/rfc5988#section-3) are comprised of context, a link relation type, a link target URI and, optionally, a set of target attributes.

CoRAL uses [I-D.hartke-core-apps] link relation types. Which are the same as the ones in the IANA registry <http://www.iana.org/assignments/link-relations/link-relations.xhtml> but with a number as identifier in order to save bandwidth. New identifiers can be registered with IANA.

Example:

The Web link:

```
 <coap://example.com/info/tos>;rel=terms-of-service;type=text/plain
```

CoRAL serialization:

```
[ /abs_link/          0,
       /terms-of-service/ 64,
       [ /format/          3, 0 /text//plain/,
         /href.scheme/     4, "coap",
         /href.host.name/  6, "example.com",
         /href.port/      11, 5683,
         /href.path/      12, "info",
         /href.path/      12, "tos" ]]
```

Representations of the link's target can also be added after the link.

CoRAL also supports Forms, instead of *link-relation* types, *form-relation* types are used.

The **Data Format**
