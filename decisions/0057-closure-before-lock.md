# 0057. Closure before the lock

Date: 2026-10-22
Status: accepted

**Context**
Before v0.1 is locked, the whole standard was read once more for situations
that it does not settle yet. The aim of the lock is that v0.1 can be used
without being revised: what is added later may only add, never change a
result that is already given.

Twelve situations were found. Each of them could make two implementations
differ (blocker H1 in [`decisions/0052`](0052-quick-test-then-lock.md)), or
looked open while the text already answers it:

- **T1.** The text does not say which facts count as *before* and *after* an
  action when a constraint is checked. Found while writing the implementer
  guide.
- **T2 to T8.** Findings A22 to A28 of the reference calculator, postponed by
  the findings gate ([`decisions/0046`](0046-findings-gate.md)) because no
  case needed them.
- **T9 and T10.** Two versions of one module in one organization, and
  uninstalling a module whose facts remain (quick test, S7 and S2).
- **T11.** Five open questions that the existing rules already answer, and
  one, a property that becomes required in a later version (quick test,
  S10), that blocks a common correction.

The way of deciding: only a situation that a real user will meet is answered
by what that user needs. A situation for which no real case can be imagined
gets the strictest answer, not computable or refused. A later version may
then relax it when a case appears, without changing any result that was
already given.

**Decision**
1. **T1. One action at a time.** Actions are checked and recorded one at a
   time, in the order in which they are recorded. Before an action means the
   facts recorded before it; after means those facts plus the facts of the
   action. Case: two cashiers rent out the last tent at the same moment; the
   second is rejected. CALC-58, 06 §2.12.
2. **T2 (A22).** A unit code may reach the power 3 or −3 at most. A result
   with a higher power, for example cm⁴, is not computable because of unit
   mismatch. No business case of the 12 domains needs more. 06 §2.8.
3. **T3 (A23).** `unit_of` for a unit that is not one code without a power,
   for example `IDR/day` or `m²`, is not computable because of unit mismatch. A rule that needs
   the currency of a rate records it as a choice, as in case K2. 06 §2.5.
4. **T4 (A24).** `unit_of` for a number without a unit gives empty: such a
   number has no unit by definition (VALUE-5). 06 §2.5.
5. **T5 (A25).** An entity with no type fact valid at *T* has no place in the
   tie-breaker. If its place is needed, the result is not computable because
   of undefined order. This only happens with wrong data. 06 §2.6.
6. **T6 (A26).** `history(x.s, in: r)` with an empty `x` gives empty, like
   `x.s`. Case: the total of a rental whose item is not filled in yet. A
   collection with no members would make `sum` give 0 and hide the missing
   item. 06 §2.5.
7. **T7 (A27).** `history` of a property with many values is a collection
   with no order. A `fold` over it names `order_by` (CALC-18). No case needs
   an order between values that start at the same time. 06 §2.5.
8. **T8 (A28).** Already answered by CALC-52
   ([`decisions/0054`](0054-reference-choices-into-text.md)). Only the
   findings table of the reference calculator is brought up to date.
9. **T9. One version of each module.** An organization has at most one
   version of each module installed, counting the modules that its modules
   use. An installation that would make two versions is refused, naming both.
   Case: the cashier module uses `uniti/item@v2` and the warehouse module
   `uniti/item@v1`. The reference calculator already refused this. CHANGE-16,
   07 §2.5.
10. **T10. No uninstalling of a module in use.** A module whose content is
    used by recorded facts cannot be uninstalled. Case: a shop stops renting,
    but its old rentals must stay readable for an audit. The shop moves to
    another version or stops recording with it. CHANGE-17, 07 §2.5.
11. **T11. Answered questions, and an old gap.**
    - Rounding: there is no rounding by default, also not by the precision of
      ISO 4217, because IDR has two decimals there but is paid in whole
      rupiah. A limit on digits is a constraint. 03 §8 question 2, 06 §8
      question 7.
    - Calendar months stay in the core as written. Other conventions go into
      the calculation library when a case needs them. 06 §8 question 13.
    - Contradicting bridges change no result, because a bridge is only a
      remark (RELATION-9). 05 §8 question 1.
    - **An old gap does not block.** CONCEPT-18 does not reject an action for
      a required property that, at a time touched, was already missing before
      the action while the entity already had its type. Case: a property
      becomes required in v2, and a typo in an old customer record is
      corrected. An entity that the action creates must still be complete.
      This is the same as constraints in 06 §2.12 step 4. 04 §2.7,
      CONCEPT-18, and 04 §8 question 3.

**Alternatives**
- *Leave T2 to T8 postponed, as the findings gate says.* Rejected for the
  lock: an implementation must give some result, and two implementations would
  choose differently. The strictest answer costs nothing now and can be
  relaxed later.
- *A general rule: every situation the text does not define is not
  computable.* Rejected: an implementation cannot know which situations the
  text does not define, so the rule cannot be tested.
- *T9: allow two versions and choose the newest.* Rejected: the older module
  was frozen and proven with its own version, and choosing for it changes its
  behavior (CHANGE-15).
- *T10: allow uninstalling and keep the facts unreadable.* Rejected: facts are
  never lost (P5).
- *T11: check required properties over the whole history.* Rejected: it costs
  a full recalculation (blocker H3) and still blocks the correction of old
  records.

**Consequences**
- `04-concepts`: §2.7, CONCEPT-18, §8 question 3.
- `06-calculation-rules`: §2.5 (`unit_of`, `history`), §2.6, §2.8, §2.12,
  CALC-58, §8 questions 7 and 13.
- `07-change`: §2.5, CHANGE-16, CHANGE-17.
- `03-values` §8 question 2 and `05-relations` §8 question 1 are answered.
- The reference calculator follows T2 to T7 and T11, with tests, and new
  examples are added to the conformance tests. No existing expected result
  changes.
- `rules.md` is rebuilt.
