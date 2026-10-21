# Uniti Standard

The Uniti Standard is a **shared form** for recording the facts, knowledge, and
logic of an organization. Anyone who follows it, whether an open source
community, a company, or an institution in any domain, can make content that
is immediately usable together with content made by others, without knowing
each other and without conflict.

> **Status: v0.1, draft. Being written step by step.**
> No part is stable yet. All content may still change until v0.1 is frozen.

---

## Two parts

| Part | Contents | Nature |
|---|---|---|
| **A. Form** (`form/`) | The way to record anything: the form of facts, addresses, values, concepts, relations, calculation rules, change, proof, ownership | **Fixed.** Applies to all domains. May only grow, never be changed |
| **B. Content** (`content/`) | The first shared vocabulary (starting from the enterprise) and the outside code lists that are used | **Flexible.** May follow outside standards, may be made by oneself, and keeps growing |

An analogy: the form is the **grammar**, the vocabulary is the **shared
words**, and a module is the **story** that each person writes with that
grammar and those words. The full explanation is in
[`00-principles.md`](00-principles.md).

## How to read

1. [`00-principles.md`](00-principles.md): the purpose, scope, and principles
   that bind the whole standard.
2. [`01-glossary.md`](01-glossary.md): the meaning of every term. Terms are
   used with the same meaning in all documents.
3. `form/`: part A, read in order. How to write it is in `appendix/`.
4. `content/`: part B.
5. `uji/`: proof that the form can be used in different domains.
6. `decisions/`: the reasons behind every decision, including the alternatives
   that were rejected.
7. `kajian/`: study material for matters that cannot be decided yet, such as
   law, governance, and ownership. **Not part of the standard.**

## Map of contents

| Document | Contents | Status |
|---|---|---|
| `00-principles.md` | Purpose, scope, principles, requirement keywords | draft |
| `01-glossary.md` | List of terms | draft |
| `form/01-facts.md` | The form of one fact | draft |
| `form/02-addresses.md` | Unique and permanent addresses | draft |
| `form/03-values.md` | Value types, numbers and units, dates and instants, choice lists | draft |
| `form/04-concepts.md` | Concept cards and property cards, child concepts, types and roles | draft |
| `form/05-relations.md` | How content points to other content, including bridges | draft |
| `form/06-calculation-rules.md` | Computed properties, core operations and calculation library, constraints, projections | draft; its paper test is in `uji/01-hitung.md` <!-- ARCHIVE-LINK: uji/01-hitung.md --> |
| `form/07-change.md` | How to change without breaking what is old | draft |
| `form/08-proof.md` | Examples as contracts, and conformance tests | draft |
| `form/09-ownership.md` | Who may write what, and how the form changes | postponed to v0.2, waiting for `kajian/01-ekosistem.md` <!-- ARCHIVE-LINK: kajian/01-ekosistem.md --> ([`decisions/0048`](decisions/0048-ownership-to-v02.md)) |
| `appendix/A-notation.md` | Reference notation: how to write rules, examples, and cards | draft |
| `content/` | The first vocabulary, card templates, code lists, calculation library ([`content/README.md`](content/README.md)) | draft |
| `uji/` | Paper tests and other tests; not part of the standard (`uji/README.md` <!-- ARCHIVE-LINK: uji/README.md -->) | `01-hitung` draft |
| `kajian/` | Study material: ecosystem, intellectual property, licensing, governance | not the standard |

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
  form is the same, whatever the format.

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
| `form/02-addresses.md` §2.5, ADDRESS-15: the provisional ‹root› `https://uniti.example` | The real domain; ecosystem study, topic C1 (`kajian/01-ekosistem.md` <!-- ARCHIVE-LINK: kajian/01-ekosistem.md -->). To be replaced once before v0.1 is stable |

### Changing the standard

Every decision that shapes the standard is recorded in `decisions/`, one
decision per file, with what was decided, the reasons, and the alternatives
that were rejected. The main documents only need to contain the outcome.

The version history of the standard is in `PERUBAHAN.md` <!-- ARCHIVE-LINK: PERUBAHAN.md -->.

### Language

The standard is written in **Indonesian** while it is being shaped. When v0.1
is locked, all of it is translated into **English** and moves to its own
directory. This Indonesian text becomes the archive
([`decisions/0055`](decisions/0055-locked-in-english.md)). The English
equivalent of every term has been included since the start in
[`01-glossary.md`](01-glossary.md).
