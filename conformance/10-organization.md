# Organization and governance

Cases O1 to O3 of the paper test (`uji/01-hitung.md`)<!-- ARCHIVE-LINK: ../../01-hitung.md -->
§4.J, written in the reference notation. O2 is also in
[`00-form-examples.md`](00-form-examples.md); here its five rows are written
exactly as in the paper test, with Budi as staff.

## O1. Cost by organization chart

The direct cost is read from the cost facts in that period. The paper test
does not mention it; here it is written as a computed property with `0 IDR`,
because a unit with no cost gives the sum over an empty collection
(CALC-55).

The company has no parent. In the paper test, `u.parent_unit = this` compares
the parent of the company, which is empty, so the whole total cost is not
computable (06 §2.9). Here a reference that may be empty is checked first with
`exists` (finding A32).

```uniti
module paper/o1@v1

concept Unit
concept Cost

property parent_unit : reference Unit
property unit : reference Unit
property date : date
property amount : number (money, increase)

applies to Unit:
  parent_unit

applies to Cost:
  unit         required
  date         required
  amount       required

computed Unit.direct_cost(period) : number (money, increase), closed:
  0 IDR + sum(all(Cost, c: c.unit = this and c.date in period), c: c.amount)

computed Unit.total_cost(period) : number (money, increase), closed:
  this.direct_cost(period)
  + sum(all(Unit, u: exists(u.parent_unit) and u.parent_unit = this),
        u: u.total_cost(period))

example sales_cost
  kind         compute
  title        Total cost of the sales division
  explanation  Sales 10 million, with Store A 25 million and Store B 30 million
               under it: 65 million.
  zone         WIB
  facts        recorded 31 Oct 2026 18:00
    company    type         Unit             valid 1 Jan 2026
    sales      type         Unit             valid 1 Jan 2026
    sales      parent_unit  company          valid 1 Jan 2026
    warehouse  type         Unit             valid 1 Jan 2026
    warehouse  parent_unit  company          valid 1 Jan 2026
    store_a    type         Unit             valid 1 Jan 2026
    store_a    parent_unit  sales            valid 1 Jan 2026
    store_b    type         Unit             valid 1 Jan 2026
    store_b    parent_unit  sales            valid 1 Jan 2026
    x1         type         Cost             valid 31 Oct 2026
    x1         unit         company          valid 31 Oct 2026
    x1         date         31 Oct 2026      valid 31 Oct 2026
    x1         amount       5,000,000 IDR    valid 31 Oct 2026
    x2         type         Cost             valid 31 Oct 2026
    x2         unit         sales            valid 31 Oct 2026
    x2         date         31 Oct 2026      valid 31 Oct 2026
    x2         amount       10,000,000 IDR   valid 31 Oct 2026
    x3         type         Cost             valid 31 Oct 2026
    x3         unit         warehouse        valid 31 Oct 2026
    x3         date         31 Oct 2026      valid 31 Oct 2026
    x3         amount       15,000,000 IDR   valid 31 Oct 2026
    x4         type         Cost             valid 31 Oct 2026
    x4         unit         store_a          valid 31 Oct 2026
    x4         date         31 Oct 2026      valid 31 Oct 2026
    x4         amount       25,000,000 IDR   valid 31 Oct 2026
    x5         type         Cost             valid 31 Oct 2026
    x5         unit         store_b          valid 31 Oct 2026
    x5         date         31 Oct 2026      valid 31 Oct 2026
    x5         amount       30,000,000 IDR   valid 31 Oct 2026
  ask          sales.total_cost(range(1 Oct 2026, 1 Nov 2026))   T: 31 Oct 2026   R: 1 Nov 2026
  result       65,000,000 IDR

example company_cost
  kind         compute
  title        Total cost of the company
  explanation  5 + 65 + 15 = 85 million.
  zone         WIB
  facts        as in sales_cost
  ask          company.total_cost(range(1 Oct 2026, 1 Nov 2026))   T: 31 Oct 2026   R: 1 Nov 2026
  result       85,000,000 IDR
```

## O2. A large purchase needs manager approval

```uniti
module paper/o2@v1

concept Person
concept Contract
concept Purchase

choice_list Position, closed
  choices:
    manager
    staff

property employee : reference Person
property position : choice Position
property total : number (money, increase)

applies to Contract:
  employee     required
  position     required

applies to Purchase:
  total        required

constraint Purchase.approved_if_large
  label.en     Approved if large
  definition.en  A purchase above 10,000,000 is approved by a manager who is
               not the actor.
  message.en   A purchase above 10,000,000 needs approval by another manager.
  rule:
    this.total ≤ 10,000,000 IDR
    or (exists(this_action.approver)
        and this_action.approver ≠ this_action.actor
        and any_match(all(Contract, k: k.employee = this_action.approver),
                      k: k.position = manager))

example small_without_approver
  kind         accept
  title        Purchase of 8,000,000 without approver
  explanation  Below the limit, so it does not need approval.
  zone         WIB
  facts        recorded 2 Jan 2026 09:00
    sari   type      Person    valid 2 Jan 2026
    budi   type      Person    valid 2 Jan 2026
    andi   type      Person    valid 2 Jan 2026
    ks     type      Contract  valid 2 Jan 2026
    ks     employee  sari      valid 2 Jan 2026
    ks     position  manager   valid 2 Jan 2026
    kb     type      Contract  valid 2 Jan 2026
    kb     employee  budi      valid 2 Jan 2026
    kb     position  staff     valid 2 Jan 2026
  action       recorded 12 Oct 2026 09:00, actor andi
    p1     type      Purchase         valid 12 Oct 2026
    p1     total     8,000,000 IDR    valid 12 Oct 2026
  result       accepted

example large_without_approver
  kind         reject
  title        Purchase of 12,000,000 without approver
  explanation  Above the limit and there is no approver.
  zone         WIB
  facts        as in small_without_approver
  action       recorded 12 Oct 2026 09:00, actor andi
    p1     type      Purchase         valid 12 Oct 2026
    p1     total     12,000,000 IDR   valid 12 Oct 2026
  result       rejected by approved_if_large, entity p1, at 12 Oct 2026

example large_approved_by_staff
  kind         reject
  title        Purchase of 12,000,000 approved by staff
  explanation  Budi approves, but Budi is staff, not a manager.
  zone         WIB
  facts        as in small_without_approver
  action       recorded 12 Oct 2026 09:00, actor andi, approver budi
    p1     type      Purchase         valid 12 Oct 2026
    p1     total     12,000,000 IDR   valid 12 Oct 2026
  result       rejected by approved_if_large, entity p1

example large_approved_by_manager
  kind         accept
  title        Purchase of 12,000,000 approved by a manager
  explanation  Andi records it, Sari the manager approves.
  zone         WIB
  facts        as in small_without_approver
  action       recorded 12 Oct 2026 09:00, actor andi, approver sari
    p1     type      Purchase         valid 12 Oct 2026
    p1     total     12,000,000 IDR   valid 12 Oct 2026
  result       accepted

example large_approved_by_self
  kind         reject
  title        Purchase of 12,000,000 approved by the actor themselves
  explanation  Sari is a manager, but she is also the actor. The approver has
               to be someone else.
  zone         WIB
  facts        as in small_without_approver
  action       recorded 12 Oct 2026 09:00, actor sari, approver sari
    p1     type      Purchase         valid 12 Oct 2026
    p1     total     12,000,000 IDR   valid 12 Oct 2026
  result       rejected by approved_if_large, entity p1

example exactly_at_limit_without_approver
  kind         accept
  title        Boundary point: purchase of exactly 10,000,000 without approver
  explanation  "Above 10,000,000" does not include 10,000,000, so this
               purchase does not need approval.
  zone         WIB
  facts        as in small_without_approver
  action       recorded 12 Oct 2026 09:00, actor andi
    p1     type      Purchase         valid 12 Oct 2026
    p1     total     10,000,000 IDR   valid 12 Oct 2026
  result       accepted

example over_limit_without_approver
  kind         reject
  title        Boundary point: purchase of 10,000,001 without approver
  explanation  One rupiah above the limit already needs approval.
  zone         WIB
  facts        as in small_without_approver
  action       recorded 12 Oct 2026 09:00, actor andi
    p1     type      Purchase         valid 12 Oct 2026
    p1     total     10,000,001 IDR   valid 12 Oct 2026
  result       rejected by approved_if_large, entity p1, at 12 Oct 2026
```

## O3. Allowed status transitions

The paper test writes a transition as a pair `(draft, submitted)`. There are
no pairs in the core; here it is written as a record, as in appendix A §5.

The reject examples here need the value of the constraint before the action
(06 §2.12 step 3), while `before_action(…)` only has a meaning when there is an
action. A constraint that reads the action is taken as not yet existing before
the action (finding A31, decision 0047).

```uniti
module paper/o3@v1

concept Document

choice_list Status, closed
  choices:
    draft
    submitted
    approved
    rejected
    posted

property status : choice Status

applies to Document:
  status       required

constraint Document.ordered_status
  label.en     Ordered status
  definition.en  The status of a document only moves in the allowed order.
  message.en   This status transition is not allowed.
  rule:
    not exists(before_action(this.status))
    or before_action(this.status) = this.status
    or {from: before_action(this.status), to: this.status}
         in [{from: draft, to: submitted}, {from: submitted, to: approved},
             {from: submitted, to: rejected}, {from: approved, to: posted}]

example draft_submitted
  kind         accept
  title        Draft submitted
  explanation  Draft to submitted is in the list of transitions.
  zone         WIB
  facts        recorded 1 Oct 2026 09:00
    d1       type     Document   valid 1 Oct 2026
    f1: d1   status   draft      valid 1 Oct 2026
  action       recorded 5 Oct 2026 10:00
    f2: d1   status   submitted  valid 5 Oct 2026   replaces f1
  result       accepted

example draft_straight_to_posted
  kind         reject
  title        Draft posted directly
  explanation  A draft has to be submitted and approved first.
  zone         WIB
  facts        as in draft_submitted
  action       recorded 5 Oct 2026 10:00
    f2: d1   status   posted  valid 5 Oct 2026   replaces f1
  result       rejected by ordered_status, entity d1

example posted_back_to_draft
  kind         reject
  title        A document that is already posted is locked
  explanation  Posted to draft is not in the list, so a document that is
               already posted cannot be changed any more.
  zone         WIB
  facts        recorded 1 Oct 2026 09:00
    d1       type     Document  valid 1 Oct 2026
    f1: d1   status   posted    valid 1 Oct 2026
  action       recorded 5 Oct 2026 10:00
    f2: d1   status   draft     valid 5 Oct 2026   replaces f1
  result       rejected by ordered_status, entity d1
```
