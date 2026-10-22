# A tour: Alex's equipment rental

Status: guide; not normative

> [Uniti Standard](../README.md) › Guide · for a first-time reader who wants to
> see every part of the form work together on one small story

This guide points and explains. It adds no rule. When this guide and the
normative text differ, the normative text wins.

The story: Alex rents out tents. Alex keeps the facts of each rental and writes
a small module, `alex/rental`, that works out the total due and stops a tent
from being rented twice on the same day. Every code block below is copied from
a file in [`conformance/`](../conformance/); the link above each block says
which one. Every result is the `result` line written in the example.

## 1. Facts: what is recorded

A **fact** is one statement about one entity. It has a subject, a property, a
value, a valid time, and more ([`form/01-facts.md`](../form/01-facts.md) §2.1,
FACT-1). Two times matter:

- the **valid time**: since when the statement is true in the world;
- the **recorded time**: since when it is known and recorded
  ([§2.5](../form/01-facts.md#25-reading-facts-at-two-times)).

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

Each line says: this entity, this property, this value, valid from this day.
`tent` and `r1` are names that only exist inside the example (local ids,
[`form/08-proof.md`](../form/08-proof.md) §2.3). The first line gives the
recorded time for all the lines below it ([Appendix A
§2.9](../appendix/A-notation.md#29-examples)). The `type` lines state which
concept an entity belongs to (FACT-7).

A fact is never changed or deleted once recorded (FACT-3). If the rate
changes, a new fact replaces the old one. This is from the example
`rate_rise_after_rental`:

```uniti
    f2: tent  daily_rate  60,000 IDR/day  valid 1 Nov 2026  recorded 20 Oct 2026  replaces f1
```

The new fact has its own recorded time (20 October) and points to `f1` with
`replaces`. A replacement is one of the six fact kinds (FACT-8). The old fact
is not touched.

## 2. Addresses and the module

Alex's content lives in a **module**. The first lines of the module are:

```uniti
module alex/rental@v3
  uses uniti/item@v1
```

From [`00-form-examples.md`](../conformance/00-form-examples.md#rental). The
module has an owner (`alex`), a name (`rental`), and a version (`@v3`). It
uses another module, `uniti/item`, at one exact version (CHANGE-14).

Every concept, property, rule, and example in the module has an **address**
built as owner, module, name
([`form/02-addresses.md`](../form/02-addresses.md) §2.2, ADDRESS-1). The
concept `Rental` of this module is `alex/rental/Rental`. The address has no
version inside (ADDRESS-4,
[§2.3](../form/02-addresses.md#23-an-address-does-not-contain-a-version)).
The version is only named when one module uses another, as `@v3` above.

## 3. The concept and its properties

A **concept** is one class of entities. A **property** says something about
them. Both are described by cards
([`form/04-concepts.md`](../form/04-concepts.md) §2.1, CONCEPT-1,
CONCEPT-3). From the same module:

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

The concept card holds a label, a definition, and at least one includes and
one excludes (CONCEPT-1). The `daily_rate` property is a number with the
quantity money per duration, so its values carry a unit such as `IDR/day`
(VALUE-5, [`form/03-values.md`](../form/03-values.md) §2.3). The word
`position` is its direction: how much there is at one moment, not a change
(VALUE-17).

Then the module states which properties apply to which concept, and which are
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
belongs to the item and is not required
([`form/04-concepts.md`](../form/04-concepts.md) §2.3, CONCEPT-6,
CONCEPT-18).

## 4. A computed property: `total_due`

Alex wants to know the total due of a rental. That number can be worked out
from the facts, so the standard says it is not recorded as a fact (FACT-4,
CALC-5). It is a **computed property**
([`form/06-calculation-rules.md`](../form/06-calculation-rules.md) §2.3):

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
The helper `term` is a range from the start date up to, but not including, the
end date (CALC-26). The rule multiplies the item's daily rate by the number of
days in that range.

A computed property is asked like any other property, at a valid time `T` and
an as-of time `R` (CALC-6). This is the question in `three_night_rental`:

```uniti
  ask          r1.total_due   T: 6 Oct 2026   R: 6 Oct 2026 12:00
  result       150,000 IDR
```

The same question in `rate_rise_after_rental`, after the rate replacement from
section 1 was recorded, gives:

```uniti
  ask          r1.total_due   T: 6 Oct 2026   R: 21 Oct 2026
  result       150,000 IDR
```

The October rental is still priced with the rate valid at `T`
([`form/01-facts.md`](../form/01-facts.md) §2.5).

## 5. A constraint: `no_overlap`

A **constraint** is a yes/no rule for a concept. If an action would make it no,
the whole action is rejected
([`form/06-calculation-rules.md`](../form/06-calculation-rules.md) §2.12,
CALC-38). Alex's constraint:

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
It counts the other rentals of the same item whose term overlaps this one. The
count must be zero. The card holds a rejection message for people to read
(CALC-37).

When the constraint fails, the rejection names the constraint, its source
module and exact version, the entity, and the valid time (CALC-41). It is kept
as a rejection record, which is not a fact (CALC-42, CALC-43). In the example
`one_day_overlap`, a rental of 12 to 14 October is tried while the tent is
already booked for 10 to 13 October. The result written there is:

```uniti
  result       rejected by no_overlap, entity r2
```

## 6. Examples as proof

Every computed property needs at least one compute example, and every
constraint needs at least one accept example and one reject example (PROOF-13,
PROOF-15). An example is facts, plus one question or one action, plus the
result that must come out ([`form/08-proof.md`](../form/08-proof.md) §2.1).
There are three kinds:

| Kind | What it checks | Example in module v3 | Result written |
|---|---|---|---|
| compute | the value of a computed property at `T` and `R` | `three_night_rental`, `rate_rise_after_rental` | `150,000 IDR` for both |
| reject | the action is rejected by the named constraint | `one_day_overlap` | `rejected by no_overlap, entity r2` |
| accept | the action is accepted, and a question may follow | `adjoining_no_overlap` | `accepted`, then `100,000 IDR` |

The accept example shows that the constraint does not always reject. Here is
its action and results:

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
[`00-form-examples.md`](../conformance/00-form-examples.md#rental). The new
rental starts on the day the other ends, and the example says that no day is
used by two rentals.

What the three words mean:

- **compute**: ask a question of the facts and compare the answer;
- **accept**: try an action; it must be accepted;
- **reject**: try an action; it must be rejected by the constraint that is
  named (PROOF-32).

The result is compared exactly, unit included
([`form/08-proof.md`](../form/08-proof.md) §2.4, PROOF-5). The starting facts
of an example are taken as already recorded and are not checked; only the
action is (PROOF-30). The notation is in [Appendix
A](../appendix/A-notation.md) §2.9.

## 7. Change: from version to version

Modules change by freezing new versions. A frozen version never changes
(CHANGE-1). The kind of change between two versions is found by a machine, not
stated by the author (CHANGE-5,
[`form/07-change.md`](../form/07-change.md) §2.2).

[`15-change.md`](../conformance/15-change.md#u1-a-new-version-adds-a-property)
shows `alex/rental` at versions 1 and 2. Version 2 adds one property. Here is
the new line of version 2, and the line of its `applies to` that uses it:

```uniti
property promised_return_date : date
```

```uniti
  promised_return_date
```

The machine counts one **addition** (see
[`15-change.md`](../conformance/15-change.md#u1-a-new-version-adds-a-property)).
The example `three_night_rental` of version 1 is also in version 2, unchanged,
because every address and example of a version stays in the next one
(CHANGE-6).

A shop that uses version 1 is not affected by version 2 (CHANGE-15). The
shop's own module names its version exactly:

```uniti
module happy-camp/shop@v1
  uses alex/rental@v1
```

Copied from [`15-change.md`](../conformance/15-change.md#u2-a-user-is-bound-to-an-exact-version).
When the shop moves to version 2, its examples are run again with version 2
(PROOF-24).

**Why old facts still read the same.** Addresses do not carry a version, so
facts recorded with version 1 are still read by version 2 without being moved
or changed ([`form/07-change.md`](../form/07-change.md) §2.6). In
[`15-change.md`](../conformance/15-change.md#u2-a-user-is-bound-to-an-exact-version),
an old rental is asked for the new property:

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

The facts are still readable, and the new property is empty.

If a change does alter a result, the old example fails when it is run again.
The owner then fixes the rule or marks the old example as replaced, with a
reason; an example is never deleted (PROOF-19 to PROOF-21). The case
[`U3`](../conformance/15-change.md#u3-behavior-change) in the same file shows
this for another module.

Version 3 of `alex/rental`, used in sections 2 to 6, is in
[`00-form-examples.md`](../conformance/00-form-examples.md#rental). This tour
does not describe what changed between version 2 and version 3.

## 8. Where to go next

- [Overview](overview.md): a map of all the normative documents, and a table of
  "where do I find ...".
- [Implementing](implementing.md): for people who build software that follows
  the standard.
- [`conformance/`](../conformance/): all the worked cases. The rental cases S1
  to S4 are in [`03-rental.md`](../conformance/03-rental.md).
- [`rules.md`](../rules.md): the index of all 218 rules.
- [`form/`](../form/01-facts.md): the normative text, starting with Facts.
