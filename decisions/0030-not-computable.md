# 0030. Not computable, not 0

Date: 2026-10-19
Status: accepted

**Context**
A calculation can fail: the exchange rate is not yet recorded, a division by
zero, or incomplete data. In the earlier experiment, a failure like this
often quietly became 0 or 1, so the number was wrong without being visible.

**Decision**
- Every expression produces one of three things: a **value**, **empty**, or
  **not computable**.
- Empty means there is no value. Empty may be checked with `exists(…)`. Empty
  used in a calculation becomes not computable.
- Not computable carries one **kind of reason** from a closed list, a
  description in human language, and its location.
- Not computable **spreads** to the whole expression, except in a part that
  is not calculated, such as the branch of an `if` that is not chosen.
- Not computable is never replaced by 0 or empty.
- A constraint that is not computable is treated as not met.

**Alternatives**
- *A failed result is treated as 0 or empty.* Rejected: a number that is
  wrong without being visible is more dangerous than a number that is
  missing.
- *A failure stops the whole calculation.* Rejected: one missing rate would
  stop the whole report. With not computable per result, the other results
  can still be read.
- *`exists(…)` also catches all failures.* Rejected: errors such as division
  by zero would be hidden too.

**Consequences**
- A compute example can expect not computable, with its kind of reason
  (`form/08-proof.md`).
