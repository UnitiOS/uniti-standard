# Constraints and backdated changes

Step 6 of the reference calculator: 06 §2.12 steps 2 and 3, mainly for
corrections whose valid time is far in the past (06 §8 question 4). These
cases are not from the paper test.

## Stock corrected backdated

Stock is calculated from receipts and sales, and must not be negative. A
correction replaces the quantity of a receipt at its old valid time. The effect
is seen on the sales after it, which the correction does not touch.

```uniti
module reference/backdated-stock@v1

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

example safe_backdated_correction
  kind         accept
  title        Backdated correction that does not make stock negative
  explanation  10 received on 1 October, 8 sold on 5 October. On 20 October
               that receipt is corrected to 9. Stock on 5 October becomes 1.
  zone         WIB
  facts        recorded 6 Oct 2026 09:00
    t4       type      Item      valid 1 Oct 2026
    e1       type      Receipt   valid 1 Oct 2026
    e1       item      t4        valid 1 Oct 2026
    f1: e1   quantity  10        valid 1 Oct 2026
    j1       type      Sale      valid 5 Oct 2026
    j1       item      t4        valid 5 Oct 2026
    j1       quantity  8         valid 5 Oct 2026
  action       recorded 20 Oct 2026 10:00
    f2: e1   quantity  9         valid 1 Oct 2026   corrects f1
  result       accepted
  ask          t4.stock   T: 5 Oct 2026   R: 20 Oct 2026 12:00
  result       1

example violating_backdated_correction
  kind         reject
  title        Backdated correction that makes stock negative afterward
  explanation  The receipt is corrected to 5. On 1 October, the valid time of
               the correction, the stock is 5 and the constraint is met. On
               5 October, when the sale is valid, the stock is 5 − 8 = −3.
               The correction is rejected at 5 October, even though the sale
               is not touched by the correction.
  zone         WIB
  facts        as in safe_backdated_correction
  action       recorded 20 Oct 2026 10:00
    f2: e1   quantity  5         valid 1 Oct 2026   corrects f1
  result       rejected by stock_not_negative, entity t4, at 5 Oct 2026

example correction_far_in_the_past
  kind         reject
  title        Correction nine months back
  explanation  10 received on 15 January, then 4, 4, and 2 sold in March,
               June, and September. The January receipt is corrected to 8:
               stock 8, 4, 0, then −2 on 20 September. The one that violates
               is the third sale after the correction, not the first.
  zone         WIB
  facts        recorded 1 Oct 2026 09:00
    t4       type      Item      valid 1 Jan 2026
    e1       type      Receipt   valid 15 Jan 2026
    e1       item      t4        valid 15 Jan 2026
    f1: e1   quantity  10        valid 15 Jan 2026
    j1       type      Sale      valid 3 Mar 2026
    j1       item      t4        valid 3 Mar 2026
    j1       quantity  4         valid 3 Mar 2026
    j2       type      Sale      valid 10 Jun 2026
    j2       item      t4        valid 10 Jun 2026
    j2       quantity  4         valid 10 Jun 2026
    j3       type      Sale      valid 20 Sep 2026
    j3       item      t4        valid 20 Sep 2026
    j3       quantity  2         valid 20 Sep 2026
  action       recorded 20 Oct 2026 10:00
    f2: e1   quantity  8         valid 15 Jan 2026   corrects f1
  result       rejected by stock_not_negative, entity t4, at 20 Sep 2026

example old_violation_does_not_block
  kind         accept
  title        Stock that is already negative does not block another action
  explanation  Stock has been −2 since 20 September, before this action
               (step 4). A new receipt of 1 unit on 25 September makes it −1:
               the constraint is still not met, but not because of this
               action.
  zone         WIB
  facts        recorded 1 Oct 2026 09:00
    t4       type      Item      valid 1 Jan 2026
    e1       type      Receipt   valid 15 Jan 2026
    e1       item      t4        valid 15 Jan 2026
    e1       quantity  8         valid 15 Jan 2026
    j1       type      Sale      valid 20 Sep 2026
    j1       item      t4        valid 20 Sep 2026
    j1       quantity  10        valid 20 Sep 2026
  action       recorded 20 Oct 2026 10:00
    e2       type      Receipt   valid 25 Sep 2026
    e2       item      t4        valid 25 Sep 2026
    e2       quantity  1         valid 25 Sep 2026
  result       accepted
```

## A constraint that reads the action

The constraint is condensed from O2. `this_action` only has a meaning for the
entity that the action touches; another purchase that is not touched must not
take part in the rejection.

```uniti
module reference/backdated-permission@v1

concept Person
concept Purchase

property total : number (money, increase)

applies to Purchase:
  total        required

constraint Purchase.approved_if_large
  label.en     Approved if large
  definition.en  A purchase above 10,000,000 has an approver.
  message.en   A purchase above 10,000,000 needs approval.
  rule:
    this.total ≤ 10,000,000 IDR or exists(this_action.approver)

example small_after_old_large
  kind         accept
  title        Small purchase, while an old large purchase exists
  explanation  p0 of 12,000,000 is already recorded. Omar records p2 of
               8,000,000 without an approver. Only p2 is touched, so p0 is not
               checked again with the approver of this action.
  zone         WIB
  facts        recorded 2 Jan 2026 09:00
    omar   type      Person           valid 2 Jan 2026
    p0     type      Purchase         valid 2 Jan 2026
    f0: p0 total     12,000,000 IDR   valid 2 Jan 2026
  action       recorded 12 Oct 2026 09:00, actor omar
    p2     type      Purchase         valid 12 Oct 2026
    p2     total     8,000,000 IDR    valid 12 Oct 2026
  result       accepted

example old_large_changed
  kind         reject
  title        Old large purchase changed without an approver
  explanation  p0 is changed to 13,000,000 without an approver. p0 is touched
               by the action, so the constraint is read with this action, and
               rejected.
  zone         WIB
  facts        as in small_after_old_large
  action       recorded 12 Oct 2026 09:00, actor omar
    f1: p0 total     13,000,000 IDR   valid 12 Oct 2026   replaces f0
  result       rejected by approved_if_large, entity p0, at 12 Oct 2026
```
