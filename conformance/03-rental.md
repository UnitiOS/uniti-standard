# Rental

Cases S1 to S4 from the paper test (Indonesian archive, `uji/01-hitung.md`
§4.C), written in the reference notation. S1, S2, and S3 are also in
[`00-form-examples.md`](00-form-examples.md) with the module from appendix A;
here they are written again exactly according to the paper test.

## S1. Total due

```uniti
module paper/s1@v1

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
  this.item.daily_rate × span(this.term, day)

example three_nights
  kind         compute
  title        Three-night rental
  explanation  A rate of 50,000 a day, rental from 6 to 9 October: 6, 7, and 8
               October, so 150,000.
  zone         WIB
  facts        recorded 5 Oct 2026 10:00
    tent  type        Item            valid 1 Oct 2026
    tent  daily_rate  50,000 IDR/day  valid 1 Oct 2026
    r1    type        Rental          valid 5 Oct 2026
    r1    item        tent            valid 5 Oct 2026
    r1    start_date  6 Oct 2026      valid 5 Oct 2026
    r1    end_date    9 Oct 2026      valid 5 Oct 2026
  ask          r1.total_due   T: 6 Oct 2026   R: 6 Oct 2026
  result       150,000 IDR
```

## S2. A rate that changes in the middle of the rental

Policy B uses `overlap` as in the paper test. The result is the same as
`span(r.range, day)` in 06 §4, because `history` already cuts the range to
the rental term.

```uniti
module paper/s2@v1
  uses paper/s1@v1

computed Rental.total_due_a : number (money, increase), closed:
  at(this.term.start, this.item.daily_rate) × span(this.term, day)

computed Rental.total_due_b : number (money, increase), closed:
  sum(history(this.item.daily_rate, in: this.term),
      r: r.value × span(overlap(r.range, this.term), day))

example rate_at_start_day
  kind         compute
  title        Policy A: the rate on the start day
  explanation  A rate of 50,000, replaced with 60,000 from 1 November. Rental
               from 29 October to 3 November, five days, at the rate of the
               first day: 5 × 50,000 = 250,000.
  zone         WIB
  facts        recorded 20 Oct 2026 09:00
    tent       type        Item            valid 1 Oct 2026
    f1: tent   daily_rate  50,000 IDR/day  valid 1 Oct 2026
    f2: tent   daily_rate  60,000 IDR/day  valid 1 Nov 2026   replaces f1
    r1         type        Rental          valid 20 Oct 2026
    r1         item        tent            valid 20 Oct 2026
    r1         start_date  29 Oct 2026     valid 20 Oct 2026
    r1         end_date    3 Nov 2026      valid 20 Oct 2026
  ask          r1.total_due_a   T: 29 Oct 2026   R: 29 Oct 2026
  result       250,000 IDR

example rate_every_day
  kind         compute
  title        Policy B: the rate in effect on each day
  explanation  Three days in October and two days in November:
               3 × 50,000 + 2 × 60,000 = 270,000.
  zone         WIB
  facts        as in rate_at_start_day
  ask          r1.total_due_b   T: 29 Oct 2026   R: 29 Oct 2026
  result       270,000 IDR
```

## S3. The same item cannot be rented at the same time

```uniti
module paper/s3@v1
  uses paper/s1@v1

constraint Rental.no_overlap
  label.en     No overlap
  definition.en  One item is not rented out twice on the same day.
  message.en   This item is already rented for part of that term.
  rule:
    count(all(Rental, s: s ≠ this and s.item = this.item
                            and exists(overlap(s.term, this.term)))) = 0

example overlapping_12_oct
  kind         reject
  title        Rental of 12 to 14 October overlaps
  explanation  The tent is already rented from 10 to 13 October. The new
               rental overlaps on 12 October.
  zone         WIB
  facts        recorded 1 Oct 2026 09:00
    tent  type        Item          valid 1 Oct 2026
    r1    type        Rental        valid 1 Oct 2026
    r1    item        tent          valid 1 Oct 2026
    r1    start_date  10 Oct 2026   valid 1 Oct 2026
    r1    end_date    13 Oct 2026   valid 1 Oct 2026
  action       recorded 5 Oct 2026 15:00
    r2    type        Rental        valid 5 Oct 2026
    r2    item        tent          valid 5 Oct 2026
    r2    start_date  12 Oct 2026   valid 5 Oct 2026
    r2    end_date    14 Oct 2026   valid 5 Oct 2026
  result       rejected by no_overlap, entity r2

example adjoining_13_oct
  kind         accept
  title        Rental of 13 to 15 October does not overlap
  explanation  Half-open range: the first rental ends before 13 October, so
               no day is used by two rentals.
  zone         WIB
  facts        as in overlapping_12_oct
  action       recorded 5 Oct 2026 15:00
    r2    type        Rental        valid 5 Oct 2026
    r2    item        tent          valid 5 Oct 2026
    r2    start_date  13 Oct 2026   valid 5 Oct 2026
    r2    end_date    15 Oct 2026   valid 5 Oct 2026
  result       accepted
```

## S4. Tiered late fee

In the paper test, `difference` is compared with 3 and multiplied by 10,000
without a unit. `difference` produces a duration, so here it is first divided
by `1 day`, and the fee has the unit IDR (06 §2.8).

```uniti
module paper/s4@v1

concept Rental

property promised_return : date
property returned : date

applies to Rental:
  promised_return  required
  returned

computed Rental.fee : number (money, increase), closed:
  let late = max(0, difference(this.promised_return, this.returned, day) ÷ 1 day)
  min(150,000 IDR,
      min(late, 3) × 10,000 IDR + max(late − 3, 0) × 20,000 IDR)

example six_days_late
  kind         compute
  title        Six days late
  explanation  3 × 10,000 + 3 × 20,000 = 90,000.
  zone         WIB
  facts        recorded 16 Oct 2026 17:00
    r1   type             Rental        valid 1 Oct 2026
    r1   promised_return  10 Oct 2026   valid 1 Oct 2026
    r1   returned         16 Oct 2026   valid 16 Oct 2026
  ask          r1.fee   T: 16 Oct 2026   R: 16 Oct 2026 18:00
  result       90,000 IDR

example twelve_days_late
  kind         compute
  title        Twelve days late, capped
  explanation  3 × 10,000 + 9 × 20,000 = 210,000, capped to 150,000.
  zone         WIB
  facts        recorded 22 Oct 2026 17:00
    r1   type             Rental        valid 1 Oct 2026
    r1   promised_return  10 Oct 2026   valid 1 Oct 2026
    r1   returned         22 Oct 2026   valid 22 Oct 2026
  ask          r1.fee   T: 22 Oct 2026   R: 22 Oct 2026 18:00
  result       150,000 IDR
```
