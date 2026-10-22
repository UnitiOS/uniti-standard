# Calculation rules

Status: locked (v0.1.0)

> [Uniti Standard](../README.md) › Part A: form, 6 of 8
> · Previous: [Relations](05-relations.md) · Next: [Change](07-change.md)
> · [Rules CALC-n](../rules.md#calculation-rules)

**Contents**

- [1. Purpose](#1-purpose)
- [2. Definitions](#2-definitions)
  - [2.1 Three kinds of numbers](#21-three-kinds-of-numbers)
  - [2.2 Three kinds of rules](#22-three-kinds-of-rules)
  - [2.3 Computed property](#23-computed-property)
  - [2.4 How to write a rule](#24-how-to-write-a-rule)
  - [2.5 Operation list: core and library](#25-operation-list-core-and-library)
  - [2.6 Intermediate values](#26-intermediate-values)
  - [2.7 Time in calculation](#27-time-in-calculation)
  - [2.8 Numbers in calculation](#28-numbers-in-calculation)
  - [2.9 Empty and not computable](#29-empty-and-not-computable)
  - [2.10 Direction in calculation](#210-direction-in-calculation)
  - [2.11 Open computed properties and contributions](#211-open-computed-properties-and-contributions)
  - [2.12 Constraint](#212-constraint)
  - [2.13 Rejection record](#213-rejection-record)
  - [2.14 Computed value](#214-computed-value)
  - [2.15 Projection](#215-projection)
  - [2.16 Results reported outside](#216-results-reported-outside)
  - [2.17 What calculation rules cannot do](#217-what-calculation-rules-cannot-do)
- [3. Rules](#3-rules)
- [4. Examples](#4-examples)
- [5. Not examples](#5-not-examples)
- [6. Reasons](#6-reasons)
- [7. Outside standards](#7-outside-standards)
- [8. Open questions](#8-open-questions)

## 1. Purpose

An organization needs numbers that are not recorded directly: balance, stock,
total due, cost of goods, tax. The form of calculation rules sets how those
numbers are derived from facts, so that the result is the same in any
implementation, can be traced to the facts it came from, can be read at two
times like a fact, and can be composed together by modules from different
authors.

## 2. Definitions

### 2.1 Three kinds of numbers

Every number or value that is not recorded directly belongs to one of three
kinds ([`decisions/0025`](../decisions/0025-three-kinds-of-numbers.md)):

| Kind | Trait | Examples | Where it lives |
|---|---|---|---|
| **Derived** | From the same facts, rules, and times, the result is always the same | balance, stock, cost of goods, depreciation, tax | Calculation rule. The result is not a fact |
| **Decided** | A choice is taken by someone | which invoice this payment settles; invoice number; special price | Fact, recorded through an action |
| **Estimated** | The result of a model, a guess, or a search for a solution | sales forecast, risk score, best schedule | Fact, recorded through an action with a machine or AI actor |

This document governs only **derived** numbers.

The border between derived and decided: **a fixed policy is derived, a choice
per event is decided.** "A payment always settles the oldest installment
first" is derived and is written as a calculation rule. "The customer chooses
to pay invoice F-12" is decided and is recorded as a fact.

### 2.2 Three kinds of rules

Calculation rules are written in a module, and every rule has an address
([`02-addresses.md`](02-addresses.md)). There are three kinds:

| Kind | Meaning | Result |
|---|---|---|
| **Computed property** | A property whose value is always calculated and never recorded | One of the seven value types ([`03-values.md`](03-values.md) §2.1) |
| **Helper** | An intermediate result used by other rules | Any value, including an intermediate value (§2.6) |
| **Constraint** | A yes/no rule checked at every action (§2.12) | Yes or no |

There is also the **contribution**: a part of someone else's open computed
property, written in the module of the contributor (§2.11).

### 2.3 Computed property

A computed property is **read like other properties**. The question "what is
the total due of rental R1?" is asked in the same way as "who is the customer
of rental R1?", at valid time *T* and as of *R*. The difference is that the
value is always calculated from its rule, and may never be recorded as a fact
([`01-facts.md`](01-facts.md), FACT-4).

A computed property uses the same **property card**
([`04-concepts.md`](04-concepts.md) §2.2), with three more parts:

| Card part | Meaning | Required? |
|---|---|---|
| **Rule** | The expression that calculates its value (§2.4) | required |
| **Parameter** | A value given by the asker, for example a period | optional |
| **Open or closed** | Whether other modules may contribute (§2.11) | required |

A computed property **applies to exactly one concept**, together with its
child concepts. Like other properties, it may be written by anyone in their
own module for a concept owned by anyone, and applies only to organizations
that install that module ([`04-concepts.md`](04-concepts.md) §2.3).

Because a computed property is read like a property, **a computation on top
of a computation** works by itself: the rental total uses the total due, which
uses the rate.

### 2.4 How to write a rule

A rule is written as an **expression** that uses only the operations in §2.5.
Example:

```
computed Rental.total_due : number (money, increase), closed:
  this.item.daily_rate × span(this.term, day)

helper Rental.term : range:
  range(this.start_date, this.end_date)

constraint Rental.no_overlap:
  count(all(Rental, s: s ≠ this and s.item = this.item
                          and exists(overlap(s.term, this.term)))) = 0
```

- `Rental.total_due` is a short way of writing the property
  `alex/rental/total_due` that applies to the concept `alex/rental/Rental`.
  The short name is looked up in that module itself and in the modules it
  uses.
- In the parentheses are written the value type of the result, then the
  quantity and the direction if the result is a number.
- A computation with a parameter is written `computed Employee.salary(month) : …`.

The notation in this document is the **reference notation**, used in the
standard, in the examples, and in the tests. What is standardized is the
operations and their meaning. Another storage format, for example YAML or
RDF, may be used if the meaning is exactly the same. How to write it is
detailed in [`appendix/A-notation.md`](../appendix/A-notation.md).

### 2.5 Operation list: core and library

The operation list below is the **core operations**: fixed, closed, and the
same in all implementations
([`decisions/0026`](../decisions/0026-layered-operations.md),
[`decisions/0045`](../decisions/0045-core-operations-and-calculation-library.md)).
Operations are built from blocks, not from business patterns, and are divided
into three **levels**.

An operation enters the core only if it meets both:

- it cannot be written from other core operations at the same level; and
- it does not contain a choice of method that other domains might take
  differently.

Other ways of calculating, for example average, median, how to round, or how
to divide without a remainder, are content. They are written in the
**calculation library**, at the end of this section.

**Level 1: basic**

| Group | Operation | Meaning |
|---|---|---|
| **Get** | `this` | The entity being asked about |
| | `x.s` | The value of property `s` of entity `x` at *T*. If there is no value, the result is **empty** (§2.9). For a property with many values, the result is a collection, which may have no members |
| | `x.a.b` | Follow a reference: the value of property `b` of the entity referred to by `x.a` |
| | `T` | The valid time being asked about (§2.7) |
| | `unit_of(n)` | The unit of a number, as a choice from the code list `uniti/unit/Unit` ([`03-values.md`](03-values.md) §2.3). A unit that is not one code without a power, for example `IDR/day` or `m²`, is not computable because of unit mismatch. A number without a unit gives empty |
| | fixed value | A number, text, date, choice, or duration written directly: `10,000,000 IDR`, `manager`, `1 month` |
| | `contributions` | Only in the rule of an open computed property: the collection of the results of all contributions to `this`, from the installed modules (§2.11). This collection has no order |
| **Collect** | `all(K, x: condition)` | All entities that belong to concept `K` or its child concepts at *T*, and meet the condition. The condition may be omitted |
| | `single(k)` | The only member of collection `k`. If it does not have exactly one member, it is not computable |
| | `each(k, x: u)` | A new collection: `u` for every member `x` |
| | `each_merged(k, x: u)` | Like `each`, for a `u` that is a collection; the results are joined into one collection |
| | `group(k, by: x: u)` | A collection of groups. Every group is a record with `key` and `members` |
| **Summarize** | `sum(k, x: u)` | The sum of `u` for all members. Empty collection: 0 |
| | `count(k)` | The number of members. Empty collection: 0 |
| | `min(k, x: u)`, `max(k, x: u)` | The smallest or largest value. Also allowed for two values: `min(a, b)` |
| | `all_match(k, x: condition)` | Yes if the condition is yes for every member. Empty collection: yes. All members are always calculated, unlike `and` |
| | `any_match(k, x: condition)` | Yes if the condition is yes for at least one member. Empty collection: no. All members are always calculated, unlike `or` |
| **Calculate** | `+`, `−`, `×`, `÷` | With exact numbers (§2.8) |
| | `power(a, n)` | `a` to the power of `n`, for an integer `n` |
| | `floor_multiple(n, of: k)` | The largest multiple of `k` that is not more than `n`: `floor_multiple(−4.8 kg, of: 0.5 kg)` = −5 kg. `k` is more than zero and has the same unit as `n`. All ways of rounding are written from this operation |
| **Time** | `range(a, b)` | The range from `a` up to **before** `b` (§2.7). If `b` is before `a`, it is not computable because of reversed time |
| | `difference(a, b, unit)` | The duration from `a` to `b`, as a number with a duration unit |
| | `a + duration`, `a − duration` | A date or instant that is shifted |
| | `span(r, unit)` | The length of a range, as a number with a duration unit |
| | `overlap(r1, r2)` | The part two ranges have in common. If they do not overlap, empty |
| | `split(r, step: …)` | Range `r` cut into small ranges in sequence |
| | `in` | `t in r`: time `t` is in range `r`. `x in k`: `x` is a member of collection `k` |
| | `at(t, u)` | Expression `u` is read at valid time `t`, not at *T* |
| | `history(x.s, in: r)` | The values of the recorded property `x.s` during range `r`, each with its range of validity, cut to `r`. If `x` is empty, the result is empty. For a property with many values, the collection has no order |
| **Choose** | `if … then … else …` | Only the chosen branch is calculated |
| | `=`, `≠`, `<`, `≤`, `>`, `≥` | Comparison. Two records are equal if the names of their parts are the same and every part is equal. Two ordered collections are equal if their members are equal, in the same order. If one of the collections has no order, order is not looked at: the two are equal if every member appears the same number of times in both |
| | `and`, `or`, `not` | Read from the left. If the left side already decides the result, the right side is not calculated |
| | `exists(u)` | Yes if `u` is not empty |
| | `let name = u` | Gives a name to an intermediate result, to be used in the following expression. `u` is calculated only if the name is used |
| | `not_computable(description)` | States that the result is not computable (§2.9) |
| **Unit** | `convert(n, to: unit)` | Converts to a unit with a fixed factor, for example kg to g. Currency cannot be converted in the core, because the exchange rate is a fact: the result is not computable because of unit mismatch |
| **Intermediate value** | `{a: …, b: …}`, `r.a`, `r with a = …` | Creates a record, reads its part, creates a copy with one part replaced |
| | `[…]`, `append(k, x)` | Creates an ordered collection, adds one member at the end |
| | `r.start`, `r.end` | The start of a range, and the first time after that range |
| **Constraint** | `before_action(u)` | Expression `u` is read as it was before the action being checked. Only in constraints |
| | `this_action.actor`, `this_action.approver` | The provenance of the action being checked. Only in constraints |

**Level 2: order and fold**

| Operation | Meaning |
|---|---|
| `fold(k, order_by: x: u, initial: a, step: (state, x): …)` | Start from state `a`, then for every member in order, calculate the next state. The result is the last state |

With `fold`, a rule can calculate a running balance, FIFO, a moving average,
sequential allocation, and a cap that is used up little by little. `median`
and `percentile` in the calculation library are also written with `fold`.

**Level 3: bounded recursion**

A computed property or helper may use itself, for **another entity**, at the
same *T* and *R*, with the same parameters. An example is the standard cost of
an item that sums the standard costs of its components. Two rules that use
each other also count as recursion.

If a calculation returns to the same entity before it is finished, the result
is **not computable, because of a cycle**, together with its chain ("bicycle →
wheel → bicycle"). Because the number of entities at (*T*, *R*) is finite,
recursion like this always finishes.

The **level of a rule** is calculated by the machine from the operations it
uses, including operations in other rules that it reads. An implementation
states the levels it supports ([`08-proof.md`](08-proof.md) §2.9).

**Calculation library**

The calculation library is a helper without a concept in a vocabulary module,
written with the core only
([`decisions/0045`](../decisions/0045-core-operations-and-calculation-library.md)).
Like other content, it has an address, a version, and examples. Its user
names the library module with an exact version (CALC-17), then calls its
helpers by name.

Anyone may write a library in their own module. A new way of calculating, for
example rounding to even, is added to a library without changing the form.

The first calculation library, `uniti/calc`:

| Helper | Meaning |
|---|---|
| `average(k)` | Sum divided by count |
| `median(k)` | The middle value. If the count is even, the average of the two middle values |
| `percentile(k, p)` | Nearest rank: the member at position ⌈p × count⌉ after sorting, with 0 < p ≤ 1 |
| `round(n, to, mode)` | Rounds to a multiple of `to`. Mode `nearest` (half away from zero), `up` (to the larger number), or `down` (to the smaller), also for negative numbers |
| `allocate(total, list, to, remainder)` | Divides a total by weight, with the sum of the shares exactly equal to the total (§2.8) |
| `convert_money(n, to, rate)` | Converts currency with an exchange rate from facts. The rate is read only if the currencies differ |

Its content, together with examples, is in
[`content/calc.md`](../content/calc.md).

An implementation may calculate the library helpers in its own way, as long
as the result is exactly the same, including the reason kind (CALC-19). The
level of a rule that uses them is calculated from the operations inside that
helper (CALC-11). `median` and `percentile` use `fold`, so they are level 2.

### 2.6 Intermediate values

Inside a rule, and as the result of a helper, values that are not value types
may be used:

| Intermediate value | Examples |
|---|---|
| **Collection** | the result of `all`, `each`, `split`, `history`; `[…]` |
| **Record** | `{amount: 10, price: 100,000 IDR}`; every group from `group` |
| **Range** | `range(this.start_date, this.end_date)` |

An intermediate value is **never** the value of a computed property and is
never recorded. The rental term, for example, is recorded as two date
properties, and its range is formed in the rule, like `Rental.term` in §2.4.

**Order of a collection.** A collection from `all` and `group` has no order,
so a `fold` over it must name `order_by`. A collection from `split`,
`history` of a property with one value, `[…]`, and `append` is already
ordered, and `order_by` may be omitted. `history` of a property with many
values has no order. A summary such as `sum` does not depend on order.

**Tie-breaker.** If two members are equal by `order_by`, their order is
decided by, one after the other:

1. the valid time of the type fact of that entity;
2. the recorded time of that fact;
3. the identifier of that entity, compared as text, character by character
   by Unicode number.

If an entity has several type facts that are valid at *T*, the one used is
the one with the earliest valid time, then the one recorded earliest, whatever
concept is being asked about. A customer who was a supplier first is ordered
by the type fact of its Supplier.

In this way FIFO and sequential allocation give the same result in any
implementation, including for two events on the same date.

**Entity as key.** An `order_by` key may be an entity, and those entities are
ordered by the tie-breaker. For example `order_by: d: d.room` for records that
name a room, before a building rental is divided among those rooms.

An entity that has no type fact valid at *T*, for example one reached through
a reference whose type fact is valid only later, has no place in this order.
If its place is needed, the result is not computable because of undefined
order.

**Undefined order.** The tie-breaker exists only for entities. Members that
are not entities, for example groups from `group` or the results of
`contributions`, in a collection with no order, have no definite order. If
the order is needed, that is, `fold` with members that are equal by
`order_by`, the result is not computable because of undefined order. The
exception is members that are exactly the same, for example two numbers 7:
their order does not change the result, so no tie-breaker is needed.

### 2.7 Time in calculation

**Two times.** The result of a computed property is always asked at (*T*, *R*):

- every `x.s` is read at *T*, according to the facts known as of *R*
  ([`01-facts.md`](01-facts.md) §2.5);
- `at(t, u)` replaces *T* for expression `u`. If `t` is a range, it is read at
  its start;
- *R* **never changes** inside a rule.

**Without "now".** A rule cannot read the clock or today's date. If what is
asked is today's state, the asker gives *T* = today. A rule may use `T` as a
value, for example to sum the depreciation of the months that have started at
*T*.

**Entities that exist at T.** `all(K, …)` takes only entities whose type fact
is valid at *T*. For that reason a fact about an event should be valid from
the time of the event: an expense on 9 October is not yet counted in the
balance as of 6 October, without a date filter. Detailed guidelines for each
concept are in the vocabulary.

The same holds for a computed property: if it is asked for an entity that at
*T* does not yet or no longer belongs to its concept, the result is **empty**,
like a property without a fact. The total of a rental on a day before that
rental is recorded as valid, for example, is empty.

**Half-open range.** `range(a, b)` holds `a` up to **before** `b`. A rental of
10–13 October and a rental of 13–15 October do not overlap, and no day is
counted twice.

**Time units.**

- `span` and `difference` in days, hours, minutes, and seconds are calculated
  exactly.
- In months or years, `difference(a, b, month)` is the largest *n* such that
  `a + n months` does not go past `b`. 31 January to 28 February is 1 month;
  31 January to 27 February is 0 months. If `b` is before `a`,
  `difference(a, b, month)` = −`difference(b, a, month)`. A year equals
  12 months.
- `date + n months` falls on the same day of the month *n* months later,
  directly from that date. If that date does not exist, it falls on the last
  day of that month: 31 January + 1 month = 28 or 29 February, and
  31 January + 2 months = 31 March.
- Months and years are **for dates only**. An instant is not shifted by months
  or years, and the difference of two instants is not calculated in months or
  years.
- A date is shifted only by whole days, weeks, months, or years.
  `date + 12 hours` has no meaning.
- Otherwise the result is not computable because of unit mismatch.
- The pieces of `split(r, step: s)` are calculated from the start of `r`:
  piece *k* starts at the start of `r` + *k* × `s`, not from the previous
  piece. The last piece stops at the end of `r`, so it can be shorter. A
  monthly split from 31 January starts on 31 January, 28 February, and
  31 March.
- A date that is compared with or joined to an instant is read as the start
  of that day according to the organization's default time zone
  ([`03-values.md`](03-values.md), VALUE-10).

**Period.** A rule may receive a range as a parameter, for example
`revenue(period)`. October revenue is the sum of the sales whose date is in
the range from 1 October up to before 1 November.

**`at` and `history`.**

- `at` may be used for recorded properties as well as computed properties:
  `at(h.date, this.contract.hourly_rate)`.
- `history` is only for recorded properties. The history of a computed
  property is written with `split` and `at`.

### 2.8 Numbers in calculation

**Exact fraction.** Inside a rule, numbers are calculated as **exact
fractions**. 1,000,000 ÷ 3 is kept as one third of a million, not as
333,333.33. As a result the order of summing never changes the result, and no
rounding remainder appears silently.

**The result must terminate.** The value of a computed property is a number
([`03-values.md`](03-values.md) §2.2), so it must be writable as a
terminating decimal. If the final result is a non-terminating fraction, for
example 135,000,000 ÷ 31, the rule must round. Without that, the result is
not computable because it needs rounding. The machine reports a rule that
uses `÷` without rounding at the end, before the rule is frozen.

**Where and how to round is content.** Rounding every line and then summing
can differ from summing and then rounding. Both are valid, and the choice
**must be written** in the rule. The way of rounding, for example half away
from zero or to even, is also content. It is written in the calculation
library, from `floor_multiple`.

**Dividing without losing the remainder.** Dividing 10,000,000 into three
shares by rounding every share can give a sum of 9,999,999. A way of dividing
whose sum is exactly equal to the total, together with the receiver of the
remainder, is also content.

The first calculation library provides `allocate`: the shares are rounded
down, then the remainder is given to the member with the largest fraction, to
the first member, or to the last member. A building rental of 10,000,000
divided by areas of 120, 80, and 100 m² becomes 4,000,000, 2,666,667, and
3,333,333. The sum is exactly 10,000,000.

**Units are calculated too.**

| Operation | Condition and resulting unit |
|---|---|
| `+`, `−`, comparison | Both sides must have the same unit. 1 kg + 500 g is not computable, unless converted first |
| `×`, `÷`, `power` | Units are combined: cm × cm × cm = cm³; cm³ ÷ (cm³/kg) = kg. A code may reach the power 3 or −3 at most ([`appendix/A-notation.md`](../appendix/A-notation.md) §2.4); a result with a higher power, for example cm⁴, is not computable because of unit mismatch |
| Result of a computed property | The unit must match the quantity on its property card |

A daily rate, for example, has the unit IDR/day, so rate × `span(term, day)`
has the unit IDR. If a pure number is needed, the duration is divided by its
unit: `span(term, day) ÷ 1 day` = 3.

The same units cancel each other: IDR/day × day = IDR. Different units do
**not** cancel each other, even when the quantity is the same. IDR/day × hour
has the unit IDR·hour/day, not IDR. A unit like that has no quantity, so it
does not match a property card whose quantity is money, and the rule is
written wrongly (CALC-24). The rule author states the duration in days.

A zero without a unit, whether from an empty collection or written directly
like `else 0`, takes the unit of the other numbers used with it. If a zero
without a unit becomes the final result of a computed property that has a
quantity, its unit cannot be determined, so the result is not computable
because of unit mismatch. An example is `sum` over an empty collection for a
total in money. The rule author writes `0 IDR` if the collection can be
empty, and the machine reports a rule like that before it is frozen.

### 2.9 Empty and not computable

Every expression produces one of three things:

| Result | Meaning |
|---|---|
| **Value** | An ordinary result |
| **Empty** | There is no value: a property with one value that has no fact at *T*, an empty reference, or two ranges that do not overlap |
| **Not computable** | The result cannot be determined, together with the reason |

**Empty** may be read and checked with `exists(u)`. An empty that is used in
a calculation, for example summed or compared, becomes not computable. A
computed property whose result is empty is read like a property without a
fact.

A property with many values, whether recorded or computed, produces a
collection of values of its value type. Without values, the result is a
collection with no members, **not** empty. For that reason `exists(x.phone)`
is always yes; what is used to check is `count(x.phone) > 0`. A computed
property for an entity that at *T* does not belong to its concept stays empty
(§2.7, CALC-54).

**Not computable** never silently becomes 0 or empty. It carries a **reason
kind** from a closed list, a description in human language, and its location:
rule, entity, and *T*.

| Reason kind | Example |
|---|---|
| **empty value** | The price of an item is used, but the item has no price yet |
| **division by zero** | Price per unit, for a unit count of zero |
| **not single** | `single` finds two exchange rates, or finds no exchange rate at all |
| **empty collection** | `min` or `max` over an empty collection |
| **unit mismatch** | 10 USD + 5,000 IDR; an instant shifted by 1 month |
| **needs rounding** | The final result is a non-terminating fraction |
| **direction violated** | A negative result for a property whose direction is no direction ([`03-values.md`](03-values.md), VALUE-18) |
| **cycle** | Recursion returns to the same entity |
| **reversed time** | `range(a, b)` with `b` before `a` |
| **undefined order** | `fold` over groups that are equal by `order_by` (§2.6) |
| **redacted** **[provisional]** | The value used has already been redacted ([`01-facts.md`](01-facts.md) §2.6) |
| **declared by rule** | The rule itself uses `not_computable`, for example "stock not sufficient". This includes helpers in the calculation library, for example "median of an empty collection" |

**It spreads.** If part of an expression is not computable, the whole result
is not computable, with the reason of that part. What is not calculated does
not spread it: the branch of an `if` that is not chosen, the right side of an
`and` or `or` that is not needed, a `let` whose name is not used, and a helper
argument that is not used inside that helper.

**The reason of the first part.** If several parts are not computable for
different reasons, the reason reported is that of the first part in
calculation order: the written order from the left, and the members of a
collection in their order, or in tie-breaker order if the collection has no
order (§2.6). A collection that has no order and whose members are not
entities, for example the result of `contributions`, has no calculation
order. All of its members are calculated, and if several are not computable,
the reason kind reported is the topmost one in the table above. In this way
two implementations report the same reason.

Example: September revenue in rupiah is not computable, reason kind "not
single", description "the exchange rate from USD to IDR on 30 September does
not exist yet".

### 2.10 Direction in calculation

Every number carries a direction from its property card
([`03-values.md`](03-values.md) §2.3). The machine uses it to catch sign
errors before a rule is frozen:

| The machine reports | Example |
|---|---|
| Numbers with direction **increase** and **decrease** summed with `+` | `sum of receipts + sum of expenses` for a balance |
| Numbers with **no direction** summed or subtracted without choosing by the property that states the direction | `sum(all(Movement), m: m.amount)`, although some movements are incoming and some are outgoing |

A direction report is a **warning**: a rule that is correct but unusual may
still be frozen, with a reason written by its owner. Apart from that warning,
a negative result for a computed property whose direction is no direction is
always not computable.

### 2.11 Open computed properties and contributions

The owner of a computed property declares the computation **open** or
**closed**, like a choice list ([`03-values.md`](03-values.md) §2.6):

| Computation | Meaning |
|---|---|
| **Closed** | Only the rule of its owner decides the result |
| **Open** | Anyone may add a **contribution** in their own module |

Example: the vocabulary has `Item.available`, open. The purchasing module
contributes items received, the sales module contributes items sold, and the
rental module of Alex contributes items being rented:

```
computed uniti/item/Item.available : number (position), open:
  sum(contributions)

contribution alex/rental/being_rented to Item.available:
  − sum(all(Rental, s: s.item = this and T in s.term), s: s.amount)
```

- The rule of the owner reads the contributions with the `contributions`
  operation, and states how the contributions are combined. The way of
  combining must not depend on order: `sum`, `min`, `max`, `all_match`, or
  `any_match`. The owner may also write its own part outside the
  contributions.
- Every contribution must produce the same value type, quantity, and
  direction as its computation.
- A contribution applies only to organizations that install the module of the
  contributor. An organization that does not install Alex's module gets stock
  without the rental deduction.
- A closed computation may be opened in the next version. An open computation
  may not be closed, because the existing contributions would lose their place
  ([`04-concepts.md`](04-concepts.md) §2.9).

A contribution cannot prevent one event being recorded twice in two different
modules: that event is still counted twice. That is a data problem, not a
form problem.

### 2.12 Constraint

A **constraint** is a yes/no rule written for a concept, for example "stock
must not be negative", "an item that is being rented cannot be rented out
again", or "a purchase above 10 million needs the approval of a manager". A
constraint uses a card:

| Card part | Meaning | Required? |
|---|---|---|
| **Address**, **label**, **definition** | Like the property card | required |
| **Applies to** | One concept, together with its child concepts | required |
| **Rule** | A yes/no expression | required |
| **Rejection message** | A sentence for humans if the constraint is not met | required |

A constraint is written in a module and applies to organizations that install
that module. Anyone may write a constraint for a concept owned by anyone.

**One action at a time.** Actions are checked and recorded one at a time, in
the order in which they are recorded, also when two actions have the same
recorded time. *Before the action* means the facts recorded before it; *after
the action* means those facts plus the facts of the action. For example, when
two cashiers rent out the last tent at the same moment, the action recorded
first is checked first, and the second is checked against it and rejected
([`decisions/0057`](../decisions/0057-closure-before-lock.md)).

**Checked per action.** Like required properties
([`04-concepts.md`](04-concepts.md) §2.7), a constraint is checked after all
the facts in an action are taken into account:

1. A constraint that reads the action (see *Reading the action* below) is
   read for every entity that the action touches directly, at every time that
   the action touches ([`04-concepts.md`](04-concepts.md) §2.7): the valid
   time of its facts, plus the valid time of the target of every correction,
   retraction, and redaction.
2. Other constraints are read for every entity of their concept, at every time
   that the action touches and at every later valid time of a fact. In this
   way a backdated correction is also checked at the events after it, for
   example a sale that makes stock negative because an earlier receipt is
   corrected.
3. The action is **rejected as a whole** if a constraint is no after the
   action, while it was yes or did not exist before the action. A constraint
   that reads the action has no value before the action, so it is taken as
   not existing.
4. A constraint that was already no before the action, for example because the
   constraint was only just installed, does not block the action. That old
   violation is reported separately.
5. A constraint that is not computable is treated as not met, with its reason.
   A constraint whose result is empty is treated the same, with the reason
   kind empty value.

At every one of those times, a constraint is read only for entities that at
that time belong to its concept, like a computed property (CALC-54).

An entity and a time whose result is the same before and after the action
never reject, so an implementation may skip them if it can prove the result is
the same
([`decisions/0047`](../decisions/0047-constraints-and-backdated-changes.md)).

Between those times the constraint is not read. A constraint for the future,
for example stock for a rental that only starts next week, is written by
checking every day in its range:

```
constraint Rental.enough_stock:
  all_match(split(this.term, step: 1 day),
            h: at(h, this.item.available) ≥ 0)
```

**Reading the action.** Only a constraint may use `before_action(…)`,
`this_action.actor`, and `this_action.approver`. With them, status transitions
and permissions are written simply as constraints. A constraint like this is
about the action itself, so it is read only for entities touched by the action
(step 1):

```
constraint Purchase.approved_if_large:
  this.total ≤ 10,000,000 IDR
  or (exists(this_action.approver)
      and this_action.approver ≠ this_action.actor
      and any_match(all(Contract, k: k.employee = this_action.approver),
                    k: k.position = manager))
```

**Rejection.** Every rejection names:

| Part | Example |
|---|---|
| The constraint that failed, with its address | `alex/rental/enough_stock` |
| Its source module, with the exact version | `alex/rental@v3` |
| The entity and valid time where the constraint failed | rental R2, 15 October |
| The rejection message, and the reason if the constraint is not computable | "The stock of this item is not sufficient for part of the rental term." |

In this way the rejected party knows exactly why, and whose module rejected
it.

### 2.13 Rejection record

Every action that is rejected, by a constraint or by a form rule such as a
required property, is recorded as a **rejection record**:

- the action that was tried, together with its facts;
- the actor and the approver, and when it was tried;
- every rejection, with the parts in §2.12.

A rejection record is **not a fact**. It is never read when facts are read,
and never affects a computed value. It can be read back: for audit, for a
business owner who wants to know why a transaction was rejected, and for an AI
that learns from its mistakes.

### 2.14 Computed value

Every computed value names where it came from
([`decisions/0008`](../decisions/0008-computed-values.md)):

| Part | Meaning |
|---|---|
| **Computed property** and **entity** | What was calculated, for which entity |
| **Parameter** | If there is one |
| ***T*** and ***R*** | At which two times it was calculated |
| **Module set** | The exact version of the module of the rule, the modules it uses, and the contributor modules that are installed |
| **Result** | A value, empty, or not computable together with the reason |
| **Trace** | The facts that formed it. It does not have to be stored, but must be possible to show on request |

From the same facts, module set, parameters, *T*, and *R*, the result is
always the same. An implementation may calculate in any way, for example only
on the days when the balance changes, as long as the result is exactly the
same.

### 2.15 Projection

A **projection** is a computed value that is stored to speed up reading. In
addition to the parts in §2.14, a projection names the **last fact** that has
been taken into account.

- A projection may be discarded and rebuilt at any time.
- If a projection differs from a recalculation from the facts, the one that is
  correct is the **calculation from the facts**.
- The reader must be able to know whether the result they see is current, for
  example "calculated as of 09:15; there are 3 new facts since then".
- How to store it and when to update it is left to the implementation.

A projection for an *R* that has already passed is never stale, because the
facts known as of that *R* will not change anymore. Only projections for the
latest state need to be updated. The exception is redaction **[provisional]**:
a projection that uses a value that was later redacted must be discarded.

### 2.16 Results reported outside

The tax report of October is sent with the number 12,000,000. Later there is a
correction of a fact, and the recalculation becomes 12,500,000. The number that
was already sent must still be remembered.

The computed value is still not a fact. What is recorded as a fact is **the
act of reporting it**, with **the report as its subject**:

| Subject | Property | Value |
|---|---|---|
| report L-10 | reported number | 12,000,000 IDR |
| report L-10 | sent | 15 November, at 10:00 WIB |
| report L-10 | calculated from | property `monthly_tax`, period October, *T* 31 October, *R* 15 November |

This fact is about the report, not about the tax. The difference between what
was reported and the current calculation can always be found. Properties for a
report like this are content, and are provided in the vocabulary.

### 2.17 What calculation rules cannot do

Calculation rules **cannot**:

- record, change, or retract facts;
- read "now", random numbers, or anything from outside the facts and rules;
- read facts as of another *R*;
- use content from a module that they do not name with an exact version.

For that reason every rule can be checked, compared between versions, and run
again by anyone.

## 3. Rules

**Kinds**

- **CALC-1.** A calculation rule MUST produce only derived numbers. Decided
  and estimated numbers MUST be recorded as facts through an action.
- **CALC-2.** An action that records an estimate SHOULD state the confidence
  level.

**Kinds of rules**

- **CALC-3.** Every calculation rule MUST be a computed property, helper,
  constraint, or contribution, and MUST have an address.
- **CALC-4.** A computed property MUST have a property card, exactly one rule,
  and a declaration of open or closed. A computed property MUST apply to
  exactly one concept.
- **CALC-5.** The value of a computed property MUST NOT be stated as a fact.
- **CALC-6.** A computed property MUST be readable in the same way as a
  recorded property, at (*T*, *R*).
- **CALC-7.** A helper MUST NOT be read as a property. A helper MAY be used
  only by rules.
- **CALC-8.** The value of a computed property MUST be one of the seven value
  types, according to its property card. An intermediate value MUST NOT be the
  value of a computed property. A computed property with many values MUST
  produce a collection of values of that type, and without values MUST produce
  a collection with no members, not empty, except for an entity that does not
  belong to its concept (CALC-54).

**Operations and levels**

- **CALC-9.** A rule MUST use only the core operations in §2.5 and other
  calculation rules, including helpers in the calculation library.
- **CALC-10.** The core operations MUST NOT be added to by content. Content
  adds ways of calculating through the calculation library.
- **CALC-11.** The level of a rule MUST be calculated by the machine from the
  operations it uses, including operations in other rules that it reads.
- **CALC-12.** A rule that uses itself, directly or through other rules, MUST
  do so only for another entity, at the same *T* and *R*, with the same
  parameters. A helper without a concept MUST NOT use itself.
- **CALC-13.** Recursion that returns to the same entity before it is finished
  MUST produce not computable because of a cycle, together with its chain.

**Certainty**

- **CALC-14.** From the same facts, module set, parameters, *T*, and *R*, the
  result of a rule MUST always be the same.
- **CALC-15.** A rule MUST NOT read any time other than *T*, a time derived
  from *T* or from facts, and a time written in the rule.
- **CALC-16.** A rule MUST NOT read facts as of another *R*, and MUST NOT
  record or change facts.
- **CALC-17.** A rule MUST use only content from its own module and from the
  modules it uses with an exact version.
- **CALC-18.** `fold` over a collection with no order MUST name `order_by`. An
  `order_by` key that is an entity MUST be ordered with the tie-breaker in
  §2.6, and so are members that are equal by `order_by`. If those equal
  members are not entities and are not exactly the same, the result MUST be
  not computable because of undefined order.
- **CALC-19.** An implementation MAY calculate in any way, as long as the
  result is exactly the same as the result according to this document.

**Numbers and units**

- **CALC-20.** Inside a rule, numbers MUST be calculated as exact fractions.
- **CALC-21.** The value of a computed property that is a number MUST be
  writable as a terminating decimal. If it is not, the result MUST be not
  computable because it needs rounding.
- **CALC-22.** *Revoked
  ([`decisions/0045`](../decisions/0045-core-operations-and-calculation-library.md)).
  The way of rounding is now content of the calculation library.*
- **CALC-23.** *Revoked
  ([`decisions/0045`](../decisions/0045-core-operations-and-calculation-library.md)).
  Dividing without a remainder is now content of the calculation library.*
- **CALC-24.** Addition, subtraction, and comparison MUST be only for numbers
  with the same unit. The unit of the result of a computed property MUST match
  the quantity on its property card. Different units MUST NOT be taken to
  cancel each other, even when the quantity is the same.
- **CALC-25.** An exchange rate MUST be taken from facts.
- **CALC-50.** *Revoked
  ([`decisions/0045`](../decisions/0045-core-operations-and-calculation-library.md)).
  `percentile` is now content of the calculation library.*
- **CALC-55.** If the result of a computed property that has a quantity is a
  zero without a unit, the result MUST be not computable because of unit
  mismatch. The machine SHOULD report a rule that can produce a zero without a
  unit before the rule is frozen.
- **CALC-56.** `floor_multiple(n, of: k)` MUST produce the largest multiple of
  `k` that is not more than `n`. `k` MUST be more than zero. If the units of
  `n` and `k` differ, the result MUST be not computable because of unit
  mismatch.

**Time**

- **CALC-26.** A range MUST be read as half open: from its start up to before
  its end.
- **CALC-27.** A fact about an event SHOULD be valid from the time of the
  event.
- **CALC-53.** Months and years MUST be used only to shift a date and for the
  difference of two dates. A date MUST be shifted only by whole days, weeks,
  months, or years. Otherwise, the result MUST be not computable because of
  unit mismatch.
- **CALC-54.** A computed property that is asked for an entity that at *T* does
  not belong to its concept MUST produce empty.

**Empty and not computable**

- **CALC-28.** A result that is not computable MUST name one reason kind from
  §2.9, a description in human language, and its location.
- **CALC-29.** A result that is not computable MUST NOT be replaced with 0 or
  empty.
- **CALC-30.** If part of an expression that is calculated is not computable,
  the whole expression MUST be not computable, with the reason of that part.
- **CALC-51.** `let` MUST be calculated only if its name is used, and a helper
  argument MUST be calculated only if it is used inside that helper. A part
  that is not calculated MUST NOT make the result not computable.
- **CALC-52.** If several parts are not computable, the reason reported MUST be
  the reason of the first part in calculation order in §2.9. For a collection
  with no order whose members are not entities, the reason kind reported MUST
  be the topmost one in the table in §2.9.

**Direction**

- **CALC-31.** The machine MUST report a mixing of directions according to
  §2.10 before a rule is frozen. A rule that is reported SHOULD be corrected,
  or given a written reason by its owner.

**Open and contributions**

- **CALC-32.** A contribution MUST NOT be added to a closed computation.
- **CALC-33.** A contribution MUST produce the same value type, quantity, and
  direction as the computation it contributes to.
- **CALC-34.** The way of combining contributions MUST be one of: `sum`,
  `min`, `max`, `all_match`, `any_match`.
- **CALC-35.** A contribution MUST apply only to organizations that install
  the module of its contributor.
- **CALC-36.** An open computation MUST NOT be closed.
- **CALC-49.** `contributions` MUST NOT be used outside the rule of an open
  computed property.

**Constraints**

- **CALC-37.** A constraint MUST have a card with an address, a label, a
  definition, the one concept it applies to, a yes/no rule, and a rejection
  message.
- **CALC-38.** A constraint MUST be checked per action, for the entities and at
  the times in §2.12 steps 1 and 2. An action that makes a constraint no,
  while it was yes or did not exist before, MUST be rejected as a whole.
- **CALC-39.** A constraint that is not computable, or whose result is empty,
  MUST be treated as not met.
- **CALC-40.** `before_action`, `this_action.actor`, and
  `this_action.approver` MUST NOT be used outside constraints.
- **CALC-57.** A constraint that uses `before_action` or `this_action` MUST be
  read only for the entities touched by the action, at the times touched by
  the action, and its value before the action MUST be taken as not existing.
- **CALC-58.** Actions MUST be checked and recorded one at a time, in the
  order in which they are recorded. The state before an action MUST be the
  facts recorded before it, and the state after it those facts plus the facts
  of the action.
- **CALC-41.** Every rejection MUST name the constraint and its address, its
  source module with the exact version, the entity and valid time where the
  constraint failed, and its rejection message.

**Rejection record**

- **CALC-42.** Every action that is rejected MUST be recorded as a rejection
  record with the parts in §2.13.
- **CALC-43.** A rejection record MUST NOT be read as a fact and MUST NOT
  affect a computed value.

**Computed value and projection**

- **CALC-44.** Every computed value MUST name the parts in §2.14, and its
  trace MUST be possible to show on request.
- **CALC-45.** A projection MUST name the last fact that has been taken into
  account. A projection MAY be discarded and rebuilt at any time.
- **CALC-46.** If a projection differs from a recalculation from the facts,
  the calculation from the facts MUST be the one used.
- **CALC-47.** The reader of a projection MUST be able to know its *R*, and
  SHOULD be told if any fact has been recorded after it.

**Reported results**

- **CALC-48.** A result reported outside SHOULD be recorded as a fact about the
  report, naming the computed property, parameters, *T*, and *R* it came from.

## 4. Examples

The full cases, 38 cases from 12 domains, are in the paper test
`uji/01-hitung.md` (Indonesian archive). Three of them:

**Rental: a rate that changes in the middle of the rental term.** The rate of
a tent is 50,000 a day, replaced with 60,000 from 1 November. A rental from
29 October to 3 November. Two policies, and both can be written:

```
computed Rental.total_due_a : number (money, increase), closed:
  at(this.term, this.item.daily_rate) × span(this.term, day)

computed Rental.total_due_b : number (money, increase), closed:
  sum(history(this.item.daily_rate, in: this.term),
      r: r.value × span(r.range, day))
```

Policy A, the rate on the start day: 5 × 50,000 = **250,000**. Policy B, the
rate in effect on each day: 3 × 50,000 + 2 × 60,000 = **270,000**. The
standard does not choose the policy; the standard makes sure that whichever
policy is written clearly.

**Clinic: insurance coverage with an annual cap.** Coverage 80%, cap
10,000,000 for one policy term of a year. The claims in that term are
5,000,000, 6,000,000, 3,000,000, and 1,000,000, in order.

```
helper Policy.payments : collection:
  fold(all(Claim, k: k.policy = this
                        and k.date in range(this.start_date, this.end_date)),
       order_by: k: k.date,
       initial: {remaining: this.cap, paid_out: []},
       step: (a, k):
         let b = min(k.amount × 0.8, a.remaining)
         {remaining: a.remaining − b, paid_out: append(a.paid_out, {claim: k, amount: b})}
  ).paid_out

computed Claim.paid : number (money, increase), closed:
  sum(this.policy.payments, b: if b.claim = this then b.amount else 0)
```

The results are 4,000,000; 4,800,000; **1,200,000**, because that is all that
is left of the cap; then **0**. Level 2.

**School: class rank.** The average score of Sam is 88, Maria 84.9, Nina
84.9, Leo 70.

```
computed Student.rank : number (position), closed:
  1 + count(all(Student, s: s.class = this.class
                               and s.average_score > this.average_score))
```

Sam **1**, Maria **2**, Nina **2**, Leo **4**. Equal scores get the same rank
by themselves, without a "sort" operation.

## 5. Not examples

- **`today()` inside a rule.** The time that is asked about is given by the
  asker as *T*.
- **A rule that records a journal as a fact.** A journal derived from an
  invoice is a computation. If the law requires the journal to be recorded as
  an official act, recording it is an action with a machine actor and an
  approver.
- **The next invoice number as a computed property.** That is decided, and is
  recorded when the invoice is recorded.
- **A sales forecast as a computed property.** That is an estimate, and is
  recorded as a fact with its actor.
- **A rule that takes an exchange rate from a service on the internet.** The
  exchange rate is recorded as a fact, then read.
- **Dividing 10,000,000 into three shares by rounding every share on its
  own.** The sum can be 9,999,999. What is used is a way of dividing without
  losing the remainder, for example `allocate` in the calculation library.
- **A new operation in the core for one way of calculating**, for example
  `round_even`. That way is written in the calculation library.
- **An exchange rate that does not exist read as 1**, or an empty price read
  as 0.
- **A contribution to a closed computation.**

## 6. Reasons

- **Three kinds of numbers.** The standard does not need to be a full
  programming language to hold all of reality: what is calculated is only the
  part that is certain, and the rest is recorded as facts.
  ([`decisions/0025`](../decisions/0025-three-kinds-of-numbers.md))
- **Closed and layered operations.** Every rule can be checked, compared, and
  is certain to finish, and implementations can be built step by step.
  ([`decisions/0026`](../decisions/0026-layered-operations.md))
- **A computed property is read like a property**, so humans and AI read data
  and computed values in one way.
  ([`decisions/0028`](../decisions/0028-computed-properties.md))
- **Two times, without "now", half-open ranges**, so that a result can be read
  back as its state on any day.
  ([`decisions/0029`](../decisions/0029-time-in-calculation.md))
- **Not computable, not 0.** A number that is wrong without being seen is more
  dangerous than a number that is missing.
  ([`decisions/0030`](../decisions/0030-not-computable.md))
- **Open computations and contributions**, so that modules from different
  authors can compose one number without changing each other.
  ([`decisions/0031`](../decisions/0031-open-computed-properties.md))
- **Projection** and **reported results**: a result may be stored and
  remembered, without ever becoming a second truth.
  ([`decisions/0032`](../decisions/0032-projections.md),
  [`decisions/0033`](../decisions/0033-reported-results.md))
- **Constraints per action, and rejection records.** Business rules are
  written with the same blocks, and every rejection can be explained.
  ([`decisions/0034`](../decisions/0034-constraints.md),
  [`decisions/0035`](../decisions/0035-rejection-records.md))
- **Exact fractions, written rounding, units are calculated**, so that two
  implementations give the same number down to the last rupiah.
  ([`decisions/0041`](../decisions/0041-numbers-in-calculation.md))
- **Direction is checked by the machine.**
  ([`decisions/0027`](../decisions/0027-number-direction.md))
- **A gap found by the machine is closed with the meaning that people guess
  most easily**, then proved with the reference calculator before it is
  decided.
  ([`decisions/0044`](../decisions/0044-additions-from-reference-calculator.md))
- **A small core, ways of calculating as content.** The form stays fixed even
  as ways of calculating keep growing. A new way is written in a library and
  proved with examples, without changing the form.
  ([`decisions/0045`](../decisions/0045-core-operations-and-calculation-library.md))

## 7. Outside standards

| Part | Counterpart |
|---|---|
| Collect, summarize, group | SELECT, aggregates, and GROUP BY in SQL (ISO/IEC 9075) |
| Order and fold | window functions in SQL:2003; *fold* in functional programming languages |
| Bounded recursion | WITH RECURSIVE in SQL:1999; Datalog |
| Projection update | distributive, algebraic, and holistic aggregates (Gray et al., *Data Cube*, 1997); *incremental view maintenance*; *differential dataflow* |
| Reading at two times | bitemporal tables in SQL:2011; XTDB, Datomic |
| Exact numbers | `xsd:decimal`; exact rational numbers |
| Units are calculated | unit algebra in UCUM and QUDT |
| Core and calculation library | built-in functions and the standard library in programming languages |
| Divide without loss by the largest remainder, in the calculation library | the largest remainder method (Hamilton) |
| Half-open range | the [start, end) range convention in SQL:2011 and in many time libraries |
| Constraint | SHACL (W3C); *assertion* in XBRL Formula |
| Rule notation | FEEL in DMN (OMG); CEL. May be bridged in an appendix |
| Projection | *projection* and *read model* in *event sourcing* |

## 8. Open questions

1. **Full notation.** Answered: detailed in
   [`appendix/A-notation.md`](../appendix/A-notation.md), locked together
   with this document. The gaps in meaning that were found when writing the notation have been decided
   here
   ([`decisions/0043`](../decisions/0043-additions-from-notation.md)), and so
   have the gaps found by the reference calculator
   ([`decisions/0044`](../decisions/0044-additions-from-reference-calculator.md)).
   The remaining gaps are recorded in
   [`reference/README.md`](../reference/README.md).
2. **History of a computed property.** Should `history` be usable for a
   computed property? For a rule that uses `T`, the value can change at any
   moment, so its history cannot always be written as a list.
3. **Ways of calculating that are not yet tested.** Rounding to even
   (*banker's rounding*), day conventions such as 30/360, and fractional
   powers are written in the calculation library when there is a real case.
   Descending order and a filter over an intermediate collection may need to be
   in the core; both are tested first with the entry test for the core (§2.5).
4. **Constraints and backdated changes.** Answered: tested by the reference
   calculator and decided in
   [`decisions/0047`](../decisions/0047-constraints-and-backdated-changes.md).
   The cost for a correction that goes very far back is part of question 6.
5. **Different rules for child concepts.** May a child concept use its own
   rule for a computed property owned by its parent?
6. **Resource limits.** A rule that is certain to finish can still be very
   expensive, for example a daily constraint for a rental of one hundred
   years. Is a standard limit needed that is the same in all implementations?
7. **Precision of each currency.** Answered: there is no rounding by
   default. In practice the precision of ISO 4217 is not always used, for
   example IDR has two decimals there but is paid in whole rupiah. A number
   is rounded only where a rule says so (§2.8), and a limit on the digits of
   a recorded value is written as a constraint ([`decisions/0057`](../decisions/0057-closure-before-lock.md)).
8. **Module set in the past.** A result depends on the installed modules. To
   read a result as of an *R* that has already passed, the time a module was
   installed needs to be recorded. Discussed together with ownership, in v0.2
   ([`decisions/0048`](../decisions/0048-ownership-to-v02.md)).
9. **Retention of rejection records.** A rejection record can contain personal
   data from the action that was tried. How long is it kept, and can it be
   redacted (Indonesian archive, `kajian/01-ekosistem.md`,
   D2)?
10. **Examples for a helper without a concept.** [`08-proof.md`](08-proof.md)
    knows only the question `entity.property`, so library helpers are
    exemplified through a supporting concept. A form of example is needed that
    calls a helper directly.
11. **Types of helper parameters and results.** A helper cannot yet state the
    type of its parameters, or a result "number or date". As a result
    `percentile` in the library is only for numbers.
12. **Binding and named arguments for helpers,** so that
    `median(k, x: x.duration)` and `round(n, to: 1, mode: nearest)` can be
    written like core operations
    ([`appendix/A-notation.md`](../appendix/A-notation.md) §2.7).
13. **Calendar months.** Answered: shifting and difference in months stay in
    the core as written in §2.7, which is what most monthly billing does.
    Another convention, such as 30/360 for loans, is written in the
    calculation library when a case needs it ([`decisions/0057`](../decisions/0057-closure-before-lock.md)).
