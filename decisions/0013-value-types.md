# 0013. Seven value types; money and measures as numbers with units

Date: 2026-10-17
Status: accepted

**Context**
Every value must have the same meaning for any reader. The list of value types
is form, so it must be closed, small, and not need to grow when a new domain
comes.

**Decision**
- Seven value types: **text, number, yes/no, date, instant, choice,
  reference**.
- Money, weight, length, and duration are **not** value types of their own, but
  **numbers with units**.
- A number is always **exact** (decimal). Rounding is a calculation rule.
- Text **may** carry a language code (BCP 47); a label **must** carry it.

**Alternatives**
- *Special value types for money, percent, duration, and so on.* Rejected: the
  list would keep growing every time a new measure appears, and every new type
  needs its own rules.
- *Approximate numbers (binary numbers).* Rejected: the results of money
  calculations can be slightly off, and two readers can get different numbers.
- *A language code required for all text.* Rejected: names of people and codes
  have no language.

**Consequences**
- The list of quantities and units is contained in `content/code-lists` (stage
  6).
