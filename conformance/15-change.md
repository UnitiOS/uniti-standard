# Change between versions

Stage 5, tests U1 to U3 (`uji/02-lintas-domain.md`)<!-- ARCHIVE-LINK: ../../02-lintas-domain.md -->:
`07-change`, and the contracts between versions and between modules in `08`
§2.7 and §2.8.

An example has an address (02 §2.1), and every address in a version still
exists in the next version (CHANGE-6). So a new version contains all the
examples of the old version, and running an example of the new version is the
same as running the old example with the new rules. The kinds of change
between two versions are computed by `program/versi.py`, and tested in
`operasi/uji_versi.py`.

## U1. A new version adds a property

As in 07 §4: Rudi freezes version 2, which adds the property "promised return
date". The machine counts one **addition**. The version 1 example comes along
in version 2 unchanged, and still passes.

```uniti
module rudi/rental@v1

concept Item
concept Rental

property item : reference Item
property start_date : date
property end_date : date
property daily_rate : number (money/duration, level)

applies to Item:
  daily_rate   required

applies to Rental:
  item         required
  start_date   required
  end_date     required

computed Rental.total_due : number (money, increase), closed:
  this.item.daily_rate × span(range(this.start_date, this.end_date), day)

example three_night_rental
  kind         compute
  title        Three-night rental
  explanation  50,000 a day, from 6 to 9 October: 150,000.
  zone         WIB
  facts        recorded 6 Oct 2026 10:00
    tent  type        Item            valid 1 Oct 2026
    tent  daily_rate  50,000 IDR/day  valid 1 Oct 2026
    r1    type        Rental          valid 6 Oct 2026
    r1    item        tent            valid 6 Oct 2026
    r1    start_date  6 Oct 2026      valid 6 Oct 2026
    r1    end_date    9 Oct 2026      valid 6 Oct 2026
  ask          r1.total_due   T: 6 Oct 2026   R: 6 Oct 2026 12:00
  result       150,000 IDR

module rudi/rental@v2

concept Item
concept Rental

property item : reference Item
property start_date : date
property end_date : date
property daily_rate : number (money/duration, level)
property promised_return_date : date

applies to Item:
  daily_rate   required

applies to Rental:
  item         required
  start_date   required
  end_date     required
  promised_return_date

computed Rental.total_due : number (money, increase), closed:
  this.item.daily_rate × span(range(this.start_date, this.end_date), day)

example three_night_rental
  kind         compute
  title        Three-night rental
  explanation  50,000 a day, from 6 to 9 October: 150,000.
  zone         WIB
  facts        recorded 6 Oct 2026 10:00
    tent  type        Item            valid 1 Oct 2026
    tent  daily_rate  50,000 IDR/day  valid 1 Oct 2026
    r1    type        Rental          valid 6 Oct 2026
    r1    item        tent            valid 6 Oct 2026
    r1    start_date  6 Oct 2026      valid 6 Oct 2026
    r1    end_date    9 Oct 2026      valid 6 Oct 2026
  ask          r1.total_due   T: 6 Oct 2026   R: 6 Oct 2026 12:00
  result       150,000 IDR
```

## U2. A user is bound to an exact version

Toko Kemah Ceria uses version 1, and nothing changes for it because version 2
exists (CHANGE-15). When the shop freezes a version that uses version 2, its
examples are run again with version 2 (PROOF-24). The old rental can still be
read, with the new property empty (07 §4).

```uniti
module kemah-ceria/shop@v1
  uses rudi/rental@v1

example weekend_rental
  kind         compute
  title        Weekend rental
  explanation  A stove at 30,000 a day, from Friday 16 to Sunday 18 October:
               two days, 60,000.
  zone         WIB
  facts        recorded 16 Oct 2026 08:00
    stove  type        Item            valid 1 Oct 2026
    stove  daily_rate  30,000 IDR/day  valid 1 Oct 2026
    s1     type        Rental          valid 16 Oct 2026
    s1     item        stove           valid 16 Oct 2026
    s1     start_date  16 Oct 2026     valid 16 Oct 2026
    s1     end_date    18 Oct 2026     valid 16 Oct 2026
  ask          s1.total_due   T: 16 Oct 2026   R: 16 Oct 2026 12:00
  result       60,000 IDR

module kemah-ceria/shop@v2
  uses rudi/rental@v2

example weekend_rental
  kind         compute
  title        Weekend rental
  explanation  A stove at 30,000 a day, from Friday 16 to Sunday 18 October:
               two days, 60,000.
  zone         WIB
  facts        recorded 16 Oct 2026 08:00
    stove  type        Item            valid 1 Oct 2026
    stove  daily_rate  30,000 IDR/day  valid 1 Oct 2026
    s1     type        Rental          valid 16 Oct 2026
    s1     item        stove           valid 16 Oct 2026
    s1     start_date  16 Oct 2026     valid 16 Oct 2026
    s1     end_date    18 Oct 2026     valid 16 Oct 2026
  ask          s1.total_due   T: 16 Oct 2026   R: 16 Oct 2026 12:00
  result       60,000 IDR

example promised_return_old_rental
  kind         compute
  title        Old rental without a promised return date
  explanation  The rental was recorded before that property existed. Its
               facts can still be read, and the new property is empty.
  zone         WIB
  facts        as in weekend_rental
  ask          s1.promised_return_date   T: 16 Oct 2026   R: 16 Oct 2026 12:00
  result       empty
```

## U3. Behavior change

As in 08 §2.7: version 4 of the vocabulary changes the recipient of the
depreciation remainder from the last month to the first month. The old
example "accumulated as of 31 March 999,999" fails, because its new result is
1,000,011. The vocabulary owner marks it as replaced, with a reason, and adds
a new example. The other examples that are not affected still pass.

```uniti
module uniti/depreciation@v3
  uses uniti/calc@v1

concept Asset

property price : number (money, level)
property useful_life : number (duration, level)
property start_of_use : date

applies to Asset:
  price        required
  useful_life  required
  start_of_use required

helper Asset.depreciation : collection:
  allocate(this.price,
           each(split(range(this.start_of_use, this.start_of_use + this.useful_life), step: 1 month),
                b: {member: b, weight: 1}),
           1 IDR, last)

computed Asset.accumulated_depreciation : number (money, level), closed:
  sum(this.depreciation, p: if p.member.start ≤ T then p.share else 0 IDR)

computed Asset.current_month_depreciation : number (money, increase), closed:
  sum(this.depreciation, p: if T in p.member then p.share else 0 IDR)

example march_accumulated
  kind         compute
  title        Accumulated depreciation as of 31 March
  explanation  12,000,000 ÷ 36 = 333,333 a month, the remainder goes to the
               last month. Three months: 999,999.
  zone         WIB
  facts        recorded 2 Jan 2026 09:00
    a1  type          Asset           valid 1 Jan 2026
    a1  price         12,000,000 IDR  valid 1 Jan 2026
    a1  useful_life   36 months       valid 1 Jan 2026
    a1  start_of_use  1 Jan 2026      valid 1 Jan 2026
  ask          a1.accumulated_depreciation   T: 31 Mar 2026   R: 31 Mar 2026
  result       999,999 IDR

example february_depreciation
  kind         compute
  title        Depreciation of the second month
  explanation  The second month receives no remainder: 333,333.
  zone         WIB
  facts        as in march_accumulated
  ask          a1.current_month_depreciation   T: 15 Feb 2026   R: 15 Feb 2026
  result       333,333 IDR

module uniti/depreciation@v4
  uses uniti/calc@v1

concept Asset

property price : number (money, level)
property useful_life : number (duration, level)
property start_of_use : date

applies to Asset:
  price        required
  useful_life  required
  start_of_use required

helper Asset.depreciation : collection:
  allocate(this.price,
           each(split(range(this.start_of_use, this.start_of_use + this.useful_life), step: 1 month),
                b: {member: b, weight: 1}),
           1 IDR, first)

computed Asset.accumulated_depreciation : number (money, level), closed:
  sum(this.depreciation, p: if p.member.start ≤ T then p.share else 0 IDR)

computed Asset.current_month_depreciation : number (money, increase), closed:
  sum(this.depreciation, p: if T in p.member then p.share else 0 IDR)

example march_accumulated
  kind         compute
  title        Accumulated depreciation as of 31 March
  explanation  12,000,000 ÷ 36 = 333,333 a month, the remainder goes to the
               last month. Three months: 999,999.
  status       replaced
  reason       Following the new policy: the remainder goes to the first month.
  replaced_by  march_accumulated_remainder_first
  zone         WIB
  facts        recorded 2 Jan 2026 09:00
    a1  type          Asset           valid 1 Jan 2026
    a1  price         12,000,000 IDR  valid 1 Jan 2026
    a1  useful_life   36 months       valid 1 Jan 2026
    a1  start_of_use  1 Jan 2026      valid 1 Jan 2026
  ask          a1.accumulated_depreciation   T: 31 Mar 2026   R: 31 Mar 2026
  result       999,999 IDR

example february_depreciation
  kind         compute
  title        Depreciation of the second month
  explanation  The second month receives no remainder: 333,333.
  zone         WIB
  facts        as in march_accumulated
  ask          a1.current_month_depreciation   T: 15 Feb 2026   R: 15 Feb 2026
  result       333,333 IDR

example march_accumulated_remainder_first
  kind         compute
  title        Accumulated as of 31 March, remainder in the first month
  explanation  The first month is 12,000,000 − 35 × 333,333 = 333,345. Three
               months: 333,345 + 2 × 333,333 = 1,000,011.
  zone         WIB
  facts        as in march_accumulated
  ask          a1.accumulated_depreciation   T: 31 Mar 2026   R: 31 Mar 2026
  result       1,000,011 IDR
```
