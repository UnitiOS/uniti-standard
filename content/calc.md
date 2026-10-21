# Calculation library

Status: draft

The first calculation library: helpers without a concept in the vocabulary
module `uniti/calc`, written only with the core operations
([`06-calculation-rules`](../form/06-calculation-rules.md) §2.5;
[`decisions/0045`](../decisions/0045-core-operations-and-calculation-library.md)).

It holds the meaning of `average`, `median`, `percentile`, `round`,
`allocate`, and currency conversion, which used to be operations. Its origin
is the experiments in `uji/acuan/percobaan/`
<!-- ARCHIVE-LINK: uji/acuan/percobaan/README.md -->. Its examples are run by
the reference calculator together with the cases, and its tests are in
`uji/acuan/operasi/uji_pustaka.py`
<!-- ARCHIVE-LINK: uji/acuan/operasi/uji_pustaka.py -->.

## Library

```uniti
module uniti/calc@v1

choice_list RoundingMode, closed
  label.en       Rounding mode
  definition.en  Where a number is rounded to when it is not exactly on its
                 multiple.
  choices:
    nearest
    up
    down

choice_list RemainderRule, closed
  label.en       Recipient of the allocation remainder
  definition.en  Which share receives the rounding remainder, so that the
                 sum of the shares is exactly equal to the total.
  choices:
    largest_fraction
    first
    last

helper average(k) : number
  definition.en  The average. An empty collection is not computable.
  rule:
    if count(k) = 0 then not_computable("average of an empty collection")
    else sum(k) ÷ count(k)

helper sorted(k) : collection
  definition.en  The same collection, sorted from the smallest.
  rule:
    fold(k, order_by: x: x, initial: [], step: (s, x): append(s, x))

helper member_at(k, i) : number
  definition.en  The i-th member, counting from 1, of an ordered collection.
  rule:
    fold(k, initial: {n: 0, result: 0},
         step: (s, x): {n: s.n + 1, result: if s.n + 1 = i then x else s.result}
    ).result

helper median(k) : number
  definition.en  The middle value. When the count is even, the average of
                 the two middle values. An empty collection is not
                 computable.
  rule:
    let n = count(k)
    let u = sorted(k)
    if n = 0 then not_computable("median of an empty collection")
    else if floor_multiple(n ÷ 2, of: 1) × 2 = n
      then (member_at(u, n ÷ 2) + member_at(u, n ÷ 2 + 1)) ÷ 2
    else member_at(u, (n + 1) ÷ 2)

helper percentile(k, p) : number
  definition.en  Nearest rank: the member at position ⌈p × count⌉.
  rule:
    let n = count(k)
    if not (p > 0 and p ≤ 1) then not_computable("p is outside 0 < p ≤ 1")
    else if n = 0 then not_computable("percentile of an empty collection")
    else member_at(sorted(k), − floor_multiple(− (p × n), of: 1))

helper round(n, to, mode) : number
  definition.en  Rounds n to a multiple of to. Mode nearest: half away from
                 zero. Modes up and down: to the greater and to the smaller
                 number, also for negative numbers.
  rule:
    if mode = down then floor_multiple(n, of: to)
    else if mode = up then − floor_multiple(− n, of: to)
    else if n ≥ 0 then floor_multiple(n + to ÷ 2, of: to)
    else − floor_multiple(− n + to ÷ 2, of: to)

helper convert_money(n, to, rate) : number
  definition.en  Converts n to the currency to. The rate has the unit of the
                 target currency per source currency, and is read only when
                 the currencies differ.
  rule:
    if unit_of(n) = to then n
    else if unit_of(n × rate) = to then n × rate
    else not_computable("the rate does not match the currencies")

helper by_member(list) : collection
  definition.en  Records {member, …}, sorted by the tie-breaker of their
                 members.
  rule:
    fold(list, order_by: d: d.member, initial: [], step: (s, d): append(s, d))

helper allocate(total, list, to, remainder) : collection
  definition.en  Divides total by weight, with the sum of the shares exactly
                 equal to the total. list: an ordered collection of records
                 {member, weight}. Result: an ordered collection of records
                 {member, share}, in the order of list.
  rule:
    let ordered = fold(list, initial: [],
                       step: (s, d): append(s, {member: d.member, weight: d.weight,
                                                i: count(s) + 1}))
    let total_weight = sum(ordered, d: d.weight)
    let sign = if total < 0 then −1 else 1
    let n = sign × total ÷ to
    let parts = each(ordered, d: {member: d.member, i: d.i,
                                  exact: d.weight × n ÷ total_weight,
                                  base: floor_multiple(d.weight × n ÷ total_weight, of: 1)})
    let excess = n − sum(parts, b: b.base)
    let size = count(ordered)
    if any_match(ordered, d: d.weight < 0) then not_computable("there is a negative weight")
    else if total_weight = 0 then not_computable("the sum of the weights is zero")
    else if floor_multiple(n, of: 1) ≠ n
      then not_computable("the total is not a multiple of to")
    else each(parts, b:
      let fraction = b.exact − b.base
      let extra = (if remainder = first then (if b.i = 1 then excess else 0)
        else if remainder = last then (if b.i = size then excess else 0)
        else if sum(parts, c: if c.exact − c.base > fraction
                                  or (c.exact − c.base = fraction and c.i < b.i)
                                  then 1 else 0) < excess
          then 1 else 0)
      {member: b.member, share: sign × (b.base + extra) × to})
```

## Use and examples

The examples below use the library from another module, as a domain module
will later. A helper without a concept cannot be asked directly in an
example, so each helper is exemplified through a computed property.

```uniti
module example/user@v1
  uses uniti/calc@v1

concept Group
concept DataPoint
concept Room
concept ExchangeRate

property in_group : reference Group
property value : number (position)
property area : number (length², position)
property price : number (money, position)
property exchange_rate : number (money/money, position)
property rent : number (money, position)

applies to DataPoint:
  in_group     required
  value        required

applies to Room:
  area         required

applies to ExchangeRate:
  exchange_rate required

applies to Group:
  price
  rent

helper Group.values : collection:
  each(all(DataPoint, d: d.in_group = this), d: d.value)

computed Group.median_value : number (position), closed:
  median(this.values)

computed Group.p90 : number (position), closed:
  percentile(this.values, 0.9)

computed Group.rounded_average : number (position), closed:
  round(average(this.values), 1, nearest)

computed Group.price_idr : number (money, position), closed:
  convert_money(this.price, IDR, single(all(ExchangeRate)).exchange_rate)

computed Room.rent_share : number (money, position), closed:
  let g = single(all(Group))
  sum(allocate(g.rent, by_member(each(all(Room), r: {member: r, weight: r.area})),
               1 IDR, largest_fraction),
      b: if b.member = this then b.share else 0 IDR)

example median_with_equal_values
  kind         compute
  title        Median with equal values
  explanation  The values are 7, 3, 7, and 5. Sorted: 3, 5, 7, 7; the median
               is (5 + 7) ÷ 2 = 6. The two 7s are equal, so their order does
               not matter.
  facts        recorded 1 Oct 2026
    g   type      Group      valid 1 Oct 2026
    d1  type      DataPoint  valid 1 Oct 2026
    d1  in_group  g          valid 1 Oct 2026
    d1  value     7          valid 1 Oct 2026
    d2  type      DataPoint  valid 1 Oct 2026
    d2  in_group  g          valid 1 Oct 2026
    d2  value     3          valid 1 Oct 2026
    d3  type      DataPoint  valid 1 Oct 2026
    d3  in_group  g          valid 1 Oct 2026
    d3  value     7          valid 1 Oct 2026
    d4  type      DataPoint  valid 1 Oct 2026
    d4  in_group  g          valid 1 Oct 2026
    d4  value     5          valid 1 Oct 2026
  ask          g.median_value   T: 1 Oct 2026   R: 1 Oct 2026
  result       6

example percentile_90
  kind         compute
  title        Percentile 90
  explanation  Four values; the member at position ⌈0.9 × 4⌉ = 4 after
               sorting: 7.
  facts        as in median_with_equal_values
  ask          g.p90   T: 1 Oct 2026   R: 1 Oct 2026
  result       7

example average_five_point_five
  kind         compute
  title        Rounded average
  explanation  (7 + 3 + 7 + 5) ÷ 4 = 5.5, rounded with mode nearest to 6.
  facts        as in median_with_equal_values
  ask          g.rounded_average   T: 1 Oct 2026   R: 1 Oct 2026
  result       6

example median_empty
  kind         compute
  title        Median without data
  explanation  A group without data has no median.
  facts        recorded 1 Oct 2026
    g  type  Group  valid 1 Oct 2026
  ask          g.median_value   T: 1 Oct 2026   R: 1 Oct 2026
  result       not computable: declared by rule

example rupiah_without_rate
  kind         compute
  title        A rupiah price needs no exchange rate
  explanation  The price is already in rupiah, so the rate is not looked up.
               No rate has been recorded yet, and that does not make the
               result fail.
  facts        recorded 1 Oct 2026
    g  type   Group        valid 1 Oct 2026
    g  price  150,000 IDR  valid 1 Oct 2026
  ask          g.price_idr   T: 1 Oct 2026   R: 1 Oct 2026
  result       150,000 IDR

example dollar_with_rate
  kind         compute
  title        A dollar price converted with an exchange rate
  explanation  10 USD with a rate of 16,000 IDR/USD becomes 160,000 IDR.
  facts        recorded 1 Oct 2026
    g  type           Group           valid 1 Oct 2026
    g  price          10 USD          valid 1 Oct 2026
    k  type           ExchangeRate    valid 1 Oct 2026
    k  exchange_rate  16,000 IDR/USD  valid 1 Oct 2026
  ask          g.price_idr   T: 1 Oct 2026   R: 1 Oct 2026
  result       160,000 IDR

example building_rent_split_by_area
  kind         compute
  title        Building rent split by area
  explanation  From 06 §2.8: 10,000,000 split by areas of 120, 80, and
               100 m² becomes 4,000,000, 2,666,667, and 3,333,333. The 80 m²
               room receives the remainder of 1, because its fraction is the
               largest.
  facts        recorded 1 Oct 2026
    g  type  Group           valid 1 Oct 2026
    g  rent  10,000,000 IDR  valid 1 Oct 2026
    a  type  Room            valid 1 Oct 2026
    a  area  120 m²          valid 1 Oct 2026
    b  type  Room            valid 1 Oct 2026
    b  area  80 m²           valid 1 Oct 2026
    c  type  Room            valid 1 Oct 2026
    c  area  100 m²          valid 1 Oct 2026
  ask          b.rent_share   T: 1 Oct 2026   R: 1 Oct 2026
  result       2,666,667 IDR
```
