# A tour: Alex's equipment rental

Status: guide; not normative

> [Uniti Standard](../README.md) › Guide · for a first-time reader who wants to
> see every part of the form work together on one small story

This guide points and explains. It adds no rule. When this guide and the
normative text differ, the normative text wins.

The story: Alex rents out tents. Alex keeps the facts of each rental and writes
a small module, `alex/rental`, that does two things: it works out the **total
due** of a rental, and it stops a tent from being **rented twice** on the same
day.

How to read this tour:

- The ideas are explained in plain words in the
  [introduction](introduction.md). This tour shows the same ideas in the
  real notation.
- Every code block is copied, in whole or in part, from a file in
  [`conformance/`](../conformance/); the link near each block says which.
  Every result is the `result` line written in that example.
- You do not need to learn the notation first. After each block, the text
  says how to read it.
- Each section ends with a line **In the standard**, which names the
  sections and rules that say it exactly. You can skip those lines on a first
  reading.

## 1. Facts: what is recorded

Alex records only what happened: the tent has a daily rate, and someone rents
it from one day to another. Each of these is a **fact**, one small statement
about one thing.

Here are the facts of one rental, from the example `three_night_rental` in
[`00-form-examples.md`](../conformance/00-form-examples.md#rental):

```uniti
  facts        recorded 6 Oct 2026 10:00
    tent  type        Item            valid 1 Oct 2026
    f1: tent  daily_rate  50,000 IDR/day  valid 1 Oct 2026
    r1    type        Rental          valid 6 Oct 2026
    r1    item        tent            valid 6 Oct 2026
    r1    start_date  6 Oct 2026      valid 6 Oct 2026
    r1    end_date    9 Oct 2026      valid 6 Oct 2026
```

How to read it:

- The first line says **when** all the facts below it were recorded:
  6 October, 10:00.
- Every other line is one fact, read from left to right: **which thing**,
  **what about it**, **the value**, and **since when it is true**
  (`valid`). The first fact reads: the tent is an Item, since 1 October.
- `tent` and `r1` are short names used only inside this example. Real
  software gives every thing a permanent identifier instead.
- The `type` lines say what kind of thing each one is: the tent is an Item,
  `r1` is a Rental.
- `f1:` gives the fact a name, so that a later fact can point to it.

So every fact has two times: when it is **true** (`valid`) and when it was
**recorded**.

A fact is never changed or deleted. When the rate goes up, Alex records a new
fact. This is from the example `rate_rise_after_rental`:

```uniti
    f2: tent  daily_rate  60,000 IDR/day  valid 1 Nov 2026  recorded 20 Oct 2026  replaces f1
```

How to read it: the tent's daily rate is 60,000 IDR, true from 1 November,
recorded on 20 October, and it **replaces** `f1`. The old fact stays as it
was, and is still true for the days before 1 November.

**In the standard:** [`form/01-facts.md`](../form/01-facts.md) §2.1 (the
parts of a fact, FACT-1), §2.3 (fact kinds, FACT-8), §2.5 (the two times);
never changed (FACT-3); types (FACT-7); short names
([`form/08-proof.md`](../form/08-proof.md) §2.3); the notation of facts
([Appendix A §2.9](../appendix/A-notation.md#29-examples)).

## 2. The module and its address

Alex's words and rules are kept together in a **module**. The first lines of
the module are:

```uniti
module alex/rental@v3
  uses uniti/item@v1
```

From [`00-form-examples.md`](../conformance/00-form-examples.md#rental).

How to read it:

- `alex` is the **owner**, `rental` is the **name** of the module, and `@v3`
  is its **version**, the third edition. Versions 1 and 2 appear in
  section 7.
- `uses uniti/item@v1` says the module builds on the shared module for items,
  at exactly version 1. A new version of `uniti/item` changes nothing for Alex
  until Alex chooses to move.

Everything in the module has an **address**: owner, module, name. The concept
`Rental` of this module is `alex/rental/Rental`. Because the owner is part of
the address, another builder's `Rental` can never be confused with Alex's.
The address has **no version** inside it, which is why facts recorded with
one version can still be read by the next (section 7).

**In the standard:** [`form/02-addresses.md`](../form/02-addresses.md) §2.2
(ADDRESS-1) and
[§2.3](../form/02-addresses.md#23-an-address-does-not-contain-a-version)
(ADDRESS-4); an exact version (CHANGE-14).

## 3. The concept and its properties

Each kind of thing and each piece of information has a **card**, like a
dictionary entry. From the same module:

```uniti
concept Rental
  label.en     Rental
  definition.en  Use of an item by a renter for a certain term, for a fee.
  includes.en  Rental of a tent for three nights.
  excludes.en  Sale of a tent, because the item changes owner.

property start_date : date
  label.en     Start
  definition.en  The first day of the rental term.
  personal     no

property end_date : date
  label.en     End
  definition.en  The day the item is returned. This day is not counted.
  personal     no

property daily_rate : number (money/duration, position)
  label.en     Daily rate
  definition.en  The rental price of an item for one day.
  personal     no
```

How to read it:

- The **concept card** `Rental` has a name (`label`), a definition, one thing
  it includes, and one thing that looks similar but is excluded. `.en` means
  the text is in English; the same card may have texts in other languages.
- Each **property card** has a name after `property`, and after the colon the
  kind of value: `date`, or `number`.
- `number (money/duration, position)` says the daily rate is an amount of
  money per length of time, so its values carry a unit such as `IDR/day`.
  `position` says it is how much there is at one moment, not a change.
- `personal no` says the value is not personal data. This mark is still
  provisional.

Then the module says which properties apply to which concept, and which are
required:

```uniti
applies to Rental:
  item         required
  start_date   required
  end_date     required

applies to Item:
  daily_rate
```

A rental must have an item, a start date, and an end date. The daily rate
belongs to the item, and is not required.

`Item` and the property `item` are not defined here. They come from the
shared module `uniti/item`, which this module uses. Alex may say that
`daily_rate` applies to `Item` because the statement is in Alex's own module;
the shared `Item` card is not changed.

**In the standard:** [`form/04-concepts.md`](../form/04-concepts.md) §2.1
(cards, CONCEPT-1, CONCEPT-3) and §2.3 (applies to, CONCEPT-6, CONCEPT-18);
quantity and unit ([`form/03-values.md`](../form/03-values.md) §2.3,
VALUE-5); direction (VALUE-17).

## 4. A computed property: `total_due`

The total due can be worked out from the facts, so it is never recorded. It
is a **computed property**: a rule works it out each time it is asked for.

```uniti
helper Rental.term : range
  rule:
    range(this.start_date, this.end_date)

computed Rental.total_due : number (money, increase), closed
  label.en     Total due
  definition.en  The daily rate of the item times the number of days in the
               rental term.
  personal     no
  rule:
    this.item.daily_rate × span(this.term, day)
```

Copied from [`00-form-examples.md`](../conformance/00-form-examples.md#rental).

How to read it:

- The **helper** `term` is the rental term: from the start date up to, but
  not including, the end date. A helper is a step used by other rules.
- The rule of `total_due` reads: the daily rate of this rental's item, times
  the number of days in the term. `this` means the rental being asked about.
- `number (money, increase)` says the result is an amount of money, and a
  positive amount means an increase: a total adds to what is owed. The daily
  rate, by contrast, is a `position`: a price at one moment. `closed` says
  that other modules cannot add to this number.

A computed property is asked like any other property, with the two times
from section 1: `T`, the valid time the question is about, and `R`, the
recorded time to read up to, "as it was known at" that moment.
This is the question in `three_night_rental`:

```uniti
  ask          r1.total_due   T: 6 Oct 2026   R: 6 Oct 2026 12:00
  result       150,000 IDR
```

Three days at 50,000 IDR a day: 150,000 IDR.

The same question in `rate_rise_after_rental`, after the rate rise from
section 1 was recorded, gives:

```uniti
  ask          r1.total_due   T: 6 Oct 2026   R: 21 Oct 2026
  result       150,000 IDR
```

The answer does not change. The rule reads the daily rate as it is at `T`,
6 October, which is still 50,000 IDR; the new rate only holds from
1 November. A rental that runs across 1 November could be priced in other
ways, for example with the rate of each day; the examples `rate_on_start_day`
and `rate_every_day` in
[`00-form-examples.md`](../conformance/00-form-examples.md#rental-a-rate-that-changes-in-the-middle-of-the-rental-term)
show two such rules.

**In the standard:**
[`form/06-calculation-rules.md`](../form/06-calculation-rules.md) §2.3
(computed property, CALC-4 to CALC-6); not recorded as a fact (FACT-4,
CALC-5); ranges (CALC-26); reading at two times
([`form/01-facts.md`](../form/01-facts.md) §2.5).

## 5. A constraint: `no_overlap`

Some rules say **no**. A **constraint** is a yes/no rule. If a new recording
would make it no, the whole recording is refused. Alex's constraint:

```uniti
constraint Rental.no_overlap
  label.en     No overlap
  definition.en  One item is not rented out twice on the same day.
  message.en   This item is already rented for part of that term.
  rule:
    count(all(Rental, s: s ≠ this and s.item = this.item
                            and exists(overlap(s.term, this.term)))) = 0
```

Copied from [`00-form-examples.md`](../conformance/00-form-examples.md#rental).

How to read it:

- `all(Rental, s: …)` takes every rental `s` that matches what follows: it is
  not this rental, it has the same item, and its term overlaps this term.
- `count(…) = 0` says there must be none.
- `message` is the text people see when the rule refuses a recording.

In the example `one_day_overlap`, someone tries to rent the tent from 12 to
14 October, while it is already rented from 10 to 13 October. The two terms
share 12 October. The result written there is:

```uniti
  result       rejected by no_overlap, entity r2
```

The refusal names the rule and the rental it is about. It is kept as a
**rejection record**, so it can be read back later, for example to see why a
recording was refused. It is not a fact: it is never read when facts are
read, and never changes a computed value.

**In the standard:**
[`form/06-calculation-rules.md`](../form/06-calculation-rules.md) §2.12
(constraint, CALC-38); the message (CALC-37); what a rejection names
(CALC-41); rejection records (CALC-42, CALC-43).

## 6. Examples as proof

Every rule carries **examples**: some facts, one question or one action, and
the result that must come out. A machine runs them; a rule is accepted only
when its examples pass. There are three kinds:

| Kind | What it checks | Example in module v3 | Result written |
|---|---|---|---|
| compute | the answer to a question at `T` and `R` | `three_night_rental`, `rate_rise_after_rental` | `150,000 IDR` for both |
| reject | a recording is refused by the named constraint | `one_day_overlap` | `rejected by no_overlap, entity r2` |
| accept | a recording is accepted; a question may follow | `adjoining_no_overlap` | `accepted`, then `100,000 IDR` |

The accept example shows that the constraint does not refuse everything. It
starts from the facts of `one_day_overlap`, where the tent is already rented
from 10 to 13 October, and the rate of 50,000 IDR a day:

```uniti
  action       recorded 5 Oct 2026 15:00
    r2     type        Rental        valid 5 Oct 2026
    r2     item        tent          valid 5 Oct 2026
    r2     start_date  13 Oct 2026   valid 5 Oct 2026
    r2     end_date    15 Oct 2026   valid 5 Oct 2026
  result       accepted
  ask          r2.total_due   T: 13 Oct 2026   R: 5 Oct 2026 16:00
  result       100,000 IDR
```

Copied from the example `adjoining_no_overlap` in
[`00-form-examples.md`](../conformance/00-form-examples.md#rental).

How to read it: the `action` is a new recording, a rental from 13 to
15 October. The other rental ends on 13 October, and the end day is not
counted, so no day is used twice. The recording is `accepted`, and its total
due is two days at 50,000 IDR.

The result must match exactly, unit included. The facts an example starts
with are taken as already recorded; only the action is checked.

**In the standard:** [`form/08-proof.md`](../form/08-proof.md) §2.1 (kinds
of example), §2.4 (exact results, PROOF-5); which rules need which examples
(PROOF-13, PROOF-15); starting facts (PROOF-30); reject names its constraint
(PROOF-32); the notation of examples
([Appendix A](../appendix/A-notation.md) §2.9).

## 7. Change: from version to version

Modules change by publishing new **versions**, like new editions of a book. A
published version never changes. The module in sections 2 to 6 is version 3
of `alex/rental`. To show change, this section uses versions 1 and 2 from
[`15-change.md`](../conformance/15-change.md#u1-a-new-version-adds-a-property),
which are smaller. It has three parts: a new version, a user of the module,
and old facts.

Version 2 adds one property:

```uniti
property promised_return_date : date
```

A machine compares the two versions and finds one **addition**. The author
does not label the change; the machine does. Everything in version 1,
including its examples, is still in version 2.

A camping shop that uses Alex's module names one exact version:

```uniti
module happy-camp/shop@v1
  uses alex/rental@v1
```

Copied from [`15-change.md`](../conformance/15-change.md#u2-a-user-is-bound-to-an-exact-version).
Version 2 changes nothing for the shop. When the shop moves to version 2, its
own examples are run again with version 2.

Old facts still read the same, because addresses have no version. Here an
old rental, recorded before the new property existed, is asked for it. This
is a whole example: `kind` says what it checks, `zone` gives the time zone
used to read dates (WIB, Western Indonesia Time), and `facts as in
weekend_rental` reuses the starting facts of another example in the same
file:

```uniti
example promised_return_old_rental
  kind         compute
  title        Old rental without a promised return date
  explanation  The rental was recorded before that property existed. Its
               facts can still be read, and the new property is empty.
  zone         WIB
  facts        as in weekend_rental
  ask          s1.promised_return_date   T: 16 Oct 2026   R: 16 Oct 2026 12:00
  result       empty
```

From the same file. The old facts are read without being moved or converted,
and the new property is simply `empty`.

If a new version does change an answer, an old example fails when it is run
again. The owner then fixes the rule, or marks the old example as replaced,
with a reason; an example is never deleted. Case
[`U3`](../conformance/15-change.md#u3-behavior-change) shows this.

**In the standard:** [`form/07-change.md`](../form/07-change.md) §2.1 and
§2.2 (versions never change, CHANGE-1; the machine finds the kind of change,
CHANGE-5; everything stays, CHANGE-6); a user is not affected (CHANGE-15);
old facts ([§2.6](../form/07-change.md#26-facts-and-versions)); running examples again (PROOF-24);
marking an example replaced (PROOF-19 to PROOF-21).

## 8. What you have seen

| In the story | The idea | Where |
|---|---|---|
| The rate and the rental | Only facts are recorded, each with two times | [`form/01-facts.md`](../form/01-facts.md) |
| The rate rise | A change is a new fact; nothing is erased | [`form/01-facts.md`](../form/01-facts.md) |
| `alex/rental@v3` | Content lives in modules, with owners and versions | [`form/02-addresses.md`](../form/02-addresses.md) |
| `Rental`, `daily_rate` | Every concept and property has a card | [`form/04-concepts.md`](../form/04-concepts.md) |
| `total_due` | Numbers are worked out by rules | [`form/06-calculation-rules.md`](../form/06-calculation-rules.md) |
| `no_overlap` | Rules can refuse a recording | [`form/06-calculation-rules.md`](../form/06-calculation-rules.md) |
| The examples | Every rule proves itself | [`form/08-proof.md`](../form/08-proof.md) |
| Versions 1 and 2 | Change by new versions; users are not affected | [`form/07-change.md`](../form/07-change.md) |

Where to go next:

- [Overview](overview.md): a map of all the normative documents, and a table of
  "where do I find ...".
- [Implementing](implementing.md): for people who build software that follows
  the standard.
- [`conformance/`](../conformance/): all the worked cases. More rental cases
  are in [`03-rental.md`](../conformance/03-rental.md).
- [`rules.md`](../rules.md): the index of all 221 rules.
- [`form/`](../form/01-facts.md): the normative text, starting with Facts.
