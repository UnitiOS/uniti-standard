# 0006. Six fact kinds, derived from two questions

Date: 2026-10-17
Status: accepted

**Context**
A new fact can touch an old fact in many ways. A list put together from
examples ("typo", "price rises", ...) leaks easily, because there is always a
case nobody has thought of. The list must be complete and durable.

**Decision**
- The fact kinds are derived from two questions about the old fact that is
  touched: *was it true back then?* and *is there a replacement value?* These
  two questions produce exactly four kinds: **replacement**, **ending**,
  **correction**, and **retraction**.
- Added is **statement** for a fact that does not touch another fact, and
  **redaction** **[provisional]** for a value that must not be read any more
  (decision 0009).
- The fact kind is form, with a closed list. The **reason** for a change is
  content, with an open list.

**Alternatives**
- *Three kinds: change in the world, correction, retraction.* Rejected: it
  cannot express something that ends without a replacement, for example a
  membership that stops.
- *A list of kinds taken from real examples.* Rejected: it can never be
  confirmed to be complete.

**Consequences**
- Every kind other than statement names its target fact.
- The reasons for changes are provided in the vocabulary and can keep growing.
