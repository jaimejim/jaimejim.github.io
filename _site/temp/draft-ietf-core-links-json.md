##Status CoRE LINKS

Author: [Jaime Jiménez](http://jaimejim.github.io/)

###Tentative Timeline
* [x] [draft summary](#summary)
* [ ] [Shepherd Writeup](#shepherd-writeup) @Jaime `in progress, @due(10-08-15 15:28) `
	* [ ] Ask on Mailing list who has an implementation.
	* [ ] Check Christian's comments.
	* [x] Check Media Types @Jaime
* [ ] IESG Submission `@due(16-08-15 15:28)`

###Comments on v06
* Which is the implementation status of the draft?
	*  In Appendix A. Possibly others.
* Can all core-link relations or expressions be translated to JSON and CBOR? Is there no *loss in translation*? If there is, it should be mentioned in 2.2 if it hasn't already.
	* Authors don't think so, and agree it should be mentioned.
* From IETF96, JSON-LD was considered as an option by some, and as something to be left out of this draft for now. What is the author's opinion?
	* JSON-LD not on this draft, perhaps on a different one in the future.  
* Have Christian Amsüss <c.amsuess@energyharvesting.at> comments from the WGLC been addressed?
	* TBD.
* A formal review is required for new media types. Have you checked that with media-types@iana.org?
	* @Jaime to send email to media types mailing list, also CC CoAP parameters list (core-parameters@ietf.org) @Jaime to subscribe.
* Have table 1 references been checked at WGLC?
	* Will double-check.
* CDDL in figures 1 and 2 should be validated if they hadn't.
	* TBD.

###Editorial
* When converting between a bespoke syntax such as that defined by **CoRE Link Format** [RFC6690]

* IMO the following excerpt needs rewriting:
>This specification defines a common approach for translating between the CoRE-specific bespoke formats, JSON and CBOR formats.  Where applicable, mapping from other formats (e.g.  CoRE Link Format) into JSON or CBOR is also described.
>This specification defines a common format for representing CoRE Web Linking in JSON and CBOR.

	into something like this:

	>This specification defines a common format for representing CoRE Web Linking in JSON and CBOR, as well as translating from CoRE Link Format to both of them.

------

<span id="summary"></span>
###Summary draft-ietf-core-links-json-06

[Representing CoRE Formats in JSON and CBOR](https://tools.ietf.org/html/draft-ietf-core-links-json-06)

The draft defines a format for representing and translating Web links [RFC5988](https://tools.ietf.org/html/rfc5988) from CoRE link format [RFC6690](https://tools.ietf.org/html/rfc6690) to JSON (generic in use) and CBOR (used in the constrained space over CoAP)

Both formats are defined on their respective RFCs: JavaScript Object Notation (JSON) [RFC7159](https://tools.ietf.org/html/rfc7159) and Concise Binary Object Representation (CBOR) [RFC7049](https://tools.ietf.org/html/rfc7049).

A link-format document is a collection of web links `link-value`, each of which is a collection of attributes `link-param` applied to a `URI-Reference`. The [Information Model mapping](https://tools.ietf.org/html/draft-ietf-core-links-json-06#section-2.2) is straightforward for the collection of links and attributes, requiring CBOR an extra mapping to the encoded values, its CDDL being:

``` c
                                   +           +
links = [* link]                   |           |
link = {                           |  JSON     |
  href: tstr    ; resource URI     |           |
  * label => tstr / true           |           |
}                                  +           |
label = tstr / &(                              | CBOR
  href: 1,   rel: 2,        anchor: 3,         |
  rev: 4,    hreflang: 5,   media: 6,          |
  title: 7,  type: 8,       rt: 9,             |
  if: 10,    sz: 11,        ct: 12,            |
  obs: 13,                                     |
)                                              +
```

There is one example of mapping, answer to the following request to the CoAP Server:

``` c
REQ: GET /.well-known/core?anchor=/sensors/temp
```

Response form in CoRE Link Format:

``` c
</sensors>;ct=40;title="Sensor Index",
</sensors/temp>;rt="temperature-c";if="sensor",
</sensors/light>;rt="light-lux";if="sensor",
<http://www.example.com/sensors/t123>;anchor="/sensors/temp"
;rel="describedby",
</t>;anchor="/sensors/temp";rel="alternate"
```

Same response in JSON:

``` c
"[{"href":"/sensors","ct":"40","title":"Sensor
 Index"},{"href":"/sensors/temp","rt":"temperature-
 c","if":"sensor"},{"href":"/sensors/light","rt":"light-
 lux","if":"sensor"},{"href":"http://www.example.com/sensors/
 t123","anchor":"/sensors/
 temp","rel":"describedby"},{"href":"/t","anchor":"/sensors/
 temp","rel":"alternate"}]"
```

Same response in CBOR diagnostic format, in which there is a substitution of the [common attribute names](https://tools.ietf.org/html/draft-ietf-core-links-json-06#page-6):

``` c
[{1: "/sensors", 12: "40", 7: "Sensor Index"},
 {1: "/sensors/temp", 9: "temperature-c", 10: "sensor"},
 {1: "/sensors/light", 9: "light-lux", 10: "sensor"},
 {1: "http://www.example.com/sensors/t123", 3: "/sensors/temp",
  2: "describedby"},
 {1: "/t", 3: "/sensors/temp", 2: "alternate"}]
```

The full example of hexadecimal CBOR is found in [Section 2.4.2](https://tools.ietf.org/html/draft-ietf-core-links-json-06#page-8).

Sizewise the results are:

|Notation|Binary|Size|% to Link Format|
|:--|:-:|--:|--:|
|Link Format|no|257 bytes| -------- |
|JSON|no|321 bytes| > 25 % |
|CBOR|yes|203 bytes| < 21 % |

----

<span id="shepherd-writeup"></span>
## Shepherd Writeup

###Summary

Document Shepherd: [Jaime Jiménez](jaime.jimenez@ericsson.com)
Area Director: [Alexey Melnikov](aamelnikov@fastmail.fm)

JavaScript Object Notation, JSON (RFC7159) is a text-based data format which is popular for Web based data exchange.  Concise Binary Object Representation, CBOR (RFC7049) is a binary data format which has been optimized for data exchange for the Internet of Things (IoT). For many IoT scenarios, CBOR formats will be preferred since it can help decrease transmission payload sizes as well as implementation code sizes compared to other data formats.

Web Linking (RFC5988) provides a way to represent links between Web resources as well as the relations expressed by them and attributes of such a link. In constrained networks, a collection of Web links can be exchanged in the CoRE link format (RFC6690). Outside of constrained environments, it may be useful to represent these collections of Web links in JSON, and similarly, inside constrained environments, in CBOR. This specification defines a common format for this.

The document is intended for Standards Track.

###Review and Consensus

The document has gone through multiple expert reviews and has been discussed on multiple IETF meetings. Before the last IETF the WGLC was completed.

` Address comments section (on v 06) above please`

###Intellectual Property

Each author has stated that they do not have direct, personal knowledge of any IPR related to this document. I am not aware of any IPR discussion about this document on the CoRE WG.

` Ask authors, TBD`

###Other Points


###Checklist

* [x] Does the shepherd stand behind the document and think the document is ready for publication?
* [x] Is the correct RFC type indicated in the title page header?
* [x] Is the abstract both brief and sufficient, and does it stand alone as a brief summary?
* [x] Is the intent of the document accurately and adequately explained in the introduction?
* [ ] Have all required formal reviews (MIB Doctor, Media Type, URI, etc.) been requested and/or completed? `New media type entries (link-format+json and link-format+cbor) need verification by media-types@iana.org. The CDDL should be verified. `
* [ ] Has the shepherd performed automated checks -- idnits (see http://www.ietf.org/tools/idnits/ and the Internet-Drafts Checklist), checks of BNF rules, XML code and schemas, MIB definitions, and so on -- and determined that the document passes the tests? `Need information on how to check CDDL`
* [ ] Has each author stated that their direct, personal knowledge of any IPR related to this document has already been disclosed, in conformance with BCPs 78 and 79? `TBD once the last version is submitted`
* [x] Have all references within this document been identified as either normative or informative, and does the shepherd agree with how they have been classified? `Both seem correct to me`
* [x] Are all normative references made to documents that are ready for advancement and are otherwise in a clear state?
* [x] If publication of this document changes the status of any existing RFCs, are those RFCs listed on the title page header, and are the changes listed in the abstract and discussed (explained, not just mentioned) in the introduction? `Does not apply`
* [x] If this is a "bis" document, have all of the errata been considered? `Does not apply`

* **IANA** Considerations:

	* [x] Are the IANA Considerations clear and complete? Remember that IANA have to understand unambiguously what's being requested, so they can perform the required actions. `Are the new media type IDs assigned sequentially or do we request something concrete to IANA? URL to check http://www.iana.org/assignments/core-parameters/core-parameters.xhtml`
	* [x] Are all protocol extensions that the document makes associated with the appropriate reservations in IANA registries?
	* [ ] Are all IANA registries referred to by their exact names (check them in http://www.iana.org/protocols/ to be sure)? `The new two media types require expert review.`
	* [ ] Have you checked that any registrations made by this document correctly follow the policies and procedures for the appropriate registries?
	* [ ] For registrations that require expert review (policies of Expert Review or Specification Required), have you or the working group had any early review done, to make sure the requests are ready for last call?
	* [x] For any new registries that this document creates, has the working group actively chosen the allocation procedures and policies and discussed the alternatives? `no new registries`
	* [x]  Have reasonable registry names been chosen (that will not be confused with those of other registries), and have the initial contents and valid value ranges been clearly specified?
