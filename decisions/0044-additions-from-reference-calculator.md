# 0044. Additions in meaning found by the reference calculator

Date: 2026-10-19
Status: partly replaced by 0045. Items 1 to 5 become content of the
calculation library. Item 10 is corrected for members that are exactly the
same. `rate` in item 12 becomes a helper argument.

**Context**
The reference calculator (`reference/`) runs calculation rules exactly as the
form documents say, and stops at every state whose meaning has not been set.
In steps 2 and 3, twenty such states were found, A1 to A20. The proposal for
each finding was first run provisionally in the program. All tests and all
examples in the form documents still pass, so the proposals are set here. A18
has not been decided, because it depends on the test of constraints and
backdated changes.

**Decision**

*Operations*
1. **`round`** (A2). `up` rounds to the greater number, and `down` to the
   smaller, also for negative numbers: −4.8 kg to a multiple of 0.5 kg
   becomes −4.5 kg with `up`, and −5 kg with `down`.
2. **`allocate`** (A3). A total that is not a multiple of `to` is not
   computable because it needs rounding. The total is rounded first with
   `round`.
3. **`power`** (A4). A power result that is not a whole number is rounded
   nearest to a multiple of its precision: `power(2, 0.5, to: 0.0001)` =
   1.4142.
4. **`percentile`** (A5). `p` must be a fixed number, greater than 0 and at
   most 1, so that it is checked before the rule is frozen. Rule CALC-50.
5. **`median`** (A8) is only for numbers.
6. **Same as for collections** (A9). If one of the collections has no order,
   the order is not looked at: the two are the same if each member appears
   the same number of times in both.
7. **`all_match` and `any_match`** (A12) always calculate all members,
   unlike `and` and `or`.

*Time*
8. **Reversed range** (A6). `range(a, b)` with `b` before `a` is not
   computable, with a new kind of reason, **reversed time**.
9. **Month and year only for dates** (A7). An instant is not shifted by month
   or year, and the difference of two instants is not calculated in months or
   years. A date is shifted only by whole days, weeks, months, or years.
   Anything else is not computable because of unit mismatch. Rule CALC-53.

*Order and reasons*
10. **Undefined order** (A10). Members that are not entities, in a collection
    that has no order, have no tie-breaker. When the order is needed, for
    example by `fold` with an `order_by` that has ties or by `allocate`, the
    result is not computable with a new kind of reason, **undefined order**.
11. **The reported reason** (A11). When several parts are not computable, the
    reason reported is that of the first part in calculation order: written
    order from the left, and the members of a collection in its order, or by
    tie-breaker if the collection has no order. Rule CALC-52.
12. **What is not used is not calculated** (A13, A15). `let` is calculated
    only if its name is used, and `rate` in `convert` is calculated only if
    the currencies differ, like the branch of an `if` that is not chosen.
    Rule CALC-51.

*Results of computed properties*
13. **An entity not yet classified** (A19). A computed property asked for an
    entity that at *T* does not belong to its concept has an empty result,
    like a property without facts. Rule CALC-54.
14. **Zero without a unit** (A20). When the result of a computed property
    that has a quantity is zero without a unit, for example `sum` over an
    empty collection for a total in money, the result is not computable
    because of unit mismatch. The rule writer writes `0 IDR` when the
    collection can be empty. Rule CALC-55.
15. **The "division by zero" example** (A1) in 06 §2.9 is replaced with price
    per unit for a unit count of zero. `average` over an empty collection
    remains the kind of reason empty collection.

*Facts*
16. **A correction takes the place of its target** (A17). A replacement and
    an ending of a fact also apply to the corrections of that fact. Rate 100
    from 1 October, replaced by 150 from 1 November, then the 1 October rate
    is corrected to 120: the October rate is 120, the November rate is 150.

*Examples*
17. **Identifiers in examples are ordered by local id** (A14), compared
    character by character by their Unicode number, so that the tie-breaker
    gives the same result every time the example is run. Rule PROOF-31.
18. **Reject example with several rejections** (A16). One action can be
    rejected several times, for different entities or valid times. A reject
    example passes if every rejection comes from the named constraint or
    rule of the form, and, if an entity or valid time is named, at least one
    rejection is at that entity and time. Rule PROOF-32.

**Alternatives**
- *`up` and `down` as away from and toward zero.* Rejected: the words "up"
  and "down" are read by people as greater and smaller, and likewise in
  spreadsheets and programming languages in general (*ceiling* and *floor*).
- *`allocate` rounds its total by itself.* Rejected: where rounding takes
  place is content and must be written (06 §2.8).
- *Reversed range read as an empty range.* Rejected: an end date before the
  start date is almost always a recording mistake, and must not disappear
  quietly.
- *`let` calculated first, in order.* Rejected: a rate that is not needed, or
  a reserve that is not used, would make the whole result not computable.
- *An entity not yet classified produces not computable.* Rejected: for a
  reader, an entity that does not exist yet at *T* is the same as a property
  without facts.
- *Corrections are not replaced along with it*, according to the earlier
  wording of 01 §2.5. Rejected: in November there would be two rates, while
  the correction only fixes the 1 October number.
- *A reject example must name every rejection.* Rejected: the example writer
  would have to guess rejections that are unrelated to what is being
  exemplified.

**Consequences**
- `06-calculation-rules` §2.5 to §2.9; rules CALC-18, 22, and 23 completed;
  new rules CALC-50 to 55. Two new kinds of reason: reversed time and
  undefined order.
- `01-facts` §2.5 step 3.
- `08-proof` §2.3, §2.4, and §4; new rules PROOF-31 and 32.
- `appendix/A-notation` §2.7: `p` in `percentile`.
- The reference calculator no longer marks these proposals as provisional.
