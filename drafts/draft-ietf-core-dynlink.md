---
title: "Dynamic Resource Linking for Constrained RESTful Environments"
abbrev: Dynamic Resource Linking for CoRE
docname: draft-ietf-core-dynlink-04
date: 2017-09-14
category: info

ipr: trust200902
area: art
workgroup: CoRE Working Group
keyword: [Internet-Draft, CoRE, CoAP, Link Binding, Observe]

stand_alone: yes
pi: [toc, sortrefs, symrefs]

author:
- ins: Z. Shelby
  name: Zach Shelby
  organization: ARM
  street: 150 Rose Orchard
  city: San Jose
  code: 95134
  country: FINLAND
  phone: "+1-408-203-9434"
  email: zach.shelby@arm.com
- ins: Z.V. Vial
  name: Matthieu Vial
  organization: Schneider-Electric
  street: '' 
  city: Grenoble
  code: ''
  country: FRANCE
  phone: "+33 (0)47657 6522"
  email: matthieu.vial@schneider-electric.com
- ins: M. Koster
  name: Michael Koster
  organization: SmartThings
  street: 665 Clyde Avenue
  city: Mountain View
  code: 94043
  country: USA
  email: michael.koster@smartthings.com
- ins: C. Groves
  name: Christian Groves
  organization: Huawei
  street: '' 
  city: ''
  code: ''
  country: Australia
  email: cngroves.std@gmail.com
- ins: J. Zhu
  name: Julian Zhu
  org: Huawei
  street: No.127 Jinye Road, Huawei Base, High-Tech Development District
  city: Xi’an, Shaanxi Province
  code: ''
  country: China
  email: jintao.zhu@huawei.com
- role: editor
  ins: B. Silverajan
  name: Bilhanan Silverajan
  org: Tampere University of Technology
  street: Korkeakoulunkatu 10
  city: Tampere
  code: 'FI-33720'
  country: Finland
  email: bilhanan.silverajan@tut.fi

normative:
  RFC2119:
  RFC5988:
  RFC6690:

  
informative:
  RFC7252:
  RFC7641:
  

--- abstract

 For CoAP {{RFC7252}} Dynamic linking of state updates between resources, either on an endpoint or between endpoints, is defined with the concept of Link Bindings. This specification defines conditional observation attributes that work with Link Bindings or with CoAP Observe {{RFC7641}}.
 
 Editor's note:
 
 o The git repository for the draft is found at https://github.com/core-wg/dynlink

--- middle

Introduction        {#introduction}
============

IETF Standards for machine to machine communication in constrained environments describe a REST protocol and a set of related information standards that may be used to represent machine data and machine metadata in REST interfaces. CoRE Link-format is a standard for doing Web Linking {{RFC5988}} in constrained environments. 

This specification introduces the concept of a Link Binding, which defines a new link relation type to create a dynamic link between resources over which to exchange state updates. Specifically, a Link Binding is a link for binding the state of 2 resources together such that updates to one are sent over the link to the other. CoRE Link Format representations are used to configure, inspect, and maintain Link Bindings. This specification additionally defines a set of conditional Observe Attributes for use with Link Bindings and with the standalone CoRE Observe {{RFC7641}} method.

Terminology     {#terminology}
===========
The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",   "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this specification are to be interpreted as described in {{RFC2119}}.

This specification requires readers to be familiar with all the terms and concepts that are discussed in {{RFC5988}} and {{RFC6690}}.  This specification makes use of the following additional terminology:

Link Binding:
: A unidirectional logical link between a source resource and a destination resource, over which state information is synchronized.

State Synchronization:
: Depending on the binding method (Polling, Observe, Push) different REST methods may be used to synchronize the resource values between a source and a destination. The process of using a REST method to achieve this is defined as "State Synchronization". The endpoint triggering the state synchronization is the synchronization initiator.

Link Bindings        {#bindings}
=============
In a M2M RESTful environment, endpoints may directly exchange the content of their resources to operate the distributed system. For example, a light switch may supply on-off control information that may be sent directly to a light resource for on-off control. Beforehand, a configuration phase is necessary to determine how the resources of the different endpoints are related to each other. This can be done either automatically using discovery mechanisms or by means of human intervention and a so-called commissioning tool. In this specification the abstract relationship between two resources is called a link Binding. The configuration phase necessitates the exchange of binding information so a format recognized by all CoRE endpoints is essential. This specification defines a format based on the CoRE Link-Format to represent binding information along with the rules to define a binding method which is a specialized relationship between two resources. The purpose of a binding is to synchronize the content between a source resource and a destination resource. The destination resource MAY be a group resource if the authority component of the destination URI contains a group address (either a multicast address or a name that resolves to a multicast address). Since a binding is unidirectional, the binding entry defining a relationship is present only on one endpoint. The binding entry may be located either on the source or the destination endpoint depending on the binding method. 

Binding Methods    {#binding_methods}
---------------

A binding method defines the rules to generate the web-transfer exchanges that synchronize state between source and destination resources. By using REST methods content is sent from the source resource to the destination resource. 

The following table gives a summary of the binding methods defined in this specification.

 | Name    | Identifier  | Location    | Method        |
 | Polling | poll        | Destination | GET           |
 | Observe | obs         | Destination | GET + Observe |
 | Push    | push        | Source      | PUT           |
{: #bindsummary title="Binding Method Summary"}

The description of a binding method must define the following aspects:

Identifier: 
: This is the value of the &quot;bind&quot; attribute used to identify the method.

Location: 
: This information indicates whether the binding entry is stored on the source or on the destination endpoint.

REST Method: 
: This is the REST method used in the Request/Response exchanges.

Conditions: 
: A binding method definition must state how the condition attributes of the abstract binding definition are actually used in this specialized binding.

The binding methods are described in more detail below.

###Polling

The Polling method consists of sending periodic GET requests from the destination endpoint to the source resource and copying the content to the destination resource. The binding entry for this method MUST be stored on the destination endpoint. The destination endpoint MUST ensure that the polling frequency does not exceed the limits defined by the pmin and pmax attributes of the binding entry. The copying process MAY filter out content from the GET requests using value-based conditions (e.g based on the Change Step, Less Than, Greater Than attributes).

###Observe
 
The Observe method creates an observation relationship between the destination endpoint and the source resource. On each notification the content from the source resource is copied to the destination resource. The creation of the observation relationship requires the CoAP Observation mechanism {{RFC7641}} hence this method is only permitted when the resources are made available over CoAP. The binding entry for this method MUST be stored on the destination endpoint. The binding conditions are mapped as query string parameters (see {{observation}}).

###Push 

When the Push method is assigned to a binding, the source endpoint sends PUT requests to the destination resource when the binding condition attributes are satisfied for the source resource. The source endpoint MUST only send a notification request if the binding conditions are met. The binding entry for this method MUST be stored on the source endpoint.


Link Relation    {#relation_type}
------
Since Binding involves the creation of a link between two resources, Web Linking and the CoRE Link-Format are a natural way to represent binding information. This involves the creation of a new relation type, named "boundto". In a Web link with this relation type, the target URI contains the location of the source resource and the context URI points to the destination resource. 

Binding Attributes     {#binding_attributes}
----------------

Web link attributes allow a fine-grained control of the type of state synchronization along with the conditions that trigger an update. This specification defines the attributes below:

| Attribute         | Parameter | Value            |
| Binding method    | bind      | xsd:string       |
| Minimum Period (s)| pmin      | xsd:integer (>0) |
| Maximum Period (s)| pmax      | xsd:integer (>0) |
| Change Step       | st        | xsd:decimal (>0) |
| Greater Than      | gt       | xsd:decimal      |
| Less Than         | lt       | xsd:decimal      |
{: #weblinkattributes title="Binding Attributes Summary"}
 
###Bind Method (bind)

This is the identifier of a binding method which defines the rules to synchronize the destination resource. This attribute is mandatory.

###Minimum Period (pmin) {#pmin}

When present, the minimum period indicates the minimum time to wait (in seconds) before triggering a new state synchronization (even if it has changed). In the absence of this parameter, the minimum period is up to the synchronization initiator. The minimum period MUST be greater than zero otherwise the receiver MUST return a CoAP error code 4.00 "Bad Request" (or equivalent).

###Maximum Period (pmax) {#pmax}
When present, the maximum period indicates the maximum time in seconds between two consecutive state synchronizations (regardless if it has changed). In the absence of this parameter, the maximum period is up to the synchronization initiator. The maximum period MUST be greater than zero and MUST be greater than the minimum period parameter (if present) otherwise the receiver MUST return a CoAP error code 4.00 "Bad Request" (or equivalent).

###Change Step (st) {#st}
When present, the change step indicates how much the value of a resource SHOULD change before triggering a new state synchronization (compared to the value of the previous synchronization). Upon reception of a query including the st attribute the current value (CurrVal) of the resource is set as the initial value (STinit). Once the resource value differs from the STinit value (i.e. CurrVal >= STinit + ST or CurrVal <= STint - ST) then a new state synchronization occurs. STinit is then set to the state synchronization value and new state synchronizations are based on a change step against this value. The change step MUST be greater than zero otherwise the receiver MUST return a CoAP error code 4.00 "Bad Request" (or equivalent).

Note: Due to the state synchronization based update of STint it may result in that resource value received in two sequential state synchronizations differs by more than st.

###Greater Than (gt) {#gt}
When present, Greater Than indicates the upper limit value the resource value SHOULD cross before triggering a new state synchronization. State synchronization only occurs when the resource value exceeds the specified upper limit value. The actual resource value is used for the synchronization rather than the gt value. If the value continues to rise, no new state synchronizations are generated as a result of gt. If the value drops below the upper limit value and then exceeds the upper limit then a new state synchronization is generated. 

###Less Than (lt) {#lt}
When present, Less Than indicates the lower limit value the resource value SHOULD cross before triggering a new state synchronization. State synchronization only occurs when the resource value is less than the specified lower limit value. The actual resource value is used for the synchronization rather than the lt value. If the value continues to fall no new state synchronizations are generated as a result of lt. If the value rises above the lower limit value and then drops below the lower limit then a new state synchronization is generated. 

### Attribute Interactions

Pmin, pmax, st, gt and lt may be present in the same query. 

If pmin and pmax are present in a query then they take precedence over the other parameters. Thus even if st, gt or lt are met, if pmin has not been exceeded then no state synchronization occurs. Likewise if st, gt or lt have not been met and pmax time has expired then state synchronization occurs. The current value of the resource is used for the synchronization. If pmin time is exceeded and st, gt or lt are met then the current value of the resource is synchronized. If st is also included, a state synchronization resulting from pmin or pmax updates STinit with the synchronized value.

If gt and lt are included gt MUST be greater than lt otherwise an error CoAP error code 4.00 "Bad Request" (or equivalent) MUST be returned.

If st is included in a query with a gt or lt attribute then state synchronizations occur only when the conditions described by st AND gt or st AND gl are met. 


Binding Table     {#binding_table}
=============
The binding table is a special resource that gives access to the bindings on a endpoint. A binding table resource MUST support the Binding interface defined below. A profile SHOULD allow only one resource table per endpoint.

Binding Interface Description    {#interfaces}
----------------------
This section defines a REST interface for Binding table resources. The interface supports the link-format type.

The if= column defines the Interface Description (if=) attribute value to be used in the CoRE Link Format for a resource conforming to that interface. When this value appears in the if= attribute of a link, the resource MUST support the corresponding REST interface described in this section. The resource MAY support additional functionality, which is out of scope for this specification. Although this interface description is intended to be used with the CoRE Link Format, it is applicable for use in any REST interface definition. 

The Methods column defines the REST methods supported by the interface, which are described in more detail below. 

| Interface | if=      | Methods           | Content-Formats |
| Binding   | core.bnd | GET, POST, DELETE | link-format     |
{: #intdesc title="Binding Interface Description"}

The Binding interface is used to manipulate a binding table. A request with a POST method and a content format of application/link-format simply appends new bindings to the table. All links in the payload MUST have a relation type &quot;boundTo&quot;. A GET request simply returns the current state of a binding table whereas a DELETE request empties the table. Individual entries may be deleted from the table by specifying the resource path in a DELETE request.

The following example shows requests for adding, retrieving and deleting bindings in a binding table.

~~~~
Req: POST /bnd/ (Content-Format: application/link-format)
<coap://sensor.example.com/s/light>;
  rel="boundto";anchor="/a/light";bind="obs";pmin="10";pmax="60"
Res: 2.04 Changed 

Req: GET /bnd/
Res: 2.05 Content (application/link-format)
<coap://sensor.example.com/s/light>;
  rel="boundto";anchor="/a/light";bind="obs";pmin="10";pmax="60"

Req: DELETE /bnd/a/light
Res: 2.04 Changed  
  
Req: DELETE /bnd/
Res: 2.04 Changed
~~~~
{: #figbindexp title="Binding Interface Example"}

Resource Observation Attributes      {#observation}
-------------------------------
When resource interfaces following this specification are made available over CoAP, the CoAP Observation mechanism {{RFC7641}} MAY be used to observe any changes in a resource, and receive asynchronous notifications as a result. In addition, a set of query string parameters are defined here to allow a client to control how often a client is interested in receiving notifications and how much a resource value should change for the new representation to be interesting. These query parameters are described in the following table. A resource using an interface description defined in this specification and marked as Observable in its link description SHOULD support these observation parameters. The Change Step parameter can only be supported on resources with an atomic numeric value.

These query parameters MUST be treated as resources that are read using GET and updated using PUT, and MUST NOT be included in the Observe request. Multiple parameters MAY be updated at the same time by including the values in the query string of a PUT. Before being updated, these parameters have no default value.

| Resource       | Parameter        | Data Format      |
| Minimum Period | /{resource}?pmin | xsd:integer (>0) |
| Maximum Period | /{resource}?pmax | xsd:integer (>0) |
| Change Step    | /{resource}?st   | xsd:decimal (>0) |
| Less Than      | /{resource}?lt  | xsd:decimal      |
| Greater Than   | /{resource}?gt  | xsd:decimal      |
{: #resobsattr title="Resource Observation Attribute Summary"}

 inimum Period: 
: As per {{pmin}}

 aximum Period: 
: As per {{pmax}}

Change Step: 
: As per {{st}}

Greater Than: 
: As per {{gt}}

Less Than: 
: As per {{lt}}
 
Security Considerations   {#Security}
=======================
An implementation of a client needs to be prepared to deal with responses to a request that differ from what is specified in this specification. A server implementing what the client thinks is a resource with one of these interface descriptions could return malformed representations and response codes either by accident or maliciously. A server sending maliciously malformed responses could attempt to take advantage of a poorly implemented client for example to crash the node or perform denial of service. 


IANA Considerations
===================

Interface Description
---------------------
The specification registers the "binding" CoRE interface description link target attribute value as per {{RFC6690}}.

Attribute Value:
: core.binding

Description: The binding interface is used to manipulate a binding table which describes the link bindings between source and destination resources for the purposes of synchronizing their content.

Reference: This specification. Note to RFC editor: please insert the RFC of this specification.

Notes: None

Link Relation Type
-------------------
This specification registers the new "boundto" link relation type as per {{RFC5988}}.

Relation Name: 
: boundto

Description: 
: The purpose of a boundto relation type is to indicate that there is a binding between a source resource and a destination resource for the purposes of synchronizing their content.

Reference: 
: This specification. Note to RFC editor: please insert the RFC of this specification.

Notes: 
: None

Application Data: 
: None

Acknowledgements
================
Acknowledgement is given to colleagues from the SENSEI project who were critical in the initial development of the well-known REST interface concept, to members of the IPSO Alliance where further requirements for interface types have been discussed, and to Szymon Sasin, Cedric Chauvenet, Daniel Gavelle and Carsten Bormann who have provided useful discussion and input to the concepts in this specification.

Changelog
=========

draft-ietf-core-dynlink-03

* General: Reverted to using "gt" and "lt" from "gth" and "lth" for this draft owing to concerns raised that the attributes are already used in LwM2M with the original names "gt" and "lt".

* New author and editor added. 

draft-ietf-core-dynlink-02

* General: Changed the name of the greater than attribute "gt" to "gth" and the name of the less than attribute "lt" to "lth" due to conlict with the core resource directory draft lifetime "lt" attribute.

* Clause 6.1: Addressed the editor's note by changing the link target attribute to "core.binding".

* Added Appendix A for examples.

draft-ietf-core-dynlink-01

* General: The term state synchronization has been introduced to describe the process of synchronization between destination and source resources.

* General: The document has been restructured the make the information flow better.

* Clause 3.1: The descriptions of the binding attributes have been updated to clarify their usage.

* Clause 3.1: A new clause has been added to discuss the interactions between the resources.

* Clause 3.4: Has been simplified to refer to the descriptions in 3.1. As the text was largely duplicated.

* Clause 4.1: Added a clarification that individual resources may be removed from the binding table.

* Clause 6: Formailised the IANA considerations.

draft-ietf-core-dynlink Initial Version 00:

* This is a copy of draft-groves-core-dynlink-00

draft-groves-core-dynlink Draft Initial Version 00:

* This initial version is based on the text regarding the dynamic linking functionality in I.D.ietf-core-interfaces-05.

* The WADL description has been dropped in favour of a thorough textual description of the REST API.

--- back

Examples
========

This appendix provides some examples of the use of binding attribute / observe attributes.

Note: For brevity the only the method or response code is shown in the header field.

Greater Than (gt) example
--------------------------

~~~~
     Observed   CLIENT  SERVER     Actual
 t   State         |      |         State
     ____________  |      |  ____________
 1                 |      |
 2    unknown      |      |     18.5 Cel
 3                 +----->|                  Header: GET 
 4                 | GET  |                   Token: 0x4a
 5                 |      |                Uri-Path: temperature
 6                 |      |               Uri-Query: gt="25"
 7                 |      |                 Observe: 0 (register)
 8                 |      |
 9   ____________  |<-----+                  Header: 2.05 
10                 | 2.05 |                   Token: 0x4a
11    18.5 Cel     |      |                 Observe: 9
12                 |      |                 Payload: "18.5 Cel"
13                 |      |                 
14                 |      |
15                 |      |  ____________
16   ____________  |<-----+                  Header: 2.05 
17                 | 2.05 |     26 Cel        Token: 0x4a
18    26 Cel       |      |                 Observe: 16
29                 |      |                 Payload: "26 Cel"
20                 |      |                 
21                 |      |
~~~~
{: #figbindexp1 title="Client Registers and Receives one Notification of the Current State and One of a New State when it passes through the greather than threshold of 25."}

Greater Than (gt) and Period Max (pmax) example
----------------------------------

~~~~
     Observed   CLIENT  SERVER     Actual
 t   State         |      |         State
     ____________  |      |  ____________
 1                 |      |
 2    unknown      |      |     18.5 Cel
 3                 +----->|                  Header: GET 
 4                 | GET  |                   Token: 0x4a
 5                 |      |                Uri-Path: temperature
 6                 |      |         Uri-Query: pmax="20";gt="25"
 7                 |      |                 Observe: 0 (register)
 8                 |      |
 9   ____________  |<-----+                  Header: 2.05 
10                 | 2.05 |                   Token: 0x4a
11    18.5 Cel     |      |                 Observe: 9
12                 |      |                 Payload: "18.5 Cel"
13                 |      |                 
14                 |      |
15                 |      |
16                 |      |
17                 |      |
18                 |      |
19                 |      |
20                 |      |
21                 |      |
22                 |      |
23                 |      |
24                 |      |
25                 |      |
26                 |      |
27                 |      |
28                 |      |
29                 |      |  ____________
30   ____________  |<-----+                  Header: 2.05
31                 | 2.05 |     23 Cel        Token: 0x4a
32    23 Cel       |      |                 Observe: 30
33                 |      |                 Payload: "23 Cel"
34                 |      |                 
35                 |      |
36                 |      |  ____________
37   ____________  |<-----+                  Header: 2.05 
38                 | 2.05 |     26 Cel        Token: 0x4a
39    26 Cel       |      |                 Observe: 37
40                 |      |                 Payload: "26 Cel"
41                 |      |                 
42                 |      |
~~~~
{: #figbindexp2 title="Client Registers and Receives one Notification of the Current State, one when pmax time expires and one of a new State when it passes through the greather than threshold of 25."}

