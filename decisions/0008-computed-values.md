# 0008. Computed values are not facts

Date: 2026-10-17
Status: accepted

**Context**
Numbers such as a balance or an amount of stock are derived from facts. If such
a number is also recorded as a fact, there will be two truths that can
contradict each other.

**Decision**
- A computed value is not a fact and never becomes a source of truth.
- A computed value may be **stored**, for example in a derived database, to
  speed up reading, provided that:
  - from the same facts, rules, and times, the result is always the same;
  - it may be discarded and recomputed at any time;
  - every result can be traced to the facts that formed it;
  - every result states at which two times it was computed.
- The full form is written together with the calculation rules (stage 4).

**Alternatives**
- *Computed values recorded as facts.* Rejected for the reasons above.

**Consequences**
- The document `06-calculation-rules.md` contains the form of computed values.
