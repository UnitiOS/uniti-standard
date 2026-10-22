# Finance and accounting

Cases K1 to K6 from the paper test (Indonesian archive, `uji/01-hitung.md`
§4.A), written in the reference notation with the core and the calculation
library. Each case has its own module, `paper/‹case›@v1`. The expected results
are taken from the paper test, not from the output of the calculator
(PROOF-12).

## K1. Cash balance, read at two times

Receipts and expenditures use two properties, because their direction differs
and the direction is written on the property card. In the paper test both are
named `amount`.

```uniti
module paper/k1@v1

concept Cash
concept Receipt
concept Expenditure

property cash : reference Cash
property inflow : number (money, increase)
property outflow : number (money, decrease)

applies to Receipt:
  cash         required
  inflow       required

applies to Expenditure:
  cash         required
  outflow      required

computed Cash.balance : number (money, position), closed:
  sum(all(Receipt, p: p.cash = this), p: p.inflow)
  − sum(all(Expenditure, k: k.cash = this), k: k.outflow)

example balance_per_records_7_oct
  kind         compute
  title        Balance of 6 October according to the records of 7 October
  explanation  The expenditure of 3 October was only recorded on 8 October, so
               on 7 October it is not yet known: 5,000,000 + 750,000 =
               5,750,000.
  zone         WIB
  facts
    main_cash  type     Cash            valid 1 Oct 2026   recorded 1 Oct 2026 08:00
    m1         type     Receipt         valid 1 Oct 2026   recorded 1 Oct 2026 17:00
    m1         cash     main_cash       valid 1 Oct 2026   recorded 1 Oct 2026 17:00
    m1         inflow   5,000,000 IDR   valid 1 Oct 2026   recorded 1 Oct 2026 17:00
    k1         type     Expenditure     valid 3 Oct 2026   recorded 8 Oct 2026 10:00
    k1         cash     main_cash       valid 3 Oct 2026   recorded 8 Oct 2026 10:00
    k1         outflow  1,200,000 IDR   valid 3 Oct 2026   recorded 8 Oct 2026 10:00
    m2         type     Receipt         valid 5 Oct 2026   recorded 5 Oct 2026 17:00
    m2         cash     main_cash       valid 5 Oct 2026   recorded 5 Oct 2026 17:00
    m2         inflow   750,000 IDR     valid 5 Oct 2026   recorded 5 Oct 2026 17:00
    k2         type     Expenditure     valid 9 Oct 2026   recorded 9 Oct 2026 17:00
    k2         cash     main_cash       valid 9 Oct 2026   recorded 9 Oct 2026 17:00
    k2         outflow  300,000 IDR     valid 9 Oct 2026   recorded 9 Oct 2026 17:00
  ask          main_cash.balance   T: 6 Oct 2026   R: 7 Oct 2026 12:00
  result       5,750,000 IDR

example balance_per_records_8_oct
  kind         compute
  title        Balance of 6 October according to the records of 8 October
  explanation  After the expenditure of 3 October is recorded, the balance on
               the same day changes: 5,750,000 − 1,200,000 = 4,550,000.
  zone         WIB
  facts        as in balance_per_records_7_oct
  ask          main_cash.balance   T: 6 Oct 2026   R: 8 Oct 2026 12:00
  result       4,550,000 IDR

example balance_10_oct
  kind         compute
  title        Balance of 10 October
  explanation  All events have happened and been recorded: 5,000,000 −
               1,200,000 + 750,000 − 300,000 = 4,250,000.
  zone         WIB
  facts        as in balance_per_records_7_oct
  ask          main_cash.balance   T: 10 Oct 2026   R: 10 Oct 2026 12:00
  result       4,250,000 IDR
```

## K2. Revenue in rupiah from several currencies

As in the paper test, the rate is chosen with
`k.from_unit = unit_of(p.price)`. The source and target currencies of a rate
are choices from the unit code list `uniti/unit/Unit`
([`content/code-lists.md`](../content/code-lists.md)). The value of a rate has
the unit target currency per source currency, for example 16,200 IDR/USD. The
currency is converted with `convert_money` from the calculation library, which
reads the rate only when the currencies differ.

```uniti
module paper/k2@v1
  uses uniti/calc@v1
  uses uniti/unit@v1

concept Organization
concept Sale
concept ExchangeRate

property date : date
property price : number (money, increase)
property from_unit : choice Unit
property to_unit : choice Unit
property value : number (money/money, position)

applies to Sale:
  date         required
  price        required

applies to ExchangeRate:
  from_unit    required
  to_unit      required
  value        required

helper Sale.rate : reference ExchangeRate:
  single(all(ExchangeRate, k: k.from_unit = unit_of(this.price) and k.to_unit = IDR))

helper Sale.in_rupiah : number:
  convert_money(this.price, IDR, at(this.date, this.rate.value))

computed Organization.revenue(period) : number (money, increase), closed:
  sum(all(Sale, p: p.date in period), p: p.in_rupiah)

example october_revenue
  kind         compute
  title        October revenue in rupiah
  explanation  100 × 16,200 + 50 × 16,300 + 1,000,000 = 3,435,000. The rate was
               replaced with 16,300 from 5 October, and the sale in rupiah does
               not need a rate.
  zone         WIB
  facts        recorded 31 Oct 2026 18:00
    org      type       Organization       valid 1 Sep 2026
    usd      type       ExchangeRate       valid 1 Oct 2026
    usd      from_unit  USD                valid 1 Oct 2026
    usd      to_unit    IDR                valid 1 Oct 2026
    f1: usd  value      16,200 IDR/USD     valid 1 Oct 2026
    f2: usd  value      16,300 IDR/USD     valid 5 Oct 2026   replaces f1
    p1       type       Sale               valid 3 Oct 2026
    p1       date       3 Oct 2026         valid 3 Oct 2026
    p1       price      100 USD            valid 3 Oct 2026
    p2       type       Sale               valid 7 Oct 2026
    p2       date       7 Oct 2026         valid 7 Oct 2026
    p2       price      50 USD             valid 7 Oct 2026
    p3       type       Sale               valid 8 Oct 2026
    p3       date       8 Oct 2026         valid 8 Oct 2026
    p3       price      1,000,000 IDR      valid 8 Oct 2026
    p4       type       Sale               valid 30 Sep 2026
    p4       date       30 Sep 2026        valid 30 Sep 2026
    p4       price      10 USD             valid 30 Sep 2026
  ask          org.revenue(range(1 Oct 2026, 1 Nov 2026))   T: 31 Oct 2026   R: 1 Nov 2026
  result       3,435,000 IDR

example september_revenue
  kind         compute
  title        September revenue cannot be computed yet
  explanation  The sale of 30 September is 10 USD, but the rate only exists
               from 1 October. The result is not computable because the rate
               is not single, not 0.
  zone         WIB
  facts        as in october_revenue
  ask          org.revenue(range(1 Sep 2026, 1 Oct 2026))   T: 30 Sep 2026   R: 1 Nov 2026
  result       not computable: not single
```

## K3. A journal must balance

In the paper test every line has a debit and a credit. A line that has only
one of them makes the other empty, and an empty value that is summed is not
computable (06 §2.9), so every journal would be rejected. Here every line has
a side and an amount.

```uniti
module paper/k3@v1

concept Journal
concept JournalLine

choice_list Side, closed
  choices:
    debit
    credit

property journal : reference Journal
property side : choice Side
property amount : number (money, increase)

applies to JournalLine:
  journal      required
  side         required
  amount       required

constraint Journal.balanced:
  sum(all(JournalLine, b: b.journal = this and b.side = debit), b: b.amount)
  = sum(all(JournalLine, b: b.journal = this and b.side = credit), b: b.amount)

example balanced_journal
  kind         accept
  title        Sales journal with PPN
  explanation  Debit cash 1,110,000; credit revenue 1,000,000 and PPN
               110,000. Debit and credit are equal.
  zone         WIB
  facts        recorded 1 Oct 2026 09:00
  action       recorded 5 Oct 2026 10:00
    j1   type     Journal         valid 5 Oct 2026
    b1   type     JournalLine     valid 5 Oct 2026
    b1   journal  j1              valid 5 Oct 2026
    b1   side     debit           valid 5 Oct 2026
    b1   amount   1,110,000 IDR   valid 5 Oct 2026
    b2   type     JournalLine     valid 5 Oct 2026
    b2   journal  j1              valid 5 Oct 2026
    b2   side     credit          valid 5 Oct 2026
    b2   amount   1,000,000 IDR   valid 5 Oct 2026
    b3   type     JournalLine     valid 5 Oct 2026
    b3   journal  j1              valid 5 Oct 2026
    b3   side     credit          valid 5 Oct 2026
    b3   amount   110,000 IDR     valid 5 Oct 2026
  result       accepted

example unbalanced_journal
  kind         reject
  title        PPN typo
  explanation  The PPN is written as 100,000, so the credit is 1,100,000 and
               the debit is 1,110,000.
  zone         WIB
  facts        recorded 1 Oct 2026 09:00
  action       recorded 5 Oct 2026 10:00
    j1   type     Journal         valid 5 Oct 2026
    b1   type     JournalLine     valid 5 Oct 2026
    b1   journal  j1              valid 5 Oct 2026
    b1   side     debit           valid 5 Oct 2026
    b1   amount   1,110,000 IDR   valid 5 Oct 2026
    b2   type     JournalLine     valid 5 Oct 2026
    b2   journal  j1              valid 5 Oct 2026
    b2   side     credit          valid 5 Oct 2026
    b2   amount   1,000,000 IDR   valid 5 Oct 2026
    b3   type     JournalLine     valid 5 Oct 2026
    b3   journal  j1              valid 5 Oct 2026
    b3   side     credit          valid 5 Oct 2026
    b3   amount   100,000 IDR     valid 5 Oct 2026
  result       rejected by balanced, entity j1
```

## K4. Straight-line depreciation

`allocate` from the library accepts a collection of records
`{member, weight}`. Here the members are the months from `split`, each with
weight 1, and the remainder goes to the last month.

```uniti
module paper/k4@v1
  uses uniti/calc@v1

concept Asset

property price : number (money, position)
property residual_value : number (money, position)
property lifespan : number (duration, position)
property start_of_use : date

applies to Asset:
  price           required
  residual_value  required
  lifespan        required
  start_of_use    required

helper Asset.depreciation : collection:
  allocate(this.price − this.residual_value,
           each(split(range(this.start_of_use, this.start_of_use + this.lifespan), step: 1 month),
                b: {member: b, weight: 1}),
           1 IDR, last)

computed Asset.depreciation_this_month : number (money, increase), closed:
  sum(this.depreciation, p: if T in p.member then p.share else 0 IDR)

computed Asset.accumulated_depreciation : number (money, position), closed:
  sum(this.depreciation, p: if p.member.start ≤ T then p.share else 0 IDR)

computed Asset.book_value : number (money, position), closed:
  this.price − this.accumulated_depreciation

example accumulated_march
  kind         compute
  title        Accumulated depreciation as of 31 March
  explanation  12,000,000 ÷ 36 = 333,333.33…, rounded down to 333,333 a month.
               Three months have started: 999,999.
  zone         WIB
  facts        recorded 2 Jan 2026 09:00
    a1   type            Asset            valid 1 Jan 2026
    a1   price           12,000,000 IDR   valid 1 Jan 2026
    a1   residual_value  0 IDR            valid 1 Jan 2026
    a1   lifespan        36 months        valid 1 Jan 2026
    a1   start_of_use    1 Jan 2026       valid 1 Jan 2026
  ask          a1.accumulated_depreciation   T: 31 Mar 2026   R: 31 Mar 2026
  result       999,999 IDR

example book_value_june
  kind         compute
  title        Book value as of 30 June
  explanation  Six months have started: 12,000,000 − 6 × 333,333 =
               10,000,002.
  zone         WIB
  facts        as in accumulated_march
  ask          a1.book_value   T: 30 Jun 2026   R: 30 Jun 2026
  result       10,000,002 IDR

example first_month_depreciation
  kind         compute
  title        Depreciation of the first month
  explanation  Months 1 to 35 are 333,333 each.
  zone         WIB
  facts        as in accumulated_march
  ask          a1.depreciation_this_month   T: 15 Jan 2026   R: 15 Jan 2026
  result       333,333 IDR

example last_month_depreciation
  kind         compute
  title        The last month's depreciation receives the remainder
  explanation  Month 36, December 2028: 12,000,000 − 35 × 333,333 = 333,345,
               so the sum of the 36 months is exactly 12,000,000.
  zone         WIB
  facts        as in accumulated_march
  ask          a1.depreciation_this_month   T: 15 Dec 2028   R: 15 Dec 2028
  result       333,345 IDR
```

## K5. Cost allocation by area

The departments are ordered with `by_member` before they are divided, because
`allocate` needs an ordered list.

```uniti
module paper/k5@v1
  uses uniti/calc@v1

concept Cost
concept Department

property amount : number (money, increase)
property area : number (length², position)

applies to Cost:
  amount       required

applies to Department:
  area         required

helper Cost.allocation : collection:
  allocate(this.amount,
           by_member(each(all(Department), d: {member: d, weight: d.area})),
           1 IDR, largest_fraction)

computed Cost.department_share(department) : number (money, increase), closed:
  sum(this.allocation, b: if b.member = department then b.share else 0 IDR)

computed Cost.allocated : number (money, increase), closed:
  sum(this.allocation, b: b.share)

example department_a_share
  kind         compute
  title        Share of department A
  explanation  Rent of 10,000,000 divided by areas of 120, 80, and 100 m².
               A: 10,000,000 × 120 ÷ 300 = 4,000,000 exactly.
  zone         WIB
  facts        recorded 31 Oct 2026 09:00
    rent_oct  type    Cost             valid 1 Oct 2026
    rent_oct  amount  10,000,000 IDR   valid 1 Oct 2026
    a         type    Department       valid 1 Jan 2026
    a         area    120 m²           valid 1 Jan 2026
    b         type    Department       valid 1 Jan 2026
    b         area    80 m²            valid 1 Jan 2026
    c         type    Department       valid 1 Jan 2026
    c         area    100 m²           valid 1 Jan 2026
  ask          rent_oct.department_share(a)   T: 31 Oct 2026   R: 31 Oct 2026 12:00
  result       4,000,000 IDR

example department_b_share
  kind         compute
  title        Department B receives the remainder
  explanation  B: 2,666,666.67, rounded down 2,666,666. The remainder of 1
               rupiah goes to B, because its fraction (0.67) is the largest.
  zone         WIB
  facts        as in department_a_share
  ask          rent_oct.department_share(b)   T: 31 Oct 2026   R: 31 Oct 2026 12:00
  result       2,666,667 IDR

example department_c_share
  kind         compute
  title        Share of department C
  explanation  C: 3,333,333.33, rounded down 3,333,333.
  zone         WIB
  facts        as in department_a_share
  ask          rent_oct.department_share(c)   T: 31 Oct 2026   R: 31 Oct 2026 12:00
  result       3,333,333 IDR

example no_remainder_lost
  kind         compute
  title        The sum of the shares is exactly equal to the cost
  explanation  4,000,000 + 2,666,667 + 3,333,333 = 10,000,000. If each share
               is rounded on its own, the sum is 9,999,999 or 10,000,001.
  zone         WIB
  facts        as in department_a_share
  ask          rent_oct.allocated   T: 31 Oct 2026   R: 31 Oct 2026 12:00
  result       10,000,000 IDR

example tie_remainder_to_earlier
  kind         compute
  title        Boundary: equal fractions, the remainder goes to the earlier department
  explanation  Three departments of equal area: each 3,333,333.33, and the
               fractions are equal. The remainder of 1 rupiah is given by the
               tie-breaker (06 §2.6): C is valid earlier, so C receives it,
               even though its name is last in the order.
  zone         WIB
  facts        recorded 31 Oct 2026 09:00
    rent_oct  type    Cost             valid 1 Oct 2026
    rent_oct  amount  10,000,000 IDR   valid 1 Oct 2026
    a         type    Department       valid 1 Jan 2026
    a         area    100 m²           valid 1 Jan 2026
    b         type    Department       valid 1 Jan 2026
    b         area    100 m²           valid 1 Jan 2026
    c         type    Department       valid 1 Jan 2025
    c         area    100 m²           valid 1 Jan 2025
  ask          rent_oct.department_share(c)   T: 31 Oct 2026   R: 31 Oct 2026 12:00
  result       3,333,334 IDR

example tie_other_gets_no_remainder
  kind         compute
  title        Boundary: another department with an equal fraction
  explanation  A does not receive the remainder: 3,333,333.
  zone         WIB
  facts        as in tie_remainder_to_earlier
  ask          rent_oct.department_share(a)   T: 31 Oct 2026   R: 31 Oct 2026 12:00
  result       3,333,333 IDR
```

## K6. Gradual revenue recognition

The same as K4: a monthly `split`, `allocate` with the remainder to the last
month, then summed for the months that have started at *T*.

```uniti
module paper/k6@v1
  uses uniti/calc@v1

concept Contract

property value : number (money, position)
property start_date : date
property term : number (duration, position)

applies to Contract:
  value        required
  start_date   required
  term         required

helper Contract.schedule : collection:
  allocate(this.value,
           each(split(range(this.start_date, this.start_date + this.term), step: 1 month),
                b: {member: b, weight: 1}),
           1 IDR, last)

computed Contract.revenue_this_month : number (money, increase), closed:
  sum(this.schedule, p: if T in p.member then p.share else 0 IDR)

computed Contract.recognized : number (money, position), closed:
  sum(this.schedule, p: if p.member.start ≤ T then p.share else 0 IDR)

computed Contract.unrecognized : number (money, position), closed:
  this.value − this.recognized

example recognized_june
  kind         compute
  title        Revenue recognized as of 30 June
  explanation  10,000,000 ÷ 12 = 833,333.33…, rounded down to 833,333.
               February to June have started: 5 × 833,333 = 4,166,665.
  zone         WIB
  facts        recorded 1 Feb 2026 09:00
    l1   type        Contract         valid 1 Feb 2026
    l1   value       10,000,000 IDR   valid 1 Feb 2026
    l1   start_date  1 Feb 2026       valid 1 Feb 2026
    l1   term        12 months        valid 1 Feb 2026
  ask          l1.recognized   T: 30 Jun 2026   R: 30 Jun 2026
  result       4,166,665 IDR

example unrecognized_june
  kind         compute
  title        Revenue not yet recognized as of 30 June
  explanation  10,000,000 − 4,166,665 = 5,833,335. This is revenue received in
               advance if the whole contract has been paid up front.
  zone         WIB
  facts        as in recognized_june
  ask          l1.unrecognized   T: 30 Jun 2026   R: 30 Jun 2026
  result       5,833,335 IDR

example ordinary_month_revenue
  kind         compute
  title        Revenue of one month
  explanation  The first to the eleventh month are 833,333 each.
  zone         WIB
  facts        as in recognized_june
  ask          l1.revenue_this_month   T: 15 Feb 2026   R: 15 Feb 2026
  result       833,333 IDR

example last_month_revenue
  kind         compute
  title        The last month receives the remainder
  explanation  January 2027: 10,000,000 − 11 × 833,333 = 833,337.
  zone         WIB
  facts        as in recognized_june
  ask          l1.revenue_this_month   T: 15 Jan 2027   R: 15 Jan 2027
  result       833,337 IDR
```
