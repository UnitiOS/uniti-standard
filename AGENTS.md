# Working in this repository

Status: not normative; rules for code agents and other automated tools

This repository is a **standard**, not a program. Most files are text that
people and machines must read the same way. The program in `reference/` only
exists to prove the text. Read [`README.md`](README.md) first for what is
normative and what is not.

## Find things

| You need | Go to |
|---|---|
| A rule by ID, such as `FACT-3` or `CALC-38` | [`rules.md`](rules.md) gives the document and its first sentence; the full rule is in §3 of that document. Searching the repo for the ID also works |
| The meaning of a term | [`01-glossary.md`](01-glossary.md). Every term has one meaning everywhere |
| What a document settles, in short | [`guide/overview.md`](guide/overview.md) |
| How to write a rule, card, or example | [`appendix/A-notation.md`](appendix/A-notation.md), and the templates in [`content/card-templates.md`](content/card-templates.md) |
| A worked example of a feature | [`conformance/README.md`](conformance/README.md), which lists every example with its group and level |
| Why something is as it is | [`decisions/`](decisions/README.md). Search for the rule ID or the term |
| What is still open | §8 "Open questions" of each form document, and the [provisional] list in [`README.md`](README.md) |

Each form document has the same eight sections: Purpose, Definitions, Rules,
Examples, Not examples, Reasons, Outside standards, Open questions. The rules
are always in §3.

When you state what the standard requires, cite the rule ID and the document,
for example "FACT-3 (`form/01-facts.md` §3)". Do not quote a guide or
`rules.md` as the source of a requirement.

## Run things

From the repository root, with Python 3:

| Task | Command |
|---|---|
| All tests | `python -m unittest discover -s reference/tests -t reference` |
| The conformance cases only | `python -m unittest discover -s reference/tests -t reference -p test_cases.py` |
| Some case files only | Set `CASES` to file names, for example `CASES="03-rental.md"`, then the command above. Per-level lists are in [`conformance/README.md`](conformance/README.md) §2.3 |
| A report per example of one file | From `reference/`: `python -m calculator.examples ../content/calc.md ../content/code-lists.md ../conformance/03-rental.md` |
| Rebuild the rules index | From `reference/`: `python -m tools.rules_index` |

All tests must pass before and after any change you make.

## Hard rules

These protect the standard. Do not break them, even when asked to make a test
pass.

1. **Never change the expected result of an example** to make it pass. An
   example is a contract (`form/08-proof.md`). If an example fails, the rule or
   the calculator is wrong, or the example has a mistake that a person must
   confirm.
2. **Never delete an example.** An example that is no longer right is marked
   replaced, with a reason (PROOF-20, PROOF-21).
3. **Never change normative text on your own.** The normative text is `00`,
   `01`, `form/`, `appendix/`, `content/`, and the examples in `conformance/`.
   A change to it needs the owner's approval and, if it changes meaning, a new
   decision record in `decisions/`. A finding changes the form only through the
   findings gate ([`decisions/0046`](decisions/0046-findings-gate.md)).
4. **Never reuse a rule number or a decision number**, even after the rule or
   decision is revoked or replaced.
5. **Never edit `rules.md` by hand.** Change the form document, then rebuild
   the index; a test fails when the two differ.
6. **Do not add an operation or a new form** to make content fit. Ways of
   calculating are content in the calculation library (CALC-10,
   [`decisions/0045`](decisions/0045-core-operations-and-calculation-library.md)).
7. **Keep business words out of part A.** Words such as "customer" or
   "patient" appear in `form/` only inside examples.

## Writing conventions

- English only. Short sentences; one rule, one sentence. Wrap prose at about
  80 characters.
- Requirement keywords in capitals (MUST, MUST NOT, SHOULD, SHOULD NOT, MAY)
  appear only in rules (`00-principles.md` §6). Guides use plain words.
- A new term goes into `01-glossary.md` before it is used.
- Examples come from at least two different domains.
- People in examples have short, common names (Alex, Sam, Maria, …). Do not
  give them gendered pronouns: repeat the name or rephrase.
- Links are relative. A note such as "(Indonesian archive, `uji/01-hitung.md`)"
  points to the archive outside this repository; do not turn it into a link.
- Code in the reference notation goes in ```` ```uniti ```` blocks. Blocks in
  `conformance/` and `content/` are run as tests, so they must be complete and
  correct.
- In `guide/`, show only code copied from `conformance/`, `content/`, or
  `form/`, with a link to where it comes from. Do not invent new examples there.
