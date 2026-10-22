# Roadmap

Status: not normative; what comes after v0.1, and what is still open

v0.1 is complete and is about to be locked. What follows is grouped by
**when** it is needed, not by document. Every item that changes the form goes
through the findings gate
([`decisions/0046`](decisions/0046-findings-gate.md)) and keeps the
compatibility promise
([`decisions/0059`](decisions/0059-compatibility-promise.md)): a defined
result never changes, only strict answers may be relaxed. How a change is
made is in [`GOVERNANCE.md`](GOVERNANCE.md).

## 1. Before v0.1 is stable

v0.1 becomes stable after the first system passes the level 1 conformance
tests, or before the ecosystem is opened to outside parties, whichever comes
first ([`decisions/0052`](decisions/0052-quick-test-then-lock.md)).

| Item | Where |
|---|---|
| The real root domain, replacing `https://uniti.example` once | `form/02-addresses.md` ADDRESS-15, §8 question 1 [provisional] |
| Redaction and the personal data mark, after a review of data protection law | `form/01-facts.md` §2.6 and §8 question 1, `form/04-concepts.md` CONCEPT-20 and §8 question 2, `form/06-calculation-rules.md` §2.9 and §2.15 [provisional] |
| The license of the text and of the reference calculator | Before the standard is published to outside parties ([`GOVERNANCE.md`](GOVERNANCE.md) §7) |
| Blockers found while building the first system | Fixed in v0.1.x under [`decisions/0052`](decisions/0052-quick-test-then-lock.md) |

## 2. v0.2: ownership and the ecosystem

| Item | Where |
|---|---|
| Who may write what, and how the form itself changes (`form/09-ownership.md`) | [`decisions/0048`](decisions/0048-ownership-to-v02.md); `form/07-change.md` §8 question 2 |
| Governance with outside parties: who decides besides the owner | [`GOVERNANCE.md`](GOVERNANCE.md) §1 |
| Who holds a shared module for one domain, for example Rental, since the vocabulary asks for two domains | Quick test S1 |
| Where the deprecated and withdrawn markers of a module are recorded | `form/07-change.md` §8 question 1 |
| Who runs the examples when a module is frozen on its author's machine | `form/08-proof.md` §8 question 1 |
| Who marks a behavior change in the vocabulary | `form/08-proof.md` §8 question 5 |
| Private content of an organization: its own root or the shared one | `form/02-addresses.md` §8 question 2 |
| One entity in two organizations, addresses of entities across organizations, and references to them | `form/01-facts.md` §8 question 2, `form/02-addresses.md` §8 question 3, `form/03-values.md` §8 question 6 |
| Stating the version of the standard in a conformance claim, as a rule | PROOF-26; README "Versions and compatibility" |

## 3. After the first system runs

| Item | Where |
|---|---|
| The cost of checking constraints at later valid times (06 §2.12 step 2), measured | Quick test S6 |
| Partial installation: a module with one rule above the level of an implementation is now refused as a whole | Quick test S4; `form/08-proof.md` §2.9 |
| A scale test and the second implementation, measured by the conformance tests | [`decisions/0052`](decisions/0052-quick-test-then-lock.md) item 5 |
| Resource limits for a rule that is certain to finish but very expensive | `form/06-calculation-rules.md` §8 question 6 |
| Large examples made by a data generator | `form/08-proof.md` §8 question 2 |

## 4. Added when a practical case asks for it

Each of these can be added later without changing a defined result. None of
them has a case yet. An answer must add a new way of writing or asking; it
must not change how something that is already written is read.

| Question | Where |
|---|---|
| Facts about facts, besides provenance | `form/01-facts.md` §8 question 3 |
| Self-made units such as "box" or "package" | `form/03-values.md` §8 question 1 |
| An organization with branches in several time zones | `form/03-values.md` §8 question 3 |
| Limits on values as part of the property card | `form/03-values.md` §8 question 4 |
| Ordered choice lists | `form/03-values.md` §8 question 5 |
| A concept that must not be a direct type | `form/04-concepts.md` §8 question 1 |
| Bridges between number properties with different units | `form/05-relations.md` §8 question 2 |
| `history` of a computed property | `form/06-calculation-rules.md` §8 question 2 |
| Rounding to even, day conventions such as 30/360, other ways of calculating | `form/06-calculation-rules.md` §8 question 3 (calculation library) |
| A child concept with its own rule for a computed property of its parent | `form/06-calculation-rules.md` §8 question 5 |
| Reading with the module set of a past *R* (needs a record of when a module was installed) | `form/06-calculation-rules.md` §8 question 8 |
| Retention of rejection records that contain personal data | `form/06-calculation-rules.md` §8 question 9 |
| Examples, types, binding, and named arguments for helpers | `form/06-calculation-rules.md` §8 questions 10 to 12 |
| Examples for bridges | `form/08-proof.md` §8 question 3 |
| ASCII equivalents of the symbols, and keywords in other languages | `appendix/A-notation.md` §8 questions 1 and 2 |
| A machine format for exchange, such as JSON | `appendix/A-notation.md` §8 question 3; [`decisions/0055`](decisions/0055-locked-in-english.md) |
| Source and reason of an action in the notation of examples, so that FACT-19 to FACT-21 can be tested | [`decisions/0058`](decisions/0058-rejection-of-facts-with-a-wrong-form.md); README "Known gaps" |

## 5. Content

These grow in part B ([`content/`](content/README.md)) and do not change the
form.

| Item | Where |
|---|---|
| A guide in the vocabulary: when a date should be a valid time and when a property | Quick test S5 |
| A guide in the vocabulary: one event recorded in two modules is counted twice (decision 0031) | Quick test S3 |
| More concepts in the vocabulary, more code lists, more operations in the calculation library | [`content/README.md`](content/README.md) |

## 6. The findings of the quick test

The quick test of stage 7 (Indonesian archive, `uji/03-uji-singkat.md` §7)
left ten findings that were not blockers. Where each stands now:

| Finding | Status |
|---|---|
| S1. A shared module for one domain has no official place | v0.2, §2 |
| S2. Uninstalling a module whose facts remain | Closed: CHANGE-17 ([`decisions/0057`](decisions/0057-closure-before-lock.md)) |
| S3. One event recorded in two modules is counted twice | Content, §5 |
| S4. Partial installation | After the first system, §3 |
| S5. When a date is a valid time and when a property | Content, §5 |
| S6. Cost of checking constraints at later times | After the first system, §3 |
| S7. Two installed modules use different versions of one module | Closed: CHANGE-16 ([`decisions/0057`](decisions/0057-closure-before-lock.md)) |
| S8. Redacting a value that a constraint reads makes the constraint not computable, so the redaction is rejected | With redaction, §1 |
| S9. The reference calculator did not calculate the members of a reference with many values in tie-breaker order | Closed: the program is fixed, the text was already clear (CALC-52, [`reference/README.md`](reference/README.md) A34) |
| S10. A property that becomes required blocks corrections of old records | Closed: CONCEPT-18, an old gap does not block ([`decisions/0057`](decisions/0057-closure-before-lock.md)) |
