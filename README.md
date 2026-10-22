# Uniti Standard

The Uniti Standard is a **shared form** for recording the facts, knowledge, and
logic of an organization. Anyone who follows it, whether an open source
community, a company, or an institution in any domain, can make content that
is immediately usable together with content made by others, without knowing
each other and without conflict.

> **Status: v0.1, draft.** All parts of v0.1 are written. The next step is to
> lock v0.1 ([`decisions/0052`](decisions/0052-quick-test-then-lock.md)).
> Until then, any part may still change.

---

## The idea in one minute

- An organization stores only **facts**: what happened and what is true,
  each with the time it is true and the time it was recorded. Facts are never
  edited or deleted; a correction is a new fact.
- Everything else, such as a balance, a total due, or a stock level, is
  **calculated** from the facts by written rules.
- The standard fixes the **form**, the way anything is written, and leaves
  the **content**, the words and logic of a domain, free.
- Every rule carries **examples**: facts and the result that must come out.
  A machine runs them, so a rule is accepted only when it is proven.

## Two parts

| Part | Contents | Nature |
|---|---|---|
| **A. Form** ([`form/`](form/01-facts.md)) | The way to record anything: the form of facts, addresses, values, concepts, relations, calculation rules, change, and proof | **Fixed.** Applies to all domains. May only grow, never be changed |
| **B. Content** ([`content/`](content/README.md)) | The first shared vocabulary, the card templates, the outside code lists that are used, and the calculation library | **Flexible.** May follow outside standards, may be made by oneself, and keeps growing |

An analogy: the form is the **grammar**, the vocabulary is the **shared
words**, and a module is the **story** that each person writes with that
grammar and those words. The full explanation is in
[`00-principles.md`](00-principles.md).

## Start here

Pick the path that fits you. Each path starts short and goes deeper.

| You are | Read in this order |
|---|---|
| **New to the standard**, or deciding whether it fits | [`guide/tour.md`](guide/tour.md), one small story through every part → [`guide/overview.md`](guide/overview.md), a map of the whole standard → [`00-principles.md`](00-principles.md) |
| **Building software** that follows the standard | [`guide/overview.md`](guide/overview.md) → [`guide/implementing.md`](guide/implementing.md) → [`form/01-facts.md`](form/01-facts.md) to [`form/08-proof.md`](form/08-proof.md) and [`appendix/A-notation.md`](appendix/A-notation.md) → [`conformance/README.md`](conformance/README.md) → [`reference/README.md`](reference/README.md) |
| **Writing content**: a module or a vocabulary | [`00-principles.md`](00-principles.md) → [`01-glossary.md`](01-glossary.md) → [`form/04-concepts.md`](form/04-concepts.md), [`form/06-calculation-rules.md`](form/06-calculation-rules.md), and [`form/08-proof.md`](form/08-proof.md) → [`appendix/A-notation.md`](appendix/A-notation.md) → [`content/README.md`](content/README.md) and [`content/card-templates.md`](content/card-templates.md) |
| **A code agent** | [`AGENTS.md`](AGENTS.md) |
| **Looking for one rule** | [`rules.md`](rules.md), the index of all rules, by ID |
| **Asking why** something is as it is | [`decisions/`](decisions/README.md), one decision per file, with the alternatives that were rejected |

The normative documents are read in this order: `00` → `01` → `form/01` to
`form/08` → `appendix/A` → `content/`. Each of them has a navigation line at
the top with the previous and next document.

## What is normative

| Normative: this is the standard | Not normative: this helps you read and use it |
|---|---|
| [`00-principles.md`](00-principles.md) | [`guide/`](guide/overview.md): the tour, the overview, the implementer guide |
| [`01-glossary.md`](01-glossary.md) | [`rules.md`](rules.md): an index made from the text |
| [`form/`](form/01-facts.md): part A | [`decisions/`](decisions/README.md): the reasons |
| [`appendix/A-notation.md`](appendix/A-notation.md): the reference notation | [`reference/`](reference/README.md): the reference calculator, a program for comparison |
| [`content/`](content/README.md): part B | |
| The examples in [`conformance/`](conformance/README.md): the conformance tests of [`form/08-proof.md`](form/08-proof.md) §2.9 | |

When a guide or an index differs from the normative text, the normative text
is right, and the guide is what must be fixed.

## Map of the repository

| Place | Contents |
|---|---|
| [`00-principles.md`](00-principles.md) | Purpose, scope, the three layers, the principles, requirement keywords, conformance |
| [`01-glossary.md`](01-glossary.md) | The one meaning of every term |
| [`form/01-facts.md`](form/01-facts.md) | The form of one fact, and reading facts at two times |
| [`form/02-addresses.md`](form/02-addresses.md) | Unique and permanent addresses |
| [`form/03-values.md`](form/03-values.md) | Value types, numbers and units, dates and instants, choice lists |
| [`form/04-concepts.md`](form/04-concepts.md) | Concept cards and property cards, child concepts, types and roles |
| [`form/05-relations.md`](form/05-relations.md) | How content points to other content, including bridges |
| [`form/06-calculation-rules.md`](form/06-calculation-rules.md) | Computed properties, core operations and calculation library, constraints, projections |
| [`form/07-change.md`](form/07-change.md) | How to change without breaking what is old |
| [`form/08-proof.md`](form/08-proof.md) | Examples as contracts, and conformance tests |
| `form/09-ownership.md` | Who may write what, and how the form changes. Postponed to v0.2 ([`decisions/0048`](decisions/0048-ownership-to-v02.md)) |
| [`appendix/A-notation.md`](appendix/A-notation.md) | The reference notation: how to write rules, examples, and cards |
| [`content/`](content/README.md) | The first vocabulary, card templates, code lists, calculation library |
| [`conformance/`](conformance/README.md) | 23 case files with 188 examples, run as tests, with how to run them per level |
| [`guide/`](guide/overview.md) | Reading aids: tour, overview, implementer guide |
| [`rules.md`](rules.md) | The index of all 221 rules |
| [`decisions/`](decisions/README.md) | 59 decision records |
| [`reference/`](reference/README.md) | The reference calculator in Python, and its tests |
| [`GOVERNANCE.md`](GOVERNANCE.md) | Who decides, how to propose a change, and the limits on every change |
| [`ROADMAP.md`](ROADMAP.md) | What comes after v0.1, and every open question by when it is needed |
| [`AGENTS.md`](AGENTS.md) | Working rules for code agents in this repository |

To run all tests, from this folder (Python 3):

```
python -m unittest discover -s reference/tests -t reference
```

## The standard and software

This standard **does not name any software, database, or programming
language.**

- Software, including Uniti's own implementation, is an **executor** of the
  standard.
- When software differs from the standard, the **standard** is right, and the
  software is what must be fixed.
- The reference notation, the way of writing used in the standard documents and
  in the conformance tests, is detailed in
  [`appendix/A-notation.md`](appendix/A-notation.md). Other formats (for
  example YAML or RDF) may be used if the meaning is exactly the same. The
  form is the same, whatever the format. A machine format for exchange is
  postponed ([`decisions/0055`](decisions/0055-locked-in-english.md)).

---

## How to write the standard documents

### The layout of a form document

Every document in `form/` uses the same layout, so that every document can be
compared with the others and is easy to read for both people and machines:

```
# Name of the form
Status: draft | proposed | locked | stable

1. Purpose          What problem this form solves (2–3 sentences)
2. Definition       What the form is, as firmly as possible
3. Rules            Numbered; each uses a requirement keyword (00-principles §6)
4. Examples         At least two examples from different domains
5. Non-examples     What is deliberately not included
6. Reason           Why the form is like this, briefly (details in decisions/)
7. Outside standards  The equivalents, if any
8. Open questions
```

Rules get fixed numbers, for example `FACT-3`. A number that has been used is
never used again for another rule, even when the rule is later revoked.

### Writing style

- Short sentences. One rule, one sentence.
- Every term is used according to [`01-glossary.md`](01-glossary.md). A new term
  is added to the glossary **before** it is used.
- Examples are always taken from **at least two different domains**, for
  example a shop and a clinic, so that no rule quietly fits only one domain.
- Part A cannot contain terms belonging to one domain. Words such as
  "customer", "item", or "patient" may appear only in examples.

### The status of a document

| Status | Meaning |
|---|---|
| **draft** | Being written, free to change |
| **proposed** | Complete and under review |
| **locked** | A proposal that is no longer added to. Changes only for obstacles found when building the first system, each with its own decision ([`decisions/0052`](decisions/0052-quick-test-then-lock.md)) |
| **stable** | Approved. From then on it may only **grow**: new rules may be added, existing rules do not change their meaning and are not deleted |

### The [provisional] mark

A section, rule, or term marked **[provisional]** has its form written, but can
still change because it depends on outside parties or on a discussion that is
not finished, for example matters of law or ecosystem governance. Every
[provisional] mark comes with a note on what is still being waited for. A
document cannot become **stable** while it still contains a [provisional] mark
that has not been resolved or excepted in writing.

The list of what is marked [provisional] at present:

| Part | Waiting for |
|---|---|
| `form/01-facts.md` §2.6, FACT-23 to 25: redaction | Review of data protection law; ecosystem study, topic D2 |
| `form/04-concepts.md` §2.8, CONCEPT-20: personal data mark | Review of data protection law, together with redaction |
| `form/06-calculation-rules.md` §2.9 and §2.15: redacted values inside calculation and projections | Following redaction |
| `form/02-addresses.md` §2.5, ADDRESS-15: the provisional ‹root› `https://uniti.example` | The real domain; ecosystem study, topic C1 (Indonesian archive, `kajian/01-ekosistem.md`). To be replaced once before v0.1 is stable |

### Versions and compatibility

Whoever builds on v0.1 can rely on this
([`decisions/0059`](decisions/0059-compatibility-promise.md)):

- **A defined result never changes.** For the same facts, modules, and
  question, a value or empty stays the same in every later version, and an
  action that is accepted stays accepted.
- **Only the strict answers may be relaxed.** A result that is not
  computable, a rejection by a rule of the standard, or a refusal may become
  a defined result or an acceptance in a later version, for a practical case
  and with a decision of its own. Until then it keeps its reason kind or its
  rule.
- **Not covered:** parts marked [provisional], content inside modules (it
  changes by module versions, [`form/07-change.md`](form/07-change.md)), and
  the texts that are not normative. While v0.1 is locked and not yet stable,
  a blocker may change a defined result only where the text could be read two
  ways or contradicts itself, each time with a decision and an entry in the
  change log.

| Version | What it may contain |
|---|---|
| v0.1.0 | The version that is locked |
| v0.1.1, v0.1.2, … | Blocker fixes, words, links, new examples and guides; no relaxing |
| v0.2, v0.3, … | New rules and operations, relaxing, postponed parts such as ownership |

An implementation states the version and the level it conforms to, for
example "Uniti Standard v0.1, level 1". When a later version relaxes a
result, the conformance example that expected the old result is marked
replaced there, and stays the test for the older version.

### Known gaps

What v0.1 is known to lack, recorded so that nobody relies on it by mistake:

| Gap | Where it is recorded |
|---|---|
| No conformance example tests the source and reason of an action (FACT-19 to FACT-21): the notation of an action inside an example has neither | [`form/08-proof.md`](form/08-proof.md) §8, question 6; [`decisions/0058`](decisions/0058-rejection-of-facts-with-a-wrong-form.md) |
| Who may write what, and how the form changes (ownership) | Postponed to v0.2 ([`decisions/0048`](decisions/0048-ownership-to-v02.md)) |
| A machine format for exchange | Postponed ([`decisions/0055`](decisions/0055-locked-in-english.md)) |

### Changing the standard

Every decision that shapes the standard is recorded in `decisions/`, one
decision per file, with what was decided, the reasons, and the alternatives
that were rejected. The main documents only need to contain the outcome. A
finding changes the form only through the findings gate
([`decisions/0046`](decisions/0046-findings-gate.md)). How to propose a change,
and who decides, is in [`GOVERNANCE.md`](GOVERNANCE.md).

### Language and the Indonesian archive

English is the only normative text
([`decisions/0055`](decisions/0055-locked-in-english.md)). The standard was
shaped in Indonesian up to v0.1. That text, with its paper tests (`uji/`),
studies (`kajian/`), and version history (`PERUBAHAN.md`), is kept as an
archive outside this repository. A note such as "(Indonesian archive,
`uji/01-hitung.md`)" points to a file in that archive. Labels in other
languages, such as `label.id`, are content and stay where they are.
