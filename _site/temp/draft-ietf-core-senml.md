##Status CoRE SenML

Author: [Jaime Jiménez](http://jaimejim.github.io/)

###Tentative Timeline
* [x] [draft summary](#summary)
* [ ] [Shepherd Writeup](#shepherd-writeup) @Jaime `in progress,  @due(16-08-15 15:28)`
* [ ] IESG Submission `@due(16-08-18 15:28)`

###Comments on v06
* Which is the implementation status of the draft?
* From IETF96, ...
* A formal review is required for new registries. Has this been initiated?
* A formal review is required for new media types. Have you checked that with media-types@iana.org?


###Editorial



------

<span id="summary"></span>
###Summary draft-ietf-core-senml-02

[Media Types for Sensor Markup Language (SenML)](https://tools.ietf.org/html/draft-ietf-core-senml-02)


----

<span id="shepherd-writeup"></span>
## Shepherd Writeup

###Summary

Document Shepherd: [Jaime Jiménez](jaime.jimenez@ericsson.com)
Area Director: [Alexey Melnikov](aamelnikov@fastmail.fm)

This specification defines media types for representing simple sensor measurements and device parameters in the Sensor Markup Language (SenML).  Representations are defined in JavaScript Object Notation (JSON), Concise Binary Object Representation (CBOR), eXtensible Markup Language (XML), and Efficient XML Interchange (EXI), which share the common SenML data model.  A simple sensor, such as a temperature sensor, could use this media type in protocols such as HTTP or CoAP to transport the measurements of the sensor or to be configured.

The document is intended for Standards Track.

###Review and Consensus

The document has gone through multiple expert reviews and has been discussed on multiple IETF meetings. Before the last IETF the WGLC was completed.

`TBD`

###Intellectual Property

Each author has stated that they do not have direct, personal knowledge of any IPR related to this document. I am not aware of any IPR discussion about this document on the CoRE WG.

` Ask authors, TBD`

###Other Points

`
TBD
`

###Checklist

* [x] Does the shepherd stand behind the document and think the document is ready for publication?
* [x] Is the correct RFC type indicated in the title page header?
* [x] Is the abstract both brief and sufficient, and does it stand alone as a brief summary?
* [x] Is the intent of the document accurately and adequately explained in the introduction?
* [ ] Have all required formal reviews (MIB Doctor, Media Type, URI, etc.) been requested and/or completed? `TBD`
* [ ] Has the shepherd performed automated checks -- idnits (see http://www.ietf.org/tools/idnits/ and the Internet-Drafts Checklist), checks of BNF rules, XML code and schemas, MIB definitions, and so on -- and determined that the document passes the tests? `Need information on how to check CDDL`
* [ ] Has each author stated that their direct, personal knowledge of any IPR related to this document has already been disclosed, in conformance with BCPs 78 and 79? `TBD once the last version is submitted`
* [ ] Have all references within this document been identified as either normative or informative, and does the shepherd agree with how they have been classified? `TBD`
* [ ] Are all normative references made to documents that are ready for advancement and are otherwise in a clear state? `TBD`
* [x] If publication of this document changes the status of any existing RFCs, are those RFCs listed on the title page header, and are the changes listed in the abstract and discussed (explained, not just mentioned) in the introduction? `Does not apply`
* [x] If this is a "bis" document, have all of the errata been considered? `Does not apply`

* **IANA** Considerations:

	* [x] Are the IANA Considerations clear and complete? Remember that IANA have to understand unambiguously what's being requested, so they can perform the required actions. `Are the new media type IDs assigned sequentially or do we request something concrete to IANA? URL to check http://www.iana.org/assignments/core-parameters/core-parameters.xhtml`
	* [x] Are all protocol extensions that the document makes associated with the appropriate reservations in IANA registries?
	* [ ] Are all IANA registries referred to by their exact names (check them in http://www.iana.org/protocols/ to be sure)? `The new media types require expert review.`
	* [ ] Have you checked that any registrations made by this document correctly follow the policies and procedures for the appropriate registries?
	* [ ] For registrations that require expert review (policies of Expert Review or Specification Required), have you or the working group had any early review done, to make sure the requests are ready for last call?
	* [ ] For any new registries that this document creates, has the working group actively chosen the allocation procedures and policies and discussed the alternatives? `New registries need to be registered on IANA`
	* [x]  Have reasonable registry names been chosen (that will not be confused with those of other registries), and have the initial contents and valid value ranges been clearly specified?
