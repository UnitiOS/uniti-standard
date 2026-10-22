# Overview

Status: guide; not normative

> [Uniti Standard](../README.md) › Guide · for a reader who wants a map of the
> standard without reading all of it

This guide points and explains. It adds no rule. When this guide and the
normative text differ, the normative text wins.

## The idea in five sentences

1. An organization really stores only **facts**: what happened and what is
   true. Everything else is worked out from them
   ([`00-principles.md`](../00-principles.md) §1, FACT-4).
2. Facts are only added. A correction or a retraction is a new fact that
   points to the old one, so what was known on any day can be read back (P5).
3. The standard fixes the **form** (how to record anything) and leaves the
   **content** (the words and logic of a domain) free. Content is always
   written in the form (P1, P2).
4. Every piece of content has an address that contains its owner, so two
   builders never collide (P6, P7).
5. Every piece of logic carries **examples**: facts and the result that must
   come out of them. Content is accepted only when its examples are proven
   (P9).

The three layers are form, vocabulary, and modules
([`00-principles.md`](../00-principles.md) §3). Part A is the form. Part B is
content, which may grow.

## The normative documents, in reading order

Each form document has the same eight sections: Purpose, Definitions, Rules,
Examples, Not examples, Reasons, Outside standards, Open questions. Terms are
in the [glossary](../01-glossary.md). The full list of rules is in
[`rules.md`](../rules.md); the counts below come from there (218 rules in 9
documents).

### 00 Principles

[`00-principles.md`](../00-principles.md). Settles why the standard exists,
what it governs, the three layers, twelve principles (P1 to P12), how outside
standards are treated, and what "conforming" means for content and for
software. Terms: [form, content, vocabulary,
module](../01-glossary.md#general-terms), [requirement keyword,
conform](../01-glossary.md#rules). It has principles, not numbered rules.
Read §4 first.

### 01 Glossary

[`01-glossary.md`](../01-glossary.md). Gives the one meaning of every term.
A new term is added here before it is used elsewhere. It has no rules. Look a
term up when a document uses it.

### Form 1: Facts

[`form/01-facts.md`](../form/01-facts.md). Settles what a fact is, how facts
change (by kind, never by editing), who recorded them, and how a value is read
at two times. Terms: [entity, fact, valid time, recorded time, fact kind,
action, actor](../01-glossary.md#facts). Prefix `FACT`, 25 rules. Rules:
[§3](../form/01-facts.md#3-rules); index: [`rules.md`](../rules.md#facts).

### Form 2: Addresses

[`form/02-addresses.md`](../form/02-addresses.md). Settles the name of every
piece of content: owner, module, name, with no version inside, and the
temporary root. Terms: [address, root, version
reference](../01-glossary.md#addresses-and-change). Prefix `ADDRESS`, 15
rules. Rules: [§3](../form/02-addresses.md#3-rules); index:
[`rules.md`](../rules.md#addresses).

### Form 3: Values

[`form/03-values.md`](../form/03-values.md). Settles the seven value types,
exact numbers, quantity and unit, direction, date and instant, text, choice
lists, and references. Terms: [value type, quantity, unit, direction, choice
list, reference](../01-glossary.md#facts). Prefix `VALUE`, 19 rules. Rules:
[§3](../form/03-values.md#3-rules); index: [`rules.md`](../rules.md#values).

### Form 4: Concepts and properties

[`form/04-concepts.md`](../form/04-concepts.md). Settles how a class of
things (a concept) and what is said about it (a property) are described by
cards, how a property applies to a concept, child concepts, type and role,
labels, and the check per action. Terms: [concept, concept card, property
card, parent, role, required](../01-glossary.md#content). Prefix `CONCEPT`,
22 rules. Rules: [§3](../form/04-concepts.md#3-rules); index:
[`rules.md`](../rules.md#concepts-and-properties).

### Form 5: Relations

[`form/05-relations.md`](../form/05-relations.md). Settles the closed list of
ways one piece of content may point to another, who may state them, and
bridges to outside standards. Terms: [relation, structural relation, meaning
relation, applies to, bridge](../01-glossary.md#content). Prefix `RELATION`,
12 rules. Rules: [§3](../form/05-relations.md#3-rules); index:
[`rules.md`](../rules.md#relations).

### Form 6: Calculation rules

[`form/06-calculation-rules.md`](../form/06-calculation-rules.md). The
largest document. Settles how numbers that are not recorded are derived from
facts: computed properties, helpers, constraints, contributions, the operation
list, time and numbers inside rules, empty and not computable, rejection, and
projection. Terms: [computed property, constraint, expression, empty, not
computable, rejection record, projection](../01-glossary.md#content). Prefix
`CALC`, 57 rules (a few numbers are revoked). Rules:
[§3](../form/06-calculation-rules.md#3-rules); index:
[`rules.md`](../rules.md#calculation-rules).

### Form 7: Change

[`form/07-change.md`](../form/07-change.md). Settles drafts and frozen
versions, the kinds of change between versions, deprecated and withdrawn
marks, and using other modules by exact version. Terms: [draft, version,
freeze, deprecated, withdrawn](../01-glossary.md#addresses-and-change).
Prefix `CHANGE`, 15 rules. Rules: [§3](../form/07-change.md#3-rules); index:
[`rules.md`](../rules.md#change).

### Form 8: Proof

[`form/08-proof.md`](../form/08-proof.md). Settles examples (compute, accept,
reject), their parts, the expected result, which content needs examples, the
freeze gate, the contracts between versions and between modules, and the
conformance tests. Terms: [example, local id, behavior change, conformance
tests](../01-glossary.md#content). Prefix `PROOF`, 32 rules. Rules:
[§3](../form/08-proof.md#3-rules); index: [`rules.md`](../rules.md#proof).

### Appendix A: Notation

[`appendix/A-notation.md`](../appendix/A-notation.md). Settles how cards,
rules, and examples are written in the reference notation, so that every
reader reads the same writing the same way. It adds no meaning: if it differs
from a form document, the form document is correct (§2.1). Terms: [reference
notation, binding, keyword, full and short
form](../01-glossary.md#content). Prefix `NOTATION`, 21 rules. Rules:
[§3](../appendix/A-notation.md#3-rules); index:
[`rules.md`](../rules.md#appendix-a-notation).

### Content (part B)

[`content/README.md`](../content/README.md). The map of the shared content:
card templates, code lists, the calculation library, and the first vocabulary
(`uniti/party`, `uniti/item`, `uniti/payment`). It also gives the vocabulary
entry rules (§3). It has no rule prefix and no rules in `rules.md`; its
requirements are gathered from part A (for example CONCEPT-2, PROOF-16,
RELATION-11).

## Useful, but not normative

| Place | What it is |
|---|---|
| [`decisions/`](../decisions/) | 55 decision records: why things are as they are |
| [`conformance/README.md`](../conformance/README.md) | How to run the worked cases, per file and per level. The cases themselves are the conformance tests of [`form/08-proof.md`](../form/08-proof.md) §2.9 and belong to the standard |
| [`reference/`](../reference/README.md) | The reference calculator (Python) and its tests |
| [`rules.md`](../rules.md) | Generated index of all 218 rules |
| [`tour.md`](tour.md) | One small story, from a fact to a rejection |
| [`implementing.md`](implementing.md) | A guide for people who build software |

## Where do I find ...

| Question | Go to |
|---|---|
| What is in a fact? | [01 §2.1](../form/01-facts.md#21-the-parts-of-a-fact), FACT-1 |
| How is a wrong fact corrected? | [01 §2.3](../form/01-facts.md#23-fact-kinds), FACT-11, FACT-12 |
| How is time read (valid time and as of)? | [01 §2.5](../form/01-facts.md#25-reading-facts-at-two-times), FACT-17 |
| Why is a total not stored as a fact? | [01 §2.7](../form/01-facts.md#27-computed-values-are-not-facts), FACT-4 |
| How is an address built? | [02 §2.2](../form/02-addresses.md#22-structure-of-an-address), ADDRESS-1 |
| Why is there no version in an address? | [02 §2.3](../form/02-addresses.md#23-an-address-does-not-contain-a-version), ADDRESS-4 |
| What is the root? | [02 §2.5](../form/02-addresses.md#25-the-temporary-root), ADDRESS-15 |
| How is a number written with a unit? | [03 §2.3](../form/03-values.md#23-quantity-and-unit), VALUE-5 |
| Which value types exist? | [03 §2.1](../form/03-values.md#21-value-types), VALUE-1 |
| How does a property apply to a concept? | [04 §2.3](../form/04-concepts.md#23-a-property-that-applies-to-a-concept), CONCEPT-6 to CONCEPT-8 |
| How is a computed property defined? | [06 §2.3](../form/06-calculation-rules.md#23-computed-property), CALC-4 to CALC-6 |
| What does "not computable" mean? | [06 §2.9](../form/06-calculation-rules.md#29-empty-and-not-computable), CALC-28 to CALC-30 |
| How does a constraint reject an action? | [06 §2.12](../form/06-calculation-rules.md#212-constraint), CALC-38, CALC-41 |
| How does a module version change? | [07 §2.1 and §2.2](../form/07-change.md#21-draft-and-version), CHANGE-1 to CHANGE-7 |
| How is a module bound to another version? | [07 §2.5](../form/07-change.md#25-using-other-modules), CHANGE-14, CHANGE-15 |
| What does an example contain? | [08 §2.2](../form/08-proof.md#22-parts-of-an-example), PROOF-2 |
| Which content needs examples? | [08 §2.5](../form/08-proof.md#25-when-examples-are-required), PROOF-13 to PROOF-16 |
| When can a version be frozen? | [08 §2.6](../form/08-proof.md#26-the-freeze-gate), PROOF-18 |
| How is an example line written? | [A §2.9](../appendix/A-notation.md#29-examples) |
| How do I add to the shared vocabulary? | [Content §3](../content/README.md#3-vocabulary-entry-rules) |
