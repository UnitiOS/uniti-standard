# 0036. Three kinds of examples

Date: 2026-10-19
Status: accepted

**Context**
Principle P9 asks every piece of content to prove itself. What that proof
looks like must be decided, so that machines can run it and business owners
can read it.

**Decision**
- The proof is an **example**: a set of facts, plus one question or one
  action, and the result that must come out of it.
- There are three kinds, and only three: the **compute example**, the
  **accept example**, and the **reject example**.
- Every example has an address, a title, and an explanation in human
  language.
- The result is compared exactly. For not computable, what is compared is its
  kind of reason.
- A reject example passes only if the action is rejected by the named
  constraint.

**Alternatives**
- *Free test code.* Rejected: it runs on only one system, and business owners
  cannot read it.
- *Results with a tolerance.* Rejected: the numbers in this standard are
  exact.

**Consequences**
- Content has only two kinds of logic, the kind that calculates and the kind
  that rejects, and three kinds of examples are enough for both.
