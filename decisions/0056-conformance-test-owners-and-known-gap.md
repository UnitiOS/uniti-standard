# 0056. Owners inside the conformance tests, and a known gap

Date: 2026-10-22
Status: partly replaced by 0058. Item 3: the known gap is filled before the
lock, and only FACT-19 to FACT-21 stay without an example

**Context**
While the conformance tests were listed per example in stage 8.6
([`conformance/README.md`](../conformance/README.md)), two things were found
that the text and the tests do not agree on.

- PROOF-25 and 08 §2.9 say that the conformance tests are addressed under the
  owner `standard`. None of the modules in `conformance/` uses that owner.
  They use `alex`, `paper`, `example`, `reference`, `happy-camp`, `uniti`,
  and others. Many cases need several owners to show what they test: a shop
  that uses Alex's module (U2), a clinic and a pharmacy that each add a
  choice and bridge them (U4), a shop that changes cashier module (7.1). This
  is a contradiction between the text and the tests (blocker H4 in
  [`decisions/0052`](0052-quick-test-then-lock.md)). It was already there in
  the Indonesian text.
- The table of 08 §2.9 names "rejection of facts with a wrong form" in the
  group Facts. No conformance example rejects an action because of a FACT
  rule. The reference calculator reads a fact with a wrong form inside an
  example as a notation error, not as a rejection. The only form rules tested
  by rejection are CONCEPT-18 and VALUE-16.

**Decision**
1. The conformance tests are the examples in the files of `conformance/`.
   Those files belong to the standard. The modules inside them are example
   data: they may use any owner, so that one case can show several
   organizations working together. They are run only in the space of an
   example (PROOF-8) and are never installed as content.
2. PROOF-25 and the sentence in 08 §2.9 are written that way.
3. The missing rejection examples for facts with a wrong form are a **known
   gap** of v0.1. They are recorded in 08 §8 and in `README.md`. Filling the
   gap needs the reference calculator to report a fact with a wrong form in
   an action as a rejection, which is a new capability. It enters through the
   findings gate ([`decisions/0046`](0046-findings-gate.md)) after v0.1 is
   locked.

**Alternatives**
- *Give every module in `conformance/` the owner `standard`.* Rejected: the
  cases about versions, bridges, and modules of different organizations would
  lose what they test, and every case would have to be checked again.
- *Use the owner `example` for all of them.* Rejected for the same reason:
  one owner cannot show two organizations.
- *Write the missing rejection examples now as notation errors.* Rejected: a
  notation error is not a rejection by FACT rules (PROOF-32), so such an
  example would prove something else.

**Consequences**
- `08-proof`: §2.9, PROOF-25, and §8 open question 6.
- `README.md`: a list of known gaps.
- `rules.md` is rebuilt. No example and no expected result changes.
