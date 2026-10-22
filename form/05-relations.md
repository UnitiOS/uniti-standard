# Relations

Status: locked (v0.1.0)

> [Uniti Standard](../README.md) › Part A: form, 5 of 8
> · Previous: [Concepts and properties](04-concepts.md)
> · Next: [Calculation rules](06-calculation-rules.md)
> · [Rules RELATION-n](../rules.md#relations)

## 1. Purpose

Content is made by many authors, and every piece of content depends on other
content: child concepts on their parents, properties on the concepts they
refer to, modules on the vocabulary, the vocabulary on outside standards. The
relations form sets out the ways content may point to other content, who may
state them, and what follows from them, so that content can depend on other
content without changing it.

## 2. Definitions

### 2.1 Relations between content, not between entities

The relations in this document connect **content**: concepts, properties,
choice lists, and choices. A relation between **entities**, for example "the
customer of rental R1 is Sam", is not a relation in the sense of this
document; it is a fact with a reference property
([`03-values.md`](03-values.md) §2.7).

### 2.2 The relation list

The relation list is part of the form, and it is closed. The relations fall
into two groups.

**Structural relations** determine how content is used to record facts:

| Relation | Address | From → to | Example |
|---|---|---|---|
| **subtype of** | `standard/subtype_of` | concept → concept | Rental is a subtype of Transaction |
| **applies to** | `standard/applies_to` | property → concept | `plate_number` applies to Item |
| **refers to** | `standard/refers_to` | property → concept | `customer` refers to Party |
| **uses list** | `standard/uses_list` | property → choice list | `method` uses list PaymentMethod |
| **in list** | `standard/in_list` | choice → choice list | `qr_payment` is in list PaymentMethod |

Structural relations are the card parts described in
[`04-concepts.md`](04-concepts.md) and [`03-values.md`](03-values.md), written
here as one list.

**Meaning relations** explain the meaning of a piece of content by pointing to
other content, without changing how facts are recorded:

| Relation | Address | Meaning |
|---|---|---|
| **replaced by** | `standard/replaced_by` | This deprecated content is replaced by the content pointed to ([`07-change.md`](07-change.md) §2.3) |
| **same as** | `standard/same_as` | The meaning is the same, and they may be used interchangeably |
| **broader** | `standard/broader` | The meaning of the content pointed to is broader |
| **narrower** | `standard/narrower` | The meaning of the content pointed to is narrower |
| **similar** | `standard/similar` | The meaning is close, but not the same enough to be used interchangeably |

The last four relations are called **bridges**.

### 2.3 Who may state them

| Relation | Who may state it |
|---|---|
| subtype of, refers to, uses list | Only the owner of the source content, that is the child concept or that property |
| applies to | Anyone, in their own module; required only if stated by the owner of the concept ([`04-concepts.md`](04-concepts.md) §2.3) |
| in list | The owner of that choice; into a list owned by someone else only if the list is open ([`03-values.md`](03-values.md) §2.6) |
| replaced by | Only the owner of the deprecated content |
| bridges | Anyone, in their own module, to any address |

The content that is **pointed to** may belong to anyone. No relation needs the
permission of the owner of the content pointed to, and no relation changes the
content pointed to.

### 2.4 A relation applies through installed modules

Every relation is written in a module, and only applies to an organization
that **installs** that module. Two organizations that install different
modules may see different properties, choices, or bridges for the same
vocabulary concept, without interfering with each other.

### 2.5 Bridges

Bridges connect Uniti content with an **outside standard** or with **other
content in Uniti**:

- `uniti/party/Party` is **similar** to `schema:Organization`;
- `uniti/common/name` is **the same as** `schema:name`;
- `maria/cashier/qr_payment` is **the same as** `lena/shop/qr_payment`.

Bridges connect content of the same kind: concept with concept, property with
property, choice with choice.

A bridge is a **remark**. A bridge:

- does not change the meaning of the content pointed to, and does not apply in
  the opposite direction unless it is also stated from the opposite direction;
- does not create facts. Combining facts recorded with two bridged pieces of
  content, for example for a joint report, is a calculation rule
  ([`06-calculation-rules.md`](06-calculation-rules.md));
- stays recorded under the name of its author, so that readers can judge how
  far they trust it.

If an outside standard changes or disappears, Uniti content still means the
same ([`00-principles.md`](../00-principles.md) §5).

### 2.6 What is not provided yet

Two relations known in other standards are **deliberately not** provided yet:

| Relation | Example | Why not yet |
|---|---|---|
| **inverse of** | "rents" is the inverse of "customer" | The question from the opposite direction can already be answered by reading references |
| **part of** | a wheel is part of a car | Between entities it can already be recorded with a reference property; between concepts it has not been shown to be needed |

Both may be added in a later version of the standard without breaking existing
content ([`00-principles.md`](../00-principles.md), P3 and P4).

## 3. Rules

**The relation list**

- **RELATION-1.** Every relation between content MUST be one of the relations
  in §2.2.
- **RELATION-2.** Content MUST NOT add to the relation list.

**Who may state them**

- **RELATION-3.** A relation MUST be stated by the party named in §2.3, in
  their own module.
- **RELATION-4.** A relation MUST NOT change the content it points to.
- **RELATION-5.** A relation MUST apply only to an organization that installs
  the module in which the relation is written.

**Structural**

- **RELATION-6.** The source side and the target side of a structural relation
  MUST match the "from → to" column in §2.2.
- **RELATION-7.** A structural relation MUST point to the exact version of the
  module that owns its target content ([`07-change.md`](07-change.md),
  CHANGE-14).

**Bridges**

- **RELATION-8.** A bridge MUST point to a permanent address. To an outside
  standard, that address MUST be an IRI.
- **RELATION-9.** A bridge MUST NOT be used to create, change, or reject
  facts.
- **RELATION-10.** A bridge SHOULD come with a note about the difference in
  meaning if its kind is similar, broader, or narrower.
- **RELATION-11.** Content in the vocabulary SHOULD have a bridge to an outside
  standard if a counterpart exists ([`00-principles.md`](../00-principles.md),
  P8).
- **RELATION-12.** A bridge MUST connect content of the same kind: concept with
  concept, property with property, or choice with choice.

## 4. Examples

**Equipment rental.**

| Statement | Relation | Written in module |
|---|---|---|
| `alex/rental/Rental` subtype of `uniti/transaction/Transaction` | structural | `alex/rental` |
| `alex/rental/customer` refers to `uniti/party/Party` | structural | `alex/rental` |
| `alex/rental/plate_number` applies to `uniti/item/Item` | structural | `alex/rental` |
| `alex/rental/Rental` narrower `schema:RentAction` | bridge | `alex/rental` |

The vocabulary does not change at all, and everything stays Alex's.

**Clinic and cashier.** The vocabulary has the open list
`uniti/payment/PaymentMethod`. Healthy Clinic adds
`healthy-clinic/cashier/national_insurance` to that list. A pharmacy adds
`city-pharmacy/cashier/national_insurance`. Healthy Clinic then declares
`healthy-clinic/cashier/national_insurance` **the same as**
`city-pharmacy/cashier/national_insurance`, so that the combined report of the
two can be computed together through a calculation rule.

**School.** `uniti/education/Class` is **similar** to `schema:Course`, with
the note: "in schema.org, a Course is a subject; here a Class is a group of
students".

## 5. Non-examples

- **"Sam is the customer of rental R1"** as a relation. That is a fact.
- **A bridge that makes a system copy facts automatically** from one module to
  another module.
- **Alex declaring `uniti/transaction/Transaction` a subtype of something.**
  Only the owner of Transaction may state its parent.
- **A self-made relation "owned by"** between concepts. The relation list is
  closed; such a need is recorded as a reference property.

## 6. Rationale

- **A closed list, two groups.** Structural relations determine how facts are
  recorded and checked, so they must be few and certain. Meaning relations
  only explain, so they are safe for anyone to write.
  ([`decisions/0023`](../decisions/0023-relation-list.md))
- **Bridges by anyone, without changing what they point to.** Content can keep
  being connected with the outside world and with other content without
  waiting for anyone, and without anyone being able to change the meaning of
  content owned by someone else.
  ([`decisions/0024`](../decisions/0024-bridges.md))

## 7. Outside standards

| Part | Counterpart |
|---|---|
| subtype of | `rdfs:subClassOf` (W3C) |
| applies to | `rdfs:domain`; `schema:domainIncludes` |
| refers to | `rdfs:range`; `schema:rangeIncludes` |
| in list | `skos:inScheme` (W3C) |
| replaced by | `dcterms:isReplacedBy`; `owl:deprecated` |
| Bridges | `skos:exactMatch`, `skos:broadMatch`, `skos:narrowMatch`, `skos:closeMatch` (W3C) |
| Relations not provided yet | `owl:inverseOf`; part-whole relations in ontologies |

## 8. Open questions

1. **Bridges that contradict each other.** Answered: a bridge is only a
   remark (RELATION-9) and does not change any result, so a reader may show
   both bridges as they are ([`decisions/0057`](../decisions/0057-closure-before-lock.md)).
2. **Bridges between properties with different units.** May "same as" be used
   between two number properties that have the same quantity but are usually
   filled in with different units?
