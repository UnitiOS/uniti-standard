# Loyalty

Case R1 of the paper test (Indonesian archive, `uji/01-hitung.md`)
§4.K, written in the reference notation.

## R1. Expired points, used from the oldest

The paper test only tells the rule: `fold` like FIFO in P2, plus two more
things. Here it is written in full. The layers that have expired are dropped
with `fold` as well, because the core has no filter over intermediate
collections (06 §8 question 3). Points are no longer valid from their
expiry date.

```uniti
module paper/r1@v1

concept Member
concept PointMovement

choice_list MovementKind, closed
  choices:
    earn
    spend

property member : reference Member
property date : date
property kind : choice MovementKind
property amount : number (position)
property expiry : date

applies to PointMovement:
  member       required
  date         required
  kind         required
  amount       required
  expiry

helper Member.point_layers : collection:
  fold(all(PointMovement, m: m.member = this),
       order_by: m: m.date,
       initial: [],
       step: (k, m):
         if m.kind = earn
         then append(k, {amount: m.amount, expiry: m.expiry})
         else spend_points(still_valid(k, m.date), m.amount))

helper still_valid(layers, t) : collection:
  fold(layers, initial: [],
       step: (s, l): if l.expiry > t then append(s, l) else s)

helper spend_points(layers, n) : collection:
  let h = fold(layers,
               initial: {needed: n, layers: []},
               step: (a, l):
                 let take = min(l.amount, a.needed)
                 {needed: a.needed − take,
                  layers: if l.amount > take
                          then append(a.layers, l with amount = l.amount − take)
                          else a.layers})
  if h.needed > 0 then not_computable("not enough points")
  else h.layers

computed Member.point_balance : number (position), closed:
  sum(this.point_layers, l: if l.expiry > T then l.amount else 0)

example balance_february_2027
  kind         compute
  title        Balance after the January points expire
  explanation  The use of 120 takes 100 from January and 20 from March.
               30 from March remain, which are valid until before 10 March
               2027. If taken from the youngest first, this balance is 0.
  zone         WIB
  facts        recorded 5 Jun 2026 12:00
    maria   type    Member          valid 1 Jan 2026
    m1    type    PointMovement   valid 15 Jan 2026
    m1    member  maria             valid 15 Jan 2026
    m1    date    15 Jan 2026     valid 15 Jan 2026
    m1    kind    earn            valid 15 Jan 2026
    m1    amount  100             valid 15 Jan 2026
    m1    expiry  15 Jan 2027     valid 15 Jan 2026
    m2    type    PointMovement   valid 10 Mar 2026
    m2    member  maria             valid 10 Mar 2026
    m2    date    10 Mar 2026     valid 10 Mar 2026
    m2    kind    earn            valid 10 Mar 2026
    m2    amount  50              valid 10 Mar 2026
    m2    expiry  10 Mar 2027     valid 10 Mar 2026
    m3    type    PointMovement   valid 5 Jun 2026
    m3    member  maria             valid 5 Jun 2026
    m3    date    5 Jun 2026      valid 5 Jun 2026
    m3    kind    spend           valid 5 Jun 2026
    m3    amount  120             valid 5 Jun 2026
  ask          maria.point_balance   T: 1 Feb 2027   R: 1 Feb 2027
  result       30

example balance_april_2027
  kind         compute
  title        Balance after all points expire
  explanation  The March points expire on 10 March 2027, so as of 1 April
               2027 the balance is 0.
  zone         WIB
  facts        as in balance_february_2027
  ask          maria.point_balance   T: 1 Apr 2027   R: 1 Apr 2027
  result       0

example balance_day_before_expiry
  kind         compute
  title        Boundary point: the day before expiry
  explanation  On 9 March 2027 the March points are still valid: 30.
  zone         WIB
  facts        as in balance_february_2027
  ask          maria.point_balance   T: 9 Mar 2027   R: 9 Mar 2027
  result       30

example balance_on_expiry_day
  kind         compute
  title        Boundary point: exactly on the expiry date
  explanation  Points are no longer valid from their expiry date, so on
               10 March 2027 the balance is 0.
  zone         WIB
  facts        as in balance_february_2027
  ask          maria.point_balance   T: 10 Mar 2027   R: 10 Mar 2027
  result       0
```
