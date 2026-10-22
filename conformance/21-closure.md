# Closure before the lock

Situations that the text did not settle before v0.1 was locked, now answered
by [`decisions/0057`](../decisions/0057-closure-before-lock.md): one action at
a time (T1), the empty and unit results of `unit_of`, `history`, and unit
powers (T2 to T4, T6, T7), and an old gap in a required property (T11). The
reference calculator follows the decision, and no result of an earlier example
changes.

## Two cashiers, the last tent (T1)

Actions are checked one at a time, in the order in which they are recorded. The
first rental is in the starting facts with the same recorded time as the action
of the second, so it counts as before the action, and the second is checked
against it.

```uniti
module reference/closure-rental@v1

concept Item
concept Rental

property item : reference Item
property daily_rate : number (money/duration, position)
property start_date : date
property end_date : date

applies to Item:
  daily_rate

applies to Rental:
  item         required
  start_date   required
  end_date     required

helper Rental.term : range:
  range(this.start_date, this.end_date)

computed Rental.total_due : number (money, increase), closed:
  sum(history(this.item.daily_rate, in: this.term),
      r: r.value × span(r.range, day))

constraint Rental.no_overlap
  label.en     No overlap
  definition.en  One item is not rented out twice on the same day.
  message.en   This item is already rented for part of that term.
  rule:
    count(all(Rental, s: s ≠ this and s.item = this.item
                            and exists(overlap(s.term, this.term)))) = 0

example last_tent_same_moment
  kind         reject
  title        Two rentals of the last tent at the same moment
  explanation  Alex and Sam rent out the last tent at 15:00 on 5 October. The
               rental of Alex is recorded first, and it is already among the
               facts. The rental of Sam is checked after it and rejected.
  zone         WIB
  facts        recorded 5 Oct 2026 15:00
    tent  type        Item          valid 1 Oct 2026
    r1    type        Rental        valid 5 Oct 2026
    r1    item        tent          valid 5 Oct 2026
    r1    start_date  10 Oct 2026   valid 5 Oct 2026
    r1    end_date    12 Oct 2026   valid 5 Oct 2026
  action       recorded 5 Oct 2026 15:00
    r2    type        Rental        valid 5 Oct 2026
    r2    item        tent          valid 5 Oct 2026
    r2    start_date  10 Oct 2026   valid 5 Oct 2026
    r2    end_date    12 Oct 2026   valid 5 Oct 2026
  result       rejected by no_overlap, entity r2
```

## A rental whose item is not filled in (T6)

`history(x.s, in: r)` with an empty `x` gives empty, like `x.s`. A collection
with no members would make `sum` give 0 and hide the missing item. Here the
total is not computable because of the empty value, and `exists` of the
history is no, which it would not be for a collection without members.

```uniti
module reference/closure-history@v1
  uses reference/closure-rental@v1

computed Rental.has_rate_history : yes_no, closed:
  exists(history(this.item.daily_rate, in: this.term))

example item_not_filled_in
  kind         compute
  title        History of the rate of a rental without an item
  explanation  The rental of Nina has no item yet. The history is empty, so
               exists(…) is no. A collection without members would give yes.
  zone         WIB
  facts        recorded 5 Oct 2026 10:00
    tent  type        Item            valid 1 Oct 2026
    tent  daily_rate  50,000 IDR/day  valid 1 Oct 2026
    r1    type        Rental          valid 5 Oct 2026
    r1    start_date  6 Oct 2026      valid 5 Oct 2026
    r1    end_date    9 Oct 2026      valid 5 Oct 2026
  ask          r1.has_rate_history   T: 6 Oct 2026   R: 6 Oct 2026
  result       no

example total_without_item_is_not_zero
  kind         compute
  title        Total due of a rental without an item
  explanation  The total is not 0 IDR. The missing item is reported as an
               empty value.
  zone         WIB
  facts        as in item_not_filled_in
  ask          r1.total_due   T: 6 Oct 2026   R: 6 Oct 2026
  result       not computable: empty value

example item_filled_in
  kind         compute
  title        Total due of the same rental with an item
  explanation  With the tent filled in, three nights at 50,000 are 150,000.
  zone         WIB
  facts        as in item_not_filled_in
    r1    item        tent            valid 5 Oct 2026  recorded 5 Oct 2026 10:00
  ask          r1.total_due   T: 6 Oct 2026   R: 6 Oct 2026
  result       150,000 IDR
```

## The unit of a number (T3, T4)

`unit_of` of a number without a unit is empty, because such a number has no
unit by definition. `unit_of` of a unit of more than one code, for example
`IDR/day`, is not computable because of unit mismatch.

```uniti
module reference/closure-unit@v1
  uses uniti/unit@v1

concept Item

property daily_rate : number (money/duration, position)
property pieces : number (position)

applies to Item:
  daily_rate
  pieces

computed Item.pieces_unit : choice Unit, closed:
  unit_of(this.pieces)

computed Item.rate_unit : choice Unit, closed:
  unit_of(this.daily_rate)

example number_without_unit
  kind         compute
  title        Unit of a number without a unit
  explanation  Five pieces have no unit, so the unit is empty.
  zone         WIB
  facts        recorded 1 Oct 2026 09:00
    tent  type        Item            valid 1 Oct 2026
    tent  pieces      5               valid 1 Oct 2026
    tent  daily_rate  50,000 IDR/day  valid 1 Oct 2026
  ask          tent.pieces_unit   T: 2 Oct 2026   R: 2 Oct 2026
  result       empty

example rate_has_two_codes
  kind         compute
  title        Unit of a rate per day
  explanation  IDR/day is two unit codes, so it cannot be one choice from the
               unit list.
  zone         WIB
  facts        as in number_without_unit
  ask          tent.rate_unit   T: 2 Oct 2026   R: 2 Oct 2026
  result       not computable: unit mismatch
```

## Four lengths multiplied (T2)

A unit code reaches the power 3 or −3 at most. Four lengths give cm⁴, which is
not computable because of unit mismatch.

```uniti
module reference/closure-power@v1

concept Box

property length : number (length, position)
property width : number (length, position)
property height : number (length, position)
property depth : number (length, position)

applies to Box:
  length
  width
  height
  depth

computed Box.hyper_volume : number (length, position), closed:
  this.length × this.width × this.height × this.depth

computed Box.volume_per_area : number (length, position), closed:
  this.length × this.width × this.height ÷ 1 cm²

example four_lengths
  kind         compute
  title        Four lengths multiplied
  explanation  10 cm × 20 cm × 30 cm × 40 cm would be cm⁴, above the power 3.
  zone         WIB
  facts        recorded 1 Oct 2026 09:00
    b1  type    Box     valid 1 Oct 2026
    b1  length  10 cm   valid 1 Oct 2026
    b1  width   20 cm   valid 1 Oct 2026
    b1  height  30 cm   valid 1 Oct 2026
    b1  depth   40 cm   valid 1 Oct 2026
  ask          b1.hyper_volume   T: 2 Oct 2026   R: 2 Oct 2026
  result       not computable: unit mismatch

example three_lengths
  kind         compute
  title        Three lengths divided by an area
  explanation  cm³ divided by cm² is cm, so the power 3 is reached but not
               passed. 6,000 cm.
  zone         WIB
  facts        as in four_lengths
  ask          b1.volume_per_area   T: 2 Oct 2026   R: 2 Oct 2026
  result       6,000 cm
```

## A property with many values in `history` (T7)

`history` of a property with many values is a collection with no order, of
records `{value, range}`. Here the office number of Maria is replaced on
1 November, and her home number stays: three records in 2026.

```uniti
module reference/closure-many@v1

concept Person
property phone : text, many

applies to Person:
  phone

computed Person.phones_in_2026 : number (position), closed:
  count(history(this.phone, in: range(1 Jan 2026, 1 Jan 2027)))

example three_records
  kind         compute
  title        Phone numbers of Maria during 2026
  explanation  0811 is valid from January to October, 0821 from November, and
               0855 for the whole year. Three records.
  zone         WIB
  facts        recorded 1 Jan 2026
    a       type    Person   valid 1 Jan 2026
    f1: a   phone   "0811"   valid 1 Jan 2026
    a       phone   "0855"   valid 1 Jan 2026
    a       phone   "0821"   valid 1 Nov 2026   recorded 1 Nov 2026   replaces f1
  ask          a.phones_in_2026   T: 1 Dec 2026   R: 1 Dec 2026
  result       3
```

## A property that became required later (T11)

The phone became required in a later version of the module. An old customer
record has no phone. Correcting its name is accepted, because the gap was
already there and the customer already had its type (CONCEPT-18). A customer
that the action creates must be complete, and a phone that the action removes
leaves a gap that the action itself makes.

```uniti
module reference/required-later@v1

concept Customer
property name : text
property phone : text

applies to Customer:
  name         required
  phone        required

example correct_name_of_old_record
  kind         accept
  title        Typo in the name of an old customer
  explanation  Nina was recorded before the phone was required, so she has a
               name and no phone. Her name is corrected. The missing phone was
               there before the action, so it does not block.
  zone         WIB
  facts        recorded 1 Mar 2026 09:00
    c1       type   Customer   valid 1 Mar 2026
    f1: c1   name   "Nnia"     valid 1 Mar 2026
  action       recorded 20 Oct 2026 10:00
    c1       name   "Nina"     valid 1 Mar 2026   corrects f1
  result       accepted

example new_customer_without_phone
  kind         reject
  title        New customer without a phone
  explanation  Sam is created by this action, so Sam must be complete.
  zone         WIB
  facts        as in correct_name_of_old_record
  action       recorded 20 Oct 2026 10:00
    c2   type   Customer   valid 20 Oct 2026
    c2   name   "Sam"      valid 20 Oct 2026
  result       rejected by CONCEPT-18, entity c2

example retract_phone_of_customer
  kind         reject
  title        Correction that removes a phone
  explanation  Maria has a phone. Retracting it makes the gap in this action,
               not before it, so it is rejected.
  zone         WIB
  facts        recorded 1 Mar 2026 09:00
    c3       type    Customer   valid 1 Mar 2026
    c3       name    "Maria"    valid 1 Mar 2026
    f2: c3   phone   "0811"     valid 1 Mar 2026
  action       recorded 20 Oct 2026 10:00
    c3   phone   valid 1 Mar 2026   retracts f2
  result       rejected by CONCEPT-18, entity c3
```
