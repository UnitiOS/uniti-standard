# Decisions

Every decision that shapes the standard is recorded here, one decision per
file, numbered in sequence and never reused. A decision that is later
replaced is not deleted: it is given the status **replaced by NNNN**, and the
decision that replaces it names what it replaces. A decision that is only
partly replaced is given the status **partly replaced by NNNN**, together
with the part that is replaced, and the other parts remain in force.

## Structure

```
# NNNN. Short title
Date: YYYY-MM-DD
Status: accepted | replaced by NNNN | partly replaced by NNNN

Context       The problem or question that needs a decision
Decision      What was decided, as firmly as possible
Alternatives  Other choices that were considered, and why they were not chosen
Consequences  What changes or must be done because of this decision
```

## List

| No | Title | Date | Status |
|---|---|---|---|
| [0001](0001-standard-first.md) | Standard first, software follows | 2026-10-17 | partly replaced by 0052 |
| [0002](0002-fixed-form-free-content.md) | Fixed form, free content; three layers | 2026-10-17 | accepted |
| [0003](0003-outside-standards.md) | Its own standard, with three ways of relating to outside standards | 2026-10-17 | accepted |
| [0004](0004-how-to-write.md) | Location, language, and how the standard is reviewed | 2026-10-17 | partly replaced by 0048 and 0052 |
| [0005](0005-facts-without-end-time.md) | Facts have no end time | 2026-10-17 | accepted |
| [0006](0006-fact-kinds.md) | Six fact kinds, derived from two questions | 2026-10-17 | accepted |
| [0007](0007-provenance.md) | Provenance: its parts are form, its choices are content | 2026-10-17 | accepted |
| [0008](0008-computed-values.md) | Computed values are not facts | 2026-10-17 | accepted |
| [0009](0009-redaction.md) | Redaction of personal data | 2026-10-17 | provisional |
| [0010](0010-address-structure.md) | The address structure now, its root later | 2026-10-17 | accepted |
| [0011](0011-addresses-and-identifiers.md) | Addresses without versions; the identifier of an entity is random | 2026-10-17 | accepted |
| [0012](0012-versions-deprecated-withdrawn.md) | Versions in sequence; deprecated and withdrawn without deleting | 2026-10-17 | accepted |
| [0013](0013-value-types.md) | Seven value types; money and measures as numbers with units | 2026-10-17 | accepted |
| [0014](0014-quantities-and-units.md) | Quantity on the property, unit on the value | 2026-10-17 | accepted |
| [0015](0015-dates-and-instants.md) | Dates and instants | 2026-10-17 | accepted |
| [0016](0016-choice-lists.md) | Open or closed choice lists | 2026-10-17 | accepted |
| [0017](0017-standalone-properties.md) | Standalone properties, which may be added to concepts owned by others | 2026-10-17 | accepted |
| [0018](0018-types-and-roles.md) | Types and roles | 2026-10-17 | accepted |
| [0019](0019-one-parent.md) | One parent | 2026-10-17 | accepted |
| [0020](0020-required-per-action.md) | Required properties are checked per action | 2026-10-17 | accepted |
| [0021](0021-concept-cards.md) | Concept cards and property cards | 2026-10-17 | accepted |
| [0022](0022-personal-data-marker.md) | Personal data marker | 2026-10-17 | provisional |
| [0023](0023-relation-list.md) | A closed relation list | 2026-10-17 | accepted |
| [0024](0024-bridges.md) | Bridges by anyone, as annotations | 2026-10-17 | accepted |
| [0025](0025-three-kinds-of-numbers.md) | Three kinds of numbers: derived, decided, estimated | 2026-10-19 | accepted |
| [0026](0026-layered-operations.md) | Calculation operations that are closed, layered, and always finish | 2026-10-19 | partly replaced by 0045 |
| [0027](0027-number-direction.md) | Every number states its direction | 2026-10-19 | accepted |
| [0028](0028-computed-properties.md) | Computed properties are read like properties | 2026-10-19 | accepted |
| [0029](0029-time-in-calculation.md) | Time in calculation: two times, no "now", half-open ranges | 2026-10-19 | accepted |
| [0030](0030-not-computable.md) | Not computable, not 0 | 2026-10-19 | accepted |
| [0031](0031-open-computed-properties.md) | Open computed properties and contributions | 2026-10-19 | accepted |
| [0032](0032-projections.md) | Projections: stored calculation results | 2026-10-19 | accepted |
| [0033](0033-reported-results.md) | Reported results are recorded as facts about the report | 2026-10-19 | accepted |
| [0034](0034-constraints.md) | Constraints: yes/no rules checked per action | 2026-10-19 | accepted |
| [0035](0035-rejection-records.md) | Rejection records | 2026-10-19 | accepted |
| [0036](0036-three-kinds-of-examples.md) | Three kinds of examples | 2026-10-19 | accepted |
| [0037](0037-required-examples.md) | Required examples, and the freezing gate | 2026-10-19 | accepted |
| [0038](0038-examples-as-contracts.md) | Examples as a contract between versions and between modules | 2026-10-19 | accepted |
| [0039](0039-data-in-examples.md) | Data in examples | 2026-10-19 | accepted |
| [0040](0040-conformance-tests.md) | Conformance tests for implementations | 2026-10-19 | accepted |
| [0041](0041-numbers-in-calculation.md) | Numbers in calculation: exact fractions, written rounding, units count | 2026-10-19 | partly replaced by 0045 |
| [0042](0042-reference-notation.md) | Reference notation: one way to write rules, examples, and cards | 2026-10-19 | accepted |
| [0043](0043-additions-from-notation.md) | Seven additions in meaning found while writing the notation | 2026-10-19 | accepted |
| [0044](0044-additions-from-reference-calculator.md) | Additions in meaning found by the reference calculator | 2026-10-19 | partly replaced by 0045 |
| [0045](0045-core-operations-and-calculation-library.md) | Core operations and calculation library | 2026-10-19 | accepted |
| [0046](0046-findings-gate.md) | Findings gate: when a finding may change the form | 2026-10-20 | accepted |
| [0047](0047-constraints-and-backdated-changes.md) | The entities and times at which a constraint is read | 2026-10-20 | accepted |
| [0048](0048-ownership-to-v02.md) | Ownership moves to v0.2 | 2026-10-20 | partly replaced by 0052 |
| [0049](0049-additions-from-cross-domain-test.md) | Additions from the cross-domain test | 2026-10-20 | accepted |
| [0050](0050-code-lists.md) | Code lists | 2026-10-20 | accepted |
| [0051](0051-additions-from-first-content.md) | Additions from the first content | 2026-10-20 | accepted |
| [0052](0052-quick-test-then-lock.md) | Stage 7 becomes a quick test, then v0.1 is locked, and the first system is built new | 2026-10-20 | accepted |
| [0053](0053-reading-corrected-facts.md) | Reading facts whose history has been corrected | 2026-10-20 | accepted |
| [0054](0054-reference-choices-into-text.md) | Choices of the reference calculator moved into the text | 2026-10-20 | accepted |
| [0055](0055-locked-in-english.md) | v0.1 is locked in English, in its own directory | 2026-10-20 | accepted |
| [0056](0056-conformance-test-owners-and-known-gap.md) | Owners inside the conformance tests, and a known gap | 2026-10-22 | partly replaced by 0058 |
| [0057](0057-closure-before-lock.md) | Closure before the lock | 2026-10-22 | accepted |
| [0058](0058-rejection-of-facts-with-a-wrong-form.md) | Rejection of facts with a wrong form | 2026-10-22 | accepted |
| [0059](0059-compatibility-promise.md) | The compatibility promise | 2026-10-22 | accepted |
