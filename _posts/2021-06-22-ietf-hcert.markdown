---
title: "Electronic Health Certificates and IETF"
layout: post
date: 2021-06-22 11:20
headerImage: true
image: /assets/images/covid.png
tag:
- IETF
- HCERT
category: blog
author: jaime
headerImage: true
---

I have written nothing about COVID and the two anni horribiles we are having. So let this be the first and last post about the topic.

I got today a EU CoVID certificate from the [Finnish Health Service](https://thl.fi/en/web/thlfi-en/-/first-covid-19-vaccination-certificates-now-available-in-my-kanta-pages) (kanta.fi).  The certificate pdf contains plaintext identification information, details of the COVID-19 vaccination and metadata to identify a valid certificate. It comes with a unique URN identifier and a QR code (or Aztec Code) that encodes the same information and can be verified by a validator application.

![An EU health Certificate](/assets/images/hcert.jpg)

I could not resist trying to look into the QR code with a well-known qr code reader called `zbar`.

```sh
~ zbarimg --raw qr.png                                                              (678ms)  
HC1:NCFOXN%TSMAHN-HMR blablablablablaba :VC/4
scanned 1 barcode symbols from 1 images in 0.02 seconds
```

I was curious, as this was not just your average URL encoded into a QR, it had some sort of header, the `HC1:NCFOXN%`, which I promptly googled for. It turned out that you can find the [EU Digital Green Certificates (DGC)](https://github.com/eu-digital-green-certificates/dgc-overview) project as well as the full [certificate specification](https://github.com/ehn-dcc-development/hcert-spec/blob/main/README.md)!. There are even  available [implementations](https://github.com/ehn-dcc-development/hcert-testdata) for Electronic Health Certificates (HCERT) - which I have not tested-. It also comes with a neat [rationale](https://github.com/ehn-dcc-development/hcert-testdata/blob/main/hcert-preso.pdf) for the technology choices they made.

You can find lots of [examples](https://github.com/ehn-dcc-development/ehn-dcc-schema/blob/release/1.3.0/test/valid/T-rat-dates3.json) on the EHN github repository. For example, here you have a [valid HCERT example](https://raw.githubusercontent.com/eu-digital-green-certificates/dgc-testdata/main/FI/2DCode/raw/1.json) of someone with one vaccination. It includes the full chain from the JSON, CBOR, the COSE signed as well as the BASE45 with the HC1 prefix.

There is also a document by the World Health Organization on the [trust model](https://www.who.int/publications/m/item/interim-guidance-for-developing-a-smart-vaccination-certificate) for these certificates. As I come from the IoT angle, many of the steps are reminiscent of an IoT device onboarding process, but that's another story.

They show the general process and structure of the HCERT creation, signing and validation:

1. Encode vaccination information on a JSON structure using CBOR.
2. Sign it with COSE and the private key of one of the Country Signing Certificate Authorities (CSCA) Signer Certificates. There are no CAs or other intermediate parties, valid keys are published online. This is the same principle used in over 490 million ePassports in circulation.
3. The resulting document is compressed some more with zlib. Although this is useful specially in cases with many vaccinations.
4. They transform it to base45 for certain [reasons](https://github.com/ehn-dcc-development/hcert-spec/blob/main/README.md#base45) and generate a QR with that.

![Health Certificate overview](/assets/images/hcert-overview.jpg)

So now I know that the information from the QR code is a base45 data structure with a 3-byte header `HC1` for Health Certificate Version 1. It would be expected that after decompressing with zlib , we would obtain CBOR/COSE binary data.

I tinkered around, trying few base45 decoders, removing the header and getting up to the zlib decompression phase. It is at this point that I found the excellent post by [Tobias Girstmair](https://gir.st/blog/greenpass.html) who has worked much more with this already. So I simply run his [script](https://git.gir.st/greenpass.git/blob_plain/master:/greenpass.py) that reads the QR, extracts the data, transforms the base45, removes the COSE signature and reads the CBOR, presenting the actual data. Which is as follows:

```json+
root@93955752b07d:src/docker-ubuntu# python3 greenpass.py qr.png 
QR Code Issuer : FI
QR Code Expiry : 2022-06-22 20:59:59
QR Code Generated : 2021-06-22 06:48:13
 Vaccination Group
   Unique Certificate Identifier: UVCI : URN:UVCI:01:FI:********************
   Country of Vaccination : FI
   Dose Number : 1
   ISO8601 complete date: Date of Vaccination : 2021-06-11
   Certificate Issuer : The Social Insurance Institution of Finland
   Marketing Authorization Holder : ORG-100030215
   vaccine medicinal product : EU/1/20/1528
   Total Series of Doses : 2
   disease or agent targeted : 840539006
   vaccine or prophylaxis : J07BX03
 Date of birth : 1983-04-28
 Surname(s), forename(s)
   Surname : Jimenez Bolonio
   Forename : Jaime Antonio
   Standardised surname : JIMENEZ<BOLONIO
   Standardised forename : JAIME<ANTONIO
 Schema version : 1.0.0
```

The output is self-explanatory for the most part, and matches the plaintext information. When it comes to the disease and the vaccine numbers, they are part of a classification system. So [840539006](https://ec.europa.eu/health/sites/default/files/ehealth/docs/digital-green-value-sets_en.pdf) stands for COVID-19 disease and J07BX03 which is used for all Covid19 vaccines (Moderna, Pfizer, Astrazeneca...). The specific vaccine is defined by the [EU/1/20/1528](https://ec.europa.eu/health/documents/community-register/html/h1528.htm) field which is BioNTech Pfizer in my case.

During the tinkering I was pleasantly surprised to see use a lot of IETF-made technologies like [CBOR](https://datatracker.ietf.org/doc/html/rfc7049),  [COSE](https://www.rfc-editor.org/rfc/rfc8152.html), [CWT](https://datatracker.ietf.org/doc/html/rfc8392), [Base45](https://datatracker.ietf.org/doc/html/draft-faltstrom-base45), etc. Many of these -as far as I know- were initially intended for Internet of Things (IoT) as they focus on being lightweight and require little processing. Why did they chose IETF technologies? Well part of their [guiding principles](https://github.com/ehn-dcc-development/hcert-spec/blob/main/README.md#requirements-and-design-principles) are right on the IETF ballpark:

> 2 . Use an encoding which is as compact as practically possible whilst ensuring reliable decoding using optical means.

> 3 . Use existing, proven and modern open standards, with running code available (when possible) for all common platforms and operating environments to limit implementation efforts and minimize risk of interoperability issues.

The creators seem also looking at the edge of the standardization as they are using an IETF draft format for the [base45](https://datatracker.ietf.org/doc/draft-faltstrom-base45/) encoding and not an existing RFC. The news were also shared on [a IETF mailing list](https://mailarchive.ietf.org/arch/msg/cbor/M07MvOOyQlw-0P9i2GYYFd8hSbM/) by the creator of CBOR.

It gives a very odd feeling to be a tiny part of the story of the creation of these technologies and to watch how they come from an idea to a reality.

**Update 03.08.2021**

Incidentally, the finnish authorities are now issuing PCR test certificates using the same underlying technology as the one used in the COVID certificates, thus making them unforgeable. The personal information is the same but there is now data about the type of test done and its results.

For example, using the [EU Green Certificates](https://ec.europa.eu/health/sites/default/files/ehealth/docs/digital-green-certificates_dt-specifications_en.pdf) specification we can determine that I got a Nucleid acid amplification test or [LP6464-4](https://loinc.org/LP6464-4/) and that the Covid variant was "not present" (260415000).

```json+
QR Code Issuer : FI
QR Code Expiry : 2022-08-03 20:59:59
QR Code Generated : 2021-08-03 16:24:36
 Test Group
   Unique Certificate Identifier, UVCI : URN:UVCI:01:FI:********************
   Country of Test : FI
   Certificate Issuer : The Social Insurance Institution of Finland
   Date/Time of Sample Collection : 2021-07-30T16:01:00+03:00
   Testing Centre : Espoon kaupunki, sosiaali- ja terveystoimi
   tg : 840539006
   Test Result : 260415000
   Type of Test : LP6464-4
 Date of birth : 1983-04-28
 Surname(s), forename(s)
   Surname : Jimenez Bolonio
   Forename : Jaime Antonio
   Standardised surname : JIMENEZ<BOLONIO
   Standardised forename : JAIME<ANTONIO
 Schema version : 1.3.0

```


