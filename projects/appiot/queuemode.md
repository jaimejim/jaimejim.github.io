## LWM2M - Queue Mode

### Synopsis
Queue Mode offers functionality for a LwM2M Client (LC) to inform the LwM2M Server (LS) that it may be disconnected for an extended period of time and when it becomes reachable again. Queue Mode is useful when the LwM2M Device is not reachable by the LwM2M Server at all the times and it could help the LwM2M Client sleep longer. All servers should support it.

### Basic Operation

LWM2M has various binding modes depending on transport (U=UDP, S=SMS) and whether Queuing (Q) is enabled or not (U, UQ, SQ, USQ).

- U:  Implies that LC should be reachable at any time, as there is no queuing.
- UQ: Signals LS to queue.
- S & SQ: SMS mode, not implemented AFAIK.

During the registration, LC registers with the appropriate binding (U or UQ) during the registration procedure.

The LS needs to figure out whether the message arrived to the LC or not. In order to do that it needs to receive some form of response, either ACK or a separate response.

Relevant LWM2M Resources:

- `1/0/1 - RW - s`: Lifetime of the registration (spec says 86400 default).
- `1/0/7`: binding used by LS.

Relevant CoAP ([Section 4.8](https://tools.ietf.org/html/rfc7252#section-4.8))  transmission parameters:

- `ACK_TIMEOUT`: It is the time needed before retransmission. The endpoint doing the GET operation will retransmit the message. By default its value is 2 seconds.
- `MAX_TRANSMIT_WAIT` is the maximum time from the first transmission of a Confirmable message to the time when the sender gives up on receiving an acknowledgement or reset. By default 93 seconds.

<img src="http://jaimejim.github.io/projects/appiot/pics/acktimeout.svg">

A typical Queue Mode sequence follows the following steps:

1.	The LwM2M Client registers to the LwM2M Server and requests the LwM2M Server to run in Queue mode by using the correct Binding value in the registration.

2.	The LwM2M Client is recommended to use the CoAP `MAX_TRANSMIT_WAIT` parameter to set a timer for how long it shall stay awake since last sent message to the LwM2M Server. After `MAX_TRANSMIT_WAIT` seconds without any messages from the LwM2M Server, the LwM2M Client enters a sleep mode.

3.	At some point in time the LwM2M Client wakes up again (update trigger via SMS, changed observation trigger or about to expire registration) and transmits a registration update message. Note: During the time the LwM2M Client has been sleeping the IP address assigned to it may have been released and / or existing NAT bindings may have been released. If this is the case, then the client needs to re-run the DTLS handshake with the LwM2M Server since an IP address and/or port number change will destroy the existing security context. For performance and efficiency reasons it is RECOMMENDED to utilize the DTLS session resumption.

4.	When the LwM2M Server receives a message from the Client, it determines whether any messages need to be sent to the LwM2M Client, as instructed by the application server.

<img src="http://jaimejim.github.io/projects/appiot/pics/queuemode.svg">

### Q&A

**Q: When are messages Confirmable?**

In LWM2M IMO all messages should be confirmable if over UDP. Only Applications (e.g. temperature measurements) that are not important can be non-CON.

**Q: Is Queue mode always used?**

Queue mode probably does not make sense if the device sends notifications every few seconds or if it always connected. It boils down to whether the system is push (LS to LC) or pull (LC to LS). If the system is based on LC notifications and LC is mostly asleep, then queuing makes sense.

**Q: Implications of using U or UQ?**

A priori there is no difference, we should queue always.

**Q:  How does LS know when the device is going to be unreachable?**

As to the spec... it doesn't. Only when LC has previously registered with UQ and only for `MAX_TRANSMIT_WAIT` is Queued Mode triggered on the LC. LS should have another timeout (if LS doesn't get a response after X seconds, assume sleep).
Alternatively, we could set a resource with the sleeping schedule, an observe it. It could also just be preconfigured.

**Q: How does the LC inform the LS that it's going to sleep?**

There does not seem to be an explicit way to inform of going to sleep. As before, you could set a specific resource to inform of the sleep schedule.

**Q: How does the LC inform the LS of when it'll be reachable?**

LS only knows that LC is reachable when LC connects to it. It depends a lot on the system, if it is scheduled or not.

**Q: How does the LS know a message reached the LC?**

CON response (spec says non-Con for some reason) or ACK at transport. That confirms the message has been received (not parsed) by the transport layer. For explicit confirmation at application layer you might need to implement the client so that the CON is sent to the application and the application appends some extra ACK.

**Q: How do you distinguish between sleepy device and offline?**

Lifetime expires would mean offline vs `ACK_TIMEOUT` that would mean sleep.
online -- *`ACK_TIMEOUT` expires* -- offline -- *lifetime expires*.

**Q: Confirm which of the timeouts is the right one**

MAX_TRANSMIT_WAIT or ACK_TIMEOUT


### Firewalls and NATs

For a firewall to support LwM2M, it should be configured to allow outgoing UDP packets to destination port 5683 (other ports can be configured), and allow incoming UDP packets back to the source address/port of the outgoing UDP packet for a period of at least 240 seconds.
In cases where firewalls do not allow that, there has been work to support Websockets (AFAIK not implemented). When a firewall is configured as such any LwM2M Clients behind it should use Queue Mode.

Any LwM2M Clients behind a NAT can use Queued Mode to punch holes in it to allow the LS to connect, the NAT should take care of the different IP addresses but IPv6 is recommended to prevent NAT issues.

### Application use cases

In general, queuing is agnostic of the application, it just caches and forwards messages. An enhancement could be a filter that aggregates commands and filters those that are redundant or irrelevant with the goals of saving battery and bandwidth as well as simplifying operations.

**Multiple operations over the same Object/Resource**

User wants to read a measurement, execute a command, delete a resource, etc. it might click multiple times on UX. The filter should keep the latest command.

**Firmware Upgrades**


User sets firmware upgrade feature, changes URL. As it is an operation over a resource, it does not change anything. Scalability might be an issue, need to check.
3 Resources, one of them is the URL where the firmware package is fetch from. Two state-machine variables.

Q: URI means CoAP URI (or HTTP?).
A: HTTP for now.

**LS changes**

Device goes to sleep and wakes up connecting to a different LS. Q should be unaffected. Not clear why it'd connect to a different LS.

**Multiple GETs**

Admin on UX keeps performing a GET operation over a resource. Admin could be prompted to simply "observe" the resource and avoid queuing altogether.

**Resources no longer exist**

GET/PUT after a DELETE. If one operation on the queue deletes an Object, the associated resources are also deleted and operations on those are not possible.

### Scenarios

**Device is Registered but offline - Spec based**

<img src="http://jaimejim.github.io/projects/appiot/pics/scenario1.svg">


**Device is Unregistered - Spec based**

<img src="http://jaimejim.github.io/projects/appiot/pics/scenario2.svg">


**Device is Registered - LC status based**

<img src="http://jaimejim.github.io/projects/appiot/pics/scenario3.svg">
