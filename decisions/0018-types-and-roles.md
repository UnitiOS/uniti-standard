# 0018. Types and roles

Date: 2026-10-17
Status: accepted

**Context**
Budi is a person. He is also a customer of Rudi and an employee elsewhere. If
every role is made a type, one person can be recorded as several things, or
the type has to be replaced every time the role changes.

**Decision**
- A **type** is what an entity really is (Person, Item, Rental), and it does
  not change. A type fact may only be corrected or retracted, not replaced and
  not ended.
- A **role** (customer, employee, patient) is recorded as a **reference from
  another entity**, for example "the customer of rental R1 is Budi".
- An entity may have more than one type if that is truly its basic nature and
  the types are not subtypes of each other, but it is better to have one.

**Alternatives**
- *One type only, forever.* Rejected: too rigid for an entity that really has
  two basic natures.
- *Many types, added and ended at any time.* Rejected: the type becomes a mix
  of what the entity is and what it is doing, and the question "who are Rudi's
  customers" loses its context.

**Consequences**
- Answers the open question in `01-facts.md` about an entity with more than
  one type.
- The vocabulary does not contain concepts such as Customer or Patient as
  types; what it contains are reference properties that state the role.
