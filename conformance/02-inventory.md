# Inventory

Cases P1 to P4 of the paper test (`uji/01-hitung.md`<!-- ARCHIVE-LINK: ../../01-hitung.md -->
§4.B), written in the reference notation with the core and the calculation
library.

## P1. Available stock from three modules

The inventory vocabulary has `Item.available`, open, together with the
properties `item` and `amount` that the three contributing modules use. The
rental module belongs to Alex. The first organization installs all three; the
second organization does not install Alex's module.

```uniti
module paper/p1-inventory@v1

concept Item

property item : reference Item
property amount : number (position)

computed Item.available : number (position), open:
  sum(contributions)

module paper/p1-purchasing@v1
  uses paper/p1-inventory@v1

concept Receipt

applies to Receipt:
  item         required
  amount       required

contribution received to Item.available:
  sum(all(Receipt, p: p.item = this), p: p.amount)

module paper/p1-sales@v1
  uses paper/p1-inventory@v1

concept Sale

applies to Sale:
  item         required
  amount       required

contribution sold to Item.available:
  − sum(all(Sale, j: j.item = this), j: j.amount)

module alex/p1-rental@v1
  uses paper/p1-inventory@v1

concept Rental

property start_date : date
property end_date : date

applies to Rental:
  item         required
  amount       required
  start_date   required
  end_date     required

helper Rental.term : range:
  range(this.start_date, this.end_date)

contribution being_rented to Item.available:
  − sum(all(Rental, s: s.item = this and T in s.term), s: s.amount)

module paper/p1-shop@v1
  uses paper/p1-inventory@v1
  uses paper/p1-purchasing@v1
  uses paper/p1-sales@v1
  uses alex/p1-rental@v1

example available_while_rented
  kind         compute
  title        Available stock while two units are rented
  explanation  10 received, 3 sold, and 2 rented from 5 to 8 October:
               10 − 3 − 2 = 5.
  zone         WIB
  facts        recorded 5 Oct 2026 09:00
    t4   type        Item         valid 1 Oct 2026
    e1   type        Receipt      valid 1 Oct 2026
    e1   item        t4           valid 1 Oct 2026
    e1   amount      10           valid 1 Oct 2026
    j1   type        Sale         valid 4 Oct 2026
    j1   item        t4           valid 4 Oct 2026
    j1   amount      3            valid 4 Oct 2026
    s1   type        Rental       valid 2 Oct 2026
    s1   item        t4           valid 2 Oct 2026
    s1   amount      2            valid 2 Oct 2026
    s1   start_date  5 Oct 2026   valid 2 Oct 2026
    s1   end_date    8 Oct 2026   valid 2 Oct 2026
  ask          t4.available   T: 6 Oct 2026   R: 6 Oct 2026
  result       5

example available_after_return
  kind         compute
  title        Available stock after the rental ends
  explanation  The tent comes back on 8 October: 10 − 3 = 7.
  zone         WIB
  facts        as in available_while_rented
  ask          t4.available   T: 9 Oct 2026   R: 9 Oct 2026
  result       7

example available_on_start_day
  kind         compute
  title        Boundary: the first day of the rental
  explanation  A range includes its start date, so on 5 October the tent is
               already rented: 10 − 3 − 2 = 5.
  zone         WIB
  facts        as in available_while_rented
  ask          t4.available   T: 5 Oct 2026   R: 5 Oct 2026 12:00
  result       5

example available_on_end_day
  kind         compute
  title        Boundary: the last day of the rental
  explanation  A range does not include its end date, so on 8 October the
               tent is already back: 10 − 3 = 7.
  zone         WIB
  facts        as in available_while_rented
  ask          t4.available   T: 8 Oct 2026   R: 8 Oct 2026
  result       7

module paper/p1-shop-without-rental@v1
  uses paper/p1-inventory@v1
  uses paper/p1-purchasing@v1
  uses paper/p1-sales@v1

example without_rental_module
  kind         compute
  title        Organization without the rental module
  explanation  Without Alex's module there is no rental contribution:
               10 − 3 = 7, also on 6 October.
  zone         WIB
  facts        recorded 5 Oct 2026 09:00
    t4   type    Item       valid 1 Oct 2026
    e1   type    Receipt    valid 1 Oct 2026
    e1   item    t4         valid 1 Oct 2026
    e1   amount  10         valid 1 Oct 2026
    j1   type    Sale       valid 4 Oct 2026
    j1   item    t4         valid 4 Oct 2026
    j1   amount  3          valid 4 Oct 2026
  ask          t4.available   T: 6 Oct 2026   R: 6 Oct 2026
  result       7
```

A module that is not installed also cannot be named in an example, so the
last example has no rental at all. The paper test mentions a rental that is
recorded while its module is not installed; that situation cannot be written
as an example.

## P2. Cost of goods with FIFO

In the paper test, incoming and outgoing movements are told apart with
`m.type`, but `type` is the base property for the concept of an entity. Here
the property is `kind`. The initial state uses `0 IDR`, so that the cost of
goods keeps its unit even when no item has gone out yet (CALC-55).

```uniti
module paper/p2@v1

concept Item
concept Movement

choice_list MovementKind, closed
  choices:
    inbound
    outbound

property item : reference Item
property date : date
property kind : choice MovementKind
property amount : number (position)
property price : number (money, position)

applies to Movement:
  item         required
  date         required
  kind         required
  amount       required
  price

helper Item.fifo : record:
  fold(all(Movement, m: m.item = this),
       order_by: m: m.date,
       initial: {layers: [], cogs: 0 IDR},
       step: (k, m):
         if m.kind = inbound
         then k with layers = append(k.layers, {amount: m.amount, price: m.price})
         else take_out(k, m.amount))

helper take_out(k, n) : record:
  let h = fold(k.layers,
               initial: {needed: n, layers: [], cogs: k.cogs},
               step: (a, l):
                 let take = min(l.amount, a.needed)
                 {needed: a.needed − take,
                  cogs: a.cogs + take × l.price,
                  layers: if l.amount > take
                          then append(a.layers, l with amount = l.amount − take)
                          else a.layers})
  if h.needed > 0 then not_computable("not enough stock")
  else {layers: h.layers, cogs: h.cogs}

computed Item.cogs : number (money, increase), closed:
  this.fifo.cogs

computed Item.inventory_value : number (money, position), closed:
  sum(this.fifo.layers, l: l.amount × l.price)

example cogs_first_issue
  kind         compute
  title        Cost of goods of the first issue
  explanation  15 out on 7 October: 10 × 100,000 from the first layer and
               5 × 120,000 from the second layer = 1,600,000.
  zone         WIB
  facts        recorded 10 Oct 2026 09:00
    b1   type     Item          valid 1 Oct 2026
    m1   type     Movement      valid 1 Oct 2026
    m1   item     b1            valid 1 Oct 2026
    m1   date     1 Oct 2026    valid 1 Oct 2026
    m1   kind     inbound       valid 1 Oct 2026
    m1   amount   10            valid 1 Oct 2026
    m1   price    100,000 IDR   valid 1 Oct 2026
    m2   type     Movement      valid 5 Oct 2026
    m2   item     b1            valid 5 Oct 2026
    m2   date     5 Oct 2026    valid 5 Oct 2026
    m2   kind     inbound       valid 5 Oct 2026
    m2   amount   10            valid 5 Oct 2026
    m2   price    120,000 IDR   valid 5 Oct 2026
    m3   type     Movement      valid 7 Oct 2026
    m3   item     b1            valid 7 Oct 2026
    m3   date     7 Oct 2026    valid 7 Oct 2026
    m3   kind     outbound      valid 7 Oct 2026
    m3   amount   15            valid 7 Oct 2026
    m4   type     Movement      valid 9 Oct 2026
    m4   item     b1            valid 9 Oct 2026
    m4   date     9 Oct 2026    valid 9 Oct 2026
    m4   kind     outbound      valid 9 Oct 2026
    m4   amount   3             valid 9 Oct 2026
  ask          b1.cogs   T: 8 Oct 2026   R: 10 Oct 2026 12:00
  result       1,600,000 IDR

example cogs_after_two_issues
  kind         compute
  title        Cost of goods after two issues
  explanation  3 out on 9 October: 3 × 120,000 = 360,000. The total is
               1,600,000 + 360,000 = 1,960,000.
  zone         WIB
  facts        as in cogs_first_issue
  ask          b1.cogs   T: 10 Oct 2026   R: 10 Oct 2026 12:00
  result       1,960,000 IDR

example remaining_inventory_value
  kind         compute
  title        Remaining inventory value
  explanation  2 units remain from the layer of 120,000: 240,000. Check:
               2,200,000 − 1,960,000 = 240,000.
  zone         WIB
  facts        as in cogs_first_issue
  ask          b1.inventory_value   T: 10 Oct 2026   R: 10 Oct 2026 12:00
  result       240,000 IDR
```

## P3. Moving average cost of goods

The paper test only tells the rule. Here it is written out in full. The dates
of the movements are not in the paper test, and are added.

```uniti
module paper/p3@v1

concept Item
concept Movement

choice_list MovementKind, closed
  choices:
    inbound
    outbound

property item : reference Item
property date : date
property kind : choice MovementKind
property amount : number (position)
property price : number (money, position)

applies to Movement:
  item         required
  date         required
  kind         required
  amount       required
  price

helper Item.moving_average : record:
  fold(all(Movement, m: m.item = this),
       order_by: m: m.date,
       initial: {amount: 0, value: 0 IDR, cogs: 0 IDR},
       step: (k, m):
         if m.kind = inbound
         then k with amount = k.amount + m.amount with value = k.value + m.amount × m.price
         else {amount: k.amount − m.amount,
               value: k.value − k.value × m.amount ÷ k.amount,
               cogs: k.cogs + k.value × m.amount ÷ k.amount})

computed Item.stock : number (position), closed:
  this.moving_average.amount

computed Item.inventory_value : number (money, position), closed:
  this.moving_average.value

computed Item.cogs : number (money, increase), closed:
  this.moving_average.cogs

example cogs_after_issue_15
  kind         compute
  title        Cost of goods after issuing 15
  explanation  20 units worth 2,200,000, average 110,000. 15 out:
               15 × 110,000 = 1,650,000.
  zone         WIB
  facts        recorded 20 Oct 2026 09:00
    b1   type     Item          valid 1 Oct 2026
    m1   type     Movement      valid 1 Oct 2026
    m1   item     b1            valid 1 Oct 2026
    m1   date     1 Oct 2026    valid 1 Oct 2026
    m1   kind     inbound       valid 1 Oct 2026
    m1   amount   10            valid 1 Oct 2026
    m1   price    100,000 IDR   valid 1 Oct 2026
    m2   type     Movement      valid 5 Oct 2026
    m2   item     b1            valid 5 Oct 2026
    m2   date     5 Oct 2026    valid 5 Oct 2026
    m2   kind     inbound       valid 5 Oct 2026
    m2   amount   10            valid 5 Oct 2026
    m2   price    120,000 IDR   valid 5 Oct 2026
    m3   type     Movement      valid 7 Oct 2026
    m3   item     b1            valid 7 Oct 2026
    m3   date     7 Oct 2026    valid 7 Oct 2026
    m3   kind     outbound      valid 7 Oct 2026
    m3   amount   15            valid 7 Oct 2026
    m4   type     Movement      valid 12 Oct 2026
    m4   item     b1            valid 12 Oct 2026
    m4   date     12 Oct 2026   valid 12 Oct 2026
    m4   kind     inbound       valid 12 Oct 2026
    m4   amount   5             valid 12 Oct 2026
    m4   price    130,000 IDR   valid 12 Oct 2026
    m5   type     Movement      valid 15 Oct 2026
    m5   item     b1            valid 15 Oct 2026
    m5   date     15 Oct 2026   valid 15 Oct 2026
    m5   kind     outbound      valid 15 Oct 2026
    m5   amount   3             valid 15 Oct 2026
  ask          b1.cogs   T: 10 Oct 2026   R: 20 Oct 2026 12:00
  result       1,650,000 IDR

example final_cogs
  kind         compute
  title        Cost of goods after all movements
  explanation  5 in @130,000: 10 units worth 1,200,000, average 120,000.
               3 out: 360,000. The total is 1,650,000 + 360,000 =
               2,010,000.
  zone         WIB
  facts        as in cogs_after_issue_15
  ask          b1.cogs   T: 16 Oct 2026   R: 20 Oct 2026 12:00
  result       2,010,000 IDR

example final_value
  kind         compute
  title        Inventory value after all movements
  explanation  1,200,000 − 360,000 = 840,000.
  zone         WIB
  facts        as in cogs_after_issue_15
  ask          b1.inventory_value   T: 16 Oct 2026   R: 20 Oct 2026 12:00
  result       840,000 IDR

example final_stock
  kind         compute
  title        Stock after all movements
  explanation  10 + 10 − 15 + 5 − 3 = 7.
  zone         WIB
  facts        as in cogs_after_issue_15
  ask          b1.stock   T: 16 Oct 2026   R: 20 Oct 2026 12:00
  result       7
```

## P4. Stock must not be negative, including future rentals

In the paper test, available stock comes from P1. Here the stock is recorded
directly so that the case stands on its own, minus the rentals that are in
progress.

The paper test expects the rejection to mention 21 October. A rejection
mentions the valid time at which the constraint is read, which is the valid
time of the action; 21 October is a day inside the expression of that
constraint, and does not reach the rejection (finding A30, decision 0047).

```uniti
module paper/p4@v1

concept Item
concept Rental

property stock : number (position)
property item : reference Item
property amount : number (position)
property start_date : date
property end_date : date

applies to Item:
  stock

applies to Rental:
  item         required
  amount       required
  start_date   required
  end_date     required

helper Rental.term : range:
  range(this.start_date, this.end_date)

computed Item.available : number (position), closed:
  this.stock − sum(all(Rental, s: s.item = this and T in s.term), s: s.amount)

constraint Rental.enough_stock
  label.en       Enough stock
  definition.en  The rented item is available every day during the rental
                 term.
  message.en     The stock of this item is not enough for part of the rental
                 term.
  rule:
    all_match(split(this.term, step: 1 day),
              h: at(h, this.item.available) ≥ 0)

example stock_sufficient
  kind         accept
  title        Enough stock every day
  explanation  Stock 5, no other rental yet. A new rental of 2 units for 20 to
               22 October. Afterwards 3 are available on 20 October.
  zone         WIB
  facts        recorded 1 Oct 2026 09:00
    t4   type   Item   valid 1 Oct 2026
    t4   stock  5      valid 1 Oct 2026
  action       recorded 15 Oct 2026 10:00
    r2   type        Rental        valid 15 Oct 2026
    r2   item        t4            valid 15 Oct 2026
    r2   amount      2             valid 15 Oct 2026
    r2   start_date  20 Oct 2026   valid 15 Oct 2026
    r2   end_date    22 Oct 2026   valid 15 Oct 2026
  result       accepted
  ask          t4.available   T: 20 Oct 2026   R: 15 Oct 2026 12:00
  result       3

example stock_short_one_day
  kind         reject
  title        Not enough stock on one day
  explanation  Another rental uses 4 units on 21 October, so only 1 is
               available. A new rental of 2 units for 20 to 22 October is
               rejected, even though the stock is enough on 20 October.
  zone         WIB
  facts        recorded 1 Oct 2026 09:00
    t4   type        Item          valid 1 Oct 2026
    t4   stock       5             valid 1 Oct 2026
    s0   type        Rental        valid 1 Oct 2026
    s0   item        t4            valid 1 Oct 2026
    s0   amount      4             valid 1 Oct 2026
    s0   start_date  21 Oct 2026   valid 1 Oct 2026
    s0   end_date    22 Oct 2026   valid 1 Oct 2026
  action       recorded 15 Oct 2026 10:00
    r2   type        Rental        valid 15 Oct 2026
    r2   item        t4            valid 15 Oct 2026
    r2   amount      2             valid 15 Oct 2026
    r2   start_date  20 Oct 2026   valid 15 Oct 2026
    r2   end_date    22 Oct 2026   valid 15 Oct 2026
  result       rejected by enough_stock, entity r2, at 15 Oct 2026
```
