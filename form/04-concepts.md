# Concepts and properties

Status: draft

## 1. Purpose

Concepts and properties are the words used to record facts. The concept form
makes sure every word has a clear meaning for both humans and machines, can be
used together by different authors without colliding, and can be extended by
anyone without asking permission and without copying.

## 2. Definitions

### 2.1 Concept and concept card

A **concept** is one class of entities, for example Transaction, Rental,
Patient, or Class. Every concept is described by a **concept card**:

| Card part | Meaning | Required? |
|---|---|---|
| **Address** | Its permanent name ([`02-addresses.md`](02-addresses.md)) | required |
| **Label** | Its name in a human language (§2.6) | required, at least one language |
| **Definition** | What this concept is, in one or two sentences | required |
| **Includes** | Examples of entities that belong to this concept | required, at least one |
| **Excludes** | Examples of similar entities that do not belong, with the reason | required, at least one |
| **Parent** | The more general concept (§2.4) | optional, at most one |
| **Its properties** | Properties that apply to this concept (§2.3) | optional |
| **Bridge** | Its counterpart in an outside standard or another module ([`05-relations.md`](05-relations.md)) | optional |
| **Note** | Additional remark | optional |

A concept in the **vocabulary** has a stricter requirement: "includes" and
"excludes" are each taken from at least two different domains.

### 2.2 Standalone properties

A **property** has its own address and does not belong to one concept. The
property `uniti/common/name` means the same wherever it is used, whether for
a person, an item, or a class. Every property is described by a **property
card**:

| Card part | Meaning | Required? |
|---|---|---|
| **Address** | Its permanent name | required |
| **Label** | Its name in a human language | required, at least one language |
| **Definition** | What this property states | required |
| **Value type** | One of the seven value types ([`03-values.md`](03-values.md) §2.1) | required |
| **Quantity** | For numbers: the kind of measure ([`03-values.md`](03-values.md) §2.3) | optional, only for numbers |
| **Direction** | For numbers: what a positive number means ([`03-values.md`](03-values.md) §2.3) | required for numbers |
| **Concept referred to** | For references: the class of entities that may be referred to | required for references |
| **Choice list** | For choices: the list that is used | required for choices |
| **Number of values** | **One** or **many** values that are valid at one time | required |
| **Valid time** | Whether facts with this property use a date or an instant ([`03-values.md`](03-values.md) §2.4) | optional |
| **Personal data** **[provisional]** | Whether the value concerns a person's private matters (§2.8) | required |
| **Bridge**, **note** | As on the concept card | optional |

Example of the number of values: a date of birth is only **one**, a phone
number can be **many**. For a property with one value, a new value must
replace or correct the old value ([`01-facts.md`](01-facts.md), FACT-14).

### 2.3 A property that applies to a concept

A property **applies to** a concept when there is a statement that connects
the two. The statement also says whether the property is **required** for that
concept. The same property may be required for one concept and not required
for another concept.

The statement "applies to" may be written by anyone, in their own module:

| Who writes | Example | May be required? |
|---|---|---|
| **Concept owner**, using their own property | `rudi/rental/rental_date` applies to `rudi/rental/Rental` | yes |
| **Concept owner**, using someone else's property | `uniti/common/note` applies to `klinik-sehat/records/MedicalRecord` | yes |
| **Another party**, adding a property to a concept that is not theirs | `rudi/rental/plate_number` applies to `uniti/item/Item` | **no** |

The third way is the key to modularity: Rudi adds what Rudi needs without
changing the vocabulary and without creating a new concept. The addition must
not be required, because other modules that record an Item know nothing about
`plate_number`. When Rudi needs a required property, Rudi makes a child concept
of Rudi's own, for example `rudi/rental/Car` with the parent Item.

A statement "applies to" only applies to an organization that installs the
module in which the statement is written.

### 2.4 Child concept

A concept may state **one parent**: "Rental is a subtype of Transaction". The
consequences:

- every property that applies to the parent, including the required ones, also
  applies to the child;
- an entity that belongs to the child also belongs to the parent. Rental R1 is
  a Transaction.

A child concept may add properties, and may make a property that is not
required at the parent required for itself. A property that is required at the
parent stays required at the child.

A concept without a parent stands at the top. The form does not provide one
top concept for all entities.

### 2.5 Type and role

A **type** is what an entity actually is: Person, Organization, Item, Rental.
A type does not change as long as the entity exists.

A **role** is the position of an entity in its relation to another entity:
customer, employee, renter, guardian. A role is **not a type**. A role is
recorded as a **reference from another entity**:

| Not like this | But like this |
|---|---|
| Budi has the type Customer | rental R1 → customer → Budi |
| Budi has the type Employee | contract K5 → employee → Budi |

This way one person stays one entity, whatever the roles, and every role has
its own start and end time. The question "who are Rudi's customers" is
answered by reading references, not by checking types.

An entity **may** have more than one type, if both are what the entity
actually is and neither is a child of the other. This is rare.

A type fact may only be **corrected** or **retracted** if its recording was
wrong. A type fact is not replaced and not ended, because an entity does not
change type. Something that really does change, for example a proposal that
becomes a contract, is recorded as a property (status), or as two entities
that refer to each other.

### 2.6 Label

A label is the name of a concept, property, choice list, or choice in a human
language. Every label carries a language code ([`03-values.md`](03-values.md)
§2.5).

- For each language, there is **one main label**.
- There may be **other labels**: everyday names, abbreviations, or local
  terms. Example: main label "Party", other labels "Partner" and "Associate".
- A label may change at any time without changing the address or the meaning
  ([`02-addresses.md`](02-addresses.md), ADDRESS-10).

### 2.7 Check per action

Facts are recorded one by one, but an action records several facts at once
([`01-facts.md`](01-facts.md), FACT-18). Because of this, constraints that
involve several facts are checked **per action**, after all facts in the
action are taken into account:

- every entity touched by the action must have a value for every property that
  is required for its type;
- every property that is used must apply to the type of its subject;
- every reference must point to an entity that belongs to the concept referred
  to.

The **time touched** by an action is the valid time of each of its facts, plus
the valid time of the target of each correction, retraction, and redaction.
These three change the state at the time of their target, for example a
correction that moves a date. A replacement and an ending only change the
state from their own valid time, so the time of their target is not included.
A required property is checked at every time touched.

The second and third checks above are only for facts that state a value
(statement, replacement, and correction), read at the valid time of that fact.
A retraction, an ending, and a redaction do not state a new value, so
retracting a whole wrong record in one action can still be done.

If any one of the conditions is not met, **the whole action is rejected**, and
not one fact of that action is recorded.

Example: the action "register patient" records the type Patient, the name, and
the date of birth at once. An action that records only the type Patient,
without the required name, is rejected.

### 2.8 Personal data **[provisional]**

> This marker goes with redaction ([`01-facts.md`](01-facts.md) §2.6), which is
> still waiting for a legal review of data protection. The form is written
> now, but it may still change.

Every property card states **yes** or **no**: whether the value concerns a
person's private matters. Examples of yes: name, phone number, home address,
date of birth, diagnosis. Examples of no: price, amount, rental date. Only
facts with a property marked yes may be redacted.

### 2.9 Changes that change the meaning

Concept cards and property cards may change from version to version
([`07-change.md`](07-change.md)), but some changes change the meaning and
therefore must use a new address:

| Changes the meaning: new address required | Does not change the meaning: may stay at the same address |
|---|---|
| Changing the value type, quantity, concept referred to, or choice list of a property | Changing or adding a label |
| Changing the number of values (one ↔ many), or the direction of a number | Making the definition clearer without changing it |
| Changing or adding the parent of a concept | Adding includes, excludes, bridges, notes |
| Changing the personal data marker from yes to no | Adding a property that applies to a concept |
| Closing an open choice list or open computed property | Making a property required or not required for a concept |
| | Opening a closed choice list or closed computed property; changing the personal data marker from no to yes |
| | Correcting the rule of a computed property. Its effect on numbers is reported as a behavior change ([`08-proof.md`](08-proof.md) §2.7) |

Making a property required does not change the meaning of the facts that
already exist, but it makes later actions stricter. A machine that computes
the kinds of change ([`07-change.md`](07-change.md) §2.2) MUST report it
separately, so that users know before they install that version.

## 3. Rules

**Cards**

- **CONCEPT-1.** Every concept MUST have a concept card with an address, a
  label, a definition, at least one include, and at least one exclude.
- **CONCEPT-2.** A concept in the vocabulary MUST give includes and excludes
  from at least two different domains.
- **CONCEPT-3.** Every property MUST have a property card with an address, a
  label, a definition, a value type, a number of values, and a personal data
  marker.
- **CONCEPT-4.** A reference property MUST name exactly one concept referred
  to. A choice property MUST name exactly one choice list.
- **CONCEPT-5.** A quantity MAY be stated only for number properties. A
  direction MUST be stated for every number property, and MUST NOT be stated
  for other properties.

**Applies to**

- **CONCEPT-6.** A fact that states a value MUST NOT use a property that does
  not apply to any type of its subject at the valid time of that fact, or to
  its parent, except the base property of type. An entity that has no type at
  that time has no applicable properties.
- **CONCEPT-7.** The statement that a property applies to a concept MAY be
  written by anyone in their own module, and only applies to an organization
  that installs that module.
- **CONCEPT-8.** A property MAY be declared required for a concept only by the
  owner of that concept.

**Child concepts**

- **CONCEPT-9.** A concept MAY have at most one parent.
- **CONCEPT-10.** The chain of parents MUST NOT loop back to its original
  concept.
- **CONCEPT-11.** Every property that applies to the parent MUST also apply to
  its child, and a property that is required at the parent MUST stay required
  at its child.
- **CONCEPT-12.** An entity that belongs to a concept MUST be considered to
  belong also to all its parents.

**Type and role**

- **CONCEPT-13.** A role SHOULD NOT be made a concept that becomes the type of
  an entity. A role SHOULD be recorded as a reference from another entity.
- **CONCEPT-14.** A type fact MUST NOT be replaced or ended. A type fact MAY be
  corrected or retracted.
- **CONCEPT-15.** An entity SHOULD have one type. If it has more than one, the
  types MUST NOT be children of each other.

**Label**

- **CONCEPT-16.** Every label MUST carry a language code.
- **CONCEPT-17.** For each language, a concept, property, choice list, or
  choice MUST have at most one main label.

**Check per action**

- **CONCEPT-18.** After all facts in an action are taken into account, every
  entity that is the subject of a fact in that action MUST have a valid
  value for every property that is required for its type, at every time that
  the action touches for that entity (§2.7).
- **CONCEPT-19.** An action that does not meet CONCEPT-6, CONCEPT-18, or
  VALUE-16 MUST be rejected as a whole.

**Personal data [provisional]**

- **CONCEPT-20.** Every property card MUST state whether its value is personal
  data.

**Change**

- **CONCEPT-21.** A change that changes the meaning according to §2.9 MUST NOT
  be made at the same address.
- **CONCEPT-22.** Making a property required MUST be reported separately by
  the machine that computes the kinds of change.

## 4. Examples

**Equipment rental.**

```
Concept  rudi/rental/Rental
Label    Sewa (id) · Rental (en)
Definition  Agreement to lend an item for a certain term, for a fee.
Parent   uniti/transaction/Transaction
Includes      rental of a tent for 3 days; rental of a car with a driver for a week
Excludes      sale of a tent (the item changes owner);
              free lending between friends (no fee)
Properties    rental_date (required) · customer (required) · uniti/common/note
```

```
Property rudi/rental/customer
Label    Pelanggan (id) · Customer (en)
Definition  The party that rents.
Value type      reference → uniti/party/Party
Number of values one
Personal data   no (the value is a reference; the personal data is in the properties of Party)
```

Rudi also adds `plate_number` to `uniti/item/Item`, not required. Other shops
that install the vocabulary but do not install Rudi's module do not see that
property.

**Clinic.** The concept `klinik-sehat/records/Patient` is not created. Ani is a
Person, and Ani's role as a patient is recorded through
`MedicalRecord R-201 → patient → Ani`. When Ani also works as a nurse at that
clinic, Ani is still one entity, which is referred to by
`Contract K-12 → employee → Ani`.

**School.** The vocabulary has the concept `uniti/education/Class`. A school
adds the property `homeroom_teacher` (a reference to Party) to Class in its own
module, not required. A school that wants the homeroom teacher to be required
makes a child `sekolah-bahari/academic/RegularClass` with the parent Class, and
then declares `homeroom_teacher` required for that child.

## 5. Non-examples

- **The properties `customer_name` and `item_name`** whose meaning is both
  "name". One property `name` that applies to both is enough.
- **The concept Customer as a type of Budi.** Customer is a role.
- **A concept with two parents**, for example Rental that is at the same time a
  child of Transaction and a child of Promise.
- **A concept card whose definition is "rental data"** without explaining what
  a rental is.
- **An additional property from another party that is required** for a
  vocabulary concept.
- **Changing the value type of `price` from text to number** at the same
  address.

## 6. Rationale

- **Standalone properties, which may be added to concepts owned by others.**
  Content from different authors can be combined without copying each other,
  and every addition keeps a clear owner.
  ([`decisions/0017`](../decisions/0017-standalone-properties.md))
- **Type and role are separated**, so that one person is not recorded as
  several entities, and so that roles that come and go do not change what the
  entity actually is. ([`decisions/0018`](../decisions/0018-types-and-roles.md))
- **One parent.** A structure shaped like a tree is easy to understand. If it
  later proves necessary, opening it to many parents does not break existing
  content, while the opposite direction does.
  ([`decisions/0019`](../decisions/0019-one-parent.md))
- **Required is checked per action**, because facts are recorded one by one
  but completeness only makes sense for a set of facts recorded together.
  ([`decisions/0020`](../decisions/0020-required-per-action.md))
- **Cards with includes and excludes.** The meaning of a concept is clearest
  at its boundaries.
  ([`decisions/0021`](../decisions/0021-concept-cards.md))
- **A personal data marker on every property**, so that redaction can only
  touch what is really personal.
  ([`decisions/0022`](../decisions/0022-personal-data-marker.md))

## 7. Outside standards

| Part | Counterpart |
|---|---|
| Concept | `rdfs:Class`, `owl:Class` (W3C) |
| Standalone property | `rdf:Property` (W3C); properties in schema.org |
| Applies to | `schema:domainIncludes`; `rdfs:domain` |
| Concept referred to | `schema:rangeIncludes`; `rdfs:range` |
| Parent | `rdfs:subClassOf` |
| Main label and other label | `skos:prefLabel` and `skos:altLabel` (W3C) |
| Definition | `skos:definition` |
| Number of values and required | `sh:maxCount` and `sh:minCount` in SHACL (W3C) |
| Check per action | SHACL validation of one set of data |
| Type and role | the distinction between *kind* and *role* in OntoClean and UFO (ontology research) |
| Personal data | *personal data* in the GDPR (European Union) and similar data protection laws in many countries; ISO/IEC 29100 |

## 8. Open questions

1. **A concept that must not be a direct type.** Is a marker needed for a
   concept that is only used through its children, for example Transaction that
   is always a Rental, a Sale, or something else?
2. **Tiered personal data [provisional].** Is yes/no enough, or are tiers
   needed, for example health data that is more sensitive? Waiting for a legal
   review.
3. **Time gaps in required properties.** CONCEPT-18 only checks the time
   touched by an action. Is a full check needed over the whole history of an
   entity?
