##Status CoAP HTTP Mapping

Author: [Jaime Jiménez](http://jaimejim.github.io/)

###Timeline
* [x] Send issues back to authors  `@due(16-06-15 21:30)`.
* [x] HTTP Mapping Second WGLC `@due(16-06-22 15:28)`.
* [x] [Shepherd Writeup](#shepherd-writeup) @Jaime  `@due(16-07-09 15:28)`.
* [x] HTTP mapping IESG submission `@due(16-07-19 15:31)` `@done(16-07-22 15:31)` .

###Comments on v10
* This question might be a naive one but of the existing mappings, why have `{+cu}` or `{+su}` if `{+tu}` superseeds both?
	* Agreed, change to `{+cu}` only.
* For the content transcoding part you might want to mention some of the work done in ACE draft-selander-ace-object-security. I leave it to your discretion as content transcoding is not really advisable. Also the Object Security is still a draft.
	* Not relevant at this point.  
* Which is the implementation status of the draft?
	1. Squid HTTP-CoAP mapping module, Angelo Castellani. 	<http://telecom.dei.unipd.it/iot>
	2. HTTP-CoAP proxy based on EvCoAP, Thomas Fossati, and Salvatore Loreto.
	<https://github.com/koanlogic/webthings/tree/master/bridge/sw/lib/evcoap>
	3. FIWARE (Ericsson) implementation.
	<https://forge.fiware.org/plugins/mediawiki/wiki/fiware/index.php/Gateway_Device_Management_-_Ericsson_Gateway_-_User_and_Programmers_Guide#HTTP-CoAP_mapping>
	4. German University (Oliver Kleine) implementation, <https://media.itm.uni-luebeck.de/people/kleine/poster_kleine_ssp.pdf> available here: <http://core.ietf.narkive.com/d4MCPLLl/http-coap-proxy-setup>
	5. Californium also supports a HTTP-CoAP proxy function but they do not explicitly state that it is based on our draft. <http://www.eclipse.org/californium/>

###Editorial
* First time `{+tu}` is used probably should be expanded to "target uri" or similar.
* "There is no default **mapping** for the HC Proxy URI."
* "it **would** be able to successfully forward."

------

###Summary draft-ietf-core-http-mapping-10

[Guidelines for HTTP-to-CoAP Mapping Implementations](https://tools.ietf.org/html/draft-ietf-core-http-mapping-10)

Describes how to do HTTP-to-CoAP Mapping to allow HTTP clients to access a CoAP Server via a proxy.

It introduces [four possible entities](https://tools.ietf.org/html/draft-ietf-core-http-mapping-10#section-2), the HC Proxy, a Forward Proxy, a Reverse Proxy and an Interception Proxy.

They define basic [use cases](https://tools.ietf.org/html/draft-ietf-core-http-mapping-10#section-4): legacy building control apps, making sensor data available to 3rd parties and smartphone for using home sensors. 

The mapping has multiple parts: URI Mapping, Media Type Mapping, Response Mapping and Other Additional Mapping Guidelines. 

[CoAP URI mapping](https://tools.ietf.org/html/draft-ietf-core-http-mapping-10#section-5) is needed on cases where `coap` and `coaps` are is not supported by default on browsers/network tools. 

In the **simple form** there are few mapping templates for coap.  The default URI mapping consist on appending one URI after the other (i.e. adding target uri or `/{+tu}`), for example: `http://p.example.com/hc/coap://s.example.com/light`. Other mapping might be discovered on `./well-known/core`, on those cases the HC should use resource type: `core.hc` and attribute type `hct`. All the possible mappings are:

``` js
// default mapping
/{+tu}
// for coap uris
?coap_target_uri={+cu}
// for coaps uris
?coaps_target_uri={+su}
// either
?target_uri={+tu}

```

In the **enhanced form** more sophisticated mappings can be expressed. And certain template variables have been created for it:

```js
s  = "coap" / "coaps" 
hp = host [":" port]  
p  = path-abempty     
q  = query           
qq = [ "?" query ]      
```
The ABNF forms make use of RFC5234, RFC7252 and RFC6690. So you can do things like queries or specific paths to the sensor. For example you can specify you use secure coap and query for lights that are *on*.

`http://p.example.com/hc?s=coaps&hp=s.example.com&p=/light&q=on`

There is a **discovery**  process for the HC functionality both on the HTTP and the CoAP side. A sample discovery on the HTTP would look like this:

```js
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

```js
Req:  GET coap://[ff02::1]/.well-known/core?rt=core.hc
Res:  2.05 Content
      </hc>;anchor="http://p.example.com";
      rt="core.hc";hct="?uri={+tu}"
```

The HC proxy also performs bidirectional **Media Type Mapping** of [Media Types](https://tools.ietf.org/html/rfc7231#section-3.1.1.1) and [content encodings](https://tools.ietf.org/html/rfc7231#section-3.1.2.2) into [CoAP Content-Formats](https://tools.ietf.org/html/rfc7252#section-12.3)

The mapping will depend on whether the application is tightly or loosely coupled with the proxy. For HTTP unsupported media types the HC Proxy should simply answer with a `415 Unsupported Media Type` response.
When dealing with an unrecognised CoAP "cf" the HC proxy can use the `application/coap-payload` and append that content format `;cf=` whichever is the content format number.

CoAP content formats are more limited or tightly coupled to applications than Internet ones. Thus, it is not possible to have fine-grained subclasses and optional parameters, instead you get a simple integer value. To solve that the draft optionally proposes looser coupling for specific types like XML, JSON or others.

Although possible, **content transcoding** is generally not advisable as it would tamper with the payload and might cause loss of information. 

----

<span id="shepherd-writeup"></span>
## Shepherd Writeup

###Summary

Document Shepherd: [Jaime Jiménez](jaime.jimenez@ericsson.com)
Area Director: [Alexey Melnikov](aamelnikov@fastmail.fm)

This document provides reference information for implementing a cross-protocol network proxy that performs translation from the HTTP protocol to the CoAP protocol.  This will enable a HTTP client to access resources on a CoAP server through the proxy.  This document describes how a HTTP request is mapped to a CoAP request, and then how a CoAP response is mapped back to a HTTP response.  This includes guidelines for URI mapping, media type mapping and additional proxy implementation issues.  This document covers the Reverse, Forward and Interception cross-protocol proxy cases.
   
The document is intended as an Informational RFC.

###Review and Consensus

The document has gone through multiple expert reviews over the years and was last presented on IETF95. 

There are several implementations available:

1. Squid HTTP-CoAP mapping module, Angelo Castellani. <http://telecom.dei.unipd.it/iot>
2. HTTP-CoAP proxy based on EvCoAP, Thomas Fossati, and Salvatore Loreto. <https://github.com/koanlogic/webthings/tree/master/bridge/sw/lib/evcoap>
3. FIWARE (Ericsson) implementation. <https://forge.fiware.org/plugins/mediawiki/wiki/fiware/index.php/Gateway_Device_Management_-_Ericsson_Gateway_-_User_and_Programmers_Guide#HTTP-CoAP_mapping>
4. Oliver Kleine implementation, <https://media.itm.uni-luebeck.de/people/kleine/poster_kleine_ssp.pdf> available here: <http://core.ietf.narkive.com/d4MCPLLl/http-coap-proxy-setup>
5. Californium uses the default URI Mapping (section 5.3): <http://example.org/proxy/coap://coap.example.org>

###Intellectual Property

Each author has stated that they do not have direct, personal knowledge of any IPR related to this document. I am not aware of any IPR discussion about this document on the CoRE WG.

###Other Points

Appendix-A should be removed before publication. <https://tools.ietf.org/html/draft-ietf-core-http-mapping-12#appendix-A>

On the IANA section, the part that describes `Interoperability considerations: 
Published specification: (this I-D - TBD)` should be updated with the `RFCXXXX` reference.

Few changes since the shepherds review, see: <https://tools.ietf.org//rfcdiff?url1=https://tools.ietf.org/id/draft-ietf-core-http-mapping-10.txt&url2=https://tools.ietf.org/id/draft-ietf-core-http-mapping-13.txt>

The working group has very good consensus on this document as it is. HTTP mapping aspects raised by future CoAP extensions will then be addressed by these extensions or in separate documents.

###Checklist

* [x] Does the shepherd stand behind the document and think the document is ready for publication?
* [x] Is the correct RFC type indicated in the title page header?
* [x] Is the abstract both brief and sufficient, and does it stand alone as a brief summary?
* [x] Is the intent of the document accurately and adequately explained in the introduction?
* [x] Have all required formal reviews (MIB Doctor, Media Type, URI, etc.) been requested and/or completed?

``` 
Yes, some edits have been done, see https://tools.ietf.org//rfcdiff?url1=https://tools.ietf.org/id/draft-ietf-core-http-mapping-10.txt&url2=https://tools.ietf.org/id/draft-ietf-core-http-mapping-13.txt 
``` 

* [x] Has the shepherd performed automated checks -- idnits (see http://www.ietf.org/tools/idnits/ and the Internet-Drafts Checklist), checks of BNF rules, XML code and schemas, MIB definitions, and so on -- and determined that the document passes the tests? 

``` 
No errors, but some warnings are shown about existing ABNF. 
I aggregated all CoAP ABNF refs here: http://jaimejim.github.io/temp/coap-abnf
```

* [x] Has each author stated that their direct, personal knowledge of any IPR related to this document has already been disclosed, in conformance with BCPs 78 and 79?

* [x] Have all references within this document been identified as either normative or informative, and does the shepherd agree with how they have been classified?
* [x] Are all normative references made to documents that are ready for advancement and are otherwise in a clear state?

```
Clear state, but non-Standard reference 
[I-D.ietf-core-block]
``` 
* [x] If publication of this document changes the status of any existing RFCs, are those RFCs listed on the title page header, and are the changes listed in the abstract and discussed (explained, not just mentioned) in the introduction? ```Does not apply``` 
* [x] If this is a "bis" document, have all of the errata been considered? ```Does not apply``` 

* IANA Considerations:
	* [x] Are the IANA Considerations clear and complete? Remember that IANA have to understand unambiguously what's being requested, so they can perform the required actions.
	* [x] Are all protocol extensions that the document makes associated with the appropriate reservations in IANA registries?
	* [x] Are all IANA registries referred to by their exact names (check them in http://www.iana.org/protocols/ to be sure)?
	* [x] Have you checked that any registrations made by this document correctly follow the policies and procedures for the appropriate registries?
	* [x] For registrations that require expert review (policies of Expert Review or Specification Required), have you or the working group had any early review done, to make sure the requests are ready for last call?
	* [x] For any new registries that this document creates, has the working group actively chosen the allocation procedures and policies and discussed the alternatives?
```No registries are created. ``` 

	* [x]  Have reasonable registry names been chosen (that will not be confused with those of other registries), and have the initial contents and valid value ranges been clearly specified? ```No registries are created.``` 
