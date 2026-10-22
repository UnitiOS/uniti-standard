# Reading facts whose history was corrected

Stage 7, quick test 7.3 (Indonesian archive, `uji/03-uji-singkat.md`),
for obstacles P1 to P4. The decisions are
[`decisions/0053`](../decisions/0053-reading-corrected-facts.md)
and [`decisions/0054`](../decisions/0054-reference-choices-into-text.md).

Before those decisions, the first two cases read **two values at once** for a
property with one value, and the third case accepted a correction that made
stock negative.

## A property with one value: one timeline

A rate is one value at one time. Its value at *T* is the remaining fact whose
valid time is the latest, but not after *T* (01 §2.5 step 3).

```uniti
module reference/rate@v1

concept Item
property rate : number (money, position)
property subscription : yes_no

applies to Item:
  rate
  subscription

computed Item.rate_in_effect : number (money, position), closed:
  this.rate

computed Item.subscription_in_effect : yes_no, closed:
  this.subscription

example typo_in_new_rate
  kind         compute
  title        Typo in the new rate
  explanation  Rate 150 since January, replaced by 175 since November. It
               turned out to be a typo: the correct one is 180. In December
               the rate is 180, not 150 and 180 at once.
  zone         WIB
  facts        recorded 1 Jan 2026
    b        type    Item      valid 1 Jan 2026
    f10: b   rate    150 IDR   valid 1 Jan 2026
    f11: b   rate    175 IDR   valid 1 Nov 2026   recorded 1 Nov 2026   replaces f10
    f12: b   rate    180 IDR   valid 1 Nov 2026   recorded 2 Nov 2026   corrects f11
  ask          b.rate_in_effect   T: 15 Dec 2026   R: 20 Dec 2026
  result       180 IDR

example rate_change_moved_earlier
  kind         compute
  title        The rate change turned out to be earlier
  explanation  Rate 90 since July 2025, replaced by 100 since 1 February 2026.
               It turned out that the change was on 1 January, so that
               replacement is corrected with valid time 1 January. On
               15 January the rate is 100, not 90 and 100 at once.
  zone         WIB
  facts        recorded 1 Jul 2025
    b        type    Item      valid 1 Jul 2025
    f20: b   rate    90 IDR    valid 1 Jul 2025
    f21: b   rate    100 IDR   valid 1 Feb 2026   recorded 1 Feb 2026   replaces f20
    f22: b   rate    100 IDR   valid 1 Jan 2026   recorded 5 Feb 2026   corrects f21
  ask          b.rate_in_effect   T: 15 Jan 2026   R: 1 Mar 2026
  result       100 IDR

example typo_does_not_touch_old_rate
  kind         compute
  title        The rate before November stays
  explanation  The correction of the November rate does not change the
               October rate.
  zone         WIB
  facts        as in typo_in_new_rate
  ask          b.rate_in_effect   T: 15 Oct 2026   R: 20 Dec 2026
  result       150 IDR

example june_change_learned_late
  kind         compute
  title        A change in the middle of the history
  explanation  Rate 100 since January, replaced by 150 since November. After
               that it became known that the rate was already 120 since June.
               In July the rate is 120.
  zone         WIB
  facts        recorded 1 Jan 2026
    b       type    Item      valid 1 Jan 2026
    f1: b   rate    100 IDR   valid 1 Jan 2026
    f2: b   rate    150 IDR   valid 1 Nov 2026   recorded 1 Nov 2026   replaces f1
    f3: b   rate    120 IDR   valid 1 Jun 2026   recorded 2 Nov 2026   replaces f1
  ask          b.rate_in_effect   T: 15 Jul 2026   R: 20 Dec 2026
  result       120 IDR

example june_change_does_not_overwrite_november
  kind         compute
  title        The November rate stays
  explanation  The June change that became known late does not overwrite the
               November rate: in December the rate is 150, not 120 and 150
               at once.
  zone         WIB
  facts        as in june_change_learned_late
  ask          b.rate_in_effect   T: 15 Dec 2026   R: 20 Dec 2026
  result       150 IDR

example june_change_before_it_was_known
  kind         compute
  title        Read before the June change was recorded
  explanation  As of 1 November, the June change is not known yet. The July
               rate according to what was known then is still 100.
  zone         WIB
  facts        as in june_change_learned_late
  ask          b.rate_in_effect   T: 15 Jul 2026   R: 1 Nov 2026 12:00
  result       100 IDR

example correction_of_old_rate
  kind         compute
  title        October rate corrected after the November rate was recorded
  explanation  The example in 01 §2.5 (decision 0044). Rate 100 since October,
               replaced by 150 since November, then the October rate is
               corrected to 120. In November the rate is 150.
  zone         WIB
  facts        recorded 1 Oct 2026
    b       type    Item      valid 1 Oct 2026
    f1: b   rate    100 IDR   valid 1 Oct 2026
    f2: b   rate    150 IDR   valid 1 Nov 2026   recorded 2 Oct 2026   replaces f1
    f3: b   rate    120 IDR   valid 1 Oct 2026   recorded 5 Oct 2026   corrects f1
  ask          b.rate_in_effect   T: 15 Nov 2026   R: 6 Nov 2026
  result       150 IDR

example subscription_ended
  kind         compute
  title        Ending on the timeline
  explanation  Subscription since March, ended since October. In October
               there is no value.
  zone         WIB
  facts        recorded 1 Mar 2026
    b       type          Item   valid 1 Mar 2026
    f1: b   subscription  yes    valid 1 Mar 2026
    b       subscription         valid 1 Oct 2026   recorded 1 Oct 2026   ends f1
  ask          b.subscription_in_effect   T: 15 Oct 2026   R: 20 Oct 2026
  result       empty
```

## A property with many values: each value on its own

A phone number can be many. Each value is valid until it is replaced or
ended. A correction of a replacement also replaces the target of that
replacement.

```uniti
module reference/phone@v1

concept Person
property phone : text, many

applies to Person:
  phone

computed Person.all_phones : text, many, closed:
  this.phone

example typo_in_new_number
  kind         compute
  title        Typo in the replacing number
  explanation  The office number 0811 is replaced by 0821 since November, but
               0812 was written. After the correction, the number is only
               0821, and the home number 0855 stays.
  zone         WIB
  facts        recorded 1 Jan 2026
    a       type    Person   valid 1 Jan 2026
    f1: a   phone   "0811"   valid 1 Jan 2026
    a       phone   "0855"   valid 1 Jan 2026
    f2: a   phone   "0812"   valid 1 Nov 2026   recorded 1 Nov 2026   replaces f1
    a       phone   "0821"   valid 1 Nov 2026   recorded 2 Nov 2026   corrects f2
  ask          a.all_phones   T: 15 Dec 2026   R: 20 Dec 2026
  result       ["0821", "0855"]
```

## Checking per action at the touched time

A correction that moves a date, and a retraction, also change the state at the
valid time of their target. That time is checked too (CONCEPT-18, 06 §2.12).
Retracting a whole record in one action is accepted, because CONCEPT-6 only
applies to facts that state a value. The type of the referenced entity is read
at the valid time of the fact that refers to it (VALUE-16).

```uniti
module reference/corrected-stock@v1

concept Item
concept Receipt
concept Sale

property item : reference Item
property quantity : number (position)

applies to Receipt:
  item         required
  quantity     required

applies to Sale:
  item         required
  quantity     required

computed Item.stock : number (position), closed:
  sum(all(Receipt, p: p.item = this), p: p.quantity)
  − sum(all(Sale, j: j.item = this), j: j.quantity)

constraint Item.stock_not_negative
  label.en     Stock not negative
  definition.en  The stock of an item is never less than zero.
  message.en   The stock of this item becomes negative.
  rule:
    this.stock ≥ 0

example receipt_date_moved
  kind         reject
  title        The receipt turned out to arrive only on 12 October
  explanation  10 received on 1 October, 8 sold on 10 October. It turned out
               that the goods only arrived on 12 October, so the receipt date
               is corrected. The sale of 10 October is left without stock,
               even though the correction is valid from 12 October.
  zone         WIB
  facts        recorded 11 Oct 2026 09:00
    t4       type      Item      valid 1 Oct 2026
    f3: e1   type      Receipt   valid 1 Oct 2026
    f2: e1   item      t4        valid 1 Oct 2026
    f1: e1   quantity  10        valid 1 Oct 2026
    j1       type      Sale      valid 10 Oct 2026
    j1       item      t4        valid 10 Oct 2026
    j1       quantity  8         valid 10 Oct 2026
  action       recorded 20 Oct 2026 10:00
    e1   type      Receipt   valid 12 Oct 2026   corrects f3
    e1   item      t4        valid 12 Oct 2026   corrects f2
    e1   quantity  10        valid 12 Oct 2026   corrects f1
  result       rejected by stock_not_negative, entity t4, at 10 Oct 2026

example receipt_retracted
  kind         reject
  title        A wrongly recorded receipt is retracted
  explanation  The receipt of 1 October turned out never to exist. After it is
               retracted, the sale of 10 October is without stock. The
               receipt of 15 October does not cover it: the stock on
               10 October stays −8.
  zone         WIB
  facts        recorded 16 Oct 2026 09:00
    t4       type      Item      valid 1 Oct 2026
    f3: e1   type      Receipt   valid 1 Oct 2026
    f2: e1   item      t4        valid 1 Oct 2026
    f1: e1   quantity  10        valid 1 Oct 2026
    j1       type      Sale      valid 10 Oct 2026
    j1       item      t4        valid 10 Oct 2026
    j1       quantity  8         valid 10 Oct 2026
    e2       type      Receipt   valid 15 Oct 2026
    e2       item      t4        valid 15 Oct 2026
    e2       quantity  10        valid 15 Oct 2026
  action       recorded 20 Oct 2026 10:00
    e1   type      valid 1 Oct 2026   retracts f3
    e1   item      valid 1 Oct 2026   retracts f2
    e1   quantity  valid 1 Oct 2026   retracts f1
  result       rejected by stock_not_negative, entity t4, at 10 Oct 2026

example wrong_record_retracted_entirely
  kind         accept
  title        One wrong record is retracted entirely
  explanation  The receipt of 15 October was recorded twice. The second record
               is retracted entirely in one action: its type, item, and
               quantity. Stock is 12 again.
  zone         WIB
  facts        recorded 16 Oct 2026 09:00
    t4       type      Item      valid 1 Oct 2026
    e1       type      Receipt   valid 1 Oct 2026
    e1       item      t4        valid 1 Oct 2026
    e1       quantity  10        valid 1 Oct 2026
    j1       type      Sale      valid 10 Oct 2026
    j1       item      t4        valid 10 Oct 2026
    j1       quantity  8         valid 10 Oct 2026
    e2       type      Receipt   valid 15 Oct 2026
    e2       item      t4        valid 15 Oct 2026
    e2       quantity  10        valid 15 Oct 2026
    f3: e3   type      Receipt   valid 15 Oct 2026
    f2: e3   item      t4        valid 15 Oct 2026
    f1: e3   quantity  10        valid 15 Oct 2026
  action       recorded 20 Oct 2026 10:00
    e3   type      valid 15 Oct 2026   retracts f3
    e3   item      valid 15 Oct 2026   retracts f2
    e3   quantity  valid 15 Oct 2026   retracts f1
  result       accepted
  ask          t4.stock   T: 16 Oct 2026   R: 20 Oct 2026 12:00
  result       12

example replacement_does_not_read_the_past
  kind         accept
  title        Quantity replaced, although the first record was incomplete
  explanation  Receipt e1 is recorded with a quantity since 1 October, but its
               item is only recorded since 3 October. The quantity is replaced
               since 20 October. The replacement does not change the state on
               1 October, so that time is not checked.
  zone         WIB
  facts        recorded 5 Oct 2026 09:00
    t4       type      Item      valid 1 Oct 2026
    e1       type      Receipt   valid 1 Oct 2026
    f1: e1   quantity  10        valid 1 Oct 2026
    e1       item      t4        valid 3 Oct 2026
  action       recorded 20 Oct 2026 10:00
    e1   quantity  12   valid 20 Oct 2026   replaces f1
  result       accepted

example reference_to_item_not_yet_there
  kind         reject
  title        Backdated sale to an item that is not yet registered
  explanation  Item t5 is only registered since 20 October. A sale that is
               valid on 15 October cannot refer to it, because on 15 October
               t5 is not yet an Item.
  zone         WIB
  facts        recorded 20 Oct 2026 09:00
    t5       type      Item      valid 20 Oct 2026
    e5       type      Receipt   valid 20 Oct 2026
    e5       item      t5        valid 20 Oct 2026
    e5       quantity  10        valid 20 Oct 2026
  action       recorded 21 Oct 2026 10:00
    j5       type      Sale      valid 15 Oct 2026
    j5       item      t5        valid 15 Oct 2026
    j5       quantity  2         valid 15 Oct 2026
  result       rejected by VALUE-16, entity j5, at 15 Oct 2026

example reference_after_item_exists
  kind         accept
  title        Sale after the item is registered
  explanation  The same sale, valid on 21 October, is accepted.
  zone         WIB
  facts        as in reference_to_item_not_yet_there
  action       recorded 21 Oct 2026 10:00
    j5       type      Sale      valid 21 Oct 2026
    j5       item      t5        valid 21 Oct 2026
    j5       quantity  2         valid 21 Oct 2026
  result       accepted
```
