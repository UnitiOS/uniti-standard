# Contributing

Status: not normative; how the standard documents are written

> [Uniti Standard](README.md) › Contributing · for anyone who proposes a
> change or writes text for this repository

**To propose a change**, write a finding as described in
[`GOVERNANCE.md`](GOVERNANCE.md) §2. That page also says who decides and what
limits every change. This page says how the text itself is written, so that a
change fits the rest of the standard.

Code agents also follow [`AGENTS.md`](AGENTS.md).

## 1. The layout of a form document

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

## 2. Writing style

- Short sentences. One rule, one sentence.
- Every term is used according to [`01-glossary.md`](01-glossary.md). A new term
  is added to the glossary **before** it is used.
- Examples are always taken from **at least two different domains**, for
  example a shop and a clinic, so that no rule quietly fits only one domain.
- Part A cannot contain terms belonging to one domain. Words such as
  "customer", "item", or "patient" may appear only in examples.
- Guides use plain words and show only code copied from `conformance/`,
  `content/`, or `form/`, with a link to where it comes from.

## 3. The status of a document

| Status | Meaning |
|---|---|
| **draft** | Being written, free to change |
| **proposed** | Complete and under review |
| **locked** | A proposal that is no longer added to. Changes only for obstacles found when building the first system, each with its own decision ([`decisions/0052`](decisions/0052-quick-test-then-lock.md)) |
| **stable** | Approved. From then on it may only **grow**: new rules may be added, existing rules do not change their meaning and are not deleted |

## 4. The [provisional] mark

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

When each is planned is in [`ROADMAP.md`](ROADMAP.md) §1.

## 5. Language and the Indonesian archive

English is the only normative text
([`decisions/0055`](decisions/0055-locked-in-english.md)). The standard was
shaped in Indonesian up to v0.1. That text, with its paper tests (`uji/`),
studies (`kajian/`), and version history (`PERUBAHAN.md`), is kept as an
archive outside this repository. A note such as "(Indonesian archive,
`uji/01-hitung.md`)" points to a file in that archive. Labels in other
languages, such as `label.id`, are content and stay where they are.
