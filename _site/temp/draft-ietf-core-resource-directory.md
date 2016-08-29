##Status CoRE Resource Directory

Author: [Jaime Jiménez](http://jaimejim.github.io/)

###Tentative Timeline
* [ ] [draft summary](#summary)
* [ ] [Shepherd Writeup](#shepherd-writeup) @Jaime `in progress,  @due(16-09-05 15:28)`
* [ ] IESG Submission `@due(16-09-18 15:28)`

###Comments on v06
* Which is the implementation status of the draft?
* From IETF96, ...
* A formal review is required for new registries, resource types, etc. Has this been initiated? (RD Parameter Registry, new resource types, IPv6 ND option, Link Extensions)
* Others have pointed out on the mailing list that the "function set" should be RESTful services.
* make sure we can register any format that is a list of Web links and provide special lookup (e.g., for OCF and WoT stuff)
* Also for For hypermedia-driven services (links and forms in the entry points)
* Somewhere it should be said what a *directory server* is, Section 4 - Finding a Directory Server or the terminology section for example. I assume it is a server that implements the RD "entity" and associated REST interfaces.
* You could consider adding a ref to [RFC7650](https://tools.ietf.org/html/rfc7650) on [section 4](https://tools.ietf.org/html/draft-ietf-core-resource-directory-08#section-4):
	*  *A Directory Server can also be found via a DHT lookup (RFC7650).*
* On section 4.1. you probably should write a line about [Secure Neighbour Discovery (SEND)](https://tools.ietf.org/html/rfc3971), for those who can use security certified
* In a local network, I would assume people don't need to talk to network administrators for setting up a Resource Directory. Why isn't there some fixed IPv6 multicast address for it as one of the options on 4.


###Editorial

* On the terminology section, shouldn't the Endpoint definition be that of [RFC7252](https://tools.ietf.org/html/rfc7252#page-6)?
* The following example seems a bit random now, I would simply remove it, since RD is intended pretty much for ANY EP type:

> (for example EPs installed on vehicles enabling tracking of
   their position for fleet management purposes and monitoring
   environment parameters)

* "using IPv6 neighbor Discovery (ND)" capital N.


adsasd

------

<span id="summary"></span>
###Summary of core-resource-directory-08

[CoRE Resource Directory](https://tools.ietf.org/html/draft-ietf-core-resource-directory-08)

The Resource Directory is an entity that hosts descriptions of resources held on other servers, allowing lookups to be performed for those resources via REST interfaces.

The general architecture specifies the interfaces towards the EPs that register resources and towards clients that perform queries. Of course, constrained devices will often act in either role.

```
                Registration     Lookup, Group
                 Interface        Interfaces
     +----+          |                 |
     | EP |----      |                 |
     +----+    ----  |                 |
                   --|-    +------+    |
     +----+          | ----|      |    |     +--------+
     | EP | ---------|-----|  RD  |----|-----| Client |
     +----+          | ----|      |    |     +--------+
                   --|-    +------+    |
     +----+    ----  |                 |
     | EP |----      |                 |
     +----+
```


The **Use cases** vary, as the RD is an entity posed to be whenever CoAP is used. Often RD is co-located with bootstrapping nodes and used during bootstrapping to discover and register other devices. Another common case is that of data brokers, since applications do not have knowledge about who is the data consumer they can use the RD lookup to find links to relevant Endpoint data sources.

A server that implements the RD [can be found](https://tools.ietf.org/html/draft-ietf-core-resource-directory-08#section-4) by using IPv6 neighbour discovery, static configurations, DHCPv6 options... or even a well-known multicast address in some cases.

If IPv6 Neighbour Discovery (ND) is used, there is a new option: *Resource Directory Address Option (RDAO)* that includes the IPv6 address of the RD in the payload.

Discovery

Registration

RD Function Set

Group Function Set

DNS-SD mapping

Examples

----

<span id="shepherd-writeup"></span>
## Shepherd Writeup

###Summary

Document Shepherd: Jaime Jiménez, <jaime.jimenez@ericsson.com>
Area Director: Alexey Melnikov, <aamelnikov@fastmail.fm>

In many M2M applications, direct discovery of resources is not practical due to sleeping nodes, disperse networks, or networks where multicast traffic is inefficient.  These problems can be solved by employing an entity called a Resource Directory (RD), which hosts descriptions of resources held on other servers, allowing lookups to be performed for those resources.  This document specifies the web interfaces that a Resource Directory supports in order for web servers to discover the RD and to register, maintain, lookup and remove resources descriptions.  Furthermore, new link attributes useful in conjunction with an RD are defined.

The document is intended for Standards Track.

###Review and Consensus

The document has gone through multiple expert reviews and has been discussed on multiple IETF meetings. Before the last IETF the WGLC was completed.

`TBD`

###Intellectual Property

Each author has stated that they do not have direct, personal knowledge of any IPR related to this document. I am not aware of any IPR discussion about this document on the CoRE WG.

`TBD`

###Other Points

`TBD`

###Checklist

* [x] Does the shepherd stand behind the document and think the document is ready for publication?
* [x] Is the correct RFC type indicated in the title page header?
* [x] Is the abstract both brief and sufficient, and does it stand alone as a brief summary?
* [x] Is the intent of the document accurately and adequately explained in the introduction?
* [ ] Have all required formal reviews (MIB Doctor, Media Type, URI, etc.) been requested and/or completed?
`TBD`
* [x] Has the shepherd performed automated checks -- idnits (see http://www.ietf.org/tools/idnits/ and the Internet-Drafts Checklist), checks of BNF rules, XML code and schemas, MIB definitions, and so on -- and determined that the document passes the tests?
`Does not apply`
* [ ] Has each author stated that their direct, personal knowledge of any IPR related to this document has already been disclosed, in conformance with BCPs 78 and 79?
`TBD`
* [ ] Have all references within this document been identified as either normative or informative, and does the shepherd agree with how they have been classified? `TBD`
* [ ] Are all normative references made to documents that are ready for advancement and are otherwise in a clear state?
`TBD`
* [ ] If publication of this document changes the status of any existing RFCs, are those RFCs listed on the title page header, and are the changes listed in the abstract and discussed (explained, not just mentioned) in the introduction?
`TBD`
* [x] If this is a "bis" document, have all of the errata been considered?
`Does not apply`

* **IANA** Considerations:

	* [ ] Are the IANA Considerations clear and complete? Remember that IANA have to understand unambiguously what's being requested, so they can perform the required actions.
	`TBD`
	* [ ] Are all protocol extensions that the document makes associated with the appropriate reservations in IANA registries?
	`TBD`
	* [ ] Are all IANA registries referred to by their exact names (check them in http://www.iana.org/protocols/ to be sure)?
	`TBD`
	* [ ] Have you checked that any registrations made by this document correctly follow the policies and procedures for the appropriate registries?
	`TBD`
	* [ ] For registrations that require expert review (policies of Expert Review or Specification Required), have you or the working group had any early review done, to make sure the requests are ready for last call?
	`TBD`
	* [ ] For any new registries that this document creates, has the working group actively chosen the allocation procedures and policies and discussed the alternatives? `TBD`
	* [ ]  Have reasonable registry names been chosen (that will not be confused with those of other registries), and have the initial contents and valid value ranges been clearly specified?
	`TBD`
