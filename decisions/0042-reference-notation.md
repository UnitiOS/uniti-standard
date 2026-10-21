# 0042. Reference notation: one way to write rules, examples, and cards

Date: 2026-10-19
Status: accepted

**Context**
`06-calculation-rules` and `08-proof` use the reference notation, but do not
yet detail the order of operators, how to write numbers and units, how to
write full names, and how to write examples for machines. The reference
calculator cannot be built without those details, and two implementations
could read the same text in different ways.

**Decision**
- The reference notation is detailed in `appendix/A-notation.md`. What is
  standardized remains the meaning in the form documents; other formats may
  be used if the meaning is exactly the same.
- Calculation symbols are written with mathematical symbols (`×`, `÷`, `−`,
  `≤`). Hyphens and slashes are used only in names, addresses, and units.
- Numbers use a decimal comma and thousands points. Dates use Indonesian
  month names and always state the year.
- The reading order of operators is set in one table. Comparisons do not
  chain, and `if` always uses `else`.
- Every operation has a fixed call form, so that named arguments and binders
  can be told apart without extra marks.
- Cards and rules have a full form for modules that are frozen, and a short
  form for quotations.
- Examples are written one fact per line, with a label for the fact that is
  the target.
- In Markdown files, text for machines is in code blocks tagged `uniti`.

**Alternatives**
- *ASCII symbols (`*`, `-`, `/`).* Rejected for now: `-` and `/` are already
  used in module names and addresses. ASCII equivalents for the other symbols
  become an open question.
- *YAML or JSON as the reference notation.* Rejected: hard for business
  owners to read in examples. A machine format may be added as another
  appendix.
- *ISO 8601 dates in the reference notation.* Rejected for the reference
  notation because they are less easy to read; they remain the equivalent for
  machine formats.

**Consequences**
- The reference calculator reads this notation as it is.
- The examples in `08-proof` §4 are rewritten with the year and the time
  zone.
- Seven gaps in meaning in `06` and `08` were found, and are settled in
  [`0043`](0043-additions-from-notation.md).
