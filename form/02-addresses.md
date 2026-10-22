# Addresses

Status: locked (v0.1.0)

> [Uniti Standard](../README.md) › Part A: form, 2 of 8
> · Previous: [Facts](01-facts.md) · Next: [Values](03-values.md)
> · [Rules ADDRESS-n](../rules.md#addresses)

## 1. Purpose

Content is made by many makers who do not know each other, and the facts
recorded with that content are kept for years. The form of addresses makes sure
that every module, concept, and property has a name that is unique in the whole
ecosystem, never clashes with a name made by someone else, and never changes
meaning, so that the facts that point to it can be read forever.

## 2. Definitions

### 2.1 What is given an address

An address is given to **content**:

| What is given an address | Example |
|---|---|
| **Owner** | `alex` |
| **Module** | `alex/rental` |
| **Concept** | `alex/rental/Rental` |
| **Property** | `alex/rental/rental_date` |
| **Choice list** | `lena/guarantee/GuaranteeMethod` |
| **Choice** in a choice list | `lena/guarantee/cash` |
| **Calculation rule**: helper, constraint, contribution | `alex/rental/no_overlap` |
| **Example** | `alex/rental/three_night_rental` |
| **Part of the form**, such as the basic property *type* | `standard/type` |

**Entities are not given addresses.** An entity has an identifier (see
[`01-facts.md`](01-facts.md) §2.2). An address names *content*, an identifier
names *what is recorded with that content*.

### 2.2 Structure of an address

```
‹root› / ‹owner› / ‹module› / ‹name›
```

| Part | Meaning |
|---|---|
| **‹root›** **[provisional]** | The beginning of the address that is the same for the whole ecosystem. For now `https://uniti.example` (§2.5) |
| **‹owner›** | The name of an owner registered in the ecosystem, for example `alex`, `happycamp`, `uniti` |
| **‹module›** | The name of a module that belongs to that owner, for example `rental` |
| **‹name›** | The name of a concept, property, choice list, or choice inside that module |

Full example: `‹root›/alex/rental/Rental`, which with the temporary root becomes
`https://uniti.example/alex/rental/Rental`.

Three owners are reserved by the standard: **`standard`** for the parts of the
form, **`uniti`** for the shared vocabulary, and **`example`** for content that
is made only as an example or exercise.

### 2.3 An address does not contain a version

The address of a concept or property is **the same in all versions of its
module**. Alex's concept `Rental` has the same address in versions 1, 2, and 3,
so a fact that is recorded with version 1 is still recognized in version 3. The
version that was used when a fact was stated is recorded in the fact itself
(*version used*).

When a version needs to be referred to, for example when one module uses
another module, the reference is a pair of **module address and version
number**. Written for humans as `alex/rental@v3`.

### 2.4 Letters that are used

| Part | Allowed letters | Example |
|---|---|---|
| ‹owner› and ‹module› | lowercase a–z, digits, hyphen in the middle | `happy-camp`, `rental` |
| ‹name› of a concept and of a choice list | starts with an uppercase letter, then letters and digits | `Rental`, `Appointment`, `PaymentMethod` |
| ‹name› of a property, choice, calculation rule, and example | lowercase letters, digits, underscore in the middle | `rental_date`, `cash`, `no_overlap` |
| ‹name› of a choice in a code list ([`03-values.md`](03-values.md) §2.6) | the code from its outside standard, exactly: basic Latin letters and digits | `IDR`, `kg`, `d` |

An address uses only basic Latin letters, so that it can be written, typed, and
read by any system in the world. A name in a human language, including non-Latin
letters, is written as a **label** (see [`04-concepts.md`](04-concepts.md)), and
a label may change at any time.

### 2.5 The temporary root

The domain for the root does not exist yet. Until it exists, the root is
**`https://uniti.example`**. The ending `.example` is set aside for examples
(RFC 2606) and cannot be owned by anyone, so this root cannot be mistaken for a
real address.

So that the root can be replaced without touching content and facts, an address
is stored and written **without the root**, for example `alex/rental/Rental`.
The root is put in front only when an address is written in full, for example
to be opened (ADDRESS-12). Replacing the root means replacing that one value
only.

The root may be replaced **one time**, before v0.1 becomes stable. After that
the root never changes again, like the other parts of an address.

## 3. Rules

**Structure**

- **ADDRESS-1.** Every module, concept, property, choice list, choice,
  calculation rule, and example MUST have an address with the structure
  `‹root›/‹owner›/‹module›/‹name›`, except the addresses of an owner and of a
  module, which stop at their own part.
- **ADDRESS-2.** The parts of an address MUST use letters according to §2.4.
- **ADDRESS-3.** Within one module, every ‹name› MUST be unique among all of its
  concepts, properties, choice lists, choices, calculation rules, and examples.
- **ADDRESS-4.** An address MUST NOT contain a version number.

**Uniqueness and ownership**

- **ADDRESS-5.** The name of an owner MUST be unique in the whole ecosystem. How
  to register and hold it is set in v0.2 ([`decisions/0048`](../decisions/0048-ownership-to-v02.md)).
- **ADDRESS-6.** Only the owner MAY create addresses under its name.
- **ADDRESS-7.** The owner names `standard`, `uniti`, and `example` are
  reserved, and MUST NOT be registered by other parties.

**Permanence**

- **ADDRESS-8.** An address that is already frozen in a version MUST NOT be
  deleted, and MUST NOT be reused for another meaning.
- **ADDRESS-9.** If the meaning of a concept or property changes fundamentally,
  a new address MUST be created. The old address MAY be marked deprecated by
  naming its replacement ([`07-change.md`](07-change.md)).
- **ADDRESS-10.** Changing how a concept or property is called by humans MUST be
  done through a label, not by changing its address.

**Version reference**

- **ADDRESS-11.** A reference to a version MUST be a module address and one exact
  version number. A range of versions ("version 2 and up") MUST NOT be used.

**Opening an address**

- **ADDRESS-12.** An address SHOULD be openable, by humans and by machines, to
  show the card of its content: definition, label, owner, and its versions.

**Root**

- **ADDRESS-13.** Addresses in facts, modules, and the vocabulary MUST be stored
  and written without the ‹root›.
- **ADDRESS-14.** An implementation MUST treat the ‹root› as one value for the
  whole ecosystem, and put it on only when an address is written in full.
- **ADDRESS-15.** **[provisional]** The ‹root› is `https://uniti.example`. The
  ‹root› MAY be replaced one time, before v0.1 becomes stable. After that the
  ‹root› MUST NOT change.

## 4. Examples

**Equipment rental.** Alex and the maker of the cashier RentPro both make a
concept named `Rental`. Their addresses do not clash:

- `‹root›/alex/rental/Rental`
- `‹root›/rentpro/cashier/Rental`

A shop that uses both still knows exactly which rental was recorded through
which module.

**Clinic.** The module `healthy-clinic/schedule` version 1 has the concept
`Visit`. In version 4, its label is changed from "Visit" to "Patient
appointment". Its address stays `‹root›/healthy-clinic/schedule/Visit`, and all
the visit records since version 1 can still be read.

**Shared vocabulary.** The concept party in the vocabulary:
`‹root›/uniti/party/Party`.

## 5. Not examples

- **`7f3a9c…` as an address.** That is the identifier of an entity, not an
  address of content.
- **`‹root›/alex/rental/v2/Rental`.** An address does not contain a version.
- **`‹root›/alex/rental/Equipment_Rental`** as a replacement of `Rental` only
  because a clearer name is wanted. That is a label, not a new address.
- **The label "Rental date".** A label is a name for humans, not an address.

## 6. Reasons

- **The owner inside the address** makes name clashes impossible, without
  coordination between makers.
- **An address without a version** lets data survive across versions. A meaning
  that changes fundamentally gets a new address, so one address never has two
  meanings. ([`decisions/0011`](../decisions/0011-addresses-and-identifiers.md))
- **The structure of the address is decided now, the root later.** The structure
  already supports the idea of one ecosystem with all of its content under one
  root, while the holder of the root and its license still need to be discussed
  separately.
  ([`decisions/0010`](../decisions/0010-address-structure.md))
- **Addresses are written without the root**, so that the temporary root can be
  replaced with the real domain without touching a single fact. ([`decisions/0055`](../decisions/0055-locked-in-english.md))

## 7. Outside standards

| Part | Equivalent |
|---|---|
| Permanent global address | IRI (RFC 3987); permanent address services such as w3id.org |
| Owner in front of the name | scoped package name, for example `@owner/name` in npm, or reversed domain name in Java |
| Version separate from address | *versionIRI* in OWL (W3C) |
| Label separate from address | `rdfs:label` and `skos:prefLabel` (W3C) |

## 8. Open questions

1. **‹root› [provisional], condition before v0.1 is stable.** Which domain
   replaces the temporary root (ADDRESS-15), who holds it, and under which
   license the content of the ecosystem is shared. This is part of the
   discussion about Uniti as an ecosystem and its intellectual property.
2. **Private content of an organization.** Does a private module use the same
   root, or may it use a root owned by that organization itself?
3. **Addresses of entities across organizations.** If facts are sent from one
   organization to another, how is the identifier of the entity written?
