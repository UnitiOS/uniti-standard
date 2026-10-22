# Change log

Status: not normative; what changed in each version of the Uniti Standard

Every version lists its changes here, and names every relaxing of a strict
answer separately
([`decisions/0059`](decisions/0059-compatibility-promise.md)). What each kind
of version may contain is in "Versions and compatibility" in
[`README.md`](README.md).

## v0.1.0 (2026-10-22): locked

The first version, locked. Its normative documents have the status
**locked**: v0.1 no longer grows, and until it is stable it changes only for
blockers found while building the first system
([`decisions/0052`](decisions/0052-quick-test-then-lock.md)).

### What v0.1 contains

- Part A, the form: facts, addresses, values, concepts, relations,
  calculation rules, change, and proof (`form/01` to `form/08`), with 221
  rules ([`rules.md`](rules.md)).
- The reference notation ([`appendix/A-notation.md`](appendix/A-notation.md)).
- Part B, the first content ([`content/`](content/README.md)).
- The conformance tests: 23 case files with 188 examples, in three levels
  ([`conformance/`](conformance/README.md)).
- The reasons: 59 decision records ([`decisions/`](decisions/README.md)).
- Reading aids and a reference calculator that runs every example, which are
  not normative.

### Content frozen

These content modules are frozen as version 1 by the owner on 2026-10-22,
with no previous version (CHANGE-3): `uniti/unit@v1`, `uniti/calc@v1`,
`uniti/party@v1`, `uniti/item@v1`, `uniti/payment@v1`.

### Changes in stage 8, from the Indonesian text to v0.1.0

The standard was shaped in Indonesian up to stage 7 (Indonesian archive,
`PERUBAHAN.md`). Stage 8 moved it to English and locked it. Changes that touch
the normative text:

- **English is the only normative text**
  ([`decisions/0055`](decisions/0055-locked-in-english.md)). The direction
  `posisi` became `position`.
- **The notation was made unambiguous** (appendix A): a thousands comma is
  followed by exactly three digits, so `1,5` is not a number; units may be
  written in the plural; the duration codes `s`, `min`, `h`, `d`, `wk` are not
  written (NOTATION-8); and the reason in §6 was rewritten to match.
  [`decisions/0051`](decisions/0051-additions-from-first-content.md) now
  points to L3 of the cross-domain test.
- **Example names were made universal**: people, organizations, and local
  payment systems got plain English names. Structure, numbers, and results did
  not change. IDR and the Indonesian time zones stay, because they are real
  codes.
- **Owners inside the conformance tests**: PROOF-25 and 08 §2.9 now say that
  the modules inside `conformance/` may use any owner
  ([`decisions/0056`](decisions/0056-conformance-test-owners-and-known-gap.md)).
- **Closure before the lock**
  ([`decisions/0057`](decisions/0057-closure-before-lock.md)): one action at a
  time (CALC-58); unit powers up to 3; `unit_of` and `history` for empty
  values, compound units, and properties with many values; an entity with no
  type fact in the tie-breaker; one version of each module in an organization
  (CHANGE-16); no uninstalling of a module in use (CHANGE-17); and an old gap
  in a required property does not block a correction (CONCEPT-18).
- **Clarified in the last reading before the lock**: only `history` of a
  property with one value is ordered (06 §2.5); the power limit holds for
  `power` too (06 §2.8); actions are checked in the order they are recorded
  also when their recorded times are equal (06 §2.12); moving to another
  version of a module is not an uninstall (07 §2.5).
- **Rejection of facts with a wrong form**: new conformance examples for
  FACT-2, FACT-9, FACT-10, FACT-11, FACT-13, and FACT-14, and "in force" in
  FACT-14 is read from the facts before the action
  ([`decisions/0058`](decisions/0058-rejection-of-facts-with-a-wrong-form.md)).
- **The compatibility promise**
  ([`decisions/0059`](decisions/0059-compatibility-promise.md)).
- Open questions answered by existing text were marked so: 03 §8 question 2,
  04 §8 question 3, 05 §8 question 1, 06 §8 questions 1, 7, and 13, 08 §8
  questions 4 and 6.

Added, not normative: [`README.md`](README.md) with what is normative and a
list of known gaps, [`GOVERNANCE.md`](GOVERNANCE.md),
[`ROADMAP.md`](ROADMAP.md), [`AGENTS.md`](AGENTS.md), the guides in
[`guide/`](guide/overview.md), the rules index [`rules.md`](rules.md), and the
explanation of the conformance tests per level.

The reference calculator follows every change above, and also calculates the
members of a collection of entities with no order in tie-breaker order, as the
text already said (quick test S9, `reference/README.md` A34).

### Known gaps

- No conformance example tests the source and reason of an action (FACT-19 to
  FACT-21).
- Ownership and governance with outside parties: v0.2.
- A machine format for exchange: postponed.
- Parts marked [provisional]: redaction, the personal data mark, and the
  root domain.

See [`ROADMAP.md`](ROADMAP.md) for when each is planned.

### Notes for later

- In the conformance tests, `alex/rental@v3`
  ([`conformance/00-form-examples.md`](conformance/00-form-examples.md)) does
  not require `daily_rate`, while `alex/rental@v1` and `@v2`
  ([`conformance/15-change.md`](conformance/15-change.md)) do. Each file runs
  in its own space, so no result is affected. It came from the Indonesian
  text and is example data only.
