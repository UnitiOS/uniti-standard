# 0058. Rejection of facts with a wrong form

Date: 2026-10-22
Status: accepted

**Context**
[`decisions/0056`](0056-conformance-test-owners-and-known-gap.md) recorded a
known gap: the group Facts of 08 §2.9 names the rejection of facts with a wrong
form, but no conformance example rejected an action because of a FACT rule.
The reference calculator read such a fact as a notation error, so the example
could not be written. 0056 left the gap for after the lock.

A conformance test that is missing at the lock is a test that two
implementations can pass while they behave differently. The rules themselves
are already clear (01 §3), so filling the gap adds tests, not text.

**Decision**
1. The gap is filled before the lock, in
   [`conformance/22-fact-form.md`](../conformance/22-fact-form.md): ten actions
   rejected by FACT-2, FACT-9, FACT-10, FACT-11, FACT-13, and FACT-14, and
   three right actions that are accepted. Each one is a mistake a cashier or a
   shop owner can make, for example a second phone number stated while one is
   in force, or a price replaced on the date of the price it replaces.
2. The module of those examples has no constraint and no required property, so
   every rejection comes from the FACT rule named (PROOF-32), whatever else an
   implementation checks.
3. *In force* in FACT-14 is read from the facts before the action (CALC-58).
   So a value that is retracted and stated again for the same valid time in
   one action is rejected by FACT-14. The way to repair a wrong value in one
   step is a correction (FACT-14 names it).
4. The reference calculator checks the FACT rules first, and reports only
   those rejections if there are any, because the state after a wrong action
   has no defined reading. This is a choice of the reference calculator, not
   a rule: the text only requires that the action is rejected (FACT-18).
5. Two parts stay without a conformance example, and are recorded as a
   smaller known gap:
   - FACT-19 to FACT-21 (source and reason of an action): the notation of an
     action inside an example has no source and no reason
     ([`appendix/A-notation.md`](../appendix/A-notation.md) §2.9).
   - FACT-23 to FACT-25: redaction is provisional.
6. Item 3 of 0056 is replaced by this decision.

**Alternatives**
- *Leave the gap for after the lock, as 0056 said.* Rejected: the tests cost
  little now and the rules do not change, while a missing test lets
  implementations differ from the first day.
- *Read "in force" after the earlier facts of the same action.* Rejected: it
  makes the result depend on the order of facts inside one action, which the
  text does not give (FACT-18 records them together). A correction already
  covers the case.
- *Add a source and a reason to the notation of an action now.* Rejected for
  v0.1: no case of the twelve domains needs it in a conformance test, and it
  changes the notation. It can be added later without changing any result.

**Consequences**
- New file `conformance/22-fact-form.md`, listed in
  [`conformance/README.md`](../conformance/README.md).
- `08-proof` §8 question 6 is answered.
- `README.md`: the known gap is narrowed to FACT-19 to FACT-21.
- `0056` gets the status "partly replaced by 0058".
- The reference calculator reports FACT-2, FACT-9, FACT-10, FACT-11,
  FACT-13, and FACT-14 inside an action as rejections, with tests. Starting
  facts with a wrong form stay notation errors. No existing expected result
  changes.
