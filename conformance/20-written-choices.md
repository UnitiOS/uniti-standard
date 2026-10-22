# Reference calculator choices that are now written

Stage 7, quick test 7.3 (Indonesian archive, `uji/03-uji-singkat.md`),
for obstacles P5 to P10. Before, these choices only existed in the program;
now they are written in the form documents
([`decisions/0054`](../decisions/0054-reference-choices-into-text.md)).
P7 for contributions and P9 are tested in `operasi/uji_hitung.py`, because the
result cannot be written as an example.

## Calendar months (P5, P6)

`difference(a, b, month)` is the largest *n* such that `a + n months` is not
after `b`. The pieces of `split` are counted from the start of the range, and
the last piece stops at the end of the range.

```uniti
module reference/month@v1

concept Contract
property start_date : date
property end_date : date

applies to Contract:
  start_date
  end_date

computed Contract.length_in_months : number (duration, position), closed:
  difference(this.start_date, this.end_date, month)

computed Contract.last_slice : number (duration, position), closed:
  span(fold(split(range(this.start_date, this.end_date), step: 1 month),
            initial: range(this.start_date, this.start_date),
            step: (s, p): p),
       day)

example end_of_month_to_end_of_month
  kind         compute
  title        31 January to 28 February
  explanation  31 January plus one month falls on 28 February, so the
               difference is one month.
  facts        recorded 1 Jan 2026
    k1   type        Contract      valid 1 Jan 2026
    k1   start_date  31 Jan 2026   valid 1 Jan 2026
    k1   end_date    28 Feb 2026   valid 1 Jan 2026
  ask          k1.length_in_months   T: 1 Mar 2026   R: 1 Mar 2026
  result       1 month

example mid_month
  kind         compute
  title        15 January to 15 March
  explanation  Two months, although only February is whole within it.
  facts        recorded 1 Jan 2026
    k1   type        Contract      valid 1 Jan 2026
    k1   start_date  15 Jan 2026   valid 1 Jan 2026
    k1   end_date    15 Mar 2026   valid 1 Jan 2026
  ask          k1.length_in_months   T: 1 Apr 2026   R: 1 Apr 2026
  result       2 months

example not_yet_a_month
  kind         compute
  title        31 January to 27 February
  explanation  It has not reached 31 January plus one month.
  facts        recorded 1 Jan 2026
    k1   type        Contract      valid 1 Jan 2026
    k1   start_date  31 Jan 2026   valid 1 Jan 2026
    k1   end_date    27 Feb 2026   valid 1 Jan 2026
  ask          k1.length_in_months   T: 1 Mar 2026   R: 1 Mar 2026
  result       0 months

example two_months_from_end_of_month
  kind         compute
  title        31 January to 29 March
  explanation  31 January + 2 months falls on 31 March, directly from
               31 January, and that is after 29 March. So the difference is
               1 month. If shifted month by month, 28 February + 1 month =
               28 March, and the result would be 2 months.
  facts        recorded 1 Jan 2026
    k1   type        Contract      valid 1 Jan 2026
    k1   start_date  31 Jan 2026   valid 1 Jan 2026
    k1   end_date    29 Mar 2026   valid 1 Jan 2026
  ask          k1.length_in_months   T: 1 Apr 2026   R: 1 Apr 2026
  result       1 month

example backwards_like_a_mirror
  kind         compute
  title        31 March backwards to 29 March
  explanation  Calculated as from 29 March to 31 March, then made negative.
               Not yet a whole month, so 0 months, not −1 month.
  facts        recorded 1 Jan 2026
    k1   type        Contract      valid 1 Jan 2026
    k1   start_date  31 Mar 2026   valid 1 Jan 2026
    k1   end_date    29 Mar 2026   valid 1 Jan 2026
  ask          k1.length_in_months   T: 1 Apr 2026   R: 1 Apr 2026
  result       0 months

example split_from_start_of_range
  kind         compute
  title        Monthly pieces from 31 January
  explanation  The pieces start on 31 January, 28 February, and 31 March, all
               counted from 31 January. The last piece stops on 15 April:
               15 days. If counted from the previous piece, the third piece
               starts on 28 March.
  facts        recorded 1 Jan 2026
    k1   type        Contract      valid 1 Jan 2026
    k1   start_date  31 Jan 2026   valid 1 Jan 2026
    k1   end_date    15 Apr 2026   valid 1 Jan 2026
  ask          k1.last_slice   T: 1 May 2026   R: 1 May 2026
  result       15 days
```

## Tie-breaker for an entity with two types (P7)

An entity with two types uses the earliest type fact, whatever concept is
asked.

```uniti
module reference/two-types@v1

concept Report
concept Supplier
concept Customer
property number : number (position)

applies to Supplier:
  number

applies to Customer:
  number

computed Report.customer_order : number (position), closed:
  fold(all(Customer), order_by: p: 0, initial: 0, step: (s, p): s × 10 + p.number)

example customer_who_was_a_supplier_first
  kind         compute
  title        Customer who first became a supplier
  explanation  x is a supplier since January and a customer since March. y is
               a customer since February. The order follows the earliest type
               fact: x (January), then y (February). The result is 1, then
               12.
  facts        recorded 1 Jan 2026
    rep   type    Report     valid 1 Jan 2026
    x     type    Supplier   valid 1 Jan 2026
    x     type    Customer   valid 1 Mar 2026
    x     number  1          valid 1 Jan 2026
    y     type    Customer   valid 1 Feb 2026
    y     number  2          valid 1 Feb 2026
  ask          rep.customer_order   T: 1 Apr 2026   R: 1 Apr 2026
  result       12
```

## A property with many values (P8)

A computed property with many values produces a collection. With no value,
the result is a collection without members, not empty. So `exists(…)` over a
property with many values is always yes, and what is used is `count(…)`.

```uniti
module reference/many@v1

concept Person
property phone : text, many

applies to Person:
  phone

computed Person.all_phones : text, many, closed:
  this.phone

computed Person.phone_exists : yes_no, closed:
  exists(this.phone)

computed Person.has_phone : yes_no, closed:
  count(this.phone) > 0

example no_phone
  kind         compute
  title        Person without a phone
  explanation  No number is recorded yet. The result is a collection without
               members.
  facts        recorded 1 Jan 2026
    a   type   Person   valid 1 Jan 2026
  ask          a.all_phones   T: 1 Feb 2026   R: 1 Feb 2026
  result       []

example exists_over_collection_without_members
  kind         compute
  title        exists(…) over a collection without members
  explanation  A collection without members is not empty, so exists(…) is
               yes.
  facts        as in no_phone
  ask          a.phone_exists   T: 1 Feb 2026   R: 1 Feb 2026
  result       yes

example count_to_check
  kind         compute
  title        count(…) to check whether there is a value
  explanation  What is used to check is the count.
  facts        as in no_phone
  ask          a.has_phone   T: 1 Feb 2026   R: 1 Feb 2026
  result       no
```

## A constraint whose result is empty (P10)

A constraint whose result is empty is treated like not computable: not met,
with the reason kind empty value.

```uniti
module reference/empty-constraint@v1

concept Purchase
property total : number (money, increase)
property checked : yes_no

applies to Purchase:
  total        required
  checked

constraint Purchase.is_checked
  label.en     Is checked
  definition.en  Every purchase has been checked.
  message.en   This purchase has not been checked yet.
  rule:
    this.checked

example purchase_without_check_mark
  kind         reject
  title        Purchase without a check mark
  explanation  checked is not required, but the constraint reads it. With no
               value, the result is empty, and the action is rejected.
  facts        recorded 1 Oct 2026
  action       recorded 2 Oct 2026 09:00
    b1   type    Purchase   valid 2 Oct 2026
    b1   total   500 IDR    valid 2 Oct 2026
  result       rejected by is_checked, entity b1

example purchase_with_check_mark
  kind         accept
  title        Purchase that has been checked
  explanation  With checked yes, the constraint is met.
  facts        recorded 1 Oct 2026
  action       recorded 2 Oct 2026 09:00
    b1   type      Purchase   valid 2 Oct 2026
    b1   total     500 IDR    valid 2 Oct 2026
    b1   checked   yes        valid 2 Oct 2026
  result       accepted
```
