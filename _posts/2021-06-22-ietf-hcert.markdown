---
title: "Electronic Health Certificates and IETF"
layout: post
date: 2021-06-22 11:20
image: /assets/images/covid.jpg
tag:
- IETF
- HCERT
blog: true
star: true
---
I have written nothing about COVID and the two annus horribilis we are having. So let this be the first and last post about the topic.

I got today a EU CoVID certificate from the [Finnish Health Service](https://thl.fi/en/web/thlfi-en/-/first-covid-19-vaccination-certificates-now-available-in-my-kanta-pages) (kanta.fi).  The certificate contains some identification information, details of the COVID-19 Vaccination and metadata to identify a valid certificate. It comes with a unique URN identifier and a QR code (or Aztec Code) that encodes the same information and can be verified by a validator application.

![An EU health Certificate](/assets/images/hcert.jpg)

I could not resist trying to look into the QR code with a well-known tool called `zbar`. 

```sh
Desktop ~ zbarimg --raw qr.png                                                              (678ms)  
HC1:NCFOXN%TSMAHN-HMR blablablablablaba :VC/4
scanned 1 barcode symbols from 1 images in 0.02 seconds
```

The QR code encodes a 3-byte header `HC1` for HC1 (Health Certificate Version 1) the rest is compressed Base45 data. After decompressing with zlib, we obtain CBOR/COSE binary data.

Before I started with that I googled online for the header `HC1:NCFOXN%` and it turned out that you can find the full [EU certificate specification](https://github.com/ehn-dcc-development/hcert-spec/blob/main/README.md) (!!).

Others like [Tobias Girstmair](https://gir.st/blog/greenpass.html) have tinkered much more already on it and you can find lots of [examples](https://github.com/ehn-dcc-development/ehn-dcc-schema/blob/release/1.3.0/test/valid/T-rat-dates3.json) on the EHN github repository of what the QR encodes. My QR code encodes a JSON structure similar to this:

```json+
{-260: {1: {'dob': '1983-04-28', date of birth
            'nam': {'fn': 'Jimenez Bolonio', family name
                    'fnt': 'JIMENEZ<BOLONIO',
                    'gn': 'Jaime Antonio', given name
                    'gnt': 'JAIME'},
            'v': [{'ci': 'URN:UVCI:01:FI:EA6KGXLJ38XXXXXXXXXXX#Z', certificate ID
                   'co': 'FI', country of vaccination
                   'dn': 1, doses received
                   'dt': '2021-06-11', date of vaccination
                   'is': 'The Social Insurance Institution of Finland', cert issuer
                   'ma': 'ORG-100030215', vaccine manufacturer
                   'mp': 'EU/1/20/1528', vaccine product id
                   'sd': 2, total number of doses
                   'tg': '840539006', targeted disease (COVID-19)
                   'vp': '1119349007'}], vaccine or prophylaxis
            'ver': '1.2.1'}}, schema version
 1: 'FI', QR code issuer
 4: 1734452437, QR code expiry
 6: 1774452437} QR code generated
 ```

I was pleasantly surprised to see use a lot of IETF-made technologies like [CBOR](https://datatracker.ietf.org/doc/html/rfc7049),  [COSE](https://www.rfc-editor.org/rfc/rfc8152.html), [CWT](https://datatracker.ietf.org/doc/html/rfc8392) [Base45](https://datatracker.ietf.org/doc/html/draft-faltstrom-base45), etc. Most of these have been done in collaboration with Ericsson folks and were initially intended for Internet of Things (IoT) as they focus on being lightweight and require little processing.

Why did they chose IETF technologies? Well part of their [guiding principles](https://github.com/ehn-dcc-development/hcert-spec/blob/main/README.md#requirements-and-design-principles) are right on the IETF ballpark:

> 2. Use an encoding which is as compact as practically possible whilst ensuring reliable decoding using optical means.
> 3. Use existing, proven and modern open standards, with running code available (when possible) for all common platforms and operating environments to limit implementation efforts and minimise risk of interoperability issues.

The JSON structure I mentioned above is encoded and signed using CBOR and COSE. When they scan the QR at the airport, the application will check the data (i.e. name, surname, vaccine, CertID, etc) and it will only be valid if it was signed with the private key of the health organization issuing the certificate. There is a document by the World Health Organization on the [trust model](https://www.who.int/publications/m/item/interim-guidance-for-developing-a-smart-vaccination-certificate) for this certificates. As I come from the IoT angle, many of these steps are reminiscent of an IoT device onboarding process, but that's another story.

The creators seem also looking at the edge of the standardization as they are using an IETF draft format for the [base45](https://datatracker.ietf.org/doc/draft-faltstrom-base45/) encoding and not an existing RFC. The news were also shared on [a IETF mailing list](https://mailarchive.ietf.org/arch/msg/cbor/M07MvOOyQlw-0P9i2GYYFd8hSbM/) by the creator of CBOR.

It gives a very odd feeling to be a tiny part of the story of the creation of these technologies and to watch how they come from an idea to a reality.