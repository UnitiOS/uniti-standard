# Subscription

Cases L1 and L2 of the paper test (`uji/01-hitung.md`<!-- ARCHIVE-LINK: ../../01-hitung.md -->
§4.E), written in the reference notation.

## L1. Moving up a plan in the middle of a period

The paper test also asks for the shortfall of the bill. Here the bill that
was already sent is recorded as a fact, and the shortfall is computed.

```uniti
module paper/l1@v1

concept Plan
concept Subscription
concept Bill

property monthly_price : number (money, position)
property plan : reference Plan
property subscription : reference Subscription
property date : date
property amount : number (money, increase)

applies to Plan:
  monthly_price  required

applies to Subscription:
  plan         required

applies to Bill:
  subscription required
  date         required
  amount       required

computed Subscription.charge(period) : number (money, increase), closed:
  sum(history(this.plan, in: period),
      r: r.value.monthly_price × span(overlap(r.range, period), day)
         ÷ span(period, day))

computed Subscription.shortfall(period) : number (money, increase), closed:
  this.charge(period)
  − sum(all(Bill, t: t.subscription = this and t.date in period), t: t.amount)

example november_charge
  kind         compute
  title        November charge with a plan upgrade
  explanation  The Basic plan is 300,000 a month, moving up to Pro at 600,000
               from 16 November. 15/30 × 300,000 + 15/30 × 600,000 = 450,000.
  zone         WIB
  facts        recorded 16 Nov 2026 10:00
    basic     type             Plan           valid 1 Jan 2026
    basic     monthly_price    300,000 IDR    valid 1 Jan 2026
    pro       type             Plan           valid 1 Jan 2026
    pro       monthly_price    600,000 IDR    valid 1 Jan 2026
    s1        type             Subscription   valid 1 Oct 2026
    f1: s1    plan             basic          valid 1 Oct 2026
    f2: s1    plan             pro            valid 16 Nov 2026   replaces f1
    t1        type             Bill           valid 1 Nov 2026
    t1        subscription     s1             valid 1 Nov 2026
    t1        date             1 Nov 2026     valid 1 Nov 2026
    t1        amount           300,000 IDR    valid 1 Nov 2026
  ask          s1.charge(range(1 Nov 2026, 1 Dec 2026))   T: 30 Nov 2026   R: 1 Dec 2026
  result       450,000 IDR

example november_shortfall
  kind         compute
  title        Shortfall of the November bill
  explanation  300,000 was already billed on 1 November: 450,000 − 300,000 =
               150,000.
  zone         WIB
  facts        as in november_charge
  ask          s1.shortfall(range(1 Nov 2026, 1 Dec 2026))   T: 30 Nov 2026   R: 1 Dec 2026
  result       150,000 IDR
```

## L2. Tiered usage price

The rule is the same as G1 in [`04-payroll.md`](04-payroll.md); only the
content of the tiers is different. The first tier has rate 0.

```uniti
module paper/l2@v1

concept Customer
concept PriceTable
concept RateTier

property usage : number (position)
property price_table : reference PriceTable
property table : reference PriceTable
property lower_limit : number (position)
property upper_limit : number (position)
property rate : number (money, position)

applies to Customer:
  usage
  price_table  required

applies to RateTier:
  table        required
  lower_limit  required
  upper_limit
  rate         required

computed Customer.bill : number (money, increase), closed:
  let n = this.usage
  sum(all(RateTier, l: l.table = this.price_table),
      l: max(0, (if exists(l.upper_limit) then min(n, l.upper_limit)
                 else n) − l.lower_limit) × l.rate)

example usage_25_thousand
  kind         compute
  title        Bill for 25,000 calls
  explanation  The first 1,000 are free, the next 9,000 at 5, and the
               remaining 15,000 at 3: 45,000 + 45,000 = 90,000.
  zone         WIB
  facts        recorded 1 Nov 2026 09:00
    pt    type         PriceTable   valid 1 Jan 2026
    l1    type         RateTier     valid 1 Jan 2026
    l1    table        pt           valid 1 Jan 2026
    l1    lower_limit  0            valid 1 Jan 2026
    l1    upper_limit  1,000        valid 1 Jan 2026
    l1    rate         0 IDR        valid 1 Jan 2026
    l2    type         RateTier     valid 1 Jan 2026
    l2    table        pt           valid 1 Jan 2026
    l2    lower_limit  1,000        valid 1 Jan 2026
    l2    upper_limit  10,000       valid 1 Jan 2026
    l2    rate         5 IDR        valid 1 Jan 2026
    l3    type         RateTier     valid 1 Jan 2026
    l3    table        pt           valid 1 Jan 2026
    l3    lower_limit  10,000       valid 1 Jan 2026
    l3    rate         3 IDR        valid 1 Jan 2026
    p1    type         Customer     valid 1 Oct 2026
    p1    price_table  pt           valid 1 Oct 2026
    p1    usage        25,000       valid 31 Oct 2026
  ask          p1.bill   T: 31 Oct 2026   R: 1 Nov 2026 12:00
  result       90,000 IDR
```
