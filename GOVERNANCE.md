# Governance

Status: not normative; the interim way the standard is looked after, until
ownership and governance are settled in v0.2
([`decisions/0048`](decisions/0048-ownership-to-v02.md))

This page says who decides about the Uniti Standard, how a change is proposed,
and what limits every change. It covers the standard itself: part A, part B,
the notation, and the conformance tests. Content that others write in their
own modules is theirs, and changes by the versions of those modules
([`form/07-change.md`](form/07-change.md)).

## 1. Who decides

Until v0.2, the **owner** of this repository is the only steward of the
standard. The owner approves every change to the normative text (see "What is
normative" in [`README.md`](README.md)), every decision record, and every
version.

Anyone may propose a change. A proposal is not a decision until the owner
approves it and it is recorded.

Who else decides, and how parties outside the owner take part, for example in
the vocabulary, is settled in v0.2 together with ownership.

## 2. How to propose a change

Write a **finding**:

1. **The case.** What you were doing, in which domain, written as facts and a
   question if you can. A finding without a practical case is recorded, but
   does not change the form
   ([`decisions/0046`](decisions/0046-findings-gate.md)).
2. **What the text says.** The rule IDs and sections involved, for example
   "CALC-18, `form/06-calculation-rules.md` §2.5".
3. **What is wrong or missing.** Two readings, a case that cannot be written,
   a contradiction, or a result you think is wrong.
4. **What you propose**, if you have a proposal.

## 3. What a finding can lead to

Every finding is sorted by the **findings gate**
([`decisions/0046`](decisions/0046-findings-gate.md)). It may change the form
only if it **arises from a case** and is **about the form**: the text does not
say what must be done, so two implementations that both follow it could give
different results. Otherwise it is one of these:

| Group | What happens |
|---|---|
| Content | Written in the vocabulary, the calculation library, or the code lists ([`content/`](content/README.md)) |
| Example fix | An example or explanation that does not match its rule is fixed; the rule stays |
| Postponed | Recorded in [`ROADMAP.md`](ROADMAP.md) without a decision |

A finding that passes the gate is answered with the smallest change. Writing
it with the form that already exists is tried first. A new operation must
also pass the entry test for the core
([`decisions/0045`](decisions/0045-core-operations-and-calculation-library.md)).

## 4. Limits on every change

- **The compatibility promise**
  ([`decisions/0059`](decisions/0059-compatibility-promise.md)). A defined
  result never changes, and an accepted action stays accepted. Only a result
  that is not computable, a rejection by a rule of the standard, or a refusal
  may be relaxed, for a practical case.
- **While v0.1 is locked**, only **blockers** are fixed
  ([`decisions/0052`](decisions/0052-quick-test-then-lock.md)): two readings
  (H1), a real case that cannot be written (H2), a forced full recalculation
  (H3), or two documents that contradict each other (H4). Each blocker gets
  at most two rounds of fixing; after that the owner decides. Everything else
  waits in the roadmap.
- **Fixed form, free content**
  ([`decisions/0002`](decisions/0002-fixed-form-free-content.md)). A need of
  one domain goes into content first. The form does not become a programming
  language.
- **The text stays in plain words.** Rules follow the writing conventions in
  [`CONTRIBUTING.md`](CONTRIBUTING.md): one sentence per rule where possible, terms from
  the glossary, no business words in part A outside examples.

## 5. How a change is made

1. **A decision record** in [`decisions/`](decisions/README.md): the context,
   the decision, the alternatives that were rejected, and the consequences,
   with the next number. A decision is never deleted; a later one may replace
   it in whole or in part.
2. **The text.** Only the outcome goes into the normative documents. New rules
   get new IDs; an ID is never reused.
3. **The proof.** Every change of behavior comes with conformance examples,
   and the reference calculator follows it, with its tests passing.
4. **The indexes.** `rules.md` is rebuilt (`python -m tools.rules_index` from
   `reference/`), and the counts and lists in the guides are updated.
5. **The change log.** Every version lists its changes in `CHANGELOG.md`, and
   names every relaxing separately.

## 6. Versions and status

The version numbers and what each may contain are in "Versions and
compatibility" in [`README.md`](README.md). The status of a document goes
draft, proposed, locked, stable. v0.1 becomes **stable** after the first
system passes the level 1 conformance tests, or before the ecosystem is opened
to outside parties, whichever comes first
([`decisions/0052`](decisions/0052-quick-test-then-lock.md)). What must be
done before that is in [`ROADMAP.md`](ROADMAP.md).

## 7. Not decided yet

- Who besides the owner decides, and how: v0.2, with ownership.
- The license of the text and of the reference calculator: decided before the
  standard is published to outside parties.
- The real root domain of addresses: before v0.1 is stable (ADDRESS-15).
