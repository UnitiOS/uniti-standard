# Loans

Cases J1 to J3 of the paper test (`uji/01-hitung.md`<!-- ARCHIVE-LINK: ../../01-hitung.md -->
§4.F), written in the reference notation with the core and the calculation
library.

## J1. Compound interest

`power` in the core is only for integer powers, so the tenor is an integer
without a unit.

```uniti
module paper/j1@v1
  uses uniti/calc@v1

concept Loan

property principal : number (money, level)
property monthly_interest : number (level)
property tenor_months : number (level)

applies to Loan:
  principal         required
  monthly_interest  required
  tenor_months      required

computed Loan.final_value : number (money, level), closed:
  round(this.principal × power(1 + this.monthly_interest, this.tenor_months), 1 IDR, nearest)

example compound_one_year
  kind         compute
  title        Interest of 1% a month for 12 months
  explanation  10,000,000 × 1.01¹² = 11,268,250.30…, rounded to 11,268,250.
  zone         WIB
  facts        recorded 1 Jan 2026 09:00
    p1   type              Loan             valid 1 Jan 2026
    p1   principal         10,000,000 IDR   valid 1 Jan 2026
    p1   monthly_interest  1%               valid 1 Jan 2026
    p1   tenor_months      12               valid 1 Jan 2026
  ask          p1.final_value   T: 1 Jan 2026   R: 1 Jan 2026 12:00
  result       11,268,250 IDR
```

## J2. Daily interest on a changing balance

The balance is a computed property, read for each day with `at`. The period of
October is the range from 1 October up to before 1 November.

```uniti
module paper/j2@v1
  uses uniti/calc@v1

concept Loan
concept Payment

property principal : number (money, level)
property annual_interest : number (level)
property loan : reference Loan
property amount : number (money, decrease)

applies to Loan:
  principal         required
  annual_interest   required

applies to Payment:
  loan         required
  amount       required

computed Loan.balance : number (money, level), closed:
  this.principal − sum(all(Payment, b: b.loan = this), b: b.amount)

computed Loan.interest(period) : number (money, increase), closed:
  round(sum(split(period, step: 1 day),
            h: at(h, this.balance) × this.annual_interest ÷ 365),
        1 IDR, nearest)

example interest_october
  kind         compute
  title        Interest of October
  explanation  Balance 10,000,000 for 10 days, then 8,000,000 for 21 days
               after 2,000,000 is paid on 11 October.
               (10,000,000 × 10 + 8,000,000 × 21) × 0.12 ÷ 365 =
               88,109.589…, rounded to 88,110.
  zone         WIB
  facts        recorded 11 Oct 2026 15:00
    p1   type             Loan             valid 1 Oct 2026
    p1   principal        10,000,000 IDR   valid 1 Oct 2026
    p1   annual_interest  12%              valid 1 Oct 2026
    b1   type             Payment          valid 11 Oct 2026
    b1   loan             p1               valid 11 Oct 2026
    b1   amount           2,000,000 IDR    valid 11 Oct 2026
  ask          p1.interest(range(1 Oct 2026, 1 Nov 2026))   T: 31 Oct 2026   R: 1 Nov 2026
  result       88,110 IDR
```

## J3. Payment goes to the oldest installment first

The paper test only tells the rule. Here it is written out in full: `fold`
over the payments by date, and each payment is distributed with a `fold`
inside it, over the installments by due date. The installment remainders are
kept as a collection of records `{installment, remaining}`.

```uniti
module paper/j3@v1

concept Loan
concept Installment
concept Payment

property loan : reference Loan
property due_date : date
property date : date
property amount : number (money, level)

applies to Installment:
  loan         required
  due_date     required
  amount       required

applies to Payment:
  loan         required
  date         required
  amount       required

helper Loan.installment_balances : collection:
  fold(all(Payment, b: b.loan = this),
       order_by: b: b.date,
       initial: fold(all(Installment, c: c.loan = this),
                     order_by: c: c.due_date,
                     initial: [],
                     step: (s, c): append(s, {installment: c, remaining: c.amount})),
       step: (entries, b): apply_payment(entries, b.amount))

helper apply_payment(entries, n) : collection:
  fold(entries,
       initial: {cash: n, rows: []},
       step: (a, d):
         let take = min(d.remaining, a.cash)
         {cash: a.cash − take, rows: append(a.rows, d with remaining = d.remaining − take)}
  ).rows

computed Installment.remaining : number (money, level), closed:
  sum(this.loan.installment_balances, d: if d.installment = this then d.remaining else 0 IDR)

example c1_paid_off
  kind         compute
  title        The oldest installment is paid off first
  explanation  The payment of 1,500,000 on 5 October pays off C1 and
               500,000 of C2.
  zone         WIB
  facts        recorded 20 Oct 2026 15:00
    p1   type      Loan            valid 1 Aug 2026
    c1   type      Installment     valid 1 Aug 2026
    c1   loan      p1              valid 1 Aug 2026
    c1   due_date  1 Sep 2026      valid 1 Aug 2026
    c1   amount    1,000,000 IDR   valid 1 Aug 2026
    c2   type      Installment     valid 1 Aug 2026
    c2   loan      p1              valid 1 Aug 2026
    c2   due_date  1 Oct 2026      valid 1 Aug 2026
    c2   amount    1,000,000 IDR   valid 1 Aug 2026
    c3   type      Installment     valid 1 Aug 2026
    c3   loan      p1              valid 1 Aug 2026
    c3   due_date  1 Nov 2026      valid 1 Aug 2026
    c3   amount    1,000,000 IDR   valid 1 Aug 2026
    b1   type      Payment         valid 5 Oct 2026
    b1   loan      p1              valid 5 Oct 2026
    b1   date      5 Oct 2026      valid 5 Oct 2026
    b1   amount    1,500,000 IDR   valid 5 Oct 2026
    b2   type      Payment         valid 20 Oct 2026
    b2   loan      p1              valid 20 Oct 2026
    b2   date      20 Oct 2026     valid 20 Oct 2026
    b2   amount    800,000 IDR     valid 20 Oct 2026
  ask          c1.remaining   T: 10 Oct 2026   R: 20 Oct 2026 16:00
  result       0 IDR

example c2_remaining_after_first_payment
  kind         compute
  title        Remainder of C2 after the first payment
  explanation  1,500,000 − 1,000,000 for C1 = 500,000 for C2, remaining
               500,000.
  zone         WIB
  facts        as in c1_paid_off
  ask          c2.remaining   T: 10 Oct 2026   R: 20 Oct 2026 16:00
  result       500,000 IDR

example c2_paid_off_after_second_payment
  kind         compute
  title        C2 paid off after the second payment
  explanation  The payment of 800,000 on 20 October pays off the remainder of
               C2, 500,000.
  zone         WIB
  facts        as in c1_paid_off
  ask          c2.remaining   T: 25 Oct 2026   R: 20 Oct 2026 16:00
  result       0 IDR

example c3_remaining_after_second_payment
  kind         compute
  title        C3 is also paid in part before its due date
  explanation  The remaining 300,000 of the second payment goes to C3, which is
               not yet due: 1,000,000 − 300,000 = 700,000.
  zone         WIB
  facts        as in c1_paid_off
  ask          c3.remaining   T: 25 Oct 2026   R: 20 Oct 2026 16:00
  result       700,000 IDR
```
