##Status CoRE ETCH

Author: [Jaime Jiménez](http://jaimejim.github.io/)

###Tentative Timeline
* [x] [draft summary](#summary)
* [x] [Shepherd Writeup](#shepherd-writeup) @Jaime `in progress` `@due(16-07-15 15:28) -> Delayed @due(10-08-15 15:28) `.
* Q/A
	* [x] Are there implementations of the draft?
	* [x] IPR declaration.
 	* [ ] Content Format check in progress.
	* [x] Normative reference core-block.

* [x] IESG submission `@due(16-07-25 15:31) -> Delayed @due(16-08-24 15:28) `.

###Comments on v01
* >"FETCH request cannot be generated from a link alone".
	* sorry for the naive question but I would like to know the main difference between FETCH and simply adding query parameters to the URI, using the "?". That could be something to be added to the document.
	* Limited to UTF8 and cannot provide type for the query parameters (we want to use CBOR query parameters).

* What about Response Codes in RFC7252 that operate on full resource representations, do they apply? What happens when multiple resources get modified, you get one response per resource or per request? `I assume per request/transaction`
	* Yes, it will depend on the payload formatting. Answers will be added as an array to the response payload (in FETCH,PATCH does not need that).

* >"The difference between the PUT and PATCH requests is extensively documented in [RFC5789]."
	* I didn't find the HTTP PATCH document that extensive on documenting the difference. But there are some good paragraphs on section 2. I think you should consider adding some explanation on the PATCH section, something on those lines:

	* >"With PATCH, however, the enclosed entity contains a set of instructions describing how a resource currently residing on the origin server should be modified to produce a new version.  The PATCH method affects the resource identified by the Request-URI, and it also MAY have side effects on other resources; i.e., new resources may be created, or existing ones modified, by the application of a PATCH."
		* It is a normative reference and people should read it in order to understand it.

* As it was pointed out, the FETCH media types are not defined.
	* There are no new media types, existing media types are used. Content Format registry is being addressed.

* if the If-Match header is there on the PATCH request is used for HTTP idempotent operations. For CoAP a new iPATCH method is used instead (or so I understood). Is this correct?
	*  Not quite. IF-MATCH is used if you need to know something about the structure of the resource.  

* What are the implications on the HTTP Mapping draft-ietf-core-http-mapping? Where will the HTTP PATCH -> CoAP PATCH be done?
	* TBD on another document.

* Which is the implementation status of the draft?
	*  None known.

* Have you checked with an expert for the media types? A formal review is required for the shepherd writeup to be complete.
	* No KNEW media types. The owner of the Content Format registry should have a look (Zach Shelby).

###Comments on v02

* IMO WGLC comments have been addressed.

###Editorial
* *as specified in sections 5.9*.
	* The link does not point to RFC7252.
* Extra " typo on  *"y-coord": 45",*

------

<span id="summary"></span>
###Summary draft-ietf-core-etch-01

[Patch and Fetch Methods for Constrained Application Protocol (CoAP)](https://tools.ietf.org/html/draft-ietf-core-etch-01)

This document adds three new CoAP methods, FETCH, to perform the equivalent of a GET with a request body; and the twin methods PATCH and iPATCH, to perform partial modifications of an existing CoAP resource.

[FETCH](https://tools.ietf.org/html/draft-ietf-core-etch-01#page-5) is modelled after the HTTP GET operation. A *normal* GET returns a representation of resource identified by the URI. In FETCH the server returns a representation as specified by the request parameters, thus it can't be assumed to be complete. Requests can be expressed as form relations on [CoRE Application Descriptions](https://tools.ietf.org/html/draft-hartke-core-apps-03).
FETCH operations don't alter the state of the targeted resource, thus are safe and idempotent, the responses are cacheable. CoAP Observe can also be used on a FETCH request.

Being this a resource in JSON:

```c
 {
 	"x-coord": 256,
  	"y-coord": 45,
	"foo": ["bar","baz"]
 }
```
The Request would be:

``` c
FETCH CoAP://www.example.com/object
Content-Format: NNN (application/example-map-keys+json)
Accept: application/json
[
	"foo"
]
```

The server response would be:

``` c
2.05 Content
Content-Format: 50 (application/json)
{
	"foo": ["bar","baz"]
}
```

[PATCH and iPATCH](https://tools.ietf.org/html/draft-ietf-core-etch-01#page-5) are mapped after the [HTTP PATCH method](https://tools.ietf.org/html/rfc5789)

The PUT payload normally contains a full representation of a resource. PATCH payload contains a set of instructions describing how a resource on the origin server should be modified to produce a new version.  The PATCH method affects the resource identified by the Request-URI, and it also **MAY have side effects on other resources**,  new resources may be created, or existing ones modified.

In fact the PATCH method strikes me as pretty dangerous for multiple reasons:

1. As seen above PATCH has effect on multiple resources.
2. Collisions can also occur and the resource might be corrupted for the subsequent PATCH operations (PATCH is not safe nor idempotent).

Neither PATCH nor iPATCH guarantee that that a resource can be modified.

To ensure idempotent operations HTTP PATCH clients use a strong ETag [RFC2616] in an If-Match header on the PATCH request; CoAP uses a new method iPATCH.

Original document in JSON:

```c
 {
   	"x-coord": 256,
    "y-coord": 45,
    "foo": ["bar","baz"]
 }
```

As an example of PATCH request:

```c
REQ: iPATCH CoAP://www.example.com/object
Content-Format: 51 (application/json-patch+json)
[
   { "op":"replace", "path":"x-coord", "value":45}
]
```

JSON document final state:

``` c
 {
	"x-coord": 45,
    "y-coord": 45,
    "foo": ["bar","baz"]
 }
```

There is a whole set of [possible errors and how can they be handled](https://tools.ietf.org/html/draft-ietf-core-etch-01#page-12).

----

<span id="shepherd-writeup"></span>
## Shepherd Writeup

###Summary

Document Shepherd: [Jaime Jiménez](jaime.jimenez@ericsson.com)
Area Director: [Alexey Melnikov](aamelnikov@fastmail.fm)

The existing Constrained Application Protocol (CoAP) methods only allow access to a complete resource.  This does not permit applications to access parts of a resource.  In case of resources with larger or complex data, or in situations where a resource continuity is required, replacing or requesting the whole resource is undesirable.  Several applications using CoAP will need to perform partial resource accesses.

Similar to HTTP, the existing Constrained Application Protocol (CoAP) GET method only allows the specification of a URI and request parameters in CoAP options, not the transfer of a request payload detailing the request.  This leads to some applications to using POST where actually a cacheable, idempotent, safe request is desired.

Again similar to HTTP, the existing Constrained Application Protocol (CoAP) PUT method only allows to replace a complete resource.  This also leads applications to use POST where actually a cacheable, possibly idempotent request is desired.

This specification adds new CoAP methods, FETCH, to perform the equivalent of a GET with a request body; and the twin methods PATCH and iPATCH, to modify parts of an existing CoAP resource.

The document is intended as an Standards Track RFC.

###Review and Consensus

The document has gone through multiple expert reviews and has been discussed on multiple IETF meetings. Before the last IETF the WGLC was completed.

There are no known implementations available.

###Intellectual Property

Each author has stated that they do not have direct, personal knowledge of any IPR related to this document. I am not aware of any IPR discussion about this document on the CoRE WG.

###Other Points
>
There is a downref to RFC 2616: This is in there because the security considerations of RFC 7252 reference (the now obsoleted) RFC 2616. The authors are not aware of someone having done the work to collect the relevant security considerations from the splinters of RFC 2616 (RFC 7230 and following).


###Checklist

* [x] Does the shepherd stand behind the document and think the document is ready for publication?
* [x] Is the correct RFC type indicated in the title page header?
* [x] Is the abstract both brief and sufficient, and does it stand alone as a brief summary?
* [x] Is the intent of the document accurately and adequately explained in the introduction?
* [x] Have all required formal reviews (MIB Doctor, Media Type, URI, etc.) been requested and/or completed?
* [x] Has the shepherd performed automated checks -- idnits (see http://www.ietf.org/tools/idnits/ and the Internet-Drafts Checklist), checks of BNF rules, XML code and schemas, MIB definitions, and so on -- and determined that the document passes the tests?
` There is no ABNF in this draft`
* [x] Has each author stated that their direct, personal knowledge of any IPR related to this document has already been disclosed, in conformance with BCPs 78 and 79?
* [x] Have all references within this document been identified as either normative or informative, and does the shepherd agree with how they have been classified?
`There is a normative reference to [I-D.ietf-core-block] but that shouldn't be a problem as it is in late stages`
* [x] Are all normative references made to documents that are ready for advancement and are otherwise in a clear state?
* [x] If publication of this document changes the status of any existing RFCs, are those RFCs listed on the title page header, and are the changes listed in the abstract and discussed (explained, not just mentioned) in the introduction? `Does not apply`
* [x] If this is a "bis" document, have all of the errata been considered? `Does not apply`

* **IANA** Considerations:

	* [x] Are the IANA Considerations clear and complete? Remember that IANA have to understand unambiguously what's being requested, so they can perform the required actions.
`I wonder if adding a link to the CoRE Parameters registry could help, but it looks OK to me. `
`http://www.iana.org/assignments/core-parameters/core-parameters.xhtml#method-codes`
	* [x] Are all protocol extensions that the document makes associated with the appropriate reservations in IANA registries?
	* [x] Are all IANA registries referred to by their exact names (check them in http://www.iana.org/protocols/ to be sure)?
`The two new entries to the content format registry (51 and 52) require expert review and a request has been SENT to that list.`
	* [x] Have you checked that any registrations made by this document correctly follow the policies and procedures for the appropriate registries?
	* [x] For registrations that require expert review (policies of Expert Review or Specification Required), have you or the working group had any early review done, to make sure the requests are ready for last call?
	* [x] For any new registries that this document creates, has the working group actively chosen the allocation procedures and policies and discussed the alternatives?
`no new registries`
	* [x]  Have reasonable registry names been chosen (that will not be confused with those of other registries), and have the initial contents and valid value ranges been clearly specified?
