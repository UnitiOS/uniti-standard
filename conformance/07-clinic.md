# Clinic

Cases C1 and C2 of the paper test (Indonesian archive, `uji/01-hitung.md`
§4.G), written in the reference notation with the core and the calculation
library. The rule of C1 is the same as the clinic example in
[`00-form-examples.md`](00-form-examples.md); here the month of the claim
follows the paper test.

## C1. Insurance coverage with an annual cap

```uniti
module paper/c1@v1

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

helper Policy.payouts : collection:
  fold(all(Claim, k: k.policy = this
                    and k.date in range(this.start_date, this.end_date)),
       order_by: k: k.date,
       initial: {cap_left: this.cap, paid: []},
       step: (a, k):
         let b = min(k.amount × 80%, a.cap_left)
         {cap_left: a.cap_left − b,
          paid: append(a.paid, {claim: k, amount: b})}
  ).paid

computed Claim.paid_out : number (money, increase), closed:
  sum(this.policy.payouts, b: if b.claim = this then b.amount else 0 IDR)

example claim_february
  kind         compute
  title        The first claim is covered 80%
  explanation  A claim of 5,000,000 in February: 80% = 4,000,000. The cap is
               down to 6,000,000.
  zone         WIB
  facts        recorded 20 Oct 2026 09:00
    p1   type        Policy           valid 1 Jan 2026
    p1   start_date  1 Jan 2026       valid 1 Jan 2026
    p1   end_date    1 Jan 2027       valid 1 Jan 2026
    p1   cap         10,000,000 IDR   valid 1 Jan 2026
    k1   type        Claim            valid 10 Feb 2026
    k1   policy      p1               valid 10 Feb 2026
    k1   date        10 Feb 2026      valid 10 Feb 2026
    k1   amount      5,000,000 IDR    valid 10 Feb 2026
    k2   type        Claim            valid 15 May 2026
    k2   policy      p1               valid 15 May 2026
    k2   date        15 May 2026      valid 15 May 2026
    k2   amount      6,000,000 IDR    valid 15 May 2026
    k3   type        Claim            valid 20 Aug 2026
    k3   policy      p1               valid 20 Aug 2026
    k3   date        20 Aug 2026      valid 20 Aug 2026
    k3   amount      3,000,000 IDR    valid 20 Aug 2026
    k4   type        Claim            valid 5 Oct 2026
    k4   policy      p1               valid 5 Oct 2026
    k4   date        5 Oct 2026       valid 5 Oct 2026
    k4   amount      1,000,000 IDR    valid 5 Oct 2026
  ask          k1.paid_out   T: 31 Oct 2026   R: 31 Oct 2026
  result       4,000,000 IDR

example claim_may
  kind         compute
  title        The second claim is still under the cap
  explanation  A claim of 6,000,000 in May: 80% = 4,800,000, still under the
               remaining cap of 6,000,000. The cap is down to 1,200,000.
  zone         WIB
  facts        as in claim_february
  ask          k2.paid_out   T: 31 Oct 2026   R: 31 Oct 2026
  result       4,800,000 IDR

example claim_august
  kind         compute
  title        The third claim is paid the remaining cap
  explanation  A claim of 3,000,000 in August: 80% = 2,400,000, but the
               remaining cap is only 1,200,000.
  zone         WIB
  facts        as in claim_february
  ask          k3.paid_out   T: 31 Oct 2026   R: 31 Oct 2026
  result       1,200,000 IDR

example claim_october
  kind         compute
  title        The cap is used up
  explanation  A claim of 1,000,000 in October is paid 0.
  zone         WIB
  facts        as in claim_february
  ask          k4.paid_out   T: 31 Oct 2026   R: 31 Oct 2026
  result       0 IDR
```

## C2. Patient waiting time

`median` and `average` are library helpers, and a helper does not accept
bindings. The waiting time of each visit is first formed with `each`.

```uniti
module paper/c2@v1
  uses uniti/calc@v1

concept Clinic
concept Visit

property clinic : reference Clinic
property arrived : instant
property called : instant

applies to Visit:
  clinic       required
  arrived      required
  called

helper Clinic.waiting_times(period) : collection:
  each(all(Visit, k: k.clinic = this and k.arrived in period),
       k: difference(k.arrived, k.called, minute))

computed Clinic.waiting_time_median(period) : number (duration, position), closed:
  median(this.waiting_times(period))

computed Clinic.waiting_time_average(period) : number (duration, position), closed:
  average(this.waiting_times(period))

example median_five_visits
  kind         compute
  title        Median waiting time
  explanation  Waiting times of 10, 25, 15, 40, and 20 minutes. Sorted 10, 15,
               20, 25, 40; the middle value is 20 minutes.
  zone         WIB
  facts        recorded 9 Oct 2026 17:00
    cl   type    Clinic                 valid 1 Jan 2026
    v1   type    Visit                  valid 9 Oct 2026
    v1   clinic  cl                     valid 9 Oct 2026
    v1   arrived 9 Oct 2026 08:00       valid 9 Oct 2026
    v1   called  9 Oct 2026 08:10       valid 9 Oct 2026
    v2   type    Visit                  valid 9 Oct 2026
    v2   clinic  cl                     valid 9 Oct 2026
    v2   arrived 9 Oct 2026 08:20       valid 9 Oct 2026
    v2   called  9 Oct 2026 08:45       valid 9 Oct 2026
    v3   type    Visit                  valid 9 Oct 2026
    v3   clinic  cl                     valid 9 Oct 2026
    v3   arrived 9 Oct 2026 09:00       valid 9 Oct 2026
    v3   called  9 Oct 2026 09:15       valid 9 Oct 2026
    v4   type    Visit                  valid 9 Oct 2026
    v4   clinic  cl                     valid 9 Oct 2026
    v4   arrived 9 Oct 2026 09:30       valid 9 Oct 2026
    v4   called  9 Oct 2026 10:10       valid 9 Oct 2026
    v5   type    Visit                  valid 9 Oct 2026
    v5   clinic  cl                     valid 9 Oct 2026
    v5   arrived 9 Oct 2026 10:30       valid 9 Oct 2026
    v5   called  9 Oct 2026 10:50       valid 9 Oct 2026
  ask          cl.waiting_time_median(range(1 Oct 2026, 1 Nov 2026))   T: 31 Oct 2026   R: 31 Oct 2026
  result       20 minutes

example average_five_visits
  kind         compute
  title        Average waiting time
  explanation  (10 + 25 + 15 + 40 + 20) ÷ 5 = 22 minutes.
  zone         WIB
  facts        as in median_five_visits
  ask          cl.waiting_time_average(range(1 Oct 2026, 1 Nov 2026))   T: 31 Oct 2026   R: 31 Oct 2026
  result       22 minutes

example median_six_visits
  kind         compute
  title        Boundary: median for an even number of data
  explanation  The sixth visit waits 30 minutes. Sorted 10, 15, 20, 25, 30,
               40; the median is the average of the two middle values:
               (20 + 25) ÷ 2 = 22.5 minutes.
  zone         WIB
  facts        recorded 9 Oct 2026 17:00
    cl   type    Clinic                 valid 1 Jan 2026
    v1   type    Visit                  valid 9 Oct 2026
    v1   clinic  cl                     valid 9 Oct 2026
    v1   arrived 9 Oct 2026 08:00       valid 9 Oct 2026
    v1   called  9 Oct 2026 08:10       valid 9 Oct 2026
    v2   type    Visit                  valid 9 Oct 2026
    v2   clinic  cl                     valid 9 Oct 2026
    v2   arrived 9 Oct 2026 08:20       valid 9 Oct 2026
    v2   called  9 Oct 2026 08:45       valid 9 Oct 2026
    v3   type    Visit                  valid 9 Oct 2026
    v3   clinic  cl                     valid 9 Oct 2026
    v3   arrived 9 Oct 2026 09:00       valid 9 Oct 2026
    v3   called  9 Oct 2026 09:15       valid 9 Oct 2026
    v4   type    Visit                  valid 9 Oct 2026
    v4   clinic  cl                     valid 9 Oct 2026
    v4   arrived 9 Oct 2026 09:30       valid 9 Oct 2026
    v4   called  9 Oct 2026 10:10       valid 9 Oct 2026
    v5   type    Visit                  valid 9 Oct 2026
    v5   clinic  cl                     valid 9 Oct 2026
    v5   arrived 9 Oct 2026 10:30       valid 9 Oct 2026
    v5   called  9 Oct 2026 10:50       valid 9 Oct 2026
    v6   type    Visit                  valid 9 Oct 2026
    v6   clinic  cl                     valid 9 Oct 2026
    v6   arrived 9 Oct 2026 11:00       valid 9 Oct 2026
    v6   called  9 Oct 2026 11:30       valid 9 Oct 2026
  ask          cl.waiting_time_median(range(1 Oct 2026, 1 Nov 2026))   T: 31 Oct 2026   R: 31 Oct 2026
  result       22.5 minutes
```
