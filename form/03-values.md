# Values

Status: draft

## 1. Purpose

A value is the content of a fact: a name, a price, a date, or another entity
that is referred to. The form of values makes sure that every value has the same
meaning for any reader: the same number is computed the same way, money does not
get mixed up with another currency, and a date does not shift because of a time
zone. The form is small on purpose, so that all the needs of a domain are met by
content, not by new value types.

## 2. Definitions

### 2.1 Value types

The list of value types is form, and it is closed. Every property states
exactly one value type ([`04-concepts.md`](04-concepts.md) §2.2).

| Value type | Address | Meaning | Example |
|---|---|---|---|
| **Text** | `standard/text` | A sequence of letters, may come with a language code (§2.5) | "Budi", "Tent with a capacity of 4 people"@en |
| **Number** | `standard/number` | An exact number, may come with a unit (§2.2, §2.3) | 3; 2.5 kg; 150,000 IDR |
| **Yes/no** | `standard/yes_no` | One of two: yes or no | yes |
| **Date** | `standard/date` | One calendar day, without a time of day (§2.4) | 6 October 2026 |
| **Instant** | `standard/instant` | One exact point in time, with its time zone (§2.4) | 6 October 2026 at 09:00 WIB |
| **Choice** | `standard/choice` | One choice from a choice list (§2.6) | paid in full |
| **Reference** | `standard/reference` | The identifier of another entity (§2.7) | rental R1 → Budi |

Money, weight, length, and duration are **not** value types of their own. All of
them are written as a **number with a unit**.

The value of the basic property *type* is the address of a concept. This is
special to the property owned by the form, and is not a value type available to
content.

### 2.2 Exact numbers

Numbers in this form are always **exact**: written and computed as decimal
numbers as they are, without silent rounding. 0.1 + 0.2 equals exactly 0.3. A
number may be negative and may have digits after the decimal point.

Rounding, for example to the nearest rupiah or to two digits after the decimal
point, is a **calculation rule** that belongs to content
([`06-calculation-rules.md`](06-calculation-rules.md)), not part of the value.

### 2.3 Quantity and unit

- A **quantity** is a kind of measurement: money, mass, length, duration, area,
  temperature, ratio.
- A **unit** is the way to measure that quantity: IDR and USD for money, kg and
  g for mass, days and hours for duration.

A number property **may set one quantity**. When it is set, every one of its
values **must carry a unit** of that quantity.

| Property | Quantity | Accepted values | Rejected values |
|---|---|---|---|
| price | money | 150,000 IDR; 10 USD | 5 kg; 150,000 (without a unit) |
| weight | mass | 2.5 kg; 800 g | 2.5 IDR |
| rental duration | duration | 3 days; 36 hours | 3 |
| number of guests | — (pure number) | 4 | 4 kg |

The list of quantities and units is **content**, taken from standard code
lists: currencies from ISO 4217, other units from UCUM. The list is the code
list `uniti/unit/Unit` in [`content/code-lists`](../content/code-lists.md).
Every unit is a choice from that code list, so a unit can also be a choice
value, for example the source currency of an exchange rate.

**There is no automatic conversion.** Changing 10 USD into rupiah, or 36 hours
into days, is a calculation rule. For money, the exchange rate itself is
recorded as a fact, because exchange rates change from day to day.

**Direction.** Every number property states a **direction**: what a positive
number means.

| Direction | Meaning | Example |
|---|---|---|
| **Increase** | A change; positive means there is more afterwards | money received, items in, points earned |
| **Decrease** | A change; positive means there is less afterwards | money paid, items out, points used |
| **No direction** | A change that is never negative; its direction is stated by another property of the same entity | the amount of a movement, with another property "in" or "out" |
| **Position** | Not a change, but how much there is at one moment | balance, price, exam score, number of guests |

Direction prevents the mistake that is most often invisible: numbers that are
added with the sign reversed, or changes that are added to positions. A
calculation rule that mixes directions in a way that makes no sense is reported
by the machine ([`06-calculation-rules.md`](06-calculation-rules.md) §2.10).

### 2.4 Date, instant, and valid time

**Date** and **instant** are two different things:

- a **date** is one calendar day without a time of day, for example a birthday
  or a due date;
- an **instant** is one exact point in time, and always contains its time
  zone, for example the time a payment is received.

Both are used in two places:

1. **As a value**, according to the value type of the property.
2. **As the valid time** of a fact. The valid time may be a date or an
   instant. A property may set one of the two; if it does not set one, both may
   be used.

When a date needs to be compared with an instant, for example when a fact whose
valid time is a date is read at an instant, the date is read as **the start of
that day, according to the default time zone of the organization** that
recorded it.

The **recorded time** is always an instant ([`01-facts.md`](01-facts.md),
FACT-15).

A duration, for example "3 days", is not a date or an instant. It is a number
with the quantity duration (§2.3).

### 2.5 Text and language

Text may come with a **language code**, for example `id` for Indonesian or `en`
for English, according to BCP 47.

- For a **label** ([`04-concepts.md`](04-concepts.md) §2.6), the language code is
  required.
- For an ordinary value, a language code may be used when the text really is in
  a language, for example the description of an item. Names of people and codes
  have no language.

### 2.6 Choice lists

A **choice list** is a set of allowed choices, for example "payment method":
cash, transfer. A choice list has its own address, so one list can be used by
many properties. Every **choice** also has its own address
([`02-addresses.md`](02-addresses.md)).

Every choice list has a card with an address, label, and definition, like a
property card ([`decisions/0051`](../decisions/0051-additions-from-first-content.md)).
A choice that is written inside its list has no card of its own.

The owner of a list declares its list:

| List | Meaning | Example |
|---|---|---|
| **Closed** | Only the owner of the list may add choices, through a new version | list of currencies, list of genders in official documents |
| **Open** | Anyone may add choices, in their own module | payment method, cancellation reason |

A choice that is added to an open list owned by someone else keeps an address
in the module of the one who added it. Example: `ani/cashier/qris` goes into
the list `uniti/payment/PaymentMethod`. Because the address contains its owner,
two people who both add `qris` do not collide. The two can be connected with a
bridge ([`05-relations.md`](05-relations.md)).

An added choice applies only to organizations that install the module that adds
it.

A **code list** holds standard codes from outside standards, such as currencies,
units, countries, and languages. A code list is always closed, and the name of
its choice is the code from the outside standard, written exactly, including
uppercase and lowercase: `uniti/unit/IDR` ([`02-addresses.md`](02-addresses.md)
§2.4; [`decisions/0050`](../decisions/0050-code-lists.md)).

### 2.7 References

A reference value is **the identifier of an entity**
([`01-facts.md`](01-facts.md) §2.2), not a name or a code that has meaning. A
reference property names **the concept that is referred to**, and the entity that
is referred to must belong to that concept or to its child concepts
([`04-concepts.md`](04-concepts.md) §2.5).

Example: the property `customer` refers to the concept Party. Its value is the
identifier of Budi, whose type is Person, and Person is a child concept of
Party.

## 3. Rules

**Value types**

- **VALUE-1.** Every value MUST be one of the seven value types in §2.1.
- **VALUE-2.** Every value MUST match the value type of its property.
- **VALUE-3.** The list of value types MUST NOT be extended by content. The
  needs of a domain MUST be met with the existing value types, plus units,
  choice lists, or concepts.

**Numbers**

- **VALUE-4.** Numbers MUST be stored and computed as exact numbers. Numbers
  MUST NOT be rounded except by a calculation rule that declares it.
- **VALUE-5.** When a number property sets a quantity, every one of its values
  MUST carry a unit of that quantity. When it does not set a quantity, its
  values MUST NOT carry a unit.
- **VALUE-6.** Quantities and units MUST be taken from a code list. Currencies
  MUST use ISO 4217 codes.
- **VALUE-7.** Conversion between units MUST NOT be done silently. A conversion
  MUST be a calculation rule.

**Time**

- **VALUE-8.** An instant MUST contain its time zone. An instant without a time
  zone MUST NOT be recorded.
- **VALUE-9.** A valid time MUST be a date or an instant. When its property sets
  one of the two, the valid time of a fact with that property MUST use the one
  that is set.
- **VALUE-10.** Every organization that records facts MUST have one default time
  zone. A date that is compared with an instant MUST be read as the start of the
  day according to that default time zone.

**Text**

- **VALUE-11.** A language code, when used, MUST follow BCP 47.

**Choices**

- **VALUE-12.** Every choice list MUST be declared open, closed, or a code list.
  A code list behaves like a closed list.
- **VALUE-13.** A choice MUST NOT be added by other parties to a closed list.
- **VALUE-14.** The value of a choice MUST be the address of a choice that goes
  into the list used by its property, from an installed module.
- **VALUE-15.** A closed list MAY be opened in a later version. An open list
  MUST NOT be closed. A code list MUST NOT be opened.
- **VALUE-19.** Every choice list MUST have a card with an address, label, and
  definition.

**References**

- **VALUE-16.** A reference value MUST be the identifier of an entity, and that
  entity MUST belong to the concept that its property refers to, or to a child
  concept of it, at the valid time of the reference fact, according to what is
  known when the action is recorded. This rule is only for facts that state a
  value.

**Direction**

- **VALUE-17.** Every number property MUST state one direction: increase,
  decrease, no direction, or position.
- **VALUE-18.** The value of a property whose direction is no direction MUST NOT
  be negative.

## 4. Examples

**Equipment rental, two currencies.** The Kemah Ceria shop rents out tents to
tourists.

| Fact | Subject | Property | Value |
|---|---|---|---|
| f1 | rental R7 | price | 450,000 IDR |
| f2 | rental R8 | price | 30 USD |
| f3 | USD rate 7 Oct | exchange rate | 16,250 IDR |

The property `price` sets the quantity money, so both rentals use the same
property. A revenue report in rupiah computes R8 through a calculation rule that
uses f3. f3 is an ordinary fact, with its own provenance.

**Clinic, dates and instants.**
- The property `date_of_birth` of a patient has a date as its value: 12 March
  1990.
- The property `arrival_time` has an instant as its value: 6 October 2026 at
  08:47 WITA.
- The price of a consultation applies since the **date** 1 November. The clinic
  in Makassar uses the default time zone WITA, so a payment at 00:30 WITA on
  1 November already uses the new price.

**School, open list.** The vocabulary provides the open list
`uniti/education/AbsenceReason`: sick, excused. A school in a coastal area adds
`sekolah-bahari/attendance/at_sea` in its own module. Other schools do not see
that choice unless they install that module.

## 5. Not examples

- **The value type "money".** Money is a number with the quantity money.
- **"150000" for a price** without a unit, when its property sets the quantity
  money.
- **Approximate binary numbers** that make 0.1 + 0.2 become
  0.30000000000000004.
- **"2026-10-06 09:00"** as an instant. Its time zone is not stated.
- **The customer name "Budi" as a reference value.** A reference is an
  identifier, not a name.
- **A yes/no value "unknown".** When something is unknown, there is no fact
  about it.

## 6. Reasons

- **Seven value types, money and measures as numbers with units.** A small list
  is rarely wrong and does not need to grow. All measures use the same single
  way. ([`decisions/0013`](../decisions/0013-value-types.md))
- **Quantity in the property, unit in the value.** The machine can still reject
  a value that makes no sense, while one property can be used for any currency
  or unit. ([`decisions/0014`](../decisions/0014-quantities-and-units.md))
- **Direction is required for every number.** Earlier experiments showed that
  numbers that are wrong without being seen most often come from the meaning of
  a sign that was never written. ([`decisions/0027`](../decisions/0027-number-direction.md))
- **Date and instant are separated**, with the default time zone of the
  organization, so that "valid since 1 November" means the same to every reader.
  ([`decisions/0015`](../decisions/0015-dates-and-instants.md))
- **Open or closed list.** The owner of a list keeps holding its list, while
  others can add without asking permission and without colliding.
  ([`decisions/0016`](../decisions/0016-choice-lists.md))

## 7. Outside standards

| Part | Equivalent |
|---|---|
| Value types | XML Schema data types: `xsd:string`, `xsd:decimal`, `xsd:boolean`, `xsd:date`, `xsd:dateTime` |
| Exact numbers | `xsd:decimal`; not IEEE 754 binary numbers |
| Quantity and unit | *quantity kind* and *unit* in QUDT; UCUM units; UN/ECE Rec. 20 |
| Currency | ISO 4217 |
| Date and instant | ISO 8601; RFC 3339 for an instant with a time zone |
| Text with a language | `rdf:langString`; language code BCP 47 |
| Choice list | `skos:ConceptScheme` (W3C) |

## 8. Open questions

1. **Self-made units.** Businesses often use units such as "box" or "package"
   whose contents differ. May a unit like this be made as content, and how does
   it relate to standard units?
2. **Precision of numbers.** May a property set the number of digits after the
   decimal point, for example following the precision of each currency in
   ISO 4217?
3. **An organization with several time zones.** If the branches of an
   organization are in Jakarta (UTC+7) and Tokyo (UTC+9), which default time
   zone is used, and
   how is the default time zone recorded and changed?
4. **Limits on values.** Is a limit such as "at least 0" or "at most 100
   characters" part of the property, or is it stated as a rule? Limits on
   numbers can now be written as a constraint ([`06-calculation-rules.md`](06-calculation-rules.md)
   §2.12); for the length of text there is no operation yet.
5. **Ordered choices.** May a choice list state an order, for example low,
   medium, high, so that its choices can be compared?
6. **References to an entity in another organization.** Depends on the open
   question about the identity of entities across organizations
   ([`01-facts.md`](01-facts.md) §8).
