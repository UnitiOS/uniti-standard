# Facts

Status: locked (v0.1.0)

> [Uniti Standard](../README.md) › Part A: form, 1 of 8
> · Previous: [Glossary](../01-glossary.md) · Next: [Addresses](02-addresses.md)
> · [Rules FACT-n](../rules.md#facts)

## 1. Purpose

Facts are the only thing an organization really stores. All numbers, reports,
and views are derived from them. The form of a fact makes sure that every fact
can be trusted, can be traced to its origin, can be read back as it was on any
day, and is never lost, whatever changes around it.

## 2. Definitions

### 2.1 The parts of a fact

A fact is **one statement about one entity**. It consists of:

| Part | Meaning | Example |
|---|---|---|
| **Identifier** | The unique code of the fact itself | `f-8c21…` |
| **Subject** | The entity being talked about | rental R1 |
| **Property** | What is said about the subject, pointed to by its address | customer |
| **Value** | The content: text, number, date, or another entity that is referred to | Sam |
| **Valid time** | Since when the fact is true in the world | 6 October 2026 |
| **Fact kind** | What this fact does to another fact (§2.3) | statement |
| **Target** | The old fact it touches, when the kind is not statement | — |
| **Version used** | The version of the module that was used when this fact was stated | rental v2 |
| **Action** | The action that recorded it, with its provenance (§2.4) | action "record rental" |

The form of values and the meaning of time are detailed in
[`03-values.md`](03-values.md). The form of the address of a property is
detailed in [`02-addresses.md`](02-addresses.md).

### 2.2 Entity

An **entity** is anything that can be talked about: a person, an item, an
event, a promise, a document. Every entity has an **identifier**:

- random, unique in the whole world, and permanent;
- carrying no meaning at all;
- never reused for another entity.

A code that has meaning for humans, such as a customer number, an item code, or
a national identity number, is a **property** of that entity, not its
identifier.

The concept an entity belongs to (for example "Rental" or "Person") is stated
with one basic property owned by the form, namely **type**. Type is a fact like
any other fact. Type is what the entity really is; a role such as customer or
patient is not a type (see [`04-concepts.md`](04-concepts.md) §2.5).

### 2.3 Fact kinds

Every fact is one of six kinds. The first five kinds are derived from two
questions about the old fact that is touched: *was it true once?* and *is there
a replacing value?*

| | There is a replacing value | There is no replacing value |
|---|---|---|
| **Was true once** (the world changed) | **Replacement** | **Ending** |
| **Was never true** (the recording was wrong) | **Correction** | **Retraction** |

| Kind | Meaning | Has a value? | Has a target? |
|---|---|---|---|
| **Statement** | A fact that does not touch another fact | yes | no |
| **Replacement** | The target was true once; since the valid time of this fact, its value is replaced | yes | yes |
| **Ending** | The target was true once; since the valid time of this fact, it no longer applies | no | yes |
| **Correction** | The target was never true; this fact replaces it completely | yes | yes |
| **Retraction** | The target was never true; there is no replacement | no | yes |
| **Redaction** **[provisional]** | The target stays in force, but its value must no longer be read (§2.6) | no | yes |

The fact kind is form, and its list is closed. The **reason** for a change
(typing mistake, court decision, customer report, audit result) is content, and
its list is open.

### 2.4 Action and provenance

A fact is never recorded alone. Every fact is recorded by exactly one
**action**, and one action may record many facts at once. The action carries the
provenance:

| Part of an action | Meaning | Required? |
|---|---|---|
| **Actor** | Who makes the statement. The actor is an entity; whether it is a person, an AI, or a machine is a fact about that actor | required |
| **Approver** | Who approves and is responsible, when different from the actor | required if the actor is not responsible alone |
| **Recorded time** | When this action is recorded | required |
| **Source** | Where the facts come from: typed in, imported, from a device, from another system, … | required |
| **Action name** | What is done, in human words | should |
| **Reason** | Why, for an action that corrects, retracts, or redacts | required for those kinds |
| **Confidence level**, **basis of authority** | How sure, and on what basis the actor has authority | may |

The parts are form. The choices of content (kinds of source, list of reasons,
confidence level) are content, and are detailed in the vocabulary.

### 2.5 Reading facts at two times

Every question about an entity is asked at **two times**:

- **valid time** *T*: the state of the world on which date is asked;
- **as of** *R*: according to what has been recorded up to which date.

The value of property *P* of subject *S* at (*T*, *R*) is read like this:

1. Take all facts about *S* and *P* whose recorded time is at most *R*.
2. Discard every fact that is corrected or retracted by another fact in step 1.
3. From those that remain, take the facts whose valid time is at most *T*.
   - **A property with one value** is read as one timeline. What applies is
     the fact with a value, or the ending, with the latest valid time; if the
     valid time is the same, the one recorded last. If that last one is an
     ending, the property has no value at *T*.
   - **A property with many values** is read per value. A fact with a value
     applies if it has not been replaced or ended by another fact in this step.
   - **A correction takes the place of its target completely.** A replacement
     or ending of that target also replaces or ends its correction. A
     correction of a replacement also replaces the target of that replacement.
4. A fact that is redacted still counts as in force, but its value is read as
   "redacted".

The valid time of a retraction or redaction is not read, because its target is
discarded or redacted at every time. The writer SHOULD use the valid time of
its target.

Example of step 3, for a rate with one value
([`decisions/0044`](../decisions/0044-additions-from-reference-calculator.md),
[`decisions/0053`](../decisions/0053-reading-corrected-facts.md)):

- Rate 100 since 1 October, replaced by 150 since 1 November, then the rate of
  1 October is corrected to 120. The October rate is 120, and the November rate
  is 150.
- Rate 150 since January, replaced by 175 since November. It turns out to be a
  typing mistake, and 175 is corrected to 180. The December rate is 180.
- Rate 100 since January, replaced by 150 since November. Later it is learned
  that the rate has been 120 since June, and that is recorded as a replacement
  of the January rate. The July rate is 120, and the December rate is 150.

In all three, there are never two rates at once.

Because the rules are fixed, two readers who ask the same question always get
the same answer, and what was known on any day can always be read back.

### 2.6 Redaction **[provisional]**

> This section concerns the legal rights of outside parties, for example the
> right of a person to ask for their personal data to be erased. The form is
> written now, but it may still change after it is discussed with parties who
> understand the law.

Redaction makes the value of a fact unreadable, without deleting the fact. What
stays visible: that the fact once existed, what it was about, when, by whom, and
that it was redacted, when, and for what reason. The technical way to redact
(emptying the value, or locking the value and then destroying the key) is left
to the implementation.

### 2.7 Computed values are not facts

A number derived from facts, such as a total, a balance, or an average, is not a
fact. It may be stored to speed up reading, but it never becomes a source of
truth. Its form is detailed in
[`06-calculation-rules.md`](06-calculation-rules.md).

## 3. Rules

**Facts**

- **FACT-1.** A fact MUST have an identifier, subject, property, valid time,
  fact kind, version used, and action.
- **FACT-2.** A fact MUST state exactly one value when its kind is statement,
  replacement, or correction, and MUST NOT state a value when its kind is
  ending, retraction, or redaction.
- **FACT-3.** A fact that is already recorded MUST NOT be changed or deleted.
  Every change MUST be a new fact.
- **FACT-4.** A computed value MUST NOT be recorded as a fact.

**Entity**

- **FACT-5.** The identifier of an entity MUST be unique in the whole world,
  permanent, and meaningless. An identifier MUST NOT be reused.
- **FACT-6.** A code that has meaning for humans MUST be recorded as a property,
  not as an identifier.
- **FACT-7.** Every entity MUST have a type fact that states the concept it
  belongs to.

**Fact kind and target**

- **FACT-8.** The fact kind MUST be one of: statement, replacement, ending,
  correction, retraction, redaction.
- **FACT-9.** A fact whose kind is not statement MUST name exactly one target,
  which is a fact that is already recorded before it, with the same subject and
  property.
- **FACT-10.** The valid time of a replacement or ending MUST be later than the
  valid time of its target. If it is the valid time of the target that is
  wrong, a correction is used.
- **FACT-11.** A correction MUST target a fact that has a value. A wrong ending
  is repaired by retracting it and then recording the right ending.
- **FACT-12.** If the subject or property of a fact is wrong, that fact MUST be
  retracted and the right fact recorded as a new statement. A correction
  MUST NOT change the subject or property.
- **FACT-13.** A retraction MUST NOT target another retraction. A fact that
  turns out to be right is stated again as a new statement.
- **FACT-14.** For a property that holds only one value at one time, a new value
  MUST be a replacement that targets the value in force at the valid time of
  that replacement, or a correction of the wrong fact, not a second statement.
  An action MUST NOT record two values for such a property on the same entity
  and valid time.

**Time**

- **FACT-15.** The recorded time MUST be given by the recorder at the moment the
  action is recorded, and MUST NOT be filled in by the actor.
- **FACT-16.** The valid time MAY be in the past or in the future.
- **FACT-17.** Reading at two times MUST follow the steps in §2.5.

**Action and provenance**

- **FACT-18.** Every fact MUST be recorded by exactly one action, and all facts
  in one action MUST be recorded together or not at all.
- **FACT-19.** Every action MUST have an actor, recorded time, and source.
- **FACT-20.** If the actor is not responsible alone for its action, for example
  an AI or a machine acting for someone else, the action MUST name an approver.
- **FACT-21.** An action that corrects, retracts, or redacts MUST name a reason.
- **FACT-22.** An action SHOULD have an action name in human words.

**Redaction [provisional]**

- **FACT-23.** A redaction MUST target a fact whose property is marked as
  personal data. A property that is not marked MUST NOT be redacted.
- **FACT-24.** A redaction MUST NOT be retracted or corrected.
- **FACT-25.** After a redaction, the value of its target MUST NOT be readable
  by anyone, while the other parts of that fact MUST remain readable.

## 4. Examples

**Equipment rental.** Sam rents a tent on 6 October. The cashier mistypes the
name of the customer, then fixes it the next day.

| Fact | Subject | Property | Value | Valid | Kind | Target | Recorded |
|---|---|---|---|---|---|---|---|
| f1 | rental R1 | type | Rental | 6 Oct | statement | — | 6 Oct 10:02 |
| f2 | rental R1 | customer | Saam | 6 Oct | statement | — | 6 Oct 10:02 |
| f3 | rental R1 | customer | Sam | 6 Oct | correction | f2 | 7 Oct 08:15 |

- Read as of 6 October at 12:00: the customer is Saam, because that is what was
  known at that time.
- Read as of 7 October at 12:00 or later: the customer is Sam, and since
  6 October.
- f1 and f2 are recorded by one action ("record rental", actor: cashier Eva,
  source: typed in). f3 is recorded by another action with the reason "typing
  mistake".

**Clinic.** The price of a consultation rises from 1 November. Then a patient
stops being a subscribed patient.

| Fact | Subject | Property | Value | Valid | Kind | Target |
|---|---|---|---|---|---|---|
| f10 | general consultation | price | 150,000 IDR | 1 Jan | statement | — |
| f11 | general consultation | price | 175,000 IDR | 1 Nov | replacement | f10 |
| f20 | patient Maria | subscription | yes | 1 Mar | statement | — |
| f21 | patient Maria | subscription | — | 1 Oct | ending | f20 |

- The price on 15 October is still 150,000 IDR. f10 is not wrong; the world
  changed.
- On 15 October, Maria is no longer a subscribed patient. On 15 September Maria
  is still a subscribed patient.

**School, with an AI actor.** An AI assistant proposes exam scores from a
scanned sheet, then the teacher approves them. The action: actor "AI
assistant", approver "Kim", source "scan".

## 5. Not examples

- **"Cash balance today 2,400,000 IDR"** is a computed value, not a fact.
- **One fact that states two values** ("phone: 0812… and 0813…"). That is two
  facts.
- **Changing the value of an old fact in place.** Every change is a new fact.
- **Customer number "PLG-001" as an identifier.** That is a property.
- **A fact without an action**, for example data that appears without anyone
  knowing who recorded it.

## 6. Reasons

- **A fact has no end time.** A fact ends when another fact replaces or ends it.
  Because of this, no old fact has to be edited when something ends, and every
  fact is connected to the fact that follows it. ([`decisions/0005`](../decisions/0005-facts-without-end-time.md))
- **The fact kinds are derived from two questions**, not from examples, so they
  are complete by themselves. ([`decisions/0006`](../decisions/0006-fact-kinds.md))
- **A property with one value is read as a timeline.** The target of a
  replacement can become obsolete when its history is repaired, while the valid
  time cannot. By reading according to valid time, corrections and changes that
  are learned later never produce two values at once. ([`decisions/0053`](../decisions/0053-reading-corrected-facts.md))
- **Provenance: the parts are form, the choices are content.** Every fact always
  answers who, through what, from where, and when, while the kinds of source and
  reasons can keep growing. ([`decisions/0007`](../decisions/0007-provenance.md))
- **A computed value is not a fact**, so that there are never two truths that
  can contradict each other. ([`decisions/0008`](../decisions/0008-computed-values.md))
- **Redaction** is the middle point between "facts are never lost" and the legal
  rights over personal data. ([`decisions/0009`](../decisions/0009-redaction.md))

## 7. Outside standards

| Part | Equivalent |
|---|---|
| Subject, property, value | RDF (W3C): *subject, predicate, object* |
| Valid time and recorded time | *valid time* and *transaction time*; bitemporal tables in SQL (ISO/IEC 9075:2011) |
| Action, actor, source | PROV-O (W3C): *Activity*, *Agent*, *wasAttributedTo*, *hadPrimarySource* |
| Correction and retraction without deleting | double-entry bookkeeping: a mistake is repaired with a reversing journal entry, not by deleting |

## 8. Open questions

1. **Redaction** (§2.6): the form needs to be reviewed together with parties who
   understand data protection law.
2. **One entity in two organizations.** If Sam is recorded in two
   organizations, Sam has two identifiers. The form of a "same as" fact between
   organizations, and who may state it, is not yet decided.
3. **Facts about facts.** Besides provenance, is a form needed to state
   something about another fact, for example "this fact is disputed"?
