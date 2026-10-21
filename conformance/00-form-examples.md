# Examples from the form documents

The examples in [`08-proof.md`](../form/08-proof.md) §4,
[`06-calculation-rules.md`](../form/06-calculation-rules.md) §4, and
[`appendix/A-notation.md`](../appendix/A-notation.md) §4 are written in full
in the reference notation, so that the reference calculator can run them.

Some examples in the form documents are only told, for example the accept
example `adjoining_no_overlap` and the reject example with an approver. Here
all of them are written as complete examples. The expected results are taken
from the documents, not from the output of the calculator (PROOF-12).

The examples in appendix A use the concept `Item` and the property `item` from
the vocabulary [`content/vocabulary/item.md`](../content/vocabulary/item.md),
`uniti/item@v1`.

## Rental

Module and examples from appendix A §4, without change.

```uniti
module rudi/rental@v3
  uses uniti/item@v1

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

applies to Rental:
  item         required
  start_date   required
  end_date     required

applies to Item:
  daily_rate

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

constraint Rental.no_overlap
  label.en     No overlap
  definition.en  One item is not rented out twice on the same day.
  message.en   This item is already rented for part of that term.
  rule:
    count(all(Rental, s: s ≠ this and s.item = this.item
                            and exists(overlap(s.term, this.term)))) = 0

example three_night_rental
  kind         compute
  title        Three-night rental
  explanation  A tent at a rate of 50,000 a day is rented from 6 to 9 October.
               Three nights, so the total is 150,000.
  zone         WIB
  facts        recorded 6 Oct 2026 10:00
    tent  type        Item            valid 1 Oct 2026
    f1: tent  daily_rate  50,000 IDR/day  valid 1 Oct 2026
    r1    type        Rental          valid 6 Oct 2026
    r1    item        tent            valid 6 Oct 2026
    r1    start_date  6 Oct 2026      valid 6 Oct 2026
    r1    end_date    9 Oct 2026      valid 6 Oct 2026
  ask          r1.total_due   T: 6 Oct 2026   R: 6 Oct 2026 12:00
  result       150,000 IDR

example rate_rise_after_rental
  kind         compute
  title        Rate rise after the rental is recorded
  explanation  The rate rises to 60,000 from 1 November. The October rental
               still uses the rate valid at T.
  zone         WIB
  facts        as in three_night_rental
    f2: tent  daily_rate  60,000 IDR/day  valid 1 Nov 2026  recorded 20 Oct 2026  replaces f1
  ask          r1.total_due   T: 6 Oct 2026   R: 21 Oct 2026
  result       150,000 IDR

example one_day_overlap
  kind         reject
  title        Overlap of one day
  explanation  The tent is already booked for 10 to 13 October. The new rental
               of 12 to 14 October overlaps on 12 October.
  zone         WIB
  facts        recorded 1 Oct 2026 09:00
    tent   type        Item          valid 1 Oct 2026
    r1     type        Rental        valid 1 Oct 2026
    r1     item        tent          valid 1 Oct 2026
    r1     start_date  10 Oct 2026   valid 1 Oct 2026
    r1     end_date    13 Oct 2026   valid 1 Oct 2026
  action       recorded 5 Oct 2026 15:00
    r2     type        Rental        valid 5 Oct 2026
    r2     item        tent          valid 5 Oct 2026
    r2     start_date  12 Oct 2026   valid 5 Oct 2026
    r2     end_date    14 Oct 2026   valid 5 Oct 2026
  result       rejected by no_overlap, entity r2
```

Accept example from the table in 08 §4. After the action is accepted, the
total of the new rental is asked: two nights, 13 and 14 October.

```uniti
example adjoining_no_overlap
  kind         accept
  title        Adjoining rental without overlap
  explanation  The tent is already booked for 10 to 13 October. The new rental
               starts on 13 October, the day the tent is returned, so no day
               is used by two rentals. The new rental is two nights, 100,000.
  zone         WIB
  facts        as in one_day_overlap
    tent   daily_rate  50,000 IDR/day  valid 1 Oct 2026  recorded 1 Oct 2026 09:00
  action       recorded 5 Oct 2026 15:00
    r2     type        Rental        valid 5 Oct 2026
    r2     item        tent          valid 5 Oct 2026
    r2     start_date  13 Oct 2026   valid 5 Oct 2026
    r2     end_date    15 Oct 2026   valid 5 Oct 2026
  result       accepted
  ask          r2.total_due   T: 13 Oct 2026   R: 5 Oct 2026 16:00
  result       100,000 IDR
```

## Rental: a rate that changes in the middle of the rental term

Two policies from 06 §4, in a separate module that uses the rental module.

```uniti
module example/rate@v1
  uses rudi/rental@v3
  uses uniti/item@v1

computed Rental.total_due_a : number (money, increase), closed:
  at(this.term, this.item.daily_rate) × span(this.term, day)

computed Rental.total_due_b : number (money, increase), closed:
  sum(history(this.item.daily_rate, in: this.term),
      r: r.value × span(r.range, day))

example rate_on_start_day
  kind         compute
  title        Rate on the start day
  explanation  The rate of the tent is 50,000 a day, replaced with 60,000 from
               1 November. A rental from 29 October to 3 November uses the
               rate on the start day: 5 × 50,000 = 250,000.
  zone         WIB
  facts        recorded 20 Oct 2026 09:00
    tent       type          Item            valid 1 Oct 2026
    f1: tent   daily_rate    50,000 IDR/day  valid 1 Oct 2026
    f2: tent   daily_rate    60,000 IDR/day  valid 1 Nov 2026  replaces f1
    r1         type          Rental          valid 20 Oct 2026
    r1         item          tent            valid 20 Oct 2026
    r1         start_date    29 Oct 2026     valid 20 Oct 2026
    r1         end_date      3 Nov 2026      valid 20 Oct 2026
  ask          r1.total_due_a   T: 29 Oct 2026   R: 29 Oct 2026
  result       250,000 IDR

example rate_every_day
  kind         compute
  title        The rate in effect on each day
  explanation  The same rental uses the rate in effect on each day:
               3 × 50,000 + 2 × 60,000 = 270,000.
  zone         WIB
  facts        as in rate_on_start_day
  ask          r1.total_due_b   T: 29 Oct 2026   R: 29 Oct 2026
  result       270,000 IDR
```

## Clinic: insurance coverage with an annual cap

From 06 §4, plus the not computable example from 08 §4.

```uniti
module example/clinic@v1

concept Policy
concept Claim

property policy : reference Policy
property date : date
property amount : number (money, increase)
property start_date : date
property end_date : date
property cap : number (money, position)

applies to Policy:
  start_date   required
  end_date     required
  cap

applies to Claim:
  policy       required
  date         required
  amount       required

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

example cap_partly_left
  kind         compute
  title        Cap partly left
  explanation  Coverage 80%, cap 10,000,000 a year. Claims of 5,000,000 and
               6,000,000 were paid 4,000,000 and 4,800,000. The third claim of
               3,000,000 is only paid the rest of the cap, 1,200,000.
  zone         WITA
  facts        recorded 20 Dec 2026 09:00
    p1   type     Policy           valid 1 Jan 2026
    p1   start_date  1 Jan 2026    valid 1 Jan 2026
    p1   end_date    1 Jan 2027    valid 1 Jan 2026
    p1   cap      10,000,000 IDR   valid 1 Jan 2026
    k1   type     Claim            valid 3 Mar 2026
    k1   policy   p1               valid 3 Mar 2026
    k1   date     3 Mar 2026       valid 3 Mar 2026
    k1   amount   5,000,000 IDR    valid 3 Mar 2026
    k2   type     Claim            valid 12 Jun 2026
    k2   policy   p1               valid 12 Jun 2026
    k2   date     12 Jun 2026      valid 12 Jun 2026
    k2   amount   6,000,000 IDR    valid 12 Jun 2026
    k3   type     Claim            valid 7 Sep 2026
    k3   policy   p1               valid 7 Sep 2026
    k3   date     7 Sep 2026       valid 7 Sep 2026
    k3   amount   3,000,000 IDR    valid 7 Sep 2026
    k4   type     Claim            valid 2 Dec 2026
    k4   policy   p1               valid 2 Dec 2026
    k4   date     2 Dec 2026       valid 2 Dec 2026
    k4   amount   1,000,000 IDR    valid 2 Dec 2026
  ask          k3.paid   T: 31 Dec 2026   R: 31 Dec 2026
  result       1,200,000 IDR

example first_claim_in_full
  kind         compute
  title        First claim covered in full
  explanation  The first claim of 5,000,000 is paid 80%, 4,000,000.
  zone         WITA
  facts        as in cap_partly_left
  ask          k1.paid   T: 31 Dec 2026   R: 31 Dec 2026
  result       4,000,000 IDR

example cap_exhausted
  kind         compute
  title        Cap already used up
  explanation  After the third claim, the cap is used up. The fourth claim is
               paid 0.
  zone         WITA
  facts        as in cap_partly_left
  ask          k4.paid   T: 31 Dec 2026   R: 31 Dec 2026
  result       0 IDR

example cap_not_recorded
  kind         compute
  title        Cap not recorded
  explanation  The policy has no cap yet, so the paid part of the claim cannot
               be computed yet. The result is not 0.
  zone         WITA
  facts        recorded 20 Mar 2026 09:00
    p1   type        Policy         valid 1 Jan 2026
    p1   start_date  1 Jan 2026     valid 1 Jan 2026
    p1   end_date    1 Jan 2027     valid 1 Jan 2026
    k1   type        Claim          valid 3 Mar 2026
    k1   policy      p1             valid 3 Mar 2026
    k1   date        3 Mar 2026     valid 3 Mar 2026
    k1   amount      5,000,000 IDR  valid 3 Mar 2026
  ask          k1.paid   T: 20 Mar 2026   R: 20 Mar 2026 12:00
  result       not computable: empty value
```

## School: class rank

Example from appendix A §4, plus Budi and Dodi from 06 §4.

```uniti
module example/school@v1

concept Class
concept Student
property class : reference Class
property average_score : number (position)

applies to Student:
  class          required
  average_score

computed Student.rank : number (position), closed:
  1 + count(all(Student, s: s.class = this.class
                               and s.average_score > this.average_score))

example tied_scores
  kind         compute
  title        Two students with the same score
  explanation  Budi 88, Ani and Citra both 84.9, Dodi 70. Ani and Citra are
               both at rank 2, and Dodi is at rank 4.
  facts        recorded 1 Dec 2026
    k7a    type           Class     valid 1 Jul 2026
    budi   type           Student   valid 1 Jul 2026
    budi   class          k7a       valid 1 Jul 2026
    budi   average_score  88        valid 1 Dec 2026
    ani    type           Student   valid 1 Jul 2026
    ani    class          k7a       valid 1 Jul 2026
    ani    average_score  84.9      valid 1 Dec 2026
    citra  type           Student   valid 1 Jul 2026
    citra  class          k7a       valid 1 Jul 2026
    citra  average_score  84.9      valid 1 Dec 2026
    dodi   type           Student   valid 1 Jul 2026
    dodi   class          k7a       valid 1 Jul 2026
    dodi   average_score  70        valid 1 Dec 2026
  ask          citra.rank   T: 1 Dec 2026   R: 1 Dec 2026
  result       2

example highest_score
  kind         compute
  title        Highest score in the class
  explanation  No student has a score above Budi.
  facts        as in tied_scores
  ask          budi.rank   T: 1 Dec 2026   R: 1 Dec 2026
  result       1

example after_tied_scores
  kind         compute
  title        Rank after two equal scores
  explanation  Three students are above Dodi, so Dodi is at rank 4, not 3.
  facts        as in tied_scores
  ask          dodi.rank   T: 1 Dec 2026   R: 1 Dec 2026
  result       4
```

## Organization: approval of a large purchase

The constraint `approved_if_large` from 06 §2.12, with a reject example from
08 §4 and two accept examples. Here the actor and the approver are exactly
what is tested, so the action is not abbreviated.

```uniti
module example/organization@v1

concept Person
concept Contract
concept Purchase

choice_list Position, closed
  label.en     Position
  definition.en  A person's position in an organization.
  choices:
    manager
    staff

property employee : reference Person
property position : choice Position
property total : number (money, increase)

applies to Contract:
  employee     required
  position     required

applies to Purchase:
  total        required

constraint Purchase.approved_if_large:
  this.total ≤ 10,000,000 IDR
  or (exists(this_action.approver)
      and this_action.approver ≠ this_action.actor
      and any_match(all(Contract, k: k.employee = this_action.approver),
                    k: k.position = manager))

example self_approved
  kind         reject
  title        Large purchase approved by its own actor
  explanation  Sari is a manager, but she records and approves a purchase of
               12,000,000 at the same time. The approver must be another
               person.
  zone         WIB
  facts        recorded 2 Jan 2026 09:00
    sari   type      Person     valid 2 Jan 2026
    budi   type      Person     valid 2 Jan 2026
    ks     type      Contract   valid 2 Jan 2026
    ks     employee  sari       valid 2 Jan 2026
    ks     position  manager    valid 2 Jan 2026
    kb     type      Contract   valid 2 Jan 2026
    kb     employee  budi       valid 2 Jan 2026
    kb     position  manager    valid 2 Jan 2026
  action       recorded 12 Oct 2026 09:00, actor sari, approver sari
    p1     type      Purchase         valid 12 Oct 2026
    p1     total     12,000,000 IDR   valid 12 Oct 2026
  result       rejected by approved_if_large, entity p1, at 12 Oct 2026

example approved_by_other_manager
  kind         accept
  title        Large purchase approved by another manager
  explanation  Sari records a purchase of 12,000,000, and Budi, another
               manager, approves it.
  zone         WIB
  facts        as in self_approved
  action       recorded 12 Oct 2026 09:00, actor sari, approver budi
    p1     type      Purchase         valid 12 Oct 2026
    p1     total     12,000,000 IDR   valid 12 Oct 2026
  result       accepted

example small_purchase
  kind         accept
  title        Small purchase without an approver
  explanation  A purchase of exactly 10,000,000, not yet above the limit, so
               it does not need approval.
  zone         WIB
  facts        as in self_approved
  action       recorded 12 Oct 2026 09:00, actor sari
    p1     type      Purchase         valid 12 Oct 2026
    p1     total     10,000,000 IDR   valid 12 Oct 2026
  result       accepted
```
